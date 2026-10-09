"""185–196 : parcelle du joueur, bateaux et allée des casinos (3 niveaux)."""
import math
import random

from mathutils import Vector

from lib import Model
from m_marche import crate
from m_deauville import window, awning

CAT = "12_parcelle"


def M(name, dims, title, note="", grime=True):
    m = Model(name, dims, CAT, title, None, note)
    m.grime = grime
    return m


def gear(p, x, y, z, r, c="metal", rot=(0, 0, 0), teeth=8, t=0.12):
    p.cyl(r, t, at=(x, y, z), rot=rot, c=c, segs=teeth * 2, bev=0.02)
    rx, ry, rz = (math.radians(a) for a in rot)
    for k in range(teeth):
        a = 2 * math.pi * k / teeth
        p.box(r * 0.35, t * 0.95, r * 0.3, at=(x, y, z), rot=rot, c=c, bev=0,
              deform=lambda co, a=a: Vector((co.x + (r + 0.08) * math.cos(a), co.y + (r + 0.08) * math.sin(a), co.z + t / 2)))
    p.cyl(r * 0.3, t * 1.4, at=(x, y, z), rot=rot, c="metal_dark", segs=6, bev=0)


def hull_taper(bow_start, bow_len, k=0.85):
    """Rétrécit la coque vers la proue (-Y)."""
    return lambda co: Vector((co.x * (1 - k * max(0, -co.y - bow_start) / bow_len), co.y, co.z))


# ---------------------------------------------------------------------------

def sac_a_dos():
    m = M("sac_a_dos", (2, 2.5, 1), "Sac à dos rapiécé", "Dos (bretelles) côté +Z")
    p = m.part("Sac")
    nz = m.noise(0.03, 1)
    p.boxb(1.6, 0.85, 1.9, 0, 0, 0, c="olive", bev=0.25, deform=nz)
    p.box(1.5, 0.9, 0.35, at=(0, -0.02, 1.9), rot=(-8, 0, 0), c="khaki", bev=0.12)  # rabat
    p.boxb(1.1, 0.3, 0.8, 0, -0.5, 0.3, c="fabric_brown", bev=0.12)  # poche avant
    for x in (-0.45, 0.45):
        p.boxb(0.12, 0.06, 1.2, x, -0.45, 1.0, c="leather", bev=0.02)
        p.boxb(0.16, 0.08, 0.12, x, -0.5, 1.15, c="brass", bev=0.02)
    p.decal(0.45, 0.4, (0.4, -0.44, 1.5), c="fabric_blue", t=0.03, seed=2)  # rustines
    p.decal(0.35, 0.3, (-0.5, -0.44, 0.75), c="fabric_red", t=0.03, seed=3)
    p.decal(0.3, 0.3, (0.81, 0.0, 0.9), c="beige", rot=(0, 0, 90), t=0.03, seed=4)
    for x in (-0.45, 0.45):  # bretelles
        p.pipe([(x, 0.42, 1.8), (x * 1.1, 0.55, 1.2), (x, 0.48, 0.3)], 0.08, c="leather", sides=4)
    p.cyl(0.11, 0.3, at=(-0.45 * 1.1 - 0.0, 0.55, 1.05), c="grey_light", segs=6, bev=0)  # scotch sur la bretelle cassée
    p.cyl(0.25, 1.9, at=(-0.95, 0.1, 0.25), rot=(0, 90, 0), c="fabric_green", segs=8, bev=0.05)  # tapis roulé dessous
    gear(p, 0.35, 0.05, 2.0, 0.28, c="brass", rot=(90, 0, 15))  # engrenage qui dépasse
    p.rod((-0.4, 0.1, 1.8), (-0.55, 0.15, 2.45), 0.05, c="rust", sides=4)  # bout de tuyau
    return m


