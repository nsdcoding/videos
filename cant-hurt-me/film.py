"""Can't Hurt Me (Hindi summary): the world, the camera path and the overlays.

One world, one camera. World units: the cover is 1306 x 2000 and sits centred on (0, 0).
  - intro: achievements to the right of the cover (road, sky, beach, boat, trail)
  - the valley below: his past, in rows the camera snakes through
  - the ridge: a black slope (like the cover's) rising to the right; each lesson is a
    station of six panels above it, and the runner climbs between stations
  - the end pulls all the way back to the cover

  python3 film.py still 4.5 out.png
  python3 film.py render out.mp4 0 39.6
"""
import json, math, random, sys

from engine import (Bar, Camera, Counter, Dot, Film, Hill, INK, Panel, RED, Runner, Stroke,
                    Text, split_sub)

timing = json.load(open("build/timing.json"))
LIGHT = (0.97, 0.95, 0.9)


def T(i, k=0):
    """Start time of sentence i (part k, falling back to the last part)."""
    parts = timing[i]["parts"]
    return parts[min(k, len(parts) - 1)][0]


def TE(i):
    return timing[i]["end"]


def heartbeat(t0):
    def f(t):
        if t < t0:
            return 1.0
        p = ((t - t0) * 1.15) % 1.0
        return 1 + 0.06 * math.exp(-((p - 0.08) / 0.05) ** 2) + 0.04 * math.exp(-((p - 0.30) / 0.05) ** 2)
    return f


def cover_xy(px, py):
    """Cover image pixel -> world."""
    return px - 653, py - 1000


def in_panel(cx, cy, w, ratio, u, v):
    """Relative point (u, v) inside a panel -> world."""
    return cx + (u - 0.5) * w, cy + (v - 0.5) * w * ratio


R169 = 768 / 1344
items = []
P = {}  # panel name -> (cx, cy, w); "name@2" reuses assets/name.png in a second place


def put(name, cx, cy, w=1800, **kw):
    P[name] = (cx, cy, w)
    items.append(Panel(f"assets/{name.split('@')[0]}.png", cx, cy, w, **kw))


def at(name, u=0.5, v=0.5):
    cx, cy, w = P[name]
    return in_panel(cx, cy, w, R169, u, v)


def label(name, u, v, text, t, h=0.042, **kw):
    x, y = at(name, u, v)
    items.append(Text(text, x, y, h * P[name][2], t, **kw))


def mark_x(name, u, v, size, t, color=RED, width=0.012):
    """A hand-drawn red X over part of a panel."""
    x, y = at(name, u, v)
    s, wd = size * P[name][2], width * P[name][2]
    items.append(Stroke(t, 0.3, pts=[(x - s, y - s), (x + s, y + s)], width=wd, color=color))
    items.append(Stroke(t + 0.18, 0.3, pts=[(x + s, y - s), (x - s, y + s)], width=wd, color=color))


def underline(name, u0, u1, v, t, color=RED, width=0.008):
    a, b = at(name, u0, v), at(name, u1, v)
    items.append(Stroke(t, 0.5, pts=[a, b], width=width * P[name][2], color=color))


# ================================================================= intro (approved sample)
HEART = cover_xy(640, 815)
ROAD = (1750, 150, 1800)
PULL = (1820, -1020, 1500)
BEACH = (3800, 150, 2000)
BOAT = (5500, 150, 1600)
TRAIL = (3200, 1700, 1900)
LEGS_AT = in_panel(*TRAIL, R169, 0.545, 0.765)

items += [
    Panel("assets/cover.png", 0, 0, 1306, feather=0.04, z=0),
    Panel("assets/heart.png", HEART[0], HEART[1], 70, mask="ellipse", feather=0.22, match=False,
          reveal=(700, 160), pulse=heartbeat(3.3), z=1),
    Panel("assets/road.png", *ROAD),
    Panel("assets/pullup.png", *PULL),
    Panel("assets/beach.png", *BEACH),
    Panel("assets/boat.png", *BOAT),
    Panel("assets/trail.png", *TRAIL),
    Panel("assets/legs.png", LEGS_AT[0], LEGS_AT[1], 190, feather=0.16, reveal=(1000, 300), z=1),
]
items += [
    Text("तुम मुझे", -1290, -140, 230, 0.6, kind="title", anim="stamp"),
    Text("तोड़ नहीं सकते", -1290, 110, 230, 1.0, kind="title", color=RED, anim="stamp"),
    Stroke(1.5, 0.7, pts=[(-1640, 300), (-940, 300)], width=14, color=INK),
]
hx, hy = HEART
items += [
    Stroke(4.5, 0.7, arc=(hx - 4.3, hy + 2.2, 2.7, -1.6, 4.7), width=0.6, color=LIGHT, t1=6.0),
    Text("जन्म से दिल में छेद", hx, hy + 13.5, 3.2, 4.6, t1=6.0, color=LIGHT),
]
rx, ry, rw = ROAD
vp = in_panel(*ROAD, R169, 0.503, 0.61)
items += [
    Runner([(6.0, rx - 60, ry + 470, 210), (8.0, rx - 30, ry + 330, 120), (10.6, vp[0], vp[1] + 8, 18)]),
    Text("अल्ट्रा मैराथन", vp[0] + 430, vp[1] - 175, 95, 8.4, kind="title", anim="wipe"),
    Stroke(8.9, 0.6, pts=[(vp[0] + 190, vp[1] - 105), (vp[0] + 670, vp[1] - 105)], width=8),
]
sun = in_panel(*PULL, R169, 0.506, 0.50)
items += [
    Stroke(11.2, 4.6, arc=(sun[0], sun[1], 330, -math.pi / 2, 1.5 * math.pi), width=16),
    Text("24 घंटे", sun[0] - 470, sun[1] - 270, 80, 11.6, kind="label"),
    Counter(sun[0] + 560, sun[1] - 40, 190, 12.4, 15.3, 0, 4000, fmt="{:,.0f}"),
    Text("+", sun[0] + 760, sun[1] - 60, 150, 15.3, kind="num", anim="stamp"),
    Text("पुल-अप", sun[0] + 560, sun[1] + 120, 90, 13.0),
    Text("विश्व रिकॉर्ड", sun[0] + 560, sun[1] + 215, 70, 15.0, color=RED),
]
bx, by, bw = BEACH
items += [
    Runner([(17.0, bx - 1000, by + 380, 120), (21.5, bx - 150, by + 400, 125)]),
    Text("नरक-सप्ताह", bx, by - 330, 170, 21.2, kind="title", color=RED, anim="stamp"),
    Text("अमेरिकी नौसेना – सील प्रशिक्षण", bx, by - 200, 64, 18.2, anim="wipe"),
]
ox, oy, ow = BOAT
tally = [(ox - 520 + i * 190, oy - 300) for i in range(3)]
for i, (x, y) in enumerate(tally):
    items.append(Stroke(23.3 + i * 0.35, 0.4, pts=[(x - 10, y - 75), (x + 12, y + 75)], width=24, color=INK))
items += [
    Text("×3", ox + 120, oy - 300, 190, 24.4, kind="num", color=RED, anim="stamp"),
    Text("चोट – फिर से शुरू", ox - 330, oy - 160, 60, 25.6),
]
for i in range(2):
    x, y = tally[i]
    items.append(Stroke(25.9 + i * 0.5, 0.35, pts=[(x - 70, y - 70), (x + 70, y + 70)], width=14))
    items.append(Stroke(26.05 + i * 0.5, 0.35, pts=[(x + 70, y - 70), (x - 70, y + 70)], width=14))
tx, ty, tw = TRAIL
lx, ly = LEGS_AT
items += [
    Counter(tx - 560, ty - 360, 170, 29.0, 31.0, 0, 200, fmt="{:,.0f}+ KM"),
    Text("बिना तैयारी", tx - 560, ty - 230, 72, 30.6, color=RED),
    Dot(lx - 22, ly - 16, 7, 32.9, t1=35.9, glow=True),
    Dot(lx + 12, ly + 12, 7, 33.2, t1=35.9, glow=True),
    Text("टूटी हड्डियाँ", lx - 47, ly + 10, 8, 33.2, t1=35.9, align="left"),
    Text("ख़राब गुर्दे", lx - 47, ly + 19.5, 8, 34.4, t1=35.9, align="left", color=RED),
]

