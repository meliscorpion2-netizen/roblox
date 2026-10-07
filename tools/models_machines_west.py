"""Slot machines: WildWest (Common) and PirateFortune (Uncommon).

Same layout as tools/models_machines.py: 6 wide (X) x 5 deep (Z) x 9 tall (Y), pivot at the ground centre,
screen faces -Z.  Front art is authored as seen from +Z (+X = right); the build mirrors X once (mirror=True),
which makes the art read correctly from the -Z front and puts the lever on the player's right.
The lever pivots at its hub (LEVER_PIVOT, +X side before mirroring) and rotates around X; the topper pivots on
the vertical centre axis at the cabinet top.
"""
import math

import numpy as np

from casino_geo import (Geo, Model, M, T, RX, RY, RZ, S, FACE, box, lathe, cyl, sphere, dome, extrude, puffy,
                        puffy_star, coin, pyramid, circle2, star2, ring2_geo, add_colors)
from models_machines import LEVER_PIVOT, rounded_rect2, rod, flat, bump, on_front, deck, lever_hub

add_colors({
    # wild west: cartoon wood, desert screen, cowboy hat
    "west_plank_a": "#C97E3C", "west_plank_b": "#B56A2C", "west_wood_light": "#E8A764",
    "west_wood_dark": "#8A4C1F", "west_wood": "#A95F27", "west_wood_deep": "#5C3015",
    "west_hat": "#9A5626", "west_hat_dark": "#6B3816",
    "west_sky": "#5CC8F5", "west_sky_light": "#A9E9FB", "west_sand": "#F4C273", "west_sand_dark": "#E09A4A",
    "west_mesa": "#E0683C",
    # pirate: treasure chest, night sea screen, ship
    "west_chest_a": "#A9562A", "west_chest_b": "#93481F", "west_chest_dark": "#673014",
    "west_sea": "#1E9BC9", "west_sea_light": "#7FE0F2", "west_parch": "#FBE7B8", "west_parch_dark": "#D9AE6A",
    "west_parrot_blue": "#2D6CF0", "west_sail": "#FFF6E2", "west_hull": "#A3592A", "west_hull_dark": "#6A3416",
    "west_deck": "#E2A866",
})

DECK_TILT = -math.degrees(math.atan2(0.45, 0.7))     # RX angle turning +Y onto the sloped top of deck()


# ----------------------------------------------------------------------------- small helpers
def deck_spot(x, f, z_front):
    """Matrix placing a +Y-up object on the sloped top of deck(..., z_front, ...); f: 0 = front edge .. 1 = back."""
    return M(T(x, 3.0 + 0.45 * f, z_front - 0.7 + 0.7 * f), RX(DECK_TILT))


def arc_pts(cx, cy, r, a0, a1, n, sx=1.0, sy=1.0):
    return [(cx + sx * r * math.cos(math.radians(a)), cy + sy * r * math.sin(math.radians(a)))
            for a in np.linspace(a0, a1, n + 1)]


def arc_band(cx, cy, r_in, r_out, a0, a1, n, sx=1.0, sy=1.0):
    """Closed outline of a thick arc (C / U shapes)."""
    return arc_pts(cx, cy, r_out, a0, a1, n, sx, sy) + arc_pts(cx, cy, r_in, a1, a0, n, sx, sy)


def prism_zy(poly, x0, x1, cap, edge_col=None, caps=True):
    """Prism of a convex (z, y) side-view outline extruded along X.
    edge_col(i, p, q) -> colour (or None to skip) for the side face of edge i."""
    g = Geo()
    P = [np.array(p, float) for p in poly]
    if caps:
        g.add([(x0, y, z) for z, y in poly], cap, (-1, 0, 0))
        g.add([(x1, y, z) for z, y in poly], cap, (1, 0, 0))
    cen = np.mean(P, axis=0)
    for i in range(len(P)):
        p, q = P[i], P[(i + 1) % len(P)]
        c = edge_col(i, p, q) if callable(edge_col) else (edge_col or cap)
        if c is None:
            continue
        d = q - p
        n = np.array((d[1], -d[0]))
        if np.dot(n, (p + q) / 2 - cen) < 0:
            n = -n
        g.add([(x0, p[1], p[0]), (x1, p[1], p[0]), (x1, q[1], q[0]), (x0, q[1], q[0])], c, (0, n[1], n[0]))
    return g


def band_zy(inner, outer, x0, x1, col, skip_edges=()):
    """Raised strap following a (z, y) outline: outer skin + two thin side walls, between x0..x1."""
    g = Geo()
    cen = np.mean(np.array(inner, float), axis=0)
    n = len(inner)
    for i in range(n):
        if i in skip_edges:
            continue
        a, b = np.array(inner[i]), np.array(inner[(i + 1) % n])
        A, B = np.array(outer[i]), np.array(outer[(i + 1) % n])
        mid = (A + B) / 2 - cen
        g.add([(x0, A[1], A[0]), (x1, A[1], A[0]), (x1, B[1], B[0]), (x0, B[1], B[0])], col, (0, mid[1], mid[0]))
        for x, s in ((x0, -1), (x1, 1)):
            g.add([(x, a[1], a[0]), (x, b[1], b[0]), (x, B[1], B[0]), (x, A[1], A[0])], col, (s, 0, 0))
    return g


def ring_x(cz, cy, r_in, r_out, n, x0, x1, col):
    """Flat ring standing in the ZY plane (axis along X) between x0..x1."""
    return ring2_geo(0, 0, r_in, r_out, n, -0.5, 0.5, col).xf(M(T((x0 + x1) / 2, cy, cz), RY(90), S(1, 1, x1 - x0)))


