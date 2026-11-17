#!/usr/bin/env python3
"""Generate a channel-style illustration ("sticker") with Gemini 2.5 Flash Image (Nano Banana) on Vertex AI,
cut out its background, and log the prompt.  Use ONLY where Manim/SVG drawing is not enough (see SKILL.md).

  python3 .claude/skills/math-lab-video/scripts/sticker.py "<subject>" <video>/assets/<name>.png
        [--ref <png> ...]      keep a character or object consistent with an earlier sticker
        [--aspect 1:1]         1:1 (default), 16:9, 9:16, 4:3, 3:4
        [--keep-bg]            keep the plain background (e.g. a full-frame scene card)

Writes <name>.png (transparent cutout) and <name>_raw.png (as generated), and appends the prompt to
<video>/assets/IMAGES.md.  Afterwards ALWAYS open the PNG and check it: no letters, words, numbers, logos,
real brands or real people; regenerate if any appear.  Credentials: GCP_SA_KEY_B64 (same key as tts.py);
self-contained, does not use the repo's shared gen.py.
"""
import argparse, base64, datetime, json, mimetypes, os, pathlib, sys, time

MODEL = "gemini-2.5-flash-image"   # "Nano Banana" on Vertex AI (location global)
SA = pathlib.Path("/tmp/sa.json")
STYLE = ("Flat vector illustration in a minimal modern editorial style, clean shapes, no gradients, no shadows, "
         "thin consistent outlines. Limited palette: soft violet #9085e9, warm orange #d95926, teal green #199e70, "
         "blue #3987e5, warm yellow #fab219, off-white #f0efec. Solid plain dark charcoal background (#3a3a37) filling "
         "the whole image, nothing touching the edges, generous empty margin. Absolutely no text, letters, numbers, "
         "labels, logos, brand marks or watermarks anywhere in the image. Generic people only, not resembling any real person.")


def generate(prompt, out, aspect="1:1", refs=()):
    """One image from Gemini 2.5 Flash Image on Vertex AI, written to `out` (PNG)."""
    import requests, google.auth.transport.requests
    from google.oauth2 import service_account
    if not SA.exists():
        SA.write_bytes(base64.b64decode(os.environ["GCP_SA_KEY_B64"])); SA.chmod(0o600)
    cr = service_account.Credentials.from_service_account_file(str(SA), scopes=["https://www.googleapis.com/auth/cloud-platform"])
    cr.refresh(google.auth.transport.requests.Request())
    proj = json.loads(SA.read_text())["project_id"]
    parts = [{"inlineData": {"mimeType": mimetypes.guess_type(r)[0] or "image/png",
                             "data": base64.b64encode(pathlib.Path(r).read_bytes()).decode()}} for r in refs]
    parts.append({"text": prompt})
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}}
    url = f"https://aiplatform.googleapis.com/v1/projects/{proj}/locations/global/publishers/google/models/{MODEL}:generateContent"
    for attempt in range(6):
        r = requests.post(url, json=body, timeout=300, headers={"Authorization": f"Bearer {cr.token}"})
        if r.status_code == 200:
            data = [p_["inlineData"] for p_ in r.json()["candidates"][0]["content"].get("parts", []) if "inlineData" in p_]
            if data:
                pathlib.Path(out).write_bytes(base64.b64decode(data[0]["data"])); return
            print("no image returned, retrying", file=sys.stderr)
        elif r.status_code not in (429, 500, 503):
            sys.exit(f"{MODEL} {r.status_code}: {r.text[:500]}")
        time.sleep(2 ** attempt * 2)
    sys.exit(f"{MODEL}: failed after retries")


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
    generate(prompt, raw, a.aspect, a.ref)
    if a.keep_bg:
        import shutil; shutil.copy(raw, out); frac = 0.0
    else:
        frac = cut_out(raw, out)
    log = out.parent / "IMAGES.md"
    if not log.exists():
        log.write_text("# Generated images (Gemini 2.5 Flash Image, 'Nano Banana')\n\nEvery generated image, its prompt, and why Manim was not enough.\n\n")
    with log.open("a") as f:
        f.write(f"## {out.name}\n- date: {datetime.date.today()}\n- subject: {a.subject}\n- refs: {', '.join(a.ref) or '-'}\n"
                f"- aspect: {a.aspect} · background removed: {not a.keep_bg} ({frac:.0%} of pixels)\n- why: FILL\n\n")
    print(f"wrote {out} (raw: {raw.name}); background {frac:.0%}. Now OPEN THE IMAGE and check for text/logos.")


if __name__ == "__main__":
    main()
