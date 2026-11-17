#!/usr/bin/env python3
"""Math Lab TV channel tracker: every planned video, its status, and how the videos connect.

Source of truth: channel/catalog.json (topics, status, connections, production details).
YouTube links:   channel/youtube-links.txt (one line per uploaded video: `slug = URL`), easy to edit on GitHub.
Generated view:  channel/README.md (python3 channel/channel.py render).

  python3 channel/channel.py status                 counts per status and the recommended next videos
  python3 channel/channel.py show <slug>            everything about one video, incl. its connections
  python3 channel/channel.py refs <slug>            what to call back to, link to, and tease (for script + description)
  python3 channel/channel.py next [<slug>]          best next video(s), optionally after a given one
  python3 channel/channel.py set <slug> <status>    planned | scripted | in-production | produced | published
  python3 channel/channel.py link <slug> <url>      record the YouTube URL (also marks it published)
  python3 channel/channel.py desc-block <slug>      a ready-to-paste "related videos" block for the description
  python3 channel/channel.py render                 rebuild channel/README.md
"""
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
CAT = HERE / "catalog.json"
LINKS = HERE / "youtube-links.txt"
STATUSES = ["planned", "scripted", "in-production", "produced", "published"]
ICON = {"planned": "⬜", "scripted": "📝", "in-production": "🛠️", "produced": "🎬", "published": "✅"}
DONE = {"produced", "published"}
URL_RE = re.compile(r"^https://(www\.)?(youtube\.com/(watch\?v=|shorts/)|youtu\.be/)[\w\-]{6,}")


# ── data ─────────────────────────────────────────────────────────────
def load():
    c = json.loads(CAT.read_text())
    links = read_links()
    for t in c["topics"]:
        if t["slug"] in links:
            t["youtube"] = links[t["slug"]]
            t["status"] = "published"
    c["by"] = {t["slug"]: t for t in c["topics"]}
    return c


def save(c):
    c = {k: v for k, v in c.items() if k != "by"}
    CAT.write_text(json.dumps(c, indent=1, ensure_ascii=False) + "\n")


