"""37–46 : chantier."""
import math
import random

from lib import Model
from m_vehicules import cabin, wheel, arches, lights_front, lights_back

CAT = "05_chantier"


def cone():
    m = Model("cone_chantier", (1.2, 2, 1.2), CAT, "Cône de chantier")
    p = m.part("Cone")
    p.boxb(1.2, 1.2, 0.14, c="plastic_black", bev=0.05)
    p.lathe([(0, 0.14), (0.45, 0.14), (0.07, 1.96), (0.05, 2.0), (0, 2.0)], segs=12, c="orange", deform=m.noise(0.01, 1))
    for z0, z1 in ((0.8, 1.05), (1.35, 1.55)):
        r0 = 0.45 - (0.38 * (z0 - 0.14) / 1.82) + 0.012
        r1 = 0.45 - (0.38 * (z1 - 0.14) / 1.82) + 0.012
        p.lathe([(r0, z0), (r1, z1)], segs=12, c="white", cap0=False, cap1=False)
    p.decal(0.25, 0.3, (0.1, -0.37, 0.6), c="mud", rot=(-12, 0, 0), seed=2)
    return m


def fut_raye():
    m = Model("fut_raye", (2, 3, 2), CAT, "Fût rayé rouge et blanc")
    p = m.part("Fut")
    p.torus(0.82, 0.18, at=(0, 0, 0.18), c="rubber", segs=14, sides=6)
    bands = [0.2, 0.75, 1.15, 1.55, 1.95, 2.35, 2.6]
    for i, (z0, z1) in enumerate(zip(bands, bands[1:])):
        r0, r1 = 0.95 - 0.12 * (z0 / 2.6), 0.95 - 0.12 * (z1 / 2.6)
        p.lathe([(r0, z0), (r0 + 0.04, z0 + 0.04), (r1 + 0.04, z1 - 0.04), (r1, z1)], segs=14,
                c=("orange" if i % 2 == 0 else "white"), cap0=False, cap1=False, deform=m.noise(0.012, i))
    p.lathe([(0.84, 2.6), (0.6, 2.7), (0, 2.72)], segs=14, c="orange", cap0=False)
    p.pipe([(-0.25, 0, 2.68), (-0.25, 0, 2.85), (0.25, 0, 2.85), (0.25, 0, 2.68)], 0.05, c="orange", sides=4)
    p.cyl(0.88, 0.2, at=(0, 0, 0.2), c="orange", segs=14)
    p.decal(0.5, 0.4, (0.3, -0.93, 0.5), c="mud", seed=3)
    p.boxb(0.12, 0.12, 0.12, 0, 0, 2.7, c="metal_dark")
    lamp = m.part("Lampe")
    lamp.boxb(0.34, 0.2, 0.14, 0, 0, 2.78, c="plastic_black", bev=0.03)
    lamp.cyl(0.13, 0.08, at=(0, -0.1, 2.97), rot=(90, 0, 0), c="light_amber", segs=10, bev=0.02)
    lamp.boxb(0.3, 0.16, 0.06, 0, 0, 2.92, c="light_amber", bev=0.01)
    return m


