"""73–95 : hôtel, presse, pharmacie, coiffeur, laverie, sport, cordonnerie, friperie, fleuriste, prêteur sur gages."""
import math
import random

from lib import Model
from m_magasins import CAT, bottle


# ---------------------------------------------------------------------------
# Hôtel
# ---------------------------------------------------------------------------

def reception():
    m = Model("comptoir_reception", (9, 3.4, 1.6), CAT, "Comptoir de réception")
    p = m.part("Comptoir")
    p.boxb(8.8, 1.4, 3.0, 0, 0.1, 0, c="wood_dark", bev=0.06)
    p.boxb(8.9, 1.2, 0.2, 0, 0.15, 0, c="wood_black")
    for i in range(5):
        x = -3.5 + i * 1.75
        p.boxb(1.45, 0.06, 2.2, x, -0.62, 0.4, c="wood_red", bev=0.04)
        p.boxb(1.25, 0.04, 1.95, x, -0.66, 0.52, c="wood_dark", bev=0.02)
    p.boxb(8.6, 0.06, 0.12, 0, -0.62, 2.75, c="gold", bev=0.01)
    g = m.part("Dessus")
    g.boxb(9.0, 0.5, 0.4, 0, -0.55, 3.0, c="gold", bev=0.06)  # tablette haute dorée
    g.boxb(8.9, 1.0, 0.12, 0, 0.3, 2.95, c="gold", bev=0.03)
    g.decal(1.2, 0.3, (2.5, -0.81, 3.2), c="yellow_dark", t=0.01, seed=1)  # dorure écaillée
    g.decal(0.8, 0.25, (-3.0, -0.81, 3.15), c="wood_dark", t=0.01, seed=2)
    return m


def sonnette():
    m = Model("sonnette_reception", (0.5, 0.3, 0.5), CAT, "Sonnette de réception")
    p = m.part("Sonnette")
    p.cyl(0.25, 0.06, c="wood_dark", segs=12, bev=0.02)
    p.lathe([(0, 0.06), (0.2, 0.06), (0.2, 0.08), (0.15, 0.18), (0.06, 0.24), (0, 0.25)], segs=12, c="gold")
    b = m.part("Bouton")
    b.cyl(0.015, 0.04, at=(0, 0, 0.25), c="chrome", segs=6, bev=0)
    b.cyl(0.04, 0.012, at=(0, 0, 0.288), c="chrome", segs=8, bev=0)
    return m


def tableau_cles():
    m = Model("tableau_cles", (4, 3, 0.2), CAT, "Tableau à clés")
    p = m.part("Tableau")
    p.boxb(4.0, 0.1, 3.0, 0, 0.05, 0, c="wood_dark", bev=0.04)
    p.boxb(3.6, 0.04, 2.6, 0, -0.02, 0.2, c="velvet", bev=0)
    k = m.part("Cles")
    rng = random.Random(3)
    for r in range(4):
        for cidx in range(6):
            x, z = -1.5 + cidx * 0.6, 2.5 - r * 0.62
            p.rod((x, -0.04, z), (x, -0.13, z + 0.02), 0.02, c="brass", sides=4)
            if rng.random() < 0.2:
                continue  # crochet vide
            k.torus(0.05, 0.012, at=(x, -0.1, z - 0.06), rot=(90, 0, 0), c="brass", segs=6, sides=3)
            k.boxb(0.05, 0.02, 0.2, x, -0.1, z - 0.3, c="brass", bev=0)
            k.boxb(0.14, 0.03, 0.18, x, -0.08, z - 0.5, c=rng.choice(["red", "wood", "teal", "brass"]), bev=0.02)
    return m


def canape():
    m = Model("canape_velours", (2.4, 2.6, 6), CAT, "Canapé 3 places velours", None, "Longueur selon Z ; assise tournée vers -X")
    p = m.part("Canape")
    nz = m.noise(0.03, 1)
    for y in (-2.7, 2.7):
        for x in (-0.95, 0.95):
            p.cyl(0.1, 0.35, at=(x, y, 0), r2=0.07, c="wood_black", segs=6, bev=0)
    p.boxb(2.4, 6.0, 0.7, 0, 0, 0.35, c="velvet", bev=0.12, deform=nz)
    p.boxb(0.65, 5.2, 1.9, 0.85, 0, 0.9, c="velvet", bev=0.2, deform=nz)  # dossier
    for y in (-2.75, 2.75):
        p.boxb(2.4, 0.5, 1.2, 0, y, 0.75, c="velvet", bev=0.18, deform=nz)  # accoudoirs
    for i, y in enumerate((-1.68, 0, 1.68)):
        p.boxb(1.65, 1.62, 0.45, -0.3, y, 1.05, c="velvet", bev=0.15, deform=m.noise(0.04, 10 + i))
        p.box(0.5, 1.55, 1.2, at=(0.35, y, 2.0), rot=(0, -10, 0), c="velvet", bev=0.18, deform=m.noise(0.04, 20 + i))
    p.decal(0.6, 0.5, (-0.3, 1.5, 1.51), c="fabric_grey", rot=(90, 0, 0), t=0.02, seed=5)  # rustine grise
    p.decal(0.8, 0.6, (-0.6, -1.6, 1.51), c="stain", rot=(90, 0, 0), t=0.02, seed=6)
    p.pipe([(-0.5, 0.1, 1.45), (-0.55, 0.15, 1.6), (-0.45, 0.2, 1.7), (-0.55, 0.25, 1.78)], 0.025, c="metal", sides=3)  # ressort
    return m


