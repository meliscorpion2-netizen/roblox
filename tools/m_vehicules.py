"""17–21 : véhicules. Longueur selon Y (avant = -Y), largeur X, hauteur Z."""
import math

from lib import Model

CAT = "02_vehicules"


def tapered(w, d, h, tx, ty, z0, z):
    k = (z - z0) / h
    return w * (1 - (1 - tx) * k), d * (1 - (1 - ty) * k)


def cabin(body, glass, cw, cd, ch, yc, z0, tx, ty, c, glass_c="glass", pillar=True, bev=0.22, deform=None):
    body.box(cw, cd, ch, at=(0, yc, z0 + ch / 2), taper=(tx, ty), c=c, bev=bev, deform=deform)
    za, zb = z0 + 0.28, z0 + ch - 0.22
    wa, da = tapered(cw, cd, ch, tx, ty, z0, za)
    wb, db = tapered(cw, cd, ch, tx, ty, z0, zb)
    hz = zb - za
    # bandeau latéral (vitres de côté)
    glass.box(wa + 0.08, da - 0.8, hz, at=(0, yc, za + hz / 2), taper=((wb + 0.08) / (wa + 0.08), (db - 0.8) / (da - 0.8)),
              c=glass_c, bev=0.03)
    # pare-brise et lunette arrière
    glass.box(wa - 0.55, da + 0.08, hz, at=(0, yc, za + hz / 2), taper=((wb - 0.55) / (wa - 0.55), (db + 0.08) / (da + 0.08)),
              c=glass_c, bev=0.03)
    if pillar:
        wm, _ = tapered(cw, cd, ch, tx, ty, z0, za)
        body.box(wa + 0.14, 0.28, hz + 0.05, at=(0, yc + 0.1, za + hz / 2), taper=((wb + 0.14) / (wa + 0.14), 1), c=c, bev=0.03)


def wheel(m, name, x, y, r, w, rim="metal_light", tire="rubber", side=1):
    p = m.part(name, pivot=(x, y, r))
    p.cyl(r, w, at=(x - w / 2, y, r), rot=(0, 90, 0), c=tire, segs=14, bev=0.12)
    p.cyl(r * 0.55, 0.06, at=(x + side * (w / 2 - 0.02), y, r), rot=(0, 90 * side, 0), c=rim, segs=10, bev=0.02)
    p.cyl(r * 0.18, 0.08, at=(x + side * (w / 2 + 0.02), y, r), rot=(0, 90 * side, 0), c="metal_dark", segs=6, bev=0)
    return p


def arches(p, x_side, ys, r, z_c, c="soot"):
    for y in ys:
        for s in (-1, 1):
            p.prism([(r * 1.12 * math.cos(math.radians(a)), r * 1.12 * math.sin(math.radians(a))) for a in range(0, 181, 30)],
                    0.04, at=(s * x_side, y, z_c), rot=(0, 0, 90), plane="XZ", c=c)


def lights_front(m, ys, xs, z, r=0.32, c="light_warm", shape="round"):
    L = m.part("Phares")
    for x in xs:
        if shape == "round":
            L.cyl(r, 0.08, at=(x, ys, z), rot=(90, 0, 0), c=c, segs=10, bev=0.02)
        else:
            L.box(r * 2.2, 0.08, r * 1.1, at=(x, ys - 0.03, z), c=c, bev=0.02)


def lights_back(m, y, xs, z, c="light_red", w=0.5, h=0.35):
    L = m.part("FeuxArriere")
    for x in xs:
        L.box(w, 0.08, h, at=(x, y + 0.03, z), c=c, bev=0.02)