def toilettes():
    m = Model("toilettes_chantier", (3.4, 7, 3.4), CAT, "Toilettes de chantier")
    p = m.part("Cabine")
    p.boxb(3.4, 3.4, 0.25, c="grey_dark")
    p.boxb(3.15, 3.15, 6.0, 0, 0.0, 0.25, c="blue", deform=m.noise(0.02, 1))
    for x in (-1.2, -0.6, 0.0, 0.6, 1.2):
        for s in (-1, 1):
            p.boxb(0.14, 0.14, 5.6, s * 1.6, x, 0.45, c="blue")
        p.boxb(0.14, 0.14, 5.6, x, 1.6, 0.45, c="blue")
    p.box(3.3, 3.3, 0.6, at=(0, 0, 6.5), taper=(0.75, 0.75), c="white", bev=0.1)
    p.cyl(0.14, 0.7, at=(1.1, 1.1, 6.2), c="plastic_black", segs=6)
    p.cyl(0.2, 0.08, at=(1.1, 1.1, 6.9), c="plastic_black", segs=6)
    p.decal(1.2, 0.9, (-1.66, 0.3, 3.2), c="pink", rot=(0, 0, 90), seed=2)  # tag abstrait
    p.decal(0.8, 1.1, (-1.66, -0.6, 2.4), c="yellow", rot=(0, 0, 90), seed=3)
    p.decal(1.4, 0.7, (0.5, 1.68, 0.8), c="mud", rot=(0, 0, 180), seed=4)
    p.cyl(0.15, 0.25, at=(-0.9, -0.6, 6.8), rot=(0, 90, 0), c="white", segs=8)  # rouleau de PQ oublié sur le toit
    d = m.part("Porte", pivot=(-1.35, -1.6, 0.3))
    d.boxb(2.7, 0.12, 5.4, 0, -1.6, 0.3, c="blue")
    d.boxb(2.3, 0.06, 0.3, 0, -1.68, 5.0, c="white")  # aération
    d.boxb(0.12, 0.12, 0.6, 1.0, -1.72, 2.6, c="plastic_black")
    d.boxb(0.3, 0.06, 0.15, 0.95, -1.7, 3.4, c="light_red", bev=0.01)  # « occupé »
    d.decal(0.9, 0.8, (-0.4, -1.67, 1.2), c="mud", seed=5)
    return m


def bungalow():
    m = Model("bungalow_chantier", (14, 7, 6), CAT, "Bungalow de chantier")
    b = m.part("Bungalow")
    for x in (-6.0, -2.0, 2.0, 6.0):
        for y in (-1.6, 2.2):
            b.boxb(0.9, 0.9, 0.6, x, y, 0, c="concrete", deform=m.noise(0.03, int(x + y * 3)))
    b.boxb(14.0, 5.0, 6.1, 0, 0.5, 0.6, c="cream", bev=0.1)
    for x in (-6.85, 6.85):
        for y in (-1.85, 2.85):
            b.boxb(0.3, 0.3, 6.3, x, y, 0.55, c="grey_dark", bev=0.04)
    b.boxb(14.0, 5.0, 0.25, 0, 0.5, 6.6, c="grey_dark")
    b.boxb(14.0, 5.0, 0.25, 0, 0.5, 0.55, c="grey_dark")
    for x in [i * 0.6 - 6.3 for i in range(22)]:
        if -5.2 < x < -2.2 or -1.0 < x < 2.0 or 3.4 < x < 5.6:
            continue
        b.boxb(0.16, 0.06, 5.6, x, -2.0, 0.85, c="cream", bev=0.02)
    for x in [i * 0.6 - 6.3 for i in range(22)]:
        b.boxb(0.16, 0.06, 5.6, x, 3.0, 0.85, c="cream", bev=0.02)
    for x in (-3.7, 0.5):  # fenêtres : cadre + grille anti-effraction
        b.boxb(2.6, 0.12, 2.3, x, -2.02, 3.0, c="grey_dark")
        for k in range(5):
            b.boxb(0.06, 0.06, 2.2, x - 1.0 + k * 0.5, -2.15, 3.05, c="metal_dark", bev=0)
    b.boxb(1.2, 0.8, 0.8, -6.0, -2.0, 4.6, c="white", bev=0.08)  # clim
    b.cyl(0.3, 0.05, at=(-6.0, -2.42, 5.0), rot=(90, 0, 0), c="metal_dark", segs=10, bev=0)
    b.decal(2.0, 0.9, (-6.0, -2.06, 1.4), c="rust", seed=6)
    b.decal(1.6, 0.8, (2.2, -2.06, 1.2), c="mud", seed=7)
    b.decal(0.9, 0.7, (-1.6, -2.07, 3.8), c="paper", seed=8)  # affiche déchirée
    # marches métalliques
    b.boxb(2.0, 0.9, 0.12, 4.5, -2.45, 0.55, c="galva")
    b.boxb(2.0, 0.9, 0.12, 4.5, -2.45, 0.05, c="galva")
    for x in (3.55, 5.45):
        b.boxb(0.1, 0.9, 0.7, x, -2.45, 0, c="galva", bev=0.01)
    b.pipe([(5.5, -2.85, 0.0), (5.5, -2.85, 1.6), (5.5, -2.05, 1.6)], 0.05, c="yellow", sides=4)
    v = m.part("Vitres")
    for x in (-3.7, 0.5):
        v.boxb(2.3, 0.06, 2.0, x, -2.05, 3.15, c="glass_dark", bev=0)
    v.decal(0.7, 0.6, (0.9, -2.09, 4.2), c="grey_light", t=0.02, seed=9)  # vitre fêlée (étoile)
    d = m.part("Porte", pivot=(3.9, -2.0, 0.7))
    d.boxb(1.6, 0.12, 4.2, 4.7, -2.02, 0.7, c="grey_light")
    d.boxb(1.2, 0.06, 0.8, 4.7, -2.1, 3.6, c="grey_dark")
    d.boxb(0.3, 0.12, 0.12, 5.2, -2.14, 2.6, c="metal_dark")
    lamp = m.part("Lampe")
    lamp.boxb(0.5, 0.35, 0.3, 4.7, -2.18, 5.4, c="plastic_black", bev=0.04)
    lamp.boxb(0.38, 0.1, 0.18, 4.7, -2.36, 5.42, c="light_warm", bev=0.02)
    return m


