#!/usr/bin/env python3
"""Listen-check: transcribe every clip with Google Speech-to-Text and diff it against the script.
Writes audio/listen_check.json and prints segments where words differ."""
import base64, difflib, json, pathlib, re, sys
from concurrent.futures import ThreadPoolExecutor
import requests
from tts import creds, SA, HERE

NUM = {}  # STT may return digits; normalise both sides to words via a small number speller

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()

def spell(n):
    n = int(n)
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n < 1000: return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + spell(n % 100))
    if n < 10**6: return spell(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + spell(n % 1000))
    return spell(n // 10**6) + " million" + ("" if n % 10**6 == 0 else " " + spell(n % 10**6))

def norm(t):
    t = t.lower().replace("-", " ").replace("%", " percent")
    t = re.sub(r"\$(\d[\d,]*)", r"\1 dollars", t)
    t = re.sub(r"(\d),(\d)", r"\1\2", t)
    t = re.sub(r"(\d+)\.(\d+)", lambda m: spell(m[1]) + " point " + " ".join(spell(d) for d in m[2]), t)
    t = re.sub(r"\d+", lambda m: spell(m[0]), t)
    t = re.sub(r"[^a-z' ]", " ", t)
    alias = {"ex": "x", "neighbors": "neighbours", "minimizing": "minimising", "p": "p", "okay": "ok"}
    return [alias.get(w, w) for w in t.split() if w not in ("and", "a", "the", "an", "of", "to", "in", "is", "it's", "it", "that", "that's", "s")]

def stt_sphinx(c, wav):
    import subprocess, tempfile
    from pocketsphinx import Decoder
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav), "-ar", "16000", "-ac", "1", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    d = Decoder(samprate=16000, logfn="/dev/null")
    d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
    return d.hyp().hypstr if d.hyp() else ""

def stt_google(c, wav):
    audio = base64.b64encode(pathlib.Path(wav).read_bytes()[44:]).decode()
    body = {"config": {"encoding": "LINEAR16", "sampleRateHertz": 24000, "languageCode": "en-US",
                       "model": "latest_long", "enableAutomaticPunctuation": True},
            "audio": {"content": audio}}
    r = requests.post("https://speech.googleapis.com/v1/speech:recognize", json=body, timeout=120,
                      headers={"Authorization": f"Bearer {c.token}",
                               "x-goog-user-project": json.loads(SA.read_text())["project_id"]})
    if r.status_code != 200:
        sys.exit(f"STT error {r.status_code}: {r.text[:400]}")
    return " ".join(x["alternatives"][0]["transcript"] for x in r.json().get("results", []))

if __name__ == "__main__":
    c = creds()
    S = json.loads((HERE / "script.json").read_text())
    if len(sys.argv) > 1:
        S = [s for s in S if s["id"] in sys.argv[1:]]
    def job(s):
        heard = stt_sphinx(c, HERE / "audio" / "clips" / f"{s['id']}.wav")
        a, b = norm(s["text"]), norm(heard)
        diffs = [(" ".join(a[i1:i2]), " ".join(b[j1:j2]))
                 for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes() if op != "equal"]
        return dict(id=s["id"], text=s["text"], heard=heard, diffs=diffs)
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(job, S))
    (HERE / "audio" / "listen_check.json").write_text(json.dumps(res, indent=1))
    bad = [r for r in res if r["diffs"]]
    for r in bad:
        print(r["id"], r["diffs"])
    print(f"{len(res) - len(bad)}/{len(res)} clips match exactly")