def read_links():
    out = {}
    if not LINKS.exists():
        return out
    for n, line in enumerate(LINKS.read_text().splitlines(), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if "=" not in line:
            sys.exit(f"youtube-links.txt line {n}: expected `slug = URL`, got {line!r}")
        slug, url = (x.strip() for x in line.split("=", 1))
        if not URL_RE.match(url):
            sys.exit(f"youtube-links.txt line {n}: {url!r} does not look like a YouTube video URL")
        out[slug] = url
    return out


def title(c, slug):
    return c["by"][slug]["title"]


def leads_to(c, slug):
    """Inverse of builds_on: topics that list `slug` as a prerequisite."""
    return [t["slug"] for t in c["topics"] if slug in t["links"]["builds_on"]]


def ready(c, t):
    """All prerequisites are produced or published."""
    return all(c["by"][p]["status"] in DONE for p in t["links"]["builds_on"])


def rank_next(c, after=None, k=5):
    """Candidates for the next video. Favour: direct follow-ups of `after` (or of any finished video),
    prerequisites already done, ML-series launch phase first, then series order."""
    done = [t["slug"] for t in c["topics"] if t["status"] in DONE]
    anchor = [after] if after else done
    scored = []
    for t in c["topics"]:
        if t["status"] in DONE:
            continue
        s = 0
        for a in anchor:
            if a in t["links"]["builds_on"]: s += 6
            if a in t["links"]["related"]: s += 3
            if a in t["links"]["overlaps"]: s -= 4          # too close to something already made
        promised = [x for x in (anchor if after else done)
                    if (c["by"][x].get("production") or {}).get("teaser_next") == t["slug"]]
        if promised:
            s += 20                                           # we promised it on screen
        if not ready(c, t): s -= 5
        if t["series"] == "ai-ml" and t["phase"]: s += (5 - t["phase"])
        if t["status"] in ("scripted", "in-production"): s += 1
        scored.append((s, -t["order"], t["slug"]))
    scored.sort(reverse=True)
    return [x[2] for x in scored[:k]]


def refs(c, slug):
    t = c["by"][slug]
    L = t["links"]
    made = lambda s: c["by"][s]["status"] in DONE
    teaser = (t.get("production") or {}).get("teaser_next")
    return dict(
        callbacks=[s for s in L["builds_on"] + L["related"] + L["overlaps"] if made(s)],
        prerequisites_not_made=[s for s in L["builds_on"] if not made(s)],
        promised_by=[x["slug"] for x in c["topics"] if (x.get("production") or {}).get("teaser_next") == slug],
        overlaps=L["overlaps"],
        tease_next=teaser or (rank_next(c, after=slug, k=1) or [None])[0],
        leads_to=leads_to(c, slug),
    )


def desc_block(c, slug):
    """Related-video lines for a YouTube description. Only videos with a recorded URL get a link."""
    r = refs(c, slug)
    lines = []
    def line(s, label):
        u = c["by"][s].get("youtube")
        return f"• {label}{title(c, s)}: {u}" if u else None
    seen = set()
    for s in r["promised_by"] + r["callbacks"]:
        if s in seen: continue
        seen.add(s)
        l = line(s, "")
        if l: lines.append(l)
    nxt = r["tease_next"]
    if nxt:
        u = c["by"][nxt].get("youtube")
        lines.append(f"• Next: {title(c, nxt)}" + (f": {u}" if u else " (coming soon, subscribe so you don't miss it)"))
    return "📺 RELATED VIDEOS\n" + "\n".join(lines) if lines else ""


# ── README ───────────────────────────────────────────────────────────
def render(c):
    from collections import Counter
    cnt = Counter(t["status"] for t in c["topics"])
    total = len(c["topics"])
    out = [f"# {c['channel']}: video tracker", "",
           f"_{c['tagline']}_ · generated by `python3 channel/channel.py render` from "
           "[`catalog.json`](catalog.json): edit the data, not this file.", "",
           "| " + " | ".join(f"{ICON[s]} {s}" for s in STATUSES) + " | total |",
           "|" + "---|" * (len(STATUSES) + 1),
           "| " + " | ".join(str(cnt.get(s, 0)) for s in STATUSES) + f" | {total} |", "",
           "**How to add a YouTube link:** edit [`youtube-links.txt`](youtube-links.txt) (one line: `slug = URL`), "
           "or tell Claude \"TOPIC is live at URL\". The link is used in the descriptions of every connected video.", ""]
    # produced / published videos
    made = [t for t in c["topics"] if t["status"] in DONE]
    out += ["## Made so far", "", "| Video | Status | Length | Where | Teaser leads to | YouTube |", "|---|---|---|---|---|---|"]
    for t in made:
        p = t.get("production") or {}
        where = f"`{p['folder']}/` on `{p['branch']}`" if p.get("folder") else (p.get("script") and f"script: `{p['script']}`") or "outside this repo"
        nxt = p.get("teaser_next")
        out.append(f"| **{t['title']}** (`{t['slug']}`) | {ICON[t['status']]} {t['status']} | {p.get('length', '–')} | {where} | "
                   f"{title(c, nxt) if nxt else '–'} | {t.get('youtube') or 'add link'} |")
    out += ["", "## Recommended next", ""]
    for i, s in enumerate(rank_next(c), 1):
        t = c["by"][s]
        why = []
        prom = [x for x in made if (x.get("production") or {}).get("teaser_next") == s]
        if prom: why.append("promised at the end of " + ", ".join(f"*{x['title']}*" for x in prom))
        b = [p for p in t["links"]["builds_on"] if c["by"][p]["status"] in DONE]
        if b: why.append("builds on " + ", ".join(f"*{title(c, p)}*" for p in b))
        if not ready(c, t): why.append("⚠ needs: " + ", ".join(p for p in t["links"]["builds_on"] if c["by"][p]["status"] not in DONE))
        out.append(f"{i}. **{t['title']}** (`{s}`){': ' + '; '.join(why) if why else ''}")
    # connection map around what's made
    out += ["", "## How the made videos connect", "", "```mermaid", "graph LR"]
    node = lambda s: f'{s.replace("-", "_")}["{title(c, s).replace(chr(34), "")}"]'
    edges = set()
    for t in made:
        p = t.get("production") or {}
        if p.get("teaser_next"):
            edges.add(f"  {node(t['slug'])} ==>|teaser| {node(p['teaser_next'])}")
        for x in leads_to(c, t["slug"]):
            edges.add(f"  {node(t['slug'])} --> {node(x)}")
        for x in t["links"]["overlaps"]:
            edges.add(f"  {node(t['slug'])} -.-|overlaps| {node(x)}")
    out += sorted(edges)
    out += [f"  style {t['slug'].replace('-', '_')} fill:#199e70,color:#fff" for t in made]
    out += ["```", "", "Arrows point from a video to the topics that build on it; a thick arrow is the on-screen teaser.", ""]
    # every series
    for s in c["series"]:
        ts = [t for t in c["topics"] if t["series"] == s["id"]]
        done_n = sum(t["status"] in DONE for t in ts)
        out += [f"## {s['name']}  ({done_n}/{len(ts)} made)", "", f"_{s['blurb']}_", "",
                "| # | | Title | Builds on | Leads to | Overlaps | YouTube |", "|---|---|---|---|---|---|---|"]
        for t in ts:
            f = lambda xs: ", ".join(f"`{x}`" for x in xs) or ""
            ph = f" · P{t['phase']}" if t["phase"] else ""
            yt = f"[watch]({t['youtube']})" if t.get("youtube") else ""
            out.append(f"| {t['order']}{ph} | {ICON[t['status']]} | **{t['title']}**<br>`{t['slug']}` | {f(t['links']['builds_on'])} | "
                       f"{f(leads_to(c, t['slug']))} | {f(t['links']['overlaps'])} | {yt} |")
        out.append("")
    out += ["---", "Status key: " + " · ".join(f"{ICON[k]} **{k}**: {v}" for k, v in c["statuses"].items()), ""]
    (HERE / "README.md").write_text("\n".join(out))


# ── CLI ──────────────────────────────────────────────────────────────
def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    c = load()
    cmd = a[0]
    need = lambda: (a[1] if len(a) > 1 and a[1] in c["by"] else sys.exit(f"unknown slug; try one of: {', '.join(list(c['by'])[:8])} …"))
    if cmd == "status":
        from collections import Counter
        cnt = Counter(t["status"] for t in c["topics"])
        print(" · ".join(f"{ICON[s]} {s}: {cnt.get(s, 0)}" for s in STATUSES), f"· total {len(c['topics'])}")
        for t in c["topics"]:
            if t["status"] != "planned":
                print(f"  {ICON[t['status']]} {t['slug']:24s} {t['title']}" + (f"  {t['youtube']}" if t.get("youtube") else ""))
        print("next:", ", ".join(rank_next(c)))
    elif cmd == "show":
        t = c["by"][need()]
        print(json.dumps({**t, "leads_to": leads_to(c, t["slug"]), "refs": refs(c, t["slug"])}, indent=1, ensure_ascii=False))
    elif cmd == "refs":
        s = need(); r = refs(c, s)
        for k, v in r.items():
            v = v if isinstance(v, list) else [v] if v else []
            print(f"{k:24s}", "; ".join(f"{x} ({title(c, x)})" + (f" {c['by'][x]['youtube']}" if c["by"][x].get("youtube") else "") for x in v) or "–")
    elif cmd == "next":
        after = need() if len(a) > 1 else None
        for s in rank_next(c, after=after):
            print(f"{s:28s} {title(c, s)}")
    elif cmd == "set":
        s = need()
        if len(a) < 3 or a[2] not in STATUSES: sys.exit(f"status must be one of {STATUSES}")
        if a[2] == "published" and s not in read_links():
            sys.exit("record the URL with `link <slug> <url>` instead; that marks it published")
        c["by"][s]["status"] = a[2]; save(c); render(load()); print(s, "→", a[2])
    elif cmd == "link":
        s = need()
        if len(a) < 3 or not URL_RE.match(a[2]): sys.exit("usage: link <slug> https://youtu.be/<id>")
        links = read_links(); links[s] = a[2]
        head = [l for l in (LINKS.read_text().splitlines() if LINKS.exists() else []) if l.strip().startswith("#") or not l.strip()]
        LINKS.write_text("\n".join(head).rstrip() + "\n\n" + "\n".join(f"{k} = {v}" for k, v in links.items()) + "\n")
        c2 = load(); render(c2); print(s, "→ published", a[2])
        touch = [x["slug"] for x in c2["topics"] if x["status"] == "published" and x["slug"] != s
                 and (s in refs(c2, x["slug"])["callbacks"] or refs(c2, x["slug"])["tease_next"] == s)]
        if touch:
            print("update the descriptions of these live videos (re-run their package.py):", ", ".join(touch))
    elif cmd == "desc-block":
        print(desc_block(c, need()))
    elif cmd == "render":
        render(c); print("wrote", HERE / "README.md")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
