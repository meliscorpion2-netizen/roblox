"""Registre des modèles : chaque module expose MODELS = [(id, fonction), ...]."""
import importlib

MODULES = ["m_rue", "m_vehicules", "m_dechets", "m_marche", "m_chantier", "m_magasins", "m_magasins2", "m_quete", "m_slot", "m_pirate", "m_deauville", "m_cochons"]


def all_models():
    out = []
    for name in MODULES:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name == name:
                continue
            raise
        out.extend(mod.MODELS)
    return sorted(out, key=lambda t: t[0])
