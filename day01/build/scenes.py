"""Day 01 world: station layout, camera path and graphic beats.

Each archival photo sits in the world as a mounted print with a graphic panel beside it; the
photo itself is never cropped, tinted or drawn over. Generated stills are prints the graphics
may sit on. The camera travels between stations; `transition: cut` shots jump.
"""
import json, math, os
import numpy as np
import skia
from engine import *  # noqa: F401,F403
from engine import DAY

SHOTS = json.load(open(os.path.join(DAY, "build.json")))["shots"]
SHOT = {s["segments"][0]: s for s in SHOTS}


def find_image(sid, kind):
    for ext in (".jpg", ".jpeg", ".png"):
        p = os.path.join(DAY, "images", f"{sid}_{kind}{ext}")
        if os.path.exists(p):
            return p
    return None


class Assets:
    def __init__(self, preview=False):
        self.preview = preview
        self.cache = {}

    def generated(self, sid):
        """Generated still, upscaled to 2560x1440 for headroom (spec 3)."""
        if sid not in self.cache:
            a = load_rgba(find_image(sid, "generated"), (2560, 1440))
            self.cache[sid] = (to_skia(a), mean_tone(a), dark_tone(a))
        return self.cache[sid]

    def archival(self, sid):
        if sid not in self.cache:
            p = find_image(sid, "archival")
            if p is None:
                if not self.preview:
                    raise SystemExit(f"STOP: archival image for {sid} is missing (BUILD_SPEC 7)")
                a = np.full((900, 1200, 4), 120, np.uint8)  # preview-only stand-in, never rendered to out/
                a[..., 3] = 255
                self.cache[sid] = (to_skia(a), (0.3, 0.3, 0.3), True)
            else:
                from PIL import Image
                im = Image.open(p)
                if im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info:
                    # transparent scans sit on white paper; the image content is untouched
                    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
                    bg.alpha_composite(im.convert("RGBA"))
                    im = bg
                im = im.convert("RGBA")
                if max(im.size) > 2600:  # resampling only, for render memory
                    im.thumbnail((2600, 2600), Image.LANCZOS)
                a = np.asarray(im)
                self.cache[sid] = (to_skia(a), dark_tone(a), False)
        return self.cache[sid]


def pill(s, x, y, size=22, rgb=INK, bg=PAPER_LIGHT, align="left", dur=0.45, tracking=2.5, bga=0.88):
    """Small-caps label on a paper chip, for text over busy imagery."""
    f = sans("SemiBold", size)
    w = text_width(s, f, tracking)
    x0 = x - (w if align == "right" else w / 2 if align == "center" else 0)

    def draw(c, age):
        p = out_cubic(age / dur)
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 - 12, y - size - 4 + 6 * (1 - p), w + 24, size + 16), 5, 5)
        c.drawRRect(r, fill(bg, bga * p))
        text(c, s, x0, y + 6 * (1 - p), f, rgb, p, "left", tracking)
    return draw


def walker(path, t_go, t_stop, stop_at=1.0, r=9):
    """The red dot (him) travelling along a path, then resting where it stopped."""
    def draw(c, age):
        p = smooth(age / max(t_stop - t_go, 1e-3)) * stop_at
        c.drawPath(partial(path, p), dashed(stroke(RED, 2.5, 0.85), 4, 7))
        x, y = point_on(path, p)
        c.drawCircle(x, y, r, fill(RED))
    return draw


def layout(img, panel_w=520, max_w=1250, top=80, max_h=760, gap=60):
    """Photo plus its graphic panel, centred as one composition. Returns (photo rect, panel x)."""
    k = min(max_w / img.width(), max_h / img.height())
    dw, dh = img.width() * k, img.height() * k
    x0 = (W - (dw + gap + panel_w)) / 2
    return (x0, top + (max_h - dh) / 2, dw, dh), x0 + dw + gap


