"""114–120 : quête du pirate (radeau, matériaux, clé x5) et entrée des égouts."""
import math
import random

from mathutils import Vector

from lib import Model, blob_poly
from m_quete import stroke, BIT

CAT = "09_pirate"


# ---------------------------------------------------------------------------
# 114 · Pirate déboussolé
# ---------------------------------------------------------------------------

def pirate():
    m = Model("pirate_deboussole", (2, 5.5, 1.5), CAT, "Pirate déboussolé", None, "Personnage tourné vers -Z ; jambe de bois")
    c = m.part("Corps")
    skin, coat = "peach", "fabric_red"
    sq = lambda k: (lambda co: Vector((co.x, co.y * k, co.z)))
    # jambes : botte à droite (-X), jambe de bois à gauche (+X)
    c.box(0.42, 0.62, 0.4, at=(-0.3, -0.08, 0.2), c="wood_black", bev=0.12)
    c.cyl(0.22, 0.55, at=(-0.3, 0.0, 0.3), c="wood_black", segs=8)
    c.cyl(0.2, 1.4, at=(-0.3, 0.0, 0.85), r2=0.24, c="cream", segs=8)
    c.cyl(0.07, 0.95, at=(0.3, 0.0, 0.0), r2=0.11, c="wood", segs=6, bev=0)
    c.cyl(0.24, 0.2, at=(0.3, 0.0, 0.95), c="wood_dark", segs=8)
    c.cyl(0.21, 1.1, at=(0.3, 0.0, 1.15), r2=0.24, c="cream", segs=8)
    for x in (-0.3, 0.3):
        for z in (1.3, 1.6):
            c.torus(0.225, 0.03, at=(x, 0, z), c="red", segs=8, sides=4)  # rayures du pantalon
    # manteau long, rapiécé
    c.lathe([(0, 1.55), (0.6, 1.55), (0.56, 2.25), (0.53, 2.9), (0.5, 3.4), (0.4, 3.85), (0, 3.9)], segs=10, c=coat, sy=0.72,
            deform=m.noise(0.02, 1))
    c.box(0.32, 0.06, 1.3, at=(0, -0.37, 3.15), rot=(-4, 0, 0), c="white", bev=0.01)  # chemise
    for x in (-0.22, 0.22):
        for z in (2.6, 2.95, 3.3):
            c.sphere(0.05, at=(x, -0.37, z), c="gold", segs=6, rings=4)
    c.torus(0.56, 0.07, at=(0, 0, 2.25), c="leather", segs=12, sides=4, deform=sq(0.72))  # ceinture
    c.boxb(0.2, 0.06, 0.18, 0, -0.43, 2.16, c="gold", bev=0.02)
    c.decal(0.28, 0.24, (0.36, -0.44, 1.95), c="fabric_blue", t=0.02, seed=2)  # rustine
    c.decal(0.22, 0.2, (-0.3, -0.38, 3.0), c="beige", t=0.02, seed=3)
    # tête
    c.cyl(0.18, 0.2, at=(0, 0, 3.8), c=skin, segs=8, bev=0)
    c.sphere(0.5, at=(0, -0.02, 4.38), c=skin, segs=12, rings=8)
    c.sphere(0.13, at=(0, -0.5, 4.33), c="beak", segs=8, rings=5)  # gros nez
    c.sphere(0.42, at=(0, -0.2, 4.05), c="wood_dark", scale=(1.0, 0.75, 0.75), segs=10, rings=6, deform=m.noise(0.03, 4))  # barbe
    for s in (-1, 1):
        c.sphere(0.1, at=(s * 0.11, -0.47, 4.22), c="wood_dark", scale=(1.6, 0.6, 0.6), rot=(0, 0, -s * 15), segs=6, rings=4)
        c.sphere(0.1, at=(s * 0.49, -0.02, 4.38), c=skin, segs=6, rings=4)  # oreilles
    c.sphere(0.1, at=(-0.17, -0.43, 4.48), c="eye_white", segs=8, rings=5)  # œil valide, qui louche vers le haut
    c.sphere(0.045, at=(-0.21, -0.52, 4.51), c="eye", segs=6, rings=4)
    c.box(0.22, 0.05, 0.05, at=(-0.18, -0.44, 4.67), rot=(0, 22, 0), c="wood_dark", bev=0)  # sourcil levé
    c.box(0.2, 0.05, 0.05, at=(0.18, -0.43, 4.63), rot=(0, -12, 0), c="wood_dark", bev=0)
    c.cyl(0.12, 0.03, at=(0.18, -0.44, 4.48), rot=(90, 0, 0), c="black", segs=8, bev=0)  # cache-œil
    c.torus(0.505, 0.025, at=(0, -0.02, 4.5), rot=(10, -14, 18), c="black", segs=14, sides=3)
    c.torus(0.06, 0.015, at=(0.51, -0.02, 4.22), rot=(0, 90, 0), c="gold", segs=8, sides=3)  # boucle d'oreille
    c.sphere(0.12, at=(0, 0.46, 4.25), c="wood_dark", segs=6, rings=4)  # catogan
    c.rod((0, 0.48, 4.2), (0, 0.52, 3.85), 0.06, c="wood_dark", sides=5)
    c.box(0.18, 0.05, 0.08, at=(0, 0.5, 4.12), c="red", bev=0.01)
    # bras droit (tient la boussole) et bras gauche (se gratte la tête)
    c.pipe([(-0.5, 0, 3.6), (-0.86, -0.15, 3.15), (-0.52, -0.6, 2.95)], 0.14, c=coat, sides=6)
    c.sphere(0.15, at=(-0.5, -0.62, 2.94), c="white", segs=6, rings=4)
    c.sphere(0.14, at=(-0.45, -0.72, 2.92), c=skin, scale=(1.1, 1.1, 0.6), segs=8, rings=5)
    c.pipe([(0.5, 0, 3.6), (0.86, 0.05, 4.1), (0.66, 0.0, 4.62)], 0.13, c=coat, sides=6)
    c.sphere(0.13, at=(0.6, 0.0, 4.7), c=skin, segs=8, rings=5)
    # tricorne
    h = m.part("Chapeau")
    HB = 4.72
    h.sphere(0.46, at=(0, 0.02, HB), c="wood_black", scale=(1, 0.95, 1.05), segs=12, rings=8,
             deform=lambda co: Vector((co.x, co.y, max(co.z, 0.0))))
    h.lathe([(0.4, 0.0), (0.9, 0.02), (0.98, 0.42), (0.88, 0.45), (0.8, 0.1), (0.4, 0.12), (0.4, 0.0)], segs=3,
            phase=-math.pi / 2, at=(0, 0.02, HB), c="wood_black", cap0=False, cap1=False)
    h.torus(0.93, 0.035, at=(0, 0.02, HB + 0.435), rot=(0, 0, 270), c="gold", segs=3, sides=4)
    h.prism([(0, 0), (0.12, 0.2), (0.1, 0.42), (0, 0.55), (-0.06, 0.35), (-0.05, 0.15)], 0.03, at=(0.5, 0.3, HB + 0.3),
            rot=(0, -25, 20), c="flower_white")  # plume
    h.decal(0.2, 0.16, (-0.3, -0.25, HB + 0.3), c="fabric_brown", rot=(-30, 0, 30), t=0.02, seed=6)  # trou rafistolé
    # boussole cassée
    b = m.part("Boussole")
    bx, by, bz = -0.45, -0.75, 2.98
    b.cyl(0.21, 0.1, at=(bx, by, bz), c="brass", segs=12, bev=0.02)
    b.cyl(0.17, 0.015, at=(bx, by, bz + 0.1), c="glass", segs=12, bev=0)
    for a1, a2 in ((0, 0.12), (0.12, 0.05), (0.12, 0.16)):  # fêlures
        b.rod((bx + 0.02, by + a1 - 0.05, bz + 0.12), (bx + 0.13, by + a2 - 0.08, bz + 0.12), 0.008, c="white", sides=3)
    b.box(0.26, 0.03, 0.02, at=(bx, by, bz + 0.13), rot=(0, 0, 35), c="red", bev=0)  # aiguille de travers
    b.box(0.12, 0.03, 0.02, at=(bx + 0.06, by - 0.02, bz + 0.18), rot=(0, 30, -60), c="white", bev=0)  # morceau cassé qui pointe
    b.pipe([(bx + 0.1 + 0.03 * math.cos(k), by + 0.06 + 0.03 * math.sin(k), bz + 0.11 + k * 0.025) for k in [i * 0.7 for i in range(10)]],
           0.008, c="metal", sides=3)  # ressort sorti
    b.cyl(0.2, 0.025, at=(bx, by + 0.21, bz + 0.05), rot=(110, 0, 15), c="brass", segs=12, bev=0)  # couvercle de travers
    return m


