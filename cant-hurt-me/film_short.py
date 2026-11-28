"""YouTube Short (9:16), built from scratch: the 40% rule as one climb up a tall world.

Its own vertical images (short/assets), one continuous camera that rises from the foot of a
cliff to a summit, and three stretches of the main narration. The promo is appended after.

  python3 film_short.py still 12 out.png
  python3 film_short.py render out.mp4        # video only
  python3 film_short.py audio out.wav         # the cut narration
"""
import json
import math
import os
import subprocess
import sys

os.environ["FORMAT"] = "short"

import cairo  # noqa: E402

from engine import (H, INK, RED, W, Bar, Camera, Counter, Film, Panel, Stroke,  # noqa: E402
                    Text, back_out, clamp, ramp, split_sub, text_image, to_surface)

LIGHT = (0.97, 0.95, 0.9)
timing = json.load(open("build/timing.json"))


def T(i, k=0):
    parts = timing[i]["parts"]
    return parts[min(k, len(parts) - 1)][0]


def TE(i):
    return timing[i]["end"]


# ---------------------------------------------------------------- narration: three stretches
# s52-53 the claim; s55-59 why (the brain, the governor, the last 100 m, fuel left);
# s61-64 what to do (a question, 10% more). The side remarks s54 and s60 are left out.
RANGES = [(T(52) - 0.1, TE(53) + 0.15), (T(55) - 0.1, TE(59) + 0.15), (T(61) - 0.1, TE(64) + 0.25)]
GAP = 0.35
OFFSETS, _acc = [], 0.4  # a breath of silence before the first word
for a, b in RANGES:
    OFFSETS.append(_acc)
    _acc += (b - a) + GAP
VOICE_END = _acc - GAP
END = VOICE_END + 2.6  # the closing pull-back, then the promo


def S(orig):
    """Narration time -> time in the Short."""
    for (a, b), off in zip(RANGES, OFFSETS):
        if a - 0.5 <= orig <= b + 0.5:
            return off + orig - a
    raise ValueError(orig)


subs = []
for r in timing:
    for t0, t1, text in r["parts"]:
        if any(a - 0.05 <= t0 and t1 <= b + 0.05 for a, b in RANGES):
            subs.append((S(t0), S(t1), text))
subs = split_sub(subs)

# ---------------------------------------------------------------- the world: one tall column
RATIO = 1344 / 768
items, P = [], {}


def put(name, cx, cy, w=1000, **kw):
    P[name] = (cx, cy, w)
    items.append(Panel(f"short/assets/{name}.png", cx, cy, w, **kw))


def at(name, u=0.5, v=0.5):
    cx, cy, w = P[name]
    return cx + (u - 0.5) * w, cy + (v - 0.5) * w * RATIO


def say(name, u, v, text, t, h=60, **kw):
    x, y = at(name, u, v)
    items.append(Text(text, x, y, h, t, **kw))


# climbing up the screen = moving to smaller y
put("v_base", 0, 0, feather=0.06)
put("v_climb", 0, -1700, feather=0.06)  # the cliff carries straight on from the base
put("v_head", -150, -3550)
BRAIN = at("v_head", 0.48, 0.64)
put("v_control", BRAIN[0], BRAIN[1], w=150, mask="ellipse", feather=0.2, reveal=(700, 230), z=1)
DIAL = at("v_control", 0.25, 0.40)
put("v_governor", DIAL[0] - 0.05 * 10, DIAL[1] + 0.08 * 17.5, w=10, mask="ellipse", feather=0.2,
    reveal=(60, 16), z=2)
put("v_track", 250, -5450)
put("v_tank", -250, -7300)
put("v_shadow", 200, -9150)
put("v_stairs", 0, -11000)

# ---------------------------------------------------------------- overlays, timed to the words
# 1. the claim: he stalls at a red line; the meter stops at 40%
mx, my = at("v_climb", 0.12, 0.30)
END1 = S(TE(53)) + 0.4  # each beat's labels leave with it
items += [Bar(mx, my, 70, 700, S(T(53)) + 2.6, 4.2, 0, 0.4, vertical=True, t1=END1),
          Counter(mx + 35, my - 70, 110, S(T(53)) + 2.6, S(T(53)) + 6.8, 0, 40, fmt="{:.0f}%", color=RED,
                  t_out=END1),
          Text("सिर्फ़", mx + 35, my - 160, 55, S(T(53)) + 5.5, t1=END1)]
