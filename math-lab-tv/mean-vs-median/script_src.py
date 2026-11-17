#!/usr/bin/env python3
"""Source of truth for the narration. Run to emit script.json + script.md.

Running example (used everywhere):
  Pine Hill (sorted, $ thousands): 30 32 35 38 40 42 45 48 230  -> mean 60, median 40
  Maple     (sorted, $ thousands): 50 52 55 58 60 62 65 68 70   -> mean 60, median 60
  Pine Hill in street order:       42 230 35 48 30 45 38 32 40
Colour roles: mean = warn #fab219, median = violet #9085e9, low/below = blue,
high/above = orange, areas/water = aqua, mistakes = red.
"""
import json, pathlib

D = 0.35  # default pause between segments
S = []

N = [0]  # auto-id counter; inserted segments use explicit ids so existing ids (and their audio) stay stable


def seg(chapter, text, visual, pause=D, sid=None):
    if sid is None:
        N[0] += 1; sid = f"s{N[0]:03d}"
    S.append(dict(id=sid, chapter=chapter, text=text, visual=visual, pause_after=pause))


def skip():
    """A retired segment: keep the numbering of later ids unchanged."""
    N[0] += 1

# ───────────────────────── 1. HOOK ─────────────────────────
c = "Two Towns"
seg(c, "Imagine you're moving, and you've narrowed it down to two towns.",
    "Two line-art town skylines draw on, left and right; a little moving truck rolls in between them.")
seg(c, "Maple, and Pine Hill.",
    "Name plates pop under each skyline: MAPLE (left), PINE HILL (right).")
seg(c, "You look up the numbers, and both towns report the same average household income.",
    "A stat card drops under each town: 'Average household income'.")
seg(c, "Sixty thousand dollars a year.",
    "Both cards count up 0 → $60k in warn yellow, in sync.", 1.0)
seg(c, "Same average. So, same kind of town, right?",
    "An '=' sign pulses between the cards, then a '?' bounces onto it.")
seg(c, "Let's actually meet the families.",
    "Camera pushes into Maple; skyline breaks into 9 house icons.")
seg(c, "Maple has nine households.",
    "Nine houses line up; a counter '9 households' ticks 1…9 as each lights.")
seg(c, "Their incomes, in thousands of dollars, are fifty, fifty-two, fifty-five, fifty-eight, sixty, sixty-two, sixty-five, sixty-eight, and seventy.",
    "Number line appears: x-axis 'Household income (thousand $)', ticks 0–240 every 20. Each house drops a dot onto its value as it is spoken.")
seg(c, "Everyone is fairly close to sixty.",
    "Aqua bracket spans 50–70 above the cluster: 'all within 10 of 60'.", 1.0)
seg(c, "Now Pine Hill. Also nine households.",
    "Camera pans right to Pine Hill: eight small houses and one mansion.")
seg(c, "Eight of them earn between thirty and forty-eight thousand.",
    "Eight blue dots drop onto a second number line (same axis) at 30, 32, 35, 38, 40, 42, 45, 48.")
seg(c, "And one family earns two hundred thirty thousand dollars a year.",
    "Mansion's dot (orange) flies far right to 230; camera zooms out to keep it in frame.", 1.0)
seg(c, "Add it all up and divide, and yes, Pine Hill's average is also sixty.",
    "Warn-yellow triangle marker slides in at 60, labelled 'average = 60'.")
seg(c, "But look where the families actually are.",
    "Camera zooms to the left cluster; the eight blue dots pulse.")
seg(c, "Eight out of nine households earn less than the average.",
    "Counter '8 of 9 below the average' builds dot by dot.", 1.5)
seg(c, "The average isn't technically wrong. But it describes a family that doesn't live there.",
    "Dashed red box around the empty zone 49–229 near the marker: 'nobody lives near here'.", 1.5)
seg(c, "What tells these towns apart is comparing two kinds of average: the mean, and the median.",
    "Title card: 'MEAN' (warn) vs 'MEDIAN' (violet) slide together; subtitle 'Which average is lying to you?'", 1.0)