INTRO_KEYS = [
    (0.0, -330, 0, 3900),
    (2.6, -40, -140, 1650, "log"),
    (4.4, hx - 2, hy + 2, 64, "log"),
    (5.95, hx - 2, hy + 3, 56, "hold"),
    (7.5, rx - 20, ry + 60, 1900, "vw"),
    (10.4, vp[0] + 130, vp[1] - 40, 1250, "hold"),
    (11.7, sun[0] + 120, sun[1] - 10, 1950, "vw"),
    (16.1, sun[0] + 160, sun[1] - 20, 1600, "hold"),
    (17.6, bx - 100, by - 40, 2150, "vw"),
    (20.8, bx - 40, by - 20, 1850, "hold"),
    (22.5, bx - 60, by + 60, 1000, "log"),
    (23.7, ox - 150, oy - 120, 1650, "vw"),
    (27.9, ox - 120, oy - 100, 1420, "hold"),
    (29.3, tx - 120, ty - 60, 2050, "vw"),
    (31.6, lx - 40, ly - 120, 820, "log"),
    (33.0, lx + 4, ly - 4, 125, "log"),
    (35.95, lx + 6, ly - 4, 112, "hold"),
    (38.6, 2300, 300, 8600, "vw"),
]

# ================================================================= camera builder for the rest
SHOTS = []  # (t_arrive, x, y, w, mode, move, push)


def shot(t, name=None, u=0.5, v=0.5, frac=1.0, mode="vw", move=1.3, push=None, xy=None, w=None):
    """Camera arrives at a panel point (or xy) at time t; then drifts until the next move."""
    if xy is None:
        x, y = at(name, u, v)
        w = frac * P[name][2]
    else:
        x, y = xy
    SHOTS.append((t, x, y, w, mode, move, push))


def build_keys():
    keys = list(INTRO_KEYS)
    prev, prev_push = keys[-1], 0.94
    for n, (t, x, y, w, mode, move, push) in enumerate(sorted(SHOTS, key=lambda s: s[0])):
        depart = max(prev[0] + 0.35, t - move)
        if t <= depart + 0.2:
            t = depart + 0.5
        if push is None:
            push = 0.93 if n % 4 else 1.05  # mostly a slow push-in, sometimes a slow pull-out
        px, py, pw = prev[1:4]
        keys.append((depart, px, py, pw * prev_push, "hold"))
        keys.append((t, x, y, w, mode))
        prev, prev_push = keys[-1], push
    return keys


def heading(i, xy, h=330):
    """Section title stamped into the world, with a red underline."""
    text = timing[i]["text"]
    t = T(i) - 0.15
    x, y = xy
    tt = Text(text, x, y, h, t, kind="title", anim="stamp")
    items.append(tt)
    items.append(Stroke(t + 0.45, 0.6, pts=[(x - tt.ww * 0.45, y + h * 0.62), (x + tt.ww * 0.45, y + h * 0.62)],
                        width=h * 0.07))
    shot(t + 0.2, xy=(x, y + h * 0.1), w=tt.ww * 1.9, move=1.5)


# ================================================================= the valley: his past
# row 1 (left -> right): the man he was
put("fatman", -2200, 3700)
put("van", -200, 3700)
put("milkshake", 1500, 3560, w=900)
put("mirror_avoid", 3000, 3700)
# row 2 (right -> left)
put("trophy_empty", 3000, 4950)
put("crossroads", 1000, 4950)
put("head_brain", -1000, 4950)
put("book_open", -3000, 4950)
# row 3 (left -> right): childhood
put("town", -4000, 6200)
put("rink", -2000, 6200)
put("house_night", 0, 6200)
put("kids_work", 2000, 6200)
put("escape_car", 4500, 6200, w=2600)
# row 4 (right -> left)
put("school_wall", 5000, 7450)
put("classroom", 3000, 7450)
put("copying", 1250, 7350, w=1100)
put("exam_hall", -500, 7450)
put("study_night", -2500, 7450)
# row 5 (left -> right): the night it changed
put("couch_tv", -4000, 8700)
put("phone_call", -2150, 8650, w=1250)
put("recruiter", -200, 8700)
put("scale_feet", 1650, 8650, w=1250)
put("workout_bike", 3350, 8700, w=1500)
put("triathlon", 5550, 8700, w=2600)
put("hill_start", 8200, 8450)

# --- real subject (s7-s11)
shot(T(7) + 0.7, "fatman", 0.55, 0.5, 1.05, move=1.9)
items += [Counter(*at("fatman", 0.24, 0.40), 150, T(7) + 0.6, T(7) + 2.6, 0, 130, fmt="{:,.0f}"),
          Text("किलो", *at("fatman", 0.24, 0.55), 70, T(7) + 1.4, color=RED)]
shot(T(7, 1) - 0.1, "van", 0.5, 0.5, 1.0)
label("van", 0.5, 0.1, "कीड़े मारने वाली कंपनी – रात की पाली", T(7, 1) + 0.2, h=0.035)
shot(T(7, 2) - 0.1, "milkshake", 0.5, 0.5, 1.15)
label("milkshake", 0.82, 0.3, "हर रात", T(7, 2) + 0.3, h=0.08, color=RED)
shot(T(7, 2) + 1.7, "mirror_avoid", 0.45, 0.5, 1.0, move=1.1)
label("mirror_avoid", 0.75, 0.42, "आईने से", T(7, 2) + 2.0, h=0.05)
label("mirror_avoid", 0.75, 0.53, "नज़र चुराना", T(7, 2) + 2.3, h=0.05, color=RED)
shot(T(8) + 0.1, "trophy_empty", 0.5, 0.5, 1.0)
label("trophy_empty", 0.5, 0.13, "प्रतिभाशाली खिलाड़ी?", T(8) + 0.3)
mark_x("trophy_empty", 0.5, 0.55, 0.06, T(8) + 1.2)
shot(T(9) + 0.1, "crossroads", 0.5, 0.5, 1.0)
label("crossroads", 0.5, 0.1, "कोई गुप्त रास्ता नहीं", T(9) + 0.4)
shot(T(10) + 0.1, "head_brain", 0.5, 0.5, 1.0)
shot(T(10) + 2.2, "head_brain", 0.66, 0.42, 0.45, mode="log", move=1.6)
label("head_brain", 0.25, 0.42, "दिमाग़ के साथ", T(10) + 0.6, h=0.05)
label("head_brain", 0.25, 0.53, "नया रिश्ता", T(10) + 1.0, h=0.05, color=RED)
shot(T(11) + 0.2, "book_open", 0.5, 0.5, 0.95, move=1.6)
shot(T(11, 1) + 0.2, "book_open", 0.5, 0.5, 0.75, mode="log", move=1.0)
label("book_open", 0.31, 0.42, "अपने दिमाग़ का", T(11, 1) - 0.2, h=0.045, anim="wipe", dur=0.9)
label("book_open", 0.31, 0.52, "मालिक बनिए", T(11, 1) + 0.5, h=0.055, color=RED, anim="wipe", dur=0.9)
label("book_open", 0.69, 0.42, "बाक़ी सब", T(11, 1) + 1.8, h=0.045, anim="wipe", dur=0.8)
label("book_open", 0.69, 0.52, "उसके पीछे आएगा", T(11, 1) + 2.3, h=0.045, anim="wipe", dur=0.9)

# --- childhood (s12-s25)
heading(12, (-6400, 6150), h=300)
shot(T(13) + 0.1, "town", 0.5, 0.5, 1.05, move=1.4)
label("town", 0.5, 0.1, "अमेरिका का एक छोटा शहर", T(13) + 0.4)
shot(T(14) + 0.1, "rink", 0.5, 0.5, 1.0)
label("rink", 0.5, 0.1, "पिता का स्केटिंग रिंक", T(14) + 0.4, color=LIGHT)
shot(T(14, 1) + 0.1, "house_night", 0.5, 0.5, 1.0)
label("house_night", 0.5, 0.1, "हर रात हिंसा", T(14, 1) + 0.4, color=RED)
shot(T(15) + 0.3, "house_night", 0.5, 0.5, 0.55, mode="log", move=1.2)
shot(T(16), "kids_work", 0.5, 0.5, 1.0)
label("kids_work", 0.5, 0.1, "रातभर काम, सुबह स्कूल", T(16) + 0.3)
# escape: follow the car along the night road
ex, ey, ew = P["escape_car"]
items.append(Runner([(T(17) - 0.3, ex - 1150, ey + 300, 120), (TE(17) + 0.6, ex + 1150, ey + 300, 120)],
                    sprite="assets/car.png", bob=0.15))
