"""22–33 : déchets, misère urbaine, animaux."""
import math

from lib import Model

CAT = "03_dechets"


def carton_ouvert():
    m = Model("carton_ouvert", (2.1, 1.9, 1.7), CAT, "Carton ouvert", None, "Variante de 22")
    p = m.part("Carton")
    w, d, h, t = 1.7, 1.4, 1.2, 0.04
    nz = m.noise(0.03, 1)
    def cave(co):
        co = nz(co)
        if co.y < -0.5 and co.z > 0.5:  # flanc avant affaissé
            co.y += 0.12 * (co.z - 0.5) / 0.7 * max(0, 1 - abs(co.x) / 0.9)
        return co
    p.boxb(w, d, t, 0, 0, 0, c="cardboard_dark", bev=0.01)
    for s in (-1, 1):
        p.boxb(t, d, h, s * (w / 2 - t / 2), 0, 0, c="cardboard", bev=0.01, deform=cave)
        p.boxb(w, t, h, 0, s * (d / 2 - t / 2), 0, c="cardboard", bev=0.01, deform=cave)
    # rabats ouverts
    p.box(w, 0.04, 0.68, at=(0, -d / 2 - 0.2, h + 0.27), rot=(-35, 0, 0), c="cardboard", bev=0.01)
    p.box(w, 0.04, 0.68, at=(0, d / 2 + 0.17, h + 0.3), rot=(28, 0, 0), c="cardboard", bev=0.01)
    p.box(0.04, d, 0.5, at=(w / 2 + 0.17, 0, h + 0.17), rot=(0, 42, 0), c="cardboard", bev=0.01)
    p.box(0.04, d * 0.7, 0.5, at=(-w / 2 - 0.1, 0.15, h + 0.2), rot=(0, -25, 0), c="cardboard_dark", bev=0.01)
    p.boxb(0.25, d + 0.02, 0.02, 0.0, 0, h - 0.01, c="beige", bev=0)  # scotch
    p.decal(0.6, 0.5, (0.3, -d / 2 - 0.01, 0.4), c="stain", seed=2)
    p.box(1.0, 0.8, 0.3, at=(-0.1, 0.1, 1.0), rot=(10, 5, 20), c="paper_dirty", deform=m.noise(0.06, 3))
    return m


def carton_aplati():
    m = Model("carton_aplati", (2.1, 1.9, 1.7), CAT, "Carton aplati", None, "Variante de 22 : appuyé contre un mur (dos côté +Z)")
    p = m.part("Carton")
    # plaque pliée en deux, adossée
    p.box(2.1, 0.06, 2.39, at=(0, 0.19, 0.965), rot=(-38.4, 0, 0), c="cardboard", bev=0.01, deform=m.noise(0.03, 4))
    p.box(2.05, 0.06, 0.75, at=(0.02, -0.88, 0.05), rot=(-84, 0, 0), c="cardboard_dark", bev=0.01, deform=m.noise(0.03, 5))
    p.box(0.3, 0.02, 2.0, at=(-0.5, 0.17, 1.0), c="beige", rot=(-38.4, 0, 0), bev=0)
    p.decal(0.8, 0.6, (0.4, -0.02, 0.9), c="stain", rot=(-38.4, 0, 0), seed=6)
    p.decal(0.5, 0.3, (-0.5, -0.9, 0.09), c="mud", rot=(-84, 0, 0), seed=7)
    return m


