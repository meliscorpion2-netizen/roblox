"""Tech slot machines: CyberSpinMachine (Uncommon), CrystalKingdomMachine (Rare).

Shared slot layout (see AUTHORING.md): 6 wide (X) x 5 deep (Z) x 9 tall (Y), pivot at ground centre,
front faces -Z.  Front art is authored in plain XY (+X right) and the build mirrors X once
(mirror=True), so the lever authored on +X ends up on the player's right.
"""
import math

import numpy as np

from casino_geo import (Geo, Model, M, T, RX, RY, RZ, S, FACE, add_colors, box, lathe, cyl, sphere,
                        extrude, puffy, circle2, star2, frustum_box, signed_area)
from models_machines import (LEVER_PIVOT, rounded_rect2, side_prism, rod, flat, bump, on_front, lever_hub,
                             strip_along)

add_colors({
    # CyberSpin: white & teal sci-fi
    "tech_white": "#F5FCFF", "tech_shade": "#D2E6EE", "tech_teal": "#14C9C0", "tech_teal_dark": "#0B929A",
    "tech_teal_deep": "#0A5D6E", "tech_screen": "#0A1F36", "tech_reel": "#E8FBFF", "tech_reel_shade": "#BFE7F0",
    "tech_glow": "#4DFFE4", "tech_holo": "#7DF9FF",
    # CrystalKingdom: ice blue crystal
    "tech_ice": "#86D8FF", "tech_ice_light": "#C4EEFF", "tech_ice_white": "#ECFAFF", "tech_ice_mid": "#5FBDF5",
    "tech_ice_dark": "#3B8FDB", "tech_ice_deep": "#2A5DB5", "tech_ice_night": "#16226A", "tech_ice_glow": "#B5F6FF",
    "tech_amethyst": "#B27DFF", "tech_amethyst_dark": "#7A45E0", "tech_rose": "#FF6FC3", "tech_rose_dark": "#D9409A",
}, neon={"tech_glow", "tech_holo", "tech_ice_glow"})


# ----------------------------------------------------------------------------- 2D helpers
def _dedupe(poly):
    out = []
    for q in poly:
        q = (float(q[0]), float(q[1]))
        if not out or math.hypot(q[0] - out[-1][0], q[1] - out[-1][1]) > 1e-6:
            out.append(q)
    if len(out) > 1 and math.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) < 1e-6:
        out.pop()
    return out


def _ccw(poly):
    p = _dedupe(poly)
    return p if signed_area(p) > 0 else p[::-1]


def inset2(poly, d):
    """Mitred inward offset of a CCW polygon (small d)."""
    p = _ccw(poly)
    n = len(p)
    out = []
    for i in range(n):
        a, b, c = np.array(p[i - 1]), np.array(p[i]), np.array(p[(i + 1) % n])
        e1 = (b - a) / np.linalg.norm(b - a)
        e2 = (c - b) / np.linalg.norm(c - b)
        n1 = np.array((-e1[1], e1[0]))
        n2 = np.array((-e2[1], e2[0]))
        q = b + d * (n1 + n2) / (1.0 + float(np.dot(n1, n2)))
        out.append((float(q[0]), float(q[1])))
    return out


def facet_rings(outline, z0, rings, colf, facing=-1):
    """Bevel / gem-facet rings starting at `outline` (depth z0), each ring = (inset, z).
    colf(ring_index, edge_index) -> colour.  facing=-1 for the front, +1 for the back."""
    p = _ccw(outline)
    g = Geo()
    prev, pz = p, z0
    for k, (d, z) in enumerate(rings):
        cur = inset2(p, d)
        for i in range(len(p)):
            j = (i + 1) % len(p)
            ex, ey = p[j][0] - p[i][0], p[j][1] - p[i][1]
            L = math.hypot(ex, ey)
            nrm = (ey / L * 0.5, -ex / L * 0.5, facing)
            g.add([(prev[i][0], prev[i][1], pz), (prev[j][0], prev[j][1], pz),
                   (cur[j][0], cur[j][1], z), (cur[i][0], cur[i][1], z)], colf(k, i), nrm)
        prev, pz = cur, z
    return g, prev, pz


def gem_slab(outline, z_front, z_back, side_col, front_rings, back_rings, front_colf, back_colf, table_col, back_col):
    """Extruded body whose front and back edges are cut into gem-like facet rings."""
    p = _ccw(outline)
    g = extrude(p, z_front, z_back, side_col, front=False, back=False)
    fr, ftab, fz = facet_rings(p, z_front, front_rings, front_colf, -1)
    br, btab, bz = facet_rings(p, z_back, back_rings, back_colf, 1)
    g += fr + br
    g.add([(x, y, fz) for x, y in ftab], table_col, (0, 0, -1))
    g.add([(x, y, bz) for x, y in btab], back_col, (0, 0, 1))
    return g, ftab, fz


def trace(pts, w=0.07, t=0.02, col="tech_glow", pad=0.075, ends=(True, True)):
    """Glowing circuit trace decal in the XY plane facing -Z, lifted t off z=0, with hexagonal solder pads."""
    g = Geo()
    for a, b in zip(pts, pts[1:]):
        a, b = np.array(a, float), np.array(b, float)
        d = (b - a) / np.linalg.norm(b - a)
        n = np.array((-d[1], d[0])) * w / 2
        a2, b2 = a - d * w / 2, b + d * w / 2
        g.add([(*(a2 - n), -t), (*(b2 - n), -t), (*(b2 + n), -t), (*(a2 + n), -t)], col, (0, 0, -1))
    for k, e in ((0, pts[0]), (1, pts[-1])):
        if ends[k]:
            g.add([(x, y, -t - 0.006) for x, y in circle2(e[0], e[1], pad, 6, start=0)], col, (0, 0, -1))
    return g


