"""source-prepped.png -> ascii-portrait.svg (monochrome, prints row by row once).
If no photo is prepped yet, renders a placeholder "SA" monogram so the README still works.
"""
import os
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-prepped.png"
STATIC = os.environ.get("STATIC") == "1"

RAMP = " .`:-=+*cs#%@"          # bright (sparse) -> dark (dense)
COLS, CW, LH, FS = 84, 4.4, 8.4, 7.4
FILL, CURSOR, BG = "#c9d1d9", "#39d353", "#0d1117"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def placeholder():
    img = Image.new("L", (840, 520), 255)
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("DejaVuSans-Bold.ttf", 420)
    except OSError:
        f = ImageFont.load_default(size=420)
    d.text((420, 270), "SA", font=f, fill=40, anchor="mm")
    return img


img = Image.open(SRC).convert("L") if SRC.exists() else placeholder()
print("using", "photo" if SRC.exists() else "placeholder")
rows_n = max(1, round(img.height / img.width * COLS * CW / LH))
img = img.resize((COLS, rows_n), Image.LANCZOS)
px = img.load()

rows = []
for y in range(rows_n):
    line = "".join(RAMP[min(int((255 - px[x, y]) / 256 * len(RAMP)), len(RAMP) - 1)] for x in range(COLS))
    rows.append(line.rstrip())

PAD = 10
W, H = COLS * CW + PAD * 2, rows_n * LH + PAD * 2
parts = []
for i, line in enumerate(rows):
    if not line.strip():
        continue
    y = PAD + (i + 1) * LH - 1.5
    text = (f'<text x="{PAD}" y="{y:.1f}" font-size="{FS}" fill="{FILL}" xml:space="preserve" '
            f'textLength="{len(line) * CW:.1f}" lengthAdjust="spacing"')
    if STATIC:
        parts.append(text + f">{escape(line)}</text>")
        continue
    d, dur = 0.3 + i * 0.05, 0.45
    full = COLS * CW
    parts.append(
        f'<clipPath id="r{i}"><rect x="{PAD}" y="{PAD + i * LH:.1f}" width="0" height="{LH}">'
        f'<animate attributeName="width" from="0" to="{full:.1f}" begin="{d:.2f}s" dur="{dur}s" fill="freeze"/>'
        f'</rect></clipPath>'
        f'<g clip-path="url(#r{i})">{text}>{escape(line)}</text></g>'
        f'<rect x="{PAD}" y="{PAD + i * LH:.1f}" width="3" height="{LH - 1}" fill="{CURSOR}" opacity="0">'
        f'<set attributeName="opacity" to="1" begin="{d:.2f}s"/>'
        f'<animate attributeName="x" from="{PAD}" to="{PAD + full:.1f}" begin="{d:.2f}s" dur="{dur}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0" begin="{d + dur:.2f}s"/></rect>'
    )

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" '
       f'style="font-family:{FONT}"><rect width="{W:.0f}" height="{H:.0f}" rx="10" fill="{BG}" stroke="#30363d"/>'
       + "".join(parts) + "</svg>")
(ROOT / "ascii-portrait.svg").write_text(svg)
print(f"wrote ascii-portrait.svg ({COLS}x{rows_n})")