shot(T(17) + 0.2, xy=(ex - 950, ey + 120), w=1500)
shot(TE(17) - 0.2, xy=(ex + 750, ey + 100), w=1700, mode="log", move=TE(17) - T(17) - 0.6)
label("escape_car", 0.33, 0.14, "एक रात – ख़ाली हाथ", T(17) + 0.6)
label("escape_car", 0.72, 0.14, "नया शहर, ग़रीबी", T(17, 1) + 0.2, color=RED)
shot(T(18) + 0.1, "school_wall", 0.5, 0.5, 1.05)
label("school_wall", 0.5, 0.09, "नए शहर में नई मुसीबत", T(18) + 0.2)
shot(T(19) + 1.0, "school_wall", 0.5, 0.45, 0.7, mode="log", move=1.4)
random.seed(4)
for k in range(9):
    cx, cy = at("school_wall", random.uniform(0.2, 0.8), random.uniform(0.25, 0.6))
    pts = [(cx + random.uniform(-90, 90), cy + random.uniform(-60, 60)) for _ in range(5)]
    items.append(Stroke(T(19) + 2.0 + k * 0.35, 0.4, pts=pts, width=14, color=RED, t1=TE(19)))
label("school_wall", 0.5, 0.88, "खुली नस्ली नफ़रत", T(19) + 3.0, color=LIGHT, t1=TE(19))
shot(T(20) + 0.1, "classroom", 0.5, 0.5, 1.0)
label("classroom", 0.5, 0.1, "पढ़ाई में पीछे", T(20) + 0.3)
label("classroom", 0.5, 0.2, "हिंसा और डर में बच्चा सीख नहीं पाता", T(20) + 1.8, h=0.03, color=RED)
shot(T(21) + 0.1, "copying", 0.5, 0.5, 1.0)
label("copying", 0.5, 0.1, "नक़ल", T(21) + 0.4, h=0.07, color=RED, anim="stamp")
label("copying", 0.5, 0.9, "बरसों की शर्म", T(21, 1) + 0.2, h=0.05, color=LIGHT)
shot(T(22) + 0.1, "exam_hall", 0.5, 0.5, 1.0)
label("exam_hall", 0.5, 0.1, "वायुसेना की परीक्षा", T(22) + 0.3)
for k in range(3):
    mark_x("exam_hall", 0.18 + k * 0.08, 0.27, 0.025, T(22) + 2.0 + k * 0.6, width=0.007)
shot(T(23) + 0.1, "study_night", 0.5, 0.5, 1.0)
label("study_night", 0.5, 0.1, "महीनों तक: आठवीं कक्षा दोबारा", T(23) + 0.3, color=LIGHT)
for k, sym in enumerate(["+", "−", "×", "÷", "A", "B", "C"]):
    x, y = at("study_night", 0.12 + 0.11 * k if k < 4 else 0.62 + 0.09 * (k - 4), 0.24)
    items.append(Text(sym, x, y, 80, T(23) + 0.9 + 0.25 * k, kind="num", color=RED if k % 2 else LIGHT,
                      anim="stamp"))
# pull back over the whole valley
shot(T(24) + 1.0, xy=(0, 6200), w=13500, move=2.4)
items.append(Text("सुविधा से नहीं निकला", 0, 6200, 520, T(25) - 0.1, t1=TE(25) + 0.2, kind="title",
                  color=RED, anim="stamp", z=9))

# --- the night it changed (s26-s36)
heading(26, (-6450, 8650), h=300)
shot(T(27) + 0.1, "couch_tv", 0.45, 0.5, 1.0)
label("couch_tv", 0.32, 0.1, "फ्रिज का खाना, टीवी", T(27) + 0.4, color=LIGHT)
TV = (0.78, 0.48)  # the TV screen in couch_tv; the intro's beach plays on it
tvx, tvy = at("couch_tv", *TV)
items.append(Panel("assets/beach.png", tvx, tvy, 210, feather=0.18, reveal=(1300, 420), z=1))
shot(T(27) + 3.6, xy=(tvx, tvy), w=600, mode="log", move=1.4)
shot(T(28) + 0.4, xy=(tvx, tvy + 10), w=150, mode="log", move=1.2)
items.append(Text("भीतर कुछ हिल गया", tvx, tvy + 46, 14, T(28, 1), color=RED))
shot(T(29) + 0.1, "phone_call", 0.5, 0.5, 1.0, move=1.6)
label("phone_call", 0.5, 0.1, "अगले दिन: भर्ती दफ़्तर", T(29) + 0.3, h=0.05)
shot(T(30) + 0.1, "recruiter", 0.5, 0.5, 1.0)
label("recruiter", 0.2, 0.12, "उम्र सीमा: कुछ महीने", T(30) + 0.6, h=0.038)
items.append(Counter(*at("recruiter", 0.8, 0.14), 110, T(30, 1), T(30, 1) + 1.8, 0, 45, fmt="+{:.0f} किलो",
                     color=RED))
items.append(Text("असंभव", *at("recruiter", 0.5, 0.5), 300, T(31) - 0.05, t1=T(32) - 0.2, kind="title",
                  color=RED, anim="stamp", rot=-0.08, z=9))
shot(T(32) + 0.1, "scale_feet", 0.5, 0.5, 1.0)
items += [Counter(*at("scale_feet", 0.2, 0.35), 120, T(32) + 0.3, T(32) + 3.0, 130, 85, fmt="{:.0f} किलो"),
          Text("3 महीने में −45", *at("scale_feet", 0.2, 0.52), 60, T(32) + 2.4, color=RED)]
shot(T(33) + 0.1, "workout_bike", 0.5, 0.5, 1.0)
wx, wy = at("workout_bike", 0.83, 0.3)
items += [Stroke(T(33) + 0.2, 1.5, arc=(wx, wy, 120, -math.pi / 2, 1.5 * math.pi), width=18),
          Text("× 2", wx, wy, 90, T(33) + 1.2, kind="num", anim="stamp"),
          Text("दिन में दो बार, चार-चार घंटे", *at("workout_bike", 0.5, 0.08), 60, T(33) + 0.4)]
shot(T(34) + 0.1, "triathlon", 0.2, 0.5, 0.6, move=1.2)
shot(TE(34) - 0.3, "triathlon", 0.8, 0.5, 0.6, mode="log", move=TE(34) - T(34) - 0.8)
for k, word in enumerate(["साइकिल", "दौड़", "तैराकी"]):
    label("triathlon", 0.17 + 0.33 * k, 0.12, word, T(34) + 0.4 + 1.2 * k, h=0.03, anim="stamp")
label("triathlon", 0.5, 0.92, "हज़ारों की संख्या में, खाने पर पूरा नियंत्रण", T(34) + 2.5, h=0.022, color=RED)
shot(T(35) + 0.1, "triathlon", 0.5, 0.5, 1.0, move=1.0)
label("triathlon", 0.5, 0.22, "यह आदर्श तरीक़ा नहीं", T(35) + 0.6, h=0.03, color=RED, t1=TE(35))
shot(T(36) + 0.2, "hill_start", 0.5, 0.5, 1.05, move=1.5)
items += [Text("असंभव", *at("hill_start", 0.3, 0.2), 140, T(36) + 0.9, kind="title", anim="stamp"),
          Stroke(T(36) + 2.6, 0.5, pts=[at("hill_start", 0.17, 0.21), at("hill_start", 0.43, 0.19)], width=22),
          Text("सिर्फ़ बहुत मुश्किल", *at("hill_start", 0.3, 0.33), 90, T(36) + 3.2, kind="title", color=RED,
               anim="wipe")]

# ================================================================= the ridge: lessons
RIDGE_X0 = 9000


def ridge_y(x):
    return 8900 - 0.2778 * (x - RIDGE_X0) + 260 * math.sin((x - RIDGE_X0) / 5200)


items.append(Hill([(x, ridge_y(x)) for x in range(6600, 142001, 400)]))

STATION_DX = 9000
SLOTS = {"TL": (-2000, -2650), "TC": (0, -2650), "TR": (2000, -2650),
         "BL": (-2000, -1400), "BC": (0, -1400), "BR": (2000, -1400)}


def base(k):
    x = 14000 + STATION_DX * k
    return x, ridge_y(x)


def station(k, layout):
    bx_ = base(k)[0]
    for slot, name in layout.items():
        dx, dy = SLOTS[slot]
        put(name, bx_ + dx, ridge_y(bx_ + dx) + dy)


def head_xy(k):
    x = base(k)[0] - 4500
    return x, ridge_y(x) - 1300


def climb(k, t0, t1):
    """Runner climbs the ridge to this station's heading; a red trail stays behind him."""
    xa = head_xy(k - 1)[0] + 1800 if k > 0 else 7000
    xb = head_xy(k)[0] - 600
    path = [(t0 + (t1 - t0) * j / 6, xa + (xb - xa) * j / 6, ridge_y(xa + (xb - xa) * j / 6) + 10, 330)
            for j in range(7)]
    items.append(Runner(path))
    items.append(Stroke(t0, t1 - t0, pts=[(x, ridge_y(x) - 40) for x in range(int(xa), int(xb), 200)],
                        width=60, color=RED, z=-1))


