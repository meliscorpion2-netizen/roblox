"""385–408 : naufrage, événements météo, mutations de machines et roue de la fortune."""
import math
import random

from mathutils import Vector

from lib import Model, blob_poly

CAT = "14_evenements"


def M(name, dims, title, note="", grime=False):
    m = Model(name, dims, CAT, title, None, note)
    m.grime = grime
    return m


def barrel(p, x, y, z, rot, c="wood", hoop="metal_dark", r=0.75, h=1.8):
    p.lathe([(0, 0), (r * 0.85, 0), (r, h * 0.5), (r * 0.85, h), (0, h)], segs=10, at=(x, y, z), rot=rot, c=c)
    for t in (0.15, 0.85):
        rr = r * (0.85 + 0.15 * (1 - abs(t - 0.5) * 2)) + 0.03
        p.torus(rr, 0.05, at=(x, y, z), rot=rot, c=hoop, segs=10, sides=3,
                deform=lambda co, t=t: Vector((co.x, co.y, co.z + h * t)))


# ---------------------------------------------------------------------------
# Naufrage
# ---------------------------------------------------------------------------

def radeau_epave():
    m = M("radeau_epave", (14, 4, 12), "Radeau disloqué", "Planches écartées, mât cassé, voile déchirée", grime=True)
    pl, mt, vo, to = m.part("Planches"), m.part("Mat"), m.part("Voile"), m.part("Tonneaux")
    rng = random.Random(3)
    for i in range(9):
        x = -5.5 + i * 1.35 + rng.uniform(-0.3, 0.3)
        pl.box(0.9, 8.5 + rng.uniform(-2, 1), 0.3, at=(x, rng.uniform(-1, 1), 0.2), rot=(rng.uniform(-3, 3), rng.uniform(-4, 4), rng.uniform(-14, 14)),
               c=rng.choice(["wood_old", "wood", "pallet"]), bev=0.06, deform=m.noise(0.05, i))
    for k, (x, y, a) in enumerate(((-4.5, 4.5, 50), (5.5, -4.6, -35), (0.5, 5.2, 80))):
        pl.box(0.8, 3.0, 0.25, at=(x, y, 0.15), rot=(0, 0, a), c="wood_old", bev=0.05)
    mt.cyl(0.2, 3.2, at=(0.5, 0.5, 0.35), rot=(0, 55, 15), c="wood", segs=8, bev=0)  # mât cassé penché
    mt.cyl(0.22, 0.9, at=(0.5, 0.5, 0.3), c="wood", segs=8, bev=0, deform=m.noise(0.08, 9))  # moignon
    mt.cyl(0.12, 4.5, at=(-1.5, -2.5, 0.45), rot=(0, 90, 20), c="wood_old", segs=6, bev=0)  # vergue tombée
    for x, y in ((-3.5, -3.5), (3.5, 3.0), (-1.0, 3.6), (4.6, -1.8)):  # cordes qui pendent par-dessus bord
        mt.pipe([(x, y, 0.4), (x * 1.1, y * 1.12, 0.3), (x * 1.18, y * 1.22, 0.0)], 0.06, c="jute", sides=4)
    mt.pipe([(0.5, 0.5, 1.0), (1.5, 1.0, 0.6), (2.5, 1.2, 0.4)], 0.05, c="jute", sides=4)
    tear = [(0, 0), (3.6, -0.2), (4.2, 1.0), (3.0, 1.4), (3.8, 2.3), (2.0, 2.0), (1.2, 2.8), (0.3, 1.5)]
    vo.prism(tear, 0.05, at=(-0.8, -0.6, 0.0), rot=(0, 52, 10), plane="XZ", c="cream", deform=m.noise(0.08, 11))
    vo.prism([(0, 0), (2.4, 0.2), (1.8, 1.2), (0.4, 0.9)], 0.05, at=(-5.0, 1.0, 0.42), rot=(90, 0, 30), plane="XZ", c="beige")  # lambeau à plat
    vo.decal(0.9, 0.7, (1.0, -0.68, 1.6), c="fabric_blue", rot=(0, 52, 10), t=0.04, seed=12)
    barrel(to, 4.5, 1.5, 0.75, (0, 90, 30), c="wood_dark")
    barrel(to, -4.0, -1.0, 0.75, (90, 0, 70), c="wood")
    return m


