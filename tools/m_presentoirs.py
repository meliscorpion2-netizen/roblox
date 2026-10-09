"""197–198 : présentoir et étiquette de prix du magasin."""
from lib import Model

CAT = "13_magasin"


def M(name, dims, title, note=""):
    m = Model(name, dims, CAT, title, None, note)
    m.grime = False
    return m


def presentoir():
    m = M("presentoir", (5, 3, 4), "Présentoir à un étage", "Plateau vide et plat sur le dessus")
    p, pl = m.part("Presentoir"), m.part("Plateau")
    p.boxb(4.2, 3.2, 0.35, 0, 0, 0, c="plastic_black", bev=0.08)  # socle
    p.boxb(3.6, 2.6, 2.3, 0, 0, 0.35, c="white", bev=0.12)
    p.boxb(3.65, 2.65, 0.15, 0, 0, 0.6, c="orange", bev=0.02)
    pl.boxb(5, 4, 0.3, 0, 0, 2.65, c="metal_light", bev=0.08)
    pl.boxb(4.6, 3.6, 0.06, 0, 0, 2.95, c="grey_light", bev=0)
    return m


def etiquette():
    m = M("etiquette_prix", (2, 1.2, 0.2), "Étiquette de prix", "Zone vierge pour le nom et le prix")
    p = m.part("Etiquette")
    p.boxb(0.6, 0.2, 0.06, 0, 0, 0, c="metal_dark", bev=0.02)
    p.boxb(0.08, 0.06, 0.4, 0, 0.0, 0.06, c="metal_dark", bev=0)
    p.boxb(2.0, 0.08, 0.75, 0, 0, 0.45, c="flower_yellow", bev=0.04)
    p.boxb(1.8, 0.03, 0.58, 0, -0.05, 0.53, c="white", bev=0)
    return m


MODELS = [("197_presentoir", presentoir), ("198_etiquette_prix", etiquette)]