def section(k, i_head, layout):
    station(k, layout)
    t = T(i_head)
    climb(k, t - 3.2, t + 0.4)
    hx_, hy_ = head_xy(k)
    shot(t - 2.4, xy=(hx_ - 1000, ridge_y(hx_ - 1000) - 500), w=4300, move=2.2)
    heading(i_head, (hx_, hy_))


# --- 4. accountability mirror (s37-s50)
section(0, 37, {"TL": "mirror", "TC": "blame", "TR": "coach_app", "BL": "notes_close", "BC": "stair_step",
                "BR": "mirror_avoid@2"})
shot(T(38) + 0.1, "mirror", 0.5, 0.5, 1.05, move=1.5)
label("mirror", 0.5, 0.08, "आईने के सामने ख़ुद से सच", T(38) + 0.6)
shot(T(39) + 0.1, "mirror", 0.5, 0.45, 0.6, mode="log")
label("mirror", 0.2, 0.4, "तसल्ली नहीं", T(40) - 0.1, h=0.04, color=RED, anim="stamp")
label("mirror", 0.8, 0.4, "बहाना नहीं", T(40) + 0.9, h=0.04, color=RED, anim="stamp")
shot(T(41) + 0.1, "notes_close", 0.5, 0.5, 1.0)
label("notes_close", 0.5, 0.08, "काग़ज़ की पर्चियाँ", T(41) + 0.3)
NOTE1, NOTE2 = (0.3, 0.5), (0.7, 0.5)
label("notes_close", NOTE1[0], NOTE1[1], "बेहतर बनूँगा", T(43) - 0.1, h=0.04, anim="wipe")
underline("notes_close", NOTE1[0] - 0.12, NOTE1[0] + 0.12, NOTE1[1], T(43) + 0.9, width=0.01)
label("notes_close", NOTE2[0], NOTE2[1] - 0.04, "इस हफ़्ते", T(44), h=0.035, anim="wipe")
label("notes_close", NOTE2[0], NOTE2[1] + 0.05, "−3 किलो", T(44) + 0.5, h=0.05, color=RED, anim="stamp")
shot(T(45) + 0.1, "blame", 0.5, 0.5, 1.15)
for n, (u, txt) in enumerate([(0.32, "1. कड़वा सच"), (0.68, "2. ख़ुद के सामने जवाबदेह")]):
    label("blame", u, 0.08, txt, T(45) + 0.5 + n * 0.6, h=0.035)
shot(T(47) + 0.1, "blame", 0.55, 0.5, 0.75, mode="log")
label("blame", 0.8, 0.88, "हालात – समय – दूसरे", T(47) + 1.5, h=0.035, color=RED)
shot(T(48) + 0.1, "coach_app", 0.5, 0.5, 1.0)
label("coach_app", 0.5, 0.08, "कोच या ऐप के सामने नहीं", T(48) + 1.2)
shot(T(49) + 0.1, "mirror_avoid@2", 0.5, 0.5, 1.0)
label("mirror_avoid@2", 0.75, 0.45, "ख़ुद को गाली देना", T(49) + 1.0, h=0.04)
mark_x("mirror_avoid@2", 0.75, 0.45, 0.05, T(49) + 2.2)
shot(T(50) + 0.1, "stair_step", 0.5, 0.5, 1.0)
label("stair_step", 0.3, 0.12, "छिपी बात ज़ोर से कहिए", T(50) + 0.3)
label("stair_step", 0.3, 0.22, "फिर अगला ठोस क़दम", T(50) + 2.5, color=RED)

# --- 5. the 40 percent rule (s51-s64)
section(1, 51, {"TL": "exhausted", "TC": "fuel_gauge", "TR": "brain_shield", "BL": "finish_sprint",
                "BC": "tank_cutaway", "BR": "question"})
shot(T(52) + 0.1, "exhausted", 0.5, 0.5, 1.0)
label("exhausted", 0.5, 0.08, "सबसे मशहूर विचार", T(52) + 0.2)
label("exhausted", 0.25, 0.25, "“अब और नहीं…”", T(53) + 0.6, h=0.045, color=RED)
shot(T(53) + 3.6, "fuel_gauge", 0.5, 0.5, 1.0)
items.append(Bar(*at("fuel_gauge", 0.08, 0.85), 1500, 90, T(53) + 3.6, 2.0, 0, 0.4))
items.append(Counter(*at("fuel_gauge", 0.85, 0.2), 170, T(53) + 3.6, T(53) + 5.6, 0, 40, fmt="{:.0f}%", color=RED))
shot(T(54) + 0.1, "fuel_gauge", 0.5, 0.5, 0.8, mode="log")
label("fuel_gauge", 0.15, 0.2, "मोटा अनुमान", T(54) + 0.5, h=0.04, anim="stamp")
shot(T(55) + 0.1, "brain_shield", 0.5, 0.5, 1.0)
label("brain_shield", 0.5, 0.08, "दिमाग़ = शरीर का रक्षक", T(56) + 0.2)
label("brain_shield", 0.5, 0.92, "असली सीमा से बहुत पहले थकान का संकेत", T(56) + 2.5, h=0.03, color=RED)
shot(T(57) + 0.1, "brain_shield", 0.5, 0.45, 0.6, mode="log")
label("brain_shield", 0.5, 0.18, "केंद्रीय नियंत्रक", T(57) + 0.3, h=0.05, kind="title", color=RED, anim="stamp")
shot(T(58) + 0.1, "finish_sprint", 0.5, 0.5, 1.0)
label("finish_sprint", 0.5, 0.08, "आख़िरी सौ मीटर: लोग तेज़ हो जाते हैं", T(58) + 0.4)
shot(T(59) + 0.1, "tank_cutaway", 0.5, 0.5, 1.0)
label("tank_cutaway", 0.2, 0.3, "ईंधन बचा था", T(59) + 0.3, h=0.045)
label("tank_cutaway", 0.8, 0.3, "दिमाग़ रोके बैठा था", T(59) + 1.6, h=0.04, color=RED)
shot(T(60) + 0.1, "question", 0.5, 0.5, 1.0)
label("question", 0.5, 0.08, "हर दिन ख़ुद को तोड़ना नहीं", T(60) + 0.3)
mark_x("question", 0.5, 0.08, 0.03, T(60) + 1.6, width=0.006)
label("question", 0.2, 0.35, "रुकने की आवाज़", T(61) + 0.8, h=0.04)
label("question", 0.2, 0.45, "अंतिम सच नहीं", T(61) + 1.8, h=0.04, color=RED)
shot(T(62) + 0.1, "question", 0.5, 0.45, 0.6, mode="log")
label("question", 0.8, 0.35, "एक सवाल", T(62) + 0.3, h=0.06, kind="title", color=RED, anim="stamp")
shot(T(63) + 0.1, "question", 0.5, 0.5, 1.0, mode="log", move=0.8)
items.append(Text("+10%", *at("question", 0.8, 0.6), 160, T(63) + 0.2, kind="num", color=RED, anim="stamp"))
qx, qy = at("question", 0.12, 0.88)
items.append(Stroke(T(64) + 0.3, 2.6, pts=[(qx, qy), (qx + 200, qy), (qx + 200, qy - 70), (qx + 400, qy - 70),
                                            (qx + 400, qy - 140), (qx + 600, qy - 140), (qx + 600, qy - 210),
                                            (qx + 800, qy - 210)], width=16))
label("question", 0.5, 0.92, "सीमा आगे खिसकती है", T(64) + 1.5, h=0.03, color=RED)

# --- 6. the governor (s65-s77)
section(2, 65, {"TL": "speedometer", "TC": "km_road", "TR": "reading_timer", "BL": "pain_injury",
                "BC": "burnout", "BR": "stair_step@2"})
shot(T(66) + 0.1, "speedometer", 0.5, 0.5, 1.0)
label("speedometer", 0.5, 0.08, "गाड़ी का गति-सीमक", T(66) + 0.4)
shot(T(67) + 0.1, "speedometer", 0.55, 0.5, 0.6, mode="log")
label("speedometer", 0.2, 0.3, "दिमाग़ में भी", T(67) + 0.5, h=0.05)
label("speedometer", 0.2, 0.42, "ढीला किया जा सकता है", T(67) + 3.0, h=0.04, color=RED)
shot(T(68) + 0.1, "km_road", 0.5, 0.5, 1.0)
label("km_road", 0.5, 0.08, "क्रमिक बढ़ोतरी", T(68) + 0.2, h=0.05, kind="title", color=RED, anim="stamp")
items.append(Counter(*at("km_road", 0.18, 0.3), 160, T(69) + 0.4, T(69) + 3.0, 5, 7, fmt="{:.0f} KM"))
shot(T(70) + 0.1, "reading_timer", 0.5, 0.5, 1.0)
items.append(Counter(*at("reading_timer", 0.2, 0.3), 150, T(70) + 0.4, T(70) + 2.4, 20, 25, fmt="{:.0f} मिनट",
                     color=RED))
