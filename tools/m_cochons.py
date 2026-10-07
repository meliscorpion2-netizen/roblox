"""167–178 : jeu de cartes du loup (table, 8 cochons, loups, kiosque). Couleurs propres, style atelier."""
import math

from mathutils import Vector

from lib import Model
from m_quete import clover
from m_slot import casque_shape

CAT = "11_cochons"
PK, PKD = "pink", "rat_pink"


def M(name, dims, title, note=""):
    m = Model(name, dims, CAT, title, None, note)
    m.grime = False
    return m


RH, LH = (-0.78, -0.55, 1.05), (0.78, -0.55, 1.05)  # mains droite (-X) et gauche (+X)


def pig(m, arms_up=False):
    c = m.part("Corps")
    for x in (-0.3, 0.3):
        c.cyl(0.2, 0.4, at=(x, 0, 0.06), c=PK, segs=8)
        c.cyl(0.21, 0.08, at=(x, 0, 0.0), c="wood_black", segs=8, bev=0.02)
    c.sphere(0.7, at=(0, 0, 0.95), c=PK, scale=(1.05, 0.95, 0.9), segs=12, rings=8)
    c.sphere(0.4, at=(0, -0.45, 0.85), c="peach", scale=(1, 0.5, 1), segs=8, rings=5)  # ventre clair
    for s, h in ((-1, RH), (1, LH)):
        hz = h[2] + (0.6 if arms_up else 0)
        c.pipe([(s * 0.6, 0, 1.2), (s * 0.85, -0.25, (1.15 + hz) / 2), (h[0], h[1], hz)], 0.14, c=PK, sides=6)
        c.sphere(0.15, at=(h[0], h[1], hz), c=PK, segs=6, rings=4)
    c.sphere(0.58, at=(0, -0.05, 1.85), c=PK, segs=12, rings=8)
    c.cyl(0.2, 0.16, at=(0, -0.55, 1.78), rot=(90, 0, 0), c=PKD, segs=10, bev=0.04)
    for s in (-1, 1):
        c.cyl(0.04, 0.02, at=(s * 0.07, -0.72, 1.78), rot=(90, 0, 0), c="maroon", segs=6, bev=0)
        c.sphere(0.08, at=(s * 0.2, -0.5, 1.98), c="eye", segs=6, rings=4)
        c.sphere(0.025, at=(s * 0.2 + 0.02, -0.57, 2.01), c="eye_white", segs=4, rings=3)
        c.prism([(-0.13, 0), (0.13, 0), (0, 0.3)], 0.06, at=(s * 0.33, 0.0, 2.25), rot=(15, 0, -s * 30), c=PKD)
    c.pipe([(0, 0.62, 0.9), (0.12, 0.75, 0.95), (0, 0.8, 1.05), (-0.1, 0.72, 1.0)], 0.05, c=PKD, sides=4)
    return c


