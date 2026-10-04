"""96–99 : quête secondaire « x2 Luck Key » (repas du SDF, fragments de clé, clé finie, marqueur de quête).

Les pièces « Lueur » sont des halos qui enveloppent le fragment : en jeu, Material = Neon et
Transparency ≈ 0,6 (l'aperçu du canevas les montre ainsi).
"""
import math

from lib import Model

CAT = "07_quete"


# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------

def stroke(p, pts, a, b, c, y=0.0):
    """Trait épais à section octogonale le long d'une courbe du plan XZ (a : demi-largeur, b : demi-épaisseur en Y)."""
    sec = [(1, 0.6), (0.6, 1), (-0.6, 1), (-1, 0.6), (-1, -0.6), (-0.6, -1), (0.6, -1), (1, -0.6)]
    verts, faces = [], []
    n = len(pts)
    for i, (x, z) in enumerate(pts):
        x0, z0 = pts[max(0, i - 1)]
        x1, z1 = pts[min(n - 1, i + 1)]
        tx, tz = x1 - x0, z1 - z0
        L = math.hypot(tx, tz)
        nx, nz = -tz / L, tx / L
        for su, sv in sec:
            verts.append((x + nx * a * su, y + b * sv, z + nz * a * su))
    k = len(sec)
    for i in range(n - 1):
        for j in range(k):
            j2 = (j + 1) % k
            faces.append((i * k + j, i * k + j2, (i + 1) * k + j2, (i + 1) * k + j))
    faces.append(tuple(range(k)))
    faces.append(tuple((n - 1) * k + j for j in range(k)))
    p.raw(verts, faces, c)