def rocher_recif():
    m = M("rocher_recif", (16, 6, 12), "Rochers de récif", "À fleur d'eau", grime=True)
    ro, al = m.part("Rochers"), m.part("Algues")
    rng = random.Random(4)
    rocks = [(0, 0, 3.0, 5.5), (-4.5, 1.5, 2.6, 3.2), (4.8, -1.0, 2.8, 3.8), (-2.0, -3.6, 2.0, 2.2), (2.5, 3.6, 2.2, 2.6), (-6.2, -1.8, 1.4, 1.5), (6.4, 2.6, 1.3, 1.6)]
    for k, (x, y, r, h) in enumerate(rocks):
        ro.sphere(r, at=(x, y, 0), c=("grey", "slate", "concrete_dark")[k % 3], segs=8, rings=6, scale=(1.2, 1.0, h / r),
                  deform=lambda co, k=k: m.noise(0.35, 20 + k)(Vector((co.x, co.y, max(co.z, -0.3)))))
    for k in range(18):
        x, y = rng.uniform(-6, 6), rng.uniform(-4, 4)
        z = rng.uniform(0.2, 1.4)
        al.pipe([(x, y, z), (x + 0.2, y - 0.1, z + 0.6), (x - 0.1, y, z + 1.1)], 0.08, c=("leaf_dark", "olive", "mint")[k % 3], sides=3)
    for k in range(10):
        x, y = rng.uniform(-6, 6), rng.uniform(-4, 4)
        al.lathe([(0, 0), (0.25, 0), (0, 0.45)], segs=6, at=(x, y, rng.uniform(0.3, 2.5)), rot=(rng.uniform(-60, 60), rng.uniform(-60, 60), 0),
                 c=("peach", "cream", "flower_pink")[k % 3])
    for k in range(6):
        al.sphere(0.2, at=(rng.uniform(-5, 5), rng.uniform(-3, 3), rng.uniform(1, 4)), c="navy_paint", segs=5, rings=3, scale=(1, 1, 0.5))  # moules
    return m


def debris_plage():
    m = M("debris_plage", (10, 1, 10), "Débris de plage", "À poser sur le sable", grime=True)
    pl, co, to = m.part("Planches"), m.part("Cordes"), m.part("Tonneau")
    for k, (x, y, a, L) in enumerate(((-3, 2, 20, 4.5), (2.5, 3.0, -50, 3.5), (-1, -3, 70, 5.0), (3.5, -2.5, 10, 2.5))):
        pl.box(0.8, L, 0.22, at=(x, y, 0.11 + 0.2 * (k == 2)), rot=(0, 0, a), c=("wood_old", "wood", "pallet", "wood_old")[k], bev=0.05,
               deform=m.noise(0.04, k))
    co.pipe([(-4.5, -1, 0.06), (-3, -0.2, 0.06), (-2, -1.5, 0.06), (-0.5, -0.8, 0.06), (0.5, 0.6, 0.06), (1.8, 0.0, 0.06)], 0.07, c="jute", sides=4)
    barrel(to, 2.8, 1.2, 0.8, (90, 0, 20), c="wood")  # tonneau couché
    to.decal(0.25, 1.4, (2.95, 0.55, 1.62), c="soot", rot=(90, 0, 20), t=0.06, seed=31)  # fente
    return m


# ---------------------------------------------------------------------------
# Événements météo
# ---------------------------------------------------------------------------