def matelas():
    m = Model("matelas", (4.5, 0.8, 7), CAT, "Matelas sale taché")
    p = m.part("Matelas")
    nz = m.noise(0.03, 11)
    def sag(co):
        co = nz(co)
        if co.z > 0.2:
            co.z -= 0.12 * max(0, 1 - (co.x ** 2 / 4 + co.y ** 2 / 9))
        return co
    p.box(4.5, 7.0, 0.8, at=(0, 0, 0.4), c="mattress", bev=0.22, deform=sag)
    for (x, y, w, h, c, s) in ((-0.8, -1.0, 2.2, 1.8, "stain", 1), (1.1, 1.5, 1.6, 1.3, "stain", 2), (0.7, -2.4, 1.0, 0.7, "mud", 3),
                               (-1.1, 2.2, 1.3, 1.5, "rust", 4), (-0.2, 0.4, 0.8, 0.6, "mud", 6)):
        p.decal(w, h, (x, y, 0.7 - 0.12 * max(0, 1 - (x * x / 4 + y * y / 9)) + 0.05), c=c, rot=(90, 0, 0), t=0.04, seed=s)
    for s in (-1, 1):
        p.box(0.03, 6.4, 0.06, at=(s * 2.25, 0, 0.42), c="sky", bev=0)  # passepoil
    for x in (-1.2, 0, 1.2):
        for y in (-2.0, 0, 2.0):
            p.cyl(0.08, 0.04, at=(x, y, 0.72), c="beige", segs=6, bev=0)
    # ressort qui dépasse
    pts = [(1.6 + 0.12 * math.cos(a), -2.6 + 0.12 * math.sin(a), 0.62 + a * 0.04) for a in [i * 0.6 for i in range(12)]]
    p.pipe(pts, 0.025, c="metal", sides=3)
    p.decal(0.5, 0.4, (1.6, -2.6, 0.78), c="soot", rot=(90, 0, 0), t=0.02, seed=5)
    return m


def pneu():
    m = Model("pneu", (2.6, 0.9, 2.6), CAT, "Pneu usé")
    p = m.part("Pneu")
    p.torus(0.88, 0.42, at=(0, 0, 0.45), c="rubber", segs=18, sides=8, sz=1.07, deform=m.noise(0.015, 1))
    for i in range(18):
        a = 360 * i / 18 + 10
        r = math.radians(a)
        p.box(0.12, 0.32, 0.55, at=(1.27 * math.cos(r), 1.27 * math.sin(r), 0.45), rot=(0, 0, a), c="plastic_black", bev=0.03)
    p.cyl(0.55, 0.06, at=(0, 0, 0.12), c="mud", segs=10, bev=0)  # flaque boueuse au fond
    p.decal(0.4, 0.3, (0.8, -0.6, 0.85), c="mud", rot=(90, 0, 0), t=0.02, seed=2)
    return m


def caddie():
    m = Model("caddie", (2.6, 3, 3.4), CAT, "Caddie de supermarché rouillé")
    p = m.part("Caddie")
    c1, c2 = "galva", "rust"
    # panier : bas (z=1.3) étroit à l'avant, haut (z=2.75) plus large
    def corners(z, front, back, wb, wf):
        return [(-wf / 2, front, z), (wf / 2, front, z), (wb / 2, back, z), (-wb / 2, back, z)]
    lo = corners(1.3, -1.3, 1.25, 1.9, 1.5)
    hi = corners(2.75, -1.7, 1.45, 2.5, 2.1)
    for i in range(4):
        p.rod(lo[i], hi[i], 0.045, c=c1, sides=4)
    for z, ring in ((1.3, lo), (2.75, hi)):
        p.pipe(ring + [ring[0]], 0.045, c=c1 if z > 2 else c2, sides=4, caps=False)
    for k in range(1, 4):
        t = k / 4
        ring = [tuple(lo[i][j] + (hi[i][j] - lo[i][j]) * t for j in range(3)) for i in range(4)]
        p.pipe(ring + [ring[0]], 0.022, c=(c1 if k % 2 else c2), sides=3, caps=False)
    for side in (0, 1, 2, 3):
        a0, a1 = lo[side], lo[(side + 1) % 4]
        b0, b1 = hi[side], hi[(side + 1) % 4]
        n = 7 if side in (1, 3) else 6
        for k in range(1, n):
            t = k / n
            pa = tuple(a0[j] + (a1[j] - a0[j]) * t for j in range(3))
            pb = tuple(b0[j] + (b1[j] - b0[j]) * t for j in range(3))
            p.rod(pa, pb, 0.02, c=(c1 if k % 3 else c2), sides=3)
    for k in range(1, 6):  # fond
        x = -0.85 + k * 0.28
        p.rod((x * 0.85, -1.25, 1.3), (x, 1.2, 1.3), 0.02, c=c2, sides=3)
    # châssis et roues
    p.pipe([(-0.8, -1.4, 0.35), (-0.95, 1.3, 0.35), (-1.0, 1.55, 3.0)], 0.06, c=c1, sides=5)
    p.pipe([(0.8, -1.4, 0.35), (0.95, 1.3, 0.35), (1.0, 1.55, 3.0)], 0.06, c=c1, sides=5)
    p.rod((-0.8, -1.4, 0.35), (0.8, -1.4, 0.35), 0.05, c=c2, sides=4)
    p.rod((-0.95, 1.2, 0.35), (0.95, 1.2, 0.35), 0.05, c=c2, sides=4)
    p.rod((-0.95, 1.2, 0.35), (-0.85, 1.0, 1.3), 0.05, c=c1, sides=4)
    p.rod((0.95, 1.2, 0.35), (0.85, 1.0, 1.3), 0.05, c=c1, sides=4)
    p.boxb(2.15, 0.22, 0.2, 0, 1.6, 2.9, c="red")  # poignée plastique
    for x, y, missing in ((-0.8, -1.4, False), (0.8, -1.4, True), (-0.95, 1.2, False), (0.95, 1.2, False)):
        if missing:
            p.boxb(0.08, 0.08, 0.15, x, y, 0.2, c="rust_dark")
            continue
        p.boxb(0.12, 0.2, 0.15, x, y, 0.2, c="metal_dark")
        p.cyl(0.18, 0.12, at=(x - 0.06, y, 0.18), rot=(0, 90, 0), c="plastic_black", segs=8, bev=0.02)
    # bric-à-brac dedans
    p.sphere(0.45, at=(0.2, 0.3, 1.75), c="bag_black", scale=(1.2, 1, 0.9), segs=7, rings=5, deform=m.noise(0.05, 3))
    p.box(0.8, 0.6, 0.5, at=(-0.3, -0.6, 1.6), rot=(5, 0, 15), c="cardboard")
    p.cyl(0.1, 0.55, at=(0.55, -0.5, 1.4), rot=(30, 20, 0), c="green_dark", segs=6)
    return m