def caisse_pieces():
    m = M("caisse_pieces", (3, 3, 3), "Caisse de pièces", "Atelier de la parcelle")
    p = m.part("Caisse")
    crate(p, 2.9, 2.9, 2.2, c="wood_old", c2="wood")
    p.box(0.1, 1.2, 0.5, at=(1.42, 0.6, 1.9), rot=(25, 0, 0), c="wood_old", bev=0.02)  # planche décollée
    p.decal(0.8, 0.5, (0.4, -1.46, 0.6), c="mud", seed=1)
    p.boxb(2.6, 2.6, 1.6, 0, 0, 0.2, c="wood_dark", bev=0)  # intérieur
    gear(p, -0.5, 0.2, 2.1, 0.5, c="metal", rot=(70, 0, 20))
    gear(p, 0.5, -0.3, 2.0, 0.35, c="brass", rot=(80, 0, -40))
    p.pipe([(0.2, 0.6, 1.8), (0.3, 0.7, 2.6), (0.7, 0.8, 2.9)], 0.1, c="rust", sides=6)
    p.pipe([(0.9 + 0.12 * math.cos(a), 0.6 + 0.12 * math.sin(a), 1.8 + a * 0.06) for a in [i * 0.6 for i in range(14)]], 0.03, c="chrome", sides=3)
    p.box(0.15, 1.0, 0.06, at=(-0.3, -0.6, 2.35), rot=(0, 0, 30), c="chrome", bev=0.01)  # clé
    p.box(0.5, 0.4, 0.3, at=(-0.9, -0.7, 1.95), rot=(10, 0, 20), c="red", bev=0.05)
    return m


def barque():
    m = M("barque_moteur", (6, 4, 14), "Barque à moteur", "Proue vers -Z, moteur à l'arrière")
    c, mo = m.part("Coque"), m.part("Moteur")
    tp = hull_taper(1.5, 5.5, 0.9)
    def lift(co):
        co = tp(co)
        return Vector((co.x, co.y, co.z + 0.08 * max(0, -co.y - 3) ** 1.3 * (co.z > -0.5)))
    c.box(5.4, 12.6, 1.8, at=(0, 0.2, 0.9), taper=(1.12, 1.0), c="wood", bev=0.35, deform=lift)
    c.box(4.8, 12.0, 0.2, at=(0, 0.3, 1.75), c="wood_dark", bev=0.05, deform=lift)
    for z in (0.5, 1.1):
        c.box(5.6, 12.6, 0.08, at=(0, 0.2, z), c=("red" if z < 1 else "wood_light"), bev=0, deform=lift)
    c.decal(1.5, 0.6, (2.7, 2.0, 1.0), c="soot", rot=(0, 0, 90), seed=1)
    for y, w in ((-1.5, 2.4), (2.0, 4.8)):
        c.boxb(w, 0.8, 0.15, 0, y, 1.6, c="wood_light", bev=0.03)  # bancs
    for x, y, h in ((-1.3, 4.6, 0.8), (-1.3, 3.7, 0.7), (-1.0, 4.2, 0.6)):
        c.box(1.0, 0.8, h, at=(x, y, 1.85 + h / 2 + (0.75 if y == 4.2 else 0)), rot=(0, 0, 8), c="crate", bev=0.05)
    c.boxb(5.2, 0.3, 1.2, 0, 6.4, 0.8, c="wood_dark", bev=0.05)  # tableau arrière
    mo.box(0.8, 1.0, 0.9, at=(1.2, 6.7, 2.6), c="grey", bev=0.2)
    mo.box(0.85, 1.05, 0.15, at=(1.2, 6.7, 2.2), c="red_dark", bev=0.03)
    mo.cyl(0.12, 2.2, at=(1.2, 6.8, 0.0), c="metal_dark", segs=6, bev=0)
    mo.box(0.25, 0.7, 0.25, at=(1.2, 6.9, 0.15), c="metal_dark", bev=0.05)
    for a in (0, 120, 240):
        mo.box(0.08, 0.06, 0.35, at=(1.2, 7.28, 0.15), rot=(0, a, 0), c="brass", bev=0, deform=lambda co: Vector((co.x, co.y, co.z + 0.15)))
    mo.rod((1.2, 6.2, 2.7), (1.2, 5.3, 2.4), 0.05, c="black", sides=4)  # barre
    mo.decal(0.4, 0.3, (1.2, 6.18, 2.7), c="rust", seed=2)
    return m


