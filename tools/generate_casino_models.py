"""Builds the 8 Casino Machine Tycoon models into ../models/*.glb and preview renders into ../previews/.

    python3 tools/generate_casino_models.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from casino_geo import export_glb, render, RY  # noqa: E402
import models_world as W  # noqa: E402
import models_machines as MM  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "models")
PREV = os.path.join(ROOT, "previews")

BUILDERS = [
    ("JackpotSpire", W.jackpot_spire, False),
    ("ConveyorSegment", W.conveyor_segment, False),
    ("CasinoTier1", W.casino_tier1, False),
    ("PlotSign", W.plot_sign, False),
    ("MachineSlot", W.machine_slot, False),
    ("LuckyFruitsMachine", MM.lucky_fruits, True),
    ("OceanTreasureMachine", MM.ocean_treasure, True),
    ("NeonFortuneMachine", MM.neon_fortune, True),
    ("GoldenPharaohMachine", MM.golden_pharaoh, True),
]
VIEWS = {
    "JackpotSpire": dict(eye=(-1, 0.42, -1.4), fit=0.78),
    "ConveyorSegment": dict(eye=(-0.55, 0.55, -1), fit=0.62),
    "CasinoTier1": dict(eye=(-0.85, 0.75, -1.25), fit=0.72),
    "PlotSign": dict(eye=(-0.55, 0.3, -1.3), fit=0.72),
    "MachineSlot": dict(eye=(-0.7, 0.75, -1.2), fit=0.95),
}


def build(only=None, previews=True):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREV, exist_ok=True)
    report = {}
    models = {}
    for name, fn, mirror in BUILDERS:
        if only and name not in only:
            continue
        m = fn()
        if mirror:
            m.mirror_x()
        assert m.name == name
        models[name] = m
        stats = export_glb(m, os.path.join(OUT, name + ".glb"))
        report[name] = {"parts": stats, "triangles": sum(stats.values())}
        if previews:
            v = VIEWS.get(name, dict(eye=(-0.8, 0.42, -1.3), fit=0.8))
            render([(m, None)], os.path.join(PREV, name + ".png"), size=(900, 900), **v)
        print(f"{name:22s} {report[name]['triangles']:6d} tris  {stats}")
    if previews and "JackpotSpire" in models and "ConveyorSegment" in models:
        ring = [(models["JackpotSpire"], None)] + [(models["ConveyorSegment"], RY(22.5 * k)) for k in range(16)]
        render(ring, os.path.join(PREV, "SpireWithConveyorRing.png"), size=(1200, 900), eye=(-1, 0.5, -1.35), fit=0.7)
    if previews and all(n in models for n in ("LuckyFruitsMachine", "OceanTreasureMachine", "NeonFortuneMachine", "GoldenPharaohMachine")):
        from casino_geo import T
        line = [(models[n], T(10.5 - 7 * i, 0, 0)) for i, n in enumerate(
            ("LuckyFruitsMachine", "OceanTreasureMachine", "NeonFortuneMachine", "GoldenPharaohMachine"))]
        render(line, os.path.join(PREV, "SlotMachineLineup.png"), size=(1600, 700), eye=(-0.25, 0.3, -1), fit=0.5)
    if previews and all(n in models for n in ("MachineSlot", "GoldenPharaohMachine")):
        from casino_geo import T
        render([(models["MachineSlot"], None), (models["GoldenPharaohMachine"], T(0, 1.1, 0))],
               os.path.join(PREV, "MachineSlotWithMachine.png"), size=(900, 900), eye=(-0.7, 0.55, -1.2), fit=0.9)
    with open(os.path.join(OUT, "triangle_counts.json"), "w") as f:
        json.dump(report, f, indent=2)
    return report


if __name__ == "__main__":
    build(sys.argv[1:] or None)
