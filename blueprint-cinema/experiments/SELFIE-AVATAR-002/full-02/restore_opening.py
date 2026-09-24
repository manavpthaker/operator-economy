"""One authorized Original C Sync v3 restoration for the full-02 continuous opening.

Usage: python3 restore_opening.py {preflight,submit,status,result,download}
INPUT.json lives in full-02/opening/ and requires video_url, video_sha256,
video_local_path, audio_url, audio_sha256, audio_local_path, duration. Duration
means the source audio duration, not the rounded native generation duration.
Paths may be absolute or repository-relative, but must resolve to the exact
section media paths. Optional fields: scope, model, sync_mode.

Preflight is local and read-only: no network, credentials, or receipt writes.
Submit verifies hosted bytes, binds the request, writes an exclusive durable
intent, then makes one POST without retries. Never delete an intent to retry.
Status/result are separate GETs. Downloads and all receipt writes are scoped.
"""

import argparse
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


FULL = Path(__file__).resolve().parent
REPO = FULL.parents[3]
MEDIA = FULL / "media"
MODEL = "fal-ai/sync-lipsync/v3"
ORIGIN = "https://queue.fal.run"
NAMESPACE = "/fal-ai/sync-lipsync/requests/"
MASTER_SHA = "0ad39c68a67b6c0f11edcbbe952380fc616716a59788dc049e2613313e4091e0"
RANGES = {"opening": (0, 1048000)}
AUDIO_SHA = "90bd248de78abdd33fc302e384bed4cc562ae652248e9379e201ca5bafe72ede"
AUDIO_URL = "https://d2ol7oe51mr4n9.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/28e85a36-6514-4ab5-9f56-dc1f756da439.mp3"
NATIVE_JOB = "4b7e8bdd-218d-4cec-b839-6ee066796bfd"
BASE = None
SECTION = "opening"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2) + "\n").encode()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def read(name):
    return json.loads((BASE / name).read_bytes())


def durable(path, data):
    """Exclusive writes preserve both completed receipts and uncertain intent."""
    require(path.parent.resolve() in (BASE, MEDIA.resolve()), "Write escaped section scope")
    with os.fdopen(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def save(name, value):
    durable(BASE / name, encoded(value))


def fixed(name, data):
    path = BASE / name
    if path.exists():
        require(path.is_file() and not path.is_symlink() and path.read_bytes() == data,
                "Existing bound receipt differs; preserve it and investigate")
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
            "Media URL is outside established media hosts")
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
    require(isinstance(url, str), "Queue URL is missing")
    parsed = urllib.parse.urlsplit(url)
    require(parsed.scheme == "https" and parsed.hostname == "queue.fal.run"
            and parsed.port is None and not parsed.username and not parsed.password
            and not parsed.query and not parsed.fragment,
            "Authenticated URL is outside the exact queue origin")
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
        require(len(data) <= 1024 * 1024 and key.encode() not in data,
                "Queue response exceeded bounds or contained authentication material")
        result = json.loads(data)
        require(isinstance(result, dict), "Queue response is not an object")
        return result
    except (urllib.error.URLError, OSError, ValueError) as error:
        save("SYNC-ERROR-" + uuid.uuid4().hex + ".json", {
            "at": now(), "operation": operation, "exception_type": type(error).__name__,
            "http_status": getattr(error, "code", None),
            "instruction": "Do not repeat submission. Preserve intent and reconcile provider state; GET may be checked again."})
        raise RuntimeError("Fal response failed or is uncertain. Do not resubmit; inspect preserved SYNC records.") from None


def exact_local(value, expected):
    require(isinstance(value, str), "Local media path is missing")
    path = Path(value)
    local = (path if path.is_absolute() else REPO / path).resolve()
    require(not expected.is_symlink() and expected.resolve() == local
            and local.parent == MEDIA.resolve() and local.is_file(), "Local media path differs from exact section file")
    return local