def cargo():
    m = M("bateau_cargo", (12, 10, 30), "Petit cargo", "Proue vers -Z")
    h, ca, cg = m.part("Coque"), m.part("Cabine"), m.part("Cargaison")
    tp = hull_taper(6, 8.5, 0.85)
    h.box(11.5, 29, 3.4, at=(0, 0.3, 1.7), c="navy_paint", bev=0.4, deform=tp)
    h.box(11.6, 29.1, 1.0, at=(0, 0.3, 0.5), c="red_dark", bev=0.2, deform=tp)
    h.box(11.2, 28.6, 0.2, at=(0, 0.3, 3.45), c="grey_dark", bev=0.05, deform=tp)
    for k, (y, z) in enumerate(((-3, 2.5), (2, 1.8), (8, 2.6), (12, 1.5))):
        for s in (-1, 1):
            h.decal(2.2, 0.9, (s * 5.76, y, z), c=("rust" if k % 2 else "rust_dark"), rot=(0, 0, 90), seed=k * 2 + (s > 0))
    h.boxb(11, 0.4, 0.8, 0, -6, 3.5, c="yellow_dark", bev=0.05)
    for s in (-1, 1):
        h.rod((s * 5.5, -6, 4.4), (s * 5.5, 12, 4.4), 0.06, c="white", sides=4)
    ca.boxb(9, 6, 3.5, 0, 10.5, 3.5, c="white", bev=0.15)
    ca.boxb(7, 4.5, 2.4, 0, 10.8, 7.0, c="white", bev=0.15)
    ca.boxb(7.6, 5, 0.3, 0, 10.8, 9.4, c="grey_dark", bev=0.05)
    for x in (-2.4, -0.8, 0.8, 2.4):
        window(ca, ca, x, 8.2, 1.2, 1.0, "-y", 8.55, frame="white")
    ca.cyl(0.8, 2.6, at=(2.0, 12.0, 7.4), c="red", segs=10, bev=0.08)  # cheminée
    ca.cyl(0.82, 0.4, at=(2.0, 12.0, 9.3), c="black", segs=10, bev=0)
    ca.decal(1.0, 0.8, (0, 7.48, 5.0), c="rust", seed=9)
    cols = ["red", "blue", "green_dark", "orange", "teal", "yellow_dark"]
    rng = random.Random(4)
    i = 0
    for y in (-3.5, 0.5, 4.5):
        for x in (-2.7, 2.7):
            col = cols[i % len(cols)]; i += 1
            cg.boxb(5.0, 3.6, 2.6, x, y, 3.55, c=col, bev=0.06)
            for k in range(6):
                cg.boxb(0.08, 3.62, 2.4, x - 2.2 + k * 0.88, y, 3.65, c=col, bev=0)
            if rng.random() < 0.5:
                cg.boxb(4.6, 3.2, 2.2, x, y, 6.15, c=cols[(i + 2) % len(cols)], bev=0.06)
    for x, y in ((-3, -7.8), (-1.6, -8.2), (2.5, -7.8)):
        cg.box(1.2, 1.2, 1.0, at=(x, y, 4.05), rot=(0, 0, rng.uniform(-10, 10)), c="crate", bev=0.05)
    return m


# ---------------------------------------------------------------------------
# Casinos de l'allée (façade ouverte côté -Z)
# ---------------------------------------------------------------------------