def _tente():
    m = Model("tente_fortune", (7, 5, 7), CAT, "Tente de fortune avec bâche")
    s = m.part("Structure")
    for sx in (-1, 1):
        for y in (-3.1, 3.1):
            s.rod((sx * 3.2, y, 0), (sx * 0.12, y, 4.75), 0.08, c="wood_old", sides=5)
    s.rod((0, -3.4, 4.78), (0, 3.4, 4.78), 0.06, c="yellow", sides=4)
    for x in (-1.2, 0.2, 1.4):
        s.boxb(1.25, 2.2, 0.12, x, 0.6, 0, c="pallet")
    s.box(1.0, 2.0, 0.35, at=(-1.4, 1.4, 0.3), c="fabric_green", bev=0.12, deform=m.noise(0.05, 2))
    s.box(1.6, 0.08, 1.3, at=(1.7, -3.25, 0.65), rot=(0, 0, -15), c="cardboard", bev=0.01)
    s.torus(0.6, 0.25, at=(-2.7, 2.4, 0.25), c="rubber", segs=12, sides=6)
    s.boxb(0.5, 0.5, 0.5, 3.0, 2.6, 0, c="concrete", deform=m.noise(0.03, 3))
    s.box(0.5, 0.4, 0.4, at=(0.6, -1.5, 0.32), rot=(0, 0, 25), c="red", bev=0.06)  # glacière
    b = m.part("Bache")
    L = math.hypot(3.2, 4.75)
    ang = math.degrees(math.atan2(4.75, 3.2))
    for sx in (-1, 1):
        nz = m.noise(0.07, 5 + sx)
        def sag(co, nz=nz):
            co = nz(co)
            # le creux de la bâche entre les perches
            co.z -= 0.22 * max(0, 1 - (co.x / (L / 2)) ** 2) * max(0, 1 - (co.y / 3.4) ** 2)
            return co
        b.box(L + 0.1, 6.9, 0.06, at=(sx * 1.62, 0, 2.4), rot=(0, sx * ang, 0), c="tarp_blue", bev=0, deform=sag)
    # pan arrière fermé par une couverture
    b.prism([(-3.1, 0), (3.1, 0), (0, 4.6)], 0.06, at=(0, 3.25, 0.05), c="fabric_brown", deform=m.noise(0.05, 8))
    b.decal(1.6, 1.0, (-1.6, 0.0, 2.5), c="grey_light", rot=(0, -ang, 0), t=0.07, seed=9)  # rustine
    return m


