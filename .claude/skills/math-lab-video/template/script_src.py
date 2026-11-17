#!/usr/bin/env python3
"""Source of truth for the narration. Run to emit script.json + script.md.

Running example (used everywhere; every number checked in verify_numbers.py):
  FILL: the one running example and all its numbers.
Colour roles (one per concept, kept for the whole video):
  FILL: e.g. answer = violet, key quantity = warn, low = blue, high = orange, areas = aqua, mistakes = red.
Connections (from `python3 channel/channel.py refs <slug>`):
  FILL: callbacks used, the promise this video pays off, the overlap it must not repeat, the teaser target.
"""
import json, pathlib, sys

SLUG = "FILL-slug"            # id in channel/catalog.json
TARGET_MIN = (15, 20)         # from the skill arguments; words ≈ minutes × 150 (voice ~165 wpm + pauses)
D = 0.35                      # default pause between segments
S = []
N = [0]   # auto-id counter; once voiced, insert new lines with explicit ids (e.g. s017a) so old clips stay cached


def seg(chapter, text, visual, pause=D, sid=None):
    if sid is None:
        N[0] += 1; sid = f"s{N[0]:03d}"
    S.append(dict(id=sid, chapter=chapter, text=text, visual=visual, pause_after=pause))


# ───────────── 1. HOOK (~60–70 s): relatable story with real numbers, ends on the title card ─────────────
c = "FILL Hook Chapter Name"
seg(c, "FILL", "FILL")

# ───────────── 2. WELCOME (15–20 s) ─────────────
c = "Welcome"
seg(c, "Welcome to Math Lab TV. Where math is something you can see.",
    "Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.", 0.7)
seg(c, "Today you will learn FILL.", "Big ① + mini visual + caption; small logo top-right.")
seg(c, "You will see FILL.", "Big ② + mini visual + caption.")
seg(c, "And you will FILL.", "Big ③ + mini visual + caption.", 0.6)

# ───────────── 3. WHY IT MATTERS · 4. BUILD + RUNNING EXAMPLE · 5. REAL WORLD (ML, DS, Finance, CS)
# ───────────── 6. COMMON MISTAKES · 7. RECIPE ─────────────
# FILL: one chapter name per scene; chapters must each last ≥ 10 s.

# ───────────── 8. SUBSCRIBE (~12 s) ─────────────
c = "Subscribe"
seg(c, "Look around your world, and notice FILL.", "Four everyday cards stamped with the reflection question.", 0.6)
seg(c, "If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together.",
    "Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓'; 'so we can keep building together' appears.", 0.8)

# ───────────── 9. NEXT TIME ─────────────
c = "Next Time"
seg(c, "But here's a puzzle for next time.", "Small logo top-centre; puzzle icon.")
seg(c, "FILL teaser line(s) connected to this topic.", "FILL; 'next: <topic>' chip under the logo.")
seg(c, "I will see you in the next video.", "Logo + next chip hold.", 2.0)

if __name__ == "__main__":
    import re
    out = pathlib.Path(__file__).parent
    bad = [s["id"] for s in S if re.search(r"[0-9%$]", s["text"])]
    if bad:
        print("WARNING digits/symbols in narration (write numbers as words):", bad)
    (out / "script.json").write_text(json.dumps(S, indent=2, ensure_ascii=False))
    words = sum(len(s["text"].split()) for s in S)
    pauses = sum(s["pause_after"] for s in S)
    est = words / 165 + pauses / 60
    md = [f"# FILL video title\n",
          f"{len(S)} segments · {words} words · est. {est:.1f} min (voice ≈165 wpm + {pauses:.0f} s pauses) · target {TARGET_MIN[0]}–{TARGET_MIN[1]} min\n"]
    cur, cw = None, {}
    for s in S:
        cw[s["chapter"]] = cw.get(s["chapter"], 0) + len(s["text"].split())
    for s in S:
        if s["chapter"] != cur:
            cur = s["chapter"]; md.append(f"\n## {cur}  ·  {cw[cur]} words, ~{cw[cur] / 165 * 60:.0f} s\n")
        p = f" ⏸{s['pause_after']}s" if s["pause_after"] > D else ""
        md.append(f"- **{s['id']}** {s['text']}{p}\n  - *Visual:* {s['visual']}")
    (out / "script.md").write_text("\n".join(md) + "\n")
    print(md[1])
