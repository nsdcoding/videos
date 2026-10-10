---
name: motion-video-style
description: Use when making any narrated, explainer or long-form motion graphic video for Naushad, or generating its images and voiceover, to apply his preferred visual style and his Vertex AI asset pipeline (Nano Banana images, Gemini TTS voice).
---

# Motion video style preference

Naushad wants every video, including long narrated ones (10+ minutes), to feel like real motion design, not animated subtitles.

## Do
- Keep the spoken text small, as a subtitle strip near the bottom of the screen.
- Give the main screen a new animated visual for every sentence or key idea, for example:
  - illustrated scenes or line-art drawings that build on screen
  - diagrams, flowcharts and comparisons that animate in
  - number and stat reveals, counters, charts
  - icons and symbols that change and transform with the topic
  - camera moves: push-ins, pans, parallax, zoom-throughs
  - varied transitions between ideas (wipes, masks, splits, morphs)
- Aim for something new happening on screen every 2–3 seconds, like a hand-animated promo.
- Keep variety high across the video. Avoid one repeated layout for long stretches.

## Don't
- Don't let the narration text become the main visual for minutes at a time.
- Don't rely on one slowly moving icon per section as the only motion.

## Other preferences
- No background music in religious (Islamic) content; voice only.
- Landscape 16:9 for explainer videos unless he says otherwise.
- Make a short sample first for approval before rendering a long video.

# Asset pipeline: images and voiceover on Vertex AI

Generate all images and narration on Google Vertex AI with the bundled script
`scripts/vertex_assets.py` (in this skill's folder). Don't substitute other image or TTS providers unless he asks.

## Credentials
- The service-account key comes from the env var `GCP_SA_KEY_B64` (base64 JSON).
  The script decodes it to `/tmp/sa.json` (mode 600) and sets `GOOGLE_APPLICATION_CREDENTIALS` itself.
- Project: `claudevideo-503905`, account `vertex-express@claudevideo-503905.iam.gserviceaccount.com`.
- Auth uses Python `google-auth` (the script installs it with `requests` if missing) and mints the
  OAuth token from the key file. **Do not use `gcloud auth print-access-token`**: in the cloud
  sandbox it returns a short placeholder token that Vertex rejects with 401 `CREDENTIALS_MISSING`.
- Never print, commit or copy the key or token anywhere.

## Models (verified working)
- Images: `gemini-2.5-flash-image` (Nano Banana), `global` endpoint, `responseModalities: ["IMAGE"]`,
  `imageConfig.aspectRatio` `"16:9"` by default (1344×768 PNG).
- Voice: `gemini-2.5-flash-tts`, `global` endpoint, prebuilt voice `Kore` by default.
  It returns raw 16-bit mono PCM at 24 kHz; the script wraps it into a `.wav`.
- Endpoint: `https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/publishers/google/models/{model}:generateContent`.
- To try another model (for example a newer Nano Banana), pass `--model`; keep the defaults if it errors.

## Commands
```bash
S=<this skill's folder>/scripts/vertex_assets.py

# one image (add --ref char.png to keep a character or style consistent)
python3 $S image "flat vector illustration of ..." assets/s01.png --aspect 16:9

# one voice line; --style is a spoken-delivery instruction prepended to the text
python3 $S voice "Narration sentence here." assets/s01.wav --voice Kore --style "Say warmly:"

# a whole video: one entry per scene/sentence; reruns skip finished files
python3 $S batch scenes.json assets/ --voice Kore --ref assets/style_ref.png
```
`scenes.json`: `[{"id": "s01", "image": "<prompt>", "voice": "<narration>", "style": "optional"}, ...]`

## How to use it in a video
- Write the script first, split into sentences/key ideas, and make one scene per idea
  (this matches the "new visual every 2–3 seconds" rule above).
- Generate voice **per scene**, not one long file. The WAV length of each line sets that scene's
  duration and timing, and short calls avoid TTS length limits. Concatenate for the final mix.
- Image prompts: say the style explicitly every time (for example "clean flat vector illustration,
  consistent palette, no text"). Ask for "no text" in images: Nano Banana garbles small text, so
  put titles, numbers and labels in the motion layer instead.
- For a recurring character or consistent look, generate one reference image, check it, then pass
  it with `--ref` to every later image.
- Treat generated images as raw material: animate them (parallax layers, push-ins, masks,
  builds) rather than showing them as static slides.
- Keep voice consistent: same voice and style across a video. For Islamic content use a calm,
  respectful delivery and no music.
- For the approval sample, generate only the first 3–5 scenes, render, and share before batching the rest.
- On 429/5xx the script retries with backoff; if a call keeps failing, report the error text.
