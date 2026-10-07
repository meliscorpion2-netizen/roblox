"""JackpotSpire, ConveyorSegment, CasinoTier1, PlotSign."""
import math

import numpy as np

from casino_geo import (Geo, Model, M, T, RX, RY, RZ, S, FACE, UP_TO_FRONT, box, lathe, cyl, sphere, dome,
                        extrude, puffy, puffy_star, coin, pyramid, circle2, star2)

COS8 = math.cos(math.radians(22.5))


# =====================================================================================
# MODEL 1 - JackpotSpire
# =====================================================================================
def _spire_R(y):
    """Circumradius of the octagonal spire body at height y."""
    if y <= 100:
        return 23.0 + (19.0 - 23.0) * (y - 56.0) / 44.0
    return 18.6 + (14.6 - 18.6) * (y - 104.4) / 33.6


def jackpot_spire():
    m = Model("JackpotSpire")
    base = m.part("Base")
    skirt = m.part("Skirt", smooth=True)
    spire = m.part("Spire")
    crown = m.part("Crown")
    rings = m.part("NeonRings", neon=True)

    # ---- Base: low gold-rimmed plinth under the slide edge (radius 60.6, 0..3)
    bp = [(60.6, 0.0), (60.6, 2.3), (60.25, 3.0), (60.0, 3.0)]
    base.add(lathe(bp, 64, lambda i, j: ("purple_deep" if (i // 2) % 2 else "purple_mid") if j == 0 else "gold"))
    # little gold studs around the plinth wall
    for k in range(32):
        a = k * 360 / 32 + 5.625
        base.add(sphere(0.45, 6, 3, "gold_light"), M(FACE(a), T(0, 1.15, -60.6)))

    # ---- Skirt: perfectly smooth cone slide r60 @ y3 -> r25 @ y50, white/purple stripes
    skirt.add(lathe([(60.0, 3.0), (25.0, 50.0)], 64, lambda i, j: "white" if (i // 4) % 2 == 0 else "purple"))

    # ---- Spire: tapered octagon 50 -> 146, mast to 170
    prof = [(24.0, 50.0), (27.6, 50.0), (27.6, 53.6), (25.2, 54.8), (23.2, 54.8), (23.0, 56.0),
            (19.0, 100.0), (20.6, 100.4), (20.6, 103.6), (18.6, 104.4), (14.6, 138.0),
            (16.0, 138.4), (16.0, 141.4), (14.4, 142.0), (12.6, 146.0), (2.2, 146.0), (2.2, 166.5), (0.0, 170.0)]

    def spire_col(i, j):
        if j in (5, 9, 13):
            return "purple_mid" if i % 2 else "purple_deep"
        if j == 14:
            return None                       # covered by the crown floor
        if j in (0, 6, 10):
            return "gold_dark"
        if j == 3:
            return "gold_light"
        return "gold"
    spire.add(lathe(prof, 8, spire_col))

    def on_face(angle, y, lift=0.0):
        R = _spire_R(y)
        ap = R * COS8
        dR = (19.0 - 23.0) / 44.0 if y <= 100 else (14.6 - 18.6) / 33.6
        tilt = math.degrees(math.atan(-dR * COS8))
        return M(FACE(angle), T(0, y, -ap - lift), RX(tilt))

    for k in range(8):
        a = k * 45.0
        if k % 2 == 0:
            spire.add(coin(6.2, 1.4), on_face(a, 78))
            spire.add(puffy_star(4.4, 2.0, 0.8, 0.8, "gold", "gold_dark", back=False), on_face(a, 121, 0.4))
        else:
            spire.add(puffy_star(5.6, 2.6, 0.9, 0.9, "gold", "gold_dark", back=False), on_face(a, 78, 0.45))
            spire.add(coin(4.5, 1.1), on_face(a, 121))
        # gold diamond studs between the motifs
        spire.add(puffy([(0, 1.6), (1.0, 0), (0, -1.6), (-1.0, 0)], 0.3, 0.5, "gold_light", "gold", back=False), on_face(a, 96, 0.15))

    # ---- Crown: band + spikes + gems + huge star
    cp = [(12.0, 145.2), (13.6, 145.8), (13.6, 152.2), (14.4, 153.0), (14.4, 154.2), (12.6, 154.2),
          (12.6, 146.4), (2.2, 146.4)]
    crown.add(lathe(cp, 16, lambda i, j: "purple_deep" if j == 6 else ("gold_light" if j in (3, 4) else "gold"), phase=0.0))
    for k in range(8):
        a = k * 45.0 + 22.5
        crown.add(pyramid(1.5, 5.4, 4, "gold"), M(FACE(a), T(0, 154.2, -13.5)))
        crown.add(sphere(0.9, 6, 3, "pink" if k % 2 else "cyan"), M(FACE(a), T(0, 160.0, -13.5)))
        crown.add(puffy([(0, 1.3), (0.9, 0), (0, -1.3), (-0.9, 0)], 0.3, 0.45, "pink" if k % 2 == 0 else "cyan",
                        "purple", back=False), M(FACE(k * 45.0), T(0, 149.0, -13.75)))
    crown.add(puffy_star(9.0, 4.3, 2.4, 1.7, "gold", "gold_dark"), T(0, 163.0, 0))
    crown.add(puffy_star(4.0, 1.9, 0.4, 0.5, "gold_light", "gold", back=False), T(0, 163.0, -2.85))
    crown.add(puffy_star(4.0, 1.9, 0.4, 0.5, "gold_light", "gold", back=False), M(T(0, 163.0, 2.85), RY(180)))

    # ---- NeonRings: glowing octagonal bands hugging the spire (+ one on the collar)
    def band(y0, y1, col, out=1.0):
        Rm = _spire_R((y0 + y1) / 2) + out
        return lathe([(_spire_R(y0), y0), (Rm, y0), (Rm, y1), (_spire_R(y1), y1)], 8, col)
    rings.add(band(60, 61.8, "neon_pink"))
    rings.add(band(89, 90.8, "neon_cyan"))
    rings.add(band(112, 113.8, "neon_pink"))
    rings.add(band(130, 131.8, "neon_cyan"))
    rings.add(lathe([(27.6, 51.2), (28.3, 51.2), (28.3, 52.4), (27.6, 52.4)], 8, "neon_pink"))
    rings.add(lathe([(14.4, 152.6), (14.9, 152.6), (14.9, 153.4), (14.4, 153.4)], 16, "neon_cyan", phase=0.0))
    return m


# =====================================================================================
# MODEL 2 - ConveyorSegment
# =====================================================================================
def _clip(poly, a, b, c):
    """Keep the part of a 2D polygon where a*x + b*y <= c (Sutherland-Hodgman)."""
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def conveyor_segment():
    m = Model("ConveyorSegment")
    belt = m.part("Belt")
    frame = m.part("Frame")
    r_in = m.part("RailInner", neon=True)
    r_out = m.part("RailOuter", neon=True)
    rollers = m.part("Rollers")

    HALF = 11.25
    RMID, Y = 70.0, 2.5
    L = math.radians(2 * HALF) * RMID
    SLICES = 8
    PERIOD = L / 6.0                 # 6 chevrons per segment -> tiles seamlessly
    SLOPE = 0.45

    def to3(s, w):
        a = s / RMID
        r = RMID + w
        return (r * math.sin(a), Y, -r * math.cos(a))

    # Belt top: perfectly flat (every vertex at y = 2.5) chevron stripes
    for sl in range(SLICES):
        s0 = -L / 2 + L * sl / SLICES
        s1 = -L / 2 + L * (sl + 1) / SLICES
        for sgn in (-1, 1):                       # w < 0 / w > 0 halves
            w0, w1 = (-8.0, 0.0) if sgn < 0 else (0.0, 8.0)
            for k in range(-6, 16):
                b0 = -L / 2 + k * PERIOD / 2
                b1 = b0 + PERIOD / 2
                poly = [(s0, w0), (s1, w0), (s1, w1), (s0, w1)]
                # s >= b0 + SLOPE*|w|  and  s <= b1 + SLOPE*|w|,  |w| = sgn*w
                poly = _clip(poly, -1.0, SLOPE * sgn, -b0)
                if len(poly) >= 3:
                    poly = _clip(poly, 1.0, -SLOPE * sgn, b1)
                if len(poly) >= 3:
                    belt.geo.add([to3(s, w) for s, w in poly], "charcoal" if k % 2 == 0 else "charcoal_light", (0, 1, 0))
    belt.add(lathe([(62.0, 2.0), (78.0, 2.0)], SLICES, "black_soft", -HALF, HALF))

    # Frame: chunky gold side beams (inner one flush with the belt so items slide on)
    def beam(r0, r1, y0, y1, hide_inner_from=None):
        ch = 0.3
        pts = [(r0, y0), (r1, y0), (r1, y1 - ch), (r1 - ch, y1), (r0 + ch, y1), (r0, y1 - ch), (r0, y0)]
        return lathe(pts, SLICES, lambda i, j: "gold_dark" if j == 0 else ("gold_light" if j in (2, 3, 4) else "gold"), -HALF, HALF)
    frame.add(lathe([(60.8, 1.9), (62.0, 1.9), (62.0, 2.0)], SLICES, lambda i, j: "gold_dark" if j == 0 else "gold", -HALF, HALF))
    frame.add(lathe([(62.0, 2.5), (61.6, 2.5)], SLICES, "gold_light", -HALF, HALF))
    frame.add(lathe([(61.0, 2.5), (60.8, 2.3), (60.8, 1.9)], SLICES, "gold", -HALF, HALF))
    frame.add(beam(78.0, 79.2, 1.9, 3.4))
    # bearing blocks holding each roller end
    for a in (-7.5, 0.0, 7.5):
        for r0, r1 in ((60.9, 62.0), (78.0, 79.1)):
            frame.add(box((-0.75, 0.85, -r1), (0.75, 1.9, -r0), "gold_dark", 0.12, skip=("+y",)), FACE(a))
    # legs at the centre of the segment
    for r0, r1 in ((60.9, 61.9), (78.1, 79.1)):
        frame.add(box((-0.55, 0.0, -r1 + 0.15), (0.55, 0.85, -r0 - 0.15), "gold_deep", 0.1, skip=("-y", "+y")))
        frame.add(box((-1.3, 0.0, -r1 - 0.3), (1.3, 0.35, -r0 + 0.3), "gold_dark", 0.1, skip=("-y",)))
    # bolt caps where the roller axles meet the beams
    for a in (-7.5, 0.0, 7.5):
        frame.add(cyl(0.34, 0.0, 0.15, 8, "gold_light"), M(FACE(a), T(0, 1.45, -79.1), RX(-90)))
        frame.add(cyl(0.34, 0.0, 0.15, 8, "gold_light"), M(FACE(a), T(0, 1.45, -60.9), RX(90)))
        frame.add(cyl(0.3, 0.0, 0.15, 8, "gold_light"), M(FACE(a), T(0, 2.75, -79.2), RX(-90)))

    # Rails: neon cyan. Inner rail is a low flat strip (top 2.72 < slide edge 3.0)
    r_in.add(lathe([(61.8, 2.5), (61.8, 2.72), (61.0, 2.72), (61.0, 2.5)], SLICES, "neon_cyan", -HALF, HALF))
    rp = [(78.6 + 0.4 * math.cos(math.radians(t)), 3.4 + 0.45 * math.sin(math.radians(t))) for t in range(0, 181, 30)]
    r_out.add(lathe(rp, SLICES, "neon_cyan", -HALF, HALF))

    # Rollers: chunky cartoon rollers under the belt, axis along the radius
    for a in (-7.5, 0.0, 7.5):
        prof = [(0.32, 62.0), (0.55, 62.35), (0.55, 64.0), (0.5, 64.3), (0.55, 64.6), (0.55, 69.7), (0.5, 70.0), (0.55, 70.3),
                (0.55, 75.4), (0.5, 75.7), (0.55, 76.0), (0.55, 77.65), (0.32, 78.0)]
        g = lathe(prof, 8, lambda i, j: "steel" if j in (0, 3, 4, 7, 8, 11) else "chrome")
        rollers.add(g, M(FACE(a), T(0, 1.45, 0), RX(-90)))
    return m


# =====================================================================================
# MODEL 3 - CasinoTier1
# =====================================================================================
HEART = [(0, -1.0), (0.55, -0.35), (0.85, 0.12), (0.8, 0.5), (0.5, 0.72), (0.18, 0.6), (0, 0.38),
         (-0.18, 0.6), (-0.5, 0.72), (-0.8, 0.5), (-0.85, 0.12), (-0.55, -0.35)]
DIAMOND = [(0, 1.0), (0.7, 0), (0, -1.0), (-0.7, 0)]
SPADE = [(0, 1.0), (0.55, 0.38), (0.82, -0.05), (0.72, -0.4), (0.4, -0.5), (0.14, -0.32), (0.3, -0.95),
         (-0.3, -0.95), (-0.14, -0.32), (-0.4, -0.5), (-0.72, -0.4), (-0.82, -0.05), (-0.55, 0.38)]


def playing_card(suit, col):
    g = box((-1.5, -2.1, -0.15), (1.5, 2.1, 0.15), "white", 0.12)
    g += puffy([(x * 1.0, y * 1.0) for x, y in suit], 0.1, 0.18, col, back=False).xf(T(0, 0, -0.2))
    for sx, sy in ((-1, 1), (1, -1)):
        g += extrude([(x * 0.32 + sx * 1.0, y * 0.32 + sy * 1.55) for x, y in suit], -0.2, -0.15, col, back=False)
    return g


def casino_tier1():
    m = Model("CasinoTier1")
    floor = m.part("Floor")
    walls = m.part("Walls")
    sign = m.part("SignBoard")
    neon = m.part("NeonStrip", neon=True)
    door = m.part("Door")
    bulbs = m.part("Bulbs", neon=True)

    W, D, H, t = 28.0, 22.0, 13.4, 1.5
    # ---- Floor: carpet inside, doorway, step, red runner outside
    ix, iz = W - t, D - t
    floor.add(box((-ix, 0, -iz), (ix, 0.999, iz), "red", skip=("-y", "+y", "-x", "+x", "-z", "+z")))
    border = 0.8
    for x0, x1, z0, z1 in ((-ix, ix, -iz, -iz + border), (-ix, ix, iz - border, iz),
                           (-ix, -ix + border, -iz + border, iz - border), (ix - border, ix, -iz + border, iz - border)):
        floor.geo.add([(x0, 1, z0), (x1, 1, z0), (x1, 1, z1), (x0, 1, z1)], "gold_dark", (0, 1, 0))
    nx, nz = 12, 9
    cx0, cx1, cz0, cz1 = -ix + border, ix - border, -iz + border, iz - border
    dx, dz = (cx1 - cx0) / nx, (cz1 - cz0) / nz
    for i in range(nx):
        for j in range(nz):
            x0, z0 = cx0 + i * dx, cz0 + j * dz
            xm, zm = x0 + dx / 2, z0 + dz / 2
            dia = [(xm, z0), (x0 + dx, zm), (xm, z0 + dz), (x0, zm)]
            floor.geo.add([(x, 1, z) for x, z in dia], "red_dark" if (i + j) % 2 == 0 else "purple_deep", (0, 1, 0))
            corners = [((x0, z0), (xm, z0), (x0, zm)), ((x0 + dx, z0), (x0 + dx, zm), (xm, z0)),
                       ((x0 + dx, z0 + dz), (xm, z0 + dz), (x0 + dx, zm)), ((x0, z0 + dz), (x0, zm), (xm, z0 + dz))]
            for tri in corners:
                floor.geo.add([(x, 1, z) for x, z in tri], "red", (0, 1, 0))
            if (i + j) % 2 == 0:
                s = 0.35
                floor.geo.add([(xm, 1.01, zm - dz * s / 2), (xm + dx * s / 2, 1.01, zm), (xm, 1.01, zm + dz * s / 2),
                               (xm - dx * s / 2, 1.01, zm)], "gold", (0, 1, 0))
    floor.add(box((-7, 0, -D), (7, 1, -iz), "red", skip=("-y", "-x", "+x", "+z"), top="red"))
    floor.add(box((-7, 0, -D - 2.2), (7, 0.5, -D), "gold", 0.0, skip=("-y", "+z"), top="gold_light"))
    floor.add(box((-5, 0, -D - 12), (5, 0.18, -D - 2.2), "red", skip=("-y", "+z")))
    for sx in (-1, 1):
        floor.add(box((sx * 4.4 - 0.3, 0, -D - 12), (sx * 4.4 + 0.3, 0.2, -D - 2.2), "gold", skip=("-y", "+z")))

    # ---- Walls: cream with red base trim and gold cap trim
    pieces = [((-W, 0, iz), (W, H, D), ("-y",)),
              ((-W, 0, -iz), (-ix, H, iz), ("-y", "-z", "+z")),
              ((ix, 0, -iz), (W, H, iz), ("-y", "-z", "+z")),
              ((-W, 0, -D), (-7, H, -iz), ("-y",)),
              ((7, 0, -D), (W, H, -iz), ("-y",)),
              ((-7, 10, -D), (7, H, -iz), ("-x", "+x"))]
    for lo, hi, sk in pieces:
        walls.add(box(lo, hi, "cream", skip=sk + ("+y",)))
    # cap
    cap = [((-W - 0.25, H, iz - 0.25), (W + 0.25, 14, D + 0.25)),
           ((-W - 0.25, H, -iz + 0.25), (-ix + 0.25, 14, iz - 0.25)),
           ((ix - 0.25, H, -iz + 0.25), (W + 0.25, 14, iz - 0.25)),
           ((-W - 0.25, H, -D - 0.25), (W + 0.25, 14, -iz + 0.25))]
    for lo, hi in cap:
        walls.add(box(lo, hi, "gold", 0.15, skip=("-y",), top="gold_light"))
    # red base trim (outside + inside)
    walls.add(box((-W - 0.3, 0, D - 0.01), (W + 0.3, 1.8, D + 0.3), "red", 0.08, skip=("-y", "-z")))
    walls.add(box((-W - 0.3, 0, -iz + 0.01), (-W + 0.01, 1.8, iz - 0.01), "red", 0.0, skip=("-y", "+x", "-z", "+z")))
    walls.add(box((W - 0.01, 0, -iz + 0.01), (W + 0.3, 1.8, iz - 0.01), "red", 0.0, skip=("-y", "-x", "-z", "+z")))
    for x0, x1 in ((-W - 0.3, -7.0), (7.0, W + 0.3)):
        walls.add(box((x0, 0, -D - 0.3), (x1, 1.8, -D + 0.01), "red", 0.08, skip=("-y", "+z")))
    # red stripe band
    walls.add(box((-W - 0.15, 8.6, D - 0.01), (W + 0.15, 9.2, D + 0.15), "red", skip=("-z", "-y")))
    for x0, x1 in ((-W - 0.15, -8.4), (8.4, W + 0.15)):
        walls.add(box((x0, 8.6, -D - 0.15), (x1, 9.2, -D + 0.01), "red", skip=("+z",)))
    for sx in (-1, 1):
        x0, x1 = (W - 0.01, W + 0.15) if sx > 0 else (-W - 0.15, -W + 0.01)
        walls.add(box((x0, 8.6, -D + 0.01), (x1, 9.2, D - 0.01), "red", skip=("-z", "+z", "+x" if sx < 0 else "-x")))
    # inner red wainscot
    walls.add(box((-ix, 1.0, iz - 0.2), (ix, 2.6, iz + 0.01), "red_dark", skip=("+z", "-y")))
    for sx in (-1, 1):
        x0, x1 = (ix - 0.2, ix + 0.01) if sx > 0 else (-ix - 0.01, -ix + 0.2)
        walls.add(box((x0, 1.0, -iz), (x1, 2.6, iz - 0.2), "red_dark", skip=("+x" if sx > 0 else "-x", "-y", "+z", "-z")))
    for x0, x1 in ((-ix, -7.0), (7.0, ix)):
        walls.add(box((x0, 1.0, -iz - 0.01), (x1, 2.6, -iz + 0.2), "red_dark", skip=("-z", "-y")))
    # corner pillars with gold ball tops
    for sx in (-1, 1):
        for sz in (-1, 1):
            cx, cz = sx * (W - 1.0), sz * (D - 1.0)
            walls.add(box((cx - 1.4, 0, cz - 1.4), (cx + 1.4, 14.6, cz + 1.4), "red", 0.3, skip=("-y",), top="gold"))
            walls.add(sphere(1.1, 8, 4, "gold"), T(cx, 15.5, cz))
    # playing cards and coins on the front facade
    for sx in (-1, 1):
        walls.add(playing_card(HEART, "red"), M(T(sx * 16.8, 5.4, -D - 0.25), RZ(sx * 10)))
        walls.add(playing_card(SPADE if sx < 0 else DIAMOND, "black" if sx < 0 else "red"), M(T(sx * 14.2, 5.1, -D - 0.55), RZ(-sx * 8)))
        walls.add(coin(1.8, 0.5), T(sx * 22.6, 6.0, -D))
        walls.add(coin(1.2, 0.4), T(sx * 20.5, 3.8, -D))
        walls.add(coin(1.0, 0.4), T(sx * 24.4, 3.6, -D))

    # ---- SignBoard: gold frame + perfectly flat blank panel above the door
    sign.add(box((-10, 10.4, -D - 0.9), (10, 17.6, -D), "gold", 0.25, top="gold_light"))
    sign.add(box((-8.6, 11.6, -D - 1.15), (8.6, 16.4, -D - 0.9), "purple_deep", skip=("+z",)))
    sign.add(puffy_star(1.3, 0.6, 0.4, 0.4, "gold_light", "gold", back=False), T(0, 18.6, -D - 0.45))
    sign.add(box((-0.25, 17.55, -D - 0.6), (0.25, 17.9, -D - 0.3), "gold_dark", skip=("-y",)))

    # ---- Bulbs: marquee bulbs around the sign frame (separate so they can glow)
    xs = np.linspace(-9.3, 9.3, 13)
    for x in xs:
        for y in (11.0, 17.0):
            bulbs.add(dome(0.33, 6, 2, "bulb"), M(T(x, y, -D - 0.9), RX(-90)))
    for y in np.linspace(12.5, 15.5, 3):
        for x in (-9.3, 9.3):
            bulbs.add(dome(0.33, 6, 2, "bulb"), M(T(x, y, -D - 0.9), RX(-90)))

    # ---- NeonStrip: pink neon tube along the front wall
    for x0, x1 in ((-27.0, -10.6), (10.6, 27.0)):
        neon.add(box((x0, 11.8, -D - 0.55), (x1, 12.45, -D), "neon_pink", 0.2, skip=("+z",)))
        neon.add(box((x0, 7.2, -D - 0.45), (x1, 7.6, -D), "neon_pink", 0.15, skip=("+z",)))

    # ---- Door: gold frame trim around the opening + two red doors swung open
    door.add(box((-8.4, 0, -D - 0.5), (-7.0, 10.4, -D), "gold", 0.15, skip=("+z", "-y"), top="gold_light"))
    door.add(box((7.0, 0, -D - 0.5), (8.4, 10.4, -D), "gold", 0.15, skip=("+z", "-y"), top="gold_light"))
    door.add(box((-7.0, 9.3, -D - 0.5), (7.0, 10.4, -D), "gold", 0.15, skip=("+z",), top="gold_light"))
    for sx in (-1, 1):
        leaf = box((-0.3, 0.2, 0), (0.3, 9.1, 6.2), "red", 0.12, top="red_dark")
        # gold panel trims and a round window on each face of the leaf
        for side in (-1, 1):
            xo = side * 0.3
            g = Geo()
            g += box((-0.08, 1.0, 0.7), (0.08, 1.4, 5.5), "gold")
            g += box((-0.08, 4.0, 0.7), (0.08, 4.4, 5.5), "gold")
            g += box((-0.08, 1.0, 0.7), (0.08, 8.3, 1.1), "gold")
            g += box((-0.08, 1.0, 5.1), (0.08, 8.3, 5.5), "gold")
            g += box((-0.08, 7.9, 0.7), (0.08, 8.3, 5.5), "gold")
            leaf += g.xf(T(xo + side * 0.08, 0, 0))
            leaf += puffy(DIAMOND, 0.12, 0.25, "gold_light", "gold", back=False).xf(M(T(xo + side * 0.1, 6.0, 3.1), RY(90 * side), S(1.1)))
        door.add(leaf, M(T(sx * 7.65, 0, -D - 6.7)))
    return m


# =====================================================================================
# MODEL 4 - PlotSign
# =====================================================================================
def die(size, pips="red"):
    h = size / 2
    g = box((-h, -h, -h), (h, h, h), "white", size * 0.16)
    faces = {(0, -1): 1, (0, 1): 6, (1, 1): 2, (1, -1): 5, (2, -1): 3, (2, 1): 4}
    layouts = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
               5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}
    p = size * 0.11
    off = size * 0.26
    for (ax, s), n in faces.items():
        o = [a for a in range(3) if a != ax]
        for u, v in layouts[n]:
            c = np.zeros(3)
            c[ax] = s * (h + 0.01)
            c[o[0]] = u * off
            c[o[1]] = v * off
            lo, hi = c - p, c + p
            lo[ax], hi[ax] = (c[ax] - 0.02, c[ax] + 0.04) if s > 0 else (c[ax] - 0.04, c[ax] + 0.02)
            g += box(lo, hi, pips)
    return g


def plot_sign():
    m = Model("PlotSign")
    display = m.part("Display", gradient=False)
    accent = m.part("Accent", gradient=False)
    posts = m.part("Posts")
    deco = m.part("Decorations")
    bulbs = m.part("Bulbs", neon=True)

    # Display: one perfectly flat blank white quad, recessed in the frame, facing -Z
    display.add(box((-7.1, 3.9, -0.3), (7.1, 9.3, 0.0), "white", skip=("+z", "-x", "+x", "-y", "+y")))
    # Accent: thick neutral white frame + back plate (recoloured per player in-game)
    for lo, hi, sk in (((-8.4, 2.6, -0.7), (8.4, 3.9, 0.7), ()), ((-8.4, 9.3, -0.7), (8.4, 10.6, 0.7), ()),
                       ((-8.4, 3.9, -0.7), (-7.1, 9.3, 0.7), ("-y", "+y")), ((7.1, 3.9, -0.7), (8.4, 9.3, 0.7), ("-y", "+y"))):
        accent.add(box(lo, hi, "white", 0.28, skip=sk))
    accent.add(box((-7.1, 3.9, 0.0), (7.1, 9.3, 0.7), "white", skip=("-z", "-x", "+x", "-y", "+y")))
    # Posts: chunky gold posts with feet, rings and ball caps
    for sx in (-1, 1):
        x = sx * 9.2
        posts.add(box((x - 0.8, 0.8, -0.8), (x + 0.8, 10.8, 0.8), "gold", 0.25, skip=("-y",), top="gold_light"))
        posts.add(box((x - 1.2, 0.0, -1.2), (x + 1.2, 0.8, 1.2), "gold_dark", 0.2, skip=("-y",)))
        posts.add(box((x - 0.95, 2.0, -0.95), (x + 0.95, 2.4, 0.95), "gold_dark", 0.1))
        posts.add(box((x - 0.95, 9.6, -0.95), (x + 0.95, 10.0, 0.95), "gold_dark", 0.1))
        posts.add(sphere(0.95, 8, 4, "gold_light"), T(x, 11.6, 0))
    # Decorations: golden star, dice, coins on top of the frame
    deco.add(puffy_star(1.9, 0.85, 0.7, 0.55, "gold", "gold_dark"), T(0, 12.15, 0))
    deco.add(die(1.5), M(T(-4.6, 10.6 + 0.75, 0), RY(25)))
    deco.add(die(1.25), M(T(-6.5, 10.6 + 0.625, 0.1), RY(-15)))
    for k in range(4):
        deco.add(cyl(0.85, 0, 0.3, 12, "gold_dark", topcol="gold_light"), T(4.5 + 0.06 * (k % 2), 10.6 + 0.3 * k, -0.04 * k))
    deco.add(coin(1.05, 0.35), M(T(6.6, 11.65, 0.15), RY(-20)))
    deco.add(coin(1.05, 0.35), M(T(6.6, 11.65, 0.15), RY(160)))
    # Bulbs: marquee bulbs around the frame (separate mesh so they can glow)
    for x in np.linspace(-7.75, 7.75, 11):
        for y in (3.25, 9.95):
            bulbs.add(dome(0.3, 6, 2, "bulb"), M(T(x, y, -0.7), RX(-90)))
    for y in (4.95, 6.6, 8.25):
        for x in (-7.75, 7.75):
            bulbs.add(dome(0.3, 6, 2, "bulb"), M(T(x, y, -0.7), RX(-90)))
    return m
