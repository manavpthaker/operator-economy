"""One opening-only Sync 2 Pro request. No implicit submission or retry.

Video probing belongs to the Higgsfield sandbox. This adapter checks the pinned
root VIDEO-QA record, media hashes, and WAV structure; it never runs ffprobe.
"""
import argparse
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
import wave
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
MEDIA = REPO / "blueprint-cinema/experiments/SELFIE-AVATAR-001/media/revision-07"
MODEL = "fal-ai/sync-lipsync/v2/pro"
SYNC_MODE = "cut_off"
OUTPUT = MEDIA / "home-olive-gtm-r7-opening-sync.mp4"
LIMITS = "Byte/provenance/format checks only; no perceptual sync or performance acceptance."


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def read(name):
    return json.loads((BASE / name).read_text())


def save(name, value, exclusive=False):
    BASE.mkdir(parents=True, exist_ok=True)
    with (BASE / name).open("x" if exclusive else "w") as output:
        json.dump(value, output, indent=2)
        output.write("\n")
        output.flush()
        # The exclusive intent must be durable before the sole POST begins.
        if exclusive:
            os.fsync(output.fileno())
    if exclusive:
        directory_fd = os.open(BASE, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)


def https_url(url, authenticated=False):
    require(isinstance(url, str), "URL must be a string")
    parsed = urllib.parse.urlsplit(url)
    require(parsed.scheme == "https" and parsed.hostname, "HTTPS URL required")
    require(not parsed.username and not parsed.password and not parsed.fragment,
            "URL credentials and fragments are prohibited")
    require(parsed.port in (None, 443), "Only HTTPS port 443 is permitted")
    if authenticated:
        require(parsed.hostname == "queue.fal.run", "Auth is restricted to queue.fal.run")
    return url


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect())


def credential():
    for line in (REPO / ".env").read_text().splitlines():
        match = re.match(r"^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$", line)
        if match:
            value = match.group(1).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            require(bool(value), "FAL_KEY is empty")
            return value
    raise ValueError("FAL_KEY unavailable in existing OE .env")


def fetch(url):
    request = urllib.request.Request(https_url(url), headers={"User-Agent": "OE-R7-integrity-check"})
    with OPENER.open(request, timeout=60) as response:
        return response.read()


def api(url, payload=None):
    https_url(url, authenticated=True)  # Validate before reading credentials.
    key = credential()
    request = urllib.request.Request(url,
        data=None if payload is None else json.dumps(payload).encode(),
        headers={"Authorization": "Key " + key, "Content-Type": "application/json",
                 "X-Fal-No-Retry": "1", "x-app-fal-disable-fallback": "1"})
    try:
        with OPENER.open(request, timeout=45) as response:
            return json.loads(response.read().decode().replace(key, "[REDACTED]"))
    except urllib.error.HTTPError as error:
        save("ERROR.json", {"at": now(), "http_status": error.code,
             "detail": error.read(8000).decode(errors="replace").replace(key, "[REDACTED]"),
             "is_submission": payload is not None,
             "instruction": "Stop and inspect. Preserve the intent; do not resubmit."})
        raise RuntimeError("Fal HTTP error recorded; no submission retry is allowed") from None
    except (urllib.error.URLError, TimeoutError, OSError, UnicodeError, json.JSONDecodeError) as error:
        save("TRANSPORT-UNCERTAIN.json", {"at": now(), "exception_type": type(error).__name__,
             "is_submission": payload is not None,
             "instruction": "Do not retry submission. Preserve intent and reconcile provider state."})
        raise RuntimeError("Outcome uncertain; do not submit again") from None


def pinned_bytes(item, media=False):
    path = (REPO / item["local_path"]).resolve()
    require(path.is_relative_to((MEDIA if media else REPO).resolve()), "Pinned path is outside permitted scope")
    require(re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is not None, "Invalid SHA-256")
    data = path.read_bytes()
    require(digest(data) == item["sha256"], "Pinned local bytes changed: " + str(path))
    return data