# ---------------------------------------------------------------------------
# 115 · Planche flottée
# ---------------------------------------------------------------------------

PLANK = [(-1.1, -0.25), (0.7, -0.25), (0.85, -0.18), (0.95, -0.24), (1.1, -0.1), (1.0, 0.0), (1.1, 0.12), (0.9, 0.25),
         (-0.95, 0.25), (-1.1, 0.12)]


def planche_flottee():
    m = Model("planche_flottee", (2.4, 0.3, 0.6), CAT, "Planche flottée", None, "À ramasser")
    p = m.part("Planche")
    nz = m.noise(0.015, 1)
    warp = lambda co: nz(Vector((co.x, co.y, co.z + 0.03 * math.sin(co.x * 2.2))))
    p.prism(PLANK, 0.16, at=(0, 0, 0.12), c="wood_old", plane="XY", deform=warp)
    for k, (x, w, c) in enumerate(((-0.5, 0.7, "wood_dark"), (0.4, 0.5, "wood_dark"), (-0.1, 0.4, "olive"), (0.8, 0.3, "leaf_dark"))):
        p.decal(w, 0.3, (x, 0.02 * k, 0.205 + 0.03 * math.sin(x * 2.2)), c=c, rot=(90, 0, 0), t=0.01, seed=10 + k)  # bois humide, algues
    for y in (-0.12, 0.08):
        p.box(1.6, 0.025, 0.01, at=(-0.2, y, 0.2 + 0.0), c="wood", bev=0)  # veines
    p.pipe([(-0.7, 0.24, 0.18), (-0.65, 0.3, 0.1), (-0.6, 0.29, 0.02)], 0.03, c="leaf_dark", sides=3)  # algue qui pend
    for (x, y) in ((-0.9, -0.15), (-0.85, -0.05), (-0.95, 0.05)):
        p.sphere(0.04, at=(x, y, 0.2), c="grey_light", segs=5, rings=3, scale=(1, 1, 0.6))  # bernacles
    p.rod((0.55, 0.05, 0.12), (0.62, 0.0, 0.3), 0.018, c="rust", sides=4)  # clou rouillé
    g = m.part("Lueur")
    g.prism([(x * 1.08, y * 1.15) for x, y in PLANK], 0.3, at=(0, 0, 0.15), c="light_warm", plane="XY")
    return m


