"""Prepare or run one original Sync v3 pass for the authorized seven-second test.

INPUT.json requires video_url, video_sha256, audio_url, audio_sha256.
Optional fields: scope, model, sync_mode, video_local_path (repository-relative).
Commands: preflight, submit, status, result, download. No command retries a POST.
All repair receipts use SYNC-* names to preserve the native generation records.
"""

import datetime
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
import wave
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[3]
MEDIA = BASE.parent / "media/test-01"
AUDIO = MEDIA / "test01-original-c.wav"
AUDIO_SHA = "2fda60f4b9f61fcb2f784ae311ce13f87525a484920e5a6d0079e0033b730609"
MODEL = "fal-ai/sync-lipsync/v3"
ORIGIN = "https://queue.fal.run"
NAMESPACE = "/fal-ai/sync-lipsync/requests/"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def read(name):
    return json.loads((BASE / name).read_bytes())


def durable(path, data, replace=False):
    flags = os.O_WRONLY | os.O_CREAT | (os.O_TRUNC if replace else os.O_EXCL)
    with os.fdopen(os.open(path, flags, 0o600), "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def save(name, value, replace=False):
    durable(BASE / name, (json.dumps(value, indent=2) + "\n").encode(), replace)


def fixed(name, data):
    path = BASE / name
    if path.exists():
        require(path.read_bytes() == data, "An existing bound repair record differs; preserve it and investigate")
    else:
        durable(path, data)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect())


def media_url(url):
    require(isinstance(url, str), "Media URL is missing")
    parsed = urllib.parse.urlsplit(url)
    host = parsed.hostname or ""
    require(parsed.scheme == "https" and not parsed.username and not parsed.password
            and parsed.port in (None, 443) and not parsed.fragment,
            "Media URL must be HTTPS without embedded credentials or fragments")
    require(host == "fal.media" or host.endswith(".fal.media") or host.endswith(".cloudfront.net"),
            "Media URL is outside the established media hosts")
    return url


def fetch(url):
    with OPENER.open(media_url(url), timeout=60) as response:
        require(response.status == 200, "Media response is not HTTP 200")
        data = response.read(100 * 1024 * 1024 + 1)
    require(0 < len(data) <= 100 * 1024 * 1024, "Media response is empty or unexpectedly large")
    return data


def credential():
    for line in (REPO / ".env").read_text().splitlines():
        match = re.match(r"^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$", line)
        if match:
            key = match.group(1).strip().strip('\"').strip("'")
            require(key and "\r" not in key and "\n" not in key, "Local FAL_KEY is unavailable")
            return key
    raise ValueError("Local FAL_KEY is unavailable")


def queue_url(url, operation, request_id=None):
    parsed = urllib.parse.urlsplit(url)
    require(parsed.scheme == "https" and parsed.hostname == "queue.fal.run"
            and parsed.port is None and not parsed.username and not parsed.password
            and not parsed.query and not parsed.fragment, "Authenticated URL is outside the exact queue origin")
    if operation == "submit":
        expected = "/" + MODEL
    else:
        require(operation in ("status", "result") and isinstance(request_id, str)
                and re.fullmatch(r"[A-Za-z0-9_-]{1,100}", request_id), "Invalid bound queue operation or request id")
        expected = NAMESPACE + request_id + ("/status" if operation == "status" else "")
    require(parsed.path == expected, "Authenticated URL differs from the bound model request path")


def api(url, operation, payload=None, request_id=None):
    queue_url(url, operation, request_id)
    require((operation == "submit") == (payload is not None), "Unexpected API request method")
    key = credential()
    request = urllib.request.Request(url,
        data=None if payload is None else json.dumps(payload, separators=(",", ":")).encode(),
        headers={"Authorization": "Key " + key, "Content-Type": "application/json",
                 "X-Fal-No-Retry": "1", "x-app-fal-disable-fallback": "1"})
    try:
        with OPENER.open(request, timeout=60) as response:
            data = response.read(1024 * 1024 + 1)
        require(len(data) <= 1024 * 1024, "Queue response exceeded expected bounds")
        require(key.encode() not in data, "Queue response unexpectedly contained authentication material")
        result = json.loads(data)
        require(isinstance(result, dict), "Queue response is not an object")
        return result
    except (urllib.error.URLError, OSError, ValueError) as error:
        save("SYNC-ERROR-" + uuid.uuid4().hex + ".json", {
            "at": now(), "operation": operation, "exception_type": type(error).__name__,
            "http_status": getattr(error, "code", None),
            "instruction": "Never repeat this submission. Preserve intent and reconcile provider state; read-only status may be checked again."})
        raise RuntimeError("Fal response failed or is uncertain. Do not resubmit; inspect the preserved SYNC records.") from None


