#!/usr/bin/env python3
"""Start a new Math Lab TV video for a topic the owner picked from the recommendations.

  python3 .claude/skills/math-lab-video/scripts/new_video.py --slug SLUG --minutes 15-20
  options:
      --new "Title" SERIES    the owner wants a topic that is not in the catalog (SERIES = a series id)
      --folder NAME           folder name under math-lab-tv/ (default: the slug)
      --dry-run               only print the brief

Recommendations come from `python3 math-lab-tv/channel/channel.py recommend` (SKILL.md, step 0).
This script creates math-lab-tv/<folder>/ from the skill template, fills SLUG and the target duration,
writes BRIEF.md (what to cover, planned visual, callbacks, promises to pay off, overlaps to avoid,
prerequisites, the default teaser), and marks the topic in-production in the tracker.
"""
import json, pathlib, re, shutil, subprocess, sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
HOME = REPO / "math-lab-tv"                      # everything Math Lab TV lives here, apart from this skill
sys.path.insert(0, str(HOME / "channel"))
import channel as ch  # noqa: E402


def parse(argv):
    o = dict(minutes=(15, 20), slug=None, new=None, folder=None, dry=False)
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--slug": o["slug"] = argv[i + 1]; i += 2
        elif a == "--minutes":
            m = re.fullmatch(r"\s*(\d+)\s*(?:[-–]|to)?\s*(\d+)?\s*(?:min|mins|minutes)?\s*", argv[i + 1].lower())
            if not m: sys.exit(f"--minutes: expected e.g. 15-20 or 12, got {argv[i + 1]!r}")
            o["minutes"] = (int(m.group(1)), int(m.group(2) or m.group(1))); i += 2
        elif a == "--new": o["new"] = (argv[i + 1], argv[i + 2]); i += 3
        elif a == "--folder": o["folder"] = argv[i + 1]; i += 2
        elif a == "--dry-run": o["dry"] = True; i += 1
        else: sys.exit(f"unknown argument {a!r}\n{__doc__}")
    if not (o["slug"] or o["new"]):
        sys.exit("pass --slug (from `channel.py recommend`) or --new \"Title\" SERIES")
    return o


def brief(c, slug, minutes):
    t = c["by"][slug]; r = ch.refs(c, slug)
    lo, hi = minutes
    def desc(s):
        x = c["by"][s]; p = x.get("production") or {}
        extra = []
        if p.get("running_example"): extra.append(f"running example: {p['running_example']}")
        if p.get("hook"): extra.append(f"hook: {p['hook']}")
        if x.get("youtube"): extra.append(x["youtube"])
        return f"- `{s}`: **{x['title']}** ({x['status']})" + ("\n  - " + "\n  - ".join(extra) if extra else "")
    sec = lambda name, xs, note: [f"### {name}", f"_{note}_", ""] + ([desc(s) for s in xs] or ["- none"]) + [""]
    series = next(s["name"] for s in c["series"] if s["id"] == t["series"])
    out = [f"# Brief: {t['title']}", "",
           f"- slug: `{slug}` · series: {series}" + (f" (phase {t['phase']})" if t.get("phase") else ""),
           (f"- target: {lo}–{hi} min → about {lo * 150}–{hi * 150} narration words" if hi != lo else
            f"- target: {lo} min → about {lo * 150} narration words") + " (voice ≈165 wpm plus pauses)",
           "", "## What the owner planned", "", f"**Must cover:** {t['covers']}", "", f"**Planned visual:** {t['visual']}", ""]
    if t.get("notes"):
        out += [f"**Notes:** {t['notes']}", ""]
    out += ["## Connections (from the channel tracker)", ""]
    out += sec("Pay off this promise", r["promised_by"], "a previous video's teaser promised this one: open the lesson by paying it off")
    out += sec("Callbacks", r["callbacks"], "finished videos to reference naturally (1–3 times), on screen and in the narration")
    out += sec("Overlaps", r["overlaps"], "same idea from another angle: use a DIFFERENT running example and refer to it")
    out += sec("Prerequisites not made yet", r["prerequisites_not_made"], "give a 1–2 sentence intuition instead of assuming them")
    out += sec("Default teaser", [r["tease_next"]] if r["tease_next"] else [], "the NEXT TIME topic unless the owner picks another (confirm at checkpoint 1)")
    out += sec("Leads to", r["leads_to"], "later videos this one sets up: plant a seed for them where natural")
    return "\n".join(out) + "\n"


def main():
    o = parse(sys.argv[1:])
    c = ch.load()
    if o["new"]:
        title, series = o["new"]
        if series not in {s["id"] for s in c["series"]}:
            sys.exit(f"unknown series {series!r}; one of {[s['id'] for s in c['series']]}")
        slug = o["slug"] or re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        if slug in c["by"]:
            sys.exit(f"{slug} already exists")
        order = 1 + max(t["order"] for t in c["topics"] if t["series"] == series)
        t = dict(slug=slug, title=title, series=series, order=order, phase=None, status="planned",
                 visual="", covers="", links=dict(builds_on=[], related=[], overlaps=[]), production=None,
                 youtube=None, notes="added by new_video.py: fill covers/visual/links in catalog.json")
        c["topics"].append(t); c["by"][slug] = t
        ch.save(c); c = ch.load()
    else:
        slug = o["slug"]
        if slug not in c["by"]: sys.exit(f"unknown slug {slug}; see `channel.py recommend` or channel/README.md")
    t = c["by"][slug]
    if t["status"] in ch.DONE:
        print(f"note: {slug} is already {t['status']} ({(t.get('production') or {}).get('folder')})")
    text = brief(c, slug, o["minutes"])
    if o["dry"]:
        print(text); return
    folder = HOME / (o["folder"] or slug)
    if folder.exists() and any(folder.iterdir()):
        sys.exit(f"{folder} already exists and is not empty (continue working there, or pass --folder)")
    shutil.copytree(SKILL / "template", folder, dirs_exist_ok=True)
    for f in ("script_src.py", "package.py"):
        p = folder / f; p.write_text(p.read_text().replace('SLUG = "FILL-slug"', f'SLUG = "{slug}"'))
    p = folder / "script_src.py"
    p.write_text(p.read_text().replace("TARGET_MIN = (15, 20)", f"TARGET_MIN = {tuple(o['minutes'])}"))
    (folder / "scenes").mkdir(exist_ok=True)
    (folder / "BRIEF.md").write_text(text)
    branch = subprocess.run(["git", "-C", str(REPO), "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    t["status"] = "in-production"
    t["production"] = {**(t.get("production") or {}), "folder": folder.name, "branch": branch or None}
    ch.save(c); ch.render(ch.load())
    print(text)
    print(f"created {folder.relative_to(REPO)}/ from the template; {slug} → in-production (branch {branch})")


if __name__ == "__main__":
    main()
