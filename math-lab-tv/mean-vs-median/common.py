"""Shared style, timing and QA helpers for all scenes."""
import json, pathlib, os
import numpy as np
from manim import *

HERE = pathlib.Path(__file__).parent
TIM = json.loads((HERE / "timings.json").read_text())
SEGS = {s["id"]: s for s in TIM["segments"]}
ORDER = [s["id"] for s in TIM["segments"]]
CHAPTERS = []
for s in TIM["segments"]:
    if not CHAPTERS or CHAPTERS[-1]["name"] != s["chapter"]:
        CHAPTERS.append(dict(name=s["chapter"], first=s["id"], segs=[]))
    CHAPTERS[-1]["segs"].append(s["id"])
# scene windows: chapter k runs from (first start of k, or 0) to first start of k+1 (or total)
for k, c in enumerate(CHAPTERS):
    c["t0"] = 0.0 if k == 0 else SEGS[c["first"]]["start"] - 0.25
for k, c in enumerate(CHAPTERS):
    c["t1"] = CHAPTERS[k + 1]["t0"] if k + 1 < len(CHAPTERS) else TIM["total"]

# ── palette ──
BG = "#1a1a19"
BLUE_ = "#3987e5"; ORANGE_ = "#d95926"; AQUA = "#199e70"; VIOLET = "#9085e9"
WARN = "#fab219"; RED_ = "#d03b3b"; INK = "#f0efec"; INK2 = "#c3c2b7"; MUTED = "#898781"
GRID = "#3a3a37"
config.background_color = BG
config.frame_rate = 30
config.pixel_width, config.pixel_height = 1920, 1080

FONT, FONT_D = "Inter", "Inter Display"

# ── safe area (in screen units relative to camera frame, frame = 14.222 x 8) ──
# subtitles occupy the bottom 175 px; chapter label occupies top-left 520x110 px
PX = 8 / 1080
SAFE_BOTTOM = -4 + 175 * PX          # content must stay above this
LABEL_BOX = (-7.111, 4 - 110 * PX, -7.111 + 520 * PX, 4)  # x0, y0, x1, y1


def T(text, size=36, color=INK, weight=NORMAL, display=False, **kw):
    return Text(text, font=FONT_D if display else FONT, font_size=size, color=color, weight=weight, **kw)


def TB(text, size=48, color=INK, **kw):
    return T(text, size=size, color=color, weight=BOLD, display=True, **kw)


def glow(mob, color=None, layers=6, width=14, opacity=0.06):
    """Return VGroup(glow layers..., mob). Glow is built from copies of mob, so it moves,
    scales and fades with the group. Always animate the returned group, never mob alone."""
    color = color or mob.get_color()
    g = VGroup()
    for i in range(layers, 0, -1):
        c = mob.copy().set_fill(opacity=0).set_stroke(color, width=width * i / layers, opacity=opacity)
        g.add(c)
    grp = VGroup(g, mob)
    grp.is_glow_group = True
    for m in g.family_members_with_points():
        m.qa_ignore = True
    return grp


def money_axis(x_max=240, step=20, length=12.2, label="Household income (thousand $)", label_every=1,
               font_size=24):
    ax = NumberLine(x_range=[0, x_max, step], length=length, color=INK2, stroke_width=3,
                    include_tip=False, tick_size=0.09)
    nums = VGroup()
    for i, v in enumerate(np.arange(0, x_max + 0.1, step)):
        if i % label_every: continue
        n = T(f"{int(v):,}", size=font_size, color=INK2)
        n.next_to(ax.n2p(v), DOWN, buff=0.18)
        n.qa_clip_ok = True
        nums.add(n)
    title = T(label, size=26, color=MUTED).next_to(nums, DOWN, buff=0.2).align_to(ax, LEFT)
    g = VGroup(ax, nums, title)
    g.axis, g.nums, g.title = ax, nums, title
    return g