def cochon(kind):
    titles = {"macon": "Cochon maçon", "bucheron": "Cochon bûcheron", "fermier": "Cochon fermier", "architecte": "Cochon architecte",
              "banquier": "Cochon banquier", "chanceux": "Cochon chanceux", "costaud": "Cochon costaud", "magicien": "Cochon magicien"}
    m = M(f"cochon_{kind}", (2, 2.5, 2), titles[kind])
    pig(m, arms_up=(kind in ("chanceux", "costaud")))
    a = m.part("Accessoire")
    if kind == "macon":
        casque_shape(a, 0, -0.03, 2.25, 0.45)
        a.rod((RH[0], RH[1], RH[2]), (RH[0], RH[1] - 0.25, RH[2] + 0.1), 0.05, c="wood", sides=5)
        a.prism([(-0.15, 0), (0.15, 0), (0, 0.45)], 0.03, at=(RH[0], RH[1] - 0.45, RH[2] + 0.1), rot=(90, 0, 0), c="inox")
        a.box(0.5, 0.26, 0.25, at=(LH[0], LH[1] - 0.15, LH[2]), c="brick", bev=0.04)
    elif kind == "bucheron":
        a.rod((RH[0], RH[1] + 0.1, RH[2] - 0.3), (RH[0], RH[1] - 0.1, RH[2] + 0.7), 0.06, c="wood_light", sides=6)
        a.prism([(0, 0), (0.35, -0.1), (0.4, 0.3), (0, 0.2)], 0.06, at=(RH[0], RH[1] - 0.1, RH[2] + 0.55), rot=(0, 0, 90), c="inox")
        a.box(0.25, 0.15, 1.5, at=(LH[0] + 0.05, LH[1] + 0.1, LH[2] + 0.1), rot=(0, 15, 0), c="wood_light", bev=0.03)
        a.box(1.25, 0.05, 0.12, at=(0, 0, 2.35), c="red", bev=0.02)  # bandeau à carreaux
    elif kind == "fermier":
        a.box(1.3, 0.6, 0.6, at=(0, -0.85, 1.05), c="sand", bev=0.1, deform=m.noise(0.02, 1))
        for x in (-0.3, 0.3):
            a.box(0.05, 0.62, 0.62, at=(x, -0.85, 1.05), c="red_dark", bev=0)
        a.lathe([(0, 0), (0.75, 0), (0.75, 0.04), (0.38, 0.06), (0.35, 0.35), (0, 0.38)], segs=10, at=(0, -0.05, 2.25), c="flower_yellow")
    elif kind == "architecte":
        a.cyl(0.13, 0.9, at=(LH[0] - 0.45, LH[1], LH[2] + 0.05), rot=(0, 90, 0), c="blue", segs=8, bev=0.02)
        a.cyl(0.035, 0.6, at=(RH[0], RH[1], RH[2] - 0.1), rot=(-20, 0, 0), c="flower_yellow", segs=6, bev=0)
        a.lathe([(0.035, 0), (0, 0.1)], segs=6, at=(RH[0], RH[1] - 0.2, RH[2] + 0.46), rot=(-20, 0, 0), c="wood_dark", cap0=True)
        a.box(0.25, 0.05, 0.05, at=(0, -0.52, 2.0), c="black", bev=0)  # lunettes
        for s in (-1, 1):
            a.torus(0.09, 0.02, at=(s * 0.2, -0.56, 1.98), rot=(90, 0, 0), c="black", segs=8, sides=3)
    elif kind == "banquier":
        a.cyl(0.42, 0.04, at=(0, -0.05, 2.32), c="black", segs=12, bev=0)
        a.cyl(0.28, 0.5, at=(0, -0.05, 2.34), c="black", segs=12, bev=0.03)
        a.cyl(0.285, 0.08, at=(0, -0.05, 2.4), c="red", segs=12, bev=0)
        a.sphere(0.35, at=(LH[0], LH[1] - 0.15, LH[2] - 0.15), c="jute", segs=8, rings=6)
        a.cyl(0.1, 0.12, at=(LH[0], LH[1] - 0.15, LH[2] + 0.17), c="jute", segs=6, bev=0)
        for k in range(3):
            a.cyl(0.12, 0.04, at=(LH[0] - 0.1 + k * 0.1, LH[1] - 0.2, LH[2] + 0.28 + k * 0.03), rot=(30, 0, 0), c="gold", segs=8, bev=0)
        a.torus(0.06, 0.012, at=(-0.2, -0.56, 1.98), rot=(90, 0, 0), c="gold", segs=8, sides=3)  # monocle
    elif kind == "chanceux":
        h = (RH[0], RH[1], RH[2] + 0.6)
        a.rod(h, (h[0], h[1], h[2] + 0.3), 0.03, c="green", sides=4)
        clover(a, 0.22, h[0], h[2] + 0.5, h[1], 0.07, 0.025)
        a.sphere(0.06, at=(0.35, -0.5, 1.6), c="light_green", segs=5, rings=3)  # étincelle
    elif kind == "costaud":
        for h in (RH, LH):
            hz = h[2] + 0.6
            a.rod((h[0] - 0.3, h[1], hz), (h[0] + 0.3, h[1], hz), 0.04, c="metal_dark", sides=5)
            for s in (-1, 1):
                a.cyl(0.2, 0.12, at=(h[0] + s * 0.3 - 0.06, h[1], hz), rot=(0, 90, 0), c="black", segs=10, bev=0.02)
        a.torus(0.57, 0.06, at=(0, -0.05, 2.05), c="red", segs=12, sides=4)  # bandeau
    elif kind == "magicien":
        a.cyl(0.55, 0.04, at=(0, -0.05, 2.3), c="purple", segs=12, bev=0)
        a.lathe([(0, 0), (0.33, 0), (0.15, 0.5), (0.05, 0.75), (0, 0.8)], segs=10, at=(0, -0.05, 2.32), c="purple")
        a.sphere(0.05, at=(0.15, -0.35, 2.55), c="flower_yellow", segs=5, rings=3)
        a.rod((RH[0], RH[1] + 0.1, RH[2] - 0.1), (RH[0] - 0.05, RH[1] - 0.4, RH[2] + 0.4), 0.035, c="black", sides=5)
        a.sphere(0.05, at=(RH[0] - 0.05, RH[1] - 0.42, RH[2] + 0.43), c="white", segs=5, rings=3)
        a.lathe([(0, 0), (0.4, 0.05), (0.38, 0.6), (0, 0.65)], segs=10, at=(0, 0.75, 0.6), rot=(-80, 0, 0), c="red")  # cape
    return m


