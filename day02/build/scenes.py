"""Day 02 scenes: one world, beat by beat (build.json v3 beats, in order).

World layout (world pixels; each station is a 1920x1080 place):
  the Philippines, lower left: the island seen from the air; the jungle places nest inside the island,
  so walking into the jungle is a dive into the plate.
  Japan, upper right and far away: the village, the classroom, the bookshop, Tokyo.
Every beat records the camera keys that frame it; transitions are camera moves unless the beat says cut.
"""
import json, math, os
import skia
from engine import *  # noqa: F401,F403

BUILD = json.load(open(os.path.join(DAY, "build.json")))
CJK = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"


class Assets:
    def __init__(self):
        self.cache = {}

    def _get(self, key, fn):
        if key not in self.cache:
            self.cache[key] = fn()
        return self.cache[key]

    def plate(self, sid):
        return self._get(("set", sid), lambda: to_skia(load_rgba(os.path.join(DAY, "images", "raw", f"set_{sid}.png"),
                                                                    (W + 48, H + 28))))

    def prop(self, pid):
        if pid not in BUILD["props"]:
            raise SystemExit(f"STOP: prop {pid} is not declared in build.json")  # spec 9
        return self._get(("prop", pid), lambda: to_skia(load_rgba(os.path.join(DAY, "images", "props", f"{pid}.png"))))

    def rig(self, cid, pose):
        if pose not in BUILD["cast"][cid]["poses"]:
            raise SystemExit(f"STOP: pose {cid}/{pose} is not declared in build.json")  # spec 9
        return self._get(("rig", cid, pose), lambda: Rig(os.path.join(DAY, "images", "cast", f"{cid}_{pose}")))

    def photo(self, pid):
        meta = BUILD["photos"][pid]
        if not all(meta.get(k) for k in ("author", "licence", "page_url")):
            raise SystemExit(f"STOP: photo {pid} is missing credit fields")  # spec 9
        import urllib.parse
        name = urllib.parse.unquote(meta["file_url"].rsplit("/", 1)[1])
        return self._get(("photo", pid), lambda: Photo(pid, meta, os.path.join(DAY, "archival", name)))