say("v_base", 0.4, 0.45, "सबसे मशहूर विचार", S(T(52)) + 0.2, h=84, kind="title", t1=S(T(53)) + 1.2)
say("v_climb", 0.42, 0.62, "“अब और नहीं…”", S(T(53)) + 1.0, h=62, color=RED, kind="title", anim="stamp",
    t1=END1)
# 2. why: the brain, its alarm, its governor
say("v_head", 0.5, 0.12, "असली शारीरिक तथ्य", S(T(55)) + 0.3, h=62, kind="title", t1=S(T(56)) + 1.2)
cx_, cy_ = at("v_control", 0.5, 0.18)
items += [Text("थकान!", cx_, cy_, 20, S(T(56)) + 2.6, t1=S(T(57)) + 0.4, kind="title", color=RED, anim="stamp"),
          Text("असली सीमा से बहुत पहले", *at("v_control", 0.5, 0.78), 9, S(T(56)) + 4.0, t1=S(T(57)) + 0.4,
               color=INK)]
gx, gy = at("v_governor", 0.5, 0.15)
items.append(Text("केंद्रीय नियंत्रक", gx, gy, 1.1, S(T(57)) + 0.7, t1=S(T(58)) + 0.6, kind="title", color=RED,
                  anim="stamp"))
# 3. the last 100 m, fuel left in the tank
say("v_track", 0.5, 0.27, "आख़िरी 100 मीटर", S(T(58)) + 1.6, h=74, kind="title", color=RED, anim="stamp",
    t1=S(T(59)) + 0.2)
say("v_track", 0.5, 0.455, "लोग तेज़ हो जाते हैं", S(T(58)) + 2.6, h=54, color=RED, t1=S(T(59)) + 0.2)
say("v_tank", 0.5, 0.1, "ईंधन बचा था", S(T(59)) + 0.4, h=62, kind="title", t1=S(TE(59)) + 0.4)
lock = at("v_tank", 0.5, 0.39)
items += [Stroke(S(T(59)) + 1.4, 0.6, arc=(lock[0], lock[1], 75, -math.pi / 2, 1.5 * math.pi), width=9),
          Text("ताला: दिमाग़ का", lock[0], lock[1] + 640, 52, S(T(59)) + 1.6, t1=S(TE(59)) + 0.4, color=RED)]
# 4. what to do: the voice says stop; treat it as a question; then 10% more, step by step
hand = at("v_shadow", 0.62, 0.42)
items += [Text("रुको!", hand[0], hand[1], 110, S(T(61)) + 0.9, t1=S(T(62)) - 0.1, kind="title", color=LIGHT,
               anim="stamp"),
          Stroke(S(T(61)) + 3.0, 0.3, pts=[(hand[0] - 140, hand[1] - 70), (hand[0] + 140, hand[1] + 70)],
                 width=14, t1=S(T(62)) - 0.1),
          Stroke(S(T(61)) + 3.2, 0.3, pts=[(hand[0] + 140, hand[1] - 70), (hand[0] - 140, hand[1] + 70)],
                 width=14, t1=S(T(62)) - 0.1),
          Text("?", hand[0], hand[1] + 40, 430, S(T(62)) + 0.1, t1=S(T(63)) + 0.8, kind="title", color=RED,
               anim="stamp")]
say("v_shadow", 0.5, 0.1, "अंतिम सच नहीं, एक सवाल", S(T(61)) + 3.4, h=54, t1=S(T(63)) + 0.6)
for n in range(4):
    u, v = (0.62, 0.78 - 0.17 * n)
    say("v_stairs", u + 0.08, v, "+10%", S(T(63)) + 1.0 + 0.75 * n, h=60, kind="num", color=RED, anim="stamp")
say("v_stairs", 0.5, 0.06, "सीमा आगे खिसकती है", S(T(64)) + 1.6, h=60, kind="title")

# ---------------------------------------------------------------- camera: always rising
FULL = 985  # a whole panel fills the frame


def C(name, u=0.5, v=0.5, w=FULL):
    return at(name, u, v) + (w,)


