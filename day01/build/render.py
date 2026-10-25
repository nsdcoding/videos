#!/usr/bin/env python3
"""Render Day 01.

  python3 build/render.py stills 0.5 12 40 --preview      # PNG frames for checking (placeholders allowed)
  python3 build/render.py video s01 s09 out/sample.mp4    # segments s01..s09 incl. trailing pause
"""
import os, subprocess, sys, tempfile
from multiprocessing import Pool
import numpy as np
import skia

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
import scenes

PREVIEW = "--preview" in sys.argv
_ctx = {}


def setup():
    if _ctx:
        return _ctx
    tl = E.Timeline()
    assets = scenes.Assets(PREVIEW)
    # map plate feathered into the paper; paper colour sampled from the map's own margins
    a = E.load_rgba(scenes.find_image("s02", "generated"), (2560, 1440)).copy()
    border = np.median(a[500:900, 150:600, :3].reshape(-1, 3), 0) / 255  # open sea, clear of the map's corners
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.minimum.reduce([xx, w - 1 - xx, yy, h - 1 - yy]).astype(float)
    a[..., 3] = (np.clip(d / 420, 0, 1) ** 1.6 * 255).astype(np.uint8)
    assets.cache["s02"] = (E.to_skia(a), tuple(border), None)
    paper = E.to_skia(E.make_paper(1024, base=tuple(border)))
    stations, cam, overlays, no_subs = scenes.build(tl, assets)
    _ctx.update(tl=tl, stations=stations, cam=cam, overlays=overlays, no_subs=no_subs,
                paper=paper, cues=E.cues(tl), surface=skia.Surface(E.W, E.H))
    return _ctx


def frame(t):
    x = setup()
    tl, cam = x["tl"], x["cam"]
    ta = tl.anim_time(t)  # frozen inside structural silences
    s = x["surface"]
    c = s.getCanvas()
    c.save()
    c.concat(cam.matrix(ta))
    sh = x["paper"].makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, E.SAMPLING)
    c.drawPaint(skia.Paint(Shader=sh))
    for stn in x["stations"]:
        stn.render(c, ta)
    c.restore()
    x["overlays"](c, t, ta)
    if not any(a <= t < b for a, b in x["no_subs"]):
        for q in x["cues"]:
            if q["start"] <= t < q["end"]:
                E.draw_subtitle(c, q, t)
    return s.makeImageSnapshot().toarray()  # BGRA


def render_chunk(args):
    f0, f1, path = args
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                          "-s", f"{E.W}x{E.H}", "-r", str(E.FPS), "-i", "-", "-c:v", "libx264",
                          "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", path],
                         stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(frame(f / E.FPS).tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError(f"ffmpeg failed on {path}")
    return path


def video(sid0, sid1, out, workers=4, tail=0.0):
    tl = setup()["tl"]
    t0, t1 = tl.start(sid0), tl.next_start(sid1) + tail
    f0, f1 = int(round(t0 * E.FPS)), int(round(t1 * E.FPS))
    tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(out)))
    step = (f1 - f0 + workers - 1) // workers
    jobs = [(a, min(a + step, f1), os.path.join(tmp, f"c{i:02}.mp4")) for i, a in enumerate(range(f0, f1, step))]
    with Pool(workers) as pool:
        parts = pool.map(render_chunk, jobs)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    master = os.path.join(E.DAY, "audio", "master.wav")
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                           "-ss", f"{t0}", "-t", f"{t1 - t0}", "-i", master,
                           "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                           "-af", "alimiter=limit=0.83:level=false,aresample=48000", "-ac", "2",
                           "-c:a", "aac", "-b:a", "256k", "-shortest", out])
    E.write_srt([q for q in setup()["cues"] if t0 <= q["start"] < t1], os.path.splitext(out)[0] + ".srt", t0)
    for p in parts + [lst]:
        os.remove(p)
    os.rmdir(tmp)
    print(f"{out}: {t1 - t0:.2f}s")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args[0] == "stills":
        outdir = os.environ.get("STILLS", "/tmp")
        from PIL import Image
        for t in map(float, args[1:]):
            a = frame(t)
            Image.fromarray(a[..., [2, 1, 0]]).save(os.path.join(outdir, f"f_{t:07.2f}.png"))
            print("still", t)
    elif args[0] == "video":
        if PREVIEW:
            sys.exit("video render needs every real archival file; --preview is for stills only")
        video(args[1], args[2], args[3])
