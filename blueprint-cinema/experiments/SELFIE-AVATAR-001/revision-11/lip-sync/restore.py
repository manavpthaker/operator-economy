"""One bound R11 tail-only Sync v3 request. No automatic retries or fallbacks.

Commands: preflight, prepare, submit, status, result, download.
INPUT.json and its referenced inspection report are owner-workflow records; this
runner never edits either. Preparation makes an exclusive REQUEST.json. Submit
revalidates local and hosted bytes, then fsyncs an exclusive intent before POST.
An existing intent always blocks another submission, including uncertain ones.
"""

import datetime
import hashlib
import json
import math
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
REPO = BASE.parents[4]
EXPERIMENT = REPO / "blueprint-cinema/experiments/SELFIE-AVATAR-001"
MEDIA = EXPERIMENT / "media/revision-11"
MODEL = "fal-ai/sync-lipsync/v3"
QUEUE = "https://queue.fal.run/"
REQUEST_NAMESPACE = "/fal-ai/sync-lipsync/requests/"
SHA_PATTERN = re.compile(r"^[0-9a-f]{64}$")
NO_RETRY = "Do not resubmit. Preserve the intent and reconcile provider state."


def require(condition, message):
    if not condition:
        raise ValueError(message)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_bytes())


def fsync_directory(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def save(name, data, exclusive=True):
    """Exclusive receipts are never replaced; fsync both file and directory."""
    raw = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode()
    flags = os.O_WRONLY | os.O_CREAT | (os.O_EXCL if exclusive else os.O_TRUNC)
    fd = os.open(BASE / name, flags, 0o600)
    with os.fdopen(fd, "wb") as output:
        output.write(raw)
        output.flush()
        os.fsync(output.fileno())
    fsync_directory(BASE)


def failure_receipt(kind, operation, details):
    save(f"{kind}-{uuid.uuid4().hex}.json", {
        "at": now(), "operation": operation, **details,
        "instruction": NO_RETRY if operation == "submit" else
        "Read-only status/result may be checked again; never resubmit this request."
    })


def repo_path(value, allowed_root):
    require(isinstance(value, str), "Expected a repository-relative path")
    path = Path(value)
    require(not path.is_absolute(), "Record paths must be repository-relative")
    resolved = (REPO / path).resolve()
    require(resolved.is_relative_to(allowed_root.resolve()), "Path escapes its allowed record/media directory")
    require(resolved.is_file(), "Bound local file is unavailable")
    return resolved


def check_hash(path, expected, label):
    require(isinstance(expected, str) and SHA_PATTERN.fullmatch(expected), f"Invalid {label} hash")
    require(sha(path.read_bytes()) == expected, f"Bound {label} hash changed")


def media_url(url):
    require(isinstance(url, str), "Media URL is missing")
    parsed = urllib.parse.urlsplit(url)
    require(parsed.scheme == "https" and parsed.hostname and not parsed.username
            and not parsed.password and parsed.port in (None, 443)
            and not parsed.fragment, "Media URL must be HTTPS without credentials or fragments")
    host = parsed.hostname
    require(host == "fal.media" or host.endswith(".fal.media")
            or host.endswith(".cloudfront.net"), "Media host is outside the bound workflow")
    return url


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect())


def fetch(url):
    with OPENER.open(media_url(url), timeout=60) as response:
        require(response.status == 200, "Media download did not return HTTP 200")
        data = response.read(200 * 1024 * 1024 + 1)
    require(0 < len(data) <= 200 * 1024 * 1024, "Media response is empty or exceeds expected bounds")
    return data


def credential():
    for line in (REPO / ".env").read_text().splitlines():
        match = re.match(r"^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$", line)
        if match:
            value = match.group(1).strip().strip('\"').strip("'")
            require(value and "\n" not in value and "\r" not in value, "FAL_KEY is unavailable")
            return value
    raise ValueError("FAL_KEY is unavailable")


def validate_api_url(url, operation, request_id=None):
    parsed = urllib.parse.urlsplit(url)
    require(parsed.scheme == "https" and parsed.hostname == "queue.fal.run"
            and parsed.port is None and not parsed.username and not parsed.password
            and not parsed.query and not parsed.fragment,
            "Authenticated URL is outside the exact Fal queue origin")
    if operation == "submit":
        expected = "/" + MODEL
    else:
        require(isinstance(request_id, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,100}", request_id),
                "Invalid provider request id")
        require(operation in ("status", "result"), "Unsupported authenticated operation")
        expected = REQUEST_NAMESPACE + request_id + ("/status" if operation == "status" else "")
    require(parsed.path == expected, "Authenticated URL does not match the bound model request path")