def casino_baraque():
    m = M("casino_baraque", (30, 14, 30), "Casino niveau 1 : baraque", "Façade ouverte vers -Z ; néon à moitié éteint")
    mu, to, en = m.part("Murs"), m.part("Toit"), m.part("Enseigne")
    mu.boxb(30, 30, 0.4, 0, 0, 0, c="wood_old", bev=0.05)
    for i in range(30):
        mu.boxb(0.05, 30, 0.02, -14.5 + i, 0, 0.4, c="wood_dark", bev=0)
    H = 9.5
    for s in (-1, 1):  # murs latéraux en tôle ondulée
        mu.boxb(0.3, 29, H, s * 14.8, 0.5, 0.4, c="galva", bev=0.03)
        for k in range(14):
            mu.boxb(0.12, 0.25, H, s * 14.95, -13.5 + k * 2.1, 0.4, c="metal_light", bev=0)
    mu.boxb(29.6, 0.3, H, 0, 14.8, 0.4, c="galva", bev=0.03)
    for k in range(14):
        mu.boxb(0.25, 0.12, H, -13.5 + k * 2.1, 14.95, 0.4, c="metal_light", bev=0)
    for k, (x, z, w, h, c) in enumerate(((-14.9, 2.0, 0.1, 3.0, "wood_old"), (14.9, 5.0, 0.1, 2.5, "wood"), (-14.9, 7.0, 0.1, 2.0, "rust"))):
        mu.box(0.35, 4.0, h, at=(x, -6 + k * 7, z + h / 2), c=c, bev=0.03)  # planches rapiécées
    for s in (-1, 1):
        mu.boxb(0.5, 0.5, H + 0.5, s * 14.6, -14.6, 0.4, c="wood_old", bev=0.05)  # poteaux d'entrée
    mu.boxb(30, 0.5, 1.6, 0, -14.6, H - 1.2, c="wood_old", bev=0.05)  # linteau
    mu.decal(4, 2.5, (14.97, 4, 3), c="rust", rot=(0, 0, 90), seed=1)
    mu.decal(3, 2, (-14.97, -8, 6), c="rust_dark", rot=(0, 0, 90), seed=2)
    to.box(31, 31, 0.3, at=(0, 0, H + 1.2), rot=(-6, 0, 0), c="galva", bev=0.03)
    for k in range(15):
        to.box(0.3, 31, 0.15, at=(-14 + k * 2, 0, H + 1.42), rot=(-6, 0, 0), c="metal_light", bev=0)
    for k, (x, y, w) in enumerate(((-8, 5, 5), (6, -4, 4), (10, 8, 3))):
        to.box(w, w * 0.7, 0.05, at=(x, y, H + 1.6 - y * 0.105), rot=(-6, 0, 0), c="rust", bev=0)
    to.box(4, 3, 0.4, at=(-3, 9, H + 2.2), rot=(-6, 0, 15), c="tarp_blue", bev=0.05)  # bâche + pneu pour tenir
    to.torus(0.6, 0.25, at=(4, 6, H + 0.95), rot=(-6, 0, 0), c="rubber", segs=10, sides=5)
    en.boxb(14, 0.4, 2.6, 0, -15.0, H + 1.6, c="wood_dark", bev=0.06)
    for k in range(9):  # tubes néon, un sur deux éteint
        en.boxb(1.2, 0.15, 0.18, -5.6 + k * 1.4, -15.25, H + 2.9, c=("neon_pink" if k % 3 != 1 else "grey_dark"), bev=0.02)
        en.boxb(0.18, 0.15, 1.6, -6.2 + k * 1.4, -15.25, H + 2.0, c=("neon_blue" if k % 2 == 0 else "grey_dark"), bev=0.02)
    en.boxb(0.25, 0.25, 2.6, -7.2, -14.9, H + 0.9, c="metal_dark", bev=0.03)
    en.boxb(0.25, 0.25, 2.6, 7.2, -14.9, H + 0.9, c="metal_dark", bev=0.03)
    return m


