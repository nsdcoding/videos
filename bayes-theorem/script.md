# Bayes' Theorem Explained Simply, With Real Examples

143 segments · 2475 words · est. 18.0 min at 150 wpm (incl. 91 s pauses)


## The Positive Test  ·  186 words, ~74 s

- **s001** Imagine you go for a routine health check, and the doctor suggests a quick screening test.
  - *Visual:* Line-art clinic door draws on; a small person icon walks to it; a clipboard with 'screening test' pops up.
- **s002** It looks for a condition that is fairly rare. About one in every hundred people your age has it.
  - *Visual:* 10 x 10 grid of person squares on axes (columns 1–10, rows 1–10); one square turns orange. Chip: '1 in 100 have it'.
- **s003** The test is good. If you have the condition, it catches it nine times out of ten.
  - *Visual:* Stat card 1: ten orange squares; nine get an aqua 'positive' ring. Caption 'catches 9 of 10 who have it'.
- **s004** And if you are healthy, it only gives a false alarm one time in ten.
  - *Visual:* Stat card 2: ten blue squares; one gets an aqua ring. Caption 'false alarm for 1 in 10 healthy people'.
- **s005** A few days later, the result comes back. Positive. ⏸1.0s
  - *Visual:* An envelope slides in and opens; 'POSITIVE' stamps on in aqua.
- **s006** So, how worried should you be? What is the chance you actually have it?
  - *Visual:* A probability meter appears: a horizontal axis 0%–100% with ticks every 10, title 'chance you have it'.
- **s006a** Take a second, and make your own guess. ⏸1.5s
  - *Visual:* The meter waits; a blinking '?' cursor sits on it; tiny clock ticks.
- **s007** Most people say about ninety percent. After all, the test is ninety percent accurate.
  - *Visual:* A grey 'gut feeling' pointer slides to 90% on the meter.
- **s008** Here's the surprise. The real answer is about eight percent. ⏸2.0s
  - *Visual:* A violet pointer drops in at 8.3%; the grey 90% pointer is crossed out in red.
- **s009** Not ninety. Eight. Less than one in ten. ⏸1.0s
  - *Visual:* Big comparison: '90%' (grey, struck) vs '≈ 8%' (violet), camera pushes in on the violet number.
- **s010** Nothing in that story is a trick. The test really is good. Your gut just left out one number.
  - *Visual:* The three fact chips line up: '1 in 100 have it' · 'catches 9 of 10' · 'false alarm 1 in 10'.
- **s011** How rare the condition was to begin with. ⏸1.0s
  - *Visual:* The '1 in 100' chip turns warn yellow and glows: 'the base rate'.
- **s012** The tool that puts that number back in is called Bayes' theorem. And by the end of this video, you will be able to do this in your head. ⏸1.0s
  - *Visual:* Title card: 'BAYES' THEOREM' (violet) with subtitle 'explained simply, with real examples'.

## Welcome  ·  60 words, ~24 s

- **s013** Welcome to Math Lab TV. Where math is something you can see. ⏸0.7s
  - *Visual:* Logo (violet rounded square with a green bell curve) + MATH LAB TV + tagline 'where math is something you can see'.
- **s014** Today you will learn how to turn a test result into a real probability, just by counting people.
  - *Visual:* Small logo moves top-right. Big ① (aqua); mini grid where 108 squares light up and 9 turn orange; caption 'turn a test result into a real probability'.
- **s015** You will see Bayes' theorem as a formula, and exactly what every symbol means.
  - *Visual:* Big ② (violet); the formula P(A|B) = P(B|A)·P(A) / P(B) writes on; caption 'the formula, symbol by symbol'.
- **s016** And you will see how evidence adds up, in spam filters, fraud alerts and machine learning. ⏸0.6s
  - *Visual:* Big ③ (warn); a mini meter walks 1% → 8% → 45%; caption 'how evidence adds up'.

## Why It Matters  ·  167 words, ~67 s

- **s017** This isn't just about medical tests.
  - *Visual:* The clinic icon shrinks to the corner; three empty cards slide in.
- **s018** Any time a rare thing meets an imperfect detector, the same trap is waiting.
  - *Visual:* Equation of icons: 'rare thing' (orange dot) + 'imperfect detector' (aqua radar) = 'trap' (red).
- **s019** A smoke alarm going off. An email flagged as spam. A message from your bank asking, was this you?
  - *Visual:* Three cards fill in turn: smoke alarm, envelope with 'spam' tag, phone with 'Was this you?'.