def on_side(g, sx, x_wall):
    """Place XY art (facing -Z, back at z=0, local x = world z) on the side wall at x = sx * x_wall."""
    if sx > 0:
        return g.xf(M(FACE(90), T(0, 0, -x_wall)))
    return g.xf(M(FACE(-90), S(-1, 1, 1), T(0, 0, -x_wall)))


def hoop(R, w, t, seg, colf):
    """Flat ring around +Y (radius R, radial width w, height t)."""
    prof = [(R - w / 2, -t / 2), (R + w / 2, -t / 2), (R + w / 2, t / 2), (R - w / 2, t / 2), (R - w / 2, -t / 2)]
    return lathe(prof, seg, colf)


def crystal(r, h, tip, colf, seg=6, bottom=None):
    """Hexagonal crystal standing on y=0 along +Y: prism of height h plus a pointed tip.
    bottom: optional pointed bottom length (else open bottom, meant to be embedded)."""
    prof = ([(0.0, -bottom)] if bottom else []) + [(r, 0.0), (r, h), (0.0, h + tip)]
    return lathe(prof, seg, colf, phase=0.0)


def gem_cols(*cols):
    return lambda i, j: cols[(i + j) % len(cols)]


def reel_drum(xc, yc, z_front, w, h, col, bulge=0.1, seg=8):
    """Slightly curved reel drum (axis along X) whose front-most line is at z_front."""
    R = ((h / 2) ** 2 + bulge ** 2) / (2 * bulge)
    half = math.degrees(math.asin((h / 2) / R))
    g = lathe([(R, -w / 2), (R, w / 2)], seg, col, a0=-half, a1=half)
    return g.xf(M(T(xc, yc, z_front + R), RZ(-90)))


# ----------------------------------------------------------------------------- icons (unit size, facing -Z, back at z=0)
def ic_robot():
    g = Geo()
    # head
    g += box((-0.36, -0.34, -0.12), (0.36, 0.24, 0.0), "tech_teal", 0.07, skip=("+z",))
    # face visor with glowing eyes
    g += box((-0.27, -0.18, -0.16), (0.27, 0.12, -0.12), "black_soft", 0.03, skip=("+z",))
    for sx in (-1, 1):
        g += flat(circle2(sx * 0.12, -0.02, 0.065, 6, start=0), "tech_glow", 0.02).xf(T(0, 0, -0.16))
        # ear bolts
        g += box((-0.05, -0.17, -0.09), (0.05, 0.07, -0.02), "tech_teal_dark", skip=("+z",)).xf(T(sx * 0.41, 0, 0))
    # mouth grill
    for k in range(3):
        x = -0.12 + 0.12 * k
        g.add([(x - 0.035, -0.29, -0.121), (x + 0.035, -0.29, -0.121), (x + 0.035, -0.23, -0.121), (x - 0.035, -0.23, -0.121)],
              "tech_white", (0, 0, -1))
    # antenna
    g += rod((0, 0.22, -0.06), (0, 0.42, -0.06), 0.03, "steel", 4, caps=False)
    g += sphere(0.075, 6, 3, "seven").xf(T(0, 0.46, -0.06))
    return g


def ic_chip():
    g = Geo()
    g += box((-0.3, -0.3, -0.1), (0.3, 0.3, 0.0), "charcoal", 0.05, skip=("+z",))
    for k in range(3):
        o = -0.17 + 0.17 * k
        for sx in (-1, 1):
            for (x0, y0, x1, y1) in ((0.28, o - 0.045, 0.44, o + 0.045), (o - 0.045, 0.28, o + 0.045, 0.44)):
                if sx < 0:
                    x0, x1, y0, y1 = (-x1, -x0, y0, y1) if x0 > 0.2 else (x0, x1, -y1, -y0)
                g.add([(x0, y0, -0.05), (x1, y0, -0.05), (x1, y1, -0.05), (x0, y1, -0.05)], "gold", (0, 0, -1))
    g += box((-0.16, -0.16, -0.14), (0.16, 0.16, -0.1), "tech_teal", 0.03, skip=("+z",))
    g.add([(x, y, -0.142) for x, y in circle2(0, 0, 0.075, 6, start=0)], "tech_glow", (0, 0, -1))
    g.add([(x, y, -0.102) for x, y in circle2(-0.215, 0.215, 0.035, 6)], "tech_white", (0, 0, -1))
    return g


def mini_robot():
    """Cheap flat robot for the half-hidden reel rows."""
    g = flat(rounded_rect2(-0.36, -0.3, 0.36, 0.26, 0.1, 0.1, 2), "tech_teal", 0.03)
    g.add([(x, y, -0.035) for x, y in rounded_rect2(-0.26, -0.15, 0.26, 0.12, 0.04, 0.04, 1)], "black_soft", (0, 0, -1))
    for sx in (-1, 1):
        g.add([(x, y, -0.04) for x, y in circle2(sx * 0.12, -0.015, 0.06, 6, start=0)], "tech_glow", (0, 0, -1))
    g.add([(-0.03, 0.26, -0.03), (0.03, 0.26, -0.03), (0.03, 0.4, -0.03), (-0.03, 0.4, -0.03)], "steel", (0, 0, -1))
    g.add([(x, y, -0.035) for x, y in circle2(0, 0.43, 0.07, 6)], "seven", (0, 0, -1))
    return g


