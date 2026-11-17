import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def gauge(title, color, tr, vmax=300, r=1.05):
    arc = Arc(radius=r, start_angle=PI, angle=-PI, color=INK2, stroke_width=4)
    ticks, labs = VGroup(), VGroup()
    for v in range(0, vmax + 1, 50):
        a = PI - v / vmax * PI
        d = np.array([np.cos(a), np.sin(a), 0])
        ticks.add(Line(d * (r - 0.1), d * r, color=INK2, stroke_width=3))
        if v % 100 == 0:
            labs.add(T(str(v), 20, INK2).move_to(d * (r + 0.25)))
    ttl = T(title, 28, color, weight=BOLD).next_to(arc, DOWN, buff=0.15)
    g = VGroup(arc, ticks, labs, ttl)
    c = arc.get_arc_center()
    needle = always_redraw(lambda: Line(g[0].get_arc_center(), g[0].get_arc_center() + (r - 0.2) * np.array(
        [np.cos(PI - min(tr.get_value(), vmax) / vmax * PI), np.sin(PI - min(tr.get_value(), vmax) / vmax * PI), 0]),
        color=color, stroke_width=6))
    val = always_redraw(lambda: T(f"{tr.get_value():.0f}", 30, color, weight=BOLD).move_to(g[0].get_arc_center() + UP * 0.38))
    hub = always_redraw(lambda: Dot(g[0].get_arc_center(), radius=0.07, color=color))
    g.add(needle, hub, val)
    return g


