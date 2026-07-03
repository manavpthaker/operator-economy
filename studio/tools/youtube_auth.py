"""
One-time YouTube OAuth: runs the browser consent flow and writes
.secrets/token.json (access + refresh token) for the uploader/analytics.

Run LOCALLY (needs a browser):
    pip install google-auth-oauthlib
    python studio/tools/youtube_auth.py
Sign in as brownmanbeard@gmail.com (the authorized test user).
The "Google hasn't verified this app" screen is expected in testing mode:
Advanced -> Continue.
"""

import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

ROOT = Path(__file__).parent.parent  # studio/
SECRETS = ROOT / ".secrets"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]

flow = InstalledAppFlow.from_client_secrets_file(str(SECRETS / "client_secret.json"), SCOPES)
creds = flow.run_local_server(port=0, prompt="consent")

token = {
    "refresh_token": creds.refresh_token,
    "client_id": creds.client_id,
    "client_secret": creds.client_secret,
    "token_uri": "https://oauth2.googleapis.com/token",
    "scopes": SCOPES,
}
out = SECRETS / "token.json"
out.write_text(json.dumps(token, indent=2))
print(f"OK — token written to {out}")
print("refresh_token present:", bool(creds.refresh_token))