def wolf_head(p, x, y, z, s, g="grey", gl="grey_light", mouth=None):
    p.sphere(0.6 * s, at=(x, y, z), c=g, segs=12, rings=8)
    p.lathe([(0, 0), (0.3 * s, 0), (0.24 * s, 0.35 * s), (0.1 * s, 0.6 * s), (0, 0.63 * s)], segs=8, at=(x, y - 0.3 * s, z - 0.12 * s),
            rot=(90, 0, 0), c=gl)
    p.sphere(0.1 * s, at=(x, y - 0.95 * s, z - 0.1 * s), c="black", segs=6, rings=4)
    for k in (-1, 1):
        p.prism([(-0.2 * s, 0), (0.2 * s, 0), (0.03 * s, 0.55 * s)], 0.12 * s, at=(x + k * 0.33 * s, y, z + 0.38 * s), rot=(0, 0, -k * 15), c=g)
        p.prism([(-0.1 * s, 0.05 * s), (0.1 * s, 0.05 * s), (0.02 * s, 0.38 * s)], 0.13 * s, at=(x + k * 0.33 * s, y - 0.01, z + 0.38 * s),
                rot=(0, 0, -k * 15), c=PKD)
        p.sphere(0.09 * s, at=(x + k * 0.22 * s, y - 0.5 * s, z + 0.15 * s), c="flower_yellow", segs=6, rings=4)
        p.sphere(0.04 * s, at=(x + k * 0.22 * s, y - 0.58 * s, z + 0.16 * s), c="eye", segs=4, rings=3)
        p.box(0.25 * s, 0.06 * s, 0.07 * s, at=(x + k * 0.2 * s, y - 0.52 * s, z + 0.3 * s), rot=(0, k * 22, 0), c="iron", bev=0)


def table_loup():
    m = M("table_loup_cartes", (6, 6, 4), "Table de jeu du loup", "Bois et métal façon atelier ; pas de casino")
    t, pl, lo, ar, pa = m.part("Table"), m.part("Plateau"), m.part("Loup"), m.part("Ardoise"), m.part("Paquet")
    for x in (-2.6, 2.6):
        for y in (-1.5, 1.5):
            t.boxb(0.35, 0.35, 2.8, x, y, 0, c="wood", bev=0.05)
            t.boxb(0.42, 0.42, 0.25, x, y, 0, c="metal_dark", bev=0.03)
        t.boxb(0.25, 3.2, 0.25, x, 0, 0.6, c="wood_dark", bev=0.03)
    t.boxb(5.4, 0.25, 0.25, 0, 0, 0.6, c="wood_dark", bev=0.03)
    for x in (-2.6, 2.6):
        for y in (-1.5, 1.5):
            t.boxb(0.5, 0.5, 0.06, x, y, 2.6, c="metal_dark", bev=0.01)
    for i in range(6):
        pl.boxb(0.98, 3.9, 0.2, -2.5 + i * 1.0, 0, 2.8, c=("wood_light" if i % 2 else "pallet"), bev=0.04)
    pl.boxb(6.0, 0.15, 0.15, 0, -1.95, 2.85, c="metal_dark", bev=0.02)
    pl.boxb(6.0, 0.15, 0.15, 0, 1.95, 2.85, c="metal_dark", bev=0.02)
    for x in (-2.8, -1.2, 1.2, 2.8):
        pl.sphere(0.05, at=(x, -2.03, 2.93), c="metal_light", segs=4, rings=3)  # rivets
    # dosseret et tête de loup sculptée
    lo.boxb(4.0, 0.3, 2.0, 0, 1.75, 3.0, c="wood", bev=0.06)
    lo.boxb(0.3, 0.3, 3.2, -2.1, 1.75, 2.8, c="metal_dark", bev=0.03)
    lo.boxb(0.3, 0.3, 3.2, 2.1, 1.75, 2.8, c="metal_dark", bev=0.03)
    wolf_head(lo, 0, 1.5, 4.9, 1.3, g="wood_dark", gl="wood")
    ar.boxb(1.6, 0.1, 1.2, -1.2, 1.55, 3.25, c="slate", bev=0)
    ar.boxb(1.8, 0.14, 1.4, -1.2, 1.6, 3.15, c="wood_light", bev=0.03)
    ar.boxb(0.3, 0.12, 0.05, -1.2, 1.5, 3.2, c="white", bev=0)  # craie
    pa.boxb(0.5, 0.75, 0.25, 0.6, -0.5, 3.0, c="red", bev=0.03)
    pa.boxb(0.48, 0.73, 0.02, 0.6, -0.5, 3.25, c="white", bev=0)
    for k in range(3):  # cartes étalées
        pa.box(0.5, 0.75, 0.02, at=(-0.6 + k * 0.35, -0.8, 3.02 + k * 0.01), rot=(0, 0, -20 + k * 20), c=("white" if k != 1 else "cream"), bev=0)
    return m