def table_basse():
    m = Model("table_basse", (2, 1.4, 3), CAT, "Table basse", None, "Longueur selon Z")
    p = m.part("Table")
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.boxb(0.14, 0.14, 1.25, sx * 0.82, sy * 1.32, 0, c="wood_dark", bev=0.03)
    p.boxb(2.0, 3.0, 0.15, 0, 0, 1.25, c="wood", bev=0.04)
    p.boxb(1.7, 2.7, 0.06, 0, 0, 0.35, c="wood_dark", bev=0.01)
    p.cyl(0.2, 0.01, at=(0.3, -0.6, 1.4), c="stain", segs=10, bev=0)
    p.boxb(0.7, 0.9, 0.04, -0.3, 0.6, 1.4, c="pink", rot=(0, 0, 12), bev=0)  # magazine
    p.boxb(0.65, 0.85, 0.04, -0.25, 0.65, 1.44, c="sky", rot=(0, 0, -5), bev=0)
    p.boxb(0.06, 0.4, 0.1, 0.85, 1.3, 0.0, c="cardboard", bev=0)  # cale
    return m


def ascenseur():
    m = Model("porte_ascenseur", (4, 6.5, 0.3), CAT, "Porte d'ascenseur", None, "Panneau EN PANNE séparé (vierge)")
    f = m.part("Encadrement")
    f.boxb(4.0, 0.3, 0.3, 0, 0, 5.4, c="inox", bev=0.04)
    for x in (-1.85, 1.85):
        f.boxb(0.3, 0.3, 5.4, x, 0, 0, c="inox", bev=0.04)
    f.boxb(4.0, 0.25, 0.8, 0, 0.02, 5.7, c="metal_dark", bev=0.03)
    f.boxb(0.3, 0.06, 0.6, 1.85, -0.15, 2.4, c="metal_dark", bev=0.02)  # boîte d'appel
    f.decal(0.6, 0.4, (-1.85, -0.16, 0.3), c="mud", seed=1)
    ind = m.part("Indicateur")
    ind.boxb(1.6, 0.06, 0.4, 0, -0.14, 5.9, c="screen_dark", bev=0)
    ind.prism([(-0.08, 0), (0.08, 0), (0, 0.14)], 0.03, at=(0.6, -0.18, 6.03), c="light_amber")
    b = m.part("BoutonAppel")
    b.cyl(0.08, 0.03, at=(1.85, -0.18, 2.7), rot=(90, 0, 0), c="light_amber", segs=8, bev=0)
    for name, x in (("PorteGauche", -0.85), ("PorteDroite", 0.85)):
        d = m.part(name)
        d.boxb(1.7, 0.08, 5.35, x, 0.05, 0.02, c="alu", bev=0.02)
        d.boxb(1.5, 0.02, 0.06, x, 0.0, 2.6, c="inox", bev=0)
    m.part("PorteGauche").decal(0.7, 0.9, (-0.9, -0.0, 1.4), c="pink", t=0.02, seed=3)  # tag abstrait
    m.part("PorteDroite").decal(0.5, 0.4, (1.0, -0.0, 0.8), c="rust", t=0.02, seed=4)
    pn = m.part("PanneauEnPanne")
    pn.box(3.2, 0.04, 0.9, at=(0, -0.12, 3.0), rot=(0, 12, 0), c="yellow", bev=0.01)
    pn.box(0.5, 0.05, 0.18, at=(-1.55, -0.13, 3.35), rot=(0, 40, 0), c="grey_light", bev=0)  # scotch
    pn.box(0.5, 0.05, 0.18, at=(1.55, -0.13, 2.65), rot=(0, 40, 0), c="grey_light", bev=0)
    return m


def valise():
    m = Model("valise", (1.5, 2, 0.8), CAT, "Valise")
    p = m.part("Valise")
    p.boxb(1.5, 0.75, 1.5, 0, 0, 0.12, c="fabric_blue", bev=0.12, deform=m.noise(0.02, 1))
    for z in (0.5, 1.15):
        p.boxb(1.53, 0.78, 0.08, 0, 0, z, c="black", bev=0.02)  # sangles
    p.boxb(1.4, 0.06, 0.08, 0, -0.38, 0.9, c="metal_dark", bev=0)  # fermeture éclair
    for x in (-0.55, 0.55):
        p.cyl(0.1, 0.08, at=(x - 0.04, 0.25, 0.1), rot=(0, 90, 0), c="plastic_black", segs=8, bev=0.01)
        p.boxb(0.06, 0.06, 0.6, x * 0.45, 0.33, 1.62, c="alu", bev=0)
    p.boxb(0.75, 0.12, 0.08, 0, 0.33, 1.95 - 0.08, c="plastic_black", bev=0.02)
    p.decal(0.35, 0.3, (0.4, -0.38, 1.2), c="yellow", t=0.02, seed=2)  # autocollants sans texte
    p.decal(0.3, 0.3, (-0.4, -0.38, 0.4), c="red", t=0.02, seed=3)
    p.decal(0.4, 0.25, (-0.2, -0.38, 1.4), c="mint", t=0.02, seed=4)
    p.box(0.5, 0.05, 0.25, at=(0.3, -0.38, 0.35), rot=(0, 20, 0), c="grey_light", bev=0)  # scotch sur un trou
    return m