def sac_couchage():
    m = Model("sac_couchage", (2, 0.6, 5), CAT, "Sac de couchage / couverture en boule")
    p = m.part("SacCouchage")
    nz = m.noise(0.04, 21)
    p.box(1.9, 3.8, 0.35, at=(0, 0.5, 0.18), c="fabric_blue", bev=0.15, deform=nz)
    p.box(1.95, 3.0, 0.08, at=(0, 0.9, 0.38), rot=(2, 0, 0), c="fabric_red", bev=0.03, deform=m.noise(0.05, 22))  # couverture
    p.sphere(0.6, at=(0.0, -1.7, 0.32), c="fabric_blue", scale=(1.55, 1.25, 0.5), segs=8, rings=5, deform=m.noise(0.07, 23))
    p.sphere(0.4, at=(-0.35, -2.2, 0.25), c="fabric_red", scale=(1.3, 1.0, 0.6), segs=7, rings=5, deform=m.noise(0.05, 24))
    p.decal(0.6, 0.5, (0.5, 1.2, 0.43), c="stain", rot=(90, 0, 0), t=0.02, seed=25)
    return m


def bouteille():
    m = Model("bouteille", (0.35, 1, 0.35), CAT, "Bouteille vide")
    p = m.part("Bouteille")
    p.lathe([(0, 0), (0.16, 0), (0.175, 0.03), (0.175, 0.55), (0.13, 0.68), (0.065, 0.78), (0.06, 0.95), (0.075, 0.97),
             (0.07, 1.0), (0, 1.0)], segs=10, c="green_dark")
    p.cyl(0.18, 0.22, at=(0, 0, 0.2), c="paper_dirty", segs=10, bev=0)  # étiquette délavée (vierge)
    return m


def canette():
    m = Model("canette", (0.35, 0.6, 0.35), CAT, "Canette écrasée")
    p = m.part("Canette")
    def crush(co):
        if 0.15 < co.z < 0.45:
            k = math.sin((co.z - 0.15) / 0.3 * math.pi)
            a = math.atan2(co.y, co.x)
            co.x *= 1 - 0.45 * k * (0.5 + 0.5 * math.cos(3 * a))
            co.y *= 1 - 0.45 * k * (0.5 + 0.5 * math.cos(3 * a))
            co.z -= 0.04 * k * math.sin(2 * a)
        return co
    p.lathe([(0, 0), (0.14, 0), (0.175, 0.04), (0.175, 0.2), (0.17, 0.3), (0.175, 0.4), (0.175, 0.53), (0.13, 0.58),
             (0.13, 0.6), (0, 0.6)], segs=12, c="red", deform=crush, rot=(6, 0, 0))
    p.box(0.08, 0.12, 0.02, at=(0.03, 0.04, 0.6), rot=(6, 0, 20), c="alu", bev=0)
    return m


def gobelet():
    m = Model("gobelet", (0.3, 0.4, 0.3), CAT, "Gobelet")
    p = m.part("Gobelet")
    p.lathe([(0, 0), (0.11, 0), (0.115, 0.01), (0.15, 0.38), (0.15, 0.4), (0.135, 0.4), (0.105, 0.03), (0, 0.03)], segs=12,
            c="white", deform=m.noise(0.006, 1), cap0=False, cap1=False)
    p.lathe([(0.128, 0.12), (0.138, 0.12), (0.143, 0.26), (0.133, 0.26)], segs=12, c="cardboard", cap0=False, cap1=False)
    p.cyl(0.13, 0.01, at=(0, 0, 0.32), c="wood_dark", segs=10, bev=0)  # fond de café
    return m


def journal():
    m = Model("journal", (0.9, 0.1, 0.9), CAT, "Journal froissé")
    p = m.part("Journal")
    nz = m.noise(0.02, 31)
    p.box(0.85, 0.85, 0.02, at=(0, 0, 0.02), rot=(0, 0, 8), c="paper", bev=0, deform=nz)
    p.box(0.6, 0.7, 0.02, at=(0.12, -0.05, 0.05), rot=(6, -8, -14), c="paper_dirty", bev=0, deform=m.noise(0.025, 32))
    p.box(0.45, 0.5, 0.02, at=(-0.15, 0.15, 0.075), rot=(-10, 12, 30), c="paper", bev=0, deform=m.noise(0.02, 33))
    for (x, y, w, h) in ((-0.2, -0.2, 0.25, 0.18), (0.18, 0.2, 0.2, 0.25)):  # photos (aplats sans texte)
        p.box(w, h, 0.01, at=(x, y, 0.035), rot=(0, 0, 8), c="grey", bev=0)
    return m


