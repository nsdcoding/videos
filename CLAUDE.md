# Math Lab TV: how videos are made in this repo

Math Lab TV is a YouTube channel of math explainers for people who are NOT good at math.
Claude makes every video end to end: script → voice-over → Manim video → YouTube package.

**To make a video, use the `math-lab-video` skill** (`.claude/skills/math-lab-video/`), e.g.
`/math-lab-video hypothesis testing 15-20`. It holds the full production prompt (SKILL.md), the pipeline
template, `scripts/new_video.py` (topic + duration → folder, brief, tracker status) and `scripts/sticker.py`
(generated images). The rest of this file is the summary.

## Start here: the channel tracker (`channel/`)

| file | what it is |
|---|---|
| `channel/catalog.json` | **source of truth**: all 96 planned videos in 9 series, their status, what each must cover, the planned visual, and how the videos connect (`builds_on`, `related`, `overlaps`), plus production details of every finished video |
| `channel/README.md` | the tracker as a page (generated: `python3 channel/channel.py render`; never edit by hand) |
| `channel/youtube-links.txt` | the owner pastes `slug = URL` here after uploading; a line there = published |
| `.claude/skills/math-lab-video/SKILL.md` | the owner's standing production prompt (structure, checklists, checkpoints, style). Follow it for every video |
| `channel/lesson-lab/<slug>/` | older draft scripts from the Lesson Lab app (reference only) |
| `channel/channel.py` | `status`, `show`, `refs`, `next`, `set`, `link`, `desc-block`, `render` |

## Workflow for every new video

1. **Pick the topic.** If the owner names one, use its slug from the catalog; if they say "next" or
   "suggest one", run `python3 channel/channel.py next` and propose the top pick (a topic promised in a
   previous teaser comes first).
2. **Read its connections**: `python3 channel/channel.py refs <slug>` and `show <slug>`.
   - `callbacks`: finished videos to reference on screen and in the narration
     (e.g. "In our mean versus median video, we saw…"). Use 1–3 natural callbacks, never a list.
   - `promised_by`: a video whose ending teased this one. Open by paying off that promise.
   - `overlaps`: a related video made from a different angle. Use a **different running example**
     (check that video's `production.running_example`) and refer to it rather than repeating it.
   - `prerequisites_not_made`: give a 1–2 sentence intuition instead of assuming it.
   - `tease_next`: default topic for the NEXT TIME teaser. Confirm it at checkpoint 1.
   - The topic's own `covers` and `visual` in the catalog are the beats and picture the owner planned.
3. Run `.claude/skills/math-lab-video/scripts/new_video.py <topic> <duration>` (creates the folder from the
   template, writes BRIEF.md, sets the topic in-production), then follow the skill's SKILL.md exactly (both
   ⏸ checkpoints). `bayes-theorem/` is the most recent complete example of every file.
4. **Description**: `package.py` must include `channel.desc_block(...)` (see `bayes-theorem/package.py`):
   links to connected videos that are live, and the next video.
5. **When the final video is done**, fill the topic's `production` record in `catalog.json`
   (folder, branch, length, video, package, youtube_title, running_example, hook, callbacks,
   teaser_next), run `set <slug> produced`, then `render`, and commit.
6. **When the owner sends a YouTube link**: `python3 channel/channel.py link <slug> <url>`, then
   re-run `package.py` for every video the command lists, so their descriptions gain the new link.
   Commit and push.

## Owner preferences (keep these)

- **Images: Manim/SVG first.** Gemini 2.5 Flash Image ("Nano Banana") is allowed only through the skill's
  `scripts/sticker.py`, only where Manim is not enough (relatable people, real-world objects, recurring
  characters), and only for images listed in the visual plan the owner approves at checkpoint 1. Never for
  numbers, charts, formulas or text, and never outside that workflow without asking.
- Voice: Google Cloud TTS `en-US-Chirp3-HD-Zubenelgenubi`. Credentials: `GCP_SA_KEY_B64`.
- Text must never touch frame edges or box borders; the overlap checker in `common.py` enforces it.
- Thumbnails: keyword headline (e.g. "BAYES' THEOREM / EXPLAINED VISUALLY"), the key formula, a real
  diagram from the running example, where viewers will use it (ML, DS, Finance, CS), and an
  "Explained in X minutes" badge; bottom-right corner clear; readable at 320×180.
- Commit and push milestones to the session's working branch; the default branch is
  `claude/stoic-fermi-aw89bv`, and finished work lives on per-video branches recorded in the catalog.
