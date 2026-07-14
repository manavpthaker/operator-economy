"""
Set the custom thumbnail on an already-uploaded YouTube video via the
Data API v3. Reuses the OAuth token from .secrets/token.json (the same
one upload_youtube.py refreshes).

Usage:
    python scripts/originate/set_yt_thumbnail.py <youtube_id> <path/to/thumbnail.png>
"""
from __future__ import annotations

import json
import mimetypes
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).parent.parent.parent
TOKEN_PATH = ROOT / ".secrets" / "token.json"


def access_token() -> str:
    t = json.loads(TOKEN_PATH.read_text())
    r = requests.post(t["token_uri"], data={
        "client_id": t["client_id"],
        "client_secret": t["client_secret"],
        "refresh_token": t["refresh_token"],
        "grant_type": "refresh_token",
    }, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("usage: set_yt_thumbnail.py <video_id> <thumbnail_path>")
    vid, path_str = sys.argv[1], sys.argv[2]
    img = Path(path_str)
    if not img.exists():
        sys.exit(f"no such file: {img}")
    mime = mimetypes.guess_type(img.name)[0] or "image/png"

    tok = access_token()
    with img.open("rb") as f:
        r = requests.post(
            f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
            headers={"Authorization": f"Bearer {tok}", "Content-Type": mime},
            data=f, timeout=120)
    if r.status_code != 200:
        print(f"THUMBNAIL FAILED ({r.status_code}): {r.text[:500]}", file=sys.stderr)
        sys.exit(1)
    print(f"THUMBNAIL SET: {vid} ← {img.name}")


if __name__ == "__main__":
    main()