def sheet(P, nu, nv, col, off, hint, side=None, back_col=None, edges=(True, True, True, True)):
    """Thin two-skinned surface.  P(i, j) -> point on the front skin (i in 0..nu, j in 0..nv); the back skin is the
    front shifted by `off`.  hint(p) -> rough outward normal of the front skin.  edges = (i=0, i=nu, j=0, j=nv)."""
    off = np.asarray(off, float)
    F = [[np.asarray(P(i, j), float) for j in range(nv + 1)] for i in range(nu + 1)]
    B = [[F[i][j] + off for j in range(nv + 1)] for i in range(nu + 1)]
    cen = np.mean([F[i][j] for i in range(nu + 1) for j in range(nv + 1)], axis=0) + off / 2
    colf = col if callable(col) else (lambda i, j: col)
    g = Geo()
    for i in range(nu):
        for j in range(nv):
            for G, sgn, c in ((F, 1, colf(i, j)), (B, -1, back_col or colf(i, j))):
                a, b, cc, d = G[i][j], G[i + 1][j], G[i + 1][j + 1], G[i][j + 1]
                for tri in ((a, b, cc), (a, cc, d)):
                    g.add(list(tri), c, sgn * np.asarray(hint(np.mean(tri, axis=0)), float))
    sc = side or (col if not callable(col) else colf(0, 0))

    def edge(fs, bs):
        for k in range(len(fs) - 1):
            quad = [fs[k], fs[k + 1], bs[k + 1], bs[k]]
            g.add(quad, sc, np.mean(quad, axis=0) - cen)
    if edges[0]:
        edge([F[0][j] for j in range(nv + 1)], [B[0][j] for j in range(nv + 1)])
    if edges[1]:
        edge([F[nu][j] for j in range(nv + 1)], [B[nu][j] for j in range(nv + 1)])
    if edges[2]:
        edge([F[i][0] for i in range(nu + 1)], [B[i][0] for i in range(nu + 1)])
    if edges[3]:
        edge([F[i][nv] for i in range(nu + 1)], [B[i][nv] for i in range(nu + 1)])
    return g


def gem(r, col, side):
    """Small cut gem (octahedron-ish) standing on y=0."""
    g = lathe([(0.0, 0.0), (r, r * 0.9), (r * 0.62, r * 1.45), (0.0, r * 1.45)], 6,
              lambda i, j: side if j == 0 else col)
    return g


def coin_stack(n, r=0.2, h=0.075):
    g = Geo()
    for k in range(n):
        g += cyl(r, k * h, (k + 1) * h - 0.005, 10, "gold_dark" if k % 2 else "gold", topcol="gold_light").xf(
            T(0.012 * ((k * 7) % 3 - 1), 0, 0.012 * ((k * 5) % 3 - 1)))
    return g


# ----------------------------------------------------------------------------- icons (unit size ~1, facing -Z)
def ic_horseshoe(col="gold", side="gold_dark", hole="west_wood_deep"):
    g = flat(arc_band(0, 0.04, 0.24, 0.44, 148, 392, 12, sx=0.9), side, 0.1)
    g += flat(arc_band(0, 0.04, 0.28, 0.4, 152, 388, 12, sx=0.9), col, 0.04).xf(T(0, 0, -0.1))
    for a in (148, 392):                                     # calkins (toe tips)
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        x, y = 0.9 * 0.34 * c, 0.04 + 0.34 * s
        g += box((x - 0.11, y - 0.02, -0.16), (x + 0.11, y + 0.1, 0.0), col, 0.03, skip=("+z",))
    for a in (185, 222, 258, 282, 318, 355):                 # nail holes
        c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
        x, y = 0.9 * 0.34 * c, 0.04 + 0.34 * s
        hole_pts = [(x + dx * c - dy * s, y + dx * s + dy * c) for dx, dy in ((-0.03, -0.018), (0.03, -0.018), (0.03, 0.018), (-0.03, 0.018))]
        g += flat(hole_pts, hole, 0.02).xf(T(0, 0, -0.14))
    return g


def cactus_outline():
    """Saguaro silhouette: trunk with a low left arm and a high right arm (one concave outline)."""
    return ([(-0.13, -0.42), (0.13, -0.42), (0.13, 0.02)] + arc_pts(0.29, 0.09, 0.07, 270, 360, 3)
            + arc_pts(0.29, 0.31, 0.07, 0, 180, 4) + [(0.22, 0.16), (0.13, 0.16)] + arc_pts(0, 0.3, 0.13, 0, 180, 6)
            + [(-0.13, 0.0)] + arc_pts(-0.29, 0.17, 0.07, 0, 180, 4) + arc_pts(-0.29, -0.07, 0.07, 180, 270, 3)
            + [(-0.13, -0.14)])


