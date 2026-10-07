"""Re-reads every exported .glb and checks part names, pivots and overall dimensions."""
import json, os, struct, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECT = {
    "JackpotSpire": ["Spire", "Skirt", "Crown", "NeonRings", "Base"],
    "ConveyorSegment": ["Belt", "Frame", "RailInner", "RailOuter", "Rollers"],
    "CasinoTier1": ["Floor", "Walls", "SignBoard", "NeonStrip", "Door"],
    "PlotSign": ["Display", "Accent", "Posts", "Decorations"],
    "MachineSlot": ["PedestalBase", "Pedestal", "Pad"],
    "LuckyFruitsMachine": ["Cabinet", "Screen", "Lever", "Topper", "Base"],
    "OceanTreasureMachine": ["Cabinet", "Screen", "Lever", "Topper", "Base"],
    "NeonFortuneMachine": ["Cabinet", "Screen", "Lever", "Topper", "Base", "NeonStrips"],
    "GoldenPharaohMachine": ["Cabinet", "Screen", "Lever", "Topper", "Base", "Wings"],
}


def load(path):
    data = open(path, "rb").read()
    magic, ver, total = struct.unpack_from("<III", data, 0)
    assert magic == 0x46546C67 and ver == 2 and total == len(data)
    jl, jt = struct.unpack_from("<II", data, 12)
    js = json.loads(data[20:20 + jl])
    bl, bt = struct.unpack_from("<II", data, 20 + jl)
    binary = data[28 + jl:28 + jl + bl]
    return js, binary


def positions(js, binary, mesh_idx):
    acc = js["accessors"][js["meshes"][mesh_idx]["primitives"][0]["attributes"]["POSITION"]]
    bv = js["bufferViews"][acc["bufferView"]]
    return np.frombuffer(binary, np.float32, acc["count"] * 3, bv["byteOffset"]).reshape(-1, 3)


ok = True
for name, parts in EXPECT.items():
    js, binary = load(os.path.join(ROOT, "models", name + ".glb"))
    root = js["nodes"][js["scenes"][0]["nodes"][0]]
    names = [js["nodes"][c]["name"] for c in root["children"]]
    missing = [p for p in parts if p not in names]
    allpts, info = [], {}
    for c in root["children"]:
        n = js["nodes"][c]
        p = positions(js, binary, n["mesh"]) + np.array(n["translation"])
        allpts.append(p)
        info[n["name"]] = (np.round(n["translation"], 2).tolist(), np.round(p.min(0), 2).tolist(), np.round(p.max(0), 2).tolist())
    P = np.concatenate(allpts)
    lo, hi = P.min(0), P.max(0)
    print(f"{name}: root='{root['name']}' parts={names}")
    print(f"   size X {hi[0]-lo[0]:.2f}  Y {hi[1]-lo[1]:.2f}  Z {hi[2]-lo[2]:.2f}   min {np.round(lo,2)}  max {np.round(hi,2)}")
    for k in ("Lever", "Topper", "Wings", "Belt", "Skirt", "Spire", "Display", "PedestalBase", "Pedestal", "Pad"):
        if k in info:
            print(f"   {k:8s} pivot {info[k][0]}  min {info[k][1]}  max {info[k][2]}")
    if missing or root["name"] != name:
        ok = False
        print("   !! missing", missing)
    if name == "ConveyorSegment":
        belt = js["nodes"][[c for c in root["children"] if js["nodes"][c]["name"] == "Belt"][0]]
        bp = positions(js, binary, belt["mesh"])
        top = bp[bp[:, 1] > 2.2]
        r = np.hypot(top[:, 0], top[:, 2])
        ang = np.degrees(np.arctan2(top[:, 0], -top[:, 2]))
        print(f"   belt top y in [{top[:,1].min():.4f},{top[:,1].max():.4f}]  r [{r.min():.2f},{r.max():.2f}]  angle [{ang.min():.3f},{ang.max():.3f}]")
print("OK" if ok else "FAILED")
