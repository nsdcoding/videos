#!/usr/bin/env python3
"""Source of truth for the narration. Run to emit script.json + script.md.

Running example (used everywhere; every number checked in verify_numbers.py):
  A screening test for a condition that 1 in 100 people have.
  The test catches 9 of 10 people who have it (sensitivity / recall 90%),
  and gives a false alarm to 1 in 10 healthy people (false-positive rate 10%).
  Crowd of 1,000 (a 40 x 25 grid):  10 sick -> 9 true positives, 1 missed
                                    990 healthy -> 99 false alarms, 891 true negatives
  Positive: 9 / 108 = 1/12 ~ 8.3 %.  Negative: 1 / 892 ~ 1 in 900.
  Second independent positive: 81 / 180 = 45 %.  Third: 729 / 828 ~ 88 %.
  Odds form: 1:99 -> x9 -> 9:99 -> x9 -> 81:99 -> x9 -> 729:99.

Colour roles (one per concept, kept for the whole video):
  sick / has the condition = orange      healthy = blue
  positive test / evidence = aqua ring   base rate / prior = warn yellow
  the answer / posterior   = violet      mistakes = red
"""
import json, pathlib

D = 0.35  # default pause between segments
S = []
N = [0]   # auto-id counter; later insertions use explicit ids (e.g. s017a) so existing ids keep their audio


def seg(chapter, text, visual, pause=D, sid=None):
    if sid is None:
        N[0] += 1; sid = f"s{N[0]:03d}"
    S.append(dict(id=sid, chapter=chapter, text=text, visual=visual, pause_after=pause))


# ───────────────────────── 1. HOOK ─────────────────────────
c = "The Positive Test"
seg(c, "Imagine you go for a routine health check, and the doctor suggests a quick screening test.",
    "Line-art clinic door draws on; a small person icon walks to it; a clipboard with 'screening test' pops up.")
seg(c, "It looks for a condition that is fairly rare. About one in every hundred people your age has it.",
    "10 x 10 grid of person squares on axes (columns 1–10, rows 1–10); one square turns orange. Chip: '1 in 100 have it'.")
seg(c, "The test is good. If you have the condition, it catches it nine times out of ten.",
    "Stat card 1: ten orange squares; nine get an aqua 'positive' ring. Caption 'catches 9 of 10 who have it'.")
seg(c, "And if you are healthy, it only gives a false alarm one time in ten.",
    "Stat card 2: ten blue squares; one gets an aqua ring. Caption 'false alarm for 1 in 10 healthy people'.")
seg(c, "A few days later, the result comes back. Positive.",
    "An envelope slides in and opens; 'POSITIVE' stamps on in aqua.", 1.0)
seg(c, "So, how worried should you be? What is the chance you actually have it?",
    "A probability meter appears: a horizontal axis 0%–100% with ticks every 10, title 'chance you have it'.")
seg(c, "Take a second, and make your own guess.",
    "The meter waits; a blinking '?' cursor sits on it; tiny clock ticks.", 1.5, sid="s006a")
seg(c, "Most people say about ninety percent. After all, the test is ninety percent accurate.",
    "A grey 'gut feeling' pointer slides to 90% on the meter.")
seg(c, "Here's the surprise. The real answer is about eight percent.",
    "A violet pointer drops in at 8.3%; the grey 90% pointer is crossed out in red.", 2.0)
seg(c, "Not ninety. Eight. Less than one in ten.",
    "Big comparison: '90%' (grey, struck) vs '≈ 8%' (violet), camera pushes in on the violet number.", 1.0)
seg(c, "Nothing in that story is a trick. The test really is good. Your gut just left out one number.",
    "The three fact chips line up: '1 in 100 have it' · 'catches 9 of 10' · 'false alarm 1 in 10'.")
seg(c, "How rare the condition was to begin with.",
    "The '1 in 100' chip turns warn yellow and glows: 'the base rate'.", 1.0)
seg(c, "The tool that puts that number back in is called Bayes' theorem. And by the end of this video, you will be able to do this in your head.",
    "Title card: 'BAYES' THEOREM' (violet) with subtitle 'explained simply, with real examples'.", 1.0)