def build(tl, A):
    at, st, en, nx = tl.at, tl.start, tl.end, tl.next_start
    cam = Camera()
    stations = []
    overlays = []  # screen-space layers on real time: (t0, t1, draw(c, age))

    def S(name, x, y, s=1.0, plate_id=None, reveal=None):
        stn = Station(name, x, y, s, reveal)
        if plate_id:
            stn.add(-999, plate(A.plate(plate_id)))
        stations.append(stn)
        return stn

    # ------------------------------------------------------------ the world
    ISL = S("island_sea", 0, 0, 1.0, "island_sea")
    k_in = 0.075  # jungle places nested in the island
    CLR = S("jungle_clearing", *ISL.world(860, 560), k_in, "jungle_clearing", reveal=(0.18, 0.45))
    DEEP = S("jungle_deep", *ISL.world(860 + W * k_in, 560), k_in, "jungle_deep", reveal=(0.18, 0.45))
    VIL = S("village_1920s", 9200, -5600, 1.0, "village_1920s")
    SHOP = S("bookshop", 9200 + W * 1.06, -5600 + H * 1.1, 1.0, "bookshop")

    # ============================================================ s01: 9 March 1974, the island
    t = 0.0
    ISL.add(0.25, tag("9 MAR 1974", 330, 150, 46, rot=-4, pin=True), until=at("s01", "walked into") + 0.4)
    # the route from Japan (off the top right) to the island, with a small plane along it
    route = curve((1880, 60), (900, 500), -0.18)
    ISL.add(at("s01", "flew from Japan") - 0.3, ink(route, RUST, 7, 1.6, dash=(18, 14)), until=at("s01", "walked into") + 0.3)
    ISL.add(at("s01", "flew from Japan") - 0.35, tag("JAPAN", 1700, 120, 34, bg=MUSTARD), until=at("s01", "walked into") + 0.3)

    def plane(c, age):
        p = in_out(age / 1.6)
        if p <= 0 or p >= 1:
            return
        (x, y), ang = point_on(route, p)
        c.save()
        c.translate(x, y)
        c.rotate(ang)
        pts = [(-26, 0), (26, 0)]
        c.drawLine(*pts[0], *pts[1], stroke(INK, 7))
        c.drawPath(poly([(-4, 0), (-16, -24), (-8, -24), (12, 0), (-8, 24), (-16, 24)], True), fill(INK))
        c.restore()
    ISL.add(at("s01", "flew from Japan") - 0.3, plane)
    ISL.add(at("s01", "to a small island"), tag("LUBANG", 880, 360, 40, rot=3, pin=True), until=at("s01", "walked into") + 0.4)
    p01 = A.photo("p01")
    ISL.add(at("s01", "in the Philippines") - 0.2, photo_card(p01, 1480, 640, 620, "slide_up", hold=4),
            until=at("s01", "walked into") + 0.1, fade=0.3)
    ISL.add(at("s01", "in the Philippines") + 0.3, tag("THE PHILIPPINES", 1480, 300, 32, bg=CREAM, rot=-2),
            until=at("s01", "walked into") + 0.1)
    cam.key(0.0, frame_on(ISL, W / 2, H / 2, 1.0))
    cam.key(at("s01", "walked into") - 0.4, frame_on(ISL, W / 2 + 40, H / 2 + 10, 1.04), "hold")
    # dive into the island: arrive in the clearing just before "read a short statement"
    cam.key(at("s01", "and read") - 0.1, frame_on(CLR, W / 2, H / 2, 1.0))

    # the clearing: Taniguchi walks in with a paper, Onoda stands at attention
    tan_r = A.rig("taniguchi", "read_order")
    ono_att = A.rig("onoda", "attention")
    t_walk = at("s01", "walked into") - 0.2
    CLR.add(t_walk, actor(tan_r, 640, 930, 640, motion=walk(-700, 0, 0.0, 2.4)), until=nx("s02"), fade=0.0)
    CLR.add(-999, actor(ono_att, 1380, 940, 610, flip=True, seed=1.3), until=None)
    CLR.add(at("s01", "and read") + 0.3, tag("A BOOKSELLER, 61", 560, 210, 40, rot=-3, pin=True), until=st("s02") + 0.2)
    CLR.add(at("s01", "a man standing"), tag("A PATCHED UNIFORM", 1390, 200, 40, bg=MUSTARD, rot=3, pin=True),
            until=st("s02") + 0.2)
    CLR.add(at("s01", "in a patched") + 0.2, arrow((1390, 250), (1330, 520), 0.25, RUST, 7, 0.5), until=st("s02") + 0.2)

    # ============================================================ s02: the statement
    cam.key(st("s02") + 0.1, frame_on(CLR, W / 2 + 40, H / 2 + 10, 1.06), "hold")
    cam.key(st("s02") + 1.2, frame_on(CLR, 780, 520, 1.45))
    # Taniguchi's head nods as he reads
    CLR.add(st("s02"), panel((990, 170, 450, 640), CREAM, 0.97), until=nx("s02") - 0.1)
    CLR.add(st("s02") + 0.2, sprite(A.prop("order"), 1080, 255, 120, entry="pop", rot=-6), until=nx("s02") - 0.1)
    CLR.add(st("s02") + 0.5, headline("BY ORDER", 1290, 275, 48, RUST, f=title_font(50)), until=nx("s02") - 0.1)
    items = [("14TH AREA ARMY", "DISSOLVED", at("s02", "Japanese Fourteenth")),
             ("ALL COMBAT", "CEASE", at("s02", "That all combat")),
             ("HE IS", "RELIEVED OF DUTY", at("s02", "That the man"))]
    for i, (a, b, ti) in enumerate(items):
        y = 400 + i * 135
        CLR.add(ti, typewriter(a, 1025, y, 30, INK, 30), until=nx("s02") - 0.1)
        CLR.add(ti + 0.6, headline(b, 1025, y + 48, 38, RUST, "left", rise=12), until=nx("s02") - 0.1)
        CLR.add(ti + 0.9, check(1395, y + 6, 1.0, INK), until=nx("s02") - 0.1)
    CLR.add(at("s02", "dissolved") + 0.1, sprite(A.prop("flag_folded"), 330, 810, 190, entry="drop", rot=8),
            until=nx("s02") - 0.1)

    # ============================================================ s03: the man listening
    cam.key(st("s03") - 0.2, frame_on(CLR, 1180, 540, 1.55))
    cam.key(nx("s03") - 0.2, frame_on(CLR, 1180, 540, 1.58), "hold")
    p02 = A.photo("p02")
    CLR.add(at("s03", "Second Lieutenant") - 0.3, photo_card(p02, 790, 450, 340, "pin", tilt=-2.5, hold=14),
            until=nx("s03") - 0.2)
    CLR.add(at("s03", "Hiroo Onoda") + 0.2, tag("2ND LT HIROO ONODA", 790, 200, 32, rot=-2, pin=True), until=nx("s03") - 0.2)
    CLR.add(at("s03", "He was fifty-one"), panel((1560, 250, 220, 180), INK, 0.92), until=nx("s03") - 0.2)
    CLR.add(at("s03", "He was fifty-one") + 0.1, counter(0, 51, 1670, 395, 110, 1.0, rgb=MUSTARD), until=nx("s03") - 0.2)
    CLR.add(at("s03", "He was fifty-one") + 0.3, headline("AGE", 1670, 292, 30, CREAM, rise=8), until=nx("s03") - 0.2)
    # a timeline: 1945 to 1974, with others then alone
    x0, x1, y = 640, 1170, 760
    yr = lambda v: lerp(x0, x1, (v - 1945) / (1974.2 - 1945))
    CLR.add(at("s03", "He had been fighting") - 0.2, panel((600, 690, 610, 125), CREAM, 0.96), until=nx("s03") - 0.2)
    t_alone = at("s03", "alone")
    t_others = at("s03", "and with others")
    CLR.add(t_alone, ink(poly([(yr(1972.8), y), (yr(1974.2), y)]), RUST, 20, 0.5), until=nx("s03") - 0.2)
    CLR.add(t_alone + 0.3, headline("ALONE: 18 MONTHS", yr(1974.2), y - 24, 22, RUST, "right", rise=8), until=nx("s03") - 0.2)
    CLR.add(t_others, ink(poly([(yr(1972.8), y), (yr(1945), y)]), OLIVE, 20, 1.2), until=nx("s03") - 0.2)
    CLR.add(t_others + 0.8, headline("WITH OTHERS: 27 YEARS BEFORE", yr(1945), y + 44, 22, INK, "left", rise=8),
            until=nx("s03") - 0.2)
    CLR.add(t_others + 0.4, headline("1945", yr(1945), y - 24, 22, OLIVE, "left", rise=6), until=nx("s03") - 0.2)

    # ============================================================ s04: all of it dismissed
    cam.key(st("s04") + 0.2, frame_on(DEEP, W / 2, H / 2, 1.0))
    cam.key(at("s04", "He had dismissed") - 0.2, frame_on(DEEP, W / 2 - 60, H / 2 + 20, 1.05), "hold")
    cam.key(at("s04", "He had dismissed") + 0.6, frame_on(DEEP, 760, 420, 1.25))
    ono_cr = A.rig("onoda", "crouch_watch")
    DEEP.add(st("s04") - 0.5, actor(ono_cr, 1560, 1000, 520, flip=True, seed=0.4,
                                    motion=keys((0, {}), (13.5, {}), (14.0, {"head": -6}), (14.4, {"head": 6}),
                                                (14.8, {"head": -4}), (15.2, {"head": 0}))), until=nx("s05"))
    lines = [("LEAFLETS", at("s04", "He had read leaflets"), 330),
             ("LOUDSPEAKERS", at("s04", "from loudspeakers"), 470),
             ("SEARCH PARTIES", at("s04", "from search parties"), 610),
             ("HIS FAMILY'S VOICES", at("s04", "from his own family"), 750)]
    DEEP.add(at("s04", "He had heard") + 0.1, tag("THE WAR IS OVER", 520, 170, 44, bg=CREAM, rot=-3, pin=True),
             until=nx("s04") - 0.2)
    for i, (s, ti, y) in enumerate(lines):
        DEEP.add(ti, tag(s, 420, y, 38, bg=MUSTARD if i % 2 else CREAM, rot=(-2, 2, -1, 3)[i]), until=nx("s04") - 0.2)
        DEEP.add(at("s04", "He had dismissed") + 0.25 * i, cross(420, y, 30, RUST, 11), until=nx("s04") - 0.2)
    # leaflets flutter down; a loudspeaker on its pole; the search party on the ridge; the plane overhead
    DEEP.add(lines[0][1] - 0.2, sprite(A.prop("leaflets"), 980, 380, 300, path=curve((900, -200), (980, 380), 0.3),
                                       dur=1.2, wobble=3, seed=1), until=nx("s04") - 0.2)
    DEEP.add(lines[1][1] - 0.2, sprite(A.prop("loudspeaker"), 820, 700, 230, entry="rise", wobble=1.0), until=nx("s04") - 0.2)

    def waves(cx, cy, n=3, rgb=RUST, period=1.0):
        def d(c, age):
            for i in range(n):
                p = ((age / period) + i / n) % 1.0
                c.drawPath(arc_path(cx, cy, 30 + 90 * p, -40, 80), stroke(rgb, 6, 1 - p))
        return d
    DEEP.add(lines[1][1] + 0.3, waves(900, 580), until=nx("s04") - 0.2)
    crowd = A.rig("crowd", "search_party")
    DEEP.add(lines[2][1] - 0.4, actor(crowd, 900, 560, 210, motion=walk(-600, 260, 0.0, 6.0, bob=4, swing=0)),
             until=nx("s04") - 0.2)
    plane_path = curve((-300, 170), (2200, 120), 0.04)
    DEEP.add(lines[3][1] - 0.6, sprite(A.prop("plane_speaker"), 0, 0, 340, path=plane_path, dur=5.0), until=nx("s04"))
    DEEP.add(lines[3][1], waves(1100, 230, 3, MUSTARD, 0.8), until=nx("s04") - 0.2)

    # ============================================================ s05 (calm): an order, in person
    cam.key(st("s05") + 0.3, frame_on(DEEP, 760, 470, 1.2))
    cam.key(nx("s05"), frame_on(DEEP, 760, 470, 1.24), "hold")
    DEEP.add(st("s05"), panel((300, 190, 920, 560), CREAM, 0.97), until=nx("s05") + 0.2)
    DEEP.add(st("s05") + 0.3, sprite(A.prop("order"), 520, 460, 300, entry="rise", wobble=1.2), until=nx("s05") + 0.2)
    DEEP.add(at("s05", "An order"), headline("AN ORDER", 900, 380, 64, INK, "left", dur=0.8), until=nx("s05") + 0.2)
    DEEP.add(at("s05", "from the officer"), headline("FROM THE OFFICER", 900, 470, 34, OLIVE, "left", dur=0.8),
             until=nx("s05") + 0.2)
    DEEP.add(at("s05", "from the officer") + 0.4, headline("WHO GAVE THE FIRST", 900, 515, 34, OLIVE, "left", dur=0.8),
             until=nx("s05") + 0.2)
    DEEP.add(at("s05", "delivered in person"), headline("IN PERSON", 900, 640, 64, RUST, "left", dur=0.8),
             until=nx("s05") + 0.2)
    DEEP.add(at("s05", "delivered in person") + 0.5, underline(900, 1190, 665, RUST, 8, 0.6), until=nx("s05") + 0.2)

    # ============================================================ s06: that officer, a bookseller now
    cam.key(st("s06") + 0.35, frame_on(SHOP, W / 2, H / 2, 1.0))
    cam.key(nx("s06") - 0.1, frame_on(SHOP, W / 2 + 80, H / 2 + 20, 1.05), "hold")
    bk = A.rig("taniguchi", "bookseller")
    SHOP.add(st("s06") - 1.0, actor(bk, 760, 960, 650, flip=True, seed=0.9,
                                    motion=keys((0, {}), (3.2, {}), (4.2, {"head": 8, "armR": -6}),
                                                (6, {"head": 8}))))
    SHOP.add(at("s06", "That officer") + 0.1, tag("THAT OFFICER", 520, 200, 40, rot=-3, pin=True), until=nx("s06"))
    SHOP.add(at("s06", "was a bookseller") + 0.1, tag("NOW A BOOKSELLER", 600, 300, 40, bg=MUSTARD, rot=2), until=nx("s06"))
    SHOP.add(at("s06", "found in a shop"), tag("A SHOP IN JAPAN", 560, 400, 34, bg=CREAM, rot=-1), until=nx("s06"))
    SHOP.add(at("s06", "asked to put") - 0.4, sprite(A.prop("uniform"), 1400, 640, 520, entry="slide_r", dur=0.7),
             until=nx("s06"))
    SHOP.add(at("s06", "the uniform back on") - 0.2, tag("PUT THE UNIFORM BACK ON", 1400, 300, 38, bg=CREAM, rot=-2,
                                                         pin=True), until=nx("s06"))
    SHOP.add(at("s06", "the uniform back on") + 0.2, arrow((1400, 350), (1400, 470), 0.0, RUST, 7, 0.4), until=nx("s06"))

    # ============================================================ s07 (cut): the bolt; the title in the silence
    t7 = st("s07")
    cam.key(t7 - 0.001, frame_on(SHOP, W / 2 + 80, H / 2 + 20, 1.05), "cut")
    cam.key(t7, frame_on(CLR, 1100, 560, 1.2), "cut")
    cam.key(en("s07"), frame_on(CLR, 1100, 560, 1.23), "hold")
    ho = A.rig("onoda", "hand_over")
    CLR.add(t7 - 0.001, actor(ho, 1180, 940, 600, seed=2.0))
    p03 = A.photo("p03")
    CLR.add(t7 + 0.2, photo_card(p03, 560, 700, 440, "drop", tilt=-2, hold=4))
    # the bolt slides out of the rifle as he speaks the line, then holds
    CLR.add(at("s07", "took the bolt") - 0.1, sprite(A.prop("bolt"), 1460, 640, 230,
                                                     path=curve((1300, 640), (1500, 600), -0.2), dur=1.3))
    CLR.add(at("s07", "took the bolt") + 1.0, ring_glow(1500, 600, 90))
    # title_overlay: built during the beat's trailing pause (spec 5 and the beat note), then held still
    title = BUILD["beats"][6]["title_overlay"]
    overlays.append((en("s07"), nx("s07") + 0.45, title_card(title, fade_at=nx("s07") - en("s07"))))

    # ============================================================ s08: an ordinary young man
    t8 = st("s08")
    cam.key(t8 - 0.001, frame_on(CLR, 1100, 560, 1.23), "cut")  # the frame the silence held
    cam.key(t8 + 1.6, frame_on(VIL, W / 2, H / 2, 1.0))
    cam.key(at("s08", "He had a gift"), frame_on(VIL, W / 2 + 120, H / 2 + 20, 1.06), "hold")
    cam.key(at("s08", "He had a gift") + 1.0, frame_on(VIL, 1100, 560, 1.18))
    cam.key(nx("s08"), frame_on(VIL, 1120, 560, 1.22), "hold")
    young = A.rig("onoda", "civilian_young")
    VIL.add(t8 + 0.8, actor(young, 260, 960, 560, motion=walk(-500, 340, 0.0, 5.0)))
    VIL.add(at("s08", "born in March") , tag("BORN MAR 1922", 470, 170, 44, rot=-3, pin=True))
    VIL.add(at("s08", "Wakayama"), tag("WAKAYAMA", 450, 270, 36, bg=MUSTARD, rot=2))
    VIL.add(at("s08", "Before the war"), panel((1180, 120, 680, 330), CREAM, 0.95))
    VIL.add(at("s08", "trading company") - 0.1, headline("TRADING COMPANY", 1520, 200, 40, INK))
    VIL.add(at("s08", "in China") - 0.1, headline("JAPAN  →  CHINA", 1520, 250, 30, OLIVE, f=semi_font(30)))
    VIL.add(at("s08", "selling lacquerware") - 0.2, sprite(A.prop("lacquerware"), 1520, 360, 230, entry="pop"))
    VIL.add(at("s08", "selling lacquerware") + 0.4, headline("LACQUERWARE", 1720, 430, 26, RUST, f=semi_font(26)))
    for i in range(3):
        VIL.add(at("s08", "He was good at it") + 0.18 * i, check(1250 + 60 * i, 400, 0.9, RUST))
    # languages: three greetings in speech bubbles (set by the animation layer)
    for i, (s_, fnt) in enumerate((("Hello", None), ("你好", CJK), ("こんにちは", CJK))):
        VIL.add(at("s08", "a gift for languages") + 0.25 * i, bubble(s_, 560 + i * 200, 420 - (i % 2) * 60, fnt))
    p04 = A.photo("p04")
    VIL.add(at("s08", "an ordinary young man") - 0.3, photo_card(p04, 1450, 650, 420, "slide_left", tilt=2, hold=8))
    VIL.add(at("s08", "drafted at twenty"), tag("DRAFTED AT 20", 980, 760, 40, bg=MUSTARD, rot=-3, pin=True))
    VIL.add(at("s08", "unremarkable") - 0.1, stamp("UNREMARKABLE", 1000, 560, 64))

    return stations, cam, overlays


