"""Bibliothèque de modélisation procédurale low-poly pour les props Roblox.

Convention de travail (dans Blender) :
  - unités = studs pendant la construction, converties en mètres (1 stud = 0,28 m) à l'export ;
  - X = largeur, Y = profondeur, Z = hauteur ; la face avant regarde -Y
    (à l'export FBX « -Z forward / Y up », -Y devient la face avant Roblox) ;
  - pivot au centre de la base (0, 0, 0).

Les dimensions du cahier des charges sont données en Roblox « X × Y × Z »
= largeur × hauteur × profondeur. Model(dims=(X, Y, Z)) recale automatiquement la
boîte englobante exacte à la fin de la construction.
"""
import math
import os
import random

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

STUD_M = 0.28

# ---------------------------------------------------------------------------
# Palette : une seule texture 512×256, 16×8 cases de 32 px.
# Chaque case est un léger dégradé vertical (bas plus sale/sombre) ; les UV d'une
# face pointent au centre horizontal de sa case, et la coordonnée verticale suit
# la hauteur dans l'objet → crasse automatique près du sol, sans texture photo.
# ---------------------------------------------------------------------------
PALETTE = [
    # 0 métaux
    ("metal_light", "#a3a9ab"), ("metal", "#737b80"), ("metal_dark", "#474d51"), ("steel_blue", "#5d7387"),
    ("chrome", "#cdd5d9"), ("iron", "#2c2e30"), ("brass", "#c9a24a"), ("copper", "#b5653a"),
    ("gold", "#e0b43c"), ("galva", "#8f9a92"), ("alu", "#b9bec0"), ("inox", "#c2c8cb"),
    ("gunmetal", "#3a4047"), ("lamp_grey", "#5f6466"), ("pole_green", "#3d5a45"), ("navy_paint", "#2d3f5c"),
    # 1 rouille / peintures
    ("rust", "#9c4f26"), ("rust_dark", "#6b3518"), ("rust_orange", "#c06a2c"), ("red", "#c2382f"),
    ("red_dark", "#8e2620"), ("maroon", "#6a2329"), ("orange", "#e07a2a"), ("yellow", "#e8b923"),
    ("yellow_dark", "#b88d1c"), ("green", "#4f8f3a"), ("green_dark", "#2f5e2c"), ("olive", "#7a7f3a"),
    ("teal", "#2f8c88"), ("blue", "#2f6fb0"), ("blue_dark", "#224b78"), ("purple", "#7b4fa0"),
    # 2 neutres
    ("pink", "#e07fa3"), ("cream", "#e8dcc0"), ("white", "#e2dfd6"), ("beige", "#c8b48a"),
    ("grey_light", "#b4b1a8"), ("grey", "#8a8780"), ("grey_dark", "#55534f"), ("black", "#232323"),
    ("sky", "#7fb6d9"), ("mint", "#8fd1b0"), ("lilac", "#b39bd6"), ("peach", "#f0a878"),
    ("sand", "#d8c08a"), ("khaki", "#8c8250"), ("jute", "#b49a64"), ("tarp_blue", "#2d6fa8"),
    # 3 bois / papier
    ("wood_light", "#c08a52"), ("wood", "#9a6534"), ("wood_dark", "#6a4122"), ("wood_old", "#8a7660"),
    ("cardboard", "#b98c55"), ("cardboard_dark", "#8e6a3e"), ("paper", "#e6e0cf"), ("paper_dirty", "#c9c0a6"),
    ("wood_red", "#7a3524"), ("wood_black", "#3a2a20"), ("pallet", "#c7a575"), ("crate", "#d0a868"),
    ("felt", "#2e7d4a"), ("velvet", "#9e2b3a"), ("leather", "#7a2a22"), ("cork", "#b8875a"),
    # 4 minéraux / caoutchouc
    ("concrete", "#a7a39a"), ("concrete_dark", "#7e7a72"), ("brick", "#b0533a"), ("brick_dark", "#8a3d2a"),
    ("asphalt", "#3a3a3c"), ("rubber", "#262626"), ("plastic_black", "#1c1d1f"), ("bag_black", "#2b2e33"),
    ("bag_shine", "#4a5059"), ("tile_white", "#dcdcd4"), ("slate", "#2f3437"), ("marble", "#d8d4cc"),
    ("mud", "#6e5a3e"), ("soot", "#1a1817"), ("char", "#2a2420"), ("ash", "#6d6862"),
    # 5 lumières / verre (cases unies, sans dégradé)
    ("glass", "#9fd3e6"), ("glass_dark", "#5e8fa3"), ("light_warm", "#ffd36b"), ("light_white", "#f4f7ff"),
    ("light_red", "#ff3b30"), ("light_amber", "#ffaa1f"), ("light_green", "#3be06a"), ("screen", "#5fd0ff"),
    ("flame_yellow", "#ffcf3a"), ("flame_orange", "#ff7a1a"), ("flame_red", "#e8381a"), ("ember", "#ff4a1f"),
    ("neon_pink", "#ff4fa8"), ("neon_blue", "#3fb8ff"), ("mirror", "#c6dbe3"), ("screen_dark", "#20313a"),
    # 6 tissus / animaux
    ("fabric_red", "#a8323a"), ("fabric_blue", "#3e5e8e"), ("fabric_green", "#4f7a52"), ("fabric_yellow", "#d6a83a"),
    ("fabric_brown", "#7a5a3e"), ("fabric_grey", "#7b7d80"), ("mattress", "#d8cfb4"), ("stain", "#9a8457"),
    ("pigeon", "#7d8590"), ("pigeon_dark", "#4f565f"), ("pigeon_neck", "#4f7f74"), ("beak", "#d9a07a"),
    ("rat", "#6b5a4e"), ("rat_pink", "#e3a3a0"), ("eye", "#111111"), ("eye_white", "#f2f2f2"),
    # 7 végétal / nourriture
    ("leaf", "#4f9a3a"), ("leaf_dark", "#2f6e2a"), ("flower_red", "#e0424a"), ("flower_pink", "#f08cc0"),
    ("flower_yellow", "#f5d23a"), ("flower_white", "#f5f2ea"), ("flower_purple", "#9a5ad0"), ("soil", "#4a3426"),
    ("croissant", "#d99a45"), ("bread", "#c78640"), ("tomato", "#e0453a"), ("lettuce", "#8cc84b"),
    ("onion", "#efe2d0"), ("sauce", "#f2efe0"), ("meat", "#9c5a35"), ("meat_dark", "#6e3a20"),
]
PAL_COLS, PAL_ROWS, TILE = 16, 8, 32
assert len(PALETTE) == PAL_COLS * PAL_ROWS, len(PALETTE)
PAL_INDEX = {n: i for i, (n, _) in enumerate(PALETTE)}
FLAT_ROWS = {5}  # lumières et verre : pas de dégradé de crasse


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def make_palette_png(path):
    from PIL import Image
    img = Image.new("RGB", (PAL_COLS * TILE, PAL_ROWS * TILE))
    px = img.load()
    for i, (_, hx) in enumerate(PALETTE):
        r, g, b = hex_rgb(hx)
        cx, cy = (i % PAL_COLS) * TILE, (i // PAL_COLS) * TILE
        flat = (i // PAL_COLS) in FLAT_ROWS
        for y in range(TILE):
            # y image vers le bas ; bas de la case = sale (facteur 0.68), haut = propre (1.0)
            t = 1.0 - y / (TILE - 1)
            k = 1.0 if flat else 0.68 + 0.32 * t
            # léger désaturé vers un brun de crasse en bas
            dirt = (0.0 if flat else 0.18 * (1 - t))
            rr = int(min(255, (r * (1 - dirt) + 80 * dirt) * k))
            gg = int(min(255, (g * (1 - dirt) + 68 * dirt) * k))
            bb = int(min(255, (b * (1 - dirt) + 50 * dirt) * k))
            for x in range(TILE):
                px[cx + x, cy + y] = (rr, gg, bb)
    img.save(path)


def swatch_uv(color, t):
    i = PAL_INDEX[color]
    col, row = i % PAL_COLS, i // PAL_COLS
    u = (col + 0.5) / PAL_COLS
    # ligne 0 en haut de l'image → v haut
    v0 = 1.0 - (row + 1) / PAL_ROWS
    v = v0 + (0.12 + 0.76 * t) / PAL_ROWS
    return u, v


# ---------------------------------------------------------------------------
# Géométrie : chaque primitive est construite dans un bmesh temporaire puis
# copiée sous forme de listes (sommets, faces, couleur par face).
# ---------------------------------------------------------------------------

def _mat(at=(0, 0, 0), rot=(0, 0, 0)):
    return Matrix.Translation(Vector(at)) @ Euler([math.radians(a) for a in rot], "XYZ").to_matrix().to_4x4()


def _bevel_sharp(bm, offset, angle=40):
    if offset <= 0:
        return
    edges = [e for e in bm.edges if e.is_manifold and e.calc_face_angle(0) > math.radians(angle)]
    if not edges:
        return
    verts = list({v for e in edges for v in e.verts})
    bmesh.ops.bevel(bm, geom=verts + edges, offset=offset, offset_type="OFFSET", segments=1,
                    profile=0.5, affect="EDGES", clamp_overlap=True)


class Part:
    def __init__(self, model, name, pivot=None):
        self.model, self.name, self.pivot = model, name, pivot
        self.verts, self.faces, self.cols = [], [], []

    # -- ajout générique -------------------------------------------------
    def _add_bm(self, bm, c, m, deform=None):
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        if deform:
            for v in bm.verts:
                v.co = Vector(deform(v.co.copy()))
        bm.verts.index_update()
        base = len(self.verts)
        for v in bm.verts:
            self.verts.append(m @ v.co)
        for f in bm.faces:
            self.faces.append([base + v.index for v in f.verts])
            self.cols.append(c)
        bm.free()
        return self

    def raw(self, verts, faces, c, at=(0, 0, 0), rot=(0, 0, 0)):
        bm = bmesh.new()
        bv = [bm.verts.new(v) for v in verts]
        for f in faces:
            try:
                bm.faces.new([bv[i] for i in f])
            except ValueError:
                pass
        return self._add_bm(bm, c, _mat(at, rot))

    # -- boîtes ---------------------------------------------------------------
    def box(self, w, d, h, at=(0, 0, 0), c="grey", rot=(0, 0, 0), bev=None, deform=None, taper=None):
        """Boîte centrée sur `at` (w=X, d=Y, h=Z). taper=(sx, sy) rétrécit le haut."""
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        for v in bm.verts:
            x, y, z = v.co
            if taper and z > 0:
                x *= taper[0]
                y *= taper[1]
            v.co = Vector((x * w, y * d, z * h))
        if bev is None:
            bev = min(0.08, 0.14 * min(w, d, h))
        if bev > 0.004:
            _bevel_sharp(bm, bev)
        return self._add_bm(bm, c, _mat(at, rot), deform)

    def boxb(self, w, d, h, x=0, y=0, z=0, **kw):
        """Boîte posée : (x, y) centre, z = dessous."""
        return self.box(w, d, h, at=(x, y, z + h / 2), **kw)

    # -- révolution --------------------------------------------------------
    def lathe(self, prof, segs=12, at=(0, 0, 0), rot=(0, 0, 0), c="grey", cap0=True, cap1=True,
              deform=None, phase=None, sx=1.0, sy=1.0):
        """Profil [(r, z), ...] tourné autour de Z. r=0 en bout → pointe."""
        bm = bmesh.new()
        rings = []
        ph = (math.pi / segs) if phase is None else phase
        for r, z in prof:
            if r <= 1e-6:
                rings.append([bm.verts.new((0, 0, z))])
            else:
                rings.append([bm.verts.new((sx * r * math.cos(ph + 2 * math.pi * i / segs),
                                            sy * r * math.sin(ph + 2 * math.pi * i / segs), z))
                              for i in range(segs)])
        for a, b in zip(rings, rings[1:]):
            if len(a) == 1 and len(b) == 1:
                continue
            for i in range(segs):
                j = (i + 1) % segs
                if len(a) == 1:
                    bm.faces.new((a[0], b[i], b[j]))
                elif len(b) == 1:
                    bm.faces.new((a[i], a[j], b[0]))
                else:
                    bm.faces.new((a[i], a[j], b[j], b[i]))
        if cap0 and len(rings[0]) > 2:
            bm.faces.new(rings[0])
        if cap1 and len(rings[-1]) > 2:
            bm.faces.new(rings[-1])
        return self._add_bm(bm, c, _mat(at, rot), deform)

    def cyl(self, r, h, at=(0, 0, 0), c="grey", segs=12, rot=(0, 0, 0), bev=None, r2=None, **kw):
        """Cylindre (ou tronc de cône si r2) dont la base est en `at`, axe Z local."""
        r2 = r if r2 is None else r2
        if bev is None:
            bev = min(0.06, 0.15 * min(r, r2, h))
        if bev > 0.004 and min(r, r2) > bev * 1.5:
            prof = [(0, 0), (r - bev, 0), (r, bev), (r2, h - bev), (r2 - bev, h), (0, h)]
        else:
            prof = [(0, 0), (r, 0), (r2, h), (0, h)]
        return self.lathe(prof, segs=segs, at=at, rot=rot, c=c, **kw)

    def tube_open(self, r, h, t, at=(0, 0, 0), c="grey", segs=12, rot=(0, 0, 0), r2=None, bottom=True, **kw):
        """Récipient ouvert (poubelle, seau, fût ouvert) : paroi d'épaisseur t."""
        r2 = r if r2 is None else r2
        prof = []
        if bottom:
            prof += [(0, 0)]
        prof += [(r - 0.04, 0), (r, 0.04), (r2, h - 0.02), (r2 - t, h), (r2 - t - 0.01 * 0, h - 0.04),
                 ((r - t) if bottom else (r - t), t if bottom else 0)]
        if bottom:
            prof += [(0, t)]
        return self.lathe(prof, segs=segs, at=at, rot=rot, c=c, cap0=False, cap1=False, **kw)

    # -- sphères, tores ----------------------------------------------------
    def sphere(self, r, at=(0, 0, 0), c="grey", segs=8, rings=6, scale=(1, 1, 1), rot=(0, 0, 0), deform=None):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=r)
        for v in bm.verts:
            v.co = Vector((v.co.x * scale[0], v.co.y * scale[1], v.co.z * scale[2]))
        return self._add_bm(bm, c, _mat(at, rot), deform)

    def torus(self, R, r, at=(0, 0, 0), c="grey", segs=16, sides=6, rot=(0, 0, 0), sz=1.0, deform=None):
        bm = bmesh.new()
        vs = []
        for i in range(segs):
            a = 2 * math.pi * i / segs
            row = []
            for j in range(sides):
                b = 2 * math.pi * j / sides + math.pi / sides
                rr = R + r * math.cos(b)
                row.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a), r * sz * math.sin(b))))
            vs.append(row)
        for i in range(segs):
            for j in range(sides):
                a, b = vs[i], vs[(i + 1) % segs]
                bm.faces.new((a[j], b[j], b[(j + 1) % sides], a[(j + 1) % sides]))
        return self._add_bm(bm, c, _mat(at, rot), deform)

    # -- tubes le long d'une polyligne ------------------------------------
    def pipe(self, pts, r, c="grey", sides=6, caps=True, at=(0, 0, 0), rot=(0, 0, 0), closed=False):
        pts = [Vector(p) for p in pts]
        n = len(pts)
        bm = bmesh.new()
        tangents = []
        for i in range(n):
            if closed:
                t = pts[(i + 1) % n] - pts[i - 1]
            elif i == 0:
                t = pts[1] - pts[0]
            elif i == n - 1:
                t = pts[-1] - pts[-2]
            else:
                t = (pts[i + 1] - pts[i]).normalized() + (pts[i] - pts[i - 1]).normalized()
            tangents.append(t.normalized())
        up = Vector((0, 0, 1)) if abs(tangents[0].z) < 0.9 else Vector((1, 0, 0))
        nrm = tangents[0].cross(up).normalized()
        rings = []
        for i in range(n):
            t = tangents[i]
            nrm = (nrm - t * nrm.dot(t)).normalized()
            bi = t.cross(nrm).normalized()
            # compensation d'épaisseur aux coudes
            k = 1.0
            if 0 < i < n - 1 and not closed:
                d = (pts[i + 1] - pts[i]).normalized()
                k = 1.0 / max(0.5, abs(d.dot(t)))
            ring = []
            for j in range(sides):
                a = 2 * math.pi * j / sides
                off = nrm * math.cos(a) * r + bi * math.sin(a) * r
                # étirer dans la direction du coude
                off = off + t * (off.dot(t)) * (k - 1)
                ring.append(bm.verts.new(pts[i] + off))
            rings.append(ring)
        segs = n if closed else n - 1
        for i in range(segs):
            a, b = rings[i], rings[(i + 1) % n]
            for j in range(sides):
                bm.faces.new((a[j], a[(j + 1) % sides], b[(j + 1) % sides], b[j]))
        if caps and not closed:
            bm.faces.new(rings[0])
            bm.faces.new(rings[-1])
        return self._add_bm(bm, c, _mat(at, rot))

    def rod(self, a, b, r, c="grey", sides=6):
        return self.pipe([a, b], r, c=c, sides=sides)

    # -- extrusion d'un polygone 2D ---------------------------------------
    def prism(self, poly, t, at=(0, 0, 0), c="grey", rot=(0, 0, 0), plane="XZ", bev=0.0, deform=None):
        """Polygone 2D extrudé d'épaisseur t (centrée). plane XZ → épaisseur selon Y."""
        bm = bmesh.new()
        def P(u, v, w):
            if plane == "XZ":
                return (u, w, v)
            if plane == "XY":
                return (u, v, w)
            return (w, u, v)  # YZ
        front = [bm.verts.new(P(u, v, -t / 2)) for u, v in poly]
        back = [bm.verts.new(P(u, v, t / 2)) for u, v in poly]
        bm.faces.new(front)
        bm.faces.new(list(reversed(back)))
        n = len(poly)
        for i in range(n):
            j = (i + 1) % n
            bm.faces.new((front[i], front[j], back[j], back[i]))
        if bev > 0:
            _bevel_sharp(bm, bev)
        return self._add_bm(bm, c, _mat(at, rot), deform)


