# BUILD_SPEC.md

Standing instructions for the build agent. Written once for the channel. Every video reads this same file. Per-video data lives in that video's `build.json`; nothing title-specific belongs here.

Revision: v3 · 2026-10-26. v3 makes every video a hand-animated motion-design piece in the channel's vintage editorial style, built the way the Nice Guy and Mind Tricks videos were built: a rigged cartoon cast, background sets and cut-out props generated with Nano Banana and animated in code, with real photographs dropped in as evidence cards. Audio, credits, captions, subtitles and failure behaviour carry over from v2. `build.json` files written for v1 or v2 (`shots`) are superseded by v3 files (`cast`, `sets`, `props`, `photos`, `beats`).

---

## 1. Inputs

```
Day NN - Title/
 narration.md   segmented script, plain text
 build.json     cast, sets, props, photo library and beats (spec v3)
 audio/         generated: one wav per segment, plus silence and the master
 images/        downloaded photos; generated sheets, plates and keyed cut-outs
 out/           final mp4, subtitles.srt, credits.txt, description.txt, checklist.md
```

`BUILD_SPEC.md` sits at the History folder root. Ignore any file whose name starts with `SUPERSEDED - do not use`.

---

## 2. Audio

1. Parse `narration.md`. Each segment begins with `--- sNN | pause_after: ms` (default 400). Synthesise each segment separately as **plain text**, never SSML, with `build.json` → `audio.voice`, `audio.encoding`, `audio.sample_rate_hz`, `audio.speaking_rate` (Google Chirp 3 HD). Never normalise the speaking rate.
2. Measure each file with `ffprobe`; write `audio/timings.json` (segment, start, end). Word times inside a segment come from forced alignment where available, else from character position weighted for punctuation.
3. One silence file per distinct `pause_after`; concatenate into `audio/master.wav`; normalise to **-16 LUFS, -1.5 dBTP**.
4. No music by default. If one is specified, duck to -28 LUFS under speech and **mute it entirely across any segment whose `pause_after` is 2000 or more**.

---

## 3. The look

### 3.1 Style

The channel has one look: **flat vintage editorial illustration**. Clean ink outlines, flat fills with a little paper grain and light halftone, mid-century print feel. Palette:

| Name | Hex | Use |
|---|---|---|
| Ink | `#26392b` | outlines, dark panels, text |
| Mustard | `#d4a640` | main warm field, highlights |
| Cream | `#f3e7cf` | paper, light panels |
| Olive | `#6d6a3a` | secondary fills |
| Rust | `#b5522f` | the single accent: the thing to look at |

**Style lock**, appended verbatim to every Nano Banana prompt:

```
Flat vintage editorial illustration, clean confident ink outlines, flat colour fills with subtle paper grain and light halftone texture, mid-century print style, palette of deep ink green #26392b, mustard #d4a640, cream #f3e7cf, olive #6d6a3a and a rust #b5522f accent, clearly illustrated and not photorealistic, no text, no lettering, no numbers, no watermarks.
```

### 3.2 Assets: generate once, animate everywhere

Every video is assembled from three kinds of generated asset, all with the style lock:

- **Cast** (`cast`): each recurring character gets a **character sheet** first (front, three-quarter, side and back views on plain cream), checked by eye, then every pose is generated with `--ref` to the sheet so the character stays identical. Poses are full-body on **plain flat magenta `#FF00FF`**, keyed out and split into a rig: body, head, and separate arms so they can swing, point and gesture. Heads for close-ups are generated separately. Extras (crowds, officials, passers-by) are generated as a lineup sheet and keyed.
- **Sets** (`sets`): full-bleed background plates, edge to edge, no border, no people, open space in the lower centre for the cast. Sets are places in the video's one continuous world.
- **Props** (`props`): isolated objects on plain magenta, generated as sheets of several props with wide gaps, keyed and split.

Key with a soft matte and despill; check every cut-out on a contrasting background before use.

### 3.3 Real people

