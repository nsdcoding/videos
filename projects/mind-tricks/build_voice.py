import re, json, os, wave, struct, hashlib
from concurrent.futures import ThreadPoolExecutor
from tts import synth
md = open("script.md").read().split("---", 1)[1]
sents = []; sec = 0
for para in [p.strip() for p in md.split("\n") if p.strip()]:
    if para.startswith("#"):
        sec += 1; sents.append({"text": para.lstrip("# ").strip(), "head": True, "sec": sec, "pe": True}); continue
    parts = [s.strip() for s in re.split(r"(?<=[।?!])\s+", para) if s.strip()]
    for k, s in enumerate(parts):
        sents.append({"text": s, "head": False, "sec": sec, "pe": k == len(parts) - 1})
print(len(sents), "sentences", sum(len(s["text"]) for s in sents), "chars")
os.makedirs("vo2", exist_ok=True)
key = lambda i: "vo2/" + hashlib.md5(sents[i]["text"].encode()).hexdigest()[:12] + ".wav"
def job(i):
    out = key(i)
    if not os.path.exists(out): synth(sents[i]["text"], out)
    return i
with ThreadPoolExecutor(4) as ex: list(ex.map(job, range(len(sents))))
# assemble with pauses
rate = 24000; frames = bytearray(); t = 0.4
frames += b"\x00\x00" * int(rate * 0.4)
for i, s in enumerate(sents):
    w = wave.open(key(i)); data = w.readframes(w.getnframes()); d = w.getnframes() / w.getframerate()
    s["start"] = round(t, 3); s["end"] = round(t + d, 3)
    frames += data; t += d
    gap = 0.9 if s["head"] else (0.65 if s["pe"] else 0.3)
    if i + 1 < len(sents) and sents[i + 1]["head"]: gap = 1.0
    frames += b"\x00\x00" * int(rate * gap); t += gap
w = wave.open("narration.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(bytes(frames)); w.close()
json.dump(sents, open("timing.json", "w"), ensure_ascii=False, indent=1)
print("total", round(t, 1), "s")