def lustre():
    m = Model("lustre", (3, 2, 3), CAT, "Lustre", None, "Accroché au plafond par le haut")
    p = m.part("Lustre")
    p.cyl(0.25, 0.08, at=(0, 0, 1.92), c="gold", segs=10, bev=0.02)
    p.rod((0, 0, 1.92), (0, 0, 1.0), 0.04, c="gold", sides=5)
    p.lathe([(0, 0.25), (0.18, 0.35), (0.25, 0.65), (0.15, 0.95), (0, 1.05)], segs=8, c="gold")
    a = m.part("Ampoules")
    rng = random.Random(8)
    for i in range(6):
        ang = math.radians(i * 60 + 15)
        x, y = 1.2 * math.cos(ang), 1.2 * math.sin(ang)
        p.pipe([(0, 0, 0.5), (0.5 * math.cos(ang), 0.5 * math.sin(ang), 0.35), (x, y, 0.42), (x, y, 0.62)], 0.04, c="gold", sides=4)
        p.cyl(0.1, 0.1, at=(x, y, 0.62), c="gold", segs=6, bev=0)
        p.lathe([(0, 0), (0.04, 0.05), (0, 0.18)], segs=4, at=(x * 0.75, y * 0.75, 0.15), c="glass")  # pampille
        if i in (2,):
            continue  # ampoule manquante
        p.cyl(0.05, 0.3, at=(x, y, 0.72), c="white", segs=6, bev=0)
        col = "screen_dark" if i == 4 else "light_warm"  # une grillée
        a.lathe([(0, 0), (0.07, 0.04), (0.08, 0.12), (0.03, 0.24), (0, 0.27)], segs=6, at=(x, y, 1.02), c=col)
    p.decal(0.5, 0.15, (0.2, -0.2, 1.5), c="grey_light", rot=(0, 0, 0), t=0.01, seed=3)  # toile d'araignée
    return m


# ---------------------------------------------------------------------------
# Presse / pharmacie / opticien
# ---------------------------------------------------------------------------

def presentoir_magazines():
    m = Model("presentoir_magazines", (3, 3.5, 0.6), CAT, "Présentoir mural à magazines")
    p = m.part("Presentoir")
    p.boxb(3.0, 0.1, 3.5, 0, 0.25, 0, c="metal_dark", bev=0.02)
    for x in (-1.45, 1.45):
        p.boxb(0.08, 0.6, 3.4, x, 0.0, 0.0, c="metal_dark", bev=0.01)
    g = m.part("Magazines")
    rng = random.Random(6)
    cols = ["red", "yellow", "blue", "pink", "green", "orange", "purple", "teal", "white", "sky"]
    for r in range(4):
        z = 0.15 + r * 0.85
        p.box(2.9, 0.06, 0.25, at=(0, -0.22, z + 0.1), rot=(-15, 0, 0), c="metal", bev=0.01)
        p.boxb(2.9, 0.45, 0.05, 0, 0.0, z, c="metal", bev=0)
        for k in range(4):
            if rng.random() < 0.15:
                continue
            g.box(0.62, 0.04, 0.82, at=(-1.05 + k * 0.7, -0.08 + 0.02 * k, z + 0.42), rot=(-12, 0, rng.uniform(-3, 3)), c=rng.choice(cols), bev=0)
            g.box(0.4, 0.01, 0.3, at=(-1.05 + k * 0.7, -0.11 + 0.02 * k, z + 0.52), rot=(-12, 0, 0), c=rng.choice(cols), bev=0)  # « photo » de couverture
    return m


def croix_pharmacie():
    m = Model("croix_pharmacie", (2, 2, 0.3), CAT, "Croix de pharmacie lumineuse")
    s = m.part("Support")
    s.boxb(0.4, 0.06, 0.4, 0, 0.12, 0.8, c="metal_dark", bev=0.01)
    cross = [(-0.32, -1), (0.32, -1), (0.32, -0.32), (1, -0.32), (1, 0.32), (0.32, 0.32), (0.32, 1), (-0.32, 1), (-0.32, 0.32), (-1, 0.32),
             (-1, -0.32), (-0.32, -0.32)]
    s.prism(cross, 0.12, at=(0, 0.04, 1.0), c="gunmetal", bev=0.03)
    c = m.part("Croix")
    c.prism([(x * 0.94, z * 0.94) for x, z in cross], 0.1, at=(0, -0.08, 1.0), c="light_green")
    c.decal(0.25, 0.25, (0.6, -0.14, 1.05), c="screen_dark", t=0.01, seed=1)  # LED grillées
    return m


def tableau_acuite():
    m = Model("tableau_acuite", (2, 3, 0.1), CAT, "Tableau d'acuité visuelle", None, "Cadre seul, lettres ajoutées en jeu")
    p = m.part("Cadre")
    for z in (0, 2.88):
        p.boxb(2.0, 0.1, 0.12, 0, 0, z, c="white", bev=0.02)
    for x in (-0.94, 0.94):
        p.boxb(0.12, 0.1, 3.0, x, 0, 0, c="white", bev=0.02)
    t = m.part("Tableau")
    t.boxb(1.78, 0.04, 2.78, 0, 0.02, 0.11, c="paper", bev=0)
    t.decal(0.5, 0.4, (0.5, -0.01, 0.4), c="paper_dirty", t=0.01, seed=1)
    t.boxb(1.6, 0.01, 0.03, 0, -0.005, 0.7, c="red", bev=0)  # ligne de lecture
    return m