def api(url, operation, payload=None, request_id=None):
    validate_api_url(url, operation, request_id)
    require((operation == "submit") == (payload is not None), "Unexpected API method or payload")
    key = credential()
    request = urllib.request.Request(url,
        data=None if payload is None else json.dumps(payload, separators=(",", ":")).encode(),
        headers={"Authorization": "Key " + key, "Content-Type": "application/json",
                 "X-Fal-No-Retry": "1", "x-app-fal-disable-fallback": "1"})
    try:
        with OPENER.open(request, timeout=60) as response:
            body = response.read(4 * 1024 * 1024 + 1)
        require(len(body) <= 4 * 1024 * 1024, "Unexpectedly large queue response")
        # Never persist or print any accidental credential echo from a provider.
        require(key.encode() not in body, "Provider response unexpectedly contained authentication material")
        result = json.loads(body)
        require(isinstance(result, dict), "Provider queue response is not an object")
        return result
    except urllib.error.HTTPError as error:
        failure_receipt("HTTP-ERROR", operation, {"http_status": error.code})
        raise RuntimeError("Fal HTTP failure. " + NO_RETRY) from None
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
        failure_receipt("TRANSPORT-UNCERTAIN", operation, {"exception_type": type(error).__name__})
        raise RuntimeError("Fal response unavailable or invalid. " + NO_RETRY) from None


def validate_input(hosted=False):
    input_path = BASE / "INPUT.json"
    record = read_json(input_path)
    require(record.get("model") == MODEL, "Only the authorized original Sync v3 model is allowed")
    require(record.get("sync_mode") == "silence", "Only the original silence mode is allowed")
    require(isinstance(record.get("scope"), str) and record["scope"].strip(), "Repair scope is missing")
    video = repo_path(record["video_local_path"], EXPERIMENT / "media")
    audio = repo_path(record["audio_local_path"], EXPERIMENT / "media")
    script = repo_path(record["script_path"], EXPERIMENT)
    report_path = repo_path(record["input_report_path"], BASE.parent)
    for path, field, label in ((video, "video_sha256", "tail picture"),
                              (audio, "audio_sha256", "tail voice"),
                              (script, "script_sha256", "owner script"),
                              (report_path, "input_report_sha256", "input inspection report")):
        check_hash(path, record[field], label)
    report = read_json(report_path)
    expected_fields = {"video_sha256": record["video_sha256"],
                       "audio_sha256": record["audio_sha256"],
                       "video_url": record["video_url"], "audio_url": record["audio_url"],
                       "width": 720, "height": 1280, "fps": 24, "frame_count": 420,
                       "start_frame": 902, "end_frame_exclusive": 1322,
                       "source_audio_start_sample": 1804000,
                       "audio_sample_rate_hz": 48000, "audio_channels": 1,
                       "audio_sample_width_bytes": 2, "audio_sample_count": 839731}
    for field, value in expected_fields.items():
        require(report.get(field) == value, f"Inspection report {field} mismatch")
    require(report.get("strict_decode_passed") is True, "Tail inspection did not pass strict decoding")
    duration = report.get("duration_seconds")
    require(isinstance(duration, (int, float)) and math.isfinite(duration)
            and abs(duration - 17.5) < 0.00001, "Tail picture must be exactly 420 frames / 17.5 seconds")
    audio_duration = report.get("audio_duration_seconds")
    require(isinstance(audio_duration, (int, float)) and math.isfinite(audio_duration)
            and abs(audio_duration - 839731 / 48000) < 0.0000001,
            "Tail voice duration differs from the measured source slice")
    with wave.open(str(audio), "rb") as stream:
        require((stream.getframerate(), stream.getnchannels(), stream.getsampwidth(), stream.getnframes(),
                 stream.getcomptype()) == (48000, 1, 2, 839731, "NONE"),
                "Tail WAV sample contract differs from the measured R10 slice")
    video_url = media_url(record["video_url"])
    audio_url = media_url(record["audio_url"])
    if hosted:
        require(sha(fetch(video_url)) == record["video_sha256"], "Hosted tail picture differs from bound local bytes")
        require(sha(fetch(audio_url)) == record["audio_sha256"], "Hosted tail voice differs from bound local bytes")
    request = {"model": MODEL,
               "input": {"video_url": video_url, "audio_url": audio_url, "sync_mode": "silence"},
               "input_record_sha256": sha(input_path.read_bytes()),
               "input_report_sha256": record["input_report_sha256"],
               "video_sha256": record["video_sha256"], "audio_sha256": record["audio_sha256"],
               "script_sha256": record["script_sha256"]}
    return record, request