def validate_input(remote=False):
    require(not (BASE / "INPUT.json").is_symlink(), "Input record must not be a symlink")
    raw = (BASE / "INPUT.json").read_bytes()
    value = json.loads(raw)
    required = {"video_url", "video_sha256", "video_local_path", "audio_url", "audio_sha256", "audio_local_path", "duration"}
    require(isinstance(value, dict) and required <= set(value)
            and set(value) <= required | {"scope", "model", "sync_mode"}, "INPUT.json has missing or unsupported fields")
    require(value.get("model", MODEL) == MODEL and value.get("sync_mode", "silence") == "silence",
            "Only Sync v3 with silence mode is authorized")
    manifest_raw = (FULL / "AUDIO-IMAGE-INPUTS.json").read_bytes()
    manifest = json.loads(manifest_raw)
    require(isinstance(manifest, list) and all(isinstance(item, dict) for item in manifest),
            "Authoritative audio and image manifest must remain a list")
    sections = [item for item in manifest if item.get("name") == SECTION]
    require(len(sections) == 1, "Audio section is missing or ambiguous")
    audio = sections[0]
    require(audio["sha256"] == AUDIO_SHA and audio["url"] == AUDIO_URL,
            "Authoritative opening audio hash or hosted URL changed")
    frames = RANGES[SECTION][1] - RANGES[SECTION][0]
    require(isinstance(value["duration"], (int, float)) and not isinstance(value["duration"], bool)
            and math.isfinite(value["duration"]) and abs(value["duration"] - frames / 48000) < 1e-8,
            "Duration differs from exact authorized audio samples")
    for key in ("video_sha256", "audio_sha256"):
        require(isinstance(value[key], str) and re.fullmatch(r"[0-9a-f]{64}", value[key]), "Media hash is invalid")
    require(value["audio_sha256"] == audio["sha256"] and value["audio_url"] == audio["url"],
            "Audio differs from exact authorized section")
    wav = exact_local(value["audio_local_path"], MEDIA / "opening.wav")
    video = exact_local(value["video_local_path"], MEDIA / (SECTION + "-native.mp4"))
    require(sha(wav.read_bytes()) == audio["sha256"], "Local authorized audio changed")
    require(sha(video.read_bytes()) == value["video_sha256"], "Local native video differs from bound hash")
    with wave.open(str(wav), "rb") as stream:
        require((stream.getframerate(), stream.getnchannels(), stream.getsampwidth(), stream.getnframes(), stream.getcomptype())
                == (48000, 1, 2, frames, "NONE"), "Audio must remain exact source-duration 48 kHz mono PCM16")
        opening_pcm = stream.readframes(frames)
    master = FULL.parent / "media/voice/voice-w2b.original-c.wav"
    require(sha(master.read_bytes()) == MASTER_SHA, "Approved full Original C master changed")
    with wave.open(str(master), "rb") as stream:
        require((stream.getframerate(), stream.getnchannels(), stream.getsampwidth(), stream.getcomptype())
                == (48000, 1, 2, "NONE"), "Approved master PCM format changed")
        require(stream.readframes(frames) == opening_pcm,
                "Opening must preserve approved master samples [0,1048000) exactly")
    media_url(value["audio_url"])
    media_url(value["video_url"])
    if remote:
        require(sha(fetch(value["video_url"])) == value["video_sha256"], "Hosted native video differs from bound hash")
        require(sha(fetch(value["audio_url"])) == audio["sha256"], "Hosted audio differs from authoritative WAV")
    request = {"model": MODEL, "section": SECTION, "native_job": NATIVE_JOB,
               "input": {"video_url": value["video_url"], "audio_url": value["audio_url"], "sync_mode": "silence"},
               "input_record_sha256": sha(raw), "audio_manifest_sha256": sha(manifest_raw),
               "video_sha256": value["video_sha256"], "audio_sha256": audio["sha256"], "duration": frames / 48000}
    require((BASE / "INPUT.json").read_bytes() == raw and (FULL / "AUDIO-IMAGE-INPUTS.json").read_bytes() == manifest_raw,
            "Inputs changed during validation")
    return raw, value, request


def validate_job_urls(result):
    queue_url(result["status_url"], "status", result["request_id"])
    queue_url(result["response_url"], "result", result["request_id"])


