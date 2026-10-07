"""Tiny low-poly modelling kit used to build the Casino Machine Tycoon models.

Everything is plain Python + numpy so the models can be regenerated anywhere:
  * primitives (chamfered boxes, lathes, extrusions, puffy stars, spheres...)
  * per-face colours from one shared palette texture (flat, low-poly look)
  * GLB export (one node + one mesh per named part, pivots kept as node origins)
  * a small software rasteriser for preview renders

Conventions: 1 unit = 1 stud, +Y up, the FRONT of every model faces -Z.
Angles passed to lathe/placement helpers are measured around +Y starting at
-Z (the front) and turning towards +X.
"""
import json
import math
import struct
import zlib

import numpy as np

# ---------------------------------------------------------------- palette
PALETTE = {
    # casino core
    "gold": "#FFC21A", "gold_light": "#FFE27A", "gold_dark": "#D98A0B", "gold_deep": "#A8620A",
    "purple": "#7B2FE0", "purple_deep": "#3F1690", "purple_mid": "#5A20B8", "purple_light": "#A66BFF",
    "pink": "#FF4FA8", "cyan": "#24D9F2", "red": "#E8243C", "red_dark": "#A3122A", "red_deep": "#6E0A1E",
    "white": "#FFFFFF", "offwhite": "#F3EEFF", "cream": "#FFF0D2", "cream_dark": "#F0D9AE",
    "charcoal": "#2A2A33", "charcoal_light": "#3A3A47", "black": "#14131B", "black_soft": "#22202C",
    "chrome": "#D5DDE8", "steel": "#8D99AD", "steel_dark": "#5B6578",
    # neon (emissive)
    "neon_pink": "#FF3FD2", "neon_cyan": "#3FF4FF", "neon_magenta": "#FF2BB8", "neon_purple": "#B455FF",
    "bulb": "#FFF2A6",
    # fruits
    "cherry": "#E3142F", "cherry_dark": "#A00C22", "leaf": "#3FBF3A", "leaf_dark": "#2B8A2A",
    "lemon": "#FFE53B", "lemon_dark": "#F2B705", "melon_red": "#FF4C5E", "melon_green": "#2EAA3F",
    "seed": "#1B1B1B", "screen_cream": "#FFF8E8",
    # ocean
    "aqua": "#3FD6E8", "aqua_light": "#9AF0F5", "teal": "#11A3AF", "teal_dark": "#0B6F7E",
    "ocean_deep": "#0C3E78", "ocean_mid": "#1767B0", "shell": "#FFB8C6", "shell_dark": "#F07D98",
    "coral": "#FF6F61", "coral_dark": "#E0433A", "pearl": "#F6F3FF", "pearl_shade": "#D9D3F2",
    "fish": "#FF9A1F", "fish_dark": "#E0620B", "anchor": "#24324F", "foam": "#E9FDFF", "brass": "#E3B23C",
    # cyber
    "holo": "#59E6FF", "holo_purple": "#7A5CFF", "holo_deep": "#1B1446", "holo_line": "#A8F6FF",
    "seven": "#FF2B6E", "diamond": "#8CF3FF", "diamond_dark": "#2FB8E8",
    # egypt
    "lapis": "#1F4FC4", "lapis_dark": "#13307E", "turquoise": "#2CC7B4", "sand": "#F2D39A",
    "egypt_night": "#10204F", "eye_white": "#FFF7E6",
}
COLOR_NAMES = list(PALETTE)
NEON_COLORS = {"neon_pink", "neon_cyan", "neon_magenta", "neon_purple", "bulb"}
CELL = 8          # px per palette column
TEX_H = 32


def hex_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float) / 255.0


def palette_png_bytes():
    """Palette texture: one 8px column per colour, a very subtle vertical gradient
    (lighter at the top, slightly darker at the bottom)."""
    n = len(COLOR_NAMES)
    w = 1
    while w < n * CELL:
        w *= 2
    img = np.zeros((TEX_H, w, 3), np.uint8)
    for i, name in enumerate(COLOR_NAMES):
        c = hex_rgb(PALETTE[name])
        for row in range(TEX_H):
            t = row / (TEX_H - 1)                      # 0 top .. 1 bottom
            f = 1.06 - 0.14 * t
            if name in NEON_COLORS:
                f = 1.0
            col = np.clip(c * f, 0, 1)
            img[row, i * CELL:(i + 1) * CELL] = (col * 255).round()
    raw = b"".join(b"\x00" + img[r].tobytes() for r in range(TEX_H))

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, TEX_H, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")), w