# ---------------------------------------------------------------------------
# Coiffeur
# ---------------------------------------------------------------------------

def fauteuil_barbier():
    m = Model("fauteuil_barbier", (1.8, 4, 1.8), CAT, "Fauteuil de barbier")
    p = m.part("Pied")
    p.cyl(0.75, 0.12, c="chrome", segs=14, bev=0.04)
    p.cyl(0.2, 1.0, at=(0, 0, 0.12), c="chrome", segs=10, bev=0.02)
    p.boxb(0.3, 0.2, 0.1, 0.5, -0.3, 0.12, c="black", bev=0.02)  # pédale
    p.box(1.2, 0.5, 0.08, at=(0, -0.95, 0.55), rot=(20, 0, 0), c="chrome", bev=0.02)  # repose-pieds
    p.rod((0, -0.3, 1.0), (0, -0.85, 0.6), 0.05, c="chrome", sides=5)
    s = m.part("Siege", pivot=(0, 0, 1.12))
    s.boxb(1.4, 1.3, 0.2, 0, 0.0, 1.12, c="chrome", bev=0.04)
    s.boxb(1.3, 1.25, 0.45, 0, -0.05, 1.3, c="leather", bev=0.15, deform=m.noise(0.02, 1))
    s.box(1.3, 0.45, 2.0, at=(0, 0.6, 2.6), rot=(-10, 0, 0), c="leather", bev=0.18, deform=m.noise(0.02, 2))
    s.box(0.7, 0.3, 0.4, at=(0, 0.83, 3.75), rot=(-10, 0, 0), c="leather", bev=0.12)  # appui-tête
    s.rod((0, 0.75, 3.4), (0, 0.8, 3.6), 0.04, c="chrome", sides=4)
    for x in (-0.8, 0.8):
        s.boxb(0.2, 1.2, 0.15, x, -0.05, 2.0, c="leather", bev=0.06)
        s.rod((x, -0.5, 1.4), (x, -0.5, 2.0), 0.04, c="chrome", sides=4)
        s.rod((x, 0.4, 1.4), (x, 0.4, 2.0), 0.04, c="chrome", sides=4)
    s.box(0.4, 0.3, 0.02, at=(0.2, -0.3, 1.755), rot=(0, 0, 25), c="grey_light", bev=0)  # chatterton
    s.decal(0.4, 0.3, (-0.3, 0.37, 2.3), c="mattress", rot=(-10, 0, 0), t=0.02, seed=3)  # mousse qui sort
    return m


def miroir_mural():
    m = Model("miroir_mural", (2.4, 3, 0.1), CAT, "Miroir mural avec cadre")
    p = m.part("Cadre")
    for z in (0, 2.8):
        p.boxb(2.4, 0.1, 0.2, 0, 0, z, c="gold", bev=0.03)
    for x in (-1.1, 1.1):
        p.boxb(0.2, 0.1, 3.0, x, 0, 0, c="gold", bev=0.03)
    p.decal(0.3, 0.12, (-1.1, -0.05, 1.5), c="wood_dark", t=0.01, seed=1)
    mi = m.part("Miroir")
    mi.boxb(2.02, 0.03, 2.62, 0, 0.02, 0.19, c="mirror", bev=0)
    for a, b in (((0.3, 1.8), (0.75, 2.15)), ((0.75, 2.15), (0.55, 2.3)), ((0.75, 2.15), (0.95, 2.6)), ((0.3, 1.8), (0.1, 1.55))):
        mi.rod((a[0], -0.005, a[1]), (b[0], -0.005, b[1]), 0.012, c="grey_light", sides=3)  # fêlure
    mi.boxb(0.3, 0.02, 0.4, -0.7, -0.005, 0.5, c="yellow", rot=(0, 10, 0), bev=0)  # post-it
    return m


def poteau_barbier():
    m = Model("enseigne_barbier", (0.8, 3, 0.8), CAT, "Enseigne poteau de barbier", None, "Rayures en pièce séparée (rotation)")
    p = m.part("Support")
    p.boxb(0.5, 0.08, 2.4, 0, 0.36, 0.3, c="chrome", bev=0.02)
    for z in (0.0, 2.6):
        p.lathe([(0, 0), (0.36, 0), (0.38, 0.1), (0.3, 0.3), (0, 0.4)] if z > 1 else [(0, 0), (0.3, 0.1), (0.38, 0.3), (0.36, 0.4), (0, 0.4)],
                segs=12, at=(0, 0, z), c="chrome")
    p.sphere(0.18, at=(0, 0, 2.95), c="chrome", segs=8, rings=5, scale=(1, 1, 0.4))
    g = m.part("Cylindre")
    g.cyl(0.3, 2.2, at=(0, 0, 0.4), c="white", segs=12, bev=0)
    r = m.part("Rayures", pivot=(0, 0, 1.5))
    for k, col in enumerate(("red", "blue", "red", "blue")):
        pts = []
        for i in range(31):
            t = i / 30
            a = 2 * math.pi * (t * 2.2) + k * math.pi / 2
            pts.append((0.305 * math.cos(a), 0.305 * math.sin(a), 0.45 + t * 2.1))
        r.pipe(pts, 0.05, c=col, sides=4)
    return m


# ---------------------------------------------------------------------------
# Laverie
# ---------------------------------------------------------------------------

