"""1–16 : mobilier urbain. Coordonnées Blender en studs : X largeur, Y profondeur (avant = -Y), Z hauteur."""
import math

from lib import Model

CAT = "01_rue"


def ring_poly(r_out, r_in, a0=0, a1=180, n=8):
    outer = [(r_out * math.cos(math.radians(a0 + (a1 - a0) * i / n)), r_out * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    inner = [(r_in * math.cos(math.radians(a0 + (a1 - a0) * i / n)), r_in * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n, -1, -1)]
    return outer + inner


def lampadaire():
    m = Model("lampadaire", (1.4, 14.5, 2.6), CAT, "Lampadaire", 52)
    p = m.part("Poteau")
    y0 = 0.6
    p.cyl(0.7, 0.35, at=(0, y0, 0), c="concrete_dark", segs=8)
    p.cyl(0.55, 0.9, at=(0, y0, 0.35), r2=0.32, c="pole_green", segs=8)
    p.boxb(0.34, 0.05, 0.45, 0, y0 - 0.43, 0.5, c="pole_green", rot=(-14, 0, 0))  # trappe
    p.boxb(0.4, 0.03, 0.25, 0.05, y0 - 0.49, 0.45, c="rust", rot=(-14, 0, 0))
    p.torus(0.3, 0.07, at=(0, y0, 1.28), c="pole_green", segs=10, sides=4)
    p.cyl(0.22, 12.0, at=(0, y0, 1.25), r2=0.16, c="pole_green", segs=8, bev=0)
    p.boxb(0.2, 0.2, 0.7, 0.12, y0 - 0.1, 1.3, c="rust", rot=(0, 0, 30), bev=0.02)  # coulure de rouille
    p.boxb(0.3, 0.02, 0.5, 0.02, y0 - 0.2, 3.1, c="paper_dirty", rot=(0, 0, 4))  # vieille affichette
    p.torus(0.2, 0.05, at=(0, y0, 13.2), c="pole_green", segs=8, sides=4)
    arm = [(0, y0, 13.1), (0, y0, 13.85), (0, y0 - 0.2, 14.2), (0, y0 - 0.6, 14.32), (0, -0.55, 14.28), (0, -0.7, 14.1)]
    p.pipe(arm, 0.1, c="pole_green", sides=6)
    p.pipe([(0, y0, 13.3), (0, 0.1, 13.75), (0, -0.2, 14.25)], 0.05, c="pole_green", sides=4)
    h = m.part("TeteLampe")
    h.lathe([(0, 14.5), (0.14, 14.48), (0.25, 14.3), (0.62, 13.82), (0.66, 13.7), (0.6, 13.62), (0, 13.62)],
            segs=10, at=(0, -0.7, 0), c="lamp_grey", cap0=False, cap1=False)
    h.boxb(0.2, 0.08, 0.06, 0.25, -0.95, 14.0, c="rust", rot=(30, 0, 20))
    a = m.part("Ampoule")
    a.lathe([(0, 13.66), (0.5, 13.66), (0.44, 13.5), (0, 13.42)], segs=10, at=(0, -0.7, 0), c="light_warm", cap0=False, cap1=False)
    return m


def hood(p, cx, cz, y):
    p.prism(ring_poly(0.42, 0.36, -10, 190, 8), 0.28, at=(cx, y, cz), c="plastic_black", plane="XZ")


def feu_tricolore():
    m = Model("feu_tricolore", (1.4, 11, 1.2), CAT, "Feu tricolore", 12)
    p = m.part("Poteau")
    p.cyl(0.24, 0.3, at=(0, 0.42, 0), c="metal_dark", segs=8)
    p.cyl(0.15, 7.9, at=(0, 0.45, 0.3), c="metal", segs=8, bev=0)
    for z in (0.6, 1.0, 1.4):
        p.boxb(0.33, 0.33, 0.15, 0, 0.45, z, c="yellow", bev=0.02)  # bandes réfléchissantes usées
    p.boxb(0.2, 0.02, 0.35, 0, 0.29, 1.9, c="paper", rot=(0, 0, -6))  # autocollant
    b = m.part("Boitier")
    b.boxb(0.9, 0.7, 2.9, 0, 0, 8.0, c="yellow_dark")
    b.boxb(1.4, 0.06, 3.0, 0, 0.41, 7.95, c="plastic_black")
    b.boxb(1.0, 0.76, 0.1, 0, 0, 10.9, c="yellow_dark")
    for z in (8.5, 9.45, 10.4):
        b.cyl(0.36, 0.04, at=(0, -0.35, z), rot=(90, 0, 0), c="plastic_black", segs=12)
        hood(b, 0, z, -0.49)
    b.boxb(0.3, 0.05, 0.4, 0.3, -0.36, 8.1, c="rust", rot=(0, 0, 0))
    for name, z, c in (("Feu_Rouge", 10.4, "light_red"), ("Feu_Orange", 9.45, "light_amber"), ("Feu_Vert", 8.5, "light_green")):
        L = m.part(name)
        L.lathe([(0, 0), (0.3, 0), (0.3, 0.03), (0.2, 0.09), (0, 0.1)], segs=12, at=(0, -0.38, z), rot=(90, 0, 0), c=c,
                cap0=False, cap1=False)
    return m


def corbeille():
    m = Model("corbeille", (1.8, 2.6, 1.8), CAT, "Corbeille de rue", 24)
    p = m.part("Corbeille")
    dent = m.noise(0.035, 3)
    p.cyl(0.42, 0.3, at=(0, 0, 0), c="concrete_dark", segs=8)
    p.cyl(0.16, 0.5, at=(0, 0, 0.25), c="pole_green", segs=6, bev=0)
    def dents(co):
        co = dent(co)
        # gros coup de pied sur le devant
        if co.y < -0.6 and 1.0 < co.z < 1.7:
            co.y += 0.12 * (1 - abs(co.z - 1.35) / 0.35) * max(0, 1 - abs(co.x) / 0.5)
        return co
    p.tube_open(0.82, 1.9, 0.06, at=(0, 0, 0.6), c="pole_green", segs=14, r2=0.87, deform=dents)
    for z in (0.75, 2.42):
        p.torus(0.86 if z > 2 else 0.83, 0.05, at=(0, 0, z), c="pole_green", segs=14, sides=4)
    p.decal(0.5, 0.6, (0.25, -0.85, 1.9), c="rust", rot=(0, 0, 10), seed=1)
    p.decal(0.35, 0.4, (-0.55, -0.62, 1.15), c="rust_dark", rot=(0, 0, 40), seed=2)
    # déchets qui débordent
    p.box(0.55, 0.45, 0.35, at=(-0.2, 0.15, 2.4), c="paper_dirty", rot=(18, 12, 30), deform=m.noise(0.05, 4))
    p.cyl(0.11, 0.55, at=(0.35, -0.1, 2.1), rot=(25, -20, 0), c="green", segs=6)
    p.box(0.45, 0.3, 0.3, at=(0.25, 0.4, 2.35), c="cardboard", rot=(-25, 10, 15))
    p.sphere(0.32, at=(-0.35, -0.3, 2.3), c="bag_black", scale=(1.2, 1, 0.8), segs=6, rings=4, deform=m.noise(0.05, 5))
    return m


def benne():
    m = Model("benne", (6, 4, 3.4), CAT, "Benne à ordures", 40)
    p = m.part("Benne")
    dent = m.noise(0.04, 7)
    p.box(5.4, 2.6, 2.9, at=(0, 0.1, 0.55 + 1.45), c="green_dark", taper=(1.04, 1.2), deform=dent)
    p.boxb(5.5, 3.25, 0.18, 0, 0.1, 3.42, c="green_dark")  # rebord
    for x in (-2.0, -0.7, 0.7, 2.0):  # nervures avant
        p.box(0.22, 0.12, 2.75, at=(x, -1.38, 1.95), c="green_dark", rot=(-6, 0, 0))
    for x in (-2.8, 2.8):  # fourreaux de levage
        p.boxb(0.38, 1.6, 0.5, x, 0.1, 2.3, c="metal_dark")
    for k, (x, y, sx, sz, z) in enumerate(((-1.4, -1.43, 1.2, 0.8, 1.2), (1.4, -1.37, 0.8, 1.4, 1.5), (0.0, -1.3, 0.9, 0.5, 2.6))):
        p.decal(sx, sz, (x, y, z), c=("rust", "rust_dark", "rust_orange")[k], rot=(-6, 0, 0), seed=k)
    p.decal(1.3, 0.9, (-2.0, 1.72, 1.9), c="rust_dark", rot=(6, 0, 0), seed=7)
    p.boxb(0.8, 0.04, 0.5, 0.9, -1.36, 2.6, c="paper", rot=(-6, 0, 5))  # affiche arrachée
    for x in (-2.3, 2.3):
        for y in (-0.85, 1.05):
            p.boxb(0.5, 0.5, 0.12, x, y, 0.5, c="metal_dark")
            p.boxb(0.12, 0.35, 0.3, x - 0.14, y, 0.22, c="metal_dark")
            p.boxb(0.12, 0.35, 0.3, x + 0.14, y, 0.22, c="metal_dark")
            p.cyl(0.21, 0.14, at=(x - 0.07, y, 0.21), rot=(0, 90, 0), c="rubber", segs=8)
    # sac qui dépasse sous le couvercle
    p.sphere(0.5, at=(1.4, -0.9, 3.55), c="bag_black", scale=(1.2, 0.9, 0.55), segs=7, rings=4, deform=m.noise(0.05, 8))
    c = m.part("Couvercle", pivot=(0, 1.75, 3.62))
    c.box(5.7, 3.45, 0.2, at=(0.0, 0.03, 3.78), c="plastic_black", rot=(-4, 0, 0), deform=m.noise(0.02, 9))
    c.box(5.0, 2.6, 0.12, at=(0.0, 0.0, 3.9), c="plastic_black", rot=(-4, 0, 0))
    c.box(1.2, 0.2, 0.1, at=(-1.6, -1.6, 3.85), c="metal_dark", rot=(-4, 0, 0))
    c.box(1.2, 0.2, 0.1, at=(1.6, -1.6, 3.85), c="metal_dark", rot=(-4, 0, 0))
    c.box(0.5, 0.06, 0.18, at=(0, -1.72, 3.72), c="metal_dark")
    return m


def _sac(name, seed, variant):
    m = Model(name, (1.5, 1.3, 1.4), CAT, f"Sac poubelle {variant}", 200, "3 variantes (A/B/C)")
    p = m.part("Sac")
    nz = m.noise(0.05, seed)
    def body(co):
        co = nz(co)
        if co.z < -0.15:
            co.z = -0.15 + (co.z + 0.15) * 0.35
        return co
    if variant == "A":
        p.sphere(1.0, at=(0, 0, 0.62), c="bag_black", segs=12, rings=8, scale=(0.72, 0.66, 0.64), deform=body)
        p.lathe([(0.12, 1.05), (0.05, 1.18), (0.03, 1.22)], segs=6, c="bag_black", cap0=False)
        p.sphere(0.18, at=(-0.12, 0, 1.22), c="bag_shine", scale=(1.4, 0.6, 0.6), rot=(0, 30, 10), segs=6, rings=4)
        p.sphere(0.16, at=(0.14, 0.02, 1.2), c="bag_black", scale=(1.4, 0.6, 0.6), rot=(0, -40, -20), segs=6, rings=4)
    elif variant == "B":
        p.sphere(1.0, at=(0.05, 0, 0.6), c="bag_black", segs=12, rings=8, scale=(0.75, 0.68, 0.6), rot=(0, 12, 0), deform=body)
        p.lathe([(0.14, 1.0), (0.06, 1.12), (0.05, 1.2)], segs=6, at=(0.15, 0, 0), c="bag_black", cap0=False)
        p.sphere(0.2, at=(0.05, 0, 1.25), c="bag_black", scale=(1.6, 0.5, 0.5), rot=(0, 20, 0), segs=6, rings=4)
        p.sphere(0.14, at=(0.35, 0.05, 1.25), c="bag_shine", scale=(1.2, 0.5, 0.6), rot=(0, -50, 0), segs=6, rings=4)
    else:  # C : déchiré, déchets qui sortent
        p.sphere(1.0, at=(0, 0, 0.55), c="bag_black", segs=12, rings=8, scale=(0.74, 0.7, 0.5), rot=(0, 0, 20), deform=body)
        p.lathe([(0.1, 0.95), (0.05, 1.05), (0.04, 1.1)], segs=6, at=(-0.1, 0.05, 0), c="bag_black", cap0=False)
        p.sphere(0.15, at=(-0.1, 0.05, 1.12), c="bag_black", scale=(1.5, 0.6, 0.5), segs=6, rings=4)
        p.box(0.45, 0.06, 0.3, at=(0.35, -0.6, 0.45), c="paper", rot=(-20, 0, 25), deform=m.noise(0.04, 2))
        p.cyl(0.09, 0.32, at=(0.15, -0.62, 0.15), rot=(80, 0, 30), c="red", segs=6)
        p.box(0.3, 0.22, 0.04, at=(-0.35, -0.6, 0.3), c="cardboard", rot=(-50, 0, -20))
        p.sphere(0.12, at=(0.5, -0.45, 0.2), c="tomato", segs=6, rings=4)
    return m


def baril_feu():
    m = Model("baril_feu", (2.2, 3.2, 2.2), CAT, "Baril de feu", 5)
    p = m.part("Fut")
    dent = m.noise(0.03, 11)
    p.tube_open(1.0, 2.6, 0.05, at=(0, 0, 0), c="rust", segs=14, deform=dent)
    for z in (0.08, 0.9, 1.75, 2.55):
        p.torus(1.02, 0.05, at=(0, 0, z), c="rust_dark", segs=14, sides=4)
    p.decal(1.0, 0.6, (-0.2, -0.98, 1.35), c="red_dark", rot=(0, 0, 8), seed=3)  # reste de peinture
    p.decal(0.6, 0.5, (0.55, -0.8, 2.2), c="soot", rot=(0, 0, 35), seed=4)
    for x in (-0.6, 0.6):
        p.box(0.25, 1.6, 0.25, at=(x * 0.5, 0, 2.5), c="wood_black", rot=(20, 10 * x, 0))
    b = m.part("Braises")
    for a in range(0, 360, 60):
        x, y = math.cos(math.radians(a)) * 1.0, math.sin(math.radians(a)) * 1.0
        b.cyl(0.11, 0.06, at=(x * 0.99, y * 0.99, 0.45), rot=(90, 0, a + 90), c="ember", segs=6, bev=0)
    b.cyl(0.92, 0.06, at=(0, 0, 2.3), c="ember", segs=12, bev=0)
    f = m.part("Flammes")
    for (x, y, h, r, c) in ((0, 0, 1.0, 0.55, "flame_orange"), (0.35, 0.3, 0.75, 0.35, "flame_orange"),
                            (-0.4, 0.15, 0.85, 0.38, "flame_red"), (0.1, -0.35, 0.7, 0.33, "flame_red"),
                            (0.05, 0.0, 0.7, 0.32, "flame_yellow"), (-0.25, -0.25, 0.5, 0.22, "flame_yellow")):
        f.lathe([(0, 0), (r * 0.8, 0.1 * h), (r, 0.3 * h), (r * 0.6, 0.6 * h), (r * 0.2, 0.85 * h), (0, h)], segs=7,
                at=(x, y, 2.25), rot=(0, 0, x * 90), c=c, deform=m.noise(0.04 * h, int(10 * (x + y) + 50)))
    return m


def abribus():
    m = Model("abribus", (12, 9.3, 3.3), CAT, "Abribus")
    s = m.part("Structure")
    for x in (-5.85, 5.85):
        for y in (-1.45, 1.45):
            s.boxb(0.22, 0.22, 8.6, x, y, 0, c="steel_blue")
    for x in (-1.95, 1.95):
        s.boxb(0.18, 0.18, 8.6, x, 1.45, 0, c="steel_blue")
    s.boxb(11.9, 0.2, 0.25, 0, 1.45, 8.35, c="steel_blue")
    s.boxb(11.9, 0.2, 0.25, 0, 1.45, 0.3, c="steel_blue")
    for x in (-5.85, 5.85):
        s.boxb(0.2, 2.9, 0.25, x, 0, 8.35, c="steel_blue")
    s.boxb(0.5, 0.05, 1.2, -5.85 + 0.0, -1.58, 1.0, c="rust", rot=(0, 0, 0))
    s.boxb(0.6, 0.05, 0.9, 1.3, 1.6, 2.7, c="paper", rot=(0, 0, 5))  # affichettes collées derrière
    s.boxb(0.5, 0.05, 0.7, 2.6, 1.6, 3.4, c="pink", rot=(0, 0, -7))
    t = m.part("Toit")
    t.box(12.0, 3.3, 0.4, at=(0, 0, 8.9), rot=(-4, 0, 0), c="steel_blue")
    t.box(11.6, 2.9, 0.12, at=(0, 0, 9.12), rot=(-4, 0, 0), c="grey_dark")
    t.box(2.0, 1.4, 0.15, at=(-3.5, 0.2, 9.22), rot=(-4, 0, 12), c="mud", deform=m.noise(0.06, 3))  # feuilles mortes
    t.box(0.6, 0.5, 0.3, at=(3.8, -0.3, 9.25), rot=(-10, 5, 20), c="cardboard")
    v = m.part("Vitres")
    v.boxb(3.6, 0.06, 7.8, -3.9, 1.45, 0.55, c="glass", bev=0)
    v.boxb(3.6, 0.06, 7.8, 0, 1.45, 0.55, c="glass", bev=0)
    v.boxb(2.75, 0.06, 7.8, -5.85, 0, 0.55, c="glass", rot=(0, 0, 90), bev=0)
    # vitre cassée : éclats restant dans le cadre de droite
    v.prism([(-1.8, 0), (1.8, 0), (1.8, 2.6), (0.4, 1.4), (-0.7, 2.9), (-1.8, 1.8)], 0.06, at=(3.9, 1.45, 0.55), c="glass")
    v.prism([(1.8, 7.8), (-1.8, 7.8), (-1.8, 6.4), (-0.2, 6.9), (1.0, 5.9), (1.8, 6.6)], 0.06, at=(3.9, 1.45, 0.55), c="glass")
    b = m.part("Banc")
    for x in (-3.0, 3.0):
        b.boxb(0.2, 0.9, 1.5, x, 1.0, 0, c="metal_dark")
    b.boxb(7.0, 1.0, 0.18, 0, 0.95, 1.5, c="wood", rot=(-3, 0, 0))
    b.boxb(2.0, 1.02, 0.2, 2.2, 0.95, 1.5, c="wood_old", rot=(-3, 0, 6))  # planche rafistolée
    b.box(0.5, 0.3, 0.2, at=(-2.0, 0.8, 1.78), c="cardboard", rot=(0, 0, 25))
    h = m.part("PanneauHoraires")
    h.boxb(0.2, 1.6, 3.4, 5.85, -0.3, 2.2, c="steel_blue")
    h.boxb(0.1, 1.35, 2.9, 5.72, -0.3, 2.45, c="white")
    h.boxb(0.12, 0.6, 0.4, 5.7, 0.0, 3.6, c="yellow", rot=(5, 0, 0))  # post-it de travers
    return m


def plaque_egout():
    m = Model("plaque_egout", (2.6, 0.1, 2.6), CAT, "Plaque d'égout", 15)
    p = m.part("Plaque")
    p.cyl(1.3, 0.05, c="rust_dark", segs=20, bev=0.015)
    p.cyl(1.18, 0.07, c="iron", segs=20, bev=0.015)
    for r in (0.35, 0.75):
        p.torus(r, 0.04, at=(0, 0, 0.07), c="iron", segs=16, sides=4, sz=0.7)
    for a in (0, 45, 90, 135):
        p.box(2.2, 0.08, 0.04, at=(0, 0, 0.08), rot=(0, 0, a), c="iron", bev=0.01)
    for x in (-0.95, 0.95):
        p.cyl(0.08, 0.02, at=(x, 0.0, 0.07), c="soot", segs=6, bev=0)
    p.box(0.6, 0.35, 0.03, at=(0.4, -0.6, 0.085), c="rust", rot=(0, 0, 30), bev=0)
    return m


def armoire_electrique():
    m = Model("armoire_electrique", (2.6, 4, 1.4), CAT, "Armoire électrique", 8)
    p = m.part("Caisson")
    p.boxb(2.5, 1.3, 0.35, 0, 0, 0, c="concrete")
    p.boxb(2.36, 1.12, 3.3, 0, 0.06, 0.35, c="beige")
    p.box(2.6, 1.4, 0.2, at=(0, 0.0, 3.82), rot=(-4, 0, 0), c="beige")
    p.boxb(2.1, 0.04, 0.3, 0, 0.6, 3.25, c="grey_dark")  # grille d'aération arrière
    for z in (0.5, 0.65, 0.8):
        p.boxb(0.9, 0.05, 0.06, 0.6, -0.5, z, c="grey_dark")
    p.boxb(0.9, 0.04, 1.1, -0.4, 0.65, 0.9, c="rust")
    # affiches arrachées et tag abstrait
    p.boxb(0.8, 0.04, 1.0, -1.18, -0.2, 1.5, c="paper", rot=(0, 0, 90))
    p.boxb(0.5, 0.04, 0.6, -1.19, 0.25, 1.9, c="sky", rot=(0, 0, 90))
    for name, x, piv in (("PorteGauche", -0.57, (-1.15, -0.5, 0)), ("PorteDroite", 0.57, (1.15, -0.5, 0))):
        d = m.part(name, pivot=piv)
        d.boxb(1.1, 0.08, 3.0, x, -0.52, 0.5, c="beige")
        d.boxb(0.9, 0.03, 2.6, x, -0.57, 0.7, c="white")
        d.cyl(0.07, 0.06, at=(x - 0.4 * (1 if x > 0 else -1), -0.57, 2.0), rot=(90, 0, 0), c="metal_dark", segs=6)
    sg = m.part("PorteGauche")
    sg.prism([(-0.25, 0), (0.25, 0), (0, 0.43)], 0.03, at=(-0.57, -0.6, 2.6), c="yellow")
    sg.prism([(0.02, 0.36), (-0.08, 0.17), (0.0, 0.18), (-0.05, 0.04), (0.08, 0.22), (0.0, 0.21)], 0.03, at=(-0.57, -0.62, 2.6), c="black")
    pd = m.part("PorteDroite")
    pd.boxb(0.6, 0.04, 0.8, 0.7, -0.6, 1.0, c="pink", rot=(0, 0, -8))
    pd.boxb(0.45, 0.04, 0.35, 0.4, -0.6, 2.4, c="rust", rot=(0, 0, 20))
    return m


def isolateur(p, x, y, z, c="glass_dark"):
    p.cyl(0.05, 0.3, at=(x, y, z), c="metal_dark", segs=6, bev=0)
    p.lathe([(0, 0), (0.12, 0), (0.24, 0.12), (0.12, 0.2), (0.2, 0.3), (0.1, 0.4), (0.15, 0.48), (0.06, 0.6), (0, 0.6)],
            segs=8, at=(x, y, z + 0.25), c=c)


def poteau_bois():
    m = Model("poteau_electrique", (6, 24, 1), CAT, "Poteau électrique en bois", 47)
    p = m.part("Poteau")
    p.cyl(0.5, 22.9, r2=0.36, c="wood_old", segs=8, bev=0.05, deform=m.noise(0.02, 1))
    p.cyl(0.52, 1.2, c="wood_black", segs=8, bev=0)  # pied goudronné
    p.boxb(0.3, 0.05, 0.45, 0, -0.46, 5.0, c="metal_light", rot=(-2, 0, 0))  # plaque
    for i in range(6):
        z = 7.5 + i * 1.6
        x = 0.42 if i % 2 else -0.42
        p.rod((x * 0.8, 0, z), (x * 2.0, 0, z), 0.05, c="metal_dark", sides=4)
    for i, z in enumerate((3.0, 4.3)):
        p.boxb(0.6, 0.04, 0.45, 0.0, -0.5 + 0.02 * i, z, c=("paper", "yellow")[i], rot=(-4, 0, 8 - 14 * i))
    p.boxb(6.0, 0.5, 0.5, 0, 0, 21.3, c="wood_old")
    for s in (-1, 1):
        p.rod((s * 0.3, 0, 19.6), (s * 1.9, 0, 21.32), 0.07, c="metal_dark", sides=4)
    for x in (-2.6, 2.6):
        isolateur(p, x, 0, 21.8)
    isolateur(p, 0, 0, 22.9 - 0.25 + 0.55)
    return m


def transformateur():
    m = Model("transformateur", (1.8, 2.6, 1.8), CAT, "Transformateur sur poteau")
    p = m.part("Transformateur")
    p.cyl(0.66, 1.9, at=(0, -0.1, 0.1), c="galva", segs=12)
    p.lathe([(0, 2.0), (0.68, 2.0), (0.7, 2.05), (0.5, 2.2), (0, 2.25)], segs=12, at=(0, -0.1, 0), c="galva", cap0=False)
    p.cyl(0.6, 0.12, at=(0, -0.1, 0), c="metal_dark", segs=12)
    for a in (-60, -20, 20, 60, 160, 200):
        r = math.radians(a - 90)
        p.box(0.08, 0.28, 1.3, at=(math.cos(r) * 0.75, -0.1 + math.sin(r) * 0.75, 1.05), rot=(0, 0, a), c="galva", bev=0.02)
    p.boxb(0.5, 0.05, 0.5, 0.2, -0.78, 1.0, c="rust")
    p.boxb(0.4, 0.04, 0.3, -0.3, -0.77, 1.5, c="metal_light")  # plaque signalétique sans texte
    p.boxb(0.25, 0.3, 1.6, 0, 0.62, 0.3, c="metal_dark")  # étrier de fixation
    for z in (0.5, 1.6):
        p.boxb(1.0, 0.12, 0.18, 0, 0.82, z, c="metal_dark")
    for x in (-0.3, 0.3):
        isolateur(p, x, -0.1, 2.0, c="grey_dark")
    return m


def haut_parleur():
    m = Model("haut_parleur", (1.6, 1.3, 1.3), CAT, "Haut-parleur pavillon")
    p = m.part("HautParleur")
    prof = [(0, 0), (0.28, 0), (0.3, 0.05), (0.3, 0.32), (0.2, 0.38), (0.24, 0.5), (0.78, 1.15), (0.72, 1.18),
            (0.2, 0.6), (0, 0.6)]
    p.lathe(prof, segs=14, at=(0, 0.62, 0.72), rot=(90, 0, 0), c="grey_light", sy=0.68, cap0=False, cap1=False)
    p.lathe([(0, 0), (0.62, 0), (0, 0.02)], segs=14, at=(0, -0.38, 0.72), rot=(90, 0, 0), c="soot", sy=0.68, cap0=False, cap1=False)
    p.decal(0.3, 0.2, (0.3, -0.25, 1.05), c="rust", rot=(-40, 0, 0), seed=5)
    # étrier
    p.pipe([(-0.36, 0.1, 0.72), (-0.36, 0.1, 0.3), (0.36, 0.1, 0.3), (0.36, 0.1, 0.72)], 0.05, c="metal_dark", sides=4)
    p.boxb(0.2, 0.2, 0.3, 0, 0.1, 0.0, c="metal_dark")
    p.boxb(0.5, 0.06, 0.4, 0, 0.3, 0.02, c="metal_dark")
    p.boxb(0.3, 0.05, 0.25, 0.25, -0.15, 0.78, c="rust", rot=(50, 0, 0))
    return m


def sacs_sable():
    m = Model("sacs_sable", (2.4, 1, 1.4), CAT, "Sacs de sable empilés")
    p = m.part("Sacs")
    k = 0
    def bag(x, y, z, rz, c):
        nonlocal k
        k += 1
        p.box(1.15, 0.62, 0.34, at=(x, y, z), rot=(0, 0, rz), c=c, bev=0.13, deform=m.noise(0.025, k))
    for i, x in enumerate((-0.6, 0.6)):
        for j, y in enumerate((-0.36, 0.36)):
            bag(x, y, 0.17, 3 - 6 * j + 4 * i, ("jute", "sand")[(i + j) % 2])
    bag(0.0, -0.3, 0.5, 4, "sand")
    bag(-0.05, 0.36, 0.5, -3, "jute")
    bag(0.05, 0.0, 0.82, 88, "khaki")
    return m


def cloture():
    m = Model("cloture_grillagee", (8, 6, 0.3), CAT, "Clôture grillagée avec barbelés", None, "Module de 8 studs")
    s = m.part("Poteaux")
    for x in (-3.88, 3.88):
        s.cyl(0.12, 5.0, at=(x, 0, 0), c="galva", segs=8, bev=0)
        s.lathe([(0, 5.0), (0.15, 5.0), (0.15, 5.08), (0, 5.12)], segs=8, at=(x, 0, 0), c="galva", cap0=False)
        s.cyl(0.05, 1.0, at=(x, 0, 5.0), c="metal_dark", segs=4, bev=0)
    s.cyl(0.06, 7.76, at=(-3.88, 0, 4.8), rot=(0, 90, 0), c="galva", segs=6, bev=0)
    s.cyl(0.05, 7.76, at=(-3.88, 0, 0.35), rot=(0, 90, 0), c="galva", segs=6, bev=0)
    s.boxb(0.5, 0.05, 0.7, 2.5, -0.06, 2.0, c="pink", rot=(0, 0, 6))  # vieille affiche accrochée
    g = m.part("Grillage")
    x0, x1, z0, z1 = -3.85, 3.85, 0.4, 4.78
    step = 0.48
    hole = lambda x, z: (x - 1.6) ** 2 / 1.0 + (z - 0.4) ** 2 / 1.6 < 1.0  # trou découpé en bas
    def clip(xa, za, dx, dz):
        pts = []
        t = 0.0
        while True:
            x, z = xa + dx * t, za + dz * t
            if x < x0 - 1e-6 or x > x1 + 1e-6 or z > z1 + 1e-6 or z < z0 - 1e-6:
                break
            pts.append((x, z))
            t += 0.12
        return pts
    for sgn in (1, -1):
        k = x0 - (z1 - z0)
        while k < x1 + (z1 - z0):
            # ligne x = k + sgn*(z - z0)
            pts = []
            n = 60
            for i in range(n + 1):
                z = z0 + (z1 - z0) * i / n
                x = k + sgn * (z - z0) if sgn > 0 else k + (z1 - z)
                pts.append((x, z))
            segs, cur = [], []
            for (x, z) in pts:
                if x0 <= x <= x1 and not hole(x, z):
                    cur.append((x, z))
                elif cur:
                    segs.append(cur)
                    cur = []
            if cur:
                segs.append(cur)
            for sg in segs:
                if len(sg) >= 2:
                    a, b = sg[0], sg[-1]
                    g.rod((a[0], 0.02 * sgn, a[1]), (b[0], 0.02 * sgn, b[1]), 0.025, c="galva", sides=3)
            k += step
    # bord retroussé du trou
    g.pipe([(0.62, -0.02, 0.4), (0.75, -0.08, 1.0), (1.4, -0.11, 1.45), (2.1, -0.08, 1.2), (2.55, -0.03, 0.4)], 0.03, c="galva", sides=3)
    b = m.part("Barbele")
    for z in (5.2, 5.55, 5.9):
        b.rod((-3.88, 0, z), (3.88, 0, z), 0.025, c="metal_dark", sides=3)
        x = -3.6
        while x < 3.7:
            b.rod((x - 0.08, -0.08, z - 0.08), (x + 0.08, 0.08, z + 0.08), 0.018, c="metal_dark", sides=3)
            b.rod((x - 0.08, 0.08, z + 0.08), (x + 0.08, -0.08, z - 0.08), 0.018, c="metal_dark", sides=3)
            x += 0.55
    b.box(0.5, 0.05, 0.4, at=(-1.4, 0, 5.4), c="bag_black", rot=(0, 20, 15), deform=m.noise(0.05, 2))  # sac plastique pris dans les barbelés
    return m


def panneau_signalisation():
    m = Model("panneau_signalisation", (2, 7, 0.3), CAT, "Panneau de signalisation")
    p = m.part("Poteau")
    p.cyl(0.09, 6.4, at=(0, 0.08, 0), c="galva", segs=8, bev=0, deform=lambda co: co.__class__((co.x + 0.004 * co.z * co.z * 0.3, co.y, co.z)))
    p.lathe([(0, 6.4), (0.09, 6.4), (0, 6.45)], segs=8, at=(0.05, 0.08, 0), c="galva", cap0=False)
    for z in (5.4, 6.2):
        p.boxb(0.3, 0.12, 0.12, 0.05, 0.03, z, c="metal_dark")
    p.boxb(0.25, 0.03, 0.3, 0.03, -0.0, 2.6, c="yellow", rot=(0, 0, -10))
    s = m.part("Panneau")
    s.cyl(1.0, 0.05, at=(0, -0.05, 6.0), rot=(90, 0, 4), c="red", segs=20, bev=0.01)
    s.box(1.3, 0.04, 0.3, at=(0, -0.1, 6.0), rot=(0, 4, 0), c="white", bev=0)
    s.cyl(0.97, 0.03, at=(0, 0.05, 6.0), rot=(-90, 0, 4), c="metal", segs=20, bev=0)
    s.cyl(0.13, 0.03, at=(0.55, -0.08, 6.35), rot=(90, 0, 0), c="sky", segs=8, bev=0)  # autocollant
    s.box(0.3, 0.03, 0.18, at=(-0.45, -0.08, 5.55), rot=(0, 15, 0), c="rust", bev=0)
    return m


def passerelle():
    m = Model("passerelle", (8, 1, 3), CAT, "Passerelle métallique", None, "Module de 8 studs")
    p = m.part("Passerelle")
    for y in (-1.42, 1.42):
        p.boxb(8.0, 0.16, 1.0, 0, y, 0, c="yellow_dark")
        p.boxb(8.0, 0.4, 0.08, 0, y - 0.12 * (1 if y > 0 else -1), 0.0, c="yellow_dark", bev=0.02)
        p.boxb(8.0, 0.4, 0.08, 0, y - 0.12 * (1 if y > 0 else -1), 0.92, c="yellow_dark", bev=0.02)
    for x in (-3.5, -1.2, 1.2, 3.5):
        p.boxb(0.2, 2.7, 0.35, x, 0, 0.3, c="metal_dark")
    for i in range(12):
        y = -1.25 + i * (2.5 / 11)
        p.boxb(7.9, 0.06, 0.18, 0, y, 0.62, c="galva", bev=0.01)
    for i in range(16):
        x = -3.75 + i * 0.5
        p.boxb(0.05, 2.6, 0.08, x, 0, 0.72, c="galva", bev=0)
    for (x, y, w) in ((-2.5, 0.3, 1.2), (1.8, -0.6, 0.9), (3.2, 0.9, 0.6)):
        p.boxb(w, w * 0.6, 0.02, x, y, 0.8, c="rust", rot=(0, 0, 20 * x), bev=0)
    return m


MODELS = [
    ("01_lampadaire", lampadaire), ("02_feu_tricolore", feu_tricolore), ("03_corbeille", corbeille),
    ("04_benne", benne),
    ("05a_sac_poubelle", lambda: _sac("sac_poubelle_a", 21, "A")),
    ("05b_sac_poubelle", lambda: _sac("sac_poubelle_b", 22, "B")),
    ("05c_sac_poubelle", lambda: _sac("sac_poubelle_c", 23, "C")),
    ("06_baril_feu", baril_feu), ("07_abribus", abribus), ("08_plaque_egout", plaque_egout),
    ("09_armoire_electrique", armoire_electrique), ("10_poteau_electrique", poteau_bois),
    ("11_transformateur", transformateur), ("12_haut_parleur", haut_parleur), ("13_sacs_sable", sacs_sable),
    ("14_cloture_grillagee", cloture), ("15_panneau_signalisation", panneau_signalisation),
    ("16_passerelle", passerelle),
]