def wav_info(data, expected_count):
    with wave.open(io.BytesIO(data)) as audio:
        actual = (audio.getframerate(), audio.getnchannels(), audio.getsampwidth(), audio.getnframes())
        require(actual == (48000, 1, 2, expected_count), "Audio must be matched 48kHz mono 16-bit WAV")
        require(audio.getcomptype() == "NONE", "Uncompressed PCM WAV required")
        pcm = audio.readframes(expected_count)
        require(len(pcm) == expected_count * 2, "Truncated WAV PCM")
        return {"sample_rate_hz": 48000, "channels": 1, "sample_width_bytes": 2,
                "sample_count": expected_count, "pcm_sha256": digest(pcm)}


def video_from_qa(record, video):
    require(record["video"]["sha256"] == video["sha256"], "VIDEO-QA belongs to different video bytes")
    probe = record["matched_probe"]
    streams = probe["streams"]
    pictures = [s for s in streams if s.get("codec_type") == "video"]
    require(len(pictures) == 1, "Exactly one video stream required")
    require(not any(s.get("codec_type") == "audio" for s in streams), "Input video must have no audio")
    picture = pictures[0]
    count = int(picture.get("nb_read_frames", picture.get("nb_frames", "0")))
    require(count == video["frame_count"] > 0, "Probed frame count mismatch")
    require((picture["width"], picture["height"], picture["r_frame_rate"]) == (720, 1280, "24/1"),
            "Expected 720x1280 at 24fps")
    duration = float(picture.get("duration", probe["format"]["duration"]))
    require(abs(duration - count / 24) <= 0.001, "Probed duration differs from frame duration")
    require(abs(float(video["duration_seconds"]) - count / 24) <= 0.001, "Manifest duration mismatch")
    require((video["width"], video["height"], video["frame_rate"], video["audio_stream_count"]) ==
            (720, 1280, "24/1", 0), "Manifest picture fields mismatch")
    return {"width": 720, "height": 1280, "frame_rate": "24/1", "frame_count": count,
            "duration_seconds": count / 24, "audio_stream_count": 0,
            "basis": "Pinned root VIDEO-QA matched_probe; no local video probe performed"}


def validate(incoming, hosted):
    require(incoming["section_index"] == 1, "Only the R7 opening is permitted")
    require("sections" not in incoming, "Batch input is prohibited")
    if "model" in incoming:
        require(incoming["model"] == MODEL, "Model override prohibited")
    if "sync_mode" in incoming:
        require(incoming["sync_mode"] == SYNC_MODE, "Sync-mode override prohibited")
    video, audio = incoming["video"], incoming["audio"]
    video_data, audio_data = pinned_bytes(video, media=True), pinned_bytes(audio, media=True)
    for item in (video, audio):
        https_url(item["url"])
    qa = json.loads(pinned_bytes(incoming["video_qa"]))
    picture = video_from_qa(qa, video)
    count = audio["sample_count"]
    require(type(count) is int and count == picture["frame_count"] * 2000,
            "Audio samples must equal frame count times 2000")
    require((audio["sample_rate_hz"], audio["channels"], audio["sample_width_bytes"]) == (48000, 1, 2),
            "Manifest audio format mismatch")
    wav = wav_info(audio_data, count)
    for name in ("source_audio", "script", "voice_proof"):
        pinned_bytes(incoming[name])
    require(isinstance(json.loads(pinned_bytes(incoming["voice_proof"])), dict), "Voice proof must be a JSON report")
    if hosted:
        require(digest(fetch(video["url"])) == video["sha256"], "Hosted video byte mismatch")
        remote_audio = fetch(audio["url"])
        require(digest(remote_audio) == audio["sha256"], "Hosted audio byte mismatch")
        require(wav_info(remote_audio, count) == wav, "Hosted WAV structure/PCM mismatch")
    return {"picture": picture, "audio": wav, "hosted_bytes_checked": hosted,
            "provenance": "Source, script and voice-proof report hashes checked. PCM transformation proof remains in the voice report.",
            "limits": LIMITS}


