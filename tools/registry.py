"""Collects the model definitions from every model module.

Each module defines BUILDERS = [dict(name=..., fn=..., parts=[...], mirror=False, view=dict(eye=..., fit=...)), ...]
  name   exact model / file name
  fn     builder returning a casino_geo.Model named `name`
  parts  exact mesh names the model must contain (nothing else)
  mirror True for front-facing art authored as seen from +Z (slot machines): mirrors X once at build
  view   optional preview camera (eye direction, fit)
"""
import importlib
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MODULES = [
    "models_world",          # JackpotSpire, ConveyorSegment, CasinoTier1, PlotSign, MachineSlot
    "models_machines",       # Lucky / Ocean / Neon / Pharaoh slot machines
    "models_machines_west",  # WildWestMachine, PirateFortuneMachine
    "models_machines_tech",  # CyberSpinMachine, CrystalKingdomMachine
    "models_machines_space",  # SpaceJackpotMachine, DragonTreasureMachine
    "models_machines_myth",  # VolcanoRichesMachine, GalaxyFortuneMachine
    "models_buildings",      # CasinoTier2, CasinoTier3, CasinoTier4
    "models_plaza",          # BoostStand, PlotArch, UpgradeKiosk, CashStack
    "models_decor",          # TreeRound, PalmTree, Bush, LampPost, Bench, PlazaFountain
    "models_boxes",          # CommonBox .. SecretBox
]


def collect(strict=False):
    entries = []
    for name in MODULES:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), name + ".py")):
            continue
        try:
            mod = importlib.import_module(name)
        except Exception:
            if strict:
                raise
            print(f"[registry] WARNING: could not import {name}:\n{traceback.format_exc()}", file=sys.stderr)
            continue
        for e in getattr(mod, "BUILDERS", []):
            e = dict(e)
            e.setdefault("mirror", False)
            e.setdefault("view", None)
            e["module"] = name
            entries.append(e)
    names = [e["name"] for e in entries]
    dup = {n for n in names if names.count(n) > 1}
    assert not dup, f"duplicate model names: {dup}"
    return entries
