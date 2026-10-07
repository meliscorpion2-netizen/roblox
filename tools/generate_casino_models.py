"""Builds every Casino Machine Tycoon model into ../models/*.glb and preview renders into ../previews/.

    python3 tools/generate_casino_models.py                 # everything
    python3 tools/generate_casino_models.py WildWestMachine  # only the named models (+ checks)
    python3 tools/generate_casino_models.py --no-previews ...

Models come from the modules listed in tools/registry.py (each module's BUILDERS list).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from casino_geo import export_glb, render, RY, T  # noqa: E402
import registry  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "models")
PREV = os.path.join(ROOT, "previews")
DEFAULT_VIEW = dict(eye=(-0.8, 0.42, -1.3), fit=0.8)
OLD_MACHINES = ("LuckyFruitsMachine", "OceanTreasureMachine", "NeonFortuneMachine", "GoldenPharaohMachine")


def build_model(entry):
    m = entry["fn"]()
    if entry["mirror"]:
        m.mirror_x()
    assert m.name == entry["name"], f"builder returned model {m.name!r}, expected {entry['name']!r}"
    got = [p.name for p in m.parts]
    assert sorted(got) == sorted(entry["parts"]), f"{m.name}: parts {got} != expected {entry['parts']}"
    for p in m.parts:
        assert p.geo.polys, f"{m.name}.{p.name} is empty"
    return m


def build(only=None, previews=True):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREV, exist_ok=True)
    entries = registry.collect()
    if only:
        missing = set(only) - {e["name"] for e in entries}
        assert not missing, f"unknown model(s): {missing}"
    counts_path = os.path.join(OUT, "triangle_counts.json")
    report = json.load(open(counts_path)) if os.path.exists(counts_path) else {}
    models = {}
    for e in entries:
        if only and e["name"] not in only:
            continue
        m = build_model(e)
        models[e["name"]] = m
        stats = export_glb(m, os.path.join(OUT, e["name"] + ".glb"))
        report[e["name"]] = {"parts": stats, "triangles": sum(stats.values())}
        if previews:
            render([(m, None)], os.path.join(PREV, e["name"] + ".png"), size=(900, 900), **(e["view"] or DEFAULT_VIEW))
        print(f"{e['name']:24s} {report[e['name']]['triangles']:6d} tris  {stats}")
    if previews and not only:
        ring = [(models["JackpotSpire"], None)] + [(models["ConveyorSegment"], RY(22.5 * k)) for k in range(16)]
        render(ring, os.path.join(PREV, "SpireWithConveyorRing.png"), size=(1200, 900), eye=(-1, 0.5, -1.35), fit=0.7)
        line = [(models[n], T(10.5 - 7 * i, 0, 0)) for i, n in enumerate(OLD_MACHINES)]
        render(line, os.path.join(PREV, "SlotMachineLineup.png"), size=(1600, 700), eye=(-0.25, 0.3, -1), fit=0.5)
        render([(models["MachineSlot"], None), (models["GoldenPharaohMachine"], T(0, 1.1, 0))],
               os.path.join(PREV, "MachineSlotWithMachine.png"), size=(900, 900), eye=(-0.7, 0.55, -1.2), fit=1.1)
    known = {e["name"] for e in entries}
    report = {k: v for k, v in report.items() if k in known}
    with open(counts_path, "w") as f:
        json.dump(report, f, indent=2)
    return models


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    build(args or None, previews="--no-previews" not in sys.argv)
