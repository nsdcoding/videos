#!/usr/bin/env python3
"""Two 1280x720 thumbnails (A/B) for YouTube Test & compare, rendered from HTML with Playwright.
TEMPLATE: FILL HEADLINE, FORMULA_TEX, FORMULA_LABELS, TILES, HOOK_HTML and diagram_svg() (thumbnail B).
Generated stickers (scripts/sticker.py) may be placed with <img src="file://..."> when they add a human element.

Both lead with the keyword headline "BAYES' THEOREM / EXPLAINED VISUALLY" and the colour-coded formula
(typeset with LaTeX -> SVG), plus a relatable picture from the running example:
  A: where you'll use it: Machine Learning, Data Science, Finance and CS tiles with hand-drawn SVG icons,
     plus the hook "a positive test: 90% → 8%".
  B: the 1,000-person grid from the video (9 real positives, 99 false alarms lit up) -> 9 vs 99 -> 8%.
"""
import json, pathlib, re, subprocess
import numpy as np

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
MINS = round(json.loads((HERE / "timings.json").read_text())["total"] / 60)
C = dict(bg="#1a1a19", blue="#3987e5", orange="#d95926", aqua="#199e70", violet="#9085e9", warn="#fab219",
         ink="#f0efec", ink2="#c3c2b7", muted="#898781", red="#d03b3b", card="#22221f")

# ── FILL per video ────────────────────────────────────────────────────
HEADLINE = ("BAYES'<br>THEOREM", "EXPLAINED VISUALLY")       # keyword headline (big, 2 lines) + subline
HEADLINE_ONE_LINE = "BAYES' THEOREM"                           # thumbnail B
FORMULA_TEX = r"{\color{vio}P(A\mid B)} = \frac{{\color{aq}P(B\mid A)}\,{\color{wa}P(A)}}{P(B)}"  # colours: vio aq wa ink
FORMULA_LABELS = [("the real chance", "violet", 34), ("test hit rate", "aqua", 250), ("base rate", "warn", 420)]  # (text, colour, x)
TILES = [("MACHINE LEARNING", "precision vs recall", "violet", "ICON_ML"),
         ("DATA SCIENCE", "update beliefs with data", "aqua", "ICON_DS"),
         ("FINANCE", "fraud alerts &amp; signals", "warn", "ICON_FIN"),
         ("COMPUTER SCIENCE", "naive Bayes spam filters", "blue", "ICON_CS")]
HOOK_HTML = ("a <span style='color:#199e70'>positive</span> test: <span style='color:#898781;text-decoration:line-through;"
             "text-decoration-color:#d03b3b;text-decoration-thickness:4px'>90%</span> → <span style='color:#9085e9'>8%</span>")

# EXAMPLE diagram for thumbnail B (Bayes): the same crowd as the video (common.py): 40 x 25, sick = column 0 top ten rows, 99 scattered false alarms
COLS, ROWS = 40, 25
SICK = [(0, ROWS - 1 - k) for k in range(10)]
_sick = set(SICK)
HEALTHY = [(c, r) for r in range(ROWS - 1, -1, -1) for c in range(COLS) if (c, r) not in _sick]
FALSE_POS = [HEALTHY[k] for k in sorted(np.random.default_rng(7).choice(990, 99, replace=False))]


def formula_svg(width):
    """Typeset the formula with LaTeX (colours: posterior violet, likelihood aqua, prior yellow)."""
    d = HERE / "build" / "tex"; d.mkdir(parents=True, exist_ok=True)
    (d / "f.tex").write_text(r"""\documentclass[preview,border=2pt]{standalone}
\usepackage{xcolor,amsmath}
\definecolor{vio}{HTML}{9085E9}\definecolor{aq}{HTML}{199E70}\definecolor{wa}{HTML}{FAB219}\definecolor{ink}{HTML}{F0EFEC}
\begin{document}
\color{ink}$\displaystyle """ + FORMULA_TEX + r"""$
\end{document}
""")
    subprocess.run(["latex", "-interaction=nonstopmode", "f.tex"], cwd=d, check=True, capture_output=True)
    subprocess.run(["dvisvgm", "--no-fonts", "--exact", "f.dvi", "-o", "formula.svg"], cwd=d, check=True, capture_output=True)
    svg = (d / "formula.svg").read_text()
    svg = svg[svg.index("<svg"):]
    vb = [float(x) for x in re.search(r"viewBox='([^']+)'", svg).group(1).split()]
    h = width * vb[3] / vb[2]
    svg = re.sub(r"width='[^']+' height='[^']+'", f"width='{width:.0f}' height='{h:.0f}'", svg, count=1)
    return svg, h


