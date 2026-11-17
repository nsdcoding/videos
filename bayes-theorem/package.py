#!/usr/bin/env python3
"""YouTube package: title options, description (chapters from timings.json), tags, pinned comment, settings."""
import math, pathlib
from common import CHAPTERS, TIM, SEGS

HERE = pathlib.Path(__file__).resolve().parent
SLUG = "bayes-examples"   # this video's id in channel/catalog.json
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)

TITLES = [
    "Bayes' Theorem Explained Simply: Why a 90% Accurate Test Means 8% | ML, Data Science, Finance, CS",
    "Bayes' Theorem Explained Simply, With Real Examples | Machine Learning, Data Science, Finance & CS",
    "Bayes' Theorem for Beginners: Count People, Not Percentages (ML, Data Science, Finance, CS)",
]
TITLE = TITLES[0]   # recommended

CH_TITLES = {
    "The Positive Test": "A positive test: 90% accurate, but only an 8% chance?",
    "Welcome": "Welcome to Math Lab TV + what you'll learn",
    "Why It Matters": "Why it matters: alarms, spam, fraud and a study of doctors",
    "Count the Crowd": "Count the crowd: 1,000 people, 9 real vs 99 false alarms",
    "Bayes' Rule": "Bayes' theorem: the formula, symbol by symbol",
    "Test Again": "Test again: posterior becomes prior, the odds shortcut",
    "What Moves the Answer": "What moves the answer: base rate, hit rate, false alarms",
    "Real World": "Machine learning, data science, finance & computer science",
    "Common Mistakes": "3 common mistakes (+ a bonus)",
    "Recipe": "Recipe recap: Bayes in five steps",
    "Subscribe": "Look around your world + subscribe",
    "Next Time": "Next: p-values",
}


def ts(t):
    t = int(math.floor(t)); m, s = divmod(t, 60)
    return f"{m}:{s:02d}"


def chapters():
    rows = []
    for k, c in enumerate(CHAPTERS):
        start = 0.0 if k == 0 else c["t0"]
        end = CHAPTERS[k + 1]["t0"] if k + 1 < len(CHAPTERS) else TIM["total"]
        assert end - start >= 10, c["name"]
        rows.append((ts(start), CH_TITLES[c["name"]], round(end - start, 1)))
    return rows