def ic_cactus():
    g = extrude(cactus_outline(), -0.12, 0.0, "leaf", "leaf_dark", back=False)
    zf = -0.12
    for x0, y0, x1, y1 in ((-0.065, -0.36, -0.035, 0.3), (0.035, -0.36, 0.065, 0.3),
                           (-0.305, -0.06, -0.275, 0.17), (0.275, 0.07, 0.305, 0.3)):
        g += flat([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "leaf_dark", 0.02).xf(T(0, 0, zf))
    g += puffy_star(0.1, 0.045, 0.05, 0.04, "pink", "red", back=False).xf(T(0, 0.43, -0.12))
    g += flat(arc_pts(0, -0.42, 0.3, 0, 180, 8, sy=0.45), "west_sand_dark", 0.05).xf(T(0, 0, -0.13))
    return g


def ic_hat(col="west_hat", side="west_hat_dark"):
    upper = [(-0.52, 0.11), (-0.42, 0.01), (-0.28, -0.05), (0.0, -0.07), (0.28, -0.05), (0.42, 0.01), (0.52, 0.11)]
    lower = [(0.49, 0.05), (0.4, -0.08), (0.26, -0.15), (0.0, -0.18), (-0.26, -0.15), (-0.4, -0.08), (-0.49, 0.05)]
    g = extrude(upper + lower, -0.16, -0.02, col, side, back=False)
    crown = [(-0.27, -0.06), (0.27, -0.06), (0.31, 0.24), (0.21, 0.37), (0.08, 0.33), (0.0, 0.27), (-0.08, 0.33),
             (-0.21, 0.37), (-0.31, 0.24)]
    g += extrude(crown, -0.1, 0.0, col, side, back=False)
    g += flat([(-0.285, 0.02), (0.285, 0.02), (0.29, 0.11), (-0.29, 0.11)], "red", 0.02).xf(T(0, 0, -0.1))
    g += puffy_star(0.07, 0.03, 0.03, 0.03, "gold", "gold_dark", back=False).xf(T(0, 0.065, -0.135))
    g += flat([(-0.18, 0.16), (-0.1, 0.16), (-0.12, 0.3), (-0.17, 0.28)], "west_wood_light", 0.015).xf(T(0, 0, -0.1))
    return g


def ic_coin():
    g = coin(0.27, 0.1, emblem=True).xf(T(0.17, 0.17, 0.0))
    g += coin(0.36, 0.13, emblem=True).xf(T(-0.06, -0.06, -0.05))
    g += puffy([(0, 0.11), (0.03, 0.03), (0.11, 0), (0.03, -0.03), (0, -0.11), (-0.03, -0.03), (-0.11, 0), (-0.03, 0.03)],
               0.03, 0.02, "white", None, back=False, center=(0, 0)).xf(T(0.32, 0.36, -0.12))
    return g


def ic_map():
    g = Geo()
    sheet_pts = [(-0.36, -0.28), (0.36, -0.28), (0.36, 0.28), (-0.36, 0.28)]
    g += flat(sheet_pts, "west_parch", 0.05)
    for sx in (-1, 1):                                       # rolled ends
        g += rod((sx * 0.38, -0.31, -0.05), (sx * 0.38, 0.31, -0.05), 0.075, "west_parch_dark", 6)
    zf = -0.07
    g += flat(circle2(-0.12, 0.04, 0.15, 9, sx=1.2, sy=0.9), "leaf", 0.02).xf(T(0, 0, zf))
    g += flat(circle2(-0.08, 0.06, 0.06, 6), "leaf_dark", 0.01).xf(T(0, 0, zf - 0.02))
    for k, (x, y) in enumerate(((-0.24, -0.16), (-0.12, -0.19), (0.0, -0.16), (0.09, -0.08))):
        g += flat([(x - 0.035, y - 0.015), (x + 0.035, y - 0.015), (x + 0.035, y + 0.015), (x - 0.035, y + 0.015)],
                  "west_wood_dark", 0.015).xf(M(T(0, 0, zf), T(x, y, 0), RZ(20 * (k % 2) - 5), T(-x, -y, 0)))
    for a in (45, -45):
        g += flat([(-0.1, -0.025), (0.1, -0.025), (0.1, 0.025), (-0.1, 0.025)], "red", 0.03).xf(
            M(T(0.2, 0.05, zf - 0.005), RZ(a)))
    g += flat([(0.25, 0.17), (0.31, 0.24), (0.27, 0.24), (0.25, 0.27), (0.23, 0.24), (0.19, 0.24)], "west_wood_dark", 0.015).xf(T(0, 0, zf))
    return g.xf(RZ(-8))


def ic_parrot():
    g = Geo()
    # perch + tail behind
    g += flat([(-0.26, -0.5), (-0.14, -0.53), (0.04, -0.2), (-0.08, -0.16)], "west_parrot_blue", 0.04).xf(T(0, 0, 0.0))
    g += flat([(-0.16, -0.46), (-0.06, -0.49), (0.06, -0.24), (-0.03, -0.2)], "lemon", 0.04).xf(T(0, 0, -0.04))
    g += box((-0.42, -0.36, -0.1), (0.42, -0.28, 0.0), "west_wood_dark", 0.02, skip=("+z",))
    # body + head
    g += bump(circle2(0.0, -0.05, 0.25, 12, sx=0.72, sy=1.0), "red", "red_dark", 0.08, 0.07).xf(
        M(T(0, -0.05, -0.04), RZ(-12), T(0, 0.05, 0)))
    g += bump(circle2(0.11, 0.27, 0.165, 10), "red", "red_dark", 0.08, 0.06).xf(T(0, 0, -0.04))
    zf = -0.19
    # wing (blue with a yellow shoulder band)
    wing = [(-0.12, 0.1), (0.04, 0.12), (0.1, 0.0), (0.04, -0.2), (-0.08, -0.34), (-0.16, -0.12)]
    g += flat(wing, "west_parrot_blue", 0.04).xf(T(0, 0, zf + 0.06))
    g += flat([(-0.12, 0.1), (0.04, 0.12), (0.08, 0.02), (-0.15, 0.0)], "lemon", 0.02).xf(T(0, 0, zf + 0.04))
    # face patch, eye, beak
    g += flat(circle2(0.17, 0.27, 0.085, 8), "white", 0.02).xf(T(0, 0, zf + 0.04))
    g += flat(circle2(0.18, 0.29, 0.035, 6), "black", 0.02).xf(T(0, 0, zf + 0.02))
    beak = [(0.24, 0.34), (0.33, 0.33), (0.39, 0.26), (0.38, 0.16), (0.33, 0.2), (0.25, 0.2)]
    g += extrude(beak, -0.16, -0.02, "gold", "gold_dark", back=False)
    # feet
    for x in (-0.06, 0.07):
        g += flat([(x - 0.04, -0.37), (x + 0.04, -0.37), (x + 0.03, -0.27), (x - 0.03, -0.27)], "gold_dark", 0.02).xf(T(0, 0, -0.1))
    return g


def cutlass():
    """Pirate sword pointing up (+Y), blade centred on the origin, facing -Z (back at z=0)."""
    g = Geo()
    blade = [(-0.055, -0.4), (0.055, -0.4), (0.08, 0.1), (0.1, 0.42), (0.04, 0.62), (-0.02, 0.5), (-0.05, 0.1)]
    g += extrude(blade, -0.06, 0.0, "chrome", "steel", back=False)
    g += box((-0.17, -0.48, -0.09), (0.17, -0.4, 0.0), "gold", 0.02, skip=("+z",))
    g += box((-0.045, -0.75, -0.08), (0.045, -0.48, 0.0), "red_dark", 0.015, skip=("+z",))
    g += sphere(0.065, 6, 3, "gold").xf(T(0, -0.79, -0.04))
    return g


def skull(col="white", shade="cream_dark", ink="black_soft"):
    g = bump(circle2(0, 0.08, 0.3, 12, sy=0.92), col, shade, 0.1, 0.05)
    g += bump(rounded_rect2(-0.17, -0.3, 0.17, -0.06, 0.0, 0.06, 3), col, shade, 0.1, 0.03)
    zf = -0.15
    for sx in (-1, 1):
        g += flat(circle2(sx * 0.11, 0.05, 0.085, 8, sy=1.1), ink, 0.03).xf(T(0, 0, zf))
    g += flat([(0.0, -0.06), (0.05, -0.15), (-0.05, -0.15)], ink, 0.03).xf(T(0, 0, zf))
    for x in (-0.08, 0.0, 0.08):
        g += flat([(x - 0.012, -0.29), (x + 0.012, -0.29), (x + 0.012, -0.19), (x - 0.012, -0.19)], ink, 0.02).xf(T(0, 0, -0.13))
    return g


def skull_swords():
    g = Geo()
    g += ring2_geo(0, 0, 0.5, 0.6, 14, -0.1, 0.12, "gold")
    g += extrude(circle2(0, 0, 0.5, 14), -0.06, 0.12, "black_soft", back=False)
    for a in (38, -38):
        g += cutlass().xf(M(T(0, -0.02, -0.06), RZ(a), S(1.25)))
    g += skull().xf(T(0, 0.03, -0.12))
    return g


def sheriff_star(r=0.45):
    g = puffy(star2(0, 0, r, r * 0.56, 6), 0.1, 0.12, "gold", "gold_dark", back=False).xf(T(0, 0, -0.05))
    for k in range(6):
        a = math.radians(90 + 60 * k)
        g += sphere(r * 0.15, 6, 3, "gold_light").xf(T((r + 0.02) * math.cos(a), (r + 0.02) * math.sin(a), -0.07))
    g += ring2_geo(0, 0, r * 0.3, r * 0.38, 10, -0.2, -0.1, "gold_dark")
    g += sphere(r * 0.2, 8, 4, "gold_light").xf(M(T(0, 0, -0.17), S(1, 1, 0.6)))
    return g


# =============================================================================================
# WildWestMachine (COMMON) - wooden saloon
# =============================================================================================
WW_TOP = 7.1


def wild_west():
    m = Model("WildWestMachine")
    cab = m.part("Cabinet")
    scr = m.part("Screen")
    lev = m.part("Lever", pivot=LEVER_PIVOT)
    top = m.part("Topper", pivot=(0, WW_TOP, 0))
    base = m.part("Base")

    # ---- Base: boardwalk (dark skirting + planks across with small gaps)
    base.add(box((-3, 0, -2.5), (3, 0.64, 2.5), "west_wood_deep", 0.18, skip=("-y",)))
    xs = np.linspace(-2.92, 2.92, 13)
    for k in range(12):
        base.add(box((xs[k] + 0.025, 0.6, -2.42), (xs[k + 1] - 0.025, 1.0, 2.42),
                     "west_wood_light" if k % 2 else "west_plank_a", 0.04, skip=("-y",)))

    # ---- Cabinet: clapboard saloon with a stepped false front
    ys = np.linspace(1.0, 6.2, 11)
    for k in range(10):
        skip = ("-y",) + (("+y",) if k < 9 else ())
        cab.add(box((-2.3, ys[k], -1.9), (2.3, ys[k + 1], 2.1), "west_plank_a" if k % 2 == 0 else "west_plank_b",
                    0.05, skip=skip))
    cab.add(box((-2.05, 6.2, -1.9), (2.05, 6.62, 2.1), "west_plank_a", 0.05, skip=("-y",)))
    cab.add(box((-1.4, 6.62, -1.9), (1.4, 6.98, 2.1), "west_plank_b", 0.05, skip=("-y",)))
    # red cornices on every step (the top one is the cabinet top at y = 7.1)
    cab.add(box((-2.4, 6.1, -2.02), (2.4, 6.28, 2.22), "red", 0.05, top="red_dark"))
    cab.add(box((-2.14, 6.52, -2.0), (2.14, 6.68, 2.2), "red", 0.04, top="red_dark"))
    cab.add(box((-1.5, 6.95, -2.0), (1.5, WW_TOP, 2.2), "red", 0.04, top="red_dark"))
    # red corner boards
    for sx in (-1, 1):
        for z0, z1 in ((-2.0, -1.72), (1.92, 2.2)):
            x0, x1 = sorted((sx * 2.12, sx * 2.38))
            cab.add(box((x0, 1.0, z0), (x1, 6.1, z1), "red", 0.04, skip=("-y", "+y")))
    # window frame (red) with gold rivets
    cab.add(extrude(rounded_rect2(-2.0, 3.5, 2.0, 6.0, 0.22, 0.22, 3), -2.0, -1.9, "red", "red_dark", back=False))
    for x, y in ((-1.88, 3.62), (1.88, 3.62), (-1.88, 5.88), (1.88, 5.88)):
        cab.add(dome(0.07, 6, 2, "gold_light"), M(T(x, y, -2.0), RX(-90)))
    # sheriff star on the false front
    cab.add(sheriff_star(0.44), T(0, 6.62, -2.05))
    # bar counter deck + buttons
    cab.add(deck(-2.1, 2.1, -1.9, "west_wood_dark", "west_wood_light"))
    for x, c in ((-0.9, "red"), (0.0, "gold"), (0.9, "red")):
        cab.add(cyl(0.2, 0, 0.1, 8, c, topcol="gold_light" if c == "gold" else "pink"), deck_spot(x, 0.45, -1.9))
    # swinging saloon doors in front of a dark doorway
    cab.add(box((-1.05, 1.0, -1.97), (1.05, 2.55, -1.9), "black_soft", skip=("+z", "-y", "+y")))
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 1.05, sx * 1.22))
        cab.add(box((x0, 1.0, -2.04), (x1, 2.6, -1.9), "red", 0.03, skip=("+z", "-y")))
    door = [(0.05, 1.32), (0.97, 1.32), (0.97, 2.42), (0.75, 2.38), (0.5, 2.3), (0.25, 2.22), (0.05, 2.19)]
    for sx in (-1, 1):
        pts = [(sx * x, y) for x, y in door]
        cab.add(extrude(pts, -2.07, -1.99, "red", "red_dark"))
        for k in range(3):
            y = 1.52 + 0.2 * k
            x0, x1 = sorted((sx * 0.2, sx * 0.86))
            cab.add(box((x0, y, -2.1), (x1, y + 0.08, -2.07), "west_wood_light", skip=("+z",)))
        for y in (1.45, 2.2):
            x0, x1 = sorted((sx * 0.84, sx * 1.0))
            cab.add(box((x0, y, -2.11), (x1, y + 0.1, -2.07), "gold", 0.015, skip=("+z",)))
    # lever mount disc and lucky horseshoes on both sides
    cab.add(cyl(0.6, 0, 0.08, 10, "red"), M(T(2.3, 4.2, 0.3), RZ(-90)))
    cab.add(ring_x(0.3, 4.2, 0.45, 0.6, 10, 2.38, 2.42, "gold"))
    for sx in (-1, 1):
        cab.add(ic_horseshoe().xf(M(FACE(90 * sx), T(sx * -0.9, 5.15, -2.3), S(1.25))))

    # ---- Screen: desert scene with three reels
    z = -2.0
    X0, X1, Y0, Y1 = -1.8, 1.8, 3.68, 5.82
    scr.add(box((X0, Y0, z - 0.1), (X1, 4.25, z), "west_sand", skip=("+z", "+y")))
    scr.add(box((X0, 4.25, z - 0.1), (X1, 4.85, z), "west_sky_light", skip=("+z", "-y", "+y")))
    scr.add(box((X0, 4.85, z - 0.1), (X1, Y1, z), "west_sky", skip=("+z", "-y")))
    zf = z - 0.1
    for cx in (-1.2, 0.0, 1.2):                          # distant mesas on each reel
        scr.add(flat([(cx - 0.58, 4.25), (cx - 0.5, 4.5), (cx - 0.3, 4.5), (cx - 0.24, 4.25)], "west_mesa", 0.01).xf(T(0, 0, zf)))
        scr.add(flat([(cx + 0.28, 4.25), (cx + 0.34, 4.42), (cx + 0.5, 4.42), (cx + 0.56, 4.25)], "west_mesa", 0.01).xf(T(0, 0, zf)))
    for x in (-0.6, 0.6):
        scr.add(box((x - 0.06, Y0, z - 0.16), (x + 0.06, Y1, z - 0.1), "west_wood_dark", skip=("+z",)))
    for sx in (-1, 1):                                   # pay-line pointers
        scr.add(flat([(sx * 1.8, 4.62), (sx * 1.8, 4.92), (sx * 1.62, 4.77)], "red", 0.05).xf(T(0, 0, zf)))
    for x, icon in ((-1.2, ic_horseshoe), (0.0, ic_cactus), (1.2, ic_hat)):
        scr.add(on_front(icon(), x, 4.78, zf - 0.01, 1.08))

    # ---- Lever: six-shooter (barrel down in the hub, wooden grip as the handle)
    px, py, pz = LEVER_PIVOT
    lev.add(lever_hub("west_wood_dark", "gold").xf(T(px, py, pz)))
    lev.add(rod((px, py, pz), (px, py + 1.22, pz), 0.12, "chrome", 8))
    lev.add(cyl(0.16, py + 0.4, py + 0.54, 8, "steel_dark", bottom=True), T(px, 0, pz))
    lev.add(box((px - 0.035, py + 0.58, pz + 0.1), (px + 0.035, py + 0.78, pz + 0.19), "steel_dark"))
    lev.add(rod((px, py + 0.62, pz - 0.15), (px, py + 1.2, pz - 0.15), 0.055, "steel", 6))
    drum = lathe([(0.0, 0.0), (0.22, 0.0), (0.27, 0.07), (0.27, 0.5), (0.22, 0.57), (0.0, 0.57)], 6,
                 lambda i, j: ("chrome" if i % 2 == 0 else "steel") if j == 2 else "steel")
    lev.add(drum, T(px, py + 1.18, pz))
    lev.add(box((px - 0.12, py + 1.72, pz - 0.24), (px + 0.12, py + 2.06, pz + 0.3), "steel_dark", 0.04))
    lev.add(box((px - 0.07, py + 1.08, pz + 0.24), (px + 0.07, py + 1.76, pz + 0.33), "steel_dark", 0.02))
    lev.add(prism_zy([(pz + a, py + b) for a, b in ((0.22, 1.98), (0.32, 1.98), (0.5, 2.26), (0.42, 2.32), (0.22, 2.12))],
                     px - 0.05, px + 0.05, "steel_dark"))
    lev.add(ring_x(pz - 0.34, py + 1.86, 0.1, 0.17, 8, px - 0.04, px + 0.04, "gold"))
    lev.add(prism_zy([(pz + a, py + b) for a, b in ((-0.22, 1.98), (-0.3, 1.84), (-0.35, 1.86), (-0.29, 2.0))],
                     px - 0.03, px + 0.03, "steel_dark"))
    grip = [(0.26, 2.04), (-0.22, 2.04), (-0.48, 2.6), (-0.6, 2.94), (-0.24, 3.04), (0.0, 2.62)]
    lev.add(prism_zy([(pz + a, py + b) for a, b in grip], px - 0.14, px + 0.14, "west_wood",
                     lambda i, p, q: "west_wood_dark"))
    cap = [(-0.6, 2.94), (-0.24, 3.04), (-0.2, 3.16), (-0.64, 3.08)]
    lev.add(prism_zy([(pz + a, py + b) for a, b in cap], px - 0.15, px + 0.15, "gold", "gold_dark"))
    for sx in (-1, 1):
        lev.add(puffy_star(0.1, 0.045, 0.04, 0.03, "gold", "gold_dark", back=False),
                M(T(px + sx * 0.14, py + 2.6, pz - 0.27), FACE(90 * sx)))

    # ---- Topper: cowboy hat (brim curled up at the sides, red band, gold star)
    ty = WW_TOP
    zs = 1.18                                         # crown / brim are a bit longer front-to-back

    def brim(i, j):
        a = 2 * math.pi * i / 20
        t = j / 3
        ex, ez = 0.6 + (1.4 - 0.6) * t, 0.6 * zs + (1.12 - 0.6 * zs) * t
        y = 0.18 + 0.46 * t * t * math.sin(a) ** 2 - 0.07 * t * t * math.cos(a) ** 2
        return (ex * math.sin(a), ty + y, -ez * math.cos(a))
    top.add(sheet(brim, 20, 3, "west_hat", (0, -0.09, 0), lambda p: (0, 1, 0), side="west_hat_dark",
                  back_col="west_hat_dark", edges=(False, False, False, True)))
    crown = [(0.66, 0.0), (0.66, 0.5), (0.62, 1.12), (0.55, 1.55), (0.42, 1.77), (0.2, 1.7), (0.0, 1.6)]
    top.add(lathe(crown, 14, lambda i, j: "west_hat" if j < 4 else "west_hat_dark" if j == 5 else "west_hat"),
            M(T(0, ty, 0), S(1, 1, zs)))
    top.add(lathe([(0.65, 0.2), (0.7, 0.22), (0.7, 0.46), (0.65, 0.48)], 14, "red"), M(T(0, ty, 0), S(1, 1, zs)))
    for rot in (0, 180):
        top.add(puffy_star(0.15, 0.065, 0.05, 0.05, "gold", "gold_dark", back=False),
                M(RY(rot), T(0, ty + 0.34, -0.7 * zs - 0.03)))
    return m