def louveteau():
    m = M("louveteau", (3, 4, 3), "Louveteau", "Boss de la manche paille")
    c = m.part("Corps")
    g = "grey"
    for x in (-0.45, 0.45):
        c.cyl(0.28, 0.6, at=(x, 0, 0.05), c=g, segs=8)
        c.box(0.42, 0.6, 0.2, at=(x, -0.15, 0.1), c="grey_light", bev=0.08)
    c.sphere(0.95, at=(0, 0.05, 1.3), c=g, scale=(1, 0.9, 0.95), segs=12, rings=8)
    c.sphere(0.6, at=(0, -0.55, 1.2), c="grey_light", scale=(1, 0.5, 1), segs=8, rings=5)
    for s in (-1, 1):
        c.pipe([(s * 0.8, 0, 1.7), (s * 1.25, -0.35, 1.35), (s * 1.1, -0.75, 1.0)], 0.2, c=g, sides=6)
        c.sphere(0.22, at=(s * 1.1, -0.78, 0.98), c="grey_light", segs=6, rings=4)
    wolf_head(c, 0, -0.1, 2.85, 1.5)
    c.pipe([(0, 0.8, 1.0), (0.4, 1.2, 1.3), (0.6, 1.3, 1.8)], 0.22, c=g, sides=6)
    for k in range(5):  # brins de paille sur la tête et dans la gueule
        c.rod((-0.3 + k * 0.15, -0.2, 3.65), (-0.45 + k * 0.25, -0.35, 3.95), 0.025, c="flower_yellow", sides=3)
    c.rod((0.1, -1.3, 2.6), (0.7, -1.2, 2.75), 0.03, c="flower_yellow", sides=3)
    return m


