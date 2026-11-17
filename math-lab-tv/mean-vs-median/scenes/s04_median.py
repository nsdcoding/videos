import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def strike(t):
    return Line(t.get_corner(DL) + DL * 0.04, t.get_corner(UR) + UR * 0.04, color=INK2, stroke_width=4)


class S04Median(Base):
    CHAPTER = "The Median"

    def cross_pairs(self, row, pairs, sid, words, rt=0.45):
        marks = VGroup()
        for (i, j), w in zip(pairs, words):
            if w is not None:
                self.until(word_time(sid, w) - 0.05)
            a, b = strike(row[i]), strike(row[j])
            self.play(Create(a), Create(b), row[i].animate.set_opacity(0.3), row[j].animate.set_opacity(0.3),
                      self.wl.animate.next_to(row[i + 1], DOWN, buff=0.15), self.wr.animate.next_to(row[j - 1], DOWN, buff=0.15),
                      run_time=rt)
            marks.add(a, b)
        return marks

    def construct(self):
        fr = self.camera.frame
        # ── s061 MEDIAN ──
        self.at("s061", 0.5)
        word = glow(TB("MEDIAN", 140, VIOLET), VIOLET).move_to(UP * 0.9)
        self.play(Write(word[1]), FadeIn(word[0]), run_time=1.0)
        # ── s062 definition ──
        self.at("s062", 0.0)
        dfn = VGroup(T("median", 44, VIOLET, weight=BOLD), T("=", 44, MUTED), T("the middle value", 44, INK)).arrange(RIGHT, buff=0.3)
        aft = T("(after putting the values in order)", 32, INK2)
        dg = VGroup(dfn, aft).arrange(DOWN, buff=0.25).next_to(word, DOWN, buff=0.5)
        self.play(word.animate.scale(0.6).shift(UP * 0.7), FadeIn(dfn, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(aft), run_time=0.5)
        # ── s063 sort ──
        self.at("s063", 0.0)
        self.play(FadeOut(VGroup(word, dg)), run_time=0.5)
        step1 = chip("step 1: sort", INK, 30).to_edge(UP, buff=0.4).shift(RIGHT * 4.6)
        street = tiles(STREET).move_to(UP * 1.6)
        lab = T("in street order", 26, MUTED).next_to(street, UP, buff=0.6)
        self.play(FadeIn(step1), LaggedStart(*[FadeIn(t, shift=DOWN * 0.4) for t in street], lag_ratio=0.06), FadeIn(lab),
                  run_time=1.0)
        target = tiles(PINE).move_to(UP * 1.6)
        order = sorted(range(9), key=lambda i: STREET[i])
        self.at("s063", 2.2)
        lab2 = T("sorted: smallest → largest", 26, MUTED).next_to(target, UP, buff=0.6)
        self.play(*[street[i].animate.move_to(target[k]) for k, i in enumerate(order)],
                  Transform(lab, lab2), run_time=1.6, path_arc=0.8)
        row = VGroup(*[street[i] for i in order])
        # ── s064 read them out ──
        self.at("s064", 0.0)
        ws = [x.strip(",.").lower() for x in SEGS["s064"]["text"].split()]
        starts = [i for i, w in enumerate(ws) if w in ("thirty", "thirty-two", "thirty-five", "thirty-eight", "forty",
                                                        "forty-two", "forty-five", "forty-eight", "two")]
        for k, t in enumerate(row):
            self.until(word_time("s064", starts[k]) - 0.05)
            self.play(t.animate.shift(UP * 0.15), rate_func=there_and_back, run_time=0.35)
        # ── s065 walkers ──
        self.at("s065", 0.0)
        step2 = chip("step 2: find the middle", INK, 30).move_to(step1)
        self.wl = Triangle(color=INK, fill_opacity=1).scale(0.14).next_to(row[0], DOWN, buff=0.15)
        self.wr = Triangle(color=INK, fill_opacity=1).scale(0.14).next_to(row[8], DOWN, buff=0.15)
        self.play(Transform(step1, step2), FadeIn(self.wl, shift=UP * 0.2), FadeIn(self.wr, shift=UP * 0.2), run_time=0.7)
        # ── s066 cross off pairs ──
        self.at("s066", 0.0)
        ws = [x.strip(",.").lower() for x in SEGS["s066"]["text"].split()]
        pw = [ws.index("thirty"), ws.index("thirty-two"), ws.index("thirty-five"), ws.index("thirty-eight")]
        marks = self.cross_pairs(row, [(0, 8), (1, 7), (2, 6), (3, 5)], "s066", pw)
        # ── s067 forty remains ──
        self.at("s067", 0.6)
        mid = row[4]
        self.play(FadeOut(self.wl), FadeOut(self.wr), mid.animate.shift(UP * 0.35), run_time=0.4)
        self.play(*hl(mid, VIOLET), run_time=0.3)
        gl = glow(mid[1].copy(), VIOLET)
        for m in gl.get_family(): m.qa_ignore = True
        self.play(FadeIn(gl), Flash(mid, color=VIOLET, line_length=0.3), run_time=0.6)
        # ── s068 median = 40 on the number line ──
        self.at("s068", 0.0)
        ax = money_axis(); ax.shift(DOWN * 0.75 - ax.axis.get_center()); L = ax.axis
        dots = dot_plot(PINE, L, [BLUE_] * 4 + [VIOLET] + [BLUE_] * 3 + [ORANGE_], r=0.1)
        card = glow(T("median = 40", 40, VIOLET, weight=BOLD), VIOLET).move_to(UP * 0.55 + LEFT * 0.6)
        self.play(FadeIn(ax), LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in dots], lag_ratio=0.05), run_time=1.0)
        dm = diamond(L, 40, VIOLET, height=1.1)
        self.play(FadeIn(card, shift=UP * 0.2), FadeIn(dm, shift=DOWN * 0.3), run_time=0.7)
        # ── s069 four below, four above ──
        self.at("s069", 0.0)
        self.play(FadeOut(VGroup(row, marks, gl, lab, step1, card)), run_time=0.6)
        self.play(fr.animate.scale(0.6).move_to([L.n2p(40)[0], -0.2, 0]), run_time=0.9)
        sh_l = Rectangle(width=L.n2p(40)[0] - L.n2p(27)[0], height=0.85, stroke_width=0, fill_color=BLUE_, fill_opacity=0.18)
        sh_l.move_to(L.n2p(27), aligned_edge=LEFT).shift(UP * 0.42 + RIGHT * 0.0)
        sh_r = Rectangle(width=L.n2p(53)[0] - L.n2p(40)[0], height=0.85, stroke_width=0, fill_color=ORANGE_, fill_opacity=0.18)
        sh_r.move_to(L.n2p(40), aligned_edge=LEFT).shift(UP * 0.42)
        for r in (sh_l, sh_r): r.qa_ignore = True
        tb = T("4 below", 30, BLUE_).next_to(sh_l, LEFT, buff=0.2)
        ta = T("4 above", 30, ORANGE_).next_to(sh_r, RIGHT, buff=0.2)
        self.play(FadeIn(sh_l), FadeIn(tb, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeIn(sh_r), FadeIn(ta, shift=LEFT * 0.2), run_time=0.6)
        promise = T("it splits the group in half", 30, VIOLET).move_to([L.n2p(40)[0], 1.25, 0])
        self.at("s069", word_time("s069", word_index("s069", "splits")) - SEGS["s069"]["start"] - 0.3)
        self.play(FadeIn(promise, shift=UP * 0.2), run_time=0.6)
        # ── s070 vs the mean ──
        self.at("s070", 0.0)
        self.play(FadeOut(VGroup(sh_l, sh_r, tb, ta, promise)), fr.animate.scale(1 / 0.6).move_to(ORIGIN), run_time=0.9)
        mm = marker(L, 60, WARN, "", height=0.85)
        ml = VGroup(T("mean 60:", 30, WARN, weight=BOLD), T("8 below", 30, BLUE_), T("|", 30, MUTED), T("1 above", 30, ORANGE_)).arrange(RIGHT, buff=0.2)
        dl = VGroup(T("median 40:", 30, VIOLET, weight=BOLD), T("4 below", 30, BLUE_), T("|", 30, MUTED), T("4 above", 30, ORANGE_)).arrange(RIGHT, buff=0.2)
        cmp_ = VGroup(dl, ml).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 2.0 + RIGHT * 2.0)
        self.play(FadeIn(mm, shift=DOWN * 0.3), run_time=0.6)
        self.play(FadeIn(dl, shift=LEFT * 0.3), run_time=0.6)
        self.play(FadeIn(ml, shift=LEFT * 0.3), run_time=0.6)
        # ── s071 Maple: both at 60 ──
        self.at("s071", 0.0)
        mdots = dot_plot(MAPLE, L, [INK] * 9, r=0.1)
        mt = TB("Maple", 40).move_to(UP * 2.3 + LEFT * 4.6)
        mmed = diamond(L, 60, VIOLET, height=1.6)
        mmean = marker(L, 60, WARN, "", height=1.2)
        both = T("mean = median = 60", 32, INK, weight=BOLD).next_to(mmed, UP, buff=0.2)
        both[:4].set_color(WARN); both[5:11].set_color(VIOLET)
        self.play(FadeOut(VGroup(dots, dm, mm, cmp_)), FadeIn(mt), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in mdots], lag_ratio=0.05), run_time=0.8)
        self.play(FadeIn(mmean, shift=DOWN * 0.2), FadeIn(mmed, shift=DOWN * 0.2), FadeIn(both), run_time=0.7)
        # ── s072 50th percentile ──
        self.at("s072", 0.0)
        self.play(FadeOut(VGroup(mdots, mt, mmed, mmean, both, ax)), run_time=0.5)
        row2 = tiles(PINE).move_to(UP * 0.3)
        ruler = NumberLine(x_range=[0, 100, 10], length=row2.width, include_tip=False, color=INK2, tick_size=0.08)
        ruler.next_to(row2, UP, buff=0.45)
        rl = VGroup(*[T(f"{v}%", 20, INK2).next_to(ruler.n2p(v), UP, buff=0.12) for v in range(0, 101, 25)])
        rt = T("position in the sorted list", 24, MUTED).next_to(rl, UP, buff=0.15)
        self.play(FadeIn(row2), Create(ruler), FadeIn(rl), FadeIn(rt), run_time=1.0)
        self.play(*hl(row2[4], VIOLET), run_time=0.5)
        ptr = Line(ruler.n2p(50), row2[4].get_top(), color=VIOLET, stroke_width=4)
        p50 = glow(TB("p50", 48, VIOLET), VIOLET).next_to(row2, DOWN, buff=0.45)
        p50t = T("50th percentile = median", 30, INK).next_to(p50, RIGHT, buff=0.35)
        self.play(Create(ptr), run_time=0.5)
        self.play(FadeIn(p50, shift=UP * 0.2), FadeIn(p50t), run_time=0.7)
        # ── s073 even count? ──
        self.at("s073", 0.0)
        self.play(FadeOut(VGroup(ruler, rl, rt, ptr, p50, p50t)), *unhl(row2[4], BLUE_), run_time=0.5)
        qq = TB("even number of values?", 40, INK).move_to(UP * 2.2)
        self.play(FadeIn(qq, shift=DOWN * 0.2), row2.animate.move_to(UP * 0.6), run_time=0.6)
        nomid = T("no single middle", 30, RED_).next_to(row2, DOWN, buff=0.5)
        # ── s074 a new family earning 50 ──
        self.at("s074", 0.0)
        new = tile(50, AQUA).next_to(row2, DOWN, buff=1.0)
        hs = house(0.6, AQUA).next_to(new, LEFT, buff=0.3)
        self.play(FadeOut(qq), FadeIn(VGroup(hs, new), shift=LEFT * 0.6), run_time=0.7)
        row10 = tiles(PINE[:8] + [50, 230], colors=[BLUE_] * 8 + [AQUA, ORANGE_]).move_to(UP * 0.6)
        self.play(*[row2[i].animate.move_to(row10[i]) for i in range(8)], row2[8].animate.move_to(row10[9]),
                  new.animate.move_to(row10[8]), FadeOut(hs), run_time=1.0, path_arc=0.4)
        row = VGroup(*row2[:8], new, row2[8])
        # ── s075 n = 10 ──
        self.at("s075", 0.0)
        n10 = T("n = 10 households", 32, AQUA).move_to(UP * 2.2)
        self.play(FadeIn(n10, shift=DOWN * 0.2), run_time=0.5)
        # ── s076 cross off, two remain ──
        self.at("s076", 0.0)
        self.wl = Triangle(color=INK, fill_opacity=1).scale(0.14).next_to(row[0], DOWN, buff=0.15)
        self.wr = Triangle(color=INK, fill_opacity=1).scale(0.14).next_to(row[9], DOWN, buff=0.15)
        self.play(FadeIn(self.wl), FadeIn(self.wr), run_time=0.3)
        marks = self.cross_pairs(row, [(0, 9), (1, 8), (2, 7), (3, 6)], "s076", [None] * 4, rt=0.4)
        self.play(FadeOut(self.wl), FadeOut(self.wr), row[4].animate.shift(UP * 0.3), row[5].animate.shift(UP * 0.3), run_time=0.4)
        self.play(*hl(row[4], VIOLET), *hl(row[5], VIOLET), run_time=0.3)
        two = T("two middle values", 30, VIOLET).next_to(VGroup(row[4], row[5]), UP, buff=0.3)
        self.play(FadeIn(two), FadeOut(n10), run_time=0.5)
        # ── s077 halfway rule ──
        self.at("s077", 0.0)
        hf = MathTex(r"{40 + 42 \over 2}", font_size=84, color=INK).move_to(DOWN * 1.15 + LEFT * 4.0)
        self.play(FadeOut(two), FadeIn(hf, shift=DOWN * 0.3), run_time=0.9)
        # ── s078 = 41 ──
        self.at("s078", 0.0)
        hf2 = MathTex(r"{82 \over 2}", font_size=84, color=INK).move_to(hf)
        self.play(FadeTransform(hf, hf2), run_time=0.6)
        hf = hf2
        self.until(word_time("s078", word_index("s078", "forty-one")) - 0.2)
        e41 = glow(TB("= 41", 84, VIOLET), VIOLET).next_to(hf, RIGHT, buff=0.35)
        self.play(FadeIn(e41, shift=LEFT * 0.3), run_time=0.6)
        # ── s079 median = 41 ──
        self.at("s079", 0.0)
        c41 = T("median of 10 families = 41", 34, VIOLET, weight=BOLD).move_to(UP * 2.3)
        self.play(FadeIn(c41, shift=DOWN * 0.2), Circumscribe(e41, color=VIOLET), run_time=0.9)
        # ── s080 mean = 59 ──
        self.at("s080", 0.0)
        mf = MathTex(r"{590 \over 10}", font_size=84, color=INK).move_to(DOWN * 1.15 + RIGHT * 1.9)
        self.play(FadeIn(mf, shift=UP * 0.2), run_time=0.7)
        self.until(word_time("s080", word_index("s080", "fifty-nine")) - 0.2)
        e59 = glow(TB("= 59", 84, WARN), WARN).next_to(mf, RIGHT, buff=0.35)
        self.play(FadeIn(e59, shift=LEFT * 0.3), run_time=0.6)
        # ── s081 back to nine ──
        self.at("s081", 0.0)
        self.play(FadeOut(VGroup(hf, e41, mf, e59, c41, marks)), *[t.animate.set_opacity(1) for t in row], run_time=0.5)
        self.play(*unhl(row[4], BLUE_), *unhl(row[5], BLUE_), run_time=0.3)
        row[4].shift(DOWN * 0.3); row[5].shift(DOWN * 0.3)
        back = tiles(PINE).move_to(UP * 0.6)
        n9 = T("back to our 9 households", 32, INK).move_to(UP * 2.2)
        self.play(new.animate.shift(DOWN * 2.0).set_opacity(0), *[row[i].animate.move_to(back[i]) for i in range(8)],
                  row[9].animate.move_to(back[8]), FadeIn(n9), run_time=1.0)
        self.finish()
