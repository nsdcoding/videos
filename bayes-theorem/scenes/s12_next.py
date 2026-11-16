import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def puzzle(s=1.0, c=AQUA):
    sq = Square(1.4 * s)
    bump_r = Circle(0.28 * s).move_to(sq.get_right())
    bump_t = Circle(0.28 * s).move_to(sq.get_top())
    return Union(sq, bump_r, bump_t, color=c, stroke_width=5, fill_color=c, fill_opacity=0.15)


class S12Next(Base):
    CHAPTER = "Next Time"

    def construct(self):
        lg = logo(1.1).move_to(UP * 1.1).scale(0.42).to_edge(UP, buff=0.32)   # carried over from the Subscribe scene
        self.add(lg)
        # ── s132 puzzle ──
        self.at("s132", 0.0)
        pz = puzzle().move_to(UP * 0.4)
        pt = T("a puzzle for next time", 34, AQUA).next_to(pz, DOWN, buff=0.4)
        self.play(DrawBorderThenFill(pz), FadeIn(pt), run_time=1.0)
        # ── s133 p-value described as "chance it's a fluke" ──
        self.at("s133", 0.0)
        self.play(FadeOut(VGroup(pz, pt)), run_time=0.4)
        pc = card(3.6, 1.8, INK2).move_to(LEFT * 3.2 + UP * 0.2)
        pv = MathTex(r"p = 0.03", font_size=72, color=INK).move_to(pc)
        self.play(FadeIn(pc), Write(pv), run_time=0.8)
        bt = T("“a 3% chance it's a fluke?”", 30, WARN)
        bub = card(bt.width + 0.9, 1.4, WARN).move_to(RIGHT * 2.6 + UP * 0.9)
        bt.move_to(bub)
        tail = Polygon(bub.get_corner(DL) + RIGHT * 0.5, bub.get_corner(DL) + RIGHT * 1.1, pc.get_right() + RIGHT * 0.15,
                       stroke_color=WARN, stroke_width=3, fill_color="#22221f", fill_opacity=1)
        tail.qa_container = True
        self.until(word_time("s133", word_index("s133", "described")) - 0.2)
        self.play(FadeIn(tail), FadeIn(bub), FadeIn(bt), run_time=0.7)
        qm = TB("?", 80, RED_).next_to(bub, DOWN, buff=0.35)
        self.play(FadeIn(qm, shift=DOWN * 0.3), run_time=0.5)
        # ── s134 flips the question ──
        self.at("s134", 0.0)
        self.play(FadeOut(VGroup(pc, pv, bub, bt, tail, qm)), run_time=0.4)
        a = MathTex(r"P(\text{data this extreme} \mid \text{no effect})", font_size=50, color=AQUA)
        b = MathTex(r"P(\text{no effect} \mid \text{data})", font_size=50, color=VIOLET)
        ne = MathTex(r"\neq", font_size=60, color=RED_)
        grp = VGroup(a, ne, b).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        la = T("what a p-value measures", 24, AQUA).next_to(a, DOWN, buff=0.12)
        grp = VGroup(a, la, ne, b).arrange(DOWN, buff=0.25).move_to(UP * 0.2)
        self.play(FadeIn(a), FadeIn(la), run_time=0.6)
        self.play(FadeIn(ne), FadeIn(b), run_time=0.6)
        sw = T("same flip as mistake one", 26, RED_).next_to(grp, RIGHT, buff=0.4)
        sw.set_x(min(sw.get_x(), 7.11 - 0.45 - sw.width / 2))
        # ── s135 next: p-values ──
        self.at("s135", 0.0)
        nx = chip("next:  p-values", AQUA, 30).next_to(lg, DOWN, buff=0.3)
        nx[0].qa_container = True
        self.play(FadeIn(nx, shift=DOWN * 0.2), run_time=0.6)
        self.until(word_time("s135", word_index("s135", "Bayes")) - 0.2)
        miss = pill("Bayes = the missing piece", VIOLET, 28).next_to(grp, DOWN, buff=0.4)
        self.play(FadeIn(miss, shift=UP * 0.2), run_time=0.5)
        # ── s136 see you ──
        self.at("s136", 0.0)
        self.play(Indicate(nx, color=AQUA, scale_factor=1.08), run_time=1.0)
        self.finish()