- **s020** Each one is a positive test. And each one asks the same question: given this alarm, how likely is the real thing? ⏸1.0s
  - *Visual:* Each card gets an aqua 'positive' ring; a banner: 'given the alarm → how likely is the real thing?'.
- **s021** And smart people get this wrong. In one well known study, doctors were given a screening puzzle with numbers like ours.
  - *Visual:* Card 'Study of doctors · a screening puzzle like ours' (generic, no names or logos).
- **s022** Only about one in five picked the right answer. Almost half picked nine in ten. ⏸1.0s
  - *Visual:* Bar chart on axes, y 'share of doctors (%)' 0–50: bar 'about 1 in 10 (correct)' ≈ 21%, bar '9 in 10' ≈ 47%.
- **s023** That's not because doctors are bad at math. It's because the numbers came as percentages of percentages.
  - *Visual:* A jumble of '%' signs ('1%', '90%', '10%') swirl together.
- **s024** Change the form, and the problem becomes easy. So here is the trick for this whole video: stop thinking in percentages, and start counting people. ⏸1.0s
  - *Visual:* The '%' signs morph into a neat grid of person squares. Chip: 'count people'.
- **s025** And Bayes isn't only about tests. It's a rule for changing your mind by the right amount when new evidence arrives. Not too little, and not too much. ⏸1.0s
  - *Visual:* A dial labelled 'how sure am I?' turns a little, not all the way: 'update by the right amount'.

## Count the Crowd  ·  320 words, ~128 s

- **s026** Let's do it. Picture one thousand people, all taking the same test.
  - *Visual:* Axes appear: x 'column' 0–40 (ticks every 5), y 'row' 0–25 (ticks every 5), equal scale. A 40 x 25 grid of squares fills in, counter 0 → 1,000.
- **s027** Each little square is one person. Forty across, twenty five down. One thousand.
  - *Visual:* Camera zooms to the top-left corner: one square labelled 'one person'; then '40 × 25 = 1,000'.
- **s028** Step one. How many of them have the condition? One in a hundred. So, ten people.
  - *Visual:* Step chip '1'. Ten squares in the first column turn orange; counter '10 have it' (orange); warn tag 'base rate 1 in 100'.
- **s029** The other nine hundred and ninety are healthy.
  - *Visual:* The rest pulse blue; counter '990 healthy' (blue).
- **s030** Step two. Test the ten people who have the condition. It catches nine of them.
  - *Visual:* Step chip '2'. Camera zooms on the orange column; nine get aqua rings one by one.
- **s031** So, nine true positives, and one person the test misses.
  - *Visual:* Labels: '9 true positives' (aqua) and '1 missed' (muted) beside the column.
- **s032** Step three. Test the nine hundred and ninety healthy people. It wrongly flags one in ten of them.
  - *Visual:* Step chip '3'. Camera pulls back; aqua rings ripple across the blue squares, one in every ten.
- **s033** That's ninety nine false alarms. ⏸1.0s
  - *Visual:* Counter '99 false alarms' ticks up in aqua as the rings land.
- **s034** Now, look only at the people holding a positive result.
  - *Visual:* Everyone without a ring dims to 15%.
- **s035** Nine of them actually have the condition. Ninety nine are healthy. One hundred and eight positives in total.
  - *Visual:* The 108 ringed squares fly out into two stacks on new axes (y 'people who tested positive' 0–100, ticks every 20): an orange bar of 9 and a blue bar of 99, each built from countable squares.
- **s036** If your test is positive, you are one of these one hundred and eight. And only nine of them are sick.
  - *Visual:* A 'you are somewhere in here' bracket over both stacks; the orange 9 glows.
- **s037** Nine out of one hundred and eight. That's one in twelve, about eight percent. ⏸2.0s
  - *Visual:* Fraction 9 / 108 (LaTeX) = 1/12 ≈ 8.3%, in violet.
- **s038** The test did its job. It caught almost everyone who was sick.
  - *Visual:* Tick on '9 of 10 caught'.
- **s039** But healthy people outnumber sick people ninety nine to one. So even a small false alarm rate creates a crowd of false alarms. ⏸1.0s
  - *Visual:* Balance beam: left pan 10 orange, right pan 990 blue — beam crashes right. Then the pans swap to 9 vs 99 — still crashes right.