def vieille_voiture():
    W, H, L = 5.2, 4.6, 10.1
    m = Model("vieille_voiture", (W, H, L), CAT, "Vieille voiture cabossée")
    b = m.part("Carrosserie")
    g = m.part("Vitres")
    nz = m.noise(0.05, 31)
    def dent(co):
        co = nz(co)
        if co.x > 1.8 and -1.5 < co.y < 1.0 and 1.0 < co.z < 2.2:  # portière enfoncée
            co.x -= 0.18 * (1 - abs(co.y + 0.25) / 1.25)
        if co.y < -4.6 and co.x < -0.8:  # pare-choc avant tordu
            co.y += 0.15
        return co
    b.box(4.7, L - 0.2, 1.7, at=(0, 0, 0.65 + 0.85), c="teal", bev=0.32, deform=dent)
    b.box(0.06, 2.3, 1.2, at=(2.36, -0.25, 1.5), c="grey_light", bev=0.0)  # portière de récup (apprêt gris)
    cabin(b, g, 4.3, 4.6, 1.75, 0.6, 2.3, 0.82, 0.62, "teal", deform=m.noise(0.04, 32))
    b.boxb(4.5, 0.4, 0.45, 0, -L / 2 + 0.2, 0.75, c="chrome", rot=(0, 3, 0))
    b.boxb(4.5, 0.4, 0.45, 0, L / 2 - 0.2, 0.75, c="chrome")
    b.boxb(2.2, 0.08, 0.6, 0, -L / 2 + 0.05, 1.35, c="metal_dark")  # calandre
    b.decal(1.4, 0.7, (-2.37, 2.6, 1.5), c="rust", rot=(0, 0, 90), seed=1)
    b.decal(0.9, 0.5, (2.36, 3.2, 1.0), c="rust_dark", rot=(0, 0, 90), seed=2)
    b.decal(1.2, 0.6, (1.0, -3.3, 2.32), c="rust", rot=(90, 0, 0), seed=3)
    b.box(1.4, 1.2, 0.05, at=(-0.4, -2.0, 2.37), c="red", rot=(0, 0, 8))  # capot d'une autre couleur… en partie
    for s in (-1, 1):
        b.boxb(0.35, 0.25, 0.25, s * 2.42, -1.4, 2.4, c="teal")  # rétros
        b.box(0.25, 0.4, 0.06, at=(s * 2.36, 0.0, 2.05), c="metal_dark")  # poignées
    b.pipe([(-1.3, L / 2 - 0.2, 0.55), (-1.3, L / 2 + 0.0, 0.5), (-1.25, L / 2 + 0.05, 0.42)], 0.1, c="metal_dark", sides=6)
    b.pipe([(0.0, 0.3, 4.6), (0.6, 0.6, 4.4)], 0.03, c="metal", sides=3)  # antenne tordue
    arches(b, 2.37, (-3.0, 3.1), 1.0, 0.95)
    g.decal(0.9, 0.9, (0.4, -1.68, 3.2), c="grey_light", rot=(-55, 0, 0), t=0.02, seed=9)  # pare-brise étoilé
    lights_front(m, -L / 2 + 0.05, (-1.6, 1.6), 1.45)
    lights_back(m, L / 2 - 0.05, (-1.8, 1.8), 1.6)
    for name, x, y in (("Roue_AvG", 2.15, -3.0), ("Roue_AvD", -2.15, -3.0), ("Roue_ArG", 2.15, 3.1), ("Roue_ArD", -2.15, 3.1)):
        wheel(m, name, x, y, 0.95, 0.75, rim=("rust" if name == "Roue_ArD" else "metal_light"), side=(1 if x > 0 else -1))
    return m