shot(T(71) + 0.1, "stair_step@2", 0.5, 0.5, 1.0)
label("stair_step@2", 0.3, 0.12, "हर क़दम पर दिमाग़", T(71) + 0.8)
label("stair_step@2", 0.3, 0.22, "‘संभव’ की परिभाषा बदलता है", T(71) + 2.4, color=RED)
shot(T(72) + 0.1, "pain_injury", 0.5, 0.5, 1.1)
label("pain_injury", 0.5, 0.08, "दो चेतावनियाँ", T(72) + 0.3, h=0.05, kind="title", anim="stamp")
label("pain_injury", 0.25, 0.92, "दर्द", T(74) + 0.3, h=0.05)
label("pain_injury", 0.75, 0.92, "चोट", T(74) + 1.0, h=0.05, color=RED)
shot(T(74) + 0.1, "pain_injury", 0.5, 0.5, 0.85, mode="log")
label("pain_injury", 0.5, 0.2, "गॉगिंस ख़ुद गंभीर रूप से घायल हुए", T(75) + 0.2, h=0.03, color=RED)
shot(T(76) + 0.1, "burnout", 0.5, 0.5, 1.0)
label("burnout", 0.5, 0.08, "बढ़ोतरी धीमी हो", T(76) + 0.3)
label("burnout", 0.22, 0.3, "हफ़्ता 1: सब कुछ", T(77) + 0.4, h=0.035)
label("burnout", 0.22, 0.4, "हफ़्ता 3: बैठ गए", T(77) + 2.2, h=0.035, color=RED)

# --- 7. cookie jar (s78-s90)
section(3, 78, {"TL": "jar", "TC": "list_hand", "TR": "exam_sick", "BL": "rejections", "BC": "sleepless",
                "BR": "hand_in_jar"})
shot(T(79) + 0.1, "jar", 0.5, 0.5, 1.0)
label("jar", 0.5, 0.08, "बुरे दिनों का जार", T(79) + 0.5)
shot(T(80) + 0.1, "list_hand", 0.5, 0.5, 1.0)
label("list_hand", 0.5, 0.08, "मुश्किल हालात में किया हर काम", T(80) + 1.2)
label("list_hand", 0.5, 0.9, "बड़ी उपलब्धियाँ + छोटी लड़ाइयाँ", T(82) + 0.3, h=0.035, color=RED)
shot(T(81) + 0.1, "list_hand", 0.55, 0.5, 0.65, mode="log")
shot(T(83), "exam_sick", 0.5, 0.5, 1.0, move=1.0)
label("exam_sick", 0.5, 0.08, "बीमारी में दी परीक्षा", T(83) + 0.2)
shot(T(84), "rejections", 0.5, 0.5, 1.0, move=0.9)
items.append(Counter(*at("rejections", 0.2, 0.3), 150, T(84) + 0.1, T(84) + 1.5, 0, 100, fmt="{:.0f} इनकार",
                     color=RED))
shot(T(85), "sleepless", 0.5, 0.5, 1.0, move=0.9)
label("sleepless", 0.5, 0.08, "बिना सोए, फिर भी काम ठीक", T(85) + 0.3)
shot(T(86) + 0.1, "hand_in_jar", 0.5, 0.5, 1.0)
label("hand_in_jar", 0.5, 0.08, "टूटने लगें? जार में हाथ डालिए", T(86) + 0.4)
NOTE = at("hand_in_jar", 0.64, 0.30)
items.append(Panel("assets/pullup.png", NOTE[0], NOTE[1], 160, feather=0.2, mask="ellipse", reveal=(900, 300),
                   z=1))
shot(T(87) + 0.8, xy=NOTE, w=170, mode="log", move=2.0)
items.append(Text("कैसा लगा था? क्या डर था?", NOTE[0], NOTE[1] + 38, 10, T(87) + 2.6, color=RED))
shot(T(88) + 0.5, "jar", 0.5, 0.5, 1.1, move=1.8)
label("jar", 0.2, 0.3, "दर्द: सिर्फ़ आज", T(89) + 0.4, h=0.04)
label("jar", 0.8, 0.3, "इतिहास: मिटा", T(89) + 2.4, h=0.04, color=RED)
label("jar", 0.5, 0.92, "जार इतिहास लौटाता है: भरोसा", T(90) + 0.4, h=0.035, color=RED)

# --- 8. choosing discomfort (s91-s101)
section(4, 91, {"TL": "easy_world", "TC": "cold_shower", "TR": "alarm_5am", "BL": "phone_avoid",
                "BC": "stoic_bust", "BR": "todo_list"})
shot(T(92) + 0.1, "easy_world", 0.5, 0.5, 1.0)
label("easy_world", 0.5, 0.08, "हर चीज़ आसान बनाई जा रही है", T(92) + 0.5)
label("easy_world", 0.5, 0.92, "सहने की क्षमता गल रही है", T(92) + 4.5, h=0.035, color=RED)
shot(T(93) + 0.1, "easy_world", 0.75, 0.5, 0.6, mode="log")
label("easy_world", 0.75, 0.2, "रोज़ एक नापसंद काम", T(93) + 0.8, h=0.035)
shot(T(94) + 0.1, "cold_shower", 0.5, 0.5, 1.0, move=1.0)
label("cold_shower", 0.5, 0.08, "ठंडा पानी", T(94) + 0.2, h=0.05)
shot(T(94) + 2.0, "alarm_5am", 0.5, 0.5, 1.0, move=0.9)
label("alarm_5am", 0.2, 0.2, "5:00", T(94) + 2.1, h=0.08, kind="num", color=RED, anim="stamp")
shot(T(94) + 4.2, "phone_avoid", 0.5, 0.5, 1.0, move=0.9)
label("phone_avoid", 0.5, 0.08, "टाली हुई कॉल, टाली हुई बातचीत", T(94) + 4.3)
shot(T(95) + 0.1, "phone_avoid", 0.5, 0.5, 0.75, mode="log", move=0.7)
label("phone_avoid", 0.2, 0.4, "तकलीफ़ मक़सद नहीं", T(95), h=0.04)
label("phone_avoid", 0.25, 0.75, "मन की मर्ज़ी", T(96) + 0.8, h=0.045)
label("phone_avoid", 0.75, 0.75, "आपका फ़ैसला", T(96) + 1.8, h=0.045, color=RED)
shot(T(97) + 0.1, "stoic_bust", 0.5, 0.5, 1.0)
label("stoic_bust", 0.2, 0.3, "स्टोइक दार्शनिक", T(97) + 1.5, h=0.04)
label("stoic_bust", 0.8, 0.3, "रोज़ाना अभ्यास", T(98) + 1.0, h=0.045, color=RED, anim="stamp")
shot(T(99) + 0.1, "todo_list", 0.5, 0.5, 1.0)
label("todo_list", 0.5, 0.08, "जिससे सबसे ज़्यादा बच रहे हैं", T(100) + 0.4)
label("todo_list", 0.82, 0.3, "आख़िरी नंबर", T(101) + 0.5, h=0.04)
label("todo_list", 0.82, 0.42, "कल सबसे पहले", T(101) + 2.0, h=0.045, color=RED, anim="stamp")

# --- 9. callused mind (s102-s111)
section(5, 102, {"TL": "hands_callus", "TC": "fear_door", "TR": "speaking", "BL": "say_no", "BC": "swim_fear",
                 "BR": "study_night@2"})
