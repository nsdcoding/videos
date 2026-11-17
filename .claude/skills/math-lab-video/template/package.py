#!/usr/bin/env python3
"""YouTube package: title options, description (chapters from timings.json + related videos from the
channel tracker), tags, pinned comment, settings.  FILL every constant below; see bayes-theorem/package.py."""
import math, pathlib, sys
from common import CHAPTERS, TIM, SEGS

HERE = pathlib.Path(__file__).resolve().parent
SLUG = "FILL-slug"   # id in channel/catalog.json
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE.parent / "channel"))
import channel as ch  # noqa: E402

TITLES = ["FILL keyword first … | ML, Data Science, Finance, CS", "FILL option 2", "FILL option 3"]   # each < 100 chars
TITLE = TITLES[0]                                   # recommended
CH_TITLES = {c["name"]: c["name"] for c in CHAPTERS}  # FILL: a descriptive, keyword-rich title per chapter
DOMAIN_SEGS = dict(ml="FILL sid", ds="FILL sid", fin="FILL sid", cs="FILL sid")   # first segment of each domain part
LINES = dict(
    first2="FILL line 1: main keyword + Machine Learning (ML), Data Science (DS), Finance and Computer Science (CS).\n"
           "FILL line 2: more keywords in a natural sentence.",
    hook="FILL the hook story in 2–3 sentences, with real numbers.",
    domains=dict(ml="FILL", ds="FILL", fin="FILL", cs="FILL"),
    formulas="FILL • formula\n  every symbol explained in plain words",
    worked="FILL • every worked-example answer",
    recipe="FILL 1. …\n2. …",
    next="FILL the next-video teaser",
    pinned_extra="FILL clarifications with timestamps",
)
TAGS = ["FILL topic keywords", "machine learning", "statistics for machine learning", "data science",
        "statistics for data science", "finance", "statistics for finance", "computer science", "ML", "DS", "CS",
        "statistics explained", "Math Lab TV"]


def ts(t):
    t = int(math.floor(t)); m, s = divmod(t, 60)
    return f"{m}:{s:02d}"


def main():
    total = TIM["total"]; mins = round(total / 60)
    rows = []
    for k, c in enumerate(CHAPTERS):
        start = 0.0 if k == 0 else c["t0"]
        end = CHAPTERS[k + 1]["t0"] if k + 1 < len(CHAPTERS) else total
        assert end - start >= 10, c["name"]
        rows.append(f"{ts(start)} {CH_TITLES[c['name']]}")
    at = lambda sid: ts(SEGS[sid]["start"])
    related = ch.desc_block(ch.load(), SLUG)
    d = LINES["domains"]
    desc = f"""{LINES['first2']}

{LINES['hook']} A {mins}-minute explainer for people who don't think of themselves as "math people".

⏱ CHAPTERS
""" + "\n".join(rows) + f"""

🌍 WHERE YOU'LL USE IT
• Machine Learning / ML ({at(DOMAIN_SEGS['ml'])}): {d['ml']}
• Data Science / DS ({at(DOMAIN_SEGS['ds'])}): {d['ds']}
• Finance ({at(DOMAIN_SEGS['fin'])}): {d['fin']}
• Computer Science / CS ({at(DOMAIN_SEGS['cs'])}): {d['cs']}

📐 KEY FORMULAS
{LINES['formulas']}

✅ WORKED EXAMPLE
{LINES['worked']}

🧭 THE RECIPE
{LINES['recipe']}

{related + chr(10) + chr(10) if related else ''}▶ NEXT VIDEO: {LINES['next']}

#machinelearning #datascience #statistics
"""
    tag_str = ", ".join(TAGS)
    assert all(len(t) < 100 for t in TITLES), [len(t) for t in TITLES]
    assert len(tag_str) < 500, len(tag_str)
    pinned = f"📌 Quick summary: FILL\n\nWorth adding:\n{LINES['pinned_extra']}\n\nFILL a question for viewers 👇"
    settings = f"""Category: Education
Language: English · Captions: upload out/captions.srt (English)
Audience: Not made for kids
License: Standard YouTube License · Allow embedding: on
Chapters: automatic from the description timestamps (first at 0:00, all ≥ 10 s)
Thumbnails: upload thumbnail_A.png and thumbnail_B.png to "Test & compare"
End screen: link the next video in the last 20 s · Comments: on · pin pinned_comment.txt
Video length: {ts(total)} ({total:.1f} s)"""
    (OUT / "title.txt").write_text("\n".join(f"{'★ ' if t == TITLE else '  '}{t}  ({len(t)} chars)" for t in TITLES) + "\n")
    (OUT / "description.txt").write_text(desc)
    (OUT / "tags.txt").write_text(tag_str + "\n")
    (OUT / "pinned_comment.txt").write_text(pinned + "\n")
    (OUT / "settings.txt").write_text(settings + "\n")
    for t in TITLES: print(f"{len(t):3d}  {t}")
    print(f"tags: {len(tag_str)} chars | description: {len(desc)} chars")
    print("\n".join(rows))


if __name__ == "__main__":
    main()
