# Casino Machine Tycoon: 3D models

Eight low-poly models for a Roblox casino tycoon simulator. They all share one style: chunky rounded shapes, flat saturated colours, and a gold, purple, pink, cyan and red casino palette.

| File (`models/`) | Parts (one mesh each, exact names) | Triangles |
|---|---|---|
| `JackpotSpire.glb` | Spire, Skirt, Crown, NeonRings, Base | 4,092 |
| `ConveyorSegment.glb` | Belt, Frame, RailInner, RailOuter, Rollers | 1,664 |
| `CasinoTier1.glb` | Floor, Walls, SignBoard, NeonStrip, Door, *Bulbs* | 4,367 |
| `PlotSign.glb` | Display, Accent, Posts, Decorations, *Bulbs* | 2,204 |
| `LuckyFruitsMachine.glb` (Common) | Cabinet, Screen, Lever, Topper, Base | 1,453 |
| `OceanTreasureMachine.glb` (Rare) | Cabinet, Screen, Lever, Topper, Base | 2,718 |
| `NeonFortuneMachine.glb` (Epic) | Cabinet, Screen, Lever, Topper, Base, NeonStrips | 1,595 |
| `GoldenPharaohMachine.glb` (Legendary) | Cabinet, Screen, Lever, Topper, Base, Wings | 3,812 |

The renders in `previews/` include the spire with 16 conveyor segments around it and a lineup of the four machines.

## Conventions
- 1 unit = 1 stud, +Y is up, and the front faces **-Z**.
- Each file has one root node named after the model. Every part is a child node holding one mesh with the same name. The node's translation is the part's pivot.
- **Pivots**
  - Most models: ground level, at the centre of the base.
  - ConveyorSegment: the **ring centre** (0,0,0). The segment covers -11.25° to +11.25° around -Z, so the copies go at `CFrame.Angles(0, math.rad(22.5*i), 0)`.
  - Lever: the hub at its base, so you can animate it by rotating around X.
  - Topper (and Wings on the Pharaoh): the vertical centre axis at the top of the cabinet, so you can spin them around Y.
- **Colours:** parts with several colours use a shared palette texture (`CasinoPalette`, flat colour cells with a very slight vertical gradient). Parts with a single colour have no texture, just a material colour, so you can recolour them in Roblox. This applies to PlotSign `Display` (white) and `Accent` (neutral white).
- **Glowing parts are separate meshes:** NeonRings, RailInner, RailOuter, NeonStrip, NeonStrips and Bulbs. Set their `Material` to `Neon` in Studio.

## Key dimensions
- **JackpotSpire:** 121 studs across and 172 tall (the star tip sits 2 studs above the spire top).
  - Skirt: a single smooth cone from r60 at y3 to r25 at y50, with no bumps.
  - Spire: y50 to y170.
  - Base: radius 60.6, so the conveyor ring fits around it.
- **ConveyorSegment:**
  - Belt: r62 to r78, with its top at exactly y = 2.5.
  - Inner frame and RailInner: kept low, with the rail top at y2.72, under the slide's bottom edge at y3. Items sliding off the spire therefore drop straight onto the belt.
  - Outer frame and RailOuter: these form the guard wall.
- **CasinoTier1:** footprint 56 × 44, walls 14 tall, open top.
  - Entrance: 14 wide, centred on the -Z side.
  - Floor top: y = 1.
  - The sign panel is a flat, blank quad.
- **PlotSign:** 20 wide and about 14 tall. `Display` is a single flat quad facing -Z.
- **Slot machines:** 6 × 5 × about 9 studs.
  - Screen faces -Z.
  - Lever is on the player's right side when they face the machine (model -X).

## Importing into Roblox Studio
Every model also exists as a **binary FBX** in `models/fbx/` (FBX 7.4, the palette texture embedded). Use these for a direct import into Roblox.

1. Open Home/Avatar → **Import 3D** and choose a file from `models/fbx/` (or a `.glb`).
2. The FBX files are 1 unit = 1 stud (UnitScaleFactor 1), with Y up and the front at −Z. If the preview size looks wrong, set **File Dimensions / Scale Unit to "Studs"**.
3. Keep "Import as a single Model" on so each part becomes a named MeshPart, then set the neon parts to `Material = Neon`.

## Regenerating
The models are fully procedural. You need Python 3 with numpy, plus Pillow for the previews.

```
python3 tools/generate_casino_models.py   # writes models/*.glb and previews/*.png
python3 tools/validate_glb.py             # checks part names, pivots and sizes
pip install bpy && python3 tools/export_fbx.py   # converts the GLBs to models/fbx/*.fbx (Blender as a module)
python3 tools/validate_fbx.py             # checks the FBX units, axes, part names, pivots and sizes
```

To change a model, edit `tools/models_world.py` or `tools/models_machines.py`. The palette is in `tools/casino_geo.py`.
