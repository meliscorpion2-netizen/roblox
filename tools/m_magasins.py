"""47–72 : meubles communs, bar, café, kebab/pizza."""
import math
import random

from lib import Model

CAT = "06_magasins"


# ---------------------------------------------------------------------------
# Meubles communs
# ---------------------------------------------------------------------------

def comptoir(L):
    m = Model(f"comptoir_boutique_{L}", (L, 3.4, 1.6), CAT, f"Comptoir de boutique {L}", None,
              "Face client vers -Z ; côté vendeur ouvert avec étagère")
    p = m.part("Comptoir")
    p.boxb(L, 1.6, 0.18, 0, 0, 3.22, c="wood_light", bev=0.05)
    p.boxb(L - 0.2, 0.12, 3.22, 0, -0.68, 0, c="teal")  # façade
    p.boxb(L - 0.2, 0.14, 0.3, 0, -0.62, 0, c="plastic_black")  # plinthe
    for s in (-1, 1):
        p.boxb(0.12, 1.4, 3.22, s * (L / 2 - 0.16), 0.0, 0, c="teal")
    p.boxb(L - 0.4, 1.3, 0.1, 0, 0.05, 1.2, c="wood_light")  # étagère côté vendeur
    p.boxb(L - 0.4, 1.3, 0.1, 0, 0.05, 0.2, c="wood_light")
    n = int(L // 2.5)
    for i in range(n + 1):  # baguettes décoratives
        x = -L / 2 + 0.2 + i * (L - 0.4) / n
        p.boxb(0.1, 0.05, 2.8, x, -0.76, 0.3, c="teal")
    p.decal(1.2, 0.6, (-L * 0.25, -0.77, 0.6), c="mud", seed=1)
    p.decal(0.5, 0.4, (L * 0.3, -0.77, 2.2), c="yellow", seed=2)  # autocollant
    p.box(0.9, 0.06, 0.12, at=(L * 0.1, -0.77, 1.7), rot=(0, 25, 0), c="grey_light", bev=0)  # scotch qui tient la façade
    p.box(1.0, 0.7, 0.08, at=(-L * 0.3, 0.1, 3.44), rot=(0, 0, 8), c="paper", bev=0)
    return m


def caisse():
    m = Model("caisse_enregistreuse", (1.2, 1, 1), CAT, "Caisse enregistreuse", None, "Clavier et tiroir côté -Z (vendeur)")
    p = m.part("Caisse")
    p.boxb(1.2, 1.0, 0.32, 0, 0, 0, c="grey_dark", bev=0.04)
    p.box(1.1, 0.7, 0.25, at=(0, -0.05, 0.45), rot=(-14, 0, 0), c="cream", bev=0.04)
    for i in range(4):
        for j in range(3):
            p.boxb(0.14, 0.12, 0.05, -0.35 + i * 0.16, -0.25 + j * 0.15, 0.53 + j * 0.035, c=("grey" if i < 3 else "red"), bev=0.015, rot=(-14, 0, 0))
    p.boxb(0.12, 0.12, 0.3, 0.32, 0.25, 0.55, c="grey_dark")
    e = m.part("Ecran")
    e.boxb(0.5, 0.12, 0.28, 0.32, 0.25, 0.72, c="grey_dark", bev=0.03)
    e.boxb(0.42, 0.04, 0.2, 0.32, 0.18, 0.76, c="light_green", bev=0)
    e.boxb(0.42, 0.04, 0.2, 0.32, 0.32, 0.76, c="light_green", bev=0)
    t = m.part("Tiroir")
    t.boxb(1.1, 0.9, 0.24, 0, 0.0, 0.04, c="grey", bev=0.03)
    t.boxb(0.3, 0.06, 0.06, 0, -0.47, 0.14, c="metal_dark", bev=0.01)
    return m


PRODUCT_COLS = ["red", "yellow", "blue", "green", "orange", "white", "purple", "teal", "pink", "flame_red", "cream", "sky"]


def products_row(p, rng, x0, x1, y, z, depth, hmax):
    x = x0
    while x < x1 - 0.2:
        kind = rng.random()
        c = rng.choice(PRODUCT_COLS)
        if kind < 0.45:  # boîte
            w, h = rng.uniform(0.35, 0.6), rng.uniform(0.4, hmax)
            if x + w > x1:
                break
            p.boxb(w, depth * rng.uniform(0.6, 0.85), h, x + w / 2, y, z, c=c, bev=0.02)
            x += w + 0.05
        elif kind < 0.75:  # conserves
            r = 0.13
            for k in range(2):
                if x + 2 * r > x1:
                    break
                p.cyl(r, 0.32, at=(x + r, y - 0.15 + k * 0.3, z), c=c, segs=6, bev=0)
            x += 2 * r + 0.04
        else:  # bouteille
            r = 0.11
            if x + 2 * r > x1:
                break
            p.lathe([(0, 0), (r, 0), (r, 0.45), (0.04, 0.62), (0.04, 0.72), (0, 0.72)], segs=6, at=(x + r, y, z), c=c)
            x += 2 * r + 0.05


def etagere(L):
    m = Model(f"etagere_metal_{L}", (L, 5, 1.2), CAT, f"Étagère métal remplie {L}", None, "4 niveaux")
    p = m.part("Etagere")
    for x in (-L / 2 + 0.06, L / 2 - 0.06) + ((0.0,) if L > 5 else ()):
        for y in (-0.54, 0.54):
            p.boxb(0.1, 0.1, 5.0, x, y, 0, c="grey_light", bev=0.02)
    p.boxb(L - 0.1, 0.04, 4.6, 0, 0.56, 0.3, c="grey", bev=0)  # fond perforé
    rng = random.Random(L)
    levels = (0.2, 1.4, 2.6, 3.8)
    for i, z in enumerate(levels):
        p.boxb(L - 0.05, 1.15, 0.08, 0, 0, z, c="grey_light", bev=0.02)
        p.boxb(L - 0.05, 0.06, 0.18, 0, -0.56, z - 0.06, c="red" if i % 2 else "yellow", bev=0)  # bandeau prix vierge
        products_row(p, rng, -L / 2 + 0.12, L / 2 - 0.12, -0.05, z + 0.08, 1.0, 0.9)
    p.box(0.5, 0.4, 0.4, at=(L / 2 - 0.5, -0.1, 4.9 - 0.2), rot=(0, 0, 20), c="cardboard", bev=0.03)
    p.decal(0.6, 0.3, (-L / 4, -0.6, 0.05), c="rust", seed=3)
    return m


def frigo():
    m = Model("frigo_vitre", (2.6, 6, 1.6), CAT, "Frigo vitré à canettes")
    p = m.part("Caisson")
    p.boxb(2.6, 1.5, 0.4, 0, 0.05, 0, c="plastic_black")
    p.boxb(2.6, 1.5, 4.9, 0, 0.05, 0.4, c="red", bev=0.06)
    p.boxb(2.6, 1.6, 0.7, 0, 0.0, 5.3, c="red", bev=0.08)
    p.boxb(2.2, 1.2, 4.5, 0, 0.1, 0.6, c="white", bev=0)  # intérieur
    rng = random.Random(9)
    for z in (0.7, 1.8, 2.9, 4.0):
        p.boxb(2.1, 1.1, 0.06, 0, 0.1, z, c="galva", bev=0)
        for i in range(7):
            p.cyl(0.13, 0.45, at=(-0.9 + i * 0.3, -0.25, z + 0.06), c=rng.choice(["red", "blue", "green", "yellow", "orange"]), segs=6, bev=0)
            p.cyl(0.13, 0.45, at=(-0.9 + i * 0.3, 0.1, z + 0.06), c=rng.choice(["red", "blue", "teal"]), segs=6, bev=0)
    p.boxb(2.2, 0.1, 0.3, 0, -0.7, 0.42, c="grey_dark")  # grille basse
    p.decal(0.6, 0.4, (1.0, -0.77, 0.2), c="rust", seed=1)
    porte = m.part("Porte", pivot=(-1.25, -0.72, 0.5))
    porte.boxb(2.5, 0.12, 0.18, 0, -0.72, 0.5, c="grey_light")
    porte.boxb(2.5, 0.12, 0.18, 0, -0.72, 5.0, c="grey_light")
    for x in (-1.16, 1.16):
        porte.boxb(0.18, 0.12, 4.68, x, -0.72, 0.5, c="grey_light")
    porte.boxb(0.12, 0.16, 1.4, 0.95, -0.82, 2.2, c="metal_dark")  # poignée
    v = m.part("Vitre", pivot=(-1.25, -0.72, 0.5))
    v.boxb(2.14, 0.04, 4.35, 0, -0.72, 0.66, c="glass", bev=0)
    v.decal(0.5, 0.3, (-0.5, -0.75, 4.4), c="paper", t=0.01, seed=4)  # étiquette décollée (vierge)
    lum = m.part("Lumiere")
    lum.boxb(2.3, 1.62, 0.5, 0, -0.01, 5.4, c="light_white", bev=0.0)  # bandeau lumineux (enseigne ajoutée en jeu)
    lum.boxb(2.0, 0.08, 0.06, 0, -0.3, 4.95, c="light_white", bev=0)  # tube intérieur
    return m


def neon():
    m = Model("plafonnier_neon", (3, 0.2, 0.8), CAT, "Plafonnier néon", None, "Base = face plafond inversée : poser le dessus contre le plafond")
    p = m.part("Boitier")
    p.boxb(3.0, 0.8, 0.08, 0, 0, 0.12, c="white", bev=0.02)
    for s in (-1, 1):
        p.boxb(3.0, 0.06, 0.12, 0, s * 0.37, 0.02, c="white", bev=0.01)
        p.boxb(0.08, 0.8, 0.12, s * 1.46, 0, 0.02, c="grey_light", bev=0.01)
    p.decal(0.6, 0.3, (0.8, 0.0, 0.2), c="soot", rot=(90, 0, 0), t=0.01, seed=1)  # moucherons morts
    n = m.part("Neon")
    for y in (-0.16, 0.16):
        n.cyl(0.06, 2.8, at=(-1.4, y, 0.07), rot=(0, 90, 0), c="light_white", segs=6, bev=0)
    return m


def tabouret():
    m = Model("tabouret_bar", (1.2, 2.5, 1.2), CAT, "Tabouret de bar")
    p = m.part("Tabouret")
    p.cyl(0.55, 0.08, c="chrome", segs=12, bev=0.03)
    p.cyl(0.08, 2.1, at=(0, 0, 0.08), c="chrome", segs=6, bev=0)
    p.torus(0.42, 0.04, at=(0, 0, 0.75), c="chrome", segs=12, sides=4)
    for a in (0, 90, 180, 270):
        r = math.radians(a)
        p.rod((0, 0, 0.75), (0.42 * math.cos(r), 0.42 * math.sin(r), 0.75), 0.03, c="chrome", sides=3)
    p.cyl(0.6, 0.32, at=(0, 0, 2.18), c="red", segs=14, bev=0.1, deform=m.noise(0.01, 1))
    p.box(0.5, 0.12, 0.02, at=(0.15, -0.1, 2.505), rot=(0, 0, 30), c="grey_light", bev=0)  # chatterton
    p.box(0.5, 0.12, 0.02, at=(0.15, -0.1, 2.51), rot=(0, 0, -40), c="grey_light", bev=0)
    return m


def chaise():
    m = Model("chaise_bois", (1.5, 3.6, 1.5), CAT, "Chaise en bois", None, "Assise à 1,7 stud")
    p = m.part("Chaise")
    for sx in (-1, 1):
        for sy in (-1, 1):
            h = 3.6 if sy > 0 else 1.6
            p.boxb(0.14, 0.14, h, sx * 0.62, sy * 0.62, 0, c="wood", bev=0.03, rot=(0, 0, 0) if h < 2 else (0, 0, 0))
    p.boxb(1.5, 1.5, 0.12, 0, 0, 1.58, c="wood_light", bev=0.04)
    for z in (0.6,):
        p.boxb(1.24, 0.08, 0.08, 0, -0.62, z, c="wood")
        p.boxb(1.24, 0.08, 0.08, 0, 0.62, z, c="wood")
        p.boxb(0.08, 1.24, 0.08, -0.62, 0, z + 0.15, c="wood")
    for z in (2.3, 3.2):
        p.boxb(1.3, 0.1, 0.32, 0, 0.66, z, c="wood_light", bev=0.03)
    p.boxb(1.3, 0.1, 0.3, 0.05, 0.66, 2.75, c="wood_light", bev=0.03, rot=(0, 8, 0))  # barreau de travers
    p.decal(0.4, 0.3, (0.3, -0.2, 1.71), c="stain", rot=(90, 0, 0), t=0.01, seed=1)
    return m


def table_bistrot():
    m = Model("table_bistrot", (2.6, 2.8, 2.6), CAT, "Table bistrot ronde")
    p = m.part("Table")
    p.cyl(0.75, 0.1, c="iron", segs=12, bev=0.04)
    p.lathe([(0, 0.1), (0.2, 0.1), (0.1, 0.4), (0.08, 2.5), (0.25, 2.62), (0, 2.62)], segs=8, c="iron")
    p.cyl(1.3, 0.18, at=(0, 0, 2.62), c="chrome", segs=16, bev=0.04)
    p.cyl(1.2, 0.02, at=(0, 0, 2.79), c="marble", segs=16, bev=0)
    p.cyl(0.22, 0.02, at=(0.5, -0.3, 2.8), c="wood_dark", segs=10, bev=0)  # trace de verre
    p.cyl(0.12, 0.02, at=(-0.4, 0.5, 2.8), c="stain", segs=8, bev=0)
    p.box(0.3, 0.3, 0.06, at=(0.9, 0.9, 0.08), rot=(0, 0, 15), c="cardboard", bev=0.0)  # carton qui cale le pied
    return m


def table_murale():
    m = Model("table_haute_murale", (1.2, 3.3, 5), CAT, "Table haute murale", None, "Longueur selon Z ; côté mur vers +X")
    p = m.part("Table")
    p.boxb(1.2, 5.0, 0.15, 0, 0, 3.15, c="wood_light", bev=0.04)
    for y in (-2.0, 2.0):
        p.boxb(0.1, 0.2, 1.4, 0.55, y, 1.8, c="iron")
        p.rod((0.55, y, 1.85), (-0.3, y, 3.15), 0.05, c="iron", sides=4)
        p.boxb(0.12, 0.12, 3.15, -0.45, y, 0, c="iron", bev=0.02)  # pied avant
        p.boxb(0.3, 0.3, 0.05, -0.45, y, 0, c="iron", bev=0.01)
    p.boxb(0.08, 4.0, 0.08, -0.45, 0, 0.5, c="iron", bev=0.01)  # repose-pieds
    p.cyl(0.18, 0.02, at=(-0.1, 1.0, 3.3), c="wood_dark", segs=8, bev=0)
    p.decal(0.6, 0.3, (-0.1, -1.0, 3.305), c="stain", rot=(90, 0, 0), t=0.005, seed=1)
    return m


def plante():
    m = Model("plante_pot", (2.2, 3.3, 2.2), CAT, "Plante en pot")
    p = m.part("Pot")
    p.lathe([(0, 0), (0.7, 0), (0.75, 0.05), (0.95, 1.2), (1.05, 1.25), (1.05, 1.4), (0.92, 1.4), (0.92, 1.3), (0, 1.3)], segs=12,
            c="brick", deform=m.noise(0.01, 1))
    p.decal(0.4, 0.3, (0.3, -0.88, 0.7), c="soot", rot=(-10, 0, 0), seed=2)
    p.boxb(0.06, 0.02, 0.5, -0.2, -0.86, 0.5, c="black", rot=(-10, 0, 25), bev=0)  # fêlure
    f = m.part("Feuilles")
    rng = random.Random(4)
    for i in range(11):
        a = i * 360 / 11 + rng.uniform(-10, 10)
        tilt = rng.uniform(20, 55)
        L = rng.uniform(1.3, 2.0)
        col = "leaf" if i % 4 else ("leaf_dark" if i % 8 else "yellow_dark")
        if i == 5:
            col = "wood_old"  # feuille morte
            tilt = 80
        f.prism([(-0.25, 0), (-0.32, L * 0.45), (0, L), (0.32, L * 0.45), (0.25, 0)], 0.04, at=(0, 0, 1.25), rot=(tilt, 0, a),
                plane="XZ", c=col, deform=m.noise(0.03, i))
    f.cyl(0.08, 0.5, at=(0, 0, 1.2), c="leaf_dark", segs=6, bev=0)
    return m


# ---------------------------------------------------------------------------
# Bar
# ---------------------------------------------------------------------------

def comptoir_bar():
    m = Model("comptoir_bar", (10, 3.4, 1.6), CAT, "Comptoir de bar en bois")
    p = m.part("Comptoir")
    p.boxb(10.0, 1.6, 0.25, 0, 0, 3.15, c="wood_dark", bev=0.08)
    p.boxb(9.7, 1.25, 2.85, 0, 0.12, 0.3, c="wood")
    p.boxb(9.8, 1.3, 0.3, 0, 0.1, 0, c="wood_black")
    for i in range(6):
        x = -4.05 + i * 1.62
        p.boxb(1.35, 0.08, 2.2, x, -0.52, 0.6, c="wood_red", bev=0.04)
    p.decal(1.0, 0.5, (2.0, -0.57, 1.0), c="stain", seed=1)
    for i in range(3):
        p.cyl(0.18, 0.02, at=(-2.5 + i * 2.4, 0.1, 3.4), c="stain", segs=8, bev=0)
    f = m.part("ReposePieds")
    f.rod((-4.8, -0.85, 0.55), (4.8, -0.85, 0.55), 0.08, c="brass", sides=8)
    for x in (-4.6, -1.6, 1.6, 4.6):
        f.rod((x, -0.85, 0.55), (x, -0.52, 0.55), 0.05, c="brass", sides=5)
    f.decal(0.6, 0.12, (0.6, -0.95, 0.55), c="copper", t=0.01, seed=2)
    return m


def bottle(p, x, y, z, c, kind, rng):
    if kind == 0:
        prof = [(0, 0), (0.13, 0), (0.13, 0.5), (0.05, 0.62), (0.045, 0.78), (0, 0.78)]
    elif kind == 1:
        prof = [(0, 0), (0.15, 0), (0.15, 0.35), (0.06, 0.45), (0.05, 0.6), (0, 0.6)]
    else:
        prof = [(0, 0), (0.11, 0), (0.12, 0.55), (0.04, 0.72), (0.035, 0.9), (0, 0.9)]
    p.lathe(prof, segs=6, at=(x, y, z), c=c)


def etagere_bouteilles():
    m = Model("etagere_bouteilles", (12, 2, 0.8), CAT, "Étagère murale à bouteilles", None, "2 niveaux garnis, fixation au mur côté +Z")
    p = m.part("Etagere")
    for z in (0.05, 1.05):
        p.boxb(12.0, 0.8, 0.1, 0, 0, z, c="wood_dark", bev=0.03)
    for x in (-5.5, 0, 5.5):
        p.boxb(0.1, 0.1, 1.1, x, 0.35, 0.0, c="iron")
    b = m.part("Bouteilles")
    rng = random.Random(12)
    cols = ["green_dark", "glass_dark", "wood_dark", "copper", "white", "red_dark", "glass"]
    for z in (0.15, 1.15):
        x = -5.7
        while x < 5.6:
            if rng.random() < 0.12:  # trou dans la rangée
                x += 0.45
                continue
            bottle(b, x, rng.uniform(-0.1, 0.1), z, rng.choice(cols), rng.randrange(3), rng)
            x += rng.uniform(0.32, 0.42)
    b.box(0.6, 0.3, 0.02, at=(3.0, 0, 1.16), c="stain", bev=0)
    return m


def miroir_bar():
    m = Model("miroir_bar", (12, 1.6, 0.1), CAT, "Miroir de bar")
    p = m.part("Cadre")
    p.boxb(12.0, 0.1, 0.18, 0, 0, 0, c="wood_dark", bev=0.03)
    p.boxb(12.0, 0.1, 0.18, 0, 0, 1.42, c="wood_dark", bev=0.03)
    for x in (-5.91, 5.91):
        p.boxb(0.18, 0.1, 1.6, x, 0, 0, c="wood_dark", bev=0.03)
    for x in (-5.91, 5.91):
        for z in (0.09, 1.51):
            p.cyl(0.13, 0.04, at=(x, -0.03, z), rot=(90, 0, 0), c="brass", segs=8, bev=0)
    mi = m.part("Miroir")
    mi.boxb(11.66, 0.03, 1.26, 0, 0.02, 0.17, c="mirror", bev=0)
    for a, b in (((4.5, 0.6), (5.0, 0.75)), ((5.0, 0.75), (4.7, 1.05)), ((4.5, 0.6), (4.6, 1.2))):
        mi.rod((a[0], -0.01, a[1]), (b[0], -0.01, b[1]), 0.012, c="grey_light", sides=3)  # fissure
    mi.decal(1.4, 0.5, (-3.0, -0.015, 0.5), c="paper_dirty", t=0.01, seed=3)  # traces de doigts/buée
    return m


def cible():
    m = Model("cible_flechettes", (1.8, 1.8, 0.2), CAT, "Cible de fléchettes")
    p = m.part("Cible")
    p.cyl(0.9, 0.1, at=(0, 0.05, 0.9), rot=(90, 0, 0), c="black", segs=20, bev=0.02)
    p.cyl(0.85, 0.02, at=(0, -0.05, 0.9), rot=(90, 0, 0), c="black", segs=20, bev=0)
    for i in range(20):
        a0, a1 = 360 * i / 20 - 9, 360 * (i + 1) / 20 - 9
        col = "cream" if i % 2 else "black"
        ring = "red" if i % 2 else "green"
        def arc(r0, r1):
            pts = [(r1 * math.cos(math.radians(a)), r1 * math.sin(math.radians(a))) for a in (a0, a1)]
            pts += [(r0 * math.cos(math.radians(a)), r0 * math.sin(math.radians(a))) for a in (a1, a0)]
            return pts
        p.prism(arc(0.08, 0.62), 0.02, at=(0, -0.07, 0.9), c=col)
        p.prism(arc(0.62, 0.7), 0.02, at=(0, -0.07, 0.9), c=ring)
        p.prism(arc(0.36, 0.42), 0.022, at=(0, -0.071, 0.9), c=ring)
    p.cyl(0.08, 0.03, at=(0, -0.06, 0.9), rot=(90, 0, 0), c="red", segs=8, bev=0)
    fl = m.part("Flechettes")
    for (x, z) in ((0.25, 1.05), (-0.3, 0.7), (0.95, 1.6)):  # une plantée dans le mur
        fl.rod((x, -0.08, z), (x + 0.02, -0.0 - 0.1, z + 0.0), 0.012, c="metal", sides=3)
        fl.rod((x, -0.09, z), (x, -0.1, z), 0.03, c="metal", sides=3)
    return m


def tv_pmu():
    m = Model("tv_courses", (4, 2.4, 0.3), CAT, "TV murale des courses")
    p = m.part("TV")
    p.boxb(4.0, 0.2, 2.4, 0, -0.03, 0, c="plastic_black", bev=0.05)
    p.boxb(1.2, 0.12, 0.8, 0, 0.12, 0.8, c="metal_dark")
    p.box(0.8, 0.02, 0.12, at=(1.6, -0.14, 2.2), rot=(0, 30, 0), c="grey_light", bev=0)  # scotch
    e = m.part("Ecran")
    e.boxb(3.7, 0.03, 2.1, 0, -0.14, 0.15, c="screen", bev=0)
    e.decal(0.8, 0.5, (1.2, -0.16, 1.7), c="screen_dark", t=0.01, seed=1)  # pixel mort / tache
    return m


def billard():
    m = Model("billard", (4, 3, 7), CAT, "Billard avec queue et boules", None, "Longueur selon Z")
    p = m.part("Table")
    for sx in (-1, 1):
        for sy in (-1, 0, 1):
            p.lathe([(0, 0), (0.25, 0), (0.18, 0.4), (0.22, 1.6), (0.3, 2.2), (0, 2.2)], segs=8, at=(sx * 1.55, sy * 2.8, 0), c="wood_dark")
    p.boxb(4.0, 7.0, 0.55, 0, 0, 2.15, c="wood_red", bev=0.08)
    p.boxb(3.3, 6.3, 0.05, 0, 0, 2.7, c="felt", bev=0)
    for sx in (-1, 1):
        p.boxb(0.35, 6.3, 0.3, sx * 1.83, 0, 2.7, c="wood_red", bev=0.06)
    for sy in (-1, 1):
        p.boxb(4.0, 0.35, 0.3, 0, sy * 3.33, 2.7, c="wood_red", bev=0.06)
    for sx in (-1, 1):
        for sy in (-1, 0, 1):
            p.cyl(0.2, 0.06, at=(sx * 1.62, sy * 3.1, 2.72), c="black", segs=8, bev=0)
    p.decal(0.8, 0.5, (0.5, 1.2, 2.76), c="stain", rot=(90, 0, 0), t=0.01, seed=1)
    p.decal(0.3, 0.6, (-0.8, -2.0, 2.76), c="olive", rot=(90, 0, 0), t=0.01, seed=2)  # feutre usé
    bl = m.part("Boules")
    rng = random.Random(16)
    cols = ["white", "yellow", "blue", "red", "purple", "orange", "green", "maroon", "black", "yellow", "blue", "red", "purple",
            "orange", "green", "maroon"]
    pos = [(0, 1.8)]
    for row in range(5):
        for k in range(row + 1):
            pos.append((-row * 0.13 + k * 0.26, -1.4 - row * 0.23))
    for (x, y), c in zip(pos, cols):
        bl.sphere(0.12, at=(x, y, 2.85), c=c, segs=8, rings=6)
    q = m.part("Queue")
    q.pipe([(-1.2, 2.6, 2.83), (1.4, -2.9, 2.83)], 0.05, c="wood_light", sides=6)
    q.rod((-1.2, 2.6, 2.83), (-0.75, 1.65, 2.83), 0.075, c="wood_black", sides=6)
    return m


def jukebox():
    m = Model("jukebox", (2.5, 4.5, 1.5), CAT, "Jukebox rétro")
    p = m.part("Caisson")
    arch = [(-1.15, 0), (1.15, 0)] + [(1.15 * math.cos(math.radians(a)), 3.2 + 1.15 * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    p.prism(arch, 1.3, at=(0, 0.05, 0.15), c="wood_red", bev=0.05)
    p.boxb(2.5, 1.5, 0.15, 0, 0, 0, c="chrome", bev=0.04)
    p.boxb(1.8, 0.1, 1.2, 0, -0.62, 0.5, c="grey_dark", bev=0.03)  # grille haut-parleur
    for k in range(6):
        p.boxb(1.6, 0.06, 0.06, 0, -0.68, 0.62 + k * 0.18, c="chrome", bev=0)
    p.boxb(1.6, 0.12, 0.5, 0, -0.62, 1.85, c="cream", bev=0.03)  # sélecteurs
    for k in range(8):
        p.boxb(0.12, 0.08, 0.12, -0.6 + k * 0.17, -0.7, 1.95, c="chrome", bev=0.01)
    p.decal(0.4, 0.3, (0.9, -0.62, 0.3), c="rust", seed=1)
    v = m.part("Vitre")
    v.cyl(0.85, 0.08, at=(0, -0.6, 3.15), rot=(90, 0, 0), c="glass", segs=16, bev=0.02)
    v.boxb(1.6, 0.08, 0.7, 0, -0.64, 2.45, c="glass", bev=0.02)
    n = m.part("Neon")
    tube = [(1.2 * math.cos(math.radians(a)), -0.66, 0.15 + 3.2 + 1.2 * math.sin(math.radians(a))) for a in range(0, 181, 12)]
    tube = [(1.2, -0.66, 0.3)] + tube + [(-1.2, -0.66, 0.3)]
    n.pipe(tube, 0.08, c="neon_pink", sides=5)
    n.pipe([(0.98, -0.68, 2.3)] + [(0.98 * math.cos(math.radians(a)), -0.68, 3.2 + 0.98 * math.sin(math.radians(a))) for a in range(0, 181, 15)] + [(-0.98, -0.68, 2.3)],
           0.05, c="neon_blue", sides=4)
    return m


# ---------------------------------------------------------------------------
# Café / boulangerie
# ---------------------------------------------------------------------------

def machine_cafe():
    m = Model("machine_cafe", (2, 1.6, 1), CAT, "Machine à café pro")
    p = m.part("Machine")
    p.boxb(2.0, 0.95, 1.3, 0, 0.0, 0.0, c="inox", bev=0.06)
    p.boxb(1.9, 0.9, 0.05, 0, 0, 1.3, c="metal_dark", bev=0)
    p.boxb(1.7, 0.6, 0.12, 0, -0.18, 0.0, c="metal_dark", bev=0.02)  # égouttoir
    p.boxb(1.8, 0.06, 0.65, 0, -0.48, 0.55, c="red", bev=0.02)  # façade
    for x in (-0.5, 0.5):
        p.cyl(0.13, 0.22, at=(x, -0.42, 0.4), c="chrome", segs=8)
        p.rod((x, -0.48, 0.42), (x, -0.68, 0.42), 0.03, c="black", sides=4)  # porte-filtre
        p.cyl(0.1, 0.18, at=(x, -0.42, 0.12), c="white", segs=8)  # tasse
    p.pipe([(0.85, -0.45, 0.95), (0.88, -0.6, 0.7), (0.88, -0.62, 0.3)], 0.025, c="chrome", sides=4)  # buse vapeur
    p.cyl(0.12, 0.08, at=(-0.8, -0.5, 1.0), rot=(90, 0, 0), c="chrome", segs=10, bev=0)  # manomètre
    p.cyl(0.09, 0.02, at=(-0.8, -0.58, 1.0), rot=(90, 0, 0), c="white", segs=10, bev=0)
    for i in range(4):  # tasses sur le chauffe-tasses
        p.cyl(0.1, 0.16, at=(-0.6 + i * 0.38, 0.1, 1.35), c="white", segs=8, bev=0)
    p.decal(0.4, 0.2, (0.2, -0.51, 0.7), c="wood_dark", t=0.01, seed=1)  # coulure de café
    vy = m.part("Voyants")
    for x in (-0.3, -0.15):
        vy.boxb(0.08, 0.04, 0.08, x, -0.52, 1.05, c=("light_green" if x < -0.2 else "light_amber"), bev=0)
    return m


def croissant(p, x, y, z, rz=0):
    pts = []
    for k in range(7):
        a = math.radians(-70 + k * 140 / 6)
        pts.append((x + 0.18 * math.sin(a), y + 0.18 * (1 - math.cos(a)) - 0.05, z))
    p.pipe(pts, 0.065, c="croissant", sides=6, rot=(0, 0, 0))


def vitrine_patisseries():
    m = Model("vitrine_patisseries", (2.6, 1.2, 1), CAT, "Vitrine à pâtisseries avec croissants")
    p = m.part("Vitrine")
    p.boxb(2.6, 1.0, 0.18, 0, 0, 0, c="wood_light", bev=0.03)
    p.boxb(2.4, 0.9, 0.04, 0, 0.0, 0.55, c="glass", bev=0)
    for x in (-1.25, 1.25):
        p.boxb(0.08, 0.95, 1.02, x, 0, 0.18, c="inox", bev=0.01)
    p.boxb(2.5, 0.95, 0.06, 0, 0, 1.14, c="inox", bev=0.01)
    p.boxb(2.4, 0.85, 0.03, 0, 0.0, 0.18, c="paper", bev=0)  # papier dentelle (uni)
    for i in range(5):
        croissant(p, -0.95 + i * 0.47, -0.1, 0.27)
    for i in range(4):
        croissant(p, -0.7 + i * 0.47, -0.05, 0.63)
    p.box(0.3, 0.25, 0.1, at=(0.9, 0.2, 0.65), c="bread", bev=0.04)  # pain au chocolat solitaire
    v = m.part("Vitre")
    v.box(2.42, 0.04, 1.0, at=(0, -0.42, 0.68), rot=(-14, 0, 0), c="glass", bev=0)
    v.decal(0.5, 0.3, (-0.6, -0.48, 0.5), c="grey_light", rot=(-14, 0, 0), t=0.01, seed=2)  # traces de doigts
    return m


def ardoise():
    m = Model("ardoise_menu", (7, 2.6, 0.2), CAT, "Ardoise menu", None, "Cadre seul, texte ajouté en jeu")
    p = m.part("Cadre")
    for z in (0, 2.4):
        p.boxb(7.0, 0.2, 0.2, 0, 0, z, c="wood", bev=0.04)
    for x in (-3.4, 3.4):
        p.boxb(0.2, 0.2, 2.6, x, 0, 0, c="wood", bev=0.04)
    p.boxb(1.2, 0.12, 0.1, 2.0, -0.05, 0.12, c="white", bev=0.02)  # craie
    a = m.part("Ardoise")
    a.boxb(6.62, 0.06, 2.22, 0, 0.02, 0.19, c="slate", bev=0)
    a.decal(1.6, 0.6, (-1.8, -0.02, 0.7), c="grey_dark", t=0.01, seed=1)  # traces mal effacées
    return m


# ---------------------------------------------------------------------------
# Kebab / hot-dog / pizza
# ---------------------------------------------------------------------------

def comptoir_inox():
    m = Model("comptoir_inox", (9, 4.7, 1.6), CAT, "Comptoir inox avec vitre anti-postillons")
    p = m.part("Comptoir")
    p.boxb(9.0, 1.6, 0.15, 0, 0, 3.25, c="inox", bev=0.04)
    p.boxb(8.8, 1.45, 3.25, 0, 0.05, 0, c="inox", bev=0.05)
    for i in range(4):
        p.boxb(2.0, 0.05, 2.6, -3.3 + i * 2.2, -0.7, 0.4, c="alu", bev=0.02)
        p.boxb(0.6, 0.06, 0.08, -3.3 + i * 2.2, -0.74, 2.6, c="metal_dark", bev=0)
    p.decal(1.0, 0.6, (2.6, -0.73, 0.5), c="sauce", t=0.01, seed=1)  # éclaboussure de sauce blanche
    p.decal(0.5, 0.3, (-1.5, -0.73, 0.9), c="flame_red", t=0.01, seed=2)  # sauce harissa
    for x in (-4.0, 0, 4.0):
        p.rod((x, -0.45, 3.4), (x, -0.45, 4.6), 0.05, c="chrome", sides=5)
    v = m.part("Vitre")
    v.box(8.6, 0.06, 1.2, at=(0, -0.55, 4.05), rot=(-18, 0, 0), c="glass", bev=0.01)
    v.box(8.6, 0.6, 0.06, at=(0, -0.3, 4.65), c="glass", bev=0.01)
    v.decal(0.8, 0.4, (-2.0, -0.62, 3.9), c="grey_light", rot=(-18, 0, 0), t=0.01, seed=3)  # postillons séchés
    return m


def bacs_garnitures():
    m = Model("bacs_garnitures", (4.4, 0.3, 0.8), CAT, "Bacs à garnitures")
    p = m.part("Bacs")
    p.boxb(4.4, 0.8, 0.05, 0, 0, 0.0, c="inox", bev=0.01)
    for i, c in enumerate(("lettuce", "tomato", "onion", "sauce")):
        x = -1.62 + i * 1.08
        p.boxb(1.02, 0.74, 0.04, x, 0, 0.05, c="inox", bev=0)
        for s in (-1, 1):
            p.boxb(1.02, 0.04, 0.25, x, s * 0.35, 0.05, c="inox", bev=0)
            p.boxb(0.04, 0.74, 0.25, x + s * 0.49, 0, 0.05, c="inox", bev=0)
        g = m.part("Garnitures")
        rng = random.Random(i)
        if c == "sauce":
            g.boxb(0.92, 0.66, 0.16, x, 0, 0.06, c=c, bev=0, deform=m.noise(0.015, 30))
            g.rod((x + 0.2, 0.1, 0.22), (x + 0.45, 0.28, 0.3), 0.025, c="chrome", sides=4)  # louche
        else:
            g.boxb(0.92, 0.66, 0.12, x, 0, 0.06, c=c, bev=0)
            for k in range(7):
                g.box(0.16, 0.12, 0.06, at=(x + rng.uniform(-0.35, 0.35), rng.uniform(-0.22, 0.22), 0.21), rot=(rng.uniform(-20, 20), 0, rng.uniform(0, 90)),
                      c=c if c != "tomato" else ("tomato" if k % 3 else "flame_red"), bev=0.01)
    return m


def broche_kebab():
    m = Model("broche_kebab", (1.6, 3.6, 1.6), CAT, "Broche à kebab")
    p = m.part("Socle")
    p.boxb(1.6, 1.4, 0.5, 0, 0.05, 0, c="inox", bev=0.05)
    p.boxb(1.4, 0.06, 0.25, 0, -0.66, 0.15, c="metal_dark")
    p.cyl(0.55, 0.06, at=(0, -0.15, 0.5), c="inox", segs=12, bev=0)  # plateau
    p.cyl(0.04, 3.0, at=(0, -0.15, 0.5), c="chrome", segs=6, bev=0)
    p.cyl(0.25, 0.05, at=(0, -0.15, 3.3), c="inox", segs=8, bev=0)
    p.boxb(1.6, 0.25, 3.4, 0, 0.67, 0.2, c="inox", bev=0.04)  # dos du grill
    p.decal(0.6, 0.3, (0.3, -0.66, 0.3), c="sauce", t=0.01, seed=1)
    v = m.part("Viande")
    v.lathe([(0, 0.56), (0.25, 0.56), (0.42, 0.9), (0.55, 2.3), (0.5, 2.9), (0.32, 3.2), (0, 3.25)], segs=10, at=(0, -0.15, 0),
            c="meat", deform=m.noise(0.04, 2))
    v.decal(0.5, 1.2, (0, -0.72, 1.8), c="meat_dark", rot=(0, 0, 0), t=0.05, seed=4)  # côté grillé
    g = m.part("Grill")
    for k in range(5):
        g.boxb(1.3, 0.06, 0.4, 0, 0.53, 0.75 + k * 0.52, c="ember", bev=0.01)
    return m


def friteuse():
    m = Model("friteuse_pro", (1.8, 3.2, 1.2), CAT, "Friteuse pro")
    p = m.part("Friteuse")
    p.boxb(1.8, 1.15, 2.85, 0, 0.0, 0.0, c="inox", bev=0.05)
    p.boxb(1.8, 0.15, 0.35, 0, 0.52, 2.85, c="inox", bev=0.03)  # dosseret
    p.boxb(1.7, 0.06, 2.3, 0, -0.56, 0.2, c="alu", bev=0.02)
    for x in (-0.6, 0.6):
        p.cyl(0.07, 0.05, at=(x, -0.6, 2.5), rot=(90, 0, 0), c="black", segs=8, bev=0)
    p.decal(1.0, 0.8, (0.2, -0.6, 1.2), c="yellow_dark", t=0.01, seed=1)  # coulure d'huile
    o = m.part("Huile")
    for x in (-0.42, 0.42):
        o.boxb(0.7, 0.8, 0.04, x, -0.05, 2.8, c="flame_yellow", bev=0)
    b = m.part("Paniers")
    for x in (-0.42, 0.42):
        b.boxb(0.6, 0.6, 0.3, x, -0.05, 2.7, c="galva", bev=0.02)
        b.rod((x, -0.35, 2.95), (x, -0.58, 3.12), 0.04, c="galva", sides=4)
        b.rod((x, -0.55, 3.11), (x, -0.62, 3.14), 0.06, c="red", sides=5)
    return m


def four_pizza():
    m = Model("four_pizza", (3.2, 3.6, 2), CAT, "Four à pizza en briques")
    p = m.part("Four")
    p.boxb(3.2, 2.0, 1.4, 0, 0, 0, c="concrete", bev=0.05)
    p.boxb(3.2, 2.0, 0.15, 0, 0, 1.4, c="tile_white", bev=0.03)
    p.boxb(2.2, 0.06, 0.6, 0, -0.98, 0.2, c="wood_black")  # niche à bois
    for i in range(3):
        p.cyl(0.12, 2.0, at=(-0.9, -0.7 + i * 0.25, 0.35 + (i % 2) * 0.1), rot=(0, 90, 0), c="wood", segs=6, bev=0)
    p.sphere(1.4, at=(0, 0.1, 1.55), c="brick", scale=(1.08, 0.66, 1.0), segs=12, rings=8,
             deform=lambda co: co.__class__((co.x, co.y, max(co.z, 0.0))))
    arch = [(-0.6, 0), (0.6, 0)] + [(0.6 * math.cos(math.radians(a)), 0.4 + 0.6 * math.sin(math.radians(a))) for a in range(0, 181, 30)]
    p.prism(arch, 0.25, at=(0, -0.87, 1.55), c="brick_dark")
    p.prism([(x * 0.85, z * 0.85 + 0.03) for x, z in arch], 0.27, at=(0, -0.87, 1.55), c="soot")
    p.decal(1.2, 0.7, (0, -0.94, 2.65), c="soot", rot=(-35, 0, 0), t=0.03, seed=1)
    p.cyl(0.22, 1.25, at=(0, 0.25, 2.35), c="metal_dark", segs=8, bev=0)
    p.cyl(0.3, 0.12, at=(0, 0.25, 3.48), c="metal_dark", segs=8, bev=0.02)
    f = m.part("Feu")
    for (x, h, c) in ((-0.15, 0.55, "flame_orange"), (0.2, 0.45, "flame_red"), (0.0, 0.35, "flame_yellow")):
        f.lathe([(0, 0), (0.18, 0.08), (0.14, 0.25), (0.05, 0.42), (0, h)], segs=6, at=(x, 0.1, 1.6), c=c, deform=m.noise(0.03, int(x * 10) + 5))
    f.boxb(0.9, 0.5, 0.06, 0, 0.1, 1.55, c="ember", bev=0)
    return m


def panneau_menu():
    m = Model("panneau_menu_lumineux", (9, 2.6, 0.2), CAT, "Panneau menu lumineux", None, "Cadre + écran lumineux, texte ajouté en jeu")
    p = m.part("Cadre")
    p.boxb(9.0, 0.2, 2.6, 0, 0, 0, c="plastic_black", bev=0.05)
    for x in (-1.5, 1.5):
        p.boxb(0.1, 0.06, 2.3, x, -0.11, 0.15, c="plastic_black", bev=0)
    p.box(0.6, 0.02, 0.15, at=(3.8, -0.12, 2.4), rot=(0, 20, 0), c="grey_light", bev=0)
    e = m.part("Ecran")
    for x in (-3.0, 0.0, 3.0):
        e.boxb(2.85, 0.04, 2.3, x, -0.1, 0.15, c="light_white", bev=0)
    e.decal(0.6, 0.4, (3.9, -0.13, 0.5), c="screen_dark", t=0.01, seed=1)  # tube grillé
    return m


MODELS = [
    ("47a_comptoir_boutique_5", lambda: comptoir(5)), ("47b_comptoir_boutique_10", lambda: comptoir(10)),
    ("48_caisse_enregistreuse", caisse), ("49a_etagere_metal_4", lambda: etagere(4)), ("49b_etagere_metal_8", lambda: etagere(8)),
    ("50_frigo_vitre", frigo), ("51_plafonnier_neon", neon), ("52_tabouret_bar", tabouret), ("53_chaise_bois", chaise),
    ("54_table_bistrot", table_bistrot), ("55_table_haute_murale", table_murale), ("56_plante_pot", plante),
    ("57_comptoir_bar", comptoir_bar), ("58_etagere_bouteilles", etagere_bouteilles), ("59_miroir_bar", miroir_bar),
    ("60_cible_flechettes", cible), ("61_tv_courses", tv_pmu), ("62_billard", billard), ("63_jukebox", jukebox),
    ("64_machine_cafe", machine_cafe), ("65_vitrine_patisseries", vitrine_patisseries), ("66_ardoise_menu", ardoise),
    ("67_comptoir_inox", comptoir_inox), ("68_bacs_garnitures", bacs_garnitures), ("69_broche_kebab", broche_kebab),
    ("70_friteuse_pro", friteuse), ("71_four_pizza", four_pizza), ("72_panneau_menu_lumineux", panneau_menu),
]
