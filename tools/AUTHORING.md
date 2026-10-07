# Authoring a model module (Casino Machine Tycoon kit)

Every model is built procedurally in Python from the small kit in `tools/casino_geo.py`, exported to GLB (and later FBX), and previewed with a built-in renderer. This guide covers what a module author needs.

## Your module
- Your module is one file, `tools/<module>.py`, listed in `tools/registry.py`. **Edit only your own module file.**
  - Don't change `casino_geo.py`, `registry.py`, the generator, the validators or other modules.
  - If the kit has a bug that blocks you, work around it in your module and report it.
- End the module with a `BUILDERS` list:
  ```python
  BUILDERS = [
      dict(name="WildWestMachine", fn=wild_west, mirror=True,
           parts=["Cabinet", "Screen", "Lever", "Topper", "Base"],
           view=dict(eye=(-0.8, 0.42, -1.3), fit=0.8)),   # view is optional
  ]
  ```
  - `name` is the exact model and file name.
  - `parts` lists the exact mesh names. The model must contain exactly these parts: no extras, none missing, none empty.
- **Build and preview:** `python3 tools/generate_casino_models.py WildWestMachine PirateFortuneMachine`. This writes `models/<Name>.glb` and `previews/<Name>.png`.
  - Look at the PNG with your image-reading tool and iterate until it looks good.
  - The preview camera looks from the front-left-above, so the -Z front faces the camera.
- **Check:** `python3 tools/validate_glb.py WildWestMachine`. It prints the part names, overall size, min/max and the pivots of special parts.
- You may also render extra views into the scratchpad to inspect the back or side. Use `casino_geo.render([(model, None)], path, eye=(x, y, z), fit=...)`, where `eye` is the direction from the model towards the camera.
- **Don't run git.**

## Conventions (hard rules)
- **Units and axes:** 1 unit = 1 stud. +Y is up. **The front faces -Z.** The pivot is at ground level (Y=0), centred on the base, unless the spec says otherwise.
- **Parts and pivots:**
  - Every listed part is its own `Part` with exactly the given name: `m.part("Name", pivot=(x, y, z), neon=False, gradient=True)`.
  - A part's pivot is its node origin. Geometry is always added in **model (world) coordinates**; the exporter subtracts the pivot.
- **Glowing parts:** use `neon=True` (NeonStrip, NeonStrips, Lava, glowing bulbs and similar). They are exported with an emissive material and the user sets `Material = Neon` in Roblox.
- **Textures:** every part is textured with the shared palette texture automatically, so nothing can come out plain grey. Still, avoid boring greys unless the spec asks for silver, stone or similar.
- **Mobile budget:** low triangle counts.
  - Slot machines: about 1.5k-5k triangles.
  - Buildings: 8k or fewer.
  - Plaza props: 3k or fewer.
  - Decor and boxes: about 1.5k or fewer.
  - Any single part: fewer than 10k.
- **No hidden geometry:**
  - Skip faces that are hidden: `box(..., skip=("-y",))` for faces on the ground, faces pressed against other geometry, and bottoms of things sitting on surfaces.
  - Avoid coplanar overlapping faces between parts (z-fighting). Offset by 0.01-0.05 or skip one of them.
- **Style:** low-poly, chunky, rounded, cartoon proportions, big readable shapes and clean silhouettes.
  - Use saturated flat colours and the casino palette (gold, purple, pink, cyan, red) plus each model's theme colours.
  - No realistic or photo textures. The only "texture" is flat palette colour.
  - Detail and flashiness rise with rarity: Common < Uncommon < Rare < Epic < Legendary < Mythic < Secret.

## Kit API (`from casino_geo import ...`)
- **Matrices** (4x4, column vectors):
  - `T(x,y,z)`, `S(sx,sy,sz)`, `RX/RY/RZ(deg)`.
  - `M(a, b, c)` composes them, with the right-most applied first.
  - `FACE(angle)` turns the front direction (-Z) towards `angle` degrees around +Y. 0 = -Z (front), 90 = +X, 180 = +Z, -90 = -X.
  - `UP_TO_FRONT()` maps +Y onto -Z, which turns a lathe axis to point at the viewer.
- **`Geo`** is a bag of coloured polygons.
  - `g.xf(matrix)` transforms it, `g + g2` combines two, `g.add(points, colour, expected_normal)` adds a polygon, and `part.add(geo, matrix=None)` adds geometry to a part.
  - Polygons must be planar. Concave polygons are ear-clipped automatically.
