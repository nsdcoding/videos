"""Can't Hurt Me (Hindi summary): the world, the camera path and the overlays.

World units: the cover is 1306 x 2000 and sits centred on (0, 0). Everything else is
placed around it so the camera can travel there and back.

  python3 film.py still 4.5 out.png
  python3 film.py render out.mp4 0 39.6
"""
import json, math, sys

from engine import (Camera, Counter, Dot, Film, INK, Panel, RED, Runner, Stroke, Text,
                    split_sub)


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
    """Relative point (u, v) inside a 16:9-ish panel -> world."""
    return cx + (u - 0.5) * w, cy + (v - 0.5) * w * ratio


R169 = 768 / 1344

# ---------------------------------------------------------------- world
HEART = cover_xy(640, 815)
ROAD = (1750, 150, 1800)
PULL = (1820, -1020, 1500)
BEACH = (3800, 150, 2000)
BOAT = (5500, 150, 1600)
TRAIL = (3200, 1700, 1900)
LEGS_AT = in_panel(*TRAIL, R169, 0.545, 0.765)

items = [
    Panel("assets/cover.png", 0, 0, 1306, feather=0.04, z=0),
    Panel("assets/heart.png", HEART[0], HEART[1], 70, mask="ellipse", feather=0.22, match=False,
          reveal=(700, 160), pulse=heartbeat(3.3), z=1),
    Panel("assets/road.png", *ROAD),
    Panel("assets/pullup.png", *PULL),
    Panel("assets/beach.png", *BEACH),
    Panel("assets/boat.png", *BOAT),
    Panel("assets/trail.png", *TRAIL),
    Panel("assets/legs.png", LEGS_AT[0], LEGS_AT[1], 190, feather=0.16,
          reveal=(1000, 300), z=1),
]

# opening: the Hindi title stamped beside the cover (seen again at the very end)
items += [
    Text("तुम मुझे", -1290, -140, 230, 0.6, kind="title", anim="stamp"),
    Text("तोड़ नहीं सकते", -1290, 110, 230, 1.0, kind="title", color=RED, anim="stamp"),
    Stroke(1.5, 0.7, pts=[(-1640, 300), (-940, 300)], width=14, color=INK),
]

# heart: a red ring finds the hole, a label
hx, hy = HEART
items += [
    Stroke(4.5, 0.7, arc=(hx - 4.3, hy + 2.2, 2.7, -1.6, 4.7), width=0.6, color=(0.95, 0.92, 0.88), t1=6.0),
    Text("जन्म से दिल में छेद", hx, hy + 13.5, 3.2, 4.6, t1=6.0, color=(0.95, 0.92, 0.88)),
]

# road: ultra marathon, the runner heads for the horizon
rx, ry, rw = ROAD
vp = in_panel(*ROAD, R169, 0.503, 0.61)
items += [
    Runner([(6.0, rx - 60, ry + 470, 210), (8.0, rx - 30, ry + 330, 120), (10.6, vp[0], vp[1] + 8, 18)]),
    Text("अल्ट्रा मैराथन", vp[0] + 430, vp[1] - 175, 95, 8.4, kind="title", anim="wipe"),
    Stroke(8.9, 0.6, pts=[(vp[0] + 190, vp[1] - 105), (vp[0] + 670, vp[1] - 105)], width=8),
]

# pull-ups: counter + a 24h ring round the red sun
px_, py_, pw = PULL
sun = in_panel(*PULL, R169, 0.506, 0.50)
items += [
    Stroke(11.2, 4.6, arc=(sun[0], sun[1], 330, -math.pi / 2, 1.5 * math.pi), width=16),
    Text("24 घंटे", sun[0] - 470, sun[1] - 270, 80, 11.6, kind="label"),
    Counter(sun[0] + 560, sun[1] - 40, 190, 12.4, 15.3, 0, 4000, fmt="{:,.0f}"),
    Text("+", sun[0] + 760, sun[1] - 60, 150, 15.3, kind="num", anim="stamp"),
    Text("पुल-अप", sun[0] + 560, sun[1] + 120, 90, 13.0),
    Text("विश्व रिकॉर्ड", sun[0] + 560, sun[1] + 215, 70, 15.0, color=RED),
]

# hell week: beach, then the boat with three tally marks, two struck out
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

# 200 km without preparing, then into the legs: broken bones, failing kidneys
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

# ---------------------------------------------------------------- camera (t, x, y, w, mode)
cam = Camera([
    (0.0, -330, 0, 3900),
    (2.6, -40, -140, 1650, "log"),
    (4.4, hx - 2, hy + 2, 64, "log"),          # dive into the chest: the heart
    (5.95, hx - 2, hy + 3, 56, "hold"),
    (7.5, rx - 20, ry + 60, 1900, "vw"),         # pull out and swoop right to the road
    (10.4, vp[0] + 130, vp[1] - 40, 1250, "hold"),  # creep toward the horizon
    (11.7, sun[0] + 120, sun[1] - 10, 1950, "vw"),  # tilt up into the sky: pull-ups
    (16.1, sun[0] + 160, sun[1] - 20, 1600, "hold"),
    (17.6, bx - 100, by - 40, 2150, "vw"),       # swoop to the beach
    (20.8, bx - 40, by - 20, 1850, "hold"),
    (22.5, bx - 60, by + 60, 1000, "log"),       # push into the linked arms
    (23.7, ox - 150, oy - 120, 1650, "vw"),      # across to the boat + tally
    (27.9, ox - 120, oy - 100, 1420, "hold"),
    (29.3, tx - 120, ty - 60, 2050, "vw"),       # swoop down to the night trail
    (31.6, lx - 40, ly - 120, 820, "log"),       # push toward the runner
    (33.0, lx + 4, ly - 4, 125, "log"),          # into his legs
    (35.95, lx + 6, ly - 4, 112, "hold"),
    (38.6, 2300, 300, 8600, "vw"),               # pull right back: the whole world so far
    (40.0, 2300, 300, 8900, "hold"),
])

timing = json.load(open("build/timing.json"))
subs = split_sub([p for r in timing for p in r["parts"]])
film = Film(items, cam, subs)

if __name__ == "__main__":
    if sys.argv[1] == "still":
        film.still(float(sys.argv[2]), sys.argv[3])
    else:
        film.render(sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))
