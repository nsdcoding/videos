import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class S02Welcome(Base):
    CHAPTER = "Welcome"

    def item(self, n, color, caption):
        num = TB(str(n), 72, color).move_to(UP * 2.45 + LEFT * 0.0)
        cap = T(caption, 34, INK).move_to(DOWN * 2.0)
        return num, cap

    def construct(self):
        title = bayes_title()
        self.add(title)
        # ── s013 welcome card ──
        self.at("s013", 0.0)
        lg = logo(1.15, tagline=True).move_to(UP * 0.4)
        mark, name, tag = lg[0][0], lg[0][1], lg[1]
        self.play(FadeOut(title, scale=0.85), run_time=0.5)
        self.play(DrawBorderThenFill(mark[0]), run_time=0.6)
        self.play(Create(mark[1]), FadeIn(name, shift=LEFT * 0.3), run_time=0.8)
        self.until(word_time("s013", word_index("s013", "where")) - 0.1)
        self.play(AddTextLetterByLetter(tag), run_time=1.2)
        # ── s014 ① count people ──
        self.at("s014", 0.0)
        small = logo(0.42).to_edge(UP, buff=0.32).to_edge(RIGHT, buff=0.45)
        learn = T("TODAY YOU WILL LEARN", 24, MUTED, weight=BOLD).next_to(small, LEFT, buff=0.5)
        self.play(ReplacementTransform(lg[0], small), FadeOut(tag), FadeIn(learn), run_time=0.8)
        n1, c1 = self.item(1, AQUA, "turn a test result into a real probability")
        cell = 0.115
        axg = crowd_axes(cell, fs=16); axg.xt.set_opacity(0); axg.yt.set_opacity(0)
        axg.move_to(UP * 0.15 + LEFT * 2.4)
        cr = crowd(axg, cell, color=MUTED, opacity=0.35)
        self.play(FadeIn(n1, scale=0.5), FadeIn(axg), FadeIn(cr, lag_ratio=0.0005), FadeIn(c1), run_time=1.0)
        fp = VGroup(*[cr.cell[k] for k in FALSE_POS]); tp = VGroup(*[cr.cell[k] for k in SICK[:9]])
        self.play(fp.animate.set_fill(BLUE_, 1), tp.animate.set_fill(ORANGE_, 1), run_time=0.9)
        res = pill("9 of 108 positives are real", VIOLET, 28).next_to(axg, RIGHT, buff=0.35).shift(UP * 0.8)
        self.play(FadeIn(res, shift=LEFT * 0.3), Indicate(tp, color=ORANGE_, scale_factor=1.6), run_time=0.9)
        # ── s015 ② the formula ──
        self.at("s015", 0.0)
        n2, c2 = self.item(2, VIOLET, "the formula, symbol by symbol")
        F = MathTex(r"P(A\mid B)", "=", r"{P(B\mid A)\,P(A)", r"\over", r"P(B)}", font_size=96).move_to(UP * 0.2)
        F[0].set_color(VIOLET)
        self.play(FadeOut(VGroup(n1, axg, cr, res, c1), shift=LEFT * 1.0), FadeIn(n2, scale=0.5), run_time=0.6)
        self.play(Write(F), FadeIn(c2), run_time=1.4)
        self.play(Circumscribe(F[0], color=VIOLET, buff=0.12), run_time=1.0)
        # ── s016 ③ evidence adds up ──
        self.at("s016", 0.0)
        n3, c3 = self.item(3, ORANGE_, "how evidence adds up, test after test")
        mt = meter(10.5, fs=20, title="chance you have it").move_to(DOWN * 0.75)
        self.play(FadeOut(VGroup(n2, F, c2), shift=LEFT * 1.0), FadeIn(n3, scale=0.5), run_time=0.6)
        self.play(FadeIn(mt), FadeIn(c3), run_time=0.6)
        ptr = marker(mt.nl, 1, VIOLET, "1%", height=0.75, fs=28)
        self.play(FadeIn(ptr, shift=DOWN * 0.3), run_time=0.4)
        for v in (8.33, 45):
            lab = T(f"{round(v)}%", 28, VIOLET, weight=BOLD)
            tgt = mt.nl.n2p(v) - mt.nl.n2p(1)
            new_lab = lab.move_to(ptr.lab.get_center() + tgt)
            self.play(ptr[0].animate.shift(tgt - (ptr.tri.get_x() - mt.nl.n2p(1)[0]) * RIGHT),
                      ptr.tri.animate.move_to(mt.nl.n2p(v) + UP * 0.75), Transform(ptr.lab, lab.next_to(mt.nl.n2p(v) + UP * 0.75, UP, buff=0.27)),
                      run_time=0.8, rate_func=rate_functions.ease_out_back)
            self.wait(0.4)
        icons = VGroup(pill("spam filters", INK, 24), pill("fraud alerts", INK, 24), pill("machine learning", INK, 24)).arrange(RIGHT, buff=0.3)
        icons.move_to(UP * 1.5)
        self.until(word_time("s016", word_index("s016", "spam")) - 0.1)
        self.play(LaggedStart(*[FadeIn(i, shift=UP * 0.2) for i in icons], lag_ratio=0.35), run_time=1.4)
        self.until(SEGS["s016"]["end"] + 0.1)
        self.play(FadeOut(VGroup(small, learn, n3, mt, ptr, c3, icons)), run_time=0.4)
        self.finish()
