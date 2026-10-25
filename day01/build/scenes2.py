"""Day 01, s10 to s65: the Hiroshima row, the journey, the Nagasaki row, the record, the return.

Same rules as scenes.py: photos are mounted prints with graphic panels beside them; graphics may
sit on generated stills; notes in build.json decide where the screen stays quiet.
"""
import math
import skia
from engine import *  # noqa: F401,F403
from scenes import SHOT, layout, pill, walker

PW = 520  # graphic panel width beside a photo


# ---------------------------------------------------------------- small builders

def row(stn, t, x, y, title, sub=None, ic=None, rgb=INK, size=24, sub_rgb=GREY, icon_rgb=None):
    """An icon, a small-caps line and an optional second line: one beat in a panel list."""
    tx = x
    if ic:
        stn.add(t, icon(ic, x + 30, y - 10, 0.62, icon_rgb or rgb, 2.5, 0.7))
        tx = x + 78
    stn.add(t + 0.15, label(title, tx, y, size, rgb, tracking=3))
    if sub:
        stn.add(t + 0.45, label(sub, tx, y + 30, 17, sub_rgb, tracking=2.5))


def big_number(stn, t, v0, v1, x, y, unit, sub=None, dur=1.2, fmt="{:,.0f}", size=100, rgb=INK):
    stn.add(t, counter(v0, v1, x, y, size, dur, fmt, rgb))
    w = text_width(fmt.format(v1), sans("Light", size)) + 24
    stn.add(t + 0.25, label(unit, x + w, y - size * 0.42, 24, rgb, tracking=3))
    if sub:
        stn.add(t + 0.5, label(sub, x + w, y - size * 0.42 + 30, 17, GREY, tracking=2.5))


def tick(x, y, s=16, rgb=INK, w=3.5, dur=0.35):
    return line_on(poly([(x - s, y), (x - s * 0.3, y + s * 0.7), (x + s, y - s * 0.8)]), rgb, w, dur)


def family(stn, t_him, x, y, names, t_names, ring=True, gap=110):
    """Him (red) and his family as plain circles. Never a face."""
    stn.add(t_him, dot(x, y, 12))
    for i, (nm, tn) in enumerate(zip(names, t_names)):
        cx = x + gap * (i + 1)
        stn.add(tn, line_on(poly([(x + gap * i + 16, y), (cx - 16, y)]), GREY, 2, 0.4))
        stn.add(tn + 0.2, ring_on(cx, y, 12 if i == 0 else 9, INK, 2.5, 0.5))
        stn.add(tn + 0.3, label(nm, cx, y + 44, 16, GREY, align="center", tracking=2))


def photo_card(stn, assets, sid, panel_w=PW, max_w=1250, today=None):
    img, matte, _ = assets.archival(sid)
    region, px = layout(img, panel_w, max_w)
    stn.add(-99, print_photo(img, region, matte))
    if today:  # honest context for a modern photograph, set in the panel, never on the photo
        stn.add(-99, label(today, region[0], region[1] - 22, 15, GREY, tracking=2.5, dur=0.01))
    return region, px


def plate_card(stn, assets, sid):
    stn.add(-99, print_plate(assets.generated(sid)[0], (0, 0, W, H)))


# ---------------------------------------------------------------- the film after the title