def tornade():
    m = M("tornade", (30, 70, 30), "Tornade", "Entonnoir et débris séparés")
    e, d = m.part("Entonnoir"), m.part("Debris")
    prof = [(0, 0), (2.0, 0), (1.6, 6), (2.8, 18), (5, 32), (8.5, 48), (12.5, 62), (14.5, 70), (0, 70)]
    e.lathe(prof, segs=14, c="grey", deform=lambda co: Vector((co.x + 1.5 * math.sin(co.z / 9), co.y + 1.0 * math.cos(co.z / 11), co.z)))
    hel = []
    for i in range(70):
        z = i
        r = 1.8 + (i / 70) ** 1.6 * 12.5
        a = i * 0.45
        hel.append((r * math.cos(a) + 1.5 * math.sin(z / 9) + 0, r * math.sin(a) + 1.0 * math.cos(z / 11), z))
    e.pipe(hel[2:68], 0.5, c="grey_light", sides=4)
    rng = random.Random(6)
    for k in range(18):
        z = rng.uniform(8, 64)
        r = 2.5 + (z / 70) ** 1.6 * 13
        a = rng.uniform(0, 2 * math.pi)
        x, y = r * math.cos(a) * 1.05, r * math.sin(a) * 1.05
        if k % 2:
            d.box(0.6, 3.0, 0.2, at=(x, y, z), rot=(rng.uniform(0, 90), rng.uniform(0, 90), rng.uniform(0, 90)), c="wood_old", bev=0.04)
        else:
            d.prism([(-0.6, 0), (0, -0.4), (0.6, 0), (0, 0.9)], 0.05, at=(x, y, z), rot=(rng.uniform(0, 90), rng.uniform(0, 90), 0), c=("leaf", "orange")[k % 4 == 0])
    return m


def nuage_orage():
    m = M("nuage_orage", (60, 15, 40), "Nuage d'orage")
    n = m.part("Nuage")
    rng = random.Random(7)
    puffs = [(0, 0, 7, 9), (-14, 3, 6, 7.5), (14, -2, 6, 8), (-25, 0, 4.5, 5.5), (25, 2, 4.5, 5.5), (-7, -9, 6, 6), (8, 9, 6, 6.5), (-5, 10, 8.5, 5)]
    for k, (x, y, z, r) in enumerate(puffs):
        n.sphere(r, at=(x, y, z), c=("grey_dark", "slate")[k % 2], segs=12, rings=8, scale=(1.3, 1.1, 0.85), deform=m.noise(0.3, k))
    for k, (x, y) in enumerate(((-16, 0), (0, -4), (16, 2), (-6, 8), (8, -10))):
        n.sphere(7, at=(x, y, 3.2), c="purple", segs=10, rings=6, scale=(1.4, 1.2, 0.35))
    return m


def soleil():
    m = M("soleil_canicule", (20, 20, 4), "Soleil caniculaire", "Face vers -Z, lunettes de soleil")
    s, r = m.part("Soleil"), m.part("Rayons")
    C = 10.0
    s.cyl(6.5, 2.4, at=(0, 1.2, C), rot=(90, 0, 0), c="orange", segs=20, bev=0.6)
    s.cyl(5.6, 0.3, at=(0, -1.15, C), rot=(90, 0, 0), c="flower_yellow", segs=20, bev=0.1)
    for sx in (-1, 1):  # lunettes
        s.box(3.6, 0.3, 2.0, at=(sx * 2.0, -1.5, C + 1.2), c="black", bev=0.5)
        s.box(0.8, 0.31, 0.6, at=(sx * 2.5, -1.62, C + 1.6), rot=(0, 20, 0), c="grey_light", bev=0.1)
    s.box(1.2, 0.3, 0.3, at=(0, -1.5, C + 1.6), c="black", bev=0.08)
    smile = [(4.0 * math.cos(math.radians(a)), C - 1.0 + 2.2 * math.sin(math.radians(a))) for a in range(200, 341, 20)]
    for (x0, z0), (x1, z1) in zip(smile, smile[1:]):
        s.rod((x0, -1.35, z0), (x1, -1.35, z1), 0.25, c="red_dark", sides=4)
    for k in range(12):
        a = 2 * math.pi * k / 12
        L = 3.4 if k % 2 == 0 else 2.6
        r.prism([(-1.0, 0), (1.0, 0), (0, L)], 1.2, at=(6.6 * math.cos(a), 0, C + 6.6 * math.sin(a)), rot=(0, -math.degrees(a) + 90, 0), c="flame_orange", bev=0.15)
    return m