def casino_moyen():
    m = M("casino_moyen", (36, 20, 36), "Casino niveau 2 : bâtiment en brique", "Façade ouverte vers -Z", grime=False)
    mu, to, en = m.part("Murs"), m.part("Toit"), m.part("Enseigne")
    mu.boxb(36, 36, 0.5, 0, 0, 0, c="concrete", bev=0.08)
    H = 14
    for s in (-1, 1):
        mu.boxb(1.0, 34, H, s * 17.2, 0.5, 0.5, c="brick", bev=0.08)
        for z in range(2, int(H), 2):
            mu.boxb(1.05, 34.1, 0.08, s * 17.2, 0.5, z, c="brick_dark", bev=0)
    mu.boxb(35.4, 1.0, H, 0, 17.2, 0.5, c="brick", bev=0.08)
    for s in (-1, 1):
        mu.boxb(4, 1.2, H, s * 15.4, -16.6, 0.5, c="brick", bev=0.08)  # trumeaux d'entrée
    mu.boxb(36, 1.2, 4, 0, -16.6, H - 3.5, c="brick", bev=0.08)  # bandeau au-dessus de l'ouverture
    mu.boxb(36.4, 1.6, 0.4, 0, -16.6, H - 3.6, c="cream", bev=0.05)
    for x in (-15.4, 15.4):
        window(mu, mu, x, 6, 2.0, 3.0, "-y", -17.2, frame="cream")
    for i in range(16):  # marquise rouge
        mu.box(2.2, 4.5, 0.15, at=(-16.5 + i * 2.2, -19.2, H - 4.5), rot=(12, 0, 0), c=("red" if i % 2 == 0 else "red_dark"), bev=0)
    for x in range(-16, 17, 8):
        mu.rod((x, -21.2, H - 5.0), (x, -17.2, H - 3.8), 0.08, c="gold", sides=4)
    to.boxb(36.4, 36.4, 0.8, 0, 0, H + 0.5, c="concrete_dark", bev=0.08)
    to.boxb(36.4, 1.0, 1.2, 0, -17.7, H + 1.3, c="cream", bev=0.08)
    en.boxb(18, 0.6, 4.0, 0, -17.6, H + 0.5, c="red_dark", bev=0.1)
    en.boxb(16.4, 0.4, 2.8, 0, -17.95, H + 1.1, c="cream", bev=0.05)
    for k in range(20):  # ampoules du cadre
        t = k / 20
        per = 2 * (17 + 3.4)
        d = t * per
        if d < 17:
            x, z = -8.5 + d, H + 0.8
        elif d < 20.4:
            x, z = 8.5, H + 0.8 + (d - 17)
        elif d < 37.4:
            x, z = 8.5 - (d - 20.4), H + 4.2
        else:
            x, z = -8.5, H + 4.2 - (d - 37.4)
        en.sphere(0.22, at=(x, -18.0, z), c="light_warm", segs=6, rings=4)
    return m