def build(tl, assets, ctx):
    at, st, en, nx = tl.at, tl.start, tl.end, tl.next_start
    S, MAP, H_, N_ = ctx["S"], ctx["MAP"], ctx["H_"], ctx["N_"]
    plan = []

    # ================================================= HIROSHIMA ROW (y ~ 4400)
    # ---- s10-s11: the drawing board, an ordinary life
    BD = S("s10", -1950, 4500, 1.1)
    plate_card(BD, assets, "s10")
    t = at("s10", "born in Nagasaki")
    x0, x1, ty = 200, 1720, 110
    BD.add(t - 0.3, lambda c, age: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(150, 50, 1770, 190), 10, 10),
                                               fill(PAPER_LIGHT, 0.86 * out_cubic(age / 0.4))))
    BD.add(t - 0.1, line_on(poly([(x0, ty), (x1, ty)]), INK, 2.5, 1.0))
    BD.add(t, dot(x0, ty, 9, INK))
    BD.add(t + 0.1, label("1916", x0, ty + 50, 22, INK, align="center", tracking=2))
    BD.add(t + 0.3, label("BORN · NAGASAKI", x0 + 40, ty - 22, 17, GREY, tracking=2.5))
    t = at("s10", "by 1945")
    BD.add(t, walker(poly([(x0, ty), (x0 + (x1 - x0) * 0.62, ty)]), 0, 1.4, 1.0, 10))
    BD.add(t + 1.3, label("1945", x0 + (x1 - x0) * 0.62, ty + 50, 22, RED, align="center", tracking=2))
    BD.add(at("s10", "does not end up"), label("AN ORDINARY LIFE", x0 + (x1 - x0) * 0.62 + 40, ty - 22, 17, GREY, tracking=2.5))
    t = at("s10", "A draughtsman")
    BD.add(t, pill("DRAUGHTSMAN", 300, 330, 24))
    BD.add(t + 0.5, pill("MITSUBISHI HEAVY INDUSTRIES", 300, 376, 17, GREY))
    BD.add(t + 0.2, line_on(curve((450, 400), (700, 560), 0.2), OFFWHITE, 2, 0.8, 0.9, (5, 6)))
    fx, fy = 1180, 330
    BD.add(at("s10", "A wife") - 0.3, lambda c, age, fx=fx, fy=fy: c.drawRRect(
        skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(fx - 60, fy - 60, fx + 330, fy + 90), 10, 10), fill(PAPER_LIGHT, 0.86 * out_cubic(age / 0.4))))
    family(BD, at("s10", "A wife") - 0.2, fx, fy, ["HISAKO", "SON"], [at("s10", "Hisako"), at("s10", "an infant son")])
    t = at("s10", "drew ships")
    BD.add(t, icon("ship", 1480, 640, 1.2, OFFWHITE, 3, 1.1))
    BD.add(at("s10", "went home"), icon("house", fx + 110, fy - 2, 2.1, GREY, 2, 1.0))
    # s11: sent to Hiroshima with two colleagues
    t = at("s11", "summer of 1945")
    BD.add(t, pill("SUMMER 1945", 300, 540, 24))
    t = at("s11", "sent him to Hiroshima")
    BD.add(t - 0.2, lambda c, age: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(240, 600, 760, 760), 10, 10),
                                               fill(PAPER_LIGHT, 0.86 * out_cubic(age / 0.4))))
    BD.add(t, dot(300, 700, 7, INK))
    BD.add(t + 0.1, label("NAGASAKI", 300, 742, 15, GREY, align="center", tracking=2))
    BD.add(t + 0.2, line_on(curve((310, 690), (680, 660), -0.2), RED, 2.5, 1.0, dash=(6, 6)))
    BD.add(t + 1.1, dot(690, 660, 8))
    BD.add(t + 1.1, label("HIROSHIMA", 690, 702, 15, INK, align="center", tracking=2))
    t = at("s11", "three months")
    for k in range(13):  # thirteen weeks
        BD.add(t + k * 0.08, dot(300 + k * 30, 795, 5, INK, 0.2))
    BD.add(t + 1.1, pill("3 MONTHS", 700, 806, 18))
    t = at("s11", "two colleagues")
    cx0, cy0 = 1180, 520
    BD.add(t - 0.3, lambda c, age, cx0=cx0, cy0=cy0: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(cx0 - 60, cy0 - 50, cx0 + 520, cy0 + 170), 10, 10),
                                               fill(PAPER_LIGHT, 0.86 * out_cubic(age / 0.4))))
    BD.add(t, dot(cx0, cy0, 11))
    BD.add(at("s11", "Akira Iwanaga") - 0.1, dot(cx0, cy0 + 56, 9, GREY))
    BD.add(at("s11", "Akira Iwanaga"), label("AKIRA IWANAGA", cx0 + 36, cy0 + 63, 18, INK, tracking=2.5))
    BD.add(at("s11", "Kuniyoshi Sato") - 0.1, dot(cx0, cy0 + 110, 9, GREY))
    BD.add(at("s11", "Kuniyoshi Sato"), label("KUNIYOSHI SATO", cx0 + 36, cy0 + 117, 18, INK, tracking=2.5))
    BD.add(t + 0.2, label("YAMAGUCHI", cx0 + 36, cy0 + 8, 18, RED, tracking=2.5))
    BD.add(at("s11", "finished the work"), tick(cx0 + 440, cy0 + 60, 20, INK))
    BD.add(at("s11", "August the sixth"), pill("6 AUG 1945 · DUE TO LEAVE", 1180, 800, 20))
    plan.append((BD, "s10", None))

    # ---- s12-s13: the hanko explained (note: let it sit; only the diagram builds)
    HJ = S("s12", 400, 4250, 0.95)
    region, px = photo_card(HJ, assets, "s12", 560, 1000)
    cx, cy = px + 120, 260
    t = at("s12", "A hanko is")
    cyl = skia.Path()
    cyl.addOval(skia.Rect.MakeLTRB(cx - 40, cy - 14, cx + 40, cy + 14))
    side = poly([(cx - 40, cy), (cx - 40, cy + 170)])
    side2 = poly([(cx + 40, cy), (cx + 40, cy + 170)])
    bot = arc_path(cx, cy + 170, 40, 0, 180)
    HJ.add(t, line_on(cyl, INK, 2.5, 0.5))
    HJ.add(t + 0.3, line_on(side, INK, 2.5, 0.5))
    HJ.add(t + 0.3, line_on(side2, INK, 2.5, 0.5))
    HJ.add(t + 0.7, lambda c, age, p=None, cx=cx, cy=cy: c.drawPath(partial(_ellipse_half(cx, cy + 170, 40, 14), smooth(age / 0.4)), stroke(INK, 2.5)))
    HJ.add(t + 0.8, label("A SMALL CYLINDER", cx + 80, cy + 30, 20, tracking=3))
    HJ.add(at("s12", "usually wood"), label("WOOD", cx + 80, cy + 70, 17, GREY, tracking=2.5))
    HJ.add(at("s12", "or ivory"), label("OR IVORY", cx + 150, cy + 70, 17, GREY, tracking=2.5))
    t = at("s12", "family name carved")
    for k in range(4):
        HJ.add(t + k * 0.12, line_on(poly([(cx - 22 + k * 14, cy + 160), (cx - 26 + k * 14, cy + 182)]), INK, 2, 0.2))
    HJ.add(t + 0.4, label("A FAMILY NAME, CARVED IN ONE END", cx + 80, cy + 172, 17, GREY, tracking=2.5))
    t = at("s12", "Pressed into red ink")
    HJ.add(t, lambda c, age, cx=cx, cy=cy: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - 70, cy + 230, 140, 26), 6, 6),
                                         fill(RED, 0.85 * min(1, age / 0.4))))
    HJ.add(t + 0.3, label("RED INK", cx + 90, cy + 252, 17, RED, tracking=2.5))
    t = at("s12", "functions as a signature")
    HJ.add(t - 0.2, seal(cx, cy + 340, 38))
    HJ.add(t + 0.2, label("=", cx + 62, cy + 354, 40, GREY, "Light", 0))
    HJ.add(t + 0.4, label("A SIGNATURE", cx + 100, cy + 350, 22, tracking=3))
    HJ.add(at("s12", "not optional"), label("NOT OPTIONAL IN 1945", cx + 100, cy + 380, 17, RED, tracking=2.5))
    docs = [("Travel documents", "TRAVEL"), ("company paperwork", "COMPANY"), ("bank forms", "BANK")]
    for k, (ph, nm) in enumerate(docs):
        t = at("s12", ph)
        HJ.add(t, icon("doc", px + 60 + k * 150, cy + 500, 0.7, INK, 2.5))
        HJ.add(t + 0.2, label(nm, px + 60 + k * 150, cy + 560, 15, GREY, align="center", tracking=2))
    t = at("s12", "None of them")
    for k in range(3):
        HJ.add(t + 0.3 + k * 0.2, cross(px + 60 + k * 150, cy + 500, 22, RED, 3.5))
    t = at("s13", "So he walked back")
    u = skia.Path()
    u.moveTo(px + 20, cy + 640)
    u.lineTo(px + 300, cy + 640)
    u.cubicTo(px + 380, cy + 640, px + 380, cy + 700, px + 300, cy + 700)
    u.lineTo(px + 120, cy + 700)
    HJ.add(t, walker(u, 0, 1.6, 1.0, 9))
    HJ.add(at("s13", "That detour"), label("THE DETOUR", px + 20, cy + 750, 24, RED, tracking=4))
    plan.append((HJ, "s12", None))

    # ---- s14: Hiroshima, 08:15 (cut)
    C1 = S("s14", 2750, 4600, 1.0)
    region, px = photo_card(C1, assets, "s14", 560)
    y = 160
    C1.add(st("s14"), label("08:15", px, y + 40, 96, INK, "Light", 0, dur=0.5))
    C1.add(st("s14") + 0.4, label("6 AUG 1945 · HIROSHIMA", px, y + 80, 18, GREY, tracking=2.5))
    row(C1, at("s14", "a B-29"), px, y + 170, "B-29 · ENOLA GAY", None, "plane")
    row(C1, at("s14", "uranium bomb"), px, y + 240, "URANIUM BOMB", "OVER THE CITY CENTRE")
    t = at("s14", "six hundred metres")
    gx, gy = px + 30, y + 470
    C1.add(t - 0.2, line_on(poly([(gx - 20, gy), (gx + 200, gy)]), INK, 2.5, 0.5))
    C1.add(t, line_on(poly([(gx + 90, gy), (gx + 90, gy - 140)]), RED, 2.5, 0.8, dash=(5, 5)))
    C1.add(t + 0.7, dot(gx + 90, gy - 140, 8))
    C1.add(t, counter(0, 600, gx + 230, gy - 60, 64, 1.0, "{:.0f}"))
    C1.add(t + 0.4, label("METRES ABOVE THE GROUND", gx + 230, gy - 20, 16, GREY, tracking=2.5))
    big_number(C1, at("s14", "fifteen kilotons"), 0, 15, px, y + 570, "KILOTONS", size=80)
    big_number(C1, at("s14", "fifteen thousand tons"), 0, 15000, px, y + 650, "TONS", "OF HIGH EXPLOSIVE", size=56)
    big_number(C1, at("s14", "a hundred and forty thousand"), 0, 140000, px, y + 730, "DEAD", "BY THE END OF 1945", 1.6, size=56, rgb=INK)
    plan.append((C1, "s14", "cut"))

    # ---- s15: three kilometres (rings)
    R1 = S("s15", 4750, 4250, 0.62)
    plate_card(R1, assets, "s15")
    t = st("s15")
    R1.add(t + 0.2, line_on(poly([(960, 540), (1500, 300)]), RED, 3, 1.0))
    R1.add(t + 1.0, dot(1500, 300, 14))
    R1.add(t + 1.0, pulse(1500, 300, 10, 90))
    R1.add(t + 1.2, pill("≈ 3 KM", 1540, 270, 30))
    R1.add(at("s15", "directly beneath"), pill("THE POINT DIRECTLY BENEATH", 760, 640, 22))
    plan.append((R1, "s15", None))

    # ---- s16-s17: the flash and after
    AF = S("s16", 6850, 4500, 1.05)
    region, px = photo_card(AF, assets, "s16", 560, 1150)
    y = 150
    t = at("s16", "two small objects")
    for k in range(2):
        AF.add(t + k * 0.3, lambda c, age, k=k, px=px, y=y: c.drawCircle(px + 30 + k * 26, y - 30 + 60 * smooth(age / 2.0), 6, fill(INK)))
    AF.add(t + 0.2, label("TWO SMALL OBJECTS", px + 90, y + 10, 20, tracking=3))
    t = at("s16", "Then the light")

    def flash(c, age, cx=px + 40, cy=y + 100):
        p = out_cubic(age / 0.5)
        for k in range(12):
            a = math.radians(k * 30)
            c.drawLine(cx + math.cos(a) * 12, cy + math.sin(a) * 12, cx + math.cos(a) * (12 + 22 * p),
                       cy + math.sin(a) * (12 + 22 * p), stroke(INK, 2.5))
        c.drawCircle(cx, cy, 8, fill(INK))
    AF.add(t, flash)
    AF.add(t + 0.2, label("THE LIGHT", px + 90, y + 108, 20, tracking=3))
    AF.add(at("s16", "magnesium flare"), label("LIKE A MAGNESIUM FLARE", px + 90, y + 138, 16, GREY, tracking=2.5))
    t = at("s16", "dropped to the ground")
    AF.add(t, line_on(poly([(px, y + 240), (px + 400, y + 240)]), INK, 2.5, 0.5))
    AF.add(t + 0.2, lambda c, age, px=px, y=y: c.drawCircle(px + 40, y + 180 + 50 * out_cubic(age / 0.5), 8, fill(RED)))
    AF.add(t + 0.3, label("DROPPED TO THE GROUND", px + 90, y + 220, 18, tracking=2.5))
    t = at("s16", "lifted him")
    AF.add(t, line_on(curve((px + 40, y + 228), (px + 330, y + 228), -0.4), RED, 2.5, 1.2, dash=(5, 5)))
    AF.add(t + 0.3, label("THE BLAST WAVE", px + 140, y + 290, 18, RED, tracking=2.5))
    AF.add(at("s16", "lost consciousness"), label("UNCONSCIOUS", px + 140, y + 320, 16, GREY, tracking=2.5))
    t = at("s17", "it was dark")
    AF.add(t, lambda c, age, px=px, y=y: c.drawRect(skia.Rect.MakeXYWH(px, y + 380, 420, 90), fill(INK, 0.85 * smooth(age / 1.0))))
    AF.add(t + 0.3, label("DARK", px + 24, y + 434, 30, OFFWHITE, tracking=5))
    AF.add(at("s17", "Not night"), label("NOT NIGHT", px + 170, y + 432, 20, (0.75, 0.72, 0.68), tracking=3))
    AF.add(at("s17", "dust and smoke"), label("DUST AND SMOKE BLOT OUT THE MORNING", px, y + 506, 15, GREY, tracking=2.2))
    for k, (ph, nm) in enumerate([("left side was badly", "LEFT SIDE · BADLY BURNED"),
                                  ("Both eardrums", "BOTH EARDRUMS · RUPTURED"),
                                  ("temporarily blinded", "TEMPORARILY BLINDED")]):
        t = at("s17", ph)
        AF.add(t, cross(px + 14, y + 590 + k * 58, 11, RED, 3))
        AF.add(t + 0.15, label(nm, px + 44, y + 600 + k * 58, 19, tracking=2.5))
    plan.append((AF, "s16", None))

    # ---- s18: through the city, looking for his colleagues
    KY = S("s18", 9300, 4300, 1.0)
    region, px = photo_card(KY, assets, "s18", 520, 1150)
    t = at("s18", "walked toward")
    path = skia.Path()
    path.moveTo(px + 20, 760)
    path.cubicTo(px + 160, 700, px + 120, 520, px + 300, 470)
    path.cubicTo(px + 420, 440, px + 360, 300, px + 440, 260)
    t_found = at("s18", "He found both men")
    KY.add(t, walker(path, 0, t_found - t - 0.2, 1.0))
    KY.add(t + 0.4, label("TOWARD THE CITY", px + 40, 820, 18, GREY, tracking=2.5))
    KY.add(at("s18", "looking for his colleagues"), label("LOOKING FOR IWANAGA AND SATO", px + 40, 850, 16, GREY, tracking=2.2))
    KY.add(t_found, dot(px + 410, 230, 9, GREY))
    KY.add(t_found + 0.2, dot(px + 470, 236, 9, GREY))
    KY.add(t_found + 0.6, label("BOTH ALIVE", px + 260, 190, 22, INK, tracking=3))
    KY.add(t_found + 0.8, tick(px + 230, 182, 14, INK))
    plan.append((KY, "s18", None))

    # ---- s19-s20: Tram 651, home (cut; no motion on the photo, never above 1080 tall)
    TR = S("s19", 11250, 4650, 0.8)
    img, matte, _ = assets.archival("s19")
    k = 1.0  # native size: the file is 500 px wide and softens visibly when enlarged
    dw, dh = img.width() * k, img.height() * k
    x0 = (W - (dw + 60 + 460)) / 2
    TR.add(-99, print_photo(img, (x0, (H - dh) / 2 - 40, dw, dh), matte))
    px = x0 + dw + 60
    t = at("s20", "He decided")
    TR.add(t, icon("house", px + 40, 520, 1.0, INK, 3))
    TR.add(t + 0.3, label("HOME", px + 100, 520, 30, INK, tracking=5))
    TR.add(t + 0.6, label("NAGASAKI · 400 KM", px + 100, 556, 17, RED, tracking=2.5))
    plan.append((TR, "s19", "cut"))

    # ---- s21-s22: the shelter, a weapon with no name
    SH = S("s21", 13500, 4400, 1.1)
    plate_card(SH, assets, "s21")
    SH.add(at("s21", "first night"), pill("THE NIGHT OF 6 AUG", 150, 150, 22))
    SH.add(at("s21", "air-raid shelter"), pill("AN AIR-RAID SHELTER", 150, 196, 17, GREY))
    t = at("s21", "Nobody in the shelter")
    for k in range(3):
        SH.add(t + k * 0.25, pill("?", 1450 + k * 70, 300 - k * 30, 34, RED))
    for k, (ph, nm) in enumerate([("no siren", "SIREN"), ("no formation", "FORMATION OF BOMBERS"), ("no sustained raid", "SUSTAINED RAID")]):
        t = at("s21", ph)
        SH.add(t, pill(nm, 150, 330 + k * 64, 22))
        SH.add(t + 0.35, strike(140, 160 + text_width(nm, sans("SemiBold", 22), 2.5) + 10, 322 + k * 64, RED, 3.5))
    for k, (ph, n, nm) in enumerate([("One aircraft", "1", "AIRCRAFT"), ("one flash", "1", "FLASH"), ("a city gone", "1", "CITY GONE")]):
        t = at("s21", ph)
        SH.add(t, pill(f"{n}  {nm}", 1350, 560 + k * 70, 30))
    t = at("s21", "People tried to explain")
    for k in range(4):
        SH.add(t + k * 0.5, pill("…", 820 + k * 120, 500 + (k % 2) * 50, 30, GREY))
    SH.add(at("s21", "none of the words fit"), pill("NONE OF THE WORDS FIT", 820, 640, 18))
    t = at("s22", "what an atomic bomb was")
    SH.add(t, pill("ATOMIC BOMB", 150, 640, 34))
    SH.add(at("s22", "did not exist"), strike(140, 170 + text_width("ATOMIC BOMB", sans("SemiBold", 34), 2.5), 630, RED, 4))
    SH.add(at("s22", "did not exist") + 0.4, pill("A TERM THAT DID NOT EXIST YET", 150, 690, 17, GREY))
    t = at("s22", "had no name")
    SH.add(t, lambda c, age: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(150, 760, 360, 70), 8, 8),
                                         dashed(stroke(OFFWHITE, 2.5, min(1, age / 0.5)), 8, 8)))
    SH.add(t + 0.5, pill("NO NAME", 180, 810, 18, GREY))
    plan.append((SH, "s21", None))

    # ---- s23-s24: to the station; the river; the bridges down
    GS = S("s23", 16000, 4500, 1.0)
    region, px = photo_card(GS, assets, "s23", 560, 1150)
    t = st("s23")
    GS.add(t + 0.1, label("7 AUG 1945", px, 170, 30, tracking=4))
    sx = px + 470
    GS.add(t + 0.3, icon("tram", sx, 270, 0.6, INK, 2.5))
    GS.add(t + 0.5, label("THE STATION", sx, 330, 15, GREY, align="center", tracking=2))
    trio = poly([(px + 20, 280), (sx - 60, 280)])
    GS.add(t + 0.4, walker(trio, 0, 2.6, 0.55, 8))
    GS.add(t + 0.6, dot(px + 20, 300, 7, GREY))
    GS.add(t + 0.7, dot(px + 44, 300, 7, GREY))
    t = at("s24", "still running")
    GS.add(t - 0.3, line_on(poly([(px, 420), (px + 500, 420)]), INK, 3, 0.8))
    for k in range(12):
        GS.add(t - 0.3 + k * 0.05, line_on(poly([(px + 10 + k * 42, 410), (px + 10 + k * 42, 430)]), INK, 2.5, 0.2))
    GS.add(t, label("THE TRAINS WERE STILL RUNNING", px, 470, 18, tracking=2.5))
    t = at("s24", "damaged but not destroyed")
    GS.add(t, lambda c, age, px=px: c.drawRect(skia.Rect.MakeXYWH(px + 200, 404, 90 * smooth(age / 0.4), 32), fill(PAPER_LIGHT)))
    GS.add(t + 0.4, line_on(poly([(px + 200, 420), (px + 290, 420)]), RED, 2.5, 0.6, dash=(6, 6)))
    GS.add(t + 0.5, label("DAMAGED, NOT DESTROYED", px, 500, 16, GREY, tracking=2.2))
    t = at("s24", "enormous numbers")

    def stream(c, age, x0=px, y0=560):
        n = min(60, int(age * 18))
        for k in range(n):
            u = ((age * 0.25 + k * 0.137) % 1.0)
            c.drawCircle(x0 + 20 + u * 470, y0 + (k * 37 % 90), 3.5, fill(GREY, 0.8 * min(1, (age - k / 18) * 3)))
    GS.add(t - 0.3, stream, until=at("s24", "To reach the station"))
    GS.add(t + 0.2, label("PEOPLE LEFT IN ENORMOUS NUMBERS", px, 690, 16, GREY, tracking=2.2))
    for k, ph in enumerate(["For relatives", "for hospitals", "for anywhere else"]):
        GS.add(at("s24", ph), label(["RELATIVES", "HOSPITALS", "ANYWHERE ELSE"][k], px + k * 150, 730, 17, INK, tracking=2.5))
    t = at("s24", "cross the river")
    wave = skia.Path()
    wave.moveTo(px, 840)
    for k in range(10):
        wave.quadTo(px + 25 + k * 50, 822 if k % 2 else 858, px + 50 + k * 50, 840)
    GS.add(t, line_on(wave, INK, 2.5, 1.0))
    GS.add(t + 0.4, label("THE RIVER", px, 890, 16, GREY, tracking=2.5))
    t = at("s24", "The bridges were down")
    GS.add(t, line_on(poly([(px + 150, 800), (px + 240, 790)]), INK, 4, 0.4))
    GS.add(t, line_on(poly([(px + 360, 790), (px + 270, 800)]), INK, 4, 0.4))
    GS.add(t + 0.4, cross(px + 255, 800, 12, RED, 3))
    GS.add(t + 0.5, label("BRIDGES DOWN", px + 300, 890, 16, RED, tracking=2.5))
    plan.append((GS, "s23", None))

    # ---- s25: the river (cut; deliberately empty: nothing added)
    RV = S("s25", 18400, 4400, 1.0)
    plate_card(RV, assets, "s25")
    plan.append((RV, "s25", "cut"))

    # ================================================= THE JOURNEY (s26-s27): the strongest visual
    JM = S("s26", 15800, 7150, 1.7)
    JM.add(-99, print_plate(assets.generated("s26")[0], (0, 0, W, H)))
    Hj, Nj = (677, 650), (347, 752)
    route = skia.Path()
    route.moveTo(*Hj)
    route.cubicTo(600, 680, 520, 690, 480, 690)    # west along the coast to the strait
    route.cubicTo(450, 692, 445, 700, 440, 712)    # across to Kyushu
    route.cubicTo(420, 735, 400, 745, 380, 748)
    route.cubicTo(366, 750, 356, 752, *Nj)
    t0, t1 = at("s26", "The journey"), en("s27") + 0.3
    JM.add(t0 - 0.4, dot(*Hj, 9))
    JM.add(t0 - 0.3, pill("HIROSHIMA", Hj[0] + 18, Hj[1] - 22, 16))
    JM.add(t0, dot(*Nj, 9, INK))
    JM.add(t0 + 0.1, pill("NAGASAKI", Nj[0] - 18, Nj[1] + 44, 16, align="right"))
    stations = [0.18, 0.36, 0.52, 0.68, 0.84]

    def journey(c, age, dur=t1 - t0):
        p = clamp01(age / dur)  # slow and even across both segments, as the note asks
        c.drawPath(partial(route, p), stroke(RED, 3.2))
        for q in stations:
            if p >= q:
                x, y = point_on(route, q)
                c.drawCircle(x, y, 4.5, fill(PAPER_LIGHT))
                c.drawCircle(x, y, 4.5, stroke(INK, 2))
        x, y = point_on(route, p)
        c.drawCircle(x, y, 7, fill(RED))
        c.drawCircle(x, y, 13, stroke(RED, 2, 0.6))
    JM.add(t0, journey)
    JM.add(at("s26", "four hundred kilometres") - 0.4, lambda c, age: c.drawRRect(
        skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(1040, 190, 1840, 860), 12, 12), fill(PAPER_LIGHT, 0.9 * out_cubic(age / 0.5))))
    big_number(JM, at("s26", "four hundred kilometres"), 0, 400, 1080, 300, "KM", "A LITTLE OVER", 1.4, "{:.0f}", 90)
    t = at("s26", "Today it takes")
    JM.add(t, icon("clock", 1110, 430, 0.6, INK, 2.5))
    JM.add(t + 0.2, label("TODAY · ABOUT 2 HOURS", 1160, 438, 20, tracking=3))
    t = at("s26", "In August 1945")
    JM.add(t, icon("clock", 1110, 500, 0.6, RED, 2.5))
    JM.add(t + 0.2, label("AUG 1945 · MOST OF A DAY", 1160, 508, 20, RED, tracking=3))
    JM.add(at("s26", "crowded trains"), label("CROWDED TRAINS", 1160, 540, 16, GREY, tracking=2.5))
    JM.add(at("s26", "running out of everything"), label("A COUNTRY RUNNING OUT OF EVERYTHING", 1160, 568, 16, GREY, tracking=2.2))
    for k, (ph, nm) in enumerate([("burned raw", "BURNED"), ("arms wrapped", "ARMS WRAPPED"), ("deaf in both ears", "DEAF")]):
        JM.add(at("s27", ph), pill(nm, [1080, 1230, 1450][k], 680, 17))
    for k, ph in enumerate(["Fields.", "Stations.", "Other passengers."]):
        JM.add(at("s27", ph), pill(ph.rstrip(".").upper(), [1080, 1230, 1400][k], 740, 16, GREY))
    JM.add(at("s27", "looked entirely normal"), label("A LANDSCAPE THAT LOOKED NORMAL", 1080, 790, 16, GREY, tracking=2.2))
    t = at("s27", "something that nobody else")
    JM.add(t, pill("WHAT ONLY HE KNEW", 1080, 836, 20, RED))
    plan.append((JM, "s26", None))

    # ================================================= NAGASAKI ROW (y ~ 9900), travelling back west
    # ---- s28-s30: bandages; home; the next morning
    BG = S("s28", 15900, 9900, 1.1)
    plate_card(BG, assets, "s28")
    BG.add(at("s28", "He reached Nagasaki"), pill("NAGASAKI · 8 AUG · LATE", 140, 140, 22))
    t = at("s28", "went to a hospital")
    BG.add(t, line_on(poly([(170, 250), (170, 300)]), RED, 6, 0.3))
    BG.add(t, line_on(poly([(145, 275), (195, 275)]), RED, 6, 0.3))
    BG.add(t + 0.2, pill("HOSPITAL", 230, 290, 20))
    BG.add(at("s28", "a former classmate"), pill("A DOCTOR, A FORMER CLASSMATE", 230, 334, 16, GREY))
    t = at("s28", "so heavily bandaged")
    for k in range(5):
        BG.add(t + k * 0.12, line_on(poly([(1400, 200 + k * 26), (1700, 214 + k * 26)]), OFFWHITE, 9, 0.5, 0.9))
    BG.add(t + 0.7, pill("FACE AND ARMS · BANDAGED", 1400, 380, 18))
    BG.add(at("s28", "did not recognise him"), pill("NOT RECOGNISED", 1400, 424, 18, RED))
    t = at("s28", "He went home")
    BG.add(t, icon("house", 1460, 560, 1.0, OFFWHITE, 3))
    BG.add(t + 0.3, pill("HOME", 1530, 572, 20))
    BG.add(at("s28", "looking at a ghost"), pill("HISAKO", 1530, 616, 16, GREY))
    t = at("s29", "He slept at home")
    BG.add(t, lambda c, age: (c.drawCircle(220, 520, 34 * out_cubic(age / 0.5), fill(OFFWHITE, 0.9)),
                              c.drawCircle(234, 510, 30 * out_cubic(age / 0.5), fill((0.35, 0.33, 0.31)))))
    BG.add(t + 0.3, pill("THE NIGHT OF 8 AUG", 280, 532, 20))
    t = at("s30", "morning of August the ninth")
    BG.add(t, icon("clock", 220, 680, 0.8, OFFWHITE, 3))
    BG.add(t + 0.3, pill("THE MORNING OF 9 AUG", 280, 692, 20))
    for k, nm in enumerate(["BURNED", "DEAF", "BANDAGED"]):
        BG.add(at("s30", ["badly burned", "deaf,", "bandaged from"][k]), pill(nm, 280 + k * 150, 750, 16, GREY))
    t = at("s30", "went in to work")
    BG.add(t, icon("office", 1460, 760, 0.9, OFFWHITE, 3))
    BG.add(t + 0.3, pill("TO WORK", 1530, 772, 20, RED))
    plan.append((BG, "s28", None))

    # ---- s31-s32: you went to work (modern photograph of the yard)
    MH = S("s31", 13400, 9800, 1.0)
    region, px = photo_card(MH, assets, "s31", 560, 1150, today="MHI NAGASAKI SHIPYARD · PRESENT DAY")
    y = 150
    t = at("s31", "foolishness")
    MH.add(t, label("FOOLISHNESS?", px, y, 28, GREY, tracking=4))
    MH.add(at("s31", "It was not."), strike(px - 6, px + text_width("FOOLISHNESS?", sans("SemiBold", 28), 4) + 6, y - 10, RED, 4))
    MH.add(at("s31", "you went to work"), label("AUG 1945: YOU WENT TO WORK", px, y + 60, 20, tracking=3))
    t = at("s31", "fourth year of total war")
    MH.add(t, counter(1, 4, px, y + 170, 80, 0.8, "{:.0f}"))
    MH.add(t + 0.2, label("TH YEAR OF TOTAL WAR", px + 50, y + 140, 18, tracking=2.5))
    row(MH, at("s31", "food was rationed"), px, y + 250, "FOOD RATIONED")
    row(MH, at("s31", "firebombed nightly"), px, y + 300, "CITIES FIREBOMBED NIGHTLY")
    row(MH, at("s31", "absence had to be explained"), px, y + 350, "ABSENCE HAD TO BE EXPLAINED", None, None, RED)
    t = at("s31", "away three months")
    MH.add(t, icon("calendar", px + 30, y + 440, 0.7, INK, 2.5))
    MH.add(t + 0.2, label("3 MONTHS AWAY ON COMPANY BUSINESS", px + 80, y + 450, 16, GREY, tracking=2.2))
    MH.add(at("s31", "he had to report"), label("A REPORT WAS DUE", px + 80, y + 480, 20, tracking=3))
    t = at("s32", "So he walked into")
    MH.add(t, icon("office", px + 400, y + 640, 0.9, INK, 2.5))
    MH.add(t, walker(poly([(px + 20, y + 670), (px + 340, y + 670)]), 0, 2.0))
    MH.add(at("s32", "his supervisor") - 0.2, dot(px + 400, y + 700, 9, GREY))
    MH.add(at("s32", "his supervisor"), label("HIS SUPERVISOR", px + 260, y + 750, 16, GREY, tracking=2.5))
    plan.append((MH, "s31", None))

    # ---- s33-s35: Sato's office
    OF = S("s33", 10900, 10000, 1.1)
    plate_card(OF, assets, "s33")
    t = at("s33", "The supervisor")
    OF.add(t, dot(640, 700, 13, GREY))
    OF.add(at("s33", "Sato"), pill("SATO", 600, 760, 20))
    OF.add(at("s33", "He listened to Yamaguchi"), dot(1280, 700, 13))
    OF.add(at("s33", "He listened to Yamaguchi") + 0.2, pill("YAMAGUCHI", 1230, 760, 20, RED))
    t = at("s33", "One aircraft")
    OF.add(t, pill("1 AIRCRAFT", 140, 150, 24))
    OF.add(at("s33", "one bomb"), pill("1 BOMB", 140, 200, 24))
    t = at("s33", "three hundred thousand")
    OF.add(t, lambda c, age: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(130, 240, 470, 120), 8, 8), fill(PAPER_LIGHT, 0.88 * min(1, age / 0.3))))
    OF.add(t, counter(0, 300000, 150, 330, 72, 1.4, "{:,.0f}"))
    OF.add(t + 0.4, label("PEOPLE · ONE CITY", 160, 350, 15, GREY, tracking=2.2))
    OF.add(at("s33", "in a single moment"), pill("IN A SINGLE MOMENT", 140, 410, 20, RED))
    t = at("s34", "out of his mind")
    OF.add(t, pill("OUT OF HIS MIND", 560, 600, 26))
    t = at("s35", "impossible")
    OF.add(t, lambda c, age: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(1330, 140, 470, 110), 8, 8), fill(PAPER_LIGHT, 0.88 * min(1, age / 0.3))))
    OF.add(t, serif_label("Impossible.", 1360, 220, 64, INK, "Italic"))
    OF.add(at("s35", "every standard he had"), pill("BY EVERY STANDARD HE HAD", 1340, 300, 16, GREY))
    for k, (ph, nm) in enumerate([("burned, deaf", "BURNED"), ("heavily bandaged", "BANDAGED"), ("visibly in shock", "IN SHOCK")]):
        OF.add(at("s35", ph), pill(nm, 1180 + k * 150, 840, 16, GREY))
    t = at("s35", "no bomb in the history")
    OF.add(t, pill("NO BOMB IN HISTORY HAD EVER DONE THIS", 1180, 900, 16))
    t = at("s35", "how a single bomb")
    OF.add(t, pill("1 BOMB", 140, 520, 28))
    OF.add(t + 0.4, line_on(poly([(300, 508), (400, 508)]), RED, 3, 0.4))
    OF.add(t + 0.7, pill("1 CITY ?", 420, 520, 28, RED))
    plan.append((OF, "s33", None))

    # ---- s36: the same white (cut; the centre of the film)
    plan.append((ctx["WHITE"], "s36", "cut"))

    # ---- s37: Nagasaki, 11:02 (cut)
    C2 = S("s37", 8500, 9800, 1.0)
    region, px = photo_card(C2, assets, "s37", 600)
    y = 160
    C2.add(st("s37"), label("11:02", px, y + 40, 96, INK, "Light", 0, dur=0.5))
    C2.add(st("s37") + 0.4, label("9 AUG 1945 · NAGASAKI", px, y + 80, 18, GREY, tracking=2.5))
    row(C2, at("s37", "a B-29 called Bockscar"), px, y + 170, "B-29 · BOCKSCAR", None, "plane")
    row(C2, at("s37", "plutonium bomb"), px, y + 240, "PLUTONIUM BOMB", "OVER THE URAKAMI VALLEY")
    t = at("s37", "The yield was higher")
    bx, by = px, y + 330
    C2.add(t, label("YIELD", bx, by, 16, GREY, tracking=2.5))
    for k, (nm, v, col_) in enumerate([("HIROSHIMA", 15, GREY), ("NAGASAKI", 21, INK)]):
        yy = by + 30 + k * 48
        C2.add(t + 0.2 + k * 0.5, lambda c, age, yy=yy, v=v, col_=col_, bx=bx: c.drawRect(
            skia.Rect.MakeXYWH(bx + 150, yy, v * 14 * out_cubic(age / 0.8), 26), fill(col_)))
        C2.add(t + 0.2 + k * 0.5, label(nm, bx, yy + 20, 15, col_, tracking=2))
        C2.add(t + 0.8 + k * 0.5, label(f"{v} KT", bx + 160 + v * 14, yy + 20, 17, col_, tracking=2))
    t = at("s37", "The hills around")
    hill = skia.Path()
    hill.moveTo(px, y + 560)
    hill.cubicTo(px + 80, y + 440, px + 160, y + 450, px + 220, y + 560)
    hill.cubicTo(px + 280, y + 450, px + 380, y + 440, px + 460, y + 560)
    C2.add(t, line_on(hill, INK, 2.5, 1.0))
    C2.add(t + 0.6, ring_on(px + 220, y + 540, 26, RED, 2.5, 0.6))
    C2.add(t + 0.8, label("THE HILLS CONTAINED THE BLAST", px, y + 600, 16, GREY, tracking=2.2))
    big_number(C2, at("s37", "Roughly seventy thousand"), 0, 70000, px, y + 720, "KILLED", None, 1.4, size=64)
    plan.append((C2, "s37", "cut"))

    # ---- s38: three kilometres. Again.
    R2 = S("s38", 6550, 10150, 0.62)
    plate_card(R2, assets, "s38")
    t = st("s38")
    R2.add(t + 0.2, line_on(poly([(960, 540), (1480, 330)]), RED, 3, 1.0))
    R2.add(t + 1.0, dot(1480, 330, 14))
    R2.add(t + 1.0, pulse(1480, 330, 10, 90))
    R2.add(t + 1.2, pill("≈ 3 KM", 1520, 300, 30))
    R2.add(at("s38", "Again"), pill("AGAIN", 1520, 380, 34, RED))
    plan.append((R2, "s38", None))

    # ---- s39-s40: the second blast
    TP = S("s39", 4550, 9800, 1.0)
    region, px = photo_card(TP, assets, "s39", 540, 1150)
    y = 160
    t = at("s39", "The office windows")
    wx, wy = px + 60, y + 40
    TP.add(t, lambda c, age, wx=wx, wy=wy: c.drawRect(skia.Rect.MakeXYWH(wx - 50, wy - 40, 100, 80), stroke(INK, 3, min(1, age / 0.3))))
    TP.add(t, line_on(poly([(wx, wy - 40), (wx, wy + 40)]), INK, 2.5, 0.3))
    TP.add(t + 0.4, line_on(poly([(wx - 30, wy - 20), (wx + 10, wy + 10), (wx - 10, wy + 30)]), RED, 2.5, 0.3))
    TP.add(t + 0.5, label("THE WINDOWS BLEW IN", px + 140, wy + 10, 20, tracking=3))
    t = at("s39", "second time in three days")
    TP.add(t - 0.2, line_on(poly([(px, y + 200), (px + 440, y + 200)]), INK, 2.5, 0.6))
    TP.add(t, dot(px, y + 200, 9, RED))
    TP.add(t + 0.1, label("6 AUG", px, y + 240, 16, GREY, align="center", tracking=2))
    TP.add(t + 0.5, dot(px + 440, y + 200, 9, RED))
    TP.add(t + 0.6, label("9 AUG", px + 440, y + 240, 16, GREY, align="center", tracking=2))
    TP.add(t + 0.7, label("THROWN TO THE FLOOR · TWICE", px + 40, y + 180, 16, INK, tracking=2.2))
    TP.add(at("s39", "second atomic weapon"), label("THE SECOND ATOMIC WEAPON EVER USED", px, y + 310, 16, GREY, tracking=2.2))
    TP.add(at("s39", "trying to convince"), label("WHILE EXPLAINING THE FIRST", px, y + 345, 18, RED, tracking=2.5))
    t = at("s40", "His bandages")
    for k in range(4):
        TP.add(t + k * 0.1, lambda c, age, k=k, px=px, y=y: c.drawLine(px + 20 + k * 30 + 40 * out_cubic(age / 0.6), y + 450 + k * 8 - 30 * out_cubic(age / 0.6),
                                                          px + 120 + k * 30 + 60 * out_cubic(age / 0.6), y + 470 + k * 8 - 50 * out_cubic(age / 0.6),
                                                          stroke(GREY, 7, 1 - 0.5 * clamp01(age / 1.2))))
    TP.add(t + 0.3, label("BANDAGES TORN AWAY", px, y + 530, 20, tracking=3))
    t = at("s40", "this time he knew")
    TP.add(t, dot(px + 20, y + 640, 11))
    TP.add(t + 0.3, label("THIS TIME HE KNEW", px + 50, y + 650, 24, RED, tracking=3))
    plan.append((TP, "s39", None))

    # ---- s41-s43: the search; out for ointment; the causal turn (hold through s43, no cut)
    CT = S("s41", 2050, 10050, 1.05)
    region, px = photo_card(CT, assets, "s41", 600)
    y = 150
    family(CT, at("s41", "Hisako and their infant son") - 0.2, px + 20, y, ["HISAKO", "KATSUTOSHI"],
           [at("s41", "Hisako"), at("s41", "Katsutoshi")])
    CT.add(at("s41", "at home when"), icon("house", px + 400, y - 4, 0.8, INK, 2.5))
    t = at("s41", "searched the ruins")
    gx, gy = px + 10, y + 120
    for k in range(5):
        CT.add(t - 0.4 + k * 0.06, line_on(poly([(gx, gy + k * 50), (gx + 440, gy + k * 50)]), GREY, 1.5, 0.4, 0.7))
        CT.add(t - 0.4 + k * 0.06, line_on(poly([(gx + k * 110, gy), (gx + k * 110, gy + 200)]), GREY, 1.5, 0.4, 0.7))
    zig = poly([(gx, gy), (gx + 440, gy), (gx + 440, gy + 50), (gx, gy + 50), (gx, gy + 100), (gx + 440, gy + 100),
                (gx + 440, gy + 150), (gx, gy + 150), (gx, gy + 200), (gx + 330, gy + 200)])
    CT.add(t, walker(zig, 0, at("s42", "They were.") - t - 0.2, 1.0, 8))
    CT.add(t + 0.4, label("URAKAMI · STREET BY STREET", gx, gy + 250, 16, GREY, tracking=2.2))
    t = at("s42", "They were.")
    CT.add(t, serif_label("They were.", px, y + 445, 56, INK))
    CT.add(at("s42", "burn ointment"), label("OUT LOOKING FOR BURN OINTMENT", px, y + 490, 16, GREY, tracking=2.2))
    t = at("s42", "black rain")

    def rain(c, age, x0=px + 280, y0=y + 530):
        for k in range(26):
            u = (age * 0.6 + k * 0.173) % 1.0
            xx = x0 + (k * 53 % 220)
            c.drawLine(xx, y0 + u * 90, xx - 3, y0 + u * 90 + 12, stroke(INK, 2, 0.7 * min(1, age)))
    CT.add(t, rain, until=en("s42") + 0.3)
    CT.add(t + 0.3, label("BLACK RAIN", px, y + 575, 18, INK, tracking=3))
    CT.add(at("s42", "but they were alive"), label("ALIVE", px, y + 615, 26, RED, tracking=5))
    chain = ["1ST BOMB", "HIS BURNS", "OINTMENT", "OUT OF THE HOUSE", "ALIVE"]
    t = st("s43")
    for k, nm in enumerate(chain):
        yy = y + 680 + (k // 3) * 46
        xx = px + [0, 190, 380, 0, 260][k]
        CT.add(t + k * 0.6, label(nm, xx, yy, 16, RED if k == len(chain) - 1 else INK, tracking=2))
        if k % 3:
            CT.add(t + k * 0.6 - 0.2, line_on(poly([(xx - 44, yy - 6), (xx - 14, yy - 6)]), GREY, 2, 0.2))
    plan.append((CT, "s41", None))

    # ---- s44-s46: the war ends; sixty-five years (cut)
    MS = S("s44", -550, 9800, 1.0)
    region, px = photo_card(MS, assets, "s44", 520, 1150)
    y = 170
    MS.add(st("s44"), label("15 AUG 1945", px, y, 36, tracking=4))
    MS.add(st("s44") + 0.4, label("THE WAR ENDS", px, y + 40, 20, RED, tracking=3))
    t = at("s45", "sixty-five years")
    MS.add(t - 0.6, line_on(poly([(px, y + 205), (px + 460, y + 205)]), INK, 2.5, 1.2))
    MS.add(t - 0.6, dot(px, y + 205, 8, INK))
    MS.add(t - 0.5, label("1945", px, y + 240, 16, GREY, align="center", tracking=2))
    MS.add(t + 0.6, dot(px + 460, y + 205, 8, INK))
    MS.add(t + 0.6, label("2010", px + 460, y + 240, 16, GREY, align="center", tracking=2))
    MS.add(t, counter(0, 65, px + 140, y + 185, 64, 1.2, "{:.0f}"))
    MS.add(t + 0.3, label("YEARS", px + 230, y + 175, 18, tracking=3))
    MS.add(at("s45", "end at Nagasaki"), label("MOST VERSIONS END HERE", px, y + 88, 16, GREY, tracking=2.2))
    for k, (ph, nm) in enumerate([("He was ill", "ILL FOR A LONG TIME"), ("His hair fell out", "HIS HAIR FELL OUT"),
                                  ("His burns took years", "BURNS: YEARS TO HEAL"), ("deaf in one ear", "DEAF IN ONE EAR, FOR LIFE")]):
        MS.add(at("s46", ph), label(nm, px, y + 320 + k * 52, 19, tracking=2.5))
        MS.add(at("s46", ph), dot(px - 22, y + 313 + k * 52, 5, GREY))
    plan.append((MS, "s44", "cut"))

    # ---- s47: something very ordinary (modern photograph)
    YD = S("s47", -3050, 10050, 1.05)
    region, px = photo_card(YD, assets, "s47", 520, 1200, today="MHI NAGASAKI SHIPYARD · PRESENT DAY")
    y = 150
    YD.add(at("s47", "very ordinary"), label("SOMETHING VERY ORDINARY", px, y, 20, GREY, tracking=3))
    for k, (ph, nm, sub) in enumerate([("translator", "TRANSLATOR", "US OCCUPATION FORCES"),
                                       ("taught at a junior", "TEACHER", "JUNIOR HIGH SCHOOL"),
                                       ("two daughters", "TWO DAUGHTERS", "EARLY 1950s"),
                                       ("returned to Mitsubishi", "MITSUBISHI", "BACK AT THE YARD")]):
        row(YD, at("s47", ph), px, y + 80 + k * 100, nm, sub)
    t = at("s47", "two daughters")
    YD.add(t + 0.3, ring_on(px + 360, y + 262, 8, INK, 2.5, 0.4))
    YD.add(t + 0.5, ring_on(px + 390, y + 262, 8, INK, 2.5, 0.4))
    t = at("s47", "He drew ships again")
    YD.add(t, icon("ship", px + 200, y + 560, 1.3, INK, 3, 1.2))
    YD.add(t + 0.5, label("HE DREW SHIPS AGAIN", px, y + 640, 22, RED, tracking=3))
    plan.append((YD, "s47", None))

    # ---- s48-s50: the certificate that named one city
    CF = S("s48", -5650, 9800, 1.1)
    plate_card(CF, assets, "s48")
    CF.add(at("s48", "In 1957"), pill("1957", 1350, 150, 40))
    t = at("s48", "the hibakusha")
    CF.add(t, pill("HIBAKUSHA", 1350, 230, 26))
    CF.add(t + 0.4, pill("SURVIVORS OF THE BOMBINGS", 1350, 274, 16, GREY))
    CF.add(at("s48", "issued them certificates"), pill("A CERTIFICATE", 1350, 330, 20))
    bx, by = 1350, 460

    def box(c, age, x, y, ticked_at=None, now=None):
        c.drawRect(skia.Rect.MakeXYWH(x, y - 26, 32, 32), fill(PAPER_LIGHT, 0.95 * min(1, age / 0.3)))
        c.drawRect(skia.Rect.MakeXYWH(x, y - 26, 32, 32), stroke(INK, 2.5, min(1, age / 0.3)))
    t = at("s48", "named Nagasaki")
    CF.add(t, lambda c, age, bx=bx, by=by: box(c, age, bx, by))
    CF.add(t + 0.2, pill("NAGASAKI", bx + 50, by + 2, 24))
    CF.add(t + 0.5, tick(bx + 16, by - 12, 14, RED))
    t = at("s48", "Hiroshima was not")
    CF.add(t, lambda c, age, bx=bx, by=by: box(c, age, bx, by + 70))
    CF.add(t + 0.2, pill("HIROSHIMA", bx + 50, by + 72, 24, GREY))
    CF.add(at("s48", "Only Nagasaki"), pill("ONLY NAGASAKI", bx + 50, by + 130, 16, RED))
    t = at("s49", "Not for fifty years")
    CF.add(t, lambda c, age: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(130, 120, 360, 130), 8, 8), fill(PAPER_LIGHT, 0.88 * min(1, age / 0.3))))
    CF.add(t, counter(0, 50, 150, 220, 90, 1.2, "{:.0f}"))
    CF.add(t + 0.3, label("YEARS UNCORRECTED", 280, 200, 16, GREY, tracking=2.2))
    CF.add(at("s49", "He did not correct"), pill("HE DID NOT CORRECT IT", 130, 300, 20))
    t = at("s50", "practical")
    CF.add(t, pill("THE PRACTICAL REASON", 130, 420, 18, GREY))
    CF.add(at("s50", "medical care"), pill("MEDICAL CARE ✓", 130, 470, 20))
    CF.add(at("s50", "an allowance"), pill("AN ALLOWANCE ✓", 130, 516, 20))
    CF.add(at("s50", "changed nothing on paper"), pill("+ HIROSHIMA = NO CHANGE ON PAPER", 130, 562, 18))
    CF.add(at("s50", "the larger reason"), pill("THE LARGER REASON", 130, 660, 18, GREY))
    CF.add(at("s50", "comparatively well"), pill("HE FELT COMPARATIVELY WELL", 130, 708, 20))
    CF.add(at("s50", "He had survived"), pill("SURVIVED", 130, 756, 18))
    CF.add(at("s50", "raised children"), pill("RAISED CHILDREN", 280, 756, 18))
    CF.add(at("s50", "far worse off"), pill("OTHERS WERE FAR WORSE OFF", 130, 804, 18, RED))
    plan.append((CF, "s48", None))

    # ---- s51-s53: stigma, silence, loss
    RM = S("s51", -8250, 10050, 1.1)
    plate_card(RM, assets, "s51")
    RM.add(at("s51", "outside Japan"), pill("OUTSIDE JAPAN, LITTLE KNOWN", 1180, 140, 16, GREY))
    RM.add(at("s51", "carried a stigma"), pill("STIGMA", 1180, 200, 40))
    RM.add(at("s51", "treated as contaminated"), pill("TREATED AS CONTAMINATED", 1180, 260, 20))
    for k, (ph, nm) in enumerate([("Refused jobs", "JOBS"), ("refused marriages", "MARRIAGES")]):
        t = at("s51", ph)
        RM.add(t, pill(nm, 1180 + k * 160, 330, 22))
        RM.add(t + 0.3, strike(1170 + k * 160, 1196 + k * 160 + text_width(nm, sans("SemiBold", 22), 2.5), 320, RED, 3.5))
    RM.add(at("s51", "passing something on"), pill("CHILDREN?", 1500, 330, 22, RED))
    RM.add(at("s51", "For decades"), pill("FOR DECADES, MANY SAID NOTHING", 1180, 420, 18))
    t = at("s51", "not modesty")
    RM.add(t, pill("MODESTY", 1180, 480, 22, GREY))
    RM.add(t + 0.4, strike(1170, 1300, 470, RED, 3.5))
    RM.add(at("s51", "self-protection"), pill("SELF-PROTECTION", 1330, 480, 22, RED))
    t = at("s52", "nearly ninety")
    RM.add(t - 1.2, counter(30, 89, 1180, 640, 90, 1.4, "{:.0f}", OFFWHITE))
    RM.add(t + 0.2, pill("NEARLY NINETY", 1320, 616, 20))
    RM.add(at("s52", "stayed quiet"), pill("QUIET", 1320, 660, 16, GREY))
    t = at("s53", "was his son")
    fx, fy = 220, 180
    RM.add(t - 0.3, lambda c, age: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(120, 110, 700, 560), 10, 10),
                                               fill(PAPER_LIGHT, 0.88 * out_cubic(age / 0.4))))
    for k, (ph, nm, l1, l2) in enumerate([("Katsutoshi", "KATSUTOSHI", "SON", "DIED 2005 · AGE 59"),
                                          ("Hisako died", "HISAKO", "WIFE", "DIED 2008 · AGE 88")]):
        tt = at("s53", ph)
        yy = fy + k * 170
        RM.add(tt, ring_on(fx, yy, 22, INK, 3, 0.6))
        RM.add(tt + 0.2, label(nm, fx + 50, yy - 4, 24, tracking=3))
        RM.add(tt + 0.4, label(l1, fx + 50, yy + 26, 15, GREY, tracking=2.5))
        RM.add(tt + 0.8, label(l2, fx + 50, yy + 56, 18, INK, tracking=2.5))
    RM.add(at("s53", "cancer in 2005"), label("CANCER", fx + 50, fy + 86, 15, GREY, tracking=2.5))
    RM.add(at("s53", "liver and kidney"), label("LIVER AND KIDNEY CANCER", fx + 50, fy + 256, 15, GREY, tracking=2.5))
    RM.add(at("s53", "Both had been exposed"), label("BOTH EXPOSED AT NAGASAKI", fx - 30, fy + 340, 20, RED, tracking=3))
    plan.append((RM, "s51", None))

    # ---- s54-s57: he began to talk; the record names both
    NB = S("s54", -10850, 9800, 1.1)
    plate_card(NB, assets, "s54")
    NB.add(st("s54"), pill("HE BEGAN TO TALK", 140, 140, 30, RED))
    for k, (ph, nm, sub) in enumerate([("wrote a book", "A BOOK", "IN HIS EIGHTIES"),
                                       ("a documentary", "A DOCUMENTARY", "NIJU HIBAKUSHA · DOUBLE SURVIVORS"),
                                       ("United Nations", "THE UNITED NATIONS", "HE TRAVELLED THERE TO SPEAK"),
                                       ("He gave interviews", "INTERVIEWS", None),
                                       ("He wrote tanka", "TANKA", "SHORT JAPANESE POEMS")]):
        t = at("s55", ph)
        NB.add(t, pill(nm, 140, 230 + k * 80, 22))
        if sub:
            NB.add(t + 0.4, pill(sub, 140, 268 + k * 80, 14, GREY))
    t = at("s56", "In March 2009")
    NB.add(t, lambda c, age: c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(1240, 120, 1800, 620), 10, 10),
                                         fill(PAPER_LIGHT, 0.9 * out_cubic(age / 0.4))))
    NB.add(t + 0.1, label("MARCH 2009 · AGE 93", 1280, 190, 22, tracking=3))
    bx, by = 1290, 300
    for k, nm in enumerate(["NAGASAKI", "HIROSHIMA"]):
        NB.add(t + 0.3, lambda c, age, k=k, bx=bx, by=by: c.drawRect(skia.Rect.MakeXYWH(bx, by - 26 + k * 70, 32, 32), stroke(INK, 2.5, min(1, age / 0.3))))
        NB.add(t + 0.3, label(nm, bx + 54, by + 2 + k * 70, 24, tracking=3))
    NB.add(t + 0.5, tick(bx + 16, by - 12, 14, RED))
    NB.add(at("s56", "certified him for Hiroshima"), tick(bx + 16, by + 58, 14, RED))
    t = at("s56", "the only person on record")
    NB.add(t, seal(1340, 500, 40))
    NB.add(t + 0.3, label("OFFICIALLY RECOGNISED", 1400, 494, 18, tracking=2.5))
    NB.add(t + 0.5, label("A SURVIVOR OF BOTH", 1400, 524, 18, RED, tracking=2.5))
    t = at("s57", "official record")
    NB.add(t, pill("IN THE OFFICIAL RECORD", 140, 700, 20))
    NB.add(at("s57", "younger people"), pill("SO IT COULD TELL YOUNGER PEOPLE", 140, 746, 18, GREY))
    NB.add(at("s57", "after he was gone"), pill("AFTER HE WAS GONE", 140, 792, 18, RED))
    plan.append((NB, "s54", None))

    # ---- s58: quote card (cut; a paraphrase, so no quotation marks)
    QT = S("s58", -13350, 10050, 1.0)
    qbg = assets.generated("s54")[1]
    lum = 0.299 * qbg[0] + 0.587 * qbg[1] + 0.114 * qbg[2]
    qink = INK if lum > 0.5 else OFFWHITE
    QT.add(-99, lambda c, age, qbg=qbg: c.drawRect(skia.Rect.MakeWH(W, H), fill(qbg)))
    q = SHOT["s58"]
    lines = ["What he hated about the atomic bomb,", "he said, was what it does", "to the dignity of human beings."]
    t = at("s58", "What he hated")
    for k, ln in enumerate(lines):
        QT.add(t + k * 0.9, serif_label(ln, W / 2, 420 + k * 86, 60, qink, "Italic", align="center", dur=0.9))
    QT.add(t + 2.8, line_on(poly([(W / 2 - 80, 700), (W / 2 + 80, 700)]), RED, 2.5, 0.6))
    QT.add(t + 3.1, label(q["attribution"].upper(), W / 2, 750, 20, qink, align="center", tracking=4))
    plan.append((QT, "s58", "cut"))

    # ---- s59-s60: 165 people; the record names one (cut)
    PS = S("s59", -15850, 9800, 1.0)
    region, px = photo_card(PS, assets, "s59", 620, 1150, today="NAGASAKI PEACE PARK · 2019")
    t = at("s59", "An estimated 165")
    gx, gy = px + 10, 170
    for k in range(165):
        r_, c_ = divmod(k, 15)
        PS.add(t + k * 0.012, dot(gx + c_ * 34, gy + r_ * 34, 6, RED if k == 0 else GREY, 0.2))
    PS.add(t + 0.3, counter(0, 165, gx, gy + 440, 72, 2.0, "{:.0f}"))
    PS.add(t + 0.6, label("EXPERIENCED BOTH BOMBINGS", gx + 140, gy + 412, 16, GREY, tracking=2.2))
    t = at("s59", "the only one the record names")
    PS.add(t, ring_on(gx, gy, 16, RED, 2.5, 0.5))
    PS.add(t + 0.3, label("1 NAMED IN THE RECORD", gx + 140, gy + 442, 18, RED, tracking=2.5))
    t = at("s60", "the fourth of January")
    PS.add(t, label("4 JAN 2010 · NAGASAKI", gx, gy + 560, 24, tracking=3))
    PS.add(at("s60", "stomach cancer"), label("STOMACH CANCER", gx, gy + 596, 16, GREY, tracking=2.5))
    PS.add(at("s60", "ninety-three years old"), serif_label("1916 – 2010", gx, gy + 680, 48, INK))
    plan.append((PS, "s59", "cut"))

    # ---- s61-s64: not luck (modern photograph)
    DM = S("s61", -18350, 10050, 1.1)
    region, px = photo_card(DM, assets, "s61", 560, 1150, today="ATOMIC BOMB DOME, HIROSHIMA · 2018")
    y = 140
    t = at("s61", "a piece of trivia")
    DM.add(t, label("THE TRIVIA VERSION", px, y, 22, GREY, tracking=3))
    DM.add(at("s61", "The unluckiest"), label("UNLUCKIEST", px, y + 50, 26, tracking=4))
    DM.add(at("s61", "or the luckiest"), label("LUCKIEST", px + 250, y + 50, 26, tracking=4))
    DM.add(at("s61", "ninety seconds"), label("~90 SECONDS · ENDS AT NAGASAKI", px, y + 90, 16, GREY, tracking=2.2))
    t = at("s62", "That version")
    DM.add(t + 0.3, strike(px - 6, px + 230, y + 40, RED, 4))
    DM.add(t + 0.6, strike(px + 244, px + 420, y + 40, RED, 4))
    DM.add(at("s63", "not luck"), label("NOT LUCK, EITHER WAY", px, y + 170, 22, RED, tracking=3))
    for k, (ph, nm, why) in enumerate([("He was in Hiroshima because", "HIROSHIMA", "A COMPANY SENT HIM"),
                                       ("He was in a field", "A FIELD", "HE HAD FORGOTTEN A STAMP"),
                                       ("He was in Nagasaki three days", "NAGASAKI", "IT WAS HOME"),
                                       ("reported to his office", "THE OFFICE", "HE REPORTED FOR WORK")]):
        t = at("s63", ph)
        yy = y + 250 + k * 70
        DM.add(t, label(nm, px, yy, 22, tracking=3))
        DM.add(t + 0.5, line_on(poly([(px + 180, yy - 8), (px + 220, yy - 8)]), GREY, 2, 0.3))
        DM.add(t + 0.7, label(why, px + 236, yy, 15, GREY, tracking=2))
    DM.add(at("s63", "forgotten a stamp"), seal(px + 540, y + 314, 16))
    for k, (ph, nm) in enumerate([("He worked", "WORKED"), ("He taught", "TAUGHT"), ("He raised daughters", "RAISED DAUGHTERS"),
                                  ("He buried a son", "BURIED A SON")]):
        DM.add(at("s64", ph), label(nm, px + (k % 2) * 250, y + 570 + (k // 2) * 40, 18, tracking=2.5))
    DM.add(at("s64", "not talking"), label("65 YEARS", px, y + 530, 26, tracking=4))
    DM.add(at("s64", "at ninety-three"), label("AT 93: THE RECORD", px, y + 700, 24, RED, tracking=3))
    plan.append((DM, "s61", None))

    # ---- s65: back to the seal, beside the first print on the map (cut; bookend)
    P1_local = ctx["P1_local"]
    H2 = S("s65", *MAP.to_world(P1_local[0], P1_local[1] + 240), 1.6 * 0.15)
    img, matte, _ = assets.archival("s65")
    region, px = layout(img)
    H2.add(-99, print_photo(img, region, matte))
    t = at("s65", "his seal")
    H2.add(t - 0.1, seal(px + 46, 420, 42))
    H2.add(at("s65", "go home") - 0.1, icon("house", px + 46, 560, 1.0, INK, 3))
    H2.add(at("s65", "go home") + 0.1, label("HOME", px + 110, 572, 30, INK, tracking=5))
    plan.append((H2, "s65", "cut"))
    return plan


def _ellipse_half(cx, cy, rx, ry):
    p = skia.Path()
    p.addArc(skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry), 0, 180)
    return p
