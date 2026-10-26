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

# ---------------------------------------------------------------- poses (each with --ref to its sheet)
MAG = (" One single full-body figure, centred, filling about three quarters of the image height, feet fully "
       "visible, on a plain flat solid magenta #FF00FF background that fills the whole image right to all four "
       "edges, no border, no frame, nothing else in the image and no ground shadow. ")
GAP = "Both arms hang a little away from the body so a clear strip of magenta shows between each arm and the torso. "
# id -> (sheet refs, split arms?, prompt). Wording carries the beat's action from build.json.
POSES = {
    "onoda/attention": (["onoda"], True, "The same soldier as the reference sheet, front view, standing rigidly at "
        "attention, heels together, chest out, chin up, rifle slung on his back. " + GAP),
    "onoda/hand_over": (["onoda"], False, "The same soldier as the reference sheet, three-quarter view facing right, "
        "standing straight, head slightly bowed, presenting his one rifle lying flat and horizontal across both "
        "open upturned palms at waist height, as if handing it over in a ceremony, the barrel pointing to the "
        "side and slightly down, never aimed. He carries only that one rifle: nothing is slung on his back."),
    "onoda/crouch_watch": (["onoda"], False, "The same soldier as the reference sheet, side view facing right, "
        "crouching low on one knee, watching intently ahead, one hand parting a leaf at head height, rifle held "
        "pointing at the ground."),
    "onoda/civilian_young": (["onoda_civilian"], True, "The same young civilian man as the reference sheet, "
        "three-quarter view facing right, walking with a light confident stride, one foot forward. " + GAP),
    "taniguchi/read_order": (["taniguchi", "taniguchi_bookseller"], False, "The officer from the first reference "
        "sheet in the same old uniform and peaked cap, but now in his sixties with the grey hair and round glasses "
        "of the second reference sheet. Three-quarter view facing right, standing upright and reading aloud from "
        "a single sheet of blank paper held open in both hands at chest height."),
    "taniguchi/bookseller": (["taniguchi_bookseller"], True, "The same bookseller as the reference sheet, "
        "three-quarter view facing left, standing calmly with a small stack of plain books under one arm. " + GAP),
    "crowd/search_party": (["crowd"], False, "Three searchers dressed exactly like the two men on the far left of "
        "the reference sheet: matching khaki 1950s field shirts and trousers, khaki bush hats, boots. They walk in "
        "single file towards the right, side view, close together as one group. The leader holds a megaphone; the "
        "second carries a rolled map; the third a walking stick. No cameras, no weapons."),
}

MATTE = ("Edit this image into a flat colour-coded segmentation matte of the same figure, keeping the exact same "
         "outline, size and position. Fill the whole sleeve and hand on the left side of the image with solid pure "
         "green #00FF00. Fill the whole sleeve and hand on the right side of the image with solid pure blue #0000FF. "
         "Fill the head, cap and neck with solid pure yellow #FFFF00. Fill everything else of the figure with solid "
         "pure black. Keep the magenta background unchanged. No outlines, no shading, no other colours.")

# ---------------------------------------------------------------- sets (full-bleed plates)
PLATE = ("Full-bleed background plate for an animation, edge to edge with no border and no frame, no people, no "
         "animals, open empty ground in the lower centre of the picture. ")

# ---------------------------------------------------------------- props (sheets of three on magenta)
PROPSHEET = ("A prop sheet of exactly {n} separate isolated objects in a single row with very wide magenta gaps "
             "between them, each object whole and not touching any other, plain flat solid magenta #FF00FF "
             "background, no ground shadows, nothing else in the image. From left to right: ")
PROP_SHEETS = [  # sample props first
    ["order", "flag_folded", "bolt"],
    ["leaflets", "loudspeaker", "plane_speaker"],
    ["uniform", "rifle", "lacquerware"],
]


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
    elif kind == "poses":
        import json as _j
        build = _j.load(open(os.path.join(DAY, "build.json")))
        for pid, (refs, _, prompt) in POSES.items():
            cid, pose = pid.split("/")
            if pose not in build["cast"][cid]["poses"]:
                sys.exit(f"STOP: pose {pid} is not declared in build.json")  # spec 9
            if only and pid not in only and cid not in only:
                continue
            out = os.path.join(RAW, f"pose_{cid}_{pose}.png")
            gen(vx, prompt + MAG + FACE, out, "16:9", [os.path.join(RAW, f"sheet_{r}.png") for r in refs])
            if POSES[pid][1]:  # a rig matte: an edit of the pose that colours head and arms for the split
                m = out.replace(".png", "_matte.png")
                gen(vx, MATTE, m, "16:9", [out])
    elif kind == "sets":
        import json as _j
        sets = _j.load(open(os.path.join(DAY, "build.json")))["sets"]
        for sid, prompt in sets.items():
            if only and sid not in only:
                continue
            gen(vx, PLATE + prompt[0].upper() + prompt[1:] + ".", os.path.join(RAW, f"set_{sid}.png"))
    elif kind == "props":
        import json as _j
        props = _j.load(open(os.path.join(DAY, "build.json")))["props"]
        for sheet in PROP_SHEETS:
            if only and not (only & set(sheet)):
                continue
            desc = "; ".join(f"{i + 1}) {props[p]}" for i, p in enumerate(sheet))
            gen(vx, PROPSHEET.format(n=len(sheet)) + desc + ".", os.path.join(RAW, "props_" + "+".join(sheet) + ".png"))
    else:
        sys.exit(f"unknown kind {kind}")


if __name__ == "__main__":
    main()