- A real person in the story appears as a **cartoon character with a deliberately vague face**: simple shapes, no attempt at likeness, minimal features, never a portrait. Their real face appears only in real photographs.
- Where `cast.<id>.face` is `hidden`, the face is never shown at all: back view, silhouette, hat brim or turned away, in every pose and close-up.
- Expressions on vague faces are carried by posture, eyebrows and simple mouth lines drawn by the animation layer.

### 3.4 Hard rules on generated images

- **Never photoreal**, and never imitating a documentary photograph of a real event, person or place.
- **Never a likeness** of a real person (3.3).
- **Never graphic**: no injuries, bodies, remains or casualties, illustrated or otherwise.
- **Never text** in a generated image. Every word, number and place name is set by the animation layer.
- Real documents and artefacts that are the evidence of the story (a letter, a tablet, a papyrus, a map) are always shown from `photos`, never generated.
- If a prompt asks for any of these, stop and report rather than generate.

YouTube requires disclosure for synthetic content: toggle "altered or synthetic content" on every video.

---

## 4. Motion

### 4.1 One continuous world

Every set has a fixed place in one connected world. The camera travels between them: push in, pull back, pan, tilt, rise, dive into a detail, follow a moving character or prop. No hard cuts, wipes or dissolves, except where a beat says `transition: cut`. Earlier sets stay in the world and can be glimpsed again. Ease every move; interpolate zoom on a log scale; pull back mid-move on long journeys so it reads as a swoop. Arrive at each new subject just before the line about it begins. Bookend the film: end where it began.

### 4.2 Pace

- Something new appears or moves every **2-3 seconds**: a character enters, gestures or reacts; a prop pops, flips or slides; a label, counter, arrow, timeline or map route builds; the camera moves.
- Vary scale constantly: wide set, medium on the cast, close on a head or prop, extreme detail, and back out.
- Keep a slow drift (2-5%) on anything held, so no frame is frozen, except during `energy: still` and structural silences.
- Use the motion vocabulary of the earlier videos: pop with overshoot, rise, draw-on ink paths, typewriter labels, tear-off calendars, counters, split screens, speech bubbles, tags pinned at an angle, characters walking on and off, props flying along arcs.

### 4.3 Energy

| `energy` | Behaviour |
|---|---|
| `high` | Full motion design. The default. |
| `calm` | Slower cadence, gentler moves, fewer graphics. For reflective lines. |
| `still` | No new motion at all: hold the frame without drift. For structural silences, the turn, and passages about the dead. |

**Structural silences are always still**: across any segment's `pause_after` of 2000 or more, nothing moves, nothing appears, and no audio plays, whatever the beat says.

### 4.4 Photo cards

A beat shows a real photograph with `photo: {ref, entry, hold}`:

- The photo is a card in the scene, on a thin matte sampled from its own dark tones, with a soft shadow. A cast member may stand beside it, point at it or hold it up.
- `entry`: `slide_up`, `slide_left`, `slide_right`, `drop`, `flip`, `pin` (lands with an overshoot and a pin) or `grow`. The card may move, tilt up to 4° and scale as a card.
- **The photograph itself is never cropped, tinted, filtered, retouched, warped, colourised or drawn on.** Graphics sit beside it, never over it. Its contents move at most 6% in scale over its time on screen.
- `hold`: `beat` (default) or a number of following segments to stay.
- `low_res: true` photos are shown no larger than native size.
- **`caption` is mandatory where present**: lower left of the card, sans-serif, about 26px at 1080p, off-white at 85% with a soft shadow, visible as long as the card is.

---

## 5. build.json (v3)

