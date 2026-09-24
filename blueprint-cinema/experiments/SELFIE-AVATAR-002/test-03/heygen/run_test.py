"""One bounded HeyGen Avatar IV request. No POST retries or automatic repairs.

Commands: preflight (public input GETs only), submit, status, result, download.
Credentials come only from runtime HEYGEN_API_KEY or this OE checkout's .env.
Every artifact written by this helper stays in its own directory.
"""

import datetime
import hashlib
import io
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
EXPERIMENT = BASE.parents[1]
REPO = BASE.parents[4]
IMAGE_SHA = "4b0301ae71ce0a613e6d0d537191be0d0b1cd49dd9147ca13d4ef3a0d11362ad"
AUDIO_SHA = "2fda60f4b9f61fcb2f784ae311ce13f87525a484920e5a6d0079e0033b730609"
IMAGE_URL = "https://v3b.fal.media/files/b/0aaa4d9d/0jMafvpQWUPbcX1UQ32-W_selfie-w2-near-frontal-v12.png"
AUDIO_URL = "https://v3b.fal.media/files/b/0aaa4ce5/8wlAwsss4900PrY4KYAmi_selfie-w2-test01-original-c.wav"
API_ORIGIN = "https://api.heygen.com"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(name):
    return json.loads((BASE / name).read_bytes())


def durable(path, data):
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
    durable(BASE / name, (json.dumps(value, indent=2) + "\n").encode())


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect())


def credential():
    value = os.environ.get("HEYGEN_API_KEY", "").strip()
    if not value and (REPO / ".env").is_file():
        for line in (REPO / ".env").read_text().splitlines():
            match = re.match(r"^\s*(?:export\s+)?HEYGEN_API_KEY\s*=\s*(.*?)\s*$", line)
            if match:
                value = match.group(1).strip().strip('"').strip("'")
                break
    require(value and "\r" not in value and "\n" not in value,
            "HEYGEN_API_KEY is unavailable in runtime or the scoped OE .env")
    return value


def public_get(url, limit=100 * 1024 * 1024):
    parsed = urllib.parse.urlsplit(url)
    require(parsed.scheme == "https" and parsed.hostname and not parsed.username
            and not parsed.password and parsed.port in (None, 443) and not parsed.fragment,
            "Expected an HTTPS media URL without embedded credentials")
    with OPENER.open(url, timeout=60) as response:
        require(response.status == 200, "Media response is not HTTP 200")
        content_type = response.headers.get("Content-Type", "")
        data = response.read(limit + 1)
    require(0 < len(data) <= limit, "Media response is empty or unexpectedly large")
    return data, content_type


def validate_inputs():
    request_raw = (BASE / "REQUEST.json").read_bytes()
    payload = json.loads(request_raw)
    require(set(payload) == {"type", "image", "audio_url", "resolution",
                            "aspect_ratio", "output_format", "title", "callback_id"},
            "Request fields changed from the reviewed direct-image comparison")
    require(payload["type"] == "image" and payload["image"] == {"type": "url", "url": IMAGE_URL}
            and payload["audio_url"] == AUDIO_URL
            and payload["resolution"] == "720p" and payload["aspect_ratio"] == "9:16"
            and payload["output_format"] == "mp4", "Request changed the bound model, source, or output")
    record = read("INPUT.json")
    require(record["reference_sha256"] == IMAGE_SHA and record["audio_sha256"] == AUDIO_SHA,
            "Input provenance differs from authorized sources")
    for local, url, expected in (
        (EXPERIMENT / "media/reference/stone-polo-office-reference-v12.png", IMAGE_URL, IMAGE_SHA),
        (EXPERIMENT / "media/test-01/test01-original-c.wav", AUDIO_URL, AUDIO_SHA),
    ):
        require(sha(local.read_bytes()) == expected, "Local authorized source changed")
        remote, _ = public_get(url)
        require(sha(remote) == expected, "Hosted source differs from the authorized hash")
        if expected == AUDIO_SHA:
            with wave.open(io.BytesIO(remote), "rb") as audio:
                require((audio.getframerate(), audio.getnchannels(), audio.getsampwidth(),
                         audio.getnframes(), audio.getcomptype()) == (48000, 1, 2, 336000, "NONE"),
                        "Audio must remain exactly seven seconds of 48 kHz mono PCM16")
    require((BASE / "REQUEST.json").read_bytes() == request_raw, "Request changed during validation")
    return request_raw, payload