skip()  # s018 retired: replaced by the channel welcome + 'today you will learn' preview

# ─────────── 1b. WELCOME (channel intro, same pattern as the Math Lab TV reference intro) ───────────
c = "Welcome"
seg(c, "Welcome to Math Lab TV. Where math is something you can see.",
    "Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.", 1.0, sid="s017a")
seg(c, "Today you will learn exactly what the mean and the median are, and how each one is calculated.",
    "Preview ① : x-bar formula morphs beside a sorted row whose middle tile glows violet.", sid="s017b")
seg(c, "You will see why one rich family can make an average lie.",
    "Preview ② : Pine Hill dot plot; the orange outlier drags the warn mean marker; median stays.", sid="s017c")
seg(c, "And you will learn how to pick the right one, every time.",
    "Preview ③ : the two signposts TOTALS → mean / TYPICAL → median.", 1.0, sid="s017d")

# ───────────────────────── 2. WHY IT MATTERS ─────────────────────────
c = "Why It Matters"
seg(c, "This isn't just a puzzle about two made-up towns.",
    "Towns shrink into the top-right; three headline cards fly in.")
seg(c, "Every week, you hear averages in the news.",
    "Headline cards stack: 'Average salary rises', 'Average home price hits record', 'Average wait time up'.")
seg(c, "Average salary. Average house price. Average wait time at the hospital.",
    "Each card highlights in turn with a small icon (wallet, house, clock).")
seg(c, "Each of those is one number standing in for thousands of people.",
    "Hundreds of tiny dots funnel into a single big number on one card.")
seg(c, "If it's the wrong kind of average, it can push you into a bad decision.",
    "The big number flickers; a red warning triangle appears beside it.")
seg(c, "Like moving to Pine Hill expecting to earn what your neighbours earn.",
    "Pine Hill dot line returns; a 'you' dot drops at 60, alone, far from the cluster.")
seg(c, "Or opening a fancy restaurant there, counting on sixty-thousand-dollar customers who mostly aren't there.",
    "Restaurant icon with price tag; arrows point to the 60 marker, then swing to the real crowd at 30–48.", 1.0)
seg(c, "The good news: telling the two averages apart takes a few minutes, and no fancy math.",
    "Stopwatch icon spins; 'no fancy math' badge.", 0.6)

# ───────────────────────── 3. THE MEAN ─────────────────────────
c = "The Mean"
seg(c, "Let's start with the one you already know: the mean.",
    "Word 'MEAN' writes on in warn yellow.")
seg(c, "The mean is what most people call 'the average'.",
    "Equation card: mean = “the average”.")
seg(c, "To find it, add up all the values, then divide by how many there are.",
    "Two step chips: ① add them all  ② divide by how many.")
seg(c, "Let's do it for Pine Hill.",
    "Nine number tiles for Pine Hill slide in: 30 32 35 38 40 42 45 48 230.")
seg(c, "Thirty, plus thirty-two, plus thirty-five, and so on, all the way up to two hundred thirty.",
    "Tiles fly one by one into a running-total counter: 30 → 62 → 97 → 135 → 175 → 217 → 262 → 310 → 540.")
seg(c, "The total is five hundred forty.",
    "Counter lands on 540 with a bounce.", 0.6)
seg(c, "There are nine households, so we divide by nine.",
    "540 slides up into a fraction 540 over 9 (LaTeX).")
seg(c, "Five hundred forty divided by nine is sixty.",
    "'= 60' appears in warn yellow; marker drops onto the number line at 60.", 1.0)
seg(c, "In math books, you'll see this written as a formula. Let's decode it, one symbol at a time.",
    "Formula appears in grey: x̄ = (Σ xᵢ) / n (LaTeX fraction).")
seg(c, "The letter x stands for one value. Here, one household's income.",
    "'x' lights up; arrow points to the 42 tile: 'x = one income'.")
