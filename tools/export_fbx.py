"""Converts models/*.glb into Roblox-ready binary FBX files (models/fbx/*.fbx) using Blender as a module.

    pip install bpy        # Blender as a Python module
    python3 tools/export_fbx.py

Output convention matches the GLB files: 1 FBX unit = 1 stud (UnitScaleFactor 1, as Roblox expects),
Y up, front facing -Z, one mesh object per named part with its pivot kept as the object origin,
all parented to an empty named after the model. The palette texture is embedded in each file.
"""
import os
import sys

import bpy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "models")
DST = os.path.join(ROOT, "models", "fbx")
NAMES = ["JackpotSpire", "ConveyorSegment", "CasinoTier1", "PlotSign", "LuckyFruitsMachine",
         "OceanTreasureMachine", "NeonFortuneMachine", "GoldenPharaohMachine"]


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.unit_settings.system = "METRIC"
    s.unit_settings.scale_length = 0.01     # 1 Blender unit -> 1 FBX centimetre -> 1 Roblox stud


def convert(name):
    reset()
    bpy.ops.import_scene.gltf(filepath=os.path.join(SRC, name + ".glb"), merge_vertices=False)
    for ob in bpy.context.scene.objects:
        if ob.type == "MESH":
            ob.data.name = ob.name          # mesh data carries the exact part name too
            for poly in ob.data.polygons:
                poly.use_smooth = False
    out = os.path.join(DST, name + ".fbx")
    bpy.ops.export_scene.fbx(
        filepath=out,
        object_types={"EMPTY", "MESH"},
        apply_unit_scale=True,
        global_scale=1.0,
        apply_scale_options="FBX_SCALE_NONE",
        axis_forward="-Z",
        axis_up="Y",
        use_mesh_modifiers=False,
        mesh_smooth_type="FACE",
        add_leaf_bones=False,
        bake_anim=False,
        path_mode="COPY",
        embed_textures=True,
        use_custom_props=False,
    )
    return out


if __name__ == "__main__":
    os.makedirs(DST, exist_ok=True)
    for n in (sys.argv[1:] or NAMES):
        print("exported", convert(n))