def build(tl, assets):
    at, st, en, nx = tl.at, tl.start, tl.end, tl.next_start
    stations = []

    def S(*a):
        s = Station(*a)
        stations.append(s)
        return s

    # ---------------------------------------------------------- the map: the world's centre
    MAP = S("map", 0, 0, 1.6)
    H_ = (747.6, 693.7)   # Hiroshima, map-local
    N_ = (645.3, 787.5)   # Nagasaki, map-local
    mimg = assets.generated("s02")[0]
    MAP.add(-99, print_plate(mimg, (0, 0, W, H), feather=True))

    # s01 print, nested in the open sea west of Hiroshima so the opening pull-back reveals the map
    P1_local = (300, 540)
    P1 = S("s01", *MAP.to_world(*P1_local), 1.6 * 0.15)

    # ---------------------------------------------------------- s01: the seal
    img, matte, _ = assets.archival("s01")
    region, px = layout(img)
    P1.add(-99, print_photo(img, region, matte))
    P1.add(0.35, label("TSUTOMU YAMAGUCHI", px, 300, 30, tracking=4))
    P1.add(0.9, line_on(poly([(px, 330), (px + 400, 330)]), GREY, 2, 0.7))
    P1.add(1.5, serif_label("1916 – 2010", px, 392, 44, GREY))
    t = at("s01", "officially recognised")
    P1.add(t - 0.1, seal(px + 46, 520, 42))
    P1.add(t + 0.2, label("OFFICIALLY", px + 110, 512, 22, GREY))
    P1.add(t + 0.35, label("RECOGNISED", px + 110, 542, 22, GREY))
    t = at("s01", "both atomic bombs")
    for i, nm in enumerate(("HIROSHIMA", "NAGASAKI")):
        yy = 660 + i * 78
        P1.add(t + i * 0.55, ring_on(px + 22, yy - 9, 20, INK, 2.5, 0.5))
        P1.add(t + i * 0.55 + 0.15, dot(px + 22, yy - 9, 6, INK))
        P1.add(t + i * 0.55 + 0.1, label(nm, px + 60, yy, 24, tracking=3))
    P1.add(t + 1.3, label("× 2", px + 300, 715, 64, RED, "Light", 0))

    # ---------------------------------------------------------- s02: on the map
    p1_edge = (P1_local[0] + W * 0.15 / 2, P1_local[1])
    MAP.add(7.5, line_on(curve(p1_edge, H_, -0.22), RED, 2.5, 1.1, 0.9, (6, 7)))
    t = st("s02")
    MAP.add(t - 0.2, pulse(*H_, 6, 70))
    MAP.add(t - 0.2, dot(*H_, 7))
    MAP.add(t, pill("HIROSHIMA", H_[0] + 26, H_[1] + 52, 20))
    MAP.add(at("s02", "Not nearby"), serif_label("Not nearby.", 1300, 690, 46, GREY, "Italic"))
    MAP.add(at("s02", "Not in the next"), serif_label("Not in the next town.", 1300, 750, 46, GREY, "Italic"))
    t = at("s02", "Three kilometres")
    MAP.add(t - 0.2, loupe(560, 250, 150, H_, (0.33, 0.66, 1.0), 0.35))
    MAP.add(at("s02", "sixth of August"), pill("6 AUG 1945", 560, 455, 22, align="center"))
    t = at("s02", "and three kilometres")
    MAP.add(t - 0.3, line_on(curve(H_, N_, 0.35), RED, 2.5, 1.0, 0.9, (6, 7)))
    MAP.add(t + 0.6, pulse(*N_, 6, 70))
    MAP.add(t + 0.6, dot(*N_, 7))
    MAP.add(t + 0.7, pill("NAGASAKI", N_[0] - 30, N_[1] + 56, 20, align="right"))
    MAP.add(t + 1.0, loupe(1000, 850, 110, N_, (0.33, 0.66, 1.0), 0.35))
    t = at("s02", "three days later")
    tlx0, tlx1, tly = 1350, 1760, 905
    MAP.add(t - 0.6, line_on(poly([(tlx0, tly), (tlx1, tly)]), INK, 2.5, 0.6))
    MAP.add(t - 0.4, dot(tlx0, tly, 8, INK))
    MAP.add(t - 0.3, label("6 AUG", tlx0, tly + 40, 20, GREY, align="center"))
    MAP.add(t + 0.1, line_on(curve((tlx0, tly - 16), (tlx1, tly - 16), -0.25), RED, 2.5, 0.7))
    MAP.add(t + 0.7, dot(tlx1, tly, 8, RED))
    MAP.add(t + 0.7, label("9 AUG", tlx1, tly + 40, 20, GREY, align="center"))
    MAP.add(t + 0.5, label("+3 DAYS", (tlx0 + tlx1) / 2, tly - 86, 24, RED, align="center"))

    # ---------------------------------------------------------- s03: the drafting desk
    D = S("s03", 3550, -250, 1.0)
    D.add(-99, print_plate(assets.generated("s03")[0], (0, 0, W, H)))
    t = at("s03", "not a soldier")
    D.add(t, icon("helmet", 180, 200, 1.0, OFFWHITE, 3.5))
    D.add(t + 0.2, pill("SOLDIER", 245, 214, 22, bga=0.8))
    D.add(t + 0.8, cross(180, 196, 34))
    t = at("s03", "or a scientist")
    D.add(t, icon("flask", 180, 360, 1.0, OFFWHITE, 3.5))
    D.add(t + 0.2, pill("SCIENTIST", 245, 374, 22, bga=0.8))
    D.add(t + 0.7, cross(180, 360, 34))
    t = at("s03", "twenty-nine")
    D.add(t - 0.2, counter(0, 29, 1520, 330, 150, 1.4, rgb=OFFWHITE, align="right"))
    D.add(t + 0.4, pill("YEARS OLD", 1545, 290, 22, bga=0.8))
    D.add(at("s03", "engineer"), pill("ENGINEER", 1545, 330, 22, bga=0.8))
    t = at("s03", "designed oil tankers")
    D.add(t, icon("ship", 1660, 520, 1.1, OFFWHITE, 3, 1.1))
    D.add(t + 0.5, pill("OIL TANKERS", 1660, 600, 20, align="center", bga=0.8))
    t = at("s03", "morning of the sixth")
    D.add(t, pill("6 AUG 1945 · MORNING", 1580, 860, 22, align="center", bga=0.85))
    t = at("s03", "a stamp")
    D.add(t - 0.15, seal(1120, 860, 62))

    # ---------------------------------------------------------- s04: the tram he was walking to
    T = S("s04", 3550, 1150, 1.0)
    img, matte, _ = assets.archival("s04")
    region, px = layout(img)
    T.add(-99, print_photo(img, region, matte))
    t = at("s04", "three months")
    T.add(t - 0.1, counter(0, 3, px, 210, 110, 0.9))
    T.add(t + 0.2, label("MONTHS", px + 80, 205, 26, tracking=4))
    T.add(t + 0.3, label("IN HIROSHIMA", px + 80, 170, 18, GREY, tracking=3))
    T.add(at("s04", "business trip"), label("MITSUBISHI BUSINESS TRIP", px, 250, 18, GREY, tracking=2.5))
    t = at("s04", "That morning")
    T.add(t, icon("calendar", px + 36, 330, 0.8, INK, 2.5))
    T.add(t + 0.3, label("6 AUG 1945", px + 90, 330, 24, tracking=3))
    T.add(t + 0.5, label("THE LAST MORNING", px + 90, 362, 18, GREY, tracking=2.5))
    # office -> tram: the walk that stops
    t = at("s04", "walking to the tram")
    ox, tx, wy = px + 34, px + 420, 470
    T.add(t - 0.2, icon("office", ox, wy - 6, 0.7, INK, 2.5))
    T.add(t + 0.1, icon("tram", tx, wy, 0.7, INK, 2.5))
    walk = poly([(ox + 36, wy + 30), (tx - 40, wy + 30)])
    t_real = at("s04", "realised he had left")
    T.add(t + 0.4, walker(walk, 0, t_real - t - 0.4, 0.72))
    T.add(at("s04", "with his bags"), icon("bag", px + 250, wy - 34, 0.45, GREY, 2.2))
    T.add(t_real + 0.1, label("?", px + 300, wy - 8, 44, RED, "Bold", 0))
    T.add(t_real + 0.3, pulse(ox, wy - 6, 6, 52))
    T.add(at("s04", "personal seal"), seal(ox, wy - 6, 18))
    T.add(at("s04", "at the office"), label("SEAL LEFT AT THE OFFICE", px, wy + 82, 18, RED, tracking=2.5))
    t = at("s04", "served as a man")
    T.add(t - 0.6, seal(px + 40, 650, 30))
    T.add(t - 0.1, label("=", px + 100, 664, 44, GREY, "Light", 0))
    sig = skia.Path()
    sig.moveTo(px + 150, 660)
    for i in range(6):
        sig.cubicTo(px + 165 + i * 34, 620, px + 175 + i * 34, 690, px + 190 + i * 34, 650)
    T.add(t + 0.1, line_on(sig, INK, 2.5, 0.9))
    T.add(t + 0.6, label("A SIGNATURE", px + 150, 712, 18, GREY, tracking=2.5))
    t = at("s04", "no travel papers")
    T.add(t - 0.4, icon("doc", px + 34, 806, 0.75, INK, 2.5))
    T.add(t - 0.1, label("TRAVEL PAPERS", px + 90, 812, 24, tracking=3))
    T.add(at("s04", "were valid"), strike(px + 84, px + 90 + text_width("TRAVEL PAPERS", sans("SemiBold", 24), 3) + 6, 804))
    t = at("s04", "He could not get home")
    T.add(t, icon("house", px + 34, 918, 0.75, INK, 2.5))
    T.add(t + 0.2, line_on(poly([(px + 84, 920), (px + 400, 920)]), INK, 2, 0.8, dash=(8, 8)))
    T.add(t + 0.9, cross(px + 242, 920, 16, RED, 3.5))
    T.add(t + 0.4, label("HOME", px + 360, 900, 18, GREY, tracking=2.5, align="right"))

    # ---------------------------------------------------------- s05: hard cut, the second seal
    H3 = S("s05", 3550, 2350, 0.55)
    img, matte, _ = assets.archival("s05")
    region, px = layout(img)
    H3.add(-99, print_photo(img, region, matte))
    t = st("s05")
    u = skia.Path()
    u.moveTo(px, 380)
    u.lineTo(px + 300, 380)
    u.cubicTo(px + 470, 380, px + 470, 640, px + 300, 640)
    u.lineTo(px + 30, 640)
    H3.add(t + 0.1, line_on(u, INK, 3, 1.8, dash=(10, 9)))
    H3.add(t + 0.1, walker(u, 0, 2.2, 1.0, 11))
    H3.add(t + 1.9, label("TURNED BACK", px, 730, 26, RED, tracking=4))

    # ---------------------------------------------------------- s06: the field
    F = S("s06", 1700, 2760, 1.25)
    F.add(-99, print_plate(assets.generated("s06")[0], (0, 0, W, H)))
    t = st("s06")
    F.add(t + 0.2, line_on(poly([(620, 640), (620, 860)]), RED, 2.5, 0.5))
    F.add(t + 0.5, dot(620, 870, 11))
    F.add(t + 0.5, pulse(620, 870, 8, 80))
    F.add(at("s06", "a field"), pill("A FIELD", 650, 650, 22))
    F.add(at("s06", "edge of the city"), pill("ON THE EDGE OF THE CITY", 650, 694, 18, GREY))
    t = at("s06", "fifteen minutes")

    def clock(c, age, cx=1660, cy=200, r=70):
        p = smooth(age / 1.6)
        c.drawCircle(cx, cy, r, fill(PAPER_LIGHT, 0.85 * min(1, age / 0.3)))
        c.drawPath(partial(arc_path(cx, cy, r), smooth(age / 0.5)), stroke(INK, 3))
        for k in range(12):
            a = math.radians(k * 30)
            c.drawLine(cx + math.sin(a) * r * 0.82, cy - math.cos(a) * r * 0.82,
                       cx + math.sin(a) * r * 0.92, cy - math.cos(a) * r * 0.92, stroke(INK, 2, min(1, age / 0.4)))
        mins = 15 * p
        am = math.radians(mins * 6)
        ah = math.radians((8 + mins / 60) * 30)
        c.drawLine(cx, cy, cx + math.sin(ah) * r * 0.5, cy - math.cos(ah) * r * 0.5, stroke(INK, 5))
        c.drawLine(cx, cy, cx + math.sin(am) * r * 0.78, cy - math.cos(am) * r * 0.78, stroke(RED, 3))
        c.drawCircle(cx, cy, 5, fill(INK))
        text(c, f"08:{int(round(mins)):02d}", cx, cy + r + 50, sans("Light", 40), INK, min(1, age / 0.3), "center")
    F.add(t - 0.3, clock)
    t = at("s06", "instead of on a tram")
    city = (1260, 560)
    F.add(t, line_on(poly([(760, 900), city]), INK, 2.5, 1.0, 0.8, (8, 8)))
    F.add(t + 0.3, icon("tram", 1080, 700, 0.6, INK, 2.5))
    F.add(t + 0.5, pill("THE TRAM INTO THE CENTRE", 1130, 790, 18))
    F.add(at("s06", "into the centre") + 0.3, cross(1080, 700, 22))

    # ---------------------------------------------------------- s07: the sky above the field
    B = S("s07", 1700, 1420, 1.0)
    img, matte, _ = assets.archival("s07")
    region, px = layout(img)
    B.add(-99, print_photo(img, region, matte))
    t = at("s07", "aircraft first")
    fly = poly([(px - 20, 210), (px + 440, 160)])

    def plane(c, age, path=fly):
        p = smooth(age / 2.2)
        c.drawPath(partial(path, p), dashed(stroke(GREY, 2, 0.8), 3, 9))
        x, y = point_on(path, p)
        c.save()
        c.translate(x, y)
        c.rotate(-6)
        icon("plane", 0, 0, 0.7, INK, 3, 0.01)(c, 1)
        c.restore()
    B.add(t - 0.2, plane)
    t = at("s07", "A single bomber")
    B.add(t - 0.1, counter(0, 1, px, 400, 120, 0.5))
    B.add(t + 0.2, label("AIRCRAFT", px + 90, 392, 26, tracking=4))
    t = at("s07", "very high up")
    B.add(t - 0.2, line_on(poly([(px + 20, 760), (px + 20, 470)]), INK, 2.5, 0.8))
    B.add(t + 0.5, line_on(poly([(px + 6, 486), (px + 20, 468), (px + 34, 486)]), INK, 2.5, 0.3))
    B.add(t + 0.3, label("VERY HIGH UP", px + 50, 520, 22, GREY, tracking=3))
    t = at("s07", "something small")
    drop = poly([(px + 430, 176), (px + 430, 900)])
    B.add(t - 0.1, line_on(drop, GREY, 2, nx("s07") - t - 0.2, 0.7, (3, 9), ease=lambda x: clamp01(x) ** 1.6))
    B.add(t - 0.1, lambda c, age, d=drop, dur=nx("s07") - t - 0.2:
          c.drawCircle(*point_on(d, clamp01(age / dur) ** 1.6), 7, fill(INK)))

    # ---------------------------------------------------------- s08 / s36: the white (one station, revisited)
    WHITE = S("white", -4300, 2900, 1.0)
    WHITE.add(-99, print_plate(assets.generated("s08")[0], (0, 0, W, H), shadow=False))

    # ---------------------------------------------------------- s09: title card on the white's own tone
    TITLE = S("s09", -4300, 4250, 1.0)
    title_bg = assets.generated("s08")[1]
    title = json.load(open(os.path.join(DAY, "build.json")))["title"]
    TITLE.add(-99, lambda c, age: c.drawRect(skia.Rect.MakeWH(W, H), fill(title_bg)))
    words = title.split()
    a0 = st("s09")
    for li, line in enumerate([" ".join(words[:3]), " ".join(words[3:])]):
        TITLE.add(a0 + 0.1 + li * 0.45, serif_label(line, W / 2, 430 + li * 100, 76, INK, align="center", dur=0.9, rise=14))
    TITLE.add(a0 + 1.1, line_on(poly([(W / 2 - 260, 600), (W / 2 + 260, 600)]), RED, 3, 0.8))
    tt = at("s09", "Three days later")
    TITLE.add(tt + 0.2, label("6 AUG 1945", W / 2 - 180, 680, 24, GREY, align="center", tracking=3, dur=0.6))
    TITLE.add(tt + 0.5, line_on(poly([(W / 2 - 60, 672), (W / 2 + 60, 672)]), RED, 2.5, 0.7))
    TITLE.add(tt + 1.1, line_on(poly([(W / 2 + 48, 664), (W / 2 + 60, 672), (W / 2 + 48, 680)]), RED, 2.5, 0.2))
    TITLE.add(tt + 1.1, label("9 AUG 1945", W / 2 + 180, 680, 24, GREY, align="center", tracking=3, dur=0.6))
    TITLE.add(at("s09", "four hundred"), label("400 KM", W / 2, 740, 22, RED, align="center", tracking=4, dur=0.6))

    plan = [  # (station, shot id, move-in window (a, b), "cut", or None for automatic)
        (P1, "s01", None),
        (MAP, "s02", (7.45, 9.05)),
        (D, "s03", (19.8, 21.2)),
        (T, "s04", (at("s03", "a stamp") + 0.15, st("s04"))),
        (H3, "s05", "cut"),
        (F, "s06", (en("s05") + 0.05, st("s06") + 0.55)),
        (B, "s07", (en("s06") - 0.7, st("s07"))),
        (WHITE, "s08", "cut"),
        (TITLE, "s09", "cut"),
    ]
    import scenes2
    ctx = dict(S=S, MAP=MAP, P1=P1, WHITE=WHITE, P1_local=P1_local, H_=H_, N_=N_)
    plan += scenes2.build(tl, assets, ctx)
    cam = make_camera(tl, plan)
    no_subs = [(st("s08"), st("s09")), (st("s36"), st("s37"))]  # nothing on screen but white
    return stations, cam, no_subs


