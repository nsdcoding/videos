import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class S01bWelcome(Base):
    CHAPTER = "Welcome"

    def item(self, n, color, visual, caption):
        num = TB(str(n), 64, color).move_to(UP * 2.55)
        cap = T(caption, 32, INK).move_to(DOWN * 1.75)
        visual.move_to(UP * 0.45)
        return num, visual, cap

    def construct(self):
        # end state of scene 1, for a seamless cut
        wm = glow(TB("MEAN", 110, WARN), WARN); wd = glow(TB("MEDIAN", 110, VIOLET), VIOLET); vs = T("vs", 48, MUTED)
        row = VGroup(wm, vs, wd).arrange(RIGHT, buff=0.55).move_to(UP * 0.6)
        sub = T("Which average is lying to you?", 44, INK).move_to(DOWN * 1.0)
        title = VGroup(row, sub)
        self.add(title)
        # ── s017a welcome card ──
        self.at("s017a", 0.0)
        lg = logo(1.15, tagline=True).move_to(UP * 0.4)
        mark, name, tag = lg[0][0], lg[0][1], lg[1]
        self.play(FadeOut(title, scale=0.85), run_time=0.5)
        self.play(DrawBorderThenFill(mark[0]), run_time=0.6)
        self.play(Create(mark[1]), FadeIn(name, shift=LEFT * 0.3), run_time=0.8)
        self.until(word_time("s017a", word_index("s017a", "where")) - 0.1)
        self.play(AddTextLetterByLetter(tag), run_time=1.3)
        # ── s017b ① what mean & median are ──
        self.at("s017b", 0.0)
        small = logo(0.42).to_edge(UP, buff=0.32).to_edge(RIGHT, buff=0.45)
        learn = T("TODAY YOU WILL LEARN", 24, MUTED, weight=BOLD).next_to(small, LEFT, buff=0.5)
        self.play(ReplacementTransform(lg[0], small), FadeOut(tag), FadeIn(learn), run_time=0.8)
        F = MathTex(r"\bar{x}", "=", r"{\sum", r"x_i", r"\over", r"n}", font_size=90)
        F[0].set_color(WARN)
        tl = tiles(PINE, size=0.6, fs=22)
        tl[4][0].set_stroke(VIOLET).set_fill(VIOLET, 0.25); tl[4][1].set_color(VIOLET)
        vis1 = VGroup(F, tl).arrange(RIGHT, buff=0.8)
        n1, v1, c1 = self.item(1, VIOLET, vis1, "what the mean and the median are, and how to calculate them")
        self.play(FadeIn(n1, scale=0.5), Write(F), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.3) for t in tl], lag_ratio=0.06), FadeIn(c1), run_time=0.9)
        self.play(Indicate(tl[4], color=VIOLET), run_time=0.7)
        # ── s017c ② one family makes the average lie ──
        self.at("s017c", 0.0)
        ax = money_axis(length=9.0, font_size=20); ax.title.set_opacity(0)
        dots = dot_plot(PINE, ax.axis, [BLUE_] * 8 + [ORANGE_], r=0.09)
        mk = marker(ax.axis, 38.75, WARN, "mean", height=0.95, fs=24, label_dir=RIGHT)
        dm = diamond(ax.axis, 40, VIOLET, "median", height=1.55, fs=24, label_dir=LEFT)
        vis2 = VGroup(ax, dots, mk, dm)
        vis2.shift(UP * 0.1 - ax.axis.get_center())
        n2, _, c2 = self.item(2, ORANGE_, VGroup(), "why one rich family can make an average lie")
        self.play(FadeOut(VGroup(n1, vis1, c1), shift=LEFT * 1.0), FadeIn(n2, scale=0.5), run_time=0.6)
        self.play(FadeIn(VGroup(ax, dots[:8], mk, dm)), FadeIn(c2), run_time=0.6)
        self.add(dots[8])
        self.play(FadeIn(dots[8], shift=LEFT * 0.5), mk.animate.shift((ax.axis.n2p(60)[0] - mk.get_x()) * RIGHT), run_time=1.2)
        self.play(Flash(dots[8], color=ORANGE_, line_length=0.25), run_time=0.5)
        # ── s017d ③ pick the right one ──
        self.at("s017d", 0.0)
        def post(text, color):
            t = T(text, 32, color, weight=BOLD)
            b = RoundedRectangle(corner_radius=0.1, width=t.width + 0.6, height=0.8, stroke_color=color, stroke_width=3,
                                 fill_color="#22221f", fill_opacity=1)
            b.qa_container = True
            t.move_to(b)
            return VGroup(Line(b.get_bottom(), b.get_bottom() + DOWN * 1.0, color=INK2, stroke_width=5), b, t)
        p1, p2 = post("TOTALS → mean", WARN), post("TYPICAL → median", VIOLET)
        vis3 = VGroup(p1, p2).arrange(RIGHT, buff=1.4, aligned_edge=DOWN)
        n3, v3, c3 = self.item(3, AQUA, vis3, "how to pick the right one, every time")
        self.play(FadeOut(VGroup(n2, vis2, c2), shift=LEFT * 1.0), FadeIn(n3, scale=0.5), run_time=0.6)
        self.play(FadeIn(p1, shift=UP * 0.4), run_time=0.5)
        self.play(FadeIn(p2, shift=UP * 0.4), FadeIn(c3), run_time=0.5)
        self.until(SEGS["s017d"]["end"] + 0.25)
        self.play(FadeOut(VGroup(small, learn, n3, vis3, c3)), run_time=0.5)
        self.finish()
