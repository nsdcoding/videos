import sys, pathlib, random
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

PINE = [30, 32, 35, 38, 40, 42, 45, 48, 230]


def news_card(headline, w=4.1, h=2.5):
    box = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=INK2, stroke_width=2,
                           fill_color="#22221f", fill_opacity=1)
    box.qa_container = True
    # header strip clipped to the card's rounded shape, with the border redrawn on top
    strip = Rectangle(width=w, height=0.36).move_to(box.get_top(), aligned_edge=UP)
    bar = Intersection(strip, box.copy(), stroke_width=0, fill_color="#2c2c29", fill_opacity=1)
    bar.qa_container = True
    rim = box.copy().set_fill(opacity=0); rim.qa_container = True
    tag = T("NEWS", 18, MUTED, weight=BOLD).move_to(bar).align_to(box, LEFT).shift(RIGHT * 0.25)
    hl = T(headline, 28, INK, weight=BOLD, line_spacing=0.9)
    if hl.width > w - 0.5:
        hl.scale_to_fit_width(w - 0.5)
    hl.next_to(bar, DOWN, buff=0.28).align_to(box, LEFT).shift(RIGHT * 0.25)
    lines = VGroup(*[Line(ORIGIN, RIGHT * (w - 0.5) * f, stroke_width=6, color="#3a3a37") for f in (1, 0.9, 0.6)])
    lines.arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(hl, DOWN, buff=0.3).align_to(hl, LEFT)
    return VGroup(box, bar, tag, hl, lines, rim)


def wallet():
    b = RoundedRectangle(corner_radius=0.08, width=0.62, height=0.44)
    f = RoundedRectangle(corner_radius=0.06, width=0.26, height=0.2).move_to(b.get_right() + LEFT * 0.12)
    d = Dot(radius=0.035).move_to(f)
    return VGroup(b, f, d).set_stroke(INK, 3).set_fill(opacity=0)


def clock(r=0.26):
    c = Circle(r)
    h1 = Line(ORIGIN, UP * r * 0.7); h2 = Line(ORIGIN, RIGHT * r * 0.5)
    return VGroup(c, h1, h2).set_stroke(INK, 3)


def restaurant():
    plate = Circle(0.5).set_stroke(INK, 3)
    inner = Circle(0.32).set_stroke(INK2, 2)
    fork = VGroup(Line(UP * 0.45, DOWN * 0.45), *[Line(UP * 0.45 + RIGHT * dx, UP * 0.2 + RIGHT * dx) for dx in (-0.08, 0.08)])
    fork.set_stroke(INK, 3).next_to(plate, LEFT, buff=0.15)
    knife = VGroup(Line(UP * 0.45, DOWN * 0.45), ArcBetweenPoints(UP * 0.45, UP * 0.05, angle=-1.2))
    knife.set_stroke(INK, 3).next_to(plate, RIGHT, buff=0.15)
    return VGroup(plate, inner, fork, knife)


