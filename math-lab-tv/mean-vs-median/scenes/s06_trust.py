import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def signpost(text, color):
    post = Line(DOWN * 0.9, UP * 0.4, color=INK2, stroke_width=5)
    t = T(text, 30, color, weight=BOLD)
    board = RoundedRectangle(corner_radius=0.1, width=t.width + 0.6, height=0.8, stroke_color=color, stroke_width=3,
                             fill_color="#22221f", fill_opacity=1).move_to(UP * 0.6)
    board.qa_container = True
    t.move_to(board)
    return VGroup(post, board, t)


def town_hall():
    base = Rectangle(width=1.6, height=0.9)
    roof = Polygon(base.get_corner(UL) + LEFT * 0.15, base.get_corner(UR) + RIGHT * 0.15, base.get_top() + UP * 0.6)
    cols = VGroup(*[Line(base.get_bottom() + RIGHT * x, base.get_top() + RIGHT * x) for x in (-0.5, -0.17, 0.17, 0.5)])
    return VGroup(base, roof, cols).set_stroke(INK, 3)


class S06Trust(Base):
    CHAPTER = "Which One to Trust"

    def construct(self):
        # ── s104 the fork ──
        self.at("s104", 0.0)
        stem = Line(DOWN * 2.2, DOWN * 0.6, color=GRID, stroke_width=26)
        lft = Line(DOWN * 0.6, LEFT * 3.4 + UP * 0.7, color=GRID, stroke_width=26)
        rgt = Line(DOWN * 0.6, RIGHT * 3.4 + UP * 0.7, color=GRID, stroke_width=26)
        for m in (stem, lft, rgt): m.qa_ignore = True
        q = chip("which average?", INK, 32).move_to(DOWN * 1.5 + RIGHT * 2.6)
        self.play(Create(stem), run_time=0.5)
        self.play(Create(lft), Create(rgt), FadeIn(q), run_time=0.8)
        sL = signpost("TOTALS → mean", WARN).move_to(LEFT * 3.6 + UP * 1.6)
        sR = signpost("TYPICAL → median", VIOLET).move_to(RIGHT * 3.6 + UP * 1.6)
        sL[1:].set_opacity(0.25); sR[1:].set_opacity(0.25)
        self.play(FadeIn(sL), FadeIn(sR), run_time=0.6)
        # ── s105 totals → mean ──
        self.at("s105", 0.0)
        self.play(sL[1:].animate.set_opacity(1), sL.animate.scale(1.1), lft.animate.set_color("#5a4a20"), run_time=0.7)
        # ── s106 council + tax ──
        self.at("s106", 0.0)
        road = VGroup(stem, lft, rgt, q, sR)
        self.play(FadeOut(road), FadeOut(sL[0]), run_time=0.3)
        sL.remove(sL[0])
        self.play(sL.animate.scale(0.6).to_corner(UR, buff=0.4), run_time=0.5)
        hall = town_hall().move_to(LEFT * 4.6 + UP * 1.2)
        hl_ = T("Pine Hill council", 26, INK2).next_to(hall, DOWN, buff=0.2)
        tax = chip("2% income tax", AQUA, 32).next_to(hall, RIGHT, buff=0.6)
        self.play(Create(hall), FadeIn(hl_), run_time=0.8)
        self.play(GrowFromCenter(tax), run_time=0.5)
        # ── s107 60 × 9 = 540 ──
        self.at("s107", 0.0)
        row = tiles([60] * 9, colors=[WARN] * 9, size=0.7, fs=26).move_to(DOWN * 0.6)
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.3) for t in row], lag_ratio=0.06), run_time=0.9)
        eq = VGroup(TB("60", 56, WARN), TB("×", 56, INK), TB("9", 56, INK), TB("=", 56, INK), TB("540", 56, AQUA)).arrange(RIGHT, buff=0.3)
        eq.move_to(DOWN * 1.75)
        self.until(word_time("s107", word_index("s107", "sixty")))
        self.play(FadeIn(eq[:3]), run_time=0.5)
        big = tile(540, AQUA, size=0.9, fs=36).move_to(row)
        self.play(ReplacementTransform(row, big), FadeIn(eq[3:]), run_time=0.9)
        thou = T("thousand $ in total", 26, AQUA).next_to(big, RIGHT, buff=0.3)
        self.play(FadeIn(thou), run_time=0.4)
        # ── s108 2% → $10,800 ──
        self.at("s108", 0.0)
        coins = VGroup()
        for i in range(10):
            c = Ellipse(width=1.1, height=0.32, color=WARN, fill_color="#3a3018", fill_opacity=1, stroke_width=3)
            c.move_to(RIGHT * 4.9 + DOWN * 1.9 + UP * i * 0.17); coins.add(c)
        ctr = ValueTracker(0)
        ct = always_redraw(lambda: TB(f"${ctr.get_value():,.0f}", 48, WARN).next_to(coins, UP, buff=0.25))
        self.add(ct)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.4) for c in coins], lag_ratio=0.12), ctr.animate.set_value(10800),
                  run_time=1.6)
        ct.clear_updaters()
        pyr = T("per year", 24, INK2).next_to(ct, UP, buff=0.1)
        self.play(FadeIn(pyr), run_time=0.3)
        # ── s109 pie: rich family pays 43% ──
        self.at("s109", 0.0)
        self.play(FadeOut(VGroup(hall, hl_, tax, big, eq, thou, coins, pyr)), ct.animate.move_to(UP * 2.3 + LEFT * 3.0), run_time=0.7)
        share = 4600 / 10800
        R = 1.5
        c0 = DOWN * 0.15 + LEFT * 3.0
        rich = Sector(radius=R, angle=share * TAU, start_angle=PI / 2, fill_color=ORANGE_, fill_opacity=0.95, stroke_color=BG,
                      stroke_width=3).shift(c0)
        rest = Sector(radius=R, angle=(1 - share) * TAU, start_angle=PI / 2 + share * TAU, fill_color=BLUE_, fill_opacity=0.85,
                      stroke_color=BG, stroke_width=3).shift(c0)
        self.play(FadeIn(rest), run_time=0.5)
        self.play(FadeIn(rich, scale=1.15), run_time=0.6)
        lr = VGroup(T("richest family: $4,600", 30, ORANGE_, weight=BOLD), T("43% of the total", 28, ORANGE_)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lb = VGroup(T("other 8 families: $6,200", 30, BLUE_, weight=BOLD), T("57%", 28, BLUE_)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lr.move_to(RIGHT * 2.2 + UP * 0.75, aligned_edge=LEFT); lb.move_to(RIGHT * 2.2 + DOWN * 0.75, aligned_edge=LEFT)
        lr.align_to(LEFT * 0.5, LEFT); lb.align_to(LEFT * 0.5, LEFT)
        self.play(FadeIn(lr, shift=LEFT * 0.3), FadeIn(lb, shift=LEFT * 0.3), run_time=0.7)
        need = T("the council needs that outlier counted", 30, INK).move_to(DOWN * 2.2 + RIGHT * 1.6)
        self.until(word_time("s109", word_index("s109", "council")))
        self.play(FadeIn(need), run_time=0.5)
        # ── s110 median can't do totals ──
        self.at("s110", 0.0)
        self.play(FadeOut(VGroup(rich, rest, lr, lb, need, ct)), run_time=0.5)
        A = xy_axes([0, 3, 1], [0, 600, 100], 6.4, 4.0, "", "Total income (thousand $)", x_labels={})
        A.move_to(LEFT * 2.2 + UP * 0.3)
        ax = A.ax
        bw = 1.1
        b1 = Rectangle(width=bw, height=ax.c2p(0, 540)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=WARN, fill_opacity=0.9)
        b1.move_to(ax.c2p(1, 0), aligned_edge=DOWN)
        b2 = Rectangle(width=bw, height=ax.c2p(0, 360)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=VIOLET, fill_opacity=0.9)
        b2.move_to(ax.c2p(2, 0), aligned_edge=DOWN)
        l1 = T("mean × 9", 24, WARN).next_to(ax.c2p(1, 0), DOWN, buff=0.15)
        l2 = T("median × 9", 24, VIOLET).next_to(ax.c2p(2, 0), DOWN, buff=0.15)
        v1 = T("540", 28, WARN, weight=BOLD).next_to(b1, UP, buff=0.1)
        v2 = T("360", 28, VIOLET, weight=BOLD).next_to(b2, UP, buff=0.1)
        self.play(Create(ax), FadeIn(A.labs), FadeIn(A.yt), run_time=0.7)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), FadeIn(v1), run_time=0.6)
        self.until(word_time("s110", word_index("s110", "forty")))
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), FadeIn(v2), run_time=0.6)
        gap = DashedLine(ax.c2p(2.4, 360), ax.c2p(2.4, 540), color=RED_, stroke_width=4)
        top = DashedLine(ax.c2p(1.45, 540), ax.c2p(2.5, 540), color=RED_, stroke_width=2)
        gl = VGroup(T("180 missing", 30, RED_, weight=BOLD), T("= one third", 28, RED_)).arrange(DOWN, buff=0.1)
        gl.next_to(ax.c2p(2.5, 450), RIGHT, buff=0.25)
        self.until(word_time("s110", word_index("s110", "misses")))
        self.play(Create(top), Create(gap), FadeIn(gl, shift=LEFT * 0.2), run_time=0.8)
        # ── s111 typical → median ──
        self.at("s111", 0.0)
        self.play(FadeOut(VGroup(A, b1, b2, l1, l2, v1, v2, gap, top, gl)), run_time=0.5)
        sR2 = signpost("TYPICAL → median", VIOLET).move_to(UP * 1.0)
        self.play(FadeIn(sR2, shift=UP * 0.3), sL.animate.set_opacity(0.4), run_time=0.7)
        # ── s112 your neighbours ──
        self.at("s112", 0.0)
        self.play(FadeOut(sR2[0]), run_time=0.2)
        sR2.remove(sR2[0])
        self.play(sR2.animate.scale(0.6).next_to(sL, LEFT, buff=0.4).align_to(sL, DOWN), run_time=0.5)
        axp = money_axis(); axp.shift(DOWN * 0.6 - axp.axis.get_center()); L = axp.axis
        dots = dot_plot(PINE, L, [BLUE_] * 8 + [ORANGE_])
        self.play(FadeIn(axp), FadeIn(dots), run_time=0.6)
        fr = self.camera.frame
        self.play(fr.animate.scale(0.55).move_to([L.n2p(48)[0], -0.1, 0]), run_time=0.9)
        g40 = diamond(L, 40, VIOLET, "guess 40", height=1.45, fs=20, label_dir=LEFT)
        g60 = marker(L, 60, WARN, "guess 60", height=1.45, fs=20, label_dir=RIGHT)
        self.play(FadeIn(g40), FadeIn(g60), run_time=0.5)
        near = VGroup(*[Line(g40.tri.get_bottom(), d.get_top(), color=VIOLET, stroke_width=1.5) for d in dots[:8]])
        far = VGroup(*[Line(g60.tri.get_bottom(), d.get_top(), color=WARN, stroke_width=1.5) for d in dots[:8]])
        self.play(Create(near), run_time=0.6)
        self.play(Create(far), run_time=0.6)
        bt = T("40 is closer to the typical neighbour", 24, VIOLET).move_to([L.n2p(56)[0], 1.45, 0])
        self.play(FadeIn(bt), run_time=0.5)
        # ── s113 other averages ──
        self.at("s113", 0.0)
        self.play(FadeOut(VGroup(axp, dots, g40, g60, near, far, bt)), fr.animate.scale(1 / 0.55).move_to(ORIGIN), run_time=0.8)
        cards = VGroup(chip("mean", WARN, 40), chip("median", VIOLET, 40), chip("+ others", AQUA, 40)).arrange(RIGHT, buff=0.6)
        cards.move_to(UP * 0.8)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards], lag_ratio=0.25), run_time=0.9)
        # ── s114 mode ──
        self.at("s114", 0.0)
        mode = chip("mode = the most common value", AQUA, 32).move_to(UP * 2.3)
        self.play(FadeOut(cards), FadeIn(mode, shift=DOWN * 0.2), run_time=0.6)
        row = tiles(PINE).move_to(UP * 0.6)
        self.play(FadeIn(row, lag_ratio=0.05), run_time=0.6)
        self.until(word_time("s114", word_index("s114", "no")))
        scan = SurroundingRectangle(row[0], color=AQUA, buff=0.06)
        self.play(Create(scan), run_time=0.2)
        for t in row[1:]:
            self.play(scan.animate.move_to(t).match_width(SurroundingRectangle(t, buff=0.06)), run_time=0.14)
        nm = T("no repeats → no mode", 34, RED_).next_to(row, DOWN, buff=0.45)
        self.play(FadeOut(scan), FadeIn(nm), run_time=0.5)
        # ── s115 trimmed mean ──
        self.at("s115", 0.0)
        tm = chip("trimmed mean: cut the extremes, average the rest", AQUA, 30).move_to(UP * 2.3)
        self.play(FadeOut(nm), Transform(mode, tm), run_time=0.6)
        self.until(word_time("s115", word_index("s115", "drop")))
        cut1 = DashedLine(row[0].get_corner(UR) + RIGHT * 0.09 + UP * 0.25, row[0].get_corner(DR) + RIGHT * 0.09 + DOWN * 0.25, color=RED_)
        cut2 = DashedLine(row[8].get_corner(UL) + LEFT * 0.09 + UP * 0.25, row[8].get_corner(DL) + LEFT * 0.09 + DOWN * 0.25, color=RED_)
        self.play(Create(cut1), Create(cut2), run_time=0.5)
        self.play(row[0].animate.shift(DOWN * 1.0).set_opacity(0.25), row[8].animate.shift(DOWN * 1.0).set_opacity(0.25), run_time=0.7)
        # ── s116 280 / 7 = 40 ──
        self.at("s116", 0.0)
        f = MathTex(r"{280 \over 7}", font_size=80, color=INK).move_to(DOWN * 1.45 + LEFT * 3.4)
        self.play(FadeOut(VGroup(cut1, cut2, row[0], row[8])), FadeIn(f, shift=UP * 0.2), run_time=0.7)
        self.until(word_time("s116", word_index("s116", "forty")) - 0.2)
        e = glow(TB("= 40", 72, AQUA), AQUA).next_to(f, RIGHT, buff=0.35)
        self.play(FadeIn(e, shift=LEFT * 0.2), run_time=0.6)
        # ── s117 in-between ──
        self.at("s117", 0.0)
        same = T("here: same as the median (40)", 28, VIOLET).next_to(VGroup(f, e), RIGHT, buff=0.5)
        self.play(FadeIn(same), run_time=0.5)
        self.until(word_time("s117", word_index("s117", "general")))
        self.play(FadeOut(VGroup(row[1:8], f, e, same, mode)), run_time=0.5)
        track = Line(LEFT * 4.5, RIGHT * 4.5, color=INK2, stroke_width=6).move_to(UP * 0.4)
        lm = T("MEAN", 36, WARN, weight=BOLD).next_to(track, LEFT, buff=0.3)
        ld = T("MEDIAN", 36, VIOLET, weight=BOLD).next_to(track, RIGHT, buff=0.3)
        knob = Dot(radius=0.2, color=AQUA).move_to(track.get_left())
        kt = T("trimmed mean", 28, AQUA).next_to(knob, UP, buff=0.25)
        kt.add_updater(lambda m: m.next_to(knob, UP, buff=0.25))
        self.play(Create(track), FadeIn(lm), FadeIn(ld), FadeIn(knob), FadeIn(kt), run_time=0.7)
        self.play(knob.animate.move_to(track.get_center()), run_time=1.0)
        uses = T("uses most values", 26, INK2).next_to(track, DOWN, buff=0.35).shift(LEFT * 2.0)
        hij = T("one extreme can't hijack it", 26, INK2).next_to(track, DOWN, buff=0.35).shift(RIGHT * 2.2)
        self.play(FadeIn(uses), run_time=0.4)
        self.play(FadeIn(hij), run_time=0.4)
        kt.clear_updaters()
        # ── s118 report both ──
        self.at("s118", 0.0)
        self.play(FadeOut(VGroup(track, lm, ld, knob, kt, uses, hij)), run_time=0.5)
        both = VGroup(glow(TB("mean 60", 72, WARN), WARN), T("|", 72, MUTED), glow(TB("median 40", 72, VIOLET), VIOLET)).arrange(RIGHT, buff=0.5)
        both.move_to(UP * 0.8)
        self.play(FadeIn(both[0], shift=RIGHT * 0.3), FadeIn(both[1]), FadeIn(both[2], shift=LEFT * 0.3), run_time=0.8)
        br = Brace(both, DOWN, color=AQUA)
        bt2 = T("gap of 20 → the data is skewed", 32, AQUA).next_to(br, DOWN, buff=0.15)
        self.until(word_time("s118", word_index("s118", "gap")))
        self.play(GrowFromCenter(br), FadeIn(bt2), run_time=0.7)
        self.finish()
