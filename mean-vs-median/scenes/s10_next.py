import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

CEDAR = [10, 20, 30, 45, 60, 75, 90, 100, 110]


def puzzle(s=1.0, c=AQUA):
    sq = Square(1.4 * s)
    bump_r = Circle(0.28 * s).move_to(sq.get_right())
    bump_t = Circle(0.28 * s).move_to(sq.get_top())
    return Union(sq, bump_r, bump_t, color=c, stroke_width=5, fill_color=c, fill_opacity=0.15)


class S10Next(Base):
    CHAPTER = "Next Time"

    def construct(self):
        # ── s163 puzzle ──
        self.at("s163", 0.0)
        pz = puzzle().move_to(UP * 0.6)
        pt = T("a puzzle for next time", 34, AQUA).next_to(pz, DOWN, buff=0.4)
        self.play(DrawBorderThenFill(pz), FadeIn(pt), run_time=1.0)
        # ── s164 same mean, same median, different towns ──
        self.at("s164", 0.0)
        self.play(FadeOut(VGroup(pz, pt)), run_time=0.4)
        aM = money_axis(x_max=120, step=10, length=11, label_every=2); aM.title.set_opacity(0)
        aM.shift(UP * 1.3 - aM.axis.get_center())
        aC = money_axis(x_max=120, step=10, length=11, label_every=2); aC.shift(DOWN * 1.0 - aC.axis.get_center())
        LM, LC = aM.axis, aC.axis
        dM = dot_plot(MAPLE, LM, [INK] * 9); dC = dot_plot(CEDAR, LC, [AQUA] * 9)
        nM = TB("Maple", 30).next_to(LM, LEFT, buff=0.3)
        nC = TB("Cedar", 30, AQUA).next_to(LC, LEFT, buff=0.3)
        self.play(FadeIn(aM), FadeIn(nM), FadeIn(dM), run_time=0.7)
        self.play(FadeIn(aC), FadeIn(nC), LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in dC], lag_ratio=0.06), run_time=0.9)
        mks = VGroup(marker(LM, 60, WARN, "", height=0.7), diamond(LM, 60, VIOLET, height=1.0),
                     marker(LC, 60, WARN, "", height=0.7), diamond(LC, 60, VIOLET, height=1.0))
        both = T("mean 60 · median 60 — in both towns", 28, INK).move_to(UP * 2.75 + RIGHT * 2.2)
        both[:6].set_color(WARN); both[7:15].set_color(VIOLET)
        self.play(FadeIn(mks), FadeIn(both), run_time=0.8)
        # ── s165 spread ──
        self.at("s165", 0.0)
        sM = DoubleArrow(LM.n2p(50) + DOWN * 0.0 + UP * 0.0, LM.n2p(70), buff=0, color=INK, stroke_width=4).shift(DOWN * 0.0)
        sM.next_to(LM, DOWN, buff=0.0).shift(DOWN * 0.0)
        sM = DoubleArrow(LM.n2p(50) + UP * 1.3 - UP * 1.3 + DOWN * 0.0, LM.n2p(70), buff=0, color=INK, stroke_width=4)
        sM.move_to([LM.n2p(60)[0], LM.get_y() + 1.35, 0])
        sC = DoubleArrow(LC.n2p(10), LC.n2p(110), buff=0, color=AQUA, stroke_width=4).move_to([LC.n2p(60)[0], LC.get_y() + 1.35, 0])
        tM = T("narrow spread", 24, INK).next_to(sM, LEFT, buff=0.2)
        tC = T("wide spread", 24, AQUA).next_to(sC, LEFT, buff=0.2)
        self.play(FadeOut(both), mks.animate.set_opacity(0.35), run_time=0.4)
        self.play(GrowFromCenter(sM), FadeIn(tM), run_time=0.6)
        self.play(GrowFromCenter(sC), FadeIn(tC), run_time=0.7)
        # ── s166 next: standard deviation ──
        self.at("s166", 0.0)
        self.play(FadeOut(VGroup(aM, aC, dM, dC, nM, nC, mks, sM, sC, tM, tC)), run_time=0.5)
        nx = T("NEXT", 30, MUTED, weight=BOLD).move_to(UP * 1.6)
        sd = glow(TB("Standard Deviation", 80, AQUA), AQUA).move_to(UP * 0.6)
        sub = T("how far values typically sit from the middle", 30, INK2).next_to(sd, DOWN, buff=0.35)
        self.play(FadeIn(nx), FadeIn(sd, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.5)
        # ── s167 end card ──
        self.at("s167", 0.0)
        self.play(FadeOut(VGroup(nx, sd, sub)), run_time=0.4)
        logo = VGroup(TB("Math Lab", 84, INK), TB("TV", 84, WARN)).arrange(RIGHT, buff=0.3).move_to(UP * 0.6)
        flask = VGroup(Line(UP * 0.5 + LEFT * 0.15, UP * 0.1 + LEFT * 0.15), Line(UP * 0.5 + RIGHT * 0.15, UP * 0.1 + RIGHT * 0.15),
                       Polygon(UP * 0.1 + LEFT * 0.15, DOWN * 0.5 + LEFT * 0.45, DOWN * 0.5 + RIGHT * 0.45, UP * 0.1 + RIGHT * 0.15))
        flask.set_stroke(AQUA, 5).next_to(logo, LEFT, buff=0.4)
        see = T("see you in the lab", 34, INK2).next_to(logo, DOWN, buff=0.45)
        self.play(FadeIn(logo, scale=0.9), Create(flask), run_time=0.8)
        self.play(FadeIn(see, shift=UP * 0.2), run_time=0.5)
        self.finish()
