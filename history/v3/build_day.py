#!/usr/bin/env python3
"""Write out/dayNN.build.json from days/dayNN.py, then validate it.

  python3 build_day.py day01 65

A day module defines META, NOTES, CAST, SETS, PROPS, PHOTOS and BEATS (a list of B(...) calls).
"""
import importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def B(seg, set=..., cast=(), props=(), photo=None, g=(), e="high", cut=False, title=None, labels=None, note=None):
    b = {"segments": [seg] if isinstance(seg, str) else list(seg), "energy": e}
    if set is not ...:
        b["set"] = set
    if cast:
        b["cast"] = [list(c) for c in cast]
    if props:
        b["props"] = list(props)
    if photo:
        ref, entry, *hold = photo
        b["photo"] = {"ref": ref, "entry": entry, "hold": hold[0] if hold else "beat"}
    if g:
        b["graphics"] = list(g)
    if cut:
        b["transition"] = "cut"
    if title:
        b["title_overlay"] = title
    if labels:
        b["labels"] = labels
    if note:
        b["note"] = note
    return b


def photos_from(path):
    """The verified photo library from an earlier file, so no URL is retyped."""
    d = json.load(open(os.path.join(HERE, path), encoding="utf-8"))
    if "photos" in d:
        return d["photos"]
    out = {}
    for s in d["shots"]:
        if s["type"] == "archival" and not any(p["file_url"] == s["file_url"] for p in out.values()):
            out[f"p{len(out) + 1:02d}"] = {k: s[k] for k in ("title", "file_url", "page_url", "author", "licence")}
    return out


def house_format(doc):
    d = lambda v: json.dumps(v, ensure_ascii=False)
    lines = ["{"]
    keys = list(doc)
    for i, k in enumerate(keys):
        end = "," if i < len(keys) - 1 else ""
        v = doc[k]
        if isinstance(v, dict) and k in ("cast", "sets", "props", "photos"):
            lines.append(f" {d(k)}: {{")
            items = list(v.items())
            for j, (kk, vv) in enumerate(items):
                lines.append(f"  {d(kk)}: {d(vv)}" + ("," if j < len(items) - 1 else ""))
            lines.append(" }" + end)
        elif isinstance(v, list):
            lines.append(f" {d(k)}: [")
            for j, x in enumerate(v):
                lines.append(f"  {d(x)}" + ("," if j < len(v) - 1 else ""))
            lines.append(" ]" + end)
        else:
            lines.append(f" {d(k)}: {d(v)}{end}")
    lines.append("}")
    out = "\n".join(lines) + "\n"
    json.loads(out)
    return out


def main(day, nseg):
    sys.path.insert(0, HERE)
    spec = importlib.util.spec_from_file_location(day, os.path.join(HERE, "days", f"{day}.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    doc = {"spec_version": "v3", **m.META, "notes": m.NOTES, "cast": m.CAST, "sets": m.SETS, "props": m.PROPS,
           "photos": m.PHOTOS, "beats": m.BEATS}
    path = os.path.join(HERE, "out", f"{day}.build.json")
    open(path, "w", encoding="utf-8").write(house_format(doc))
    return subprocess.call([sys.executable, os.path.join(HERE, "validate.py"), path, str(nseg)])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], int(sys.argv[2])))
