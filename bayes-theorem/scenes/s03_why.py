import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def smoke_alarm(c=INK2):
    disc = Circle(0.55).set_stroke(c, 4)
    inner = Circle(0.18).set_stroke(c, 3)
    waves = VGroup(*[Arc(radius=0.75 + 0.2 * k, start_angle=-PI / 4, angle=PI / 2).set_stroke(RED_, 3) for k in range(2)])
    waves2 = waves.copy().rotate(PI, about_point=ORIGIN)
    return VGroup(disc, inner, waves, waves2)


def mail(c=INK2):
    b = Rectangle(width=1.5, height=1.0).set_stroke(c, 4)
    v = VMobject().set_points_as_corners([b.get_corner(UL), b.get_center() + DOWN * 0.1, b.get_corner(UR)]).set_stroke(c, 4)
    return VGroup(b, v)


def phone(c=INK2):
    b = RoundedRectangle(corner_radius=0.15, width=0.95, height=1.6).set_stroke(c, 4)
    bub = RoundedRectangle(corner_radius=0.08, width=0.7, height=0.35).set_stroke(c, 3).move_to(b.get_center() + UP * 0.25)
    return VGroup(b, bub)


def radar(c=AQUA):
    arcs = VGroup(*[Arc(radius=r, start_angle=PI / 6, angle=2 * PI / 3).set_stroke(c, 4) for r in (0.3, 0.55, 0.8)])
    base = Dot(radius=0.08, color=c).move_to(ORIGIN)
    return VGroup(arcs, base).shift(DOWN * 0.3)


