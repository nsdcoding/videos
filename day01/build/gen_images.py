#!/usr/bin/env python3
"""Generate the `generated` shots in build.json with Nano Banana, style lock appended verbatim (spec 3).

  python3 build/gen_images.py            # all generated shots
  python3 build/gen_images.py s01 s09    # shots whose first segment is in this range
Stops on the first refusal or failure (spec 7); reruns skip finished files.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); DAY = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(DAY), "skills", "motion-video-style", "scripts"))
STYLE_LOCK = ("Muted desaturated palette, warm grey and ink tones, soft directional light,\n"
              "film grain, shallow depth of field, no text, no lettering, no watermarks,\n"
              "no identifiable human faces, editorial illustration, not photorealistic.")
shots = json.load(open(os.path.join(DAY, "build.json")))["shots"]
lo, hi = (sys.argv[1], sys.argv[2]) if len(sys.argv) == 3 else ("s00", "s99")
import vertex_assets as va
vx = None
os.makedirs(os.path.join(DAY, "images"), exist_ok=True)
for s in shots:
    sid = s["segments"][0]
    if s["type"] != "generated" or not (lo <= sid <= hi):
        continue
    out = os.path.join(DAY, "images", f"{sid}_generated.png")
    if os.path.exists(out):
        continue
    vx = vx or va.Vertex()
    vx.image(f"{s['prompt']}\n\n{STYLE_LOCK}", out, "16:9")  # exits non-zero on refusal/failure
