---
name: math-lab-video
description: Make a complete Math Lab TV video end to end from a topic name and a duration. Writes the script, voices it with Google Cloud TTS, builds a Manim video, and produces the YouTube package (title, description, chapters, tags, thumbnails, pinned comment). Keeps the channel tracker in channel/ up to date, so each video calls back to earlier ones, pays off promised teasers and teases a connected next video. Use when the owner asks for a Math Lab TV video, says "make the video for <topic>", "next video", or types /math-lab-video <topic> [duration].
argument-hint: "<topic name> [duration, e.g. 15-20 or 12]"
---

# Math Lab TV video, end to end

Math Lab TV: math explainers for people who are NOT good at math. Channel line: "where math is something you
can see". You run the whole job: **script → voice-over → Manim video → YouTube package**, stopping for the
owner's approval at the two ⏸ checkpoints. Arguments: `$ARGUMENTS` = topic words + optional duration
(default 15–20 min).

## Step 0: set up and read the brief

1. **Tools** (fresh container): see `reference/setup.md` (manim, LaTeX, google-auth, the `srt` build fix,
   Inter fonts, Playwright). Credentials: `GCP_SA_KEY_B64` (base64 service-account JSON).
2. **Resolve the topic and create the folder:**
   `python3 .claude/skills/math-lab-video/scripts/new_video.py <topic words> <duration> --dry-run`
   - Exit code 2 = ambiguous: ask the owner which candidate they mean (AskUserQuestion), then pass `--slug`.
   - Not in the catalog at all: confirm a title and series with the owner, then use `--new "Title" <series-id>`.
   - Already produced: tell the owner and ask whether to remake it before continuing.
   - Then run it without `--dry-run`. It copies `template/` into a new folder named after the topic, writes
     `<folder>/BRIEF.md` and marks the topic `in-production` in `channel/catalog.json`.
3. **Read `BRIEF.md`**: the owner's planned beats (`covers`) and picture (`visual`), plus the connections:
   - **Pay off this promise**: an earlier video's teaser promised this one. Open the lesson by paying it off
     ("Last time, we saw that a p-value flips the question. Today, let's see what it really measures.").
   - **Callbacks**: finished videos to reference naturally, 1–3 times, in narration and on screen
     (e.g. a small chip "from: Mean vs Median"). Reuse their running example briefly when it helps.
   - **Overlaps**: the same idea from another angle. Use a DIFFERENT running example and refer back to it.
   - **Prerequisites not made yet**: give a 1–2 sentence intuition instead of assuming them.
   - **Default teaser**: the NEXT TIME topic; confirm it with the owner at checkpoint 1.
   - **Leads to**: plant a seed for those later videos where natural.
4. Look at the newest finished video folder (see `channel/catalog.json` → production.folder; currently
   `bayes-theorem/`) for working examples of every file in the template.

## Step 1: write the script

Write the full narration in `script_src.py`, which emits `script.json`: a list of short segments (one sentence
or idea each). Every segment has: id, chapter, narration text, the on-screen visual for it, and `pause_after`
(seconds of silence after it; 0.35 s by default, 1–2 s after every key "aha" moment). Give segments stable ids
(s001, s002, …). When a line is added after voicing, give it a new id (e.g. s017a) instead of renumbering, so
only new or changed lines need to be re-voiced.

**Length:** aim for `minutes × 150` words for the target duration (the voice runs ~165 wpm; pauses add the
rest). `python3 script_src.py` prints the estimate. Measure the real length after voicing and add or trim
lines (new ids) if it falls outside the target.

**Structure (keep this order; one Manim scene per chapter, each chapter ≥ 10 s):**
1. **HOOK** (~60–70 s): a relatable story with real numbers that sets up the topic. End by naming the topic,
   shown as a title card (`title_card()` in common.py).
2. **CHANNEL WELCOME** (~15–20 s), its own chapter, "Welcome":
   - "Welcome to Math Lab TV. Where math is something you can see." (word for word), over the logo card:
     a violet rounded square with a green bell curve, "MATH LAB TV", and the tagline "where math is something
     you can see".
   - "Today you will learn…" with a numbered preview 1, 2, 3. Each item gets one spoken sentence, a big
     coloured number, a mini visual and a caption, and the small logo stays top-right.
