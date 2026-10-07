"""Slot machines: LuckyFruits (Common), OceanTreasure (Rare), NeonFortune (Epic), GoldenPharaoh (Legendary).

Shared layout: 6 wide (X) x 5 deep (Z) x 9 tall (Y), pivot at ground centre, screen faces -Z.
Lever pivots at its hub on the +X side (rotates around the X axis), toppers pivot on the
vertical centre axis at the top of the cabinet.
"""
import math

import numpy as np

from casino_geo import (Geo, Model, M, T, RX, RY, RZ, S, FACE, UP_TO_FRONT, box, lathe, cyl, sphere, dome,
                        extrude, puffy, puffy_star, coin, pyramid, circle2, star2, frustum_box, ring2_geo)

LEVER_PIVOT = (2.6, 4.2, 0.3)


# ----------------------------------------------------------------------------- helpers
def rounded_rect2(x0, y0, x1, y1, rt, rb=0.0, n=5):
    pts = []

    def arc(cx, cy, r, a0, a1):
        if r <= 0:
            pts.append((cx, cy))
            return
        for k in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    arc(x0 + rb, y0 + rb, rb, 180, 270)
    arc(x1 - rb, y0 + rb, rb, 270, 360)
    arc(x1 - rt, y1 - rt, rt, 0, 90)
    arc(x0 + rt, y1 - rt, rt, 90, 180)
    return pts


def side_prism(poly_zy, x0, x1, col, side=None):
    """Prism whose profile is drawn in the side view (z, y) and extruded along X."""
    return extrude([(-z, y) for z, y in poly_zy], x0, x1, col, side).xf(RY(90))


def align_y(d):
    """Rotation matrix turning +Y into direction d."""
    d = np.asarray(d, float)
    d = d / np.linalg.norm(d)
    y = np.array((0.0, 1.0, 0.0))
    v = np.cross(y, d)
    c = float(np.dot(y, d))
    m = np.eye(4)
    if np.linalg.norm(v) < 1e-9:
        if c < 0:
            m[:3, :3] = np.diag((1, -1, -1))
        return m
    vx = np.array(((0, -v[2], v[1]), (v[2], 0, -v[0]), (-v[1], v[0], 0)))
    m[:3, :3] = np.eye(3) + vx + vx @ vx * (1 / (1 + c))
    return m


def rod(p0, p1, r, col, seg=6, caps=True):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    L = np.linalg.norm(p1 - p0)
    prof = ([(0, 0)] if caps else []) + [(r, 0), (r, L)] + ([(0, L)] if caps else [])
    return lathe(prof, seg, col).xf(M(T(*p0), align_y(p1 - p0)))


def flat(poly, col, t=0.08):
    """Thin flat sticker shape facing -Z, back at z=0."""
    return extrude(poly, -t, 0.0, col, back=False)


def bump(poly, col, side=None, t=0.06, b=0.08):
    """Chunky pillow-shaped sticker facing -Z with its back at z=0."""
    return puffy(poly, t, b, col, side, back=False).xf(T(0, 0, -t / 2))


def on_front(g, x, y, z, s=1.0):
    return g.xf(M(T(x, y, z), S(s)))


def deck(x0, x1, z_front, col, top_col):
    """Sloped control deck under the screen."""
    poly = [(z_front + 0.0, 2.55), (z_front - 0.7, 2.7), (z_front - 0.7, 3.0), (z_front + 0.0, 3.45)]
    return side_prism(poly, x0, x1, col, top_col)


def lever_hub(col, ring, x_in=-0.3, x_out=0.3, r=0.42):
    prof = [(0, x_in), (r, x_in), (r, x_out - 0.12), (r - 0.08, x_out), (0, x_out)]
    g = lathe(prof, 10, col)
    g += lathe([(r + 0.02, -0.04), (r + 0.06, 0.0), (r + 0.06, 0.08), (r + 0.02, 0.12)], 10, ring)
    return g.xf(RZ(-90))


# ----------------------------------------------------------------------------- icons (unit size ~1, facing -Z)
def ic_cherry():
    g = Geo()
    g += rod((-0.22, -0.12, -0.05), (0.08, 0.42, -0.05), 0.045, "leaf_dark", 4)
    g += rod((0.25, -0.2, -0.05), (0.08, 0.42, -0.05), 0.045, "leaf_dark", 4)
    g += bump(circle2(-0.22, -0.25, 0.27, 10), "cherry", "cherry_dark", 0.08, 0.1)
    g += bump(circle2(0.25, -0.32, 0.27, 10), "cherry", "cherry_dark", 0.08, 0.1)
    g += bump([(0.08, 0.42), (0.32, 0.5), (0.48, 0.42), (0.3, 0.36)], "leaf")
    return g


def ic_lemon():
    pts = [(0.5, 0.0)] + [p for p in circle2(0, 0, 0.36, 12, start=15, sx=1.05, sy=0.78)][:5] + [(-0.5, 0.0)] + \
          [p for p in circle2(0, 0, 0.36, 12, start=195, sx=1.05, sy=0.78)][:5]
    g = bump(pts, "lemon", "lemon_dark", 0.08, 0.14).xf(RZ(25))
    g += bump(circle2(-0.08, 0.1, 0.07, 6), "white", None, 0.02, 0.02).xf(T(0, 0, -0.14))
    return g