def mini_chip():
    g = Geo()
    for k in range(3):
        o = -0.17 + 0.17 * k
        g.add([(-0.43, o - 0.045, -0.02), (0.43, o - 0.045, -0.02), (0.43, o + 0.045, -0.02), (-0.43, o + 0.045, -0.02)],
              "gold", (0, 0, -1))
        g.add([(o - 0.045, -0.43, -0.021), (o + 0.045, -0.43, -0.021), (o + 0.045, 0.43, -0.021), (o - 0.045, 0.43, -0.021)],
              "gold", (0, 0, -1))
    g += flat(rounded_rect2(-0.3, -0.3, 0.3, 0.3, 0.05, 0.05, 1), "charcoal", 0.04).xf(T(0, 0, -0.02))
    g.add([(-0.15, -0.15, -0.065), (0.15, -0.15, -0.065), (0.15, 0.15, -0.065), (-0.15, 0.15, -0.065)], "tech_teal", (0, 0, -1))
    return g


def ic_diamond_cut(c_top="tech_ice_white", c_mid="diamond", c_low="diamond_dark", c_edge="tech_ice_mid"):
    """Brilliant-cut diamond: crown and pavilion facets in several shades."""
    G0, G1, G2, G3 = (-0.46, 0.1), (-0.16, 0.1), (0.16, 0.1), (0.46, 0.1)
    T0, T1 = (-0.27, 0.33), (0.27, 0.33)
    B = (0.0, -0.46)
    g = bump([G0, T0, T1, G3, B], c_edge, "tech_ice_dark", 0.06, 0.02)
    z = -0.085
    g += flat([G0, G1, T0], c_mid, 0.02).xf(T(0, 0, z))
    g += flat([G1, G2, T1, T0], c_top, 0.02).xf(T(0, 0, z))
    g += flat([G2, G3, T1], c_mid, 0.02).xf(T(0, 0, z))
    g += flat([G0, G1, B], c_low, 0.02).xf(T(0, 0, z))
    g += flat([G1, G2, B], "tech_ice_light", 0.02).xf(T(0, 0, z))
    g += flat([G2, G3, B], c_mid, 0.02).xf(T(0, 0, z))
    g += flat(star2(-0.18, 0.22, 0.09, 0.025, 4), "white", 0.02).xf(T(0, 0, z - 0.02))
    return g


def ic_crown(scale=1.0):
    g = Geo()
    body = [(-0.42, -0.12), (0.42, -0.12), (0.47, 0.3), (0.22, 0.08), (0.0, 0.4), (-0.22, 0.08), (-0.47, 0.3)]
    g += bump(body, "gold", "gold_dark", 0.08, 0.06)
    g += bump(rounded_rect2(-0.44, -0.34, 0.44, -0.1, 0.04, 0.04, 2), "gold_dark", "gold_deep", 0.1, 0.04)
    for x, y in ((-0.47, 0.3), (0.0, 0.4), (0.47, 0.3)):
        g += sphere(0.075, 6, 3, "gold_light").xf(T(x, y + 0.04, -0.06))
    for x, c in ((-0.25, "tech_rose"), (0.0, "red"), (0.25, "tech_amethyst")):
        g += bump(circle2(x, -0.22, 0.065, 6), c, None, 0.03, 0.03).xf(T(0, 0, -0.1))
    g += bump([(0, 0.17), (0.07, 0.07), (0, -0.03), (-0.07, 0.07)], "diamond", None, 0.03, 0.03).xf(T(0, 0, -0.1))
    return g


def gem_stud(col, side, r=0.13, n=6):
    return bump(circle2(0, 0, r, n, start=90), col, side, 0.05, 0.07)


# =============================================================================================
# CyberSpinMachine (UNCOMMON): white & teal sci-fi cabinet, glowing circuit lines
# =============================================================================================
def _cyber_body():
    pts = [(-2.0, 1.0), (2.0, 1.0), (2.0, 2.4), (2.3, 2.8), (2.3, 6.1)]
    for k in range(1, 7):
        a = math.radians(90 * k / 6)
        pts.append((1.3 + math.cos(a), 6.1 + math.sin(a)))
    for k in range(0, 7):
        a = math.radians(90 + 90 * k / 6)
        pts.append((-1.3 + math.cos(a), 6.1 + math.sin(a)))
    pts += [(-2.3, 2.8), (-2.0, 2.4)]
    return pts


CY_TOP = 7.1