seg(c, "The small i underneath means 'which one'. x one is the first household, x two is the second, and so on.",
    "Labels x₁, x₂, x₃… hop onto the tiles left to right.")
seg(c, "This big zigzag letter is the Greek capital sigma. It just means: add them all up.",
    "Σ lights up and grows; definition card: 'Σ (sigma) = add them all up'.", 0.8)
seg(c, "The letter n means how many values there are. For Pine Hill, n is nine.",
    "'n' lights up; card: 'n = how many = 9'.")
seg(c, "And the x with a bar on top, called x bar, is the name for the mean.",
    "'x̄' lights up; card: 'x̄ (x-bar) = the mean'.")
seg(c, "So the whole formula says: add up every value, then divide by how many there are.",
    "Plain-English captions snap under each part of the formula.", 1.0)
seg(c, "But what is the mean, really? Here are two ways to picture it.",
    "Split screen preview: left a water tank, right a see-saw.")
seg(c, "Picture one: fair shares.",
    "Wipe to bar chart: x-axis 'Household' 1–9, y-axis 'Income (thousand $)' 0–240 every 40.")
seg(c, "Here are Pine Hill's nine incomes, as bars.",
    "Bars grow: eight blue short bars, one tall orange bar at 230.")
seg(c, "Imagine all nine families pour their income into one shared pot.",
    "Bars turn aqua and drain like water into a tank at the right; tank fill level counts to 540.")
seg(c, "Then the pot is shared out equally, so every family gets the same amount.",
    "Water flows back out into nine equal columns.")
seg(c, "Every bar ends up at exactly sixty. That's the mean.",
    "All nine bars settle at 60; warn line across at y = 60, labelled 'mean = 60'.", 1.5)
seg(c, "So the mean answers one question: if everything were shared out evenly, how much would each get?",
    "Question card under the chart; the levelled bars glow.", 1.0)
seg(c, "Picture two: a balance beam.",
    "Number line (0–240, every 20) thickens into a beam on a triangle pivot.")
seg(c, "Put each household on the line as an equal weight, sitting at its income.",
    "Nine identical blocks drop onto the beam at 30…48 and 230.")
seg(c, "Where should the support go, so the beam balances perfectly?",
    "Pivot slides back and forth under the beam; beam tilts as it moves.")
seg(c, "Try forty. The beam tips to the right, because that one family is so far out.",
    "Pivot stops at 40; beam rotates clockwise, right end down; red 'tips' label.")
seg(c, "Try sixty, and it balances.",
    "Pivot slides to 60; beam swings level; warn marker 'mean = 60'.", 1.0)
seg(c, "Here's why. Measure how far each family is from sixty.",
    "Camera zooms in; distance arrows grow from 60 to each block.")
seg(c, "The eight families on the left are thirty, twenty-eight, twenty-five, twenty-two, twenty, eighteen, fifteen, and twelve below.",
    "Blue arrows labelled −30 −28 −25 −22 −20 −18 −15 −12 appear one by one.")
seg(c, "Together, that's one hundred seventy below.",
    "Blue labels collapse into one counter: '−170'.")
seg(c, "And the one family on the right is one hundred seventy above.",
    "Camera pans right; long orange arrow '+170'.", 1.0)
seg(c, "The distances below and above cancel out exactly. That's what the mean always does.",
    "'−170 + 170 = 0' assembles centre screen.", 1.5)
seg(c, "And notice: one family, far enough away, balances eight families all by itself.",
    "Split highlight: 8 blue blocks vs 1 orange block on the level beam.", 1.5)
seg(c, "That's the mean's big weakness. Every value pulls on it, and the farther away a value is, the harder it pulls.",
    "Rope from the 230 block tugs the warn marker; tension lines; label 'far values pull harder'.", 1.0)

# ───────────────────────── 4. THE MEDIAN ─────────────────────────
c = "The Median"
seg(c, "Now, the second kind of average: the median.",
    "Word 'MEDIAN' writes on in violet.")
seg(c, "The median is the middle value, once the values are in order.",
    "Card: median = the middle value (after sorting).")