def ic_melon():
    outer = [(0.5 * math.cos(math.radians(a)), 0.5 * math.sin(math.radians(a)) + 0.18) for a in range(180, 361, 20)]
    inner = [(0.4 * math.cos(math.radians(a)), 0.4 * math.sin(math.radians(a)) + 0.18) for a in range(180, 361, 20)]
    g = flat(outer, "melon_green", 0.08)
    g += bump(inner, "melon_red", None, 0.05, 0.06).xf(T(0, 0, -0.08))
    for sx, sy in ((-0.18, 0.02), (0.0, -0.08), (0.18, 0.02), (-0.08, -0.04 - 0.08), (0.1, -0.13)):
        g += flat([(sx, sy - 0.05), (sx + 0.035, sy + 0.02), (sx - 0.035, sy + 0.02)], "seed", 0.03).xf(T(0, 0, -0.15))
    return g


def ic_seven(col="seven", side="red_dark"):
    poly = [(-0.36, 0.45), (0.38, 0.45), (0.38, 0.28), (0.02, -0.46), (-0.22, -0.46), (0.12, 0.26), (-0.36, 0.26)]
    return bump(poly, col, side, 0.1, 0.1)


def ic_diamond(col="diamond", side="diamond_dark"):
    poly = [(-0.42, 0.14), (-0.24, 0.36), (0.24, 0.36), (0.42, 0.14), (0.0, -0.42)]
    return bump(poly, col, side, 0.08, 0.14)


def ic_pearl():
    g = bump(circle2(0, -0.05, 0.3, 10), "pearl", "pearl_shade", 0.08, 0.14)
    g += flat(circle2(-0.1, 0.06, 0.07, 6), "white", 0.02).xf(T(0, 0, -0.2))
    g += flat([(-0.45, -0.38), (0.45, -0.38), (0.35, -0.3), (-0.35, -0.3)], "shell_dark", 0.05)
    return g


def ic_fish():
    body = circle2(0.06, 0, 0.32, 12, sx=1.15, sy=0.75)
    g = bump(body, "fish", "fish_dark", 0.08, 0.1)
    g += bump([(-0.28, 0.0), (-0.5, 0.22), (-0.5, -0.22)], "fish_dark", None, 0.06, 0.04)
    g += flat(circle2(0.24, 0.06, 0.05, 6), "black", 0.02).xf(T(0, 0, -0.16))
    g += flat([(0.0, 0.2), (0.12, 0.35), (-0.1, 0.24)], "fish_dark", 0.05)
    return g


def ic_anchor(col="anchor"):
    g = Geo()
    g += flat([(-0.05, -0.32), (0.05, -0.32), (0.05, 0.32), (-0.05, 0.32)], col, 0.07)
    g += flat([(-0.24, 0.16), (0.24, 0.16), (0.24, 0.24), (-0.24, 0.24)], col, 0.07)
    g += ring2_geo(0, 0.4, 0.04, 0.1, 8, -0.07, 0.0, col)
    arc_o = [(0.36 * math.cos(math.radians(a)), 0.36 * math.sin(math.radians(a)) - 0.06) for a in range(200, 341, 20)]
    arc_i = [(0.27 * math.cos(math.radians(a)), 0.27 * math.sin(math.radians(a)) - 0.06) for a in range(340, 199, -20)]
    g += flat(arc_o + arc_i, col, 0.07)
    g += flat([(0.34, -0.18), (0.44, -0.06), (0.28, -0.1)], col, 0.07)
    g += flat([(-0.34, -0.18), (-0.28, -0.1), (-0.44, -0.06)], col, 0.07)
    return g


def ic_scarab():
    g = Geo()
    for sx in (-1, 1):
        for k, y in enumerate((0.12, -0.06, -0.22)):
            g += rod((0, y, -0.03), (sx * 0.38, y + 0.08 - 0.1 * k, -0.03), 0.03, "gold", 4)
    g += bump(circle2(0, -0.08, 0.27, 10, sx=0.85, sy=1.15), "lapis", "lapis_dark", 0.08, 0.1)
    g += bump(circle2(0, 0.3, 0.13, 8), "turquoise", None, 0.06, 0.05)
    g += flat([(-0.015, -0.38), (0.015, -0.38), (0.015, 0.18), (-0.015, 0.18)], "gold", 0.02).xf(T(0, 0, -0.17))
    return g


def ic_ankh(col="gold", side="gold_dark"):
    g = ring2_geo(0, 0.25, 0.09, 0.19, 10, -0.08, 0.0, col)
    g.polys = [(p * np.array((1.0, 1.0, 1.0)), c) for p, c in g.polys]
    g = g.xf(M(T(0, 0.25, 0), S(0.85, 1.25, 1), T(0, -0.25, 0)))
    g += bump([(-0.36, 0.0), (0.36, 0.0), (0.36, 0.1), (-0.36, 0.1)], col, side, 0.08, 0.04)
    g += bump([(-0.06, 0.0), (0.06, 0.0), (0.11, -0.45), (-0.11, -0.45)], col, side, 0.08, 0.04)
    return g


def ic_eye():
    lens = [(-0.42, 0.0), (-0.2, 0.15), (0.05, 0.19), (0.3, 0.12), (0.42, 0.0), (0.2, -0.1), (-0.05, -0.12), (-0.25, -0.08)]
    g = flat(lens, "eye_white", 0.06)
    g += bump(circle2(0.02, 0.03, 0.11, 8), "lapis", None, 0.04, 0.05).xf(T(0, 0, -0.06))
    g += flat([(-0.45, 0.24), (0.42, 0.26), (0.42, 0.32), (-0.45, 0.3)], "lapis", 0.06)
    g += flat([(-0.05, -0.12), (0.03, -0.12), (0.0, -0.42), (-0.08, -0.4)], "lapis", 0.06)
    g += flat([(0.12, -0.1), (0.2, -0.1), (0.38, -0.36), (0.3, -0.38)], "lapis", 0.06)
    g += flat([(-0.42, 0.0), (-0.48, 0.03), (-0.55, -0.02), (-0.44, -0.05)], "lapis", 0.06)
    return g


