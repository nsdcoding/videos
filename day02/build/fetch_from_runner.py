#!/usr/bin/env python3
"""Run on a GitHub runner: download every `photos` file_url into day02/archival/ (original files).

Stops and fails the job on a 404/403, a non-image response, or a photo missing credit fields
(BUILD_SPEC v3 section 9). 429s are waited out politely, then reported, never worked around.
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request

DAY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "HistoryChannelBuild/1.0 (https://github.com/nsdcoding/videos; nsdcoding@gmail.com)"
os.makedirs(os.path.join(DAY, "archival"), exist_ok=True)
failed = []
for pid, p in json.load(open(os.path.join(DAY, "build.json")))["photos"].items():
    if not all(p.get(k) for k in ("author", "licence", "page_url")):
        sys.exit(f"STOP {pid}: missing author/licence/page_url")
    name = urllib.parse.unquote(p["file_url"].rsplit("/", 1)[1])
    out = os.path.join(DAY, "archival", name)
    if os.path.exists(out):
        continue
    req = urllib.request.Request(p["file_url"], headers={"User-Agent": UA})
    data = None
    for wait in (20, 60, 120, None):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                ctype, data = r.headers.get("Content-Type", ""), r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and wait:
                print(f"{pid} 429, waiting {wait}s", flush=True)
                time.sleep(wait)
                continue
            failed.append(f"{pid} {e.code} {p['file_url']}")
            break
    if data is None:
        continue
    if not ctype.startswith("image/"):
        failed.append(f"{pid} non-image {ctype} {p['file_url']}")
        continue
    open(out, "wb").write(data)
    print(f"{pid} {ctype} {len(data) // 1024}KB {name}", flush=True)
    time.sleep(2)
if failed:
    print("FAILED:\n" + "\n".join(failed))
    sys.exit(1)