# =============================================================================================
# PirateFortuneMachine (UNCOMMON) - treasure chest
# =============================================================================================
PF_TOP = 7.1
LID_Y0, LID_YS = 5.74, 6.12


def lid_profile(pad=0.0, n=5):
    """(z, y) side outline of the chest lid: short upright front/back, quarter-round edges, flat top at PF_TOP."""
    z0, z1 = -1.98 - pad, 2.18 + pad
    yt = PF_TOP + pad
    rz, ry = 1.0 + pad, PF_TOP - LID_YS + pad
    pts = [(z0, LID_Y0), (z1, LID_Y0), (z1, LID_YS)]
    for k in range(1, n + 1):
        a = math.radians(90 * k / n)
        pts.append((z1 - rz + rz * math.cos(a), LID_YS + ry * math.sin(a)))
    for k in range(0, n + 1):
        a = math.radians(90 + 90 * k / n)
        pts.append((z0 + rz + rz * math.cos(a), LID_YS + ry * math.sin(a)))
    return pts


def pirate_ship(ty):
    g = Geo()
    # little sea under the ship
    g += lathe([(1.0, 0.0), (1.06, 0.1), (0.96, 0.2), (0.0, 0.2)], 16,
               lambda i, j: "west_sea_light" if j == 1 else "west_sea", rmod=lambda i: 1.0 if i % 2 == 0 else 0.9).xf(
        M(T(0, ty, 0), S(1.18, 1, 0.62)))
    for x, z, r in ((-0.85, -0.42, 0.09), (0.7, 0.45, 0.08), (0.95, -0.3, 0.07), (-0.6, 0.48, 0.07)):
        g += sphere(r, 6, 3, "white").xf(M(T(x, ty + 0.2, z), S(1.4, 0.7, 1)))
    # hull loft: (x, y_bottom, y_deck, half width bottom, half width deck), stern -> bow
    st = [(-0.95, 0.3, 0.8, 0.2, 0.36), (-0.55, 0.16, 0.68, 0.24, 0.42), (0.0, 0.12, 0.62, 0.24, 0.42),
          (0.5, 0.16, 0.66, 0.18, 0.36), (0.85, 0.3, 0.76, 0.07, 0.2), (1.04, 0.5, 0.86, 0.01, 0.03)]
    rows = []
    for x, yb, yd, wb, wd in st:
        ym = yb + 0.45 * (yd - yb)
        rows.append([(x, yd, wd), (x, yd - 0.08, wd * 0.99), (x, ym, (wd + wb) / 2 + 0.05), (x, yb, wb)])
    band = ["gold", "west_hull", "west_hull_dark"]

    def P(x, y, z):
        return np.array((x, ty + y, z))
    for k in range(len(rows) - 1):
        r0, r1 = rows[k], rows[k + 1]
        for s in (-1, 1):
            for b in range(3):
                q = [P(r[0], r[1], s * r[2]) for r in (r0[b], r1[b], r1[b + 1], r0[b + 1])]
                g.add([q[0], q[1], q[2]], band[b], (0, 0, s))
                g.add([q[0], q[2], q[3]], band[b], (0, 0, s))
        q = [P(r0[3][0], r0[3][1], -r0[3][2]), P(r1[3][0], r1[3][1], -r1[3][2]), P(r1[3][0], r1[3][1], r1[3][2]),
             P(r0[3][0], r0[3][1], r0[3][2])]
        g.add(q, "west_hull_dark", (0, -1, 0))
        q = [P(r0[0][0], r0[0][1], -r0[0][2]), P(r1[0][0], r1[0][1], -r1[0][2]), P(r1[0][0], r1[0][1], r1[0][2]),
             P(r0[0][0], r0[0][1], r0[0][2])]
        g.add(q, "west_deck", (0, 1, 0))
    for r, sgn in ((rows[0], -1), (rows[-1], 1)):
        ring = [P(p[0], p[1], -p[2]) for p in r] + [P(p[0], p[1], p[2]) for p in reversed(r)]
        g.add(ring, "west_hull_dark", (sgn, 0, 0))
    # portholes
    for x in (-0.3, 0.12, 0.52):
        w = np.interp(x, [s[0] for s in st], [s[4] for s in st]) * 0.97
        for s in (-1, 1):
            g += cyl(0.075, 0.0, w, 8, "gold", topcol="gold").xf(M(T(x, ty + 0.5, 0), RX(-90 * s)))
            g += cyl(0.045, 0.0, w + 0.025, 8, "black_soft").xf(M(T(x, ty + 0.5, 0), RX(-90 * s)))
    # stern castle with gold windows
    g += box((-0.98, ty + 0.66, -0.37), (-0.48, ty + 1.0, 0.37), "west_hull", 0.03, top="west_deck")
    g += box((-1.0, ty + 0.98, -0.39), (-0.46, ty + 1.05, 0.39), "gold", 0.02)
    for z in (-0.2, 0.0, 0.2):
        g += box((-1.0, ty + 0.74, z - 0.06), (-0.97, ty + 0.9, z + 0.06), "gold_light", skip=("+x",))
    # masts, crow's nest, yards, bowsprit
    for x, h in ((-0.12, 1.82), (0.48, 1.5)):
        g += rod((x, ty + 0.55, 0), (x, ty + h, 0), 0.05, "west_wood_dark", 6)
    g += cyl(0.13, ty + 1.42, ty + 1.52, 8, "west_wood_dark", bottom=True, topcol="west_hull").xf(T(-0.12, 0, 0))
    g += sphere(0.06, 6, 3, "gold_light").xf(T(-0.12, ty + 1.86, 0))
    g += rod((0.95, ty + 0.8, 0), (1.32, ty + 1.02, 0), 0.04, "west_wood_dark", 6)

    # billowing sails (YZ plane, bulging towards the bow)
    def sail(xm, y0, y1, wb, wt, bulge):
        def Ps(i, j):
            u, v = i / 4, j / 2
            w = wb + (wt - wb) * v
            zz = (2 * u - 1) * w
            xx = xm + 0.05 + bulge * (1 - (2 * u - 1) ** 2) * (0.7 + 0.3 * math.sin(math.pi * v))
            return (xx, ty + y0 + (y1 - y0) * v, zz)
        return sheet(Ps, 4, 2, lambda i, j: "red" if j == 1 and i in (1, 2) else "west_sail", (-0.04, 0, 0),
                     lambda p: (1, 0, 0), side="cream_dark")
    g += sail(-0.12, 0.84, 1.38, 0.54, 0.44, 0.16)
    g += sail(0.48, 0.84, 1.3, 0.44, 0.36, 0.13)
    for x, y, w in ((-0.12, 1.38, 0.5), (-0.12, 0.84, 0.58), (0.48, 1.3, 0.4), (0.48, 0.84, 0.48)):
        g += rod((x + 0.04, ty + y, -w), (x + 0.04, ty + y, w), 0.03, "west_wood_dark", 4)
    # jolly roger
    flag = [(-0.16, 1.56), (-0.66, 1.57), (-0.6, 1.68), (-0.66, 1.8), (-0.16, 1.8)]
    g += extrude([(x, ty + y) for x, y in flag], -0.02, 0.02, "black_soft")
    for rot, zz in ((0, -0.02), (180, 0.02)):
        mini = Geo()
        mini += flat(circle2(0, 0.02, 0.06, 8), "white", 0.01)
        mini += flat(rounded_rect2(-0.035, -0.06, 0.035, -0.01, 0, 0.0), "white", 0.01)
        for a in (40, -40):
            mini += flat([(-0.1, -0.012), (0.1, -0.012), (0.1, 0.012), (-0.1, 0.012)], "white", 0.008).xf(M(T(0, -0.02, 0.005), RZ(a)))
        mini += flat(circle2(-0.022, 0.025, 0.016, 5), "black_soft", 0.005).xf(T(0, 0, -0.01))
        mini += flat(circle2(0.022, 0.025, 0.016, 5), "black_soft", 0.005).xf(T(0, 0, -0.01))
        g += mini.xf(M(T(-0.4, ty + 1.68, zz), RY(rot)))
    return g


