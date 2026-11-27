# usage: python3 voice.py <short-dir>   -> narration.wav, timing.json, env.json
import json, os, wave, hashlib, sys
import numpy as np
sys.path.insert(0, "/home/user/videos/projects/mind-tricks")
from tts import synth
V = "hi-IN-Chirp3-HD-Umbriel"
D = sys.argv[1]
lines = [l.strip() for l in open(f"{D}/script.txt") if l.strip()]
os.makedirs("vo", exist_ok=True)
rate = 24000; frames = bytearray(); t = 0.3; frames += b"\x00\x00" * int(rate * 0.3); out = []
for i, s in enumerate(lines):
    f = "vo/" + hashlib.md5((V + s).encode()).hexdigest()[:12] + ".wav"
    if not os.path.exists(f): synth(s, f, V)
    w = wave.open(f); assert w.getframerate() == rate; data = w.readframes(w.getnframes()); d = w.getnframes() / rate
    out.append({"text": s, "head": False, "start": round(t, 3), "end": round(t + d, 3)})
    frames += data; t += d
    gap = 0.35 if i < len(lines) - 1 else 0.5
    frames += b"\x00\x00" * int(rate * gap); t += gap
w = wave.open(f"{D}/narration.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(bytes(frames)); w.close()
json.dump(out, open(f"{D}/timing.json", "w"), ensure_ascii=False, indent=1)
a = np.frombuffer(bytes(frames), np.int16).astype(np.float32); hop = rate // 30
rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
rms = np.clip(rms / np.percentile(rms[rms > 50], 80), 0, 1.5)
json.dump([round(float(x), 3) for x in rms], open(f"{D}/env.json", "w"))
for s in out: print(s["start"], s["end"], s["text"][:40])
print("total", round(t, 2))