def dot(color=BLUE_, r=0.13):
    d = Dot(radius=r, color=color).set_stroke(BG, 2)
    d.qa_dot = True
    return d


def chip(text, color=INK, size=30, fill=None, pad=0.22):
    t = T(text, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 2 * pad, height=t.height + 1.5 * pad,
                           stroke_color=color, stroke_width=2, fill_color=fill or BG, fill_opacity=1)
    t.move_to(box)
    g = VGroup(box, t)
    box.qa_container = True
    return g


def house(w=0.62, color=INK2, mansion=False):
    if mansion:
        body = Rectangle(width=w * 1.9, height=w * 1.0)
        roof = Polygon(body.get_corner(UL) + LEFT * 0.08, body.get_corner(UR) + RIGHT * 0.08,
                       body.get_top() + UP * w * 0.55)
        door = Rectangle(width=w * 0.24, height=w * 0.42).align_to(body, DOWN)
        wins = VGroup(*[Square(w * 0.2).move_to(body.get_center() + np.array([dx, 0.12 * w, 0]))
                        for dx in (-0.6 * w, -0.3 * w, 0.3 * w, 0.6 * w)])
        cols = VGroup(*[Line(body.get_corner(DL) + RIGHT * dx, body.get_corner(UL) + RIGHT * dx)
                        for dx in (w * 0.05, w * 1.85)])
        g = VGroup(body, roof, door, wins, cols)
    else:
        body = Rectangle(width=w, height=w * 0.7)
        roof = Polygon(body.get_corner(UL) + LEFT * 0.06, body.get_corner(UR) + RIGHT * 0.06,
                       body.get_top() + UP * w * 0.45)
        door = Rectangle(width=w * 0.22, height=w * 0.36).align_to(body, DOWN)
        g = VGroup(body, roof, door)
    g.set_stroke(color, 3).set_fill(BG, 1)
    return g