# ---------------------------------------------------------------------------
# 116 · Plaque de moisissure murale
# ---------------------------------------------------------------------------

def moisissure():
    m = Model("plaque_moisissure", (2, 2, 0.2), CAT, "Plaque de moisissure murale", None, "À plat sur un mur, face visible vers -Z")
    p = m.part("Moisissure")
    p.prism(blob_poly(1.8, 1.8, seed=4, n=14), 0.04, at=(0, 0.06, 1.0), c="olive")
    p.prism([(x + 0.1, z + 0.05) for x, z in blob_poly(1.25, 1.15, seed=5, n=12)], 0.04, at=(0, 0.03, 1.0), c="leaf_dark")
    p.prism([(x - 0.2, z - 0.05) for x, z in blob_poly(0.75, 0.65, seed=6, n=10)], 0.04, at=(0, 0.0, 1.0), c="mud")
    rng = random.Random(7)
    for k in range(16):
        a, r = rng.uniform(0, 2 * math.pi), rng.uniform(0.05, 0.7)
        x, z = r * math.cos(a), 1.0 + r * math.sin(a)
        p.sphere(rng.uniform(0.05, 0.11), at=(x, -0.03, z), c=rng.choice(["lettuce", "mint", "olive", "khaki"]), scale=(1, 0.5, 1),
                 segs=6, rings=4)
    for x in (-0.35, 0.15, 0.45):  # coulures
        p.rod((x, 0.02, 0.55), (x + 0.02, 0.02, 0.25), 0.03, c="olive", sides=4)
    g = m.part("Lueur")
    g.prism([(x * 1.11, z * 1.11) for x, z in blob_poly(1.8, 1.8, seed=4, n=14)], 0.2, at=(0, 0.0, 1.0), c="light_green")
    return m