# ─────────── 2. WELCOME (channel intro) ───────────
c = "Welcome"
seg(c, "Welcome to Math Lab TV. Where math is something you can see.",
    "Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.", 0.7)
seg(c, "Today you will learn how to turn a test result into a real probability, just by counting people.",
    "Small logo moves top-right. Big ① (aqua); mini grid where 108 squares light up and 9 turn orange; caption 'turn a test result into a real probability'.")
seg(c, "You will see Bayes' theorem as a formula, and exactly what every symbol means.",
    "Big ② (violet); the formula P(A|B) = P(B|A)·P(A) / P(B) writes on; caption 'the formula, symbol by symbol'.")
seg(c, "And you will see how evidence adds up, in spam filters, fraud alerts and machine learning.",
    "Big ③ (warn); a mini meter walks 1% → 8% → 45%; caption 'how evidence adds up'.", 0.6)

# ───────────────────────── 3. WHY IT MATTERS ─────────────────────────
c = "Why It Matters"
seg(c, "This isn't just about medical tests.",
    "The clinic icon shrinks to the corner; three empty cards slide in.")
seg(c, "Any time a rare thing meets an imperfect detector, the same trap is waiting.",
    "Equation of icons: 'rare thing' (orange dot) + 'imperfect detector' (aqua radar) = 'trap' (red).")
seg(c, "A smoke alarm going off. An email flagged as spam. A message from your bank asking, was this you?",
    "Three cards fill in turn: smoke alarm, envelope with 'spam' tag, phone with 'Was this you?'.")
seg(c, "Each one is a positive test. And each one asks the same question: given this alarm, how likely is the real thing?",
    "Each card gets an aqua 'positive' ring; a banner: 'given the alarm → how likely is the real thing?'.", 1.0)
seg(c, "And smart people get this wrong. In one well known study, doctors were given a screening puzzle with numbers like ours.",
    "Card 'Study of doctors · a screening puzzle like ours' (generic, no names or logos).")
seg(c, "Only about one in five picked the right answer. Almost half picked nine in ten.",
    "Bar chart on axes, y 'share of doctors (%)' 0–50: bar 'about 1 in 10 (correct)' ≈ 21%, bar '9 in 10' ≈ 47%.", 1.0)
seg(c, "That's not because doctors are bad at math. It's because the numbers came as percentages of percentages.",
    "A jumble of '%' signs ('1%', '90%', '10%') swirl together.")
seg(c, "Change the form, and the problem becomes easy. So here is the trick for this whole video: stop thinking in percentages, and start counting people.",
    "The '%' signs morph into a neat grid of person squares. Chip: 'count people'.", 1.0)
seg(c, "And Bayes isn't only about tests. It's a rule for changing your mind by the right amount when new evidence arrives. Not too little, and not too much.",
    "A dial labelled 'how sure am I?' turns a little, not all the way: 'update by the right amount'.", 1.0)

# ───────────────────────── 4a. COUNT THE CROWD ─────────────────────────
c = "Count the Crowd"
seg(c, "Let's do it. Picture one thousand people, all taking the same test.",
    "Axes appear: x 'column' 0–40 (ticks every 5), y 'row' 0–25 (ticks every 5), equal scale. A 40 x 25 grid of squares fills in, counter 0 → 1,000.")
seg(c, "Each little square is one person. Forty across, twenty five down. One thousand.",
    "Camera zooms to the top-left corner: one square labelled 'one person'; then '40 × 25 = 1,000'.")
seg(c, "Step one. How many of them have the condition? One in a hundred. So, ten people.",
    "Step chip '1'. Ten squares in the first column turn orange; counter '10 have it' (orange); warn tag 'base rate 1 in 100'.")
seg(c, "The other nine hundred and ninety are healthy.",
    "The rest pulse blue; counter '990 healthy' (blue).")
seg(c, "Step two. Test the ten people who have the condition. It catches nine of them.",
    "Step chip '2'. Camera zooms on the orange column; nine get aqua rings one by one.")
