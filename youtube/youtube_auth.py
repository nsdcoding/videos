#!/usr/bin/env python3
"""One-time YouTube sign-in: turns a Desktop OAuth client into a refresh token.

Run this on YOUR OWN computer (it opens a browser), not in the cloud session:

  pip install google-auth-oauthlib
  python3 youtube_auth.py client_secret.json

Sign in with the Google account that owns the channel (pick the channel if it
asks for a brand account). It prints the three values to save as secrets:
YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN. Don't commit them anywhere.
"""
import json, sys

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",  # videos.insert
    "https://www.googleapis.com/auth/youtube",         # thumbnails, playlists, channel check
]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        sys.exit("Install the helper first: pip install google-auth-oauthlib")

    flow = InstalledAppFlow.from_client_secrets_file(sys.argv[1], SCOPES)
    # offline + consent makes Google return a refresh token every time.
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    if not creds.refresh_token:
        sys.exit("No refresh token came back. Remove the app's access at "
                 "https://myaccount.google.com/permissions and run this again.")

    client = json.load(open(sys.argv[1]))
    client = client.get("installed") or client.get("web")
    print("\nSave these three as secrets in the cloud environment:\n")
    print(f"YT_CLIENT_ID={client['client_id']}")
    print(f"YT_CLIENT_SECRET={client['client_secret']}")
    print(f"YT_REFRESH_TOKEN={creds.refresh_token}")


if __name__ == "__main__":
    main()