3. **Why it matters.** If a promise is being paid off, do it in the hook or here.
4. **Build the idea step by step**, then ONE running worked example with real numbers.
5. **Big picture / real-world uses**: one short part each for Machine Learning, Data Science, Finance and
   Computer Science where relevant, tied back to the running example. Use the catalog's callbacks here too.
6. **Common mistakes**: the 2–3 most common beginner mistakes, explicitly (a bonus one is fine).
7. **Recipe recap**: a numbered card, each step as a bold heading plus a one-line explanation. End with a
   memorable closing line.
8. **CHANNEL OUTRO** (~12 s), its own chapter, "Subscribe":
   - "Look around your world, and notice …" (a reflection tied to the topic), with everyday examples on screen.
   - "If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building
     together." (word for word). On screen: the logo, a red SUBSCRIBE button, a cursor that clicks it, the
     button turning grey "SUBSCRIBED ✓", and "so we can keep building together".
9. **NEXT TIME**: a teaser for the next video (from the brief, confirmed by the owner), connected to this
   topic. The small logo stays top-centre, with a "next: <topic>" chip, and the video ends on
   "I will see you in the next video."

**Script checklist (all must pass):**
1. Accuracy: check every factual and mathematical claim, and verify every number in the running example
   with code (`verify_numbers.py`, exact fractions). No "close but not exactly right" statements.
2. State limits and assumptions, and call rules of thumb rules of thumb.
3. Show, don't assert: every "why" needs a visual demonstration. Be honest about alternatives.
4. Define every symbol in plain words when it first appears (Σ = "add them all up").
5. ONE running example throughout; don't switch datasets. Schematic illustrations are labelled
   "illustration" or "shape only". If the topic overlaps a finished video, use a different running example.
6. Concrete before abstract: real numbers early, then generalise.
7. Address the 2–3 most common beginner mistakes explicitly.
8. End with the numbered recipe-recap card.
9. Spoken style: short sentences, written for the ear. Write every number as words (no digits, %, $ or
   symbols in the narration); avoid words that sound like other words in context ("sick side" → "six side").
10. Real-world claims are named generically on screen (e.g. "Census income report"): no logos or branding of
    real organisations. Studies can be cited by author in the pinned comment.
11. Continuity: the promise is paid off, 1–3 callbacks are in, overlaps are not repeated, the teaser is set.

**Visual plan for generated images** (see "Images" below): list every planned sticker in the visual column
with the reason Manim is not enough. Usually zero to four per video.

⏸ **CHECKPOINT 1**: send the owner `script.md` (narration plus the visual plan, grouped by chapter, with word
count and estimated length). Also give: the connections used (promise, callbacks, overlaps), the proposed
next-video teaser, any planned generated images, and real-world claims that need confirming. Commit, push,
and wait for approval.

## Step 2: generate the voice-over

Use Google Cloud Text-to-Speech with voice `en-US-Chirp3-HD-Zubenelgenubi` (languageCode en-US). Test with
one sentence first (`python3 tts.py test "…" out.wav`).
- `python3 tts.py all`: ONE clip PER SEGMENT, cached by a hash of its spoken text, so reruns only re-voice
  changed lines. Respell words for the voice only with `SPOKEN_FIXES` / `SPOKEN_FIXES_BY_ID` in tts.py.
- `python3 assemble_audio.py`: trims leading and trailing silence, caps pauses inside a clip at ~0.55 s,
  inserts the real `pause_after` silences, normalises each clip to −20 LUFS, then the mix to −14 LUFS with a
  gentle oversampled limiter and **−2.0 dBTP** (leaves headroom for AAC), 48 kHz. Writes `timings.json`
  (id, chapter, start, end, text): it drives the animation, the subtitles and the chapters.
