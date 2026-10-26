"""Day 02, s09 to s62: the training, the island, the reasoning, the dead, the finding, the order, the return.

Same rules as scenes.py. Still beats (s25-s27, s31, s45) are framed before their clocks stop, so the
camera arrives in the pause before them; nothing is added inside them. Cards that `hold` across a
camera move ride on a screen overlay so they stay put while the world moves behind them.
"""
import math
import skia
from engine import *  # noqa: F401,F403
from scenes import bubble, stamp, ring_glow, CJK


class Cam:
    """Camera keys written beat by beat: go (eased move), hold (linear drift), cut."""

    def __init__(self, cam, pos, t):
        self.cam, self.pos, self.t = cam, pos, t

    def go(self, t, pos, dur=1.2):
        t0 = max(self.t + 0.02, t - dur)
        if t0 > self.t + 0.01:
            self.cam.key(t0, self.pos, "hold")
        self.cam.key(t, pos, "move")
        self.pos, self.t = pos, t

    def hold(self, t, pos):
        self.cam.key(t, pos, "hold")
        self.pos, self.t = pos, t

    def cut(self, t, pos):
        self.cam.key(t, pos, "cut")
        self.pos, self.t = pos, t


def zoomed(pos, k):
    return (pos[0], pos[1], pos[2] * k)


def tags(stn, items, x, y0, dy=95, size=38, until=None, rot=(-3, 2, -1, 3, -2), bg=(CREAM, MUSTARD)):
    """A column of pill tags, each popping on its own cue: items = [(text, t)]."""
    for i, (s, t) in enumerate(items):
        stn.add(t, tag(s, x, y0 + i * dy, size, bg=bg[i % len(bg)], rot=rot[i % len(rot)]), until=until)


def men(stn, n0, n1, x, y, t, t_drop, until=None, label=None):
    """A row of n0 small soldier markers; one goes grey and drops away at t_drop (n0 -> n1)."""
    def draw(c, age):
        for i in range(n0):
            gone = i >= n1
            q = clamp01((age - (t_drop - t)) / 0.6) if gone else 0.0
            cx = x + i * 70
            cy = y + 120 * in_cubic(q)
            a = 1 - q
            if a <= 0:
                continue
            col_ = RUST if i == 0 else INK
            c.drawCircle(cx, cy - 34, 15, fill(col_, a))
            c.drawRoundRect(skia.Rect.MakeXYWH(cx - 17, cy - 14, 34, 44), 12, 12, fill(col_, a))
        if label:
            text(c, label, x - 20, y + 70, semi_font(24), INK, min(1, age / 0.3))
    stn.add(t, draw, until=until)


def not_equal(cx, cy, s=1.0, rgb=RUST, dur=0.4):
    """A drawn not-equals sign (the display font has no glyph for it)."""
    a = poly([(cx - 26 * s, cy - 10 * s), (cx + 26 * s, cy - 10 * s)])
    b = poly([(cx - 26 * s, cy + 10 * s), (cx + 26 * s, cy + 10 * s)])
    d = poly([(cx + 14 * s, cy - 28 * s), (cx - 14 * s, cy + 28 * s)])

    def draw(c, age):
        for i, p in enumerate((a, b, d)):
            c.drawPath(partial(p, smooth((age - i * 0.12) / 0.25)), stroke(rgb, 8 * s))
    return draw


def equals(cx, cy, s=1.0, rgb=INK):
    def draw(c, age):
        for dy in (-9, 9):
            c.drawPath(partial(poly([(cx - 22 * s, cy + dy * s), (cx + 22 * s, cy + dy * s)]), smooth(age / 0.3)),
                       stroke(rgb, 8 * s))
    return draw


def loop_arrows(cx, cy, r, n=4, rgb=RUST, dur=1.6):
    """A ring of arrows that all curve back into the ring: every argument is part of the trap."""
    arcs = [arc_path(cx, cy, r, i * 360 / n + 8, 360 / n - 22) for i in range(n)]

    def draw(c, age):
        for i, p in enumerate(arcs):
            q = smooth((age - i * dur / n * 0.6) / (dur / n))
            if q <= 0:
                continue
            c.drawPath(partial(p, q), stroke(rgb, 9))
            if q >= 1:
                (hx, hy), ang = point_on(p, 1.0)
                a = math.radians(ang)
                for s in (-0.5, 0.5):
                    c.drawLine(hx, hy, hx - 28 * math.cos(a + s), hy - 28 * math.sin(a + s), stroke(rgb, 9))
    return draw


def light_corridor(cx, top, bottom, w0, w1, a=0.85):
    """A long corridor of light narrowing to a far point, on dark ink."""
    def draw(c, age):
        p = out_cubic(age / 0.8)
        c.drawRect(skia.Rect.MakeWH(W, H), fill(INK, 0.92 * p))
        path = poly([(cx - w0 / 2, bottom), (cx + w0 / 2, bottom), (cx + w1 / 2, top), (cx - w1 / 2, top)], True)
        lp = fill(CREAM, a * p)
        lp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
        c.drawPath(path, lp)
    return draw


def window_light(rect, a=0.95):
    """A dark room with one bright window: the hotel room."""
    x, y, w, h = rect

    def draw(c, age):
        p = smooth(age / 0.8)
        c.drawRect(skia.Rect.MakeWH(W, H), fill(INK, 0.95 * p))
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), fill(CREAM, a * p))
        for i in (1, 2):
            c.drawLine(x + w * i / 3, y, x + w * i / 3, y + h, stroke(INK, 12, p))
        c.drawLine(x, y + h / 2, x + w, y + h / 2, stroke(INK, 12, p))
        glow = fill(CREAM, 0.18 * p)
        glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60))
        c.drawPath(poly([(x, y + h), (x + w, y + h), (x + w + 300, H), (x - 300, H)], True), glow)
    return draw


def open_door(x, y, w, h):
    """The bookshop door standing open onto a bright street: a bright doorway and the door swung in."""
    def draw(c, age):
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), fill(OFFWHITE))
        glow = fill(CREAM, 0.55)
        glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
        c.drawPath(poly([(x, y + h), (x + w, y + h), (x + w + 260, y + h + 220), (x - 160, y + h + 220)], True), glow)
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), stroke(INK, 10))
        door = poly([(x, y), (x - w * 0.45, y + 40), (x - w * 0.45, y + h + 30), (x, y + h)], True)
        c.drawPath(door, fill(OLIVE))
        c.drawPath(door, stroke(INK, 8))
        c.drawCircle(x - w * 0.36, y + h * 0.55, 9, fill(MUSTARD))
    return draw


def two_sides(left, right, t, until=None):
    """Split screen: left on ink, right on cream, each with a headline (the 1944 / 1974 comparison)."""
    def draw(c, age):
        p = out_cubic(age / 0.6)
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W / 2 * p, H), fill(INK, 0.92))
        c.drawRect(skia.Rect.MakeXYWH(W - W / 2 * p, 0, W / 2 * p, H), fill(CREAM, 0.94))
    return draw