def main():
    total = TIM["total"]
    mins = round(total / 60)
    # related-video links come from the channel tracker (channel/catalog.json + channel/youtube-links.txt)
    import sys as _s; _s.path.insert(0, str(HERE.parent / "channel"))
    import channel as _ch
    related = _ch.desc_block(_ch.load(), SLUG)
    related = related + "\n\n" if related else ""
    ch = chapters()
    at = lambda sid: ts(SEGS[sid]["start"])
    desc = f"""Bayes' theorem explained simply, with real examples from Machine Learning (ML), Data Science (DS), Finance and Computer Science (CS).
Learn Bayes' rule by counting people: base rates, false positives, precision vs recall, naive Bayes spam filters, fraud alerts and Bayesian updating.

You take a screening test that catches 9 out of 10 people who have a condition and gives a false alarm to only 1 in 10 healthy people. It comes back positive. Most people guess there's a 90% chance they have it. The real answer is about 8%. In this {mins}-minute explainer for people who don't think of themselves as "math people", we picture 1,000 people, count them, and see exactly where the other 92% went.

⏱ CHAPTERS
""" + "\n".join(f"{t} {name}" for t, name, _ in ch) + f"""

🌍 WHERE YOU'LL USE IT
• Machine Learning / ML ({at('s093')}): recall vs precision, and why a model can be 99% accurate and useless
• Data Science / DS ({at('s098')}): Bayesian updating (today's posterior is tomorrow's prior) and judging automated flags
• Finance ({at('s101')}): fraud detectors, "was this you?" checks, and market warning signals
• Computer Science / CS ({at('s104')}): naive Bayes spam filters and intrusion alarms

📐 KEY FORMULAS
• Bayes' theorem: P(A | B) = P(B | A) × P(A) / P(B)
  P( ) = "the probability of" · A = has the condition · B = tests positive · | = "given"
  P(A) = the prior (base rate) · P(B | A) = the likelihood (hit rate) · P(A | B) = the posterior (the answer)
• The bottom part: P(B) = P(B | A) × P(A) + P(B | not A) × P(not A) → real positives + false alarms
• In plain words: real positives ÷ all positives
• Odds shortcut: posterior odds = prior odds × likelihood ratio (here 90% ÷ 10% = 9)

✅ WORKED EXAMPLE (1,000 people, condition in 1 in 100, test catches 9 in 10, false alarm 1 in 10)
• 10 have it → 9 test positive, 1 is missed
• 990 healthy → 99 false alarms, 891 correctly cleared
• Positive: 9 ÷ 108 = 1 in 12 ≈ 8.3% (more than 8× the starting 1%)
• Negative: 1 ÷ 892 ≈ 0.1% (about 1 in 900)
• Overall accuracy really is 90%: (9 + 891) ÷ 1,000
• Second independent positive: 81 ÷ 180 = 45% · third: 729 ÷ 828 ≈ 88%
• Same test, base rate 1 in 10 → 50% · 1 in 5 → about 69% · 1 in 2 → 90%
• False alarms cut to 1 in 100 → about 48% · perfect hit rate → only about 9%
(Illustrative numbers for a screening test, not any specific disease or product.)

🧭 THE RECIPE
1. Start with the base rate: how common is it, before any evidence?
2. Picture a crowd: e.g. 1,000 people, so there are no fractions
3. Split it with the test: count the true positives and the false alarms
4. Keep the matches and divide: real cases ÷ all positives
5. Update: when new, independent evidence arrives, the answer becomes the next base rate
"A test result is a clue, not a verdict."

{related}▶ NEXT VIDEO: p-values. A p-value is often described as "the chance the result is a fluke", but that flips the question, exactly like mistake one. Next time: what a p-value really measures, and why Bayes is the missing piece.

#machinelearning #datascience #statistics
"""
    first2 = desc.split("\n")[:2]
    tags = ["bayes theorem", "bayes theorem explained", "bayes rule", "bayes' theorem examples", "conditional probability",
            "base rate fallacy", "false positives", "precision and recall", "naive bayes", "bayesian statistics",
            "machine learning", "statistics for machine learning", "data science", "statistics for data science",
            "finance", "statistics for finance", "computer science", "ML", "DS", "CS",
            "probability for beginners", "statistics explained", "Math Lab TV"]
    tag_str = ", ".join(tags)
    assert all(len(t) < 100 for t in TITLES) and len(tag_str) < 500

    s = {c["name"]: ts(0 if k == 0 else c["t0"]) for k, c in enumerate(CHAPTERS)}
    pinned = f"""📌 Quick summary: a positive result from a good test (catches 9 in 10, false alarm 1 in 10) means only about an 8% chance when the condition affects 1 in 100 people. Picture 1,000 people: 9 real positives vs 99 false alarms ({s['Count the Crowd']}). The rarer the thing, the more the false alarms win ({s['What Moves the Answer']}).

Worth adding:
1️⃣ The numbers are illustrative, chosen so the counting comes out in whole people. Real tests have their own hit and false-alarm rates, and your own base rate depends on age, symptoms and history. Ask your doctor what YOUR result means.
2️⃣ Multiplying the odds test after test assumes each test's mistakes are independent of the last. A repeat of the same test on the same sample can repeat the same false alarm ({at('s080')}).
3️⃣ The study of doctors ({at('s021')}) is Gigerenzer et al. (2007): in a screening puzzle with numbers like ours, about 21% of the gynaecologists picked the right answer (about 1 in 10) and 47% picked "9 in 10".

Where have you seen an alarm that was usually a false alarm? 👇"""

    settings = f"""Category: Education
Language: English · Captions: upload out/captions.srt (English)
Audience: Not made for kids
License: Standard YouTube License · Allow embedding: on
Chapters: automatic from the description timestamps (first at 0:00, all ≥ 10 s)
Thumbnails: upload thumbnail_A.png and thumbnail_B.png to "Test & compare"
Playlist suggestion: "Statistics from zero" · End screen: link the next video (p-values) in the last 20 s
Comments: on · pin the comment in pinned_comment.txt
Video length: {ts(total)} ({total:.1f} s)"""

    (OUT / "title.txt").write_text("\n".join(f"{'★ ' if t == TITLE else '  '}{t}  ({len(t)} chars)" for t in TITLES) + "\n")
    (OUT / "description.txt").write_text(desc)
    (OUT / "tags.txt").write_text(tag_str + "\n")
    (OUT / "pinned_comment.txt").write_text(pinned + "\n")
    (OUT / "settings.txt").write_text(settings + "\n")
    for t in TITLES:
        print(f"{len(t):3d}  {t}")
    print(f"tags: {len(tag_str)} chars | description: {len(desc)} chars")
    print("first two lines:\n  " + "\n  ".join(first2))
    for t, n, d in ch:
        print(f"  {t} {n}  ({d}s)")


if __name__ == "__main__":
    main()