keys = [
    (0.0, *C("v_base", 0.4, 0.74, 640)),
    (S(T(52)) + 1.6, *C("v_base", 0.42, 0.62, 880), "hold"),
    (S(T(53)) + 2.4, *C("v_climb", 0.5, 0.5, FULL), "log"),     # climb the cliff with him
    (S(TE(53)), *C("v_climb", 0.5, 0.46, 900), "hold"),
    (S(T(55)) + 0.4, *C("v_head", 0.5, 0.5, FULL), "vw"),        # up into his head
    (S(T(56)) + 0.3, *C("v_head", 0.48, 0.6, 820), "hold"),
    (S(T(56)) + 2.0, *(BRAIN + (160,)), "log"),                  # dive into the brain
    (S(T(57)) - 0.2, BRAIN[0], BRAIN[1] - 2, 145, "hold"),
    (S(T(57)) + 0.8, DIAL[0], DIAL[1] + 1, 10.5, "log"),        # into the dial: the governor
    (S(T(58)) - 0.1, DIAL[0], DIAL[1] + 1, 9.6, "hold"),
    (S(T(58)) + 1.5, *C("v_track", 0.5, 0.72, 820), "vw"),       # swoop out and up to the track
    (S(T(59)) - 0.3, *C("v_track", 0.5, 0.36, 760), "log"),     # run with them to the tape
    (S(T(59)) + 0.6, *C("v_tank", 0.5, 0.45, FULL), "vw"),
    (S(TE(59)), *C("v_tank", 0.5, 0.42, 880), "hold"),
    (S(T(61)) + 0.6, *C("v_shadow", 0.5, 0.5, FULL), "vw"),
    (S(T(62)), *C("v_shadow", 0.58, 0.45, 820), "hold"),
    (S(T(63)) + 0.9, *C("v_stairs", 0.5, 0.72, 820), "vw"),       # the stairs, step by step
    (S(TE(64)) - 0.3, *C("v_stairs", 0.5, 0.22, 760), "log"),     # up to the flag
    (VOICE_END + 1.9, 0, -5480, 7300, "vw"),                       # the whole climb, base to summit
    (END + 0.5, 0, -5480, 7600, "hold"),
]

# ---------------------------------------------------------------- hook header and call to action


def banner(text, color, px):
    im = text_image(text, "title", color, px)
    return to_surface(im), im.width, im.height


HOOK = [banner("आप सिर्फ़ 40% पर", (240, 236, 228), 92), banner("रुक जाते हैं", (205, 40, 50), 92)]
CTA = banner("पूरी कहानी: चैनल पर पूरा वीडियो", (240, 236, 228), 54)


class ShortFilm(Film):
    def frame(self, t, surf=None):
        surf = super().frame(t, surf)
        ctx = cairo.Context(surf)
        u = clamp(t / 0.5)
        k = 1 + 0.25 * (1 - back_out(u, 2.0)) if u < 1 else 1
        top = H * 0.045
        bh = sum(h for _, _, h in HOOK) - 30
        ctx.set_source_rgba(*INK, 0.86 * clamp(u * 3))
        ctx.rectangle(0, top - 10, W, bh + 20)
        ctx.fill()
        y = top - 18
        for s, sw, sh in HOOK:
            ctx.save()
            ctx.translate(W / 2, y + sh / 2)
            ctx.scale(k, k)
            ctx.set_source_surface(s, -sw / 2, -sh / 2)
            ctx.paint_with_alpha(clamp(u * 3))
            ctx.restore()
            y += sh - 30
        ctx.set_source_rgb(*RED)
        ctx.rectangle(0, top + bh + 10, W * clamp((t - 0.3) / 0.6), 8)
        ctx.fill()
        a = ramp(t, VOICE_END - 0.4, 0.4)
        if a > 0:
            s, sw, sh = CTA
            ctx.set_source_rgba(*RED, 0.92 * a)
            ctx.rectangle((W - sw) / 2 - 20, H * 0.80, sw + 40, sh)
            ctx.fill()
            ctx.set_source_surface(s, (W - sw) / 2, H * 0.80)
            ctx.paint_with_alpha(a)
        return surf


film = ShortFilm(items, Camera(keys, breath=0.008), subs)


def cut_audio(out):
    parts = "".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000[a{i}];" for i, (a, b) in
                    enumerate(RANGES))
    gaps = f"anullsrc=r=48000:cl=mono,atrim=0:{GAP}[g];[g]asplit=2[g0][g1];anullsrc=r=48000:cl=mono,atrim=0:0.4[g9];"
    chain = "[g9][a0][g0][a1][g1][a2]concat=n=6:v=0:a=1[v]"
    subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", "-i", "narration.mp3", "-filter_complex",
                           gaps + parts + chain, "-map", "[v]", out])


if __name__ == "__main__":
    if sys.argv[1] == "still":
        film.still(float(sys.argv[2]), sys.argv[3])
    elif sys.argv[1] == "audio":
        cut_audio(sys.argv[2])
    else:
        film.render(sys.argv[2], 0, END)