def thermometre():
    m = M("thermometre_geant", (4, 16, 2), "Thermomètre géant", "Liquide séparé, pivot en bas : étirer en Y pour le faire monter")
    t, l = m.part("Thermometre"), m.part("Liquide", pivot=(0, 0, 1.6))
    t.boxb(4, 2, 0.5, 0, 0, 0, c="red_dark", bev=0.12)
    t.boxb(2.6, 0.6, 14.5, 0, 0.6, 0.5, c="white", bev=0.2)
    t.lathe([(0, 0), (0.75, 0.3), (0.9, 1.0), (0.6, 1.8), (0.5, 2.0), (0.5, 14.8), (0.35, 15.2), (0, 15.3)], segs=10, at=(0, -0.15, 0.6),
            c="glass")
    for k in range(13):
        t.boxb(0.7 if k % 2 == 0 else 0.4, 0.1, 0.08, 0.95 + (0 if k % 2 == 0 else -0.15), 0.25, 3.0 + k * 0.95, c="black", bev=0)
    l.sphere(0.75, at=(0, -0.15, 1.6), c="light_red", segs=10, rings=7)
    l.cyl(0.35, 12.8, at=(0, -0.15, 2.0), c="light_red", segs=8, bev=0)
    return m


def fissure():
    m = M("fissure_sol", (20, 1, 6), "Fissure de séisme")
    f, ro = m.part("Fissure"), m.part("Rochers")
    zig = [(-10, 0.3), (-7, -0.4), (-4, 0.6), (-1, -0.3), (2, 0.5), (5, -0.5), (8, 0.4), (10, 0.0)]
    top = [(-10, 3)] + [(x, y + 0.5) for x, y in zig[::-1]][::-1] + [(10, 3)]
    a_side = [(-10, 3), (10, 3)] + [(x, y + 0.5) for x, y in zig[::-1]]
    b_side = [(x, y - 0.5) for x, y in zig] + [(10, -3), (-10, -3)]
    f.prism(a_side, 0.5, at=(0, 0, 0.25), plane="XY", c="mud", deform=m.noise(0.06, 1))
    f.prism(b_side, 0.5, at=(0, 0, 0.25), plane="XY", c="mud", deform=m.noise(0.06, 2))
    f.prism([(x, y + 0.5) for x, y in zig] + [(x, y - 0.5) for x, y in zig[::-1]], 0.1, at=(0, 0, 0.02), plane="XY", c="soot")
    rng = random.Random(8)
    for k in range(10):
        x = rng.uniform(-9, 9)
        ro.box(rng.uniform(0.4, 0.9), rng.uniform(0.4, 0.8), rng.uniform(0.3, 0.7), at=(x, rng.uniform(-2.5, 2.5), 0.75),
               rot=(rng.uniform(0, 40), rng.uniform(0, 40), rng.uniform(0, 90)), c=("concrete", "grey", "soil")[k % 3], bev=0.08)
    return m


def meteorite():
    m = M("meteorite", (8, 8, 8), "Météorite", "Roche et lave séparées")
    r, l = m.part("Roche"), m.part("Lave")
    r.sphere(3.9, at=(0, 0, 4), c="char", segs=12, rings=9, deform=m.noise(0.35, 3))
    for k in range(5):
        a0 = k * 1.3
        pts = []
        for i in range(8):
            t = -0.9 + i * 0.25
            ang = a0 + t * 0.6
            pts.append((4.05 * math.cos(ang) * math.cos(t), 4.05 * math.sin(ang) * math.cos(t), 4 + 4.05 * math.sin(t)))
        l.pipe(pts, 0.22, c="flame_orange", sides=4)
    for k in range(4):
        l.sphere(0.6, at=(3.6 * math.cos(k * 1.6), 3.6 * math.sin(k * 1.6), 4 + (k - 1.5) * 1.5), c="ember", segs=6, rings=4)
    return m


