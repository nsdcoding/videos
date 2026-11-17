#!/usr/bin/env python3
"""YouTube package: title, description (chapters from timings.json), tags, pinned comment, settings."""
import json, math, pathlib
from common import CHAPTERS, TIM

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out" / "youtube"; OUT.mkdir(parents=True, exist_ok=True)

TITLE = "Mean vs Median: Which Average Lies? | Machine Learning, Data Science, Finance & CS"

CH_TITLES = {
    "Two Towns": "Two towns, same average: the hook",
    "Welcome": "Welcome to Math Lab TV + what you'll learn",
    "Why It Matters": "Why the wrong average misleads you",
    "The Mean": "The mean: formula, fair shares & balance beam",
    "The Median": "The median: sort, find the middle, even counts",
    "Stress Test": "Outliers, robustness & skewed data",
    "Which One to Trust": "Which average to use (totals vs typical)",
    "Real World": "Finance, computer science, data science & ML",
    "Common Mistakes": "3 common mistakes",
    "Recipe": "Recipe recap",
    "Subscribe": "Look around your world + subscribe",
    "Next Time": "Next: standard deviation",
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
    ch = chapters()
    from common import SEGS
    rw = {k: ts(SEGS[v]["start"]) for k, v in (("fin", "s120"), ("cs", "s125"), ("ds", "s129"), ("ml", "s133"))}
    desc = f"""Mean vs median explained simply, with real uses in Machine Learning, Data Science (DS), Finance and Computer Science (CS).
Learn which average to trust: MSE vs MAE loss in machine learning, outliers in data science, median income in finance, p50 latency in CS.

Two towns both report an average household income of $60,000. In one of them, 8 out of 9 families earn less than that "average". In this {mins}-minute explainer for people who don't think of themselves as "math people", we work through ONE example step by step and find out which average tells the truth.

⏱ CHAPTERS
""" + "\n".join(f"{t} {name}" for t, name, _ in ch) + f"""

🌍 WHERE YOU'LL USE IT
• Finance ({rw['fin']}): median household income, median house prices, and why "average salary" can mislead
• Computer Science / CS ({rw['cs']}): p50 (median) and p99 latency instead of mean response time
• Data Science / DS ({rw['ds']}): spotting typos and outliers, filling missing values with the median
• Machine Learning / ML ({rw['ml']}): loss functions; minimising MSE gives the mean, minimising MAE gives the median

📐 KEY FORMULAS
• Mean: x̄ = (Σ xᵢ) / n → add all the values, divide by how many there are
  (Σ "sigma" = add them all up · xᵢ = one value · n = how many values · x̄ "x-bar" = the mean)
• Median: sort the values and take the middle one. Even count: (middle₁ + middle₂) / 2
• Trimmed mean: drop the most extreme values at each end, then take the mean of the rest
• Minimising squared error (MSE) → the mean · minimising absolute error (MAE) → the median

✅ WORKED EXAMPLE: PINE HILL (incomes in $ thousands)
30, 32, 35, 38, 40, 42, 45, 48, 230
• Mean = 540 ÷ 9 = 60 → $60,000 (only 1 of the 9 families is above it)
• Median = 40 → $40,000 (4 families below, 4 above)
• With a 10th family earning 50: median = (40 + 42) ÷ 2 = 41, mean = 590 ÷ 10 = 59
• If the top income jumps to 2,300: mean = 2,610 ÷ 9 = 290, median is still 40
• Trimmed mean (drop 30 and 230): 280 ÷ 7 = 40
Maple (50, 52, 55, 58, 60, 62, 65, 68, 70) is symmetric, so its mean and median are both 60.

🧭 THE RECIPE
1. Sort the values
2. Find the mean (add up ÷ how many)
3. Find the median (the middle value)
4. Compare them. If the mean is much bigger, a few large values are pulling it up (a rule of thumb, not a law)
5. Match the question: totals & fair shares → mean · a typical person → median · unsure → report both

▶ NEXT VIDEO: Two towns can have the same mean AND the same median and still be completely different places to live. Next time: standard deviation, how far values typically sit from the middle, and why it squares the distances first.

#machinelearning #datascience #statistics
"""
    first2 = desc.split("\n")[:2]
    tags = ["mean vs median", "median vs mean", "mean and median", "which average to use",
            "machine learning", "statistics for machine learning", "data science", "statistics for data science",
            "finance", "statistics for finance", "computer science", "CS", "DS", "ML",
            "MSE vs MAE", "loss function", "median income", "median house price", "p50 latency",
            "outliers", "skewed data", "robust statistics", "statistics for beginners", "statistics explained",
            "Math Lab TV"]
    tag_str = ", ".join(tags)
    assert len(TITLE) < 100 and len(tag_str) < 500

    s = {c["name"]: ts(0 if k == 0 else c["t0"]) for k, c in enumerate(CHAPTERS)}
    pinned = f"""📌 Quick summary: the MEAN is the "fair share" (add everything up, split it evenly). The MEDIAN is the "typical one" (the middle value once you sort). In Pine Hill the mean is $60k but the median is $40k, because one very rich family drags the mean up ({s['Stress Test']}).

Two clarifications:
1️⃣ "Mean much bigger than median means a right tail" is a rule of thumb, not a law. With oddly shaped or lumpy data it can fail, so always look at the actual values ({s['Stress Test']}).
2️⃣ "Minimising absolute error gives the median": with an even number of values, ANY guess between the two middle values gives the same smallest total, and the median (their midpoint) is one of them ({s['Real World']}).

Which "average" have you seen in the news that you now suspect is the mean? 👇"""

    settings = f"""Category: Education
Language: English · Captions: upload out/captions.srt (English)
Audience: Not made for kids
License: Standard YouTube License · Allow embedding: on
Chapters: automatic from the description timestamps (first at 0:00, all ≥ 10 s)
Thumbnails: upload thumbnail_A.png and thumbnail_B.png to "Test & compare"
Playlist suggestion: "Statistics from zero" · End screen: link the next video (standard deviation) in the last 20 s
Comments: on · pin the comment in pinned_comment.txt
Video length: {ts(total)} ({total:.1f} s)"""

    (OUT / "title.txt").write_text(TITLE + "\n")
    (OUT / "description.txt").write_text(desc)
    (OUT / "tags.txt").write_text(tag_str + "\n")
    (OUT / "pinned_comment.txt").write_text(pinned + "\n")
    (OUT / "settings.txt").write_text(settings + "\n")
    print(f"title: {len(TITLE)} chars | tags: {len(tag_str)} chars | description: {len(desc)} chars")
    print("first two lines:\n  " + "\n  ".join(first2))
    for t, n, d in ch:
        print(f"  {t} {n}  ({d}s)")


if __name__ == "__main__":
    main()