# ---------------------------------------------------------------------------
# 117 · Rouleau de corde
# ---------------------------------------------------------------------------

def rouleau_corde():
    m = Model("rouleau_corde", (1.2, 0.6, 1.2), CAT, "Rouleau de corde", None, "Objet d'inventaire")
    p = m.part("Corde")
    n, turns, R = 54, 3.2, 0.44
    pts, twist = [], []
    for i in range(n):
        a = 2 * math.pi * turns * i / n
        z = 0.09 + 0.42 * i / (n - 1)
        rr = R + 0.012 * math.sin(i * 1.7)
        pts.append((rr * math.cos(a), rr * math.sin(a), z))
        b = 7 * a
        rad = Vector((math.cos(a), math.sin(a), 0))
        off = rad * (0.075 * math.cos(b)) + Vector((0, 0, 0.075 * math.sin(b)))
        twist.append(tuple(Vector(pts[-1]) + off))
    a_end = 2 * math.pi * turns
    tail = [(0.62 * math.cos(a_end + 0.4), 0.62 * math.sin(a_end + 0.4) * 0.8, 0.35), (0.35, -0.5, 0.12), (0.12, -0.53, 0.085)]
    p.pipe(pts + tail, 0.085, c="jute", sides=6)
    p.pipe(twist, 0.025, c="cardboard_dark", sides=3)
    for k in range(4):  # bout effiloché
        p.rod((0.12, -0.53, 0.085), (0.0 - 0.03 * k, -0.5 - 0.04 * k + 0.06, 0.06 + 0.02 * (k % 2)), 0.015, c="sand", sides=3)
    for a in (0.6, 3.7):  # liens
        p.torus(0.28, 0.025, at=(R * math.cos(a), R * math.sin(a), 0.31), rot=(90, 0, math.degrees(a)), c="cardboard_dark",
                segs=10, sides=3, deform=lambda co: Vector((co.x * 0.42, co.y, co.z)))
    return m


# ---------------------------------------------------------------------------
# 118 · Radeau de fortune
# ---------------------------------------------------------------------------

