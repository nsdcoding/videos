#!/usr/bin/env python3
"""Two 1280x720 thumbnails (A/B) for YouTube Test & compare, rendered from HTML with Playwright."""
import pathlib
import subprocess, json
MINS = round(json.loads((pathlib.Path(__file__).parent / "timings.json").read_text())["total"] / 60)

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
PINE = [30, 32, 35, 38, 40, 42, 45, 48, 230]
MAPLE = [50, 52, 55, 58, 60, 62, 65, 68, 70]
C = dict(bg="#1a1a19", blue="#3987e5", orange="#d95926", aqua="#199e70", violet="#9085e9", warn="#fab219",
         ink="#f0efec", ink2="#c3c2b7", muted="#898781", red="#d03b3b")


def dotplot_svg(vals, w, x0, y0, xmax=240, step=40, r=11, colors=None, mean=None, median=None, fs=22, marker_h=70,
                labels=True, mean_lab="mean", med_lab="median", lab_fs=30):
    sx = lambda v: x0 + v / xmax * w
    out = [f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="{C["ink2"]}" stroke-width="4"/>']
    for v in range(0, xmax + 1, step):
        out.append(f'<line x1="{sx(v)}" y1="{y0}" x2="{sx(v)}" y2="{y0 + 10}" stroke="{C["ink2"]}" stroke-width="3"/>')
        out.append(f'<text x="{sx(v)}" y="{y0 + 36}" fill="{C["ink2"]}" font-size="{fs}" text-anchor="middle">{v}</text>')
    placed = []
    for i, v in enumerate(vals):
        x = sx(v); lvl = 0
        while any(abs(x - px) < 2 * r + 2 and pl == lvl for px, pl in placed): lvl += 1
        placed.append((x, lvl))
        col = (colors or [C["blue"]] * len(vals))[i]
        out.append(f'<circle cx="{x}" cy="{y0 - r - 4 - lvl * (2 * r + 2)}" r="{r}" fill="{col}" stroke="{C["bg"]}" stroke-width="3"/>')
    if mean is not None:
        x = sx(mean); top = y0 - marker_h - 20
        out.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{top + 18}" stroke="{C["warn"]}" stroke-width="5" stroke-dasharray="9 7"/>')
        out.append(f'<polygon points="{x - 16},{top} {x + 16},{top} {x},{top + 24}" fill="{C["warn"]}"/>')
        if labels:
            out.append(f'<text x="{x + 22}" y="{top + 8}" fill="{C["warn"]}" font-size="{lab_fs}" font-weight="800">{mean_lab}</text>')
    if median is not None:
        x = sx(median); top = y0 - marker_h - 75
        out.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{top + 18}" stroke="{C["violet"]}" stroke-width="5" stroke-dasharray="9 7"/>')
        out.append(f'<rect x="{x - 13}" y="{top - 13}" width="26" height="26" fill="{C["violet"]}" transform="rotate(45 {x} {top})"/>')
        if labels:
            out.append(f'<text x="{x - 22}" y="{top + 10}" fill="{C["violet"]}" font-size="{lab_fs}" font-weight="800" text-anchor="end">{med_lab}</text>')
    return "\n".join(out)


BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1280px;height:720px;background:%(bg)s;overflow:hidden;font-family:'Inter','Inter Display',sans-serif;color:%(ink)s}
.h{font-family:'Inter Display','Inter';font-weight:900;letter-spacing:-2px;line-height:.92}
.badge{display:inline-block;border:3px solid %(aqua)s;color:%(aqua)s;border-radius:14px;padding:8px 18px;font-weight:800;font-size:30px}
svg text{font-family:'Inter'}
</style></head><body>%(body)s</body></html>"""


def thumb_a():
    svg = dotplot_svg(PINE, 590, 30, 470, colors=[C["blue"]] * 8 + [C["orange"]], mean=60, median=40, fs=26,
                      marker_h=150, labels=False, r=15)
    body = f"""