class S03Why(Base):
    CHAPTER = "Why It Matters"

    def construct(self):
        fr = self.camera.frame
        # ── s017 not just medical tests ──
        self.at("s017", 0.0)
        tube = VGroup(RoundedRectangle(corner_radius=0.2, width=0.5, height=1.6).set_stroke(INK2, 4),
                      Rectangle(width=0.4, height=0.6).set_stroke(width=0).set_fill(AQUA, 0.8).shift(DOWN * 0.42))
        tube.move_to(UP * 0.5)
        tl = T("medical tests", 32, INK2).next_to(tube, DOWN, buff=0.3)
        self.play(FadeIn(tube, shift=UP * 0.3), FadeIn(tl), run_time=0.6)
        self.play(VGroup(tube, tl).animate.scale(0.6).move_to(RIGHT * 5.6 + UP * 2.3), run_time=0.7)
        # ── s018 rare thing + imperfect detector = trap ──
        self.at("s018", 0.0)
        a = VGroup(Dot(radius=0.32, color=ORANGE_), T("a rare thing", 30, ORANGE_)).arrange(DOWN, buff=0.35)
        b = VGroup(radar(), T("an imperfect detector", 30, AQUA)).arrange(DOWN, buff=0.35)
        tr = VGroup(TB("!", 90, RED_), T("the same trap", 30, RED_)).arrange(DOWN, buff=0.35)
        plus, eq = TB("+", 64, MUTED), TB("=", 64, MUTED)
        row = VGroup(a, plus, b, eq, tr).arrange(RIGHT, buff=0.6).move_to(UP * 0.4)
        for m in (plus, eq): m.align_to(a[0], UP).shift(DOWN * 0.05)
        self.play(FadeOut(VGroup(tube, tl)), FadeIn(a, shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(plus), FadeIn(b, shift=UP * 0.3), run_time=0.6)
        self.until(word_time("s018", word_index("s018", "same")) - 0.2)
        self.play(FadeIn(eq), FadeIn(tr, scale=1.4), run_time=0.6)
        self.play(Wiggle(tr[0]), run_time=0.8)
        # ── s019 three everyday alarms ──
        self.at("s019", 0.0)
        def tcard(icon, label, color):
            box = card(3.6, 3.2)
            icon.move_to(box.get_center() + UP * 0.4)
            t = T(label, 28, INK, weight=BOLD).move_to(box.get_bottom() + UP * 0.5)
            return VGroup(box, icon, t)
        cards = VGroup(tcard(smoke_alarm(), "smoke alarm", RED_), tcard(mail(), "flagged as spam", BLUE_),
                       tcard(phone(), "“Was this you?”", WARN)).arrange(RIGHT, buff=0.55).move_to(UP * 0.55)
        self.play(FadeOut(row, shift=UP * 0.4), run_time=0.5)
        for k, w in enumerate(("smoke", "email", "message")):
            self.until(word_time("s019", word_index("s019", w)) - 0.15)
            self.play(FadeIn(cards[k], shift=UP * 0.4), run_time=0.5)
            if k == 0:
                self.play(Indicate(cards[0][1][2:], color=RED_, scale_factor=1.15), run_time=0.6)
        # ── s020 each is a positive test ──
        self.at("s020", 0.0)
        rings = VGroup(*[RoundedRectangle(corner_radius=0.22, width=c[0].width + 0.22, height=c[0].height + 0.22)
                         .set_stroke(AQUA, 5).move_to(c[0]) for c in cards])
        for r in rings: r.qa_ignore = True
        tags = VGroup(*[pill("positive", AQUA, 24).move_to(c[0].get_top()) for c in cards])
        self.play(LaggedStart(*[AnimationGroup(Create(r), FadeIn(t, scale=0.6)) for r, t in zip(rings, tags)],
                              lag_ratio=0.3), run_time=1.6)
        self.until(word_time("s020", word_index("s020", "given")) - 0.1)
        ban = VGroup(T("given the alarm", 36, AQUA, weight=BOLD), T("→", 36, MUTED),
                     T("how likely is the real thing?", 36, VIOLET, weight=BOLD)).arrange(RIGHT, buff=0.3)
        ban.next_to(cards, DOWN, buff=0.45)
        self.play(FadeIn(ban[0], shift=RIGHT * 0.3), run_time=0.5)
        self.play(FadeIn(ban[1]), FadeIn(ban[2], shift=RIGHT * 0.3), run_time=0.6)
        self.play(Circumscribe(ban[2], color=VIOLET), run_time=1.0)
        # ── s021 the doctors study ──
        self.at("s021", 0.0)
        sh = T("Study of doctors", 40, INK, weight=BOLD)
        sd = T("a screening puzzle with numbers like ours", 28, INK2)
        st = card(max(sh.width, sd.width) + 1.0, 2.4, INK2)
        sh.move_to(st.get_top() + DOWN * 0.6); sd.next_to(sh, DOWN, buff=0.35)
        sg = VGroup(st, sh, sd).move_to(UP * 0.4)
        docs = VGroup(*[person(INK2, 0.55) for _ in range(10)]).arrange(RIGHT, buff=0.22).next_to(sg, DOWN, buff=0.35)
        self.play(FadeOut(VGroup(cards, rings, tags, ban), shift=UP * 0.4), run_time=0.5)
        self.play(FadeIn(sg, shift=UP * 0.3), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.2) for d in docs], lag_ratio=0.08), run_time=1.0)
        # ── s022 bar chart: right answer vs 9 in 10 ──
        self.at("s022", 0.0)
        axg = xy_axes([0, 2, 1], [0, 50, 10], 6.0, 3.6, None, "share of doctors (%)", x_labels={}, font_size=22)
        axg.move_to(LEFT * 1.6 + UP * 0.35)
        ax = axg.ax
        self.play(FadeOut(VGroup(sg, docs), shift=UP * 0.3), run_time=0.4)
        self.play(Create(ax), FadeIn(axg.labs), FadeIn(axg.yt), run_time=0.7)
        def bar(x, v, color, cat):
            r = Rectangle(width=1.5, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=color, fill_opacity=0.9)
            r.move_to(ax.c2p(x, 0), aligned_edge=DOWN)
            l = T(f"≈ {v}%", 26, color, weight=BOLD).next_to(r, UP, buff=0.12)
            c_ = T(cat, 22, color, line_spacing=0.8).next_to(ax.c2p(x, 0), DOWN, buff=0.18)
            return VGroup(r, l, c_)
        b1 = bar(0.55, 21, VIOLET, "answered 1 in 10\n(the right answer)")
        b2 = bar(1.45, 47, MUTED, "answered 9 in 10\n(wrong)")
        self.play(GrowFromEdge(b1[0], DOWN), FadeIn(b1[1:]), run_time=0.7)
        v1 = T("about 1 in 5 got it right", 28, VIOLET).move_to(RIGHT * 4.4 + UP * 0.1)
        self.play(FadeIn(v1), run_time=0.3)
        self.until(word_time("s022", word_index("s022", "Almost")) - 0.1)
        self.play(GrowFromEdge(b2[0], DOWN), FadeIn(b2[1:]), run_time=0.7)
        v2 = T("almost half said 9 in 10", 28, INK2).next_to(v1, UP, buff=0.5).align_to(v1, LEFT)
        note = T("other answers not shown", 20, MUTED).next_to(v1, DOWN, buff=0.4).align_to(v1, LEFT)
        self.play(FadeIn(v2), FadeIn(note), run_time=0.4)
        # ── s023 percentages of percentages ──
        self.at("s023", 0.0)
        pcs = VGroup(*[TB(t, 64, c) for t, c in (("1%", WARN), ("90%", AQUA), ("10%", BLUE_), ("of", MUTED), ("%", INK2), ("?", RED_))])
        spots = [LEFT * 3.5 + UP * 1.3, RIGHT * 0.2 + UP * 1.8, RIGHT * 3.6 + UP * 0.9, LEFT * 1.2 + DOWN * 0.2,
                 RIGHT * 1.9 + DOWN * 0.7, LEFT * 3.9 + DOWN * 0.9]
        for p, s_ in zip(pcs, spots): p.move_to(s_)
        self.play(FadeOut(VGroup(axg, b1, b2, v1, v2, note)), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in pcs], lag_ratio=0.12), run_time=1.2)
        self.play(*[Rotate(p, angle=(0.25 if k % 2 else -0.25), about_point=p.get_center()) for k, p in enumerate(pcs)],
                  *[p.animate.shift(0.5 * (RIGHT if k % 2 else LEFT)) for k, p in enumerate(pcs)], run_time=1.6,
                  rate_func=there_and_back)
        self.play(*[p.animate.shift(0.4 * (UP if k % 3 else DOWN)).scale(1.15) for k, p in enumerate(pcs)], run_time=1.2,
                  rate_func=there_and_back)
        self.play(LaggedStart(*[Wiggle(p, scale_value=1.2) for p in pcs], lag_ratio=0.15), run_time=1.6)
        self.play(Indicate(pcs[3], color=WARN, scale_factor=1.5), run_time=0.8)
        # ── s024 → count people ──
        self.at("s024", 0.0)
        g = VGroup(*[Square(0.34, stroke_width=0, fill_color=BLUE_, fill_opacity=0.9) for _ in range(40)]).arrange_in_grid(4, 10, buff=0.1)
        g.move_to(UP * 0.4)
        g[0].set_fill(ORANGE_)
        self.play(*[ReplacementTransform(p, VGroup(*g[k::6])) for k, p in enumerate(pcs)], run_time=1.4)
        self.play(g.animate.scale(1.12), rate_func=there_and_back, run_time=0.8)
        easy = T("easy", 34, AQUA, weight=BOLD).next_to(g, UP, buff=0.4)
        self.play(FadeIn(easy, shift=DOWN * 0.2), run_time=0.4)
        self.until(word_time("s024", word_index("s024", "stop")) - 0.2)
        self.play(FadeOut(easy), run_time=0.3)
        cp = pill("count people", AQUA, 36).next_to(g, DOWN, buff=0.5)
        self.until(word_time("s024", word_index("s024", "counting")) - 0.1)
        self.play(FadeIn(cp, shift=UP * 0.2), run_time=0.5)
        cnt = ValueTracker(0)
        ct = always_redraw(lambda: T(f"{int(cnt.get_value())} people", 30, INK2).next_to(g, RIGHT, buff=0.45))
        self.add(ct)
        self.play(LaggedStart(*[Indicate(s, scale_factor=1.3, color=s.get_fill_color()) for s in g], lag_ratio=0.03),
                  cnt.animate.set_value(40), run_time=1.6, rate_func=linear)
        ct.clear_updaters()
        # ── s025 changing your mind by the right amount ──
        self.at("s025", 0.0)
        dial_c = Arc(radius=2.0, start_angle=PI, angle=-PI).set_stroke(INK2, 6).move_to(DOWN * 0.1)
        cen = dial_c.get_center() + DOWN * 1.0 + DOWN * 0.0
        cen = dial_c.get_bottom() * 0 + np.array([dial_c.get_center()[0], dial_c.get_bottom()[1], 0])
        ticks = VGroup()
        for k in range(11):
            ang = PI - k * PI / 10
            d = np.array([np.cos(ang), np.sin(ang), 0])
            ticks.add(Line(cen + d * 1.82, cen + d * 2.0).set_stroke(INK2, 3))
        l0 = T("not sure", 24, MUTED).next_to(cen + LEFT * 2.0, DOWN, buff=0.15)
        l1 = T("certain", 24, MUTED).next_to(cen + RIGHT * 2.0, DOWN, buff=0.15)
        needle = Line(cen, cen + LEFT * 1.6).set_stroke(VIOLET, 7)
        hub = Dot(cen, radius=0.1, color=VIOLET)
        dt = T("how sure am I?", 32, INK, weight=BOLD).next_to(dial_c, UP, buff=0.35)
        dial = VGroup(dial_c, ticks, l0, l1, needle, hub, dt)
        dial.scale(1.3).move_to(UP * 0.4)
        cen = hub.get_center()
        self.play(FadeOut(VGroup(g, cp, ct), shift=UP * 0.3), FadeIn(dial), run_time=0.7)
        self.play(Rotate(needle, angle=-PI * 0.12, about_point=cen), run_time=0.9, rate_func=smooth)
        self.until(word_time("s025", word_index("s025", "Not")) - 0.1)
        ghost0 = needle.copy().set_stroke(BLUE_, 5, opacity=0.7)
        self.play(Rotate(ghost0, angle=-PI * 0.02, about_point=cen), run_time=0.4)
        t0 = T("too little", 26, BLUE_).next_to(l0, UP, buff=1.3).shift(LEFT * 1.1)
        self.play(FadeIn(t0), run_time=0.3)
        self.play(FadeOut(ghost0), FadeOut(t0), run_time=0.3)
        ghost1 = needle.copy().set_stroke(RED_, 5, opacity=0.6)
        self.play(Rotate(ghost1, angle=-PI * 0.75, about_point=cen), run_time=0.6)
        t1 = T("too much", 26, RED_).next_to(l1, UP, buff=1.3).shift(RIGHT * 1.1)
        self.play(FadeIn(t1), run_time=0.3)
        self.play(FadeOut(ghost1), FadeOut(t1), run_time=0.4)
        ok = pill("update by the right amount", VIOLET, 30).next_to(l0, DOWN, buff=0.45).set_x(cen[0])
        self.play(FadeIn(ok, shift=UP * 0.2), run_time=0.5)
        self.until(SEGS["s025"]["end"] + 0.6)
        self.play(FadeOut(VGroup(dial, ok)), run_time=0.5)
        self.finish()