def cloth(p, x0, x1, z0, z1, y, bulge, c, nx=6, nz=6, t=0.03):
    """Toile gonflée (vers -Y) à deux faces, entre x0..x1 et z0..z1."""
    def Y(u, v):
        return y - bulge * math.sin(math.pi * u) * math.sin(math.pi * v)
    verts = []
    for side in (0, 1):
        for j in range(nz + 1):
            for i in range(nx + 1):
                u, v = i / nx, j / nz
                verts.append((x0 + (x1 - x0) * u, Y(u, v) + side * t, z0 + (z1 - z0) * v))
    W = nx + 1
    off = W * (nz + 1)
    idx = lambda i, j, s: s * off + j * W + i
    faces = []
    for j in range(nz):
        for i in range(nx):
            faces.append((idx(i, j, 0), idx(i + 1, j, 0), idx(i + 1, j + 1, 0), idx(i, j + 1, 0)))
            faces.append((idx(i, j, 1), idx(i, j + 1, 1), idx(i + 1, j + 1, 1), idx(i + 1, j, 1)))
    border = [(i, 0) for i in range(nx)] + [(nx, j) for j in range(nz)] + [(i, nz) for i in range(nx, 0, -1)] + [(0, j) for j in range(nz, 0, -1)]
    for k in range(len(border)):
        a, b = border[k], border[(k + 1) % len(border)]
        faces.append((idx(*a, 0), idx(*b, 0), idx(*b, 1), idx(*a, 1)))
    p.raw(verts, faces, c)
    return Y


def radeau():
    m = Model("radeau", (8, 6, 6), CAT, "Radeau de fortune", None, "Planches et rondins liés à la corde")
    pl = m.part("Planches")
    rng = random.Random(8)
    xs = [-3.5 + i for i in range(8)]
    for i, x in enumerate(xs):
        L = 5.8 - rng.uniform(0, 0.5)
        pl.cyl(0.45, L, at=(x, L / 2 + rng.uniform(-0.15, 0.15), 0.45), rot=(90, 0, 0), c=("wood_old", "wood", "wood_dark")[i % 3], segs=8,
               bev=0.06, deform=m.noise(0.03, 20 + i))
    for y in (-2.1, 0.0, 2.1):
        pl.boxb(7.8, 0.5, 0.12, 0, y, 0.86, c="pallet", rot=(0, 0, rng.uniform(-2, 2)), bev=0.03)
    pl.boxb(2.0, 3.0, 0.1, 2.0, 0.6, 0.98, c="teal", bev=0.03, rot=(0, 0, 6))  # vieille porte récupérée comme pont
    pl.cyl(0.07, 0.06, at=(2.75, -0.6, 1.08), c="brass", segs=6, bev=0)
    pl.decal(0.8, 0.5, (2.0, 0.9, 1.085), c="mud", rot=(90, 0, 6), t=0.01, seed=21)
    for k in range(4):  # morceau de palette
        pl.boxb(1.6, 0.25, 0.08, -2.2, -1.0 + k * 0.35, 0.98, c="pallet", bev=0.02)
    pl.boxb(0.5, 0.5, 0.3, 0, 0.3, 0.98, c="wood_dark", bev=0.04)  # pied de mât
    co = m.part("Cordes")
    for y0 in (-2.1, 0.0, 2.1):
        y = y0 + 0.36
        pts = []
        for k in range(17):
            x = -4.0 + k * 0.5
            top = (k % 2 == 1)
            pts.append((x, y, 0.95 if top else 0.72))
        co.pipe(pts, 0.05, c="jute", sides=4)
        for x in (-3.5, 3.5):
            co.torus(0.5, 0.05, at=(x, y0 - 0.3, 0.45), rot=(90, 0, 0), c="jute", segs=10, sides=4)
    for (x, y) in ((-3.7, -2.8), (3.7, -2.8), (-3.7, 2.8), (3.7, 2.8)):  # haubans
        co.rod((0, 0.3, 5.3), (x, y, 0.9), 0.03, c="jute", sides=3)
    for z in (1.35, 1.45, 1.55):
        co.torus(0.17, 0.035, at=(0, 0.3, z), c="jute", segs=8, sides=3)
    mt = m.part("Mat")
    mt.cyl(0.14, 4.8, at=(0, 0.3, 1.0), r2=0.11, c="wood", segs=8, bev=0)
    mt.cyl(0.08, 4.8, at=(-2.4, 0.3, 5.4), rot=(0, 90, 0), c="wood_old", segs=6, bev=0)  # vergue
    mt.cyl(0.08, 4.6, at=(-2.3, 0.3, 1.8), rot=(0, 90, 0), c="wood_old", segs=6, bev=0)  # bôme
    v = m.part("Voile")
    Y = cloth(v, -2.3, 2.3, 1.9, 5.32, 0.15, 0.55, "cream")
    for k, (u, w, h, c) in enumerate(((0.25, 0.9, 0.7, "fabric_blue"), (0.65, 0.7, 0.9, "tarp_blue"), (0.45, 0.6, 0.5, "fabric_red"),
                                      (0.8, 0.5, 0.6, "beige"))):
        vz = 0.25 + 0.5 * (k % 2) + 0.1 * k
        x, z = -2.3 + 4.6 * u, 1.9 + 3.42 * vz
        yy = Y(u, vz)
        v.decal(w, h, (x, yy - 0.025, z), c=c, t=0.02, seed=30 + k)
        v.decal(w, h, (x, yy + 0.055, z), c=c, t=0.02, seed=30 + k)
    v.prism([(0, 0), (0.55, -0.08), (0.48, 0.12), (0.62, 0.22), (0, 0.25)], 0.02, at=(0.12, 0.3, 5.75), c="red")  # chiffon en guise de drapeau
    return m