def palette():
    m = Model("palette", (4, 0.5, 4), CAT, "Palette")
    p = m.part("Palette")
    rng = random.Random(3)
    cols = ["pallet", "pallet", "wood_light", "wood_old"]
    for y in (-1.7, 0, 1.7):
        p.boxb(4.0, 0.5, 0.07, 0, y, 0, c=rng.choice(cols), bev=0.02)
        for x in (-1.7, 0, 1.7):
            p.boxb(0.5, 0.5, 0.26, x, y, 0.07, c="wood_light", bev=0.03)
        p.boxb(4.0, 0.5, 0.07, 0, y, 0.33, c=rng.choice(cols), bev=0.02)
    for i in range(5):
        x = -1.68 + i * 0.84
        if i == 3:  # planche cassée
            p.boxb(0.55, 2.2, 0.08, x, -0.9, 0.4, c="wood_old", bev=0.02, rot=(0, 0, 3))
            continue
        p.boxb(0.55, 4.0, 0.08, x, 0, 0.42, c=rng.choice(cols), bev=0.02)
    p.decal(0.8, 0.6, (-0.8, 0.6, 0.505), c="stain", rot=(90, 0, 0), t=0.01, seed=4)
    return m


def tuyau():
    m = Model("gros_tuyau", (16, 1, 1), CAT, "Gros tuyau béton/acier", None, "⌀1 × 16, couché selon X")
    p = m.part("Tuyau")
    prof = [(0.4, 0), (0.5, 0), (0.5, 16), (0.4, 16), (0.4, 0)]
    p.lathe(prof, segs=14, at=(-8, 0, 0.5), rot=(0, 90, 0), c="concrete", cap0=False, cap1=False)
    for x in (-7.6, 0.0, 7.6):
        p.lathe([(0.49, 0), (0.505, 0.02), (0.505, 0.4), (0.49, 0.42)], segs=14, at=(x - 0.2, 0, 0.5), rot=(0, 90, 0),
                c="rust", cap0=False, cap1=False)
    p.cyl(0.39, 0.6, at=(-8, 0, 0.5), rot=(0, 90, 0), c="soot", segs=12, bev=0)  # intérieur sombre
    p.cyl(0.39, 0.6, at=(7.4, 0, 0.5), rot=(0, 90, 0), c="soot", segs=12, bev=0)
    p.decal(2.5, 0.5, (-3.0, -0.48, 0.55), c="concrete_dark", rot=(0, 0, 0), seed=1)
    p.decal(1.6, 0.4, (3.5, -0.48, 0.3), c="rust", rot=(0, 0, 0), seed=2)
    return m


