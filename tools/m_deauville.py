"""121–166 : Deauville, station balnéaire chic (même style low-poly, couleurs propres, aucun logo)."""
import math
import random

from mathutils import Vector

from lib import Model
from m_quete import stroke
from m_vehicules import cabin, wheel

CAT = "10_deauville"
WHITE, CREAM, GREEN, SLATE, NAVY = "white", "cream", "pole_green", "steel_blue", "navy_paint"


def M(name, dims, title, note=""):
    m = Model(name, dims, CAT, title, None, note)
    m.grime = False
    return m


# ---------------------------------------------------------------------------
# Briques d'architecture
# ---------------------------------------------------------------------------

def window(pw, pg, cx, cz, w, h, face, coord, frame=WHITE, shutters=None):
    """Fenêtre sur une face : '-y', '+y', '-x', '+x' ; coord = position de la face."""
    s = -1 if face[0] == "-" else 1
    if face[1] == "y":
        pw.box(w + 0.3, 0.14, h + 0.3, at=(cx, coord + s * 0.05, cz), c=frame, bev=0)
        pg.box(w, 0.1, h, at=(cx, coord + s * 0.1, cz), c="glass", bev=0)
        pw.box(0.08, 0.13, h, at=(cx, coord + s * 0.13, cz), c=frame, bev=0)
        if shutters:
            for k in (-1, 1):
                pw.box(w * 0.5, 0.08, h + 0.1, at=(cx + k * (w * 0.75 + 0.15), coord + s * 0.06, cz), c=shutters, bev=0)
    else:
        pw.box(0.14, w + 0.3, h + 0.3, at=(coord + s * 0.05, cx, cz), c=frame, bev=0)
        pg.box(0.1, w, h, at=(coord + s * 0.1, cx, cz), c="glass", bev=0)
        pw.box(0.13, 0.08, h, at=(coord + s * 0.13, cx, cz), c=frame, bev=0)
        if shutters:
            for k in (-1, 1):
                pw.box(0.08, w * 0.5, h + 0.1, at=(coord + s * 0.06, cx + k * (w * 0.75 + 0.15), cz), c=shutters, bev=0)


def windows_row(pw, pg, x0, x1, n, cz, w, h, face, coord, **kw):
    for i in range(n):
        cx = x0 + (x1 - x0) * (i + 0.5) / n
        window(pw, pg, cx, cz, w, h, face, coord, **kw)


def colombage(p, x0, x1, z0, z1, face, coord, step=1.6, c=GREEN, t=0.22, diag=True):
    """Pans de bois en relief sur une face (vert sapin)."""
    s = -1 if face[0] == "-" else 1
    def bx(a0, a1, zz0, zz1):
        if face[1] == "y":
            p.rod((a0, coord + s * 0.06, zz0), (a1, coord + s * 0.06, zz1), t / 2, c=c, sides=4)
        else:
            p.rod((coord + s * 0.06, a0, zz0), (coord + s * 0.06, a1, zz1), t / 2, c=c, sides=4)
    n = max(1, round((x1 - x0) / step))
    for i in range(n + 1):
        a = x0 + (x1 - x0) * i / n
        bx(a, a, z0, z1)
    for z in (z0, (z0 + z1) / 2, z1):
        bx(x0, x1, z, z)
    if diag:
        for i in range(n):
            a, b = x0 + (x1 - x0) * i / n, x0 + (x1 - x0) * (i + 1) / n
            if i % 2 == 0:
                bx(a, b, z0, (z0 + z1) / 2)
            else:
                bx(a, b, (z0 + z1) / 2, z0)


def gable(p, x, y, z, w, d, h, c=SLATE, ridge="x", over=0.5):
    """Toit à deux pans ; ridge = axe du faîtage."""
    if ridge == "x":
        p.prism([(-d / 2 - over, 0), (d / 2 + over, 0), (0, h)], w + 2 * over * 0.6, at=(x, y, z), c=c, plane="YZ", bev=0.05)
    else:
        p.prism([(-w / 2 - over, 0), (w / 2 + over, 0), (0, h)], d + 2 * over * 0.6, at=(x, y, z), c=c, plane="XZ", bev=0.05)


def pyramid(p, x, y, z, w, d, h, c=SLATE, over=0.4):
    k = 1 / math.sqrt(2)
    p.lathe([(0, 0), (1, 0), (0, h)], segs=4, phase=math.pi / 4, at=(x, y, z), sx=(w / 2 + over) / k, sy=(d / 2 + over) / k, c=c)


def turret(pw, pr, x, y, z, r, h, rh, wall=WHITE, roof=SLATE):
    pw.cyl(r, h, at=(x, y, z), c=wall, segs=10, bev=0.05)
    pr.lathe([(0, 0), (r + 0.35, 0), (0.05, rh), (0, rh)], segs=10, at=(x, y, z + h), c=roof)
    pr.cyl(0.05, 0.6, at=(x, y, z + h + rh - 0.05), c="gold", segs=4, bev=0)


def awning(p, x, y, z, w, depth, n=8, c1=NAVY, c2=WHITE, ang=25):
    for i in range(n):
        cx = x - w / 2 + w * (i + 0.5) / n
        p.box(w / n, depth, 0.08, at=(cx, y - depth / 2 * math.cos(math.radians(ang)), z - depth / 2 * math.sin(math.radians(ang))),
              rot=(ang, 0, 0), c=(c1 if i % 2 == 0 else c2), bev=0)
        p.prism([(-w / n / 2, 0), (w / n / 2, 0), (0, -0.35)], 0.05, at=(cx, y - depth * math.cos(math.radians(ang)),
                 z - depth * math.sin(math.radians(ang))), c=(c1 if i % 2 == 0 else c2))


def statue(p, x, y, z, s=1.0, c="marble"):
    p.boxb(0.9 * s, 0.9 * s, 0.6 * s, x, y, z, c=c, bev=0.05)
    p.cyl(0.25 * s, 1.1 * s, at=(x, y, z + 0.6 * s), r2=0.18 * s, c=c, segs=8)
    p.sphere(0.2 * s, at=(x, y, z + 1.9 * s), c=c, segs=8, rings=5)
    p.rod((x, y, z + 1.55 * s), (x + 0.4 * s, y - 0.1, z + 2.0 * s), 0.07 * s, c=c, sides=5)


# ---------------------------------------------------------------------------
# Monuments
# ---------------------------------------------------------------------------

def casino():
    m = M("casino_deauville", (60, 24, 30), "Casino", "Façade Belle Époque, coupoles, statues")
    f, v, co, e = m.part("Facade"), m.part("Vitres"), m.part("Coupoles"), m.part("Entree")
    f.boxb(60, 26, 1.2, 0, 2, 0, c="marble", bev=0.2)
    f.boxb(56, 22, 14, 0, 3, 1.2, c=WHITE, bev=0.3)
    f.boxb(57, 23, 0.8, 0, 3, 8.0, c=CREAM, bev=0.15)
    f.boxb(57.5, 23.5, 1.0, 0, 3, 15.2, c=CREAM, bev=0.2)
    for x in (-24, -12, 12, 24):  # pavillons en avancée
        f.boxb(7, 2, 15.5, x, -8.8, 1.2, c=WHITE, bev=0.2)
        f.boxb(7.6, 2.6, 0.8, x, -8.8, 16.2, c=CREAM, bev=0.1)
    for k in range(-11, 12):  # balustrade du toit
        f.cyl(0.18, 1.0, at=(k * 2.4, -7.85, 16.2), c=WHITE, segs=6, bev=0)
    f.boxb(56, 0.4, 0.3, 0, -7.85, 17.2, c=WHITE, bev=0.05)
    for z, h in ((2.4, 4.8), (9.2, 4.6)):
        for x0, x1, n in ((-27, -20.5, 2), (-20.5, -15.5, 1), (-8.5, 8.5, 5), (15.5, 20.5, 1), (20.5, 27, 2)):
            windows_row(f, v, x0, x1, n, z + h / 2, 2.0 if z < 5 else 1.8, h, "-y", -7.9)
    for x in (-24, -12, 12, 24):
        for z in (4.6, 11.4):
            window(f, v, x, z, 2.6, 4.4 if z < 6 else 4.0, "-y", -9.8)
    # entrée centrale à colonnes et marquise
    for x in (-6, -3, 3, 6):
        e.cyl(0.45, 7.8, at=(x, -10.5, 1.2), c="marble", segs=10, bev=0.08)
    e.boxb(14, 4, 0.9, 0, -9.2, 9.0, c=WHITE, bev=0.15)
    e.prism([(-7.5, 0), (7.5, 0), (0, 3.2)], 4.0, at=(0, -9.2, 9.9), c=WHITE, bev=0.1)  # fronton
    e.boxb(10, 5, 0.3, 0, -13, 7.8, c="gold", bev=0.05)  # marquise
    for x in (-4.6, 4.6):
        e.rod((x, -15.3, 7.8), (x, -9.5, 9.5), 0.08, c="gold", sides=5)
    for i, x in enumerate((-4, -1.3, 1.3, 4)):
        e.boxb(2.2, 0.2, 5, x, -9.0, 1.2, c="gold" if i in (1, 2) else "wood_dark", bev=0.05)
    for k in range(3):
        e.boxb(16 - k * 1.2, 1.2, 0.4, 0, -14.6 + k * 1.2, k * 0.4, c="marble", bev=0.05)
    e.boxb(14, 6, 0.05, 0, -12, 1.2, c="red", bev=0)  # tapis rouge
    # coupoles et statues
    for x, r in ((0, 4.5), (-24, 2.6), (24, 2.6)):
        y = 3 if x == 0 else -8.8
        co.cyl(r * 0.9, 1.6, at=(x, y, 16.2), c=WHITE, segs=12, bev=0.1)
        co.sphere(r, at=(x, y, 17.8), c=SLATE, segs=14, rings=8, scale=(1, 1, 1.15),
                  deform=lambda co_: Vector((co_.x, co_.y, max(co_.z, 0))))
        co.lathe([(0, 0), (0.6, 0), (0.3, 1.2), (0.1, 2.0), (0, 2.2)], segs=8, at=(x, y, 17.8 + r * 1.12), c="gold")
    for x in (-12, 12):
        statue(co, x, -8.8, 16.9, 1.6, c=WHITE)
    for x in (-28, 28):
        co.boxb(2, 2, 3, x, 13.5, 16.2, c=CREAM, bev=0.1)
    return m