def pirate_fortune():
    m = Model("PirateFortuneMachine")
    cab = m.part("Cabinet")
    scr = m.part("Screen")
    lev = m.part("Lever", pivot=LEVER_PIVOT)
    top = m.part("Topper", pivot=(0, PF_TOP, 0))
    base = m.part("Base")

    # ---- Base: dark ship-wood plinth, gold studs and corner caps, spilled treasure in front
    base.add(box((-3, 0, -2.5), (3, 0.82, 2.5), "west_chest_dark", 0.25, skip=("-y",)))
    base.add(box((-2.86, 0.8, -2.38), (2.86, 1.0, 2.38), "west_chest_b", 0.06, skip=("-y",)))
    for x in np.linspace(-2.4, 2.4, 7):
        base.add(dome(0.1, 6, 2, "gold"), M(T(x, 0.42, -2.5), RX(-90)))
    for sx in (-1, 1):
        for sz in (-1, 1):
            x0, x1 = sorted((sx * 2.9, sx * 2.5))
            z0, z1 = sorted((sz * 2.42, sz * 2.02))
            base.add(box((x0, 0.97, z0), (x1, 1.05, z1), "gold", 0.02, skip=("-y",)))
    base.add(coin_stack(4), T(-2.42, 1.0, -2.12))
    base.add(coin_stack(2), T(-2.05, 1.0, -2.25))
    base.add(coin(0.2, 0.07, emblem=True), M(T(-2.2, 1.14, -2.42), RX(35)))
    base.add(gem(0.14, "pink", "neon_magenta"), T(-2.62, 1.0, -2.3))
    base.add(coin_stack(3), T(2.4, 1.0, -2.15))
    base.add(cyl(0.2, 0, 0.07, 10, "gold", topcol="gold_light"), T(2.1, 1.0, -2.3))
    base.add(gem(0.15, "cyan", "teal"), T(2.12, 1.07, -2.28))
    base.add(coin(0.2, 0.07, emblem=True), M(T(2.62, 1.14, -2.4), RY(-20), RX(35)))

    # ---- Cabinet: treasure chest (plank body + rounded lid, gold straps, skull & crossed swords)
    ys = np.linspace(1.0, 5.74, 8)
    for k in range(7):
        skip = ("-y",) + (("+y",) if k < 6 else ())
        cab.add(box((-2.25, ys[k], -1.9), (2.25, ys[k + 1], 2.1), "west_chest_a" if k % 2 == 0 else "west_chest_b",
                    0.05, skip=skip))
    lid = lid_profile()
    nl = len(lid)

    def lid_col(i, p, q):
        if i == 0:
            return None
        return "west_chest_a" if (i // 2) % 2 == 0 else "west_chest_b"
    cab.add(prism_zy(lid, -2.3, 2.3, "west_chest_b", lid_col))
    outer = lid_profile(0.05)
    for x0, x1 in ((-2.24, -1.94), (-0.2, 0.2), (1.94, 2.24)):
        cab.add(band_zy(lid, outer, x0, x1, "gold", skip_edges=(0,)))
    # seam band between body and lid
    cab.add(box((-2.31, 5.6, -1.97), (2.31, 5.8, 2.17), "gold_dark", 0.04))
    # vertical straps (front, back) and side corner straps, with rivets
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 1.94, sx * 2.27))
        cab.add(box((x0, 1.0, -1.97), (x1, 5.6, -1.88), "gold", 0.02, skip=("-y", "+y", "+z")))
        cab.add(box((x0, 1.0, 2.08), (x1, 5.6, 2.17), "gold", 0.02, skip=("-y", "+y", "-z")))
        for z0, z1 in ((-1.86, -1.56), (1.76, 2.06)):
            xa, xb = sorted((sx * 2.22, sx * 2.29))
            cab.add(box((xa, 1.0, z0), (xb, 5.6, z1), "gold", 0.02, skip=("-y", "+y")))
        for y in (1.35, 2.3, 3.3, 4.3, 5.25):
            cab.add(dome(0.06, 6, 2, "gold_light"), M(T(sx * 2.105, y, -1.97), RX(-90)))
        # side handles
        xa = sx * 2.25
        for zc in (-1.27, -0.63):
            xb0, xb1 = sorted((xa, xa + sx * 0.06))
            cab.add(box((xb0, 5.1, zc - 0.08), (xb1, 5.32, zc + 0.08), "gold_dark", 0.02))
        xr0, xr1 = sorted((xa + sx * 0.03, xa + sx * 0.1))
        cab.add(prism_zy(arc_band(-0.95, 5.2, 0.25, 0.33, 180, 360, 8), xr0, xr1, "gold"))
    # bottom band
    cab.add(box((-2.29, 1.0, -1.94), (2.29, 1.2, 2.14), "gold_dark", 0.03, skip=("-y",)))
    # screen frame (gold) with corner rivets
    cab.add(extrude(rounded_rect2(-1.9, 3.46, 1.9, 5.54, 0.16, 0.16, 3), -2.0, -1.9, "gold", "gold_dark", back=False))
    for x, y in ((-1.8, 3.56), (1.8, 3.56), (-1.8, 5.44), (1.8, 5.44)):
        cab.add(dome(0.06, 6, 2, "gold_light"), M(T(x, y, -2.0), RX(-90)))
    # skull & crossed swords badge on the lid front (tilted to follow the curve)
    cab.add(skull_swords(), M(T(0, 6.4, -2.0), RX(30), S(0.82)))
    # control deck (red velvet top) with gold coin buttons
    cab.add(deck(-1.9, 1.9, -1.9, "west_chest_dark", "red"))
    for x in (-0.85, 0.0, 0.85):
        cab.add(coin(0.21, 0.08, emblem=True), M(deck_spot(x, 0.45, -1.9), RX(90)))
    # coin tray
    cab.add(box((-1.0, 1.3, -2.3), (1.0, 1.86, -1.9), "gold_dark", 0.1, skip=("+z",), top="gold"))
    cab.add(box((-0.78, 1.6, -2.32), (0.78, 1.76, -2.05), "black_soft", skip=("+z", "-y")))
    # lever mount disc
    cab.add(cyl(0.6, 0, 0.08, 10, "west_chest_dark"), M(T(2.25, 4.2, 0.3), RZ(-90)))
    cab.add(ring_x(0.3, 4.2, 0.45, 0.6, 10, 2.33, 2.37, "gold"))

    # ---- Screen: night sea with gold coins, treasure maps and parrots
    z = -2.0
    X0, X1, Y0, Y1 = -1.75, 1.75, 3.6, 5.4
    scr.add(box((X0, Y0, z - 0.1), (X1, 4.02, z), "west_sea", skip=("+z", "+y")))
    scr.add(box((X0, 4.02, z - 0.1), (X1, Y1, z), "purple_deep", skip=("+z", "-y")))
    zf = z - 0.1
    for k in range(12):
        x = X0 + 0.15 + k * 0.29
        scr.add(flat(arc_pts(x, 4.02, 0.13, 0, 180, 4, sy=0.7), "west_sea_light", 0.01).xf(T(0, 0, zf)))
    for x, y in ((-1.5, 5.2), (-0.85, 5.25), (-0.3, 5.15), (0.35, 5.27), (0.82, 5.12), (1.5, 5.22), (-1.45, 4.35), (1.45, 4.4)):
        scr.add(flat(star2(x, y, 0.06, 0.02, 4), "gold_light", 0.01).xf(T(0, 0, zf)))
    for x in (-0.583, 0.583):
        scr.add(box((x - 0.05, Y0, z - 0.16), (x + 0.05, Y1, z - 0.1), "gold", skip=("+z",)))
    for sx in (-1, 1):
        scr.add(flat([(sx * 1.75, 4.36), (sx * 1.75, 4.66), (sx * 1.58, 4.51)], "red", 0.05).xf(T(0, 0, zf)))
    for x, icon, s in ((-1.17, ic_coin, 1.0), (0.0, ic_map, 1.12), (1.17, ic_parrot, 1.0)):
        scr.add(on_front(icon(), x, 4.55, zf - 0.01, s))

    # ---- Lever: golden anchor (arms in the swing plane, ring as the handle)
    px, py, pz = LEVER_PIVOT
    lev.add(lever_hub("west_chest_dark", "gold").xf(T(px, py, pz)))
    lev.add(box((px - 0.09, py, pz - 0.09), (px + 0.09, py + 2.7, pz + 0.09), "gold", 0.03))
    lev.add(prism_zy([(pz + a, py + b) for a, b in arc_band(0, 1.32, 0.62, 0.8, 196, 344, 10)],
                     px - 0.1, px + 0.1, "gold", "gold_dark"))
    for s in (-1, 1):
        fl = [(s * 0.6, 1.0), (s * 0.95, 1.02), (s * 0.84, 1.34)]
        lev.add(prism_zy([(pz + a, py + b) for a, b in fl], px - 0.11, px + 0.11, "gold", "gold_dark"))
    lev.add(box((px - 0.1, py + 2.22, pz - 0.5), (px + 0.1, py + 2.38, pz + 0.5), "gold", 0.04))
    for s in (-1, 1):
        lev.add(sphere(0.11, 6, 3, "gold_light"), T(px, py + 2.3, pz + s * 0.54))
    lev.add(ring_x(pz, py + 2.98, 0.17, 0.32, 12, px - 0.08, px + 0.08, "gold_light"))
    for y in (1.6, 1.78, 1.96):
        lev.add(lathe([(0.11, -0.05), (0.15, 0.0), (0.11, 0.05)], 8, "west_parch_dark").xf(M(T(px, py + y, pz), RX(8))))

    # ---- Topper: small pirate ship on a patch of sea
    top.add(pirate_ship(PF_TOP))
    return m


BUILDERS = [
    dict(name="WildWestMachine", fn=wild_west, mirror=True, parts=["Cabinet", "Screen", "Lever", "Topper", "Base"]),
    dict(name="PirateFortuneMachine", fn=pirate_fortune, mirror=True,
         parts=["Cabinet", "Screen", "Lever", "Topper", "Base"]),
]
