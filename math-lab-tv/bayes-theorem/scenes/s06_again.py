import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def odds_theta(s_, h_):
    return 0.32 * np.tanh(np.log(s_ / h_) / 2.5)


class S06Again(Base):
    CHAPTER = "Test Again"

    def construct(self):
        # ── s066 one in twelve; what next? ──
        self.at("s066", 0.0)
        c12 = pill("your chance now: 1 in 12", VIOLET, 40).move_to(LEFT * 2.0 + UP * 0.6)
        t1 = tube(AQUA).move_to(RIGHT * 3.6 + UP * 0.6)
        twelve = VGroup(*[Square(0.42, stroke_width=0, fill_color=ORANGE_ if k == 0 else BLUE_, fill_opacity=1) for k in range(12)])
        twelve.arrange(RIGHT, buff=0.1).next_to(c12, DOWN, buff=0.5)
        self.play(FadeIn(c12, scale=0.9), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(q_, shift=UP * 0.2) for q_ in twelve], lag_ratio=0.06), run_time=0.8)
        self.until(word_time("s066", word_index("s066", "What")) - 0.1)
        q = T("what next?", 34, INK2).next_to(c12, DOWN, buff=0.5)
        q.next_to(twelve, DOWN, buff=0.4)
        self.play(FadeIn(t1, shift=LEFT * 0.4), FadeIn(q), run_time=0.6)
        # ── s067 test again: posterior becomes prior ──
        self.at("s067", 0.0)
        t2 = tube(AQUA).next_to(t1, RIGHT, buff=0.4)
        ta = T("test again", 30, AQUA, weight=BOLD).next_to(VGroup(t1, t2), DOWN, buff=0.35)
        self.play(FadeIn(t2, shift=LEFT * 0.3), FadeIn(ta), FadeOut(q), run_time=0.6)
        self.until(word_time("s067", word_index("s067", "answer")) - 0.1)
        post = pill("posterior: 1 in 12", VIOLET, 34).move_to(RIGHT * 3.0 + UP * 0.4)
        prio = pill("new prior: 1 in 12", WARN, 34).move_to(LEFT * 3.0 + UP * 0.4)
        self.play(FadeOut(VGroup(t1, t2, ta, twelve)), ReplacementTransform(c12, post), run_time=0.8)
        lp = loop_arrows(prio, post, VIOLET, WARN)
        self.play(Create(lp[0]), run_time=0.6)
        self.play(TransformFromCopy(post, prio), run_time=0.7)
        self.play(Create(lp[1]), run_time=0.6)
        # ── s068 yesterday's posterior is today's prior ──
        self.at("s068", 0.0)
        mot = T("yesterday's posterior is today's prior", 36, INK, weight=BOLD).next_to(lp, DOWN, buff=0.45)
        self.play(Write(mot), run_time=1.0)
        self.play(ShowPassingFlash(lp[0].copy().set_stroke(INK, 8), time_width=0.4), run_time=0.8)
        self.play(ShowPassingFlash(lp[1].copy().set_stroke(INK, 8), time_width=0.4), run_time=0.8)
        # ── s069 the 108 positives take a second test ──
        self.at("s069", 0.0)
        self.play(FadeOut(VGroup(prio, post, lp, mot)), run_time=0.5)
        sg = stacks_axes(); sg.move_to(LEFT * 2.6 + UP * 0.25)
        sax = sg.ax
        s9, s99 = stack(sax, 0.6, 9, ORANGE_), stack(sax, 1.4, 99, BLUE_)
        l9 = TB("9", 40, ORANGE_).next_to(s9, UP, buff=0.15); l99 = TB("99", 40, BLUE_).next_to(s99, UP, buff=0.15)
        c9 = T("have it", 24, ORANGE_).next_to(sax.c2p(0.6, 0), DOWN, buff=0.2)
        c99 = T("healthy", 24, BLUE_).next_to(sax.c2p(1.4, 0), DOWN, buff=0.2)
        self.play(FadeIn(sg), FadeIn(s9, lag_ratio=0.05), FadeIn(s99, lag_ratio=0.005), FadeIn(VGroup(l9, l99, c9, c99)), run_time=1.0)
        tt = VGroup(tube(AQUA, 1.2, 0.4), T("second test", 30, AQUA, weight=BOLD)).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.6 + UP * 0.8)
        self.until(word_time("s069", word_index("s069", "They")) - 0.1)
        self.play(FadeIn(tt, shift=LEFT * 0.3), run_time=0.6)
        # ── s070 ten times as many ──
        self.at("s070", 0.0)
        x10 = pill("× 10  (no fractions of people)", INK, 30).move_to(RIGHT * 3.6 + DOWN * 0.4)
        self.play(FadeIn(x10, scale=1.2), run_time=0.5)
        bg = stacks_axes(1200, 200, title="people (× 10)"); bg.move_to(sg)
        bax = bg.ax
        b90, b990 = bar(bax, 0.6, 90, ORANGE_), bar(bax, 1.4, 990, BLUE_)
        n90 = TB("90", 40, ORANGE_).next_to(b90, UP, buff=0.15); n990 = TB("990", 40, BLUE_).next_to(b990, UP, buff=0.15)
        c90 = T("have it", 24, ORANGE_).next_to(bax.c2p(0.6, 0), DOWN, buff=0.2)
        c990 = T("healthy", 24, BLUE_).next_to(bax.c2p(1.4, 0), DOWN, buff=0.2)
        self.until(word_time("s070", word_index("s070", "Ninety")) - 0.3)
        self.play(ReplacementTransform(sg, bg), ReplacementTransform(s9, b90), ReplacementTransform(s99, b990),
                  ReplacementTransform(l9, n90), ReplacementTransform(l99, n990), ReplacementTransform(c9, c90),
                  ReplacementTransform(c99, c990), run_time=1.2)
        # ── s071 the test catches 9 in 10 of the sick, flags 1 in 10 of the healthy ──
        self.at("s071", 0.0)
        k81 = bar(bax, 0.6, 81, ORANGE_, opacity=1).set_stroke(AQUA, 4)
        k99 = bar(bax, 1.4, 99, BLUE_, opacity=1).set_stroke(AQUA, 4)
        self.play(FadeOut(x10), b90.animate.set_fill(opacity=0.25), FadeIn(k81), run_time=0.7)
        r1 = T("90 → 81 test positive", 30, ORANGE_).move_to(RIGHT * 3.6 + DOWN * 0.3)
        self.play(FadeIn(r1), run_time=0.4)
        self.until(word_time("s071", word_index("s071", "wrongly")) - 0.1)
        self.play(b990.animate.set_fill(opacity=0.25), FadeIn(k99), run_time=0.7)
        r2 = T("990 → 99 test positive", 30, BLUE_).next_to(r1, DOWN, buff=0.3)
        self.play(FadeIn(r2), run_time=0.4)
        # ── s072 81 vs 99 ──
        self.at("s072", 0.0)
        sg2 = stacks_axes(); sg2.move_to(LEFT * 2.6 + UP * 0.25)
        ax2 = sg2.ax
        s81, s99b = stack(ax2, 0.6, 81, ORANGE_), stack(ax2, 1.4, 99, BLUE_)
        l81 = TB("81", 40, ORANGE_).next_to(s81, UP, buff=0.15); l99b = TB("99", 40, BLUE_).next_to(s99b, UP, buff=0.15)
        c81 = T("have it", 24, ORANGE_).next_to(ax2.c2p(0.6, 0), DOWN, buff=0.2)
        c99b = T("healthy", 24, BLUE_).next_to(ax2.c2p(1.4, 0), DOWN, buff=0.2)
        old = VGroup(bg, b90, b990, k81, k99, n90, n990, c90, c990, r1, r2, tt)
        self.play(FadeOut(old), FadeIn(sg2), run_time=0.6)
        self.play(LaggedStart(FadeIn(s81, lag_ratio=0.01), FadeIn(s99b, lag_ratio=0.01), lag_ratio=0.3),
                  FadeIn(VGroup(l81, l99b, c81, c99b)), run_time=1.2)
        lv = T("nearly level", 28, INK2).move_to(RIGHT * 3.4 + UP * 1.8)
        self.play(FadeIn(lv), run_time=0.4)
        # ── s073 81 / 180 = 45% ──
        self.at("s073", 0.0)
        f = MathTex(r"{81", r"\over", r"180}", "=", r"45\%", font_size=80)
        f[0].set_color(ORANGE_); f[4].set_color(VIOLET)
        f.move_to(RIGHT * 3.4 + UP * 0.3)
        self.play(FadeOut(lv), Write(f[:3]), run_time=0.8)
        self.until(word_time("s073", word_index("s073", "forty")) - 0.1)
        self.play(Write(f[3:]), run_time=0.6)
        self.play(Circumscribe(f[4], color=VIOLET), run_time=0.8)
        # ── s074 1 → 8 → 45 walk ──
        self.at("s074", 0.0)
        self.play(FadeOut(VGroup(sg2, s81, s99b, l81, l99b, c81, c99b, f)), run_time=0.5)
        mt = meter(11.5).move_to(DOWN * 0.6)
        self.play(FadeIn(mt), run_time=0.5)
        steps = [(1, WARN, "start 1%"), (8.33, VIOLET, "1 positive: 8%"), (45, VIOLET, "2 positives: 45%")]
        mks = VGroup()
        for k, (v, colr, lab) in enumerate(steps):
            m = marker(mt.nl, v, colr, lab, height=2.3 - 0.75 * k, fs=28)
            if k < 2:
                m.lab.shift(RIGHT * (m.lab.width / 2 - 0.3))
            mks.add(m)
            words = ["One", "eight", "forty"]
            self.until(word_time("s074", word_index("s074", words[k])) - 0.1)
            self.play(FadeIn(m, shift=DOWN * 0.3), run_time=0.5)
        # ── s075–s079 odds ──
        self.at("s075", 0.0)
        self.play(FadeOut(VGroup(mt, mks)), run_time=0.5)
        bs, th, PL, PR = beam_scale(4.0)
        bs.move_to(LEFT * 3.5 + UP * 0.6)
        ll = pill("sick", ORANGE_, 28); lr = pill("healthy", BLUE_, 28)
        ll.add_updater(lambda m: m.next_to(PL[0], DOWN, buff=0.15)); lr.add_updater(lambda m: m.next_to(PR[0], DOWN, buff=0.15))
        hd = T("odds = sick : healthy", 34, INK, weight=BOLD).move_to(RIGHT * 2.4 + UP * 2.55)
        self.play(FadeIn(bs), FadeIn(ll), FadeIn(lr), Write(hd), run_time=0.9)
        # s076 1 : 99
        self.at("s076", 0.0)
        rows = VGroup()
        def orow(a, b, col=INK):
            return VGroup(TB(a, 44, ORANGE_), TB(":", 44, MUTED), TB(b, 44, BLUE_)).arrange(RIGHT, buff=0.2)
        r0 = orow("1", "99").move_to(RIGHT * 1.4 + UP * 1.55)
        tag0 = T("before any test", 24, WARN).next_to(r0, RIGHT, buff=0.4)
        self.play(FadeIn(r0, shift=DOWN * 0.2), FadeIn(tag0), th.animate.set_value(odds_theta(1, 99)), run_time=0.9)
        # s077 likelihood ratio 9
        self.at("s077", 0.0)
        lr9 = VGroup(T("90% ÷ 10% = 9", 34, AQUA, weight=BOLD), T("likelihood ratio", 24, AQUA)).arrange(DOWN, buff=0.12)
        lr9.move_to(LEFT * 3.5 + DOWN * 2.05)
        self.until(word_time("s077", word_index("s077", "Ninety")) - 0.2)
        self.play(FadeIn(lr9, shift=UP * 0.2), run_time=0.6)
        # s078 × 9, × 9
        self.at("s078", 0.0)
        r1_ = orow("9", "99").next_to(r0, DOWN, buff=0.6).align_to(r0, LEFT)
        r2_ = orow("81", "99").next_to(r1_, DOWN, buff=0.6).align_to(r0, LEFT)
        x1 = T("× 9", 28, AQUA, weight=BOLD).next_to(VGroup(r0, r1_), LEFT, buff=0.35)
        x2 = T("× 9", 28, AQUA, weight=BOLD).next_to(VGroup(r1_, r2_), LEFT, buff=0.35)
        self.until(word_time("s078", word_index("s078", "becomes")) - 0.2)
        self.play(FadeIn(x1), TransformFromCopy(r0, r1_), th.animate.set_value(odds_theta(9, 99)), run_time=0.9)
        self.until(word_time("s078", word_index("s078", "then")) - 0.1)
        self.play(FadeIn(x2), TransformFromCopy(r1_, r2_), th.animate.set_value(odds_theta(81, 99)), run_time=0.9)
        # s079 third positive: 729 : 99 ≈ 88%
        self.at("s079", 0.0)
        r3_ = orow("729", "99").next_to(r2_, DOWN, buff=0.6).align_to(r0, LEFT)
        x3 = T("× 9", 28, AQUA, weight=BOLD).next_to(VGroup(r2_, r3_), LEFT, buff=0.35)
        self.play(FadeIn(x3), TransformFromCopy(r2_, r3_), th.animate.set_value(odds_theta(729, 99)), run_time=0.9)
        p88 = MathTex(r"{729 \over 828}", r"\approx", r"88\%", font_size=50, color=VIOLET).next_to(r3_, RIGHT, buff=0.5)
        self.until(word_time("s079", word_index("s079", "About")) - 0.1)
        self.play(Write(p88), run_time=0.7)
        self.play(Indicate(ll, color=ORANGE_), run_time=0.6)
        # ── s080 assumption: independent errors ──
        self.at("s080", 0.0)
        ll.clear_updaters(); lr.clear_updaters()
        self.play(FadeOut(VGroup(bs, ll, lr, hd, r0, tag0, r1_, r2_, r3_, x1, x2, x3, p88, lr9)), run_time=0.5)
        a_t = T("Assumption", 40, INK, weight=BOLD)
        a_s = T("the second test's mistakes are independent of the first", 30, INK2)
        a_box = card(a_s.width + 1.0, 2.0, INK).move_to(UP * 0.6)
        a_t.move_to(a_box.get_top() + DOWN * 0.55); a_s.next_to(a_t, DOWN, buff=0.35)
        self.play(FadeIn(a_box), FadeIn(a_t), run_time=0.5)
        self.until(word_time("s080", word_index("s080", "only")) - 0.1)
        self.play(Write(a_s), run_time=1.2)
        # ── s081 same test, same sample: same false alarm ──
        self.at("s081", 0.0)
        self.play(FadeOut(VGroup(a_box, a_t, a_s)), run_time=0.4)
        ta1, ta2 = tube(BLUE_), tube(BLUE_)
        for t_ in (ta1, ta2):
            sm = Dot(radius=0.09, color=RED_).move_to(t_[0].get_center() + UP * 0.2)
            t_.add(sm)
        pair = VGroup(ta1, ta2).arrange(RIGHT, buff=2.6).move_to(LEFT * 2.6 + UP * 0.5)
        lb1 = T("same test", 26, INK2).next_to(ta1, DOWN, buff=0.3)
        lb2 = T("same sample", 26, INK2).next_to(ta2, DOWN, buff=0.3)
        self.play(FadeIn(pair, shift=UP * 0.2), FadeIn(lb1), FadeIn(lb2), run_time=0.7)
        self.until(word_time("s081", word_index("s081", "repeat", )) + 1.0)
        sm_l = T("same smudge, same false alarm", 28, RED_).next_to(VGroup(lb1, lb2), DOWN, buff=0.35)
        self.play(Indicate(ta1[2], color=RED_, scale_factor=2), Indicate(ta2[2], color=RED_, scale_factor=2), FadeIn(sm_l), run_time=0.9)
        self.until(word_time("s081", word_index("s081", "Then")) - 0.1)
        one = VGroup(TB("= 1 clue", 50, INK), T("not 2", 32, RED_)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.4 + UP * 0.5)
        self.play(FadeIn(one, shift=LEFT * 0.3), run_time=0.6)
        # ── s082 confirm with a different kind of test ──
        self.at("s082", 0.0)
        alt = VGroup(Circle(radius=0.55).set_stroke(INK2, 4), Circle(radius=0.3).set_stroke(width=0).set_fill(VIOLET, 0.8))
        alt.move_to(ta2[0].get_center())
        lb3 = T("a different method", 26, AQUA).next_to(alt, DOWN, buff=0.3).set_y(lb2.get_y())
        self.play(FadeOut(VGroup(one, sm_l)), ReplacementTransform(ta2, alt), ReplacementTransform(lb2, lb3), run_time=0.9)
        two = VGroup(TB("2 real clues", 46, AQUA)).move_to(RIGHT * 3.4 + UP * 0.5)
        self.play(FadeIn(two, shift=LEFT * 0.3), run_time=0.5)
        self.until(SEGS["s082"]["end"] + 0.4)
        self.play(FadeOut(VGroup(ta1, alt, lb1, lb3, two)), run_time=0.4)
        self.finish()
