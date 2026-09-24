#!/usr/bin/env python3
"""One exact Short 01 guide and one Original C transfer; immutable input, no retries."""
from __future__ import annotations

import base64
import datetime
import hashlib
import json
import sys
import urllib.error
import urllib.request
import wave
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
REPO = next(path for path in (BASE, *BASE.parents) if path.name == "operator-economy")
SCRIPT = BASE / "SCRIPT.txt"
STYLE = BASE / "VOICE-STYLE.json"
MEDIA = BASE / "media"

sys.path.insert(0, str(REPO / "operator-blueprint-v2/02-narration-production/tools"))
import capture_n4b as capture  # noqa: E402
import calibrate as cal  # noqa: E402

EXPECTED_SCRIPT_SHA256 = "94988c28ca3aee85f14737e9214d63267c3aa1e7d91dc5deeb9e9a5d37dab2e2"
EXPECTED_STYLE_SHA256 = "41a9ec82b906a974729827a3ab66897f42e8832d842fd17729b1d788b283e123"
EXPECTED_WORDS = 149


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save(path: Path, data: object) -> None:
    with path.open("x", encoding="utf-8") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)
        output.write("\n")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def safe_post(url: str, data: bytes, headers: dict[str, str]) -> tuple[int, bytes]:
    from urllib.parse import urlparse

    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.hostname in ("us-texttospeech.googleapis.com", "api.elevenlabs.io")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=600) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


cal.post = safe_post


def wav_metadata(path: Path) -> dict[str, object]:
    with wave.open(str(path)) as handle:
        return {
            "path": str(path.relative_to(REPO)),
            "sha256": sha(path.read_bytes()),
            "bytes": path.stat().st_size,
            "sample_rate_hz": handle.getframerate(),
            "channels": handle.getnchannels(),
            "sample_width_bits": handle.getsampwidth() * 8,
            "sample_count": handle.getnframes(),
            "duration_seconds": handle.getnframes() / handle.getframerate(),
        }


def main() -> None:
    stage = sys.argv[1]
    assert stage in ("prepare", "guide", "transfer")
    raw_text = SCRIPT.read_bytes()
    raw_style = STYLE.read_bytes()
    assert sha(raw_text) == EXPECTED_SCRIPT_SHA256
    assert sha(raw_style) == EXPECTED_STYLE_SHA256
    text = raw_text.decode("utf-8")
    style = json.loads(raw_style)["style_instructions"]
    assert len(text.split()) == EXPECTED_WORDS
    assert capture.GUIDE_VOICE == "Algieba"
    assert cal.TRANSFER_VOICE_ID == "scMbPZwQjr40V1MzL3Nj"
    assert len(text.encode()) <= 4000 and len(style.encode()) <= 4000
    MEDIA.mkdir(exist_ok=True)
    guide = MEDIA / "short01-final-guide.wav"
    final = MEDIA / "short01-final-original-c.wav"
    request = cal.guide_body(text, style, capture.GUIDE_VOICE)

    if stage == "prepare":
        save(
            BASE / "VOICE-INPUT.json",
            {
                "scope": "One exact locked Short 01 guide plus one Original C transfer; no segmentation, processing, retry or canonical edit.",
                "script_path": str(SCRIPT.relative_to(REPO)),
                "script_sha256": EXPECTED_SCRIPT_SHA256,
                "style_path": str(STYLE.relative_to(REPO)),
                "style_sha256": EXPECTED_STYLE_SHA256,
                "text": text,
                "word_count": EXPECTED_WORDS,
                "guide_request": request,
                "guide_source": str(Path(capture.__file__).relative_to(REPO)),
                "guide_source_sha256": sha(Path(capture.__file__).read_bytes()),
                "request_helper_sha256": sha(Path(cal.__file__).read_bytes()),
                "transfer": {
                    "model": cal.TRANSFER_MODEL,
                    "voice_id": cal.TRANSFER_VOICE_ID,
                    "settings": cal.TRANSFER_VOICE_SETTINGS,
                    "seed": cal.TRANSFER_SEED,
                    "output_format": cal.TRANSFER_OUTPUT_FORMAT,
                    "remove_background_noise": False,
                },
                "force_duration": False,
                "max_guide_calls": 1,
                "max_transfer_calls": 1,
                "credential_redirect_policy": "deny",
                "transport_timeout_seconds": 600,
                "authorization_record": "production/final-v1/PRODUCTION-AUTHORIZATION.json",
            },
        )
        print(json.dumps({"stage": stage, "status": "prepared", "words": EXPECTED_WORDS}))
        return

    authority = json.loads((BASE / "PRODUCTION-AUTHORIZATION.json").read_text())
    assert authority["status"] == "explicit_paid_generation_authority_received"
    pinned = json.loads((BASE / "VOICE-INPUT.json").read_text())
    assert pinned["guide_request"] == request
    assert pinned["request_helper_sha256"] == sha(Path(cal.__file__).read_bytes())
    assert pinned["guide_source_sha256"] == sha(Path(capture.__file__).read_bytes())

    save(
        BASE / f"{stage.upper()}-INTENT.json",
        {
            "at": now(),
            "stage": stage,
            "script_sha256": EXPECTED_SCRIPT_SHA256,
            "scope": "One authorized attempt; uncertain outcomes require inspection, never duplicate submission.",
        },
    )
    if stage == "guide":
        headers = {
            "Authorization": "Bearer " + cal.google_access_token(),
            "Content-Type": "application/json",
        }
        project = cal.google_quota_project()
        if not project:
            raise RuntimeError("Google quota project unavailable")
        headers["x-goog-user-project"] = project
        status, body = capture.guide_once(text, style, headers, retries=0)
        raw = MEDIA / "short01-final-google-response.bin"
        with raw.open("xb") as output:
            output.write(body)
        receipt: dict[str, object] = {
            "at": now(),
            "http_status": status,
            "raw_body_path": str(raw.relative_to(REPO)),
            "raw_body_sha256": sha(body),
        }
        if status == 200:
            audio = base64.b64decode(json.loads(body)["audioContent"], validate=True)
            with guide.open("xb") as output:
                output.write(audio)
            receipt["guide"] = wav_metadata(guide)
        else:
            receipt["error"] = body.decode(errors="replace").replace(headers["Authorization"], "[REDACTED]")[:4000]
        save(BASE / "GUIDE-RECEIPT.json", receipt)
    else:
        previous = json.loads((BASE / "GUIDE-RECEIPT.json").read_text())
        assert previous["http_status"] == 200
        assert previous["guide"]["sha256"] == sha(guide.read_bytes())
        api_key = cal.read_dotenv_key("ELEVENLABS_API_KEY")
        status, body = capture.transfer_once(guide, api_key)
        raw = MEDIA / "short01-final-elevenlabs-response.pcm"
        with raw.open("xb") as output:
            output.write(body)
        receipt = {
            "at": now(),
            "http_status": status,
            "raw_body_path": str(raw.relative_to(REPO)),
            "raw_body_sha256": sha(body),
            "guide_sha256": sha(guide.read_bytes()),
        }
        if status == 200:
            assert not final.exists()
            cal.wav_from_pcm(body, cal.TRANSFER_OUTPUT_RATE_HZ, final)
            receipt["voice"] = wav_metadata(final)
            receipt["transfer_duration_delta_seconds"] = receipt["voice"]["duration_seconds"] - previous["guide"]["duration_seconds"]
        else:
            receipt["error"] = body.decode(errors="replace").replace(api_key, "[REDACTED]")[:4000]
        save(BASE / "TRANSFER-RECEIPT.json", receipt)
    print(json.dumps(receipt))
    if status != 200:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