def lave_linge():
    m = Model("lave_linge", (2.2, 2.6, 2.2), CAT, "Lave-linge à hublot")
    p = m.part("Machine")
    p.boxb(2.2, 2.1, 2.3, 0, 0.05, 0.1, c="white", bev=0.08, deform=m.noise(0.015, 1))
    p.boxb(2.1, 2.0, 0.12, 0, 0.05, 0, c="grey_dark")
    p.boxb(2.2, 2.1, 0.3, 0, 0.05, 2.3, c="grey_light", bev=0.05)
    p.boxb(0.6, 0.06, 0.2, -0.65, -1.02, 2.35, c="grey", bev=0.02)  # bac à lessive
    p.cyl(0.13, 0.08, at=(0.75, -1.0, 2.45), rot=(90, 0, 0), c="grey_dark", segs=10, bev=0.02)
    p.boxb(0.25, 0.04, 0.12, 0.3, -1.01, 2.4, c="screen_dark", bev=0)
    p.boxb(0.25, 0.04, 0.12, 0.0, -1.01, 2.4, c="screen_dark", bev=0)  # monnayeur
    p.cyl(0.62, 0.04, at=(0, -0.99, 1.15), rot=(90, 0, 0), c="grey_light", segs=16, bev=0)
    p.decal(1.0, 0.4, (0.3, -1.0, 0.3), c="rust", seed=2)
    p.decal(0.5, 0.3, (-0.7, -1.0, 0.25), c="rust_dark", seed=3)
    p.box(0.7, 0.04, 0.4, at=(-0.55, -1.01, 1.95), rot=(0, 8, 0), c="paper", bev=0)  # affichette « hors service » (vierge)
    v = m.part("Voyant")
    v.cyl(0.04, 0.03, at=(-0.2, -1.02, 2.46), rot=(90, 0, 0), c="light_red", segs=6, bev=0)
    h = m.part("Hublot", pivot=(-0.6, -1.05, 1.15))
    h.torus(0.5, 0.09, at=(0, -1.06, 1.15), rot=(90, 0, 0), c="chrome", segs=16, sides=5)
    h.boxb(0.1, 0.08, 0.3, 0.55, -1.08, 1.0, c="grey_dark", bev=0.02)
    vh = m.part("VitreHublot", pivot=(-0.6, -1.05, 1.15))
    vh.lathe([(0, 0.04), (0.43, 0.0), (0, -0.05)], segs=16, at=(0, -1.06, 1.15), rot=(90, 0, 0), c="glass_dark", cap0=False, cap1=False)
    return m


def banc_attente():
    m = Model("banc_attente", (1.2, 1.6, 5), CAT, "Banc d'attente", None, "Longueur selon Z")
    p = m.part("Banc")
    for y in (-2.1, 2.1):
        p.boxb(1.0, 0.12, 0.12, 0, y, 0.0, c="metal_dark", bev=0.02)
        for x in (-0.4, 0.4):
            p.boxb(0.1, 0.1, 1.4, x, y, 0.0, c="metal_dark", bev=0.02)
        p.boxb(1.1, 0.14, 0.1, 0, y, 1.3, c="metal_dark", bev=0.02)
    for i, x in enumerate((-0.42, -0.14, 0.14, 0.42)):
        p.boxb(0.24, 5.0, 0.12, x, 0, 1.4 + (0.02 if i == 2 else 0), c=("wood" if i != 2 else "wood_old"), bev=0.03,
               rot=(0, 0, 0) if i != 2 else (0, 0, 0.6))
    p.box(0.2, 0.6, 0.08, at=(0.14, 1.2, 1.6), rot=(0, 0, 0), c="grey_light", bev=0)  # chatterton
    p.box(0.6, 0.45, 0.1, at=(-0.2, -1.4, 1.6), rot=(0, 0, 18), c="paper", bev=0.01)  # journal oublié
    return m


# ---------------------------------------------------------------------------
# Salle de sport
# ---------------------------------------------------------------------------

def banc_muscu():
    m = Model("banc_muscu", (4.5, 3.6, 4), CAT, "Banc de musculation", None, "Barre et disques séparés")
    p = m.part("Banc")
    p.boxb(0.9, 3.2, 0.3, 0, -0.3, 1.25, c="leather", bev=0.1)
    p.boxb(0.25, 2.8, 0.12, 0, -0.3, 0.6, c="metal_dark", bev=0.02)
    for y in (-1.6, 1.0):
        p.boxb(0.2, 0.2, 1.2, 0, y, 0.05, c="metal_dark", bev=0.02)
        p.boxb(1.2, 0.25, 0.1, 0, y, 0.0, c="metal_dark", bev=0.02)
    for x in (-1.1, 1.1):
        p.boxb(0.2, 0.2, 3.5, x, 1.6, 0.0, c="metal_dark", bev=0.02)
        p.boxb(0.25, 0.3, 0.2, x, 1.45, 2.5, c="metal", bev=0.02)  # supports en J
        p.boxb(0.25, 1.0, 0.1, x, 1.6, 0.0, c="metal_dark", bev=0.02)
    p.boxb(2.4, 0.2, 0.15, 0, 1.6, 3.4, c="metal_dark", bev=0.02)
    p.box(0.3, 0.5, 0.02, at=(0.1, -0.8, 1.56), rot=(0, 0, 20), c="grey_light", bev=0)  # chatterton
    b = m.part("Barre", pivot=(0, 1.45, 2.85))
    b.cyl(0.05, 4.5, at=(-2.25, 1.45, 2.85), rot=(0, 90, 0), c="chrome", segs=6, bev=0)
    d = m.part("Disques")
    for s in (-1, 1):
        for k, (r, c) in enumerate(((0.75, "black"), (0.55, "red"), (0.45, "blue"))):
            x = s * (1.45 + k * 0.17)
            d.cyl(r, 0.14, at=(x - 0.07, 1.45, 2.85), rot=(0, 90, 0), c=c, segs=12, bev=0.03)
        d.cyl(0.1, 0.1, at=(s * 1.95 - 0.05, 1.45, 2.85), rot=(0, 90, 0), c="metal_dark", segs=6, bev=0)
    return m


