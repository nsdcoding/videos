# Pustika promo

Current cut: `pustika_promo_7s.mp4` (7 s, voice only, from `promo2.html` + `v/vo2t.wav` placed at 0.5 s). Older 21 s cut: `pustika_promo.mp4`.

- `pustika_promo.mp4` — final video
- `promo.html` — the animation; `render(t)` draws frame at time t
- `render.js` — `node render.js test 3.5 9` (stills) / `node render.js full 21` (frames -> video.mp4)
- `tts.py` — Google Cloud TTS, voice `hi-IN-Chirp3-HD-Sulafat` (lines in `v/`)
- `music.py` — synthesized music bed + SFX -> music.wav
- `a/` — crops of the app screenshots (stitched scrolling screen, covers, logo, tab bar)

Voice placement: l1 @2.9s, l2a @8.1s, l2b @9.2s, l3 @16.0s; music side-chain ducked under voice.