seg(c, "Step one: sort. Line the incomes up from smallest to largest.",
    "Tiles in street order 42 230 35 48 30 45 38 32 40 shuffle into sorted order.")
seg(c, "Thirty, thirty-two, thirty-five, thirty-eight, forty, forty-two, forty-five, forty-eight, two hundred thirty.",
    "Sorted tiles highlight left to right in time with speech.")
seg(c, "Step two: find the middle. Cross one off each end, again and again, walking inward.",
    "Two walker markers appear at each end of the row.")
seg(c, "Thirty and two hundred thirty go. Then thirty-two and forty-eight. Then thirty-five and forty-five. Then thirty-eight and forty-two.",
    "Pairs are struck through and fade, in sync; walkers step inward.")
seg(c, "One value is left standing: forty.",
    "40 tile glows violet and lifts.", 1.5)
seg(c, "The median income in Pine Hill is forty thousand dollars.",
    "'median = 40' card; violet diamond marker on the number line at 40.", 1.0)
seg(c, "Four families earn less, and four earn more. That's the median's promise: it splits the group in half.",
    "Split line at 40: '4 below' (blue) | '4 above' (orange).", 1.0)
seg(c, "Compare that with the mean of sixty, where eight families were below and only one was above.",
    "Both markers on one axis: mean 60 '8 below | 1 above' vs median 40 '4 | 4'.", 1.5)
seg(c, "In Maple, the middle value is sixty, exactly the same as its mean.",
    "Maple dot line: violet and warn markers overlap at 60.", 1.0)
seg(c, "You'll also hear the median called the fiftieth percentile, or p fifty, because it sits halfway through the sorted list.",
    "Sorted row with a 0%–100% ruler above it; 40 sits at the 50% mark; label 'p50'.")
seg(c, "But what if there's an even number of values? Then there's no single middle.",
    "Card with '?' and an even row of placeholder tiles.")
seg(c, "Say a new family moves to Pine Hill, earning fifty thousand.",
    "New house slides in; new tile '50' joins the sorted row between 48 and 230.")
seg(c, "Now there are ten households.",
    "Counter 'n = 10'.")
seg(c, "Cross off from both ends again, and this time two values are left in the middle: forty and forty-two.",
    "Crossing-off animation; 40 and 42 remain.")
seg(c, "The rule: take the halfway point between them. Add the two, and divide by two.",
    "Fraction (40 + 42) over 2 (LaTeX).")
seg(c, "Forty plus forty-two is eighty-two. Half of that is forty-one.",
    "'= 41' violet; marker sits between the 40 and 42 dots.", 1.0)
seg(c, "So with ten families, the median is forty-one thousand.",
    "'median = 41' card.")
seg(c, "And the mean? Five hundred ninety, divided by ten, which is fifty-nine.",
    "Fraction 590 over 10 = 59; warn marker at 59.", 0.6)
seg(c, "For the rest of this video, let's go back to our original nine households.",
    "New house slides back out; 'n = 9'.")

# ───────────────────────── 5. TUG OF WAR ─────────────────────────
c = "Stress Test"
seg(c, "So which average is more trustworthy? Let's stress test them.",
    "Two gauges labelled MEAN and MEDIAN, needles at 60 and 40.")
seg(c, "Suppose Pine Hill's richest family has an amazing year.",
    "Mansion icon sparkles orange.")
seg(c, "Their income jumps from two hundred thirty thousand to two point three million. Ten times more.",
    "Camera zooms out as the axis rescales to 0–2400 (ticks every 400); the orange dot slides to 2300.")
seg(c, "Nobody else's income changes at all.",
    "Eight blue dots stay put, tagged 'unchanged'.")
seg(c, "The new total is two thousand six hundred ten. Divided by nine, the mean becomes two hundred ninety thousand dollars.",
    "Fraction 2610 over 9 = 290; warn marker races right to 290.", 1.0)
