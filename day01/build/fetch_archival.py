#!/usr/bin/env python3
"""Collect every archival shot's file (BUILD_SPEC section 3) into images/.

Source order: day01/archival/<original filename> (added by hand, because Wikimedia rate-limits the
build sandbox), else a direct download of file_url. Stops on any failure (section 7): a missing
author/licence/page_url, a missing file, a 404/403, or anything that is not an image.
"""
import json, os, shutil, sys, time, urllib.error, urllib.parse, urllib.request

DAY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "HistoryChannelBuild/1.0 (https://github.com/nsdcoding/videos)"
SIGS = {b"\xff\xd8\xff": "image/jpeg", b"\x89PNG": "image/png"}


def sniff(data):
    for sig, mime in SIGS.items():
        if data.startswith(sig):
            return mime
    return None


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for wait in (30, 60, 120, None):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.headers.get("Content-Type", ""), r.read()
        except urllib.error.HTTPError as e:
            # 429 is rate limiting, not a broken URL: wait and retry. Anything else stops (section 7).
            if e.code != 429 or wait is None:
                raise
            print(f"  429, waiting {wait}s", flush=True)
            time.sleep(wait)


def main():
    shots = json.load(open(os.path.join(DAY, "build.json")))["shots"]
    os.makedirs(os.path.join(DAY, "images"), exist_ok=True)
    local_only = "--local" in sys.argv
    missing = []
    for s in shots:
        if s["type"] != "archival":
            continue
        sid = s["segments"][0]
        lack = [k for k in ("author", "licence", "page_url") if not s.get(k)]
        if lack:
            sys.exit(f"STOP {sid}: archival shot missing {lack}")
        name = urllib.parse.unquote(s["file_url"].rsplit("/", 1)[1])
        ext = os.path.splitext(name)[1].lower()
        out = os.path.join(DAY, "images", f"{sid}_archival{ext}")
        if os.path.exists(out):
            continue
        src = os.path.join(DAY, "archival", name)
        if os.path.exists(src):
            data, how = open(src, "rb").read(), "repo"
        elif local_only:
            missing.append(f"{sid}: {name}")
            continue
        else:
            try:
                ctype, data = download(s["file_url"])
            except Exception as e:
                sys.exit(f"STOP {sid}: {s['file_url']} -> {e}")
            if not ctype.startswith("image/"):
                sys.exit(f"STOP {sid}: non-image content type {ctype}")
            how = "wikimedia"
            time.sleep(5)
        if not sniff(data):
            sys.exit(f"STOP {sid}: {name} is not a JPEG or PNG (first bytes {data[:8]!r})")
        open(out, "wb").write(data)
        print(f"{sid} {sniff(data)} {len(data) // 1024}KB from {how}", flush=True)
    if missing:
        sys.exit("STOP: not yet in day01/archival/:\n  " + "\n  ".join(missing))


if __name__ == "__main__":
    main()
