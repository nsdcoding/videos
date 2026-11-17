import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def clinic():
    body = Rectangle(width=3.2, height=2.4).set_stroke(INK2, 3)
    roof = Line(body.get_corner(UL) + LEFT * 0.25, body.get_corner(UR) + RIGHT * 0.25).set_stroke(INK2, 4)
    door = Rectangle(width=0.9, height=1.4).set_stroke(INK2, 3).align_to(body, DOWN)
    knob = Dot(radius=0.05, color=INK2).move_to(door.get_right() + LEFT * 0.15)
    plus = VGroup(Rectangle(width=0.5, height=0.16), Rectangle(width=0.16, height=0.5)).set_stroke(width=0).set_fill(RED_, 1)
    plus.move_to(body.get_top() + DOWN * 0.42)
    w1 = Square(0.5).set_stroke(INK2, 3).move_to(body.get_center() + LEFT * 1.0 + UP * 0.1)
    w2 = w1.copy().move_to(body.get_center() + RIGHT * 1.0 + UP * 0.1)
    return VGroup(body, roof, door, knob, plus, w1, w2)


def clipboard():
    b = RoundedRectangle(corner_radius=0.12, width=3.1, height=3.2).set_stroke(INK2, 3).set_fill("#22221f", 1)
    b.qa_container = True
    clip = RoundedRectangle(corner_radius=0.08, width=1.0, height=0.3).set_stroke(INK2, 3).set_fill(BG, 1).move_to(b.get_top())
    clip.qa_container = True
    t = T("screening test", 26, INK, weight=BOLD).move_to(b.get_top() + DOWN * 0.65)
    lines = VGroup(*[Line(LEFT * 0.9, RIGHT * 0.9).set_stroke(MUTED, 3) for _ in range(4)]).arrange(DOWN, buff=0.35)
    lines.next_to(t, DOWN, buff=0.4)
    return VGroup(b, clip, t, lines)


def envelope():
    b = Rectangle(width=4.2, height=2.6).set_stroke(INK2, 3).set_fill("#22221f", 1)
    b.qa_container = True
    flap = Polygon(b.get_corner(UL), b.get_corner(UR), b.get_center() + DOWN * 0.1).set_stroke(INK2, 3).set_fill("#22221f", 1)
    flap.qa_container = True
    return VGroup(b, flap)


