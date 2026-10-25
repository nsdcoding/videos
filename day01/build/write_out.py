#!/usr/bin/env python3
"""Write out/: subtitles.srt (spec 5), credits.txt and description.txt (spec 6), checklist.md (spec 8)."""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E

OUT = os.path.join(E.DAY, "out")
build = json.load(open(os.path.join(E.DAY, "build.json")))
tl = E.Timeline()
os.makedirs(OUT, exist_ok=True)

E.write_srt(E.cues(tl), os.path.join(OUT, "subtitles.srt"))

groups = {}
for s in build["shots"]:
    if s["type"] == "archival":
        groups.setdefault(s["licence"], []).append(s)
order = sorted(groups, key=lambda k: (not k.startswith("CC BY"), k))
lines = []
for lic in order:
    lines.append(f"{lic}")
    lines += [f"{s['title']} — {s['author']} — {s['licence']} — {s['page_url']}" for s in groups[lic]]
    lines.append("")
credits = "\n".join(lines).rstrip() + "\n"
open(os.path.join(OUT, "credits.txt"), "w", encoding="utf-8").write(credits)

description = f"""{build['title']}

On 6 August 1945 Tsutomu Yamaguchi, a 29-year-old Mitsubishi engineer, turned back for his personal seal and was three kilometres from the centre of Hiroshima when the first atomic bomb exploded. Three days later, back at work in Nagasaki, he was three kilometres from the second. This is the story of the detour, the journey home, and the sixty-five years he spent not talking about it.

Photographs are from Wikimedia Commons (credits below). Maps, diagrams and illustrations are AI-generated and do not depict real events, people or places. Narration is a synthetic voice.

SOURCES
- United States Strategic Bombing Survey, "The Effects of Atomic Bombs on Hiroshima and Nagasaki" (30 June 1946). Primary source. Truman Library record: https://www.presidentialtimeline.org/html/record_id-93.html — full text: https://www.atomicarchive.com/resources/documents/bombing-survey/index.html
- Associated Press obituary of Tsutomu Yamaguchi (January 2010): https://www.legacy.com/legacy/notable-deaths/tsutomu-yamaguchi

PHOTO CREDITS
{credits}"""
open(os.path.join(OUT, "description.txt"), "w", encoding="utf-8").write(description)

open(os.path.join(OUT, "checklist.md"), "w", encoding="utf-8").write("""# Pre-upload checklist

- [ ] Watched end to end at full length
- [ ] No generated image depicts a real event, person or place
- [ ] Every CC BY and CC BY-SA image credited in `credits.txt`
- [ ] Every `caption` visible for the whole of its shot, and the title overlay appears once
- [ ] Structural silences intact, nothing playing under them
- [ ] Subtitles synced and free of mis-spelled proper nouns
- [ ] "Altered or synthetic content" toggled in YouTube Studio
- [ ] Description includes attributions and at least one primary source
""")
print("wrote", sorted(os.listdir(OUT)))