def hotel_normand(name, dims, title, n_gables=4, roof=SLATE):
    W, H, D = dims
    m = M(name, dims, title, "Style anglo-normand, colombages vert sapin")
    mu, co, to, v = m.part("Murs"), m.part("Colombages"), m.part("Toits"), m.part("Vitres")
    wall_h = H * 0.55
    mu.boxb(W - 2, D - 6, 1.0, 0, 0, 0, c="marble", bev=0.1)
    mu.boxb(W - 3, D - 7, wall_h, 0, 0, 1.0, c=WHITE, bev=0.2)
    yf, yb = -(D - 7) / 2, (D - 7) / 2
    floors = 3
    fh = (wall_h - 1) / floors
    for k in range(floors):
        z0 = 1.0 + k * fh
        windows_row(mu, v, -W / 2 + 2.5, W / 2 - 2.5, int(W / 5), z0 + fh * 0.55, 1.6, fh * 0.5, "-y", yf, shutters=None)
        if k > 0:
            colombage(co, -W / 2 + 1.6, W / 2 - 1.6, z0 - 0.1, z0 + fh - 0.2, "-y", yf, step=2.5)
    gable(to, 0, 0, wall_h + 1.0, W - 3, D - 7, H - wall_h - 1.5, c=roof, ridge="x", over=1.0)
    gw = (W - 6) / n_gables
    for i in range(n_gables):  # pignons pointus en façade
        x = -W / 2 + 3 + gw * (i + 0.5)
        mu.prism([(-gw * 0.38, 0), (gw * 0.38, 0), (0, gw * 0.55)], 1.2, at=(x, yf - 0.4, wall_h + 1.0), c=WHITE)
        colombage(co, x - gw * 0.3, x + gw * 0.3, wall_h + 1.0, wall_h + 1.0 + gw * 0.35, "-y", yf - 1.0, step=1.2, diag=False)
        to.prism([(-gw * 0.45, 0), (gw * 0.45, 0), (0, gw * 0.62)], 3.0, at=(x, yf + 0.6, wall_h + 0.9), c=roof, bev=0.05)
        window(mu, v, x, wall_h + 2.3, 1.4, 1.6, "-y", yf - 1.0)
    for x in (-W / 2 + 6, 0, W / 2 - 6):  # cheminées
        mu.boxb(1.2, 1.2, 4.0, x, 2, H - 4.5, c="brick", bev=0.08)
    mu.boxb(5, 2.5, 3.5, 0, yf - 1.2, 1.0, c=WHITE, bev=0.1)  # porche
    mu.boxb(6, 3.2, 0.4, 0, yf - 1.4, 4.5, c=GREEN, bev=0.05)
    return m


def hotel_royal():
    m = M("hotel_royal", (70, 28, 25), "Hôtel Royal", "Palace blanc, toits d'ardoise bleue")
    mu, to, v, ba = m.part("Murs"), m.part("Toits"), m.part("Vitres"), m.part("Balcons")
    mu.boxb(68, 18, 1.0, 0, 0, 0, c="marble", bev=0.1)
    mu.boxb(66, 16, 18, 0, 0, 1.0, c=WHITE, bev=0.2)
    for x in (-28, 0, 28):
        mu.boxb(10, 2, 19, x, -8.6, 0.5, c=WHITE, bev=0.15)
    for k in range(5):
        z = 1.0 + k * 3.5
        mu.boxb(66.5, 16.5, 0.25, 0, 0, z, c=CREAM, bev=0)
        windows_row(mu, v, -32, 32, 16, z + 1.8, 1.6, 2.2, "-y", -8.0)
        if k > 0:
            for i in range(11):
                x = -30 + i * 6
                ba.boxb(3.4, 1.2, 0.2, x, -8.6, z, c=WHITE, bev=0)
                ba.boxb(3.4, 0.12, 0.9, x, -9.15, z + 0.2, c=WHITE, bev=0)
    pyramid(to, 0, 0, 19, 66, 16, 6, over=0.8)
    for x in (-28, 0, 28):
        pyramid(to, x, -4, 19.5, 11, 9, 8.5, over=0.4)
        to.cyl(0.1, 1.2, at=(x, -4, 27.9), c="gold", segs=4, bev=0)
        for k in (-1, 1):  # lucarnes
            mu.boxb(1.6, 1.4, 1.8, x + k * 3, -8.5, 20.0, c=WHITE, bev=0.05)
            v.boxb(1.0, 0.1, 1.0, x + k * 3, -9.25, 20.3, c="glass", bev=0)
    mu.boxb(8, 4, 0.4, 0, -11, 4.5, c=NAVY, bev=0.05)  # marquise
    for x in (-3.5, 3.5):
        mu.cyl(0.15, 3.5, at=(x, -12.6, 1.0), c="gold", segs=6, bev=0)
    return m