# ---------------------------------------------------------------- scene-specific builders

def bubble(s, x, y, fnt=None, dur=0.4):
    f = font(fnt, 36) if fnt else head_font(36)
    tw = text_width(s, f)

    def draw(c, age):
        p = out_back(age / dur)
        if p <= 0:
            return
        c.save()
        c.translate(x, y)
        c.scale(p, p)
        w, h = tw + 50, 70
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 30, 30)
        tail = poly([(-w / 2 + 30, h / 2 - 4), (-w / 2 + 22, h / 2 + 22), (-w / 2 + 52, h / 2 - 4)], True)
        c.drawRRect(rr, fill(CREAM))
        c.drawPath(tail, fill(CREAM))
        c.drawRRect(rr, stroke(INK, 4))
        c.drawPath(poly([(-w / 2 + 30, h / 2), (-w / 2 + 22, h / 2 + 22), (-w / 2 + 52, h / 2)]), stroke(INK, 4))
        text(c, s, 0, 12, f, INK, 1, "center")
        c.restore()
    return draw


def stamp(s, x, y, size=64, rgb=RUST, rot=-8, dur=0.35):
    """An ink stamp slammed down at an angle."""
    f = head_font(size)
    tw = text_width(s, f, 4)

    def draw(c, age):
        p = clamp01(age / dur)
        if p <= 0:
            return
        k = lerp(1.6, 1.0, out_cubic(p))
        c.save()
        c.translate(x, y)
        c.rotate(rot)
        c.scale(k, k)
        a = min(1, p * 2)
        r = skia.Rect.MakeXYWH(-tw / 2 - 28, -size * 0.85, tw + 56, size * 1.25)
        c.drawRoundRect(r, 10, 10, stroke(rgb, 7, a))
        text(c, s, 0, size * 0.18, f, rgb, a, "center", 4)
        c.restore()
    return draw


