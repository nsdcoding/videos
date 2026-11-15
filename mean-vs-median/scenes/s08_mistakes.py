import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def card(text, w=3.9, h=0.85, face=True):
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=RED_, stroke_width=3,
                           fill_color="#2a1c1c" if face else "#3a2020", fill_opacity=1)
    box.qa_container = True
    t = T(text, 26, INK if face else RED_, weight=BOLD).move_to(box)
    if t.width > w - 0.3: t.scale_to_fit_width(w - 0.3)
    return VGroup(box, t)


def check(color=VIOLET):
    return VMobject(color=color, stroke_width=7).set_points_as_corners([LEFT * 0.2 + UP * 0.02, DOWN * 0.18, RIGHT * 0.3 + UP * 0.3])


def cross(color=RED_, s=0.22):
    return VGroup(Line(UL * s, DR * s), Line(UR * s, DL * s)).set_stroke(color, 7)


class S08Mistakes(Base):
    CHAPTER = "Common Mistakes"

    def flip(self, back, front):
        front.move_to(back)
        self.play(back.animate.stretch(0.02, 0), run_time=0.25)
        front.stretch(0.02, 0)
        self.remove(back); self.add(front)
        self.play(front.animate.stretch(50, 0), run_time=0.25)

    def construct(self):
        # ── s143 three face-down cards ──
        self.at("s143", 0.0)
        backs = VGroup(*[card(f"mistake {i}", face=False) for i in (1, 2, 3)]).arrange(RIGHT, buff=0.35).move_to(UP * 0.6)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.4) for b in backs], lag_ratio=0.2), run_time=1.0)
        fronts = [card("① taking the middle unsorted"), card("② “half are above average”"), card("③ deleting the outlier")]
        # ── s144 card 1 ──
        self.at("s144", 0.0)
        self.flip(backs[0], fronts[0])
        top = VGroup(fronts[0], backs[1], backs[2])
        self.play(top.animate.scale(0.72).to_edge(UP, buff=0.45).shift(RIGHT * 1.6), run_time=0.6)
        # ── s145 street order ──
        self.at("s145", 0.0)
        homes = VGroup(*[house(0.6, ORANGE_ if v > 100 else INK2, mansion=v > 100) for v in STREET]).arrange(RIGHT, buff=0.32, aligned_edge=DOWN)
        homes.move_to(DOWN * 1.1)
        street = Line(homes.get_corner(DL) + LEFT * 0.4, homes.get_corner(DR) + RIGHT * 0.4, color=GRID, stroke_width=4).shift(DOWN * 0.05)
        row = VGroup(*[tile(v, BLUE_ if v < 100 else ORANGE_, size=0.62, fs=24).next_to(h, UP, buff=0.3) for v, h in zip(STREET, homes)])
        self.play(Create(street), LaggedStart(*[FadeIn(h, shift=UP * 0.3) for h in homes], lag_ratio=0.06), run_time=1.0)
        k0 = word_index("s145", "forty-two")
        for i, t in enumerate(row):
            self.until(word_time("s145", k0 + (i if i < 8 else 9)) - 0.1)
            self.play(FadeIn(t, shift=DOWN * 0.2), run_time=0.3)
        # ── s146 middle house: 30 ──
        self.at("s146", 0.0)
        ring = Circle(0.5, color=RED_, stroke_width=5).move_to(row[4])
        self.play(Create(ring), *hl(row[4], RED_), run_time=0.6)
        x = cross().next_to(ring, UR, buff=-0.1)
        lab = T("just the middle house — not the median", 28, RED_).next_to(row, UP, buff=0.4)
        self.play(Create(x), FadeIn(lab), run_time=0.6)
        # ── s147 sort first ──
        self.at("s147", 0.0)
        target = tiles(PINE, size=0.62, fs=24).move_to(row)
        order = sorted(range(9), key=lambda i: STREET[i])
        self.play(FadeOut(VGroup(ring, x, lab)), *unhl(row[4], BLUE_), run_time=0.4)
        self.play(*[row[i].animate.move_to(target[k]) for k, i in enumerate(order)], path_arc=0.7, run_time=1.2)
        mid = row[order[4]]
        tick = check().next_to(mid, UP, buff=0.2)
        ok = T("sort first: the middle is 40", 28, VIOLET).next_to(tick, RIGHT, buff=0.3)
        self.play(*hl(mid, VIOLET), Create(tick), FadeIn(ok), run_time=0.7)
        # ── s148 card 2 ──
        self.at("s148", 0.0)
        self.play(FadeOut(VGroup(homes, street, row, tick, ok)), run_time=0.5)
        self.flip(backs[1], fronts[1].scale(0.72))
        # ── s149 median yes, mean no ──
        self.at("s149", 0.0)
        r1 = VGroup(T("half above the median", 34, VIOLET, weight=BOLD), check(VIOLET)).arrange(RIGHT, buff=0.4)
        r2 = VGroup(T("half above the mean", 34, WARN, weight=BOLD), cross(RED_)).arrange(RIGHT, buff=0.4)
        rr = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.7)
        self.play(FadeIn(r1, shift=RIGHT * 0.3), run_time=0.6)
        self.until(word_time("s149", word_index("s149", "not")))
        self.play(FadeIn(r2, shift=RIGHT * 0.3), run_time=0.6)
        # ── s150 one family above the mean ──
        self.at("s150", 0.0)
        ax = money_axis(); ax.shift(DOWN * 1.0 - ax.axis.get_center()); L = ax.axis
        dots = dot_plot(PINE, L, [BLUE_] * 8 + [ORANGE_])
        mk = marker(L, 60, WARN, "mean 60", height=0.85, fs=26, label_dir=RIGHT)
        self.play(rr.animate.scale(0.75).move_to(UP * 1.45 + LEFT * 3.2), FadeIn(ax), FadeIn(dots), FadeIn(mk), run_time=0.8)
        ab = T("1 of 9 above the mean", 30, ORANGE_, weight=BOLD).move_to([L.n2p(190)[0], 0.4, 0])
        be = T("8 of 9 below", 30, BLUE_, weight=BOLD).move_to([L.n2p(20)[0], 0.4, 0])
        self.play(FadeIn(be), Indicate(dots[:8], color=BLUE_), run_time=0.7)
        self.play(FadeIn(ab), Indicate(dots[8], color=ORANGE_, scale_factor=2), run_time=0.7)
        good = T("below average here = very good company", 26, INK2).move_to(UP * 2.05 + RIGHT * 3.4)
        self.until(word_time("s150", word_index("s150", "so")))
        self.play(FadeIn(good), run_time=0.5)
        # ── s151 card 3 ──
        self.at("s151", 0.0)
        self.play(FadeOut(VGroup(ax, dots, mk, ab, be, good, rr)), run_time=0.5)
        self.flip(backs[2], fronts[2].scale(0.72))
        # ── s152 the outlier is real ──
        self.at("s152", 0.0)
        mans = house(1.2, ORANGE_, mansion=True).move_to(LEFT * 3.0 + UP * 0.5)
        real = T("real family, real income", 30, ORANGE_).next_to(mans, DOWN, buff=0.35)
        coin = VGroup(Circle(0.75, color=WARN, fill_color="#3a3018", fill_opacity=1, stroke_width=5),
                      T("$4,600", 30, WARN, weight=BOLD)).move_to(RIGHT * 2.6 + UP * 0.5)
        coin[0].qa_container = True
        tx = T("of the town's tax budget", 28, WARN).next_to(coin, DOWN, buff=0.3)
        self.play(FadeIn(mans, shift=UP * 0.3), FadeIn(real), run_time=0.7)
        self.until(word_time("s152", word_index("s152", "town's")) - 0.4)
        self.play(GrowFromCenter(coin), FadeIn(tx), run_time=0.6)
        # ── s153 checklist ──
        self.at("s153", 0.0)
        self.play(FadeOut(VGroup(mans, real, coin, tx)), run_time=0.4)
        q = T("evidence it's an error? (like that extra zero)", 32, INK, weight=BOLD).move_to(UP * 1.1)
        y1 = VGroup(T("yes →", 30, AQUA, weight=BOLD), T("fix it", 30, AQUA)).arrange(RIGHT, buff=0.25)
        n1 = VGroup(T("no →", 30, VIOLET, weight=BOLD), T("keep it, and choose the average that fits your question", 30, VIOLET)).arrange(RIGHT, buff=0.25)
        opts = VGroup(y1, n1).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(q, DOWN, buff=0.5)
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(y1, shift=RIGHT * 0.2), run_time=0.5)
        self.until(word_time("s153", word_index("s153", "otherwise")))
        self.play(FadeIn(n1, shift=RIGHT * 0.2), run_time=0.6)
        # ── s154 bonus ──
        self.at("s154", 0.0)
        self.play(FadeOut(VGroup(q, opts)), run_time=0.4)
        bonus = T("bonus: even count", 32, RED_, weight=BOLD).move_to(UP * 1.3)
        t40, t42 = tile(40, BLUE_), tile(42, BLUE_)
        pair = VGroup(t40, t42).arrange(RIGHT, buff=0.3).move_to(LEFT * 2.6 + DOWN * 0.1)
        t41 = tile(41, VIOLET).move_to(RIGHT * 2.4 + DOWN * 0.1)
        arr = Arrow(pair.get_right(), t41.get_left(), buff=0.4, color=INK2)
        self.play(FadeIn(bonus), FadeIn(pair), run_time=0.6)
        c1 = cross().move_to(t40.get_corner(UR)); c2 = cross().move_to(t42.get_corner(UR))
        self.until(word_time("s154", word_index("s154", "picking")))
        self.play(Create(c1), Create(c2), run_time=0.5)
        self.until(word_time("s154", word_index("s154", "halfway")) - 0.2)
        tk = check().move_to(t41.get_corner(UR) + UR * 0.05)
        self.play(GrowArrow(arr), FadeIn(t41), *hl(t41, VIOLET), run_time=0.6)
        self.play(Create(tk), run_time=0.4)
        self.finish()