class Base(MovingCameraScene):
    """Timing-driven scene. self.at(id, dt) waits until segment `id` starts (+dt)."""
    CHAPTER = None

    def setup(self):
        super().setup()
        self.ch = next(c for c in CHAPTERS if c["name"] == self.CHAPTER)
        self.t0 = self.ch["t0"]
        self.qa_log = []
        self.camera.frame.save_state()

    # time on the global timeline
    def now(self):
        return self.t0 + self.renderer.time

    def at(self, sid, dt=0.0):
        target = SEGS[sid]["start"] + dt
        w = target - self.now()
        if w > 1 / 30:
            self.wait(w)

    def seg_end(self, sid):
        return SEGS[sid]["end"]

    def until(self, t_global):
        w = t_global - self.now()
        if w > 1 / 30:
            self.wait(w)

    def finish(self):
        self.until(self.ch["t1"])

    def qa_mute(self, mob, on=True):
        """Exclude mobjects hidden under an opaque overlay from the overlap checks (and re-include them)."""
        for m in mob.get_family():
            m.qa_ignore = on

    def drop(self, *ms):
        """Remove mobjects and every member of their families from the scene."""
        fam = []
        for m in ms:
            fam += m.get_family()
        self.remove(*fam)

    def play(self, *a, **k):
        super().play(*a, **k)
        self.qa_check()

    # ── QA: overlap checker run after every animation ──
    def _texts(self):
        out = []
        for m in self.mobjects:
            for sub in m.get_family():
                if isinstance(sub, (Text, MathTex, Tex, MarkupText)) and not getattr(sub, "qa_ignore", False):
                    op = max([x.get_fill_opacity() for x in sub.family_members_with_points()] or [0])
                    if op > 0.3 and sub.width > 0.02:
                        out.append(sub)
        # dedupe (MathTex families include SingleStringMathTex parts)
        seen, res = set(), []
        for t in out:
            if id(t) in seen: continue
            for s in t.get_family()[1:]: seen.add(id(s))
            res.append(t)
        return [t for t in res if id(t) not in seen]

    def _screen_box(self, m):
        f = self.camera.frame
        s = 8 / f.height
        c = f.get_center()
        (x0, y0, _), (x1, y1, _) = m.get_corner(DL), m.get_corner(UR)
        return ((x0 - c[0]) * s, (y0 - c[1]) * s, (x1 - c[0]) * s, (y1 - c[1]) * s)

    def qa_check(self):
        t = round(self.now(), 2)
        texts = self._texts()
        boxes = [(m, self._screen_box(m)) for m in texts]
        W, H = 7.111, 4.0
        def name(m):
            return getattr(m, "text", None) or getattr(m, "tex_string", None) or type(m).__name__
        for m, (x0, y0, x1, y1) in boxes:
            if x1 < -W or x0 > W or y1 < -H or y0 > H:
                continue  # fully off-screen
            if (x0 < -W + 0.05 or x1 > W - 0.05 or y1 > H - 0.05 or y0 < -H + 0.05) and not getattr(m, "qa_clip_ok", False):
                self.qa_log.append(dict(t=t, kind="clipped", a=name(m)))
            if y0 < SAFE_BOTTOM:
                self.qa_log.append(dict(t=t, kind="under_subtitles", a=name(m)))
            lx0, ly0, lx1, ly1 = LABEL_BOX
            if x0 < lx1 and y1 > ly0:
                self.qa_log.append(dict(t=t, kind="chapter_corner", a=name(m)))
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                (a, A), (b, B) = boxes[i], boxes[j]
                ox = min(A[2], B[2]) - max(A[0], B[0]); oy = min(A[3], B[3]) - max(A[1], B[1])
                if ox > -0.06 and oy > -0.06:  # boxes closer than ~8 px count as touching
                    self.qa_log.append(dict(t=t, kind="text_text", a=name(a), b=name(b)))
        # text vs solid shapes (filled, not a container/background of that text)
        shapes = []
        for m in self.mobjects:
            for sub in m.get_family():
                if (isinstance(sub, VMobject) and not isinstance(sub, (Text, MathTex, Tex, MarkupText))
                        and sub.get_fill_opacity() > 0.5 and not getattr(sub, "qa_container", False)
                        and not getattr(sub, "qa_ignore", False) and len(sub.points) > 0
                        and not any(isinstance(p, (Text, MathTex, Tex)) for p in [sub])
                        and sub.get_fill_color().to_hex().lower() != BG.lower()):
                    shapes.append(sub)
        textfam = set()
        for m in texts:
            for s in m.get_family(): textfam.add(id(s))
        textfam_all = set()
        for m in self.mobjects:
            for sub in m.get_family():
                if isinstance(sub, (Text, MathTex, Tex, MarkupText)):
                    for s2 in sub.get_family(): textfam_all.add(id(s2))
        # text crossed by strokes (lines, arrows, curves, outlines): sample points along each stroke path
        strokes = []
        for m in self.mobjects:
            for sub in m.get_family():
                if (isinstance(sub, VMobject) and not isinstance(sub, (Text, MathTex, Tex, MarkupText))
                        and len(sub.points) >= 4 and sub.get_stroke_width() > 0.5 and sub.get_stroke_opacity() > 0.3
                        and not getattr(sub, "qa_container", False) and not getattr(sub, "qa_ignore", False)
                        and id(sub) not in textfam_all and sub.get_stroke_color().to_hex().lower() != BG.lower()):
                    strokes.append(sub)
        f = self.camera.frame; sc = 8 / f.height; cc = f.get_center()
        ts_ = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
        for st in strokes:
            P = st.points[: len(st.points) // 4 * 4].reshape(-1, 4, 3)
            pts = (((1 - ts_)[None, :, None] ** 3 * P[:, None, 0] + 3 * ((1 - ts_) ** 2 * ts_)[None, :, None] * P[:, None, 1]
                    + 3 * ((1 - ts_) * ts_ ** 2)[None, :, None] * P[:, None, 2] + (ts_ ** 3)[None, :, None] * P[:, None, 3]))
            pts = (pts.reshape(-1, 3)[:, :2] - cc[:2]) * sc
            for a, A in boxes:
                m = 0.03
                inside = ((pts[:, 0] > A[0] + m) & (pts[:, 0] < A[2] - m) & (pts[:, 1] > A[1] + m) & (pts[:, 1] < A[3] - m))
                if inside.any():
                    self.qa_log.append(dict(t=t, kind="text_stroke", a=name(a), b=type(st).__name__))
        # marker heads (mean triangle / median diamond) sitting on dots
        fam = [sub for m in self.mobjects for sub in m.get_family()]
        heads = [h for h in fam if getattr(h, "qa_head", False) and h.get_fill_opacity() > 0.3]
        dots_ = [d for d in fam if getattr(d, "qa_dot", False) and d.get_fill_opacity() > 0.3]
        for h in heads:
            H_ = self._screen_box(h)
            for d in dots_:
                D_ = self._screen_box(d)
                ox = min(H_[2], D_[2]) - max(H_[0], D_[0]); oy = min(H_[3], D_[3]) - max(H_[1], D_[1])
                if ox > 0.01 and oy > -0.02:
                    self.qa_log.append(dict(t=t, kind="marker_dot", a=type(h).__name__, b="Dot")); break
        for a, A in boxes:
            for s in shapes:
                if id(s) in textfam: continue
                B = self._screen_box(s)
                ox = min(A[2], B[2]) - max(A[0], B[0]); oy = min(A[3], B[3]) - max(A[1], B[1])
                if ox > 0.04 and oy > 0.04:
                    self.qa_log.append(dict(t=t, kind="text_shape", a=name(a), b=type(s).__name__))

    def tear_down(self):
        super().tear_down()
        out = HERE / "build" / "qa"; out.mkdir(parents=True, exist_ok=True)
        # collapse repeats
        uniq = {}
        for e in self.qa_log:
            k = (e["kind"], e.get("a"), e.get("b"))
            uniq.setdefault(k, []).append(e["t"])
        res = [dict(kind=k[0], a=k[1], b=k[2], times=v[:6], n=len(v)) for k, v in uniq.items()]
        (out / f"{type(self).__name__}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))


def _syl(w):
    import re
    w = w.lower()
    return max(1, len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and len(w) > 3 else 0))


def word_time(sid, k):
    """Estimated global start time of the k-th word (0-based) of segment sid,
    spreading the clip's duration over syllables plus ~0.22 s per comma/full stop."""
    s = SEGS[sid]
    words = s["text"].split()
    w = []
    for x in words:
        w.append(sum(_syl(q) for q in x.strip(",.;:?!'").split("-") if q))
        if x[-1] in ",.;:?!":
            w.append(-1)
    PAUSE = 0.22
    npause = sum(1 for v in w if v < 0)
    syl = sum(v for v in w if v > 0)
    rate = (s["end"] - s["start"] - PAUSE * npause) / syl
    t, i = s["start"], 0
    for v in w:
        if v < 0:
            t += PAUSE; continue
        if i == k:
            return t
        t += v * rate; i += 1
    return s["end"]


def word_index(sid, word):
    """Index of first word starting with `word` (case-insensitive, punctuation stripped)."""
    ws = [x.strip(",.;:?!'").lower() for x in SEGS[sid]["text"].split()]
    return ws.index(word.lower().strip(",.;:?!'"))


def dot_plot(values, axis, colors, r=0.1, gap=0.02):
    """Dots stacked upward where they would overlap, sitting on `axis` (a NumberLine)."""
    placed, g = [], VGroup()
    for v, c in zip(values, colors):
        x = axis.n2p(v)[0]
        lvl = 0
        while any(abs(x - px) < 2 * r + gap and pl == lvl for px, pl in placed):
            lvl += 1
        placed.append((x, lvl))
        d = dot(c, r).move_to(axis.n2p(v) + UP * (r + 0.06 + lvl * (2 * r + gap)))
        d.value = v
        g.add(d)
    return g


PINE = [30, 32, 35, 38, 40, 42, 45, 48, 230]
MAPLE = [50, 52, 55, 58, 60, 62, 65, 68, 70]
STREET = [42, 230, 35, 48, 30, 45, 38, 32, 40]


def xy_axes(x_range, y_range, x_len, y_len, x_label, y_label, x_labels=None, font_size=22, y_vertical=False):
    """Axes with Inter tick labels and axis titles. x_labels: optional {value: text}."""
    ax = Axes(x_range=x_range, y_range=y_range, x_length=x_len, y_length=y_len,
              axis_config=dict(color=INK2, stroke_width=3, include_tip=False, tick_size=0.07),
              x_axis_config=dict(include_ticks=True), y_axis_config=dict(include_ticks=True))
    labs = VGroup()
    xs = np.arange(x_range[0], x_range[1] + 1e-9, x_range[2])
    for v in xs:
        if x_labels is not None and v not in x_labels: continue
        txt = x_labels[v] if x_labels else f"{v:g}"
        t = T(txt, font_size, INK2).next_to(ax.c2p(v, y_range[0]), DOWN, buff=0.14); t.qa_clip_ok = True
        labs.add(t)
    for v in np.arange(y_range[0], y_range[1] + 1e-9, y_range[2]):
        t = T(f"{v:g}", font_size, INK2).next_to(ax.c2p(x_range[0], v), LEFT, buff=0.14); t.qa_clip_ok = True
        labs.add(t)
    if x_label:
        xt = T(x_label, 24, MUTED).next_to(ax.x_axis, DOWN, buff=0.5).align_to(ax.x_axis, RIGHT)
    else:
        xt = VGroup()
    if y_vertical:
        ylabs = VGroup(*[l for l in labs if abs(l.get_x() - ax.c2p(x_range[0], 0)[0]) > 0.05 and l.get_x() < ax.c2p(x_range[0], 0)[0]])
        yt = T(y_label, 22, MUTED).rotate(PI / 2).next_to(ylabs if len(ylabs) else ax.y_axis, LEFT, buff=0.15)
    else:
        yt = T(y_label, 24, MUTED).next_to(ax.y_axis, UP, buff=0.18).align_to(ax.y_axis, LEFT).shift(LEFT * 0.3)
    g = VGroup(ax, labs, xt, yt)
    g.ax, g.labs, g.xt, g.yt = ax, labs, xt, yt
    return g


def tile(v, color=INK, size=0.78, fs=30, fill="#22221f"):
    sq = RoundedRectangle(corner_radius=0.1, width=size * (1.35 if v >= 100 else 1), height=size,
                          stroke_color=color, stroke_width=2.5, fill_color=fill, fill_opacity=1)
    sq.qa_container = True
    t = T(str(v), fs, color, weight=BOLD).move_to(sq)
    g = VGroup(sq, t); g.value = v
    return g


def tiles(values, colors=None, buff=0.18, **kw):
    colors = colors or [BLUE_ if v < 100 else ORANGE_ for v in values]
    return VGroup(*[tile(v, c, **kw) for v, c in zip(values, colors)]).arrange(RIGHT, buff=buff)


def marker(axis, v, color, label, height=0.75, fs=28, side=UP, label_dir=UP):
    """Triangle pointer above axis value v with dashed stem and a label."""
    tri = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.15).rotate(PI)
    tri.move_to(axis.n2p(v) + UP * height)
    stem = DashedLine(tri.get_bottom(), axis.n2p(v), color=color, stroke_width=3)
    lab = T(label, fs, color, weight=BOLD).next_to(tri, label_dir, buff=0.12)
    tri.qa_head = True
    g = VGroup(stem, tri, lab); g.tri, g.lab = tri, lab
    return g