def api(operation, key, payload=None, video_id=None):
    require(operation in ("submit", "status", "result"), "Unknown API operation")
    if operation == "submit":
        require(payload is not None and video_id is None, "Invalid submission parameters")
        path = "/v3/videos"
    else:
        require(payload is None and re.fullmatch(r"[A-Za-z0-9_-]{1,100}", video_id or ""),
                "Invalid stored video id")
        path = "/v3/videos/" + video_id
    request = urllib.request.Request(API_ORIGIN + path,
        data=None if payload is None else json.dumps(payload).encode(),
        headers={"x-api-key": key, "Content-Type": "application/json"})
    try:
        with OPENER.open(request, timeout=60) as response:
            raw = response.read(1024 * 1024 + 1)
        require(len(raw) <= 1024 * 1024 and key.encode() not in raw,
                "Unexpected API response size or authentication material")
        result = json.loads(raw)
        require(isinstance(result, dict), "API response must be an object")
        if result.get("error"):
            raise ValueError("Provider returned an error")
        return result
    except (urllib.error.URLError, OSError, ValueError) as error:
        save("ERROR-" + uuid.uuid4().hex + ".json", {
            "at": now(), "operation": operation, "exception_type": type(error).__name__,
            "http_status": getattr(error, "code", None),
            "instruction": "Preserve intent. Do not resubmit after a failed or uncertain POST; reconcile provider state. Read-only GETs may be retried."})
        raise RuntimeError("Provider response failed or is uncertain; inspect preserved receipts. Do not resubmit.") from None


def stored_job():
    intent = read("SUBMISSION-INTENT.json")
    require(sha((BASE / "REQUEST.json").read_bytes()) == intent["request_sha256"],
            "Request changed after submission")
    require(sha((BASE / "INPUT.json").read_bytes()) == intent["input_sha256"],
            "Input record changed after submission")
    return read("JOB.json")["video_id"]


def main():
    require(len(sys.argv) == 2, "Use preflight, submit, status, result, or download")
    mode = sys.argv[1]
    require(mode in ("preflight", "submit", "status", "result", "download"), "Unknown command")
    if mode in ("preflight", "submit"):
        if mode == "submit":
            require(not (BASE / "SUBMISSION-INTENT.json").exists() and not (BASE / "JOB.json").exists(),
                    "A submission intent or job already exists. Do not resubmit.")
        request_raw, payload = validate_inputs()
        key = credential()
        if mode == "preflight":
            print(json.dumps({"status": "sources_validated_no_api_call", "credential_present": True,
                              "request_sha256": sha(request_raw), "audio_seconds": 7,
                              "estimated_usd": 0.35, "account_eligibility_and_balance": "unverified"}))
            return
        save("SUBMISSION-INTENT.json", {"at": now(), "request_sha256": sha(request_raw),
             "input_sha256": sha((BASE / "INPUT.json").read_bytes()), "endpoint": API_ORIGIN + "/v3/videos",
             "single_submit": True, "automatic_retry": False})
        response = api("submit", key, payload=payload)
        save("SUBMISSION-RESPONSE.json", response)
        data = response.get("data", {})
        video_id = data.get("video_id") or data.get("id")
        require(re.fullmatch(r"[A-Za-z0-9_-]{1,100}", video_id or ""),
                "Provider omitted video id; reconcile receipt without resubmission")
        save("JOB.json", {"at": now(), "video_id": video_id})
        print(json.dumps({"status": "submitted", "video_id": video_id}))
    elif mode in ("status", "result"):
        video_id = stored_job()
        response = api(mode, credential(), video_id=video_id)
        save("STATUS-" + uuid.uuid4().hex + ".json", {"at": now(), "response": response})
        data = response.get("data", {})
        if mode == "result":
            require(data.get("status") == "completed" and data.get("video_url"),
                    "Video is not completed with a downloadable result")
            if not (BASE / "RESULT.json").exists():
                save("RESULT.json", response)
        print(json.dumps({"video_id": video_id, "status": data.get("status"),
                          "duration": data.get("duration"), "video_url": data.get("video_url")}))
    else:
        stored_job()
        result = read("RESULT.json")["data"]
        require(result.get("status") == "completed", "Stored result is not complete")
        output = BASE / "media/heygen-original.mp4"
        require(not output.exists(), "Existing output retained; inspect it rather than overwrite")
        video, content_type = public_get(result["video_url"], 300 * 1024 * 1024)
        require(content_type.split(";", 1)[0] in ("video/mp4", "application/octet-stream", "binary/octet-stream")
                and video[4:8] == b"ftyp", "Result is not an MP4")
        output.parent.mkdir(exist_ok=True)
        durable(output, video)
        receipt = {"at": now(), "url": result["video_url"], "path": "media/heygen-original.mp4",
                   "sha256": sha(video), "bytes": len(video), "content_type": content_type,
                   "duration_and_audio_preservation": "Await decoded media QA; no repair applied"}
        save("DOWNLOAD.json", receipt)
        print(json.dumps(receipt))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        print(json.dumps({"status": "stopped", "reason": str(error)}))
        sys.exit(1)