def bound_job():
    intent = read_json(BASE / "SUBMISSION-INTENT.json")
    require(intent["request_sha256"] == sha((BASE / "REQUEST.json").read_bytes()), "Request changed after intent")
    request = read_json(BASE / "REQUEST.json")
    require(request["input_record_sha256"] == sha((BASE / "INPUT.json").read_bytes()), "Input changed after intent")
    require(request["model"] == MODEL and request["input"]["sync_mode"] == "silence", "Request route changed")
    job = read_json(BASE / "JOB.json")
    for field, operation in (("status_url", "status"), ("response_url", "result")):
        validate_api_url(job[field], operation, job["request_id"])
    return job


def main():
    require(len(sys.argv) == 2, "Use exactly one command: preflight, prepare, submit, status, result, download")
    mode = sys.argv[1]
    require(mode in ("preflight", "prepare", "submit", "status", "result", "download"), "Unknown operation")
    if mode in ("preflight", "prepare", "submit"):
        if mode != "preflight":
            require(not (BASE / "SUBMISSION-INTENT.json").exists() and not (BASE / "JOB.json").exists(),
                    "This revision already has a submission intent or job. " + NO_RETRY)
        record, expected = validate_input(hosted=mode != "preflight")
        if mode == "preflight":
            result = {"status": "local_inputs_validated_no_submission", **expected}
        elif mode == "prepare":
            save("REQUEST.json", expected)
            result = {"status": "hosted_and_local_inputs_bound_no_submission", **expected}
        else:
            request = read_json(BASE / "REQUEST.json")
            require(request == expected, "Prepared request differs from exact payload derived from current bound inputs")
            credential()  # Resolve missing credentials before creating a submission intent.
            save("SUBMISSION-INTENT.json", {
                "at": now(), "scope": record["scope"], "model": MODEL,
                "request_sha256": sha((BASE / "REQUEST.json").read_bytes()),
                "input_record_sha256": expected["input_record_sha256"],
                "input_report_sha256": expected["input_report_sha256"],
                "video_sha256": expected["video_sha256"], "audio_sha256": expected["audio_sha256"],
                "retry": False, "instruction": NO_RETRY})
            result = api(QUEUE + MODEL, "submit", request["input"])
            # Preserve the complete response before validating its read-only URLs.
            save("JOB.json", result)
            bound_job()
    elif mode in ("status", "result"):
        job = bound_job()
        result = api(job["status_url" if mode == "status" else "response_url"],
                     mode, request_id=job["request_id"])
        save(f"{mode.upper()}-{uuid.uuid4().hex}.json", result)
        save("STATUS.json" if mode == "status" else "RESULT.json", result, exclusive=False)
    else:
        job = bound_job()
        result_record = read_json(BASE / "RESULT.json")
        url = result_record["video"]["url"]
        data = fetch(url)
        path = MEDIA / "home-olive-gtm-r11-tail-sync.mp4"
        MEDIA.mkdir(parents=True, exist_ok=True)
        if path.exists():
            require(sha(path.read_bytes()) == sha(data), "Existing downloaded tail differs; preserve it and investigate")
        else:
            with path.open("xb") as output:
                output.write(data)
                output.flush()
                os.fsync(output.fileno())
            fsync_directory(MEDIA)
        result = {"url": url, "path": str(path.relative_to(REPO)), "bytes": len(data),
                  "sha256": sha(data), "request_id": job["request_id"],
                  "result_record_sha256": sha((BASE / "RESULT.json").read_bytes())}
        receipt = BASE / "DOWNLOAD.json"
        if receipt.exists():
            require(read_json(receipt) == result, "Download receipt changed; preserve the existing receipt")
        else:
            save("DOWNLOAD.json", result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, FileNotFoundError, FileExistsError, RuntimeError,
            urllib.error.URLError, OSError, wave.Error) as error:
        # Exceptions contain only our explicit checks or non-authenticated file/media errors.
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(1)