shot(T(103) + 0.1, "hands_callus", 0.5, 0.5, 1.0)
label("hands_callus", 0.5, 0.08, "रगड़ से त्वचा सख़्त", T(103) + 0.4)
shot(T(104) + 0.1, "hands_callus", 0.5, 0.5, 0.6, mode="log")
label("hands_callus", 0.5, 0.85, "दिमाग़ के साथ भी यही", T(104) + 0.6, h=0.05, color=RED)
shot(T(105) + 0.1, "fear_door", 0.5, 0.5, 1.0)
label("fear_door", 0.5, 0.08, "डर में जाइए, थोड़ा-थोड़ा", T(105) + 0.4)
shot(T(106) + 0.1, "speaking", 0.5, 0.5, 1.0)
label("speaking", 0.5, 0.08, "हर हफ़्ते, एक छोटा समूह", T(106) + 1.2)
shot(T(107) + 0.1, "say_no", 0.5, 0.5, 1.0)
label("say_no", 0.2, 0.3, "इस हफ़्ते", T(107) + 0.8, h=0.04)
label("say_no", 0.2, 0.4, "एक छोटा ‘ना’", T(107) + 1.3, h=0.05, color=RED)
shot(T(108) + 0.1, "fear_door", 0.5, 0.5, 0.6, mode="vw", move=1.4)
label("fear_door", 0.5, 0.88, "इससे गुज़रा जा सकता है", T(108) + 4.5, h=0.05, color=RED, anim="stamp")
shot(T(109) + 0.3, xy=at("fear_door", 0.5, 1.15), w=5000, move=1.6)
items.append(Text("कमज़ोरी = मैदान", *at("fear_door", 0.5, 1.12), 220, T(109) + 0.8, kind="title", color=RED,
                  anim="stamp", t1=TE(109)))
shot(T(110) + 0.1, "swim_fear", 0.5, 0.5, 1.0)
label("swim_fear", 0.5, 0.08, "पानी से डर → तैराकी इकाई", T(110) + 0.4)
shot(T(111) + 0.1, "study_night@2", 0.5, 0.5, 1.0)
label("study_night@2", 0.5, 0.08, "पढ़ने में दिक्क़त → महीनों दोबारा सीखा", T(111) + 0.4, h=0.035, color=LIGHT)

# --- 10. taking souls (s112-s124)
section(6, 112, {"TL": "instructor", "TC": "recruits_run", "TR": "argue_work", "BL": "exit_door",
                 "BC": "boat@2", "BR": "beach@2"})
shot(T(113) + 0.1, "instructor", 0.5, 0.5, 1.15, move=1.2)
label("instructor", 0.5, 0.08, "सबसे कड़ा, सबसे विवादास्पद", T(113) + 0.3)
shot(T(114) + 0.1, "instructor", 0.5, 0.5, 0.9, mode="log")
label("instructor", 0.2, 0.25, "ज़्यादा सहो", T(114) + 3.6, h=0.05)
label("instructor", 0.2, 0.36, "मुस्कुराते रहो", T(114) + 5.0, h=0.05, color=RED)
shot(T(115) + 0.1, "beach@2", 0.5, 0.5, 1.0)
label("beach@2", 0.5, 0.12, "और ठंडा पानी? और!", T(115) + 1.5, h=0.04, color=RED, anim="stamp")
shot(T(116) + 0.1, "recruits_run", 0.5, 0.5, 1.0)
label("recruits_run", 0.5, 0.08, "और दौड़ाया तो और तेज़", T(116) + 0.3)
shot(T(117) + 0.1, "recruits_run", 0.7, 0.5, 0.6, mode="log")
label("recruits_run", 0.3, 0.25, "तोड़ने वाला ख़ुद हार मानता है", T(117) + 1.5, h=0.035, color=RED)
shot(T(118) + 0.1, "argue_work", 0.5, 0.5, 1.05)
label("argue_work", 0.25, 0.08, "बहस नहीं", T(119) + 2.0, h=0.05)
label("argue_work", 0.75, 0.08, "काम", T(119) + 2.8, h=0.06, color=RED, anim="stamp")
shot(T(120) + 0.1, "argue_work", 0.75, 0.5, 0.55, mode="log")
label("argue_work", 0.75, 0.88, "ताने का असर ख़त्म", T(120) + 2.0, h=0.03, color=RED)
shot(T(121) + 0.1, "exit_door", 0.5, 0.5, 1.0)
label("exit_door", 0.5, 0.08, "एक साफ़ सीमा", T(121) + 0.2, h=0.05, kind="title", anim="stamp")
label("exit_door", 0.25, 0.3, "लगातार अपमान?", T(123) + 0.5, h=0.04)
label("exit_door", 0.25, 0.4, "निकलना बुद्धिमानी है", T(123) + 2.5, h=0.04, color=RED)
shot(T(124) + 0.1, "boat@2", 0.5, 0.5, 1.0)
label("boat@2", 0.5, 0.1, "जब मैदान आपने ख़ुद चुना हो", T(124) + 0.3)

# --- 11. visualising (s125-s136)
section(7, 125, {"TL": "visualize", "TC": "route_map", "TR": "storm", "BL": "notebook@2", "BC": "finish_sprint@2",
                 "BR": "exhausted@2"})
shot(T(126) + 0.1, "visualize", 0.5, 0.5, 1.0)
label("visualize", 0.5, 0.08, "चुनौती को पहले मन में जीना", T(126) + 0.4)
label("visualize", 0.2, 0.4, "सिर्फ़ जीत?", T(127) + 2.0, h=0.05)
mark_x("visualize", 0.2, 0.4, 0.05, T(127) + 3.3)
shot(T(128) + 0.1, "route_map", 0.5, 0.5, 1.0)
label("route_map", 0.5, 0.08, "जीत + हर वह जगह जहाँ चीज़ें बिगड़ेंगी", T(128) + 0.6, h=0.035)
for n, (u, v, w_) in enumerate([(0.3, 0.6, "पैर"), (0.55, 0.4, "मन"), (0.78, 0.55, "मौसम")]):
    t_ = T(129) + 0.4 + n * 1.6
    x, y = at("route_map", u, v)
    items += [Dot(x, y, 40, t_), Text(w_, x, y - 110, 80, t_ + 0.2, kind="title", color=RED, anim="stamp")]
shot(T(129) + 0.3, "route_map", 0.55, 0.5, 0.8, mode="log", move=0.8)
shot(T(130) + 0.1, "storm", 0.5, 0.5, 1.0)
label("storm", 0.5, 0.08, "हर बाधा का जवाब पहले से तय", T(130) + 0.3)
shot(T(131) + 0.1, "finish_sprint@2", 0.5, 0.5, 1.0)
label("finish_sprint@2", 0.5, 0.08, "मनोविज्ञान भी यही कहता है", T(131) + 0.2)
fx, fy = at("finish_sprint@2", 0.5, 0.86)
items += [Bar(fx - 700, fy - 40, 600, 80, T(132) + 0.6, 1.5, 0.7, 0.35, color=INK),
          Text("सिर्फ़ सफलता", fx - 400, fy - 110, 55, T(132) + 0.5),
          Bar(fx + 100, fy - 40, 600, 80, T(133) + 0.6, 1.5, 0.5, 0.9),
          Text("बाधा + जवाब", fx + 400, fy - 110, 55, T(133) + 0.5, color=RED)]
shot(T(134) + 0.1, "finish_sprint@2", 0.5, 0.5, 1.15, mode="log", move=0.8)
label("finish_sprint@2", 0.5, 0.2, "मानसिक विपरीत-चित्रण", T(134) + 0.4, h=0.05, kind="title", color=RED,
      anim="stamp")
shot(T(135) + 0.1, "notebook@2", 0.5, 0.5, 1.0)
for n, (txt, dt) in enumerate([("लक्ष्य", 0.6), ("3 रुकावटें", 2.6), ("हर एक का जवाब", 5.0)]):
    label("notebook@2", 0.5, 0.3 + 0.15 * n, txt, T(136) + dt, h=0.05, color=RED if n == 2 else INK, anim="wipe")
shot(T(136) + 4.0, "exhausted@2", 0.5, 0.5, 1.0, move=1.2)
label("exhausted@2", 0.5, 0.08, "अगर ऐसा हुआ, तो मैं ठीक-ठीक क्या करूँगा?", T(136) + 4.2, h=0.03, color=RED)

# --- 12. discipline, not motivation (s137-s152)
section(8, 137, {"TL": "weather", "TC": "bed_alarm", "TR": "calendar", "BL": "clothes_ready", "BC": "door_shoes",
                 "BR": "rain_run"})
shot(T(138) + 0.1, "weather", 0.5, 0.5, 1.0)
label("weather", 0.5, 0.08, "प्रेरणा = मौसम", T(139) + 0.2, h=0.05, kind="title", anim="stamp")
shot(T(140) + 0.1, "weather", 0.75, 0.5, 0.6, mode="log")
label("weather", 0.75, 0.88, "असली नतीजे उन दिनों, जब मन नहीं", T(140) + 4.0, h=0.025, color=RED)
shot(T(141) + 0.1, "calendar", 0.5, 0.5, 1.0)
label("calendar", 0.5, 0.06, "अनुशासन: फ़ैसला पहले हो चुका", T(142) + 0.2, h=0.035)
shot(T(143) + 0.1, "bed_alarm", 0.5, 0.5, 1.0)
label("bed_alarm", 0.5, 0.08, "आज जाऊँ या न जाऊँ?", T(143) + 0.6, h=0.045)
label("bed_alarm", 0.5, 0.92, "बहस में ऊर्जा जलती है", T(143) + 3.4, h=0.035, color=RED)
shot(T(144) + 0.1, xy=at("bed_alarm", 0.5, 1.12), w=4800, move=1.2)
items.append(Text("तीन सादा तरीक़े", *at("bed_alarm", 0.5, 1.12), 160, T(144) + 0.4, kind="title", anim="stamp",
                  t1=T(146)))
