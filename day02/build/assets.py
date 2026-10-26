#!/usr/bin/env python3
"""BUILD_SPEC v3 section 3: generated assets for Day 02 (Nano Banana, style lock appended verbatim).

  python3 build/assets.py sheets            # cast character sheets (step 1: checked by eye first)
  python3 build/assets.py poses [ids...]    # poses, each with --ref to its character sheet
  python3 build/assets.py sets  [ids...]    # full-bleed set plates
  python3 build/assets.py props [ids...]    # prop sheets on magenta

Prompts never carry a real person's name: cast are described by role and costume only, so the
model has nothing to draw a likeness from (spec 3.3). Stops on the first refusal (spec 9);
reruns skip files that exist.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DAY = os.path.dirname(HERE)
RAW = os.path.join(DAY, "images", "raw")
sys.path.insert(0, os.path.join(os.path.dirname(DAY), "skills", "motion-video-style", "scripts"))

STYLE_LOCK = ("Flat vintage editorial illustration, clean confident ink outlines, flat colour fills with subtle "
              "paper grain and light halftone texture, mid-century print style, palette of deep ink green #26392b, "
              "mustard #d4a640, cream #f3e7cf, olive #6d6a3a and a rust #b5522f accent, clearly illustrated and not "
              "photorealistic, no text, no lettering, no numbers, no watermarks.")

FACE = ("The face is deliberately vague and simple: two small dot eyes, short brow lines and a small line for a "
        "mouth, no nose detail, no wrinkles, no attempt at a portrait or a likeness of any real person.")

SHEET = ("Character model sheet of ONE cartoon character drawn four times in a single row, evenly spaced with wide "
         "gaps: front view, three-quarter view, side view facing right, and back view. Full body, standing upright "
         "and relaxed, arms at the sides, feet visible, same height in every view. Plain flat cream background, "
         "nothing else in the image. ")

SHEETS = {
    "onoda": SHEET + "The character: a lean young Japanese soldier of the 1940s in a faded, patched olive field "
             "uniform with puttees, a soft field cap with a neck flap, a canvas haversack and a bolt-action rifle "
             "slung on his back by its strap, barrel pointing up. Short black hair under the cap. " + FACE,
    "onoda_civilian": SHEET + "The same young man as the reference sheet, now as a civilian: a plain 1940s "
                      "dark olive suit, white shirt, narrow tie, short neat black hair, no hat. Same build, same "
                      "simple face. " + FACE,
    "onoda_older": SHEET + "The same man as the reference sheet, now in his fifties in 1974: lean, very upright "
                   "posture, short greying hair, a plain dark suit and white shirt. Same simple face. " + FACE,
    "taniguchi": SHEET + "The character: a Japanese army major of 1944 in a neat olive officer's tunic with a "
                 "high collar, riding breeches, tall brown boots, a peaked officer's cap and a sword in a scabbard "
                 "at his hip. Stocky build, round glasses. " + FACE,
    "taniguchi_bookseller": SHEET + "The same man as the reference sheet, thirty years later in 1974, now a "
                            "bookseller in his sixties: thinning grey hair, round glasses, a mustard knitted "
                            "cardigan over a cream shirt, grey trousers, slippers. Same build, same simple "
                            "face. " + FACE,
    "suzuki": SHEET + "The character: a cheerful Japanese backpacker in his twenties in 1974, shaggy black hair "
              "to the collar, a rust-coloured t-shirt under an open olive shirt, flared blue jeans, hiking boots "
              "and a very large framed backpack with a rolled sleeping mat on top. " + FACE,
    "comrades": ("Character lineup sheet: THREE different cartoon Japanese soldiers of the 1940s standing in a row "
                 "with wide gaps, each shown full body from the front, feet visible. All wear faded, patched olive "
                 "field uniforms, soft field caps with neck flaps and puttees; each has a bolt-action rifle slung on "
                 "his back. Left: the youngest, slight and thin. Middle: tall with broad shoulders. Right: short "
                 "and wiry. Plain flat cream background, nothing else in the image. "
                 "All three faces are deliberately vague and simple: dot eyes, brow lines, a small line mouth, no "
                 "nose detail, no attempt at a portrait or a likeness of any real person."),
    "crowd": ("Lineup sheet of five small groups of cartoon extras standing in a single row with wide gaps, full "
              "body, feet visible: 1) three searchers in 1950s khaki field gear with bush hats and a megaphone; "
              "2) three 1970s press photographers in jackets holding cameras; 3) three people in 1970s clothes, "
              "an airport crowd waving; 4) two ranch hands in wide-brimmed hats and work shirts; 5) three Japanese "
              "schoolchildren in caps with small backpacks. Plain flat cream background, nothing else in the image. "
              "Every face is deliberately vague and simple: dot eyes and a small line mouth, no portraits, no "
              "likeness of any real person."),
}
# outfit sheets are drawn from the main sheet so the character stays identical
SHEET_REF = {"onoda_civilian": "onoda", "onoda_older": "onoda", "taniguchi_bookseller": "taniguchi"}


def gen(vx, prompt, out, aspect="16:9", refs=()):
    if os.path.exists(out):
        return
    vx.image(f"{prompt}\n\n{STYLE_LOCK}", out, aspect, refs)  # exits non-zero on refusal (spec 9)


def main():
    import vertex_assets as va
    kind, only = sys.argv[1], set(sys.argv[2:])
    os.makedirs(RAW, exist_ok=True)
    vx = va.Vertex()
    if kind == "sheets":
        for cid, prompt in SHEETS.items():
            if only and cid not in only:
                continue
            refs = [os.path.join(RAW, f"sheet_{SHEET_REF[cid]}.png")] if cid in SHEET_REF else []
            gen(vx, prompt, os.path.join(RAW, f"sheet_{cid}.png"), "16:9", refs)
    else:
        sys.exit(f"unknown kind {kind}")


if __name__ == "__main__":
    main()