def camionnette():
    W, H, L = 5.6, 6.2, 11.3
    m = Model("camionnette", (W, H, L), CAT, "Camionnette utilitaire")
    b = m.part("Carrosserie")
    g = m.part("Vitres")
    nz = m.noise(0.04, 41)
    b.box(5.2, 7.9, 5.3, at=(0, 1.6, 0.75 + 2.65), c="white", bev=0.3, deform=nz)  # caisse
    b.box(5.2, 3.4, 1.9, at=(0, -3.9, 0.75 + 0.95), c="white", bev=0.3, taper=(1, 0.9), deform=nz)  # capot
    cabin(b, g, 5.0, 2.3, 2.6, -2.7, 2.6, 0.95, 0.55, "white", pillar=False)
    b.box(5.25, 0.25, 0.5, at=(0, -5.5, 1.0), c="plastic_black", bev=0.08)
    b.box(5.25, 0.25, 0.5, at=(0, 5.55, 1.0), c="plastic_black", bev=0.08)
    b.boxb(2.6, 0.06, 0.55, 0, -5.62, 1.3, c="plastic_black")
    b.boxb(0.06, 7.6, 0.5, 2.62, 1.6, 3.2, c="orange")
    b.boxb(0.06, 7.6, 0.5, -2.62, 1.6, 3.2, c="orange")
    b.boxb(0.06, 0.05, 4.6, 2.62, 1.0, 1.0, c="metal_dark")  # porte coulissante (jointure)
    b.boxb(0.06, 0.05, 4.6, -2.62, 2.5, 1.0, c="metal_dark")
    b.boxb(0.04, 0.05, 4.9, 0, 5.62, 0.9, c="metal_dark")
    b.decal(1.6, 1.0, (2.62, 3.5, 1.7), c="rust", rot=(0, 0, 90), seed=4)
    b.decal(2.2, 1.4, (-2.61, -0.5, 4.6), c="sky", rot=(0, 0, 90), seed=5)  # tag (forme abstraite)
    b.decal(1.4, 1.0, (-2.62, 0.4, 4.4), c="pink", rot=(0, 0, 90), seed=6)
    b.decal(1.3, 0.6, (0.0, 5.62, 2.4), c="mud", rot=(0, 0, 180), seed=7)
    for x in (-1.5, 0, 1.5):  # galerie de toit
        b.boxb(0.12, 6.5, 0.12, x, 1.8, 6.05, c="metal_dark")
    for y in (-1.0, 4.5):
        b.boxb(4.4, 0.12, 0.25, 0, y, 5.9, c="metal_dark")
    b.box(1.6, 1.0, 0.5, at=(0.6, 2.6, 6.35), c="tarp_blue", rot=(0, 0, 10), bev=0.15)  # bâche roulée
    b.cyl(0.15, 3.2, at=(-1.0, 0.7, 6.3), rot=(-90, 0, 0), c="wood_old", segs=6, bev=0)  # vieille échelle
    for s in (-1, 1):
        b.boxb(0.35, 0.3, 0.35, s * 2.75, -3.1, 3.0, c="plastic_black")
    arches(b, 2.61, (-3.7, 3.4), 1.0, 1.0)
    lights_front(m, -5.68, (-1.85, 1.85), 2.1, r=0.32, shape="rect")
    lights_back(m, 5.6, (-2.3, 2.3), 2.0, w=0.4, h=0.9)
    for name, x, y in (("Roue_AvG", 2.3, -3.7), ("Roue_AvD", -2.3, -3.7), ("Roue_ArG", 2.3, 3.4), ("Roue_ArD", -2.3, 3.4)):
        wheel(m, name, x, y, 1.0, 0.75, side=(1 if x > 0 else -1))
    return m


def citadine():
    W, H, L = 5.0, 4.2, 8.3
    m = Model("citadine", (W, H, L), CAT, "Petite citadine")
    b = m.part("Carrosserie")
    g = m.part("Vitres")
    nz = m.noise(0.04, 51)
    def dent(co):
        co = nz(co)
        if co.y > 3.6 and co.x > 0.6:  # coin arrière embouti
            co.y -= 0.2
        return co
    b.box(4.6, L - 0.2, 1.6, at=(0, 0, 0.6 + 0.8), c="yellow", bev=0.4, deform=dent)
    cabin(b, g, 4.3, 5.0, 2.0, 0.9, 2.15, 0.8, 0.7, "yellow", bev=0.3)
    b.boxb(4.5, 0.4, 0.45, 0, -L / 2 + 0.2, 0.65, c="plastic_black")
    b.boxb(4.5, 0.4, 0.45, 0, L / 2 - 0.2, 0.65, c="plastic_black")
    b.box(0.06, 1.6, 0.9, at=(-2.31, -0.3, 1.5), c="blue", bev=0.0)  # portière dépareillée
    b.decal(1.0, 0.5, (2.31, 2.6, 1.0), c="rust", rot=(0, 0, 90), seed=8)
    b.decal(0.8, 0.5, (1.0, -3.6, 2.21), c="mud", rot=(90, 0, 0), seed=9)
    b.box(0.9, 0.04, 0.6, at=(-0.9, L / 2 - 0.05, 2.9), c="cardboard", rot=(-20, 0, 6), bev=0)  # carton scotché à la place d'une vitre
    for s in (-1, 1):
        b.boxb(0.3, 0.22, 0.22, s * 2.36, -1.3, 2.25, c="yellow")
    b.cyl(0.1, 0.18, at=(-1.2, L / 2 - 0.1, 0.55), rot=(-90, 0, 0), c="metal_dark", segs=6)
    arches(b, 2.31, (-2.55, 2.55), 0.85, 0.85)
    lights_front(m, -L / 2 + 0.06, (-1.5, 1.5), 1.5, r=0.33)
    lights_back(m, L / 2 - 0.05, (-1.7, 1.7), 1.7, w=0.45, h=0.5)
    for name, x, y in (("Roue_AvG", 2.05, -2.55), ("Roue_AvD", -2.05, -2.55), ("Roue_ArG", 2.05, 2.55), ("Roue_ArD", -2.05, 2.55)):
        wheel(m, name, x, y, 0.82, 0.7, side=(1 if x > 0 else -1))
    return m