- **s040** Here, the false alarms outnumber the real cases eleven to one. ⏸1.0s
  - *Visual:* '99 ÷ 9 = 11' chip; eleven blue squares line up beside each orange one.
- **s041** And yes, the test really is ninety percent accurate overall. Nine true positives, plus eight hundred and ninety one healthy people correctly cleared. Nine hundred right answers out of a thousand. ⏸1.0s
  - *Visual:* Counter: '9 + 891 = 900 correct of 1,000 = 90% accurate' — the accuracy is real, it just answers a different question.
- **s042** And notice, the positive result still mattered. Before the test, your chance was one in a hundred. After it, one in twelve.
  - *Visual:* Probability meter 0–100% (ticks every 10, zoomed section 0–10%): warn pointer at 1%, violet pointer slides to 8.3%.
- **s043** That's more than eight times higher. The test moved you a lot. It just didn't move you anywhere near certain. ⏸1.0s
  - *Visual:* Arrow '× 8.3' between the pointers; a faint '100% certain' marker far right.
- **s044** And a negative result? Of the eight hundred and ninety two people who test negative, just one has the condition.
  - *Visual:* Back to the 1,000-grid: the 892 unringed squares light up; the one missed orange square blinks.
- **s045** So a negative test drops your chance from one in a hundred to about one in nine hundred. That's very reassuring. ⏸1.5s
  - *Visual:* Fraction 1 / 892 ≈ 0.1% (violet); meter pointer slides down from 1% to ~0.1%.

## Bayes' Rule  ·  352 words, ~141 s

- **s046** What we just did, counting people, is exactly Bayes' theorem. Let's write it the way you'll see it in books.
  - *Visual:* The two stacks (9 and 99) shrink to the left side; a blank formula card appears on the right.
- **s047** Here is the same crowd as a tree. One thousand people split into ten who have it, and nine hundred and ninety who don't.
  - *Visual:* Tree diagram builds left to right: root '1,000' → branches '10 have it' (orange, 'x 1/100') and '990 healthy' (blue, 'x 99/100').
- **s048** Then each branch splits again by the test result. Nine and one on top. Ninety nine and eight hundred and ninety one below.
  - *Visual:* Second split: 10 → '9 positive' (aqua ring) / '1 negative'; 990 → '99 positive' (aqua ring) / '891 negative'. Branch labels 9/10, 1/10, 1/10, 9/10.
- **s049** A positive result means you're on one of the two positive leaves. Nine, or ninety nine. That's all Bayes is doing. ⏸1.0s
  - *Visual:* The two positive leaves glow; the others dim; bracket '9 of 108'.
- **s050** First, the symbols. A capital P, with brackets, means the probability of whatever is inside.
  - *Visual:* Definition card: 'P( … ) = the probability of …'.
- **s051** A means having the condition. B means testing positive.
  - *Visual:* Definition cards: 'A = has the condition' (orange), 'B = tests positive' (aqua).
- **s052** And this vertical bar means given. So, P of A given B is the chance you have the condition, given that you tested positive.
  - *Visual:* Definition card '| = given'. Then 'P(A | B) = chance you have it, given a positive test' (violet).
- **s053** That's the number we want. And here is Bayes' theorem. ⏸1.0s
  - *Visual:* The full formula writes on: P(A|B) = P(B|A) · P(A) / P(B).
- **s054** P of A given B equals P of B given A, times P of A, divided by P of B.
  - *Visual:* Each term brightens as it is read.
- **s055** Now let's match each piece to our crowd.
  - *Visual:* Dashed connectors from each term to the crowd stacks.
- **s056** P of A is the base rate. How common the condition is before any test. Ten in a thousand.
  - *Visual:* P(A) glows warn; below it '= 10 / 1000'.
- **s057** P of B given A is how good the test is at catching it. Nine out of ten.
  - *Visual:* P(B|A) glows aqua; '= 9 / 10'.
- **s058** Multiply those two, and you get the true positives. Nine in a thousand.
  - *Visual:* '9/10 × 10/1000 = 9/1000'; the orange stack of 9 pulses.
- **s059** P of B, on the bottom, is the chance of testing positive at all. Real or false, that's one hundred and eight in a thousand.
  - *Visual:* P(B) underlined; '= 108 / 1000'; both stacks pulse.
- **s060** Divide, and the thousands cancel. Nine out of one hundred and eight. The same answer we got by counting. ⏸1.5s
  - *Visual:* '(9/1000) ÷ (108/1000) = 9/108 ≈ 8.3%' in violet.
