#!/usr/bin/env python3
"""Start a new Math Lab TV video from a topic name and a duration.

  python3 .claude/skills/math-lab-video/scripts/new_video.py <topic words...> [DURATION]
      DURATION: "15-20", "12", "10min" (default 15-20)
  options:
      --slug SLUG             use this catalog slug (skip fuzzy matching)
      --new "Title" SERIES    add a topic that is not in the catalog yet (SERIES = a series id)
      --folder NAME           folder name (default: the slug)
      --dry-run               only resolve the topic and print the brief

What it does: resolves the topic in channel/catalog.json, creates <folder>/ from the skill template,
fills SLUG and the target duration, writes <folder>/BRIEF.md (what to cover, planned visual, callbacks,
promises to pay off, overlaps to avoid, prerequisites, the default teaser), and marks the topic
in-production with its folder and branch.  Exit code 2 = ambiguous topic (candidates printed).
"""
import difflib, json, pathlib, re, shutil, subprocess, sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
sys.path.insert(0, str(REPO / "channel"))
import channel as ch  # noqa: E402


def parse(argv):
    o = dict(words=[], minutes=(15, 20), slug=None, new=None, folder=None, dry=False)
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--slug": o["slug"] = argv[i + 1]; i += 2; continue
        if a == "--new": o["new"] = (argv[i + 1], argv[i + 2]); i += 3; continue
        if a == "--folder": o["folder"] = argv[i + 1]; i += 2; continue
        if a == "--dry-run": o["dry"] = True; i += 1; continue
        m = re.fullmatch(r"(\d+)(?:\s*[-–to]+\s*(\d+))?\s*(min|mins|minutes|m)?", a.strip().lower())
        rest_are_options = all(x.startswith("--") for x in argv[i + 1:])
        if m and (m.group(2) or m.group(3) or rest_are_options):
            lo = int(m.group(1)); hi = int(m.group(2) or m.group(1)); o["minutes"] = (lo, hi)
        else:
            o["words"].append(a)
        i += 1
    return o


def resolve(c, words):
    q = " ".join(words).lower().strip()
    qs = re.sub(r"[^a-z0-9]+", "-", q).strip("-")
    if qs in c["by"]:
        return qs, []
    tok = set(re.findall(r"[a-z0-9]+", q))
    def cover(t):
        tt = set(re.findall(r"[a-z0-9]+", t["title"].lower() + " " + t["slug"].replace("-", " ")))
        return len(tok & tt) / max(1, len(tok))

    def score(t):
        title = t["title"].lower()
        r = difflib.SequenceMatcher(None, q, title).ratio()
        tok = set(re.findall(r"[a-z0-9]+", q)); tt = set(re.findall(r"[a-z0-9]+", title + " " + t["slug"].replace("-", " ")))
        cover = len(tok & tt) / max(1, len(tok))
        return 0.45 * r + 0.55 * cover
    ranked = sorted(c["topics"], key=score, reverse=True)
    best = ranked[0]; s0 = score(best); s1 = score(ranked[1])
    cands = [(t["slug"], t["title"], round(score(t), 2)) for t in ranked[:5]]
    if (s0 >= 0.6 and s0 - s1 >= 0.08) or (cover(best) == 1 and s0 - s1 >= 0.12):
        return best["slug"], cands
    return None, cands


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
    elif o["slug"]:
        slug = o["slug"]
        if slug not in c["by"]: sys.exit(f"unknown slug {slug}")
    else:
        slug, cands = resolve(c, o["words"])
        if not slug:
            print("Ambiguous topic. Closest catalog entries (slug, title, score):")
            for s, t_, sc in cands: print(f"  {s:28s} {t_}  ({sc})")
            print('Re-run with --slug <slug>, or --new "Title" <series-id> for a topic that is not in the catalog.')
            sys.exit(2)
    t = c["by"][slug]
    if t["status"] in ch.DONE:
        print(f"note: {slug} is already {t['status']} ({(t.get('production') or {}).get('folder')})")
    text = brief(c, slug, o["minutes"])
    if o["dry"]:
        print(text); return
    folder = REPO / (o["folder"] or slug)
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
    print(f"created {folder.relative_to(REPO)}/ from the template; {slug} → in-production on {branch}")


if __name__ == "__main__":
    main()