shot(T(145) + 0.3, "clothes_ready", 0.5, 0.5, 1.0)
label("clothes_ready", 0.5, 0.08, "1. फ़ैसले घटाइए", T(145) + 0.2, h=0.05, kind="title")
label("clothes_ready", 0.5, 0.92, "कपड़े, समय, रास्ता, खाना: पहले से तय", T(146) + 1.0, h=0.03, color=RED)
shot(T(147) + 0.1, "door_shoes", 0.5, 0.5, 1.0)
label("door_shoes", 0.5, 0.08, "2. शुरुआत की सीमा नीची", T(147) + 0.2, h=0.05, kind="title")
items.append(Counter(*at("door_shoes", 0.2, 0.35), 150, T(147) + 4.0, T(147) + 5.5, 0, 5, fmt="{:.0f} मिनट",
                     color=RED))
shot(T(149) + 0.1, "calendar", 0.5, 0.5, 1.0)
label("calendar", 0.5, 0.94, "3. हर दिन का निशान", T(149) + 0.2, h=0.045, kind="title")
CAL = dict(u0=0.29, u1=0.68, v0=0.22, v1=0.78, cols=5, rows=6)


def calendar_marks(name, t0, n, step=0.12, grid=CAL):
    cw = (grid["u1"] - grid["u0"]) / grid["cols"]
    rh = (grid["v1"] - grid["v0"]) / grid["rows"]
    for j in range(n):
        c, r = j % grid["cols"], j // grid["cols"]
        mark_x(name, grid["u0"] + cw * (c + 0.5), grid["v0"] + rh * (r + 0.5), cw * 0.3, t0 + j * step,
               width=0.006)


calendar_marks("calendar", T(149) + 0.6, 26)
shot(T(150) + 0.1, "rain_run", 0.5, 0.5, 1.0)
label("rain_run", 0.5, 0.08, "जिस दिन सबसे कम मन हो", T(151) + 0.2)
label("rain_run", 0.5, 0.18, "वही दिन सबसे क़ीमती", T(151) + 2.6, color=RED)
shot(T(152) + 0.1, "rain_run", 0.5, 0.5, 0.6, mode="log")
label("rain_run", 0.5, 0.86, "उसी दिन पहचान बदलती है", T(152) + 2.0, h=0.04, color=RED, anim="stamp")

# --- 13. time audit (s153-s161)
section(9, 153, {"TL": "time_grid", "TC": "phone_scroll", "TR": "deep_work", "BL": "excuse_wall",
                 "BC": "clothes_ready@2", "BR": "jar@2"})
shot(T(154) + 0.1, "time_grid", 0.5, 0.5, 1.0)
label("time_grid", 0.5, 0.08, "सबसे कम चर्चित, सबसे व्यावहारिक", T(154) + 0.3, h=0.035)
shot(T(155) + 0.1, "time_grid", 0.5, 0.6, 0.6, mode="log")
label("time_grid", 0.2, 0.3, "3 हफ़्ते", T(155) + 0.8, h=0.05, kind="title", color=RED)
label("time_grid", 0.8, 0.3, "हर आधा घंटा", T(155) + 1.8, h=0.04)
shot(T(156) + 0.1, "phone_scroll", 0.5, 0.5, 1.0)
label("phone_scroll", 0.5, 0.08, "पहली खोज", T(156) + 0.3)
items.append(Counter(*at("phone_scroll", 0.2, 0.3), 150, T(157) + 0.5, T(157) + 2.5, 0, 5, fmt="3–{:.0f} घंटे",
                     color=RED))
label("phone_scroll", 0.2, 0.42, "कहीं नहीं गए", T(157) + 2.5, h=0.04)
shot(T(158) + 0.1, "deep_work", 0.5, 0.5, 1.0)
label("deep_work", 0.5, 0.08, "असली काम: सिर्फ़ 2–3 घंटे", T(158) + 0.6)
shot(T(160) + 0.1, "deep_work", 0.5, 0.5, 0.6, mode="log")
label("deep_work", 0.5, 0.86, "सबसे अच्छे 2 घंटे बचाइए", T(160) + 1.5, h=0.04, color=RED)
shot(T(161) + 0.1, "excuse_wall", 0.5, 0.5, 1.0)
label("excuse_wall", 0.5, 0.08, "“मेरे पास समय नहीं”", T(161) + 0.6, h=0.05, color=RED)
label("excuse_wall", 0.5, 0.9, "यह ईंट टिक नहीं पाती", T(161) + 2.6)

# --- 14. after-action report (s162-s172)
section(10, 162, {"TL": "debrief", "TC": "notebook", "TR": "storm@2", "BL": "exhausted@3", "BC": "km_road@2",
                  "BR": "list_hand@2"})
shot(T(163) + 0.1, "debrief", 0.5, 0.5, 1.0)
label("debrief", 0.5, 0.08, "हर अभियान के बाद, बिना बचाव", T(163) + 0.6)
shot(T(163) + 4.5, "debrief", 0.5, 0.55, 0.6, mode="log")
for n, w_ in enumerate(["योजना", "क्या हुआ", "अगली बार"]):
    label("debrief", 0.25 + 0.25 * n, 0.85, w_, T(163) + 4.8 + 0.6 * n, h=0.03, color=RED if n == 2 else LIGHT,
          anim="stamp")
shot(T(164) + 0.1, "storm@2", 0.5, 0.5, 1.0)
label("storm@2", 0.5, 0.08, "हर दौड़ और हर नाकामी के बाद", T(164) + 0.3)
shot(T(165) + 0.1, "notebook", 0.5, 0.5, 1.0)
label("notebook", 0.5, 0.06, "चार सवाल", T(165), h=0.05, kind="title", color=RED, anim="stamp")
for n, i in enumerate([166, 167, 168, 169]):
    label("notebook", 0.52, 0.27 + 0.15 * n, ["क्या हासिल करना था?", "असल में क्या हुआ?",
                                              "अंतर के तीन बड़े कारण?", "अगली बार कौन-सी एक चीज़?"][n],
          T(i), h=0.035, anim="wipe", dur=0.6)
shot(T(170) + 0.1, "exhausted@3", 0.5, 0.5, 1.0)
label("exhausted@3", 0.25, 0.3, "ख़ुद पर तरस", T(170) + 2.2, h=0.04)
label("exhausted@3", 0.75, 0.3, "ख़ुद को गाली", T(170) + 3.4, h=0.04)
mark_x("exhausted@3", 0.25, 0.3, 0.06, T(171))
mark_x("exhausted@3", 0.75, 0.3, 0.06, T(171) + 0.3)
shot(T(172) + 0.1, "list_hand@2", 0.5, 0.5, 1.0)
label("list_hand@2", 0.5, 0.08, "सिर्फ़ जानकारी: निकालिए, लगाइए", T(172) + 0.3, color=RED)

# --- 15. who's gonna carry the boats (s173-s179)
section(11, 173, {"TL": "boats_shout", "TC": "team_lift", "TR": "inspire", "BL": "boat@3", "BC": "pullup@2",
                  "BR": "road@2"})
shot(T(174) + 0.1, "boat@3", 0.5, 0.5, 1.0)
label("boat@3", 0.5, 0.08, "सिर पर भारी नाव", T(174) + 0.5)
shot(T(175) + 0.1, "boats_shout", 0.5, 0.5, 1.0)
label("boats_shout", 0.5, 0.08, "“ये नावें कौन ढोएगा?”", T(175) + 2.0, h=0.05, color=LIGHT)
shot(T(175) + 4.3, "boats_shout", 0.5, 0.5, 0.65, mode="log", move=1.0)
label("boats_shout", 0.5, 0.88, "“मैं ढोऊँगा!”", T(175) + 4.6, h=0.08, kind="title", color=RED, anim="stamp")
shot(T(176) + 0.1, "team_lift", 0.5, 0.5, 1.0)
label("team_lift", 0.5, 0.08, "उनकी पहचान", T(176) + 0.3)
shot(T(177) + 0.1, "team_lift", 0.3, 0.5, 0.6, mode="log")
label("team_lift", 0.5, 0.9, "हर टीम, परिवार, समूह में कोई एक: सबसे भारी हिस्सा", T(177) + 3.0, h=0.025,
      color=RED)