# ---------------------------------------------------------------- matrices
def T(x=0.0, y=0.0, z=0.0):
    m = np.eye(4)
    m[:3, 3] = (x, y, z)
    return m


def S(x, y=None, z=None):
    y = x if y is None else y
    z = x if z is None else z
    return np.diag([x, y, z, 1.0])


def RX(deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    m = np.eye(4)
    m[1, 1], m[1, 2], m[2, 1], m[2, 2] = c, -s, s, c
    return m


def RY(deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    m = np.eye(4)
    m[0, 0], m[0, 2], m[2, 0], m[2, 2] = c, s, -s, c
    return m


def RZ(deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    m = np.eye(4)
    m[0, 0], m[0, 1], m[1, 0], m[1, 1] = c, -s, s, c
    return m


def M(*ms):
    """Compose matrices; the right-most one is applied first."""
    r = np.eye(4)
    for m in ms:
        r = r @ m
    return r


def FACE(angle_deg):
    """Rotation that turns the front direction (-Z) towards `angle_deg` around +Y."""
    return RY(-angle_deg)


def UP_TO_FRONT():
    """Rotation mapping local +Y onto -Z (axis-of-revolution pointing at the viewer)."""
    return RX(-90)


def dirvec(angle_deg):
    a = math.radians(angle_deg)
    return np.array([math.sin(a), 0.0, -math.cos(a)])


# ---------------------------------------------------------------- polygons
def newell(p):
    n = np.zeros(3)
    for i in range(len(p)):
        a, b = p[i], p[(i + 1) % len(p)]
        n += ((a[1] - b[1]) * (a[2] + b[2]), (a[2] - b[2]) * (a[0] + b[0]), (a[0] - b[0]) * (a[1] + b[1]))
    return n


def clean(p):
    out = []
    for q in p:
        if not out or np.linalg.norm(q - out[-1]) > 1e-7:
            out.append(q)
    if len(out) > 1 and np.linalg.norm(out[0] - out[-1]) < 1e-7:
        out.pop()
    return out


class Geo:
    """A bag of coloured planar polygons (CCW seen from outside)."""

    def __init__(self):
        self.polys = []

    def add(self, pts, col, expect=None):
        if col is None:
            return self
        p = clean([np.asarray(q, float) for q in pts])
        if len(p) < 3:
            return self
        if expect is not None:
            if np.dot(newell(p), np.asarray(expect, float)) < 0:
                p = p[::-1]
        self.polys.append((np.array(p), col))
        return self

    def __iadd__(self, other):
        self.polys.extend(other.polys)
        return self

    def __add__(self, other):
        g = Geo()
        g.polys = self.polys + other.polys
        return g

    def xf(self, m):
        g = Geo()
        lin = m[:3, :3]
        flip = np.linalg.det(lin) < 0
        for p, c in self.polys:
            q = p @ lin.T + m[:3, 3]
            g.polys.append((q[::-1] if flip else q, c))
        return g

    def recolor(self, mapping):
        g = Geo()
        for p, c in self.polys:
            g.polys.append((p, mapping.get(c, c) if isinstance(mapping, dict) else mapping))
        return g


def merge(*geos):
    g = Geo()
    for x in geos:
        g += x
    return g


# ---------------------------------------------------------------- primitives
_FACES = {"-x": (0, -1), "+x": (0, 1), "-y": (1, -1), "+y": (1, 1), "-z": (2, -1), "+z": (2, 1)}


def box(lo, hi, col, bevel=0.0, skip=(), top=None, front=None):
    """Axis-aligned box from corner `lo` to `hi`, optional chamfer `bevel`.
    `skip` lists faces to omit (hidden against other geometry)."""
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    c = (lo + hi) / 2
    h = (hi - lo) / 2
    g = Geo()
    facecol = {"+y": top or col, "-z": front or col}
    if bevel <= 0:
        for name, (ax, s) in _FACES.items():
            if name in skip:
                continue
            pts = []
            o = [a for a in range(3) if a != ax]
            for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                q = c.copy()
                q[ax] += s * h[ax]
                q[o[0]] += u * h[o[0]]
                q[o[1]] += v * h[o[1]]
                pts.append(q)
            n = np.zeros(3)
            n[ax] = s
            g.add(pts, facecol.get(name, col), n)
        return g
    b = min(bevel, *(h * 0.95))

    def P(sg, ax):
        q = c + sg * (h - b)
        q[ax] = c[ax] + sg[ax] * h[ax]
        return q
    corners = [np.array((sx, sy, sz), float) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    for name, (ax, s) in _FACES.items():
        if name in skip:
            continue
        pts = [P(k, ax) for k in corners if k[ax] == s]
        cen = np.mean(pts, axis=0)
        o = [a for a in range(3) if a != ax]
        pts.sort(key=lambda q: math.atan2(q[o[1]] - cen[o[1]], q[o[0]] - cen[o[0]]))
        n = np.zeros(3)
        n[ax] = s
        g.add(pts, facecol.get(name, col), n)
    for a1 in range(3):
        for a2 in range(a1 + 1, 3):
            a3 = 3 - a1 - a2
            for s1 in (-1, 1):
                for s2 in (-1, 1):
                    pts = []
                    for s3 in (-1, 1):
                        k = np.zeros(3)
                        k[a1], k[a2], k[a3] = s1, s2, s3
                        pts.append(P(k, a1))
                    for s3 in (1, -1):
                        k = np.zeros(3)
                        k[a1], k[a2], k[a3] = s1, s2, s3
                        pts.append(P(k, a2))
                    n = np.zeros(3)
                    n[a1], n[a2] = s1, s2
                    ecol = top if (top and a2 == 1 and s2 == 1) or (top and a1 == 1 and s1 == 1) else col
                    g.add(pts, ecol, n)
    for k in corners:
        g.add([P(k, 0), P(k, 1), P(k, 2)], top if (top and k[1] > 0) else col, k)
    return g


def lathe(profile, seg, col, a0=0.0, a1=360.0, phase=0.5, caps=False, rmod=None):
    """Surface of revolution around +Y.  `profile` is a list of (r, y) points
    ordered so that the outside is on the right (bottom-to-top on an outer wall,
    CCW for a closed outline).  `col` is a colour or f(seg_index, edge_index)->colour
    (None skips that face).  Angles in degrees from -Z towards +X."""
    full = abs(a1 - a0 - 360.0) < 1e-9
    if full:
        angs = [a0 + (k + phase) * 360.0 / seg for k in range(seg + 1)]
    else:
        angs = list(np.linspace(a0, a1, seg + 1))
    cf = col if callable(col) else (lambda i, j: col)
    rm = rmod or (lambda i: 1.0)
    g = Geo()

    def pt(r, y, k):
        a = math.radians(angs[k])
        rr = r * (rm(k % seg) if full else rm(k))
        return np.array((rr * math.sin(a), y, -rr * math.cos(a)))
    for j in range(len(profile) - 1):
        (r0, y0), (r1, y1) = profile[j], profile[j + 1]
        nr, ny = (y1 - y0), -(r1 - r0)
        for i in range(seg):
            cc = cf(i, j)
            if cc is None:
                continue
            am = math.radians((angs[i] + angs[i + 1]) / 2)
            exp = (nr * math.sin(am), ny, -nr * math.cos(am))
            g.add([pt(r0, y0, i), pt(r0, y0, i + 1), pt(r1, y1, i + 1), pt(r1, y1, i)], cc, exp)
    if caps and not full:
        for k, sgn in ((0, -1), (seg, 1)):
            a = math.radians(angs[k])
            tdir = np.array((math.cos(a), 0, math.sin(a))) * sgn
            g.add([pt(r, y, k) for r, y in profile], cf(0, 0) if k == 0 else cf(seg - 1, 0), tdir)
    return g


def cyl(r, y0, y1, seg, col, top=True, bottom=False, topcol=None, phase=0.5):
    prof = []
    if bottom:
        prof.append((0, y0))
    prof += [(r, y0), (r, y1)]
    if top:
        prof.append((0, y1))
    tc = topcol or col

    def cf(i, j):
        if top and j == len(prof) - 2:
            return tc
        return col
    return lathe(prof, seg, cf, phase=phase)


def sphere(r, seg=8, rings=4, col="white", rmod=None):
    prof = [(r * math.sin(math.pi * k / rings), -r * math.cos(math.pi * k / rings)) for k in range(rings + 1)]
    prof[0] = (0.0, -r)
    prof[-1] = (0.0, r)
    return lathe(prof, seg, col, rmod=rmod)


def dome(r, seg=6, rings=2, col="bulb"):
    """Half sphere sitting on y=0 (open bottom)."""
    prof = [(r * math.cos(math.pi / 2 * k / rings), r * math.sin(math.pi / 2 * k / rings)) for k in range(rings + 1)]
    prof[-1] = (0.0, r)
    return lathe(prof, seg, col)


def signed_area(p2):
    return 0.5 * sum(p2[i][0] * p2[(i + 1) % len(p2)][1] - p2[(i + 1) % len(p2)][0] * p2[i][1] for i in range(len(p2)))


def extrude(poly2d, z0, z1, col, side=None, front=True, back=True, sidecols=None):
    """Prism of an XY polygon between z0 (front, facing -Z) and z1 (back)."""
    p = [tuple(map(float, q)) for q in poly2d]
    if signed_area(p) < 0:
        p = p[::-1]
    g = Geo()
    if front:
        g.add([(x, y, z0) for x, y in p], col, (0, 0, -1))
    if back:
        g.add([(x, y, z1) for x, y in p], col, (0, 0, 1))
    sc = side or col
    for i in range(len(p)):
        (xa, ya), (xb, yb) = p[i], p[(i + 1) % len(p)]
        c = sidecols(i) if sidecols else sc
        g.add([(xa, ya, z0), (xb, yb, z0), (xb, yb, z1), (xa, ya, z1)], c, (yb - ya, -(xb - xa), 0))
    return g


def circle2(cx, cy, r, n=10, start=90.0, sx=1.0, sy=1.0):
    return [(cx + sx * r * math.cos(math.radians(start + 360.0 * k / n)),
             cy + sy * r * math.sin(math.radians(start + 360.0 * k / n))) for k in range(n)]


def star2(cx, cy, ro, ri, n=5, start=90.0):
    pts = []
    for k in range(2 * n):
        r = ro if k % 2 == 0 else ri
        a = math.radians(start + 180.0 * k / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def ring2_geo(cx, cy, r_in, r_out, n, z0, z1, col):
    """Flat ring (annulus) extruded between z0 (front) and z1."""
    g = Geo()
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        quad = [(cx + r_out * math.cos(a0), cy + r_out * math.sin(a0)), (cx + r_out * math.cos(a1), cy + r_out * math.sin(a1)),
                (cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)), (cx + r_in * math.cos(a0), cy + r_in * math.sin(a0))]
        g.add([(x, y, z0) for x, y in quad], col, (0, 0, -1))
        g.add([(quad[0][0], quad[0][1], z0), (quad[1][0], quad[1][1], z0),
               (quad[1][0], quad[1][1], z1), (quad[0][0], quad[0][1], z1)],
              col, (math.cos((a0 + a1) / 2), math.sin((a0 + a1) / 2), 0))
        g.add([(quad[3][0], quad[3][1], z0), (quad[2][0], quad[2][1], z0),
               (quad[2][0], quad[2][1], z1), (quad[3][0], quad[3][1], z1)],
              col, (-math.cos((a0 + a1) / 2), -math.sin((a0 + a1) / 2), 0))
    return g


def puffy(poly2d, thick, bulge, col, side=None, back=True, center=None):
    """Chunky 'pillow' shape: extruded outline whose faces rise to a centre point."""
    p = [tuple(map(float, q)) for q in poly2d]
    if signed_area(p) < 0:
        p = p[::-1]
    cx, cy = center if center else (sum(q[0] for q in p) / len(p), sum(q[1] for q in p) / len(p))
    h = thick / 2
    g = Geo()
    sc = side or col
    for i in range(len(p)):
        (xa, ya), (xb, yb) = p[i], p[(i + 1) % len(p)]
        g.add([(xa, ya, -h), (xb, yb, -h), (xb, yb, h), (xa, ya, h)], sc, (yb - ya, -(xb - xa), 0))
        g.add([(xa, ya, -h), (cx, cy, -h - bulge), (xb, yb, -h)], col, (0, 0, -1))
        if back:
            g.add([(xa, ya, h), (xb, yb, h), (cx, cy, h + bulge)], col, (0, 0, 1))
    return g


def puffy_star(r_out, r_in, thick, bulge, col, side=None, n=5, back=True):
    return puffy(star2(0, 0, r_out, r_in, n), thick, bulge, col, side, back, center=(0, 0))


def coin(r, t, col="gold", face="gold_light", emblem=True, back=False, seg=14):
    """Coin lying in the XY plane, front face at z=-t (facing -Z), back at z=0."""
    prof = [(r, 0.0), (r, t * 0.75), (r * 0.88, t), (r * 0.72, t), (r * 0.69, t * 0.82), (0.0, t * 0.82)]

    def cf(i, j):
        return face if j >= 4 else col
    g = lathe(prof, seg, cf)
    if emblem:
        g += puffy_star(r * 0.48, r * 0.2, t * 0.3, t * 0.25, col, back=False).xf(M(T(0, t * 0.97, 0), RX(90)))
    if back:
        g += Geo().add([(r * math.sin(2 * math.pi * k / seg), 0, -r * math.cos(2 * math.pi * k / seg)) for k in range(seg)], col, (0, -1, 0))
    return g.xf(UP_TO_FRONT())


def pyramid(r, h, n, col, phase=0.5):
    return lathe([(r, 0.0), (0.0, h)], n, col, phase=phase)


def frustum_box(lo_w, lo_d, hi_w, hi_d, y0, y1, col, skip=(), top=None, zc=0.0, xc=0.0):
    """Tapered box (temple / pylon shapes)."""
    def ring(w, d, y):
        return [np.array((xc + sx * w / 2, y, zc + sz * d / 2)) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    b, t = ring(lo_w, lo_d, y0), ring(hi_w, hi_d, y1)
    g = Geo()
    names = ["-z", "+x", "+z", "-x"]
    cen = np.array((xc, (y0 + y1) / 2, zc))
    for i in range(4):
        if names[i] in skip:
            continue
        quad = [b[i], b[(i + 1) % 4], t[(i + 1) % 4], t[i]]
        qc = np.mean(quad, axis=0)
        g.add(quad, col, (qc[0] - cen[0], 0, qc[2] - cen[2]))
    if "+y" not in skip:
        g.add(t, top or col, (0, 1, 0))
    if "-y" not in skip:
        g.add(b, col, (0, -1, 0))
    return g


# ---------------------------------------------------------------- triangulation
def _tri_poly(p):
    n = len(p)
    if n == 3:
        return [(0, 1, 2)]
    nrm = newell(p)
    ax = int(np.argmax(np.abs(nrm)))
    o = [(ax + 1) % 3, (ax + 2) % 3]
    q = p[:, o]
    if nrm[ax] < 0:
        q = q[:, ::-1]
    # convex fast path
    convex = True
    for i in range(n):
        a, b, c = q[i], q[(i + 1) % n], q[(i + 2) % n]
        if (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) < -1e-9:
            convex = False
            break
    if convex:
        return [(0, i, i + 1) for i in range(1, n - 1)]
    idx = list(range(n))
    tris = []

    def cross(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    guard = 0
    while len(idx) > 3 and guard < 10000:
        guard += 1
        found = False
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]
            a, b, c = q[i0], q[i1], q[i2]
            if cross(a, b, c) <= 1e-12:
                continue
            ok = True
            for j in idx:
                if j in (i0, i1, i2):
                    continue
                pp = q[j]
                if cross(a, b, pp) >= -1e-12 and cross(b, c, pp) >= -1e-12 and cross(c, a, pp) >= -1e-12:
                    ok = False
                    break
            if ok:
                tris.append((i0, i1, i2))
                idx.pop(k)
                found = True
                break
        if not found:
            break
    if len(idx) == 3:
        tris.append(tuple(idx))
    return tris


# ---------------------------------------------------------------- parts & models
class Part:
    def __init__(self, name, pivot=(0, 0, 0), neon=False, gradient=True, smooth=False):
        self.name = name
        self.smooth = smooth
        self.pivot = np.asarray(pivot, float)
        self.neon = neon
        self.gradient = gradient
        self.geo = Geo()

    def add(self, g, m=None):
        self.geo += g.xf(m) if m is not None else g
        return self

    def triangles(self):
        tris, cols = [], []
        for p, c in self.geo.polys:
            for a, b, d in _tri_poly(p):
                tri = np.array((p[a], p[b], p[d]))
                if np.linalg.norm(np.cross(tri[1] - tri[0], tri[2] - tri[0])) < 1e-10:
                    continue
                tris.append(tri)
                cols.append(c)
        return np.array(tris).reshape(-1, 3, 3), cols

    def colors_used(self):
        return sorted({c for _, c in self.geo.polys})


class Model:
    def __init__(self, name):
        self.name = name
        self.parts = []

    def part(self, name, **kw):
        p = Part(name, **kw)
        self.parts.append(p)
        return p

    def mirror_x(self):
        """Mirror left/right. Front art is authored as seen from +Z; seen from the
        front (-Z) the viewer's right is -X, so front-facing models are mirrored once."""
        for p in self.parts:
            p.geo = p.geo.xf(S(-1, 1, 1))
            p.pivot = p.pivot * np.array((-1.0, 1.0, 1.0)) + 0.0
        return self

    def __getitem__(self, name):
        return next(p for p in self.parts if p.name == name)


def smooth_normals(pos, nrm, max_angle=50.0):
    """Average normals of coincident vertices whose faces differ by < max_angle."""
    key = [tuple(np.round(p, 4)) for p in pos]
    groups = {}
    for i, k in enumerate(key):
        groups.setdefault(k, []).append(i)
    out = nrm.copy()
    lim = math.cos(math.radians(max_angle))
    for idx in groups.values():
        if len(idx) < 2:
            continue
        ns = nrm[idx]
        for a, i in enumerate(idx):
            sel = ns @ ns[a] > lim
            v = ns[sel].sum(axis=0)
            out[i] = v / (np.linalg.norm(v) + 1e-12)
    return out


# ---------------------------------------------------------------- GLB export
def export_glb(model, path):
    png, tex_w = palette_png_bytes()
    bin_chunks = []
    offset = 0
    buffer_views, accessors, meshes, nodes, materials = [], [], [], [], []

    def push(data, target=None):
        nonlocal offset
        pad = (-len(data)) % 4
        bv = {"buffer": 0, "byteOffset": offset, "byteLength": len(data)}
        if target:
            bv["target"] = target
        buffer_views.append(bv)
        bin_chunks.append(data + b"\x00" * pad)
        offset += len(data) + pad
        return len(buffer_views) - 1

    img_bv = push(png)
    materials_by_key = {}

    def material(key, solid_color, neon):
        if key in materials_by_key:
            return materials_by_key[key]
        mat = {"name": key, "pbrMetallicRoughness": {"metallicFactor": 0.0, "roughnessFactor": 0.55}}
        if solid_color is None:
            mat["pbrMetallicRoughness"]["baseColorTexture"] = {"index": 0}
            if neon:
                mat["emissiveTexture"] = {"index": 0}
                mat["emissiveFactor"] = [1.0, 1.0, 1.0]
        else:
            rgb = hex_rgb(PALETTE[solid_color])
            lin = [float(((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92) for c in rgb]
            mat["pbrMetallicRoughness"]["baseColorFactor"] = lin + [1.0]
            if neon:
                mat["emissiveFactor"] = lin
        materials.append(mat)
        materials_by_key[key] = len(materials) - 1
        return materials_by_key[key]

    stats = {}
    for part in model.parts:
        tris, cols = part.triangles()
        n = len(tris)
        stats[part.name] = n
        pos = (tris - part.pivot).reshape(-1, 3).astype(np.float32)
        nrm = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
        nrm /= np.linalg.norm(nrm, axis=1, keepdims=True)
        nrm = np.repeat(nrm, 3, axis=0)
        if part.smooth:
            nrm = smooth_normals(tris.reshape(-1, 3), nrm)
        nrm = nrm.astype(np.float32)
        ys = tris[:, :, 1]
        ymin, ymax = ys.min(), ys.max()
        uv = np.zeros((n * 3, 2), np.float32)
        for i, c in enumerate(cols):
            u = (COLOR_NAMES.index(c) * CELL + CELL / 2) / tex_w
            for k in range(3):
                if part.gradient and not part.neon and ymax - ymin > 1e-6:
                    t = (tris[i, k, 1] - ymin) / (ymax - ymin)
                    v = 0.08 + 0.84 * (1 - t)
                else:
                    v = 0.5
                uv[i * 3 + k] = (u, v)
        used = set(cols)
        solid = next(iter(used)) if len(used) == 1 else None
        if solid is not None:
            key = ("Neon_" if part.neon else "") + "".join(w.capitalize() for w in solid.split("_"))
        else:
            key = "CasinoPaletteNeon" if part.neon else "CasinoPalette"
        mat = material(key, solid, part.neon)
        idx = np.arange(n * 3, dtype=np.uint32)
        a_pos = len(accessors)
        accessors.append({"bufferView": push(pos.tobytes(), 34962), "componentType": 5126, "count": n * 3, "type": "VEC3",
                          "min": pos.min(axis=0).tolist(), "max": pos.max(axis=0).tolist()})
        accessors.append({"bufferView": push(nrm.tobytes(), 34962), "componentType": 5126, "count": n * 3, "type": "VEC3"})
        accessors.append({"bufferView": push(uv.tobytes(), 34962), "componentType": 5126, "count": n * 3, "type": "VEC2"})
        accessors.append({"bufferView": push(idx.tobytes(), 34963), "componentType": 5125, "count": n * 3, "type": "SCALAR"})
        meshes.append({"name": part.name, "primitives": [{"attributes": {"POSITION": a_pos, "NORMAL": a_pos + 1, "TEXCOORD_0": a_pos + 2},
                                                          "indices": a_pos + 3, "material": mat}]})
        nodes.append({"name": part.name, "mesh": len(meshes) - 1, "translation": part.pivot.tolist()})
    root = {"name": model.name, "children": list(range(len(nodes)))}
    nodes.append(root)
    gltf = {
        "asset": {"version": "2.0", "generator": "casino_geo.py (Casino Machine Tycoon)"},
        "scene": 0, "scenes": [{"name": model.name, "nodes": [len(nodes) - 1]}],
        "nodes": nodes, "meshes": meshes, "materials": materials, "accessors": accessors, "bufferViews": buffer_views,
        "buffers": [{"byteLength": offset}],
        "images": [{"name": "CasinoPalette", "bufferView": img_bv, "mimeType": "image/png"}],
        "samplers": [{"magFilter": 9728, "minFilter": 9728, "wrapS": 33071, "wrapT": 33071}],
        "textures": [{"source": 0, "sampler": 0, "name": "CasinoPalette"}],
        "extras": {"units": "1 unit = 1 Roblox stud", "front": "-Z"},
    }
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * ((-len(js)) % 4)
    binary = b"".join(bin_chunks)
    total = 12 + 8 + len(js) + 8 + len(binary)
    with open(path, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, total))
        f.write(struct.pack("<II", len(js), 0x4E4F534A) + js)
        f.write(struct.pack("<II", len(binary), 0x004E4942) + binary)
    return stats


# ---------------------------------------------------------------- preview renderer
def render(models_with_xf, path, size=(1000, 800), eye=(-1, 0.55, -1.25), target=None, fov=32.0, fit=1.0,
           bg=None, ss=2, outline=True, dist_scale=1.0):
    """Rasterise one or more (Model, matrix) pairs to a PNG with flat shading."""
    from PIL import Image
    tris_all, col_all, neon_all, pid_all = [], [], [], []
    pid = 0
    for model, mx in models_with_xf:
        for part in model.parts:
            tris, cols = part.triangles()
            if len(tris) == 0:
                continue
            if mx is not None:
                tris = tris @ mx[:3, :3].T + mx[:3, 3]
            ys = tris[:, :, 1].mean(axis=1)
            ymin, ymax = tris[:, :, 1].min(), tris[:, :, 1].max()
            t = (ys - ymin) / max(ymax - ymin, 1e-6)
            for i, c in enumerate(cols):
                base = hex_rgb(PALETTE[c])
                if not part.neon and part.gradient:
                    base = base * (0.92 + 0.14 * t[i])
                col_all.append(base)
                neon_all.append(part.neon or c in NEON_COLORS)
            tris_all.append(tris)
            pid_all += [pid] * len(tris)
            pid += 1
    tris = np.concatenate(tris_all)
    cols = np.clip(np.array(col_all), 0, 1)
    neon = np.array(neon_all)
    pids = np.array(pid_all)
    pts = tris.reshape(-1, 3)
    lo, hi = pts.min(axis=0), pts.max(axis=0)
    tgt = np.asarray(target, float) if target is not None else (lo + hi) / 2
    radius = np.linalg.norm(hi - lo) / 2
    fwd = -np.asarray(eye, float)
    fwd /= np.linalg.norm(fwd)
    dist = radius / math.sin(math.radians(fov / 2)) * fit * dist_scale
    cam = tgt - fwd * dist
    right = np.cross(fwd, (0, 1, 0))
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    W, H = size[0] * ss, size[1] * ss
    f = (H / 2) / math.tan(math.radians(fov / 2))
    rel = tris - cam
    xc = rel @ right
    yc = rel @ up
    zc = rel @ fwd
    sx = W / 2 + f * xc / zc
    sy = H / 2 - f * yc / zc
    nrm = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12
    L1 = np.array((-0.45, 0.8, -0.55))
    L1 /= np.linalg.norm(L1)
    L2 = np.array((0.7, 0.3, 0.2))
    L2 /= np.linalg.norm(L2)
    shade = 0.58 + 0.42 * np.clip(nrm @ L1, 0, 1) + 0.12 * np.clip(nrm @ L2, 0, 1) + 0.06 * np.clip(nrm[:, 1], 0, 1)
    shaded = np.where(neon[:, None], np.clip(cols * 1.12 + 0.05, 0, 1), np.clip(cols * shade[:, None], 0, 1))
    img = np.zeros((H, W, 3))
    depth = np.full((H, W), np.inf)
    ids = np.full((H, W), -1, np.int64)
    for i in range(len(tris)):
        if np.any(zc[i] <= 0.01):
            continue
        x0, x1 = int(max(0, math.floor(sx[i].min()))), int(min(W - 1, math.ceil(sx[i].max())))
        y0, y1 = int(max(0, math.floor(sy[i].min()))), int(min(H - 1, math.ceil(sy[i].max())))
        if x1 < x0 or y1 < y0:
            continue
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        (xa, xb, xcc), (ya, yb, ycc) = sx[i], sy[i]
        den = (yb - ycc) * (xa - xcc) + (xcc - xb) * (ya - ycc)
        if abs(den) < 1e-12:
            continue
        w0 = ((yb - ycc) * (X - xcc) + (xcc - xb) * (Y - ycc)) / den
        w1 = ((ycc - ya) * (X - xcc) + (xa - xcc) * (Y - ycc)) / den
        w2 = 1 - w0 - w1
        inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
        if not inside.any():
            continue
        iz = w0 / zc[i][0] + w1 / zc[i][1] + w2 / zc[i][2]
        z = 1 / iz
        sub = depth[y0:y1 + 1, x0:x1 + 1]
        m = inside & (z < sub)
        sub[m] = z[m]
        img[y0:y1 + 1, x0:x1 + 1][m] = shaded[i]
        ids[y0:y1 + 1, x0:x1 + 1][m] = pids[i]
    alpha = np.isfinite(depth).astype(float)
    if outline:
        d = np.where(np.isfinite(depth), depth, 1e9)
        edge = np.zeros_like(alpha, bool)
        for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
            d2 = np.roll(np.roll(d, dy, 0), dx, 1)
            i2 = np.roll(np.roll(ids, dy, 0), dx, 1)
            rel_jump = np.abs(d - d2) / np.minimum(d, d2) > 0.012 * ss
            edge |= rel_jump & ((d < 1e8) | (d2 < 1e8))
            edge |= (ids != i2) & (ids >= 0) & (i2 >= 0)
        img[edge] = img[edge] * 0.35 + np.array((0.08, 0.04, 0.16)) * 0.65
        alpha[edge] = 1.0
    if bg is not None:
        bgc = hex_rgb(bg)
        img = img * alpha[..., None] + bgc * (1 - alpha[..., None])
        out = (np.clip(img, 0, 1) * 255).astype(np.uint8)
        im = Image.fromarray(out, "RGB")
    else:
        out = np.dstack([np.clip(img, 0, 1), alpha])
        im = Image.fromarray((out * 255).astype(np.uint8), "RGBA")
    im = im.resize(size, Image.LANCZOS)
    im.save(path)
    return len(tris)