def casino_palace():
    m = M("casino_palace", (40, 30, 40), "Casino niveau 3 : palace doré", "Façade ouverte à colonnes vers -Z", grime=False)
    mu, to, en = m.part("Murs"), m.part("Toit"), m.part("Enseigne")
    mu.boxb(40, 40, 1.0, 0, 0, 0, c="marble", bev=0.15)
    for k in range(3):
        mu.boxb(30 - k * 2, 1.2, 0.35, 0, -19.4 + k * 1.2, k * 0.35, c="marble", bev=0.05)
    H = 16
    for s in (-1, 1):
        mu.boxb(1.2, 37, H, s * 18.8, 1.0, 1.0, c="white", bev=0.1)
        for y in (-8, 0, 8):
            window(mu, mu, y, 9.0, 2.4, 5.0, "-x" if s < 0 else "+x", s * 18.8, frame="gold")
    mu.boxb(37.6, 1.2, H, 0, 18.8, 1.0, c="white", bev=0.1)
    for x in [-17 + i * (34 / 7) for i in range(8)]:  # colonnade ouverte
        mu.cyl(0.85, H - 1.0, at=(x, -17.8, 1.0), c="white", segs=12, bev=0.08)
        mu.cyl(1.1, 0.5, at=(x, -17.8, 1.0), c="gold", segs=12, bev=0.05)
        mu.cyl(1.1, 0.6, at=(x, -17.8, H - 0.4), c="gold", segs=12, bev=0.05)
    mu.boxb(39, 3, 1.4, 0, -17.8, H + 0.2, c="white", bev=0.1)
    mu.boxb(39.5, 3.4, 0.4, 0, -17.8, H + 1.6, c="gold", bev=0.05)
    to.boxb(39, 39, 0.8, 0, 0.5, H + 1.0, c="white", bev=0.1)
    to.prism([(-19.5, 0), (19.5, 0), (0, 4.0)], 3.0, at=(0, -17.8, H + 2.0), c="white", bev=0.08)  # fronton
    to.prism([(-16, 0.5), (16, 0.5), (0, 3.4)], 0.3, at=(0, -19.35, H + 2.0), c="gold")
    to.cyl(8.5, 3.0, at=(0, 3, H + 1.8), c="white", segs=16, bev=0.1)
    to.sphere(8.5, at=(0, 3, H + 4.8), c="gold", segs=16, rings=10, scale=(1, 1, 0.75),
              deform=lambda co: Vector((co.x, co.y, max(co.z, 0))))
    to.lathe([(0, 0), (0.8, 0), (0.4, 1.5), (0.1, 2.6), (0, 2.8)], segs=8, at=(0, 3, H + 4.8 + 6.3), c="gold")
    for x in (-18, 18):
        to.sphere(1.0, at=(x, -17.8, H + 2.6), c="gold", segs=8, rings=5)
    en.boxb(22, 1.0, 5.0, 0, -19.6, H - 5.6, c="gold", bev=0.15)
    en.boxb(20, 0.4, 3.6, 0, -20.1, H - 4.9, c="light_white", bev=0.05)
    for k in range(16):
        x = -10.6 + k * (21.2 / 15)
        for z in (H - 5.3, H - 1.0):
            en.sphere(0.25, at=(x, -20.15, z), c="light_warm", segs=5, rings=3)
    return m


def panneau_parcelle():
    m = M("panneau_parcelle", (6, 5, 1), "Panneau de parcelle", "Zone vierge au centre pour le nom du joueur")
    pa, pi = m.part("Panneau"), m.part("Pied")
    pi.boxb(0.5, 0.5, 3.2, 0, 0.15, 0, c="wood", bev=0.06)
    pi.boxb(1.2, 1.0, 0.25, 0, 0.15, 0, c="concrete", bev=0.04)
    for k in range(4):
        pa.box(6.0 - 0.15 * (k % 2), 0.25, 0.72, at=(0.05 * (k % 2), -0.2, 2.35 + k * 0.74), c=("wood_light" if k % 2 else "pallet"), bev=0.05)
    pa.boxb(4.4, 0.06, 1.8, 0, -0.35, 2.7, c="cream", bev=0)  # zone plate vide
    for x in (-2.7, 2.7):
        for z in (2.4, 4.6):
            pa.sphere(0.08, at=(x, -0.36, z), c="metal_dark", segs=4, rings=3)  # clous
    return m


def arche():
    m = M("arche_allee", (20, 14, 3), "Arche de l'allée", "Enseigne vierge (« ALLÉE DES CASINOS » en jeu)", grime=False)
    a, en = m.part("Arche"), m.part("Enseigne")
    for s in (-1, 1):
        a.boxb(2.2, 2.6, 10, s * 8.8, 0, 0, c="red", bev=0.15)
        a.boxb(2.8, 3.0, 0.8, s * 8.8, 0, 0, c="gold", bev=0.08)
        a.boxb(2.8, 3.0, 0.6, s * 8.8, 0, 9.6, c="gold", bev=0.08)
    pts = [(8.8 * math.cos(math.radians(t)), 0, 10 + 3.2 * math.sin(math.radians(t))) for t in range(0, 181, 15)]
    a.pipe(pts, 0.8, c="red", sides=8)
    a.pipe([(x, -1.0, z) for x, _, z in pts], 0.2, c="gold", sides=5)
    for k in range(25):
        t = math.radians(k * 180 / 24)
        a.sphere(0.25, at=(9.8 * math.cos(t), -0.9, 10 + 4.0 * math.sin(t)), c="light_warm", segs=6, rings=4)
    for s in (-1, 1):
        for z in range(1, 10, 2):
            a.sphere(0.25, at=(s * 8.8, -1.35, z + 0.3), c="light_warm", segs=6, rings=4)
    en.boxb(12, 0.5, 2.6, 0, -0.6, 9.2, c="cream", bev=0.08)
    en.boxb(12.6, 0.4, 3.2, 0, -0.3, 8.9, c="gold", bev=0.06)
    for x in (-5, 5):
        en.rod((x, -0.3, 11.8), (x, -0.3, 12.8), 0.06, c="metal_dark", sides=4)
    return m


