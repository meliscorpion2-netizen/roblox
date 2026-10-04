"""100–112 : symboles de la machine à sous (thème « les trois petits cochons » version chantier).

Couleurs propres (pas de crasse) : ce sont des symboles lisibles, pas des props de rue.
"""
import math

from lib import Model
from m_quete import stroke

CAT = "08_slot"


def M(name, dims, title, note=""):
    m = Model(name, dims, CAT, title, None, note)
    m.grime = False
    return m


def casque_shape(p, cx, cy, z0, s, c="yellow"):
    """Casque de chantier : calotte, nervure, visière avant (-Y)."""
    p.sphere(0.7 * s, at=(cx, cy, z0), c=c, segs=14, rings=8, scale=(1.0, 1.1, 0.98),
             deform=lambda co: co.__class__((co.x, co.y, max(co.z, 0.0))))
    p.sphere(0.7 * s, at=(cx, cy, z0), c=c, segs=10, rings=8, scale=(0.22, 1.13, 1.05),
             deform=lambda co: co.__class__((co.x, co.y, max(co.z, 0.0))))  # nervure centrale
    p.cyl(0.78 * s, 0.07 * s, at=(cx, cy - 0.12 * s, z0), c=c, segs=16, bev=0.02 * s, deform=lambda co: co.__class__((co.x, co.y * 1.15 - (0.12 * s if co.y < 0 else 0), co.z)))


def casque():
    m = M("casque_chantier", (1.6, 1.0, 1.8), "Casque de chantier", "Symbole scatter")
    p = m.part("Casque")
    casque_shape(p, 0, 0, 0.08, 1.0)
    p.cyl(0.62, 0.08, at=(0, 0, 0.0), c="yellow_dark", segs=14, bev=0.02)
    return m


def marteau():
    m = M("marteau", (0.6, 1.8, 0.3), "Marteau", "Petit symbole")
    h = m.part("Manche")
    h.cyl(0.09, 1.45, c="wood_light", segs=8, bev=0.03)
    h.cyl(0.11, 0.45, at=(0, 0, 0.05), c="red", segs=8, bev=0.03)  # grip
    t = m.part("Tete")
    t.box(0.34, 0.26, 0.26, at=(-0.13, 0, 1.6), c="metal", bev=0.04)
    t.cyl(0.13, 0.08, at=(-0.36, 0, 1.6), rot=(0, -90, 0), c="metal_light", segs=10, bev=0.02)
    t.prism([(0.0, -0.12), (0.3, 0.02), (0.28, 0.1), (0.0, 0.12)], 0.22, at=(0.03, 0, 1.6), c="metal")  # panne fendue
    return m


def scie():
    m = M("scie_egoine", (2.0, 0.8, 0.1), "Scie égoïne", "Petit symbole")
    b = m.part("Lame")
    b.prism([(-1.0, 0.12), (0.45, 0.12), (0.45, 0.75), (-1.0, 0.42)], 0.03, at=(0, 0, 0), c="inox")
    teeth = [(-1.0 + i * 0.1, 0.12) for i in range(15)]
    for x, z in teeth:
        b.prism([(x, z + 0.01), (x + 0.1, z + 0.01), (x + 0.05, z - 0.1)], 0.03, at=(0, 0, 0.0), c="inox")
    h = m.part("Poignee")
    out = [(0.4, 0.08), (0.75, 0.08), (1.0, 0.3), (1.0, 0.75), (0.75, 0.8), (0.4, 0.8)]
    h.prism(out, 0.1, at=(0, 0, 0), c="wood_red", bev=0.03)
    h.prism([(0.62, 0.3), (0.85, 0.36), (0.85, 0.62), (0.62, 0.62)], 0.12, at=(0, 0, 0), c="wood_black")  # trou de prise
    for z in (0.3, 0.6):
        h.cyl(0.04, 0.12, at=(0.5, -0.06, z), rot=(-90, 0, 0), c="brass", segs=6, bev=0)
    return m


