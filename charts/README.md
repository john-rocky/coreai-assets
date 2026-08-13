# charts

Images referenced by repos that do not take rasters themselves. Hotlink them:

```
https://raw.githubusercontent.com/john-rocky/coreai-assets/main/charts/<file>
```

raw.githubusercontent serves these with `content-type: image/png`, so they work as
`og:image` / `twitter:image` targets. There is no Pages site on this repo.

## devicemark-board.png / devicemark-og.png

The DeviceMark leaderboard as a bar chart. `devicemark-board.png` (1144×648) is the
chart at its content bounds — attach this one to a post. `devicemark-og.png` (1238×648)
is the same image padded left/right to 1.91:1 so the X link-card crop cannot clip the
title; `devicemark.github.io` points its `og:image` and `twitter:image` here.

**The SVG source was lost** (left in a session scratchpad, which is cleared between
sessions). Rebuild from this spec rather than hunting for it:

- **Data**: `devicemark/site/board.json`, the 10 rows with `native_runtime != "cloud-api"`,
  sorted by `composite.value` descending. The 2 cloud rows are deliberately excluded —
  they are a sea level, not competitors, and including them would change Apple's visible
  rank from 4th to 6th and contradict the post text.
- **Emphasis form**: one bar highlighted, the rest gray — the story is a single row's
  position, not ten independent categories.
- **Palette** (validated, do not eyeball a substitute): accent `#2a78d6`, neutral
  `#898781`, surface `#fcfcfa`. CVD ΔE 15.9, normal-vision ΔE 17.8, contrast passes.
- **Labels**: composite score in bold at each bar end, then the model's `mem_mb` as
  "N.N GB" in muted gray beside it. Apple's row gets "built in · 0 MB" in the accent
  color instead — the size column is the whole point of the comparison.
- **Chrome**: solid hairline gridlines only (dashed rules read as thresholds), no
  legend (single series), title + one-line method subtitle, footer with the tier and
  the site domain. Top margin ≥196px or the x-axis ticks collide with the subtitle.
- **Rendering**: `qlmanage` crops 16:9 to square, and Chrome refuses `file://`. Serve
  the directory over `python3 -m http.server` on localhost and screenshot the tab, then
  crop to content bounds with PIL.

Regenerate whenever `board.json` changes; the numbers are printed on the bars, so a
stale chart is a wrong chart.
