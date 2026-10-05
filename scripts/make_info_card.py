"""Neofetch-style info card -> info-card.svg (STATIC=1 for a frozen preview)."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"
W = 490
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

# (key, value) - edit freely
ROWS = [
    ("Role",       "AI Engineer · GenAI & LLM Systems"),
    ("Now",        "AI-assisted backend systems @ Speedse Logistics"),
    ("Exploring",  "RAG pipelines · Agentic AI · advanced ML"),
    ("Stack",      "Python · FastAPI · Django/DRF · Docker · Redis"),
    ("Voice AI",   "Deepgram · ElevenLabs · Whisper"),
    ("Impact",     "30% automation efficiency · 25% lower latency"),
    ("Education",  "B.Tech CSE @ KIET (CGPA 8.2)"),
    ("Solved",     "300+ LeetCode · 100+ CodeChef"),
    ("Reach",      "shivamarora382004@gmail.com"),
]
TOP, LINE = 96, 24
H = TOP + len(ROWS) * LINE + 28


def a(i, base=""):
    cls = (base + " " + ("" if STATIC else "l")).strip()
    sty = "" if STATIC else f' style="animation-delay:{0.3 + i * 0.22:.2f}s"'
    return f' class="{cls}"{sty}'


body = [f'<text x="20" y="52" {a(0, "t")}><tspan class="g">$</tspan> neofetch</text>',
        f'<text x="20" y="76" {a(1, "h")}>shivam<tspan class="t">@</tspan>github</text>',
        f'<text x="20" y="84" {a(1, "t")}>{"─" * 40}</text>']
for i, (k, v) in enumerate(ROWS):
    body.append(f'<text x="20" y="{TOP + i * LINE}" {a(i + 2, "v")}>'
                f'<tspan class="k">{escape(k)}</tspan><tspan class="t">:</tspan> '
                f'<tspan x="112">{escape(v)}</tspan></text>')

css = "" if STATIC else (".l{opacity:0;animation:in .4s ease-out forwards}"
                         "@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}")
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
text{{font-family:{FONT};font-size:12.5px}}
.t{{fill:#8b949e}} .h{{fill:#39d353;font-weight:bold;font-size:15px}} .g{{fill:#39d353}}
.k{{fill:#58a6ff;font-weight:bold}} .v{{fill:#c9d1d9}}
{css}
</style>
<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>
<path d="M0 10a10 10 0 0 1 10-10h{W-20}a10 10 0 0 1 10 10v22H0z" fill="#161b22"/>
<circle cx="20" cy="16" r="5" fill="#ff5f56"/><circle cx="38" cy="16" r="5" fill="#ffbd2e"/><circle cx="56" cy="16" r="5" fill="#27c93f"/>
<text x="{W/2}" y="20" class="t" text-anchor="middle" style="font-size:12px">shivam@github: ~</text>
{"".join(body)}
</svg>'''
(ROOT / "info-card.svg").write_text(svg)
print("wrote info-card.svg")