def diamond(axis, v, color=VIOLET, label=None, height=0.75, fs=28, label_dir=UP):
    d = Square(0.22, color=color, fill_opacity=1, stroke_width=0).rotate(PI / 4).move_to(axis.n2p(v) + UP * height)
    stem = DashedLine(d.get_bottom(), axis.n2p(v), color=color, stroke_width=3)
    d.qa_head = True
    g = VGroup(stem, d)
    if label:
        lab = T(label, fs, color, weight=BOLD).next_to(d, label_dir, buff=0.12); g.add(lab); g.lab = lab
    g.tri = d
    return g


def defcard(sym_tex, words, color=INK, fs=30, w=None):
    """A definition card: [symbol]  =  plain words."""
    s = MathTex(sym_tex, color=color, font_size=fs * 1.6)
    e = T("=", fs, MUTED)
    t = T(words, fs, INK)
    row = VGroup(s, e, t).arrange(RIGHT, buff=0.22)
    box = RoundedRectangle(corner_radius=0.14, width=(w or row.width + 0.6), height=row.height + 0.42,
                           stroke_color=color, stroke_width=2, fill_color="#22221f", fill_opacity=1)
    box.qa_container = True
    row.move_to(box)
    return VGroup(box, row)


def frac(num, den, color=INK, fs=72):
    return MathTex(r"{" + str(num) + r"\over " + str(den) + r"}", color=color, font_size=fs)