def job():
    intent = read("SYNC-SUBMISSION-INTENT.json")
    request_raw = (BASE / "SYNC-REQUEST.json").read_bytes()
    bound_input = (BASE / "SYNC-BOUND-INPUT.json").read_bytes()
    request = json.loads(request_raw)
    require(intent["model"] == MODEL and intent["section"] == SECTION
            and request["native_job"] == NATIVE_JOB
            and intent["request_sha256"] == sha(request_raw), "Bound request changed after submission")
    require(request["input_record_sha256"] == sha(bound_input) == intent["input_record_sha256"]
            and (BASE / "INPUT.json").read_bytes() == bound_input
            and sha((FULL / "AUDIO-IMAGE-INPUTS.json").read_bytes()) == request["audio_manifest_sha256"],
            "Bound input or audio manifest changed after submission")
    result_raw = (BASE / "SYNC-JOB.json").read_bytes()
    result = json.loads(result_raw)
    binding = read("SYNC-JOB-BINDING.json")
    require(binding["job_sha256"] == sha(result_raw) and binding["request_sha256"] == sha(request_raw)
            and binding["request_id"] == result["request_id"], "Immutable job reference changed")
    validate_job_urls(result)
    return result


def main():
    global BASE, SECTION
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("preflight", "submit", "status", "result", "download"))
    args = parser.parse_args()
    expected_base = FULL / SECTION
    require(expected_base.is_dir() and not expected_base.is_symlink() and not MEDIA.is_symlink(),
            "Root must create the real section and media directories before use")
    BASE = expected_base.resolve()
    mode = args.command
    if mode in ("preflight", "submit"):
        if mode == "submit":
            require(not (BASE / "SYNC-SUBMISSION-INTENT.json").exists()
                    and not (BASE / "SYNC-JOB.json").exists(), "Intent or job already exists. Do not resubmit.")
        raw, value, request = validate_input(remote=mode == "submit")
        if mode == "preflight":
            result = {"status": "local_inputs_validated_no_network_or_submission", "hosted_bytes_verified": False, **request}
        else:
            credential()
            fixed("SYNC-BOUND-INPUT.json", raw)
            request_bytes = encoded(request)
            fixed("SYNC-REQUEST.json", request_bytes)
            save("SYNC-SUBMISSION-INTENT.json", {"at": now(), "model": MODEL, "section": SECTION,
                 "scope": value.get("scope", "Authorized SELFIE-AVATAR-002 full-02 " + SECTION + " restoration"),
                 "request_sha256": sha(request_bytes), "input_record_sha256": sha(raw),
                 "retry": False, "instruction": "One POST only. Reconcile uncertain outcomes without resubmission."})
            result = api(ORIGIN + "/" + MODEL, "submit", request["input"])
            save("SYNC-JOB.json", result)
            validate_job_urls(result)
            save("SYNC-JOB-BINDING.json", {"request_id": result["request_id"],
                 "job_sha256": sha((BASE / "SYNC-JOB.json").read_bytes()), "request_sha256": sha(request_bytes)})
            job()
    elif mode in ("status", "result"):
        bound = job()
        result = api(bound["status_url" if mode == "status" else "response_url"], mode, request_id=bound["request_id"])
        save("SYNC-" + mode.upper() + "-" + uuid.uuid4().hex + ".json", result)
        if mode == "result":
            media_url(result["video"]["url"])
            fixed("SYNC-RESULT.json", encoded(result))
            fixed("SYNC-RESULT-BINDING.json", encoded({"request_id": bound["request_id"], "result_sha256": sha(encoded(result))}))
    else:
        bound = job()
        response_raw = (BASE / "SYNC-RESULT.json").read_bytes()
        binding = read("SYNC-RESULT-BINDING.json")
        require(binding["request_id"] == bound["request_id"] and binding["result_sha256"] == sha(response_raw),
                "Bound result changed before download")
        url = json.loads(response_raw)["video"]["url"]
        data = fetch(url)
        require(b"ftyp" in data[:64], "Downloaded result is not an MP4 container")
        path = MEDIA / (SECTION + "-restored.mp4")
        require(not path.is_symlink(), "Download target must not be a symlink")
        if path.exists():
            require(sha(path.read_bytes()) == sha(data), "Existing downloaded repair differs; preserve it and investigate")
        else:
            durable(path, data)
        result = {"url": url, "path": str(path.relative_to(REPO)), "bytes": len(data), "sha256": sha(data),
                  "request_id": bound["request_id"], "result_record_sha256": sha(response_raw)}
        fixed("SYNC-DOWNLOAD.json", encoded(result))
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, OSError, RuntimeError, wave.Error) as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(1)