def grand_loup():
    m = M("grand_mechant_loup_souffle", (5, 7, 4), "Grand méchant loup qui souffle")
    c = m.part("Corps")
    g = "grey"
    for x in (-0.5, 0.5):
        c.cyl(0.3, 2.2, at=(x, 0.3, 0.2), r2=0.35, c="blue", segs=8)  # salopette
        c.box(0.5, 0.9, 0.3, at=(x, 0.05, 0.15), c="grey_light", bev=0.1)
    c.sphere(1.0, at=(0, 0.3, 3.0), c="blue", scale=(1, 0.8, 1.15), segs=12, rings=8)
    c.sphere(0.9, at=(0, 0.3, 3.65), c=g, scale=(1.05, 0.8, 0.7), segs=10, rings=6)
    for s in (-1, 1):
        c.pipe([(s * 0.9, 0.3, 3.8), (s * 1.6, 0.6, 3.3), (s * 2.0, 0.9, 3.9)], 0.24, c=g, sides=6)  # bras en arrière (élan)
        c.sphere(0.26, at=(s * 2.05, 0.92, 4.0), c="grey_light", segs=6, rings=4)
    c.sphere(0.85, at=(0, 0.2, 5.3), c=g, segs=12, rings=8)
    for s in (-1, 1):
        c.sphere(0.55, at=(s * 0.55, -0.35, 5.05), c=g, segs=10, rings=7)  # joues gonflées
        c.prism([(-0.3, 0), (0.3, 0), (0.05, 0.85)], 0.2, at=(s * 0.48, 0.25, 5.95), rot=(0, 0, -s * 15), c=g)
        c.sphere(0.13, at=(s * 0.3, -0.62, 5.6), c="flower_yellow", segs=6, rings=4)
        c.sphere(0.06, at=(s * 0.3, -0.73, 5.62), c="eye", segs=4, rings=3)
        c.box(0.38, 0.08, 0.1, at=(s * 0.28, -0.62, 5.82), rot=(0, s * 25, 0), c="iron", bev=0)
    c.lathe([(0, 0), (0.35, 0), (0.25, 0.4), (0.15, 0.6), (0, 0.62)], segs=8, at=(0, -0.55, 5.0), rot=(90, 0, 0), c="grey_light")
    c.torus(0.16, 0.08, at=(0, -1.15, 4.92), rot=(90, 0, 0), c=PKD, segs=10, sides=5)  # lèvres en cul de poule
    c.sphere(0.12, at=(0, -1.12, 5.18), c="black", segs=6, rings=4)
    c.pipe([(0, 1.05, 2.2), (0.5, 1.6, 2.0), (0.9, 1.75, 2.6)], 0.3, c=g, sides=6)
    sf = m.part("Souffle")
    for k, (r, y, z, c2) in enumerate(((0.35, -1.5, 4.9, "white"), (0.55, -2.2, 4.8, "sky"), (0.8, -3.0, 4.6, "white"))):
        pts = [(r * math.cos(a) * (1 - a / 14), y - a * 0.05, z + r * math.sin(a) * (1 - a / 14)) for a in [i * 0.5 for i in range(14)]]
        sf.pipe(pts, 0.07 + 0.02 * k, c=c2, sides=5)
    for k in range(5):
        sf.pipe([(-1.0 + k * 0.5, -1.6, 5.4 - k * 0.15), (-1.3 + k * 0.65, -2.6, 5.6 - k * 0.3), (-1.6 + k * 0.8, -3.6, 5.3 - k * 0.4)],
                0.05, c="sky", sides=4)
    return m


def kiosque():
    m = M("kiosque_pochettes", (6, 8, 5), "Kiosque à pochettes", "Enseigne vierge")
    k, po, en = m.part("Kiosque"), m.part("Pochettes"), m.part("Enseigne")
    k.boxb(6, 5, 0.3, 0, 0, 0, c="wood_dark", bev=0.05)
    k.boxb(5.6, 4.2, 3.0, 0, 0.3, 0.3, c="wood_light", bev=0.08)
    k.boxb(6, 2, 0.25, 0, -1.4, 3.3, c="wood", bev=0.05)  # comptoir
    for x in (-2.75, 2.75):
        k.boxb(0.3, 0.3, 4.4, x, -2.2, 0.3, c="metal_dark", bev=0.03)
    k.boxb(5.6, 0.2, 2.8, 0, 2.3, 3.5, c="wood_light", bev=0.05)
    for z in (4.0, 5.0):
        k.boxb(5.2, 0.6, 0.1, 0, 2.0, z, c="wood", bev=0.02)
    k.prism([(-3.3, 0), (3.3, 0), (0, 1.2)], 5.2, at=(0, 0, 6.6), c="red", plane="XZ", bev=0.05)
    k.boxb(6.4, 5.2, 0.3, 0, 0, 6.3, c="wood_dark", bev=0.05)
    for i in range(10):
        k.boxb(0.62, 0.1, 0.5, -2.8 + i * 0.62, -2.6, 5.9, c=("red" if i % 2 else "white"), bev=0)  # lambrequin
    cols = ["red", "blue", "flower_yellow", "green", "purple", "orange"]
    for row, z in enumerate((4.1, 5.1)):
        for i in range(7):
            po.box(0.5, 0.06, 0.7, at=(-2.2 + i * 0.73, 1.75, z + 0.4), rot=(-10, 0, 0), c=cols[(i + row) % 6], bev=0.02)
    for i in range(5):
        po.box(0.5, 0.7, 0.06, at=(-1.6 + i * 0.6, -1.4, 3.6), rot=(0, 0, -10 + i * 5), c=cols[i], bev=0.02)
    en.boxb(4.2, 0.2, 0.9, 0, -2.65, 6.6, c="cream", bev=0.05)
    return m


MODELS = [("167_table_loup_cartes", table_loup)] + [
    (f"{168 + i}_cochon_{k}", (lambda k=k: cochon(k))) for i, k in
    enumerate(("macon", "bucheron", "fermier", "architecte", "banquier", "chanceux", "costaud", "magicien"))
] + [("176_louveteau", louveteau), ("177_grand_mechant_loup_souffle", grand_loup), ("178_kiosque_pochettes", kiosque)]
