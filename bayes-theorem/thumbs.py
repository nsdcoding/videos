#!/usr/bin/env python3
"""Two 1280x720 thumbnails (A/B) for YouTube Test & compare, rendered from HTML with Playwright.
Both use the running example: 1,000 people → 9 real positives vs 99 false alarms → 9/108 ≈ 8%."""
import json, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
MINS = round(json.loads((HERE / "timings.json").read_text())["total"] / 60)
C = dict(bg="#1a1a19", blue="#3987e5", orange="#d95926", aqua="#199e70", violet="#9085e9", warn="#fab219",
         ink="#f0efec", ink2="#c3c2b7", muted="#898781", red="#d03b3b", card="#22221f")


def stacks_svg(x0, y0, h, cell, per_row=5, label_fs=34, tick_fs=22, ymax=120, step=20, xs=(90, 240), axis_w=330,
               names=("have it", "false alarms"), name_fs=26):
    """Countable stacks on a numbered y axis: 9 orange (have it) vs 99 blue (false alarms)."""
    unit = h / ymax                       # px per person
    pitch = per_row * unit                # one row of squares = per_row people
    out = [f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 - h - 6}" stroke="{C["ink2"]}" stroke-width="4"/>',
           f'<line x1="{x0}" y1="{y0}" x2="{x0 + axis_w}" y2="{y0}" stroke="{C["ink2"]}" stroke-width="4"/>']
    for v in range(0, ymax + 1, step):
        y = y0 - v * unit
        out.append(f'<line x1="{x0 - 10}" y1="{y}" x2="{x0}" y2="{y}" stroke="{C["ink2"]}" stroke-width="3"/>')
        out.append(f'<text x="{x0 - 16}" y="{y + 8}" fill="{C["ink2"]}" font-size="{tick_fs}" text-anchor="end">{v}</text>')
    for n, cx, col, lab, name in ((9, x0 + xs[0], C["orange"], "9", names[0]), (99, x0 + xs[1], C["blue"], "99", names[1])):
        left = cx - per_row * pitch / 2
        for k in range(n):
            c, r = k % per_row, k // per_row
            out.append(f'<rect x="{left + c * pitch + 1.5}" y="{y0 - (r + 1) * pitch + 1.5}" width="{pitch - 3}" height="{pitch - 3}" fill="{col}"/>')
        top = y0 - math_ceil(n / per_row) * pitch
        out.append(f'<text x="{cx}" y="{top - 12}" fill="{col}" font-size="{label_fs}" font-weight="900" text-anchor="middle">{lab}</text>')
        out.append(f'<text x="{cx}" y="{y0 + 36}" fill="{col}" font-size="{name_fs}" font-weight="700" text-anchor="middle">{name}</text>')
    return "\n".join(out)


def math_ceil(x):
    return int(-(-x // 1))


BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1280px;height:720px;background:%(bg)s;overflow:hidden;font-family:'Inter','Inter Display',sans-serif;color:%(ink)s}
.h{font-family:'Inter Display','Inter';font-weight:900;letter-spacing:-2px;line-height:.92}
.badge{display:inline-block;border:3px solid %(aqua)s;color:%(aqua)s;border-radius:14px;padding:8px 18px;font-weight:800;font-size:30px}
svg text{font-family:'Inter'}
</style></head><body>%(body)s</body></html>"""


def thumb_a():
    svg = stacks_svg(70, 470, 400, None)
    body = f"""
<div style="position:absolute;left:56px;top:40px" class="badge">Explained in {MINS} minutes</div>
<div class="h" style="position:absolute;left:52px;top:118px;font-size:120px;color:{C['violet']}">BAYES'<br>THEOREM</div>
<div style="position:absolute;left:58px;top:360px;font-size:44px;font-weight:800;line-height:1.2">
  test says <span style="color:{C['aqua']}">positive</span>:</div>
<div style="position:absolute;left:58px;top:420px;display:flex;align-items:baseline;gap:26px">
  <div class="h" style="font-size:104px;color:{C['muted']};text-decoration:line-through;text-decoration-color:{C['red']};text-decoration-thickness:10px">90%</div>
  <div class="h" style="font-size:52px;color:{C['muted']}">vs</div>
  <div class="h" style="font-size:118px;color:{C['violet']}">8%</div>
</div>
<div style="position:absolute;left:60px;top:560px;font-size:30px;color:{C['ink2']}">gut feeling vs real chance</div>
<svg style="position:absolute;left:760px;top:40px" width="480" height="560" viewBox="0 0 480 560">
  <text x="20" y="34" fill="{C['ink']}" font-size="30" font-weight="800">108 positives out of 1,000</text>
  {svg.replace('x1="70"', 'x1="70"')}
</svg>"""
    return BASE % dict(C, body=body)


def thumb_b():
    svg = stacks_svg(50, 280, 220, None, label_fs=28, tick_fs=18, xs=(55, 130), axis_w=170, names=("real", "false"), name_fs=22)
    body = f"""
<div class="h" style="position:absolute;left:0;right:0;top:34px;text-align:center;font-size:128px;color:{C['violet']}">BAYES' THEOREM</div>
<div style="position:absolute;left:56px;top:200px;width:560px;height:360px;border:4px solid {C['muted']};border-radius:24px;background:{C['card']}">
  <div style="position:absolute;left:30px;top:22px;font-size:36px;font-weight:900;color:{C['muted']}">YOUR GUT</div>
  <div class="h" style="position:absolute;left:30px;top:100px;font-size:170px;color:{C['muted']}">90%</div>
  <div style="position:absolute;left:24px;top:182px;width:440px;height:12px;background:{C['red']};transform:rotate(-8deg)"></div>
  <div style="position:absolute;left:30px;bottom:24px;font-size:32px;font-weight:700;color:{C['ink2']}">"the test is 90% accurate"</div>
</div>
<div style="position:absolute;left:660px;top:200px;width:560px;height:360px;border:4px solid {C['violet']};border-radius:24px;background:{C['card']}">
  <div style="position:absolute;left:30px;top:22px;font-size:36px;font-weight:900;color:{C['violet']}">REAL CHANCE</div>
  <div class="h" style="position:absolute;left:30px;top:100px;font-size:170px;color:{C['violet']}">8%</div>
  <svg style="position:absolute;left:330px;top:24px" width="220" height="330" viewBox="0 0 220 330">{svg}</svg>
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
    subprocess.run(["node", str(js), json.dumps(shots)], check=True)
    from PIL import Image
    for n in ("A", "B"):
        im = Image.open(OUT / f"thumbnail_{n}.png"); print(n, im.size)
        im.resize((320, 180), Image.LANCZOS).save(HERE / "build" / f"thumb_{n}_phone.png")
