"""Chirp3 HD TTS via Cloud Text-to-Speech. tts.py "text" out.wav [voice]"""
import sys, base64, json, runpy, wave
m = runpy.run_path("/home/user/videos/skills/motion-video-style/scripts/vertex_assets.py")
vx = m["Vertex"]()
def synth(text, out, voice="hi-IN-Chirp3-HD-Zubenelgenubi"):
    if not vx.creds.valid: vx.creds.refresh(vx.Request())
    body = {"input": {"text": text}, "voice": {"languageCode": "hi-IN", "name": voice},
            "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000}}
    for a in range(6):
        r = vx.requests.post("https://texttospeech.googleapis.com/v1/text:synthesize", json=body,
            headers={"Authorization": f"Bearer {vx.creds.token}", "x-goog-user-project": vx.project}, timeout=120)
        if r.status_code == 200: break
        if r.status_code in (429, 500, 503): import time; time.sleep(2 ** a); continue
        sys.exit(f"TTS {r.status_code}: {r.text[:500]}")
    open(out, "wb").write(base64.b64decode(r.json()["audioContent"]))
if __name__ == "__main__":
    synth(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
    w = wave.open(sys.argv[2]); print(sys.argv[2], round(w.getnframes() / w.getframerate(), 2), "s")