def brique():
    m = M("brique_rouge", (1.2, 0.6, 0.6), "Brique rouge", "Petit symbole")
    p = m.part("Brique")
    p.boxb(1.2, 0.6, 0.6, c="brick", bev=0.07, deform=m.noise(0.008, 1))
    for x in (-0.3, 0.0, 0.3):
        p.cyl(0.08, 0.02, at=(x, 0, 0.59), c="brick_dark", segs=8, bev=0)
    return m


def planche():
    m = M("planche_bois", (2.0, 0.3, 0.6), "Planche de bois", "Petit symbole")
    p = m.part("Planche")
    p.boxb(2.0, 0.6, 0.3, c="wood_light", bev=0.04)
    for k, y in enumerate((-0.18, 0.02, 0.2)):
        p.box(1.7 - 0.3 * k, 0.025, 0.01, at=(0.1 * k, y, 0.302), c="wood", bev=0)  # veinage
    p.cyl(0.06, 0.012, at=(-0.5, 0.05, 0.3), c="wood_dark", segs=8, bev=0)  # nœud
    p.cyl(0.03, 0.02, at=(0.85, 0.0, 0.3), c="metal_dark", segs=6, bev=0)  # clou
    return m


def paille():
    m = M("botte_paille", (1.4, 1.0, 1.0), "Botte de paille", "Petit symbole")
    p = m.part("Paille")
    p.boxb(1.4, 1.0, 1.0, c="sand", bev=0.14, deform=m.noise(0.03, 1))
    for i in range(10):  # brins qui dépassent
        a = i * 0.7
        p.rod((-0.7, 0.4 * math.cos(a), 0.5 + 0.4 * math.sin(a)), (-0.78, 0.45 * math.cos(a), 0.5 + 0.45 * math.sin(a)), 0.02, c="flower_yellow", sides=3)
        p.rod((0.7, 0.4 * math.sin(a), 0.5 + 0.4 * math.cos(a)), (0.78, 0.45 * math.sin(a), 0.5 + 0.45 * math.cos(a)), 0.02, c="flower_yellow", sides=3)
    l = m.part("Lien")
    for x in (-0.35, 0.35):
        l.boxb(0.07, 1.04, 1.04, x, 0, -0.02, c="red_dark", bev=0.02)
    return m


def plan():
    m = M("plan_maison", (1.6, 0.4, 1.2), "Plan de maison", "Symbole moyen")
    p = m.part("Plan")
    p.cyl(0.2, 1.6, at=(-0.8, 0.38, 0.2), rot=(0, 90, 0), c="blue", segs=12, bev=0.02)
    p.cyl(0.08, 1.62, at=(-0.81, 0.38, 0.2), rot=(0, 90, 0), c="blue_dark", segs=8, bev=0)
    p.box(1.5, 0.9, 0.03, at=(0, -0.15, 0.02), rot=(-3, 0, 0), c="blue", bev=0,
          deform=lambda co: co.__class__((co.x, co.y, co.z + 0.06 * max(0, -co.y - 0.25))))  # bord qui rebique
    w = "white"
    for a, b in (((-0.5, -0.45), (0.3, -0.45)), ((0.3, -0.45), (0.3, 0.15)), ((0.3, 0.15), (-0.5, 0.15)), ((-0.5, 0.15), (-0.5, -0.45)),
                 ((-0.1, -0.45), (-0.1, 0.15)), ((-0.5, -0.15), (-0.1, -0.15)), ((0.45, -0.45), (0.6, -0.45)), ((0.45, 0.15), (0.6, 0.15))):
        p.rod((a[0], a[1] - 0.05, 0.05), (b[0], b[1] - 0.05, 0.05), 0.012, c=w, sides=3)
    p.cyl(0.07, 0.01, at=(0.1, -0.3, 0.045), c=w, segs=10, bev=0)
    return m


def brick_lines(p, w, d, z0, h, step=0.2):
    k = 0
    z = z0 + step
    while z < z0 + h - 0.05:
        p.boxb(w + 0.02, d + 0.02, 0.02, 0, 0, z, c="brick_dark", bev=0)
        z += step
        k += 1


