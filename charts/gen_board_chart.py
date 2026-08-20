#!/usr/bin/env python3
"""Regenerate devicemark-board.{svg,png} + devicemark-og.png from board.json.

Spec lives in README.md next to this file. Renders PNGs at 2x via Chrome
headless so text stays sharp on retina displays. Run from anywhere:
    python3 gen_board_chart.py [path/to/board.json]
"""
import json, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOARD = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home()/"code/devicemark/site/board.json"
ACCENT, NEUTRAL, SURFACE = "#2a78d6", "#898781", "#fcfcfa"
INK, MUTED, GRID = "#1a1a18", "#6f6d67", "#e8e6e1"
W, H, OGW = 1144, 648, 1238  # og = padded to 1.91:1
X0, UNIT = 337, 8.71        # bar origin, px per composite point

d = json.load(open(BOARD))
rows = d if isinstance(d, list) else d.get("rows") or list(d.values())[0]
rows = sorted([r for r in rows if r.get("native_runtime") != "cloud-api"],
              key=lambda r: -r["composite"]["value"])
assert len(rows) == 10, f"expected 10 on-device rows, got {len(rows)}"

def svg(pad):
    w = W + 2*pad
    e = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" '
         f'style="font-family:-apple-system,\'Helvetica Neue\',Arial,sans-serif">',
         f'<rect width="{w}" height="{H}" fill="{SURFACE}"/>',
         f'<text x="{44+pad}" y="52" font-size="26" font-weight="700" fill="{INK}">'
         "Apple’s built-in model, measured against open models on the same phone</text>",
         f'<text x="{44+pad}" y="86" font-size="15" fill="{MUTED}">596 questions '
         "(IFEval / MMLU-Pro / MATH-500), 0-shot, greedy, no answer scored wrong. "
         "Higher is better.</text>"]
    for t in (0, 20, 40, 60):
        gx = X0 + pad + t*UNIT
        e.append(f'<text x="{gx}" y="118" font-size="13" fill="{NEUTRAL}" text-anchor="middle">{t}</text>')
        e.append(f'<line x1="{gx}" y1="128" x2="{gx}" y2="578" stroke="{GRID}" stroke-width="1"/>')
    labels = []
    for i, r in enumerate(rows):
        v = r["composite"]["value"]*100
        val = f"{v:.1f}"
        labels.append(val)
        cy = 163 + i*43.8
        apple = r["mem_mb"] is None
        bw = v*UNIT
        e.append(f'<text x="{X0+pad-12}" y="{cy+5:.0f}" font-size="15" text-anchor="end" '
                 f'fill="{"#111" if apple else "#37352f"}"'
                 f'{" font-weight=\"700\"" if apple else ""}>{r["model"]}</text>')
        e.append(f'<rect x="{X0+pad}" y="{cy-12:.0f}" width="{bw:.1f}" height="24" rx="2" '
                 f'fill="{ACCENT if apple else NEUTRAL}"/>')
        size = ('<tspan dx="8" font-size="13" font-weight="600" fill="%s">built in · 0 MB</tspan>' % ACCENT
                if apple else
                '<tspan dx="8" font-size="13" font-weight="400" fill="#98968f">%.1f GB</tspan>' % (r["mem_mb"]/1000))
        e.append(f'<text x="{X0+pad+bw+10:.1f}" y="{cy+5:.0f}" font-size="15" font-weight="700" '
                 f'fill="{INK}">{val}{size}</text>')
    e.append(f'<text x="{44+pad}" y="622" font-size="13" fill="{NEUTRAL}">iPhone 17 Pro tier '
             "· quality measured on Mac, carried by greedy token-exact parity · "
             "raw outputs published</text>")
    e.append(f'<text x="{W-44+pad}" y="622" font-size="13" fill="{NEUTRAL}" '
             'text-anchor="end">devicemark.github.io</text>')
    e.append("</svg>")
    expected = ["68.2","62.1","61.4","55.8","52.9","52.5","52.3","41.9","31.7","26.1"]
    assert labels == expected, f"score labels drifted: {labels}"
    return "\n".join(e)

def render(svg_text, w, out):
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=HERE, delete=False) as f:
        f.write(f"<!doctype html><body style='margin:0'>{svg_text}</body>")
        tmp = Path(f.name)
    try:
        subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                        "--headless=new", "--disable-gpu", f"--screenshot={out}",
                        f"--window-size={w},{H}", "--force-device-scale-factor=2",
                        "--hide-scrollbars", f"file://{tmp}"],
                       check=True, capture_output=True)
    finally:
        tmp.unlink()
    print("wrote", out)

board_svg = svg(0)
(HERE/"devicemark-board.svg").write_text(board_svg)
print("wrote", HERE/"devicemark-board.svg")
render(board_svg, W, HERE/"devicemark-board.png")
render(svg((OGW-W)//2), OGW, HERE/"devicemark-og.png")