def cyber_spin():
    m = Model("CyberSpinMachine")
    cab = m.part("Cabinet")
    scr = m.part("Screen")
    lev = m.part("Lever", pivot=LEVER_PIVOT)
    top = m.part("Topper", pivot=(0, CY_TOP, 0))
    base = m.part("Base")
    neon = m.part("NeonStrips", neon=True)

    # ---------------- Base: hovering pad (dark foot, teal rim, white top)
    base.add(box((-2.7, 0, -2.2), (2.7, 0.5, 2.2), "tech_teal_deep", 0.12, skip=("-y", "+y")))
    base.add(box((-3.0, 0.5, -2.5), (3.0, 0.82, 2.5), "tech_teal", 0.12))
    base.add(box((-2.86, 0.82, -2.38), (2.86, 1.0, 2.38), "tech_white", 0.06, skip=("-y",)))
    # hover glow under the rim
    for g in (box((-2.74, 0.3, -2.24), (2.74, 0.4, -2.2), "tech_glow", skip=("+z",)),
              box((-2.74, 0.3, 2.2), (2.74, 0.4, 2.24), "tech_glow", skip=("-z",)),
              box((-2.74, 0.3, -2.2), (-2.7, 0.4, 2.2), "tech_glow", skip=("+x",)),
              box((2.7, 0.3, -2.2), (2.74, 0.4, 2.2), "tech_glow", skip=("-x",))):
        neon.add(g)
    # glowing chevrons on the base front band
    for k, x in enumerate(np.linspace(-2.2, 2.2, 7)):
        if k == 3:
            continue
        neon.add(trace([(x - 0.13, 0.57), (x, 0.73), (x + 0.13, 0.57)], 0.06, 0.03, "tech_glow", ends=(False, False)),
                 T(0, 0, -2.5))

    # ---------------- Cabinet: rounded white pod with a teal chamfer trim
    body = _cyber_body()
    zf, zb = -1.75, 1.95
    g, ftab, fz = gem_slab(body, zf, zb, "tech_white", [(0.2, -1.95)], [(0.15, 2.1)],
                           lambda k, i: "tech_teal", lambda k, i: "tech_teal", "tech_white", "tech_white")
    cab.add(g)
    # screen bezel (teal, chamfered)
    bez = rounded_rect2(-2.02, 3.48, 2.02, 6.78, 0.55, 0.3)
    cab.add(extrude(bez, -2.02, -1.95, "tech_teal_dark", back=False))
    rg, inner, iz = facet_rings(bez, -2.02, [(0.1, -2.1)], lambda k, i: "tech_teal", -1)
    cab.add(rg)
    cab.add(Geo().add([(x, y, iz) for x, y in inner], "tech_teal_deep", (0, 0, -1)))
    # brow visor over the screen
    brow = [(-1.5, 6.78), (1.5, 6.78), (1.15, 6.98), (-1.15, 6.98)]
    cab.add(extrude(brow, -2.12, -1.95, "tech_white", "tech_shade", back=False))
    # control deck with sloped top
    dz = fz
    deck_poly = [(dz, 2.5), (dz - 0.65, 2.68), (dz - 0.65, 2.95), (dz, 3.4)]
    cab.add(side_prism(deck_poly, -2.05, 2.05, "tech_white", "tech_white"))
    cab.add(side_prism([(dz - 0.66, 2.66), (dz - 0.72, 2.66), (dz - 0.72, 2.97), (dz - 0.66, 2.97)], -2.0, 2.0,
                       "tech_teal", "tech_teal"))
    # coin tray
    cab.add(box((-0.95, 1.28, -2.28), (0.95, 1.86, fz), "tech_teal", 0.1, skip=("+z",)))
    cab.add(box((-0.72, 1.56, -2.3), (0.72, 1.72, -2.05), "tech_screen", skip=("+z", "-y")))
    # side panels (teal) + lever boss
    side_panel = rounded_rect2(-1.25, 1.45, 1.45, 5.95, 0.35, 0.35)
    for sx in (-1, 1):
        cab.add(on_side(flat(side_panel, "tech_teal", 0.04), sx, 2.3))
        cab.add(on_side(flat(rounded_rect2(-1.05, 1.62, 1.25, 5.78, 0.25, 0.25), "tech_teal_dark", 0.02), sx, 2.34))
    cab.add(cyl(0.6, 0, 0.1, 12, "tech_white", topcol="tech_shade"), M(T(2.3, 4.2, 0.3), RZ(-90)))
    # teal racing stripes over the roof
    for sx in (-1, 1):
        cab.add(box((sx * 1.08 - 0.1, CY_TOP - 0.02, -1.85), (sx * 1.08 + 0.1, CY_TOP + 0.03, 2.02), "tech_teal", skip=("-y",)))
    # back panel with vent slots
    cab.add(flat(rounded_rect2(-1.5, 1.6, 1.5, 5.6, 0.4, 0.4), "tech_teal", 0.04).xf(M(T(0, 0, 2.1), RY(180))))
    for k in range(5):
        y = 4.2 + 0.24 * k
        cab.add(flat([(-0.9, y), (0.9, y), (0.9, y + 0.1), (-0.9, y + 0.1)], "tech_teal_deep", 0.02).xf(
            M(T(0, 0, 2.14), RY(180))))

    # ---------------- NeonStrips: circuit lines
    zc = fz  # front face of the cabinet table
    # glow around the screen window
    sw = [(-1.86, 3.66), (1.86, 3.66), (1.86, 6.6), (-1.86, 6.6)]
    for p, q in zip(sw, sw[1:] + sw[:1]):
        neon.add(strip_along(p, q, 0.08, -2.13, -2.1, "tech_glow"))
    # lower front traces around the coin tray
    for sx in (-1, 1):
        for pts in ([(0.95, 1.45), (1.3, 1.45), (1.55, 1.7), (1.55, 2.3)],
                    [(0.95, 1.7), (1.15, 1.7), (1.15, 2.05), (0.75, 2.3)],
                    [(1.75, 1.2), (1.3, 1.2)]):
            neon.add(trace([(sx * x, y) for x, y in pts], 0.07, 0.03), T(0, 0, zc))
    # side circuit lines (both sides; the lever side avoids the hub)
    side_traces = [
        [(-0.95, 1.85), (-0.95, 3.9), (-0.6, 4.25), (-0.6, 5.55)],
        [(-0.45, 1.85), (-0.45, 2.6), (0.05, 3.1), (0.75, 3.1), (1.05, 3.4), (1.05, 5.55)],
        [(0.45, 1.85), (0.45, 2.3), (1.05, 2.3)],
        [(-0.15, 5.55), (-0.15, 5.15), (0.2, 4.9)],
        [(0.55, 5.55), (0.55, 5.25)],
    ]
    for sx in (-1, 1):
        for pts in side_traces:
            neon.add(on_side(trace(pts, 0.07, 0.03), sx, 2.36))
    # back logo trace
    for pts in ([(-1.1, 2.0), (-1.1, 3.2), (-0.7, 3.6), (0.7, 3.6), (1.1, 3.2), (1.1, 2.0)], [(0.0, 2.0), (0.0, 3.2)]):
        neon.add(trace(pts, 0.07, 0.03).xf(M(T(0, 0, 2.14), RY(180))))
    # deck buttons (sloped deck top)
    t_a = math.degrees(math.atan2(0.65, 0.45))
    for x, w, c in ((-1.35, 0.32, "neon_pink"), (-0.65, 0.32, "tech_glow"), (0.45, 0.62, "neon_cyan"), (1.4, 0.3, "neon_pink")):
        neon.add(box((x - w, 0, -0.17), (x + w, 0.1, 0.17), c, 0.04, skip=("-y",)),
                 M(T(0, 3.175, zc - 0.325), RX(-(90 - t_a))))
    # side arrows marking the pay line
    for sx in (-1, 1):
        neon.add(extrude([(sx * 2.0, 5.0), (sx * 2.0, 5.3), (sx * 1.9, 5.15)], -2.14, -2.1, "neon_pink", back=False))

    # ---------------- Screen: dark window with three white reel drums
    z = -2.1
    scr.add(box((-1.78, 3.72, z - 0.1), (1.78, 6.54, z), "tech_screen", skip=("+z",)))
    zs = z - 0.1
    for x in (-1.15, 0.0, 1.15):
        scr.add(reel_drum(x, 5.13, zs - 0.12, 1.02, 2.62, lambda i, j: "tech_reel" if 2 <= i <= 5 else "tech_reel_shade"))
    for x, icon in ((-1.15, ic_robot), (0.0, ic_chip), (1.15, ic_robot)):
        scr.add(on_front(icon(), x, 5.13, zs - 0.12, 0.98))
    # small half-hidden symbols above / below on the drums
    for x, (up, dn) in ((-1.15, (mini_chip, mini_chip)), (0.0, (mini_robot, mini_robot)), (1.15, (mini_chip, mini_chip))):
        scr.add(on_front(up(), x, 6.12, zs - 0.065, 0.45))
        scr.add(on_front(dn(), x, 4.14, zs - 0.065, 0.45))

    # ---------------- Lever: arcade / flight joystick
    px, py, pz = LEVER_PIVOT
    lev.add(lever_hub("tech_white", "tech_teal").xf(T(px, py, pz)))
    lev.add(lathe([(0.34, 0.0), (0.3, 0.14), (0.2, 0.3), (0.14, 0.42), (0.0, 0.42)], 8,
                  lambda i, j: "tech_teal_deep" if j % 2 == 0 else "tech_teal_dark"), T(px, py + 0.36, pz))
    lev.add(rod((px, py, pz), (px, py + 1.9, pz), 0.09, "chrome", 6))
    grip = [(0.0, 0.0), (0.2, 0.0), (0.27, 0.1), (0.28, 0.45), (0.24, 0.62), (0.28, 0.76), (0.27, 0.9), (0.18, 1.0), (0.0, 1.0)]
    lev.add(lathe(grip, 8, lambda i, j: "tech_teal" if j in (0, 4) else "tech_white"), T(px, py + 1.75, pz))
    lev.add(cyl(0.12, 0, 0.1, 8, "seven"), T(px, py + 2.73, pz))
    lev.add(box((px - 0.07, py + 2.08, pz - 0.36), (px + 0.07, py + 2.36, pz - 0.2), "neon_pink", 0.03))
    lev.add(box((px - 0.12, py + 1.75, pz - 0.12), (px + 0.12, py + 1.8, pz + 0.12), "tech_teal_dark"))

    # ---------------- Topper: hologram projector with a gyroscope of light rings
    ty = CY_TOP
    proj = [(0.92, 0.0), (0.92, 0.12), (0.82, 0.22), (0.62, 0.22), (0.58, 0.28), (0.0, 0.28)]
    top.add(lathe(proj, 12, lambda i, j: {0: "tech_white", 1: "tech_white", 2: "tech_teal", 3: "tech_teal_dark"}.get(j, "tech_glow")),
            T(0, ty, 0))
    for k in range(6):
        a = 360 * k / 6 + 30
        top.add(box((-0.08, 0.04, -0.94), (0.08, 0.1, -0.9), "tech_teal"), M(T(0, ty, 0), RY(a)))
    R = 0.8
    cy = ty + 0.28 + R - 0.02
    rc = lambda i, j: "tech_holo" if i % 2 == 0 else "tech_glow"
    top.add(hoop(R, 0.1, 0.1, 16, rc), M(T(0, cy, 0), RX(90)))
    top.add(hoop(R, 0.1, 0.1, 16, rc), M(T(0, cy, 0), RZ(90)))
    top.add(hoop(R, 0.12, 0.08, 16, lambda i, j: "tech_glow" if i % 2 == 0 else "tech_holo"), T(0, cy, 0))
    # hologram beam + floating robot head hologram (double sided)
    top.add(cyl(0.07, ty + 0.28, cy - 0.3, 6, "tech_holo", top=False))
    head = rounded_rect2(-0.34, -0.26, 0.34, 0.26, 0.1, 0.1, 3)
    top.add(extrude(head, -0.06, 0.06, "holo", "tech_holo"), T(0, cy, 0))
    for zz, rot in ((-0.06, 0), (0.06, 180)):
        hv = flat(rounded_rect2(-0.24, -0.1, 0.24, 0.12, 0.05, 0.05, 2), "holo_deep", 0.02)
        for sx in (-1, 1):
            hv += flat(circle2(sx * 0.11, 0.01, 0.05, 6), "white", 0.02).xf(T(0, 0, -0.02))
        top.add(hv, M(T(0, cy, zz), RY(rot)))
    top.add(rod((0, cy + 0.26, 0), (0, cy + 0.4, 0), 0.025, "tech_holo", 4))
    top.add(sphere(0.06, 6, 3, "neon_pink"), T(0, cy + 0.44, 0))
    return m