class S05Stress(Base):
    CHAPTER = "Stress Test"

    def construct(self):
        fr = self.camera.frame
        mt, dt = ValueTracker(60), ValueTracker(40)
        # ── s082 gauges ──
        self.at("s082", 0.0)
        gm = gauge("MEAN", WARN, mt).move_to(LEFT * 3.3 + UP * 2.0)
        gd = gauge("MEDIAN", VIOLET, dt).move_to(RIGHT * 3.3 + UP * 2.0)
        st = TB("stress test", 40, INK).move_to(UP * 2.25)
        self.play(FadeIn(gm, shift=RIGHT * 0.3), FadeIn(gd, shift=LEFT * 0.3), FadeIn(st), run_time=0.9)
        ax = money_axis(); ax.shift(DOWN * 0.95 - ax.axis.get_center()); L = ax.axis
        dots = dot_plot(PINE, L, [BLUE_] * 8 + [ORANGE_], r=0.1)
        mk = marker(L, 60, WARN, "", height=1.15)
        dm = diamond(L, 40, VIOLET, height=1.15)
        self.play(FadeIn(ax), LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in dots], lag_ratio=0.04),
                  FadeIn(mk), FadeIn(dm), run_time=1.0)
        # ── s083 the rich family ──
        self.at("s083", 0.0)
        mans = house(0.5, ORANGE_, mansion=True).next_to(dots[8], UP, buff=0.35)
        self.play(FadeIn(mans, shift=DOWN * 0.3), Flash(dots[8], color=ORANGE_, line_length=0.3), run_time=0.8)
        # ── s084 230 → 2,300: axis rescales (zoom-out) ──
        self.at("s084", 0.0)
        ax2 = money_axis(x_max=2400, step=200, label_every=2); ax2.shift(DOWN * 0.95 - ax2.axis.get_center()); L2 = ax2.axis
        k = 0.1
        old = VGroup(ax.axis, ax.nums)
        squeezed = old.copy().scale(k, about_point=L.n2p(0)).set_opacity(0)
        newpos = [L2.n2p(v) for v in PINE[:8]]
        self.play(FadeOut(mans), FadeOut(st), run_time=0.3)
        self.play(Transform(old, squeezed), FadeIn(ax2.axis), FadeIn(ax2.nums, lag_ratio=0.05),
                  *[d.animate.move_to(d.get_center() + (L2.n2p(v)[0] - d.get_x()) * RIGHT) for d, v in zip(dots[:8], PINE[:8])],
                  dots[8].animate.move_to(L2.n2p(230) + UP * 0.16),
                  mk.animate.shift((L2.n2p(60)[0] - mk.get_x()) * RIGHT), dm.animate.shift((L2.n2p(40)[0] - dm.get_x()) * RIGHT),
                  run_time=1.5)
        self.drop(old); self.add(ax2.axis, ax2.nums)
        self.until(word_time("s084", word_index("s084", "two")) + 0.8)
        self.play(dots[8].animate.move_to(L2.n2p(2300) + UP * 0.16), run_time=1.4, rate_func=smooth)
        x10 = T("×10", 36, ORANGE_, weight=BOLD).next_to(dots[8], UP, buff=0.3)
        self.play(FadeIn(x10, shift=UP * 0.2), run_time=0.5)
        # ── s085 nobody else changes ──
        self.at("s085", 0.0)
        cl = SurroundingRectangle(dots[:8], color=BLUE_, buff=0.12, corner_radius=0.06)
        unch = T("8 families: unchanged", 28, BLUE_).next_to(cl, UP, buff=0.55).align_to(cl, LEFT)
        self.play(Create(cl), FadeIn(unch), run_time=0.7)
        # ── s086 mean → 290 ──
        self.at("s086", 0.0)
        f = MathTex(r"{2610 \over 9}", font_size=72, color=INK).move_to(UP * 0.5 + RIGHT * 1.2)
        self.play(FadeIn(f, shift=UP * 0.2), FadeOut(x10), run_time=0.7)
        self.until(word_time("s086", word_index("s086", "mean")))
        e = TB("= 290", 64, WARN).next_to(f, RIGHT, buff=0.3)
        self.play(FadeIn(e, shift=LEFT * 0.2), mt.animate.set_value(290),
                  mk.animate.shift((L2.n2p(290)[0] - mk.get_x()) * RIGHT), run_time=1.5, rate_func=rate_functions.ease_out_cubic)
        # ── s087 almost five times ──
        self.at("s087", 0.0)
        badge = chip("≈ ×4.8", WARN, 30).next_to(gm, RIGHT, buff=0.3)
        self.play(GrowFromCenter(badge), run_time=0.5)
        self.until(word_time("s087", word_index("s087", "yet")))
        p0 = T("+0 each", 28, BLUE_).move_to(unch)
        self.play(Transform(unch, p0), Indicate(dots[:8], color=BLUE_), run_time=0.9)
        # ── s088 median still 40 ──
        self.at("s088", 0.0)
        self.play(FadeOut(VGroup(f, e)), run_time=0.4)
        still = glow(T("median: still 40", 34, VIOLET, weight=BOLD), VIOLET).move_to(UP * 0.5 + RIGHT * 1.2)
        self.play(Wiggle(gd, scale_value=1.04, rotation_angle=0.0), FadeIn(still), run_time=1.0)
        # ── s089 only which side ──
        self.at("s089", 0.0)
        self.play(FadeOut(still), FadeOut(badge), FadeOut(unch), FadeOut(cl), run_time=0.4)
        rowt = tiles(PINE[:8] + [2300], size=0.62, fs=24).move_to(UP * 0.55)
        for t in rowt[:4]: t[0].set_stroke(BLUE_)
        self.play(FadeIn(rowt, lag_ratio=0.05), run_time=0.6)
        self.play(*hl(rowt[4], VIOLET), run_time=0.4)
        lb = Brace(rowt[:4], DOWN, color=BLUE_); rb = Brace(rowt[5:], DOWN, color=ORANGE_)
        lt = T("4 on the left", 24, BLUE_).next_to(lb, DOWN, buff=0.08)
        rt = T("4 on the right — size doesn't matter", 24, ORANGE_).next_to(rb, DOWN, buff=0.08)
        self.play(GrowFromCenter(lb), GrowFromCenter(rb), FadeIn(lt), FadeIn(rt), run_time=0.8)
        # ── s090 outliers ──
        self.at("s090", 0.0)
        ring = Circle(0.3, color=ORANGE_, stroke_width=4).move_to(dots[8])
        ol = glow(T("outlier", 34, ORANGE_, weight=BOLD), ORANGE_).next_to(ring, UP, buff=0.12)
        self.play(FadeOut(VGroup(rowt, lb, rb, lt, rt)), Create(ring), FadeIn(ol, shift=DOWN * 0.2), run_time=0.8)
        # ── s091 tug of war ──
        self.at("s091", 0.0)
        rope = Line(ring.get_left(), mk.tri.get_right(), color=ORANGE_, stroke_width=4)
        self.play(Create(rope), run_time=0.6)
        drag = T("dragged", 28, WARN).next_to(mk, UP, buff=0.05)
        anch = T("anchored", 28, VIOLET).next_to(dm, UP, buff=0.75); anch.set_x(max(anch.get_x(), -5.9))
        self.play(FadeIn(drag), FadeIn(anch), run_time=0.5)
        rob = chip("robust = hardly moved by outliers", VIOLET, 32).move_to(UP * 0.55)
        self.until(word_time("s091", word_index("s091", "statisticians")))
        self.play(FadeIn(rob, shift=UP * 0.2), run_time=0.6)
        # ── s092 back to 230; poorest falls 30 → 10 ──
        self.at("s092", 0.0)
        self.play(FadeOut(VGroup(rope, drag, anch, rob, ring, ol)), run_time=0.4)
        ax3 = money_axis(); ax3.shift(DOWN * 0.95 - ax3.axis.get_center()); L3 = ax3.axis
        self.play(FadeOut(VGroup(ax2.axis, ax2.nums)), FadeIn(VGroup(ax3.axis, ax3.nums)),
                  *[d.animate.move_to(d.get_center() + (L3.n2p(v)[0] - d.get_x()) * RIGHT) for d, v in zip(dots[:8], PINE[:8])],
                  dots[8].animate.move_to(L3.n2p(230) + UP * 0.16), mt.animate.set_value(60),
                  mk.animate.shift((L3.n2p(60)[0] - mk.get_x()) * RIGHT), dm.animate.shift((L3.n2p(40)[0] - dm.get_x()) * RIGHT),
                  run_time=1.4)
        self.until(word_time("s092", word_index("s092", "poorest")))
        fall = Arrow(L3.n2p(30) + UP * 0.6, L3.n2p(10) + UP * 0.6, buff=0, color=BLUE_, stroke_width=4)
        poor = dots[0]
        self.play(GrowArrow(fall), poor.animate.move_to(L3.n2p(10) + UP * 0.16), run_time=1.0)
        # ── s093 mean dips to 57.8 ──
        self.at("s093", 0.0)
        self.until(word_time("s093", word_index("s093", "mean")))
        f2 = MathTex(r"{520 \over 9}", r"\approx 57.8", font_size=64, color=INK).move_to(UP * 0.3 + RIGHT * 2.3)
        f2[1].set_color(WARN)
        self.play(FadeIn(f2), mt.animate.set_value(57.8), mk.animate.shift((L3.n2p(57.8)[0] - mk.get_x()) * RIGHT), run_time=1.0)
        # ── s094 median doesn't see it ──
        self.at("s094", 0.0)
        miss = T("median: still 40 — missed it", 30, RED_).next_to(dm, UP, buff=0.12).shift(RIGHT * 1.6)
        self.play(FadeIn(miss, shift=DOWN * 0.2), Indicate(gd, color=RED_, scale_factor=1.04), run_time=0.9)
        # ── s095 trade-off card ──
        self.at("s095", 0.0)
        self.play(FadeOut(VGroup(gm, gd, f2, miss, fall, ax3.axis, ax3.nums, ax.title, dots, mk, dm)), run_time=0.5)
        tc = two_col("MEAN", ["uses every value", "dragged by outliers"], "MEDIAN", ["robust to outliers", "ignores how far values are"])
        tc.move_to(UP * 0.5)
        self.play(FadeIn(tc[0], shift=RIGHT * 0.3), run_time=0.6)
        self.play(FadeIn(tc[1], shift=LEFT * 0.3), run_time=0.6)
        cost = T("each choice has a cost", 30, INK2).next_to(tc, DOWN, buff=0.35)
        self.until(word_time("s095", word_index("s095", "each")))
        self.play(FadeIn(cost), run_time=0.5)
        # ── s096 back to normal; two dot lines ──
        self.at("s096", 0.0)
        self.play(FadeOut(VGroup(tc, cost)), run_time=0.5)
        axM = money_axis(); axM.title.set_opacity(0); axM.shift(UP * 1.1 - axM.axis.get_center()); LM = axM.axis
        axP = money_axis(); axP.shift(DOWN * 1.15 - axP.axis.get_center()); LP = axP.axis
        dM = dot_plot(MAPLE, LM, [INK] * 9); dP = dot_plot(PINE, LP, [BLUE_] * 8 + [ORANGE_])
        nM = TB("Maple", 32).next_to(LM, UP, buff=1.1).align_to(LM, LEFT)
        nP = TB("Pine Hill", 32).next_to(LP, UP, buff=1.1).align_to(LP, LEFT)
        self.play(FadeIn(axM), FadeIn(axP), FadeIn(nM), FadeIn(nP), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in [*dM, *dP]], lag_ratio=0.03), run_time=1.0)
        # ── s097 mirror ──
        self.at("s097", 0.0)
        self.play(fr.animate.scale(0.5).move_to([LM.n2p(60)[0], 1.9, 0]), FadeOut(nP), run_time=1.0)
        mir = DashedLine(LM.n2p(60) + DOWN * 0.05, LM.n2p(60) + UP * 1.1, color=AQUA, stroke_width=3)
        self.play(Create(mir), run_time=0.5)
        pairs = VGroup()
        for a, b in ((50, 70), (52, 68), (55, 65), (58, 62)):
            da = next(d for d in dM if d.value == a); db = next(d for d in dM if d.value == b)
            pairs.add(CurvedArrow(da.get_top() + UP * 0.05, db.get_top() + UP * 0.05, angle=-0.9, color=AQUA,
                                  stroke_width=2, tip_length=0.08))
        mirt = T("mirror image", 22, AQUA).next_to(mir, UP, buff=0.06)
        self.play(LaggedStart(*[Create(p) for p in pairs], lag_ratio=0.25), FadeIn(mirt), run_time=1.4)
        # ── s098 symmetric: both at 60 ──
        self.at("s098", 0.0)
        self.play(FadeOut(pairs), FadeOut(mirt), fr.animate.scale(2).move_to(ORIGIN), FadeIn(nP), run_time=0.9)
        mmM = marker(LM, 60, WARN, "", height=1.15); dmM = diamond(LM, 60, VIOLET, height=1.5)
        sym = T("symmetric: mean = median", 28, INK).next_to(dmM, RIGHT, buff=0.35)
        self.play(FadeIn(mmM), FadeIn(dmM), FadeIn(sym, shift=LEFT * 0.2), run_time=0.8)
        # ── s099 Pine Hill's long tail ──
        self.at("s099", 0.0)
        tail = Arrow(LP.n2p(52) + UP * 0.45, LP.n2p(225) + UP * 0.45, buff=0, color=ORANGE_, stroke_width=5)
        crowd = T("crowd", 26, BLUE_).next_to(dP[:8], UP, buff=0.12)
        tt = T("long, thin tail", 26, ORANGE_).next_to(tail, UP, buff=0.1)
        self.play(FadeIn(crowd), run_time=0.4)
        self.play(GrowArrow(tail), FadeIn(tt), run_time=1.0)
        # ── s100 right-skewed ──
        self.at("s100", 0.0)
        rs = glow(TB("right-skewed", 30, ORANGE_), ORANGE_).move_to([LP.n2p(185)[0], 0.25, 0])
        self.play(FadeIn(rs), run_time=0.5)
        mmP = marker(LP, 60, WARN, "", height=0.75); dmP = diamond(LP, 40, VIOLET, height=1.1)
        self.until(word_time("s100", word_index("s100", "mean")))
        self.play(FadeOut(crowd), FadeIn(dmP), FadeIn(mmP), run_time=0.6)
        pull = Arrow(mmP.tri.get_right(), mmP.tri.get_right() + RIGHT * 1.2, buff=0.05, color=WARN, stroke_width=4)
        self.play(GrowArrow(pull), run_time=0.6)
        # ── s101 flipped: tail on the left ──
        self.at("s101", 0.0)
        flip = [240 - v for v in PINE]
        dF = dot_plot(flip, LM, [BLUE_] * 8 + [ORANGE_])
        self.play(FadeOut(VGroup(dM, mmM, dmM, sym, mir)), Transform(nM, TB("mirror of Pine Hill (shape only)", 28, INK2)
                  .move_to(nM, aligned_edge=LEFT)), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in dF], lag_ratio=0.04), run_time=0.8)
        mF = marker(LM, 180, WARN, "mean", height=0.75, fs=24, label_dir=LEFT); dF_ = diamond(LM, 200, VIOLET, "median", height=1.4, fs=24, label_dir=RIGHT)
        self.play(FadeIn(mF), FadeIn(dF_), run_time=0.7)
        # ── s102 warning light ──
        self.at("s102", 0.0)
        self.play(FadeOut(VGroup(dF, mF, dF_, nM, axM, nP, axP, dP, tail, tt, rs, mmP, dmP, pull)), run_time=0.5)
        lamp = Circle(0.75, color=WARN, fill_opacity=0.9).move_to(LEFT * 4.2 + UP * 0.6)
        rays = VGroup(*[Line(UP * 0.95, UP * 1.25, color=WARN, stroke_width=5).rotate(a, about_point=ORIGIN).shift(lamp.get_center())
                        for a in np.linspace(-1.0, 1.0, 5)])
        wt = VGroup(T("mean much bigger than median", 34, INK), T("→ look for a few big values pulling it up", 34, WARN)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).next_to(lamp, RIGHT, buff=0.8)
        self.play(GrowFromCenter(lamp), run_time=0.5)
        self.play(FadeIn(rays), lamp.animate.set_fill(opacity=0.4), rate_func=there_and_back, run_time=0.6)
        self.play(FadeIn(wt[0], shift=LEFT * 0.2), run_time=0.6)
        self.play(FadeIn(wt[1], shift=LEFT * 0.2), run_time=0.6)
        # ── s103 rule of thumb ──
        self.at("s103", 0.0)
        stamp = VGroup(RoundedRectangle(corner_radius=0.1, width=4.6, height=1.0, color=RED_, stroke_width=5),
                       TB("RULE OF THUMB", 44, RED_)).rotate(0.12).move_to(DOWN * 1.35 + RIGHT * 1.3)
        stamp[0].qa_container = True
        self.play(FadeIn(stamp, scale=1.6), run_time=0.5)
        look = T("always look at the actual values too", 28, INK2).next_to(stamp, RIGHT, buff=0.4)
        look = T("always look at the actual values too", 24, INK2).move_to([4.0, -1.35, 0])
        self.until(word_time("s103", word_index("s103", "always")))
        self.play(stamp.animate.shift(LEFT * 3.8), FadeIn(look), run_time=0.7)
        self.finish()
