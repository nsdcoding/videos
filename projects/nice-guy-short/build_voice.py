import json, os, wave, hashlib, sys
sys.path.insert(0, "/home/user/videos/projects/mind-tricks")
from tts import synth
V = "hi-IN-Chirp3-HD-Umbriel"
lines = [l.strip() for l in open("script.txt") if l.strip()]
os.makedirs("vo", exist_ok=True)
rate = 24000; frames = bytearray(); t = 0.3; frames += b"\x00\x00" * int(rate * 0.3); out = []
for i, s in enumerate(lines):
    f = "vo/" + hashlib.md5((V + s).encode()).hexdigest()[:12] + ".wav"
    if not os.path.exists(f): synth(s, f, V)
    w = wave.open(f); data = w.readframes(w.getnframes()); d = w.getnframes() / w.getframerate()
    out.append({"text": s, "head": False, "start": round(t, 3), "end": round(t + d, 3)})
    frames += data; t += d
    gap = 0.35 if i < len(lines) - 1 else 0.4
    frames += b"\x00\x00" * int(rate * gap); t += gap
w = wave.open("narration.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(bytes(frames)); w.close()
json.dump(out, open("timing.json", "w"), ensure_ascii=False, indent=1)
for s in out: print(s["start"], s["end"], s["text"][:40])
print("total", round(t, 2))