def blob_poly(w, h, seed=0, n=9):
    rng = random.Random(seed)
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n + rng.uniform(-0.2, 0.2)
        k = 0.65 + 0.35 * rng.random()
        out.append((math.cos(a) * w / 2 * k, math.sin(a) * h / 2 * k))
    return out


def _decal(self, w, h, at, c="rust", rot=(0, 0, 0), t=0.03, seed=0, n=9):
    """Tache irrégulière plate (rouille, crasse, affiche déchirée) dans le plan XZ (face -Y)."""
    return self.prism(blob_poly(w, h, seed, n), t, at=at, c=c, rot=rot, plane="XZ")


Part.decal = _decal


class Model:
    def __init__(self, name, dims, category, title=None, count=None, notes=""):
        self.name, self.dims, self.category = name, dims, category
        self.title = title or name
        self.count, self.notes = count, notes
        self.parts = {}
        self.rng = random.Random(hash(name) & 0xFFFF)
        self.fit = True
        self.grime = True  # False : couleurs propres (objets de quête, récompenses)

    def part(self, name, pivot=None):
        if name not in self.parts:
            self.parts[name] = Part(self, name, pivot)
        elif pivot is not None:
            self.parts[name].pivot = pivot
        return self.parts[name]

    def noise(self, amt, seed=None):
        rng = random.Random(seed if seed is not None else self.rng.random())
        cache = {}
        def f(co):
            k = (round(co.x, 3), round(co.y, 3), round(co.z, 3))
            if k not in cache:
                cache[k] = Vector((rng.uniform(-amt, amt), rng.uniform(-amt, amt), rng.uniform(-amt, amt)))
            return co + cache[k]
        return f

    # -- finalisation ------------------------------------------------------
    def bbox(self):
        vs = [v for p in self.parts.values() for v in p.verts]
        mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
        mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
        return mn, mx

    def normalize(self):
        """Recale la boîte englobante sur les dimensions exactes (Roblox X×Y×Z)."""
        X, Y, Z = self.dims  # Roblox : largeur, hauteur, profondeur
        target = Vector((X, Z, Y))  # Blender : largeur, profondeur, hauteur
        mn, mx = self.bbox()
        size = mx - mn
        sc = Vector((target[i] / size[i] if size[i] > 1e-6 else 1.0 for i in range(3)))
        self.raw_size = (size.x, size.z, size.y)
        self.scale_fix = (sc.x, sc.z, sc.y)
        c = (mn + mx) / 2
        for p in self.parts.values():
            p.verts = [Vector(((v.x - c.x) * sc.x, (v.y - c.y) * sc.y, (v.z - mn.z) * sc.z)) for v in p.verts]
            if p.pivot is not None:
                v = Vector(p.pivot)
                p.pivot = Vector(((v.x - c.x) * sc.x, (v.y - c.y) * sc.y, (v.z - mn.z) * sc.z))

    def build_objects(self, material):
        H = self.dims[1]
        G = max(0.25, min(3.0, H))  # hauteur de la zone de crasse
        objs = []
        tris_total = 0
        for p in self.parts.values():
            if not p.faces:
                continue
            me = bpy.data.meshes.new(p.name)
            me.from_pydata([tuple(v) for v in p.verts], [], p.faces)
            me.validate(clean_customdata=False)
            uvl = me.uv_layers.new(name="UVMap")
            for poly, col in zip(me.polygons, p.cols):
                for li in poly.loop_indices:
                    z = me.vertices[me.loops[li].vertex_index].co.z
                    t = max(0.0, min(1.0, z / G)) if self.grime else 0.92
                    uvl.data[li].uv = swatch_uv(col, t)
            bm = bmesh.new()
            bm.from_mesh(me)
            bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
            bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method="BEAUTY", ngon_method="BEAUTY")
            bm.to_mesh(me)
            bm.free()
            for poly in me.polygons:
                poly.use_smooth = True
            me.set_sharp_from_angle(angle=math.radians(38))
            piv = Vector(p.pivot) if p.pivot is not None else Vector((0, 0, 0))
            me.transform(Matrix.Translation(-piv))
            me.transform(Matrix.Scale(STUD_M, 4))
            me.materials.append(material)
            ob = bpy.data.objects.new(p.name, me)
            ob.location = piv * STUD_M
            bpy.context.scene.collection.objects.link(ob)
            objs.append(ob)
            tris_total += len(me.polygons)
        self.tris = tris_total
        return objs


def reset_scene():
    for ob in list(bpy.data.objects):
        if ob.type == "MESH":
            bpy.data.objects.remove(ob, do_unlink=True)
    for me in list(bpy.data.meshes):
        if me.users == 0:
            bpy.data.meshes.remove(me)


def palette_material(png_path):
    mat = bpy.data.materials.get("Palette")
    if mat:
        return mat
    mat = bpy.data.materials.new("Palette")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value = 0.85
    tex = nt.nodes.new("ShaderNodeTexImage")
    img = bpy.data.images.load(os.path.abspath(png_path))
    img.colorspace_settings.name = "sRGB"
    tex.image = img
    tex.interpolation = "Closest"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def export_fbx(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    for ob in bpy.context.scene.objects:
        ob.select_set(ob.type == "MESH")
    bpy.ops.export_scene.fbx(
        filepath=path, use_selection=True, object_types={"MESH"},
        axis_forward="-Z", axis_up="Y", apply_unit_scale=True,
        apply_scale_options="FBX_SCALE_UNITS", bake_space_transform=True,
        mesh_smooth_type="FACE", use_mesh_modifiers=False, add_leaf_bones=False,
        path_mode="COPY", embed_textures=True, use_custom_props=False,
    )