def validate_input():
    raw = (BASE / "INPUT.json").read_bytes()
    value = json.loads(raw)
    allowed = {"video_url", "video_sha256", "audio_url", "audio_sha256", "scope",
               "model", "sync_mode", "video_local_path"}
    require(isinstance(value, dict) and set(value) <= allowed, "INPUT.json has unsupported fields")
    require(value.get("model", MODEL) == MODEL and value.get("sync_mode", "silence") == "silence",
            "Only original Sync v3 with silence mode is supported")
    require(value["audio_sha256"] == AUDIO_SHA, "Audio differs from the exact authorized test WAV")
    require(re.fullmatch(r"[0-9a-f]{64}", value["video_sha256"]), "Native video hash is invalid")
    require(sha(AUDIO.read_bytes()) == AUDIO_SHA, "Local authoritative test WAV changed")
    with wave.open(str(AUDIO), "rb") as stream:
        require((stream.getframerate(), stream.getnchannels(), stream.getsampwidth(),
                 stream.getnframes(), stream.getcomptype()) == (48000, 1, 2, 336000, "NONE"),
                "Authoritative WAV must remain seven seconds of 48 kHz mono PCM16")
    if "video_local_path" in value:
        relative = Path(value["video_local_path"])
        local = (REPO / relative).resolve()
        require(not relative.is_absolute() and local.is_relative_to(MEDIA.resolve()),
                "Optional native video path must be repository-relative inside this test's media directory")
        require(sha(local.read_bytes()) == value["video_sha256"], "Local native video differs from its bound hash")
    require(sha(fetch(value["video_url"])) == value["video_sha256"], "Hosted native video differs from its bound hash")
    require(sha(fetch(value["audio_url"])) == AUDIO_SHA, "Hosted authoritative WAV differs from the local test WAV")
    request = {"model": MODEL, "input": {"video_url": value["video_url"],
               "audio_url": value["audio_url"], "sync_mode": "silence"},
               "input_record_sha256": sha(raw), "video_sha256": value["video_sha256"],
               "audio_sha256": AUDIO_SHA}
    require((BASE / "INPUT.json").read_bytes() == raw, "INPUT.json changed during validation")
    return raw, value, request


def job():
    intent = read("SYNC-SUBMISSION-INTENT.json")
    require(intent["request_sha256"] == sha((BASE / "SYNC-REQUEST.json").read_bytes()), "Bound request changed after submission")
    request = read("SYNC-REQUEST.json")
    raw = (BASE / "SYNC-BOUND-INPUT.json").read_bytes()
    require(request["input_record_sha256"] == sha(raw) and (BASE / "INPUT.json").read_bytes() == raw,
            "Bound input changed after submission")
    result = read("SYNC-JOB.json")
    queue_url(result["status_url"], "status", result["request_id"])
    queue_url(result["response_url"], "result", result["request_id"])
    return result


def main():
    require(len(sys.argv) == 2, "Use one command: preflight, submit, status, result, download")
    mode = sys.argv[1]
    require(mode in ("preflight", "submit", "status", "result", "download"), "Unknown command")
    if mode in ("preflight", "submit"):
        if mode == "submit":
            require(not (BASE / "SYNC-SUBMISSION-INTENT.json").exists()
                    and not (BASE / "SYNC-JOB.json").exists(), "A submission intent or job already exists. Do not resubmit.")
        raw, value, request = validate_input()
        if mode == "preflight":
            result = {"status": "validated_no_submission", **request}
        else:
            credential()
            fixed("SYNC-BOUND-INPUT.json", raw)
            request_bytes = (json.dumps(request, indent=2) + "\n").encode()
            fixed("SYNC-REQUEST.json", request_bytes)
            save("SYNC-SUBMISSION-INTENT.json", {"at": now(), "model": MODEL,
                 "scope": value.get("scope", "Authorized SELFIE-AVATAR-002 seven-second test"),
                 "request_sha256": sha(request_bytes), "input_record_sha256": sha(raw),
                 "retry": False, "instruction": "One submission only. Any uncertain outcome must be reconciled without another POST."})
            result = api(ORIGIN + "/" + MODEL, "submit", request["input"])
            save("SYNC-JOB.json", result)
            job()
    elif mode in ("status", "result"):
        bound = job()
        result = api(bound["status_url" if mode == "status" else "response_url"], mode,
                     request_id=bound["request_id"])
        save("SYNC-" + mode.upper() + "-" + uuid.uuid4().hex + ".json", result)
        if mode == "status":
            save("SYNC-STATUS.json", result, replace=True)
        else:
            fixed("SYNC-RESULT.json", (json.dumps(result, indent=2) + "\n").encode())
    else:
        bound = job()
        response = read("SYNC-RESULT.json")
        url = response["video"]["url"]
        data = fetch(url)
        path = MEDIA / "test01-original-sync.mp4"
        if path.exists():
            require(sha(path.read_bytes()) == sha(data), "Existing downloaded repair differs; preserve it and investigate")
        else:
            durable(path, data)
        result = {"url": url, "path": str(path.relative_to(REPO)), "bytes": len(data),
                  "sha256": sha(data), "request_id": bound["request_id"],
                  "result_record_sha256": sha((BASE / "SYNC-RESULT.json").read_bytes())}
        fixed("SYNC-DOWNLOAD.json", (json.dumps(result, indent=2) + "\n").encode())
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, OSError, RuntimeError, wave.Error) as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(1)
