import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def back_card(n):
    b = card(2.6, 3.4, RED_)
    q = TB("?", 90, RED_).move_to(b)
    t = T(f"mistake {n}" if n else "bonus", 24, RED_).move_to(b.get_bottom() + UP * 0.4)
    return VGroup(b, q, t)


def head(n, text):
    return pill(f"Mistake {n}: {text}" if n else f"Bonus: {text}", RED_, 32).move_to(UP * 2.72)


def scales():
    post = Line(DOWN * 1.0, UP * 0.8).set_stroke(INK2, 5)
    base = Line(LEFT * 0.6, RIGHT * 0.6).set_stroke(INK2, 5).move_to(post.get_bottom())
    beam = Line(LEFT * 1.3, RIGHT * 1.3).set_stroke(INK2, 5).move_to(post.get_top())
    pans = VGroup()
    for sx in (-1, 1):
        a = Arc(radius=0.45, start_angle=PI + 0.4, angle=PI - 0.8).set_stroke(INK2, 4).move_to(beam.get_center() + RIGHT * 1.3 * sx + DOWN * 0.75)
        s1 = Line(beam.get_center() + RIGHT * 1.3 * sx, a.get_corner(UL)).set_stroke(MUTED, 2)
        s2 = Line(beam.get_center() + RIGHT * 1.3 * sx, a.get_corner(UR)).set_stroke(MUTED, 2)
        pans.add(VGroup(a, s1, s2))
    return VGroup(post, base, beam, pans)


