import re, json, sys, os, wave
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import synth
VOICE = sys.argv[1] if len(sys.argv) > 1 else "en-IN-Chirp3-HD-Charon"
lines = []; chap = None
for ln in open("narration.txt"):
    ln = ln.rstrip("\n")
    if not ln.strip(): continue
    if ln.startswith("#"):
        chap = ln[1:].strip(); continue
    sid, txt = ln.split("|", 1)
    disp = re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\1", txt)
    spk = re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\2", txt)
    lines.append(dict(id=sid, chap=chap, text=disp, speak=spk))
os.makedirs("audio", exist_ok=True)
def job(l):
    out = f"audio/{l['id']}.wav"
    if not os.path.exists(out): synth(l["speak"], out, VOICE)
    with wave.open(out) as w: l["dur"] = w.getnframes() / w.getframerate()
    return l
with ThreadPoolExecutor(8) as ex: res = list(ex.map(job, lines))
json.dump(res, open("lines.json", "w"), indent=1)
print(len(res), "lines", round(sum(l["dur"] for l in res) / 60, 2), "min speech", sum(len(l['text'].split()) for l in res), "words")
