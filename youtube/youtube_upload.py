#!/usr/bin/env python3
"""Upload a finished video to YouTube with its thumbnail, details and playlist.

Needs YT_CLIENT_ID, YT_CLIENT_SECRET and YT_REFRESH_TOKEN in the environment
(made once with youtube_auth.py; see youtube/SETUP.md).

  python3 youtube_upload.py check                     # confirm sign-in, show channel
  python3 youtube_upload.py upload video.json         # upload as the file says
  python3 youtube_upload.py upload video.json --dry-run
  python3 youtube_upload.py upload video.json --privacy unlisted
  python3 youtube_upload.py upload video.json --publish-at 2026-10-20T18:00:00+05:30

video.json (paths are relative to the json file):
  {
    "video": "final.mp4",
    "thumbnail": "thumb.png",
    "title": "...",
    "description": "...",
    "tags": ["...", "..."],
    "category": 27,              # 27 Education, 22 People & Blogs, 28 Science & Tech
    "language": "hi",            # title/description and audio language
    "privacy": "private",        # private | unlisted | public
    "publish_at": null,          # ISO time; forces private until then
    "playlist": "PL...",         # optional playlist id
    "made_for_kids": false,
    "ai_generated": true         # YouTube's altered/synthetic content label
  }

Unverified API projects can only upload private videos; see SETUP.md.
"""
import argparse, json, os, subprocess, sys, time
from datetime import datetime, timezone

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]
CHUNK = 8 * 1024 * 1024
THUMB_MAX = 2 * 1024 * 1024


def ensure_deps():
    try:
        import googleapiclient, google.oauth2  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
                               "google-api-python-client", "google-auth"])


def youtube():
    missing = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")
               if not os.environ.get(k)]
    if missing:
        sys.exit(f"Missing secrets: {', '.join(missing)} (see youtube/SETUP.md)")
    ensure_deps()
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
                        client_id=os.environ["YT_CLIENT_ID"],
                        client_secret=os.environ["YT_CLIENT_SECRET"],
                        token_uri="https://oauth2.googleapis.com/token", scopes=SCOPES)
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def load_meta(path, args):
    meta = json.load(open(path))
    base = os.path.dirname(os.path.abspath(path))
    for key in ("video", "thumbnail"):
        if meta.get(key):
            meta[key] = os.path.join(base, meta[key])
    if args.privacy:
        meta["privacy"] = args.privacy
    if args.publish_at:
        meta["publish_at"] = args.publish_at

    errors = []
    if not meta.get("video") or not os.path.isfile(meta["video"]):
        errors.append(f"video file not found: {meta.get('video')}")
    if meta.get("thumbnail") and not os.path.isfile(meta["thumbnail"]):
        errors.append(f"thumbnail not found: {meta['thumbnail']}")
    title, desc = meta.get("title", ""), meta.get("description", "")
    if not title.strip() or len(title) > 100:
        errors.append(f"title must be 1-100 characters (is {len(title)})")
    if len(desc.encode()) > 5000:
        errors.append(f"description is over 5000 bytes ({len(desc.encode())})")
    if any(c in title + desc for c in "<>"):
        errors.append("title and description can't contain < or >")
    tags = meta.get("tags", [])
    # YouTube counts quotes around tags that contain spaces toward the 500 limit.
    tag_len = sum(len(t) + (2 if " " in t else 0) for t in tags) + max(len(tags) - 1, 0)
    if tag_len > 500:
        errors.append(f"tags total {tag_len} characters, limit is 500")
    meta.setdefault("privacy", "private")
    if meta["privacy"] not in ("private", "unlisted", "public"):
        errors.append(f"privacy must be private, unlisted or public: {meta['privacy']}")
    if meta.get("publish_at"):
        try:
            when = datetime.fromisoformat(meta["publish_at"].replace("Z", "+00:00"))
            if when.tzinfo is None:
                errors.append("publish_at needs a timezone, e.g. 2026-10-20T18:00:00+05:30")
            elif when <= datetime.now(timezone.utc):
                errors.append("publish_at is in the past")
            else:
                meta["publish_at"] = when.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                meta["privacy"] = "private"  # scheduled videos must start private
        except ValueError:
            errors.append(f"publish_at isn't an ISO date-time: {meta['publish_at']}")
    if errors:
        sys.exit("video.json problems:\n  " + "\n  ".join(errors))
    return meta


