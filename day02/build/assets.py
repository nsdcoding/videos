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
MAG_GROUP = (" The whole group together, every person full body with feet visible, centred and filling about three "
             "quarters of the image height, on a plain flat solid magenta #FF00FF background that fills the whole "
             "image right to all four edges, no border, no frame, nothing else in the image and no ground shadow. ")
GAP = "Both arms hang a little away from the body so a clear strip of magenta shows between each arm and the torso. "
# id -> (sheet refs, split arms?, prompt). Wording carries the beat's action from build.json.
POSES = {
    "onoda/attention": (["onoda"], True, "The same soldier as the reference sheet, front view, standing rigidly at "
        "attention, heels together, chest out, chin up, rifle slung on his back. " + GAP),
    "onoda/hand_over": (["onoda"], False, "The same soldier as the reference sheet, three-quarter view facing right, "
        "standing straight, head slightly bowed, holding his one rifle upright and vertical in front of his chest "
        "with both hands, the muzzle pointing straight up at the sky and the butt near his belt, held out a "
        "little towards someone as if handing it over in a ceremony. Nothing is slung on his back. "),
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
        "three-quarter view facing left, standing calmly, holding nothing, both sleeves the same mustard colour "
        "as the cardigan. " + GAP),
    "onoda/patrol": (["onoda"], False, "The same soldier as the reference sheet, side view facing right, walking "
        "steadily on patrol, rifle slung on his shoulder by its strap, muzzle pointing up behind him."),
    "onoda/listen_sky": (["onoda"], False, "The same soldier as the reference sheet, three-quarter view facing right, "
        "standing still and looking up at the sky, one hand cupped behind his ear, listening."),
    "onoda/study_paper": (["onoda"], False, "The same soldier as the reference sheet, side view facing right, sitting "
        "cross-legged on the ground, studying a single blank sheet of paper held in both hands, frowning slightly."),
    "onoda/clean_rifle": (["onoda"], False, "The same soldier as the reference sheet, side view facing right, sitting "
        "on the ground with his rifle lying across his knees, wiping the rifle carefully with a cloth rag. The rifle "
        "points to the side, at nothing."),
    "onoda/sit_fire": (["onoda"], False, "The same soldier as the reference sheet, side view facing right, sitting on "
        "a low log with his forearms on his knees, rifle leaning upright beside him, talking calmly."),
    "onoda/alone_stand": (["onoda"], False, "The same soldier as the reference sheet, front view, standing alone and "
        "very straight, arms at his sides, rifle slung on his back, gazing ahead."),
    "onoda/suit_crowd": (["onoda_older"], False, "The same man in a dark suit as the reference sheet, three-quarter "
        "view facing right, standing very upright and stiff, hands at his sides, looking slightly away."),
    "onoda/rancher": (["onoda_older"], False, "The same man as the reference sheet, now a cattle rancher in his fifties: "
        "a wide-brimmed hat, a plain work shirt, jeans and boots, riding a brown horse at a walk, side view facing "
        "right, the whole horse visible."),
    "onoda/teacher_kids": (["onoda_older"], False, "The same man as the reference sheet, now in his sixties with grey "
        "hair, in an olive outdoor jacket and hiking trousers, side view facing right, kneeling on one knee and "
        "pointing down at the ground in front of him, explaining patiently."),
    "onoda/old_walk": (["onoda_older"], False, "The same man as the reference sheet, now in his seventies with white "
        "hair, a little stooped, in a plain grey jacket, seen from behind as he walks slowly away from us."),
    "taniguchi/officer_order": (["taniguchi"], False, "The same officer as the reference sheet, in 1944, three-quarter "
        "view facing right, standing upright and holding out a single folded sheet of paper at arm's length in one "
        "hand, as if handing it over."),
    "taniguchi/uniform_again": (["taniguchi", "taniguchi_bookseller"], False, "The officer from the first reference "
        "sheet in the same old uniform, but now in his sixties with the grey hair and round glasses of the second "
        "reference sheet. Front view, standing in front of a mirror-less space, fastening the top button of the tunic "
        "with both hands at his collar, the peaked cap on his head."),
    "suzuki/backpack": (["suzuki"], False, "The same backpacker as the reference sheet, three-quarter view facing "
        "right, standing with his thumbs hooked in the backpack straps, smiling, eager."),
    "suzuki/camp_wait": (["suzuki"], False, "The same backpacker as the reference sheet, without the backpack, side "
        "view facing right, sitting cross-legged on the ground with his hands on his knees, waiting patiently."),
    "suzuki/talk_log": (["suzuki"], False, "The same backpacker as the reference sheet, without the backpack, side "
        "view facing left, sitting on a low log with his elbows on his knees, leaning forward, listening."),
    "suzuki/photograph": (["suzuki"], False, "The same backpacker as the reference sheet, without the backpack, "
        "three-quarter view facing right, standing and holding a small 1970s camera up to his eye, taking a picture."),
    "comrades/four_climb": (["comrades", "onoda"], False, "Four soldiers like the reference sheets, in patched olive "
        "uniforms and soft field caps, rifles slung on their backs, climbing up a slope in single file towards the "
        "right, side view, leaning forward, close together as one group."),
    "comrades/group_fire": (["comrades"], False, "The three soldiers of the reference sheet sitting close together on "
        "the ground, side by side, leaning in towards each other as if talking quietly, rifles leaning beside them, "
        "all full body."),
    "comrades/one_leaves": (["comrades"], False, "The youngest, slightest soldier from the left of the reference sheet "
        "alone, seen from behind three-quarter, walking away towards the left with his head down, rifle slung."),
    "crowd/press": (["crowd"], False, "Three 1970s press photographers like those on the reference sheet, standing "
        "close together as one group, front view, holding their cameras up and taking pictures, one flash bulb "
        "bursting."),
    "crowd/airport": (["crowd"], False, "A tight group of five people in 1970s clothes like the airport crowd on the "
        "reference sheet, front view, waving and cheering, two in front and three behind, all feet visible."),
    "crowd/kids_hike": (["crowd"], False, "Four Japanese schoolchildren like those on the right of the reference sheet, "
        "in caps with small backpacks, hiking in single file towards the right, side view, close together."),
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

