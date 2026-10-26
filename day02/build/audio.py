#!/usr/bin/env python3
"""BUILD_SPEC section 2: per-segment Chirp 3 HD synthesis, silences, master, timings.

  python3 build/audio.py            # all segments
  python3 build/audio.py s01 s09    # only this inclusive range (for the sample)

Reruns skip segments whose wav already exists.
"""
import base64, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DAY = os.path.dirname(HERE)
AUDIO = os.path.join(DAY, "audio")
sys.path.insert(0, os.path.join(os.path.dirname(DAY), "skills", "motion-video-style", "scripts"))


def parse_narration(path):
    text = open(path, encoding="utf-8").read()
    segs = []
    for m in re.finditer(r"^--- (s\d+)(?: \| pause_after: (\d+))?\n(.*?)(?=\n--- |\Z)", text, re.S | re.M):
        segs.append({"id": m.group(1), "pause_after": int(m.group(2) or 400),
                     "text": " ".join(m.group(3).split())})
    return segs


def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]).decode())


def synth(vx, cfg, text, out):
    from google.auth.transport.requests import Request
    if not vx.creds.valid:
        vx.creds.refresh(Request())
    lang = "-".join(cfg["voice"].split("-")[:2])
    body = {"input": {"text": text},  # plain text, never SSML (spec 2)
            "voice": {"languageCode": lang, "name": cfg["voice"]},
            "audioConfig": {"audioEncoding": cfg["encoding"], "sampleRateHertz": cfg["sample_rate_hz"],
                            "speakingRate": cfg["speaking_rate"]}}
    for attempt in range(5):
        r = vx.requests.post("https://texttospeech.googleapis.com/v1/text:synthesize", json=body, timeout=180,
                             headers={"Authorization": f"Bearer {vx.creds.token}",
                                      "x-goog-user-project": vx.project})
        if r.status_code == 200:
            open(out, "wb").write(base64.b64decode(r.json()["audioContent"]))
            return
        if r.status_code not in (429, 500, 503):
            sys.exit(f"TTS failed for {out}: {r.status_code} {r.text[:400]}")
        import time; time.sleep(2 ** attempt * 2)
    sys.exit(f"TTS failed for {out} after retries")


def main():
    build = json.load(open(os.path.join(DAY, "build.json")))
    cfg = build["audio"]
    segs = parse_narration(os.path.join(DAY, "narration.md"))
    if len(sys.argv) == 3:
        ids = [s["id"] for s in segs]
        segs = segs[ids.index(sys.argv[1]): ids.index(sys.argv[2]) + 1]
    for s in segs:
        if len(s["text"].encode()) >= 5000:
            sys.exit(f"{s['id']} is over 5000 bytes")
    os.makedirs(AUDIO, exist_ok=True)

    import vertex_assets as va
    vx = None
    for s in segs:
        out = os.path.join(AUDIO, f"{s['id']}.wav")
        if not os.path.exists(out):
            vx = vx or va.Vertex()
            synth(vx, cfg, s["text"], out)
        s["dur"] = duration(out)
        print(f"{s['id']} {s['dur']:6.2f}s  +{s['pause_after']}ms")

    rate = cfg["sample_rate_hz"]
    for p in sorted({s["pause_after"] for s in segs}):
        sil = os.path.join(AUDIO, f"silence_{p}.wav")
        if not os.path.exists(sil):
            subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                                   f"anullsrc=r={rate}:cl=mono", "-t", f"{p / 1000}",
                                   "-c:a", "pcm_s16le", sil])

    lst = os.path.join(AUDIO, "concat.txt")
    t, timings = 0.0, []
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{s['id']}.wav'\nfile 'silence_{s['pause_after']}.wav'\n")
            timings.append({"id": s["id"], "start": round(t, 3), "end": round(t + s["dur"], 3),
                            "pause_after": s["pause_after"], "text": s["text"]})
            t += s["dur"] + s["pause_after"] / 1000
    raw = os.path.join(AUDIO, "master_raw.wav")
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                           "-c:a", "pcm_s16le", raw])
    # Two-pass loudnorm to -16 LUFS / -1.5 dBTP (spec 2, Loudness)
    meas = subprocess.run(["ffmpeg", "-v", "info", "-i", raw, "-af",
                           "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    m = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    af = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:"
          f"linear=true,aresample={rate}")
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", af, "-c:a", "pcm_s16le",
                           os.path.join(AUDIO, "master.wav")])
    json.dump({"total": round(t, 3), "segments": timings},
              open(os.path.join(AUDIO, "timings.json"), "w"), indent=1)
    print(f"master.wav {t:.2f}s ({len(segs)} segments)")


if __name__ == "__main__":
    main()