def two_col(left_title, left_lines, right_title, right_lines, lc=WARN, rc=VIOLET, w=5.6):
    cols = VGroup()
    for title, lines, c in ((left_title, left_lines, lc), (right_title, right_lines, rc)):
        tt = TB(title, 40, c)
        ls = VGroup(*[T("• " + l, 28, INK) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        inner = VGroup(tt, ls).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        box = RoundedRectangle(corner_radius=0.18, width=w, height=inner.height + 0.7, stroke_color=c,
                               stroke_width=2.5, fill_color="#22221f", fill_opacity=1)
        box.qa_container = True
        inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.4)
        cols.add(VGroup(box, inner))
    hmax = max(c[0].height for c in cols)
    for c in cols:
        c[0].stretch_to_fit_height(hmax); c[1].align_to(c[0], UP).shift(DOWN * 0.35)
    return cols.arrange(RIGHT, buff=0.5)


def hl(t, color, fill=0.22):
    """Animations that highlight a tile (box + number) without filling over its number."""
    return [t[0].animate.set_stroke(color).set_fill(color, fill), t[1].animate.set_color(color)]


def unhl(t, color):
    return [t[0].animate.set_stroke(color).set_fill("#22221f", 1), t[1].animate.set_color(color)]


def logo_mark(size=1.0):
    """Channel mark: violet rounded square with a green bell curve (as in the Math Lab TV intro/outro)."""
    sq = RoundedRectangle(corner_radius=0.16 * size, width=size, height=size, stroke_color=VIOLET, stroke_width=5 * size,
                          fill_color=BG, fill_opacity=1)
    sq.qa_container = True
    xs = np.linspace(-0.36, 0.36, 60) * size
    curve = VMobject(stroke_color=AQUA, stroke_width=5 * size).set_points_smoothly(
        [np.array([x, -0.24 * size + 0.5 * size * np.exp(-(x / (0.14 * size)) ** 2), 0]) for x in xs])
    curve.qa_ignore = True
    return VGroup(sq, curve)


def logo(size=1.0, tagline=False):
    mark = logo_mark(size)
    name = Text("MATH LAB TV", font=FONT_D, weight=BOLD, font_size=int(78 * size), color=INK)
    g = VGroup(mark, name).arrange(RIGHT, buff=0.32 * size)
    if tagline:
        tl = T("where math is something you can see", int(34 * size), INK2)
        tl.next_to(g, DOWN, buff=0.35 * size)
        g = VGroup(g, tl)
    return g
