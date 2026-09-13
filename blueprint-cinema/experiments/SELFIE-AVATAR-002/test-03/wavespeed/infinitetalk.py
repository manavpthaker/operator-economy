"""One authorized 7s InfiniteTalk 720p comparison; no automatic paid retry.

Commands: preflight, submit, status, result, download. Preflight and submit check
current price/balance. Credentials stay in runtime or the scoped OE .env file.
"""
import datetime
import hashlib
import io
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
LOCAL_AUDIO = BASE.parents[1] / "media/test-01/test01-original-c.wav"
MODEL = "wavespeed-ai/infinitetalk"
ORIGIN = "https://api.wavespeed.ai/api/v3/"
IMAGE = "https://v3b.fal.media/files/b/0aaa4d9d/0jMafvpQWUPbcX1UQ32-W_selfie-w2-near-frontal-v12.png"
AUDIO = "https://v3b.fal.media/files/b/0aaa4ce5/8wlAwsss4900PrY4KYAmi_selfie-w2-test01-original-c.wav"
IMAGE_SHA = "4b0301ae71ce0a613e6d0d537191be0d0b1cd49dd9147ca13d4ef3a0d11362ad"
AUDIO_SHA = "2fda60f4b9f61fcb2f784ae311ce13f87525a484920e5a6d0079e0033b730609"
PROMPT = "Natural understated near-frontal conversation, relaxed neutral expression, small natural mouth movements and ordinary blinking. Stable head and camera, without smiles, nods, or added gestures."
PAYLOAD = {"image": IMAGE, "audio": AUDIO, "resolution": "720p", "prompt": PROMPT}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def raw_json(value):
    return (json.dumps(value, indent=2) + "\n").encode()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def read(name):
    return json.loads((BASE / name).read_bytes())


def write(name, data, replace=False):
    with os.fdopen(os.open(BASE / name, os.O_WRONLY | os.O_CREAT |
                           (os.O_TRUNC if replace else os.O_EXCL), 0o600), "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    fd = os.open(BASE, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def fixed(name, data):
    if (BASE / name).exists():
        require((BASE / name).read_bytes() == data, "An existing immutable record differs; preserve it and investigate")
    else:
        write(name, data)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect())


def fetch(url):
    parsed = urllib.parse.urlsplit(url)
    require(parsed.scheme == "https" and parsed.hostname and not parsed.username
            and not parsed.password and parsed.port in (None, 443) and not parsed.fragment,
            "Media URL must be HTTPS without embedded credentials or fragments")
    with OPENER.open(url, timeout=60) as response:
        require(response.status == 200, "Media response must be HTTP 200")
        data = response.read(100 * 1024 * 1024 + 1)
    require(0 < len(data) <= 100 * 1024 * 1024, "Media response is empty or too large")
    return data


def credential():
    key = os.environ.get("WAVESPEED_API_KEY", "").strip()
    if not key and (REPO / ".env").is_file():
        for line in (REPO / ".env").read_text().splitlines():
            match = re.match(r"^\s*(?:export\s+)?WAVESPEED_API_KEY\s*=\s*(.*?)\s*$", line)
            if match:
                key = match.group(1).strip().strip('\"').strip("'")
                break
    require(key and "\r" not in key and "\n" not in key, "WAVESPEED_API_KEY is unavailable in runtime or scoped OE .env")
    return key