class S02Why(Base):
    CHAPTER = "Why It Matters"

    def construct(self):
        fr = self.camera.frame
        # callback: the two towns, which then shrink into the corner
        title = VGroup(chip("Maple", INK, 40), chip("Pine Hill", INK, 40)).arrange(RIGHT, buff=0.8).move_to(UP * 0.6)
        # ── s019 title shrinks away, first headline card in ──
        cards = VGroup(news_card("Average salary rises"), news_card("Average home price\nhits record"),
                       news_card("Average wait time up")).arrange(RIGHT, buff=0.45).move_to(UP * 0.35)
        self.at("s019", 0.0)
        self.play(FadeIn(title, scale=0.9), run_time=0.5)
        self.until(word_time("s019", word_index("s019", "made-up")))
        self.play(title.animate.scale(0.5).to_corner(UR, buff=0.4), run_time=0.8)
        self.play(FadeIn(cards[0], shift=UP * 0.8), run_time=0.7)
        # ── s020 the other two cards ──
        self.at("s020", 0.0)
        self.play(FadeIn(cards[1], shift=UP * 0.8), run_time=0.7)
        self.play(FadeIn(cards[2], shift=UP * 0.8), run_time=0.7)
        self.play(*[c[4].animate.set_color("#4a4a46") for c in cards], run_time=0.6)
        # ── s021 highlight each with an icon ──
        icons = [wallet(), house(0.5, INK), clock()]
        for k, (c, ic, w) in enumerate(zip(cards, icons, (0, 2, 5))):
            ic.move_to(c[0].get_corner(DR) + LEFT * 0.62 + UP * 0.5)
            self.until(word_time("s021", w))
            others = [cc for j, cc in enumerate(cards) if j != k]
            self.play(c[5].animate.set_stroke(WARN, 3), *[cc[5].animate.set_stroke(INK2, 2) for cc in others],
                      Create(ic), c.animate.shift(UP * 0.15), *[cc.animate.align_to(cards[0], DOWN) for cc in others],
                      run_time=0.6)
        # ── s022 many dots → one number ──
        self.at("s022", 0.0)
        self.play(FadeOut(VGroup(cards, *icons, title), shift=UP * 0.5), run_time=0.6)
        random.seed(3)
        crowd = VGroup(*[Dot(radius=0.045, color=random.choice([BLUE_, BLUE_, INK2, ORANGE_]))
                         .move_to([random.uniform(-6.4, 6.4), random.uniform(-2.2, 3.2), 0]) for _ in range(260)])
        self.play(LaggedStart(*[FadeIn(d, scale=0.2) for d in crowd], lag_ratio=0.004), run_time=0.9)
        big = glow(TB("$60k", 120, WARN), WARN).move_to(UP * 0.4)
        lbl = T("one number for thousands of people", 30, INK2).next_to(big, DOWN, buff=0.35)
        self.play(LaggedStart(*[d.animate.move_to(big.get_center()).set_opacity(0) for d in crowd], lag_ratio=0.002),
                  FadeIn(big, scale=0.3, run_time=1.6), run_time=1.6)
        self.drop(crowd)
        self.play(FadeIn(lbl, shift=UP * 0.2), run_time=0.5)
        # ── s023 flicker + warning ──
        self.at("s023", 0.4)
        self.play(Wiggle(big, scale_value=1.08, rotation_angle=0.03 * TAU), run_time=0.9)
        warn_tri = VGroup(Triangle(color=RED_, stroke_width=6).scale(0.55),
                          TB("!", 48, RED_)).next_to(big, RIGHT, buff=0.6)
        warn_tri[1].move_to(warn_tri[0].get_center() + DOWN * 0.08)
        wtxt = T("wrong kind of average?", 32, RED_).next_to(lbl, DOWN, buff=0.3)
        self.play(GrowFromCenter(warn_tri), run_time=0.5)
        self.play(FadeIn(wtxt, shift=UP * 0.2), lbl.animate.set_opacity(0.5), run_time=0.6)
        # ── s024 Pine Hill returns with a 'you' dot ──
        self.at("s024", 0.0)
        self.play(FadeOut(VGroup(big, lbl, warn_tri, wtxt)), run_time=0.5)
        ax = money_axis(); ax.shift(DOWN * 0.55 - ax.axis.get_center())
        L = ax.axis
        ttl = TB("Pine Hill", 40).move_to([L.n2p(0)[0], 2.5, 0], aligned_edge=LEFT)
        dots = dot_plot(PINE, L, [BLUE_] * 8 + [ORANGE_], r=0.1)
        self.play(FadeIn(ax), FadeIn(ttl), LaggedStart(*[FadeIn(d, shift=DOWN * 0.4) for d in dots], lag_ratio=0.08),
                  run_time=1.1)
        you = Dot(radius=0.13, color=INK).move_to(L.n2p(60) + UP * 2.4)
        ylab = T("you, expecting 60", 28, INK).next_to(you, UP, buff=0.15)
        self.until(word_time("s024", word_index("s024", "expecting")))
        self.play(you.animate.move_to(L.n2p(60) + UP * 0.19), rate_func=rate_functions.ease_out_bounce, run_time=0.8)
        ylab.next_to(you, RIGHT, buff=0.3).shift(UP * 0.45)
        br = BraceBetweenPoints(L.n2p(29) + DOWN * 0.0 + UP * 0.6, L.n2p(49) + UP * 0.6, direction=UP, color=BLUE_)
        brt = T("neighbours: 30–48", 26, BLUE_).next_to(br, UP, buff=0.1)
        self.play(FadeIn(ylab, shift=DOWN * 0.2), GrowFromCenter(br), FadeIn(brt), run_time=0.7)
        # ── s025 restaurant counting on 60 ──
        self.at("s025", 0.0)
        rest = restaurant().move_to(RIGHT * 3.6 + UP * 2.1)
        tagp = chip("$$$  fancy", ORANGE_, 24).next_to(rest, RIGHT, buff=0.3)
        self.play(FadeOut(ylab), Create(rest), FadeIn(tagp, shift=LEFT * 0.2), run_time=0.9)
        arr = CurvedArrow(rest.get_left() + LEFT * 0.2, L.n2p(62) + UP * 0.45, angle=0.6, color=WARN, stroke_width=4)
        alab = T("expected customers", 26, WARN).next_to(arr.get_start(), LEFT, buff=0.25).shift(UP * 0.3)
        self.play(Create(arr), FadeIn(alab), run_time=0.9)
        self.at("s025", word_time("s025", word_index("s025", "mostly")) - SEGS["s025"]["start"])
        arr2 = CurvedArrow(rest.get_left() + LEFT * 0.2, brt.get_top() + UP * 0.12, angle=0.5, color=BLUE_, stroke_width=4)
        alab2 = T("actual customers", 26, BLUE_).move_to(alab)
        self.play(Transform(arr, arr2), Transform(alab, alab2), br.animate.set_color(WARN), run_time=0.9)
        self.play(Indicate(dots[:8], color=BLUE_, scale_factor=1.3), run_time=0.8)
        # ── s026 good news: stopwatch + badge ──
        self.at("s026", 0.0)
        self.play(FadeOut(VGroup(ax, ttl, dots, you, br, brt, rest, tagp, arr, alab)), run_time=0.6)
        sw_c = Circle(1.2).set_stroke(INK, 6)
        knob = VGroup(Line(UP * 1.2, UP * 1.45), RoundedRectangle(corner_radius=0.05, width=0.45, height=0.16)
                      .move_to(UP * 1.53)).set_stroke(INK, 5)
        ticks = VGroup(*[Line(UP * 1.0, UP * 1.12).rotate(-i * TAU / 12, about_point=ORIGIN) for i in range(12)])
        ticks.set_stroke(INK2, 3)
        hand = Line(ORIGIN, UP * 0.95, stroke_width=6, color=AQUA)
        sw = VGroup(sw_c, knob, ticks).move_to(LEFT * 3.2 + UP * 0.4)
        hand.shift(sw_c.get_center())
        self.play(Create(sw), run_time=0.8)
        self.add(hand)
        self.play(Rotate(hand, angle=-TAU * 1.25, about_point=sw_c.get_center()), run_time=1.8, rate_func=smooth)
        t1 = TB("a few minutes", 56, INK).move_to(RIGHT * 2.6 + UP * 1.0)
        badge = chip("no fancy math", AQUA, 40).next_to(t1, DOWN, buff=0.45)
        self.play(FadeIn(t1, shift=LEFT * 0.4), run_time=0.6)
        self.play(GrowFromCenter(badge), run_time=0.6)
        self.finish()