```json
{
  "spec_version": "v3",
  "day": 1, "title": "...", "runtime_target_sec": 1150,
  "audio": {"voice": "en-US-Chirp3-HD-Charon", "encoding": "LINEAR16", "sample_rate_hz": 24000, "speaking_rate": 0.92, "music": null},
  "notes": ["..."],
  "cast": {
    "yamaguchi": {"desc": "who they are and what they wear", "face": "hidden", "poses": ["stand", "walk", "look_up"]}
  },
  "sets": {"street": "prompt for a background plate"},
  "props": {"hanko": "prompt for an isolated object"},
  "photos": {
    "p01": {"title": "...", "file_url": "https://upload.wikimedia.org/...", "page_url": "https://commons.wikimedia.org/wiki/File:...",
            "author": "...", "licence": "CC BY 2.0", "caption": "optional", "low_res": false}
  },
  "beats": [
    {"segments": ["s01"], "energy": "high", "set": "street",
     "cast": [["yamaguchi", "walk", "enters left, stops, turns back"]],
     "props": ["hanko"],
     "photo": {"ref": "p01", "entry": "drop", "hold": "beat"},
     "graphics": ["short hints for labels, counters, maps"],
     "transition": "cut", "title_overlay": "...", "labels": ["..."], "note": "..."}
  ]
}
```

- `cast.<id>.face`: `vague` (default for real people) or `hidden`. `poses` lists every pose the beats use.
- Every segment in `narration.md` is covered by exactly one beat, in order.
- `set` names the place the beat happens; `null` means the plain cream or ink paper field. A beat with no `set` key stays where the previous beat was.
- `cast` entries are `[character, pose, action]`; the action is direction for the animator.
- `props` and `graphics` are what the beat adds; the agent may add more within the rules.
- `transition: cut` is a hard cut into the beat; absent means a camera move.
- `title_overlay`: the title, built in during the beat's trailing pause. Once per video.
- `labels`: place names for a map set, set as type by the animation layer.
- `note`: script-writer instructions for the beat. Follow them; if one conflicts with this spec, stop and report.

---

## 6. Images: sourcing and the User-Agent

Archival `file_url`s are direct `upload.wikimedia.org` file URLs. Download them with a real contact User-Agent: `HistoryChannelBuild/1.0 (<channel or repo URL>; <working email>)`. Wikimedia refuses empty User-Agents and placeholder domains, and rate-limits shared cloud IPs; if a cloud sandbox gets 429s, fetch from another network (for example a GitHub Actions runner) and keep the original file. Never substitute a different file.

---

## 7. Output and subtitles

- 1920x1080, 30 fps, H.264, AAC 48 kHz stereo, -16 LUFS integrated, -1.5 dBTP.
- `out/subtitles.srt` from `audio/timings.json`: lines of at most 42 characters, at most two on screen. The same cues are burned in as a small strip near the bottom, except over frames whose note says nothing may be on screen.

---

## 8. Credits and attribution

From every photo used, read `title`, `author`, `licence`, `page_url`. Write `out/credits.txt` grouped by licence, one line per image: `<title> — <author> — <licence> — <page_url>`. Credit every licence. Build an end credits card from the same data, held 6 seconds after a fade to black. Write `out/description.txt` with the same attributions, at least one primary source, and a line saying the illustrations and animation are AI-generated.

---

## 9. Failure behaviour

**Stop and report. Never silently substitute.** On any of:

- A photo URL returns 404, 403 or a non-image (persistent 429s are reported, not worked around with another file)
- A generation is refused by the image model
- A prompt asks for a photoreal image, a real person's likeness, graphic content or text
- A `photos` entry is missing `author`, `licence` or `page_url`
- A `caption` cannot be rendered
- A beat references a cast member, pose, set, prop or photo that is not declared
- A segment is covered by no beat, or by more than one
- The assembled runtime differs from `runtime_target_sec` by more than 15%

---

## 10. Pre-upload checklist

The agent writes `out/checklist.md` with these unticked. A human ticks them.

- [ ] Watched end to end at full length
- [ ] No generated image is photoreal, a likeness of a real person, or graphic
- [ ] Every photo credited in `credits.txt`
- [ ] Every `caption` visible for as long as its card is, and the title overlay appears once
- [ ] Structural silences intact: nothing moving, nothing playing
- [ ] Subtitles synced and free of mis-spelled proper nouns
- [ ] "Altered or synthetic content" toggled in YouTube Studio
- [ ] Description includes attributions, at least one primary source, and the AI-illustration line
