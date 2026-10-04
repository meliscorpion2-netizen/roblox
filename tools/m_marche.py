"""34–36 : marché."""
import random

from lib import Model

CAT = "04_marche"


def crate(p, w, d, h, x=0, y=0, z=0, c="crate", c2="wood_light", rng=None, slats=2):
    t = 0.08
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.boxb(0.16, 0.16, h, x + sx * (w / 2 - 0.08), y + sy * (d / 2 - 0.08), z, c=c2, bev=0.02)
    sh = h / (slats * 2 - 0.4)
    for k in range(slats):
        zz = z + 0.05 + k * sh * 2
        for sy in (-1, 1):
            p.boxb(w, t, sh * 1.2, x, y + sy * (d / 2 - t / 2), zz, c=c, bev=0.015)
        for sx in (-1, 1):
            p.boxb(t, d - 0.1, sh * 1.2, x + sx * (w / 2 - t / 2), y, zz, c=c, bev=0.015)
    for k in range(4):
        yy = y - d / 2 + 0.2 + k * (d - 0.4) / 3
        p.boxb(w - 0.1, 0.32, t, x, yy, z, c=c, bev=0.015)


def etal():
    m = Model("etal_marche", (13, 9, 5), CAT, "Étal de marché", 5)
    c = m.part("Comptoir")
    c.boxb(11.0, 3.6, 0.22, 0, 0.1, 3.0, c="wood")
    for x in (-4.8, 0, 4.8):
        c.boxb(0.25, 3.2, 0.25, x, 0.1, 0.5, c="metal_dark")
        for s in (-1, 1):
            c.rod((x, 0.1 + s * 1.5, 0), (x, 0.1 + s * 1.2, 3.0), 0.08, c="metal_dark", sides=4)
    # nappe qui pend devant (légèrement ondulée)
    c.box(11.1, 0.06, 2.3, at=(0, -1.72, 1.95), c="fabric_green", bev=0, deform=m.noise(0.05, 1))
    c.decal(1.5, 0.8, (-2.5, -1.77, 1.3), c="mud", seed=2)
    c.decal(1.0, 0.6, (3.4, -1.77, 1.0), c="stain", seed=3)
    rng = random.Random(4)
    for i, (x, col) in enumerate(((-3.8, "tomato"), (-1.3, "lettuce"), (1.2, "flame_orange"), (3.7, "yellow"))):
        crate(c, 2.2, 1.6, 0.6, x, -0.5, 3.22, c="crate", rng=rng, slats=1)
        for k in range(7):
            fx = x + rng.uniform(-0.75, 0.75)
            fy = -0.5 + rng.uniform(-0.5, 0.5)
            c.sphere(0.3 if col != "lettuce" else 0.36, at=(fx, fy, 3.82 + rng.uniform(0, 0.1)), c=col, segs=6, rings=4,
                     scale=(1, 1, 0.85))
    c.box(1.2, 1.0, 0.5, at=(-0.2, 1.1, 3.47), c="cardboard", bev=0.05)
    c.box(0.6, 0.4, 0.4, at=(4.5, 1.2, 3.42), c="metal", bev=0.05)  # balance
    c.cyl(0.35, 0.05, at=(4.5, 1.2, 3.65), c="inox", segs=10, bev=0)
    s = m.part("Structure")
    for x in (-5.6, 5.6):
        s.cyl(0.1, 6.7, at=(x, -2.0, 0), c="metal", segs=6, bev=0)
        s.cyl(0.1, 7.9, at=(x, 2.0, 0), c="metal", segs=6, bev=0)
        s.cyl(0.25, 0.12, at=(x, -2.0, 0), c="concrete_dark", segs=8)
        s.cyl(0.25, 0.12, at=(x, 2.0, 0), c="concrete_dark", segs=8)
    s.rod((-5.6, 2.0, 7.85), (5.6, 2.0, 7.85), 0.08, c="metal", sides=5)
    s.rod((-5.6, -2.0, 6.65), (5.6, -2.0, 6.65), 0.08, c="metal", sides=5)
    s.rod((0, 2.0, 7.9), (0, -2.0, 6.7), 0.06, c="metal", sides=4)
    a = m.part("Auvent")
    import math
    ang = math.degrees(math.atan2(1.3, 4.8))
    for i in range(13):
        x = -6.0 + i
        col = "red" if i % 2 == 0 else "white"
        a.box(1.0, 5.0, 0.08, at=(x, -0.05, 7.3), rot=(-ang, 0, 0), c=col, bev=0, deform=m.noise(0.02, 10 + i))
        a.prism([(-0.5, 0), (0.5, 0), (0.0, -0.45)], 0.05, at=(x, -2.55, 6.68), c=col)
    a.decal(2.0, 1.4, (2.5, 0.2, 7.42), c="mud", rot=(90 - ang, 0, 0), t=0.03, seed=11)
    a.box(0.7, 0.6, 0.12, at=(-3.6, -0.6, 7.25), rot=(-ang, 0, 15), c="wood_dark", bev=0.02)  # trou rafistolé
    pn = m.part("Panneau")
    pn.boxb(6.0, 0.2, 1.0, 0, 2.05, 7.95, c="wood_dark")
    pn.boxb(5.6, 0.04, 0.7, 0, 1.93, 8.1, c="cream", bev=0)
    for x in (-2.6, 2.6):
        pn.boxb(0.12, 0.12, 0.25, x, 2.05, 7.75, c="metal_dark")
    return m


def cagette_vide():
    m = Model("cagette_vide", (2.4, 1.6, 2.4), CAT, "Cagette en bois vide")
    p = m.part("Cagette")
    crate(p, 2.4, 2.4, 1.6, c="crate", c2="wood_light")
    p.decal(0.6, 0.4, (0.5, -1.25, 0.5), c="mud", seed=1)
    return m


def cagette_fleurs():
    m = Model("cagette_fleurs", (2.4, 2, 2.4), CAT, "Cagette de fleurs pleine")
    p = m.part("Cagette")
    crate(p, 2.4, 2.4, 1.15, c="crate", c2="wood_light", slats=2)
    p.boxb(2.2, 2.2, 0.1, 0, 0, 0.95, c="soil")
    f = m.part("Fleurs")
    rng = random.Random(7)
    cols = ["flower_red", "flower_pink", "flower_yellow", "flower_white", "flower_purple"]
    for i in range(3):
        for j in range(3):
            x, y = -0.75 + i * 0.75, -0.75 + j * 0.75
            col = cols[(i * 3 + j) % len(cols)]
            f.lathe([(0, 0), (0.28, 0.25), (0.05, 0.55)], segs=5, at=(x, y, 0.95), c="leaf_dark", deform=m.noise(0.04, i * 3 + j))
            for k in range(3):
                fx, fy = x + rng.uniform(-0.22, 0.22), y + rng.uniform(-0.22, 0.22)
                fz = 1.55 + rng.uniform(0, 0.25)
                f.rod((x, y, 1.1), (fx, fy, fz), 0.025, c="leaf", sides=3)
                f.sphere(0.17, at=(fx, fy, fz + 0.04), c=col, segs=6, rings=4, scale=(1, 1, 0.55))
                f.sphere(0.06, at=(fx, fy, fz + 0.11), c="flower_yellow" if col != "flower_yellow" else "wood_dark", segs=5, rings=3)
    return m


MODELS = [("34_etal_marche", etal), ("35_cagette_vide", cagette_vide), ("36_cagette_fleurs", cagette_fleurs)]
