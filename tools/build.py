"""Construit, vérifie, exporte (FBX) et rend tous les props.

    python3 tools/build.py              # tout
    python3 tools/build.py 04 17        # seulement les modèles dont l'id commence par 04 ou 17
    python3 tools/build.py --no-render  # sans les vignettes
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(__file__))
import lib  # noqa: E402
import registry  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "models")
RENDERS = os.path.join(ROOT, "renders")
PALETTE_PNG = os.path.join(OUT, "palette.png")
MAX_TRIS = 5000


def setup_render():
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 24
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 3
    sc.render.resolution_x = sc.render.resolution_y = 480
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "Standard"
    world = bpy.data.worlds.new("W") if not sc.world else sc.world
    sc.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.9, 0.92, 1.0, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
    cam_data = bpy.data.cameras.new("Cam")
    cam_data.type = "ORTHO"
    cam = bpy.data.objects.new("Cam", cam_data)
    sun_data = bpy.data.lights.new("Sun", "SUN")
    sun_data.energy = 3.2
    sun_data.angle = math.radians(8)
    sun = bpy.data.objects.new("Sun", sun_data)
    sun.rotation_euler = (math.radians(50), math.radians(-12), math.radians(-35))
    return cam, sun


def glow_material():
    mat = bpy.data.materials.get("ApercuLueur")
    if mat:
        return mat
    mat = bpy.data.materials.new("ApercuLueur")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = 0.2
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    em = nt.nodes.new("ShaderNodeEmission")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.materials["Palette"].node_tree.nodes["Image Texture"].image
    tex.interpolation = "Closest"
    em.inputs["Strength"].default_value = 1.3
    nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    mat.blend_method = "BLEND"
    return mat


def render(model, objs, cam, sun, path):
    sc = bpy.context.scene
    for o in (cam, sun):
        if o.name not in sc.collection.objects:
            sc.collection.objects.link(o)
    sc.camera = cam
    X, Y, Z = model.dims
    w, d, h = X * lib.STUD_M, Z * lib.STUD_M, Y * lib.STUD_M
    center = Vector((0, 0, h / 2))
    direction = Vector((0.62, -1.0, 0.62)).normalized()  # vue 3/4 avant
    dist = max(w, d, h) * 3 + 2
    cam.location = center + direction * dist
    cam.rotation_euler = (-direction).to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
    # cadrage ortho : projeter les 8 coins
    import itertools
    m = cam.matrix_world.inverted()
    xs, ys = [], []
    for sx, sy, sz in itertools.product((-0.5, 0.5), repeat=3):
        p = m @ Vector((sx * w, sy * d, h / 2 + sz * h))
        xs.append(p.x)
        ys.append(p.y)
    span = max(max(xs) - min(xs), max(ys) - min(ys))
    cam.data.ortho_scale = span * 1.12
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    cam.location = cam.matrix_world @ Vector((cx, cy, 0))
    cam.data.clip_end = dist * 3
    # aperçu : les halos « Lueur » rendus translucides et lumineux, comme en jeu (Neon + Transparency)
    for o in objs:
        if o.name.startswith("Lueur"):
            o.data.materials[0] = glow_material()
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_render = "--no-render" not in sys.argv
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(RENDERS, exist_ok=True)
    lib.make_palette_png(PALETTE_PNG)
    mat = lib.palette_material(PALETTE_PNG)
    cam = sun = None
    if do_render:
        cam, sun = setup_render()
    report_path = os.path.join(OUT, "report.json")
    report = json.load(open(report_path)) if os.path.exists(report_path) else {}
    problems = []
    for mid, fn in registry.all_models():
        if args and not any(mid.startswith(a) for a in args):
            continue
        lib.reset_scene()
        model = fn()
        model.normalize()
        objs = model.build_objects(mat)
        rel = os.path.join(model.category, f"{mid}.fbx")
        lib.export_fbx(os.path.join(OUT, rel))
        if do_render:
            render(model, objs, cam, sun, os.path.join(RENDERS, f"{mid}.png"))
        dev = max(abs(s - 1) for s in model.scale_fix)
        report[mid] = {
            "titre": model.title, "categorie": model.category, "fichier": f"models/{rel}",
            "dims_studs": list(model.dims), "triangles": model.tris,
            "pieces": [o.name for o in objs], "en_jeu": model.count, "notes": model.notes,
            "ecart_avant_recalage": round(dev, 3),
        }
        flag = ""
        if model.tris > MAX_TRIS:
            flag += f"  !! {model.tris} triangles"
            problems.append(mid)
        if dev > 0.12:
            flag += f"  ~ recalage {dev:.0%} {tuple(round(s, 2) for s in model.scale_fix)}"
        print(f"{mid:32s} {model.tris:5d} tris  {', '.join(o.name for o in objs)}{flag}", flush=True)
    with open(report_path, "w") as f:
        json.dump(dict(sorted(report.items())), f, ensure_ascii=False, indent=1)
    if problems:
        print("TROP DE TRIANGLES :", problems)
        sys.exit(1)


if __name__ == "__main__":
    main()
