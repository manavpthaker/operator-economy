#!/usr/bin/env python3
"""One-shot Fal Sync v3 runner for EP007 Short 01 presenter segment B.

The generated Seedance video URL is supplied on the command line. The approved,
lossless Original C segment audio URL is pinned here. Submission is fail-closed:
the intent is persisted before the POST, and any existing intent or job blocks a
second submission.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parents[3]
MODEL = "fal-ai/sync-lipsync/v3"
SUBMIT_URL = f"https://queue.fal.run/{MODEL}"
PINNED_AUDIO_URL = (
    "https://d2ol7oe51mr4n9.cloudfront.net/"
    "user_3J3m5xtqP8Xv0MOsPutf0uV3maX/"
    "00cfdfa1-d6b6-4e19-8a2d-90fdfed2e4d6.mp3"
)
SEGMENT = "segment-b"

REQUEST_PATH = BASE / "SYNC-REQUEST.json"
INTENT_PATH = BASE / "SYNC-SUBMISSION-INTENT.json"
JOB_PATH = BASE / "SYNC-JOB.json"
STATUS_PATH = BASE / "SYNC-STATUS.json"
RESULT_PATH = BASE / "SYNC-RESULT.json"
ERROR_PATH = BASE / "SYNC-ERROR.json"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Make redirects fail visibly instead of following an unapproved host."""

    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def validate_https_media_url(url: str, label: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
    ):
        raise ValueError(f"{label} must be a credential-free HTTPS URL")
    return url


def validate_api_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "queue.fal.run"
        or parsed.port not in (None, 443)
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
    ):
        raise ValueError("Unapproved Fal API URL; only https://queue.fal.run is allowed")
    return url


def credential() -> str:
    env_path = REPO_ROOT / ".env"
    for line in env_path.read_text().splitlines():
        match = re.match(r"^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$", line)
        if match:
            key = match.group(1).strip().strip('"').strip("'")
            if key:
                return key
    raise ValueError("FAL_KEY unavailable")


def redact(value: str, secret: str) -> str:
    return value.replace(secret, "[REDACTED]") if secret else value


def api_call(
    url: str, body: dict[str, Any] | None = None, *, key: str | None = None
) -> Any:
    validate_api_url(url)
    key = key or credential()
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        headers={
            "Authorization": "Key " + key,
            "Content-Type": "application/json",
        },
        method="POST" if body is not None else "GET",
    )
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=45) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = redact(error.read(8000).decode(errors="replace"), key)
        write_json(
            ERROR_PATH,
            {
                "at": utc_now(),
                "http_status": error.code,
                "detail": detail,
                "submission_state": (
                    "uncertain after intent; inspect evidence and do not retry automatically"
                ),
            },
        )
        raise SystemExit("Fal request failed; inspect SYNC-ERROR.json; no automatic retry")
    except Exception as error:
        write_json(
            ERROR_PATH,
            {
                "at": utc_now(),
                "error_type": type(error).__name__,
                "detail": redact(str(error), key),
                "submission_state": (
                    "uncertain after intent; inspect evidence and do not retry automatically"
                ),
            },
        )
        raise SystemExit("Fal request uncertain; inspect SYNC-ERROR.json; no automatic retry")


def request_spec(video_url: str) -> dict[str, Any]:
    validate_https_media_url(video_url, "video_url")
    validate_https_media_url(PINNED_AUDIO_URL, "audio_url")
    return {
        "segment": SEGMENT,
        "model": MODEL,
        "endpoint": SUBMIT_URL,
        "input": {
            "video_url": video_url,
            "audio_url": PINNED_AUDIO_URL,
            "sync_mode": "silence",
        },
    }


def require_no_submission_record() -> None:
    existing = [path.name for path in (INTENT_PATH, JOB_PATH) if path.exists()]
    if existing:
        raise SystemExit(
            "Existing submission evidence blocks a retry: " + ", ".join(existing)
        )


def completed_status(status: Any) -> bool:
    return isinstance(status, dict) and status.get("status") == "COMPLETED"


def preflight(video_url: str) -> Any:
    require_no_submission_record()
    return {
        "network_called": False,
        "would_write_before_post": [REQUEST_PATH.name, INTENT_PATH.name],
        "request": request_spec(video_url),
    }


def submit(video_url: str) -> Any:
    require_no_submission_record()
    spec = request_spec(video_url)
    key = credential()
    write_json(REQUEST_PATH, spec)
    write_json(
        INTENT_PATH,
        {
            "at": utc_now(),
            "segment": SEGMENT,
            "scope": "One authorized Fal Sync v3 audio-restoration submission",
            "request_file": REQUEST_PATH.name,
            "model": MODEL,
            "retry_policy": "no retry after this intent without fresh inspection and authority",
        },
    )
    result = api_call(SUBMIT_URL, spec["input"], key=key)
    write_json(JOB_PATH, result)
    return result


def status() -> Any:
    if not JOB_PATH.exists():
        raise SystemExit("SYNC-JOB.json is missing; no job can be polled")
    job = read_json(JOB_PATH)
    status_url = job.get("status_url")
    if not isinstance(status_url, str):
        raise SystemExit("SYNC-JOB.json has no status_url")
    result = api_call(status_url)
    write_json(STATUS_PATH, result)
    return result


def result() -> Any:
    if not JOB_PATH.exists() or not STATUS_PATH.exists():
        raise SystemExit("SYNC-JOB.json and SYNC-STATUS.json are required")
    latest_status = read_json(STATUS_PATH)
    if not completed_status(latest_status):
        state = latest_status.get("status") if isinstance(latest_status, dict) else None
        raise SystemExit(f"Result fetch blocked: latest recorded status is {state!r}, not COMPLETED")
    job = read_json(JOB_PATH)
    response_url = job.get("response_url")
    if not isinstance(response_url, str):
        raise SystemExit("SYNC-JOB.json has no response_url")
    payload = api_call(response_url)
    write_json(RESULT_PATH, payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("preflight", "submit"):
        child = subparsers.add_parser(command)
        child.add_argument("--video-url", required=True)
    subparsers.add_parser("status")
    subparsers.add_parser("result")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "preflight":
            payload = preflight(args.video_url)
        elif args.command == "submit":
            payload = submit(args.video_url)
        elif args.command == "status":
            payload = status()
        else:
            payload = result()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(str(error)) from None
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