def screen_panel(x0, x1, y0, y1, z, col, cols=3, divider=None, bevel_col=None):
    """Flat screen panel facing -Z with optional reel dividers."""
    g = box((x0, y0, z - 0.1), (x1, y1, z), col, skip=("+z",))
    if divider:
        w = (x1 - x0) / cols
        for k in range(1, cols):
            x = x0 + k * w
            g += box((x - 0.05, y0, z - 0.16), (x + 0.05, y1, z - 0.1), divider, skip=("+z",))
    return g


# =============================================================================================
# MODEL 5 - LuckyFruitsMachine (COMMON)
# =============================================================================================
def lucky_fruits():
    m = Model("LuckyFruitsMachine")
    cab = m.part("Cabinet")
    scr = m.part("Screen")
    lev = m.part("Lever", pivot=LEVER_PIVOT)
    top = m.part("Topper", pivot=(0, 7.1, 0))
    base = m.part("Base")

    base.add(box((-3, 0, -2.5), (3, 1, 2.5), "red_dark", 0.35, skip=("-y",)))

    body = rounded_rect2(-2.3, 1.0, 2.3, 7.1, 1.2)
    cab.add(extrude(body, -1.9, 2.1, "red", "red"), None)
    cab.add(extrude(rounded_rect2(-2.05, 3.5, 2.05, 6.85, 0.75, 0.3), -2.0, -1.9, "white", back=False))
    cab.add(box((-2.36, 2.15, -1.96), (2.36, 2.45, 2.16), "white", 0.06, skip=()))
    cab.add(deck(-2.1, 2.1, -1.9, "red", "white"))
    for x, c in ((-1.1, "lemon"), (-0.35, "leaf"), (0.4, "cherry")):
        cab.add(cyl(0.22, 0, 0.14, 8, c), M(T(x, 2.88, -2.32), RX(-62)))
    cab.add(box((-1.1, 1.25, -2.35), (1.1, 1.8, -1.9), "white", 0.1, skip=("+z",)))
    cab.add(box((-0.85, 1.55, -2.37), (0.85, 1.72, -2.1), "charcoal", skip=("+z", "-y")))
    cab.add(cyl(0.6, 0, 0.08, 10, "white"), M(T(2.3, 4.2, 0.3), RZ(-90)))
    # little cherry badge on each side
    for sx in (-1, 1):
        cab.add(ic_cherry().xf(M(FACE(90 * sx), T(0, 4.8, -2.3), S(1.3))), None)

    z = -2.0
    scr.add(screen_panel(-1.8, 1.8, 3.8, 6.55, z, "screen_cream", 3, "red"))
    for x, icon in ((-1.2, ic_cherry), (0.0, ic_lemon), (1.2, ic_melon)):
        scr.add(on_front(icon(), x, 5.15, z - 0.1, 1.1))
    scr.add(box((-1.8, 5.05, z - 0.13), (-1.7, 5.25, z - 0.1), "red", skip=("+z",)))
    scr.add(box((1.7, 5.05, z - 0.13), (1.8, 5.25, z - 0.1), "red", skip=("+z",)))

    # Lever (local coordinates are relative to the pivot)
    px, py, pz = LEVER_PIVOT
    lev.add(lever_hub("white", "red").xf(T(px, py, pz)))
    lev.add(rod((px, py, pz), (px, py + 2.65, pz), 0.12, "steel", 6))
    lev.add(sphere(0.38, 10, 6, "red"), T(px, py + 2.95, pz))

    # Topper: giant cherry pair
    ty = 7.1
    for x, z0 in ((-0.55, -0.1), (0.55, 0.1)):
        top.add(sphere(0.62, 10, 6, "cherry"), T(x, ty + 0.62, z0))
        top.add(sphere(0.14, 6, 3, "white"), T(x - 0.22, ty + 0.9, z0 - 0.48))
        top.add(rod((x * 0.8, ty + 1.15, z0), (0.05, ty + 1.75, 0), 0.08, "leaf_dark", 6))
    top.add(puffy(circle2(0, 0, 0.35, 8, sx=1.4, sy=0.6), 0.08, 0.1, "leaf", "leaf_dark"), M(T(0.42, ty + 1.68, 0), RZ(20)))
    return m


# =============================================================================================
# MODEL 6 - OceanTreasureMachine (RARE)
# =============================================================================================
def scallop(r=1.0, ribs=5, col="shell", col2="shell_dark", t=0.12):
    g = Geo()
    for k in range(ribs):
        a0 = math.radians(25 + 130 * k / ribs)
        a1 = math.radians(25 + 130 * (k + 1) / ribs)
        am = (a0 + a1) / 2
        poly = [(0, -0.15), (r * math.cos(a0), r * math.sin(a0) - 0.15), (r * 1.06 * math.cos(am), r * 1.06 * math.sin(am) - 0.15),
                (r * math.cos(a1), r * math.sin(a1) - 0.15)]
        g += bump(poly, col if k % 2 == 0 else col2, col2, t, 0.1)
    g += bump([(-0.2, -0.3), (0.2, -0.3), (0.12, -0.08), (-0.12, -0.08)], col2, None, t, 0.05)
    return g


