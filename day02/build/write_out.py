#!/usr/bin/env python3
"""Write out/: subtitles.srt (spec 7), credits.txt and description.txt (spec 8), checklist.md (spec 10)."""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E

OUT = os.path.join(E.DAY, "out")
build = json.load(open(os.path.join(E.DAY, "build.json")))
tl = E.Timeline(build)
os.makedirs(OUT, exist_ok=True)

E.write_srt(E.cues(tl), os.path.join(OUT, "subtitles.srt"))

# credits: every photo used, grouped by licence, one line each
groups = {}
for p in build["photos"].values():
    groups.setdefault(p["licence"], []).append(p)
order = sorted(groups, key=lambda k: (not k.startswith("CC"), k))
lines = []
for lic in order:
    lines.append(lic)
    lines += [f"{p['title']} — {p['author']} — {p['licence']} — {p['page_url']}" for p in groups[lic]]
    lines.append("")
credits = "\n".join(lines).rstrip() + "\n"
open(os.path.join(OUT, "credits.txt"), "w", encoding="utf-8").write(credits)


def stamp(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02}"


chapters = [("s01", "9 March 1974"), ("s08", "An ordinary young man"), ("s09", "The Nakano School"),
            ("s12", "Lubang, December 1944"), ("s16", "The war ends; nobody believes it"),
            ("s17", "Why he did not believe it"), ("s23", "Twenty-nine years"), ("s24", "The islanders"),
            ("s28", "The group shrinks"), ("s33", "Norio Suzuki"), ("s41", "The bookseller"),
            ("s44", "The order is rescinded"), ("s48", "Japan, 1974"), ("s53", "Brazil, and after"),
            ("s58", "In his own terms, right")]
chap = "\n".join(f"{'0:00' if sid == 's01' else stamp(tl.start(sid))} {name}" for sid, name in chapters)

description = f"""{build['title']}

On 9 March 1974 a sixty-one-year-old bookseller flew from Japan to Lubang Island in the Philippines, walked into the jungle and read an order aloud to a man standing at attention in a patched uniform. Second Lieutenant Hiroo Onoda had been holding out since 1944. This is the story of the order that kept him there, the reasoning that made every proof of peace look like a trap, the islanders who died because of it, and the young traveller who finally found him.

CHAPTERS
{chap}

Photographs are from Wikimedia Commons (credits below). The illustrations and animation are AI-generated: they are not photographs and do not depict real people's likenesses. Narration is a synthetic voice.

SOURCES
- Hiroo Onoda, "No Surrender: My Thirty-Year War" (1974; English translation by Charles S. Terry, Kodansha International). Primary source: Onoda's own memoir.

PHOTO CREDITS
{credits}"""
open(os.path.join(OUT, "description.txt"), "w", encoding="utf-8").write(description)

runtime = tl.total + 1.0 + 6.0
open(os.path.join(OUT, "checklist.md"), "w", encoding="utf-8").write(f"""# Pre-upload checklist

- [ ] Watched end to end at full length
- [ ] No generated image is photoreal, a likeness of a real person, or graphic
- [ ] Every photo credited in `credits.txt`
- [ ] Every `caption` visible for as long as its card is, and the title overlay appears once
- [ ] Structural silences intact: nothing moving, nothing playing
- [ ] Subtitles synced and free of mis-spelled proper nouns
- [ ] "Altered or synthetic content" toggled in YouTube Studio
- [ ] Description includes attributions, at least one primary source, and the AI-illustration line

## Notes from the build

- Runtime {runtime:.0f} s against `runtime_target_sec` {build['runtime_target_sec']}: the narration at speaking rate
  {build['audio']['speaking_rate']} runs {tl.total:.0f} s. Reported under spec 9; the owner approved shipping at the
  narration's natural length.
- The s07 title is built during the 2.5 s pause after s07, as `title_overlay` (spec 5) and the beat note ask,
  although spec 4.3 says nothing appears during a structural silence. Owner was told.
- Cast arms stay as posed (no swinging or pointing), per the sample review.
""")
print("wrote", sorted(os.listdir(OUT)))