def make_camera(tl, plan):
    """Holds per shot (spec motion over the shot's full duration) and the moves between them.

    Automatic windows: arrive just before the next line; never start moving an archival photo
    before its narration ends; after a structural silence the move starts when the voice does."""
    st, en = tl.start, tl.end
    cam = Camera()
    sids = [p[1] for p in plan]
    for i, (stn, sid, mv) in enumerate(plan):
        sh = SHOT[sid]
        t0 = st(sid)
        t1 = st(sids[i + 1]) if i + 1 < len(sids) else tl.total
        motion = "still" if sid in ("s08", "s36", "s09") else sh["motion"]
        cam.holds.append([None, None, cam.framing(stn, motion, t0, t1, sh["type"] == "archival")])
        if i == 0:
            continue
        if mv == "cut" or SHOT[sid].get("transition") == "cut":
            cam.moves.append((t0, t0))
            continue
        if mv is None:
            prev = SHOT[sids[i - 1]]
            last = prev["segments"][-1]
            end_audio, pause = en(last), tl.segs[last]["pause_after"]
            prev_arch, next_arch = prev["type"] == "archival", sh["type"] == "archival"
            if pause >= 2000:
                a = t0
                b = a + 1.5
            else:
                D = 1.6
                b = t0 + (0.0 if next_arch else 0.35)
                a = b - D
                lo = end_audio + 0.05 if prev_arch else end_audio - 0.8
                if a < lo:
                    a = lo
                    b = max(b, a + 1.1)
            mv = (a, b)
        cam.moves.append(mv)
    for i, h in enumerate(cam.holds):
        h[0] = cam.moves[i - 1][1] if i else -1e9
        h[1] = cam.moves[i][0] if i < len(cam.moves) else 1e9
    cam.holds = [tuple(h) for h in cam.holds]
    return cam