def crowd_svg(cell):
    """The 1,000-person grid: 9 real positives (orange, ringed), 99 false alarms (blue, ringed), rest dimmed."""
    tp, fp = set(SICK[:9]), set(FALSE_POS)
    out = []
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * cell, (ROWS - 1 - r) * cell
            k = (c, r)
            if k in tp:
                col, op = C["orange"], 1
            elif k in fp:
                col, op = C["blue"], 1
            elif k in _sick:
                col, op = C["orange"], 0.35
            else:
                col, op = "#4a4a46", 1
            out.append(f'<rect x="{x + 1}" y="{y + 1}" width="{cell - 2}" height="{cell - 2}" fill="{col}" opacity="{op}"/>')
            if k in tp or k in fp:
                out.append(f'<rect x="{x - 0.5}" y="{y - 0.5}" width="{cell + 1}" height="{cell + 1}" fill="none" stroke="{C["aqua"]}" stroke-width="2"/>')
    return "\n".join(out), COLS * cell, ROWS * cell


def tile(title, outcome, col, icon):
    return f"""<div style="width:250px;height:200px;background:{C['card']};border:3px solid {col};border-radius:20px;position:relative;box-sizing:border-box">
  <svg style="position:absolute;left:0;right:0;margin:auto;top:16px" width="110" height="80" viewBox="0 0 110 80">{icon(col)}</svg>
  <div style="position:absolute;left:0;right:0;top:110px;text-align:center;font-size:21px;font-weight:900;white-space:nowrap;letter-spacing:0;color:{col}">{title}</div>
  <div style="position:absolute;left:0;right:0;top:148px;text-align:center;font-size:18px;font-weight:600;white-space:nowrap;color:{C['ink2']}">{outcome}</div>
</div>"""


def ICON_ML(col):   # small neural network: 3 -> 4 -> 2 nodes
    L = [[(15, y) for y in (16, 40, 64)], [(55, y) for y in (10, 30, 50, 70)], [(95, y) for y in (28, 52)]]
    lines = "".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{C["muted"]}" stroke-width="1.5"/>'
                    for l1, l2 in zip(L, L[1:]) for a in l1 for b in l2)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{col}"/>' for l in L for x, y in l)
    return lines + dots


def ICON_DS(col):   # prior (wide) narrowing into posterior (tall)
    import math
    def path(mu, sd, peak):
        pts = [(x, 72 - peak * math.exp(-0.5 * ((x - mu) / sd) ** 2)) for x in range(4, 107, 3)]
        return "M" + " L".join(f"{x:.0f},{y:.1f}" for x, y in pts)
    return (f'<line x1="4" y1="72" x2="106" y2="72" stroke="{C["ink2"]}" stroke-width="3"/>'
            f'<path d="{path(62, 22, 26)}" fill="none" stroke="{C["warn"]}" stroke-width="4"/>'
            f'<path d="{path(48, 9, 60)}" fill="none" stroke="{C["violet"]}" stroke-width="4"/>')


def ICON_FIN(col):  # credit card with an alert badge
    return (f'<rect x="6" y="14" width="76" height="50" rx="8" fill="none" stroke="{col}" stroke-width="4"/>'
            f'<rect x="6" y="26" width="76" height="10" fill="{col}" opacity="0.7"/>'
            f'<circle cx="86" cy="58" r="17" fill="{C["red"]}"/>'
            f'<rect x="83.5" y="47" width="5" height="13" rx="2" fill="{C["ink"]}"/><circle cx="86" cy="66" r="3" fill="{C["ink"]}"/>')


def ICON_CS(col):   # envelope with a red flag
    return (f'<rect x="8" y="18" width="70" height="48" rx="5" fill="none" stroke="{col}" stroke-width="4"/>'
            f'<polyline points="8,20 43,46 78,20" fill="none" stroke="{col}" stroke-width="4"/>'
            f'<line x1="92" y1="10" x2="92" y2="70" stroke="{C["ink2"]}" stroke-width="4"/>'
            f'<polygon points="92,10 108,17 92,26" fill="{C["red"]}"/>')


BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1280px;height:720px;background:%(bg)s;overflow:hidden;font-family:'Inter','Inter Display',sans-serif;color:%(ink)s}
.h{font-family:'Inter Display','Inter';font-weight:900;letter-spacing:-2px;line-height:.9}
.badge{display:inline-block;border:3px solid %(aqua)s;color:%(aqua)s;border-radius:14px;padding:8px 18px;font-weight:800;font-size:30px}
.card{background:%(card)s;border:3px solid #3a3a37;border-radius:22px}
.lab{font-size:22px;font-weight:700}
svg text{font-family:'Inter'}
</style></head><body>%(body)s</body></html>"""


def thumb_a():
    f, fh = formula_svg(470)
    body = f"""
<div class="h" style="position:absolute;left:50px;top:34px;font-size:124px;color:{C['violet']}">{HEADLINE[0]}</div>
<div class="h" style="position:absolute;left:54px;top:268px;font-size:58px;letter-spacing:-1px;color:{C['warn']}">{HEADLINE[1]}</div>
<div class="card" style="position:absolute;left:50px;top:362px;width:600px;height:{fh + 92:.0f}px">
  <div style="position:absolute;left:62px;top:22px">{f}</div>
  {"".join(f'<div class="lab" style="position:absolute;left:{x}px;bottom:16px;color:{C[col]}">{txt}</div>' for txt, col, x in FORMULA_LABELS)}
</div>
<div style="position:absolute;left:54px;top:{362 + fh + 92 + 26:.0f}px" class="badge">Explained in {MINS} minutes</div>
<div style="position:absolute;left:720px;top:40px;font-size:30px;font-weight:900;letter-spacing:1px;color:{C['ink2']}">WHERE YOU'LL USE IT</div>
<div style="position:absolute;left:720px;top:96px;display:grid;grid-template-columns:250px 250px;gap:18px">
  {"".join(tile(a, b, C[col], globals()[ic]) for a, b, col, ic in TILES)}
</div>
<div style="position:absolute;left:720px;top:532px;font-size:30px;font-weight:800;color:{C['ink']}">
  {HOOK_HTML}</div>"""
    return BASE % dict(C, body=body)


def thumb_b():   # FILL: replace crowd_svg and the right-hand panel with this video's running-example diagram
    f, fh = formula_svg(400)
    grid, gw, gh = crowd_svg(13)
    body = f"""
<div class="h" style="position:absolute;left:50px;top:30px;font-size:112px;color:{C['violet']}">{HEADLINE_ONE_LINE}</div>
<div class="h" style="position:absolute;left:54px;top:146px;font-size:56px;letter-spacing:-1px;color:{C['warn']}">{HEADLINE[1]}</div>
<div class="card" style="position:absolute;left:836px;top:156px;width:396px;height:{fh + 40:.0f}px">
  <div style="position:absolute;left:18px;top:20px">{f.replace("width='400'", "width='360'").replace(f"height='{fh:.0f}'", f"height='{fh * 0.9:.0f}'")}</div></div>
<div style="position:absolute;left:54px;top:236px;font-size:30px;font-weight:800">1,000 people take the test</div>
<svg style="position:absolute;left:54px;top:286px" width="{gw}" height="{gh}" viewBox="0 0 {gw} {gh}">{grid}</svg>
<div style="position:absolute;left:{54 + gw + 30}px;top:340px;font-size:64px;color:{C['ink2']}">→</div>
<div style="position:absolute;left:{54 + gw + 110}px;top:318px;line-height:1.05">
  <div style="font-size:30px;font-weight:800;color:{C['aqua']}">108 test POSITIVE</div>
  <div class="h" style="font-size:70px;margin-top:14px"><span style="color:{C['orange']}">9</span>
    <span style="font-size:34px;color:{C['orange']};letter-spacing:0">really have it</span></div>
  <div class="h" style="font-size:70px;margin-top:6px"><span style="color:{C['blue']}">99</span>
    <span style="font-size:34px;color:{C['blue']};letter-spacing:0">false alarms</span></div>
  <div style="margin-top:18px;display:flex;align-items:baseline;gap:16px">
    <span class="h" style="font-size:96px;color:{C['violet']}">8%</span>
    <span style="font-size:30px;font-weight:800;color:{C['violet']}">real chance</span></div>
</div>
<div style="position:absolute;left:54px;top:{286 + gh + 26:.0f}px" class="badge">Explained in {MINS} minutes</div>"""
    return BASE % dict(C, body=body)


if __name__ == "__main__":
    shots = []
    for name, html in (("thumbnail_A.png", thumb_a()), ("thumbnail_B.png", thumb_b())):
        h = HERE / "build" / name.replace(".png", ".html"); h.write_text(html); shots.append((str(h.resolve()), str(OUT / name)))
    js = HERE / "build" / "shot.js"
    js.write_text("""const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1280,height:720}, deviceScaleFactor:1});
for (const [src, dst] of JSON.parse(process.argv[2])) { await p.goto('file://' + src); await p.waitForTimeout(500); await p.screenshot({path: dst}); }
await b.close(); })();""")
    subprocess.run(["node", str(js), json.dumps(shots)], check=True)
    from PIL import Image
    for n in ("A", "B"):
        im = Image.open(OUT / f"thumbnail_{n}.png"); print(n, im.size)
        im.resize((320, 180), Image.LANCZOS).save(HERE / "build" / f"thumb_{n}_phone.png")