seg(c, "So, nine true positives, and one person the test misses.",
    "Labels: '9 true positives' (aqua) and '1 missed' (muted) beside the column.")
seg(c, "Step three. Test the nine hundred and ninety healthy people. It wrongly flags one in ten of them.",
    "Step chip '3'. Camera pulls back; aqua rings ripple across the blue squares, one in every ten.")
seg(c, "That's ninety nine false alarms.",
    "Counter '99 false alarms' ticks up in aqua as the rings land.", 1.0)
seg(c, "Now, look only at the people holding a positive result.",
    "Everyone without a ring dims to 15%.")
seg(c, "Nine of them actually have the condition. Ninety nine are healthy. One hundred and eight positives in total.",
    "The 108 ringed squares fly out into two stacks on new axes (y 'people who tested positive' 0–100, ticks every 20): an orange bar of 9 and a blue bar of 99, each built from countable squares.")
seg(c, "If your test is positive, you are one of these one hundred and eight. And only nine of them are sick.",
    "A 'you are somewhere in here' bracket over both stacks; the orange 9 glows.")
seg(c, "Nine out of one hundred and eight. That's one in twelve, about eight percent.",
    "Fraction 9 / 108 (LaTeX) = 1/12 ≈ 8.3%, in violet.", 2.0)
seg(c, "The test did its job. It caught almost everyone who was sick.",
    "Tick on '9 of 10 caught'.")
seg(c, "But healthy people outnumber sick people ninety nine to one. So even a small false alarm rate creates a crowd of false alarms.",
    "Balance beam: left pan 10 orange, right pan 990 blue — beam crashes right. Then the pans swap to 9 vs 99 — still crashes right.", 1.0)
seg(c, "Here, the false alarms outnumber the real cases eleven to one.",
    "'99 ÷ 9 = 11' chip; eleven blue squares line up beside each orange one.", 1.0)
seg(c, "And yes, the test really is ninety percent accurate overall. Nine true positives, plus eight hundred and ninety one healthy people correctly cleared. Nine hundred right answers out of a thousand.",
    "Counter: '9 + 891 = 900 correct of 1,000 = 90% accurate' — the accuracy is real, it just answers a different question.", 1.0)
seg(c, "And notice, the positive result still mattered. Before the test, your chance was one in a hundred. After it, one in twelve.",
    "Probability meter 0–100% (ticks every 10, zoomed section 0–10%): warn pointer at 1%, violet pointer slides to 8.3%.")
seg(c, "That's more than eight times higher. The test moved you a lot. It just didn't move you anywhere near certain.",
    "Arrow '× 8.3' between the pointers; a faint '100% certain' marker far right.", 1.0)
seg(c, "And a negative result? Of the eight hundred and ninety two people who test negative, just one has the condition.",
    "Back to the 1,000-grid: the 892 unringed squares light up; the one missed orange square blinks.")
seg(c, "So a negative test drops your chance from one in a hundred to about one in nine hundred. That's very reassuring.",
    "Fraction 1 / 892 ≈ 0.1% (violet); meter pointer slides down from 1% to ~0.1%.", 1.5)

# ───────────────────────── 4b. BAYES' RULE ─────────────────────────
c = "Bayes' Rule"
seg(c, "What we just did, counting people, is exactly Bayes' theorem. Let's write it the way you'll see it in books.",
    "The two stacks (9 and 99) shrink to the left side; a blank formula card appears on the right.")
seg(c, "Here is the same crowd as a tree. One thousand people split into ten who have it, and nine hundred and ninety who don't.",
    "Tree diagram builds left to right: root '1,000' → branches '10 have it' (orange, 'x 1/100') and '990 healthy' (blue, 'x 99/100').")
seg(c, "Then each branch splits again by the test result. Nine and one on top. Ninety nine and eight hundred and ninety one below.",
    "Second split: 10 → '9 positive' (aqua ring) / '1 negative'; 990 → '99 positive' (aqua ring) / '891 negative'. Branch labels 9/10, 1/10, 1/10, 9/10.")