- **s061** So the formula is just a short way of saying: real positives, divided by all positives. ⏸1.0s
  - *Visual:* Plain-words version under the formula: 'real positives ÷ all positives'.
- **s062** The bottom part is where people slip. It hides the false alarms.
  - *Visual:* P(B) splits open like a box: inside, '9 real' + '99 false alarms' (the 99 glowing).
- **s063** Written out in full, P of B is the true positives from the sick, plus the false alarms from the healthy.
  - *Visual:* Expanded: P(B) = P(B|A)·P(A) + P(B|not A)·P(not A); definition chip 'not A = healthy'; numbers 9/1000 + 99/1000.
- **s064** Three names you'll hear. The base rate is called the prior. The answer is called the posterior. And P of B given A is called the likelihood.
  - *Visual:* Labels attach to the formula: 'prior' (warn) under P(A), 'likelihood' (aqua) under P(B|A), 'posterior' (violet) under P(A|B).
- **s065** Prior means before the evidence. Posterior means after. ⏸1.0s
  - *Visual:* Timeline arrow: 'before evidence → after evidence', prior 1% → posterior 8.3%.

## Test Again  ·  287 words, ~115 s

- **s066** So you tested positive, and your chance is now about one in twelve. What would a sensible doctor do next?
  - *Visual:* The violet '1 in 12' card; a second test tube icon slides in.
- **s067** Test again. And here is the beautiful part. The answer from the first test becomes the starting point for the second.
  - *Visual:* Loop arrow: posterior (violet) curls back around and becomes the new prior (warn).
- **s068** Yesterday's posterior is today's prior. ⏸1.0s
  - *Visual:* Text card with the loop arrow; 'posterior → prior'.
- **s069** Take our one hundred and eight positives. Nine are sick, ninety nine are healthy. They all take a second test.
  - *Visual:* The two stacks (9 orange, 99 blue) return on their axes.
- **s070** To avoid fractions of people, picture ten times as many. Ninety people who have it, and nine hundred and ninety who don't.
  - *Visual:* '× 10' badge; stacks rescale: y axis now 0–1,000, ticks every 200; bars 90 and 990.
- **s071** The test catches nine in ten of the sick, and wrongly flags one in ten of the healthy. Same as before.
  - *Visual:* Aqua rings sweep the bars: 90 → 81 kept; 990 → 99 kept.
- **s072** After a second positive: eighty one sick, and ninety nine healthy.
  - *Visual:* New bars: orange 81, blue 99 (axis 0–100, ticks every 20) — now nearly level.
- **s073** Eighty one out of one hundred and eighty. That's forty five percent. ⏸1.5s
  - *Visual:* Fraction 81 / 180 = 45% in violet.
- **s074** One percent, then eight, then forty five. Each positive pushes the number up.
  - *Visual:* Number-line walk on the meter 0–100%: pointer hops 1% → 8.3% → 45%.
- **s075** There's a neat shortcut here. Compare sick to healthy as odds.
  - *Visual:* Balance beam returns with 'odds = sick : healthy'.
- **s076** Before any test, the odds are one sick person for every ninety nine healthy.
  - *Visual:* Beam: 1 orange vs 99 blue → '1 : 99'.
- **s077** A sick person is nine times more likely to test positive than a healthy one. Ninety percent, versus ten.
  - *Visual:* '90% ÷ 10% = 9' chip, labelled 'likelihood ratio'.
- **s078** So each positive multiplies the odds of having it by nine. One to ninety nine becomes nine to ninety nine, then eighty one to ninety nine.
  - *Visual:* Odds ladder: 1 : 99 → × 9 → 9 : 99 → × 9 → 81 : 99; beam levels out step by step.
- **s079** A third positive makes it seven hundred and twenty nine to ninety nine. About eighty eight percent. ⏸1.0s
  - *Visual:* '729 : 99 → 729 / 828 ≈ 88%'; meter pointer hops to 88%. Beam tips toward 'sick'.
- **s080** One important condition. This only works if the second test makes its mistakes independently of the first.
  - *Visual:* Assumption card (white border): 'assumes the tests' errors are independent'.
- **s081** If you repeat the same test on the same sample, it might simply repeat the same false alarm. Then the second positive tells you much less.
  - *Visual:* Two identical test tubes; the same smudge on both → '= 1 clue, not 2'.