class S01Hook(Base):
    CHAPTER = "The Positive Test"

    def construct(self):
        fr = self.camera.frame
        # ── s001 clinic + clipboard ──
        cl = clinic().move_to(LEFT * 3.2 + UP * 0.5)
        ground = Line(LEFT * 7.5, RIGHT * 0.5, color=GRID, stroke_width=2).next_to(cl, DOWN, buff=0).shift(RIGHT * 0.4)
        you = person(INK, 0.9).move_to(LEFT * 7.6 + UP * 0.5).align_to(ground, DOWN).shift(UP * 0.02)
        self.at("s001", 0.0)
        self.play(Create(ground), Create(cl, lag_ratio=0.15), run_time=1.6)
        self.add(you)
        self.play(you.animate.next_to(cl[2], LEFT, buff=0.15).align_to(ground, DOWN).shift(UP * 0.02),
                  run_time=1.4, rate_func=smooth)
        cb = clipboard().move_to(RIGHT * 2.6 + UP * 0.5)
        self.play(FadeIn(cb, shift=LEFT * 0.5), run_time=0.7)
        self.play(LaggedStart(*[Create(l) for l in cb[3]], lag_ratio=0.25), run_time=0.9)

        # ── s002 10 x 10 grid, 1 in 100 ──
        self.at("s002", 0.0)
        axg = xy_axes([0, 10, 5], [0, 10, 5], 4.0, 4.0, "column", "row", font_size=20)
        axg.move_to(LEFT * 3.6 + UP * 0.35)
        ax = axg.ax
        cells = VGroup(*[Square(0.33, stroke_width=0, fill_color=BLUE_, fill_opacity=0.9).move_to(ax.c2p(c + 0.5, r + 0.5))
                         for r in range(9, -1, -1) for c in range(10)])
        self.play(FadeOut(VGroup(cl, ground, you, cb), shift=UP * 0.3), run_time=0.5)
        self.play(Create(ax), FadeIn(axg.labs), FadeIn(axg.xt), FadeIn(axg.yt), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in cells], lag_ratio=0.012), run_time=1.3)
        one = cells[6]
        self.until(word_time("s002", word_index("s002", "one")))
        self.play(one.animate.set_fill(ORANGE_), Flash(one, color=ORANGE_, line_length=0.18), run_time=0.6)
        rate = pill("1 in 100 have it", ORANGE_, 30).move_to(RIGHT * 2.9 + UP * 2.6)
        arr = Arrow(rate.get_left() + DOWN * 0.05, one.get_top() + UP * 0.05, buff=0.15, color=ORANGE_, stroke_width=4,
                    max_tip_length_to_length_ratio=0.06)
        self.play(FadeIn(rate, shift=LEFT * 0.3), GrowArrow(arr), run_time=0.7)

        # ── s003 catches 9 of 10 ──
        self.at("s003", 0.3)
        def stat(color, n_ring, caption):
            box = card(6.6, 1.95)
            sq = VGroup(*[Square(0.4, stroke_width=0, fill_color=color, fill_opacity=0.95) for _ in range(10)]).arrange(RIGHT, buff=0.16)
            sq.move_to(box.get_top() + DOWN * 0.55)
            rings = VGroup(*[ring(s, AQUA, 4, 0.05) for s in sq[:n_ring]]) if color == ORANGE_ else VGroup(ring(sq[3], AQUA, 4, 0.05))
            cap = T(caption, 26, INK).move_to(box.get_bottom() + UP * 0.48)
            return VGroup(box, sq, rings, cap)
        c1 = stat(ORANGE_, 9, "catches 9 of 10 who have it").move_to(RIGHT * 3.25 + UP * 0.75)
        self.play(FadeOut(arr), FadeIn(c1[0]), FadeIn(c1[1], lag_ratio=0.1), run_time=0.8)
        self.play(LaggedStart(*[Create(r) for r in c1[2]], lag_ratio=0.15), FadeIn(c1[3]), run_time=1.6)
        # ── s004 false alarm 1 in 10 ──
        self.at("s004", 0.2)
        c2 = stat(BLUE_, 1, "false alarm for 1 in 10 healthy people").next_to(c1, DOWN, buff=0.3)
        self.play(FadeIn(c2[0]), FadeIn(c2[1], lag_ratio=0.1), run_time=0.8)
        self.play(Create(c2[2]), FadeIn(c2[3]), run_time=0.8)
        self.play(Indicate(c2[2], color=AQUA, scale_factor=1.3), run_time=0.7)

        # ── s005 envelope, POSITIVE ──
        self.at("s005", 0.0)
        env = envelope().move_to(UP * 0.4)
        self.play(FadeOut(VGroup(axg, cells, rate, c1, c2), shift=DOWN * 0.3), FadeIn(env, shift=UP * 0.4), run_time=0.7)
        flap = env[1]
        self.play(Rotate(flap, PI, axis=RIGHT, about_point=env[0].get_top()), run_time=0.5)
        self.until(word_time("s005", word_index("s005", "positive")) - 0.1)
        stamp = pill("POSITIVE", AQUA, 50, pad=0.26).rotate(8 * DEGREES).move_to(env[0])
        self.play(FadeIn(stamp, scale=1.8), run_time=0.35, rate_func=rate_functions.ease_out_back)
        self.play(Flash(stamp, color=AQUA, line_length=0.35, flash_radius=1.8), run_time=0.6)

        # ── s006 meter ──
        self.at("s006", 0.0)
        res = VGroup(env, stamp)
        self.play(res.animate.scale(0.32).move_to(RIGHT * 5.6 + UP * 2.85), run_time=0.7)
        mt = meter(11.0).move_to(DOWN * 0.6)
        q = T("What is the chance you actually have it?", 40, INK, weight=BOLD).move_to(UP * 2.6 + LEFT * 0.9)
        self.play(Create(mt.nl), FadeIn(mt.nums, lag_ratio=0.05), FadeIn(mt.title), run_time=1.0)
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=0.6)
        # ── s006a make a guess ──
        self.at("s006a", 0.0)
        qm = TB("?", 72, WARN).move_to(mt.nl.n2p(50) + UP * 0.85)
        self.play(FadeIn(qm, scale=0.4), run_time=0.4)
        for _ in range(3):
            self.play(qm.animate.set_opacity(0.15), run_time=0.35)
            self.play(qm.animate.set_opacity(1), run_time=0.35)

        # ── s007 gut feeling 90 ──
        self.at("s007", 0.0)
        gut = marker(mt.nl, 50, MUTED, "gut feeling", height=0.85, fs=28)
        self.play(FadeOut(qm), FadeIn(gut), run_time=0.4)
        self.play(gut.animate.shift(mt.nl.n2p(90) - mt.nl.n2p(50)), run_time=1.4, rate_func=smooth)
        g90 = T("90%", 30, MUTED, weight=BOLD).next_to(gut.lab, RIGHT, buff=0.2)
        self.play(FadeIn(g90), run_time=0.4)

        # ── s008 the real answer ≈ 8% ──
        self.at("s008", 0.6)
        real = marker(mt.nl, 8.33, VIOLET, "real answer ≈ 8%", height=0.85, fs=30)
        real.tri.shift(UP * 0.6); real.lab.next_to(real.tri, UP, buff=0.12)
        real[0].become(DashedLine(real.tri.get_bottom(), mt.nl.n2p(8.33), color=VIOLET, stroke_width=3))
        real.lab.shift(RIGHT * (real.lab.width / 2 - 0.4))
        self.until(word_time("s008", word_index("s008", "real")))
        self.play(FadeIn(real, shift=DOWN * 1.2), run_time=0.7, rate_func=rate_functions.ease_out_bounce)
        x = cross(RED_, 0.22).move_to(gut[0].get_center())
        self.play(Create(x), VGroup(gut, g90).animate.set_opacity(0.45), run_time=0.5)
        self.play(Flash(real.tri, color=VIOLET, line_length=0.3), run_time=0.6)

        # ── s009 Not ninety. Eight. ──
        self.at("s009", 0.0)
        n90 = TB("90%", 150, MUTED).move_to(LEFT * 3.3 + UP * 0.4)
        n8 = glow(TB("≈ 8%", 150, VIOLET), VIOLET).move_to(RIGHT * 3.0 + UP * 0.4)
        self.play(FadeOut(VGroup(mt, gut, g90, real, x, q, res)), FadeIn(n90, shift=RIGHT * 0.4), run_time=0.6)
        strike = Line(n90.get_left() + LEFT * 0.15, n90.get_right() + RIGHT * 0.15, color=RED_, stroke_width=10)
        strike.qa_ignore = True  # deliberate strike-through
        self.play(Create(strike), run_time=0.35)
        self.until(word_time("s009", word_index("s009", "eight")))
        self.play(FadeIn(n8, scale=0.6), run_time=0.5)
        self.play(fr.animate.scale(0.7).move_to(n8[1].get_center() + LEFT * 0.6 + DOWN * 0.3), VGroup(n90, strike).animate.set_opacity(0),
                  run_time=1.0, rate_func=smooth)
        ltt = T("less than 1 in 10", 36, INK).next_to(n8, DOWN, buff=0.4)
        self.play(FadeIn(ltt, shift=UP * 0.2), run_time=0.5)

        # ── s010 three facts ──
        self.at("s010", 0.0)
        facts = VGroup(pill("1 in 100 have it", INK, 32), pill("catches 9 of 10", INK, 32),
                       pill("false alarm 1 in 10", INK, 32)).arrange(RIGHT, buff=0.45).move_to(UP * 0.5)
        self.play(FadeOut(VGroup(n90, strike, n8, ltt)), fr.animate.restore(), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.4) for f in facts], lag_ratio=0.3), run_time=1.3)
        self.until(word_time("s010", word_index("s010", "Your")))
        gutb = T("your gut uses these two", 30, MUTED).next_to(facts[1:], DOWN, buff=0.5)
        br = Brace(facts[1:], DOWN, color=MUTED, buff=0.15)
        gutb.next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(gutb), run_time=0.7)

        # ── s011 the base rate ──
        self.at("s011", 0.0)
        f0 = facts[0]
        self.play(f0.box.animate.set_stroke(WARN, 4), f0.text.animate.set_color(WARN), run_time=0.5)
        f0g = glow(f0.box.copy().set_fill(opacity=0), WARN, width=18, opacity=0.08)
        base = T("the base rate", 34, WARN, weight=BOLD).next_to(f0, UP, buff=0.4)
        self.play(FadeIn(f0g), FadeIn(base, shift=DOWN * 0.2), f0.animate.scale(1.12), f0g.animate.scale(1.12), run_time=0.7)
        self.play(fr.animate.scale(0.75).move_to(VGroup(f0, base).get_center() + RIGHT * 0.8), FadeOut(VGroup(br, gutb, facts[1:])), run_time=0.8)

        # ── s012 title card ──
        self.at("s012", 0.3)
        title = bayes_title()
        self.drop(facts[1:], br, gutb)
        slot = VGroup(f0, f0g)
        self.play(FadeOut(base), fr.animate.restore(), slot.animate.move_to(UP * 0.4), run_time=0.9)
        self.play(slot.animate.scale(1.15), rate_func=there_and_back, run_time=0.8)
        self.until(word_time("s012", word_index("s012", "Bayes'")) - 0.15)
        self.play(FadeOut(slot, scale=1.6), FadeIn(title[0], scale=0.85), run_time=0.8)
        self.play(Write(title[1]), run_time=1.0)
        self.finish()
