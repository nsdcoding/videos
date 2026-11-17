I run the YouTube channel "Math Lab TV": math explainers for people who are NOT good at math.

TOPIC: <TOPIC>
TARGET LENGTH: 15–20 minutes (unless I say otherwise)
NEXT VIDEO (for the teaser): <NEXT TOPIC, or "suggest one">
DOMAINS to connect where relevant: Machine Learning (ML), Data Science (DS), Finance, Computer Science (CS)

Your job, end to end: write the script → generate the voice-over → build the Manim video → create the YouTube package.
Stop for my approval at the two checkpoints marked ⏸. Reuse the existing pipeline in this repo (see mean-vs-median/: script_src.py, tts.py, assemble_audio.py, common.py, scenes/, build.py, render_all.sh, package.py, thumbs.py) in a new folder named after the topic.

━━ STEP 1: WRITE THE SCRIPT ━━
Write the full narration in a script source that emits script.json: a list of short segments (one sentence or idea each). Every segment has:
  id, chapter, narration text, the on-screen visual for it, and pause_after (seconds of silence after it; 0.35 s by default, 1–2 s after every key "aha" moment).
Give segments stable ids (s001, s002, …). When a line is added later, give it a new id (e.g. s017a) instead of renumbering, so only new or changed lines need to be re-voiced.

Structure (keep this order):
1. HOOK (~60–70 s): a relatable story with real numbers that sets up the topic. End by naming the topic, shown as a title card.
2. CHANNEL WELCOME (~15–20 s), its own chapter, "Welcome":
   - "Welcome to Math Lab TV. Where math is something you can see." (word for word), over the logo card: a violet rounded square with a green bell curve, "MATH LAB TV", and the tagline "where math is something you can see".
   - "Today you will learn…" with a numbered preview 1, 2, 3. Each item gets one spoken sentence, a big coloured number, a mini visual and a caption, and the small logo stays top-right.
3. Why it matters.
4. Build the idea step by step, then ONE running worked example with real numbers.
5. Big picture / real-world uses: one short part each for ML, DS, Finance and CS where relevant, tied back to the running example.
6. Common mistakes: the 2–3 most common beginner mistakes, explicitly.
7. Recipe recap: a numbered card, each step as a bold heading plus a one-line explanation. End with a memorable closing line.
8. CHANNEL OUTRO (~12 s), its own chapter, "Subscribe":
   - "Look around your world, and notice …" (a reflection tied to the topic), with everyday examples on screen.
   - "If this lesson made things clear for you, please subscribe to Math Lab TV, so we can keep building together." (word for word). On screen: the logo, a red SUBSCRIBE button, a cursor that clicks it, the button turning grey "SUBSCRIBED ✓", and "so we can keep building together".
9. NEXT TIME: a teaser for the next video. The small logo stays top-centre, with a "next: <topic>" chip, and the video ends on "I will see you in the next video."

Script checklist (all must pass):
1. Accuracy: check every factual and mathematical claim, and verify every number in the running example with code. No "close but not exactly right" statements (e.g. standard deviation is the typical root-mean-square distance, not the plain average distance).
2. State limits and assumptions, and call rules of thumb rules of thumb (e.g. "this works for bell-shaped data").
3. Show, don't assert: every "why" needs a visual demonstration. Be honest about alternatives.
4. Define every symbol in plain words when it first appears (Σ = "add them all up").
5. ONE running example throughout; don't switch datasets. Any schematic illustration (e.g. a shape only) is labelled "illustration" or "shape only".
6. Concrete before abstract: real numbers early, then generalise.
7. Address the 2–3 most common beginner mistakes explicitly.
8. End with the numbered recipe-recap card.
9. Spoken style: short sentences, written for the ear. Write every number as words (no digits, %, $ or symbols in the narration).
10. Real-world claims are named generically on screen (e.g. "Census income report"): no logos or branding of real organisations.

⏸ CHECKPOINT 1: send me script.md (narration plus the visual plan, grouped by chapter, with word count and estimated length) and wait for my approval.

━━ STEP 2: GENERATE THE VOICE-OVER ━━
Use Google Cloud Text-to-Speech with voice "en-US-Chirp3-HD-Zubenelgenubi" (languageCode en-US). The credentials are in GCP_SA_KEY_B64 (base64 service-account JSON). Test with one sentence first.
- Synthesise ONE clip PER SEGMENT and cache it by a hash of its text, so reruns only re-voice changed lines.
- Don't rely on SSML for pauses. Trim leading and trailing silence, cap pauses inside a clip at ~0.55 s, then insert the real pause_after silences between clips.
- Normalise each clip to −20 LUFS, then the final mix to −14 LUFS (true peak −1.5 dBTP), 48 kHz.
- Save timings.json (id, chapter, start, end, text). It drives the animation, the subtitles and the chapters.
- Listen-check: transcribe every clip and diff it against the script. Report any word the voice says wrongly and fix its spelling for the voice only. If no reliable speech-to-text is available, say so plainly, list the risky words for me to check by ear, and tell me what to enable (e.g. the Cloud Speech-to-Text API).

