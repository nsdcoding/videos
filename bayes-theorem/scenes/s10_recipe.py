import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

STEPS = [("Start with the base rate", "how common is it, before any evidence?", WARN),
         ("Picture a crowd", "e.g. 1,000 people: no fractions", INK),
         ("Split it with the test", "count true positives and false alarms", AQUA),
         ("Keep the matches and divide", "real cases ÷ all positives", VIOLET),
         ("Update", "the answer becomes the next base rate", INK)]


class S10Recipe(Base):
    CHAPTER = "Recipe"

    def construct(self):
        # ── s122 card frame ──
        self.at("s122", 0.0)
        title = TB("Bayes in five steps", 44, INK)
        rows = VGroup()
        heads = [T(h, 30, c, weight=BOLD) for h, d, c in STEPS]
        hw = max(h_.width for h_ in heads)
        for k, (h, d, c) in enumerate(STEPS):
            disc = Circle(radius=0.28, stroke_width=0, fill_color=c, fill_opacity=1); disc.qa_container = True
            n = TB(str(k + 1), 30, BG).move_to(disc)
            ht = heads[k]
            dt = T(d, 24, INK2)
            r = VGroup(VGroup(disc, n), ht, dt)
            VGroup(disc, n).move_to(ORIGIN)
            ht.next_to(disc, RIGHT, buff=0.3)
            dt.move_to(disc.get_center() + RIGHT * (0.28 + 0.3 + hw + 0.45), aligned_edge=LEFT)
            rows.add(VGroup(r[0], VGroup(ht, dt)))
        rows.arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        inner = VGroup(title, rows).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        frame_ = card(inner.width + 1.0, inner.height + 0.8, INK2)
        frame_.move_to(UP * 0.3); inner.move_to(frame_)
        fit = VGroup(frame_, inner)
        if fit.width > 12.4:
            fit.scale(12.4 / fit.width)
        fit.move_to(UP * 0.3)
        self.play(Create(frame_), run_time=0.8)
        self.play(Write(title), run_time=0.8)
        # ── s123–s127 items ──
        for k, sid in enumerate(["s123", "s124", "s125", "s126", "s127"]):
            self.at(sid, 0.0)
            r = rows[k]
            self.play(FadeIn(r[0], scale=0.5), FadeIn(r[1][0], shift=RIGHT * 0.2), run_time=0.6)
            self.until(SEGS[sid]["start"] + 0.45 * (SEGS[sid]["end"] - SEGS[sid]["start"]))
            self.play(FadeIn(r[1][1], shift=RIGHT * 0.2), run_time=0.5)
        # ── s128 our test ──
        self.at("s128", 0.0)
        whole = VGroup(frame_, inner)
        self.play(whole.animate.scale(0.66).move_to(UP * 1.0), run_time=0.8)
        strip = VGroup(T("1 in 100", 30, WARN, weight=BOLD), T("→", 30, MUTED),
                       T("9 real vs 99 false", 30, INK, weight=BOLD), T("→", 30, MUTED),
                       MathTex(r"{9 \over 108} \approx 8\%", font_size=46, color=VIOLET)).arrange(RIGHT, buff=0.25)
        strip.next_to(whole, DOWN, buff=0.3)
        for k, w in ((0, "one"), (2, "Nine"), (4, "About")):
            self.until(word_time("s128", word_index("s128", w)) - 0.15)
            self.play(*([FadeIn(strip[k - 1])] if k else []), FadeIn(strip[k], shift=RIGHT * 0.2), run_time=0.5)
        # ── s129 closing line ──
        self.at("s129", 0.0)
        self.play(FadeOut(VGroup(whole, strip)), run_time=0.5)
        l1 = TB("A test result is a clue, not a verdict.", 52, VIOLET)
        l2 = T("Bayes tells you how much the clue is worth.", 36, INK)
        close = VGroup(l1, l2).arrange(DOWN, buff=0.45).move_to(UP * 0.4)
        self.play(AddTextLetterByLetter(l1), run_time=1.6)
        self.until(word_time("s129", word_index("s129", "Bayes")) - 0.1)
        self.play(FadeIn(l2, shift=UP * 0.2), run_time=0.7)
        self.until(SEGS["s129"]["end"] + 1.4)
        self.play(FadeOut(close), run_time=0.5)
        self.finish()