def cratere():
    m = M("cratere", (20, 3, 20), "Cratère d'impact", "Fumant", grime=True)
    c, ro = m.part("Cratere"), m.part("Rochers")
    c.torus(8.2, 1.8, at=(0, 0, 0.6), c="soil", segs=20, sides=8, sz=0.7, deform=m.noise(0.3, 1))
    c.cyl(7.5, 0.3, c="soot", segs=20, bev=0)
    c.cyl(4.0, 0.32, c="char", segs=14, bev=0)
    for k in range(5):
        c.sphere(1.0 + 0.2 * k, at=(0.6 * math.cos(k), 0.6 * math.sin(k), 0.8 + k * 0.45), c="grey_light", segs=7, rings=5, scale=(1, 1, 0.6))
    rng = random.Random(9)
    for k in range(14):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(8.5, 9.6) if k % 2 else rng.uniform(2, 6)
        ro.box(rng.uniform(0.4, 1.0), rng.uniform(0.4, 0.9), rng.uniform(0.3, 0.7), at=(rr * math.cos(a), rr * math.sin(a), 0.6 + (k % 2) * 0.5),
               rot=(rng.uniform(0, 40), rng.uniform(0, 40), rng.uniform(0, 90)), c=("ash", "concrete_dark", "char")[k % 3], bev=0.08)
    return m


def vague():
    m = M("vague_geante", (60, 30, 15), "Vague géante", "Déferle vers -Z")
    v, e = m.part("Vague"), m.part("Ecume")
    prof = [(7.5, 0), (5, 6), (3, 13), (2.0, 19), (2.5, 24), (0.5, 28), (-3.5, 30), (-7.5, 28.5), (-7.5, 26), (-4.5, 26.5), (-2.8, 23.5), (-3.0, 18), (-4.5, 11),
            (-6.5, 5), (-7.5, 0)]
    v.prism([(-y, z) for y, z in prof], 58, at=(0, 0, 0), plane="YZ", c="blue",
            deform=lambda co: Vector((co.x, co.y + 1.2 * math.sin(co.x / 6), co.z * (1 - 0.15 * (abs(co.x) / 29) ** 2))))
    v.prism([(-y * 0.9 + 0.5, z * 0.85) for y, z in prof[:6]] + [(4, 0)], 58.5, at=(0, 0, 0), plane="YZ", c="sky")
    for k in range(20):
        x = -28 + k * 2.95
        zc = 29.5 * (1 - 0.15 * (abs(x) / 29) ** 2)
        e.sphere(1.6, at=(x, -0.5 + 1.2 * math.sin(x / 6), zc), c="white", segs=8, rings=5, deform=m.noise(0.2, k))
        e.sphere(1.0, at=(x + 1.2, 6.0 + 1.2 * math.sin(x / 6), zc * 0.88 - 1.5), c="white", segs=6, rings=4)
    for k in range(12):
        x = -27 + k * 4.9
        e.sphere(1.3, at=(x, 7.0, 0.8), c="white", segs=6, rings=4, scale=(1.4, 1, 0.6))
    return m


def bloc_glace():
    m = M("bloc_glace", (8, 6, 8), "Bloc de glace", "Glace et givre séparés")
    g, gv = m.part("Glace"), m.part("Givre")
    g.box(7.6, 7.6, 5.6, at=(0, 0, 2.8), c="glass", bev=0.6, deform=m.noise(0.25, 1))
    g.box(3.5, 3.0, 2.5, at=(1.5, -1.5, 4.8), rot=(10, 8, 20), c="sky", bev=0.3, deform=m.noise(0.15, 2))
    rng = random.Random(10)
    for k in range(12):  # stalactites sur les bords
        a = k * math.pi / 6
        x, y = 3.7 * math.cos(a), 3.7 * math.sin(a)
        gv.lathe([(0, 0), (0.28, 0), (0, -1.3)], segs=5, at=(x, y, 5.0), c="white", cap0=True)
    gv.box(7.9, 7.9, 0.3, at=(0, 0, 5.75), c="white", bev=0.15, deform=m.noise(0.15, 3))
    return m


def arc_en_ciel():
    m = M("arc_en_ciel", (60, 30, 4), "Arc-en-ciel")
    a = m.part("Arc")
    cols = ["red", "orange", "flower_yellow", "lettuce", "blue", "purple"]
    R0 = 26.5
    for i, c in enumerate(cols):
        R = R0 - i * 2.3
        pts = [(R * math.cos(math.radians(t)), 0, 1.0 + R * math.sin(math.radians(t))) for t in range(0, 181, 9)]
        a.pipe(pts, 1.3, c=c, sides=6)
    for s in (-1, 1):
        for k, (dx, dz, r) in enumerate(((0, 0.8, 2.6), (2.4, 0.3, 2.0), (-2.4, 0.4, 2.1), (0.5, 2.4, 1.8))):
            a.sphere(r, at=(s * 20.7 + dx, 0, dz), c="white", segs=10, rings=7, scale=(1, 0.8, 0.8))
    return m


