#!/usr/bin/env python3
"""Generate video assets on Vertex AI: images (Nano Banana) and voiceover (Gemini TTS).

Usage:
  vertex_assets.py image "prompt" out.png [--aspect 16:9] [--ref a.png ...] [--model M]
  vertex_assets.py voice "text" out.wav [--voice Kore] [--style "Say calmly:"] [--model M]
  vertex_assets.py batch scenes.json OUT_DIR      # many images/voice lines in one run

scenes.json: [{"id": "s01", "image": "prompt", "voice": "narration text"}, ...]
Either key is optional per scene. Existing outputs are skipped, so reruns resume.
"""
import argparse, base64, json, mimetypes, os, sys, time, wave

KEY_PATH = "/tmp/sa.json"
SCOPE = "https://www.googleapis.com/auth/cloud-platform"
IMAGE_MODEL = "gemini-2.5-flash-image"   # Nano Banana
TTS_MODEL = "gemini-2.5-flash-tts"


def ensure_deps():
    try:
        import google.auth, requests  # noqa: F401
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "google-auth", "requests"])


def ensure_key():
    if not os.path.exists(KEY_PATH):
        b64 = os.environ.get("GCP_SA_KEY_B64")
        if not b64:
            sys.exit("No /tmp/sa.json and GCP_SA_KEY_B64 is not set")
        with open(KEY_PATH, "wb") as f:
            f.write(base64.b64decode(b64))
        os.chmod(KEY_PATH, 0o600)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH


class Vertex:
    def __init__(self):
        ensure_deps(); ensure_key()
        import google.auth, requests
        from google.auth.transport.requests import Request
        self.requests, self.Request = requests, Request
        self.creds, self.project = google.auth.default(scopes=[SCOPE])

    def generate(self, model, body):
        # Token minted from the key file; `gcloud auth print-access-token` gives a placeholder here.
        if not self.creds.valid:
            self.creds.refresh(self.Request())
        url = (f"https://aiplatform.googleapis.com/v1/projects/{self.project}"
               f"/locations/global/publishers/google/models/{model}:generateContent")
        for attempt in range(6):
            r = self.requests.post(url, json=body, timeout=300, headers={
                "Authorization": f"Bearer {self.creds.token}"})
            if r.status_code == 200 and "candidates" not in r.json():
                # e.g. promptFeedback.blockReason: report it; repeated blocks end in a failure exit
                print(f"  no candidates: {json.dumps(r.json())[:300]}", file=sys.stderr)
            elif r.status_code == 200:
                parts = r.json()["candidates"][0]["content"].get("parts", [])
                data = [p["inlineData"] for p in parts if "inlineData" in p]
                if data:
                    return data[0]
                print(f"  no media returned: {json.dumps(parts)[:300]}", file=sys.stderr)
            elif r.status_code in (429, 500, 503):
                print(f"  {r.status_code}, retrying", file=sys.stderr)
            else:
                sys.exit(f"{model} {r.status_code}: {r.text[:600]}")
            time.sleep(2 ** attempt * 2)
        sys.exit(f"{model}: failed after retries")

    def image(self, prompt, out, aspect="16:9", refs=(), model=IMAGE_MODEL):
        parts = []
        for ref in refs:  # reference images keep characters/style consistent
            mime = mimetypes.guess_type(ref)[0] or "image/png"
            parts.append({"inlineData": {"mimeType": mime,
                          "data": base64.b64encode(open(ref, "rb").read()).decode()}})
        parts.append({"text": prompt})
        d = self.generate(model, {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": aspect}}})
        with open(out, "wb") as f:
            f.write(base64.b64decode(d["data"]))
        print(f"image -> {out}")

    def voice(self, text, out, voice="Kore", style="", model=TTS_MODEL):
        d = self.generate(model, {
            "contents": [{"role": "user", "parts": [{"text": f"{style} {text}".strip()}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}})
        pcm = base64.b64decode(d["data"])  # raw 16-bit mono PCM, 24 kHz
        rate = int(d["mimeType"].split("rate=")[-1]) if "rate=" in d["mimeType"] else 24000
        with wave.open(out, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
        print(f"voice -> {out} ({len(pcm) / (2 * rate):.2f}s)")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("image"); a.add_argument("prompt"); a.add_argument("out")
    a.add_argument("--aspect", default="16:9"); a.add_argument("--ref", nargs="*", default=[])
    a.add_argument("--model", default=IMAGE_MODEL)
    v = sub.add_parser("voice"); v.add_argument("text"); v.add_argument("out")
    v.add_argument("--voice", default="Kore"); v.add_argument("--style", default="")
    v.add_argument("--model", default=TTS_MODEL)
    b = sub.add_parser("batch"); b.add_argument("scenes"); b.add_argument("outdir")
    b.add_argument("--aspect", default="16:9"); b.add_argument("--voice", default="Kore")
    b.add_argument("--style", default=""); b.add_argument("--ref", nargs="*", default=[])
    args = ap.parse_args()

    vx = Vertex()
    if args.cmd == "image":
        vx.image(args.prompt, args.out, args.aspect, args.ref, args.model)
    elif args.cmd == "voice":
        vx.voice(args.text, args.out, args.voice, args.style, args.model)
    else:
        os.makedirs(args.outdir, exist_ok=True)
        for s in json.load(open(args.scenes)):
            img, wav = (os.path.join(args.outdir, f"{s['id']}.{e}") for e in ("png", "wav"))
            if s.get("image") and not os.path.exists(img):
                vx.image(s["image"], img, args.aspect, args.ref)
            if s.get("voice") and not os.path.exists(wav):
                vx.voice(s["voice"], wav, args.voice, s.get("style", args.style))


if __name__ == "__main__":
    main()