def bind(path):
    require(not (BASE / "MANIFEST.json").exists(), "Already bound; rebinding is prohibited")
    require(not (BASE / "SUBMISSION-INTENT.json").exists(), "Submission intent already exists")
    raw = path.resolve().read_bytes()
    incoming = json.loads(raw)
    checks = validate(incoming, hosted=True)
    save("BOUND-INPUT.json", incoming, exclusive=True)
    manifest = {"bound_at": now(), "input_path": str(path.resolve()), "input_sha256": digest(raw),
                "bound_input_sha256": digest((BASE / "BOUND-INPUT.json").read_bytes()),
                "adapter_sha256": digest(Path(__file__).read_bytes()), "checks": checks}
    save("MANIFEST.json", manifest, exclusive=True)
    save("REQUEST.json", {"model": MODEL, "input": {"video_url": incoming["video"]["url"],
         "audio_url": incoming["audio"]["url"], "sync_mode": SYNC_MODE},
         "manifest_sha256": digest((BASE / "MANIFEST.json").read_bytes())}, exclusive=True)
    return {"status": "one_opening_bound_no_submission", "checks": checks}


def bound():
    manifest, request = read("MANIFEST.json"), read("REQUEST.json")
    require(manifest["adapter_sha256"] == digest(Path(__file__).read_bytes()), "Adapter changed after bind")
    require(manifest["bound_input_sha256"] == digest((BASE / "BOUND-INPUT.json").read_bytes()), "Bound input changed")
    require(manifest["input_sha256"] == digest(Path(manifest["input_path"]).read_bytes()), "Root request input changed")
    require(request["manifest_sha256"] == digest((BASE / "MANIFEST.json").read_bytes()), "Manifest changed")
    incoming = read("BOUND-INPUT.json")
    expected = {"video_url": incoming["video"]["url"], "audio_url": incoming["audio"]["url"], "sync_mode": SYNC_MODE}
    require(request["model"] == MODEL and request["input"] == expected, "Request/model changed")
    return incoming, request


def submit():
    require(not (BASE / "SUBMISSION-INTENT.json").exists(), "Intent exists; a second POST is prohibited")
    require(not (BASE / "JOB.json").exists(), "Job already exists")
    incoming, request = bound()
    checks = validate(incoming, hosted=True)  # Fresh local and hosted checks immediately before POST.
    credential()  # Fail before consuming intent if the existing credential is absent.
    save("SUBMISSION-INTENT.json", {"at": now(), "section_index": 1, "model": MODEL,
         "sync_mode": SYNC_MODE, "max_submission_calls": 1, "retry": False,
         "request_sha256": digest((BASE / "REQUEST.json").read_bytes()),
         "video_sha256": incoming["video"]["sha256"], "audio_sha256": incoming["audio"]["sha256"],
         "checks": checks}, exclusive=True)
    job = api("https://queue.fal.run/" + MODEL, request["input"])
    save("JOB.json", job, exclusive=True)
    return job


def status_or_result(mode):
    job = read("JOB.json")
    result = api(job["status_url"] if mode == "status" else job["response_url"])
    save("STATUS.json" if mode == "status" else "RESULT.json", result)
    return result


def download():
    url = read("RESULT.json")["video"]["url"]
    data = fetch(url)
    require(bool(data), "Empty provider output")
    MEDIA.mkdir(parents=True, exist_ok=True)
    if OUTPUT.exists():
        require(digest(OUTPUT.read_bytes()) == digest(data), "Existing output differs; do not overwrite")
    else:
        with OUTPUT.open("xb") as output:
            output.write(data)
    result = {"url": url, "local_path": str(OUTPUT.relative_to(REPO)), "sha256": digest(data),
              "bytes": len(data), "limits": "Downloaded bytes only. Root must run sandbox media/audio QA."}
    save("DOWNLOAD.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["preflight", "bind", "submit", "status", "result", "download"])
    parser.add_argument("input_path", nargs="?", type=Path)
    args = parser.parse_args()
    if args.operation == "preflight":
        result = {"status": "adapter_prepared", "model": MODEL, "sync_mode": SYNC_MODE,
                  "max_submission_calls": 1, "manifest_exists": (BASE / "MANIFEST.json").exists(),
                  "intent_exists": (BASE / "SUBMISSION-INTENT.json").exists(), "limits": LIMITS}
    elif args.operation == "bind":
        require(args.input_path is not None, "bind requires REQUEST-INPUT.json path")
        result = bind(args.input_path)
    else:
        require(args.input_path is None, "Only bind accepts an input path; there are no section/batch arguments")
        result = submit() if args.operation == "submit" else download() if args.operation == "download" else status_or_result(args.operation)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        # Do not print provider request objects, headers, tracebacks or credential values.
        print(type(error).__name__ + ": " + str(error), file=sys.stderr)
        sys.exit(1)
