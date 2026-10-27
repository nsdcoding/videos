#!/usr/bin/env python3
"""YouTube thumbnail for Day 02 (1280x720), built from the film's own assets: the clearing plate, the cartoon
Onoda at attention (vague face, no likeness) and type set by the animation layer."""
import os, sys
import skia

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
import scenes

A = scenes.Assets()
s = skia.Surface(E.W, E.H)
c = s.getCanvas()
E.plate(A.plate("jungle_clearing"))(c, 0)
c.drawRect(skia.Rect.MakeWH(E.W, E.H), E.fill(E.INK, 0.45))
# a pool of light on the soldier, the rest of the clearing in shadow
glow = E.fill(E.CREAM, 0.35)
glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60))
c.drawOval(skia.Rect.MakeXYWH(1150, 180, 640, 980), glow)
E.actor(A.rig("onoda", "attention"), 1470, 1120, 1020, flip=True, idle=False)(c, 0)
# type
E.text(c, "HE KEPT", 90, 250, E.head_font(150), E.CREAM)
E.text(c, "FIGHTING", 90, 400, E.head_font(150), E.CREAM)
E.text(c, "29 YEARS", 90, 590, E.head_font(190), E.MUSTARD)
r = skia.Rect.MakeXYWH(96, 660, 690, 120)
c.drawRoundRect(r.makeOffset(8, 8), 18, 18, E.fill(E.INK))
c.drawRoundRect(r, 18, 18, E.fill(E.RUST))
E.text(c, "THE WAR ENDED IN 1945", 441, 742, E.head_font(58), E.CREAM, 1, "center")

from PIL import Image
img = Image.fromarray(s.makeImageSnapshot().toarray()[..., [2, 1, 0]]).resize((1280, 720), Image.LANCZOS)
out = os.path.join(E.DAY, "out", "thumbnail.jpg")
img.save(out, quality=92)
print(out, os.path.getsize(out) // 1024, "KB")