- **s082** That's one reason doctors often confirm with a different kind of test. ⏸1.0s
  - *Visual:* Second tube changes shape and colour: 'different method'.

## What Moves the Answer  ·  221 words, ~88 s

- **s083** So what actually moves the answer? There are only three dials. The base rate, the hit rate, and the false alarm rate.
  - *Visual:* Three dials: 'base rate' (warn) at 1 in 100, 'hit rate' (aqua) at 9 in 10, 'false alarm rate' (blue) at 1 in 10.
- **s084** Let's turn the base rate dial first, and keep the test exactly the same.
  - *Visual:* Axes: x 'base rate (%)' 0–50 (ticks every 10), y 'chance you have it after a positive (%)' 0–100 (ticks every 20).
- **s085** At one in a hundred, we're at eight percent. At one in ten, it jumps to fifty percent.
  - *Visual:* A violet curve traces from left; dots pinned at (1, 8.3) and (10, 50) with labels.
- **s085a** Let's check that middle one by counting. With one in ten, a thousand people means one hundred sick, and the test catches ninety of them.
  - *Visual:* Mini crowd: 100 orange squares (ten columns of the 40 x 25 grid), 90 ringed aqua.
- **s085b** Nine hundred healthy, and one in ten flagged. Ninety false alarms. Ninety real, ninety false. Fifty percent. ⏸1.0s
  - *Visual:* 900 blue, 90 ringed; two equal stacks 90 | 90 on axes 0–100; '90 / 180 = 50%' violet.
- **s086** And only when half the people have the condition does your gut's ninety percent finally become right. ⏸1.5s
  - *Visual:* Curve reaches (50, 90); a grey 'gut: 90%' dashed line meets it there.
- **s087** The rarer the condition, the more the false alarms win. ⏸1.0s
  - *Visual:* Left end of the curve highlighted; '1 in 100 → 8%'.
- **s088** Now turn the false alarm dial instead. Same base rate, one in a hundred, but a test that wrongly flags only one healthy person in a hundred.
  - *Visual:* False-alarm dial turns from 1 in 10 to 1 in 100; the blue stack of 99 shrinks.
- **s089** Now there are about ten false alarms instead of ninety nine, and a positive means about forty eight percent.
  - *Visual:* Stacks: orange 9 vs blue 9.9 (≈10); '9 / 18.9 ≈ 48%' in violet.
- **s090** And the hit rate dial? Push it from nine in ten all the way to perfect, and the answer barely moves. From about eight percent to about nine. ⏸1.0s
  - *Visual:* Hit-rate dial turns to 10 of 10; orange stack 9 → 10; '10 / 109 ≈ 9%'.
- **s091** So, a rule of thumb. When the thing you're looking for is rare, the false alarm rate matters far more than the hit rate. ⏸1.5s
  - *Visual:* Rule-of-thumb card: 'rare thing → false alarm rate matters most' (labelled 'rule of thumb').

## Real World  ·  422 words, ~169 s

- **s092** Now let's see where this shows up in the real world. The labels change, but the counting is the same.
  - *Visual:* Four domain tiles: ML, DS, FINANCE, CS.
- **s093** Machine learning. A classifier is just a test run by a computer.
  - *Visual:* ML tile expands: input dots → model box → 'positive' / 'negative' outputs.
- **s094** Engineers have names for our numbers. Catching nine out of ten sick people is called recall.
  - *Visual:* 'recall = 9 / 10 = 90%' (aqua), with the orange column of 10 and 9 rings.
- **s095** And nine out of one hundred and eight, the share of alarms that are real, is called precision.
  - *Visual:* 'precision = 9 / 108 ≈ 8%' (violet), with the two stacks.
- **s096** When the thing you're looking for is rare, a model can have great recall and still terrible precision. That's the base rate at work. ⏸1.0s
  - *Visual:* Two gauges side by side: recall 90% (full), precision 8% (nearly empty).
- **s096a** That's why teams measure precision on data with the real base rate. On a balanced test set, half positive and half negative, our same test would show ninety percent precision. In the real world, about eight percent. ⏸1.0s
  - *Visual:* Two panels: 'balanced test set (50% positive) → precision 90%' vs 'real world (1% positive) → precision 8%'.
- **s097** And here's a trap. A model that simply says healthy to everyone is ninety nine percent accurate, and completely useless. ⏸1.0s
  - *Visual:* Grid of 1,000 all marked 'healthy': '990 / 1000 correct = 99% accuracy' with a red '0 of 10 caught'.