def build(ctx):
    tl, A = ctx["tl"], ctx["A"]
    at, st, en, nx = tl.at, tl.start, tl.end, tl.next_start
    cam = Cam(ctx["cam"], ctx["last"], ctx["last_t"])
    G = ctx
    CLR, DEEP, RICE, BEACH, STRIP, FARM, SCHOOL = (G[k] for k in ("CLR", "DEEP", "RICE", "BEACH", "STRIP", "FARM", "SCHOOL"))
    MAP, PALACE, VIL, SHOP, CLASS, PORT, TOKYO, CAMP = (G[k] for k in ("MAP", "PALACE", "VIL", "SHOP", "CLASS", "PORT", "TOKYO", "CAMP"))
    RANCH, HIMAL, PAPER, ISL = G["RANCH"], G["HIMAL"], G["PAPER"], G["ISL"]
    ov = G["overlays"]
    R = A.rig
    P = A.prop

    # ============================================================ s09 (calm): where he was sent to train
    cam.go(st("s09") + 0.6, frame_on(CLASS, W / 2, H / 2, 1.0), 1.4)
    cam.hold(nx("s09"), frame_on(CLASS, W / 2, H / 2 - 10, 1.04))
    CLASS.add(at("s09", "where he was sent"), tag("WHERE HE TRAINED", 960, 200, 46, rot=-2, pin=True), until=st("s10") + 0.4)

    # ============================================================ s10: the Nakano School
    u10 = nx("s10") - 0.2
    cam.go(st("s10") + 0.8, frame_on(CLASS, 1000, 560, 1.05), 1.0)
    cam.hold(at("s10", "Both were failures"), frame_on(CLASS, 1000, 560, 1.08))
    cam.go(at("s10", "Both were failures") + 0.8, frame_on(CLASS, 1150, 640, 1.18), 0.9)
    cam.hold(u10, frame_on(CLASS, 1150, 640, 1.21))
    CLASS.add(st("s10") - 0.3, actor(R("onoda", "study_paper"), 560, 930, 420, seed=0.3), until=nx("s11") + 0.3)
    CLASS.add(at("s10", "The Nakano School"), tag("NAKANO SCHOOL, TOKYO", 560, 300, 40, bg=MUSTARD, rot=-3, pin=True),
              until=u10)
    CLASS.add(at("s10", "trained men for"), panel((1010, 170, 760, 700), CREAM, 0.96), until=u10)
    rows = [("INTELLIGENCE", at("s10", "trained men for")), ("UNCONVENTIONAL WAR", at("s10", "unconventional")),
            ("GUERRILLA", at("s10", "Guerrilla")), ("SABOTAGE", at("s10", "sabotage")),
            ("HOLD OUT BEHIND THE LINES", at("s10", "holding out"))]
    for i, (s, t) in enumerate(rows):
        CLASS.add(t, typewriter(s, 1050, 250 + i * 62, 30, INK, 32), until=u10)
    CLASS.add(at("s10", "Not infantry"), headline("NOT INFANTRY", 1600, 330, 26, RUST, rise=6), until=u10)
    CLASS.add(at("s10", "Not infantry") + 0.2, strike(1500, 1700, 322), until=u10)
    for i, (s, t, mark) in enumerate([("CAPTURED", at("s10", "to be captured"), "x"),
                                      ("SUICIDE", at("s10", "kill themselves"), "x"),
                                      ("SURVIVE AND RESIST", at("s10", "Survival and continued"), "v")]):
        y = 620 + i * 75
        CLASS.add(t, headline(s, 1050, y, 36, RUST if mark == "v" else INK, "left", rise=8), until=u10)
        CLASS.add(t + 0.4, cross(1720, y - 12, 20, RUST, 9) if mark == "x" else check(1720, y - 12, 1.0, INK), until=u10)
    CLASS.add(at("s10", "Survival and continued") - 0.2, sprite(P("flag_folded"), 330, 440, 170, entry="drop", rot=-6),
              until=u10)

    # ============================================================ s11: trained to do exactly this
    u11 = nx("s11")
    cam.go(st("s11") + 0.5, frame_on(CLASS, W / 2, H / 2, 1.0), 0.9)
    cam.hold(u11 - 0.1, frame_on(CLASS, W / 2, H / 2 - 20, 1.05))
    CLASS.add(st("s11") - 0.2, light_corridor(960, 330, 1080, 900, 120), until=u11 + 0.4)
    CLASS.add(st("s11") + 0.4, actor(R("onoda", "alone_stand"), 960, 470, 170, seed=1.1, enter="fade"), until=u11 + 0.4)
    CLASS.add(at("s11", "not a frightened"), tag("A FRIGHTENED CONSCRIPT?", 520, 200, 38, rot=-3), until=u11)
    CLASS.add(at("s11", "not a frightened") + 1.2, cross(520, 200, 40, RUST, 12), until=u11)
    CLASS.add(at("s11", "specifically trained"), tag("TRAINED TO DO EXACTLY THIS", 1380, 200, 38, bg=MUSTARD, rot=2, pin=True),
              until=u11)
    CLASS.add(at("s11", "considered doing it"), sprite(P("medal"), 520, 700, 300, entry="pop", wobble=1.0), until=u11)
    CLASS.add(at("s11", "a success"), tag("DECADES = SUCCESS", 1380, 760, 40, rot=-2), until=u11)
    CLASS.add(at("s11", "rather than a tragedy"), headline("NOT A TRAGEDY", 1380, 860, 30, CREAM, rise=8), until=u11)

    # ============================================================ s12: Lubang, December 1944 (map)
    MAPX, MAPY = 844, 372  # Lubang on the map plate: the islets north-west of Mindoro (read off the plate)
    u12 = nx("s12")
    cam.go(st("s12") + 0.3, frame_on(MAP, W / 2, H / 2, 1.0), 1.4)
    cam.hold(at("s12", "The island is small") - 0.4, frame_on(MAP, W / 2, H / 2, 1.04))
    cam.go(at("s12", "The island is small"), frame_on(MAP, MAPX - 200, MAPY - 20, 1.35), 0.9)
    cam.hold(at("s12", "The Allied advance") - 0.2, frame_on(MAP, MAPX - 200, MAPY - 20, 1.39))
    cam.go(at("s12", "The Allied advance") + 0.6, frame_on(MAP, W / 2, H / 2, 1.05), 0.9)
    cam.hold(u12 - 0.1, frame_on(MAP, W / 2, H / 2, 1.08))
    MAP.add(at("s12", "In December 1944"), tag("DEC 1944", 300, 150, 48, rot=-3, pin=True), until=u12)
    MAP.add(at("s12", "the Philippines") - 0.2, headline("PHILIPPINES", 1560, 860, 44, INK, f=title_font(46)), until=u12)
    MAP.add(at("s12", "Lubang Island"), ink(arc_path(MAPX, MAPY, 46), RUST, 7, 0.6), until=u12)
    MAP.add(at("s12", "Lubang Island") + 0.3, tag("LUBANG", MAPX - 190, MAPY - 50, 36, bg=MUSTARD, rot=3), until=u12)
    MAP.add(at("s12", "about thirty"), tag("~30 KM", MAPX - 190, MAPY + 50, 32, rot=-2), until=u12)
    MAP.add(at("s12", "The Allied advance"), arrow((1800, 160), (MAPX + 140, MAPY - 120), 0.15, RUST, 8, 0.9), until=u12)
    for i, (s, t) in enumerate([("DESTROY THE AIRSTRIP AND PIER", at("s12", "destroy the island")),
                                ("HARASS ANY LANDING", at("s12", "to harass")), ("HOLD", at("s12", "and to hold"))]):
        MAP.add(t, tag(s, 520, 620 + i * 100, 40 if s != "HOLD" else 56, bg=CREAM if i < 2 else RUST,
                       rgb=INK if i < 2 else CREAM, rot=(-2, 2, -3)[i]), until=u12)
    MAP.add(at("s12", "destroy the island") - 0.3, sprite(P("rifle"), 520, 520, 420, entry="slide_l"), until=u12)
    p05 = A.photo("p05")
    t5 = at("s12", "The island is small") + 0.2
    ov.append((t5, nx("s13") + 0.4, glide(photo_card(p05, 1530, 330, 440, "slide_up", tilt=2, hold=12),
                                         st("s13") - t5, (0, 0), (150, -60), 1.2, nx("s13") - t5)))  # hold: 1 (s13)

    # ============================================================ s13: the order, the airstrip
    u13 = nx("s13")
    cam.go(st("s13") + 0.6, frame_on(STRIP, 760, 520, 1.22), 1.6)
    cam.hold(u13 - 0.1, frame_on(STRIP, 760, 520, 1.28))
    STRIP.add(st("s13") - 0.6, actor(R("taniguchi", "officer_order"), 520, 960, 600, seed=0.2), until=u13 + 0.5)
    STRIP.add(st("s13") - 0.6, actor(R("onoda", "attention"), 1000, 960, 560, flip=True, seed=2.2), until=u13 + 0.5)
    STRIP.add(at("s13", "Major Yoshimi") - 0.2, tag("MAJ. YOSHIMI TANIGUCHI", 430, 200, 32, bg=MUSTARD, rot=-2, pin=True),
              until=u13)
    STRIP.add(at("s13", "The order Taniguchi"), sprite(P("order"), 860, 600, 100, path=curve((700, 560), (860, 600), -0.3),
                                                         dur=0.9, rot=-8), until=u13)
    for i, (s, t) in enumerate([("SURRENDER", at("s13", "was he to surrender")),
                                ("SUICIDE", at("s13", "take his own life"))]):
        STRIP.add(t, tag(s, 360 + i * 300, 320, 32, rot=(-2, 3)[i]), until=u13)
        STRIP.add(t + 0.35, cross(360 + i * 300, 320, 28, RUST, 10), until=u13)
    STRIP.add(at("s13", "He was to hold out"), tag("HOLD OUT, HOWEVER LONG", 900, 200, 32, bg=RUST, rgb=CREAM, rot=-1),
              until=u13)
    STRIP.add(at("s13", "Taniguchi would come back"), bubble("I will come back for you", 760, 790), until=u13)

    # ============================================================ s14: the Americans land; four men into the hills
    u14 = nx("s14")
    cam.go(st("s14") + 0.4, frame_on(BEACH, W / 2, H / 2, 1.16), 1.2)
    cam.hold(u14 - 0.1, frame_on(BEACH, W / 2, H / 2, 1.2))
    BEACH.add(at("s14", "Three months later") - 0.2, panel((1110, 250, 580, 150), CREAM, 0.94), until=u14)
    BEACH.add(at("s14", "Three months later"), tag("3 MONTHS LATER", 1400, 200, 40, rot=-3, pin=True), until=u14)
    BEACH.add(at("s14", "the Americans landed"), headline("THE AMERICANS LAND", 1400, 300, 38, RUST, rise=10), until=u14)
    BEACH.add(at("s14", "The Japanese garrison"), headline("GARRISON DESTROYED IN DAYS", 1400, 360, 30, INK),
              until=u14)
    BEACH.add(at("s14", "Onoda took to the hills") - 0.3,
              actor(R("comrades", "four_climb"), 1050, 960, 330, motion=walk(-250, 300, 0, 6.0, bob=6), seed=0.5), until=u14 + 0.4)
    names = [("AKATSU", at("s14", "Yuichi Akatsu")), ("SHIMADA", at("s14", "Shoichi Shimada")),
             ("KOZUKA", at("s14", "Kinshichi Kozuka"))]
    for i, (s, t) in enumerate(names):
        BEACH.add(t, tag(s, 1160 + i * 240, 470, 32, bg=(CREAM, MUSTARD)[i % 2], rot=(-3, 2, -1)[i]), until=u14)
    p07 = A.photo("p07")
    BEACH.add(at("s14", "The Japanese garrison") + 0.3, photo_card(p07, 600, 420, 600, "slide_right", tilt=2, hold=10),
              until=u14)

    # ============================================================ s15 (calm): four men, one island, one order
    u15 = nx("s15")
    cam.go(st("s15") + 0.6, frame_on(CLR, W / 2, H / 2, 1.16), 1.4)
    cam.hold(u15 - 0.1, frame_on(CLR, W / 2, H / 2 - 10, 1.2))
    CLR.add(st("s15") - 0.4, actor(R("comrades", "group_fire"), 1300, 560, 170, seed=0.8), until=u15 + 0.3)
    CLR.add(st("s15") - 0.4, actor(R("onoda", "sit_fire"), 1180, 560, 150, seed=1.8), until=u15 + 0.3)
    CLR.add(at("s15", "Four men") - 0.2, panel((440, 260, 420, 340), CREAM, 0.95), until=u15)
    CLR.add(at("s15", "Four men"), headline("4 MEN", 520, 360, 64, INK, "left"), until=u15)
    CLR.add(at("s15", "on a small island"), headline("1 ISLAND", 520, 450, 64, OLIVE, "left"), until=u15)
    CLR.add(at("s15", "with an order"), headline("1 ORDER", 520, 540, 64, RUST, "left"), until=u15)

    # ============================================================ s16 (cut): the war ends; nobody believed it
    u16 = nx("s16")
    cam.cut(st("s16"), frame_on(DEEP, 900, 560, 1.18))
    cam.hold(u16 - 0.1, frame_on(DEEP, 960, 560, 1.22))
    DEEP.add(st("s16"), actor(R("onoda", "patrol"), 700, 960, 520, motion=walk(-200, 500, 0.0, 6.0, bob=7)), until=u16 + 0.3)
    DEEP.add(st("s16") + 0.2, sprite(P("calendar_1945"), 1460, 380, 300, entry="pop", wobble=2), until=u16)
    for i in range(6):  # pages tear off and fly past
        DEEP.add(st("s16") + 0.6 + i * 0.35, page_fly(1460, 300, i), until=u16)
    DEEP.add(at("s16", "The war ended"), tag("AUG 1945: THE WAR ENDS", 640, 200, 42, bg=MUSTARD, rot=-2, pin=True), until=u16)
    DEEP.add(at("s16", "Nobody"), tag("NOBODY BELIEVED IT", 640, 300, 38, rot=2), until=u16)

    # ============================================================ s17: the reasoning
    u17 = nx("s17")
    cam.go(st("s17") + 0.5, frame_on(DEEP, 760, 560, 1.3), 0.9)
    cam.hold(u17 - 0.1, frame_on(DEEP, 760, 560, 1.34))
    DEEP.add(st("s17") - 0.3, lambda c, a: c.drawRect(skia.Rect.MakeWH(W, H), fill(INK, 0.55 * smooth(a / 0.8))), until=u17 + 0.4)
    DEEP.add(st("s17") - 0.2, sprite(P("campfire"), 900, 860, 220, entry="pop"), until=u17 + 0.4)
    DEEP.add(st("s17") - 0.2, actor(R("onoda", "study_paper"), 620, 930, 400, seed=0.4), until=u17 + 0.4)
    DEEP.add(at("s17", "not insane"), tag("NOT INSANE", 1300, 300, 42, rot=-3), until=u17)
    DEEP.add(at("s17", "not stupid"), tag("NOT STUPID", 1300, 410, 42, bg=MUSTARD, rot=2), until=u17)
    DEEP.add(at("s17", "He was applying"), sprite(P("chess"), 1300, 620, 330, entry="pop"), until=u17)
    DEEP.add(at("s17", "almost airtight"), stamp("ALMOST AIRTIGHT", 1300, 820, 46, rot=-5), until=u17)

    # ============================================================ s18: every announcement is bait
    u18 = nx("s18")
    cam.go(st("s18") + 0.4, frame_on(DEEP, W / 2, H / 2, 1.16), 0.8)
    cam.hold(u18 - 0.1, frame_on(DEEP, W / 2 + 40, H / 2, 1.21))
    DEEP.add(st("s18") - 0.2, actor(R("onoda", "crouch_watch"), 1560, 1000, 500, flip=True, seed=0.7), until=u18 + 0.3)
    DEEP.add(at("s18", "trained in deception"), tag("TRAINED IN DECEPTION", 520, 190, 40, rot=-2, pin=True), until=u18)
    DEEP.add(at("s18", "in order to flush"), sprite(P("lure"), 860, 420, 200, path=curve((860, -200), (860, 420), 0.05),
                                                     dur=1.2, wobble=4, seed=2), until=u18)
    DEEP.add(at("s18", "So every announcement"), tag("ANNOUNCEMENT = BAIT", 520, 320, 40, bg=MUSTARD, rot=2), until=u18)
    DEEP.add(at("s18", "The louder"), sprite(P("loudspeaker"), 520, 760, 200, entry="rise"), until=u18)
    DEEP.add(at("s18", "the more effort"), meter(260, 560, at("s18", "the more effort") - at("s18", "The louder")), until=u18)
    DEEP.add(at("s18", "he mattered"), tag("LOUDER = MORE PROOF HE MATTERED", 900, 600, 34, rot=-2), until=u18)

    # ============================================================ s19: the leaflets are forgeries
    u19 = nx("s19")
    cam.go(st("s19") + 0.4, frame_on(DEEP, 900, 560, 1.18), 0.8)
    cam.hold(u19 - 0.1, frame_on(DEEP, 900, 560, 1.22))
    DEEP.add(st("s19") - 0.2, actor(R("comrades", "group_fire"), 420, 960, 330, seed=0.3), until=u19 + 0.3)
    DEEP.add(st("s19") - 0.2, actor(R("onoda", "study_paper"), 760, 960, 380, seed=0.9), until=u19 + 0.3)
    DEEP.add(at("s19", "In late 1945"), tag("LATE 1945", 380, 180, 40, rot=-3, pin=True), until=u19)
    DEEP.add(at("s19", "leaflets were dropped") - 0.2, sprite(P("leaflets"), 1300, 380, 380,
                                                               path=curve((1300, -250), (1300, 380), 0.25), dur=1.2), until=u19)
    DEEP.add(at("s19", "General Tomoyuki"), tag("GEN. TOMOYUKI YAMASHITA'S ORDER", 1300, 150, 30, bg=MUSTARD, rot=2), until=u19)
    DEEP.add(at("s19", "examined them closely"), sprite(P("magnifier"), 1560, 460, 220, path=curve((1900, 800), (1560, 460), 0.2),
                                                        dur=0.8, wobble=2), until=u19)
    for i in range(3):  # errors circled beside the leaflet, not on it
        DEEP.add(at("s19", "found what they considered") + i * 0.35, ring_glow(1060 + i * 90, 640, 32), until=u19)
    DEEP.add(at("s19", "phrasing"), headline("PHRASING ERRORS?", 1170, 720, 30, RUST, rise=8), until=u19)
    DEEP.add(at("s19", "were forgeries"), stamp("FORGERIES", 1300, 820, 60), until=u19)

    # ============================================================ s20 (calm): right by their logic
    u20 = nx("s20")
    cam.go(st("s20") + 0.6, frame_on(DEEP, 1100, 500, 1.3), 1.0)
    cam.hold(u20 - 0.1, frame_on(DEEP, 1100, 500, 1.33))
    DEEP.add(at("s20", "By their own logic"), tag("RIGHT, BY THEIR LOGIC", 1100, 250, 42, rot=-2), until=u20)
    DEEP.add(at("s20", "By any other measure"), headline("TALKED OUT OF", 1100, 680, 46, CREAM, rise=10), until=u20)
    DEEP.add(at("s20", "By any other measure") + 0.6, headline("THE END OF THE WAR", 1100, 750, 46, MUSTARD, rise=10), until=u20)

    # ============================================================ s21: more came; his brother's voice
    u21 = nx("s21")
    cam.go(st("s21") + 0.6, frame_on(DEEP, W / 2, H / 2, 1.16), 1.0)
    cam.hold(at("s21", "Onoda listened") - 0.2, frame_on(DEEP, W / 2, H / 2, 1.2))
    cam.go(at("s21", "Onoda listened") + 0.6, frame_on(DEEP, 1300, 500, 1.4), 0.8)
    cam.hold(u21 - 0.1, frame_on(DEEP, 1300, 500, 1.44))
    DEEP.add(st("s21") - 0.3, actor(R("onoda", "listen_sky"), 1350, 960, 520, seed=0.2), until=u21 + 0.3)
    items = [("NEWSPAPERS", at("s21", "Newspapers")), ("PHOTOGRAPHS", at("s21", "Photographs")),
             ("LETTERS", at("s21", "Letters from")), ("LOUDSPEAKERS", at("s21", "Loudspeakers"))]
    tags(DEEP, items, 420, 220, 90, 36, until=u21)
    DEEP.add(at("s21", "Newspapers") + 0.2, sprite(P("newspapers"), 760, 720, 280, entry="drop"), until=u21)
    DEEP.add(at("s21", "played from aircraft") - 0.6, sprite(P("plane_speaker"), 0, 0, 380,
                                                            path=curve((-300, 160), (2200, 120), 0.03), dur=6.0), until=u21)
    DEEP.add(at("s21", "his own brother"), bubble("HIS BROTHER'S VOICE", 1050, 300), until=u21)
    for i, (s, t) in enumerate([("UNDER DURESS?", at("s21", "under duress")), ("SPLICED?", at("s21", "or spliced")),
                                ("IMITATED?", at("s21", "or imitated"))]):
        DEEP.add(t, tag(s, 960 + i * 0, 520 + i * 90, 34, bg=(CREAM, MUSTARD, CREAM)[i], rot=(-3, 2, -2)[i]), until=u21)

    # ============================================================ s22 (calm): every argument is part of the trap
    u22 = nx("s22")
    cam.go(st("s22") + 0.6, frame_on(DEEP, W / 2, H / 2, 1.16), 1.0)
    cam.hold(u22 - 0.1, frame_on(DEEP, W / 2, H / 2, 1.2))
    DEEP.add(st("s22") - 0.2, lambda c, a: c.drawRect(skia.Rect.MakeWH(W, H), fill(CREAM, 0.8 * smooth(a / 0.6))),
             until=u22 + 0.3)
    DEEP.add(st("s22"), actor(R("onoda", "alone_stand"), 960, 720, 360, seed=0.3, enter="fade"), until=u22 + 0.3)
    DEEP.add(st("s22") + 0.4, loop_arrows(960, 560, 300), until=u22 + 0.3)
    DEEP.add(at("s22", "every argument"), tag("EVERY ARGUMENT = PART OF THE TRAP", 960, 160, 38, rot=-1), until=u22)

    # ============================================================ s23: so they stayed
    u23 = nx("s23")
    cam.go(st("s23") + 0.5, frame_on(DEEP, W / 2, H / 2, 1.16), 0.9)
    cam.hold(u23 - 0.1, frame_on(DEEP, W / 2 - 40, H / 2, 1.21))
    DEEP.add(st("s23") - 0.2, actor(R("onoda", "clean_rifle"), 1250, 960, 420, seed=0.5), until=u23 + 0.3)
    DEEP.add(at("s23", "They lived on"), sprite(P("bananas"), 420, 760, 300, entry="pop"), until=u23)
    DEEP.add(at("s23", "They lived on") + 0.3, tag("BANANAS · COCONUTS · RICE", 420, 560, 34, rot=-2), until=u23)
    DEEP.add(at("s23", "They built shelters"), sprite(P("lean_to"), 760, 520, 330, entry="drop"), until=u23)
    DEEP.add(at("s23", "in the rainy season"), tag("RAINY SEASON: SHELTERS", 420, 200, 34, bg=MUSTARD, rot=2), until=u23)
    DEEP.add(at("s23", "moved constantly"), tag("DRY SEASON: MOVING", 420, 290, 34, rot=-2), until=u23)
    DEEP.add(at("s23", "They maintained"), sprite(P("oil_tin"), 1500, 860, 170, entry="pop"), until=u23)
    DEEP.add(at("s23", "for twenty-nine years"), panel((1450, 160, 330, 220), INK, 0.92), until=u23)
    DEEP.add(at("s23", "for twenty-nine years") + 0.1, counter(0, 29, 1615, 320, 120, 1.6, rgb=MUSTARD), until=u23)
    DEEP.add(at("s23", "for twenty-nine years") + 0.3, headline("YEARS", 1615, 210, 28, CREAM, rise=6), until=u23)
    DEEP.add(at("s23", "still worked"), tag("THE RIFLE STILL WORKED", 1250, 470, 34, bg=MUSTARD, rot=-2, pin=True), until=u23)

    # ============================================================ s24 (calm, cut): and they fought
    u24 = en("s24") + 0.3
    cam.cut(st("s24"), frame_on(DEEP, 900, 420, 1.3))
    cam.hold(en("s24"), frame_on(DEEP, 900, 420, 1.33))
    DEEP.add(at("s24", "And they fought"), headline("AND THEY FOUGHT", 900, 440, 80, CREAM, rise=14), until=u24)

    # ============================================================ s25-s27 (still): the islanders who were killed
    # The empty rice field, framed before the clock stops; nothing is added (beat note).
    cam.go(st("s25") - 0.05, frame_on(RICE, W / 2, H / 2, 1.16), 1.3)
    cam.hold(nx("s27"), frame_on(RICE, W / 2, H / 2, 1.16))

    # ============================================================ s28: the group shrank
    u28 = nx("s28")
    cam.go(st("s28") + 0.7, frame_on(CLR, W / 2, H / 2, 1.16), 1.5)
    cam.hold(u28 - 0.1, frame_on(CLR, W / 2 + 40, H / 2, 1.2))
    CLR.add(at("s28", "The group shrank") - 0.4, actor(R("comrades", "group_fire"), 1300, 900, 300, seed=0.4), until=u28 + 0.3)
    CLR.add(at("s28", "walked away"), actor(R("comrades", "one_leaves"), 760, 920, 380,
                                             motion=walk(0, -560, 0.2, 4.5, bob=6)), until=u28)
    men(CLR, 4, 3, 300, 220, at("s28", "The group shrank"), at("s28", "gave himself up"), until=u28 + 0.2)
    CLR.add(at("s28", "Akatsu, the youngest"), tag("AKATSU LEAVES, 1949", 1300, 260, 38, rot=-2, pin=True), until=u28)
    CLR.add(at("s28", "gave himself up"), tag("SURRENDERS, 1950", 1300, 360, 36, bg=MUSTARD, rot=2), until=u28)
    CLR.add(at("s28", "treated his defection"), tag("PROOF HE WAS TURNED?", 1300, 460, 36, rot=-1), until=u28)

    # ============================================================ s29 (calm): May 1954, Shimada
    u29 = nx("s29")
    cam.go(st("s29") + 0.6, frame_on(BEACH, W / 2, H / 2, 1.16), 1.2)
    cam.hold(u29 - 0.1, frame_on(BEACH, W / 2, H / 2, 1.2))
    BEACH.add(st("s29") + 0.3, photo_card(p07, 1250, 500, 760, "slide_left", tilt=-1.5, hold=8), until=u29)
    men(BEACH, 3, 2, 300, 260, st("s29") + 0.2, at("s29", "Shimada was"), until=u29)
    BEACH.add(at("s29", "In May 1954"), tag("MAY 1954: SHIMADA", 380, 420, 40, rot=-2, pin=True), until=u29)

    # ============================================================ s30 (calm): October 1972, Kozuka
    u30 = nx("s30") - 1.0
    cam.go(st("s30") + 0.6, frame_on(FARM, W / 2, H / 2, 1.16), 1.2)
    cam.hold(en("s30"), frame_on(FARM, W / 2, H / 2, 1.2))
    p08 = A.photo("p08")
    FARM.add(at("s30", "Kinshichi Kozuka") - 0.3, photo_card(p08, 1380, 470, 300, "pin", tilt=2, hold=10, view=1.2), until=u30)
    men(FARM, 2, 1, 300, 260, st("s30") + 0.2, at("s30", "was killed"), until=u30)
    FARM.add(at("s30", "In October 1972"), tag("OCT 1972", 380, 420, 42, rot=-2, pin=True), until=u30)
    FARM.add(at("s30", "twenty-seven years"), tag("27 YEARS AFTER THE WAR", 420, 520, 34, bg=MUSTARD, rot=2), until=u30)
    FARM.add(at("s30", "Kozuka had been"), tag("KOZUKA, WITH HIM SINCE 1944", 1380, 830, 32, rot=-1), until=u30)

    # ============================================================ s31 (still): alone. A rifle against a tree, a cold fire.
    t31 = st("s31")
    cam.go(t31 - 0.05, frame_on(CLR, 1100, 620, 1.3), 1.4)
    cam.hold(nx("s31"), frame_on(CLR, 1100, 620, 1.3))
    CLR.add(t31 - 0.6, sprite(P("rifle"), 1420, 640, 380, entry="none", rot=-72), until=nx("s31"), fade=0.0)
    CLR.add(t31 - 0.6, cold_fire(P("campfire"), 960, 860, 260), until=nx("s31"), fade=0.0)

    # ============================================================ s32: back in the papers
    u32 = nx("s32")
    cam.go(st("s32") + 0.6, frame_on(DEEP, W / 2, H / 2, 1.16), 1.2)
    cam.hold(u32 - 0.1, frame_on(DEEP, W / 2 + 40, H / 2, 1.2))
    DEEP.add(st("s32") + 0.2, sprite(P("newspapers"), 520, 600, 420, entry="drop"), until=u32)
    DEEP.add(st("s32") + 0.6, tag("BACK IN THE PAPERS", 520, 330, 42, rot=-3, pin=True), until=u32)
    DEEP.add(at("s32", "Search parties"), actor(R("crowd", "search_party"), 1100, 700, 300,
                                                motion=walk(-200, 500, 0, 3.0, bob=4)), until=u32)
    DEEP.add(at("s32", "found nothing"), tag("SEARCH PARTIES: NOTHING", 1250, 300, 36, bg=MUSTARD, rot=2), until=u32)
    DEEP.add(at("s32", "found nothing") + 0.4, cross(1500, 520, 40, RUST, 12), until=u32)

    # ============================================================ s33: early 1974, Norio Suzuki
    u33 = nx("s33")
    cam.go(st("s33") + 0.9, frame_on(PORT, W / 2, H / 2, 1.0), 2.0)
    cam.hold(u33 - 0.1, frame_on(PORT, W / 2 + 40, H / 2, 1.04))
    PORT.add(st("s33") - 0.6, actor(R("suzuki", "backpack"), 760, 960, 560, seed=0.2), until=nx("s34") + 0.3)
    PORT.add(at("s33", "in early 1974"), tag("EARLY 1974", 400, 200, 42, rot=-3, pin=True), until=u33)
    PORT.add(at("s33", "Norio Suzuki"), tag("NORIO SUZUKI, 24", 1200, 300, 42, bg=MUSTARD, rot=2), until=u33)
    PORT.add(at("s33", "university dropout"), tag("UNIVERSITY DROPOUT", 1200, 400, 34, rot=-2), until=u33)

    # ============================================================ s34: his list of three
    u34 = nx("s34")
    cam.go(st("s34") + 0.5, frame_on(PORT, 1100, 520, 1.12), 0.9)
    cam.hold(u34 - 0.1, frame_on(PORT, 1100, 520, 1.16))
    for i, (s, t) in enumerate([("SOLDIER", at("s34", "not a soldier")), ("JOURNALIST", at("s34", "a journalist")),
                                ("OFFICIAL", at("s34", "government official"))]):
        PORT.add(t, tag(s, 1200 + i * 0, 200 + i * 80, 32, rot=(-2, 2, -1)[i]), until=at("s34", "He was a traveller") + 0.4)
        PORT.add(t + 0.3, cross(1200, 200 + i * 80, 24, RUST, 8), until=at("s34", "He was a traveller") + 0.4)
    PORT.add(at("s34", "He was a traveller"), panel((1080, 140, 720, 640), CREAM, 0.97), until=u34)
    PORT.add(at("s34", "He was a traveller") + 0.2, headline("THE LIST", 1440, 220, 44, RUST, f=title_font(48)), until=u34)
    PORT.add(at("s34", "three things") + 0.1, sprite(P("notebook_sketch"), 1440, 370, 340, entry="pop"), until=u34)
    for i, (s, t, prop) in enumerate([("1. LIEUTENANT ONODA", at("s34", "Lieutenant Onoda"), None),
                                      ("2. A PANDA", at("s34", "a panda"), "panda"),
                                      ("3. THE ABOMINABLE SNOWMAN", at("s34", "the Abominable"), "footprint")]):
        PORT.add(t, typewriter(s, 1120, 540 + i * 70, 32, INK, 30), until=u34)
        if prop:
            PORT.add(t + 0.2, sprite(P(prop), 1700, 520 + i * 70, 120, entry="pop"), until=u34)
    PORT.add(at("s34", "In that order"), underline(1120, 1460, 555, RUST, 6, 0.4), until=u34)

    # ============================================================ s35: he went alone and waited
    u35 = nx("s35")
    cam.go(st("s35") + 0.9, frame_on(CLR, W / 2, H / 2, 1.16), 2.0)
    cam.hold(u35 - 0.1, frame_on(CLR, W / 2, H / 2, 1.2))
    CLR.add(st("s35") - 0.5, sprite(P("tent"), 1260, 840, 420, entry="none"), until=nx("s40") + 0.3)
    CLR.add(st("s35") - 0.5, actor(R("suzuki", "camp_wait"), 900, 960, 330, seed=0.4), until=nx("s37") + 0.3)
    CLR.add(at("s35", "He went to Lubang alone"), tag("ALONE", 520, 220, 48, bg=MUSTARD, rot=-3, pin=True), until=u35)
    for i, (s, t) in enumerate([("SEARCH PARTY", at("s35", "a search party")), ("LOUDSPEAKER", at("s35", "a loudspeaker")),
                                ("WEAPON", at("s35", "or a weapon"))]):
        CLR.add(t, tag(s, 520, 340 + i * 90, 34, rot=(-2, 2, -1)[i]), until=u35)
        CLR.add(t + 0.3, cross(520, 340 + i * 90, 26, RUST, 9), until=u35)
    CLR.add(at("s35", "and waited"), headline("...AND WAITED", 1300, 300, 40, INK, rise=8), until=u35)

    # ============================================================ s36 (calm): day 4, Onoda found him
    u36 = nx("s36")
    cam.go(st("s36") + 0.5, frame_on(CLR, 1100, 560, 1.18), 0.9)
    cam.hold(u36 - 0.1, frame_on(CLR, 1100, 560, 1.22))
    CLR.add(at("s36", "after four days") - 0.8, actor(R("onoda", "crouch_watch"), 1720, 760, 260, flip=True, enter="fade",
                                                      dur=1.4), until=nx("s37") + 0.3)
    CLR.add(at("s36", "On the twentieth"), tag("20 FEB 1974", 520, 220, 42, rot=-2, pin=True), until=u36)
    CLR.add(at("s36", "after four days"), day_counter(520, 360, 4), until=u36)

    # ============================================================ s37: 29 years of searches vs one young man
    u37 = nx("s37")
    cam.go(st("s37") + 0.5, frame_on(CLR, W / 2, H / 2, 1.16), 0.9)
    cam.hold(u37 - 0.1, frame_on(CLR, W / 2, H / 2, 1.2))
    t37 = at("s37", "Twenty-nine years")
    CLR.add(t37 - 0.3, lambda c, a: c.drawRect(skia.Rect.MakeXYWH(0, 0, W / 2 * out_cubic(a / 0.6), H), fill(INK, 0.9)),
            until=u37)
    CLR.add(t37, headline("29 YEARS OF SEARCHES", 480, 230, 44, MUSTARD, rise=10), until=u37)
    CLR.add(at("s37", "search parties"), actor(R("crowd", "search_party"), 480, 760, 300,
                                               motion=keys((0, {"scale": 1.0}), (4.5, {"scale": 1.0}), (6.5, {"scale": 0.0}))),
            until=u37)
    CLR.add(at("s37", "aircraft"), sprite(P("plane_speaker"), 480, 400, 300, entry="slide_l", exit_at=4.0), until=u37)
    CLR.add(at("s37", "broadcasts"), sprite(P("loudspeaker"), 240, 600, 140, entry="pop", exit_at=3.6), until=u37)
    CLR.add(at("s37", "And then one young man"), tag("VS ONE YOUNG MAN WITH NOTHING", 1440, 230, 34, bg=MUSTARD, rot=2), until=u37)
    CLR.add(at("s37", "apparently wanting to talk"), bubble("...", 1060, 640), until=u37)

    # ============================================================ s38: to listen to a soldier's feelings
    u38 = nx("s38")
    cam.go(st("s38") + 0.6, frame_on(CLR, 1000, 600, 1.3), 1.0)
    cam.hold(u38 - 0.1, frame_on(CLR, 1000, 600, 1.34))
    CLR.add(st("s38") - 0.3, sprite(P("campfire"), 960, 900, 200, entry="pop"), until=nx("s39") + 0.3)
    CLR.add(st("s38") - 0.3, actor(R("onoda", "sit_fire"), 700, 960, 420, seed=0.2), until=nx("s39") + 0.3)
    CLR.add(st("s38") - 0.3, actor(R("suzuki", "talk_log"), 1240, 960, 400, seed=1.2), until=nx("s39") + 0.3)
    CLR.add(at("s38", "to listen to"), tag("TO LISTEN TO A SOLDIER'S FEELINGS", 1000, 250, 36, rot=-2, pin=True), until=u38)
    CLR.add(at("s38", "Suzuki asked him"), bubble("Why won't you come out?", 1240, 420), until=u38)

    # ============================================================ s39: friends; only Taniguchi could rescind it
    u39 = nx("s39")
    cam.hold(at("s39", "Onoda explained") - 0.2, frame_on(CLR, 1000, 600, 1.37))
    cam.go(at("s39", "Onoda explained") + 0.6, frame_on(CLR, W / 2, H / 2, 1.16), 0.8)
    cam.hold(u39 - 0.1, frame_on(CLR, W / 2, H / 2, 1.2))
    CLR.add(at("s39", "They became friends"), tag("FRIENDS", 1000, 260, 52, bg=MUSTARD, rot=-3, pin=True), until=at("s39", "Onoda explained") + 0.2)
    CLR.add(at("s39", "He would not come out"), panel((1060, 150, 620, 470), CREAM, 0.96), until=u39)
    CLR.add(at("s39", "He would not come out") + 0.2, headline("ORDERED IN", 1110, 240, 34, INK, "left"), until=u39)
    CLR.add(at("s39", "had not been ordered out") - 0.3, headline("ONLY ORDERED OUT", 1110, 310, 34, RUST, "left"), until=u39)
    CLR.add(at("s39", "He had received an order"), sprite(P("order"), 1140, 430, 90, entry="pop", rot=-6), until=u39)
    CLR.add(at("s39", "only Major Taniguchi"), headline("ONLY MAJ. TANIGUCHI", 1210, 440, 32, INK, "left"), until=u39)
    CLR.add(at("s39", "Anything else"), headline("ANYTHING ELSE = DECEPTION", 1110, 570, 30, RUST, "left"), until=u39)

    # ============================================================ s40: photographs as proof, and home
    u40 = nx("s40")
    cam.go(st("s40") + 0.4, frame_on(CLR, 1100, 560, 1.2), 0.8)
    cam.hold(u40 - 0.1, frame_on(CLR, 1100, 560, 1.24))
    CLR.add(st("s40") - 0.2, actor(R("suzuki", "photograph"), 1200, 960, 520, seed=0.4), until=u40 + 0.3)
    CLR.add(st("s40") + 0.3, sprite(P("camera"), 820, 760, 220, entry="pop"), until=u40)
    for i in range(3):
        CLR.add(at("s40", "took photographs") + i * 0.45, burst(1290, 520, 30, 140, 12, CREAM, 0.4, 7), until=u40)
    CLR.add(at("s40", "as proof"), tag("PHOTOGRAPHS AS PROOF", 760, 260, 40, rot=-2, pin=True), until=u40)
    CLR.add(at("s40", "and flew home"), plane_icon(curve((1000, 420), (2100, -100), -0.2), 1.6), until=u40)

    # ============================================================ s41: found, a bookseller
    u41 = nx("s41")
    cam.go(st("s41") + 0.9, frame_on(SHOP, W / 2, H / 2, 1.0), 2.0)
    cam.hold(u41 - 0.1, frame_on(SHOP, W / 2 + 40, H / 2, 1.04))
    SHOP.add(st("s41") - 0.6, actor(R("taniguchi", "bookseller"), 760, 960, 650, flip=True, seed=0.6), until=nx("s42") + 0.3)
    SHOP.add(at("s41", "went looking"), tag("WANTED: TANIGUCHI", 1300, 240, 40, rot=-2, pin=True), until=u41)
    SHOP.add(at("s41", "They found him"), tag("FOUND", 1300, 340, 48, bg=MUSTARD, rot=2), until=u41)
    SHOP.add(at("s41", "working as a bookseller"), tag("WORKING AS A BOOKSELLER", 1300, 440, 34, rot=-1), until=u41)

    # ============================================================ s42: thirty years late
    u42 = nx("s42")
    cam.go(st("s42") + 0.5, frame_on(SHOP, 1100, 560, 1.14), 0.9)
    cam.hold(u42 - 0.1, frame_on(SHOP, 1100, 560, 1.18))
    SHOP.add(at("s42", "He was in his sixties"), tag("IN HIS SIXTIES", 520, 220, 40, rot=-3, pin=True), until=u42)
    SHOP.add(at("s42", "assumed that the men"), tag("ASSUMED THEY WERE DEAD", 520, 320, 34, bg=MUSTARD, rot=2), until=u42)
    SHOP.add(at("s42", "put on his old uniform") - 0.3, sprite(P("uniform"), 1420, 660, 380, entry="slide_r"), until=u42)
    SHOP.add(at("s42", "fly to the Philippines") - 0.2, sprite(P("suitcase"), 1100, 860, 240, entry="drop"), until=u42)
    SHOP.add(at("s42", "thirty years late"), panel((1480, 140, 330, 200), INK, 0.92), until=u42)
    SHOP.add(at("s42", "thirty years late") + 0.1, counter(0, 30, 1645, 290, 110, 1.2, rgb=MUSTARD), until=u42)
    SHOP.add(at("s42", "thirty years late") + 0.3, headline("YEARS LATE", 1645, 190, 26, CREAM, rise=6), until=u42)

    # ============================================================ s43 (calm): he agreed
    u43 = nx("s43")
    cam.go(st("s43") + 0.3, frame_on(SHOP, 900, 520, 1.22), 0.9)
    cam.hold(u43 - 0.05, frame_on(SHOP, 900, 520, 1.26))
    SHOP.add(st("s43") - 0.3, actor(R("taniguchi", "uniform_again"), 900, 960, 660, seed=0.3, enter="fade", dur=0.5), until=u43 + 0.3)
    SHOP.add(st("s43") + 0.3, tag("HE AGREED", 1380, 380, 52, bg=MUSTARD, rot=-3, pin=True), until=u43)

    # ============================================================ s44 (calm, cut): the order rescinded; s45 (still) the turn
    t44 = st("s44")
    u45 = nx("s45")
    cam.cut(t44, frame_on(CLR, 1000, 560, 1.18))
    cam.hold(en("s44"), frame_on(CLR, 1000, 560, 1.22))
    cam.hold(u45, frame_on(CLR, 1000, 560, 1.22))
    CLR.add(t44, actor(R("taniguchi", "read_order"), 560, 960, 640, seed=0.4), until=u45)
    p09 = A.photo("p09")
    CLR.add(at("s44", "Major Taniguchi read") - 0.3, photo_card(p09, 1290, 480, 400, "drop", tilt=-1.5, hold=20, view=1.22),
            until=u45)  # hold: 1 (through s45)
    CLR.add(at("s44", "On the ninth"), tag("9 MAR 1974", 560, 200, 42, rot=-3, pin=True), until=u45)
    CLR.add(at("s44", "rescinding the 1944"), tag("1944 ORDER RESCINDED", 1290, 850, 34, bg=MUSTARD, rot=1), until=u45)
    CLR.add(at("s44", "Onoda was relieved"), tag("RELIEVED", 1290, 200, 48, bg=RUST, rgb=CREAM, rot=-2, pin=True), until=u45)

    # ============================================================ s46: weapons handed over
    u46 = nx("s46")
    cam.go(st("s46") + 0.5, frame_on(CLR, W / 2, H / 2, 1.16), 0.5)
    cam.hold(u46 - 0.1, frame_on(CLR, W / 2, H / 2, 1.2))
    CLR.add(st("s46") - 0.2, actor(R("onoda", "hand_over"), 560, 960, 600, seed=0.6), until=u46 + 0.3)
    for i, (prop, t, x, w) in enumerate([("rifle", at("s46", "his rifle"), 1000, 420), ("sword", at("s46", "his sword"), 1000, 380),
                                         ("ammo", at("s46", "around five hundred"), 1000, 260)]):
        CLR.add(t, sprite(P(prop), x - 120, 640 + i * 110, w, entry="slide_l", dur=0.5), until=u46)
    CLR.add(at("s46", "several hand grenades"), tag("RIFLE · SWORD · ~500 ROUNDS · GRENADES", 960, 200, 34, rot=-1), until=u46)
    p06 = A.photo("p06")
    CLR.add(at("s46", "The rifle was still") - 0.3, photo_card(p06, 1480, 470, 560, "slide_right", tilt=1.5, hold=4), until=u46)
    CLR.add(at("s46", "in working order"), tag("STILL IN WORKING ORDER", 1480, 790, 34, bg=MUSTARD, rot=2, pin=True), until=u46)

    # ============================================================ s47: Manila, the sword, the pardon
    u47 = nx("s47")
    cam.go(st("s47") + 0.8, frame_on(PALACE, W / 2, H / 2, 1.0), 1.8)
    cam.hold(u47 - 0.1, frame_on(PALACE, W / 2, H / 2, 1.04))
    PALACE.add(at("s47", "Two days later"), tag("MANILA, 2 DAYS LATER", 420, 200, 40, rot=-3, pin=True), until=u47)
    PALACE.add(at("s47", "he presented his sword") - 0.2, sprite(P("sword"), 420, 520, 460, path=curve((-200, 700), (420, 520), 0.2),
                                                               dur=1.0, rot=-10), until=u47)
    p10 = A.photo("p10")
    PALACE.add(at("s47", "President Ferdinand") - 0.4, photo_card(p10, 1300, 470, 760, "slide_up", tilt=-1, hold=5), until=u47)
    PALACE.add(at("s47", "President Ferdinand") + 0.4, tag("SWORD PRESENTED TO FERDINAND MARCOS", 1300, 870, 30, rot=1), until=u47)
    PALACE.add(at("s47", "who pardoned him"), stamp("PARDONED", 430, 790, 60), until=u47)

    # ============================================================ s48: 12 March 1974, Japan loses its mind
    u48 = nx("s48")
    cam.go(st("s48") + 0.9, frame_on(PORT, W / 2, H / 2, 1.0), 2.0)
    cam.hold(u48 - 0.1, frame_on(PORT, W / 2, H / 2, 1.05))
    PORT.add(st("s48") - 0.4, actor(R("onoda", "suit_crowd"), 900, 960, 600, motion=walk(-260, 0, 0, 1.6, bob=5)), until=nx("s49") + 0.3)
    PORT.add(st("s48") + 0.6, actor(R("crowd", "press"), 1500, 980, 420, flip=True, seed=0.5), until=st("s49") + 0.6)
    for i in range(4):
        PORT.add(at("s48", "and the country") + i * 0.35, sprite(P("flashbulbs"), 1350 + (i % 2) * 260, 560 - i * 30, 220,
                                                                  entry="pop", dur=0.25, exit_at=0.5), until=u48)
    PORT.add(at("s48", "He flew into Japan"), tag("12 MAR 1974", 420, 200, 42, rot=-3, pin=True), until=u48)
    PORT.add(at("s48", "the country lost"), tag("JAPAN LOSES ITS MIND", 420, 310, 40, bg=RUST, rgb=CREAM, rot=2), until=u48)

    # ============================================================ s49: crowds, front pages, a vanished Japan
    u49 = nx("s49")
    cam.go(st("s49") + 0.4, frame_on(PORT, 1100, 560, 1.12), 0.8)
    cam.hold(u49 - 0.1, frame_on(PORT, 1100, 560, 1.16))
    PORT.add(st("s49") + 0.1, actor(R("crowd", "airport"), 420, 990, 440, seed=0.7, enter="rise"), until=u49 + 0.3)
    PORT.add(at("s49", "He was on every"), sprite(P("tv_wall"), 1500, 420, 520, entry="pop"), until=u49)
    PORT.add(at("s49", "He was on every") + 0.3, sprite(P("newspapers"), 1300, 820, 300, entry="drop"), until=u49)
    PORT.add(at("s49", "He was on every") + 0.5, tag("EVERY FRONT PAGE", 1500, 120, 36, rot=-2, pin=True), until=u49)
    PORT.add(at("s49", "a vanished Japan"), tag("A VANISHED JAPAN", 760, 200, 38, bg=MUSTARD, rot=2), until=u49)
    PORT.add(at("s49", "Proof, to some"), tag("THE LOYALTY JAPAN HAD 'ABANDONED'", 760, 310, 32, rot=-1), until=u49)

    # ============================================================ s50 (calm): he hated it
    u50 = nx("s50")
    cam.go(st("s50") + 0.4, frame_on(PORT, W / 2, H / 2, 1.06), 0.6)
    cam.hold(u50 - 0.1, frame_on(PORT, W / 2, H / 2, 1.09))
    PORT.add(st("s50") - 0.2, window_light((1060, 220, 520, 520)), until=u50 + 0.3)
    PORT.add(st("s50") + 0.2, actor(R("onoda", "suit_crowd"), 1320, 960, 600, flip=True, tint=INK, idle=False,
                                    enter="fade"), until=u50 + 0.3)
    PORT.add(at("s50", "He hated it"), headline("HE HATED IT", 520, 540, 64, CREAM, rise=12), until=u50)

    # ============================================================ s51: a country that no longer existed
    u51 = nx("s51")
    cam.go(st("s51") + 0.6, frame_on(TOKYO, W / 2, H / 2, 1.0), 1.0)
    cam.hold(u51 - 0.1, frame_on(TOKYO, W / 2, H / 2, 1.05))
    TOKYO.add(st("s51") - 0.4, actor(R("onoda", "suit_crowd"), 1400, 960, 560, flip=True,
                                     motion=walk(300, -100, 0, 9.0, bob=5)), until=u51 + 0.3)
    TOKYO.add(at("s51", "He had left"), panel((240, 130, 360, 400), INK, 0.92), until=u51)
    TOKYO.add(at("s51", "He had left") + 0.2, headline("1944", 420, 230, 56, MUSTARD), until=u51)
    TOKYO.add(at("s51", "a militarised empire"), headline("A MILITARISED", 420, 300, 26, CREAM), until=u51)
    TOKYO.add(at("s51", "a militarised empire") + 0.3, headline("EMPIRE", 420, 340, 26, CREAM), until=u51)
    TOKYO.add(at("s51", "come back to"), panel((640, 130, 380, 400), CREAM, 0.95), until=u51)
    TOKYO.add(at("s51", "come back to") + 0.2, headline("1974", 830, 230, 56, RUST), until=u51)
    for i, (s_, ph) in enumerate([("PROSPEROUS", "a prosperous"), ("DEMOCRATIC", "democratic"),
                                  ("AMERICAN-ALLIED", "American-allied"), ("CONSUMER SOCIETY", "consumer society")]):
        TOKYO.add(at("s51", ph), headline(s_, 830, 300 + i * 40, 24, INK), until=u51)
    TOKYO.add(at("s51", "The country he had killed"), sprite(P("tv_wall"), 1700, 520, 300, entry="pop"), until=u51)
    t_ce = at("s51", "He was a celebrity")
    TOKYO.add(t_ce, tag("CELEBRITY", 380, 660, 36, rot=-2), until=u51)
    TOKYO.add(t_ce + 0.6, not_equal(610, 660), until=u51)
    TOKYO.add(t_ce + 0.9, tag("UNDERSTOOD", 840, 660, 36, bg=MUSTARD, rot=2), until=u51)

    # ============================================================ s52 (calm): a memoir; then gone
    u52 = nx("s52")
    cam.go(st("s52") + 0.5, frame_on(TOKYO, 960, 520, 1.12), 0.8)
    cam.hold(u52 - 0.1, frame_on(TOKYO, 960, 520, 1.15))
    TOKYO.add(st("s52") - 0.2, lambda c, a: c.drawRect(skia.Rect.MakeWH(W, H), fill(CREAM, 0.85 * smooth(a / 0.5))), until=u52 + 0.3)
    TOKYO.add(at("s52", "He wrote a memoir"), sprite(P("memoir"), 700, 560, 380, entry="rise"), until=u52)
    TOKYO.add(at("s52", "He wrote a memoir") + 0.4, headline("A MEMOIR", 700, 300, 52, INK), until=u52)
    TOKYO.add(at("s52", "And within"), sprite(P("suitcase"), 1250, 600, 300, entry="pop"), until=u52)
    TOKYO.add(at("s52", "he left"), tag("18 MONTHS LATER: GONE", 1250, 330, 38, bg=RUST, rgb=CREAM, rot=2), until=u52)

    # ============================================================ s53: Brazil, cattle, nobody knew him
    u53 = nx("s53")
    cam.go(st("s53") + 1.0, frame_on(RANCH, W / 2, H / 2, 1.0), 2.2)
    cam.hold(u53 - 0.1, frame_on(RANCH, W / 2 + 80, H / 2, 1.05))
    RANCH.add(st("s53") - 0.4, actor(R("onoda", "rancher"), 500, 900, 480, motion=walk(-300, 600, 0, 14.0, bob=6), seed=0.2),
              until=u53 + 0.3)
    RANCH.add(at("s53", "became a cattle"), sprite(P("cattle"), 1450, 820, 520, entry="rise"), until=u53)
    RANCH.add(at("s53", "In 1975"), tag("1975: BRAZIL", 420, 200, 44, rot=-3, pin=True), until=u53)
    RANCH.add(at("s53", "became a cattle"), tag("CATTLE RANCHER", 420, 300, 36, bg=MUSTARD, rot=2), until=u53)
    RANCH.add(at("s53", "He married"), tag("MARRIED", 420, 390, 36, rot=-2), until=u53)
    RANCH.add(at("s53", "nobody recognised"), tag("NOBODY RECOGNISED HIM", 1300, 260, 38, rot=1, pin=True), until=u53)

    # ============================================================ s54: the nature school
    u54 = nx("s54")
    cam.go(st("s54") + 1.0, frame_on(CAMP, W / 2, H / 2, 1.0), 2.2)
    cam.hold(u54 - 0.1, frame_on(CAMP, W / 2 - 40, H / 2, 1.05))
    CAMP.add(at("s54", "he set up") - 0.3, actor(R("onoda", "teacher_kids"), 760, 960, 440, seed=0.4), until=u54 + 0.3)
    CAMP.add(at("s54", "he set up") - 0.1, sprite(P("campfire"), 1000, 900, 180, entry="pop"), until=u54)
    CAMP.add(at("s54", "for children") - 0.3, actor(R("crowd", "kids_hike"), 1400, 960, 300, motion=walk(-200, 0, 0, 2.0, bob=5)),
             until=u54 + 0.3)
    CAMP.add(at("s54", "An organisation"), sprite(P("tent"), 1620, 640, 300, entry="pop"), until=u54)
    CAMP.add(at("s54", "He came back to Japan"), tag("BACK TO JAPAN, 1980S", 420, 200, 40, rot=-3, pin=True), until=u54)
    CAMP.add(at("s54", "a nature school"), tag("A NATURE SCHOOL", 420, 300, 40, bg=MUSTARD, rot=2), until=u54)
    for i, (s, ph) in enumerate([("CAMPING", "camping"), ("SURVIVAL", "survival"), ("SELF-RELIANCE", "self-reliance")]):
        CAMP.add(at("s54", ph), tag(s, 1250 + i * 0, 200 + i * 80, 32, rot=(-2, 2, -1)[i]), until=u54)

    # ============================================================ s55 (calm): back to the island, 1996
    u55 = nx("s55")
    cam.go(st("s55") + 1.0, frame_on(SCHOOL, W / 2, H / 2, 1.16), 2.4)
    cam.hold(u55 - 0.1, frame_on(SCHOOL, W / 2, H / 2, 1.2))
    SCHOOL.add(st("s55") - 0.2, actor(R("onoda", "old_walk"), 700, 960, 380, motion=walk(0, 140, 0, 10.0, bob=3)), until=u55 + 0.3)
    SCHOOL.add(at("s55", "In 1996"), tag("1996: BACK TO LUBANG", 420, 200, 40, rot=-3, pin=True), until=u55)
    p11 = A.photo("p11")
    SCHOOL.add(at("s55", "He met islanders") - 0.2, photo_card(p11, 1360, 430, 680, "slide_up", tilt=1.5, hold=12), until=u55)
    SCHOOL.add(at("s55", "ten thousand dollars"), tag("$10,000 TO A SCHOOL", 420, 310, 36, bg=MUSTARD, rot=2), until=u55)
    SCHOOL.add(at("s55", "a reconciliation") - 0.4, tag("NOT A RECONCILIATION", 1360, 860, 36, rot=-1), until=u55)

    # ============================================================ s56 (calm, set null): Tokyo, January 2014
    u56 = nx("s56")
    cam.go(st("s56") + 0.9, frame_on(PAPER, W / 2, H / 2, 1.0), 1.8)
    cam.hold(u56 - 0.1, frame_on(PAPER, W / 2, H / 2, 1.03))
    p12 = A.photo("p12")
    PAPER.add(st("s56") + 0.2, photo_card(p12, 1250, 520, 520, "pin", tilt=-1.5, hold=8), until=u56)
    PAPER.add(at("s56", "January 2014"), tag("JAN 2014, TOKYO", 560, 330, 44, rot=-3, pin=True), until=u56)
    PAPER.add(at("s56", "He was ninety-one") - 0.6, headline("1922 – 2014", 560, 480, 60, INK, f=title_font(64)), until=u56)
    PAPER.add(at("s56", "He was ninety-one"), headline("AGE 91", 560, 580, 44, RUST), until=u56)

    # ============================================================ s57 (calm, cut): Suzuki and the third thing
    u57 = nx("s57")
    cam.cut(st("s57"), frame_on(HIMAL, W / 2, H / 2, 1.0))
    cam.hold(en("s57"), frame_on(HIMAL, W / 2, H / 2 - 20, 1.04))
    HIMAL.add(st("s57") + 0.2, tag("NORIO SUZUKI", 420, 200, 44, rot=-3, pin=True), until=u57)
    HIMAL.add(at("s57", "found the panda") - 0.2, sprite(P("panda"), 420, 620, 300, entry="pop"), until=u57)
    HIMAL.add(at("s57", "found the panda") + 0.3, check(600, 480, 1.4, RUST), until=u57)
    HIMAL.add(at("s57", "He died in 1986"), tag("1986: AN AVALANCHE", 1300, 220, 40, bg=MUSTARD, rot=2), until=u57)
    HIMAL.add(at("s57", "still looking"), sprite(P("footprint"), 1300, 640, 300, entry="fade", dur=1.0), until=u57)
    HIMAL.add(at("s57", "still looking") + 0.3, tag("STILL LOOKING FOR THE THIRD", 1300, 860, 32, rot=-1), until=u57)

    # ============================================================ s58 (calm, set null): in his own terms, right
    u58 = nx("s58")
    cam.go(st("s58") + 0.9, frame_on(PAPER, W / 2, H / 2, 1.0), 1.8)
    cam.hold(u58 - 0.1, frame_on(PAPER, W / 2, H / 2, 1.03))
    p04 = A.photo("p04")
    ov.append((st("s58") + 0.3, nx("s59") + 0.4, photo_card(p04, 1520, 560, 400, "flip", tilt=1.5, hold=14)))  # hold: 1 (s59)
    PAPER.add(at("s58", "It is that Onoda"), headline("IN HIS OWN TERMS,", 560, 480, 52, INK, f=title_font(56)), until=u58)
    PAPER.add(at("s58", "right"), headline("RIGHT", 560, 600, 80, RUST), until=u58)

    # ============================================================ s59: held until relieved; 3,000 km away
    u59 = nx("s59")
    cam.go(st("s59") + 0.8, frame_on(MAP, MAPX - 150, 520, 1.0), 1.6)
    cam.hold(u59 - 0.1, frame_on(MAP, MAPX - 150, 520, 1.04))
    MAP.add(st("s59") - 0.2, actor(R("onoda", "alone_stand"), MAPX, MAPY + 30, 110, seed=0.1), until=u59 + 0.3)
    MAP.add(at("s59", "He was told"), headline("HOLD UNTIL RELIEVED", MAPX - 900, 330, 34, INK, "left"), until=u59)
    MAP.add(at("s59", "He held out"), equals(MAPX - 940, 390), until=u59)
    MAP.add(at("s59", "He held out") + 0.2, headline("HELD UNTIL RELIEVED", MAPX - 900, 410, 34, RUST, "left"), until=u59)
    TX, TY = MAPX + 60, 190  # far to the north: the bookshop
    MAP.add(at("s59", "and the one source"), actor(R("taniguchi", "bookseller"), TX, TY, 150, flip=True), until=u59 + 0.3)
    MAP.add(at("s59", "and the one source") + 0.2, tag("THE ONLY TRUSTED SOURCE", TX - 380, TY - 60, 30, bg=MUSTARD, rot=2),
            until=u59)
    MAP.add(at("s59", "three thousand"), ink(curve((TX, TY + 10), (MAPX, MAPY - 90), 0.2), RUST, 7, 1.2, dash=(18, 14)), until=u59)
    MAP.add(at("s59", "three thousand") + 0.6, tag("3,000 KM AWAY", MAPX - 420, (TY + MAPY) / 2, 38, rot=-2, pin=True), until=u59)
    MAP.add(at("s59", "three thousand") + 0.3, sprite(P("order"), MAPX + 90, MAPY - 30, 70, entry="pop", rot=-8), until=u59)

    # ============================================================ s60 (calm): a way in and no way out
    u60 = nx("s60")
    cam.go(st("s60") + 1.0, frame_on(CLR, W / 2, H / 2, 1.16), 2.2)
    cam.hold(u60 - 0.1, frame_on(CLR, W / 2, H / 2, 1.2))
    CLR.add(at("s60", "had a way in") - 0.3, sprite(P("door_one_handle"), 960, 560, 380, entry="fade", dur=0.8), until=u60)
    CLR.add(at("s60", "a way in"), tag("A WAY IN", 560, 360, 42, bg=MUSTARD, rot=-2), until=u60)
    CLR.add(at("s60", "no way out"), tag("NO WAY OUT", 1360, 360, 42, rot=2), until=u60)
    CLR.add(at("s60", "no way out") + 0.4, cross(1360, 360, 40, RUST, 12), until=u60)

    # ============================================================ s61 (calm): not mad; obedient
    u61 = nx("s61")
    cam.go(st("s61") + 0.6, frame_on(CLR, 1300, 520, 1.22), 1.0)
    cam.hold(u61 - 0.1, frame_on(CLR, 1300, 520, 1.26))
    CLR.add(st("s61") - 0.2, actor(R("onoda", "alone_stand"), 1360, 700, 300, seed=0.4, enter="fade"), until=u61 + 0.3)
    CLR.add(at("s61", "He was not mad"), tag("NOT MAD", 900, 320, 44, rot=-3), until=u61)
    CLR.add(at("s61", "He was obedient"), tag("OBEDIENT", 900, 440, 48, bg=RUST, rgb=CREAM, rot=2, pin=True), until=u61)

    # ============================================================ s62 (calm, cut): a bookseller had to get on a plane
    cam.cut(st("s62"), frame_on(SHOP, W / 2, H / 2, 1.0))
    cam.hold(en("s62"), frame_on(SHOP, W / 2, H / 2 - 10, 1.02))
    cam.hold(tl.total + 10, frame_on(SHOP, W / 2, H / 2 - 10, 1.02))
    SHOP.add(st("s62") - 0.01, open_door(1500, 330, 220, 440), until=tl.total + 10)


