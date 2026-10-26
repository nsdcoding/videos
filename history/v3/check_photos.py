#!/usr/bin/env python3
"""Check a photo library against the Commons API: each page_url's file must exist and its
original URL must equal file_url. One batched request per 40 files.

  python3 check_photos.py drafts/day04.photos.json
"""
import json, sys, urllib.parse, urllib.request

UA = "HistoryChannelBuild/1.0 (https://github.com/nsdcoding/videos)"
API = "https://commons.wikimedia.org/w/api.php"

d = json.load(open(sys.argv[1], encoding="utf-8"))
photos = d.get("photos", d)
titles = {pid: urllib.parse.unquote(p["page_url"].split("/wiki/", 1)[1]).replace("_", " ") for pid, p in photos.items()}
bad = 0
items = list(titles.items())
for i in range(0, len(items), 40):
    chunk = items[i:i + 40]
    q = urllib.parse.urlencode({"action": "query", "format": "json", "prop": "imageinfo", "iiprop": "url|size",
                                "titles": "|".join(t for _, t in chunk)})
    r = json.load(urllib.request.urlopen(urllib.request.Request(f"{API}?{q}", headers={"User-Agent": UA}), timeout=60))
    norm = {n["from"]: n["to"] for n in r["query"].get("normalized", [])}
    pages = {p["title"]: p for p in r["query"]["pages"].values()}
    for pid, t in chunk:
        p = pages.get(norm.get(t, t))
        if not p or "imageinfo" not in p:
            print(f"{pid} MISSING on Commons: {t}"); bad += 1; continue
        ii = p["imageinfo"][0]
        if urllib.parse.unquote(ii["url"]) != urllib.parse.unquote(photos[pid]["file_url"]):
            print(f"{pid} URL MISMATCH\n  have {photos[pid]['file_url']}\n  api  {ii['url']}"); bad += 1
        else:
            print(f"{pid} ok {ii['width']}x{ii['height']}")
sys.exit(1 if bad else 0)