seg(c, "A positive result means you're on one of the two positive leaves. Nine, or ninety nine. That's all Bayes is doing.",
    "The two positive leaves glow; the others dim; bracket '9 of 108'.", 1.0)
seg(c, "First, the symbols. A capital P, with brackets, means the probability of whatever is inside.",
    "Definition card: 'P( … ) = the probability of …'.")
seg(c, "A means having the condition. B means testing positive.",
    "Definition cards: 'A = has the condition' (orange), 'B = tests positive' (aqua).")
seg(c, "And this vertical bar means given. So, P of A given B is the chance you have the condition, given that you tested positive.",
    "Definition card '| = given'. Then 'P(A | B) = chance you have it, given a positive test' (violet).")
seg(c, "That's the number we want. And here is Bayes' theorem.",
    "The full formula writes on: P(A|B) = P(B|A) · P(A) / P(B).", 1.0)
seg(c, "P of A given B equals P of B given A, times P of A, divided by P of B.",
    "Each term brightens as it is read.")
seg(c, "Now let's match each piece to our crowd.",
    "Dashed connectors from each term to the crowd stacks.")
seg(c, "P of A is the base rate. How common the condition is before any test. Ten in a thousand.",
    "P(A) glows warn; below it '= 10 / 1000'.")
seg(c, "P of B given A is how good the test is at catching it. Nine out of ten.",
    "P(B|A) glows aqua; '= 9 / 10'.")
seg(c, "Multiply those two, and you get the true positives. Nine in a thousand.",
    "'9/10 × 10/1000 = 9/1000'; the orange stack of 9 pulses.")
seg(c, "P of B, on the bottom, is the chance of testing positive at all. Real or false, that's one hundred and eight in a thousand.",
    "P(B) underlined; '= 108 / 1000'; both stacks pulse.")
seg(c, "Divide, and the thousands cancel. Nine out of one hundred and eight. The same answer we got by counting.",
    "'(9/1000) ÷ (108/1000) = 9/108 ≈ 8.3%' in violet.", 1.5)
seg(c, "So the formula is just a short way of saying: real positives, divided by all positives.",
    "Plain-words version under the formula: 'real positives ÷ all positives'.", 1.0)
seg(c, "The bottom part is where people slip. It hides the false alarms.",
    "P(B) splits open like a box: inside, '9 real' + '99 false alarms' (the 99 glowing).")
seg(c, "Written out in full, P of B is the true positives from the sick, plus the false alarms from the healthy.",
    "Expanded: P(B) = P(B|A)·P(A) + P(B|not A)·P(not A); definition chip 'not A = healthy'; numbers 9/1000 + 99/1000.")
seg(c, "Three names you'll hear. The base rate is called the prior. The answer is called the posterior. And P of B given A is called the likelihood.",
    "Labels attach to the formula: 'prior' (warn) under P(A), 'likelihood' (aqua) under P(B|A), 'posterior' (violet) under P(A|B).")
seg(c, "Prior means before the evidence. Posterior means after.",
    "Timeline arrow: 'before evidence → after evidence', prior 1% → posterior 8.3%.", 1.0)

# ───────────────────────── 4c. TEST AGAIN ─────────────────────────
c = "Test Again"
seg(c, "So you tested positive, and your chance is now about one in twelve. What would a sensible doctor do next?",
    "The violet '1 in 12' card; a second test tube icon slides in.")
seg(c, "Test again. And here is the beautiful part. The answer from the first test becomes the starting point for the second.",
    "Loop arrow: posterior (violet) curls back around and becomes the new prior (warn).")
seg(c, "Yesterday's posterior is today's prior.",
    "Text card with the loop arrow; 'posterior → prior'.", 1.0)
seg(c, "Take our one hundred and eight positives. Nine are sick, ninety nine are healthy. They all take a second test.",
    "The two stacks (9 orange, 99 blue) return on their axes.")
seg(c, "To avoid fractions of people, picture ten times as many. Ninety people who have it, and nine hundred and ninety who don't.",
    "'× 10' badge; stacks rescale: y axis now 0–1,000, ticks every 200; bars 90 and 990.")
