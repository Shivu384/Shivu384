"""data/contributions.json -> contrib-heatmap.svg (animated once, then frozen)"""
import json, os
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "contributions.json").read_text())
STATIC = os.environ.get("STATIC") == "1"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP = 12, 3
PITCH = CELL + GAP
W = 860
X0, Y0 = 40, 78
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

days = [(dt.date.fromisoformat(d["date"]), d["count"], d["level"]) for d in DATA["days"]]
first = days[0][0]
first_sunday = first - dt.timedelta(days=(first.weekday() + 1) % 7)
MAXC = max(c for _, c, _ in days)


def pick(count, lvl):
    # promote the very top days to the neon level 5
    return 5 if lvl == 4 and count > 0 and count >= MAXC * 0.75 else lvl


cells, month_labels, last_m = [], [], None
for date, count, lvl in days:
    col = (date - first_sunday).days // 7
    row = (date.weekday() + 1) % 7
    x, y = X0 + col * PITCH, Y0 + row * PITCH
    delay = 0.15 + (col + row) * 0.018
    anim = "" if STATIC else f' style="animation-delay:{delay:.2f}s"'
    cells.append(
        f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
        f'fill="{PALETTE[pick(count, lvl)]}"{anim}><title>{count} on {date}</title></rect>'
    )
    if row == 0 and date.month != last_m:
        if last_m is not None or date.day <= 7:
            month_labels.append(f'<text x="{x}" y="{Y0 - 8}" class="m">{MONTHS[date.month - 1]}</text>')
        last_m = date.month

day_labels = "".join(
    f'<text x="{X0 - 8}" y="{Y0 + i * PITCH + 10}" class="m" text-anchor="end">{n}</text>'
    for i, n in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
)

s = DATA["stats"]
H = Y0 + 7 * PITCH + 62
footer_y = Y0 + 7 * PITCH + 24
legend_y = footer_y + 22
legend = "".join(
    f'<rect x="{W - 20 - 6 * PITCH - 36 + i * PITCH}" y="{legend_y - 10}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>'
    for i, c in enumerate(PALETTE)
)
anim_css = "" if STATIC else (
    ".c{opacity:0;animation:pop .45s ease-out forwards}"
    "@keyframes pop{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}"
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
text{{font-family:{FONT}}}
.m{{font-size:10px;fill:#8b949e}}
.t{{font-size:12px;fill:#8b949e}}
.k{{fill:#39d353}}
{anim_css}
</style>
<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>
<path d="M0 10a10 10 0 0 1 10-10h{W-20}a10 10 0 0 1 10 10v22H0z" fill="#161b22"/>
<circle cx="20" cy="16" r="5" fill="#ff5f56"/><circle cx="38" cy="16" r="5" fill="#ffbd2e"/><circle cx="56" cy="16" r="5" fill="#27c93f"/>
<text x="{W/2}" y="20" class="t" text-anchor="middle">shivam@github: ~/contributions</text>
<text x="20" y="52" class="t"><tspan class="k">$</tspan> ./contributions.sh --last-year</text>
{"".join(month_labels)}{day_labels}
{"".join(cells)}
<text x="20" y="{footer_y}" class="t">{s["total"]:,} contributions in the last year · streak {s["current_streak"]}d · longest {s["longest_streak"]}d · best {s["best_day"]["count"]} on {s["best_day"]["date"]}</text>
<text x="{W - 20 - 6 * PITCH - 36 - 6}" y="{legend_y}" class="m" text-anchor="end">Less</text>{legend}<text x="{W - 20 - 30}" y="{legend_y}" class="m">More</text>
</svg>'''
(ROOT / "contrib-heatmap.svg").write_text(svg)
print("wrote contrib-heatmap.svg")
