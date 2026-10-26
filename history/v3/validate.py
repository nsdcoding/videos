#!/usr/bin/env python3
"""Check a spec-v3 build.json against BUILD_SPEC v3 sections 3.3-3.4, 5 and 9.

  python3 validate.py out/day02.build.json 62     # 62 = number of segments in narration.md (s01..s62)
"""
import json, re, sys

BANNED = [r"\bphotoreal", r"\bphotograph of\b", r"\bportrait\b", r"\btext\b(?! rendered)", r"\blettering\b",
          r"\blabel(s|led)?\b", r"\bcorpse", r"\bbod(y|ies)\b(?! language)", r"\bblood", r"\bwound", r"\bremains\b",
          r"\bnumbers?\b", r"\b(bust|statue|sculpture)s?\b(?!.*\b(behind|silhouette|turned)\b)"]
FACE = r"\bfaces?\b(?! turned| away| hidden| in shadow| unseen| down| out of)"
ENTRIES = {"slide_up", "slide_left", "slide_right", "drop", "flip", "pin", "grow"}
ENERGY = {"high", "calm", "still"}


def scan(where, s, problems, faces=True):
    for pat in BANNED + ([FACE] if faces else []):
        if re.search(pat, s, re.I):
            problems.append(f"{where} matches {pat!r}: {s[:90]}")


path, n = sys.argv[1], int(sys.argv[2])
raw = open(path, encoding="utf-8").read()
doc = json.loads(raw)
P = []
if doc.get("spec_version") != "v3":
    P.append("spec_version is not v3")
cast, sets, props, photos = doc["cast"], doc["sets"], doc["props"], doc["photos"]
for cid, c in cast.items():
    if c.get("face", "vague") not in ("vague", "hidden"):
        P.append(f"cast {cid} face {c.get('face')}")
    scan(f"cast {cid}", c["desc"], P, faces=False)
for k, v in sets.items():
    scan(f"set {k}", v, P)
for k, v in props.items():
    scan(f"prop {k}", v, P)
for pid, p in photos.items():
    for k in ("title", "file_url", "page_url", "author", "licence"):
        if not p.get(k):
            P.append(f"photo {pid} missing {k}")
    if not p["file_url"].startswith("https://upload.wikimedia.org/wikipedia/commons/"):
        P.append(f"photo {pid} file_url not direct")
    if not p["page_url"].startswith("https://commons.wikimedia.org/wiki/File:"):
        P.append(f"photo {pid} page_url not a Commons file page")
covered, used = [], {"cast": set(), "poses": set(), "sets": set(), "props": set(), "photos": set()}
overlays = 0
for b in doc["beats"]:
    sid = b["segments"][0]
    covered += b["segments"]
    if b.get("energy", "high") not in ENERGY:
        P.append(f"{sid} energy")
    if b.get("set") is not None:
        if b["set"] not in sets:
            P.append(f"{sid} set {b['set']} undeclared")
        used["sets"].add(b["set"])
    for entry in b.get("cast", []):
        cid, pose = entry[0], entry[1]
        if cid not in cast:
            P.append(f"{sid} cast {cid} undeclared")
            continue
        if pose not in cast[cid]["poses"]:
            P.append(f"{sid} pose {cid}.{pose} undeclared")
        used["cast"].add(cid)
        used["poses"].add(f"{cid}.{pose}")
    for pr in b.get("props", []):
        if pr not in props:
            P.append(f"{sid} prop {pr} undeclared")
        used["props"].add(pr)
    if "photo" in b:
        if b["photo"]["ref"] not in photos:
            P.append(f"{sid} photo {b['photo']['ref']} undeclared")
        if b["photo"]["entry"] not in ENTRIES:
            P.append(f"{sid} entry {b['photo']['entry']}")
        used["photos"].add(b["photo"]["ref"])
    overlays += bool(b.get("title_overlay"))
expected = [f"s{i:02d}" for i in range(1, n + 1)]
if covered != expected:
    P.append(f"coverage: missing {[s for s in expected if s not in covered]}, "
             f"dup/extra {sorted({s for s in covered if covered.count(s) > 1 or s not in expected})}")
for kind, decl in (("cast", cast), ("sets", sets), ("props", props), ("photos", photos)):
    unused = sorted(set(decl) - used[kind])
    if unused:
        P.append(f"{kind} never used: {unused}")
declared_poses = {f"{c}.{p}" for c, v in cast.items() for p in v["poses"]}
if declared_poses - used["poses"]:
    P.append(f"poses never used: {sorted(declared_poses - used['poses'])}")
if overlays != 1:
    P.append(f"title_overlay appears {overlays} times")
print(f"{path}: {len(doc['beats'])} beats · cast {len(cast)} ({len(declared_poses)} poses) · sets {len(sets)} · "
      f"props {len(props)} · photos {len(used['photos'])}/{len(photos)} · {len(raw.encode())} bytes")
for p in P:
    print("  PROBLEM:", p)
sys.exit(1 if P else 0)