━━ STEP 3: BUILD THE VIDEO ━━
Visual style:
- 1920×1080, 30 fps, background #1a1a19. Font: Inter / Inter Display. Use LaTeX only for real fractions, roots and formulas.
- Colour-blind-safe palette: blue #3987e5 (negative/low), orange #d95926 (positive/high), aqua #199e70 (areas), violet #9085e9 (the answer), warn #fab219 (highlight / the key quantity), red #d03b3b (mistakes/traps), ink #f0efec / #c3c2b7 / muted #898781. Give each key concept ONE colour and keep it for the whole video.
- EVERY explanation sits on real x/y axes with numbered ticks and axis titles. Squares and areas use equal x/y scale so cells can be counted.
- A new visual beat every 2–3 s: comparisons (A vs B), metaphors (balance beam, water levelling, number-line walks), counters, stacking dots, on-screen symbol definitions, and the final recipe card. Keep variety high.
- Camera: MovingCameraScene with zooms and pans to focus and compare, always kept inside the subtitle-safe area. Fade out anything a zoom would cut at the frame edge.
- Overlay, burned in after rendering with libass/ASS so the camera can move freely: a small subtitle strip at the bottom (Inter 40 px on a dark box, ≤ 64 characters per line, timed from timings.json), the chapter label top-left, and a thin progress bar along the top with chapter ticks.
- Safe zones: keep scene content above the bottom 175 px (subtitles) and out of the top-left 520×110 px (chapter label).
Build rules:
- One Manim scene per chapter, driven by timings.json (wait until each segment's start; sync key beats to estimated word times). Render scenes in parallel with --disable_caching, normalise each to an exact frame count, then join and add the voice-over.
- Each scene starts from the previous scene's last frame, or the previous scene fades out cleanly.
- Run an automatic overlap checker after every animation. It must cover:
  - text vs text, with a minimum gap of ~8 px
  - text vs filled shapes
  - text crossed by strokes (lines, arrows, curves, outlines), sampled along the path
  - marker heads (e.g. mean or median pointers) sitting on data dots
  - text clipped at the frame edge, text under the subtitles, and text in the chapter-label corner
  Fix until every scene is clean.
- The checker can't see everything, so also review contact sheets of every scene (one frame every 2.5 s, numbered, multiple pages) and fix the crowding they show:
  - boxes too small for their text, or header strips that break rounded corners
  - labels touching chips or arrows, and rings or highlights that pile together
  - leftover objects from earlier beats
- Implementation gotchas:
  - Size every box or badge from its text width.
  - Highlight tiles by tinting the border and number, never by filling over the number.
  - Remove whole object families (not just the group) when clearing a beat.
  - Don't let play-level rate functions override per-animation ones.
  - Glows must follow and disappear with their text.
  - Never combine FadeIn and Rotate on the same object.

⏸ CHECKPOINT 2: render a ~2-minute sample with audio, covering the hook, the channel welcome and the start of the lesson, and wait for my approval before rendering the full video.

━━ STEP 4: YOUTUBE PACKAGE (after the final video) ━━
1. Final MP4 + .srt captions (built from timings.json).
2. Title: the main keyword first, under 100 characters (counted), naming the domains (Machine Learning, Data Science, Finance, CS) where relevant. Give 2–3 options with character counts, and recommend one.
3. Description:
   - The first 2 lines contain the main keyword and the domains spelled out: Machine Learning, Data Science (DS), Finance, Computer Science (CS).
   - Then the hook story, and chapters starting at 0:00 (each at least 10 s, taken from timings.json, including "Welcome" and "Subscribe").
   - A "Where you'll use it" section: one line per domain, each with a timestamp.
   - Key formulas with every symbol explained, the worked-example answers, the recipe, and the next-video teaser.
   - 3 hashtags, led by the domain ones (e.g. #machinelearning #datascience #statistics).
4. Tags under 500 characters (counted), including the domain keywords (machine learning, data science, finance, computer science, ML, DS, CS, "statistics for …"). Also paste them in chat as one comma-separated line, ready to copy. Add the suggested category and settings.
5. Two 1280×720 thumbnails for YouTube "Test & compare":
   - the topic KEYWORD as the big headline (no vague hooks)
   - a real diagram of the concept from the running example
   - a clear comparison (e.g. low vs high)
   - a badge "Explained in X minutes", where X is the real length
   Keep the bottom-right corner clear, and check that the text is readable at phone size (320×180).
6. A pinned comment: a short summary, plus any clarification worth adding, with timestamps.

━━ DELIVERY ━━
Commit and push the code, script, timings, final MP4, captions and package to the working branch at each milestone. Send me the MP4, the .srt, both thumbnails and the description. At the end, list the file paths, the final length, and anything I should check by ear.
