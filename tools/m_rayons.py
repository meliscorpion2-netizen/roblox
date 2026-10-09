"""197–202 : rayons du magasin de pièces de machines."""
import math
import random

from lib import Model

CAT = "13_rayons"
LEVELS = (0.3, 2.85, 5.4)


def M(name, dims, title, note=""):
    m = Model(name, dims, CAT, title, None, note)
    m.grime = False
    return m


def rayon(m):
    r = m.part("Rayon")
    for x in (-4.9, 0, 4.9):
        for y in (-1.35, 1.35):
            r.boxb(0.2, 0.2, 8.0, x, y, 0, c="steel_blue", bev=0.03)
    r.boxb(10, 0.08, 7.6, 0, 1.42, 0.3, c="grey_light", bev=0)  # fond
    for z in LEVELS + (7.85,):
        r.boxb(10, 3, 0.15, 0, 0, z, c="metal_light", bev=0.03)
        r.boxb(10, 0.08, 0.3, 0, -1.48, z - 0.08, c="orange", bev=0)  # bord porte-étiquettes
    return r, m.part("Articles")


def slots(n=4):
    return [(-3.75 + i * 7.5 / (n - 1), z) for z in LEVELS for i in range(n)]


def boitiers():
    m = M("rayon_boitiers", (10, 8, 3), "Rayon des boîtiers", "Du plus abîmé (gauche) au plus propre (droite)")
    _, a = rayon(m)
    states = [("rust_dark", "rust"), ("rust", "metal"), ("metal", "grey"), ("grey", "red_dark"), ("red_dark", "red"), ("red", "gold")]
    for k, (x, z) in enumerate(slots(4)):
        t = (k % 4) / 3 + (2 - LEVELS.index(z)) * 0.0
        c1, c2 = states[min(5, int((k % 4) * 1.4 + (LEVELS.index(z)) * 0.5))]
        a.boxb(1.6, 1.3, 2.1, x, -0.1, z + 0.15, c=c1, bev=0.12)
        a.boxb(1.2, 0.08, 0.8, x, -0.77, z + 1.1, c=("screen_dark" if k % 4 < 2 else "screen"), bev=0)
        a.boxb(1.7, 1.35, 0.2, x, -0.1, z + 2.1, c=c2, bev=0.05)
        a.boxb(1.0, 0.1, 0.25, x, -0.78, z + 0.5, c="black", bev=0)
        if k % 4 == 0:
            a.decal(0.7, 0.5, (x + 0.3, -0.76, z + 0.4), c="rust", seed=k)
            a.box(0.08, 0.4, 0.6, at=(x - 0.82, -0.1, z + 1.5), c=c1, bev=0)  # tôle bosselée
        if k % 4 == 3:
            a.sphere(0.12, at=(x, -0.8, z + 2.05), c="light_warm", segs=6, rings=4)
    return m


def mecanismes():
    m = M("rayon_mecanismes", (10, 8, 3), "Rayon des mécanismes à rouleaux")
    _, a = rayon(m)
    cols = ["red", "flower_yellow", "blue", "green", "purple"]
    for k, (x, z) in enumerate(slots(4)):
        a.boxb(1.8, 1.2, 0.15, x, -0.1, z + 0.15, c="metal_dark", bev=0.03)
        for s in (-1, 1):
            a.boxb(0.12, 1.0, 1.6, x + s * 0.85, -0.1, z + 0.3, c="metal_dark", bev=0.02)
        a.cyl(0.05, 1.8, at=(x - 0.9, -0.1, z + 1.1), rot=(0, 90, 0), c="chrome", segs=6, bev=0)
        for i in range(3):
            a.cyl(0.6, 0.45, at=(x - 0.72 + i * 0.5, -0.1, z + 1.1), rot=(0, 90, 0), c="cream", segs=8, bev=0)
            for j in range(2):
                ang = math.radians(-30 + j * 60)
                a.box(0.3, 0.05, 0.25, at=(x - 0.5 + i * 0.5, -0.1 - 0.6 * math.cos(ang), z + 1.1 + 0.6 * math.sin(ang)),
                      rot=(-math.degrees(ang), 0, 0), c=cols[(i + j + k) % 5], bev=0)
    return m