def pigeon():
    m = Model("pigeon", (0.6, 0.8, 1), CAT, "Pigeon")
    p = m.part("Pigeon")
    p.sphere(0.3, at=(0, 0.05, 0.38), c="pigeon", scale=(0.95, 1.15, 0.9), segs=10, rings=7, rot=(-12, 0, 0))
    p.sphere(0.2, at=(0, -0.22, 0.48), c="pigeon_neck", scale=(1, 1, 1.1), segs=8, rings=6)
    p.sphere(0.15, at=(0, -0.33, 0.66), c="pigeon_dark", segs=8, rings=6)
    p.lathe([(0, 0), (0.035, 0), (0, 0.13)], segs=6, at=(0, -0.46, 0.65), rot=(95, 0, 0), c="beak")
    for s in (-1, 1):
        p.sphere(0.03, at=(s * 0.1, -0.42, 0.7), c="flame_orange", segs=6, rings=4)
        p.sphere(0.25, at=(s * 0.22, 0.12, 0.42), c="pigeon_dark", scale=(0.25, 1.2, 0.7), segs=7, rings=5, rot=(-15, 0, 0))
        for k in (0.0, 0.05):
            p.box(0.18, 0.04, 0.01, at=(s * 0.25, 0.1 + k * 2, 0.5), rot=(0, 0, 90), c="iron", bev=0)
        p.rod((s * 0.08, 0.0, 0.18), (s * 0.08, -0.02, 0.0), 0.025, c="rat_pink", sides=4)
        p.rod((s * 0.08, -0.02, 0.01), (s * 0.1, -0.14, 0.01), 0.02, c="rat_pink", sides=3)
    p.prism([(-0.12, 0), (0.12, 0), (0.09, 0.24), (-0.09, 0.24)], 0.04, at=(0, 0.33, 0.34), rot=(-78, 0, 0), plane="XZ", c="pigeon_dark")
    return m


def rat():
    m = Model("rat", (0.5, 0.4, 1.6), CAT, "Rat avec sa queue")
    p = m.part("Rat")
    p.sphere(0.25, at=(0, -0.05, 0.2), c="rat", scale=(1, 1.65, 0.8), segs=10, rings=7, deform=m.noise(0.015, 1))
    p.lathe([(0, 0), (0.15, 0.05), (0.13, 0.15), (0.05, 0.3), (0, 0.34)], segs=8, at=(0, -0.38, 0.22), rot=(95, 0, 0), c="rat")
    p.sphere(0.03, at=(0, -0.72, 0.2), c="rat_pink", segs=6, rings=4)
    for s in (-1, 1):
        p.cyl(0.07, 0.025, at=(s * 0.1, -0.45, 0.33), rot=(70, 0, s * 20), c="rat_pink", segs=8, bev=0)
        p.sphere(0.03, at=(s * 0.09, -0.58, 0.29), c="eye", segs=6, rings=4)
        for y in (-0.3, 0.2):
            p.box(0.08, 0.12, 0.05, at=(s * 0.16, y, 0.025), c="rat_pink", bev=0.01)
        p.rod((s * 0.05, -0.69, 0.22), (s * 0.24, -0.74, 0.25), 0.006, c="grey_light", sides=3)
    tail = [(0, 0.32, 0.17), (0.04, 0.45, 0.1), (0.12, 0.6, 0.05), (0.18, 0.72, 0.04), (0.15, 0.82, 0.05), (0.05, 0.86, 0.06)]
    p.pipe(tail, 0.035, c="rat_pink", sides=5)
    return m


MODELS = [
    ("22a_carton_ouvert", carton_ouvert), ("22b_carton_aplati", carton_aplati), ("23_matelas", matelas), ("24_pneu", pneu),
    ("25_caddie", caddie), ("26_tente_fortune", _tente), ("27_sac_couchage", sac_couchage), ("28_bouteille", bouteille),
    ("29_canette", canette), ("30_gobelet", gobelet), ("31_journal", journal), ("32_pigeon", pigeon), ("33_rat", rat),
]