seg(c, "The test catches nine in ten of the sick, and wrongly flags one in ten of the healthy. Same as before.",
    "Aqua rings sweep the bars: 90 → 81 kept; 990 → 99 kept.")
seg(c, "After a second positive: eighty one sick, and ninety nine healthy.",
    "New bars: orange 81, blue 99 (axis 0–100, ticks every 20) — now nearly level.")
seg(c, "Eighty one out of one hundred and eighty. That's forty five percent.",
    "Fraction 81 / 180 = 45% in violet.", 1.5)
seg(c, "One percent, then eight, then forty five. Each positive pushes the number up.",
    "Number-line walk on the meter 0–100%: pointer hops 1% → 8.3% → 45%.")
seg(c, "There's a neat shortcut here. Compare sick to healthy as odds.",
    "Balance beam returns with 'odds = sick : healthy'.")
seg(c, "Before any test, the odds are one sick person for every ninety nine healthy.",
    "Beam: 1 orange vs 99 blue → '1 : 99'.")
seg(c, "A sick person is nine times more likely to test positive than a healthy one. Ninety percent, versus ten.",
    "'90% ÷ 10% = 9' chip, labelled 'likelihood ratio'.")
seg(c, "So each positive multiplies the odds of having it by nine. One to ninety nine becomes nine to ninety nine, then eighty one to ninety nine.",
    "Odds ladder: 1 : 99 → × 9 → 9 : 99 → × 9 → 81 : 99; beam levels out step by step.")
seg(c, "A third positive makes it seven hundred and twenty nine to ninety nine. About eighty eight percent.",
    "'729 : 99 → 729 / 828 ≈ 88%'; meter pointer hops to 88%. Beam tips toward 'sick'.", 1.0)
seg(c, "One important condition. This only works if the second test makes its mistakes independently of the first.",
    "Assumption card (white border): 'assumes the tests' errors are independent'.")
seg(c, "If you repeat the same test on the same sample, it might simply repeat the same false alarm. Then the second positive tells you much less.",
    "Two identical test tubes; the same smudge on both → '= 1 clue, not 2'.")
seg(c, "That's one reason doctors often confirm with a different kind of test.",
    "Second tube changes shape and colour: 'different method'.", 1.0)

# ───────────────────────── 4d. WHAT MOVES THE ANSWER ─────────────────────────
c = "What Moves the Answer"
seg(c, "So what actually moves the answer? There are only three dials. The base rate, the hit rate, and the false alarm rate.",
    "Three dials: 'base rate' (warn) at 1 in 100, 'hit rate' (aqua) at 9 in 10, 'false alarm rate' (blue) at 1 in 10.")
seg(c, "Let's turn the base rate dial first, and keep the test exactly the same.",
    "Axes: x 'base rate (%)' 0–50 (ticks every 10), y 'chance you have it after a positive (%)' 0–100 (ticks every 20).")
seg(c, "At one in a hundred, we're at eight percent. At one in ten, it jumps to fifty percent.",
    "A violet curve traces from left; dots pinned at (1, 8.3) and (10, 50) with labels.")
seg(c, "Let's check that middle one by counting. With one in ten, a thousand people means one hundred sick, and the test catches ninety of them.",
    "Mini crowd: 100 orange squares (ten columns of the 40 x 25 grid), 90 ringed aqua.", sid="s085a")
seg(c, "Nine hundred healthy, and one in ten flagged. Ninety false alarms. Ninety real, ninety false. Fifty percent.",
    "900 blue, 90 ringed; two equal stacks 90 | 90 on axes 0–100; '90 / 180 = 50%' violet.", 1.0, sid="s085b")
seg(c, "And only when half the people have the condition does your gut's ninety percent finally become right.",
    "Curve reaches (50, 90); a grey 'gut: 90%' dashed line meets it there.", 1.5)
seg(c, "The rarer the condition, the more the false alarms win.",
    "Left end of the curve highlighted; '1 in 100 → 8%'.", 1.0)
