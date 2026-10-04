"""Régénère le tableau des modèles du README à partir de models/report.json."""
import json, os
ROOT = os.path.join(os.path.dirname(__file__), "..")
rep = json.load(open(os.path.join(ROOT, "models", "report.json")))
fmt = lambda v: f"{v:g}".replace(".", ",")
rows = ["| # | Objet | Dimensions (X × Y × Z studs) | Triangles | Pièces | Fichier |", "|---|---|---|---|---|---|"]
for mid, r in rep.items():
    rows.append(f"| {mid.split('_')[0]} | {r['titre']} | {' × '.join(fmt(v) for v in r['dims_studs'])} | {r['triangles']} | "
                f"{', '.join(r['pieces'])} | [{os.path.basename(r['fichier'])}]({r['fichier']}) |")
src = open(os.path.join(ROOT, "README.md")).read()
a, b = src.index("<!-- table -->"), src.index("<!-- /table -->")
open(os.path.join(ROOT, "README.md"), "w").write(src[:a] + "<!-- table -->\n" + "\n".join(rows) + "\n" + src[b:])
