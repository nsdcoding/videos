#!/usr/bin/env python3
"""YouTube thumbnail for Day 02 (1280x720): the real 1944 portrait of Onoda and the 1974 surrender photograph
as mounted prints, on the film's jungle darkened to ink, with display type.

The photographs follow the film's photo-card rules: shown whole (never cropped, tinted, retouched or
colourised), on a matte sampled from their own dark tones, and no larger than their native size."""
import os, sys
import numpy as np
import skia

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
import scenes

TW, TH = 1280, 720
A = scenes.Assets()
s = skia.Surface(TW, TH)
c = s.getCanvas()

# background: the film's clearing, pushed down to deep ink, with a warm light falling from the top right
c.save()
c.scale(TW / E.W, TH / E.H)
E.plate(A.plate("jungle_clearing"))(c, 0)
c.restore()
c.drawRect(skia.Rect.MakeWH(TW, TH), E.fill(E.INK, 0.86))
glow = E.fill(E.MUSTARD, 0.22)
glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 120))
c.drawCircle(1000, 260, 340, glow)
vig = skia.Paint(Shader=skia.GradientShader.MakeRadial(
    (640, 360), 820, [skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, 0.55)], [0.45, 1.0]))
c.drawRect(skia.Rect.MakeWH(TW, TH), vig)


def print_card(ph, cx, cy, tilt, label, label_rgb):
    """A photograph mounted whole at native size (never larger), with a soft shadow and a date tab."""
    iw, ih = ph.native
    m = 12
    w, h = iw + 2 * m, ih + 2 * m
    c.save()
    c.translate(cx, cy)
    c.rotate(tilt)
    card = skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h)
    c.drawRect(card.makeOffset(14, 20), E.shadow_paint(0.6, 22))
    c.drawRect(card, E.fill(E.CREAM))
    c.drawRect(card.makeInset(5, 5), E.fill(ph.matte))
    c.drawImageRect(ph.img, skia.Rect.MakeXYWH(-iw / 2, -ih / 2, iw, ih), E.CUBIC, skia.Paint(AntiAlias=True))
    f = E.head_font(40)
    tw = E.text_width(label, f)
    tab = skia.Rect.MakeXYWH(-w / 2 + 18, h / 2 - 30, tw + 40, 60)
    c.drawRoundRect(tab.makeOffset(5, 5), 10, 10, E.fill(E.INK))
    c.drawRoundRect(tab, 10, 10, E.fill(label_rgb))
    E.text(c, label, -w / 2 + 38, h / 2 + 14, f, E.CREAM if label_rgb == E.RUST else E.INK)
    c.restore()


p_young, p_1974 = A.photo("p02"), A.photo("p09")
print_card(p_1974, 1035, 420, 4.0, "1974", E.RUST)    # behind
print_card(p_young, 835, 292, -3.5, "1944", E.MUSTARD)  # in front

# type, left column
COL = 560  # the type stays left of the prints


def fit(word, size, maxw):
    while E.text_width(word, E.head_font(size)) > maxw:
        size -= 2
    return E.head_font(size)


E.text(c, "HE KEPT", 64, 175, fit("FIGHTING", 106, COL), E.CREAM)
E.text(c, "FIGHTING", 64, 285, fit("FIGHTING", 106, COL), E.CREAM)
E.text(c, "29 YEARS", 60, 435, fit("29 YEARS", 150, COL), E.MUSTARD)
c.drawLine(68, 470, 68 + COL - 20, 470, E.stroke(E.RUST, 8))
E.text(c, "after World War II ended", 66, 538, E.title_font(42), E.CREAM, 0.95)

from PIL import Image
img = Image.fromarray(s.makeImageSnapshot().toarray()[..., [2, 1, 0]])
out = os.path.join(E.DAY, "out", "thumbnail.jpg")
img.save(out, quality=93)
print(out, img.size, os.path.getsize(out) // 1024, "KB",
      "| photos at native size:", p_young.native, p_1974.native)