def briques():
    m = Model("tas_briques", (3, 1.5, 2), CAT, "Tas de briques")
    p = m.part("Briques")
    rng = random.Random(5)
    bw, bd, bh = 0.7, 0.34, 0.29
    def brick(x, y, z, rz=0, c=None, l=bw):
        p.box(l, bd, bh, at=(x, y, z + bh / 2), rot=(0, 0, rz), c=c or rng.choice(["brick", "brick", "brick_dark"]), bev=0.03)
    for layer in range(5):
        z = layer * bh
        n = 4 - layer // 2
        if layer % 2 == 0:
            for i in range(n):
                for j in range(4 - layer // 2):
                    brick(-1.05 + i * 0.72 + layer * 0.18, -0.55 + j * 0.36 + layer * 0.05, z)
        else:
            for i in range(n - 1):
                for j in range(2):
                    brick(-0.75 + i * 0.72 + layer * 0.12, -0.38 + j * 0.72, z, rz=90)
    brick(1.25, 0.7, 0, rz=35)
    brick(1.2, -0.75, 0, rz=-20, c="brick_dark", l=0.4)  # demi-brique
    brick(-1.25, 0.75, 0, rz=70)
    p.box(bw, bd, bh, at=(0.9, 0.85, 0.35), rot=(25, 0, 10), c="brick", bev=0.03)
    return m


def tour_eclairage():
    m = Model("tour_eclairage", (3, 12, 3), CAT, "Tour d'éclairage mobile")
    r = m.part("Remorque")
    r.boxb(2.4, 2.4, 0.25, 0, 0.1, 0.85, c="metal_dark")
    r.boxb(2.3, 2.1, 1.6, 0, 0.25, 1.1, c="yellow", bev=0.1)
    r.boxb(2.32, 0.06, 1.2, 0, -0.82, 1.3, c="metal_dark")  # grille
    r.decal(0.9, 0.6, (0.6, -0.84, 1.3), c="rust", seed=1)
    r.decal(1.0, 0.7, (-0.5, 1.32, 1.5), c="mud", rot=(0, 0, 180), seed=2)
    r.rod((-0.6, -1.0, 0.95), (0, -1.5, 0.8), 0.07, c="metal_dark", sides=4)
    r.rod((0.6, -1.0, 0.95), (0, -1.5, 0.8), 0.07, c="metal_dark", sides=4)
    r.cyl(0.12, 0.1, at=(0, -1.5, 0.72), c="metal_dark", segs=8)
    for sx in (-1, 1):
        for sy in (-1, 1):
            r.rod((sx * 1.1, sy * 1.0 + 0.1, 0.95), (sx * 1.4, sy * 1.35 + 0.1, 0.1), 0.06, c="yellow_dark", sides=4)
            r.boxb(0.3, 0.3, 0.08, sx * 1.35, sy * 1.3 + 0.1, 0, c="metal_dark")
    for sx in (-1, 1):
        r.cyl(0.45, 0.3, at=(sx * 1.05, 0.2, 0.45), rot=(0, 90 * sx, 0), c="rubber", segs=12, bev=0.08)
        r.boxb(0.35, 1.0, 0.1, sx * 1.15, 0.2, 0.95, c="metal_dark")
    mast = m.part("Mat")
    mast.cyl(0.22, 4.0, at=(0, 0.7, 2.7), c="galva", segs=8, bev=0.02)
    mast.cyl(0.17, 3.0, at=(0, 0.7, 6.6), c="galva", segs=8, bev=0.02)
    mast.cyl(0.12, 1.8, at=(0, 0.7, 9.5), c="galva", segs=8, bev=0.02)
    mast.boxb(2.9, 0.2, 0.18, 0, 0.7, 11.2, c="metal_dark")
    mast.boxb(2.9, 0.2, 0.18, 0, 0.7, 10.3, c="metal_dark")
    mast.boxb(0.2, 0.2, 1.1, 0, 0.7, 10.3, c="metal_dark")
    pr = m.part("Projecteurs")
    hs = m.part("Boitiers")
    for x in (-1.05, 1.05):
        for z in (10.55, 11.45):
            hs.boxb(0.75, 0.4, 0.55, x, 0.45, z - 0.27, c="plastic_black", bev=0.05)
            pr.boxb(0.6, 0.06, 0.42, x, 0.23, z - 0.21, c="light_white", bev=0.01)
    return m


def toupie():
    W, H, L = 7, 9, 22
    m = Model("camion_toupie", (W, H, L), CAT, "Camion toupie béton")
    ch = m.part("Chassis")
    ch.boxb(1.8, 19.6, 0.6, 0, 0.6, 1.0, c="iron")
    ch.boxb(6.0, 0.5, 0.6, 0, -10.6, 0.9, c="plastic_black")
    for s in (-1, 1):
        ch.boxb(0.15, 8.0, 1.3, s * 2.95, 5.3, 1.2, c="yellow_dark")  # garde-boue / protections latérales
    ch.boxb(1.4, 2.0, 1.2, 2.4, -2.6, 1.1, c="metal")  # réservoir d'eau
    ch.cyl(0.55, 1.8, at=(-2.3, -3.6, 1.8), rot=(-90, 0, 0), c="white", segs=10)
    for z in (1.0, 2.2, 3.4, 4.6):  # échelle arrière
        ch.rod((1.5, 10.3, z), (2.1, 10.3, z), 0.04, c="metal_dark", sides=4)
    for x in (1.5, 2.1):
        ch.rod((x, 10.3, 0.9), (x, 10.0, 6.5), 0.05, c="metal_dark", sides=4)
    ch.boxb(1.2, 0.3, 4.6, 0, -4.4, 1.6, c="yellow_dark")  # support avant toupie
    ch.boxb(2.6, 0.5, 4.4, 0, 8.0, 1.6, c="yellow_dark")  # support arrière
    cab = m.part("Cabine")
    g = m.part("Vitres")
    cab.box(6.4, 4.4, 3.4, at=(0, -8.4, 1.5 + 1.7), c="orange", bev=0.35, deform=m.noise(0.04, 1))
    cabin(cab, g, 6.2, 4.0, 2.6, -8.3, 4.9, 0.95, 0.85, "orange", pillar=False)
    cab.boxb(4.0, 0.1, 1.4, 0, -10.62, 1.9, c="metal_dark")
    for s in (-1, 1):
        cab.boxb(0.2, 0.5, 1.2, s * 3.35, -9.3, 5.2, c="plastic_black")
    cab.decal(1.5, 0.8, (3.21, -8.2, 2.2), c="concrete", rot=(0, 0, 90), seed=2)  # béton séché
    cab.decal(1.2, 0.6, (-3.21, -7.6, 2.6), c="concrete", rot=(0, 0, 90), seed=3)
    t = m.part("Toupie", pivot=(0, 1.8, 5.2))
    ang = 12
    prof = [(0, 0), (1.2, 0.0), (2.75, 3.6), (2.75, 7.2), (1.4, 11.4), (1.0, 11.8), (0, 11.8)]
    t.lathe(prof, segs=16, at=(0, -4.2, 3.6), rot=(-90 + ang, 0, 0), c="white", deform=m.noise(0.03, 4))
    import math as _m
    hel = []
    for k in range(36):
        a = k / 36 * 2 * _m.pi * 2.0
        z = 0.5 + k / 35 * 10.8
        r = min(2.78, 1.25 + z * 0.43) if z < 3.6 else (2.78 if z < 7.2 else 2.78 - (z - 7.2) * 0.33)
        hel.append((r * _m.cos(a), r * _m.sin(a), z))
    t.pipe(hel, 0.12, c="red", sides=4, at=(0, -4.2, 3.6), rot=(-90 + ang, 0, 0))
    t.decal(2.0, 1.4, (2.0, 1.5, 6.6), c="concrete_dark", rot=(0, 0, 70), t=0.4, seed=5)
    goul = m.part("Goulotte")
    goul.box(1.6, 1.6, 1.0, at=(0, 8.3, 6.6), taper=(1.5, 1.5), c="yellow_dark", bev=0.05)  # trémie
    goul.box(0.9, 2.6, 0.12, at=(0.6, 10.2, 5.2), rot=(-25, 0, 20), c="metal", bev=0.02)  # goulotte
    goul.box(0.1, 2.6, 0.35, at=(0.18, 10.2, 5.35), rot=(-25, 0, 20), c="metal", bev=0.01)
    lights_front(m, -10.66, (-2.4, 2.4), 2.1, r=0.35, shape="rect")
    lights_back(m, 10.6, (-2.7, 2.7), 1.2, w=0.5, h=0.3)
    for name, x, y in (("Roue_AvG", 2.8, -7.0), ("Roue_AvD", -2.8, -7.0), ("Roue_Av2G", 2.8, -4.6), ("Roue_Av2D", -2.8, -4.6),
                       ("Roue_Ar1G", 2.8, 5.3), ("Roue_Ar1D", -2.8, 5.3), ("Roue_Ar2G", 2.8, 7.8), ("Roue_Ar2D", -2.8, 7.8)):
        wheel(m, name, x, y, 1.2, 1.1, side=(1 if x > 0 else -1))
    return m


def lattice_box(p, x0, x1, y0, y1, z0, z1, step, chord=0.35, brace=0.08, c="yellow", vertical=True):
    """Treillis rectangulaire : 4 membrures + diagonales en zigzag sur les 4 faces."""
    if vertical:
        for x in (x0, x1):
            for y in (y0, y1):
                p.boxb(chord, chord, z1 - z0, x, y, z0, c=c, bev=0.05)
        n = max(1, round((z1 - z0) / step))
        for k in range(n):
            za, zb = z0 + (z1 - z0) * k / n, z0 + (z1 - z0) * (k + 1) / n
            faces = (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0)))
            for (a, b) in faces:
                if k % 2:
                    a, b = b, a
                p.rod((a[0], a[1], za), (b[0], b[1], zb), brace, c=c, sides=3)
                p.rod((a[0], a[1], za), (b[0], b[1], za), brace, c=c, sides=3)