- **s098** Data science. Bayes is the engine of Bayesian statistics.
  - *Visual:* DS tile expands.
- **s099** You start with a prior belief, say, about how often visitors to a website buy something, and update it as each day's data comes in.
  - *Visual:* Axes x 'purchase rate (%)' 0–10, y 'belief (shape only)': a wide warn curve narrows into a violet curve as day-1, day-2, day-3 data chips arrive. Labelled 'shape only'.
- **s100** Each day's posterior becomes the next day's prior. Exactly like our second test. ⏸1.0s
  - *Visual:* Loop arrow posterior → prior, as in the Test Again chapter.
- **s100a** And before trusting any automated flag on a dashboard, a good analyst asks: of all the past flags, how many were real? That's precision again, measured on real data.
  - *Visual:* Dashboard card with a column of past flags: few aqua-ringed orange (real), many blue (false); 'real ÷ all flags'.
- **s101** Finance. Banks run fraud detectors on card payments.
  - *Visual:* Finance tile expands: card + payment stream.
- **s102** Fraud is rare, far rarer than one in a hundred payments. So even a detector as good as our test would flag mostly honest payments.
  - *Visual:* Same 1,000-grid relabelled 'payments', with even fewer orange squares; aqua flags land mostly on blue ('honest').
- **s103** That's one reason many banks send a quick, was this you, message instead of simply blocking the card. In Bayes terms, your reply is a second, independent test. ⏸1.0s
  - *Visual:* Phone with 'Was this you?' → reply 'Yes' → meter drops / 'No' → meter jumps.
- **s103a** The same idea applies to market signals. A warning sign that fired before most crashes may also fire in many calm years. Always ask how often it fires when nothing happens. ⏸1.0s
  - *Visual:* Timeline of years (axis 'year 1–20', generic, labelled 'illustration'): signal flags on several years, only two of them crash years.
- **s104** Computer science. Some of the first really effective spam filters were built on Bayes' theorem.
  - *Visual:* CS tile expands: inbox with a spam folder.
- **s105** The prior is how much of all email is spam. The evidence is the words inside.
  - *Visual:* Email card; words 'FREE', 'winner', 'meeting' highlighted; prior chip 'share of email that is spam'.
- **s106** Each word nudges the odds up or down, just like each positive test. The filter multiplies them together.
  - *Visual:* Odds ladder like before: '× (FREE)' up, '× (meeting)' down. Each arrow labelled 'shape only' factors.
- **s107** To keep it simple, it treats every word as independent of the others. That shortcut is why it's called naive Bayes. It isn't true, but it works surprisingly well. ⏸1.0s
  - *Visual:* 'naive Bayes = assume words are independent' card; a check mark 'works surprisingly well'.
- **s107a** Computer security has the same problem. An intrusion alarm that fires on just one in a thousand normal logins can still bury the few real attacks under false alarms. ⏸1.0s
  - *Visual:* Login stream: thousands of blue login dots, rare orange attack dots; aqua alarms mostly on blue.

## Common Mistakes  ·  230 words, ~92 s

- **s108** Before we wrap up, here are the three most common mistakes people make with Bayes.
  - *Visual:* Three red cards face down.
- **s109** Mistake one: flipping the question.
  - *Visual:* Card 1 flips: 'Flipping the question'.
- **s110** The chance of a positive test, if you're sick, is ninety percent. The chance you're sick, if you test positive, is about eight percent.
  - *Visual:* P(B | A) = 90% (aqua) above P(A | B) ≈ 8% (violet); the A and B letters swap places.
- **s111** Same words, swapped around. Completely different numbers. ⏸1.0s
  - *Visual:* Red swap arrows between the two; '90% ≠ 8%'.
- **s112** In courtrooms, this flip has a name: the prosecutor's fallacy. The chance of the evidence if someone is innocent is not the chance they're innocent, given the evidence. ⏸1.0s
  - *Visual:* Scales of justice icon; two cards 'P(evidence | innocent)' vs 'P(innocent | evidence)' with '≠'.
- **s113** Mistake two: ignoring the base rate.
  - *Visual:* Card 2 flips: 'Ignoring the base rate'.
- **s114** Take the same test, but give it only to patients who already have symptoms. Say one in five of them has the condition.
  - *Visual:* Same 40 x 25 grid; now 200 squares (five columns) turn orange; warn tag 'base rate 1 in 5'.
