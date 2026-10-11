import subprocess, os
from concurrent.futures import ThreadPoolExecutor
G = ["python3", "../../gen.py", "image"]
C = "Same layered PAPER-CUT style as the references (cut paper layers, paper fibre texture, crisp cut edges, soft depth), palette navy, teal, coral, sand cream, soft gold."
M = "Plain solid flat magenta #FF00FF background, no shadow on background, no text, no letters."
CH = "the SAME woman Ananya from the character sheet reference (same face, hair in low ponytail, gold studs, teal kurta, coral dupatta, sand trousers)"
BG = "Full-bleed layered PAPER-CUT DIORAMA background plate, edge to edge, NO border, NO frame, no people, no text. Stacked cut-paper layers with soft drop shadows and depth, paper fibre texture. Palette navy, teal, coral, sand cream, soft gold. Leave open space in the lower centre for a character."
jobs = {
 # character poses (full body)
 "a_stand": (f"{CH}, full body, standing front view, gentle smile, arms relaxed. {C} {M}", ["ref/ananya_sheet.png"]),
 "a_worried": (f"{CH}, full body standing, worried and frustrated, one hand on her forehead, eyebrows raised. {C} {M}", ["ref/ananya_sheet.png"]),
 "a_think": (f"{CH}, full body standing, thinking, one hand on her chin, eyes looking up. {C} {M}", ["ref/ananya_sheet.png"]),
 "a_happy": (f"{CH}, full body standing, confident and happy, warm smile, arms loosely crossed. {C} {M}", ["ref/ananya_sheet.png"]),
 "a_run": (f"{CH}, wearing running shoes, full body side view, jogging mid-stride, ponytail flying. {C} {M}", ["ref/ananya_sheet.png"]),
 "a_phone": (f"{CH}, full body standing, looking down at a smartphone in her hands, absorbed, slightly hunched. {C} {M}", ["ref/ananya_sheet.png"]),
 "a_desk": (f"{CH}, sitting on a chair at a small wooden desk working on a laptop, focused, side three-quarter view, full figure with the desk and chair. {C} {M}", ["ref/ananya_sheet.png"]),
 "a_sad": (f"{CH}, sitting on the floor hugging her knees, head lowered, sad and helpless. {C} {M}", ["ref/ananya_sheet.png"]),
 "a_write": (f"{CH}, sitting cross-legged writing in a notebook with a pen, calm. {C} {M}", ["ref/ananya_sheet.png"]),
 "a_shoes": (f"{CH}, full body, bending slightly to tie the laces of her running shoes, ready to go out. {C} {M}", ["ref/ananya_sheet.png"]),
 # heads for close-ups
 "h_neutral": (f"{CH}, head and shoulders portrait, front view, calm neutral friendly face. {C} {M}", ["ref/ananya_sheet.png"]),
 "h_worried": (f"{CH}, head and shoulders portrait, front view, worried anxious face, brows knitted. {C} {M}", ["ref/ananya_sheet.png"]),
 "h_aha": (f"{CH}, head and shoulders portrait, front view, surprised realisation, eyes wide, small open-mouth smile. {C} {M}", ["ref/ananya_sheet.png"]),
 "h_happy": (f"{CH}, head and shoulders portrait, front view, confident content smile. {C} {M}", ["ref/ananya_sheet.png"]),
 # cast
 "cast": (f"Lineup of FIVE different supporting characters, full body front view, each separated by wide gaps: a young Indian man in a shirt holding a new phone, an older uncle in a kurta proudly holding car keys, a young woman colleague with a laptop bag, a middle-aged office manager in a blazer, an elderly grandmother in a saree. {C} {M}", ["ref/ananya_sheet.png"]),
 # props
 "props1": (f"Props sheet, eight separate isolated objects with wide gaps: (1) a running hare, (2) a slow tortoise, (3) a cricket bat with a red ball, (4) a shop price tag on a string, (5) a cube of ice, (6) a pair of running shoes, (7) a smartphone with glowing notification bubbles, (8) a laptop. {C} {M}", ["ref/style_key.png"]),
 "props2": (f"Props sheet, eight separate isolated objects with wide gaps: (1) a piggy bank, (2) a stack of gold coins, (3) a small sapling growing into a tree in a pot, (4) a compass, (5) a glowing paper lantern, (6) a broken chain, (7) an old key, (8) an hourglass. {C} {M}", ["ref/style_key.png"]),
 "props3": (f"Props sheet, eight separate isolated objects with wide gaps: (1) a wall calendar page, (2) an open notebook with pen, (3) an alarm clock, (4) a car steering wheel, (5) a stack of five hardcover books in navy, teal, coral, gold and sand colours (no titles), (6) a balance scale, (7) a glowing light bulb, (8) a red alert notification bell. {C} {M}", ["ref/style_key.png"]),
 # backgrounds
 "bg_bedroom": (f"{BG} Scene: a cosy Indian bedroom at early morning, bed, window with sunrise, wardrobe, plant.", ["ref/style_key.png"]),
 "bg_desk": (f"{BG} Scene: a small home study at night with a desk lamp glow, bookshelf, window with city lights.", ["ref/style_key.png"]),
 "bg_market": (f"{BG} Scene: a colourful Indian market street with small shops, hanging lamps, awnings and shelves of goods.", ["ref/style_key.png"]),
 "bg_office": (f"{BG} Scene: a modern open office with desks, monitors, plants and big windows.", ["ref/style_key.png"]),
 "bg_park": (f"{BG} Scene: a city park running track at sunrise, trees, benches, layered hills behind.", ["ref/style_key.png"]),
 "bg_cafe": (f"{BG} Scene: a warm small cafe interior, tables, hanging lights, a counter.", ["ref/style_key.png"]),
 "bg_dawn": (f"{BG} Scene: a solemn, respectful symbolic landscape: a barbed-wire fence in the foreground silhouette, beyond it a wide empty field and a soft gold dawn breaking over distant hills. Quiet and hopeful.", ["ref/style_key.png"]),
 "bg_mountain": (f"{BG} Scene: a winding mountain path climbing toward a glowing sunrise over layered peaks.", ["ref/style_key.png"]),
 "bg_city": (f"{BG} Scene: an Indian city skyline at night with lit windows, a crescent moon and layered buildings.", ["ref/style_key.png"]),
 "bg_rooftop": (f"{BG} Scene: a rooftop terrace on New Year's night with paper fireworks bursting in the navy sky and string lights.", ["ref/style_key.png"]),
 "bg_plain": (f"Full-bleed plain background, NO border: deep navy blue cut paper with subtle fibre texture and a soft lighter vignette in the centre, completely empty, no objects, no text.", ["ref/style_key.png"]),
}
def run(k):
    out = f"raw/{k}.png"
    if os.path.exists(out): return k
    p, refs = jobs[k]
    r = subprocess.run(G + [p, out, "--ref", *refs], capture_output=True, text=True)
    print(k, "ok" if r.returncode == 0 else "FAIL " + r.stderr[-200:], flush=True)
    return k
with ThreadPoolExecutor(2) as ex: list(ex.map(run, jobs))
print("ALLDONE")
