# Math Lab TV: how videos are made in this repo

Math Lab TV is a YouTube channel of math explainers for people who are NOT good at math.
Claude makes every video end to end: script → voice-over → Manim video → YouTube package.

**This folder is the whole Math Lab TV channel.** The repo also holds other channels' work; keep them apart:
Math Lab TV files go only in `math-lab-tv/` (plus the skill in `.claude/skills/math-lab-video/`), and nothing
from other channels (their folders, branches, `gen.py`, `skills/motion-video-style`) is used here.

**To make a video, type `/math-lab-video`.** The skill recommends the next topic from what has been made, you
pick it and give the duration, and it does the rest (full prompt in its SKILL.md).

## Start here: the channel tracker (`math-lab-tv/channel/`)

| file | what it is |
|---|---|
| `math-lab-tv/channel/catalog.json` | **source of truth**: all 96 planned videos in 9 series, their status, what each must cover, the planned visual, and how the videos connect (`builds_on`, `related`, `overlaps`), plus production details of every finished video |
| `math-lab-tv/channel/README.md` | the tracker as a page (generated: `python3 math-lab-tv/channel/channel.py render`; never edit by hand) |
| `math-lab-tv/channel/youtube-links.txt` | the owner pastes `slug = URL` here after uploading; a line there = published |
| `.claude/skills/math-lab-video/SKILL.md` | the owner's standing production prompt (structure, checklists, checkpoints, style). Follow it for every video |
| `math-lab-tv/channel/lesson-lab/<slug>/` | older draft scripts from the Lesson Lab app (reference only) |
| `math-lab-tv/channel/channel.py` | `status`, `show`, `refs`, `next`, `set`, `link`, `desc-block`, `render` |

## Workflow for every new video

1. **Recommend the topic**: `python3 math-lab-tv/channel/channel.py recommend 3`, the owner picks; then
   ask for the duration.
2. **Read its connections**: `python3 math-lab-tv/channel/channel.py refs <slug>` and `show <slug>`.
   - `callbacks`: finished videos to reference on screen and in the narration
     (e.g. "In our mean versus median video, we saw…"). Use 1–3 natural callbacks, never a list.
   - `promised_by`: a video whose ending teased this one. Open by paying off that promise.
   - `overlaps`: a related video made from a different angle. Use a **different running example**
     (check that video's `production.running_example`) and refer to it rather than repeating it.
   - `prerequisites_not_made`: give a 1–2 sentence intuition instead of assuming it.
   - `tease_next`: default topic for the NEXT TIME teaser. Confirm it at checkpoint 1.
   - The topic's own `covers` and `visual` in the catalog are the beats and picture the owner planned.
3. Run `.claude/skills/math-lab-video/scripts/new_video.py --slug <slug> --minutes <lo-hi>` (creates
   `math-lab-tv/<slug>/` from the template, writes BRIEF.md, sets the topic in-production), then follow the
   skill's SKILL.md exactly (both ⏸ checkpoints). `math-lab-tv/bayes-theorem/` is the newest complete example.
4. **Description**: `package.py` must include `channel.desc_block(...)` (see `math-lab-tv/bayes-theorem/package.py`):
   links to connected videos that are live, and the next video.
5. **When the final video is done**, fill the topic's `production` record in `catalog.json`
   (folder, branch, length, video, package, youtube_title, running_example, hook, callbacks,
   teaser_next), run `set <slug> produced`, then `render`, and commit.
6. **When the owner sends a YouTube link**: `python3 math-lab-tv/channel/channel.py link <slug> <url>`, then
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
- Commit and push milestones; Math Lab TV's home branch is `defaults.home_branch` in the catalog. Never
  commit Math Lab TV work to another channel's branch.