def ring_glow(cx, cy, r, rgb=RUST, dur=0.6):
    """An ink ring drawn round a detail, which stays."""
    return ink(arc_path(cx, cy, r, -110, 340), rgb, 6, dur)


def title_card(title, fade_at=99.0):
    """The title, built in over the held frame in a band across the top (clear of the photo card):
    an ink band unrolls, the words set in one by one, then it holds until the silence ends."""
    words = title.split()
    lines = [" ".join(words[:4]), " ".join(words[4:])]
    f1, f2 = title_font(78), title_font(96)

    def draw(c, age):
        p = out_cubic(age / 0.5)
        if p <= 0:
            return
        fo = 1 - clamp01((age - fade_at) / 0.45)
        if fo <= 0:
            return
        if fo < 1:
            c.saveLayerAlpha(None, int(255 * fo))
        band = skia.Rect.MakeXYWH(0, 36, W, 290 * p)
        c.drawRect(band, fill(INK, 0.92))
        y1, y2 = 140, 262
        for li, (ln, f, y, rgb) in enumerate(((lines[0], f1, y1, CREAM), (lines[1], f2, y2, MUSTARD))):
            q = out_cubic((age - 0.35 - li * 0.55) / 0.6)
            if q > 0:
                text(c, ln, W / 2, y + 24 * (1 - q), f, rgb, q, "center")
        q = in_out((age - 1.3) / 0.6)
        if q > 0:
            c.drawLine(W / 2 - 300 * q, 300, W / 2 + 300 * q, 300, stroke(RUST, 6))
        if fo < 1:
            c.restore()
    return draw