def maison():
    m = M("maison_briques", (2.0, 2.0, 2.0), "Petite maison en briques", "Symbole moyen, sert aussi pendant la construction")
    w = m.part("Murs")
    w.boxb(1.7, 1.6, 1.15, c="brick", bev=0.04)
    brick_lines(w, 1.7, 1.6, 0, 1.15)
    w.boxb(0.3, 0.3, 0.6, 0.5, 0.25, 1.3, c="brick_dark", bev=0.03)  # cheminée
    w.boxb(0.36, 0.12, 0.36, -0.5, -0.8, 0.45, c="white", bev=0.02)
    w.boxb(0.28, 0.13, 0.28, -0.5, -0.8, 0.49, c="glass", bev=0)
    t = m.part("Toit")
    t.prism([(-1.0, 0), (1.0, 0), (0, 0.85)], 2.0, at=(0, 0, 1.15), c="red", bev=0.04)
    p = m.part("Porte", pivot=(0.1, -0.8, 0))
    p.boxb(0.42, 0.08, 0.7, 0.3, -0.81, 0.0, c="wood", bev=0.02)
    p.cyl(0.03, 0.04, at=(0.43, -0.85, 0.35), rot=(90, 0, 0), c="gold", segs=6, bev=0)
    return m


def manoir():
    m = M("manoir", (3.0, 3.0, 2.4), "Grande maison (manoir)", "Symbole fort")
    w = m.part("Murs")
    w.boxb(2.8, 2.0, 1.9, c="brick", bev=0.05)
    brick_lines(w, 2.8, 2.0, 0, 1.9, 0.24)
    w.boxb(2.9, 2.1, 0.12, 0, 0, 0.0, c="concrete", bev=0.03)
    w.boxb(2.9, 2.1, 0.08, 0, 0, 0.95, c="cream", bev=0.02)  # bandeau d'étage
    for x in (-0.35, 0.35):
        w.cyl(0.07, 1.2, at=(x, -1.15, 0.12), c="cream", segs=8, bev=0)  # colonnes
    w.boxb(1.0, 0.5, 0.1, 0, -1.1, 1.3, c="cream", bev=0.02)  # marquise
    for x in (-0.8, 0.8):
        w.boxb(0.3, 0.3, 0.6, x, 0.3, 2.3, c="brick_dark", bev=0.03)
    t = m.part("Toit")
    t.prism([(-1.5, 0), (1.5, 0), (1.0, 0.9), (-1.0, 0.9)], 2.4, at=(0, 0, 1.9), c="blue_dark", bev=0.05)
    f = m.part("Fenetres")
    for x in (-1.0, 1.0):
        for z in (0.35, 1.25):
            w.boxb(0.5, 0.1, 0.5, x, -1.0, z, c="white", bev=0.02)
            f.boxb(0.4, 0.12, 0.4, x, -1.0, z + 0.05, c="light_warm", bev=0)
    w.boxb(0.5, 0.1, 0.5, 0, -1.0, 1.25, c="white", bev=0.02)
    f.boxb(0.4, 0.12, 0.4, 0, -1.0, 1.3, c="light_warm", bev=0)
    p = m.part("Porte", pivot=(-0.22, -1.0, 0.12))
    p.boxb(0.44, 0.08, 0.75, 0, -1.02, 0.12, c="wood_dark", bev=0.02)
    p.cyl(0.03, 0.04, at=(0.12, -1.07, 0.5), rot=(90, 0, 0), c="gold", segs=6, bev=0)
    return m