seg(c, "Now turn the false alarm dial instead. Same base rate, one in a hundred, but a test that wrongly flags only one healthy person in a hundred.",
    "False-alarm dial turns from 1 in 10 to 1 in 100; the blue stack of 99 shrinks.")
seg(c, "Now there are about ten false alarms instead of ninety nine, and a positive means about forty eight percent.",
    "Stacks: orange 9 vs blue 9.9 (≈10); '9 / 18.9 ≈ 48%' in violet.")
seg(c, "And the hit rate dial? Push it from nine in ten all the way to perfect, and the answer barely moves. From about eight percent to about nine.",
    "Hit-rate dial turns to 10 of 10; orange stack 9 → 10; '10 / 109 ≈ 9%'.", 1.0)
seg(c, "So, a rule of thumb. When the thing you're looking for is rare, the false alarm rate matters far more than the hit rate.",
    "Rule-of-thumb card: 'rare thing → false alarm rate matters most' (labelled 'rule of thumb').", 1.5)

# ───────────────────────── 5. REAL WORLD ─────────────────────────
c = "Real World"
seg(c, "Now let's see where this shows up in the real world. The labels change, but the counting is the same.",
    "Four domain tiles: ML, DS, FINANCE, CS.")
seg(c, "Machine learning. A classifier is just a test run by a computer.",
    "ML tile expands: input dots → model box → 'positive' / 'negative' outputs.")
seg(c, "Engineers have names for our numbers. Catching nine out of ten sick people is called recall.",
    "'recall = 9 / 10 = 90%' (aqua), with the orange column of 10 and 9 rings.")
seg(c, "And nine out of one hundred and eight, the share of alarms that are real, is called precision.",
    "'precision = 9 / 108 ≈ 8%' (violet), with the two stacks.")
seg(c, "When the thing you're looking for is rare, a model can have great recall and still terrible precision. That's the base rate at work.",
    "Two gauges side by side: recall 90% (full), precision 8% (nearly empty).", 1.0)
seg(c, "That's why teams measure precision on data with the real base rate. On a balanced test set, half positive and half negative, our same test would show ninety percent precision. In the real world, about eight percent.",
    "Two panels: 'balanced test set (50% positive) → precision 90%' vs 'real world (1% positive) → precision 8%'.", 1.0, sid="s096a")
seg(c, "And here's a trap. A model that simply says healthy to everyone is ninety nine percent accurate, and completely useless.",
    "Grid of 1,000 all marked 'healthy': '990 / 1000 correct = 99% accuracy' with a red '0 of 10 caught'.", 1.0)
seg(c, "Data science. Bayes is the engine of Bayesian statistics.",
    "DS tile expands.")
seg(c, "You start with a prior belief, say, about how often visitors to a website buy something, and update it as each day's data comes in.",
    "Axes x 'purchase rate (%)' 0–10, y 'belief (shape only)': a wide warn curve narrows into a violet curve as day-1, day-2, day-3 data chips arrive. Labelled 'shape only'.")
seg(c, "Each day's posterior becomes the next day's prior. Exactly like our second test.",
    "Loop arrow posterior → prior, as in the Test Again chapter.", 1.0)
seg(c, "And before trusting any automated flag on a dashboard, a good analyst asks: of all the past flags, how many were real? That's precision again, measured on real data.",
    "Dashboard card with a column of past flags: few aqua-ringed orange (real), many blue (false); 'real ÷ all flags'.", sid="s100a")
seg(c, "Finance. Banks run fraud detectors on card payments.",
    "Finance tile expands: card + payment stream.")
seg(c, "Fraud is rare, far rarer than one in a hundred payments. So even a detector as good as our test would flag mostly honest payments.",
    "Same 1,000-grid relabelled 'payments', with even fewer orange squares; aqua flags land mostly on blue ('honest').")
seg(c, "That's one reason many banks send a quick, was this you, message instead of simply blocking the card. In Bayes terms, your reply is a second, independent test.",
    "Phone with 'Was this you?' → reply 'Yes' → meter drops / 'No' → meter jumps.", 1.0)
