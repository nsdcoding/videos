#!/usr/bin/env python3
"""Process clips -> exact timeline.

For each clip: trim lead/tail silence (keep 40 ms), cap internal silences at 0.55 s,
gain-normalise to -20 LUFS (integrated, measured with ffmpeg ebur128).
Then join with each segment's pause_after, starting after LEAD seconds.
Outputs audio/voiceover.wav (48 kHz mono, final loudnorm to -14 LUFS / -1.5 dBTP, linear)
and timings.json [{id, chapter, start, end, text}].
"""
import json, pathlib, re, subprocess, wave
import numpy as np

HERE = pathlib.Path(__file__).parent
CLIPS, PROC = HERE / "audio" / "clips", HERE / "audio" / "proc"
SR, LEAD, TAIL = 24000, 0.6, 1.5
THR_DB, KEEP, CAP = -42.0, 0.04, 0.55


def read(p):
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def write(p, x, sr=SR):
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def lufs(p):
    o = subprocess.run(["ffmpeg", "-nostats", "-i", str(p), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+([-\d.]+) LUFS", o)[-1])


def process(x):
    hop = int(0.01 * SR)
    n = len(x) // hop
    rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    loud = 20 * np.log10(rms) > THR_DB
    idx = np.flatnonzero(loud)
    a, b = max(0, idx[0] * hop - int(KEEP * SR)), min(len(x), (idx[-1] + 1) * hop + int(KEEP * SR))
    # internal silences
    out, i, cap = [], idx[0], int(CAP / 0.01)
    keep = np.ones(n, bool)
    run = 0
    for f in range(idx[0], idx[-1] + 1):
        run = run + 1 if not loud[f] else 0
        if run > cap:
            keep[f] = False
    mask = np.repeat(keep, hop)
    mask = np.concatenate([mask, np.ones(len(x) - len(mask), bool)])
    y = x[a:b][mask[a:b]]
    f = int(0.008 * SR)  # tiny fades at edges
    y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y


if __name__ == "__main__":
    PROC.mkdir(parents=True, exist_ok=True)
    S = json.loads((HERE / "script.json").read_text())
    parts, timings, t = [np.zeros(int(LEAD * SR), np.float32)], [], LEAD
    for s in S:
        y = process(read(CLIPS / f"{s['id']}.wav"))
        tmp = PROC / f"{s['id']}.wav"; write(tmp, y)
        g = 10 ** ((-20.0 - lufs(tmp)) / 20); y = y * g; write(tmp, y)
        dur = len(y) / SR
        timings.append(dict(id=s["id"], chapter=s["chapter"], start=round(t, 3),
                            end=round(t + dur, 3), text=s["text"]))
        parts += [y, np.zeros(int(round(s["pause_after"] * SR)), np.float32)]
        t += dur + int(round(s["pause_after"] * SR)) / SR
    parts.append(np.zeros(int(TAIL * SR), np.float32))
    full = np.concatenate(parts)
    write(HERE / "audio" / "voice_raw.wav", full)
    total = len(full) / SR
    # gentle oversampled peak limiter (touches ~1% of samples) so linear loudnorm can reach -14 LUFS under -1.5 dBTP
    lim = HERE / "audio" / "voice_lim.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(HERE / "audio" / "voice_raw.wav"), "-af",
                    "aresample=96000,alimiter=limit=0.35:attack=1:release=40:level=disabled,aresample=24000",
                    str(lim)], check=True)
    # final loudness: two-pass loudnorm (linear) to -14 LUFS, 48 kHz
    o = subprocess.run(["ffmpeg", "-nostats", "-i", str(lim), "-af",
                        "loudnorm=I=-14:TP=-2.0:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(o[o.rindex("{"):o.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-2.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(lim), "-af", af,
                    "-ar", "48000", "-t", f"{total:.3f}", str(HERE / "audio" / "voiceover.wav")], check=True)
    (HERE / "timings.json").write_text(json.dumps(dict(total=round(total, 3), segments=timings), indent=1))
    print(f"total {total:.2f}s = {total/60:.2f} min; {len(timings)} segments")
