#!/usr/bin/env python3
"""MiniCPM5-2B int8 on Core AI — decode rate by quantization granularity (SVG source).

Data: models/minicpm5-2b/bench-mac-llm-benchmark.json in the zoo (M4 Max, llm-benchmark
512p/1024g, 5 trials, greedy-free synthetic prompt) and the PipelinedBench device probes
(iPhone 17 Pro, 128-token prompt, 256 generated, Release, cold). 2026-09-08.
Render: python3 gen_minicpm5_granularity_chart.py > minicpm5-2b-int8-granularity.svg
"""
W, H = 1144, 560
BG, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, BLUE_LIGHT, GRAY = "#2a78d6", "#9ec5f4", "#c3c2b7"

panels = [
    ("Mac Studio M4 Max · macOS 27 beta", "llm-benchmark, 512-token prompt / 1024 generated, 5 trials",
     [("int8 per-channel", 25.6, BLUE_LIGHT), ("fp16 (no compression)", 80.0, GRAY), ("int8 per-block-32 (shipped)", 127.6, BLUE)], 140),
    ("iPhone 17 Pro · iOS 27 beta", "PipelinedBench, 128-token prompt / 256 generated, cold",
     [("int8 per-channel", 22.7, BLUE_LIGHT), ("fp16 (no compression)", None, GRAY), ("int8 per-block-32 (shipped)", 22.4, BLUE)], 140),
]

out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" style="font-family:-apple-system,\'Helvetica Neue\',Arial,sans-serif">',
       f'<rect width="{W}" height="{H}" fill="{BG}"/>',
       f'<text x="44" y="52" font-size="26" font-weight="700" fill="{INK}">MiniCPM5-2B on Apple Core AI: same int8 weights, one scale-granularity line apart</text>',
       f'<text x="44" y="84" font-size="15" fill="{INK2}">Decode tokens/s, greedy. coreai-opt quantization_config: per_channel vs per_block (block_size 32). fp16 is the uncompressed control.</text>']

panel_w = 500
for pi, (title, sub, rows, xmax) in enumerate(panels):
    x0 = 44 + pi * (panel_w + 56)
    y0 = 130
    out.append(f'<text x="{x0}" y="{y0}" font-size="17" font-weight="600" fill="{INK}">{title}</text>')
    out.append(f'<text x="{x0}" y="{y0 + 22}" font-size="13" fill="{MUTED}">{sub}</text>')
    label_w = 215
    bar_x0 = x0 + label_w
    bar_w_max = panel_w - label_w
    top = y0 + 52
    # gridlines
    for v in range(0, xmax + 1, 35 if xmax > 100 else 35):
        gx = bar_x0 + bar_w_max * v / xmax
        out.append(f'<line x1="{gx:.1f}" y1="{top - 8}" x2="{gx:.1f}" y2="{top + 3 * 62 + 4}" stroke="{GRID}" stroke-width="1"/>')
        out.append(f'<text x="{gx:.1f}" y="{top + 3 * 62 + 22}" font-size="12" fill="{MUTED}" text-anchor="middle">{v}</text>')
    out.append(f'<line x1="{bar_x0}" y1="{top - 8}" x2="{bar_x0}" y2="{top + 3 * 62 + 4}" stroke="{AXIS}" stroke-width="1"/>')
    for ri, (name, value, color) in enumerate(rows):
        y = top + ri * 62
        out.append(f'<text x="{bar_x0 - 12}" y="{y + 26}" font-size="14" fill="{INK2}" text-anchor="end">{name}</text>')
        if value is None:
            out.append(f'<text x="{bar_x0 + 12}" y="{y + 26}" font-size="13" fill="{MUTED}">not run — 5.0 GB does not fit the phone</text>')
            continue
        w = bar_w_max * value / xmax
        out.append(f'<rect x="{bar_x0}" y="{y + 8}" width="{w:.1f}" height="28" rx="4" fill="{color}"/>')
        out.append(f'<text x="{bar_x0 + w + 10:.1f}" y="{y + 27}" font-size="15" font-weight="600" fill="{INK}">{value:.1f}</text>')
    out.append(f'<text x="{bar_x0 + bar_w_max / 2:.1f}" y="{top + 3 * 62 + 44}" font-size="12" fill="{MUTED}" text-anchor="middle">tokens / s</text>')

foot_y = H - 60
out.append(f'<text x="44" y="{foot_y}" font-size="13" fill="{INK2}">Per-channel int8 lowers to a dequantize-then-matmul path on the Mac GPU; per-block-32 lands on the quantized-matmul path. On the phone decode is memory-bandwidth-bound either way.</text>')
out.append(f'<text x="44" y="{foot_y + 22}" font-size="13" fill="{INK2}">Numerics: both int8 bundles 16/16 token-exact vs the fp32 oracle (margin-aware gate); per-block-32 also matches fp32 on a 30-token free-run where per-channel flipped a 0.245-margin token.</text>')
out.append(f'<text x="44" y="{foot_y + 44}" font-size="12" fill="{MUTED}">github.com/john-rocky/coreai-model-zoo · models/minicpm5-2b · 2026-09-08</text>')
out.append('</svg>')
print("\n".join(out))