seg(c, "The same idea applies to market signals. A warning sign that fired before most crashes may also fire in many calm years. Always ask how often it fires when nothing happens.",
    "Timeline of years (axis 'year 1–20', generic, labelled 'illustration'): signal flags on several years, only two of them crash years.", 1.0, sid="s103a")
seg(c, "Computer science. Some of the first really effective spam filters were built on Bayes' theorem.",
    "CS tile expands: inbox with a spam folder.")
seg(c, "The prior is how much of all email is spam. The evidence is the words inside.",
    "Email card; words 'FREE', 'winner', 'meeting' highlighted; prior chip 'share of email that is spam'.")
seg(c, "Each word nudges the odds up or down, just like each positive test. The filter multiplies them together.",
    "Odds ladder like before: '× (FREE)' up, '× (meeting)' down. Each arrow labelled 'shape only' factors.")
seg(c, "To keep it simple, it treats every word as independent of the others. That shortcut is why it's called naive Bayes. It isn't true, but it works surprisingly well.",
    "'naive Bayes = assume words are independent' card; a check mark 'works surprisingly well'.", 1.0)
seg(c, "Computer security has the same problem. An intrusion alarm that fires on just one in a thousand normal logins can still bury the few real attacks under false alarms.",
    "Login stream: thousands of blue login dots, rare orange attack dots; aqua alarms mostly on blue.", 1.0, sid="s107a")

# ───────────────────────── 6. COMMON MISTAKES ─────────────────────────
c = "Common Mistakes"
seg(c, "Before we wrap up, here are the three most common mistakes people make with Bayes.",
    "Three red cards face down.")
seg(c, "Mistake one: flipping the question.",
    "Card 1 flips: 'Flipping the question'.")
seg(c, "The chance of a positive test, if you're sick, is ninety percent. The chance you're sick, if you test positive, is about eight percent.",
    "P(B | A) = 90% (aqua) above P(A | B) ≈ 8% (violet); the A and B letters swap places.")
seg(c, "Same words, swapped around. Completely different numbers.",
    "Red swap arrows between the two; '90% ≠ 8%'.", 1.0)
seg(c, "In courtrooms, this flip has a name: the prosecutor's fallacy. The chance of the evidence if someone is innocent is not the chance they're innocent, given the evidence.",
    "Scales of justice icon; two cards 'P(evidence | innocent)' vs 'P(innocent | evidence)' with '≠'.", 1.0)
seg(c, "Mistake two: ignoring the base rate.",
    "Card 2 flips: 'Ignoring the base rate'.")
seg(c, "Take the same test, but give it only to patients who already have symptoms. Say one in five of them has the condition.",
    "Same 40 x 25 grid; now 200 squares (five columns) turn orange; warn tag 'base rate 1 in 5'.")
seg(c, "Out of a thousand, that's one hundred and eighty true positives, against eighty false alarms. Now a positive means about seventy percent.",
    "Stacks: orange 180 vs blue 80 (axis 0–200, ticks every 50); '180 / 260 ≈ 69%' in violet.")
seg(c, "Same test. Same result. The base rate changed everything.",
    "Side by side: 'base rate 1 in 100 → 8%' vs 'base rate 1 in 5 → 69%'.", 2.0)
seg(c, "Mistake three: counting the same clue twice.",
    "Card 3 flips: 'Counting a clue twice'.")
seg(c, "If two tests share the same weakness, or two news stories copy the same source, they are really one piece of evidence, not two.",
    "Two news cards with arrows back to one source card.")
seg(c, "Multiply them as if they were independent, and you'll end up far too confident.",
    "Meter pointer overshoots to 88% (red 'overconfident'), then settles back toward 8% with '1 clue'.", 1.0)
seg(c, "And a bonus mistake: deciding the test is useless because the answer was only eight percent.",
    "Red card 'Bonus: “the test is useless”'.")
seg(c, "It isn't. A positive raised the chance more than eightfold, and a negative almost rules the condition out. A good test is a strong clue. It's just not a verdict.",
    "Meter: 1% → 8.3% (positive) and 1% → 0.1% (negative), both arrows big.", 1.0)