- **s115** Out of a thousand, that's one hundred and eighty true positives, against eighty false alarms. Now a positive means about seventy percent.
  - *Visual:* Stacks: orange 180 vs blue 80 (axis 0–200, ticks every 50); '180 / 260 ≈ 69%' in violet.
- **s116** Same test. Same result. The base rate changed everything. ⏸2.0s
  - *Visual:* Side by side: 'base rate 1 in 100 → 8%' vs 'base rate 1 in 5 → 69%'.
- **s117** Mistake three: counting the same clue twice.
  - *Visual:* Card 3 flips: 'Counting a clue twice'.
- **s118** If two tests share the same weakness, or two news stories copy the same source, they are really one piece of evidence, not two.
  - *Visual:* Two news cards with arrows back to one source card.
- **s119** Multiply them as if they were independent, and you'll end up far too confident. ⏸1.0s
  - *Visual:* Meter pointer overshoots to 88% (red 'overconfident'), then settles back toward 8% with '1 clue'.
- **s120** And a bonus mistake: deciding the test is useless because the answer was only eight percent.
  - *Visual:* Red card 'Bonus: “the test is useless”'.
- **s121** It isn't. A positive raised the chance more than eightfold, and a negative almost rules the condition out. A good test is a strong clue. It's just not a verdict. ⏸1.0s
  - *Visual:* Meter: 1% → 8.3% (positive) and 1% → 0.1% (negative), both arrows big.

## Recipe  ·  128 words, ~51 s

- **s122** Let's turn all of that into a recipe you can use for any yes or no question.
  - *Visual:* Recipe card frame unrolls: 'Bayes in five steps'.
- **s123** Step one: start with the base rate. How common is the thing, before any evidence?
  - *Visual:* Item 1 (warn): 'Start with the base rate' + 'how common is it before any evidence?'.
- **s124** Step two: picture a crowd. One thousand people usually avoids fractions.
  - *Visual:* Item 2: 'Picture a crowd' + 'e.g. 1,000 people'.
- **s125** Step three: split the crowd with the test. Count the true positives, and the false alarms.
  - *Visual:* Item 3 (aqua): 'Split by the test' + 'true positives and false alarms'.
- **s126** Step four: keep only the people who match the evidence, and divide. Real cases, over all positives.
  - *Visual:* Item 4 (violet): 'Keep the matches and divide' + 'real ÷ all positives'.
- **s127** Step five: update. When new, independent evidence arrives, your answer becomes the new base rate. ⏸1.5s
  - *Visual:* Item 5: 'Update' + 'posterior becomes the next prior'.
- **s128** For our test: one in a hundred to start. Nine real positives, ninety nine false alarms. About eight percent. ⏸1.0s
  - *Visual:* Summary strip under the card: '1 in 100 → 9 real vs 99 false → 9/108 ≈ 8%'.
- **s129** A test result is a clue, not a verdict. Bayes tells you how much the clue is worth. ⏸2.0s
  - *Visual:* Closing line types on in violet, centred.

## Subscribe  ·  40 words, ~16 s

- **s130** Look around your world, and notice how many alarms are false alarms, and how rare the real thing usually is. ⏸0.6s
  - *Visual:* Four everyday cards: smoke alarm, car alarm, spam folder, 'was this you?' text — each stamped 'real or false alarm?'.
- **s131** If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together. ⏸0.8s
  - *Visual:* Logo + red SUBSCRIBE button; a cursor clicks it; it turns grey 'SUBSCRIBED ✓'; 'so we can keep building together' appears.

## Next Time  ·  62 words, ~25 s

- **s132** But here's a puzzle for next time.
  - *Visual:* Small logo stays top-centre; a puzzle-piece icon draws on.
- **s133** Scientists often report a number called a p-value, and it's very often described as the chance that a result is a fluke.
  - *Visual:* Card 'p = 0.03' with a speech bubble 'a 3% chance it's a fluke?' and a red question mark.
- **s134** That description flips the question, just like mistake one.
  - *Visual:* The two flipped cards from mistake one reappear: 'P(data | no effect)' vs 'P(no effect | data)'.
- **s135** Next time, we'll see what a p-value really measures, and why Bayes is the missing piece.
  - *Visual:* Chip 'next: p-values' appears under the small logo.
- **s136** I will see you in the next video. ⏸2.0s
  - *Visual:* Logo + 'next: p-values' chip hold.