def coffre():
    m = M("coffre_recettes", (3, 3, 3), "Coffre des recettes", "Porte sur charnière côté gauche")
    c, po = m.part("Coffre"), m.part("Porte", pivot=(-1.2, -1.25, 0.4))
    for x in (-1.1, 1.1):
        for y in (-1.1, 1.1):
            c.boxb(0.4, 0.4, 0.3, x, y, 0, c="iron", bev=0.05)
    c.boxb(2.8, 2.6, 2.5, 0, 0.1, 0.3, c="gunmetal", bev=0.2, deform=m.noise(0.03, 1))
    c.box(0.06, 1.0, 0.7, at=(1.42, 0.4, 1.8), c="gunmetal", bev=0, deform=lambda co: Vector((co.x - 0.05, co.y, co.z)))  # bosse
    c.decal(0.8, 0.4, (1.41, -0.3, 0.8), c="rust", rot=(0, 0, 90), seed=2)
    po.boxb(2.4, 0.25, 2.1, 0, -1.25, 0.5, c="steel_blue", bev=0.1)
    po.cyl(0.4, 0.12, at=(0.3, -1.38, 1.75), rot=(90, 0, 0), c="chrome", segs=16, bev=0.03)
    po.cyl(0.15, 0.12, at=(0.3, -1.5, 1.75), rot=(90, 0, 0), c="metal_dark", segs=8, bev=0.02)
    for k in range(12):
        a = 2 * math.pi * k / 12
        po.box(0.04, 0.05, 0.1, at=(0.3 + 0.33 * math.cos(a), -1.51, 1.75 + 0.33 * math.sin(a)), rot=(0, -math.degrees(a) + 90, 0), c="black", bev=0)
    for z in (0.9, 1.2):
        po.rod((0.0, -1.4, z), (0.8, -1.4, z), 0.05, c="chrome", sides=5)
    po.rod((0.8, -1.4, 0.75), (0.8, -1.4, 1.35), 0.05, c="chrome", sides=5)
    for x in (-1.1, 1.1):
        po.cyl(0.08, 0.5, at=(-1.15, -1.3, 0.7 + (x + 1.1) * 0.55), c="metal_dark", segs=6, bev=0)  # gonds
    rng = random.Random(3)
    for k in range(9):  # pièces qui dépassent de la porte et tas au sol
        x = rng.uniform(-1.0, 1.0)
        if k < 4:
            c.cyl(0.18, 0.05, at=(x, -1.38, 2.6), rot=(70, 0, rng.uniform(-30, 30)), c="gold", segs=10, bev=0)
        else:
            c.cyl(0.18, 0.05, at=(x, -1.55 + rng.uniform(-0.1, 0.1), 0.0 + 0.05 * (k % 3)), c="gold", segs=10, bev=0)
    return m


MODELS = [
    ("185_sac_a_dos", sac_a_dos), ("186_caisse_pieces", caisse_pieces), ("187_barque_moteur", barque), ("188_bateau_cargo", cargo),
    ("191_casino_baraque", casino_baraque), ("192_casino_moyen", casino_moyen), ("193_casino_palace", casino_palace),
    ("194_panneau_parcelle", panneau_parcelle), ("195_arche_allee", arche), ("196_coffre_recettes", coffre),
]