def sirene():
    m = M("sirene_alerte", (4, 10, 4), "Sirène d'alerte")
    p, s, g = m.part("Poteau"), m.part("Sirene"), m.part("Gyrophare")
    p.boxb(2.0, 2.0, 0.3, c="concrete", bev=0.06)
    p.cyl(0.22, 7.6, at=(0, 0, 0.3), c="galva", segs=8, bev=0)
    p.boxb(0.8, 0.5, 1.0, 0, 0.3, 2.5, c="yellow_dark", bev=0.06)  # boîtier
    s.cyl(0.5, 1.0, at=(0, 0, 7.8), c="grey_light", segs=10, bev=0.08)
    for a in (0, 90, 180, 270):
        s.lathe([(0, 0), (0.3, 0), (0.35, 0.6), (0.9, 1.6), (0.82, 1.65), (0, 0.8)], segs=10, at=(0, 0, 8.3), rot=(90, 0, a), c="grey_light",
                cap0=False, cap1=False)
    g.cyl(0.42, 0.15, at=(0, 0, 8.8), c="black", segs=10, bev=0)
    g.lathe([(0, 0), (0.38, 0), (0.38, 0.7), (0.2, 1.0), (0, 1.05)], segs=10, at=(0, 0, 8.95), c="light_amber")
    return m


def ecran_meteo():
    m = M("ecran_meteo", (12, 10, 2), "Écran d'annonce météo", "Écran vierge")
    p, e = m.part("Pieds"), m.part("Ecran")
    for x in (-4.5, 4.5):
        p.boxb(0.5, 0.5, 3.5, x, 0.3, 0, c="black", bev=0.05)
        p.boxb(1.6, 2.0, 0.25, x, 0.3, 0, c="black", bev=0.05)
    p.boxb(12, 1.0, 6.5, 0, 0.2, 3.5, c="black", bev=0.15)
    for i in range(12):  # cadre rayé jaune et noir
        p.box(1.0, 1.04, 0.5, at=(-5.5 + i, 0.2, 9.75), c=("flower_yellow" if i % 2 else "black"), bev=0)
        p.box(1.0, 1.04, 0.5, at=(-5.5 + i, 0.2, 3.75), c=("flower_yellow" if i % 2 == 0 else "black"), bev=0)
    for s in (-1, 1):
        for i in range(5):
            p.box(0.5, 1.04, 1.1, at=(s * 5.75, 0.2, 4.55 + i * 1.1), c=("flower_yellow" if i % 2 else "black"), bev=0)
    e.boxb(10.8, 0.1, 5.2, 0, -0.35, 4.1, c="screen_dark", bev=0)
    return m


# ---------------------------------------------------------------------------
# Mutations des machines
# ---------------------------------------------------------------------------

def cristaux():
    m = M("cristaux_glace", (6, 3, 6), "Couronne de cristaux de glace", "Centre libre pour la machine")
    c = m.part("Cristaux")
    rng = random.Random(11)
    for k in range(14):
        a = 2 * math.pi * k / 14
        h = rng.uniform(1.6, 3.0)
        c.lathe([(0, 0), (0.45, 0), (0.35, h * 0.7), (0, h)], segs=5, at=(2.5 * math.cos(a), 2.5 * math.sin(a), 0),
                rot=(rng.uniform(-20, 20), rng.uniform(-20, 20), 0), c=("glass", "sky", "white")[k % 3])
    return m