# =============================================================================================
# CrystalKingdomMachine (RARE): ice-blue faceted crystal cabinet, crowns & diamonds
# =============================================================================================
CK_TOP = 7.0
CK_BODY = [(-2.3, 1.0), (-0.77, 1.0), (0.77, 1.0), (2.3, 1.0), (2.3, 2.6), (2.3, 4.15), (2.3, 5.7),
           (1.8, 6.35), (1.3, 7.0), (0.0, 7.0), (-1.3, 7.0), (-1.8, 6.35), (-2.3, 5.7), (-2.3, 4.15), (-2.3, 2.6)]
CK_ARCH = [(-1.72, 3.55), (1.72, 3.55), (1.72, 5.75), (0.0, 6.75), (-1.72, 5.75)]


def crystal_kingdom():
    m = Model("CrystalKingdomMachine")
    cab = m.part("Cabinet")
    scr = m.part("Screen")
    lev = m.part("Lever", pivot=LEVER_PIVOT)
    top = m.part("Topper", pivot=(0, CK_TOP, 0))
    base = m.part("Base")

    # ---------------- Base: faceted ice plinth with gem studs and crystal clusters
    base.add(box((-3.0, 0, -2.5), (3.0, 0.5, 2.5), "tech_ice_deep", 0.18, skip=("-y",)))
    base.add(frustum_box(5.7, 4.7, 5.15, 4.2, 0.5, 1.0, "tech_ice_dark", skip=("-y",), top="tech_ice_light"))
    gem_c = [("tech_amethyst", "tech_amethyst_dark"), ("tech_rose", "tech_rose_dark"), ("diamond", "diamond_dark")]
    for k, x in enumerate(np.linspace(-2.45, 2.45, 7)):
        c, s = gem_c[k % 3]
        base.add(bump([(0, 0.15), (0.12, 0), (0, -0.15), (-0.12, 0)], c, s, 0.04, 0.06), T(x, 0.26, -2.5))
    for sx in (-1, 1):
        for (x, z, r, h, tip, tz, tx, cols) in ((2.45, -1.95, 0.2, 0.75, 0.32, -4, 12, ("tech_ice_light", "tech_ice")),
                                                 (2.6, -1.68, 0.14, 0.4, 0.22, 6, 26, ("tech_amethyst", "tech_ice_light")),
                                                 (2.25, -2.18, 0.13, 0.3, 0.2, -22, 4, ("tech_ice", "tech_ice_white"))):
            base.add(crystal(r, h, tip, gem_cols(*cols)), M(T(sx * x, 0.82, z), RZ(-sx * tx), RX(tz)))

    # ---------------- Cabinet: gem-cut body
    def fcol(k, i):
        if k == 0:
            return "tech_ice_light" if i % 2 == 0 else "tech_ice"
        return "tech_ice_white" if i % 2 else "tech_ice_light"

    def bcol(k, i):
        return "tech_ice" if (i + k) % 2 == 0 else "tech_ice_mid"
    g, ftab, fz = gem_slab(CK_BODY, -1.5, 1.75, "tech_ice", [(0.2, -1.78), (0.38, -1.92)], [(0.2, 1.98), (0.36, 2.1)],
                           fcol, bcol, "tech_ice_mid", "tech_ice_mid")
    cab.add(g)
    # arched screen frame: faceted gold-and-ice ring
    def frcol(k, i):
        return ("gold_light", "gold", "gold_dark")[k]
    rg, inner, iz = facet_rings(CK_ARCH, fz, [(0.08, -2.1), (0.18, -2.1), (0.24, -2.02)], frcol, -1)
    cab.add(rg)
    # gem studs on the frame
    studs = [((-1.72, 3.55), "tech_rose"), ((1.72, 3.55), "tech_rose"), ((-1.72, 5.75), "tech_amethyst"),
             ((1.72, 5.75), "tech_amethyst"), ((0.0, 6.75), "red"), ((-0.86, 6.25), "diamond"), ((0.86, 6.25), "diamond")]
    for (x, y), c in studs:
        side = {"tech_rose": "tech_rose_dark", "tech_amethyst": "tech_amethyst_dark", "red": "red_dark"}.get(c, "diamond_dark")
        cab.add(gem_stud(c, side, 0.15 if y > 6.5 else 0.12), T(x, y, -2.1))
    # faceted control deck with gem buttons
    dz = fz
    deck_poly = [(dz, 2.5), (dz - 0.55, 2.62), (dz - 0.68, 2.8), (dz - 0.6, 2.98), (dz, 3.32)]
    cab.add(side_prism(deck_poly, -1.95, 1.95, "tech_ice_light", "tech_ice_white"))
    t_a = math.degrees(math.atan2(0.6, 0.34))
    for x, c, s in ((-1.2, "tech_rose", "tech_rose_dark"), (-0.4, "diamond", "diamond_dark"),
                    (0.4, "tech_amethyst", "tech_amethyst_dark"), (1.2, "tech_rose", "tech_rose_dark")):
        btn = puffy(circle2(0, 0, 0.2, 6, start=0), 0.08, 0.06, c, s, back=False).xf(T(0, 0, -0.04))
        cab.add(btn, M(T(x, 3.15, dz - 0.3), RX(-(90 - t_a)), RX(90)))
    # coin tray
    cab.add(box((-0.95, 1.3, -2.22), (0.95, 1.85, fz), "tech_ice_white", 0.1, skip=("+z",)))
    cab.add(box((-0.72, 1.57, -2.24), (0.72, 1.72, -2.0), "tech_ice_night", skip=("+z", "-y")))
    for sx in (-1, 1):
        cab.add(bump([(0, 0.3), (0.22, 0.08), (0, -0.3), (-0.22, 0.08)], "tech_amethyst", "tech_amethyst_dark", 0.06, 0.1),
                T(sx * 1.45, 1.6, fz))
    # crystal clusters growing from the roof shoulders (kept inside x +-2.2, clear of the lever)
    for sx in (-1, 1):
        for (dx, dz_, r, h, tip, tilt, lean, cols) in (
                (0.0, 0.1, 0.27, 0.95, 0.42, 14, 0, ("tech_ice_light", "tech_ice_white", "tech_ice")),
                (-0.1, -0.6, 0.18, 0.55, 0.3, 20, -18, ("tech_amethyst", "tech_ice_light")),
                (-0.1, 0.78, 0.2, 0.62, 0.3, 10, 18, ("tech_ice", "tech_ice_white"))):
            cab.add(crystal(r, h, tip, gem_cols(*cols)), M(T(sx * (1.7 + dx), 6.05, dz_), RZ(-sx * tilt), RX(lean)))
    # faceted gem plates on both sides (the lever boss sits on the +X plate)
    plate = [(-0.75, 1.35), (1.05, 1.35), (1.45, 1.8), (1.45, 5.0), (1.05, 5.45), (-0.75, 5.45), (-1.15, 5.0), (-1.15, 1.8)]
    pg, ptab, pz_ = facet_rings(plate, 0.0, [(0.16, -0.08), (0.3, -0.11)],
                                lambda k, i: ("tech_ice_white", "tech_ice_light")[(i + k) % 2], -1)
    pg.add([(x, y, pz_) for x, y in ptab], "tech_ice_light", (0, 0, -1))
    emb = bump([(0, 0.55), (0.42, 0.12), (0, -0.55), (-0.42, 0.12)], "tech_amethyst", "tech_amethyst_dark", 0.05, 0.07)
    emb += flat([(0, 0.38), (0.24, 0.12), (0, -0.25), (-0.24, 0.12)], "tech_ice_white", 0.02).xf(T(0, 0, -0.1))
    for sx in (-1, 1):
        cab.add(on_side(pg + emb.xf(T(0.15, 2.45, pz_)), sx, 2.3))
    cab.add(on_side(ic_crown().xf(M(T(0.15, 4.25, pz_), S(1.35, 1.35, 0.7))), -1, 2.3))
    cab.add(cyl(0.62, 0, 0.2, 12, "gold", topcol="gold_light"), M(T(2.3, 4.2, 0.3), RZ(-90)))
    # big cut diamond on the back
    cab.add(ic_diamond_cut().xf(M(T(0, 4.6, 2.1), RY(180), S(2.2))))
    # frost sparkles on the front panel
    for x, y, r in ((-1.62, 2.15, 0.14), (1.62, 2.15, 0.14), (-1.75, 6.05, 0.12), (1.75, 6.05, 0.12)):
        cab.add(flat(star2(x, y, r, r * 0.3, 4), "tech_ice_white", 0.02).xf(T(0, 0, fz)))

    # ---------------- Screen: royal-blue arched window, diamond | crown | diamond
    sc = inset2(CK_ARCH, 0.24)
    scr.add(flat(sc, "tech_ice_night", 0.08).xf(T(0, 0, -1.94)))
    zs = -2.02
    for x in (-0.555, 0.555):
        scr.add(box((x - 0.04, 3.82, zs - 0.03), (x + 0.04, 5.58, zs), "tech_ice_mid", skip=("+z",)))
    scr.add(box((-1.48, 5.6, zs - 0.03), (1.48, 5.66, zs), "gold", skip=("+z",)))
    for x, icon, s in ((-1.06, ic_diamond_cut, 1.06), (0.0, ic_crown, 1.1), (1.06, ic_diamond_cut, 1.06)):
        scr.add(on_front(icon(), x, 4.66, zs, s))
    # sparkles in the arch
    for x, y, r in ((0.0, 6.12, 0.2), (-0.55, 5.95, 0.11), (0.55, 5.95, 0.11), (-1.3, 3.85, 0.08), (1.3, 3.85, 0.08)):
        scr.add(flat(star2(x, y, r, r * 0.3, 4), "tech_ice_white", 0.02).xf(T(0, 0, zs)))

    # ---------------- Lever: crystal scepter
    px, py, pz = LEVER_PIVOT
    lev.add(lever_hub("tech_ice_white", "gold").xf(T(px, py, pz)))
    lev.add(rod((px, py, pz), (px, py + 2.15, pz), 0.1, "tech_ice_white", 6))
    for y in (0.7, 1.4):
        lev.add(lathe([(0.11, 0), (0.17, 0.05), (0.17, 0.13), (0.11, 0.18)], 8, "gold"), T(px, py + y, pz))
    lev.add(lathe([(0.1, 0.0), (0.26, 0.16), (0.31, 0.3), (0.23, 0.3), (0.0, 0.3)], 8, "gold"), T(px, py + 2.05, pz))
    for k in range(4):
        a = math.radians(45 + 90 * k)
        lev.add(rod((px + 0.26 * math.sin(a), py + 2.3, pz - 0.26 * math.cos(a)),
                    (px + 0.21 * math.sin(a), py + 2.72, pz - 0.21 * math.cos(a)), 0.045, "gold", 4))
        lev.add(sphere(0.06, 6, 3, "gold_light"), T(px + 0.21 * math.sin(a), py + 2.74, pz - 0.21 * math.cos(a)))
    lev.add(crystal(0.27, 0.55, 0.42, gem_cols("tech_ice_light", "tech_ice_white", "tech_ice"), seg=6, bottom=0.3),
            T(px, py + 2.52, pz))

    # ---------------- Topper: golden crown dais with a big floating crystal
    ty = CK_TOP
    top.add(lathe([(0.86, 0.0), (0.86, 0.1), (0.76, 0.16), (0.0, 0.16)], 12,
                  lambda i, j: "gold_dark" if j == 0 else "gold"), T(0, ty, 0))
    n = 8
    b0, b1 = 0.16, 0.38
    top.add(lathe([(0.66, b0), (0.66, b1)], n * 2, "gold", phase=0.0), T(0, ty, 0))
    top.add(lathe([(0.6, b1), (0.6, b0)], n * 2, "gold_dark", phase=0.0), T(0, ty, 0))
    top.add(lathe([(0.66, b1), (0.6, b1)], n * 2, "gold_light", phase=0.0), T(0, ty, 0))
    for k in range(n):
        a = 360 * k / n
        pt = extrude([(-0.16, 0.0), (0.16, 0.0), (0.0, 0.28)], -0.035, 0.035, "gold", "gold_dark")
        top.add(pt, M(T(0, ty + b1, 0), RY(a), T(0, 0, -0.63)))
        top.add(sphere(0.06, 6, 3, "gold_light"), M(T(0, ty + b1, 0), RY(a), T(0, 0.31, -0.63)))
        gc = ("tech_rose", "tech_amethyst", "diamond", "red")[k % 4]
        top.add(bump(circle2(0, 0, 0.06, 6), gc, None, 0.03, 0.03), M(T(0, ty + 0.27, 0), RY(a), T(0, 0, -0.66)))
    # glow pool the crystal hovers over
    top.add(cyl(0.58, 0.15, 0.19, 12, "tech_ice_glow"), T(0, ty, 0))
    top.add(lathe([(0.32, 0.19), (0.18, 0.27), (0.0, 0.27)], 8, "white"), T(0, ty, 0))
    # the big floating crystal (bottom tip clear of the glow pool)
    prof = [(0.0, 0.0), (0.5, 0.4), (0.68, 0.62), (0.68, 0.95), (0.0, 1.43)]
    cc = [("tech_ice_mid", "tech_ice_dark"), ("tech_ice", "tech_ice_mid"), ("tech_ice_light", "tech_ice"),
          ("tech_ice_white", "tech_ice_light")]
    top.add(lathe(prof, 8, lambda i, j: cc[j][i % 2], phase=0.0), T(0, ty + 0.57, 0))
    return m


BUILDERS = [
    dict(name="CyberSpinMachine", fn=cyber_spin, mirror=True,
         parts=["Cabinet", "Screen", "Lever", "Topper", "Base", "NeonStrips"]),
    dict(name="CrystalKingdomMachine", fn=crystal_kingdom, mirror=True,
         parts=["Cabinet", "Screen", "Lever", "Topper", "Base"]),
]