<div style="position:absolute;left:56px;top:40px" class="badge">Explained in {MINS} minutes</div>
<div class="h" style="position:absolute;left:52px;top:118px;font-size:128px;color:{C['warn']}">MEAN</div>
<div class="h" style="position:absolute;left:58px;top:236px;font-size:54px;color:{C['muted']}">vs</div>
<div class="h" style="position:absolute;left:52px;top:292px;font-size:128px;color:{C['violet']}">MEDIAN</div>
<div style="position:absolute;left:58px;top:450px;font-size:40px;font-weight:800;line-height:1.18;color:{C['ink']}">
  8 of 9 families earn<br><span style="color:{C['red']}">less than the “average”</span></div>
<svg style="position:absolute;left:610px;top:40px" width="660" height="560" viewBox="0 0 660 560">
  <rect x="30" y="10" width="560" height="120" rx="18" fill="#22221f" stroke="{C['ink2']}" stroke-width="2"/>
  <polygon points="60,40 92,40 76,64" fill="{C['warn']}"/>
  <text x="110" y="62" fill="{C['warn']}" font-size="40" font-weight="900">mean = $60k</text>
  <rect x="64" y="84" width="24" height="24" fill="{C['violet']}" transform="rotate(45 76 96)"/>
  <text x="110" y="110" fill="{C['violet']}" font-size="40" font-weight="900">median = $40k</text>
  {svg}
  <text x="30" y="545" fill="{C['muted']}" font-size="24">one town · household income (thousand $)</text>
</svg>"""
    return BASE % dict(C, body=body)


def thumb_b():
    m = dotplot_svg(MAPLE, 500, 30, 175, xmax=240, colors=[C["ink"]] * 9, mean=60, median=60, fs=22, marker_h=72, labels=False, r=12)
    p = dotplot_svg(PINE, 500, 30, 175, xmax=240, colors=[C["blue"]] * 8 + [C["orange"]], mean=60, median=40, fs=22,
                    marker_h=72, labels=False, r=12)
    panel = lambda title, col, svg, verdict, vcol: f"""
<div style="width:560px;height:330px;border:4px solid {col};border-radius:24px;background:#22221f;position:relative">
  <div style="position:absolute;left:26px;top:16px;font-size:36px;font-weight:900;color:{col}">{title}</div>
  <svg style="position:absolute;left:0;top:66px" width="560" height="220" viewBox="0 0 560 220">{svg}</svg>
  <div style="position:absolute;left:26px;bottom:16px;font-size:32px;font-weight:800;color:{vcol}">{verdict}</div>
</div>"""
    body = f"""
<div class="h" style="position:absolute;left:0;right:0;top:34px;text-align:center;font-size:132px">
  <span style="color:{C['warn']}">MEAN</span> <span style="color:{C['muted']};font-size:64px">vs</span> <span style="color:{C['violet']}">MEDIAN</span></div>
<div style="position:absolute;left:56px;top:210px;display:flex;gap:48px">
  {panel("BALANCED", C['ink2'], m, "mean = median = 60", C['aqua'])}
  {panel("SKEWED", C['orange'], p, "mean 60 ≠ median 40", C['red'])}
</div>
<div style="position:absolute;left:56px;top:600px" class="badge">Explained in {MINS} minutes</div>"""
    return BASE % dict(C, body=body)


if __name__ == "__main__":
    shots = []
    for name, html in (("thumbnail_A.png", thumb_a()), ("thumbnail_B.png", thumb_b())):
        h = HERE / "build" / name.replace(".png", ".html"); h.write_text(html); shots.append((str(h), str(OUT / name)))
    js = HERE / "build" / "shot.js"
    js.write_text("""const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1280,height:720}, deviceScaleFactor:1});
for (const [src, dst] of JSON.parse(process.argv[2])) { await p.goto('file://' + src); await p.waitForTimeout(400); await p.screenshot({path: dst}); }
await b.close(); })();""")
    import json
    subprocess.run(["node", str(js), json.dumps(shots)], check=True)
    from PIL import Image
    for n in ("A", "B"):
        im = Image.open(OUT / f"thumbnail_{n}.png"); print(n, im.size)
        im.resize((320, 180), Image.LANCZOS).save(HERE / "build" / f"thumb_{n}_phone.png")