def tapis_course():
    m = Model("tapis_course", (2, 4.6, 5), CAT, "Tapis de course", None, "Console vers -Z")
    p = m.part("Chassis")
    for x in (-0.85, 0.85):
        p.boxb(0.3, 4.6, 0.45, x, 0.2, 0.0, c="grey_dark", bev=0.06)
    p.boxb(2.0, 0.6, 0.55, 0, -2.2, 0.0, c="grey_dark", bev=0.08)  # capot moteur
    for x in (-0.85, 0.85):
        p.rod((x, -2.0, 0.5), (x * 0.9, -2.3, 3.6), 0.09, c="grey_light", sides=6)
        p.pipe([(x * 0.9, -2.1, 3.2), (x * 0.95, -1.4, 3.3), (x * 0.95, -0.6, 3.2)], 0.06, c="black", sides=5)  # mains courantes
    p.box(1.9, 0.6, 0.9, at=(0, -2.25, 3.9), rot=(25, 0, 0), c="grey_dark", bev=0.1)  # console
    p.box(0.9, 0.06, 0.3, at=(0.4, -2.0, 3.6), rot=(25, 0, 10), c="grey_light", bev=0)  # chatterton
    p.cyl(0.12, 0.25, at=(-0.7, -2.0, 3.85), rot=(25, 0, 0), c="sky", segs=6, bev=0)  # gourde oubliée
    e = m.part("Ecran")
    e.box(1.0, 0.04, 0.45, at=(0, -2.5, 4.1), rot=(-65, 0, 0), c="screen", bev=0)
    t = m.part("Tapis")
    t.boxb(1.4, 4.3, 0.08, 0, 0.25, 0.4, c="rubber", bev=0.02)
    t.cyl(0.2, 1.4, at=(-0.7, 2.35, 0.25), rot=(0, 90, 0), c="metal_dark", segs=8, bev=0)
    return m


# ---------------------------------------------------------------------------
# Cordonnerie / réparateur
# ---------------------------------------------------------------------------

def etabli():
    m = Model("etabli_bois", (1.6, 3, 4), CAT, "Établi en bois", None, "Longueur selon Z ; côté travail vers -X")
    p = m.part("Etabli")
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.boxb(0.2, 0.2, 2.6, sx * 0.62, sy * 1.75, 0, c="wood", bev=0.03)
    p.boxb(1.6, 4.0, 0.2, 0, 0, 2.6, c="wood_light", bev=0.04)
    p.boxb(1.3, 3.6, 0.08, 0, 0, 0.6, c="wood", bev=0.02)
    p.boxb(0.1, 4.0, 0.3, 0.75, 0, 2.7, c="wood", bev=0.02)  # rebord arrière
    p.decal(0.6, 0.4, (0.0, 0.8, 2.805), c="stain", rot=(90, 0, 0), t=0.01, seed=1)
    p.decal(0.5, 0.5, (-0.2, -1.0, 2.805), c="soot", rot=(90, 0, 0), t=0.01, seed=2)
    o = m.part("Outils")
    o.boxb(0.4, 0.5, 0.25, -0.6, -1.4, 2.8, c="blue", bev=0.04)  # étau
    o.boxb(0.2, 0.15, 0.15, -0.85, -1.4, 2.85, c="metal_dark", bev=0.02)
    o.boxb(0.5, 0.25, 0.15, 0.0, 0.0, 2.8, c="metal_dark", bev=0.03)  # forme à chaussure
    o.sphere(0.25, at=(0.1, 0.0, 3.0), c="leather", scale=(1.0, 2.0, 0.6), segs=8, rings=5)  # chaussure
    o.boxb(0.35, 0.7, 0.04, 0.2, 1.3, 2.8, c="plastic_black", bev=0.02, rot=(0, 0, 10))  # téléphone éventré
    o.boxb(0.3, 0.6, 0.02, 0.4, 1.0, 2.84, c="screen", bev=0, rot=(0, 0, -20))
    o.rod((-0.2, -0.5, 2.83), (-0.25, 0.2, 2.83), 0.03, c="wood_light", sides=4)  # marteau
    o.boxb(0.25, 0.1, 0.1, -0.25, 0.25, 2.8, c="metal_dark", bev=0.02)
    o.cyl(0.1, 0.2, at=(0.5, -0.6, 2.8), c="red", segs=6, bev=0)  # pot de colle
    return m