# ---------------------------------------------------------------- builders used only here

def glide(draw, t_move, a, b, dur, t_end=None):
    """Move a drawn card from offset a to offset b starting t_move (ages); a card may move, never rescale."""
    def d(c, age):
        q = in_out((age - t_move) / dur)
        c.save()
        c.translate(lerp(a[0], b[0], q), lerp(a[1], b[1], q))
        draw(c, age)
        c.restore()
    return d


def page_fly(x, y, i):
    """One blank calendar page tearing off and blowing away along an arc."""
    path = curve((x, y), (x + 900 + i * 60, y - 380 + i * 50), 0.3)

    def draw(c, age):
        p = in_out(age / 1.4)
        if p >= 1:
            return
        (px, py), ang = point_on(path, p)
        c.save()
        c.translate(px, py)
        c.rotate(ang + age * 200)
        c.scale(1 - 0.5 * p, 1 - 0.5 * p)
        r = skia.Rect.MakeXYWH(-55, -40, 110, 80)
        c.drawRect(r, fill(CREAM))
        c.drawRect(r, stroke(INK, 4))
        c.restore()
    return draw


def meter(x, y, dur):
    """A volume meter that climbs bar by bar."""
    def draw(c, age):
        n = int(clamp01(age / max(dur + 2.5, 1)) * 8) + 1
        for i in range(8):
            r = skia.Rect.MakeXYWH(x + i * 46, y - i * 14, 34, 40 + i * 14)
            c.drawRect(r, fill(RUST if i < n else CREAM, 0.95))
            c.drawRect(r, stroke(INK, 4))
    return draw


