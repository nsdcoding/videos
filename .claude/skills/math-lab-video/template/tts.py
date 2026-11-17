#!/usr/bin/env python3
"""Google Cloud Text-to-Speech, one clip per segment.

  python3 tts.py test "sentence" out.wav
  python3 tts.py all            # synthesise every segment in script.json -> audio/clips/<id>.wav

Credentials: GCP_SA_KEY_B64 (base64 service-account JSON), decoded to /tmp/sa.json.
Uses the voice en-US-Chirp3-HD-Zubenelgenubi, LINEAR16 @ 24 kHz.
Reruns skip clips whose text has not changed (hash stored next to the clip).
"""
import base64, hashlib, json, os, pathlib, sys, time
import requests
import google.auth.transport.requests
from google.oauth2 import service_account

VOICE = "en-US-Chirp3-HD-Zubenelgenubi"
HERE = pathlib.Path(__file__).parent
SA = pathlib.Path("/tmp/sa.json")
URL = "https://texttospeech.googleapis.com/v1/text:synthesize"

# Spelling fixes for words the voice mispronounces (spoken form only; subtitles keep the original).
SPOKEN_FIXES = {}
# Per-segment spoken spellings: {segment id: [(written, spoken), ...]}
SPOKEN_FIXES_BY_ID = {
    "s108": [("with Bayes.", "with Bays.")],   # heard as "bass" at the end of the sentence
}


def creds():
    if not SA.exists():
        SA.write_bytes(base64.b64decode(os.environ["GCP_SA_KEY_B64"]))
        SA.chmod(0o600)
    c = service_account.Credentials.from_service_account_file(
        str(SA), scopes=["https://www.googleapis.com/auth/cloud-platform"])
    c.refresh(google.auth.transport.requests.Request())
    return c


def spoken(text, sid=None):
    for a, b in SPOKEN_FIXES.items():
        text = text.replace(a, b)
    for a, b in SPOKEN_FIXES_BY_ID.get(sid, []):
        text = text.replace(a, b)
    return text


def synth(c, text, out, sid=None):
    body = {"input": {"text": spoken(text, sid)},
            "voice": {"languageCode": "en-US", "name": VOICE},
            "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000}}
    for attempt in range(6):
        if not c.valid:
            c.refresh(google.auth.transport.requests.Request())
        r = requests.post(URL, json=body, timeout=120, headers={
            "Authorization": f"Bearer {c.token}",
            "x-goog-user-project": json.loads(SA.read_text())["project_id"]})
        if r.status_code == 200:
            pathlib.Path(out).write_bytes(base64.b64decode(r.json()["audioContent"]))
            return
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(2 ** attempt); continue
        sys.exit(f"TTS error {r.status_code}: {r.text[:500]}")
    sys.exit("TTS kept failing")


if __name__ == "__main__":
    c = creds()
    if sys.argv[1] == "test":
        synth(c, sys.argv[2], sys.argv[3]); print("wrote", sys.argv[3])
    else:
        d = HERE / "audio" / "clips"; d.mkdir(parents=True, exist_ok=True)
        S = json.loads((HERE / "script.json").read_text())
        from concurrent.futures import ThreadPoolExecutor
        def job(s):
            h = hashlib.sha1((VOICE + spoken(s["text"], s["id"])).encode()).hexdigest()
            wav, hf = d / f"{s['id']}.wav", d / f"{s['id']}.hash"
            if wav.exists() and hf.exists() and hf.read_text() == h:
                return
            synth(c, s["text"], wav, s["id"]); hf.write_text(h); print(s["id"], flush=True)
        with ThreadPoolExecutor(6) as ex:
            list(ex.map(job, S))
        print("all clips done")