seg(c, "According to the mean, the typical family is now almost five times richer. Yet not one of the other eight got a raise.",
    "'≈ ×4.8' badge on the mean gauge; eight blue dots each show '+0'.", 1.5)
seg(c, "And the median? Sort, cross off, and the middle is still forty.",
    "Violet marker stays at 40; median gauge needle doesn't move.", 1.5)
seg(c, "The median doesn't care how far away an extreme value is, only which side of the middle it's on.",
    "Left/right halves shaded; the 2300 dot just counts as '1 on the right'.")
seg(c, "Values that sit far away from the rest are called outliers.",
    "Orange ring around the 2300 dot, label 'outlier'.")
seg(c, "The mean gets dragged toward outliers. The median hardly notices them. Statisticians call that being robust.",
    "Tug-of-war: outlier rope drags the warn marker; violet marker anchored. Card 'robust = hardly moved by outliers'.", 1.0)
seg(c, "But being robust has a cost. Let's go back to two hundred thirty thousand, and this time, the poorest family's income falls from thirty thousand to ten.",
    "Axis zooms back to 0–240; orange dot returns to 230; the leftmost blue dot slides 30 → 10.")
seg(c, "Their life just got much harder. The mean dips, to about fifty-seven point eight.",
    "Warn marker slides 60 → 57.8.")
seg(c, "The median stays at forty. It doesn't see the change at all.",
    "Violet marker frozen at 40; red label 'missed it'.", 1.5)
seg(c, "The median ignores how far values are from the middle. The mean uses every bit of that. Each choice has a cost.",
    "Two-column card: MEAN 'uses every value / dragged by outliers' — MEDIAN 'robust / ignores distance'.", 1.0)
seg(c, "Now let's put everything back as it was, and step back to look at the shape of the data.",
    "Poorest dot returns to 30; Maple and Pine Hill dot lines stack, top and bottom.")
seg(c, "Maple's incomes are spread evenly around the middle. The left side is a mirror image of the right.",
    "Mirror line at 60 on Maple; left dots reflect onto right dots (−10↔+10, −8↔+8 …).")
seg(c, "We call that symmetric. And for symmetric data, the mean and the median land in the same spot.",
    "Both markers overlap at 60; label 'symmetric: mean = median'.", 1.0)
seg(c, "Pine Hill is lopsided: a crowd on the left, and a long, thin tail stretching off to the right.",
    "Orange shaded arrow along Pine Hill from 48 to 230: 'long tail'.")
seg(c, "That's called right-skewed. And in right-skewed data, the mean usually gets pulled toward the tail, past the median.",
    "Warn marker at 60 with an arrow toward the tail; violet marker at 40.", 1.0)
seg(c, "Flip it, with the tail on the left, and the mean usually lands below the median.",
    "Pine Hill's dot pattern mirrors horizontally on a schematic axis (labelled 'shape only'): tail now left, mean marker left of median.")
seg(c, "So here's a handy warning light: if the mean is much bigger than the median, a few large values are probably pulling it up.",
    "Dashboard warning light: 'mean much bigger than median → look for big values'.", 1.0)
seg(c, "One honest caveat: this is a rule of thumb, not a law. With oddly shaped data, it can fail. So always look at the actual values too.",
    "'RULE OF THUMB' stamp lands on the warning light; small dot plot beside it.", 1.0)

# ───────────────────────── 6. WHICH ONE TO TRUST ─────────────────────────
c = "Which One to Trust"
seg(c, "So which average should you use? It depends on the question you're asking.",
    "Road splits into two paths with signposts.")
seg(c, "If your question is about totals, use the mean.",
    "Left signpost lights warn: 'TOTALS → mean'.")
seg(c, "Say Pine Hill's town council wants to plan a budget from a two percent local income tax.",
    "Town hall icon; badge '2% tax'.")
seg(c, "Total income is the mean times the number of households. Sixty times nine is five hundred forty thousand.",
    "60 × 9 = 540 builds from nine blocks of 60.")
seg(c, "Two percent of that is ten thousand eight hundred dollars a year.",
    "Coin stack counter → $10,800.")