def coral_branch(col="coral", side="coral_dark", t=0.25):
    poly = [(-0.12, 0.0), (0.12, 0.0), (0.1, 0.45), (0.38, 0.75), (0.42, 1.1), (0.3, 1.12), (0.26, 0.82),
            (0.08, 0.66), (0.06, 1.28), (-0.08, 1.3), (-0.1, 0.62), (-0.3, 0.86), (-0.34, 1.0), (-0.46, 0.96),
            (-0.4, 0.74), (-0.12, 0.42)]
    return extrude(poly, -t / 2, t / 2, col, side)


def ocean_treasure():
    m = Model("OceanTreasureMachine")
    cab = m.part("Cabinet")
    scr = m.part("Screen")
    lev = m.part("Lever", pivot=LEVER_PIVOT)
    top = m.part("Topper", pivot=(0, 7.0, 0))
    base = m.part("Base")

    base.add(box((-3, 0, -2.5), (3, 0.8, 2.5), "teal_dark", 0.3, skip=("-y",)))
    base.add(box((-2.9, 0.8, -2.4), (2.9, 1.0, 2.4), "foam", 0.08, skip=("-y",)))
    for k, x in enumerate(np.linspace(-2.6, 2.6, 9)):
        base.add(dome(0.16 + 0.06 * (k % 2), 6, 2, "aqua_light"), M(T(x, 0.42, -2.5), RX(-90)))

    body = rounded_rect2(-2.3, 1.0, 2.3, 7.0, 1.7)
    cab.add(extrude(body, -1.9, 2.1, "aqua", "teal"))
    cab.add(extrude(rounded_rect2(-2.12, 1.15, 2.12, 6.82, 1.55, 0.2), -1.97, -1.9, "teal", back=False))
    cab.add(box((-2.36, 2.2, -2.0), (2.36, 2.5, 2.16), "foam", 0.08))
    for x in np.linspace(-2.0, 2.0, 7):
        cab.add(sphere(0.17, 6, 3, "foam"), T(x, 2.55, -2.02))
    cab.add(deck(-2.0, 2.0, -1.97, "teal_dark", "aqua_light"))
    for x, c in ((-1.0, "shell"), (0.0, "pearl"), (1.0, "shell")):
        cab.add(sphere(0.22, 8, 4, c), M(T(x, 2.9, -2.3), RX(-62), S(1, 0.55, 1)))
    cab.add(box((-1.15, 1.2, -2.35), (1.15, 1.85, -1.97), "brass", 0.12, skip=("+z",)))
    cab.add(box((-0.9, 1.6, -2.37), (0.9, 1.78, -2.1), "ocean_deep", skip=("+z", "-y")))
    # porthole ring with bolts
    ring = [(1.36, 0.0), (1.8, 0.0), (1.86, 0.18), (1.8, 0.36), (1.36, 0.36), (1.32, 0.18), (1.36, 0.0)]
    cab.add(lathe(ring, 20, lambda i, j: None if j == 0 else "brass").xf(M(T(0, 5.0, -1.97), UP_TO_FRONT())))
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        cab.add(sphere(0.1, 6, 3, "gold_light"), T(1.58 * math.cos(a), 5.0 + 1.58 * math.sin(a), -2.33))
    # seashells, coral and a starfish
    cab.add(scallop(1.0).xf(M(FACE(-90), T(0.2, 4.5, -2.3))))
    cab.add(scallop(0.6).xf(M(FACE(90), T(-0.6, 6.0, -2.3))))
    for sx in (-1, 1):
        cab.add(coral_branch().xf(M(T(sx * 1.95, 1.0, -2.25), RY(sx * 20), S(sx * 0.95, 1.0, 1))))
    cab.add(puffy_star(0.45, 0.2, 0.12, 0.12, "fish", "fish_dark", back=False), M(T(1.55, 6.2, -2.0), RZ(12)))
    cab.add(cyl(0.6, 0, 0.08, 10, "brass"), M(T(2.3, 4.2, 0.3), RZ(-90)))

    z = -1.97
    scr.add(lathe([(1.38, 0.0), (1.38, 0.1), (0.0, 0.1)], 20, lambda i, j: "ocean_mid" if j == 1 else "ocean_deep").xf(
        M(T(0, 5.0, z), UP_TO_FRONT())))
    zf = z - 0.1
    scr.add(flat([(-1.22, 4.35), (1.22, 4.35), (0.9, 4.0), (-0.9, 4.0)], "sand", 0.03).xf(T(0, 0, zf)))
    for x, icon in ((-0.78, ic_pearl), (0.0, ic_fish), (0.78, ic_anchor)):
        scr.add(on_front(icon(), x, 5.05, zf, 0.82))
    for x, y, r in ((-0.35, 5.75, 0.07), (0.45, 5.85, 0.09), (0.15, 6.05, 0.05), (-0.75, 5.6, 0.05)):
        scr.add(flat(circle2(x, y, r, 6), "aqua_light", 0.03).xf(T(0, 0, zf)))

    # Lever: trident
    px, py, pz = LEVER_PIVOT
    lev.add(lever_hub("teal", "brass").xf(T(px, py, pz)))
    lev.add(rod((px, py, pz), (px, py + 2.3, pz), 0.11, "brass", 6))
    for y in (0.6, 1.2, 1.8):
        lev.add(cyl(0.15, 0, 0.12, 6, "aqua"), T(px, py + y, pz))
    hy = py + 2.3
    lev.add(box((px - 0.1, hy, pz - 0.5), (px + 0.1, hy + 0.18, pz + 0.5), "gold", 0.04))
    for dz, h in ((-0.42, 0.55), (0.0, 0.75), (0.42, 0.55)):
        lev.add(box((px - 0.08, hy + 0.18, pz + dz - 0.07), (px + 0.08, hy + 0.18 + h, pz + dz + 0.07), "gold", 0.02))
        lev.add(pyramid(0.16, 0.32, 4, "gold_light"), T(px, hy + 0.18 + h, pz + dz))

    # Topper: open clam shell with a big pearl
    ty = 7.0

    def ribs(i, j):
        return "shell" if i % 2 == 0 else "shell_dark"
    dish = [(0.0, 0.0), (0.6, 0.06), (1.05, 0.3), (1.1, 0.45), (1.0, 0.47), (0.55, 0.22), (0.0, 0.16)]
    rm = lambda i: 1.0 if i % 2 == 0 else 0.93
    top.add(lathe(dish, 16, ribs, rmod=rm), T(0, ty, 0))
    lid = lathe(dish, 16, ribs, rmod=rm).xf(S(1, -1, 1))
    top.add(lid, M(T(0, ty + 0.47, 1.05), RX(52), T(0, 0, -1.05)))
    top.add(sphere(0.48, 10, 6, "pearl"), T(0, ty + 0.62, -0.12))
    top.add(sphere(0.12, 6, 3, "white"), T(-0.18, ty + 0.85, -0.5))
    return m