# ───────────────────────── 7. RECIPE ─────────────────────────
c = "Recipe"
seg(c, "Let's turn all of that into a recipe you can use for any yes or no question.",
    "Recipe card frame unrolls: 'Bayes in five steps'.")
seg(c, "Step one: start with the base rate. How common is the thing, before any evidence?",
    "Item 1 (warn): 'Start with the base rate' + 'how common is it before any evidence?'.")
seg(c, "Step two: picture a crowd. One thousand people usually avoids fractions.",
    "Item 2: 'Picture a crowd' + 'e.g. 1,000 people'.")
seg(c, "Step three: split the crowd with the test. Count the true positives, and the false alarms.",
    "Item 3 (aqua): 'Split by the test' + 'true positives and false alarms'.")
seg(c, "Step four: keep only the people who match the evidence, and divide. Real cases, over all positives.",
    "Item 4 (violet): 'Keep the matches and divide' + 'real ÷ all positives'.")
seg(c, "Step five: update. When new, independent evidence arrives, your answer becomes the new base rate.",
    "Item 5: 'Update' + 'posterior becomes the next prior'.", 1.5)
seg(c, "For our test: one in a hundred to start. Nine real positives, ninety nine false alarms. About eight percent.",
    "Summary strip under the card: '1 in 100 → 9 real vs 99 false → 9/108 ≈ 8%'.", 1.0)
seg(c, "A test result is a clue, not a verdict. Bayes tells you how much the clue is worth.",
    "Closing line types on in violet, centred.", 2.0)

# ─────────── 8. SUBSCRIBE (channel outro) ───────────
c = "Subscribe"
seg(c, "Look around your world, and notice how many alarms are false alarms, and how rare the real thing usually is.",
    "Four everyday cards: smoke alarm, car alarm, spam folder, 'was this you?' text — each stamped 'real or false alarm?'.", 0.6)
seg(c, "If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together.",
    "Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓'; 'so we can keep building together' appears.", 0.8)

# ───────────────────────── 9. NEXT TIME ─────────────────────────
c = "Next Time"
seg(c, "But here's a puzzle for next time.",
    "Small logo stays top-centre; a puzzle-piece icon draws on.")
seg(c, "Scientists often report a number called a p-value, and it's very often described as the chance that a result is a fluke.",
    "Card 'p = 0.03' with a speech bubble 'a 3% chance it's a fluke?' and a red question mark.")
seg(c, "That description flips the question, just like mistake one.",
    "The two flipped cards from mistake one reappear: 'P(data | no effect)' vs 'P(no effect | data)'.")
seg(c, "Next time, we'll see what a p-value really measures, and why Bayes is the missing piece.",
    "Chip 'next: p-values' appears under the small logo.")
seg(c, "I will see you in the next video.",
    "Logo + 'next: p-values' chip hold.", 2.0)

if __name__ == "__main__":
    out = pathlib.Path(__file__).parent
    (out / "script.json").write_text(json.dumps(S, indent=2, ensure_ascii=False))
    words = sum(len(s["text"].split()) for s in S)
    pauses = sum(s["pause_after"] for s in S)
    md = [f"# Bayes' Theorem Explained Simply, With Real Examples\n",
          f"{len(S)} segments · {words} words · est. {words/150+pauses/60:.1f} min at 150 wpm (incl. {pauses:.0f} s pauses)\n"]
    cur = None
    chap_words = {}
    for s in S:
        chap_words[s["chapter"]] = chap_words.get(s["chapter"], 0) + len(s["text"].split())
    for s in S:
        if s["chapter"] != cur:
            cur = s["chapter"]
            w = chap_words[cur]
            md.append(f"\n## {cur}  ·  {w} words, ~{w/150*60:.0f} s\n")
        p = f" ⏸{s['pause_after']}s" if s["pause_after"] > D else ""
        md.append(f"- **{s['id']}** {s['text']}{p}\n  - *Visual:* {s['visual']}")
    (out / "script.md").write_text("\n".join(md) + "\n")
    print(md[1])
    for k, v in chap_words.items():
        print(f"  {k:20s} {v:4d} words ~{v/150*60:5.0f} s")