seg(c, "And the richest family alone pays more than forty percent of it. The council needs that outlier counted.",
    "Pie of the $10,800: orange slice '$4,600' (43%) vs blue rest.", 1.0)
seg(c, "The median can't do this. Forty times nine is three hundred sixty, which misses a third of the real total.",
    "Bar 540 (warn) next to bar 360 (violet); red gap '180 missing = 1/3'.", 1.0)
seg(c, "But if your question is, what's life like for a typical family here, use the median.",
    "Right signpost lights violet: 'TYPICAL → median'.")
seg(c, "If you move to Pine Hill, forty thousand is a far better guess for your neighbours' income than sixty.",
    "'you' dot among the cluster; short gaps to neighbours at 40 vs long gaps at 60.", 1.0)
seg(c, "And the mean and the median aren't the only options.",
    "Shelf of three cards appears: mean, median, + 'others'.")
seg(c, "There's the mode, the value that appears most often. But no income in Pine Hill repeats, so here there isn't one.",
    "Mode card; dots check for twins one by one: 'no repeats → no mode'.")
seg(c, "There's also the trimmed mean: drop the most extreme values at each end, then take the mean of what's left.",
    "Scissors snip the 30 and 230 tiles off the row.")
seg(c, "Trim one from each end of Pine Hill, and the remaining seven add up to two hundred eighty. Divide by seven, and you get forty.",
    "Fraction 280 over 7 = 40 (aqua).", 1.0)
seg(c, "Here it happens to match the median exactly. In general, a trimmed mean sits somewhere between the two ideas: it uses most of the values, but one extreme one can't hijack it.",
    "Slider from MEAN to MEDIAN with 'trimmed mean' in between.")
seg(c, "And when in doubt, report both the mean and the median. The gap between them tells you something too.",
    "'mean 60 | median 40' side by side; aqua brace 'gap = 20 → skewed'.", 1.0)

# ───────────────────────── 7. REAL WORLD ─────────────────────────
c = "Real World"
seg(c, "This choice shows up everywhere data is used. Let's visit four places.",
    "Four tiles: Finance, Computer Science, Data Science, Machine Learning.")
seg(c, "First, money.",
    "Finance tile zooms to fill the screen.")
seg(c, "Incomes and house prices usually have a long right tail, just like Pine Hill: lots of ordinary values, and a few huge ones.",
    "Pine Hill dot line morphs into a right-skewed outline (labelled 'shape like Pine Hill').")
seg(c, "That's why the U.S. Census Bureau headlines median household income, not the mean.",
    "Report card mock-up (no logos): 'Median household income'.")
seg(c, "And why housing reports usually quote the median sale price.",
    "House card: 'Median sale price'.")
seg(c, "If a company advertises its average salary, ask whether the boss's pay is in there. One huge salary can lift the mean, just like Pine Hill's richest family.",
    "Org-chart dots; one far-right 'CEO' dot tugs a warn marker, echoing the 230 dot.", 1.0)
seg(c, "Next, computer science. Think about how long a website takes to respond.",
    "CS tile; browser window with a loading spinner.")
seg(c, "Most requests are quick, but now and then one gets stuck and takes ages.",
    "Response-time dot plot on schematic axis 'response time' — crowd left, rare dots far right.")
seg(c, "It's the Pine Hill pattern again. A few slow requests drag the mean up, so it no longer describes a normal visit.",
    "Warn marker dragged right by the slow dots; violet marker stays with the crowd.")
seg(c, "So engineers track the median, which they call p fifty, alongside the slow tail, such as p ninety-nine: the time that ninety-nine percent of requests beat or match.",
    "Markers 'p50' (violet) and 'p99' (orange) on the axis; 99% of dots shaded left of p99.", 1.0)
seg(c, "In data science, one of the first jobs with new data is cleaning it.",
    "Spreadsheet grid with Pine Hill's nine incomes.")