SET_DETAIL = {  # added after a plate came back with lettering or a real mark on it
    "tokyo_1974": "The neon signs are plain glowing coloured shapes and stripes with absolutely no characters, letters "
                  "or symbols of any script on them.",
    "airport_1974": "The jet outside is plain cream and olive with no logo, no emblem and no markings at all.",
}

# ---------------------------------------------------------------- props (sheets of three on magenta)
PROPSHEET = ("A prop sheet of exactly {n} separate isolated objects in a single row with very wide magenta gaps "
             "between them, each object whole and not touching any other, plain flat solid magenta #FF00FF "
             "background, no ground shadows, nothing else in the image. From left to right: ")
PROP_DETAIL = {
    "flashbulbs": "a cluster of three bright camera flash bursts, drawn as white and mustard starbursts",
    "tv_wall": "a stacked wall of nine 1970s television sets in wooden cabinets, every screen glowing the same plain "
               "pale cream, nothing shown on the screens",
    "calendar_1945": "a tear-off wall calendar block with a few blank pages curling and flying off the top, no numbers",
    "notebook_sketch": "a traveller's notebook lying open, its pages showing three small simple pencil sketches: a "
                       "soldier's field cap, a panda and a giant footprint, no writing",
    "uniform": "an old 1940s Japanese army officer's uniform laid out flat and neatly folded: an olive tunic with a "
               "high standing collar and brass buttons, and on top of it a peaked officer's cap with a red band",  # extra description where the build file's short prompt was not enough on its own
    "bolt": "a single 1940s bolt-action rifle bolt drawn out of the rifle, lying horizontally: a steel cylinder "
            "with a short bent handle ending in a round knob, seen from the side",
}
PROP_SHEETS = [  # sample props first; a name starting with "x_" marks a rejected object on that sheet
    ["order", "flag_folded", "x_bolt"],
    ["bolt"],
    ["newspapers", "magnifier", "oil_tin"],
    ["bananas", "lean_to", "campfire"],
    ["chess", "lure", "medal"],
    ["tent", "camera", "suitcase"],
    ["notebook_sketch", "memoir", "calendar_1945"],
    ["panda", "footprint", "cattle"],
    ["sword", "ammo", "flashbulbs"],
    ["tv_wall"],
    ["door_one_handle"],
    ["leaflets", "loudspeaker", "plane_speaker"],
    ["x_uniform", "rifle", "lacquerware"],
    ["uniform"],
]


def gen(vx, prompt, out, aspect="16:9", refs=()):
    if os.path.exists(out):
        return
    import time
    for attempt in range(4):
        try:
            vx.image(f"{prompt}\n\n{STYLE_LOCK}", out, aspect, refs)  # exits non-zero on refusal (spec 9)
            return
        except SystemExit as e:
            # a long run of 429s is waited out; anything else (a refusal, a bad request) stops the build
            if "failed after retries" not in str(e) or attempt == 3:
                raise
            print(f"  rate-limited, waiting before retrying {os.path.basename(out)}", file=sys.stderr)
            time.sleep(90)


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
            group = cid in ("crowd", "comrades") and pose != "one_leaves"
            gen(vx, prompt + (MAG_GROUP if group else MAG) + FACE, out, "16:9",
                [os.path.join(RAW, f"sheet_{r}.png") for r in refs])
            if POSES[pid][1]:  # a rig matte: an edit of the pose that colours head and arms for the split
                m = out.replace(".png", "_matte.png")
                gen(vx, MATTE, m, "16:9", [out])
    elif kind == "sets":
        import json as _j
        sets = _j.load(open(os.path.join(DAY, "build.json")))["sets"]
        for sid, prompt in sets.items():
            if only and sid not in only:
                continue
            gen(vx, PLATE + prompt[0].upper() + prompt[1:] + ". " + SET_DETAIL.get(sid, ""), os.path.join(RAW, f"set_{sid}.png"))
    elif kind == "props":
        import json as _j
        props = _j.load(open(os.path.join(DAY, "build.json")))["props"]
        for sheet in PROP_SHEETS:
            if only and not (only & set(sheet)):
                continue
            out = os.path.join(RAW, "props_" + "+".join(sheet) + ".png")
            if os.path.exists(out):
                continue
            desc = "; ".join(f"{i + 1}) {PROP_DETAIL.get(p, props[p])}" for i, p in enumerate(sheet))
            gen(vx, PROPSHEET.format(n=len(sheet)) + desc + ".", out)
    else:
        sys.exit(f"unknown kind {kind}")


if __name__ == "__main__":
    main()
