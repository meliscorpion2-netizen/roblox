"""Planche contact des rendus : python3 tools/sheet.py sortie.png id1 id2 ..."""
import sys, os
from PIL import Image, ImageDraw
out, ids = sys.argv[1], sys.argv[2:]
R = os.path.join(os.path.dirname(__file__), "..", "renders")
files = sorted(f for f in os.listdir(R) if f.endswith(".png") and (not ids or any(f.startswith(i) for i in ids)))
n = len(files); cols = min(6, n); rows = (n + cols - 1) // cols; S = 260
img = Image.new("RGB", (cols * S, rows * S), (236, 238, 242))
d = ImageDraw.Draw(img)
for k, f in enumerate(files):
    t = Image.open(os.path.join(R, f)).convert("RGBA").resize((S, S))
    x, y = (k % cols) * S, (k // cols) * S
    img.paste(t, (x, y), t)
    d.text((x + 6, y + 4), f[:-4], fill=(20, 20, 20))
img.save(out)