- **Listen-check** (`python3 listen_check.py`): transcribes every clip blind (Gemini on Vertex; Cloud
  Speech-to-Text if enabled) and diffs it against the script. Fix real mis-hearings by rewording the line
  (new audio) or respelling for the voice. Ignore spelling-only differences ("mathlab", "anytime"). If no
  speech-to-text works, say so plainly, list the risky words for the owner to check by ear, and say what
  to enable (the Cloud Speech-to-Text API).
- Report the measured length; adjust the script if it is outside the target duration.

## Step 3: build the video

**Visual style**
- 1920×1080, 30 fps, background #1a1a19. Font: Inter / Inter Display. LaTeX only for real fractions, roots
  and formulas (plain arithmetic like "40 × 25 = 1,000" in Inter).
- Colour-blind-safe palette: blue #3987e5 (negative/low), orange #d95926 (positive/high), aqua #199e70
  (areas), violet #9085e9 (the answer), warn #fab219 (highlight / the key quantity), red #d03b3b
  (mistakes/traps), ink #f0efec / #c3c2b7 / muted #898781. Give each key concept ONE colour and keep it.
- EVERY explanation sits on real x/y axes with numbered ticks and axis titles. Squares and areas use equal
  x/y scale so cells can be counted.
- A new visual beat every 2–3 s: comparisons, metaphors (balance beam, water levelling, number-line walks),
  counters, stacking dots, on-screen symbol definitions, and the final recipe card. Keep variety high.
- Camera: MovingCameraScene with zooms and pans, always kept inside the subtitle-safe area. Fade out
  anything a zoom would cut at the frame edge (axis labels included).
- Overlay, burned in with libass/ASS by build.py: subtitle strip at the bottom (Inter 40 px on a dark box,
  ≤ 64 characters per line), the chapter label top-left, and a thin progress bar with chapter ticks.
- Safe zones: scene content above the bottom 175 px and out of the top-left 520×110 px.

**Images (Gemini 2.5 Flash Image, "Nano Banana")**: Manim first. Generate an image ONLY when the beat needs
something code cannot draw well, and only where the visual plan (approved at checkpoint 1) lists it:
- Use for: relatable people with emotion (a worried patient, a happy shopper), real-world objects or places
  that line art makes unrecognisable (a hospital, a stock-exchange floor, a bank card), consistent recurring
  characters, and a human element on thumbnails.
- Never use for: anything with numbers, axes, formulas, charts, grids, text or data (always Manim/SVG), logos,
  real brands, real people, or decoration a simple Manim shape would do.
- Make them with `python3 .claude/skills/math-lab-video/scripts/sticker.py "<subject>" <folder>/assets/<name>.png`
  (house style and palette, no-text rule, background cut out, prompt logged to `assets/IMAGES.md`; pass
  `--ref` to keep a character consistent). Open every result and regenerate if letters, logos or odd details
  appear. Place them with `sticker("assets/<name>.png", height)` in Manim (the overlap checker treats them as
  solid), and label scenes "illustration" where a viewer could mistake them for real data.

**Build rules**
- One Manim scene per chapter in `scenes/`, a `Base` subclass with `CHAPTER = "<chapter name>"` (build.py
  finds them). Drive everything from timings.json: `self.at(sid)`, `word_time(sid, word_index(sid, "word"))`.
  `title_card()`, `logo()`, `pill()`, `card()`, `defcard()`, `xy_axes()`, `meter()`, `stack()`, `bar()`,
  `gauge()`, `beam_scale()`, `loop_arrows()`, `marker()` are in common.py.
- Template scenes: `s02_welcome.py`, `s90_subscribe.py`, `s91_next.py` (fill the FILL parts).
- `./render_all.sh [stems]` renders in parallel with `--disable_caching`; build.py normalises each scene to an
  exact frame count, joins them and adds the voice-over. Each scene starts from the previous scene's last
  frame, or the previous scene fades out cleanly.
- **Overlap checker** (runs after every animation; `build/qa/<Scene>.json`; render until every scene is `[]`):
  text vs text (≥ ~8 px gap), text vs filled shapes and images, text crossed or touched by strokes (lines,
  arrows, curves, outlines; sampled along the path, within ~3 px), marker heads on data dots, text clipped at
  the frame edge or within 40 px of it, text under the subtitles, text in the chapter-label corner, and text
  within 10 px of the border of the box/chip/card it sits in.