def couronne():
    m = M("couronne_or", (3, 2, 3), "Couronne dorée")
    c = m.part("Couronne")
    c.lathe([(1.2, 0), (1.45, 0), (1.45, 0.8), (1.3, 0.8), (1.2, 0)], segs=16, c="gold", cap0=False, cap1=False)
    for k in range(8):
        a = 2 * math.pi * k / 8
        c.prism([(-0.4, 0), (0.4, 0), (0, 1.0)], 0.2, at=(1.35 * math.cos(a), 1.35 * math.sin(a), 0.8), rot=(0, 0, math.degrees(a) + 90), c="gold")
        c.sphere(0.12, at=(1.35 * math.cos(a), 1.35 * math.sin(a), 1.85), c="gold", segs=6, rings=4)
        c.sphere(0.13, at=(1.47 * math.cos(a), 1.47 * math.sin(a), 0.4), c=("light_red", "neon_blue")[k % 2], segs=6, rings=4)
    return m


def eclairs():
    m = M("eclairs_metal", (5, 5, 1), "Éclairs (mutation électrique)")
    e = m.part("Eclairs")
    bolt = [(0.3, 2.5), (1.3, 2.5), (0.7, 1.4), (1.3, 1.4), (-0.2, -0.0), (0.2, 1.0), (-0.4, 1.0)]
    for s, dx in ((1, -1.7), (-1, 1.7)):
        e.prism([(dx + s * x * 0.9, z * 1.9) for x, z in bolt][::s], 0.8, at=(0, 0, 0.1), c="flower_yellow", bev=0.08)
    return m


# ---------------------------------------------------------------------------
# Roue de la fortune (complète et en pièces détachées)
# ---------------------------------------------------------------------------

def socle_geo(p, z0=0.0, pillar=False, wheel_z=7.5):
    p.boxb(8, 5, 0.5, 0, 0, z0, c="red_dark", bev=0.1)
    p.box(7, 4, 2.0, at=(0, 0, z0 + 1.5), taper=(0.8, 0.8), c="red", bev=0.15)
    p.boxb(5.8, 3.4, 0.5, 0, 0, z0 + 2.5, c="gold", bev=0.1)
    for x in (-3.6, 3.6):
        p.sphere(0.3, at=(x, -2.3, z0 + 0.5), c="gold", segs=6, rings=4)
    if pillar:
        p.boxb(1.2, 1.0, wheel_z - 3.0, 0, 0.9, z0 + 3.0, c="red", bev=0.1)
        p.cyl(0.4, 1.0, at=(0, 0.9, wheel_z), rot=(90, 0, 0), c="gold", segs=10, bev=0.05)


def roue_geo(p, cx, cy, cz, R=3.5):
    cols = ["red", "flower_yellow", "blue", "green", "purple", "orange", "white", "teal"]
    p.cyl(R, 0.5, at=(cx, cy + 0.25, cz), rot=(90, 0, 0), c="wood_dark", segs=16, bev=0.06)
    n = 16
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        p.prism([(cx, cz), (cx + (R - 0.25) * math.cos(a0), cz + (R - 0.25) * math.sin(a0)), (cx + (R - 0.25) * math.cos(a1), cz + (R - 0.25) * math.sin(a1))],
                0.06, at=(0, cy - 0.28, 0), c=cols[k % len(cols)])
        p.cyl(0.08, 0.3, at=(cx + (R - 0.1) * math.cos(a0), cy - 0.25, cz + (R - 0.1) * math.sin(a0)), rot=(90, 0, 0), c="gold", segs=5, bev=0)
    p.torus(R, 0.15, at=(cx, cy, cz), rot=(90, 0, 0), c="gold", segs=24, sides=4, sz=3.0)
    p.cyl(0.8, 0.3, at=(cx, cy - 0.3, cz), rot=(90, 0, 0), c="gold", segs=12, bev=0.08)
    p.sphere(0.35, at=(cx, cy - 0.6, cz), c="gold", segs=8, rings=5)


def pointeur_geo(p, cx, cy, cz):
    p.prism([(cx - 0.45, cz + 1.6), (cx + 0.45, cz + 1.6), (cx, cz)], 0.4, at=(0, cy, 0), c="gold", bev=0.05)
    p.prism([(cx - 0.3, cz + 1.45), (cx + 0.3, cz + 1.45), (cx, cz + 0.35)], 0.45, at=(0, cy, 0), c="red")
    p.cyl(0.25, 0.5, at=(cx, cy - 0.0, cz + 1.75), rot=(90, 0, 0), c="gold", segs=8, bev=0.03, deform=lambda co: Vector((co.x, co.y + 0.25, co.z)))