seg(c, "Suppose the richest family's income was typed with one extra zero: two point three million instead of two hundred thirty thousand.",
    "Cell '230,000' gains a red extra '0' → '2,300,000'.")
seg(c, "As we saw, that one typo drags the mean to two hundred ninety thousand. The median doesn't flinch.",
    "Mini gauges: mean 60 → 290 (warn), median 40 → 40 (violet).", 1.0)
seg(c, "So data scientists compare the mean and median as a quick check for typos and outliers. And when filling in missing values in skewed data, they often use the median.",
    "Checklist ticks: 'mean vs median gap check'; empty cell fills with '40' (violet).")
seg(c, "Finally, machine learning. Here, the choice hides inside something called a loss function.",
    "ML tile; card 'loss function = how we score mistakes'.")
seg(c, "Imagine a model that must make one single guess for every Pine Hill family's income. What's the best guess?",
    "Guess slider (aqua line) on the Pine Hill number line.")
seg(c, "It depends on how you score the mistakes.",
    "Two empty score panels appear.")
seg(c, "Score one: add up how far off the guess is for each family. That's called absolute error.",
    "Plot: x 'guess (thousand $)' 0–120, y 'total distance' 0–800; distance lines from the guess to each dot.")
seg(c, "Slide the guess along, and the total distance is smallest at forty. The median.",
    "Point traces the V-shaped curve; minimum at 40 (total 230) glows violet.", 1.0)
seg(c, "Score two: square each distance before adding, so big misses count extra. That's called squared error.",
    "Second plot: y 'total squared distance (thousands)' 0–70; squares drawn on the distances, equal x/y scale.")
seg(c, "Now the best guess is sixty. The mean.",
    "Point traces the U-shaped curve; minimum at 60 (≈ 32.8 thousand) glows warn.", 1.0)
seg(c, "This works for any data, not just Pine Hill. Minimising squared error lands on the mean. Minimising absolute error lands on the median, or with an even count, anywhere between the two middle values.",
    "Rule card: 'squared error → mean' / 'absolute error → median'.", 1.5)
seg(c, "So when someone trains a model with mean squared error or mean absolute error, they're choosing whether it aims for a mean or a median.",
    "'MSE → aims for the mean', 'MAE → aims for the median'.")
seg(c, "Squared error chases outliers. Absolute error shrugs them off. Same trade-off, new setting.",
    "Outlier dot yanks the MSE curve's minimum; MAE minimum stays put.", 1.0)

# ───────────────────────── 8. COMMON MISTAKES ─────────────────────────
c = "Common Mistakes"
seg(c, "Before we wrap up, here are the three most common mistakes people make with averages.",
    "Three red cards face down.")
seg(c, "Mistake one: taking the middle without sorting first.",
    "Card 1 flips: 'Not sorting'.")
seg(c, "Here are Pine Hill's incomes in the order the houses sit on the street: forty-two, two hundred thirty, thirty-five, forty-eight, thirty, forty-five, thirty-eight, thirty-two, and forty.",
    "Street of houses with tiles above, unsorted.")
seg(c, "The middle of that list is thirty. That's not the median. It's just whoever lives in the middle house.",
    "Middle tile 30 circled red with a cross.", 1.0)
seg(c, "Always sort first. Sorted, the middle is forty.",
    "Tiles sort; 40 glows violet with a tick.")
seg(c, "Mistake two: assuming half the people are above the average.",
    "Card 2 flips: 'Half are above average?'")
seg(c, "That's true for the median, by design. It's not true for the mean.",
    "'half above: median ✓, mean ✗'.")
seg(c, "In Pine Hill, only one family out of nine is above the mean. So if you're below average there, you're in very good company.",
    "Pine Hill dots: 8 blue below the warn marker, 1 orange above.", 1.0)
seg(c, "Mistake three: deciding the median is always better, and that outliers should just be deleted.",
    "Card 3 flips: 'Delete the outlier?'")
seg(c, "That rich family is real. Their income is real money, and the town's tax budget depends on it.",
    "Mansion and the $4,600 tax coin.")