- The checker can't see everything: review contact sheets of every scene (`bash contact.sh <scene.mp4>
  build/contact/<name>`: one frame every 2.5 s, numbered, multiple pages) and fix crowding: boxes too small
  for their text, labels touching chips or arrows, piled-up highlights, leftover objects, long static stretches.
- Gotchas: size every box from its text width; highlight tiles by tinting border and number, never by filling
  over the number; remove whole object families when clearing a beat (`self.drop`); don't let play-level rate
  functions override per-animation ones; glows must follow and disappear with their text (glow a copy with
  fill opacity 0); never combine FadeIn and Rotate on one object; Indicate a group of separate dots one by one
  (scaling a group pushes them apart); `qa_mute` objects hidden under an opaque overlay; mark deliberate
  strike-throughs and highlight boxes `qa_ignore` with a comment. More in `reference/lessons.md`.

⏸ **CHECKPOINT 2**: render a ~2–3 minute sample with audio (`python3 build.py sample <cut-sid>`: hook,
welcome, why it matters and the start of the lesson). Send it, commit, push, and wait for approval before the
full render.

## Step 4: YouTube package (after the final video, `python3 build.py full`)

1. Final MP4 + `.srt` captions (built from timings.json). Check: 1920×1080, 30 fps, AAC 48 kHz, about
   −14 LUFS, true peak ≤ −1.5 dBTP.
2. Title: the main keyword first, under 100 characters (counted), naming the domains (Machine Learning,
   Data Science, Finance, CS) where relevant. Give 2–3 options with character counts, and recommend one.
3. Description (`package.py`):
   - The first 2 lines contain the main keyword and the domains spelled out: Machine Learning, Data Science
     (DS), Finance, Computer Science (CS).
   - Then the hook story, and chapters starting at 0:00 (each at least 10 s, from timings.json, including
     "Welcome" and "Subscribe").
   - A "Where you'll use it" section: one line per domain, each with a timestamp.
   - Key formulas with every symbol explained, the worked-example answers, the recipe, and the teaser.
   - **📺 Related videos** from the tracker: `channel.desc_block()` (live links to connected videos; the next one).
   - 3 hashtags, led by the domain ones (e.g. #machinelearning #datascience #statistics).
4. Tags under 500 characters (counted), including machine learning, data science, finance, computer science,
   ML, DS, CS and "statistics for …". Paste them in chat as one comma-separated line. Add category and settings.
5. Two 1280×720 thumbnails (`thumbs.py`) for "Test & compare":
   - the topic KEYWORD as the big headline plus "EXPLAINED VISUALLY" (no vague hooks);
   - the key formula, colour-coded like the video, with plain-word labels under its parts;
   - A: "where you'll use it" tiles (ML, DS, Finance, CS, each with an icon and a one-line takeaway) and the
     hook in one line; B: a real diagram of the running example and its punchline number;
   - a badge "Explained in X minutes" (real length); keep the bottom-right corner clear; check readability at
     320×180. A generated sticker may add a human element only if the owner approved it.
6. A pinned comment: a short summary, plus clarifications worth adding, with timestamps.

## Step 5: update the channel tracker

- Fill the topic's `production` record in `channel/catalog.json`: folder, branch, length, video, package,
  youtube_title, running_example, hook, callbacks (slugs referenced), teaser_next (slug teased).
- `python3 channel/channel.py set <slug> produced` and `render`.
- When the owner later sends the YouTube URL: `python3 channel/channel.py link <slug> <url>`, re-run
  `package.py` of every video the command lists (their descriptions gain the link), commit and push.

## Delivery

Commit and push the code, script, timings, final MP4, captions, package and tracker to the working branch at
each milestone (checkpoint 1, checkpoint 2, final). Send the owner the MP4, the .srt, both thumbnails and the
description. At the end, list the file paths, the final length, the connections used, and anything to check
by ear. The repo's default branch is `claude/stoic-fermi-aw89bv`; tell the owner which branch holds the work.