def leviers():
    m = M("rayon_leviers", (10, 8, 3), "Rayon des leviers")
    _, a = rayon(m)
    cols = ["red", "blue", "green", "flower_yellow"]
    for k, (x, z) in enumerate(slots(3)):
        a.boxb(2.6, 1.6, 0.6, x, -0.2, z + 0.15, c=("blue_dark" if k % 2 else "red_dark"), bev=0.06)  # bac
        for i in range(4):
            lx = x - 0.9 + i * 0.6
            a.rod((lx, -0.2, z + 0.4), (lx, -0.3, z + 1.9), 0.05, c="chrome", sides=5)
            a.sphere(0.17, at=(lx, -0.31, z + 2.0), c=cols[(i + k) % 4], segs=8, rings=5)
    return m


def tabouret(p, x, y, z):
    p.cyl(0.62, 0.18, at=(x, y, z + 0.95), c="red", segs=12, bev=0.05)
    p.torus(0.45, 0.04, at=(x, y, z + 0.4), c="chrome", segs=10, sides=3)
    for a in range(4):
        ang = math.radians(a * 90 + 45)
        p.rod((x + 0.4 * math.cos(ang), y + 0.4 * math.sin(ang), z + 0.95), (x + 0.55 * math.cos(ang), y + 0.55 * math.sin(ang), z), 0.05,
              c="chrome", sides=3)


def sieges():
    m = M("rayon_sieges", (10, 8, 3), "Rayon des sièges", "Tabourets empilés")
    _, a = rayon(m)
    for k, (x, z) in enumerate(slots(3)):
        for s in range(2):
            tabouret(a, x, -0.1, z + 0.15 + s * 0.55)
    return m


def cpu():
    m = M("rayon_cpu", (10, 8, 3), "Rayon des cartes électroniques", "Cartes rangées dans des casiers")
    _, a = rayon(m)
    rng = random.Random(5)
    for k, (x, z) in enumerate(slots(3)):
        a.boxb(2.6, 2.0, 0.15, x, -0.2, z + 0.15, c="plastic_black", bev=0.03)
        for s in (-1, 1):
            a.boxb(0.1, 2.0, 1.6, x + s * 1.25, -0.2, z + 0.15, c="plastic_black", bev=0.02)
        for i in range(6):
            bx = x - 1.0 + i * 0.4
            a.boxb(0.06, 1.6, 1.3, bx, -0.2, z + 0.3, c="green_dark", bev=0)
            for j in range(2):
                a.boxb(0.08, 0.35, 0.3, bx - 0.05, -0.6 + j * 0.7, z + 0.6 + rng.uniform(0, 0.4), c="black", bev=0)
            a.boxb(0.08, 0.2, 0.08, bx - 0.05, 0.3, z + 1.3, c="gold", bev=0)
    return m


def panneau():
    m = M("panneau_rayon", (4, 1.5, 0.3), "Pancarte de rayon", "Zone vierge pour le nom du rayon")
    p = m.part("Panneau")
    p.boxb(4, 0.2, 1.0, 0, 0, 0, c="orange", bev=0.06)
    p.boxb(3.5, 0.06, 0.7, 0, -0.12, 0.15, c="white", bev=0)
    for x in (-1.6, 1.6):
        for k in range(3):
            p.torus(0.08, 0.02, at=(x, 0, 1.08 + k * 0.14), rot=((90 if k % 2 else 0), 0, 0), c="metal", segs=6, sides=3)
    return m


MODELS = [("197_rayon_boitiers", boitiers), ("198_rayon_mecanismes", mecanismes), ("199_rayon_leviers", leviers),
          ("200_rayon_sieges", sieges), ("201_rayon_cpu", cpu), ("202_panneau_rayon", panneau)]