# =============================================================================================
# MODEL 7 - NeonFortuneMachine (EPIC)
# =============================================================================================
NEON_BODY = [(-2.3, 1.0), (2.3, 1.0), (2.3, 5.8), (1.9, 6.9), (1.1, 7.3), (-1.1, 7.3), (-1.9, 6.9), (-2.3, 5.8)]


def strip_along(p0, p1, w, z0, z1, col, inset=0.0, facing_back=False):
    """Thin neon bar following a 2D segment on the front plane (x,y) between z0..z1."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    L = np.linalg.norm(d)
    d /= L
    n = np.array((-d[1], d[0]))
    a = p0 + n * inset
    b = p1 + n * inset
    poly = [a - n * w / 2, b - n * w / 2, b + n * w / 2, a + n * w / 2]
    return extrude([tuple(q) for q in poly], z0, z1, col, front=not facing_back, back=facing_back)


def neon_fortune():
    m = Model("NeonFortuneMachine")
    cab = m.part("Cabinet")
    scr = m.part("Screen")
    lev = m.part("Lever", pivot=LEVER_PIVOT)
    top = m.part("Topper", pivot=(0, 7.3, 0))
    base = m.part("Base")
    neon = m.part("NeonStrips", neon=True)

    base.add(box((-2.95, 0, -2.45), (2.95, 0.85, 2.45), "black_soft", 0.3, skip=("-y",)))
    base.add(box((-2.75, 0.85, -2.3), (2.75, 1.0, 2.3), "charcoal", 0.05, skip=("-y",)))

    cab.add(extrude(NEON_BODY, -1.9, 2.1, "black", "black_soft"))
    # chamfered screen bezel
    cab.add(box((-2.05, 3.55, -2.05), (2.05, 6.7, -1.9), "charcoal_light", 0.12, skip=("+z",)))
    cab.add(deck(-2.0, 2.0, -1.9, "black_soft", "charcoal_light"))
    # speaker grilles
    for x0 in (-1.9, 0.5):
        for k in range(4):
            y = 1.35 + 0.22 * k
            cab.add(box((x0, y, -2.0), (x0 + 1.4, y + 0.1, -1.9), "charcoal_light", skip=("+z",)))
    # angular side panels
    for sx in (-1, 1):
        x = sx * 2.3
        g = extrude([(-1.2, 1.4), (1.4, 1.4), (1.6, 5.2), (-1.4, 5.4)], -0.06, 0.0, "charcoal", back=False)
        cab.add(g, M(FACE(90 * sx), T(0.0, 0.0, -2.3), RY(0)))
    cab.add(cyl(0.6, 0, 0.08, 6, "charcoal_light"), M(T(2.3, 4.2, 0.3), RZ(-90)))

    # Neon strips: front outline, side edges, base glow, bezel, buttons
    cols = ["neon_magenta", "neon_cyan", "neon_purple"]
    edges = list(zip(NEON_BODY, NEON_BODY[1:] + NEON_BODY[:1]))[1:]
    for k, (p, q) in enumerate(edges):
        neon.add(strip_along(p, q, 0.12, -1.98, -1.9, cols[k % 3], inset=0.1))
        pb = [(x, y) for x, y in (p, q)]
        neon.add(strip_along(pb[0], pb[1], 0.12, 2.1, 2.18, cols[(k + 1) % 3], inset=0.1, facing_back=True))
    for sx in (-1, 1):
        for zc in (-1.3, 1.5):
            lo_x, hi_x = (2.3, 2.38) if sx > 0 else (-2.38, -2.3)
            neon.add(box((lo_x, 1.3, zc - 0.06), (hi_x, 5.6, zc + 0.06), "neon_purple" if zc > 0 else "neon_cyan",
                         skip=("-x" if sx > 0 else "+x",)))
    neon.add(box((-2.8, 0.6, -2.5), (2.8, 0.72, -2.45), "neon_cyan", skip=("+z",)))
    neon.add(box((-3.0, 0.6, -2.35), (-2.95, 0.72, 2.35), "neon_cyan", skip=("+x",)))
    neon.add(box((2.95, 0.6, -2.35), (3.0, 0.72, 2.35), "neon_cyan", skip=("-x",)))
    neon.add(box((-2.8, 0.6, 2.45), (2.8, 0.72, 2.5), "neon_cyan", skip=("-z",)))
    for (x0, y0), (x1, y1) in (((-1.95, 3.65), (1.95, 3.65)), ((1.95, 3.65), (1.95, 6.6)), ((1.95, 6.6), (-1.95, 6.6)), ((-1.95, 6.6), (-1.95, 3.65))):
        neon.add(strip_along((x0, y0), (x1, y1), 0.09, -2.12, -2.05, "neon_cyan"))
    for x, c in ((-1.1, "neon_magenta"), (-0.35, "neon_cyan"), (0.4, "neon_purple"), (1.15, "neon_magenta")):
        neon.add(box((x - 0.25, 0, -0.18), (x + 0.25, 0.14, 0.18), c, 0.04, skip=("-y",)), M(T(0, 2.86, -2.27), RX(-62)))

    z = -2.05
    scr.add(screen_panel(-1.85, 1.85, 3.75, 6.5, z, "holo_deep", 3))
    zf = z - 0.1
    for k in range(12):
        y = 3.85 + k * 0.22
        scr.add(flat([(-1.82, y), (1.82, y), (1.82, y + 0.05), (-1.82, y + 0.05)], "holo_purple" if k % 3 else "holo_line", 0.01).xf(T(0, 0, zf)))
    for k in (1, 2):
        x = -1.85 + k * 3.7 / 3
        scr.add(flat([(x - 0.04, 3.75), (x + 0.04, 3.75), (x + 0.04, 6.5), (x - 0.04, 6.5)], "holo", 0.04).xf(T(0, 0, zf)))
    scr.add(flat([(-1.85, 5.05), (1.85, 5.05), (1.85, 5.1), (-1.85, 5.1)], "holo_line", 0.03).xf(T(0, 0, zf)))
    for x in (-1.23, 0.0, 1.23):
        scr.add(on_front(ic_seven(), x, 5.12, zf - 0.01, 0.95))
        scr.add(on_front(ic_diamond(), x, 6.05, zf - 0.01, 0.62))
        scr.add(on_front(ic_diamond("holo", "holo_purple"), x, 4.2, zf - 0.01, 0.62))

    px, py, pz = LEVER_PIVOT
    lev.add(lever_hub("chrome", "neon_cyan").xf(T(px, py, pz)))
    lev.add(rod((px, py, pz), (px, py + 1.3, pz), 0.12, "chrome", 6))
    lev.add(rod((px, py + 1.3, pz), (px, py + 2.45, pz - 0.25), 0.11, "chrome", 6))
    lev.add(cyl(0.18, 0, 0.22, 6, "steel"), T(px, py + 1.2, pz))
    lev.add(lathe([(0.12, 0), (0.3, 0.18), (0.3, 0.26)], 8, "chrome").xf(M(T(px, py + 2.42, pz - 0.25))))
    lev.add(sphere(0.4, 10, 6, "neon_magenta"), T(px, py + 2.75, pz - 0.25))

    ty = 7.3
    top.add(lathe([(0.75, 0.0), (0.75, 0.18), (0.6, 0.26), (0.0, 0.26)], 6, lambda i, j: "neon_cyan" if j == 1 else "black_soft"), T(0, ty, 0))
    plate = [(-1.05, 0.26), (1.05, 0.26), (1.2, 0.75), (0.85, 1.32), (-0.85, 1.32), (-1.2, 0.75)]
    top.add(extrude(plate, -0.2, 0.2, "black", "charcoal_light"), T(0, ty, 0))
    for zz, rot in ((-0.2, 0), (0.2, 180)):
        top.add(ic_seven("neon_magenta", "seven").xf(M(T(0, ty + 0.78, zz), RY(rot), S(1.05))))
        for (p, q) in zip(plate, plate[1:] + plate[:1]):
            top.add(strip_along(p, q, 0.07, -0.05, 0.0, "neon_cyan", inset=0.07).xf(M(T(0, ty, zz), RY(rot))))
    top.add(rod((0.6, ty + 1.2, 0), (0.75, ty + 1.62, 0), 0.04, "chrome", 4))
    top.add(sphere(0.09, 6, 3, "neon_cyan"), T(0.76, ty + 1.66, 0))
    return m


# =============================================================================================
# MODEL 8 - GoldenPharaohMachine (LEGENDARY)
# =============================================================================================
def column(y0, y1):
    bands = []
    prof = [(0.48, y0), (0.48, y0 + 0.22), (0.36, y0 + 0.3)]
    n = 6
    ys = np.linspace(y0 + 0.3, y1 - 0.75, n + 1)
    for k in range(1, n + 1):
        prof.append((0.33 - 0.02 * k / n, ys[k]))
    prof += [(0.52, y1 - 0.2), (0.56, y1 - 0.1), (0.56, y1)]

    def col(i, j):
        if 2 <= j < 2 + n:
            return "lapis" if (j % 2) else "gold"
        if j == 2 + n:
            return "turquoise" if i % 2 else "gold"
        return "gold"
    return lathe(prof, 8, col)


def glyph(kind):
    if kind == "ankh":
        return ic_ankh("lapis", "lapis_dark")
    if kind == "eye":
        return flat([(-0.42, 0.0), (-0.2, 0.15), (0.2, 0.15), (0.42, 0.0), (0.2, -0.12), (-0.2, -0.12)], "lapis", 0.05) + \
            flat([(-0.42, 0.24), (0.42, 0.24), (0.42, 0.31), (-0.42, 0.31)], "lapis", 0.05)
    if kind == "bird":
        return flat([(-0.35, -0.3), (0.0, -0.1), (0.3, 0.3), (0.12, 0.35), (0.0, 0.12), (-0.25, 0.0), (-0.4, -0.2)], "lapis", 0.05)
    if kind == "wave":
        pts = [(-0.4 + 0.1 * k, 0.06 if k % 2 else -0.06) for k in range(9)]
        return flat(pts + [(x, y - 0.1) for x, y in reversed(pts)], "lapis", 0.05)
    return flat(circle2(0, 0, 0.22, 8), "turquoise", 0.05)


def wing_poly(span, side):
    pts = [(0.0, 0.0), (span * 0.35, 0.25), (span * 0.75, 0.5), (span, 0.75), (span * 0.95, 0.5),
           (span * 0.7, 0.05), (span * 0.45, -0.25), (span * 0.2, -0.35), (0.0, -0.2)]
    return [(side * x, y) for x, y in pts]


def golden_pharaoh():
    m = Model("GoldenPharaohMachine")
    cab = m.part("Cabinet")
    scr = m.part("Screen")
    lev = m.part("Lever", pivot=(2.55, 4.2, 0.3))
    top = m.part("Topper", pivot=(0, 7.15, 0))
    base = m.part("Base")
    wings = m.part("Wings", pivot=(0, 7.15, 0))

    # Base: stepped temple plinth with lapis inlays
    base.add(box((-3, 0, -2.5), (3, 0.45, 2.5), "gold_dark", 0.1, skip=("-y",), top="gold"))
    base.add(box((-2.75, 0.45, -2.3), (2.75, 1.0, 2.3), "gold", 0.08, skip=("-y",), top="gold_light"))
    for k, x in enumerate(np.linspace(-2.45, 2.45, 8)):
        base.add(box((x - 0.18, 0.58, -2.34), (x + 0.18, 0.86, -2.3), "lapis" if k % 2 == 0 else "turquoise", skip=("+z",)))
    base.add(box((-1.2, 0, -2.85), (1.2, 0.3, -2.5), "gold_dark", 0.06, skip=("-y", "+z"), top="gold"))

    # Cabinet: tapered pylon, cornice, columns, hieroglyphs, winged sun
    cab.add(frustum_box(4.6, 3.9, 4.1, 3.55, 1.0, 6.5, "gold", skip=("-y", "+y"), zc=0.15))
    cab.add(box((-2.12, 6.5, -1.55), (2.12, 6.68, 1.9), "lapis", skip=("-y",)))
    cab.add(frustum_box(4.24, 3.45, 4.75, 3.9, 6.68, 7.0, "gold", skip=("-y",), zc=0.18, top="gold_light"))
    cab.add(box((-2.4, 7.0, -1.8), (2.4, 7.15, 2.15), "gold_light", 0.05, skip=("-y",)))
    for sx in (-1, 1):
        cab.add(column(1.0, 6.5), T(sx * 2.05, 0, -2.05))
    # lapis screen frame
    cab.add(box((-1.8, 3.45, -1.92), (1.8, 6.15, -1.75), "lapis", 0.08, skip=("+z",)))
    cab.add(deck(-1.7, 1.7, -1.8, "gold_dark", "gold"))
    for x, c in ((-0.9, "lapis"), (0.0, "turquoise"), (0.9, "lapis")):
        cab.add(sphere(0.22, 8, 4, c), M(T(x, 2.88, -2.18), RX(-62), S(1, 0.5, 1)))
    cab.add(box((-1.0, 1.25, -2.15), (1.0, 1.8, -1.8), "gold_dark", 0.1, skip=("+z",)))
    cab.add(box((-0.8, 1.58, -2.17), (0.8, 1.74, -1.95), "lapis_dark", skip=("+z", "-y")))
    # winged sun disk above the screen
    cab.add(sphere(0.2, 8, 4, "gold_light"), T(0, 6.33, -1.95))
    for side in (-1, 1):
        cab.add(flat([(side * 0.15, 0.06), (side * 1.25, 0.12), (side * 1.1, -0.04), (side * 0.15, -0.1)], "lapis", 0.06)
                .xf(T(0, 6.33, -1.72)))
    # hieroglyph columns on both sides
    tilt = math.degrees(math.atan(0.25 / 5.5))
    kinds = ["eye", "ankh", "bird", "wave", "sun", "ankh", "eye", "bird"]
    for sx in (-1, 1):
        zs = (-1.0, 1.3) if sx > 0 else (-1.0, 0.15, 1.3)
        for ci, zc in enumerate(zs):
            for r in range(4):
                y = 1.9 + r * 1.1
                k = kinds[(r + ci * 3 + (sx > 0)) % len(kinds)]
                halfw = 2.3 - 0.25 * (y - 1.0) / 5.5
                # side face: local x runs along -Z*sx, so the glyph column sits at depth zc
                cab.add(glyph(k).xf(S(0.75)), M(T(sx * halfw, y, zc), RZ(-sx * tilt), FACE(90 * sx)))
        for zline in (-0.45, 0.75) if sx < 0 else (-0.25, 0.75):
            cab.add(box((-0.05, 1.4, -0.04), (0.05, 6.2, 0.0), "lapis", skip=("+z",)),
                    M(T(sx * 2.21, 0, zline), RZ(-sx * tilt), FACE(90 * sx)))
    cab.add(cyl(0.55, 0, 0.08, 10, "lapis"), M(T(2.16, 4.2, 0.3), RZ(-90)))

    # Screen: 3x3 reels of scarabs, ankhs and eyes
    z = -1.92
    scr.add(screen_panel(-1.55, 1.55, 3.6, 6.0, z, "egypt_night", 3, "gold"))
    zf = z - 0.16
    grid = [[ic_eye, ic_scarab, ic_ankh], [ic_scarab, ic_ankh, ic_eye], [ic_ankh, ic_eye, ic_scarab]]
    for r, row in enumerate(grid):
        for c, icon in enumerate(row):
            scr.add(on_front(icon(), -1.03 + 1.03 * c, 5.45 - 0.83 * r, zf + 0.06, 0.62))
    scr.add(box((-1.55, 4.38, z - 0.14), (1.55, 4.43, z - 0.1), "gold", skip=("+z",)))
    scr.add(box((-1.55, 5.17, z - 0.14), (1.55, 5.22, z - 0.1), "gold", skip=("+z",)))

    # Lever: golden scepter
    px, py, pz = 2.55, 4.2, 0.3
    lev.add(lever_hub("gold", "turquoise", x_in=-0.4, x_out=0.3).xf(T(px, py, pz)))
    lev.add(rod((px, py, pz), (px, py + 2.4, pz), 0.11, "gold", 6))
    for y in (0.55, 1.05, 1.55, 2.05):
        lev.add(cyl(0.15, 0, 0.13, 6, "lapis"), T(px, py + y, pz))
    lev.add(lathe([(0.1, 0.0), (0.3, 0.2), (0.34, 0.32), (0.26, 0.3)], 8, "gold_light"), T(px, py + 2.4, pz))
    lev.add(sphere(0.27, 8, 5, "lapis"), T(px, py + 2.88, pz))
    lev.add(pyramid(0.12, 0.35, 6, "gold_light"), T(px, py + 3.12, pz))

    # Topper: pharaoh mask on a lapis pedestal
    ty = 7.15
    top.add(box((-0.75, ty, -0.6), (0.75, ty + 0.22, 0.6), "lapis", 0.05, skip=("-y",)))
    nemes = [(-1.0, 0.22), (1.0, 0.22), (0.78, 0.9), (0.55, 1.5), (0.0, 1.78), (-0.55, 1.5), (-0.78, 0.9)]
    top.add(extrude(nemes, -0.42, 0.45, "gold", "gold_dark"), T(0, ty, 0))
    for k in range(4):
        y0 = 0.32 + 0.22 * k
        for sx in (-1, 1):
            top.add(flat([(sx * 0.56, y0), (sx * (0.97 - 0.07 * k), y0), (sx * (0.95 - 0.07 * k), y0 + 0.1), (sx * 0.56, y0 + 0.1)],
                         "lapis", 0.04), T(0, ty, -0.42))
    for k in range(3):
        y0 = 1.25 + 0.15 * k
        top.add(flat([(-0.55 + 0.12 * k, y0), (0.55 - 0.12 * k, y0), (0.5 - 0.12 * k, y0 + 0.07), (-0.5 + 0.12 * k, y0 + 0.07)],
                     "lapis", 0.04), T(0, ty, -0.42))
    face = circle2(0, 0.0, 0.42, 10, sx=1.0, sy=1.22)
    top.add(puffy(face, 0.1, 0.22, "gold_light", "gold"), T(0, ty + 0.9, -0.5))
    for sx in (-1, 1):
        top.add(flat([(-0.15, 0.0), (0.0, 0.06), (0.15, 0.0), (0.0, -0.05)], "black", 0.03), T(sx * 0.17, ty + 1.02, -0.79))
        top.add(flat([(-0.17, 0.08), (0.2, 0.1), (0.2, 0.14), (-0.17, 0.12)], "lapis", 0.03), T(sx * 0.17, ty + 1.02, -0.79))
    top.add(flat([(-0.05, 0.0), (0.05, 0.0), (0.07, -0.22), (-0.07, -0.22)], "gold", 0.08), T(0, ty + 0.96, -0.74))
    top.add(extrude([(-0.13, 0.22), (0.13, 0.22), (0.1, 0.52), (-0.1, 0.52)], -0.62, -0.42, "lapis", "lapis_dark"), T(0, ty, 0))
    top.add(puffy([(-0.08, 0.0), (0.08, 0.0), (0.12, 0.25), (0.0, 0.36), (-0.12, 0.25)], 0.1, 0.06, "gold_light", "gold"),
            T(0, ty + 1.35, -0.62))
    top.add(sphere(0.07, 6, 3, "red"), T(0, ty + 1.62, -0.67))

    # Wings: spread golden wings with lapis / turquoise feather rows (spin with the topper)
    for side in (-1, 1):
        layers = [(2.2, "gold", 0.0, 0.0), (1.75, "lapis", 0.1, -0.06), (1.35, "turquoise", 0.25, -0.12), (0.95, "gold_light", 0.35, -0.18)]
        for span, col, dy, dz in layers:
            poly = wing_poly(span, side)
            w = extrude(poly, -0.07 + dz, 0.07, col, "gold_dark")
            wings.add(w, M(T(side * 0.85, ty + 0.68 + dy * 0.6, 0.1), RZ(side * 12)))
    return m
