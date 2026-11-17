#!/usr/bin/env python3
"""Generate a channel-style illustration ("sticker") with Gemini 2.5 Flash Image (Nano Banana) on Vertex AI,
cut out its background, and log the prompt.  Use ONLY where Manim/SVG drawing is not enough (see SKILL.md).

  python3 .claude/skills/math-lab-video/scripts/sticker.py "<subject>" <video>/assets/<name>.png
        [--ref <png> ...]      keep a character or object consistent with an earlier sticker
        [--aspect 1:1]         1:1 (default), 16:9, 9:16, 4:3, 3:4
        [--keep-bg]            keep the plain background (e.g. a full-frame scene card)

Writes <name>.png (transparent cutout) and <name>_raw.png (as generated), and appends the prompt to
<video>/assets/IMAGES.md.  Afterwards ALWAYS open the PNG and check it: no letters, words, numbers, logos,
real brands or real people; regenerate if any appear.  Credentials: GCP_SA_KEY_B64 (via gen.py).
"""
import argparse, datetime, pathlib, subprocess, sys

REPO = pathlib.Path(__file__).resolve().parents[4]
STYLE = ("Flat vector illustration in a minimal modern editorial style, clean shapes, no gradients, no shadows, "
         "thin consistent outlines. Limited palette: soft violet #9085e9, warm orange #d95926, teal green #199e70, "
         "blue #3987e5, warm yellow #fab219, off-white #f0efec. Solid plain dark charcoal background (#3a3a37) filling "
         "the whole image, nothing touching the edges, generous empty margin. Absolutely no text, letters, numbers, "
         "labels, logos, brand marks or watermarks anywhere in the image. Generic people only, not resembling any real person.")


def cut_out(raw, out, thresh=26):
    from PIL import Image, ImageDraw, ImageFilter
    import numpy as np
    im = Image.open(raw).convert("RGB")
    W, H = im.size
    work = im.copy(); marker = (255, 0, 255)
    for seed in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1), (W // 2, 0), (0, H // 2), (W - 1, H // 2), (W // 2, H - 1)]:
        if work.getpixel(seed) != marker:
            ImageDraw.floodfill(work, seed, marker, thresh=thresh)
    bg = np.all(np.array(work) == marker, axis=2)
    alpha = Image.fromarray(((~bg) * 255).astype("uint8")).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = im.convert("RGBA"); rgba.putalpha(alpha)
    box = alpha.getbbox()
    if not box:
        sys.exit("cut-out removed everything; re-run with --keep-bg or a different subject")
    rgba.crop(box).save(out)
    return bg.mean()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject"); ap.add_argument("out")
    ap.add_argument("--ref", action="append", default=[]); ap.add_argument("--aspect", default="1:1")
    ap.add_argument("--keep-bg", action="store_true")
    a = ap.parse_args()
    out = pathlib.Path(a.out).resolve(); out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.with_name(out.stem + "_raw.png")
    prompt = f"{a.subject.strip().rstrip('.')}. {STYLE}"
    cmd = [sys.executable, str(REPO / "gen.py"), "image", prompt, str(raw), "--aspect", a.aspect]
    for r in a.ref:
        cmd += ["--ref", r]
    subprocess.run(cmd, check=True)
    if a.keep_bg:
        import shutil; shutil.copy(raw, out); frac = 0.0
    else:
        frac = cut_out(raw, out)
    log = out.parent / "IMAGES.md"
    if not log.exists():
        log.write_text("# Generated images (Gemini 2.5 Flash Image via gen.py)\n\nEvery generated image, its prompt, and why Manim was not enough.\n\n")
    with log.open("a") as f:
        f.write(f"## {out.name}\n- date: {datetime.date.today()}\n- subject: {a.subject}\n- refs: {', '.join(a.ref) or '-'}\n"
                f"- aspect: {a.aspect} · background removed: {not a.keep_bg} ({frac:.0%} of pixels)\n- why: FILL\n\n")
    print(f"wrote {out} (raw: {raw.name}); background {frac:.0%}. Now OPEN THE IMAGE and check for text/logos.")


if __name__ == "__main__":
    main()