def day_counter(x, y, n):
    """Tear-off days 1..n: DAY 1, DAY 2 ... ending on DAY n."""
    def draw(c, age):
        k = min(n, 1 + int(age / 0.35))
        pw, ph = 220, 120
        r = skia.Rect.MakeXYWH(x - pw / 2, y - ph / 2, pw, ph)
        c.drawRect(r.makeOffset(6, 6), fill(INK))
        c.drawRect(r, fill(CREAM))
        c.drawRect(r, stroke(INK, 4))
        c.drawRect(skia.Rect.MakeXYWH(x - pw / 2, y - ph / 2, pw, 26), fill(RUST))
        text(c, f"DAY {k}", x, y + 32, head_font(48), INK, 1, "center")
    return draw


def plane_icon(path, dur):
    def draw(c, age):
        p = in_out(age / dur)
        if p <= 0 or p >= 1:
            return
        (x, y), ang = point_on(path, p)
        c.save()
        c.translate(x, y)
        c.rotate(ang)
        c.drawLine(-30, 0, 30, 0, stroke(INK, 8))
        c.drawPath(poly([(-4, 0), (-18, -28), (-9, -28), (14, 0), (-9, 28), (-18, 28)], True), fill(INK))
        c.restore()
    return draw


def cold_fire(img, x, y, w):
    """The campfire prop gone cold: drawn in flat grey ash tones (a prop, not a photograph)."""
    iw, ih = img.width(), img.height()
    h = w * ih / iw
    p = skia.Paint(AntiAlias=True)
    p.setColorFilter(skia.ColorFilters.Matrix([0.25, 0.45, 0.10, 0, 0.05,
                                               0.25, 0.45, 0.10, 0, 0.05,
                                               0.25, 0.45, 0.10, 0, 0.04,
                                               0, 0, 0, 1, 0]))

    def draw(c, age):
        c.drawImageRect(img, skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), SAMPLING, p)
    return draw
