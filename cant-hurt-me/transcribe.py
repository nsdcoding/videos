import json, sys
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2] if len(sys.argv) > 2 else "medium", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe("narration.mp3", language="hi", word_timestamps=True, beam_size=1, vad_filter=True)
out = []
for s in segs:
    for w in s.words:
        out.append([round(w.start, 2), round(w.end, 2), w.word])
    print(f"{s.end:.0f}s", s.text[:60], flush=True)
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False)