def camion_porteur():
    W, H, L = 6.9, 8.8, 20.4
    m = Model("camion_porteur", (W, H, L), CAT, "Camion porteur avec caisse")
    ch = m.part("Chassis")
    ch.boxb(1.8, 18.6, 0.6, 0, 0.6, 0.9, c="iron")
    for y in (-8.2, 9.8):
        ch.boxb(6.2, 0.5, 0.6, 0, y, 0.8, c="plastic_black")
    ch.boxb(1.2, 1.8, 1.0, -2.6, -1.5, 1.0, c="metal")  # réservoir
    ch.boxb(0.9, 1.4, 0.8, 2.6, -1.0, 1.1, c="metal_dark")
    ch.cyl(0.15, 3.0, at=(2.85, -5.4, 2.0), c="chrome", segs=6, bev=0)  # échappement vertical
    cab = m.part("Cabine")
    g = m.part("Vitres")
    cab.box(6.3, 4.6, 3.6, at=(0, -7.6, 1.4 + 1.8), c="red", bev=0.35, deform=m.noise(0.04, 61))
    cabin(cab, g, 6.1, 4.2, 2.6, -7.5, 5.0, 0.95, 0.85, "red", pillar=False)
    cab.box(5.8, 3.6, 0.9, at=(0, -7.3, 8.0), c="red", taper=(0.9, 0.7), bev=0.25)  # déflecteur
    cab.boxb(4.0, 0.1, 1.5, 0, -9.95, 1.9, c="metal_dark")  # calandre
    for z in (2.2, 2.6, 3.0):
        cab.boxb(3.6, 0.12, 0.12, 0, -10.0, z, c="chrome")
    for s in (-1, 1):
        cab.boxb(0.2, 0.5, 1.3, s * 3.3, -8.6, 5.3, c="plastic_black")  # rétros
        cab.boxb(0.9, 0.5, 0.2, s * 3.0, -8.6, 5.9, c="metal_dark")
        cab.boxb(0.05, 0.05, 2.9, s * 3.16, -6.4, 1.8, c="metal_dark")
        cab.boxb(0.5, 0.6, 0.2, s * 2.9, -6.6, 1.2, c="metal_dark")  # marchepied
    cab.decal(1.2, 0.8, (3.16, -8.6, 2.2), c="rust", rot=(0, 0, 90), seed=11)
    cab.decal(1.0, 0.5, (-1.8, -9.92, 4.0), c="mud", rot=(0, 0, 0), seed=12)
    box = m.part("Caisse")
    box.boxb(6.6, 14.2, 7.0, 0, 2.95, 1.75, c="white", bev=0.12, deform=m.noise(0.03, 62))
    for y in range(-3, 10, 2):
        for s in (-1, 1):
            box.boxb(0.08, 0.15, 6.9, s * 3.32, y, 1.8, c="alu", bev=0)
    box.boxb(6.75, 14.3, 0.2, 0, 2.95, 8.6, c="alu")
    box.boxb(6.75, 14.3, 0.2, 0, 2.95, 1.7, c="alu")
    box.decal(4.0, 2.6, (3.33, 1.0, 5.0), c="sky", rot=(0, 0, 90), seed=13)  # emplacement de logo (vierge), délavé
    box.decal(3.0, 1.6, (-3.33, 4.5, 3.0), c="pink", rot=(0, 0, 90), seed=14)  # tag
    box.decal(2.0, 1.0, (-3.33, 6.5, 2.4), c="green", rot=(0, 0, 90), seed=15)
    box.decal(2.5, 1.5, (2.0, -4.12, 6.8), c="mud", rot=(0, 0, 0), seed=16)
    porte = m.part("PorteArriere", pivot=(0, 10.05, 8.5))
    porte.boxb(6.2, 0.1, 6.6, 0, 10.07, 1.95, c="alu", bev=0.03)
    for z in (2.6, 3.9, 5.2, 6.5, 7.8):
        porte.boxb(6.0, 0.06, 0.08, 0, 10.14, z, c="metal", bev=0)
    porte.boxb(0.8, 0.12, 0.15, 0, 10.15, 2.3, c="metal_dark")
    lights_front(m, -10.0, (-2.4, 2.4), 2.2, r=0.35, shape="rect")
    lights_back(m, 10.0, (-2.8, 2.8), 1.15, w=0.5, h=0.3)
    wheels = (("Roue_AvG", 2.75, -6.6), ("Roue_AvD", -2.75, -6.6), ("Roue_Ar1G", 2.75, 5.0), ("Roue_Ar1D", -2.75, 5.0),
              ("Roue_Ar2G", 2.75, 7.6), ("Roue_Ar2D", -2.75, 7.6))
    for name, x, y in wheels:
        wheel(m, name, x, y, 1.25, 1.1, side=(1 if x > 0 else -1))
    return m


