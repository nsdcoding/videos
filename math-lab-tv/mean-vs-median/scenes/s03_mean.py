import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def block(color, s=0.2):
    return Square(s, color=color, fill_opacity=1, stroke_width=2).set_stroke(BG, 2)


class S03Mean(Base):
    CHAPTER = "The Mean"

    def construct(self):
        fr = self.camera.frame
        # ── s027 MEAN ──
        self.at("s027", 0.6)
        word = glow(TB("MEAN", 140, WARN), WARN).move_to(UP * 0.9)
        self.play(Write(word[1]), FadeIn(word[0]), run_time=1.0)
        # ── s028 mean = "the average" ──
        self.at("s028", 0.2)
        eqc = VGroup(T("mean", 44, WARN, weight=BOLD), T("=", 44, MUTED), T("“the average”", 44, INK)).arrange(RIGHT, buff=0.3)
        eqc.next_to(word, DOWN, buff=0.6)
        self.play(word.animate.scale(0.6).shift(UP * 0.6), FadeIn(eqc, shift=UP * 0.3), run_time=0.8)
        # ── s029 two steps ──
        self.at("s029", 0.4)
        c1 = chip("①  add them all up", INK, 34); c2 = chip("②  divide by how many", INK, 34)
        steps = VGroup(c1, c2).arrange(RIGHT, buff=0.6).next_to(eqc, DOWN, buff=0.7)
        self.play(FadeIn(c1, shift=RIGHT * 0.4), run_time=0.6)
        self.until(word_time("s029", word_index("s029", "divide")))
        self.play(FadeIn(c2, shift=RIGHT * 0.4), run_time=0.6)
        # ── s030 Pine Hill tiles ──
        self.at("s030", 0.0)
        self.play(FadeOut(VGroup(word, eqc)), steps.animate.scale(0.7).to_edge(UP, buff=0.35).to_edge(RIGHT, buff=0.4),
                  run_time=0.7)
        row = tiles(PINE).move_to(UP * 1.7)
        ph = TB("Pine Hill", 34).next_to(row, UP, buff=0.35).align_to(row, LEFT)
        self.play(FadeIn(ph), LaggedStart(*[FadeIn(t, shift=DOWN * 0.5) for t in row], lag_ratio=0.08), run_time=1.0)
        # ── s031 running total ──
        self.at("s031", 0.0)
        tot_lab = T("running total", 28, MUTED).move_to(DOWN * 0.1)
        tr = ValueTracker(0)
        tot = always_redraw(lambda: TB(f"{int(round(tr.get_value()))}", 96, WARN).next_to(tot_lab, DOWN, buff=0.25))
        self.add(tot); self.play(FadeIn(tot_lab), run_time=0.3)
        seg = SEGS["s031"]; span = seg["end"] - seg["start"] - 0.6
        run = 0
        for i, t in enumerate(row):
            self.until(seg["start"] + 0.3 + span * i / 9)
            c = t.copy()
            run += t.value
            self.play(c.animate.scale(0.5).move_to(tot.get_center()).set_opacity(0), tr.animate.set_value(run),
                      t.animate.set_opacity(0.35), run_time=min(0.5, span / 9 - 0.03))
            self.remove(c)
        tot.clear_updaters()
        # ── s032 540 bounce ──
        self.at("s032", 0.5)
        self.play(tot.animate.scale(1.2), rate_func=there_and_back, run_time=0.6)
        # ── s033 divide by nine ──
        self.at("s033", 0.0)
        cnt = VGroup(*[Dot(radius=0.06, color=INK) for _ in range(9)]).arrange(RIGHT, buff=0.12).next_to(row, DOWN, buff=0.25)
        nlab = T("9 households", 26, INK2).next_to(cnt, RIGHT, buff=0.25)
        self.play(row.animate.set_opacity(1), LaggedStart(*[GrowFromCenter(d) for d in cnt], lag_ratio=0.08),
                  FadeIn(nlab), run_time=0.9)
        f = frac(540, 9, INK, 96).move_to(tot.get_center() + LEFT * 1.0)
        self.play(FadeOut(tot_lab), ReplacementTransform(tot, f[0][0:3]), FadeIn(f[0][3:], shift=UP * 0.2), run_time=0.9)
        # ── s034 = 60 ──
        self.at("s034", 1.2)
        eq60 = glow(TB("= 60", 96, WARN), WARN).next_to(f, RIGHT, buff=0.4)
        self.play(FadeIn(eq60, shift=LEFT * 0.3), run_time=0.6)
        self.play(Circumscribe(eq60, color=WARN), run_time=0.9)
        # ── s035 formula ──
        self.at("s035", 0.0)
        self.play(FadeOut(VGroup(f, eq60, cnt, nlab, steps)), row.animate.scale(0.8).move_to(UP * 2.55), ph.animate.set_opacity(0),
                  run_time=0.7)
        F = MathTex(r"\bar{x}", "=", r"{\sum", r"x_i", r"\over", r"n}", font_size=108, color=MUTED).move_to(UP * 0.25)
        self.play(Write(F), run_time=1.4)
        self.at("s035", 3.0)
        dec = T("decode it, one symbol at a time", 30, MUTED).next_to(F, DOWN, buff=0.5)
        self.play(FadeIn(dec, shift=UP * 0.2), run_time=0.6)
        # ── s036 x ──
        self.at("s036", 0.0)
        self.play(FadeOut(dec), F[3].animate.set_color(BLUE_).scale(1.15), run_time=0.6)
        t42 = row[5]
        arr = Arrow([F[3].get_x(), F.get_top()[1] + 0.08, 0], t42.get_bottom() + DOWN * 0.05, color=BLUE_, buff=0.05, stroke_width=4)
        self.play(GrowArrow(arr), Indicate(t42, color=BLUE_), run_time=0.8)
        d1 = defcard(r"x", "one value (one household's income)", BLUE_, 26)
        defs = [d1]
        d1.move_to(DOWN * 1.5 + LEFT * 3.3)
        self.play(FadeIn(d1, shift=UP * 0.2), run_time=0.6)
        # ── s037 x1, x2, x3 … ──
        self.at("s037", 0.6)
        subs = VGroup(*[MathTex(f"x_{{{i + 1}}}", font_size=34, color=BLUE_).next_to(t, DOWN, buff=0.12) for i, t in enumerate(row)])
        self.play(FadeOut(arr), F[3].animate.scale(1 / 1.15), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.25) for s in subs], lag_ratio=0.25), run_time=3.0)
        # ── s038 sigma ──
        self.at("s038", 0.0)
        self.play(F[2].animate.set_color(WARN).scale(1.25), F[3].animate.set_color(MUTED), run_time=0.8)
        d2 = defcard(r"\Sigma", "(sigma) add them all up", WARN, 26).move_to(DOWN * 1.5 + RIGHT * 3.3)
        self.at("s038", 3.0)
        self.play(FadeIn(d2, shift=UP * 0.2), F[2].animate.scale(1 / 1.25), run_time=0.6)
        self.play(Indicate(d2, color=WARN, scale_factor=1.05), run_time=0.8)
        # ── s039 n ──
        self.at("s039", 0.0)
        self.play(F[2].animate.set_color(MUTED), F[5].animate.set_color(AQUA).scale(1.2), run_time=0.6)
        d3 = defcard(r"n", "how many values  (n = 9)", AQUA, 26).move_to(DOWN * 2.28 + LEFT * 3.3)
        self.play(FadeIn(d3, shift=UP * 0.2), F[5].animate.scale(1 / 1.2), run_time=0.6)
        # ── s040 x bar ──
        self.at("s040", 0.0)
        self.play(F[5].animate.set_color(MUTED), F[0].animate.set_color(VIOLET).scale(1.2), run_time=0.6)
        d4 = defcard(r"\bar{x}", "(x-bar) the mean", VIOLET, 26).move_to(DOWN * 2.28 + RIGHT * 3.3)
        self.play(FadeIn(d4, shift=UP * 0.2), F[0].animate.scale(1 / 1.2), run_time=0.6)
        # ── s041 plain English ──
        self.at("s041", 0.0)
        self.play(F[0].animate.set_color(VIOLET), F[2].animate.set_color(WARN), F[3].animate.set_color(BLUE_),
                  F[5].animate.set_color(AQUA), F[1].animate.set_color(INK), F[4].animate.set_color(INK), run_time=0.6)
        eng = T("mean  =  (add up every value)  ÷  (how many)", 34, INK).next_to(F, DOWN, buff=0.35)
        self.play(FadeOut(VGroup(d1, d2, d3, d4)), FadeIn(eng, shift=UP * 0.2), run_time=0.8)
        self.play(Circumscribe(VGroup(F, eng), color=WARN, buff=0.2), run_time=1.2)
        # ── s042 two pictures preview ──
        self.at("s042", 0.0)
        self.play(FadeOut(VGroup(F, eng, row, subs)), run_time=0.6)
        tank = VGroup(Rectangle(width=1.6, height=2.0).set_stroke(INK2, 4),
                      Rectangle(width=1.6, height=1.1, stroke_width=0, fill_color=AQUA, fill_opacity=0.8))
        tank[1].align_to(tank[0], DOWN)
        beam = VGroup(Line(LEFT * 1.6, RIGHT * 1.6, stroke_width=8, color=INK2),
                      Triangle(color=WARN, fill_opacity=1).scale(0.3).shift(DOWN * 0.3),
                      Square(0.4, color=BLUE_, fill_opacity=1).shift(LEFT * 1.1 + UP * 0.24),
                      Square(0.4, color=ORANGE_, fill_opacity=1).shift(RIGHT * 1.1 + UP * 0.24))
        p1 = VGroup(tank, T("① fair shares", 32, AQUA)).arrange(DOWN, buff=0.4).move_to(LEFT * 3.2 + UP * 0.4)
        p2 = VGroup(beam, T("② balance beam", 32, WARN)).arrange(DOWN, buff=0.75).move_to(RIGHT * 3.2 + UP * 0.4)
        p2[1].align_to(p1[1], DOWN)
        self.play(FadeIn(p1, shift=RIGHT * 0.4), run_time=0.6)
        self.play(FadeIn(p2, shift=LEFT * 0.4), run_time=0.6)

        # ════════ Picture 1: fair shares (bar chart) ════════
        self.at("s043", 0.0)
        A = xy_axes([0, 9, 1], [0, 240, 40], 7.6, 4.0, "Household", "Income (thousand $)",
                    x_labels={i: str(i) for i in range(1, 10)})
        A.move_to(LEFT * 1.6 + UP * 0.3)
        ax = A.ax
        self.play(FadeOut(p2), p1.animate.scale(0.5).to_corner(UR, buff=0.5).shift(DOWN * 0.3), run_time=0.6)
        self.play(Create(ax), FadeIn(A.labs), FadeIn(A.xt), FadeIn(A.yt), run_time=1.0)
        # ── s044 bars ──
        self.at("s044", 0.0)
        bw = 0.55
        def bar(i, h, color):
            b = Rectangle(width=bw, height=max(ax.c2p(0, h)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                          fill_color=color, fill_opacity=0.9)
            b.move_to(ax.c2p(i + 1, 0), aligned_edge=DOWN)
            return b
        bars = VGroup(*[bar(i, v, BLUE_ if v < 100 else ORANGE_) for i, v in enumerate(PINE)])
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=1.3)
        vl = VGroup(*[T(str(v), 20, INK2).next_to(b, UP, buff=0.08) for v, b in zip(PINE, bars)])
        self.play(FadeIn(vl), run_time=0.4)
        # ── s045 pour into pot ──
        self.at("s045", 0.0)
        tankR = Rectangle(width=1.5, height=3.2).set_stroke(INK2, 4).move_to(RIGHT * 4.9 + DOWN * 0.2)
        pot_lab = T("shared pot", 26, AQUA).next_to(tankR, UP, buff=0.15)
        self.play(FadeOut(p1), Create(tankR), FadeIn(pot_lab), FadeOut(vl), bars.animate.set_fill(AQUA), run_time=0.8)
        lvl = ValueTracker(0)
        water = always_redraw(lambda: Rectangle(width=1.5 - 0.08, height=max(lvl.get_value() * 3.1 / 540, 0.001), stroke_width=0,
                                                fill_color=AQUA, fill_opacity=0.85).align_to(tankR, DOWN).shift(UP * 0.04)
                              .set_x(tankR.get_x()).set(qa_container=True))
        wl = always_redraw(lambda: T(f"{int(lvl.get_value())}", 34, INK, weight=BOLD).move_to(tankR.get_center() + UP * 0.6))
        self.add(water, wl)
        self.play(*[b.animate.stretch_to_fit_height(0.001, about_edge=DOWN) for b in bars], lvl.animate.set_value(540),
                  run_time=2.2, rate_func=smooth)
        # ── s046 shared out equally ──
        self.at("s046", 0.0)
        eq_bars = VGroup(*[bar(i, 60, AQUA) for i in range(9)])
        self.play(lvl.animate.set_value(0), *[Transform(b, e) for b, e in zip(bars, eq_bars)], run_time=2.4, rate_func=smooth)
        water.clear_updaters(); wl.clear_updaters()
        # ── s047 level at 60 ──
        self.at("s047", 0.0)
        line60 = DashedLine(ax.c2p(0, 60), ax.c2p(9.3, 60), color=WARN, stroke_width=4)
        l60 = glow(T("mean = 60", 32, WARN, weight=BOLD), WARN).next_to(ax.c2p(9.3, 60), RIGHT, buff=0.15)
        self.play(Create(line60), FadeOut(VGroup(water, wl, tankR, pot_lab)), run_time=0.7)
        self.play(FadeIn(l60, shift=LEFT * 0.2), Flash(ax.c2p(5, 60), color=WARN), run_time=0.7)
        # ── s048 the question ──
        self.at("s048", 0.0)
        qcard = chip("Shared out evenly, how much would each get?", INK, 30).move_to(UP * 2.78 + RIGHT * 0.6)
        self.play(FadeIn(qcard, shift=DOWN * 0.3), A.yt.animate.set_opacity(0), run_time=0.7)
        self.play(LaggedStart(*[Indicate(b, color=AQUA, scale_factor=1.06) for b in bars], lag_ratio=0.06), run_time=1.4)

        # ════════ Picture 2: balance beam ════════
        self.at("s049", 0.0)
        self.play(FadeOut(VGroup(A, bars, line60, l60, qcard)), run_time=0.6)
        base_ax = money_axis(length=12.0); base_ax.shift(DOWN * 1.35 - base_ax.axis.get_center())
        L = NumberLine(x_range=[0, 240, 20], length=12.0, color=INK2, stroke_width=3, include_tip=False, tick_size=0.09)
        L.move_to([base_ax.axis.get_x(), 0.0, 0])
        beam_bar = Rectangle(width=12.3, height=0.12, stroke_width=0, fill_color="#55554f", fill_opacity=1).move_to(L)
        beam_bar.qa_ignore = True
        btitle = VGroup()
        piv_tr = ValueTracker(60.0)
        blocks = VGroup()
        placed = []
        for v in PINE:
            x = L.n2p(v)[0]; lvl_ = 0
            while any(abs(x - px) < 0.2 and pl == lvl_ for px, pl in placed): lvl_ += 1
            placed.append((x, lvl_))
            blocks.add(block(BLUE_ if v < 100 else ORANGE_).move_to(L.n2p(v) + UP * (0.17 + lvl_ * 0.21)))
        base = VGroup(beam_bar, L)
        def torque(p):
            return sum(v - p for v in PINE)
        def angle(p):
            return -0.11 * np.tanh(torque(p) / 160)
        def pivot_pt(p):
            return L.n2p(p) + DOWN * 0.08
        self.play(FadeIn(base), FadeIn(base_ax), run_time=0.8)
        piv = Triangle(color=WARN, fill_opacity=1, stroke_width=0).scale(0.32)
        piv.move_to(pivot_pt(60), aligned_edge=UP)
        self.play(FadeIn(piv, shift=UP * 0.3), run_time=0.5)
        # ── s050 weights drop ──
        self.at("s050", 0.2)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 1.2) for b in blocks], lag_ratio=0.12), run_time=1.6,
                  rate_func=rate_functions.ease_in_quad)
        eqw = T("each household = one equal weight", 26, INK2).move_to(UP * 2.4)
        self.play(FadeIn(eqw), run_time=0.5)
        # dynamic beam: rotate (base + blocks) about the pivot by the torque angle
        beam_static = VGroup(base, blocks)
        self.drop(base, blocks)
        ang = ValueTracker(0.0)
        dyn = always_redraw(lambda: beam_static.copy().rotate(ang.get_value(), about_point=pivot_pt(piv_tr.get_value())))
        pivm = always_redraw(lambda: piv.copy().move_to(pivot_pt(piv_tr.get_value()), aligned_edge=UP))
        self.add(dyn); self.remove(piv); self.add(pivm)
        def slide(p, rt):
            self.play(piv_tr.animate.set_value(p), ang.animate.set_value(angle(p)), run_time=rt)
        # ── s051 where does the support go ──
        self.at("s051", 0.0)
        qm = TB("?", 56, WARN).move_to(UP * 1.6)
        self.play(FadeOut(eqw), FadeIn(qm), run_time=0.4)
        slide(110, 1.2)
        slide(20, 1.3)
        # ── s052 try 40 ──
        self.at("s052", 0.0)
        slide(40, 1.0)
        tip = T("tips right", 30, RED_).move_to(UP * 1.6 + RIGHT * 3.2)
        p40 = T("support at 40", 28, WARN).move_to(UP * 1.6 + LEFT * 3.4)
        self.play(FadeOut(qm), FadeIn(tip, shift=DOWN * 0.2), FadeIn(p40), run_time=0.6)
        # ── s053 try 60: level ──
        self.at("s053", 0.0)
        p60 = T("support at 60", 28, WARN).move_to(p40)
        self.play(piv_tr.animate.set_value(60), ang.animate.set_value(0), Transform(p40, p60), FadeOut(tip), run_time=1.2)
        lev = glow(T("balanced: mean = 60", 34, WARN, weight=BOLD), WARN).move_to(UP * 2.3)
        self.play(FadeIn(lev, scale=0.8), run_time=0.6)
        dyn.clear_updaters(); pivm.clear_updaters()
        # ── s054 measure distances (deviation ladder) ──
        self.at("s054", 0.0)
        self.play(FadeOut(lev), FadeOut(p40), run_time=0.4)
        self.play(fr.animate.scale(0.42).move_to(L.n2p(42) + UP * 1.25), run_time=1.2)
        arrows, labs = VGroup(), VGroup()
        for i, v in enumerate(PINE[:8]):
            y = 0.62 + i * 0.21
            a = Arrow(L.n2p(60) + UP * y, L.n2p(v) + UP * y, buff=0, color=BLUE_, stroke_width=3,
                      max_tip_length_to_length_ratio=0.12, tip_length=0.08)
            lb = T(f"−{60 - v}", 15, BLUE_).next_to(a, LEFT, buff=0.05)
            arrows.add(a); labs.add(lb)
        vline = DashedLine(L.n2p(60) + UP * 0.1, L.n2p(60) + UP * 2.3, color=WARN, stroke_width=2)
        self.play(Create(vline), run_time=0.5)
        # ── s055 eight arrows, labels one by one ──
        self.at("s055", 0.0)
        k0 = word_index("s055", "thirty")
        names = ["thirty", "twenty-eight", "twenty-five", "twenty-two", "twenty", "eighteen", "fifteen", "twelve"]
        ws = [x.strip(",.").lower() for x in SEGS["s055"]["text"].split()]
        idx = [ws.index(n) for n in names]
        for a, lb, k in zip(arrows, labs, idx):
            self.until(word_time("s055", k) - 0.05)
            self.play(GrowArrow(a), FadeIn(lb), run_time=0.3)
        # ── s056 total −170 ──
        self.at("s056", 0.0)
        m170 = TB("−170", 40, BLUE_).move_to(L.n2p(12) + UP * 1.4)
        self.play(ReplacementTransform(labs, m170), run_time=1.0)
        # ── s057 +170 ──
        self.at("s057", 0.0)
        self.play(fr.animate.scale(1 / 0.42).move_to(UP * 0.25), m170.animate.scale(1.6), run_time=1.2)
        big = Arrow(L.n2p(60) + UP * 2.2, L.n2p(230) + UP * 2.2, buff=0, color=ORANGE_, stroke_width=6)
        p170 = TB("+170", 64, ORANGE_).next_to(big, UP, buff=0.12)
        self.play(GrowArrow(big), FadeIn(p170, shift=LEFT * 0.3), run_time=1.0)
        # ── s058 cancel ──
        self.at("s058", 0.0)
        eq0 = VGroup(TB("−170", 64, BLUE_), TB("+", 64, INK), TB("170", 64, ORANGE_), TB("=", 64, INK),
                     glow(TB("0", 72, WARN), WARN)).arrange(RIGHT, buff=0.3).move_to(UP * 2.6)
        self.play(FadeOut(VGroup(arrows, vline, big)),
                  ReplacementTransform(m170, eq0[0]), ReplacementTransform(p170, VGroup(eq0[1], eq0[2])), run_time=1.0)
        self.play(FadeIn(eq0[3:]), run_time=0.6)
        self.play(Circumscribe(eq0, color=WARN), run_time=1.0)
        # ── s059 one vs eight ──
        self.at("s059", 0.0)
        self.play(FadeOut(eq0), run_time=0.4)
        blk = dyn[1]
        g8 = SurroundingRectangle(blk[:8], color=BLUE_, buff=0.12, corner_radius=0.08)
        g1 = SurroundingRectangle(blk[8], color=ORANGE_, buff=0.12, corner_radius=0.08)
        t8 = T("8 families", 30, BLUE_).next_to(g8, UP, buff=0.2)
        t1 = T("1 family", 30, ORANGE_).next_to(g1, UP, buff=0.2)
        vs_ = T("balances", 30, INK).move_to((t8.get_center() + t1.get_center()) / 2)
        self.play(Create(g8), FadeIn(t8), run_time=0.7)
        self.play(Create(g1), FadeIn(t1), run_time=0.7)
        self.play(FadeIn(vs_, scale=0.7), run_time=0.5)
        # ── s060 far values pull harder ──
        self.at("s060", 0.0)
        self.play(FadeOut(VGroup(g8, g1, t8, t1, vs_)), run_time=0.4)
        mk = marker(L, 60, WARN, "mean", height=1.3)
        self.play(FadeIn(mk, shift=DOWN * 0.2), run_time=0.5)
        rope = Line(blk[8].get_top() + UP * 0.05, mk.tri.get_right() + RIGHT * 0.05, color=ORANGE_, stroke_width=4)
        self.play(Create(rope), run_time=0.7)
        pull = T("the farther away, the harder it pulls", 32, RED_).move_to(UP * 2.4)
        self.play(FadeIn(pull, shift=UP * 0.2), Wiggle(mk, scale_value=1.15, rotation_angle=0.0), run_time=1.0)
        self.finish()