- **Primitives** (all return a `Geo`):
  - `box(lo, hi, col, bevel=0, skip=(), top=None, front=None)`: an axis-aligned box. `bevel` gives chunky chamfered edges. `skip` takes face names "-x", "+x", "-y", "+y", "-z" and "+z".
  - `lathe(profile, seg, col, a0=0, a1=360, phase=0.5, caps=False, rmod=None)`: a surface of revolution around +Y.
    - `profile` is a list of `(r, y)`, ordered bottom-to-top along the outer wall, or CCW for a closed outline.
    - `col` can be a function `(seg_i, edge_j) -> colour or None`, where None skips that face.
    - `a0`/`a1` give a partial arc, in degrees from -Z towards +X. `rmod(i)` scales the radius per segment.
  - `cyl(r, y0, y1, seg, col, top=True, bottom=False, topcol=None)`, `sphere(r, seg, rings, col)`, `dome(r, seg, rings, col)` (a half-sphere on y=0), `pyramid(r, h, n, col)`.
  - `extrude(poly2d, z0, z1, col, side=None, front=True, back=True)`: a prism of an XY polygon between z0 (the front cap, facing -Z) and z1.
  - `puffy(poly2d, thick, bulge, col, side=None, back=True)`: a chunky pillow shape whose faces rise to a centre point; good for stars, gems and icons. `puffy_star(r_out, r_in, thick, bulge, col, side, n=5)`.
  - `coin(r, t, col="gold", face="gold_light")`: a coin facing -Z with its back at z=0. `ring2_geo(cx, cy, r_in, r_out, n, z0, z1, col)` is a flat ring.
  - `frustum_box(lo_w, lo_d, hi_w, hi_d, y0, y1, col, skip=(), top=None, zc=0, xc=0)`: a tapered box.
- **2D helpers:** `circle2(cx, cy, r, n, start=90, sx=1, sy=1)`, `star2(cx, cy, ro, ri, n)`.
- **Palette:**
  - `PALETTE` holds the existing colours: gold, gold_light, gold_dark, gold_deep, purple, purple_deep, purple_mid, purple_light, pink, cyan, red, red_dark, red_deep, white, offwhite, cream, cream_dark, charcoal, charcoal_light, black, black_soft, chrome, steel, steel_dark, neon_pink, neon_cyan, neon_magenta, neon_purple, bulb, cherry, leaf, leaf_dark, lemon, aqua, teal, teal_dark, ocean_deep, shell, coral, pearl, fish, brass, holo, holo_purple, seven, diamond, diamond_dark, lapis, lapis_dark, turquoise, sand, stone_*, pad_green and more. Read `casino_geo.py` for the exact hex values.
  - **New colours:** call `add_colors({"<prefix>_name": "#RRGGBB", ...}, neon={"<prefix>_glow"})` once at the top of your module. **Every new colour name must start with your module prefix** (given in your task) to avoid clashes with other modules.
- **Front-facing art on slot machines** (screens, symbols, numbers, text-like shapes): author in plain XY, with +X to the right as seen from **+Z**. Then set `mirror=True` in BUILDERS; the build mirrors X once, so the art reads correctly from the -Z front and the lever lands on the player's right (model -X).

## Reusable helpers
- **`models_machines.py`:**
  - `LEVER_PIVOT=(2.6, 4.2, 0.3)` (before mirroring).
  - Shapes: `rounded_rect2(x0, y0, x1, y1, r_top, r_bottom)`, `side_prism(poly_zy, x0, x1, col, side)`, `align_y(d)`, `rod(p0, p1, r, col, seg)`.
  - Stickers: `flat(poly, col, t)` is a thin sticker facing -Z with its back at z=0, `bump(poly, col, side, t, b)` is a chunky sticker, `on_front(g, x, y, z, s)` places one.
  - Cabinet pieces: `deck(...)`, `lever_hub(col, ring, x_in, x_out, r)` (a hub along X centred on the origin), `screen_panel(x0, x1, y0, y1, z, col, cols, divider)`, `strip_along(p0, p1, w, z0, z1, col, inset, facing_back)` (a thin neon bar along a 2D segment).
  - Icons (unit size, facing -Z): `ic_seven`, `ic_diamond`, `ic_cherry`, `ic_anchor`, `ic_eye` and others.
  - **Read the four existing machines in that file**, `lucky_fruits` (Common), `ocean_treasure` (Rare), `neon_fortune` (Epic) and `golden_pharaoh` (Legendary). They are the reference for structure, scale, rarity scaling and polish.
- **`models_world.py`:**
  - `casino_tier1()` is the reference building (56x44, 14-tall walls, open top).
  - `plot_sign()`, `machine_slot()`, `die(size)`, `playing_card(suit, col)`, `HEART/DIAMOND/SPADE` outlines, `_rounded_rect_xy(...)`.
  - `previews/*.png` show what the existing set looks like.

## Slot machine rules (all machines)
- **Size:** 6 wide (X) x 5 deep (Z) x 9 tall (Y). Stay within x ±3.0 and z ±2.5 (small front details may reach z -2.85). Overall height should be 8.9-9.1.
- **Parts:** Cabinet, Screen, Lever, Topper, Base, plus any extra mesh listed. Each is separate.
- **Base:** a plinth, roughly y 0..1.
- **Cabinet:** within about x ±2.3, top around y 7.0-7.3.
- **Screen:** faces -Z, on the cabinet front.
- **Lever:** its pivot is at its base hub (the rotation point), on the +X side before mirroring: `pivot=LEVER_PIVOT`. Geometry goes from the hub upwards, within x ≤ 3.0.
- **Topper:** sits on the cabinet top, with its pivot at `(0, cabinet_top_y, 0)`. It must be **centred on the vertical axis**, so its bounds are roughly symmetric in X and Z, because it spins.
  - An extra mesh that belongs to the topper (Wings, Rings) uses the same pivot as the Topper, so it can spin with it.