def grue():
    m = Model("grue_tour", (74, 85, 4), CAT, "Grue à tour", None, "La plus grosse pièce")
    base = m.part("Mat")
    xm = -18.0  # axe du mât ; flèche vers +X, contre-flèche vers -X
    base.boxb(4.0, 4.0, 1.0, xm, 0, 0, c="concrete", bev=0.1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            base.boxb(1.0, 1.0, 1.2, xm + sx * 1.5, sy * 1.5, 0.6, c="concrete_dark", bev=0.08)  # lests
    lattice_box(base, xm - 1.8, xm + 1.8, -1.8, 1.8, 1.0, 70.0, 3.45, chord=0.4, brace=0.1)
    base.boxb(3.4, 3.4, 0.3, xm, 0, 70.0, c="yellow_dark")
    rot = m.part("PartieTournante", pivot=(xm, 0, 70.3))
    rot.cyl(1.9, 0.6, at=(xm, 0, 70.3), c="metal_dark", segs=12)
    rot.boxb(3.8, 3.8, 0.8, xm, 0, 70.9, c="yellow")
    # cabine du grutier (vitrée, côté avant)
    rot.boxb(2.0, 2.0, 2.2, xm + 2.5, -0.8, 70.6, c="yellow", bev=0.12)
    rot.boxb(0.6, 1.8, 0.4, xm + 2.5, -0.8, 72.8, c="white", bev=0.06)
    # porte-flèche (tête en A)
    for sy in (-1, 1):
        rot.rod((xm - 1.6, sy * 1.6, 71.7), (xm, sy * 0.4, 84.6), 0.2, c="yellow", sides=4)
        rot.rod((xm + 1.6, sy * 1.6, 71.7), (xm, sy * 0.4, 84.6), 0.2, c="yellow", sides=4)
    for z in (74.5, 77.5, 80.5):
        k = (z - 71.7) / 12.9
        rot.rod((xm - 1.6 * (1 - k), -1.6 * (1 - k) - 0.4 * k, z), (xm + 1.6 * (1 - k), -1.6 * (1 - k) - 0.4 * k, z), 0.08, c="yellow", sides=3)
        rot.rod((xm - 1.6 * (1 - k), 1.6 * (1 - k) + 0.4 * k, z), (xm + 1.6 * (1 - k), 1.6 * (1 - k) + 0.4 * k, z), 0.08, c="yellow", sides=3)
    rot.boxb(1.0, 1.0, 0.4, xm, 0, 84.6, c="red")
    rot.cyl(0.15, 0.25, at=(xm, 0, 84.75), c="light_red", segs=6, bev=0)
    # flèche : treillis triangulaire, de xm+1.8 à +37
    xa, xb = xm + 1.8, 37.0
    zt, zl = 74.2, 71.7
    for sy in (-1, 1):
        rot.boxb(xb - xa, 0.3, 0.3, (xa + xb) / 2, sy * 1.0, zl, c="yellow", bev=0.04)
    rot.boxb(xb - xa - 2, 0.3, 0.3, (xa + xb) / 2 - 1, 0, zt, c="yellow", bev=0.04)
    n = int((xb - xa) / 2.6)
    for k in range(n):
        x0 = xa + (xb - xa) * k / n
        x1 = xa + (xb - xa) * (k + 1) / n
        xmid = (x0 + x1) / 2
        for sy in (-1, 1):
            rot.rod((x0, sy * 1.0, zl), (xmid, 0, zt), 0.07, c="yellow", sides=3)
            rot.rod((xmid, 0, zt), (x1, sy * 1.0, zl), 0.07, c="yellow", sides=3)
        rot.rod((x0, -1.0, zl), (x0, 1.0, zl), 0.06, c="yellow", sides=3)
    rot.boxb(1.0, 2.3, 0.6, xb - 0.4, 0, zl - 0.2, c="yellow_dark")
    # tirants vers la tête
    rot.rod((xm, 0, 84.6), (xm + 22, 0, zt + 0.2), 0.07, c="metal_dark", sides=3)
    rot.rod((xm, 0, 84.6), (xm - 17, 0, 73.5), 0.07, c="metal_dark", sides=3)
    # contre-flèche + lests
    xc = -37.0
    for sy in (-1, 1):
        rot.boxb(xm - 1.8 - xc, 0.4, 0.6, (xc + xm - 1.8) / 2, sy * 1.2, 71.6, c="yellow", bev=0.05)
    for k in range(6):
        x = xm - 3 - k * 2.8
        rot.boxb(0.2, 2.8, 0.25, x, 0, 71.75, c="yellow_dark", bev=0.03)
    rot.boxb(16, 2.0, 0.08, (xc + xm - 1.8) / 2, 0, 72.0, c="galva", bev=0)  # passerelle
    for k in range(4):
        rot.boxb(1.3, 2.6, 3.0, xc + 1.0 + k * 1.4, 0, 69.0, c="concrete", bev=0.08)
    rot.boxb(2.0, 1.6, 1.4, xm - 6, 0, 72.0, c="metal_dark")  # treuil
    rot.decal(1.0, 0.8, (xc + 2.5, -1.32, 70.3), c="rust", seed=3)
    ch = m.part("Chariot", pivot=(12.0, 0, 71.4))
    ch.boxb(1.6, 2.4, 0.5, 12.0, 0, 70.9, c="metal_dark")
    for sy in (-1, 1):
        ch.cyl(0.2, 0.15, at=(11.6, sy * 1.0, 71.45), rot=(90, 0, 0), c="iron", segs=8, bev=0)
        ch.cyl(0.2, 0.15, at=(12.4, sy * 1.0, 71.45), rot=(90, 0, 0), c="iron", segs=8, bev=0)
    hk = m.part("Crochet", pivot=(12.0, 0, 70.9))
    for sx in (-0.25, 0.25):
        hk.rod((12.0 + sx, 0, 70.9), (12.0 + sx, 0, 52.0), 0.04, c="iron", sides=3)
    hk.boxb(1.0, 0.6, 1.0, 12.0, 0, 51.0, c="yellow", bev=0.1)
    hk.pipe([(12.0, 0, 51.0), (12.0, 0, 50.2), (12.0 + 0.45, 0, 49.7), (12.0 + 0.2, 0, 49.2), (11.75, 0, 49.5)], 0.13, c="metal_dark", sides=5)
    return m


MODELS = [
    ("37_cone_chantier", cone), ("38_fut_raye", fut_raye), ("39_toilettes_chantier", toilettes),
    ("40_bungalow_chantier", bungalow), ("41_palette", palette), ("42_gros_tuyau", tuyau), ("43_tas_briques", briques),
    ("44_tour_eclairage", tour_eclairage), ("45_camion_toupie", toupie), ("46_grue_tour", grue),
]