def epave():
    W, H, L = 4.8, 4.6, 10.1
    m = Model("epave_brulee", (W, H, L), CAT, "Épave de voiture brûlée")
    b = m.part("Epave")
    nz = m.noise(0.09, 71)
    def crush(co):
        co = nz(co)
        if co.y < -3.5:  # avant écrasé
            co.z -= 0.25 * (-(co.y + 3.5)) / 1.5
        return co
    for x in (-1.9, 1.9):  # parpaings
        for y in (-3.0, 3.1):
            b.boxb(1.0, 0.8, 0.85, x, y, 0, c="concrete", deform=m.noise(0.02, int(x * 10 + y)))
    b.box(4.6, L - 0.3, 1.6, at=(0, 0, 0.85 + 0.8), c="char", bev=0.3, deform=crush)
    cabin(b, b, 4.2, 4.5, 1.8, 0.6, 2.45, 0.82, 0.62, "char", glass_c="soot", deform=nz)
    b.decal(2.2, 1.2, (2.31, 0.5, 1.8), c="rust", rot=(0, 0, 90), seed=21)
    b.decal(2.6, 1.0, (-2.31, -1.0, 1.6), c="rust_dark", rot=(0, 0, 90), seed=22)
    b.decal(1.6, 1.2, (2.31, 3.4, 1.4), c="ash", rot=(0, 0, 90), seed=23)
    b.decal(2.0, 1.4, (0.0, 2.8, 2.46), c="rust", rot=(90, 0, 0), seed=24)
    b.decal(1.8, 1.0, (0.3, -4.95, 1.6), c="rust_orange", rot=(0, 0, 0), seed=25)
    # capot entrouvert et tordu
    b.box(4.0, 2.9, 0.1, at=(0, -3.0, 2.85), rot=(14, 3, 2), c="char", bev=0.02, deform=m.noise(0.06, 26))
    arches(b, 2.31, (-3.0, 3.1), 0.95, 1.3, c="soot")
    for x in (-2.0, 2.0):  # fusées / moyeux nus
        for y in (-3.0, 3.1):
            b.cyl(0.3, 0.25, at=(x - 0.125 * (1 if x < 0 else -1) * 0 - 0.125, y, 1.3), rot=(0, 90, 0), c="rust_dark", segs=6)
    b.box(1.6, 0.5, 0.3, at=(-0.8, -5.0, 0.95), c="iron", rot=(0, 20, 8))  # pare-choc tombé
    b.box(0.7, 0.5, 0.2, at=(1.5, 1.0, 2.6), c="ash", rot=(0, 0, 0))
    return m


MODELS = [
    ("17_vieille_voiture", vieille_voiture), ("18_camionnette", camionnette), ("19_citadine", citadine),
    ("20_camion_porteur", camion_porteur), ("21_epave_brulee", epave),
]