def api(operation, payload=None, prediction=None):
    routes = {"balance": "balance", "price": "model/price", "submit": MODEL}
    if operation == "result":
        require(isinstance(prediction, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,100}", prediction), "Invalid prediction id")
        path = "predictions/" + prediction + "/result"
    else:
        require(operation in routes, "Unknown authenticated operation")
        path = routes[operation]
    require((payload is not None) == (operation in ("price", "submit")), "Unexpected authenticated request method")
    key = credential()
    request = urllib.request.Request(ORIGIN + path,
        data=None if payload is None else json.dumps(payload, separators=(",", ":")).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        with OPENER.open(request, timeout=60) as response:
            body = response.read(2 * 1024 * 1024 + 1)
        require(len(body) <= 2 * 1024 * 1024 and key.encode() not in body, "Unexpected queue response; no response body retained")
        value = json.loads(body)
        require(isinstance(value, dict) and value.get("code") == 200 and isinstance(value.get("data"), dict), "Provider returned an unsuccessful or invalid response")
        return value
    except (urllib.error.URLError, OSError, ValueError) as error:
        write("ERROR-" + uuid.uuid4().hex + ".json", raw_json({"at": now(), "operation": operation,
              "exception_type": type(error).__name__, "http_status": getattr(error, "code", None),
              "instruction": "Never repeat a generation submission after an intent exists. Read-only checks may be repeated manually."}))
        raise RuntimeError("WaveSpeed request failed or is uncertain; inspect preserved records without resubmitting generation") from None


def validate_inputs():
    raw = (BASE / "INPUT.json").read_bytes()
    value = json.loads(raw)
    require(value.get("model") == MODEL and value.get("input") == PAYLOAD
            and value.get("image_sha256") == IMAGE_SHA and value.get("audio_sha256") == AUDIO_SHA
            and value.get("duration_seconds") == 7 and value.get("maximum_estimate_usd") == 0.42,
            "Inputs differ from the authorized V12 / original 7s WAV / 720p comparison")
    local = LOCAL_AUDIO.read_bytes()
    require(sha(local) == AUDIO_SHA, "Authoritative local WAV hash changed")
    with wave.open(io.BytesIO(local), "rb") as stream:
        require((stream.getframerate(), stream.getnchannels(), stream.getsampwidth(), stream.getnframes(),
                 stream.getcomptype()) == (48000, 1, 2, 336000, "NONE"), "Audio must remain the exact seven-second PCM source")
    require(sha(fetch(IMAGE)) == IMAGE_SHA and sha(fetch(AUDIO)) == AUDIO_SHA, "Hosted input hash differs from the authorized source")
    require((BASE / "INPUT.json").read_bytes() == raw, "Input record changed during verification")
    return raw


def number(value, label):
    require(type(value) in (int, float) and math.isfinite(value) and value >= 0, "Invalid " + label)
    return value


def preflight():
    raw = validate_inputs()
    price = api("price", {"model_id": MODEL, "inputs": PAYLOAD})
    balance = api("balance")
    quote = price["data"]
    require(quote.get("model_id") == MODEL and quote.get("currency") == "USD", "Price quote identity or currency differs")
    payable = number(quote.get("discounted_price"), "discounted USD quote")
    available = number(balance["data"].get("balance"), "USD balance")
    report = {"at": now(), "input_sha256": sha(raw), "price_request": {"model_id": MODEL, "inputs": PAYLOAD},
              "price_response": price, "balance_response": balance, "estimated_payable_usd": payable,
              "maximum_estimate_usd": 0.42, "sufficient_balance": available >= payable,
              "status": "read_only_preflight_no_generation"}
    name = "PREFLIGHT-" + uuid.uuid4().hex + ".json"
    write(name, raw_json(report))
    write("PREFLIGHT.json", raw_json(report), replace=True)
    require(payable <= 0.420001, "Current estimate exceeds the authorized $0.42 test scope")
    require(available >= payable, "Existing balance does not cover this test; no generation submitted")
    return raw, report, name


def bound_prediction():
    intent = read("SUBMISSION-INTENT.json")
    require(intent["input_sha256"] == sha((BASE / "INPUT.json").read_bytes())
            and (BASE / "INPUT.json").read_bytes() == (BASE / "BOUND-INPUT.json").read_bytes(), "Input changed after submission intent")
    require(intent["request_sha256"] == sha((BASE / "REQUEST.json").read_bytes()), "Request changed after submission intent")
    data = read("JOB.json")["data"]
    require(isinstance(data.get("id"), str) and re.fullmatch(r"[A-Za-z0-9_-]{1,100}", data["id"]), "Invalid bound prediction id")
    require(data.get("model") == MODEL, "Prediction model differs from this authorized test")
    return data["id"]


def main():
    require(len(sys.argv) == 2 and sys.argv[1] in ("preflight", "submit", "status", "result", "download"),
            "Use one command: preflight, submit, status, result, download")
    mode = sys.argv[1]
    if mode in ("preflight", "submit"):
        if mode == "submit":
            require(not (BASE / "SUBMISSION-INTENT.json").exists() and not (BASE / "JOB.json").exists(), "A generation intent or job already exists. Never resubmit.")
        raw, result, preflight_name = preflight()
        if mode == "submit":
            fixed("BOUND-INPUT.json", raw)
            request = raw_json({"model": MODEL, "input": PAYLOAD, "input_sha256": sha(raw)})
            fixed("REQUEST.json", request)
            require((BASE / "INPUT.json").read_bytes() == raw, "Input changed after preflight")
            write("SUBMISSION-INTENT.json", raw_json({"at": now(), "model": MODEL,
                  "input_sha256": sha(raw), "request_sha256": sha(request),
                  "preflight_record": preflight_name, "preflight_sha256": sha((BASE / preflight_name).read_bytes()),
                  "estimated_payable_usd": result["estimated_payable_usd"], "retry": False}))
            result = api("submit", PAYLOAD)
            write("JOB.json", raw_json(result))
            bound_prediction()
    elif mode in ("status", "result"):
        prediction = bound_prediction()
        result = api("result", prediction=prediction)
        data = result["data"]
        require(data.get("id") == prediction and data.get("model") == MODEL, "Result identity differs from the bound prediction")
        write("STATUS-" + uuid.uuid4().hex + ".json", raw_json(result))
        write("STATUS.json", raw_json(result), replace=True)
        if data.get("status") == "completed":
            fixed("RESULT.json", raw_json(result))
        elif data.get("status") in ("failed", "cancelled", "timeout", "deleted"):
            raise RuntimeError("Prediction ended unsuccessfully; preserved status is terminal and no retry will run")
    else:
        prediction = bound_prediction()
        data = read("RESULT.json")["data"]
        require(data.get("status") == "completed" and data.get("id") == prediction, "A completed bound result is required")
        outputs = data.get("outputs")
        require(isinstance(outputs, list) and len(outputs) == 1 and isinstance(outputs[0], str), "Expected exactly one video URL")
        content = fetch(outputs[0])
        fixed("infinitetalk-test03.mp4", content)
        result = {"prediction_id": prediction, "url": outputs[0], "path": str(BASE / "infinitetalk-test03.mp4"),
                  "bytes": len(content), "sha256": sha(content), "result_sha256": sha((BASE / "RESULT.json").read_bytes())}
        fixed("DOWNLOAD.json", raw_json(result))
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, OSError, RuntimeError, wave.Error) as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(1)