def heart(L, w=0.85, n=16):
    """Contour d'une feuille de trèfle en cœur, pointe en (0, 0), lobes vers +Z (longueur L)."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x = 16 * math.sin(t) ** 3
        z = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x * w * L / 29, (z + 17) * L / 29))
    return pts


def crystal_leaf(p, L, ang, cx, cz, y, d, e, c1, c2, offset=0.03, scale=1.0):
    """Feuille de cristal à facettes : contour à double tranche + pyramides avant/arrière."""
    out = heart(L * scale)
    r = math.radians(ang)
    ca, sa = math.cos(r), math.sin(r)
    def place(u, v):
        v += offset
        return (cx + u * ca - v * sa, cz + u * sa + v * ca)
    pts = [place(u, v) for u, v in out]
    gx = sum(q[0] for q in pts) / len(pts)
    gz = sum(q[1] for q in pts) / len(pts)
    n = len(pts)
    verts = [(x, y - e, z) for x, z in pts] + [(x, y + e, z) for x, z in pts] + [(gx, y - d, gz), (gx, y + d, gz)]
    F, B = 2 * n, 2 * n + 1
    rim = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    front_a = [(i, F, (i + 1) % n) for i in range(0, n, 2)]
    front_b = [(i, F, (i + 1) % n) for i in range(1, n, 2)]
    back_a = [(n + (i + 1) % n, B, n + i) for i in range(0, n, 2)]
    back_b = [(n + (i + 1) % n, B, n + i) for i in range(1, n, 2)]
    p.raw(verts, front_a + back_b, c1)
    p.raw(verts, front_b + back_a + rim, c2)


def clover(p, L, cx, cz, y, d, e, c1="light_green", c2="mint", scale=1.0, rot=0):
    for k in range(4):
        crystal_leaf(p, L, rot + 90 * k, cx, cz, y, d, e, c1, c2, scale=scale)


# ---------------------------------------------------------------------------
# 96 · Repas du SDF
# ---------------------------------------------------------------------------

def repas():
    m = Model("repas_sdf", (1.2, 1.4, 0.8), CAT, "Repas pour le SDF", None, "Objet acheté puis donné")
    m.grime = False
    s = m.part("Sac")
    w, d, h, t = 1.08, 0.7, 0.82, 0.04
    nz = m.noise(0.02, 1)
    def crumple(co):
        co = nz(co)
        if co.z > h - 0.25:  # haut froissé, légèrement évasé
            k = (co.z - (h - 0.25)) / 0.25
            co.x *= 1 + 0.06 * k
            co.y *= 1 + 0.1 * k
            co.z += 0.04 * math.sin(co.x * 14) * k
        return co
    s.boxb(w, d, t, 0, 0, 0, c="cardboard_dark", bev=0.01)
    for sg in (-1, 1):
        s.boxb(w, t, h, 0, sg * (d / 2 - t / 2), 0, c="cardboard", bev=0.01, deform=crumple)
        s.boxb(t, d - 2 * t, h, sg * (w / 2 - t / 2), 0, 0, c="cardboard", bev=0.01, deform=crumple)
        s.box(0.03, 0.02, 0.55, at=(sg * 0.3, -d / 2 - 0.005, 0.38), c="cardboard_dark", bev=0)  # plis du papier
    s.boxb(w - 0.1, d - 0.1, 0.02, 0, 0, 0.45, c="soil", bev=0)  # fond sombre vu par l'ouverture
    s.decal(0.32, 0.24, (-0.22, -d / 2 - 0.012, 0.32), c="stain", t=0.02, seed=3)  # tache de gras
    s.decal(0.18, 0.14, (0.25, -d / 2 - 0.012, 0.55), c="stain", t=0.02, seed=4)
    s.box(0.36, 0.02, 0.1, at=(0.1, -d / 2 - 0.01, 0.66), rot=(0, 6, 0), c="red", bev=0)  # bout d'autocollant (sans texte)
    sw = m.part("Sandwich")
    tilt = (-6, 18, 0)  # baguette penchée qui dépasse largement du sac
    cx, cy, cz, L = 0.06, -0.04, 0.95, 0.9
    sw.box(0.3, 0.3, L, at=(cx - 0.07, cy, cz), rot=tilt, c="bread", bev=0.12, deform=m.noise(0.012, 5))
    sw.box(0.3, 0.3, L, at=(cx + 0.11, cy, cz - 0.06), rot=tilt, c="bread", bev=0.12, deform=m.noise(0.012, 6))
    sw.box(0.07, 0.38, L * 0.92, at=(cx + 0.02, cy, cz - 0.03), rot=tilt, c="lettuce", bev=0.02, deform=m.noise(0.03, 7))
    sw.box(0.04, 0.33, L * 0.7, at=(cx + 0.045, cy, cz), rot=tilt, c="yellow", bev=0.0)  # fromage
    for k in range(3):
        z = cz + 0.25 - k * 0.22
        sw.cyl(0.12, 0.04, at=(cx + 0.03 + (z - cz) * 0.32, cy - 0.17, z), rot=(90, 0, 0), c="tomato", segs=8, bev=0)
    for k in range(4):  # entailles de la croûte
        z = cz + 0.3 - k * 0.18
        sw.box(0.05, 0.16, 0.04, at=(cx - 0.21 + (z - cz) * 0.32, cy - 0.04, z), rot=(0, 18 - 40, 0), c="croissant", bev=0)
    return m


# ---------------------------------------------------------------------------
# 97 · Fragments de la clé
# ---------------------------------------------------------------------------

def frag_anneau():
    m = Model("fragment_1_tete", (1.0, 1.0, 0.2), CAT, "Fragment 1 : tête de clé", None, "À ramasser")
    f = m.part("Fragment")
    nz = m.noise(0.018, 11)
    def dent(co):
        co = nz(co)
        if co.x > 0.18 and co.z > 0.0:  # coup qui aplatit l'anneau en haut à droite
            co.x -= 0.05 * min(1, (co.x - 0.18) / 0.2)
        return co
    zc = 0.56
    f.torus(0.31, 0.095, at=(0, 0, zc), rot=(90, 0, 0), c="gold", segs=16, sides=7, sz=0.8, deform=dent)
    for a in (45, 135, 225, 315):
        r = math.radians(a)
        f.sphere(0.06, at=(0.31 * math.cos(r), -0.06, zc + 0.31 * math.sin(r)), c="gold", segs=6, rings=4)
    f.cyl(0.075, 0.13, at=(0, 0, zc - 0.31 - 0.08), rot=(180, 0, 0), c="gold", segs=8, bev=0, deform=m.noise(0.02, 12))
    f.decal(0.1, 0.06, (-0.2, -0.075, zc - 0.22), c="brass", rot=(0, 0, 40), t=0.01, seed=13)  # éraflure
    g = m.part("Lueur")
    g.torus(0.31, 0.135, at=(0, 0, zc), rot=(90, 0, 0), c="light_warm", segs=16, sides=7, sz=0.72)
    g.cyl(0.11, 0.2, at=(0, 0, zc - 0.31 - 0.13), c="light_warm", segs=8, bev=0)
    return m


def frag_tige():
    m = Model("fragment_2_tige", (0.3, 1.6, 0.3), CAT, "Fragment 2 : tige de clé rouillée", None, "À ramasser")
    f = m.part("Fragment")
    jag = m.noise(0.02, 21)
    f.lathe([(0, 0.06), (0.06, 0.03), (0.1, 0.08), (0.1, 1.5), (0.07, 1.56), (0.03, 1.53), (0, 1.55)], segs=8, c="rust", deform=jag)
    for z in (0.45, 1.15):
        f.torus(0.105, 0.03, at=(0, 0, z), c="rust_dark", segs=8, sides=4)
    for k, (z, c) in enumerate(((0.75, "rust_orange"), (1.35, "rust_dark"), (0.25, "brass"))):
        f.cyl(0.103, 0.12, at=(0, 0, z), rot=(0, 0, 40 * k), c=c, segs=8, bev=0, deform=m.noise(0.01, 22 + k))
    g = m.part("Lueur")
    g.cyl(0.15, 1.6, c="light_warm", segs=10, bev=0.06)
    return m


BIT = [(-0.22, 0.0), (0.0, 0.0), (0.0, 0.12), (0.09, 0.12), (0.09, 0.0), (0.22, 0.0), (0.22, 0.17), (0.34, 0.17), (0.34, 0.29),
       (0.27, 0.29), (0.27, 0.38), (0.34, 0.38), (0.34, 0.46), (-0.22, 0.46)]


def frag_panneton():
    m = Model("fragment_3_panneton", (0.8, 0.6, 0.2), CAT, "Fragment 3 : panneton", None, "À ramasser")
    f = m.part("Fragment")
    f.prism(BIT, 0.1, at=(0.02, 0, 0.04), c="brass", deform=m.noise(0.008, 31))
    f.cyl(0.085, 0.42, at=(-0.24, 0, 0.06), c="gold", segs=8, bev=0, deform=m.noise(0.02, 32))  # bout de tige cassé
    f.decal(0.16, 0.1, (0.12, -0.052, 0.3), c="rust", t=0.01, seed=33)
    g = m.part("Lueur")
    cx = sum(x for x, _ in BIT) / len(BIT)
    cz = sum(z for _, z in BIT) / len(BIT)
    g.prism([(cx + (x - cx) * 1.14, cz + (z - cz) * 1.16) for x, z in BIT], 0.18, at=(0.02, 0, 0.04), c="light_warm")
    g.cyl(0.11, 0.56, at=(-0.24, 0, 0.0), c="light_warm", segs=8, bev=0)
    return m


def frag_trefle():
    m = Model("fragment_4_trefle", (0.9, 0.9, 0.3), CAT, "Fragment 4 : trèfle en cristal", None, "À ramasser")
    m.grime = False
    f = m.part("Fragment")
    zc = 0.5
    clover(f, 0.34, 0, zc, 0, 0.11, 0.035, rot=10)
    stroke(f, [(0.02, zc - 0.05), (0.06, zc - 0.25), (0.14, zc - 0.42)], 0.035, 0.035, "green")
    g = m.part("Lueur")
    clover(g, 0.34, 0, zc, 0, 0.15, 0.07, c1="light_green", c2="light_green", scale=1.18, rot=10)
    stroke(g, [(0.02, zc - 0.05), (0.06, zc - 0.25), (0.14, zc - 0.44)], 0.07, 0.07, "light_green")
    return m


# ---------------------------------------------------------------------------
# 98 · La « x2 Luck Key »
# ---------------------------------------------------------------------------

def luck_key():
    m = Model("x2_luck_key", (1.2, 3.0, 0.4), CAT, "« x2 Luck Key »", None, "Résultat du craft ; « x2 » gravé sur la tige")
    m.grime = False
    zr = 2.42
    a = m.part("Anneau")
    a.torus(0.47, 0.11, at=(0, 0, zr), rot=(90, 0, 0), c="gold", segs=20, sides=8, sz=0.9)
    for ang in (45, 135, 225, 315):
        r = math.radians(ang)
        a.sphere(0.07, at=(0.47 * math.cos(r), -0.07, zr + 0.47 * math.sin(r)), c="gold", segs=6, rings=4)
    a.sphere(0.09, at=(0, 0, zr + 0.6), c="gold", segs=8, rings=5)  # bouton sommital
    a.lathe([(0, 1.78), (0.15, 1.78), (0.19, 1.83), (0.14, 1.9), (0.12, 1.94), (0, 1.94)], segs=10, c="gold")  # collerette
    t = m.part("Tige")
    t.cyl(0.11, 1.62, at=(0, 0, 0.18), c="gold", segs=10, bev=0)
    for z in (0.62, 1.6):
        t.torus(0.12, 0.035, at=(0, 0, z), c="gold", segs=10, sides=4)
    t.box(0.5, 0.22, 0.46, at=(0, 0, 1.12), c="gold", bev=0.07)  # cartouche
    # gravure « x2 » (en creux foncé sur la face avant)
    yg, ce = -0.108, "yellow_dark"
    t.rod((-0.2, yg, 1.02), (-0.06, yg, 1.2), 0.022, c=ce, sides=4)
    t.rod((-0.2, yg, 1.2), (-0.06, yg, 1.02), 0.022, c=ce, sides=4)
    two = [(0.03 + 0.07 * (1 + math.cos(math.radians(a2))), 1.2 + 0.065 * math.sin(math.radians(a2))) for a2 in range(160, -50, -30)]
    two += [(0.03, 1.0), (0.18, 1.0)]
    for (x0, z0), (x1, z1) in zip(two, two[1:]):
        t.rod((x0, yg, z0), (x1, yg, z1), 0.022, c=ce, sides=4)
    pn = m.part("Panneton")
    bit = [(0.0, 0.0), (0.12, 0.0), (0.12, 0.1), (0.2, 0.1), (0.2, 0.0), (0.3, 0.0), (0.3, 0.16), (0.42, 0.16), (0.42, 0.28),
           (0.35, 0.28), (0.35, 0.36), (0.42, 0.36), (0.42, 0.46), (0.0, 0.46)]
    pn.prism(bit, 0.14, at=(0.06, 0, 0.0), c="gold")
    pn.cyl(0.13, 0.2, at=(0, 0, 0.0), c="gold", segs=10, bev=0.04)
    tr = m.part("Trefle")
    clover(tr, 0.31, 0, zr, 0, 0.19, 0.05, rot=0)
    return m


# ---------------------------------------------------------------------------
# 99 · Point d'interrogation de quête
# ---------------------------------------------------------------------------

def interrogation():
    m = Model("point_interrogation", (1.2, 2.2, 0.4), CAT, "Point d'interrogation flottant", None, "Au-dessus du SDF ; pivot au bas du point")
    m.grime = False
    q = m.part("Interrogation")
    cz, R = 1.55, 0.42
    pts = [(0.0, 0.72), (0.0, 0.86), (0.03, 0.98), (0.12, 1.08)]
    pts += [(R * math.cos(math.radians(a)), cz + R * math.sin(math.radians(a))) for a in range(-48, 206, 14)]
    stroke(q, pts, 0.19, 0.2, "flame_yellow")
    ex, ez = pts[-1]
    q.sphere(0.19, at=(ex, 0, ez), c="flame_yellow", scale=(1, 1.05, 1), segs=10, rings=7)
    q.sphere(0.19, at=(0, 0, 0.72), c="flame_yellow", scale=(1, 1.05, 0.7), segs=10, rings=7)
    pt = m.part("Point")
    pt.sphere(0.2, at=(0, 0, 0.2), c="flame_yellow", segs=12, rings=8)
    return m


MODELS = [
    ("96_repas_sdf", repas), ("97a_fragment_tete", frag_anneau), ("97b_fragment_tige", frag_tige),
    ("97c_fragment_panneton", frag_panneton), ("97d_fragment_trefle", frag_trefle), ("98_x2_luck_key", luck_key),
    ("99_point_interrogation", interrogation),
]
