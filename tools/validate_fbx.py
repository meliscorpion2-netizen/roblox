"""Minimal binary-FBX reader: checks part names, units, up axis, pivots and overall size of models/fbx/*.fbx."""
import os
import struct
import zlib

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARR = {b"f": ("<f", 4), b"d": ("<d", 8), b"l": ("<q", 8), b"i": ("<i", 4), b"b": ("<?", 1)}


def read_node(d, o, v64):
    if v64:
        end, nprop, plen = struct.unpack_from("<QQQ", d, o)
        o += 24
    else:
        end, nprop, plen = struct.unpack_from("<III", d, o)
        o += 12
    nl = d[o]
    name = d[o + 1:o + 1 + nl].decode()
    o += 1 + nl
    if end == 0:
        return None, o
    props = []
    for _ in range(nprop):
        t = d[o:o + 1]
        o += 1
        if t in b"YCIFDL":
            fmt = {b"Y": "<h", b"C": "<?", b"I": "<i", b"F": "<f", b"D": "<d", b"L": "<q"}[t]
            props.append(struct.unpack_from(fmt, d, o)[0])
            o += struct.calcsize(fmt)
        elif t in b"SR":
            n = struct.unpack_from("<I", d, o)[0]
            raw = d[o + 4:o + 4 + n]
            props.append(raw.decode("utf-8", "replace") if t == b"S" else raw)
            o += 4 + n
        else:
            n, enc, clen = struct.unpack_from("<III", d, o)
            raw = d[o + 12:o + 12 + clen]
            if enc:
                raw = zlib.decompress(raw)
            fmt, sz = ARR[t]
            props.append(np.frombuffer(raw, fmt[1:]).astype(float) if t != b"b" else raw)
            o += 12 + clen
    kids = []
    while o < end:
        k, o = read_node(d, o, v64)
        if k is None:
            break
        kids.append(k)
    return (name, props, kids), end


def load(path):
    d = open(path, "rb").read()
    assert d.startswith(b"Kaydara FBX Binary"), "not binary FBX"
    ver = struct.unpack_from("<I", d, 23)[0]
    o, top = 27, []
    while True:
        n, o = read_node(d, o, ver >= 7500)
        if n is None:
            break
        top.append(n)
    return ver, top


def find(nodes, name):
    return [n for n in nodes if n[0] == name]


def prop70(node, key):
    for p70 in find(node[2], "Properties70"):
        for p in p70[2]:
            if p[1][0] == key:
                return p[1][4:]
    return None


for fn in sorted(os.listdir(os.path.join(ROOT, "models", "fbx"))):
    if not fn.endswith(".fbx"):
        continue
    ver, top = load(os.path.join(ROOT, "models", "fbx", fn))
    gs = find(top, "GlobalSettings")[0]
    objs = find(top, "Objects")[0][2]
    geos = {g[1][0]: g for g in find(objs, "Geometry")}
    models = {mm[1][0]: mm for mm in find(objs, "Model")}
    conns = [c[1] for c in find(find(top, "Connections")[0][2], "C")]
    pts_all, parts = [], []
    root = None
    for uid, mm in models.items():
        nm = mm[1][1].split("\x00")[0]
        t = prop70(mm, "Lcl Translation") or [0, 0, 0]
        if mm[1][2] != "Null" and (prop70(mm, "Lcl Rotation") or prop70(mm, "PreRotation") or prop70(mm, "Lcl Scaling")):
            nm += f"(rot={prop70(mm, 'Lcl Rotation')},pre={prop70(mm, 'PreRotation')},scl={prop70(mm, 'Lcl Scaling')})"
        if mm[1][2] == "Null":
            root = nm + f" rot={prop70(mm, 'Lcl Rotation')} scl={prop70(mm, 'Lcl Scaling')} prerot={prop70(mm, 'PreRotation')}"
            continue
        gid = next(c[1] for c in conns if c[0] == "OO" and c[2] == uid and c[1] in geos)
        v = find(geos[gid][2], "Vertices")[0][1][0].reshape(-1, 3)
        pts_all.append(v + np.array(t))
        parts.append((nm, np.round(t, 2).tolist()))
    P = np.concatenate(pts_all)
    vids = [o for o in find(objs, "Video")]
    emb = any(find(vv[2], "Content") and len(find(vv[2], "Content")[0][1][0]) > 0 for vv in vids)
    print(f"{fn}: FBX {ver}  UnitScale {prop70(gs, 'UnitScaleFactor')}  UpAxis {prop70(gs, 'UpAxis')}  "
          f"Front {prop70(gs, 'FrontAxis')}{prop70(gs, 'FrontAxisSign')}  root '{root}'  texture embedded: {emb}")
    print(f"   size {np.round(P.max(0) - P.min(0), 2)}  min {np.round(P.min(0), 2)}  max {np.round(P.max(0), 2)}")
    print("   parts:", ", ".join(f"{n}@{t}" for n, t in sorted(parts)))
