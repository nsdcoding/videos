import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class S09Recipe(Base):
    CHAPTER = "Recipe"

    def construct(self):
        # ── s155 recipe card ──
        self.at("s155", 0.0)
        frame = RoundedRectangle(corner_radius=0.25, width=13.8, height=6.1, stroke_color=AQUA, stroke_width=3,
                                 fill_color="#20201e", fill_opacity=1).move_to(UP * 0.3)
        frame.qa_container = True
        title = TB("RECIPE: mean or median?", 38, AQUA).move_to(frame.get_top() + DOWN * 0.45)
        self.play(GrowFromEdge(frame, UP), run_time=0.8)
        self.play(Write(title), run_time=0.8)
        items = [
            ("Sort the values", "smallest → largest", INK),
            ("Find the mean", "add them all up, then divide by how many", WARN),
            ("Find the median", "the middle value · even count: halfway between the middle two", VIOLET),
            ("Compare them", "close → fairly balanced · mean much bigger → big values pulling it up", INK),
            ("Match your question", "totals & fair shares → mean · a typical one → median · unsure → report both", AQUA),
        ]
        rows = VGroup()
        for i, (head, sub, col) in enumerate(items):
            num = VGroup(Circle(0.28, color=AQUA, fill_color=AQUA, fill_opacity=1), T(str(i + 1), 28, BG, weight=BOLD))
            num[0].qa_container = True
            txt = VGroup(T(head, 30, col, weight=BOLD), T(sub, 23, INK2)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            r = VGroup(num, txt).arrange(RIGHT, buff=0.35)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(title, DOWN, buff=0.35).align_to(frame, LEFT).shift(RIGHT * 0.6)
        sids = ["s156", "s157", "s158", "s159", "s160"]
        for r, sid in zip(rows, sids):
            self.at(sid, 0.0)
            self.play(FadeIn(r[0], scale=0.5), FadeIn(r[1], shift=RIGHT * 0.3), run_time=0.6)
            self.play(Indicate(r[0], color=WARN, scale_factor=1.2), run_time=0.5)
        # ── s161 Pine Hill answer ──
        self.at("s161", 0.0)
        self.play(FadeOut(VGroup(rows, title)), run_time=0.5)
        ph = TB("Pine Hill", 40, INK).move_to(UP * 2.4)
        a = VGroup(glow(TB("mean 60", 64, WARN), WARN), T("fair share", 28, WARN)).arrange(DOWN, buff=0.2)
        b = VGroup(glow(TB("median 40", 64, VIOLET), VIOLET), T("typical family", 28, VIOLET)).arrange(DOWN, buff=0.2)
        ab = VGroup(a, b).arrange(RIGHT, buff=1.6).move_to(UP * 0.7)
        bar = Line(UP * 0.6, DOWN * 0.6, color=MUTED).move_to(ab)
        self.play(FadeIn(ph), FadeIn(a, shift=RIGHT * 0.3), run_time=0.6)
        self.until(word_time("s161", word_index("s161", "median")) - 0.2)
        self.play(FadeIn(bar), FadeIn(b, shift=LEFT * 0.3), run_time=0.6)
        both = T("both correct · they answer different questions", 30, INK2).move_to(DOWN * 1.2)
        self.until(word_time("s161", word_index("s161", "both")))
        self.play(FadeIn(both, shift=UP * 0.2), run_time=0.6)
        # ── s162 the line ──
        self.at("s162", 0.0)
        self.play(FadeOut(VGroup(ph, a, b, bar, both, frame)), run_time=0.5)
        line = VGroup(T("An average only lies", 56, VIOLET, weight=BOLD), T("when you ask it the wrong question.", 56, VIOLET, weight=BOLD)).arrange(DOWN, buff=0.3)
        line.move_to(UP * 0.3)
        g = glow(line, VIOLET, layers=5, width=10, opacity=0.05)
        self.play(AddTextLetterByLetter(line[0]), run_time=1.2)
        self.play(AddTextLetterByLetter(line[1]), run_time=1.5)
        self.remove(line); self.add(g)
        self.until(SEGS["s162"]["end"] + 0.7)
        self.play(FadeOut(g), run_time=0.5)
        self.finish()