def cochon():
    m = M("cochon_constructeur", (1.6, 2.4, 1.2), "Cochon constructeur", "Symbole le plus fort")
    c = m.part("Corps")
    pk, pkd = "pink", "rat_pink"
    for x in (-0.25, 0.25):
        c.cyl(0.17, 0.5, at=(x, 0, 0.05), c=pk, segs=8)
        c.cyl(0.18, 0.08, at=(x, 0, 0.0), c="wood_black", segs=8, bev=0.02)  # sabots
    c.sphere(0.5, at=(0, 0, 0.9), c=pk, scale=(1.05, 0.9, 1.0), segs=12, rings=8)
    for s in (-1, 1):
        c.pipe([(s * 0.48, 0, 1.15), (s * 0.68, -0.1, 0.9), (s * 0.62, -0.25, 0.68)], 0.12, c=pk, sides=6)
        c.sphere(0.12, at=(s * 0.62, -0.27, 0.64), c=pk, segs=6, rings=4)
    c.sphere(0.4, at=(0, -0.05, 1.68), c=pk, segs=12, rings=8)
    c.cyl(0.15, 0.14, at=(0, -0.38, 1.62), rot=(90, 0, 0), c=pkd, segs=10, bev=0.03)
    for s in (-1, 1):
        c.cyl(0.03, 0.02, at=(s * 0.06, -0.52, 1.62), rot=(90, 0, 0), c="maroon", segs=6, bev=0)
        c.sphere(0.06, at=(s * 0.15, -0.34, 1.82), c="eye", segs=6, rings=4)
        c.sphere(0.02, at=(s * 0.15 + 0.02, -0.39, 1.84), c="eye_white", segs=4, rings=3)
        c.prism([(-0.1, 0), (0.1, 0), (0, 0.22)], 0.05, at=(s * 0.27, 0.0, 1.95), rot=(15, 0, -s * 30), c=pkd)
    c.pipe([(0, 0.45, 0.8), (0.1, 0.58, 0.85), (0.0, 0.62, 0.95), (-0.08, 0.55, 0.9)], 0.04, c=pkd, sides=4)  # queue en tire-bouchon
    k = m.part("Casque")
    casque_shape(k, 0, -0.02, 1.88, 0.5)
    o = m.part("Outils")
    o.torus(0.49, 0.06, at=(0, 0, 0.62), c="leather", segs=16, sides=4, sz=1.5)
    o.boxb(0.12, 0.12, 0.1, 0, -0.5, 0.56, c="gold", bev=0.02)
    o.boxb(0.2, 0.12, 0.22, -0.35, -0.4, 0.45, c="leather", bev=0.03)  # poche
    o.cyl(0.03, 0.5, at=(0.32, -0.45, 0.35), c="wood_light", segs=6, bev=0)  # marteau à la ceinture
    o.boxb(0.2, 0.08, 0.08, 0.32, -0.45, 0.82, c="metal", bev=0.01)
    o.boxb(0.03, 0.05, 0.3, -0.4, -0.47, 0.6, c="chrome", bev=0)  # tournevis
    return m


def loup():
    m = M("loup_salopette", (1.8, 2.6, 1.2), "Loup en salopette", "Symbole wild ; Yeux en néon")
    c = m.part("Corps")
    g, gl = "grey", "grey_light"
    for x in (-0.25, 0.25):
        c.cyl(0.14, 0.75, at=(x, 0, 0.1), c="blue", segs=8)
        c.box(0.26, 0.4, 0.14, at=(x, -0.08, 0.07), c=g, bev=0.05)  # pattes
    c.sphere(0.45, at=(0, 0, 1.05), c="blue", scale=(1.0, 0.85, 1.05), segs=12, rings=8)
    c.sphere(0.4, at=(0, 0.02, 1.35), c=g, scale=(1.0, 0.85, 0.8), segs=10, rings=6)
    c.boxb(0.5, 0.06, 0.4, 0, -0.38, 1.0, c="blue_dark", bev=0.02)
    for s in (-1, 1):
        c.rod((s * 0.2, -0.36, 1.38), (s * 0.2, -0.3, 1.6), 0.035, c="blue_dark", sides=4)  # bretelles
        c.cyl(0.04, 0.03, at=(s * 0.2, -0.4, 1.38), rot=(90, 0, 0), c="gold", segs=6, bev=0)
        c.pipe([(s * 0.42, 0, 1.45), (s * 0.75, -0.1, 1.2), (s * 0.8, -0.2, 0.9)], 0.11, c=g, sides=6)
        c.sphere(0.13, at=(s * 0.8, -0.22, 0.85), c=gl, segs=6, rings=4)
        c.prism([(-0.13, 0), (0.13, 0), (0.02, 0.38)], 0.08, at=(s * 0.24, 0.05, 2.15), rot=(0, 0, -s * 15), c=g)
        c.prism([(-0.07, 0.03), (0.07, 0.03), (0.01, 0.25)], 0.09, at=(s * 0.24, 0.03, 2.16), rot=(0, 0, -s * 15), c="rat_pink")
        c.box(0.2, 0.05, 0.06, at=(s * 0.16, -0.36, 2.14), rot=(0, s * 20, 0), c="iron", bev=0)  # sourcils méchants
    c.sphere(0.38, at=(0, 0, 1.88), c=g, segs=12, rings=8)
    c.lathe([(0, 0), (0.2, 0.0), (0.16, 0.25), (0.07, 0.4), (0, 0.42)], segs=8, at=(0, -0.2, 1.8), rot=(90, 0, 0), c=gl)
    c.sphere(0.07, at=(0, -0.62, 1.82), c="black", segs=6, rings=4)  # truffe
    c.prism([(-0.15, 0), (0.15, 0), (0.1, -0.05), (-0.1, -0.05)], 0.02, at=(0, -0.49, 1.68), c="eye_white")  # crocs
    c.pipe([(0, 0.35, 0.9), (0.15, 0.6, 0.7), (0.35, 0.62, 0.55)], 0.13, c=g, sides=6)  # queue
    c.sphere(0.12, at=(0.38, 0.6, 0.53), c=gl, segs=6, rings=4)
    y = m.part("Yeux")
    for s in (-1, 1):
        y.sphere(0.08, at=(s * 0.15, -0.32, 2.0), c="light_amber", scale=(1, 0.6, 0.8), segs=8, rings=5)
    return m


