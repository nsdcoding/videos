# Lessons from earlier videos (read before building)

## Script
- Real voice speed is ~165 wpm: 2,450 words + 84 s of pauses came out at 15:12. Plan `minutes × 150` words.
- Ambiguous spoken words get mis-heard: "ninety sick" → "ninety-six", "the sick side" → "six side",
  a sentence-final number can be swallowed ("…, eight." → say "about eight percent."). Reword, re-voice.
- "Bayes" at the end of a sentence was heard as "bass"; respelling it "Bays" for the voice fixed it.
- Keep the welcome to 15–20 s: short preview sentences and 0.6–0.7 s pauses.
- Teasers become promises: record `teaser_next` so the next video pays it off.

## Audio
- Linear loudnorm can't reach −14 LUFS when peaks are high; an oversampled limiter at 0.35 (≈1% of samples)
  before loudnorm fixes it. AAC encoding adds ~0.3 dB of peak: master to −2.0 dBTP.
- To change only the audio of a finished video, remux: `ffmpeg -i video.mp4 -i voiceover.wav -map 0:v -map 1:a
  -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest out.mp4`.

## Manim layout
- Frame is 14.22 × 8 units; subtitles cover y < −2.70; chapter label covers x < −3.26 and y > 2.98.
- Keep a fixed right-panel column (e.g. x ≥ 0.9–1.7) next to a left graph; left-align panel text to it.
- Axis titles above the y-axis collide with headers: use `y_vertical=True` or move the chart down.
- Labels next to curves: put them in empty regions under the curve with a thin leader line, or use a legend.
- When zooming into a grid, fade the axis labels (they become huge) and restore them after.
- Moving objects in flight across labels trigger the checker: `qa_mute` them for the flight.
- A Transform target placed while an updater runs lands in the wrong spot: clear updaters, transform, re-add.
- Rotating loop arrows sweep through labels: use ShowPassingFlash along the arrow instead.
- Recipe cards with many rows: a two-column layout (bold heading | one-line explanation) keeps text large.
- Build `title_card()` identically at the end of the hook and the start of the welcome scene (seamless cut).

## Thumbnails
- The owner wants: keyword headline + "EXPLAINED VISUALLY", the formula, a real diagram from the running
  example, where you'll use it (ML, DS, Finance, CS) with icons and one-line takeaways, the length badge.
- Never generate images without the owner's approval at checkpoint 1.

## Repo / GitHub
- The default branch is `claude/stoic-fermi-aw89bv`; links to files on the work branch must include the branch
  (`https://github.com/nsdcoding/videos/blob/<branch>/<path>`), or the owner sees "not found".
- Files under 100 MB can be committed (a 15-min 1080p MP4 is ~60 MB).