# ---------------------------------------------------------------------------
# 119 · Clé « x5 » à l'ancre
# ---------------------------------------------------------------------------

def cle_x5():
    m = Model("x5_anchor_key", (1.2, 3.0, 0.4), CAT, "Clé dorée « x5 »", None, "Ancre dans l'anneau ; « x5 » gravé sur la tige")
    m.grime = False
    zr = 2.42
    a = m.part("Anneau")
    a.torus(0.47, 0.11, at=(0, 0, zr), rot=(90, 0, 0), c="gold", segs=20, sides=8, sz=1.3)
    for ang in (45, 135, 225, 315):
        r = math.radians(ang)
        a.sphere(0.07, at=(0.47 * math.cos(r), -0.1, zr + 0.47 * math.sin(r)), c="gold", segs=6, rings=4)
    a.sphere(0.09, at=(0, 0, zr + 0.6), c="gold", segs=8, rings=5)
    a.lathe([(0, 1.78), (0.15, 1.78), (0.19, 1.83), (0.14, 1.9), (0.12, 1.94), (0, 1.94)], segs=10, c="gold")
    t = m.part("Tige")
    t.cyl(0.11, 1.62, at=(0, 0, 0.18), c="gold", segs=10, bev=0)
    for z in (0.62, 1.6):
        t.torus(0.12, 0.035, at=(0, 0, z), c="gold", segs=10, sides=4)
    t.box(0.5, 0.3, 0.46, at=(0, 0, 1.12), c="gold", bev=0.07)
    yg, ce = -0.148, "yellow_dark"
    t.rod((-0.2, yg, 1.02), (-0.06, yg, 1.2), 0.022, c=ce, sides=4)
    t.rod((-0.2, yg, 1.2), (-0.06, yg, 1.02), 0.022, c=ce, sides=4)
    five = [(0.18, 1.21), (0.05, 1.21), (0.04, 1.125)]
    five += [(0.1 + 0.07 * math.cos(math.radians(a2)), 1.06 + 0.07 * math.sin(math.radians(a2))) for a2 in range(135, -150, -45)]
    for (x0, z0), (x1, z1) in zip(five, five[1:]):
        t.rod((x0, yg, z0), (x1, yg, z1), 0.022, c=ce, sides=4)
    pn = m.part("Panneton")
    bit = [(0.0, 0.0), (0.12, 0.0), (0.12, 0.1), (0.2, 0.1), (0.2, 0.0), (0.3, 0.0), (0.3, 0.16), (0.42, 0.16), (0.42, 0.28),
           (0.35, 0.28), (0.35, 0.36), (0.42, 0.36), (0.42, 0.46), (0.0, 0.46)]
    pn.prism(bit, 0.14, at=(0.06, 0, 0.0), c="gold")
    pn.cyl(0.13, 0.2, at=(0, 0, 0.0), c="gold", segs=10, bev=0.04)
    an = m.part("Ancre")
    A, B = 0.05, 0.19
    stroke(an, [(0, zr + 0.22), (0, zr - 0.27)], A, B, "neon_blue")
    stroke(an, [(-0.16, zr + 0.13), (0.16, zr + 0.13)], 0.035, 0.17, "neon_blue")
    arc = [(0.22 * math.cos(math.radians(a2)), zr - 0.06 + 0.22 * math.sin(math.radians(a2))) for a2 in range(200, 341, 20)]
    stroke(an, arc, 0.045, 0.18, "neon_blue")
    for s in (-1, 1):
        ex, ez = arc[0] if s < 0 else arc[-1]
        an.prism([(ex - s * 0.03, ez - 0.05), (ex + s * 0.09, ez + 0.08), (ex - s * 0.04, ez + 0.06)], 0.3, at=(0, 0, 0), c="sky")  # pattes
    an.torus(0.065, 0.028, at=(0, 0, zr + 0.28), rot=(90, 0, 0), c="sky", segs=8, sides=4, sz=2.5)  # organeau
    return m


