import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

NEXT_TOPIC = "next topic"   # FILL from `channel.py refs <slug>` -> tease_next (confirmed at checkpoint 1)


def teaser_visual(k):
    """FILL: one visual per teaser segment (except the last 'see you' line), tied to the running example."""
    return T(f"teaser beat {k + 1}", 34, AQUA)


class S91Next(Base):
    CHAPTER = "Next Time"

    def construct(self):
        lg = logo(1.1).move_to(UP * 1.1).scale(0.42).to_edge(UP, buff=0.32)   # carried over from Subscribe
        self.add(lg)
        segs = self.ch["segs"]
        prev = None
        for k, sid in enumerate(segs[:-1]):
            self.at(sid, 0.0)
            v = teaser_visual(k).move_to(UP * 0.3)
            self.play(*([FadeOut(prev)] if prev else []), FadeIn(v, shift=UP * 0.2), run_time=0.6)
            prev = v
            if k == len(segs) - 2:
                nx = chip(f"next:  {NEXT_TOPIC}", AQUA, 30).next_to(lg, DOWN, buff=0.3)
                self.play(FadeIn(nx, shift=DOWN * 0.2), run_time=0.6)
        # ── "I will see you in the next video." (word for word) ──
        self.at(segs[-1], 0.0)
        self.play(Indicate(nx, color=AQUA, scale_factor=1.08), run_time=1.0)
        self.finish()
