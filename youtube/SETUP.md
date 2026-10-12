# YouTube upload: one-time setup

After these steps, `python3 youtube/youtube_upload.py upload video.json` uploads a
video with its thumbnail, Hindi details, tags, category and playlist in one run.

## 1. Turn on the API (Google Cloud console, project `claudevideo-503905`)

- [ ] **APIs & Services → Library** → search "YouTube Data API v3" → **Enable**.
- [ ] **APIs & Services → OAuth consent screen** (Google Auth Platform):
  - User type **External**, app name anything (e.g. "Video uploader"), your email as support and developer contact.
  - Add your channel's Google account under **Test users**.
  - Then set **Publishing status → In production**. Leave it unverified; that's fine for
    your own channel. In "Testing" mode the refresh token expires after 7 days and uploads
    stop working.
- [ ] **APIs & Services → Credentials → Create credentials → OAuth client ID**,
  type **Desktop app**. Download the JSON (`client_secret_….json`).

## 2. Sign in once (on your own computer)

```bash
pip install google-auth-oauthlib
python3 youtube_auth.py client_secret_XXXX.json
```

- A browser opens. Sign in with the account that owns the channel, and pick the
  channel if it's a brand account.
- Google warns "Google hasn't verified this app". Click **Advanced → Go to … (unsafe)**;
  it's your own app.
- The script prints `YT_CLIENT_ID`, `YT_CLIENT_SECRET` and `YT_REFRESH_TOKEN`.
  Don't commit the JSON file or these values.

## 3. Save the secrets in the cloud environment

In the Claude Code cloud environment settings (where `GCP_SA_KEY_B64` lives), add
`YT_CLIENT_ID`, `YT_CLIENT_SECRET` and `YT_REFRESH_TOKEN`, then start a new session
and run:

```bash
python3 youtube/youtube_upload.py check
```

It should print your channel's name.

## 4. Channel settings

- [ ] Phone-verify the channel (YouTube Studio → Settings → Channel → Feature eligibility),
  or custom thumbnails will fail.

## Limits to know

- **Private only until audited.** Videos uploaded through an unverified API project are
  locked to private, even if `video.json` says public or has a `publish_at` time.
  Switch each one to public in YouTube Studio, or apply for the YouTube API audit
  (https://support.google.com/youtube/contact/yt_api_form) to publish or schedule from the script.
- **Quota.** 10,000 units a day by default. One upload is about 1,600 units, plus 50
  for the thumbnail and 50 for the playlist, so about 5–6 videos a day.
- **AI label.** `ai_generated: true` sets YouTube's altered/synthetic content flag.
  Keep it on for videos with Nano Banana visuals or Gemini TTS voice.

## Using it

Copy `video.example.json` next to your video, fill it in, then:

```bash
python3 youtube/youtube_upload.py upload my_video.json --dry-run   # check details, no upload
python3 youtube/youtube_upload.py upload my_video.json
```

Paths in the JSON are relative to the JSON file. `--privacy` and `--publish-at` on
the command line override the file.
