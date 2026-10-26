#!/usr/bin/env python3
"""Render Day 02 (Day 01's renderer, on the v3 engine).

  python3 build/render.py stills 3.5 12 40            # PNG frames into $STILLS (default /tmp)
  python3 build/render.py video s01 s08 out/sample.mp4 # segments s01..s08 incl. the trailing pause
"""
import json, os, subprocess, sys, tempfile
from multiprocessing import Pool
import skia

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
import scenes

FADE, CREDITS = 1.0, 6.0
_ctx = {}


def setup():
    if _ctx:
        return _ctx
    tl = E.Timeline()
    assets = scenes.Assets()
    stations, cam, overlays = scenes.build(tl, assets)
    paper = E.to_skia(E.make_paper(1024))
    _ctx.update(tl=tl, stations=stations, cam=cam, overlays=overlays, paper=paper, cues=E.cues(tl),
                credits=credit_lines(), surface=skia.Surface(E.W, E.H))
    return _ctx


def frame(t):
    x = setup()
    tl, cam = x["tl"], x["cam"]
    ta = tl.anim_time(t)  # stopped in structural silences and still beats
    s = x["surface"]
    c = s.getCanvas()
    end = tl.total
    if t >= end + FADE:
        credits_card(c, x["credits"])
        return s.makeImageSnapshot().toarray()
    sh = x["paper"].makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, E.SAMPLING)
    c.drawPaint(skia.Paint(Shader=sh))
    cx, cy, z = cam.at(ta)
    c.save()
    c.concat(cam.matrix(ta))
    hw, hh = E.W / 2 / z, E.H / 2 / z
    for stn in x["stations"]:
        sw, shh = E.W * stn.s / 2, E.H * stn.s / 2
        if abs(stn.x - cx) < hw + sw + 60 and abs(stn.y - cy) < hh + shh + 60:
            stn.render(c, ta, t, z)
    c.restore()
    for t0, t1, draw in x["overlays"]:
        if t0 <= t < t1:
            draw(c, t - t0)
    if t >= end:  # the last line's silence ends here: fade to black before the credits card
        c.drawRect(skia.Rect.MakeWH(E.W, E.H), E.fill((0, 0, 0), (t - end) / FADE))
        return s.makeImageSnapshot().toarray()
    for q in x["cues"]:
        if q["start"] <= t < q["end"]:
            E.draw_subtitle(c, q, t)
    return s.makeImageSnapshot().toarray()  # BGRA


def credit_lines():
    """Spec 8: one line per photo used, grouped by licence."""
    photos = json.load(open(os.path.join(E.DAY, "build.json")))["photos"]
    groups = {}
    for p in photos.values():
        groups.setdefault(p["licence"], []).append(p)
    order = sorted(groups, key=lambda k: (not k.startswith("CC"), k))
    return [(lic, [(p["title"], p["author"]) for p in groups[lic]]) for lic in order]


def credits_card(c, groups):
    c.drawRect(skia.Rect.MakeWH(E.W, E.H), E.fill(E.INK))
    E.text(c, "PHOTOGRAPHS", E.W / 2, 100, E.head_font(34), E.CREAM, 1, "center", 6)
    y = 170
    ft, fl = E.body_font(24), E.head_font(22)
    for lic, rows in groups:
        E.text(c, lic.upper(), 230, y, fl, E.MUSTARD, 1, "left", 3)
        y += 36
        for title, author in rows:
            E.text(c, title, 290, y, ft, E.CREAM, 0.95)
            E.text(c, author, 1690, y, ft, (0.78, 0.76, 0.68), 1, "right")
            y += 34
        y += 16
    E.text(c, "All photographs via Wikimedia Commons. Illustrations and animation are AI-generated and are not photographs.",
           E.W / 2, E.H - 74, E.body_font(21), (0.78, 0.76, 0.68), 1, "center")
    E.text(c, "Narration: synthetic voice.", E.W / 2, E.H - 44, E.body_font(21), (0.78, 0.76, 0.68), 1, "center")


def render_chunk(args):
    f0, f1, path = args
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                          "-s", f"{E.W}x{E.H}", "-r", str(E.FPS), "-i", "-", "-c:v", "libx264",
                          "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(frame(f / E.FPS).tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError(f"ffmpeg failed on {path}")
    return path


def video(sid0, sid1, out, workers=4):
    tl = setup()["tl"]
    t0, t1 = tl.start(sid0), tl.next_start(sid1)
    if sid1 == tl.order[-1]:
        t1 = tl.total + FADE + CREDITS
    f0, f1 = int(round(t0 * E.FPS)), int(round(t1 * E.FPS))
    tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(out)))
    step = (f1 - f0 + workers * 4 - 1) // (workers * 4)
    jobs = [(a, min(a + step, f1), os.path.join(tmp, f"c{i:03}.mp4")) for i, a in enumerate(range(f0, f1, step))]
    with Pool(workers) as pool:
        parts = pool.map(render_chunk, jobs)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    master = os.path.join(E.DAY, "audio", "master.wav")
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                           "-ss", f"{t0}", "-t", f"{t1 - t0}", "-i", master,
                           "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                           "-af", "aresample=48000,apad", "-ac", "2", "-ar", "48000",
                           "-c:a", "aac", "-b:a", "256k", "-shortest", out])
    E.write_srt([q for q in setup()["cues"] if t0 <= q["start"] < t1], os.path.splitext(out)[0] + ".srt", t0)
    for p in parts + [lst]:
        os.remove(p)
    os.rmdir(tmp)
    print(f"{out}: {t1 - t0:.2f}s")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] == "stills":
        outdir = os.environ.get("STILLS", "/tmp")
        from PIL import Image
        for t in map(float, args[1:]):
            a = frame(t)
            Image.fromarray(a[..., [2, 1, 0]]).save(os.path.join(outdir, f"f_{t:07.2f}.png"))
            print("still", t)
    elif args[0] == "video":
        video(args[1], args[2], args[3])