def bains():
    m = M("bains_pompeiens", (40, 8, 12), "Bains Pompéiens", "Colonnade, mosaïques bleu et or")
    c, mo, t = m.part("Colonnes"), m.part("Mosaiques"), m.part("Toit")
    c.boxb(40, 12, 0.6, 0, 0, 0, c="marble", bev=0.1)
    for i in range(14):
        x = -18.5 + i * (37 / 13)
        c.cyl(0.4, 5.6, at=(x, -4.8, 0.6), c=WHITE, segs=10, bev=0.06)
        c.cyl(0.55, 0.3, at=(x, -4.8, 0.6), c=CREAM, segs=10, bev=0.04)
        c.cyl(0.55, 0.3, at=(x, -4.8, 5.9), c="gold", segs=10, bev=0.04)
    c.boxb(39, 3, 6.0, 0, 3.8, 0.6, c=WHITE, bev=0.1)  # mur du fond
    t.boxb(40, 12, 1.0, 0, 0, 6.2, c=WHITE, bev=0.15)
    t.boxb(40.5, 12.5, 0.6, 0, 0, 7.2, c=CREAM, bev=0.1)
    t.boxb(40, 0.3, 0.6, 0, -6.1, 6.4, c="gold", bev=0.03)
    rng = random.Random(3)
    for i in range(12):  # panneaux de mosaïques
        x = -17 + i * 3.1
        mo.boxb(2.6, 0.08, 4.0, x, 2.25, 1.2, c="blue", bev=0)
        mo.boxb(2.2, 0.1, 0.3, x, 2.22, 4.5, c="gold", bev=0)
        for k in range(6):
            mo.boxb(0.35, 0.1, 0.35, x - 0.8 + (k % 3) * 0.8, 2.21, 1.8 + (k // 3) * 1.4, c=rng.choice(["gold", "sky", "white"]), bev=0)
    mo.boxb(39, 0.1, 0.4, 0, -6.15, 6.5, c="blue", bev=0)
    for k in range(18):
        mo.boxb(0.5, 0.11, 0.25, -17 + k * 2, -6.16, 6.57, c="gold", bev=0)
    return m


def bar_soleil():
    m = M("bar_du_soleil", (16, 7, 10), "Bar du Soleil", "Pavillon de plage et terrasse")
    p, t, e = m.part("Pavillon"), m.part("Terrasse"), m.part("Enseigne")
    t.boxb(16, 10, 0.5, 0, 0, 0, c="wood_light", bev=0.05)
    for i in range(16):
        t.boxb(0.05, 10, 0.02, -7.5 + i, 0, 0.5, c="wood", bev=0)
    p.boxb(8, 4, 4.5, 2.5, 2.5, 0.5, c=WHITE, bev=0.1)
    for i in range(8):
        p.boxb(0.5, 4.05, 4.5, -1.25 + i * 1.0, 2.5, 0.5, c=(NAVY if i % 2 else WHITE), bev=0)  # bardage rayé
    p.boxb(6, 0.2, 2.0, 2.5, 0.45, 2.0, c="glass", bev=0)
    p.boxb(9, 5, 0.4, 2.5, 2.5, 5.0, c=WHITE, bev=0.08)
    gable(p, 2.5, 2.5, 5.4, 8, 4, 1.4, c="wood_light", ridge="x", over=0.6)
    awning(p, 2.5, 0.4, 4.6, 8, 2.0, n=8, c1="yellow", c2=WHITE)
    for x in (-6, -3):
        for y in (-3, 0):
            t.cyl(0.45, 0.08, at=(x, y, 1.6), c=WHITE, segs=10, bev=0)
            t.cyl(0.06, 1.1, at=(x, y, 0.5), c=WHITE, segs=6, bev=0)
            t.cyl(0.05, 3.5, at=(x, y, 1.6), c=WHITE, segs=6, bev=0)
            t.lathe([(0, 0), (1.4, 0), (0, 0.6)], segs=8, at=(x, y, 4.6), c=("yellow" if (x + y) % 2 else "red"))
    for x in (-8, 8):
        t.boxb(0.15, 10, 1.0, x - 0 * 0.0 + (0.075 if x < 0 else -0.075), 0, 0.5, c=WHITE, bev=0.02)  # garde-corps
    e.boxb(5, 0.25, 1.2, 2.5, 0.3, 5.5, c="yellow", bev=0.06)
    e.cyl(0.4, 0.1, at=(4.3, 0.15, 6.1), rot=(90, 0, 0), c="flame_yellow", segs=12, bev=0.02)  # soleil stylisé
    return m


def gare():
    m = M("gare_trouville_deauville", (40, 16, 14), "Gare de Trouville-Deauville", "Colombages, horloge centrale")
    b, h, v = m.part("Batiment"), m.part("Horloge"), m.part("Vitres")
    b.boxb(40, 14, 0.6, 0, 0, 0, c="marble", bev=0.1)
    b.boxb(36, 10, 7, 0, 0, 0.6, c=WHITE, bev=0.15)
    b.boxb(12, 11, 10, 0, -0.5, 0.6, c=WHITE, bev=0.15)
    colombage(b, -17.5, -6.2, 4.0, 7.4, "-y", -5.0, step=2.0)
    colombage(b, 6.2, 17.5, 4.0, 7.4, "-y", -5.0, step=2.0)
    colombage(b, -5.6, 5.6, 6.5, 10.4, "-y", -6.0, step=1.8)
    windows_row(b, v, -17.5, -6.5, 4, 2.3, 1.6, 2.4, "-y", -5.0)
    windows_row(b, v, 6.5, 17.5, 4, 2.3, 1.6, 2.4, "-y", -5.0)
    for x in (-3.5, 0, 3.5):
        b.boxb(2.4, 0.3, 4.0, x, -6.1, 0.6, c="wood", bev=0.04)
        v.boxb(2.0, 0.2, 1.4, x, -6.25, 4.8, c="glass", bev=0)
    gable(b, 0, 0, 7.6, 36, 10, 3.5, ridge="x", over=0.6)
    gable(b, 0, -0.5, 10.6, 12, 11, 4.5, ridge="y", over=0.6)
    b.boxb(38, 4, 0.3, 0, -7, 4.0, c=GREEN, bev=0.05)  # auvent de quai
    for x in range(-18, 19, 6):
        b.cyl(0.12, 3.4, at=(x, -8.6, 0.6), c=GREEN, segs=6, bev=0)
    h.cyl(1.4, 0.3, at=(0, -6.2, 12.2), rot=(90, 0, 0), c="gold", segs=16, bev=0.05)
    h.cyl(1.2, 0.1, at=(0, -6.45, 12.2), rot=(90, 0, 0), c=WHITE, segs=16, bev=0)
    h.box(0.12, 0.05, 0.9, at=(0.2, -6.56, 12.5), rot=(0, 25, 0), c="black", bev=0)
    h.box(0.1, 0.05, 0.6, at=(-0.2, -6.56, 12.0), rot=(0, -60, 0), c="black", bev=0)
    return m


def marche_couvert():
    m = M("marche_couvert", (30, 10, 18), "Marché couvert à colombages")
    ha, t, e = m.part("Halle"), m.part("Toit"), m.part("Etals")
    ha.boxb(30, 18, 0.4, 0, 0, 0, c="marble", bev=0.05)
    for x in (-13.5, -9, -4.5, 0, 4.5, 9, 13.5):
        for y in (-8, 8):
            ha.boxb(0.6, 0.6, 5.2, x, y, 0.4, c=GREEN, bev=0.05)
        ha.boxb(0.4, 16, 0.5, x, 0, 5.1, c=GREEN, bev=0.03)
    for y in (-8, 8):
        ha.boxb(28, 0.5, 0.6, 0, y, 5.0, c=GREEN, bev=0.05)
        colombage(ha, -14, 14, 5.6, 6.6, "-y" if y < 0 else "+y", y - 0.3 if y < 0 else y + 0.3, step=2.0, diag=True)
        ha.boxb(29, 0.4, 1.1, 0, y, 5.55, c=WHITE, bev=0.02)
    gable(t, 0, 0, 6.6, 30, 16, 3.4, c=SLATE, ridge="x", over=1.2)
    t.boxb(8, 3, 1.2, 0, 0, 9.6, c=WHITE, bev=0.05)  # lanterneau
    gable(t, 0, 0, 10.8, 8, 3, 0.9, c=SLATE, ridge="x", over=0.3)
    cols = ["tomato", "lettuce", "flower_yellow", "flower_pink", "orange", "flower_purple"]
    for i, x in enumerate((-10, -3.5, 3.5, 10)):
        for y in (-4, 4):
            e.boxb(5, 2, 1.8, x, y, 0.4, c="wood_light", bev=0.05)
            for k in range(6):
                e.sphere(0.35, at=(x - 1.9 + k * 0.75, y, 2.45), c=cols[(i + k) % len(cols)], segs=6, rings=4, scale=(1, 1, 0.7))
            e.boxb(5.2, 2.4, 0.08, x, y, 3.8, c=("red" if (i + (y > 0)) % 2 else NAVY), bev=0)
            for sx in (-2.4, 2.4):
                e.cyl(0.05, 1.6, at=(x + sx, y, 2.2), c=WHITE, segs=4, bev=0)
    return m


def villa_strass():
    m = M("villa_strassburger", (26, 20, 20), "Villa Strassburger", "Manoir normand à tourelle")
    mu, co, tu, to = m.part("Murs"), m.part("Colombages"), m.part("Tourelle"), m.part("Toits")
    v = mu
    mu.boxb(18, 16, 0.6, -2, 0, 0, c="marble", bev=0.05)
    mu.boxb(17, 15, 4.0, -2, 0, 0.6, c="brick", bev=0.1)  # soubassement en briques
    mu.boxb(17, 15, 6.0, -2, 0, 4.6, c=CREAM, bev=0.1)
    colombage(co, -10.4, 6.4, 4.7, 10.5, "-y", -7.5, step=1.4)
    colombage(co, -10.4, 6.4, 4.7, 10.5, "+y", 7.5, step=1.4)
    colombage(co, -7.4, 7.4, 4.7, 10.5, "-x", -10.5, step=1.4)
    for x in (-8, -4.5, 2.5):
        window(mu, v, x, 2.4, 1.6, 2.2, "-y", -7.5)
        window(mu, v, x, 7.6, 1.4, 1.8, "-y", -7.5, frame=GREEN)
    gable(to, -2, 0, 10.6, 17, 15, 6.5, c="brick_dark", ridge="x", over=0.8)
    for x in (-7, 1):
        mu.prism([(-2, 0), (2, 0), (0, 3.2)], 0.8, at=(x, -7.7, 10.6), c=CREAM)
        colombage(co, x - 1.4, x + 1.4, 10.7, 12.4, "-y", -8.1, step=0.9, diag=False)
        to.prism([(-2.5, 0), (2.5, 0), (0, 3.8)], 3.0, at=(x, -6.6, 10.5), c="brick_dark", bev=0.05)
    mu.boxb(1.2, 1.2, 4.0, -6, 2, 14.5, c="brick", bev=0.05)
    turret(tu, tu, 9.0, -3.5, 0.6, 2.8, 12.5, 6.5, wall=CREAM, roof="brick_dark")
    colombage(tu, 7.2, 10.8, 5.0, 12.5, "-y", -6.2, step=0.9)
    for z in (3.0, 7.0, 10.5):
        window(tu, tu, 9.0, z, 1.0, 1.4, "-y", -6.25)
    mu.boxb(4, 2.5, 3.2, -2, -8.5, 0.6, c=CREAM, bev=0.05)  # perron
    mu.boxb(4.8, 3.2, 0.3, -2, -8.6, 3.8, c=GREEN, bev=0.04)
    return m


def eglise():
    m = M("eglise_notre_dame_victoires", (20, 30, 30), "Église Notre-Dame-des-Victoires")
    n, cl, vi = m.part("Nef"), m.part("Clocher"), m.part("Vitraux")
    n.boxb(18, 26, 0.6, 0, 1, 0, c="marble", bev=0.05)
    n.boxb(16, 24, 10, 0, 2, 0.6, c=CREAM, bev=0.15)
    gable(n, 0, 2, 10.6, 16, 24, 7.0, c=SLATE, ridge="y", over=0.6)
    for y in (-6, -1, 4, 9):
        for x in (-8.0, 8.0):
            n.boxb(1.0, 1.0, 9.0, x * 1.04, y + 2.5, 0.6, c=CREAM, bev=0.05)  # contreforts
    cols = ["blue", "red", "flower_yellow", "green"]
    for i, y in enumerate((-5, 0, 5, 10)):
        for s in (-1, 1):
            arch = [(-0.8, 0), (0.8, 0)] + [(0.8 * math.cos(math.radians(a)), 3.0 + 0.8 * math.sin(math.radians(a))) for a in range(0, 181, 30)]
            vi.prism([(y + x, z) for x, z in arch], 0.12, at=(s * 8.05, 0, 3.5), plane="YZ", c=cols[(i + (s > 0)) % 4])
    cl.boxb(6, 6, 16, 0, -12, 0.6, c=CREAM, bev=0.12)
    cl.boxb(6.6, 6.6, 0.6, 0, -12, 16.6, c=WHITE, bev=0.08)
    for x in (-1.5, 1.5):
        cl.boxb(1.0, 0.2, 2.6, x, -15.05, 12.5, c="black", bev=0.02)  # abat-sons
    cl.lathe([(0, 0), (3.2, 0), (0.1, 11.5), (0, 11.5)], segs=8, phase=math.pi / 8, at=(0, -12, 17.2), c=SLATE)
    cl.rod((0, -12, 28.5), (0, -12, 30.0), 0.1, c="gold", sides=4)
    cl.rod((-0.5, -12, 29.4), (0.5, -12, 29.4), 0.08, c="gold", sides=4)
    rose = [(1.6 * math.cos(math.radians(a)), 8.0 + 1.6 * math.sin(math.radians(a))) for a in range(0, 360, 30)]
    vi.prism(rose, 0.12, at=(0, -15.06, 0), c="blue")
    for i in range(6):
        a = math.radians(i * 60)
        vi.prism([(0, 8.0), (1.4 * math.cos(a - 0.3), 8.0 + 1.4 * math.sin(a - 0.3)), (1.4 * math.cos(a + 0.3), 8.0 + 1.4 * math.sin(a + 0.3))],
                 0.13, at=(0, -15.07, 0), c=("red" if i % 2 else "flower_yellow"))
    n.boxb(3, 0.4, 4.5, 0, -15.1, 0.6, c="wood_dark", bev=0.05)  # portail
    return m


def tribune():
    m = M("tribune_hippodrome", (50, 14, 14), "Tribune de l'hippodrome")
    tr, to, g = m.part("Tribune"), m.part("Toit"), m.part("Gradins")
    tr.boxb(50, 6, 4.0, 0, 4, 0, c=WHITE, bev=0.15)
    windows_row(tr, tr, -23, 23, 12, 2.0, 2.4, 2.4, "-y", 1.0, frame=GREEN)
    for k in range(7):
        g.boxb(48, 1.2, 0.6, 0, -5.5 + k * 1.3, 4.0 + k * 0.7, c=(WHITE if k % 2 == 0 else "grey_light"), bev=0.05)
        for i in range(12):
            g.boxb(3.4, 0.5, 0.4, -22 + i * 4, -5.6 + k * 1.3, 4.6 + k * 0.7, c=("red" if k % 2 else NAVY), bev=0)
    tr.boxb(50, 2, 9, 0, 6, 4.0, c=WHITE, bev=0.1)
    for x in range(-24, 25, 8):
        tr.cyl(0.25, 9.5, at=(x, -6.2, 0), c=WHITE, segs=8, bev=0)
        to.rod((x, -6.2, 9.5), (x, 6.8, 13.0), 0.2, c=WHITE, sides=5)
    to.box(51, 15, 0.4, at=(0, 0.3, 11.4), rot=(-15, 0, 0), c=GREEN, bev=0.1)
    awning(to, 0, -6.8, 9.7, 50, 1.2, n=25, c1=GREEN, c2=WHITE, ang=60)
    for x in (-24, 0, 24):
        to.cyl(0.08, 2.0, at=(x, 4, 12.6), c=WHITE, segs=4, bev=0)
        to.prism([(0, 0), (1.4, -0.2), (1.2, 0.4), (1.4, 0.8), (0, 0.7)], 0.03, at=(x, 4, 13.6), c=("red" if x else NAVY))
    return m


# ---------------------------------------------------------------------------
# Bâtiments réutilisables
# ---------------------------------------------------------------------------

def villa_a():
    m = M("villa_anglo_normande_a", (16, 16, 14), "Villa anglo-normande A", "2 étages, colombages")
    mu, co, to, v = m.part("Murs"), m.part("Colombages"), m.part("Toit"), m.part("Vitres")
    mu.boxb(14, 12, 0.5, 0, 0, 0, c="marble", bev=0.05)
    mu.boxb(13, 11, 4.0, 0, 0, 0.5, c=WHITE, bev=0.1)
    mu.boxb(13, 11, 4.0, 0, 0, 4.5, c=CREAM, bev=0.1)
    for face, coord, a0, a1 in (("-y", -5.5, -6.5, 6.5), ("+y", 5.5, -6.5, 6.5), ("-x", -6.5, -5.5, 5.5), ("+x", 6.5, -5.5, 5.5)):
        colombage(co, a0 + 0.2, a1 - 0.2, 4.6, 8.4, face, coord, step=1.3)
    for x in (-4, 0, 4):
        window(mu, v, x, 2.5, 1.4, 2.0, "-y", -5.5, shutters=GREEN)
        window(mu, v, x, 6.4, 1.2, 1.6, "-y", -5.5)
    for y in (-2.5, 2.5):
        window(mu, v, y, 2.5, 1.4, 2.0, "+x", 6.5, shutters=GREEN)
    gable(to, 0, 0, 8.5, 13, 11, 5.5, ridge="x", over=0.8)
    mu.prism([(-2.6, 0), (2.6, 0), (0, 3.6)], 0.8, at=(-2.5, -5.8, 8.5), c=CREAM)
    colombage(co, -4.3, -0.7, 8.6, 10.6, "-y", -6.2, step=0.9, diag=False)
    to.prism([(-3.2, 0), (3.2, 0), (0, 4.2)], 2.5, at=(-2.5, -4.8, 8.4), c=SLATE, bev=0.05)
    mu.boxb(1.0, 1.0, 3.0, 3.5, 2, 12.0, c="brick", bev=0.05)
    mu.boxb(1.6, 0.25, 2.8, 4.5, -5.6, 0.5, c=GREEN, bev=0.04)  # porte
    return m


def villa_b():
    m = M("villa_anglo_normande_b", (16, 18, 14), "Villa anglo-normande B", "Tourelle, toit de tuiles")
    mu, tu, to, v = m.part("Murs"), m.part("Tourelle"), m.part("Toit"), m.part("Vitres")
    mu.boxb(12, 12, 0.5, -2, 0, 0, c="marble", bev=0.05)
    mu.boxb(11, 11, 8.0, -2, 0, 0.5, c=WHITE, bev=0.1)
    colombage(mu, -7.3, 3.3, 4.6, 8.3, "-y", -5.5, step=1.3, c="wood_dark")
    for x in (-5, -2, 1):
        window(mu, v, x, 2.5, 1.3, 2.0, "-y", -5.5, shutters=NAVY)
        window(mu, v, x, 6.4, 1.1, 1.5, "-y", -5.5)
    gable(to, -2, 0, 8.5, 11, 11, 5.5, c="brick", ridge="y", over=0.8)
    turret(tu, tu, 5.0, -2.5, 0.5, 2.3, 11.0, 6.3, wall=WHITE, roof="brick")
    for z in (2.5, 6.5, 9.8):
        window(tu, v, 5.0, z, 0.9, 1.4, "-y", -4.75)
    mu.boxb(1.6, 0.25, 2.8, -2, -5.6, 0.5, c="wood_dark", bev=0.04)
    mu.boxb(4, 2, 0.25, -2, -6.4, 3.4, c="brick", bev=0.03)
    return m


def boutique_luxe():
    m = M("immeuble_boutique_luxe", (14, 18, 12), "Immeuble à boutique de luxe", "Sans marque ; enseigne vierge")
    mu, vi, au, en = m.part("Murs"), m.part("Vitrine"), m.part("Auvent"), m.part("Enseigne")
    mu.boxb(14, 12, 4.5, 0, 0, 0, c=NAVY, bev=0.1)
    mu.boxb(13.6, 11.6, 11, 0, 0, 4.5, c=WHITE, bev=0.1)
    for k in range(3):
        z = 4.5 + k * 3.4
        windows_row(mu, mu, -6, 6, 4, z + 1.8, 1.4, 2.2, "-y", -5.8)
        for i in range(4):
            x = -6 + 12 * (i + 0.5) / 4
            mu.boxb(2.0, 0.6, 0.15, x, -6.0, z + 0.4, c=WHITE, bev=0.03)
            mu.boxb(2.0, 0.08, 0.6, x, -6.25, z + 0.55, c="black", bev=0)  # garde-corps en fer forgé
    pyramid(mu, 0, 0, 15.5, 13.6, 11.6, 2.4, c=SLATE, over=0.3)
    vi.boxb(5.0, 0.15, 3.2, -3.4, -6.05, 0.4, c="glass", bev=0)
    vi.boxb(5.0, 0.15, 3.2, 3.4, -6.05, 0.4, c="glass", bev=0)
    for x in (-3.4, 3.4):
        vi.boxb(3.0, 0.8, 0.6, x, -5.6, 0.4, c="gold", bev=0.05)
        vi.cyl(0.35, 1.0, at=(x - 0.6, -5.6, 1.0), c="white", segs=8, bev=0.05)  # présentoirs
    mu.boxb(1.6, 0.2, 3.4, 0, -6.05, 0.0, c="gold", bev=0.04)  # porte
    awning(au, 0, -6.1, 4.2, 14, 1.8, n=10, c1=NAVY, c2=WHITE)
    en.boxb(8, 0.2, 0.8, 0, -6.15, 4.4, c="gold", bev=0.04)
    return m


def residence():
    m = M("residence_balneaire", (14, 20, 12), "Résidence balnéaire", "Balcons blancs")
    mu, ba, v = m.part("Murs"), m.part("Balcons"), m.part("Vitres")
    mu.boxb(14, 12, 18, 0, 0, 0, c=CREAM, bev=0.15)
    for k in range(5):
        z = 0.5 + k * 3.4
        windows_row(mu, v, -6, 6, 3, z + 1.7, 2.2, 2.4, "-y", -6.0)
        if k > 0:
            ba.boxb(13, 1.6, 0.25, 0, -6.8, z, c=WHITE, bev=0.05)
            ba.box(13, 0.1, 1.0, at=(0, -7.55, z + 0.75), c=WHITE, bev=0.02)
            ba.boxb(13, 0.15, 0.12, 0, -7.55, z + 1.2, c=NAVY, bev=0)
    mu.boxb(14.4, 12.4, 0.6, 0, 0, 17.8, c=WHITE, bev=0.08)
    mu.boxb(4, 3, 1.4, 3, 1, 18.4, c=WHITE, bev=0.05)
    awning(mu, 0, -6.05, 3.4, 10, 1.4, n=8, c1="sky", c2=WHITE)
    return m


def brasserie():
    m = M("cafe_brasserie", (14, 10, 12), "Café-brasserie avec terrasse", "Enseigne vierge")
    mu, au, v, en = m.part("Murs"), m.part("Auvent"), m.part("Vitres"), m.part("Enseigne")
    mu.boxb(12, 8, 9.0, 0, 2, 0, c=WHITE, bev=0.1)
    mu.boxb(12.2, 8.2, 3.6, 0, 2, 0, c="wood_red", bev=0.1)
    pyramid(mu, 0, 2, 9.0, 12, 8, 1.2, c=SLATE, over=0.3)
    for x in (-3.8, 0, 3.8):
        v.boxb(3.0, 0.15, 2.6, x, -2.15, 0.6, c="glass", bev=0)
        window(mu, v, x, 6.0, 1.4, 2.0, "-y", -2.0, shutters=NAVY)
    awning(au, 0, -2.2, 4.0, 13, 2.6, n=10, c1="red", c2=WHITE)
    en.boxb(9, 0.2, 0.9, 0, -2.25, 4.3, c=NAVY, bev=0.05)
    for x in (-4.5, -1.5, 1.5, 4.5):  # terrasse
        mu.cyl(0.5, 0.07, at=(x, -4.0, 1.6), c="marble", segs=10, bev=0)
        mu.cyl(0.06, 1.6, at=(x, -4.0, 0.0), c="iron", segs=6, bev=0)
        for k in (-1, 1):
            mu.boxb(0.6, 0.6, 0.9, x + k * 0.9, -4.0, 0.0, c="wood_light", bev=0.05)
    return m


# ---------------------------------------------------------------------------
# Plage et Planches
# ---------------------------------------------------------------------------

def planches():
    m = M("module_planches", (8, 0.4, 4), "Module des Planches", "Promenade en bois, 8 studs")
    p = m.part("Planches")
    for i in range(16):
        p.boxb(0.46, 4.0, 0.25, -3.75 + i * 0.5, 0, 0.15, c=("wood_light" if i % 3 else "pallet"), bev=0.03)
    for y in (-1.6, 0, 1.6):
        p.boxb(8.0, 0.3, 0.15, 0, y, 0, c="wood", bev=0.02)
    return m


def cabine():
    m = M("cabine_plage", (3, 4.5, 3), "Cabine de plage", "Panneau de nom vierge")
    c, n = m.part("Cabine"), m.part("Nom")
    c.boxb(3, 3, 0.3, 0, 0, 0, c="wood_light", bev=0.04)
    c.boxb(2.6, 2.6, 3.2, 0, 0, 0.3, c=WHITE, bev=0.05)
    for i in range(5):
        c.boxb(0.3, 2.65, 3.2, -1.0 + i * 0.5, 0, 0.3, c=("blue" if i % 2 else WHITE), bev=0)
    gable(c, 0, 0, 3.5, 2.6, 2.6, 1.0, c=WHITE, ridge="y", over=0.2)
    c.boxb(1.4, 0.1, 2.4, 0, -1.32, 0.4, c="wood_light", bev=0.03)
    n.boxb(1.6, 0.08, 0.45, 0, -1.4, 3.0, c=WHITE, bev=0.02)
    return m


def parasol(open_=True):
    if open_:
        m = M("parasol_deauville_ouvert", (6, 6, 6), "Parasol de Deauville ouvert")
    else:
        m = M("parasol_deauville_ferme", (1, 6, 1), "Parasol de Deauville fermé")
    mt, t = m.part("Mat"), m.part("Toile")
    mt.cyl(0.08, 5.6, c="wood_light", segs=6, bev=0)
    mt.sphere(0.12, at=(0, 0, 5.8), c="wood_light", segs=6, rings=4)
    cols = ["red", "flower_yellow", "blue", "green", "orange", WHITE, "flower_pink", "teal"]
    if open_:
        for i in range(8):  # toile en quartiers multicolores (parasols de Deauville)
            a0, a1 = 2 * math.pi * i / 8, 2 * math.pi * (i + 1) / 8
            pts = [(0, 0, 5.6), (3.0 * math.cos(a0), 3.0 * math.sin(a0), 4.6), (3.0 * math.cos(a1), 3.0 * math.sin(a1), 4.6)]
            t.raw(pts + [(p[0], p[1], p[2] - 0.06) for p in pts], [(0, 1, 2), (3, 5, 4), (1, 4, 5, 2), (0, 3, 4, 1), (0, 2, 5, 3)], cols[i])
            t.prism([(-0.6, 0), (0.6, 0), (0, -0.3)], 0.03, at=(3.0 * math.cos((a0 + a1) / 2), 3.0 * math.sin((a0 + a1) / 2), 4.6),
                    rot=(0, 0, math.degrees((a0 + a1) / 2) + 90), c=cols[i])
    else:
        t.lathe([(0, 1.6), (0.32, 2.6), (0.36, 4.0), (0.2, 5.0), (0.08, 5.5), (0, 5.55)], segs=8, c="red")
        for z in (2.6, 4.0):
            t.torus(0.36, 0.04, at=(0, 0, z), c="flower_yellow", segs=8, sides=3)
    return m


def transat():
    m = M("transat", (2, 1.5, 5), "Transat", "Dossier côté +Z")
    p = m.part("Transat")
    for x in (-0.9, 0.9):
        p.rod((x, -2.4, 0.05), (x, 1.6, 1.45), 0.06, c="wood_light", sides=5)
        p.rod((x, 2.4, 0.05), (x, 0.3, 1.05), 0.06, c="wood_light", sides=5)
    p.rod((-0.9, -2.3, 0.1), (0.9, -2.3, 0.1), 0.05, c="wood_light", sides=5)
    p.rod((-0.9, 1.5, 1.42), (0.9, 1.5, 1.42), 0.05, c="wood_light", sides=5)
    ang = math.degrees(math.atan2(1.3, 3.8))
    for i in range(4):
        p.box(0.42, 3.9, 0.04, at=(-0.63 + i * 0.42, -0.4, 0.8), rot=(ang, 0, 0), c=("blue" if i % 2 == 0 else WHITE), bev=0)
    return m


def douche():
    m = M("douche_plage", (1.5, 7, 1.5), "Douche de plage")
    p = m.part("Douche")
    p.boxb(1.5, 1.5, 0.15, c="wood_light", bev=0.03)
    p.cyl(0.12, 6.4, at=(0, 0.4, 0.15), c="inox", segs=8, bev=0)
    p.pipe([(0, 0.4, 6.5), (0, 0.2, 6.8), (0, -0.4, 6.8)], 0.08, c="inox", sides=6)
    p.cyl(0.25, 0.1, at=(0, -0.45, 6.6), c="chrome", segs=10, bev=0.02)
    p.boxb(0.2, 0.2, 0.2, 0, 0.3, 3.5, c="blue", bev=0.04)
    return m


def poste_secours():
    m = M("poste_secours", (6, 10, 6), "Poste de secours sur pilotis")
    p, d = m.part("Poste"), m.part("Drapeau")
    for x in (-2, 2):
        for y in (-2, 2):
            p.boxb(0.3, 0.3, 4.0, x, y, 0, c=WHITE, bev=0.03)
    p.boxb(5, 5, 0.3, 0, 0, 4.0, c="wood_light", bev=0.04)
    p.boxb(4, 4, 2.8, 0, 0.3, 4.3, c=WHITE, bev=0.08)
    p.boxb(4.05, 4.05, 0.6, 0, 0.3, 5.5, c="red", bev=0)
    p.boxb(2.6, 0.1, 1.0, 0, -1.75, 5.0, c="glass", bev=0)
    pyramid(p, 0, 0.3, 7.1, 4, 4, 1.2, c="red", over=0.3)
    for i in range(8):
        p.boxb(0.6, 0.12, 0.08, 0, -2.3 - i * 0.0, 0.4 + i * 0.48, c="wood_light", bev=0, rot=(0, 0, 0))
    p.rod((-0.35, -2.4, 0), (-0.35, -2.4, 4.0), 0.05, c=WHITE, sides=4)
    p.rod((0.35, -2.4, 0), (0.35, -2.4, 4.0), 0.05, c=WHITE, sides=4)
    p.cyl(0.06, 1.8, at=(1.8, -1.8, 8.2), c=WHITE, segs=4, bev=0)
    p.rod((1.8, -1.8, 0), (1.8, -1.8, 8.3), 0.06, c=WHITE, sides=4)
    d.prism([(0, 0), (1.3, -0.1), (1.2, 0.4), (1.3, 0.8), (0, 0.7)], 0.03, at=(1.8, -1.8, 9.2), c="light_green")
    return m


def chateau_sable():
    m = M("chateau_sable", (3, 2, 3), "Château de sable")
    p = m.part("Chateau")
    p.boxb(2.0, 2.0, 0.9, 0, 0, 0, c="sand", bev=0.08)
    for x in (-1.1, 1.1):
        for y in (-1.1, 1.1):
            p.cyl(0.38, 1.4, at=(x, y, 0), c="sand", segs=8, bev=0.04)
            for k in range(4):
                a = k * math.pi / 2
                p.boxb(0.16, 0.16, 0.16, x + 0.3 * math.cos(a), y + 0.3 * math.sin(a), 1.4, c="sand", bev=0.02)
    p.cyl(0.45, 1.5, at=(0, 0, 0.5), r2=0.3, c="sand", segs=8, bev=0.04)
    p.cyl(0.03, 0.5, at=(0, 0, 2.0), c="wood_light", segs=4, bev=0)
    p.prism([(0, 0), (0.35, 0.1), (0, 0.22)], 0.02, at=(0, 0, 2.25), c="red")
    p.boxb(0.5, 0.1, 0.6, 0, -1.0, 0, c="wood_dark", bev=0.02)  # porte
    p.torus(1.6, 0.06, c="sky", segs=16, sides=3, at=(0, 0, 0.03))  # douve
    return m


def serviette_ballon():
    m = M("serviette_ballon", (3, 0.6, 5), "Serviette et ballon de plage")
    s, b = m.part("Serviette"), m.part("Ballon")
    s.boxb(2.6, 4.6, 0.04, 0, 0.2, 0, c=WHITE, bev=0)
    for i in range(6):
        s.boxb(2.62, 0.4, 0.045, 0, -1.8 + i * 0.8, 0, c="red" if i % 2 else "flower_yellow", bev=0)
    b.sphere(0.3, at=(1.05, -2.15, 0.3), c=WHITE, segs=12, rings=8)
    for i in range(3):
        b.torus(0.3, 0.025, at=(1.05, -2.15, 0.3), rot=(90, 0, i * 60), c=("red", "blue", "flower_yellow")[i], segs=12, sides=3)
    return m


def mouette():
    m = M("mouette", (1, 1, 1.5), "Mouette posée")
    p = m.part("Mouette")
    p.sphere(0.32, at=(0, 0.1, 0.45), c=WHITE, scale=(0.9, 1.5, 0.8), segs=10, rings=7, rot=(-8, 0, 0))
    p.sphere(0.2, at=(0, -0.38, 0.7), c=WHITE, segs=8, rings=6)
    p.lathe([(0, 0), (0.05, 0), (0, 0.22)], segs=6, at=(0, -0.55, 0.68), rot=(95, 0, 0), c="flower_yellow")
    p.sphere(0.02, at=(0, -0.66, 0.66), c="red", segs=4, rings=3)
    for s in (-1, 1):
        p.sphere(0.035, at=(s * 0.12, -0.5, 0.75), c="eye", segs=5, rings=3)
        p.sphere(0.25, at=(s * 0.27, 0.2, 0.52), c="grey_light", scale=(0.4, 1.6, 0.6), segs=7, rings=5, rot=(-8, 0, 0))
        p.rod((s * 0.1, 0.05, 0.18), (s * 0.1, 0.0, 0.0), 0.025, c="flower_yellow", sides=4)
    p.prism([(-0.15, 0), (0.15, 0), (0.0, 0.3)], 0.04, at=(0, 0.6, 0.45), rot=(-80, 0, 0), c="black")
    return m


# ---------------------------------------------------------------------------
# Port
# ---------------------------------------------------------------------------

def yacht():
    m = M("yacht_moteur", (10, 8, 30), "Yacht à moteur")
    h, c, v = m.part("Coque"), m.part("Cabine"), m.part("Vitres")
    prof = [(-14, 0.0), (-6, 0.0), (8, 0.0), (15, 1.5), (15, 3.2), (-15, 3.2), (-15, 1.0)]
    h.box(9.6, 29, 3.2, at=(0, 0, 1.6), c=WHITE, bev=0.6, taper=(1.05, 1.0),
          deform=lambda co: Vector((co.x * (1 - 0.75 * max(0, -co.y - 6) / 8.5), co.y, co.z + 0.06 * max(0, -co.y - 8) ** 1.4 * (co.z > 0))))
    h.box(9.7, 29.1, 0.4, at=(0, 0, 0.6), c=NAVY, bev=0.1, deform=lambda co: Vector((co.x * (1 - 0.75 * max(0, -co.y - 6) / 8.5), co.y, co.z)))
    h.boxb(9, 20, 0.15, 0, 3.5, 3.2, c="wood_light", bev=0.02)
    cabin(c, v, 7.5, 12, 2.4, 2.5, 3.3, 0.9, 0.8, WHITE, bev=0.3)
    cabin(c, v, 6.0, 7, 1.8, 3.5, 5.7, 0.85, 0.75, WHITE, bev=0.25)
    c.cyl(0.08, 1.6, at=(0, 5, 7.5), c="inox", segs=4, bev=0)
    for s in (-1, 1):
        h.rod((s * 4.6, -6, 3.9), (s * 4.6, 13, 3.9), 0.05, c="inox", sides=4)
    return m


def voilier():
    m = M("voilier", (8, 24, 20), "Voilier")
    h, mt, vo = m.part("Coque"), m.part("Mat"), m.part("Voiles")
    h.box(7.6, 19.5, 2.2, at=(0, 0, 1.1), c=NAVY, bev=0.5,
          deform=lambda co: Vector((co.x * (1 - 0.8 * max(0, -co.y - 3) / 7), co.y, co.z)))
    h.box(7.4, 19, 0.2, at=(0, 0, 2.25), c="wood_light", bev=0.05,
          deform=lambda co: Vector((co.x * (1 - 0.8 * max(0, -co.y - 3) / 7), co.y, co.z)))
    h.boxb(4, 6, 1.2, 0, 2, 2.3, c=WHITE, bev=0.2)
    h.box(7.65, 19.55, 0.3, at=(0, 0, 1.6), c=WHITE, bev=0.05, deform=lambda co: Vector((co.x * (1 - 0.8 * max(0, -co.y - 3) / 7), co.y, co.z)))
    mt.cyl(0.15, 21.5, at=(0, -1, 2.3), c=WHITE, segs=6, bev=0)
    mt.cyl(0.1, 7.5, at=(0, -1, 4.5), rot=(-90, 0, 0), c=WHITE, segs=6, bev=0)
    vo.prism([(0, 0), (7.2, 0), (0, 18.5)], 0.06, at=(0, -1.1, 4.8), plane="YZ", c=WHITE)  # grand-voile
    vo.prism([(0, 0), (-8.5, 0), (0, 16.5)], 0.06, at=(0, -1.6, 2.6), plane="YZ", c="sky")  # foc
    vo.rod((0, -9.8, 2.4), (0, -1.0, 23.5), 0.03, c="metal", sides=3)
    return m


def ponton():
    m = M("ponton_modulaire", (8, 1, 4), "Ponton modulaire", "8 studs")
    p = m.part("Ponton")
    p.boxb(8, 4, 0.6, 0, 0, 0, c=WHITE, bev=0.1)
    for i in range(16):
        p.boxb(0.46, 3.9, 0.12, -3.75 + i * 0.5, 0, 0.6, c="wood_light", bev=0.02)
    for x in (-3, 3):
        p.cyl(0.18, 0.28, at=(x, -1.85, 0.72), c="inox", segs=8, bev=0.03)  # taquets
    p.boxb(8, 0.15, 0.25, 0, -2.0, 0.2, c=NAVY, bev=0.02)
    return m


def phare():
    m = M("phare_jetee", (4, 18, 4), "Phare de jetée", "Rouge et blanc")
    t, l = m.part("Tour"), m.part("Lanterne")
    t.cyl(2.0, 1.0, c="marble", segs=12, bev=0.1)
    for i in range(6):
        t.cyl(1.5 - i * 0.07, 2.2, at=(0, 0, 1.0 + i * 2.2), r2=1.43 - i * 0.07, c=("red" if i % 2 == 0 else WHITE), segs=12, bev=0)
    t.cyl(1.7, 0.3, at=(0, 0, 14.2), c=WHITE, segs=12, bev=0.05)
    for k in range(10):
        a = 2 * math.pi * k / 10
        t.cyl(0.04, 0.8, at=(1.6 * math.cos(a), 1.6 * math.sin(a), 14.5), c=WHITE, segs=4, bev=0)
    t.lathe([(0, 0), (1.25, 0), (0.1, 1.6), (0, 1.6)], segs=12, at=(0, 0, 16.4), c="red")
    l.cyl(1.0, 1.9, at=(0, 0, 14.5), c="light_warm", segs=12, bev=0)
    t.boxb(1.0, 0.15, 1.8, 0, -1.42, 1.1, c=NAVY, bev=0.03)
    return m


# ---------------------------------------------------------------------------
# Hippodrome
# ---------------------------------------------------------------------------

def cheval():
    m = M("cheval_jockey", (2, 6, 7), "Cheval de course avec jockey", "Au galop, tourné vers -Z")
    ch, jo = m.part("Cheval"), m.part("Jockey")
    br = "wood"
    ch.sphere(1.0, at=(0, 0.3, 2.9), c=br, scale=(0.7, 2.0, 0.85), segs=12, rings=8)
    ch.pipe([(0, -1.4, 3.3), (0, -2.1, 4.2), (0, -2.5, 4.7)], 0.42, c=br, sides=8)
    ch.box(0.6, 1.4, 0.65, at=(0, -3.0, 4.6), rot=(30, 0, 0), c=br, bev=0.2)
    for s in (-1, 1):
        ch.prism([(-0.1, 0), (0.1, 0), (0, 0.35)], 0.08, at=(s * 0.18, -2.5, 5.05), c=br)
        ch.sphere(0.06, at=(s * 0.27, -3.0, 4.85), c="eye", segs=5, rings=3)
    ch.pipe([(0, -1.6, 3.9), (0, -2.2, 4.75)], 0.12, c="wood_black", sides=4)  # crinière
    legs = [((-0.4, -1.2), (-0.3, -2.4, 0.9), (-0.3, -2.9, 0.2)), ((0.4, -1.2), (0.3, -1.5, 1.0), (0.35, -1.0, 0.1)),
            ((-0.4, 1.6), (-0.35, 2.6, 1.3), (-0.3, 3.4, 0.6)), ((0.4, 1.6), (0.35, 1.2, 1.0), (0.3, 1.9, 0.0))]
    for (x, y), mid, foot in legs:
        ch.pipe([(x, y, 2.4), mid, foot], 0.17, c=br, sides=6)
        ch.sphere(0.17, at=foot, c="wood_black", segs=6, rings=4)
    ch.pipe([(0, 2.2, 3.2), (0, 3.0, 3.0), (0, 3.4, 2.3)], 0.15, c="wood_black", sides=5)  # queue
    ch.boxb(1.5, 1.3, 0.12, 0, -0.1, 3.65, c=WHITE, bev=0.03)  # tapis de selle
    jo.sphere(0.45, at=(0, -0.3, 4.4), c="red", scale=(0.9, 1.1, 0.9), segs=8, rings=6, rot=(40, 0, 0))
    jo.sphere(0.3, at=(0, -1.05, 5.1), c="peach", segs=8, rings=6)
    jo.sphere(0.33, at=(0, -1.0, 5.22), c="flower_yellow", segs=8, rings=5, deform=lambda co: Vector((co.x, co.y, max(co.z, 0))))
    for s in (-1, 1):
        jo.pipe([(s * 0.35, -0.4, 4.7), (s * 0.4, -1.2, 4.6), (s * 0.25, -1.9, 4.5)], 0.11, c="red", sides=5)
        jo.pipe([(s * 0.35, 0.0, 4.0), (s * 0.6, -0.4, 3.8), (s * 0.6, 0.1, 3.0)], 0.13, c=WHITE, sides=5)
    jo.boxb(0.9, 0.2, 0.5, 0, -0.75, 4.35, c="flower_yellow", bev=0.03)  # losange de casaque
    return m


def barriere():
    m = M("barriere_piste", (8, 3, 0.3), "Barrière de piste blanche", "Module de 8 studs")
    p = m.part("Barriere")
    for x in (-3.85, 0, 3.85):
        p.boxb(0.25, 0.25, 2.6, x, 0, 0, c=WHITE, bev=0.04)
    p.cyl(0.14, 8.0, at=(-4, 0, 2.8), rot=(0, 90, 0), c=WHITE, segs=10, bev=0)
    p.boxb(8, 0.15, 0.3, 0, 0, 1.2, c=WHITE, bev=0.04)
    return m


# ---------------------------------------------------------------------------
# Rues chic
# ---------------------------------------------------------------------------

def lampadaire_be():
    m = M("lampadaire_belle_epoque", (1.4, 14, 1.4), "Lampadaire Belle Époque")
    p, l = m.part("Poteau"), m.part("Lanterne")
    p.lathe([(0, 0), (0.7, 0), (0.6, 0.4), (0.35, 0.8), (0.3, 2.2), (0.2, 2.6), (0.13, 2.8), (0.11, 11.6), (0.2, 11.8), (0, 11.9)],
            segs=8, c=GREEN)
    for z in (2.5, 6.0, 11.4):
        p.torus(0.17, 0.05, at=(0, 0, z), c="gold", segs=8, sides=4)
    p.lathe([(0, 11.9), (0.5, 12.0), (0.45, 12.15), (0, 12.2)], segs=8, c=GREEN)
    l.lathe([(0, 12.2), (0.45, 12.3), (0.55, 13.0), (0, 13.05)], segs=6, c="light_warm")
    p.lathe([(0, 13.0), (0.65, 13.0), (0.15, 13.7), (0.05, 14.0), (0, 14.0)], segs=6, c=GREEN)
    return m


def banc_chic():
    m = M("banc_bois_fonte", (5, 3, 2), "Banc en bois et fonte")
    p = m.part("Banc")
    for x in (-2.2, 2.2):
        p.pipe([(x, -0.8, 0), (x, -0.7, 1.2), (x, 0.6, 1.2), (x, 0.8, 0)], 0.08, c="iron", sides=5)
        p.pipe([(x, 0.6, 1.2), (x, 0.85, 2.9)], 0.07, c="iron", sides=5)
        p.pipe([(x, -0.8, 1.2), (x, -0.85, 1.8), (x, 0.5, 1.9)], 0.06, c="iron", sides=4)
    for k in range(4):
        p.boxb(5, 0.3, 0.1, 0, -0.6 + k * 0.38, 1.2, c="wood_light", bev=0.02)
    for k in range(3):
        p.box(5, 0.08, 0.3, at=(0, 0.65 + k * 0.07, 1.6 + k * 0.42), rot=(-10, 0, 0), c="wood_light", bev=0.02)
    return m


def jardiniere():
    m = M("jardiniere_hortensias", (4, 2.5, 2), "Jardinière d'hortensias")
    b, f = m.part("Bac"), m.part("Fleurs")
    b.boxb(4, 2, 1.2, c=WHITE, bev=0.1)
    b.boxb(3.7, 1.7, 0.05, 0, 0, 1.15, c="soil", bev=0)
    for x in (-1.9, 1.9):
        b.boxb(0.25, 2.1, 1.25, x * 1.025, 0, 0, c=NAVY, bev=0.03)
    rng = random.Random(5)
    for i in range(7):
        x, y = -1.5 + i * 0.5, rng.uniform(-0.4, 0.4)
        f.sphere(0.45, at=(x, y, 1.45), c="leaf", scale=(1, 1, 0.6), segs=7, rings=4)
        f.sphere(0.36, at=(x, y, 1.95), c=("flower_purple", "sky", "flower_pink")[i % 3], segs=8, rings=5, deform=m.noise(0.04, i))
    return m


def pommier():
    m = M("pommier_normand", (8, 10, 8), "Pommier normand")
    t, fe, po = m.part("Tronc"), m.part("Feuillage"), m.part("Pommes")
    t.cyl(0.55, 4.0, r2=0.4, c="wood", segs=8, deform=m.noise(0.06, 1))
    for a, h in ((0, 1.3), (2.1, 1.1), (4.2, 1.4)):
        t.rod((0, 0, 3.6), (1.6 * math.cos(a), 1.6 * math.sin(a), 3.6 + h), 0.22, c="wood", sides=6)
    for (x, y, z, r) in ((0, 0, 6.5, 2.8), (-1.8, 0.8, 5.7, 1.9), (1.9, -0.6, 5.8, 2.0), (0.4, 1.6, 7.3, 1.7), (-0.6, -1.6, 7.0, 1.8)):
        fe.sphere(r, at=(x, y, z), c="leaf", segs=10, rings=7, deform=m.noise(0.12, int(x * 10 + y)))
    rng = random.Random(6)
    for k in range(18):
        a, e = rng.uniform(0, 2 * math.pi), rng.uniform(-0.6, 0.9)
        r = 2.9
        po.sphere(0.22, at=(r * math.cos(a) * math.cos(e), r * math.sin(a) * math.cos(e), 6.5 + r * math.sin(e)),
                  c=("red" if k % 3 else "lettuce"), segs=6, rings=4)
    return m


def topiaire():
    m = M("topiaire_buis", (2.5, 4, 2.5), "Topiaire (buis en boule)")
    p, b = m.part("Pot"), m.part("Buis")
    p.lathe([(0, 0), (0.7, 0), (0.9, 1.2), (1.0, 1.3), (0, 1.3)], segs=10, c=WHITE)
    p.torus(0.9, 0.06, at=(0, 0, 1.1), c=NAVY, segs=10, sides=3)
    p.cyl(0.85, 0.05, at=(0, 0, 1.2), c="soil", segs=10, bev=0)
    p.cyl(0.08, 0.6, at=(0, 0, 1.25), c="wood", segs=5, bev=0)
    b.sphere(1.2, at=(0, 0, 2.8), c="leaf_dark", segs=12, rings=9, deform=m.noise(0.04, 2))
    return m


def fontaine():
    m = M("fontaine", (8, 6, 8), "Fontaine")
    b, f, e = m.part("Bassin"), m.part("Fontaine"), m.part("Eau")
    b.lathe([(0, 0), (4.0, 0), (4.0, 0.9), (3.6, 1.0), (3.6, 0.3), (0, 0.3)], segs=16, c="marble")
    f.cyl(0.5, 2.6, at=(0, 0, 0.3), r2=0.35, c="marble", segs=10)
    f.lathe([(0, 2.8), (1.6, 2.9), (1.7, 3.2), (1.5, 3.25), (0, 3.1)], segs=12, c="marble")
    f.cyl(0.25, 1.4, at=(0, 0, 3.2), r2=0.18, c="marble", segs=8)
    f.lathe([(0, 4.6), (0.9, 4.7), (0.95, 4.9), (0, 4.85)], segs=10, c="marble")
    f.sphere(0.3, at=(0, 0, 5.3), c="gold", segs=8, rings=5)
    e.cyl(3.6, 0.5, at=(0, 0, 0.35), c="sky", segs=16, bev=0)
    e.cyl(1.5, 0.06, at=(0, 0, 3.15), c="sky", segs=12, bev=0)
    for k in range(8):  # jets
        a = 2 * math.pi * k / 8
        e.pipe([(0.8 * math.cos(a), 0.8 * math.sin(a), 4.9), (1.6 * math.cos(a), 1.6 * math.sin(a), 5.5), (2.4 * math.cos(a), 2.4 * math.sin(a), 0.9)],
               0.06, c="glass", sides=4)
    e.pipe([(0, 0, 5.5), (0, 0, 6.0)], 0.08, c="glass", sides=4)
    return m


def colonne_morris():
    m = M("colonne_morris", (3, 9, 3), "Colonne Morris", "Affiches vierges")
    c, a = m.part("Colonne"), m.part("Affiches")
    c.lathe([(0, 0), (1.4, 0), (1.3, 0.5), (1.2, 0.6), (1.2, 6.6), (1.4, 6.8), (1.5, 7.1), (0, 7.1)], segs=14, c=GREEN)
    c.lathe([(0, 7.1), (1.3, 7.1), (0.9, 8.1), (0.3, 8.6), (0.1, 9.0), (0, 9.0)], segs=14, c=GREEN)
    c.sphere(0.2, at=(0, 0, 8.9), c="gold", segs=6, rings=4)
    cols = [WHITE, "flower_yellow", "sky", "cream", "flower_pink", WHITE]
    for i in range(6):
        ang = i * 60
        a.box(1.15, 0.03, 4.8, at=(1.22 * math.cos(math.radians(ang - 90)), 1.22 * math.sin(math.radians(ang - 90)), 3.7),
              rot=(0, 0, ang), c=cols[i], bev=0)
    return m


def table_terrasse():
    m = M("table_parasol_terrasse", (4, 6, 4), "Parasol et table de terrasse")
    t, pa = m.part("Table"), m.part("Parasol")
    t.cyl(0.6, 0.08, c="iron", segs=10, bev=0.02)
    t.cyl(0.06, 2.4, at=(0, 0, 0.08), c="iron", segs=6, bev=0)
    t.cyl(1.0, 0.1, at=(0, 0, 2.4), c="marble", segs=14, bev=0.03)
    pa.cyl(0.05, 3.4, at=(0, 0, 2.5), c=WHITE, segs=6, bev=0)
    pa.lathe([(0, 0), (2.0, 0), (1.2, 0.5), (0, 0.8)], segs=8, at=(0, 0, 4.9), c=NAVY)
    for k in range(8):
        a = 2 * math.pi * (k + 0.5) / 8
        pa.prism([(-0.5, 0), (0.5, 0), (0, -0.3)], 0.03, at=(2.0 * math.cos(a) * 0.93, 2.0 * math.sin(a) * 0.93, 4.9),
                 rot=(0, 0, math.degrees(a) + 90), c=(WHITE if k % 2 else NAVY))
    return m


def chaise_rotin():
    m = M("chaise_rotin", (1.5, 3, 1.5), "Chaise de terrasse en rotin")
    p = m.part("Chaise")
    for sx in (-0.6, 0.6):
        for sy in (-0.6, 0.6):
            p.cyl(0.06, 1.5, at=(sx, sy, 0), c="cork", segs=5, bev=0)
    p.boxb(1.4, 1.4, 0.15, 0, 0, 1.5, c="crate", bev=0.04)
    p.boxb(1.3, 1.3, 0.12, 0, 0, 1.6, c=NAVY, bev=0.04)  # coussin
    p.pipe([(-0.65, 0.6, 1.6), (-0.65, 0.68, 2.9), (0.65, 0.68, 2.9), (0.65, 0.6, 1.6)], 0.07, c="cork", sides=5)
    for k in range(4):
        p.box(1.2, 0.06, 0.16, at=(0, 0.66, 1.9 + k * 0.25), c=("crate" if k % 2 else "cork"), bev=0)
    return m


def cabriolet():
    W, H, L = 5, 4, 10
    m = M("cabriolet_retro", (W, H, L), "Cabriolet rétro de luxe")
    b, v = m.part("Carrosserie"), m.part("Vitres")
    b.box(4.6, L - 0.3, 1.5, at=(0, 0, 1.55), c="red", bev=0.45)
    for s in (-1, 1):
        b.sphere(1.0, at=(s * 2.0, -3.0, 1.5), c="red", scale=(0.45, 1.3, 0.7), segs=10, rings=6)  # ailes galbées
        b.sphere(1.0, at=(s * 2.0, 3.1, 1.5), c="red", scale=(0.45, 1.3, 0.7), segs=10, rings=6)
    b.boxb(3.6, 3.0, 0.5, 0, 1.0, 2.0, c="leather", bev=0.15)  # sièges
    b.boxb(3.6, 0.5, 1.2, 0, 1.6, 2.2, c="leather", bev=0.15)
    v.box(3.8, 0.08, 1.0, at=(0, -1.0, 2.9), rot=(-25, 0, 0), c="glass", bev=0.02)
    b.boxb(4.6, 0.3, 0.3, 0, -L / 2 + 0.2, 0.9, c="chrome", bev=0.08)
    b.boxb(4.6, 0.3, 0.3, 0, L / 2 - 0.2, 0.9, c="chrome", bev=0.08)
    for x in (-1.5, 1.5):
        b.cyl(0.3, 0.1, at=(x, -L / 2 + 0.05, 1.6), rot=(90, 0, 0), c="light_warm", segs=10, bev=0.02)
    for name, x, y in (("RoueAvG", 2.0, -3.0), ("RoueAvD", -2.0, -3.0), ("RoueArG", 2.0, 3.1), ("RoueArD", -2.0, 3.1)):
        wheel(m, "Roues", x, y, 0.85, 0.6, rim="chrome", side=(1 if x > 0 else -1))
    m.parts["Roues"].pivot = None
    return m


def berline():
    W, H, L = 5, 4.5, 11
    m = M("berline_luxe", (W, H, L), "Berline de luxe")
    b, v = m.part("Carrosserie"), m.part("Vitres")
    b.box(4.7, L - 0.2, 1.6, at=(0, 0, 1.45), c="navy_paint", bev=0.45)
    cabin(b, v, 4.3, 5.2, 1.8, 0.6, 2.25, 0.85, 0.72, "navy_paint", bev=0.3)
    b.boxb(4.7, 0.3, 0.35, 0, -L / 2 + 0.15, 0.75, c="chrome", bev=0.08)
    b.boxb(4.7, 0.3, 0.35, 0, L / 2 - 0.15, 0.75, c="chrome", bev=0.08)
    b.boxb(1.8, 0.1, 0.6, 0, -L / 2 + 0.05, 1.3, c="chrome", bev=0.03)
    for x in (-1.7, 1.7):
        b.box(0.8, 0.08, 0.3, at=(x, -L / 2 + 0.07, 1.6), c="light_white", bev=0.02)
    for x, y in ((2.1, -3.4), (-2.1, -3.4), (2.1, 3.4), (-2.1, 3.4)):
        wheel(m, "Roues", x, y, 0.9, 0.7, rim="chrome", side=(1 if x > 0 else -1))
    m.parts["Roues"].pivot = None
    return m


# ---------------------------------------------------------------------------
# Intérieur du casino
# ---------------------------------------------------------------------------

def table_jeu_base(t, w, d, h=3.2):
    for sx in (-1, 1):
        for sy in (-1, 1):
            t.lathe([(0, 0), (0.25, 0), (0.15, 0.4), (0.18, h - 0.6), (0.3, h - 0.4), (0, h - 0.4)], segs=8,
                    at=(sx * (w / 2 - 0.6), sy * (d / 2 - 0.6), 0), c="wood_dark")
    t.boxb(w, d, 0.4, 0, 0, h - 0.4, c="wood_red", bev=0.12)


def roulette():
    m = M("table_roulette", (6, 3.5, 10), "Table de roulette")
    t, r, ta = m.part("Table"), m.part("Roue"), m.part("Tapis")
    table_jeu_base(t, 6, 10)
    ta.boxb(5.2, 9.2, 0.05, 0, 0, 3.2, c="felt", bev=0)
    for i in range(12):
        for j in range(3):
            ta.boxb(1.3, 0.45, 0.02, -1.4 + j * 1.4, -2.0 + i * 0.52, 3.25, c=("red" if (i + j) % 2 else "black"), bev=0)
    t.cyl(1.9, 0.2, at=(0, 3.0, 3.2), c="wood_dark", segs=16, bev=0.05)
    r.cyl(1.6, 0.2, at=(0, 3.0, 3.3), c="wood_red", segs=16, bev=0.03)
    for k in range(18):
        a0, a1 = 2 * math.pi * k / 18, 2 * math.pi * (k + 1) / 18
        r.prism([(0.9 * math.cos(a0), 0.9 * math.sin(a0)), (1.5 * math.cos(a0), 1.5 * math.sin(a0)), (1.5 * math.cos(a1), 1.5 * math.sin(a1)),
                 (0.9 * math.cos(a1), 0.9 * math.sin(a1))], 0.04, at=(0, 3.0, 3.52), plane="XY", c=("red" if k % 2 else "black"))
    r.cyl(0.85, 0.1, at=(0, 3.0, 3.5), c="gold", segs=12, bev=0.02)
    r.lathe([(0, 0), (0.15, 0), (0.05, 0.4), (0, 0.45)], segs=6, at=(0, 3.0, 3.6), c="gold")
    r.sphere(0.07, at=(1.2, 3.0, 3.6), c=WHITE, segs=5, rings=3)
    return m


def blackjack():
    m = M("table_blackjack", (8, 3.5, 5), "Table de blackjack")
    t, ta = m.part("Table"), m.part("Tapis")
    for x in (-2.6, 0, 2.6):
        t.lathe([(0, 0), (0.6, 0), (0.25, 0.4), (0.25, 2.6), (0, 2.6)], segs=8, at=(x, 0.6, 0), c="wood_dark")
    half = [(3.8 * math.cos(math.radians(a)), -0.2 + 2.6 * math.sin(math.radians(a))) for a in range(180, 361, 15)]
    t.prism(half, 0.5, at=(0, 0, 2.85), plane="XY", c="wood_red", bev=0.1)
    ta.prism([(x * 0.9, y * 0.88 - 0.02) for x, y in half], 0.06, at=(0, 0, 3.12), plane="XY", c="felt")
    for k in range(5):
        a = math.radians(200 + k * 35)
        ta.cyl(0.25, 0.02, at=(2.6 * math.cos(a), -0.2 + 1.8 * math.sin(a), 3.15), c="flower_yellow", segs=10, bev=0)
    t.boxb(1.4, 0.6, 0.3, 0, 0.0, 3.1, c="inox", bev=0.04)  # sabot
    t.boxb(8, 0.4, 0.5, 0, 0.1, 2.85, c="wood_red", bev=0.1)
    return m


def lustre_cristal():
    m = M("lustre_cristal", (5, 4, 5), "Lustre en cristal", "Accroché par le haut")
    l, a = m.part("Lustre"), m.part("Ampoules")
    l.cyl(0.4, 0.1, at=(0, 0, 3.9), c="gold", segs=10, bev=0.02)
    l.rod((0, 0, 3.9), (0, 0, 2.6), 0.06, c="gold", sides=5)
    l.lathe([(0, 1.2), (0.5, 1.4), (0.6, 2.0), (0.3, 2.6), (0, 2.65)], segs=10, c="gold")
    for tier, (R, z, n) in enumerate(((2.3, 1.4, 10), (1.4, 2.1, 6))):
        l.torus(R, 0.06, at=(0, 0, z), c="gold", segs=16, sides=4)
        for k in range(n):
            ang = 2 * math.pi * k / n
            x, y = R * math.cos(ang), R * math.sin(ang)
            l.lathe([(0, 0), (0.07, 0.15), (0, 0.5)], segs=4, at=(x, y, z - 0.6), c="glass")
            a.lathe([(0, 0), (0.09, 0.08), (0.1, 0.22), (0, 0.35)], segs=6, at=(x, y, z + 0.06), c="light_warm")
        for k in range(n * 2):
            ang = 2 * math.pi * (k + 0.5) / (n * 2)
            l.sphere(0.06, at=(R * math.cos(ang), R * math.sin(ang), z - 0.25), c="glass", segs=4, rings=3)
    l.lathe([(0, 0), (0.25, 0.5), (0.1, 1.2), (0, 1.25)], segs=6, c="glass")
    return m


def bar_marbre():
    m = M("bar_marbre", (12, 4, 2), "Bar chic en marbre")
    c, e = m.part("Comptoir"), m.part("Etageres")
    c.boxb(12, 1.6, 3.2, 0, -0.2, 0, c="wood_dark", bev=0.08)
    c.boxb(12.0, 1.8, 0.25, 0, -0.2, 3.2, c="marble", bev=0.06)
    for i in range(6):
        c.boxb(1.6, 0.06, 2.4, -5 + i * 2, -1.03, 0.4, c="wood_red", bev=0.03)
    c.rod((-5.8, -1.25, 0.4), (5.8, -1.25, 0.4), 0.06, c="gold", sides=6)
    c.boxb(12, 0.08, 0.15, 0, -1.08, 3.0, c="gold", bev=0)
    rng = random.Random(9)
    for z in (3.5, 3.85):
        e.boxb(11, 0.35, 0.05, 0, 0.75, z - 0.05, c="gold", bev=0)
    for k in range(18):
        x = -5.2 + k * 0.6
        e.lathe([(0, 0), (0.1, 0), (0.1, 0.35), (0.035, 0.45), (0.03, 0.5), (0, 0.5)], segs=6, at=(x, 0.75, 3.5),
                c=rng.choice(["green_dark", "glass_dark", "copper", "red_dark"]))
    return m


MODELS = [
    ("121_casino", casino),
    ("122_hotel_normandy", lambda: hotel_normand("hotel_normandy", (70, 30, 30), "Hôtel Normandy")),
    ("123_hotel_royal", hotel_royal), ("124_bains_pompeiens", bains), ("125_bar_du_soleil", bar_soleil),
    ("126_gare_trouville_deauville", gare), ("127_marche_couvert", marche_couvert), ("128_villa_strassburger", villa_strass),
    ("129_eglise_notre_dame", eglise), ("130_tribune_hippodrome", tribune),
    ("131_villa_anglo_normande_a", villa_a), ("132_villa_anglo_normande_b", villa_b), ("133_immeuble_boutique_luxe", boutique_luxe),
    ("134_residence_balneaire", residence), ("135_cafe_brasserie", brasserie),
    ("136_module_planches", planches), ("137_cabine_plage", cabine), ("138_parasol_ouvert", lambda: parasol(True)),
    ("139_parasol_ferme", lambda: parasol(False)), ("140_transat", transat), ("141_douche_plage", douche),
    ("142_poste_secours", poste_secours), ("143_chateau_sable", chateau_sable), ("144_serviette_ballon", serviette_ballon),
    ("145_mouette", mouette), ("146_yacht_moteur", yacht), ("147_voilier", voilier), ("148_ponton_modulaire", ponton),
    ("149_phare_jetee", phare), ("150_cheval_jockey", cheval), ("151_barriere_piste", barriere),
    ("152_lampadaire_belle_epoque", lampadaire_be), ("153_banc_bois_fonte", banc_chic), ("154_jardiniere_hortensias", jardiniere),
    ("155_pommier_normand", pommier), ("156_topiaire_buis", topiaire), ("157_fontaine", fontaine), ("158_colonne_morris", colonne_morris),
    ("159_table_parasol_terrasse", table_terrasse), ("160_chaise_rotin", chaise_rotin), ("161_cabriolet_retro", cabriolet),
    ("162_berline_luxe", berline), ("163_table_roulette", roulette), ("164_table_blackjack", blackjack),
    ("165_lustre_cristal", lustre_cristal), ("166_bar_marbre", bar_marbre),
]