seg(c, "Remove a value only when you have evidence it's an error, like that extra zero. Otherwise keep it, and choose the average that fits your question.",
    "Checklist: 'evidence of error? → fix it. Otherwise → keep it'.", 1.0)
seg(c, "And a bonus mistake: with an even count, picking one of the two middle numbers instead of the halfway point between them.",
    "40 and 42 tiles; red cross on '40' and '42', violet tick on '41'.")

# ───────────────────────── 9. RECIPE ─────────────────────────
c = "Recipe"
seg(c, "Let's turn all of that into a recipe you can use on any set of numbers.",
    "Recipe card frame unrolls.")
seg(c, "Step one: sort the values, from smallest to largest.",
    "Item 1 writes on with a mini sorted row.")
seg(c, "Step two: find the mean. Add them all up, and divide by how many there are.",
    "Item 2 with mini formula x̄ = Σx / n.")
seg(c, "Step three: find the median, the middle value. With an even count, take the halfway point of the middle two.",
    "Item 3 with mini row and violet middle.")
seg(c, "Step four: compare them. If they're close, the data is probably fairly balanced. If the mean is much bigger, look for large values pulling it up.",
    "Item 4 with tiny warning light.")
seg(c, "Step five: match the average to your question. Totals and fair shares: the mean. A typical person or thing: the median. Not sure? Report both.",
    "Item 5 with the two signposts.", 1.5)
seg(c, "For Pine Hill, the mean is sixty, and the median is forty. Both are correct. They answer different questions.",
    "Final card: 'Pine Hill — mean 60 (fair share) | median 40 (typical family)'.", 1.0)
seg(c, "An average only lies when you ask it the wrong question.",
    "Line types on in violet, centred.", 1.5)

# ─────────── 9b. SUBSCRIBE (channel outro, same pattern as the Math Lab TV reference outro) ───────────
c = "Subscribe"
seg(c, "Look around your world, and notice which kind of average people quote to you.",
    "Four everyday cards (salary, house price, wait time, page load), each stamped 'mean or median?'.", 0.6, sid="s162a")
seg(c, "If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together.",
    "Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓' and 'so we can keep building together' appears.", 0.8, sid="s162b")

# ───────────────────────── 10. NEXT TIME ─────────────────────────
c = "Next Time"
seg(c, "But here's a puzzle for next time.",
    "Puzzle-piece icon.")
seg(c, "Two towns can have the same mean and the same median, and still be completely different places to live.",
    "Maple (50–70) vs a new town 'Cedar' (10, 20, 30, 45, 60, 75, 90, 100, 110): both markers at 60 on both lines.")
seg(c, "The missing piece is spread: how far values typically sit from the middle.",
    "Spread arrows: short for Maple, long for Cedar.")
seg(c, "Next time, we'll measure it with the standard deviation, and see why it squares the distances first.",
    "Card: 'Next: Standard Deviation'.")
seg(c, "I will see you in the next video.",
    "Logo stays at the top; 'next: standard deviation' chip; Maple vs Cedar spread visual holds.", 2.0)

if __name__ == "__main__":
    out = pathlib.Path(__file__).parent
    (out / "script.json").write_text(json.dumps(S, indent=2, ensure_ascii=False))
    words = sum(len(s["text"].split()) for s in S)
    pauses = sum(s["pause_after"] for s in S)
    md = [f"# Mean Versus Median: Which Average Is Lying to You?\n",
          f"{len(S)} segments · {words} words · est. {words/150+pauses/60:.1f} min at 150 wpm (incl. {pauses:.0f} s pauses)\n"]
    cur = None
    for s in S:
        if s["chapter"] != cur:
            cur = s["chapter"]; md.append(f"\n## {cur}\n")
        p = f" ⏸{s['pause_after']}s" if s["pause_after"] > D else ""
        md.append(f"- **{s['id']}** {s['text']}{p}\n  - *Visual:* {s['visual']}")
    (out / "script.md").write_text("\n".join(md) + "\n")
    print(md[1])