def body_for(meta):
    lang = meta.get("language", "hi")
    status = {"privacyStatus": meta["privacy"],
              "selfDeclaredMadeForKids": bool(meta.get("made_for_kids", False)),
              "containsSyntheticMedia": bool(meta.get("ai_generated", True))}
    if meta.get("publish_at"):
        status["publishAt"] = meta["publish_at"]
    return {"snippet": {"title": meta["title"], "description": meta.get("description", ""),
                        "tags": meta.get("tags", []),
                        "categoryId": str(meta.get("category", 27)),
                        "defaultLanguage": lang, "defaultAudioLanguage": lang},
            "status": status}


def with_retries(fn, what):
    from googleapiclient.errors import HttpError
    for attempt in range(6):
        try:
            return fn()
        except HttpError as e:
            if e.resp.status not in (500, 502, 503, 504) or attempt == 5:
                sys.exit(f"{what} failed: {e.resp.status} {e.content.decode()[:600]}")
        except (ConnectionError, TimeoutError, OSError) as e:
            if attempt == 5:
                sys.exit(f"{what} failed: {e}")
        wait = 2 ** attempt * 2
        print(f"  {what}: retrying in {wait}s", file=sys.stderr)
        time.sleep(wait)


def small_thumbnail(path):
    """YouTube rejects thumbnails over 2 MB; re-encode a big PNG as JPEG with ffmpeg."""
    if os.path.getsize(path) <= THUMB_MAX:
        return path
    out = os.path.splitext(path)[0] + ".yt.jpg"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path,
                    "-vf", "scale=1280:720:force_original_aspect_ratio=decrease",
                    "-q:v", "3", out], check=True)
    if os.path.getsize(out) > THUMB_MAX:
        sys.exit(f"thumbnail is still over 2 MB after converting: {out}")
    return out


def upload(args):
    meta = load_meta(args.meta, args)
    body = body_for(meta)
    if args.dry_run:
        print(json.dumps(body, ensure_ascii=False, indent=2))
        print(f"video: {meta['video']} ({os.path.getsize(meta['video']) / 1e6:.1f} MB)")
        if meta.get("thumbnail"):
            print(f"thumbnail: {meta['thumbnail']}")
        if meta.get("playlist"):
            print(f"playlist: {meta['playlist']}")
        return

    yt = youtube()
    from googleapiclient.http import MediaFileUpload
    media = MediaFileUpload(meta["video"], chunksize=CHUNK, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = with_retries(req.next_chunk, "upload")
        if status:
            print(f"  uploaded {status.progress() * 100:.0f}%", file=sys.stderr)
    vid = resp["id"]
    print(f"Uploaded: https://youtu.be/{vid} ({resp['status']['privacyStatus']})")
    if resp["status"]["privacyStatus"] != meta["privacy"]:
        print("  Note: YouTube kept it private. Unverified API projects can't publish; "
              "switch it in YouTube Studio or get the API audit (see SETUP.md).")

    if meta.get("thumbnail"):
        thumb = small_thumbnail(meta["thumbnail"])
        with_retries(lambda: yt.thumbnails().set(
            videoId=vid, media_body=MediaFileUpload(thumb)).execute(), "thumbnail")
        print("  Thumbnail set")
    if meta.get("playlist"):
        with_retries(lambda: yt.playlistItems().insert(part="snippet", body={"snippet": {
            "playlistId": meta["playlist"],
            "resourceId": {"kind": "youtube#video", "videoId": vid}}}).execute(), "playlist")
        print("  Added to playlist")


def check(_args):
    yt = youtube()
    items = with_retries(lambda: yt.channels().list(part="snippet", mine=True).execute(),
                         "channel check").get("items", [])
    if not items:
        sys.exit("Signed in, but this account has no YouTube channel")
    for ch in items:
        print(f"OK: signed in to channel '{ch['snippet']['title']}' ({ch['id']})")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check").set_defaults(fn=check)
    u = sub.add_parser("upload")
    u.add_argument("meta")
    u.add_argument("--privacy", choices=["private", "unlisted", "public"])
    u.add_argument("--publish-at")
    u.add_argument("--dry-run", action="store_true")
    u.set_defaults(fn=upload)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