def pupitre_geo(p, cx, cy, z0=0.0):
    p.boxb(2.0, 2.0, 0.3, cx, cy, z0, c="wood_black", bev=0.06)
    p.box(1.4, 1.4, 3.0, at=(cx, cy, z0 + 1.8), taper=(0.85, 0.85), c="wood_red", bev=0.12)
    p.boxb(1.6, 0.05, 2.4, cx, cy - 0.66, z0 + 0.6, c="gold", bev=0.0)
    p.boxb(1.0, 0.06, 1.8, cx, cy - 0.68, z0 + 0.9, c="wood_red", bev=0.0)
    p.box(2.0, 1.6, 0.25, at=(cx, cy, z0 + 3.55), rot=(18, 0, 0), c="wood_red", bev=0.06)
    p.box(2.05, 1.65, 0.08, at=(cx, cy, z0 + 3.45), rot=(18, 0, 0), c="gold", bev=0)


def lumiere_geo(p, cx, cy, cz, R=3.9):
    p.torus(R, 0.18, at=(cx, cy, cz), rot=(90, 0, 0), c="gold", segs=24, sides=4, sz=2.6)
    for k in range(24):
        a = 2 * math.pi * k / 24
        p.sphere(0.22, at=(cx + R * math.cos(a), cy - 0.3, cz + R * math.sin(a)), c="light_warm", segs=6, rings=4)


def roue_fortune():
    m = M("roue_fortune", (8, 12, 5), "Roue de la fortune complète")
    WZ = 7.6
    socle_geo(m.part("Socle"), pillar=True, wheel_z=WZ)
    roue_geo(m.part("Roue", pivot=(0, 0.3, WZ)), 0, 0.3, WZ)
    lumiere_geo(m.part("Lumiere"), 0, 0.15, WZ)
    pointeur_geo(m.part("Pointeur"), 0, 0.0, WZ + 3.0)
    pupitre_geo(m.part("Pupitre"), 2.6, -1.4, 0.0)
    return m


def piece_socle():
    m = M("piece_roue_socle", (8, 3, 5), "Roue : socle seul")
    socle_geo(m.part("Socle"))
    return m


def piece_roue():
    m = M("piece_roue_roue", (7, 7, 1), "Roue : roue seule", "Pivot au centre de la base ; axe de rotation au centre du disque")
    roue_geo(m.part("Roue"), 0, 0, 3.5)
    return m


def piece_pointeur():
    m = M("piece_roue_pointeur", (1, 2, 1), "Roue : pointeur seul")
    pointeur_geo(m.part("Pointeur"), 0, 0, 0)
    return m


def piece_pupitre():
    m = M("piece_roue_pupitre", (2, 4, 2), "Roue : pupitre seul")
    pupitre_geo(m.part("Pupitre"), 0, 0, 0)
    return m


def piece_lumiere():
    m = M("piece_roue_lumiere", (8, 8, 1), "Roue : couronne d'ampoules seule")
    lumiere_geo(m.part("Lumiere"), 0, 0, 4.0)
    return m


MODELS = [
    ("385_radeau_epave", radeau_epave), ("386_rocher_recif", rocher_recif), ("387_debris_plage", debris_plage),
    ("388_tornade", tornade), ("389_nuage_orage", nuage_orage), ("390_soleil_canicule", soleil), ("391_thermometre_geant", thermometre),
    ("392_fissure_sol", fissure), ("393_meteorite", meteorite), ("394_cratere", cratere), ("395_vague_geante", vague),
    ("396_bloc_glace", bloc_glace), ("397_arc_en_ciel", arc_en_ciel), ("398_sirene_alerte", sirene), ("399_ecran_meteo", ecran_meteo),
    ("400_cristaux_glace", cristaux), ("401_couronne_or", couronne), ("402_eclairs_metal", eclairs),
    ("403_roue_fortune", roue_fortune), ("404_piece_roue_socle", piece_socle), ("405_piece_roue_roue", piece_roue),
    ("406_piece_roue_pointeur", piece_pointeur), ("407_piece_roue_pupitre", piece_pupitre), ("408_piece_roue_lumiere", piece_lumiere),
]
