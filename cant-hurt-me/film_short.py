"""YouTube Short (9:16): the 40% rule, cut from the main film's world, then the promo.

Same world, same overlays, same narration; only the frame is vertical and the camera
frames each panel tighter so its subject fills the tall screen.

  python3 film_short.py still 250 out.png
  python3 film_short.py render out.mp4
"""
import os
import sys

os.environ["FORMAT"] = "short"

import cairo  # noqa: E402

import film as F  # noqa: E402
from engine import (H, INK, RED, W, Bar, Camera, Counter, Dot, Film, Stroke, Text,  # noqa: E402
                    back_out, clamp, ramp, text_image, to_surface)

T0 = F.T(51) - 0.4  # the "चालीस प्रतिशत का नियम" heading stamps in on the first frames
T1 = F.TE(64) + 0.7  # "...आपकी सीमा को असल में आगे खिसका देता है।"
PANEL_FRAC = 0.42  # vertical view width as a share of the landscape shot's width
HEADING_FRAC = 0.62


def short_keys():
    # stop before the climb toward the next chapter's title
    shots = sorted((s for s in F.SHOTS if T0 - 0.6 <= s[0] < F.T(65) - 2.5), key=lambda s: s[0])
    t, x, y, w = shots[0][:4]
    keys = [(T0, x, y, w * HEADING_FRAC)]
    prev, prev_push = keys[0], 0.95
    for n, (t, x, y, w, mode, move, push) in enumerate(shots[1:]):
        # never closer than the whole panel height, so the labels keep their room above it
        w = max(w * PANEL_FRAC, 0.4 * 1800)
        depart = max(prev[0] + 0.35, t - move)
        if t <= depart + 0.2:
            t = depart + 0.5
        push = push or (0.93 if n % 4 else 1.05)
        keys.append((depart, prev[1], prev[2], prev[3] * prev_push, "hold"))
        keys.append((t, x, y, w, mode))
        prev, prev_push = keys[-1], push
    keys.append((T1 + 0.5, prev[1], prev[2], prev[3] * prev_push, "hold"))
    return keys


def banner(text, color, px):
    im = text_image(text, "title", color, px)
    return to_surface(im), im.width, im.height


HOOK = [banner("आप सिर्फ़ 40% पर", (240, 236, 228), 96), banner("रुक जाते हैं", (205, 40, 50), 96)]
CTA = banner("पूरी कहानी: चैनल पर पूरा वीडियो", (240, 236, 228), 54)


class ShortFilm(Film):
    def frame(self, t, surf=None):
        surf = super().frame(t, surf)
        ctx = cairo.Context(surf)
        # hook header: stamps in on the first beat and stays, like a Shorts title card
        u = clamp((t - T0) / 0.5)
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
        ctx.rectangle(0, top + bh + 10, W * clamp((t - T0 - 0.3) / 0.6), 8)
        ctx.fill()
        # call to action over the last seconds before the promo
        a = ramp(t, T1 - 3.2, 0.4)
        if a > 0:
            s, sw, sh = CTA
            ctx.set_source_rgba(*RED, 0.92 * a)
            ctx.rectangle((W - sw) / 2 - 20, H * 0.80, sw + 40, sh)
            ctx.fill()
            ctx.set_source_surface(s, (W - sw) / 2, H * 0.80)
            ctx.paint_with_alpha(a)
        return surf


# The main film lays this chapter's labels out for a wide frame; in a tall frame they pile up.
# Drop them (keeping the chapter title and the ridge climb) and lay out new ones down the middle.
LABEL_TYPES = (Text, Counter, Stroke, Bar, Dot)
items = [it for it in F.items if not (isinstance(it, LABEL_TYPES) and F.T(52) - 0.5 <= it.t0 <= T1)]


def say(panel, v, text, t, t1=1e9, h=62, **kw):
    x, y = F.at(panel, 0.5, v)
    items.append(Text(text, x, y, h, t, t1=t1, **kw))


T = F.T
say("exhausted", 0.13, "सबसे मशहूर विचार", T(52) + 0.2)
say("exhausted", 0.24, "“अब और नहीं…”", T(53) + 0.6, color=RED, h=80, kind="title", anim="stamp")
items.append(Counter(*F.at("fuel_gauge", 0.5, 0.52), 230, T(53) + 3.7, T(53) + 5.6, 0, 40, fmt="{:.0f}%",
                     color=RED))
say("fuel_gauge", 0.13, "सिर्फ़ इतना इस्तेमाल हुआ", T(53) + 4.0)
say("fuel_gauge", 0.72, "मोटा अनुमान, सटीक आँकड़ा नहीं", T(54) + 0.5, h=50)
say("brain_shield", 0.11, "दिमाग़ = शरीर का रक्षक", T(56) + 0.2)
say("brain_shield", 0.21, "केंद्रीय नियंत्रक", T(57) + 0.3, h=80, kind="title", anim="stamp")
say("finish_sprint", 0.14, "आख़िरी सौ मीटर", T(58) + 0.4, h=72, kind="title")
say("finish_sprint", 0.25, "लोग तेज़ हो जाते हैं", T(58) + 1.6, color=RED)
say("tank_cutaway", 0.11, "ईंधन बचा था", T(59) + 0.3)
say("tank_cutaway", 0.2, "दिमाग़ रोके बैठा था", T(59) + 1.6, color=RED)
# the question mark: one idea at a time
say("question", 0.11, "हर दिन ख़ुद को तोड़ना नहीं", T(60) + 0.3, t1=T(61) + 0.3)
say("question", 0.11, "रुकने की आवाज़", T(61) + 0.8, t1=T(62) - 0.1)
say("question", 0.2, "अंतिम सच नहीं", T(61) + 1.8, t1=T(62) - 0.1)
say("question", 0.15, "एक सवाल", T(62) + 0.3, t1=T(63) - 0.1, h=110, kind="title", anim="stamp")
say("question", 0.15, "+10%", T(63) + 0.2, t1=T(64) + 1.0, h=150, kind="num", anim="stamp")
qx, qy = F.at("question", 0.38, 0.66)
items.append(Stroke(T(64) + 0.3, 2.4, pts=[(qx, qy), (qx + 60, qy), (qx + 60, qy - 45), (qx + 120, qy - 45),
                                          (qx + 120, qy - 90), (qx + 180, qy - 90), (qx + 180, qy - 135),
                                          (qx + 240, qy - 135)], width=12, color=INK))
say("question", 0.11, "सीमा आगे खिसकती है", T(64) + 1.3)

film = ShortFilm(items, Camera(short_keys()), F.subs)

if __name__ == "__main__":
    if sys.argv[1] == "still":
        film.still(float(sys.argv[2]), sys.argv[3])
    else:
        film.render(sys.argv[2], T0, T1)