def panneau_perfore():
    m = Model("panneau_perfore", (8, 3, 0.3), CAT, "Panneau perforé avec outils")
    p = m.part("Panneau")
    p.boxb(8.0, 0.08, 3.0, 0, 0.11, 0, c="cork", bev=0.02)
    for x in range(-15, 16, 2):
        for z in range(6):
            p.boxb(0.06, 0.01, 0.06, x * 0.25, 0.065, 0.25 + z * 0.5, c="wood_black", bev=0)
    o = m.part("Outils")
    tools = [
        ("hammer", -3.4), ("saw", -2.2), ("wrench", -1.0), ("screw", -0.4), ("screw", 0.0), ("pliers", 0.7), ("phones", 2.2), ("cutter", 3.5),
    ]
    for kind, x in tools:
        o.rod((x, 0.05, 2.6), (x, -0.06, 2.62), 0.025, c="metal", sides=4)  # crochet
        if kind == "hammer":
            o.boxb(0.1, 0.06, 1.0, x, -0.03, 1.4, c="wood_light", bev=0.02)
            o.boxb(0.5, 0.12, 0.18, x, -0.04, 2.35, c="metal_dark", bev=0.03)
        elif kind == "saw":
            o.prism([(-0.35, 0), (0.35, 0), (0.25, 1.5), (-0.25, 1.5)], 0.02, at=(x, -0.03, 0.9), c="metal_light")
            o.boxb(0.45, 0.08, 0.3, x, -0.04, 2.35, c="red", bev=0.04)
        elif kind == "wrench":
            o.boxb(0.12, 0.04, 1.3, x, -0.03, 1.2, c="chrome", bev=0.01)
            o.cyl(0.14, 0.05, at=(x, -0.03, 2.5), rot=(90, 0, 0), c="chrome", segs=8, bev=0)
        elif kind == "screw":
            o.cyl(0.07, 0.6, at=(x, -0.03, 1.85), c=("yellow" if x < -0.2 else "red"), segs=6, bev=0.02)
            o.cyl(0.02, 0.5, at=(x, -0.03, 1.35), c="chrome", segs=4, bev=0)
        elif kind == "pliers":
            o.rod((x - 0.12, -0.03, 1.5), (x, -0.03, 2.3), 0.04, c="blue", sides=4)
            o.rod((x + 0.12, -0.03, 1.5), (x, -0.03, 2.3), 0.04, c="blue", sides=4)
            o.rod((x, -0.03, 2.3), (x, -0.03, 2.55), 0.04, c="metal_dark", sides=4)
        elif kind == "phones":
            for k in range(3):
                o.boxb(0.4, 0.05, 0.8, x - 0.55 + k * 0.55, -0.03, 1.6 - k * 0.1, c="plastic_black", bev=0.03)
                o.boxb(0.34, 0.02, 0.7, x - 0.55 + k * 0.55, -0.06, 1.65 - k * 0.1, c=("screen_dark" if k != 1 else "screen"), bev=0)
            o.prism([(0, 0), (0.15, 0.2), (0.05, 0.25), (0.2, 0.45)], 0.01, at=(x - 0.6, -0.075, 1.9), c="grey_light")  # écran fissuré
        else:
            o.boxb(0.1, 0.05, 0.6, x, -0.03, 1.9, c="yellow", bev=0.02)
    o.box(1.2, 0.04, 0.6, at=(1.0, -0.02, 0.4), rot=(0, 8, 0), c="pink", bev=0)  # vieille affiche
    return m


# ---------------------------------------------------------------------------
# Friperie / fleuriste / prêteur sur gages
# ---------------------------------------------------------------------------

def portant():
    m = Model("portant_vetements", (1, 4.5, 5), CAT, "Portant à vêtements", None, "Rail selon Z")
    p = m.part("Portant")
    for y in (-2.35, 2.35):
        p.cyl(0.06, 4.3, at=(0, y, 0.15), c="chrome", segs=6, bev=0)
        p.boxb(1.0, 0.12, 0.1, 0, y, 0.12, c="chrome", bev=0.02)
        for x in (-0.42, 0.42):
            p.cyl(0.07, 0.1, at=(x, y, 0.0), c="plastic_black", segs=6, bev=0)
    p.rod((0, -2.4, 4.4), (0, 2.4, 4.4), 0.05, c="chrome", sides=6)
    v = m.part("Vetements")
    rng = random.Random(9)
    cols = ["fabric_red", "fabric_blue", "fabric_green", "fabric_yellow", "fabric_brown", "fabric_grey", "pink", "teal", "purple", "cream"]
    y = -2.0
    while y < 2.1:
        c = rng.choice(cols)
        long = rng.random() < 0.35
        h = 2.6 if long else 1.7
        v.pipe([(-0.12, y, 4.08), (0, y, 4.45), (0.12, y, 4.08)], 0.02, c="metal", sides=3)
        v.rod((-0.4, y, 4.05), (0.4, y, 4.05), 0.025, c="wood_light", sides=3)
        v.box(0.68, 0.08, h, at=(0, y, 4.05 - h / 2), c=c, bev=0.03, deform=m.noise(0.03, int(y * 10) + 50))
        if not long:
            for s in (-1, 1):
                v.box(0.18, 0.08, 0.8, at=(s * 0.38, y, 3.5), rot=(0, s * 12, 0), c=c, bev=0.02)
        y += rng.uniform(0.3, 0.45)
    v.box(0.9, 0.1, 0.5, at=(0.1, 1.4, 0.3), rot=(0, 0, 30), c="fabric_blue", bev=0.04, deform=m.noise(0.05, 99))  # pull tombé
    return m