def gemme():
    m = M("gemme", (1.0, 1.0, 1.0), "Gemme taillée", "Symbole jackpot ; recolorée en néon Mini/Minor/Major/Grand")
    p = m.part("Gemme")
    p.lathe([(0, 0), (0.5, 0.58), (0.5, 0.64), (0.4, 0.8), (0.28, 0.92), (0, 0.92)], segs=8, c="light_white")
    return m


def token():
    m = M("bonus_token", (1.6, 1.6, 0.3), "Bonus Token", "Contour à faire briller")
    p = m.part("Piece")
    p.cyl(0.72, 0.24, at=(0, -0.12, 0.8), rot=(-90, 0, 0), c="gold", segs=24, bev=0.04)
    p.torus(0.6, 0.025, at=(0, -0.125, 0.8), rot=(90, 0, 0), c="yellow_dark", segs=24, sides=4)
    for k in range(24):  # crénelage
        a = 2 * math.pi * k / 24
        p.box(0.05, 0.22, 0.05, at=(0.73 * math.cos(a), 0, 0.8 + 0.73 * math.sin(a)), rot=(0, -math.degrees(a), 0), c="yellow_dark", bev=0)
    g = m.part("Gravure")
    head = [(-0.3, 0.05), (-0.2, -0.2), (0, -0.38), (0.2, -0.2), (0.3, 0.05), (0.38, 0.4), (0.18, 0.2), (-0.18, 0.2), (-0.38, 0.4)]
    g.prism([(x, z + 0.8) for x, z in head], 0.04, at=(0, -0.14, 0), c="brass")
    g.prism([(x, z + 0.8) for x, z in [(-0.09, -0.08), (0.09, -0.08), (0, -0.33)]], 0.02, at=(0, -0.165, 0), c="yellow_dark")  # museau
    for s in (-1, 1):
        g.prism([(s * 0.06 + x, z + 0.8) for x, z in [(-0.06, 0.05), (0.06, 0.02), (0.0, 0.08)]], 0.02, at=(s * 0.08, -0.165, 0), c="yellow_dark")  # yeux
    ct = m.part("Contour")
    ct.torus(0.74, 0.06, at=(0, 0, 0.8), rot=(90, 0, 0), c="light_warm", segs=24, sides=6, sz=2.4)
    return m


MODELS = [
    ("100_casque_chantier", casque), ("101_marteau", marteau), ("102_scie_egoine", scie), ("103_brique_rouge", brique),
    ("104_planche_bois", planche), ("105_botte_paille", paille), ("106_plan_maison", plan), ("107_maison_briques", maison),
    ("108_manoir", manoir), ("109_cochon_constructeur", cochon), ("110_loup_salopette", loup), ("111_gemme", gemme),
    ("112_bonus_token", token),
]
