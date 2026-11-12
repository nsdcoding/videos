# Day 25 · RAG with real files (Part 1: the PDF) — lesson video

A ~26 minute narrated lesson that walks students through `day25_rag.py`, using
a VS Code replica plus one big "world" canvas where the camera flies between
concept boards.

## How it is built

| Piece | File |
|---|---|
| Narration script (one line per sentence, `{shown|spoken}` for pronunciation) | `narration.txt` |
| Chirp 3 HD voice (`en-IN-Chirp3-HD-Charon`) per line → `audio/*.wav` | `tts.py`, `tts_all.py` |
| Python → VS Code Dark+ highlighted lines | `highlight.py` → `src/code_*.js` |
| Deterministic motion engine (everything is a function of time `t`) | `src/engine.js` |
| VS Code window, editor focus/marks/notes, terminal, HUD + subtitles | `src/components.js` |
| One scene file per chapter (boards + animation cues tied to spoken words) | `src/scenes/*.js` |
| Real outputs from running the lesson code on the sample docs | `assets/runs.json` |
| Frame renderer (Playwright, parallel) / audio mix / final parts | `render.js`, `mix.py`, `assemble.py` |

## Rebuild

```bash
python3 tts_all.py                 # voice lines (needs GCP_SA_KEY_B64)
python3 highlight.py day25_rag day22_rag
node timing.js && python3 plan.py  # timeline + render jobs
node render.js /tmp/segs jobs.json 4
python3 mix.py
python3 assemble.py /tmp/segs out
```

Preview any moment: `node stills.js /tmp/st a01:4 f28:3` (line id : seconds into that line).

## Reusing for the next lesson

Keep `engine.js`, `components.js`, `style.css`, the render/mix scripts.
Write a new `narration.txt`, drop the new `.py` into `assets/`, run
`highlight.py`, and write new `src/scenes/*.js`. The scene API:

- `T(id)`, `W(id, "word")` – time a line starts / a word is spoken
- `focus(t, '25', L1, L2)` – scroll the editor, spotlight lines, move the camera
- `mark`, `note`, `camTok` – box a token, pin a callout, zoom onto a token
- `panel`, `termCmd`, `termLine`, `termClear` – the integrated terminal
- `board(id, x, y, html)`, `camB(t, dur, board, x, y, zoom, {dip})` – concept boards and camera flights
- `popIn`, `fadeUp`, `slideL/R`, `wipe`, `drawIn`, `count`, `pulse`, `shake`, `glow` – motion verbs
