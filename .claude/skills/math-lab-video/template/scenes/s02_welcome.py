import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

# FILL: the topic title card (identical to the one that ends the hook scene) and the three previews.
TITLE = ("TOPIC NAME", "explained simply, with real examples")
PREVIEWS = [  # (number colour, caption)  -- one per "Today you will learn" sentence
    (AQUA, "first thing you will learn"),
    (VIOLET, "second thing you will learn"),
    (ORANGE_, "third thing you will learn"),
]


def preview_visual(k):
    """FILL: a small visual (fits roughly 9 x 3 units, centred near UP*0.2) from the running example for preview k."""
    return VGroup(RoundedRectangle(corner_radius=0.2, width=4, height=2).set_stroke(INK2, 3),
                  T(f"preview {k + 1}", 30, INK2))


class S02Welcome(Base):
    CHAPTER = "Welcome"

    def construct(self):
        seg_welcome, *seg_items = self.ch["segs"]          # welcome line, then the three "you will learn" lines
        title = title_card(*TITLE)
        self.add(title)
        # ── "Welcome to Math Lab TV. Where math is something you can see." (word for word) ──
        self.at(seg_welcome, 0.0)
        lg = logo(1.15, tagline=True).move_to(UP * 0.4)
        mark, name, tag = lg[0][0], lg[0][1], lg[1]
        self.play(FadeOut(title, scale=0.85), run_time=0.5)
        self.play(DrawBorderThenFill(mark[0]), run_time=0.6)
        self.play(Create(mark[1]), FadeIn(name, shift=LEFT * 0.3), run_time=0.8)
        self.until(word_time(seg_welcome, word_index(seg_welcome, "where")) - 0.1)
        self.play(AddTextLetterByLetter(tag), run_time=1.2)
        # ── numbered preview 1, 2, 3; small logo stays top-right ──
        small = logo(0.42).to_edge(UP, buff=0.32).to_edge(RIGHT, buff=0.45)
        learn = T("TODAY YOU WILL LEARN", 24, MUTED, weight=BOLD).next_to(small, LEFT, buff=0.5)
        prev = None
        for k, sid in enumerate(seg_items[:3]):
            self.at(sid, 0.0)
            col, cap = PREVIEWS[k]
            num = TB(str(k + 1), 72, col).move_to(UP * 2.45)
            vis = preview_visual(k).move_to(UP * 0.2)
            c_ = T(cap, 34, INK).move_to(DOWN * 2.0)
            if k == 0:
                self.play(ReplacementTransform(lg[0], small), FadeOut(tag), FadeIn(learn), run_time=0.8)
            else:
                self.play(FadeOut(prev, shift=LEFT * 1.0), run_time=0.5)
            self.play(FadeIn(num, scale=0.5), FadeIn(vis), FadeIn(c_), run_time=0.9)
            prev = VGroup(num, vis, c_)
        self.until(SEGS[seg_items[-1]]["end"] + 0.1)
        self.play(FadeOut(VGroup(small, learn, prev)), run_time=0.4)
        self.finish()
