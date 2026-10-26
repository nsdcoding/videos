#!/usr/bin/env python3
"""Assemble a spec-v3 build.json from a day module and check it against BUILD_SPEC v3 section 4 and 8.

  python3 assemble.py day01      # reads days/day01.py, writes out/day01.build.json

A day module defines META (day, title, runtime_target_sec, audio, notes), PHOTOS {id: entry},
SEGMENTS (ordered segment ids from narration.md) and BEATS: a list of dicts with
  seg: "s01" or ["s01", "s02"], scenes: [...], energy, photo: (ref, entry[, hold]), graphics, note,
  transition, title_overlay, labels.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BANNED = [r"\bphotoreal", r"\bphotograph of\b", r"\bface\b(?! turned| away| hidden| in shadow| unseen| down)",
          r"\bportrait\b", r"\btext\b(?! rendered)", r"\blettering\b", r"\blabel(s|led)?\b", r"\bcorpse", r"\bbod(y|ies)\b",
          r"\bblood", r"\bwound", r"\bremains\b", r"\bnumbers?\b",
          r"\b(bust|statue|sculpture)s?\b(?!.*\b(behind|silhouette|turned)\b)"]
ENTRIES = {"slide_up", "slide_left", "slide_right", "drop", "flip", "pin", "grow"}
ENERGY = {"high", "calm", "still"}


def house_format(doc):
    """Like the existing build files: top-level keys indented, one photo and one beat per line."""
    d = lambda v: json.dumps(v, ensure_ascii=False)
    lines = ["{"]
    keys = list(doc)
    for i, k in enumerate(keys):
        end = "," if i < len(keys) - 1 else ""
        v = doc[k]
        if k == "photos":
            lines.append(f' "photos": {{')
            items = list(v.items())
            for j, (pid, p) in enumerate(items):
                lines.append(f"  {d(pid)}: {d(p)}" + ("," if j < len(items) - 1 else ""))
            lines.append(" }" + end)
        elif k in ("beats", "notes"):
            lines.append(f" {d(k)}: [")
            for j, b in enumerate(v):
                lines.append(f"  {d(b)}" + ("," if j < len(v) - 1 else ""))
            lines.append(" ]" + end)
        else:
            lines.append(f" {d(k)}: {d(v)}{end}")
    lines.append("}")
    out = "\n".join(lines) + "\n"
    json.loads(out)
    return out


def load(day):
    spec = importlib.util.spec_from_file_location(day, os.path.join(HERE, "days", f"{day}.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main(day):
    m = load(day)
    problems, used = [], set()
    for pid, p in m.PHOTOS.items():
        for k in ("title", "file_url", "page_url", "author", "licence"):
            if not p.get(k):
                problems.append(f"photo {pid} missing {k}")
        if not p["file_url"].startswith("https://upload.wikimedia.org/"):
            problems.append(f"photo {pid} file_url is not a direct upload.wikimedia.org URL")
    beats, covered = [], []
    for b in m.BEATS:
        segs = [b["seg"]] if isinstance(b["seg"], str) else list(b["seg"])
        covered += segs
        out = {"segments": segs, "energy": b.get("energy", "high"), "scenes": b.get("scenes", [])}
        if out["energy"] not in ENERGY:
            problems.append(f"{segs[0]} energy {out['energy']}")
        if b.get("photo"):
            ref, entry, *rest = b["photo"]
            if ref not in m.PHOTOS:
                problems.append(f"{segs[0]} photo {ref} not in library")
            if entry not in ENTRIES:
                problems.append(f"{segs[0]} entry {entry}")
            used.add(ref)
            out["photo"] = {"ref": ref, "entry": entry, "hold": rest[0] if rest else "beat"}
        for k in ("graphics", "transition", "title_overlay", "labels", "note"):
            if b.get(k):
                out[k] = b[k]
        for s in out["scenes"]:
            for pat in BANNED:
                if re.search(pat, s, re.I):
                    problems.append(f"{segs[0]} scene matches {pat!r}: {s[:70]}")
        beats.append(out)
    if covered != list(m.SEGMENTS):
        missing = [s for s in m.SEGMENTS if s not in covered]
        extra = [s for s in covered if s not in m.SEGMENTS or covered.count(s) > 1]
        problems.append(f"coverage: missing {missing} extra/dup {sorted(set(extra))} order_ok={sorted(covered) == sorted(m.SEGMENTS)}")
    unused = sorted(set(m.PHOTOS) - used)
    if unused:
        problems.append(f"photos never shown: {unused}")
    if sum(1 for b in beats if b.get("title_overlay")) != 1:
        problems.append("title_overlay must appear exactly once")
    doc = {"spec_version": "v3", **m.META, "photos": m.PHOTOS, "beats": beats}
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    path = os.path.join(HERE, "out", f"{day}.build.json")
    with open(path, "w", encoding="utf-8") as f:
        f.write(house_format(doc))
    n_sc = sum(len(b["scenes"]) for b in beats)
    n_ph = sum(1 for b in beats if "photo" in b)
    print(f"{day}: {len(beats)} beats, {n_sc} scenes, {n_ph} photo cards, {len(m.PHOTOS)} photos, {os.path.getsize(path)} bytes")
    for p in problems:
        print("  PROBLEM:", p)
    return not problems


if __name__ == "__main__":
    ok = all(main(d) for d in sys.argv[1:])
    sys.exit(0 if ok else 1)