# ---------------------------------------------------------------------------
# 120 · Plaque d'égout ouverte avec échelle
# ---------------------------------------------------------------------------

def egout_ouvert():
    m = Model("egout_ouvert", (3, 1, 3), CAT, "Plaque d'égout ouverte avec échelle", None,
              "Posée sur la chaussée ; trou noir (faux puits) à utiliser comme zone de téléportation")
    p = m.part("Plaque")
    p.lathe([(1.18, 0.0), (1.45, 0.0), (1.45, 0.06), (1.38, 0.1), (1.18, 0.1), (1.18, 0.0)], segs=20, c="iron", cap0=False, cap1=False)
    p.cyl(1.19, 0.03, c="eye", segs=20, bev=0)  # trou noir
    p.decal(0.5, 0.3, (-0.9, -0.85, 0.06), c="rust", rot=(90, 0, -40), t=0.01, seed=40)
    cx = 0.95  # plaque à moitié poussée, posée de travers sur le bord du cadre
    p.cyl(1.2, 0.07, at=(cx, -0.05, 0.1), rot=(0, -2.5, 0), c="iron", segs=20, bev=0.02)
    for r in (0.35, 0.75):
        p.torus(r, 0.04, at=(cx, -0.05, 0.18), c="iron", segs=16, sides=4, sz=0.7)
    for a in (15, 60, 105, 150):
        p.box(2.1, 0.08, 0.04, at=(cx, -0.05, 0.19), rot=(0, 0, a), c="iron", bev=0.01)
    p.decal(0.5, 0.3, (cx + 0.4, -0.45, 0.2), c="rust", rot=(90, 0, 30), t=0.01, seed=41)
    e = m.part("Echelle")
    for x in (-0.36, 0.36):
        e.pipe([(x - 0.35, 1.0, 0.02), (x - 0.35, 1.0, 0.65), (x - 0.35, 0.88, 0.95), (x - 0.35, 0.65, 0.98)], 0.05, c="galva", sides=6)
    for z in (0.12, 0.45):
        e.rod((-0.71, 1.0, z), (0.01, 1.0, z), 0.035, c=("rust" if z < 0.2 else "galva"), sides=4)
    return m


MODELS = [
    ("114_pirate_deboussole", pirate), ("115_planche_flottee", planche_flottee), ("116_plaque_moisissure", moisissure),
    ("117_rouleau_corde", rouleau_corde), ("118_radeau", radeau), ("119_cle_x5_ancre", cle_x5), ("120_egout_ouvert", egout_ouvert),
]