shot(T(178) + 0.1, "inspire", 0.5, 0.5, 1.0)
label("inspire", 0.5, 0.08, "सबसे बड़ा असर: रिकॉर्ड नहीं, लोग", T(178) + 1.5)
shot(T(179) + 0.1, "inspire", 0.5, 0.5, 0.7, mode="log")
label("inspire", 0.5, 0.9, "यह संभव है", T(179) + 2.5, h=0.07, kind="title", color=RED, anim="stamp")

# --- 16. limits of the philosophy (s180-s192)
section(12, 180, {"TL": "balance_scale", "TC": "hospital", "TR": "doctor", "BL": "inner_storm",
                  "BC": "family_rest", "BR": "hill_start@2"})
shot(T(181) + 0.1, "balance_scale", 0.5, 0.5, 1.0)
label("balance_scale", 0.5, 0.08, "ईमानदार सारांश: असहमति भी", T(181) + 0.3)
label("balance_scale", 0.5, 0.92, "हर किसी के लिए नहीं", T(182) + 0.6, h=0.04, color=RED)
shot(T(183) + 0.1, "hospital", 0.5, 0.5, 1.0)
label("hospital", 0.5, 0.08, "पहली सीमा: शरीर", T(183) + 0.1, h=0.05, kind="title", anim="stamp")
label("hospital", 0.2, 0.9, "चोटें, गुर्दे, शल्य-क्रियाएँ", T(184) + 1.5, h=0.035, color=RED)
shot(T(185) + 0.1, "doctor", 0.5, 0.5, 1.0)
label("doctor", 0.5, 0.08, "मानसिक हिस्सा लीजिए", T(185) + 2.0)
label("doctor", 0.5, 0.9, "शरीर: धीमी राह, डॉक्टर की सलाह", T(185) + 4.0, h=0.035, color=RED)
shot(T(186) + 0.1, "inner_storm", 0.5, 0.5, 1.0)
label("inner_storm", 0.5, 0.08, "दूसरी सीमा: मन", T(186) + 0.1, h=0.05, kind="title", anim="stamp")
label("inner_storm", 0.5, 0.9, "कोसती आवाज़ को और तेज़ न करें", T(188) + 1.0, h=0.035, color=RED)
shot(T(189) + 0.1, "family_rest", 0.5, 0.5, 1.0)
label("family_rest", 0.5, 0.08, "तीसरी सीमा: संतुलन", T(189) + 0.1, h=0.05, kind="title", anim="stamp")
for n, w_ in enumerate(["रिश्ते", "आराम", "ख़ुशी"]):
    label("family_rest", 0.25 + 0.25 * n, 0.9, w_, T(190) + 0.6 + 0.5 * n, h=0.04, color=RED, anim="stamp")
shot(T(191) + 0.1, "family_rest", 0.5, 0.5, 0.7, mode="log")
shot(T(192) + 0.1, "hill_start@2", 0.5, 0.5, 1.0)
label("hill_start@2", 0.3, 0.2, "सीमा अक्सर वहाँ नहीं", T(192) + 1.5, h=0.04)
label("hill_start@2", 0.3, 0.3, "जहाँ हमें दिखती है", T(192) + 3.0, h=0.045, color=RED, anim="stamp")

# --- 17. fourteen-day practice (s193-s206): a tour of earlier ideas, day by day
section(13, 193, {"TL": "time_grid@2", "TC": "mirror@2", "TR": "cold_shower@2", "BL": "jar@3",
                  "BC": "route_map@2", "BR": "notebook@3"})


def day_tag(name, t, text, sub=None):
    label(name, 0.5, 0.08, text, t, h=0.05, kind="title", color=RED, anim="stamp")
    if sub:
        label(name, 0.5, 0.92, sub, t + 1.0, h=0.035)


shot(T(194) + 0.1, "time_grid@2", 0.5, 0.5, 1.0)
day_tag("time_grid@2", T(194), "दिन 1–3", "हर आधे घंटे का हिसाब")
shot(T(196) + 0.1, "time_grid@2", 0.5, 0.55, 0.7, mode="log")
shot(T(197) + 0.1, "mirror@2", 0.5, 0.5, 1.0)
day_tag("mirror@2", T(197), "दिन 4", "आईना: तीन पर्चियाँ, तारीख़ के साथ")
shot(T(200) + 0.1, "cold_shower@2", 0.5, 0.5, 1.0)
day_tag("cold_shower@2", T(200), "दिन 5–10", "रोज़ एक असहज काम")
shot(T(202) + 0.1, "cold_shower@2", 0.5, 0.5, 0.7, mode="log")
items.append(Text("+10% रोज़", *at("cold_shower@2", 0.8, 0.4), 140, T(202) + 1.5, kind="title", color=RED,
                  anim="stamp"))
shot(T(203) + 0.1, "jar@3", 0.5, 0.5, 1.0)
day_tag("jar@3", T(203), "दिन 11", "कुकी जार: कम से कम दस चीज़ें")
shot(T(205) + 0.1, "route_map@2", 0.5, 0.5, 1.0)
day_tag("route_map@2", T(205), "दिन 12–14", "तीन रुकावटें, तीन जवाब")
shot(T(206) + 0.1, "notebook@3", 0.5, 0.5, 1.0)
day_tag("notebook@3", T(206), "दिन 14", "चार सवालों वाला ब्योरा")

# --- 18. the last word, the summit and back to the cover (s207-s218)
section(14, 207, {"TL": "shadow_voice", "TC": "book_open@2", "TR": "nobody_road", "BL": "rain_run@2",
                  "BC": "summit", "BR": "trail@2"})
shot(T(208) + 0.1, "shadow_voice", 0.5, 0.5, 1.0)
label("shadow_voice", 0.5, 0.08, "तुम मुझे चोट नहीं पहुँचा सकते", T(208) + 1.0, h=0.045, kind="title")
shot(T(209) + 0.1, "shadow_voice", 0.35, 0.5, 0.6, mode="log")
label("shadow_voice", 0.5, 0.9, "भीतरी आवाज़ से, जो रुकने को कहती है", T(209) + 0.8, h=0.03, color=RED)
shot(T(210) + 0.1, "book_open@2", 0.5, 0.5, 1.0)
label("book_open@2", 0.31, 0.45, "बिना सजावट", T(211) + 0.5, h=0.045, anim="wipe")
label("book_open@2", 0.69, 0.45, "शर्म, नाकामियाँ", T(211) + 2.5, h=0.04, anim="wipe")
label("book_open@2", 0.5, 0.9, "शुरुआत की जगह अंतिम फ़ैसला नहीं", T(211) + 6.0, h=0.035, color=RED)
shot(T(212) + 0.1, "nobody_road", 0.5, 0.5, 1.0)
label("nobody_road", 0.5, 0.08, "आख़िरी संदेश", T(212) + 0.1)
shot(T(213) + 0.1, "nobody_road", 0.5, 0.55, 0.6, mode="log", move=0.8)
label("nobody_road", 0.5, 0.35, "कोई आपके लिए नहीं आ रहा", T(213) + 0.1, h=0.045, kind="title", color=RED,
      anim="stamp")
shot(T(214) + 0.4, "summit", 0.5, 0.5, 1.0, move=1.2)
label("summit", 0.5, 0.08, "न सही समय, न सही परिस्थिति", T(214) + 0.4)
shot(T(215) + 0.2, "summit", 0.5, 0.45, 0.7, mode="log")
label("summit", 0.2, 0.3, "आज", T(215) + 0.3, h=0.07, kind="title", color=RED, anim="stamp")
label("summit", 0.2, 0.42, "इसी शरीर से", T(215) + 1.2, h=0.04)
label("summit", 0.8, 0.3, "प्रेरणा नहीं", T(215) + 4.2, h=0.045)
label("summit", 0.8, 0.42, "फ़ैसला", T(215) + 5.6, h=0.07, kind="title", color=RED, anim="stamp")
# the long journey home: pull back over the whole ridge and the valley, land on the cover
shot(T(216) + 4.8, xy=(62000, -3000), w=170000, move=5.6)
shot(TE(218) - 1.4, xy=(-330, 0), w=3900, move=8.0)

# ================================================================= assemble
cam = Camera(build_keys())
subs = split_sub([p for r in timing for p in r["parts"]])
film = Film(items, cam, subs)

if __name__ == "__main__":
    if sys.argv[1] == "still":
        film.still(float(sys.argv[2]), sys.argv[3])
    else:
        film.render(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
