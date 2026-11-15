#!/usr/bin/env python3
"""Normalise scenes → join → burn subtitles/chapter label/progress bar (ASS) → mux voice-over.

  python3 build.py sample      # chapters 1-2 (the approval sample)
  python3 build.py full        # all chapters
  python3 build.py srt         # captions.srt only
"""
import json, pathlib, subprocess, sys, re
from common import CHAPTERS, SEGS, TIM, word_time

HERE = pathlib.Path(__file__).parent
B = HERE / "build"
FPS = 30
SCENES = [  # (chapter name, scene file stem, class)
    ("Two Towns", "s01_two_towns", "S01TwoTowns"),
    ("Welcome", "s01b_welcome", "S01bWelcome"),
    ("Why It Matters", "s02_why", "S02Why"),
    ("The Mean", "s03_mean", "S03Mean"),
    ("The Median", "s04_median", "S04Median"),
    ("Stress Test", "s05_stress", "S05Stress"),
    ("Which One to Trust", "s06_trust", "S06Trust"),
    ("Real World", "s07_real", "S07Real"),
    ("Common Mistakes", "s08_mistakes", "S08Mistakes"),
    ("Recipe", "s09_recipe", "S09Recipe"),
    ("Subscribe", "s09b_subscribe", "S09bSubscribe"),
    ("Next Time", "s10_next", "S10Next"),
]
MAXC = 64  # max characters per subtitle line


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    return r


def chunks(sid):
    """Split a segment's text into ≤MAXC-char pieces at word boundaries, preferring punctuation.
    Returns [(start, end, text)] using estimated word times."""
    s = SEGS[sid]
    words = s["text"].split()
    out, cur, k0 = [], [], 0
    for i, w in enumerate(words):
        cur.append(w)
        line = " ".join(cur)
        nxt = len(line) + 1 + (len(words[i + 1]) if i + 1 < len(words) else 0)
        brk = i + 1 == len(words) or nxt > MAXC or (w[-1] in ".?!;" and len(line) > 22) or \
              (w[-1] == "," and len(line) > 40)
        if brk:
            out.append((k0, i + 1, line)); cur, k0 = [], i + 1
    res = []
    for j, (a, b, line) in enumerate(out):
        st = s["start"] if j == 0 else word_time(sid, a)
        en = s["end"] if j == len(out) - 1 else word_time(sid, b)
        res.append((st, en, line))
    return res


def ts_ass(t):
    cs = int(round(t * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def ts_srt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def ass(t0, t1, total):
    """Overlay events for the window [t0, t1); times shifted so t0 → 0. Progress is relative to the full video."""
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter,40,&H00ECEFF0,&H00ECEFF0,&HB0131313,&HB0131313,0,0,0,0,100,100,0,0,3,14,0,2,200,200,62,1
Style: Chap,Inter Display,30,&H00B7C2C3,&H00B7C2C3,&H00000000,&H00000000,1,0,0,0,100,100,1,0,1,0,0,7,44,0,34,1
Style: Bar,Inter,10,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    dur = t1 - t0
    def E(a, b, style, text, layer=0):
        a, b = max(a, t0), min(b, t1)
        if b > a:
            ev.append(f"Dialogue: {layer},{ts_ass(a - t0)},{ts_ass(b - t0)},{style},,0,0,0,,{text}")
    # subtitles
    for sid in SEGS:
        for a, b, line in chunks(sid):
            E(a, b, "Sub", line.replace("{", "(").replace("}", ")"))
    # chapter label: small accent bar + name, fades in at each chapter
    for k, c in enumerate(CHAPTERS):
        E(c["t0"], c["t1"], "Chap", r"{\fad(400,250)\c&H19B2FA&}▍{\c&HB7C2C3&} " + c["name"], 2)
    # progress bar: track + fill (clip animated across the window) + chapter ticks, top edge, 6 px
    W, H, Y = 1920, 6, 0
    track = rf"{{\an7\pos(0,{Y})\bord0\shad0\1c&H3A3A37&\p1}}m 0 0 l {W} 0 {W} {H} 0 {H}{{\p0}}"
    E(t0, t1, "Bar", track, 3)
    x0 = W * t0 / total; x1 = W * t1 / total
    fill = (rf"{{\an7\pos(0,{Y})\bord0\shad0\1c&H19B2FA&\clip(0,0,{x0:.1f},{H})"
            rf"\t(0,{int(dur * 1000)},\clip(0,0,{x1:.1f},{H}))\p1}}m 0 0 l {W} 0 {W} {H} 0 {H}{{\p0}}")
    E(t0, t1, "Bar", fill, 4)
    for c in CHAPTERS[1:]:
        x = W * c["t0"] / total
        E(t0, t1, "Bar", rf"{{\an7\pos({x - 2:.1f},{Y})\bord0\shad0\1c&H1A1A19&\p1}}m 0 0 l 4 0 4 {H} 0 {H}{{\p0}}", 5)
    return hdr + "\n".join(ev) + "\n"


def srt():
    lines, n = [], 1
    for sid in SEGS:
        for a, b, line in chunks(sid):
            lines += [str(n), f"{ts_srt(a)} --> {ts_srt(b)}", line, ""]; n += 1
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / "out" / "captions.srt").write_text("\n".join(lines))


def scene_video(stem, cls):
    return B / "media" / "videos" / stem / "1080p30" / f"{cls}.mp4"


def normalise(ch, stem, cls):
    c = next(c for c in CHAPTERS if c["name"] == ch)
    n = round(c["t1"] * FPS) - round(c["t0"] * FPS)  # exact frames, cumulative-rounding safe
    src = scene_video(stem, cls)
    out = B / "norm" / f"{stem}.mp4"; out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"fps={FPS},tpad=stop_mode=clone:stop_duration=5",
         "-frames:v", str(n), "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", str(out)])
    got = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                   "stream=nb_read_frames", "-of", "csv=p=0", str(out)]).stdout.strip())
    assert got == n, (stem, got, n)
    return out, n


def assemble(names, out_name):
    total = TIM["total"]
    parts, frames = [], 0
    for ch, stem, cls in SCENES:
        if ch in names:
            p, n = normalise(ch, stem, cls); parts.append(p); frames += n
    lst = B / "concat.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
    t0 = next(c for c in CHAPTERS if c["name"] == names[0])["t0"]
    t1 = next(c for c in CHAPTERS if c["name"] == names[-1])["t1"]
    (B / "overlay.ass").write_text(ass(t0, t1, total))
    out = HERE / "out" / out_name; out.parent.mkdir(exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-ss", f"{t0:.3f}", "-t", f"{frames / FPS:.3f}", "-i", str(HERE / "audio" / "voiceover.wav"),
         "-vf", f"ass={B / 'overlay.ass'}", "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(out)])
    print(out, f"{frames} frames = {frames / FPS:.2f}s")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "srt":
        srt()
    elif mode == "sample":
        assemble(["Two Towns", "Welcome", "Why It Matters"], "sample.mp4")
    else:
        srt(); assemble([s[0] for s in SCENES], "mean_vs_median.mp4")