def seau_fleurs():
    m = Model("seau_bouquet", (1.2, 2.2, 1.2), CAT, "Seau en métal avec bouquet")
    p = m.part("Seau")
    p.tube_open(0.48, 1.0, 0.04, at=(0, 0, 0), r2=0.6, c="galva", segs=12, deform=m.noise(0.01, 1))
    p.torus(0.6, 0.03, at=(0, 0, 1.0), c="galva", segs=12, sides=4)
    p.cyl(0.55, 0.02, at=(0, 0, 0.8), c="glass_dark", segs=12, bev=0)  # eau
    p.decal(0.3, 0.25, (0.2, -0.53, 0.3), c="rust", rot=(-6, 0, 0), seed=2)
    f = m.part("Bouquet")
    rng = random.Random(10)
    cols = ["flower_red", "flower_pink", "flower_yellow", "flower_white", "flower_purple"]
    for i in range(11):
        a = i * 2.4
        r = 0.08 + 0.05 * (i % 4)
        top = (r * 2.6 * math.cos(a), r * 2.6 * math.sin(a), 1.75 + rng.uniform(0, 0.25))
        f.rod((r * math.cos(a), r * math.sin(a), 0.3), top, 0.025, c="leaf_dark", sides=3)
        if i == 7:
            f.sphere(0.13, at=(top[0], top[1], top[2] - 0.1), c="wood_old", segs=6, rings=4, scale=(1, 1, 0.6))  # fleur fanée penchée
            continue
        f.sphere(0.17, at=top, c=cols[i % len(cols)], segs=6, rings=4, scale=(1, 1, 0.6))
        f.sphere(0.06, at=(top[0], top[1], top[2] + 0.07), c="flower_yellow" if i % 5 != 2 else "wood_dark", segs=5, rings=3)
    for i in range(5):
        a = i * 1.3
        f.prism([(-0.08, 0), (0.08, 0), (0, 0.5)], 0.02, at=(0.25 * math.cos(a), 0.25 * math.sin(a), 1.05), rot=(25, 0, math.degrees(a) + 90),
                c="leaf", plane="XZ")
    return m


def comptoir_barreaux():
    m = Model("comptoir_barreaux", (8, 6.4, 1.6), CAT, "Comptoir à barreaux", None, "Guichet coulissant séparé")
    p = m.part("Comptoir")
    p.boxb(8.0, 1.6, 0.2, 0, 0, 3.2, c="wood_dark", bev=0.05)
    p.boxb(7.8, 1.4, 3.2, 0, 0.05, 0, c="wood", bev=0.05)
    for i in range(4):
        p.boxb(1.7, 0.06, 2.4, -2.85 + i * 1.9, -0.67, 0.4, c="wood_dark", bev=0.03)
    p.decal(1.4, 0.6, (1.5, -0.71, 0.6), c="mud", seed=1)
    p.decal(0.8, 0.4, (-2.5, -0.71, 2.2), c="soot", seed=2)  # trace de pied de biche
    b = m.part("Barreaux")
    b.boxb(8.0, 0.2, 0.2, 0, 0.0, 6.2, c="gunmetal", bev=0.03)
    b.boxb(8.0, 0.2, 0.15, 0, 0.0, 3.4, c="gunmetal", bev=0.03)
    for i in range(27):
        x = -3.9 + i * 0.3
        if -0.75 < x < 0.75:  # ouverture du guichet
            b.cyl(0.04, 1.8, at=(x, 0, 4.4), c="gunmetal", segs=5, bev=0)
            continue
        b.cyl(0.04, 2.7, at=(x, 0, 3.5), c="gunmetal", segs=5, bev=0)
    b.boxb(1.6, 0.2, 0.12, 0, 0.0, 4.3, c="gunmetal", bev=0.02)
    b.boxb(0.25, 0.25, 0.3, 3.0, -0.12, 4.0, c="brass", bev=0.04)  # cadenas
    g = m.part("Guichet", pivot=(0, -0.05, 3.55))
    g.boxb(1.5, 0.06, 0.75, 0, -0.12, 3.55, c="glass", bev=0)
    g.boxb(1.55, 0.1, 0.06, 0, -0.12, 4.28, c="gunmetal", bev=0)
    g.boxb(0.3, 0.12, 0.06, 0, -0.18, 3.6, c="metal_dark", bev=0.01)
    return m


MODELS = [
    ("73_comptoir_reception", reception), ("74_sonnette_reception", sonnette), ("75_tableau_cles", tableau_cles),
    ("76_canape_velours", canape), ("77_table_basse", table_basse), ("78_porte_ascenseur", ascenseur), ("79_valise", valise),
    ("80_lustre", lustre), ("81_presentoir_magazines", presentoir_magazines), ("82_croix_pharmacie", croix_pharmacie),
    ("83_tableau_acuite", tableau_acuite), ("84_fauteuil_barbier", fauteuil_barbier), ("85_miroir_mural", miroir_mural),
    ("86_enseigne_barbier", poteau_barbier), ("87_lave_linge", lave_linge), ("88_banc_attente", banc_attente),
    ("89_banc_muscu", banc_muscu), ("90_tapis_course", tapis_course), ("91_etabli_bois", etabli),
    ("92_panneau_perfore", panneau_perfore), ("93_portant_vetements", portant), ("94_seau_bouquet", seau_fleurs),
    ("95_comptoir_barreaux", comptoir_barreaux),
]