class S09Mistakes(Base):
    CHAPTER = "Common Mistakes"

    def construct(self):
        # ── s108 three cards ──
        self.at("s108", 0.0)
        cards = VGroup(back_card(1), back_card(2), back_card(3)).arrange(RIGHT, buff=0.6).move_to(UP * 0.4)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.4) for c in cards], lag_ratio=0.2), run_time=1.2)
        # ── s109 mistake 1 ──
        self.at("s109", 0.0)
        h1 = head(1, "flipping the question")
        self.play(FadeOut(cards[1:], shift=DOWN * 0.3), ReplacementTransform(cards[0], h1), run_time=0.8)
        # ── s110 the two directions ──
        self.at("s110", 0.0)
        e1 = MathTex(r"P(\text{positive} \mid \text{sick})", "=", r"90\%", font_size=64)
        e1[0].set_color(AQUA); e1[2].set_color(AQUA)
        e2 = MathTex(r"P(\text{sick} \mid \text{positive})", r"\approx", r"8\%", font_size=64)
        e2[0].set_color(VIOLET); e2[2].set_color(VIOLET)
        VGroup(e1, e2).arrange(DOWN, buff=0.9, aligned_edge=LEFT).move_to(UP * 0.4)
        w1 = T("the test's hit rate", 26, AQUA).next_to(e1, RIGHT, buff=0.5)
        w2 = T("what you want to know", 26, VIOLET).next_to(e2, RIGHT, buff=0.5)
        VGroup(e1, e2, w1, w2).move_to(UP * 0.4)
        self.play(Write(e1), FadeIn(w1), run_time=1.0)
        self.until(word_time("s110", 12) - 0.1)  # second "The chance..."
        self.play(Write(e2), FadeIn(w2), run_time=1.0)
        # ── s111 swapped ──
        self.at("s111", 0.0)
        sw = CurvedArrow(e1[0].get_left() + LEFT * 0.15, e2[0].get_left() + LEFT * 0.15, angle=PI / 2, color=RED_, stroke_width=5)
        ne = MathTex(r"90\% \neq 8\%", font_size=60, color=RED_).next_to(VGroup(e1, e2), DOWN, buff=0.5)
        self.play(Create(sw), run_time=0.6)
        self.play(FadeIn(ne, scale=1.2), run_time=0.5)
        # ── s112 prosecutor's fallacy ──
        self.at("s112", 0.0)
        self.play(FadeOut(VGroup(e1, e2, w1, w2, sw, ne)), run_time=0.4)
        sc = scales().move_to(LEFT * 4.6 + UP * 0.3)
        pf = T("the prosecutor's fallacy", 38, RED_, weight=BOLD).move_to(RIGHT * 1.6 + UP * 1.6)
        self.play(Create(sc), FadeIn(pf), run_time=0.9)
        q1 = MathTex(r"P(\text{evidence} \mid \text{innocent})", font_size=46, color=AQUA)
        q2 = MathTex(r"P(\text{innocent} \mid \text{evidence})", font_size=46, color=VIOLET)
        neq = MathTex(r"\neq", font_size=60, color=RED_)
        row = VGroup(q1, neq, q2).arrange(DOWN, buff=0.3).move_to(RIGHT * 1.6 + DOWN * 0.3)
        self.until(word_time("s112", word_index("s112", "evidence")) - 0.2)
        self.play(FadeIn(q1, shift=UP * 0.2), run_time=0.6)
        self.until(word_time("s112", word_index("s112", "not")) - 0.1)
        self.play(FadeIn(neq), FadeIn(q2, shift=UP * 0.2), run_time=0.7)
        # ── s113 mistake 2 ──
        self.at("s113", 0.0)
        h2 = head(2, "ignoring the base rate")
        self.play(FadeOut(VGroup(sc, pf, q1, neq, q2)), ReplacementTransform(h1, h2), run_time=0.7)
        # ── s114 same test, symptomatic patients: 1 in 5 ──
        self.at("s114", 0.0)
        cell = 0.13
        ag = crowd_axes(cell, fs=16); ag.move_to(LEFT * 3.3 + UP * 0.2)
        gr = crowd(ag, cell, color=BLUE_, opacity=1)
        self.play(FadeIn(ag), FadeIn(gr), run_time=0.6)
        sick5 = VGroup(*[gr.cell[(c, r)] for c in range(8) for r in range(ROWS)])
        self.until(word_time("s114", word_index("s114", "five")) - 0.4)
        self.play(sick5.animate.set_fill(ORANGE_), run_time=0.8)
        tag = pill("base rate: 1 in 5  (200 of 1,000)", WARN, 26).move_to(UP * 2.0).align_to(RIGHT * 0.0, LEFT)
        self.play(FadeIn(tag), run_time=0.4)
        # ── s115 180 vs 80 ──
        self.at("s115", 0.0)
        bx = xy_axes([0, 2, 1], [0, 200, 50], 3.2, 2.8, None, "positives", x_labels={}, font_size=20)
        bx.next_to(tag, DOWN, buff=0.55).align_to(tag, LEFT).shift(RIGHT * 0.3)
        b1, b2 = bar(bx.ax, 0.55, 180, ORANGE_, width=1.0), bar(bx.ax, 1.45, 80, BLUE_, width=1.0)
        v1 = TB("180", 28, ORANGE_).next_to(b1, UP, buff=0.1); v2 = TB("80", 28, BLUE_).next_to(b2, UP, buff=0.1)
        self.play(FadeIn(bx), GrowFromEdge(b1, DOWN), FadeIn(v1), run_time=0.7)
        self.until(word_time("s115", word_index("s115", "eighty")) - 0.2)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(v2), run_time=0.6)
        f = MathTex(r"{180 \over 260}", r"\approx", r"69\%", font_size=46, color=VIOLET).next_to(bx, RIGHT, buff=0.35)
        self.until(word_time("s115", word_index("s115", "Now")) - 0.1)
        self.play(Write(f), run_time=0.7)
        # ── s116 side by side ──
        self.at("s116", 0.0)
        self.play(FadeOut(VGroup(ag, gr, tag, bx, b1, b2, v1, v2, f)), run_time=0.4)
        def side(rate, res, col):
            b = card(4.6, 2.6, col)
            t1 = T("base rate " + rate, 32, WARN, weight=BOLD).move_to(b.get_top() + DOWN * 0.6)
            t2 = TB(res, 72, VIOLET).next_to(t1, DOWN, buff=0.35)
            return VGroup(b, t1, t2)
        sA, sB = side("1 in 100", "8%", INK2), side("1 in 5", "69%", INK2)
        pair = VGroup(sA, sB).arrange(RIGHT, buff=1.0).move_to(UP * 0.3)
        st = T("same test · same positive result", 28, INK2).next_to(pair, DOWN, buff=0.4)
        self.play(FadeIn(sA, shift=RIGHT * 0.3), FadeIn(sB, shift=LEFT * 0.3), FadeIn(st), run_time=0.8)
        self.until(word_time("s116", word_index("s116", "base")) - 0.1)
        self.play(Indicate(sA[1], color=WARN), Indicate(sB[1], color=WARN), run_time=0.9)
        # ── s117 mistake 3 ──
        self.at("s117", 0.0)
        h3 = head(3, "counting the same clue twice")
        self.play(FadeOut(VGroup(sA, sB, st)), ReplacementTransform(h2, h3), run_time=0.7)
        # ── s118 one source, two stories ──
        self.at("s118", 0.0)
        src = card(2.6, 1.4, WARN).move_to(LEFT * 4.2 + UP * 0.3)
        srt = T("one source", 28, WARN, weight=BOLD).move_to(src)
        n1 = card(2.8, 1.2, INK2).move_to(RIGHT * 0.4 + UP * 1.3)
        n2 = card(2.8, 1.2, INK2).move_to(RIGHT * 0.4 + DOWN * 0.7)
        nt1 = T("news story A", 26, INK).move_to(n1); nt2 = T("news story B", 26, INK).move_to(n2)
        a1 = Arrow(src.get_right(), n1.get_left(), buff=0.15, color=WARN, stroke_width=4)
        a2 = Arrow(src.get_right(), n2.get_left(), buff=0.15, color=WARN, stroke_width=4)
        self.play(FadeIn(VGroup(src, srt)), run_time=0.5)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(VGroup(n1, nt1, n2, nt2)), run_time=0.8)
        one = VGroup(TB("= 1 clue", 46, INK), T("not 2", 30, RED_)).arrange(DOWN, buff=0.15).move_to(RIGHT * 4.6 + UP * 0.3)
        self.until(word_time("s118", word_index("s118", "really")) - 0.1)
        self.play(FadeIn(one, shift=LEFT * 0.2), run_time=0.5)
        # ── s119 too confident ──
        self.at("s119", 0.0)
        self.play(FadeOut(VGroup(src, srt, n1, n2, nt1, nt2, a1, a2, one)), run_time=0.4)
        mt = meter(11.0).move_to(DOWN * 0.8)
        self.play(FadeIn(mt), run_time=0.4)
        good = marker(mt.nl, 8.33, VIOLET, "one clue: 8%", height=0.85, fs=28)
        good.lab.shift(RIGHT * (good.lab.width / 2 - 0.3))
        bad = marker(mt.nl, 45, RED_, "counted twice: 45%  (overconfident)", height=1.5, fs=28)
        self.play(FadeIn(good), run_time=0.4)
        self.play(FadeIn(bad, shift=RIGHT * 0.5), run_time=0.7)
        # ── s120 bonus ──
        self.at("s120", 0.0)
        hb = head(0, "“the test is useless”")
        self.play(FadeOut(VGroup(mt, good, bad)), ReplacementTransform(h3, hb), run_time=0.7)
        u = T("only 8%… so the test is useless?", 36, INK2).move_to(UP * 0.5)
        self.play(FadeIn(u), run_time=0.5)
        # ── s121 positive ×8, negative almost rules out ──
        self.at("s121", 0.0)
        self.play(FadeOut(u), run_time=0.3)
        mz = meter(11.5, fs=22, title="chance you have it (zoomed in: 0–10%)", step=1, x_max=10).move_to(DOWN * 0.5)
        self.play(FadeIn(mz), run_time=0.4)
        st0 = marker(mz.nl, 1, WARN, "before: 1%", height=0.8, fs=26)
        st0.lab.shift(RIGHT * (st0.lab.width / 2 - 0.2))
        self.play(FadeIn(st0), run_time=0.4)
        up_ = marker(mz.nl, 8.33, VIOLET, "positive: 8.3%", height=1.8, fs=28)
        dn_ = marker(mz.nl, 0.11, BLUE_, "negative: 0.1%", height=1.8, fs=28)
        dn_.lab.shift(RIGHT * (dn_.lab.width / 2 - 0.2))
        self.until(word_time("s121", word_index("s121", "positive")) - 0.1)
        self.play(FadeIn(up_, shift=RIGHT * 0.4), run_time=0.6)
        self.until(word_time("s121", word_index("s121", "negative")) - 0.1)
        self.play(FadeIn(dn_, shift=LEFT * 0.4), run_time=0.6)
        clue = pill("a strong clue, not a verdict", VIOLET, 32).move_to(DOWN * 1.95)
        self.until(word_time("s121", word_index("s121", "strong")) - 0.2)
        self.play(FadeIn(clue, shift=UP * 0.2), run_time=0.5)
        self.until(SEGS["s121"]["end"] + 0.6)
        self.play(FadeOut(VGroup(mz, st0, up_, dn_, clue, hb)), run_time=0.4)
        self.finish()
