#!/usr/bin/env python3
"""Plain two-stage narration calibration executor.

Casting-loop tooling, NOT governed runtime. It exists so voice calibration can
iterate quickly; it deliberately has no authorization latches, consumption
records, or evidence chain. Apply the governed runtime
(`oe_narration.voice_transfer`) at N4B/production capture, where provenance
matters.

Stage 1 (guide):    Google Cloud TTS `gemini-2.5-pro-tts` performs the read
                    using a separate acting-direction prompt.
Stage 2 (transfer): ElevenLabs Voice Changer moves that performance onto the
                    Original C identity.

Request shapes match the proven adapters that produced candidate A/B.

Unlike the governed runtime this has no 50s / 4.8MB ceiling and is not welded
to one passage. It also always drains the full response body before doing
anything else -- the 2026-08-26 loss was a confirmed HTTP 200 discarded with
the body still streaming.

Nothing here calls a provider without --execute.

Usage:
  calibrate.py guide    --text P.txt --style S.json --out-dir D [--n 2] [--execute]
  calibrate.py transfer --guide G.wav --out-dir D [--execute]
  calibrate.py chain    --text P.txt --style S.json --out-dir D [--n 1] [--execute]
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request
import uuid
import wave

# --- frozen provider configuration (matches the proven adapters) -------------

GUIDE_ENDPOINT = "https://us-texttospeech.googleapis.com/v1/text:synthesize"
GUIDE_MODEL = "gemini-2.5-pro-tts"
GUIDE_VOICE = "Achird"
GUIDE_LANGUAGE = "en-US"
GUIDE_AUDIO_ENCODING = "LINEAR16"
GUIDE_SAMPLE_RATE_HZ = 24_000

TRANSFER_VOICE_ID = "scMbPZwQjr40V1MzL3Nj"  # Original C
TRANSFER_MODEL = "eleven_multilingual_sts_v2"
TRANSFER_ENDPOINT = f"https://api.elevenlabs.io/v1/speech-to-speech/{TRANSFER_VOICE_ID}"
TRANSFER_OUTPUT_FORMAT = "pcm_48000"
TRANSFER_OUTPUT_RATE_HZ = 48_000
TRANSFER_SEED = 2026082501
TRANSFER_VOICE_SETTINGS = {
    "similarity_boost": 0.8,
    "speed": 1.0,
    "stability": 0.4,
    "style": 0.0,
    "use_speaker_boost": True,
}

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
DOTENV = REPO_ROOT / ".env"
HTTP_TIMEOUT_SECONDS = 600  # generous: long passages take real provider time


# --- helpers ----------------------------------------------------------------


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def read_dotenv_key(name: str) -> str:
    """Read one key from the repo .env. The value is never logged."""
    if os.environ.get(name):
        return os.environ[name]
    if not DOTENV.is_file():
        sys.exit(f"error: {name} not in environment and {DOTENV} is missing")
    for line in DOTENV.read_text(encoding="utf-8").splitlines():
        if line.startswith(f"{name}="):
            value = line.split("=", 1)[1].strip().strip('"').strip("'")
            if value:
                return value
    sys.exit(f"error: {name} not found in environment or {DOTENV}")


def google_access_token() -> str:
    """Mint an ADC access token via gcloud. The token is never logged."""
    try:
        out = subprocess.run(
            ["gcloud", "auth", "application-default", "print-access-token", "--quiet"],
            capture_output=True,
            check=True,
            timeout=60,
            env={
                "PATH": os.environ.get("PATH", ""),
                "HOME": os.environ.get("HOME", ""),
                "CLOUDSDK_CORE_DISABLE_PROMPTS": "1",
            },
        )
    except FileNotFoundError:
        sys.exit("error: gcloud not on PATH")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"error: gcloud token failed (rc={exc.returncode}); run: gcloud auth application-default login")
    return out.stdout.decode("utf-8").strip()


def google_quota_project() -> str | None:
    """Resolve the ADC quota project.

    texttospeech.googleapis.com refuses ADC without an x-goog-user-project
    header and reports it as a confusing SERVICE_DISABLED 403. The
    authoritative value lives in the ADC file itself; `gcloud config
    get-value project` is often unset even when ADC is correct.
    """
    project = os.environ.get("GOOGLE_CLOUD_QUOTA_PROJECT")
    if project:
        return project
    adc = pathlib.Path(
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        or pathlib.Path.home() / ".config/gcloud/application_default_credentials.json"
    )
    if adc.is_file():
        try:
            value = json.loads(adc.read_text(encoding="utf-8")).get("quota_project_id")
            if value:
                return str(value)
        except (OSError, ValueError):
            pass
    try:
        out = subprocess.run(
            ["gcloud", "config", "get-value", "project", "--quiet"],
            capture_output=True, check=True, timeout=30,
        )
    except Exception:
        return None
    return out.stdout.decode("utf-8").strip() or None


def post(url: str, data: bytes, headers: dict[str, str]) -> tuple[int, bytes]:
    """POST and ALWAYS fully drain the response body before returning.

    The 2026-08-26 failure was a confirmed HTTP 200 whose body was still
    streaming when containment killed the worker. Read to EOF, then decide.
    """
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def wav_from_pcm(pcm: bytes, rate: int, path: pathlib.Path) -> None:
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(pcm)


def probe(path: pathlib.Path) -> dict:
    info: dict = {"bytes": path.stat().st_size, "sha256": sha256_bytes(path.read_bytes())}
    try:
        with wave.open(str(path)) as handle:
            info |= {
                "sample_rate_hz": handle.getframerate(),
                "channels": handle.getnchannels(),
                "sample_width_bits": handle.getsampwidth() * 8,
                "duration_seconds": round(handle.getnframes() / handle.getframerate(), 3),
            }
    except Exception:
        pass
    return info


def load_style(path: pathlib.Path) -> tuple[str, str, dict[str, str]]:
    """Return (style_instructions, label, pronunciation_aliases)."""
    raw = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        record = json.loads(raw)
        text = record.get("style_instructions")
        if not isinstance(text, str) or not text:
            sys.exit(f"error: {path} has no style_instructions field")
        aliases = (record.get("pronunciation_policy") or {}).get("aliases") or {}
        return text, record.get("candidate_id") or path.stem, aliases
    return raw.strip(), path.stem, {}


def compose_style(style: str, aliases: dict[str, str], passage: str) -> str:
    """Append only the aliases whose display form actually occurs in this passage.

    Naming a token in the prompt raises its salience -- that is what
    over-stressed the target word in the original candidate C audition. So an
    alias is attached only where it is genuinely needed.
    """
    if not aliases:
        return style
    applicable = [
        f'"{display}" as "{spoken}"'
        for display, spoken in sorted(aliases.items())
        if re.search(rf"(?<![A-Za-z0-9]){re.escape(display)}(?![A-Za-z0-9])", passage)
    ]
    if not applicable:
        return style
    tail = "Pronounce " + "; ".join(applicable) + "."
    return f"{style.rstrip()} {tail}"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "passage"


# gemini-2.5-pro-tts returns HTTP 502 above roughly 75 seconds of generated
# audio. Measured 2026-08-28: 1,360 chars -> 73.7s OK; 1,479 chars -> 502,
# deterministic on retry. Keep a margin.
MAX_GUIDE_CHARS = 1_250

# Split after . ? ! followed by whitespace + an opening character, but never
# when the period is part of a number (443.6) or a single initial.
_SENTENCE_END = re.compile(r'(?<![0-9])(?<![A-Z])([.?!])\s+(?=["“(]?[A-Z0-9])')


def split_sentences(text: str) -> list[str]:
    parts = _SENTENCE_END.sub(lambda m: m.group(1) + "\x00", text).split("\x00")
    return [p.strip() for p in parts if p.strip()]


# Measured 2026-08-30 across Achird and Algieba: ~15.5 characters of locked
# text per second of generated speech, number-dense copy included.
CHARS_PER_SECOND = 15.5

# N4A finding F2: a very short trailing chunk is an independent stochastic
# generation with almost no context, so it lands at its own level and pace.
# M4's 3.65s tail sat 2.1 dB hot against its own mode. Merge such tails back.
MIN_TAIL_SECONDS = 15


def chunk_text(text: str, max_chars: int = MAX_GUIDE_CHARS) -> list[str]:
    """Pack whole sentences into chunks. Never splits a sentence.

    A trailing chunk shorter than MIN_TAIL_SECONDS of expected speech is merged
    into the previous chunk, accepting a slightly over-target chunk rather than
    emitting an isolated fragment.
    """
    if len(text) <= max_chars:
        return [text]
    chunks: list[str] = []
    current = ""
    for sentence in split_sentences(text):
        if current and len(current) + 1 + len(sentence) > max_chars:
            chunks.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        chunks.append(current)
    if len(chunks) > 1 and len(chunks[-1]) < MIN_TAIL_SECONDS * CHARS_PER_SECOND:
        chunks[-2] = f"{chunks[-2]} {chunks[-1]}"
        chunks.pop()
    return chunks


def concat_wavs(paths: list[pathlib.Path], out_path: pathlib.Path) -> None:
    frames: list[bytes] = []
    params = None
    for path in paths:
        with wave.open(str(path)) as handle:
            params = params or handle.getparams()
            frames.append(handle.readframes(handle.getnframes()))
    with wave.open(str(out_path), "wb") as handle:
        handle.setnchannels(params.nchannels)
        handle.setsampwidth(params.sampwidth)
        handle.setframerate(params.framerate)
        handle.writeframes(b"".join(frames))


def write_manifest(out_dir: pathlib.Path, name: str, record: dict) -> None:
    path = out_dir / f"{name}.manifest.json"
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  manifest -> {path}")


# --- stage 1: Google guide --------------------------------------------------


def guide_body(text: str, style: str, voice: str = GUIDE_VOICE) -> dict:
    return {
        "advancedVoiceOptions": {"enableTextnorm": False},
        "audioConfig": {
            "audioEncoding": GUIDE_AUDIO_ENCODING,
            "sampleRateHertz": GUIDE_SAMPLE_RATE_HZ,
        },
        "input": {"prompt": style, "text": text},
        "voice": {
            "languageCode": GUIDE_LANGUAGE,
            "modelName": GUIDE_MODEL,
            "name": voice,
        },
    }


def run_guide(args) -> list[pathlib.Path]:
    text = pathlib.Path(args.text).read_text(encoding="utf-8").strip()
    base_style, label, aliases = load_style(pathlib.Path(args.style))
    style = compose_style(base_style, aliases, text)
    stem = args.name or f"{slugify(pathlib.Path(args.text).stem)}.{slugify(label)}"
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    body = compact_json(guide_body(text, style, args.voice))
    print(f"[guide] {GUIDE_MODEL} / {args.voice} / {GUIDE_LANGUAGE}")
    print(f"  passage : {args.text} ({len(text)} chars, sha {sha256_bytes(text.encode())[:12]})")
    print(f"  style   : {label} ({len(style)} chars, sha {sha256_bytes(style.encode())[:12]})")
    print(f"  body    : {len(body)} bytes, sha {sha256_bytes(body)[:12]}")
    print(f"  outputs : {args.n} -> {out_dir}/{stem}.NN.wav")

    if not args.execute:
        print("  DRY RUN - no call made. Re-run with --execute to generate.")
        return []

    token = google_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"}
    project = google_quota_project()
    if project:
        headers["x-goog-user-project"] = project

    produced: list[pathlib.Path] = []
    for index in range(1, args.n + 1):
        status, payload = post(GUIDE_ENDPOINT, body, headers)
        if status != 200:
            print(f"  call {index}: HTTP {status}\n{payload[:600].decode('utf-8', 'replace')}")
            break
        audio = base64.b64decode(json.loads(payload)["audioContent"])
        path = out_dir / f"{stem}.{index:02d}.wav"
        path.write_bytes(audio)
        os.chmod(path, 0o600)
        info = probe(path)
        print(f"  call {index}: HTTP 200 -> {path.name}  "
              f"{info.get('duration_seconds')}s @ {info.get('sample_rate_hz')}Hz  sha {info['sha256'][:12]}")
        produced.append(path)
        write_manifest(out_dir, path.stem, {
            "stage": "guide",
            "provider": "google_cloud_text_to_speech",
            "model": GUIDE_MODEL, "voice": args.voice, "language": GUIDE_LANGUAGE,
            "style_label": label,
            "style_sha256": sha256_bytes(style.encode()),
            "passage_path": str(args.text),
            "passage_sha256": sha256_bytes(text.encode()),
            "request_body_sha256": sha256_bytes(body),
            "output": info | {"path": str(path)},
        })
    return produced


# --- stage 2: ElevenLabs Voice Changer --------------------------------------


def multipart(fields: dict[str, str], filename: str, payload: bytes) -> tuple[bytes, str]:
    boundary = uuid.uuid4().hex
    chunks: list[bytes] = []
    for key, value in fields.items():
        chunks.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n".encode("utf-8")
        )
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    chunks.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"audio\"; filename=\"{filename}\"\r\n"
        f"Content-Type: {content_type}\r\n\r\n".encode("utf-8")
    )
    chunks.append(payload)
    chunks.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def run_transfer(args) -> pathlib.Path | None:
    guide = pathlib.Path(args.guide)
    if not guide.is_file():
        sys.exit(f"error: guide not found: {guide}")
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.name or f"{guide.stem}.saved-c"
    out_path = out_dir / f"{stem}.wav"

    source = probe(guide)
    settings = dict(TRANSFER_VOICE_SETTINGS)
    if args.stability is not None:
        settings["stability"] = args.stability
    if args.similarity is not None:
        settings["similarity_boost"] = args.similarity
    if args.style_amount is not None:
        settings["style"] = args.style_amount

    fields = {
        "model_id": TRANSFER_MODEL,
        "remove_background_noise": "false",
        "seed": str(TRANSFER_SEED),
        "voice_settings": json.dumps(settings, sort_keys=True),
        "file_format": "other",
    }

    print(f"[transfer] Voice Changer -> Original C ({TRANSFER_VOICE_ID})")
    print(f"  guide    : {guide.name}  {source.get('duration_seconds')}s @ "
          f"{source.get('sample_rate_hz')}Hz  sha {source['sha256'][:12]}")
    print(f"  model    : {TRANSFER_MODEL}  seed {TRANSFER_SEED}")
    print(f"  settings : {json.dumps(settings, sort_keys=True)}")
    print(f"  output   : {out_path}  (pcm_48000 -> wav)")

    if not args.execute:
        print("  DRY RUN - no call made. Re-run with --execute to generate.")
        return None

    payload, content_type = multipart(fields, guide.name, guide.read_bytes())
    url = f"{TRANSFER_ENDPOINT}?output_format={TRANSFER_OUTPUT_FORMAT}&enable_logging=true"
    status, body = post(url, payload, {
        "xi-api-key": read_dotenv_key("ELEVENLABS_API_KEY"),
        "Content-Type": content_type,
        "Accept": "*/*",
    })
    if status != 200:
        print(f"  HTTP {status}\n{body[:600].decode('utf-8', 'replace')}")
        return None

    # Body fully drained above; only now write it out.
    wav_from_pcm(body, TRANSFER_OUTPUT_RATE_HZ, out_path)
    os.chmod(out_path, 0o600)
    info = probe(out_path)
    print(f"  HTTP 200 -> {out_path.name}  {info.get('duration_seconds')}s @ "
          f"{info.get('sample_rate_hz')}Hz  sha {info['sha256'][:12]}  ({len(body)} pcm bytes)")
    write_manifest(out_dir, out_path.stem, {
        "stage": "transfer",
        "provider": "elevenlabs",
        "endpoint": TRANSFER_ENDPOINT,
        "model": TRANSFER_MODEL,
        "target_voice_id": TRANSFER_VOICE_ID,
        "seed": TRANSFER_SEED,
        "voice_settings": settings,
        "output_format": TRANSFER_OUTPUT_FORMAT,
        "source_guide": source | {"path": str(guide)},
        "output": info | {"path": str(out_path)},
    })
    return out_path


def run_mode(args) -> None:
    """One calibration mode end to end, chunked to the provider ceiling.

    Every chunk uses byte-identical style, model, voice, settings and seed;
    only the text range differs. Chunk transfers are concatenated into one
    per-mode master for the continuity listen.
    """
    text = pathlib.Path(args.text).read_text(encoding="utf-8").strip()
    base_style, label, aliases = load_style(pathlib.Path(args.style))
    style = compose_style(base_style, aliases, text)
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.name or slugify(pathlib.Path(args.text).stem)
    chunks = chunk_text(text, args.max_chars)

    print(f"[mode] {stem}  {len(text)} chars -> {len(chunks)} chunk(s) at <={args.max_chars}")
    for index, chunk in enumerate(chunks, 1):
        print(f"  chunk {index}: {len(chunk)} chars  sha {sha256_bytes(chunk.encode())[:12]}")
    if not args.execute:
        print("  DRY RUN - no calls made. Re-run with --execute.")
        return

    token = google_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"}
    project = google_quota_project()
    if project:
        headers["x-goog-user-project"] = project
    api_key = read_dotenv_key("ELEVENLABS_API_KEY")

    settings = dict(TRANSFER_VOICE_SETTINGS)
    for key, value in (("stability", args.stability), ("similarity_boost", args.similarity),
                       ("style", args.style_amount)):
        if value is not None:
            settings[key] = value

    transfers: list[pathlib.Path] = []
    records: list[dict] = []
    for index, chunk in enumerate(chunks, 1):
        body = compact_json(guide_body(chunk, style, args.voice))
        guide_path = out_dir / f"{stem}.c{index:02d}.guide.wav"
        transfer_path = out_dir / f"{stem}.c{index:02d}.saved-c.wav"

        # Resume: gemini-2.5-pro-tts returns transient 502s. Never re-bill a
        # chunk that already has both artifacts on disk.
        if guide_path.is_file() and transfer_path.is_file() and not args.force:
            guide_info, transfer_info = probe(guide_path), probe(transfer_path)
            print(f"  chunk {index}: reused  guide {guide_info['duration_seconds']}s -> "
                  f"transfer {transfer_info['duration_seconds']}s")
            transfers.append(transfer_path)
            records.append({
                "chunk": index, "chars": len(chunk), "reused": True,
                "text_sha256": sha256_bytes(chunk.encode()),
                "guide_request_body_sha256": sha256_bytes(body),
                "guide": guide_info | {"path": str(guide_path)},
                "transfer": transfer_info | {"path": str(transfer_path)},
            })
            continue

        status, payload = post(GUIDE_ENDPOINT, body, headers)
        for attempt in range(args.retries):
            if status != 502:
                break
            print(f"  chunk {index} guide: HTTP 502, retry {attempt + 1}/{args.retries}")
            status, payload = post(GUIDE_ENDPOINT, body, headers)
        if status != 200:
            print(f"  chunk {index} guide: HTTP {status} - aborting mode "
                  f"(completed chunks are kept; re-run to resume)")
            return
        guide_path.write_bytes(base64.b64decode(json.loads(payload)["audioContent"]))
        os.chmod(guide_path, 0o600)
        guide_info = probe(guide_path)

        multipart_body, content_type = multipart(
            {"model_id": TRANSFER_MODEL, "remove_background_noise": "false",
             "seed": str(TRANSFER_SEED), "voice_settings": json.dumps(settings, sort_keys=True),
             "file_format": "other"},
            guide_path.name, guide_path.read_bytes(),
        )
        status, audio = post(
            f"{TRANSFER_ENDPOINT}?output_format={TRANSFER_OUTPUT_FORMAT}&enable_logging=true",
            multipart_body,
            {"xi-api-key": api_key, "Content-Type": content_type, "Accept": "*/*"},
        )
        if status != 200:
            print(f"  chunk {index} transfer: HTTP {status} - aborting mode")
            return
        wav_from_pcm(audio, TRANSFER_OUTPUT_RATE_HZ, transfer_path)
        os.chmod(transfer_path, 0o600)
        transfer_info = probe(transfer_path)
        print(f"  chunk {index}: guide {guide_info['duration_seconds']}s -> "
              f"transfer {transfer_info['duration_seconds']}s  sha {transfer_info['sha256'][:12]}")
        transfers.append(transfer_path)
        records.append({
            "chunk": index,
            "chars": len(chunk),
            "text_sha256": sha256_bytes(chunk.encode()),
            "guide_request_body_sha256": sha256_bytes(body),
            "guide": guide_info | {"path": str(guide_path)},
            "transfer": transfer_info | {"path": str(transfer_path)},
        })

    master = out_dir / f"{stem}.saved-c.master.wav"
    concat_wavs(transfers, master)
    os.chmod(master, 0o600)
    master_info = probe(master)
    print(f"  master : {master.name}  {master_info['duration_seconds']}s  sha {master_info['sha256'][:12]}")
    write_manifest(out_dir, master.stem, {
        "stage": "n4a_calibration_mode",
        "mode": stem,
        "passage_path": str(args.text),
        "passage_sha256": sha256_bytes(text.encode()),
        "style_label": label,
        "style_base_sha256": sha256_bytes(base_style.encode()),
        "style_composed_sha256": sha256_bytes(style.encode()),
        "style_composed": style,
        "chunk_count": len(chunks),
        "max_chars": args.max_chars,
        "guide": {"provider": "google_cloud_text_to_speech", "model": GUIDE_MODEL,
                  "voice": args.voice, "language": GUIDE_LANGUAGE,
                  "sample_rate_hz": GUIDE_SAMPLE_RATE_HZ, "encoding": GUIDE_AUDIO_ENCODING},
        "transfer": {"provider": "elevenlabs", "model": TRANSFER_MODEL,
                     "target_voice_id": TRANSFER_VOICE_ID, "seed": TRANSFER_SEED,
                     "voice_settings": settings, "output_format": TRANSFER_OUTPUT_FORMAT},
        "chunks": records,
        "master": master_info | {"path": str(master)},
    })


def run_chain(args) -> None:
    for guide in run_guide(args):
        transfer_args = argparse.Namespace(
            guide=str(guide), out_dir=args.out_dir, name=None, execute=args.execute,
            stability=args.stability, similarity=args.similarity, style_amount=args.style_amount,
        )
        run_transfer(transfer_args)


# --- cli --------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p, *, needs_text: bool) -> None:
        if needs_text:
            p.add_argument("--text", required=True, help="passage text file (exact locked words)")
            p.add_argument("--style", required=True, help="style-instructions .json record or plain .txt prompt")
            p.add_argument("--n", type=int, default=1, help="number of stochastic guide generations")
            p.add_argument("--voice", default=GUIDE_VOICE, help="Google guide voice (performance carrier only; narrator identity comes from the transfer)")
        p.add_argument("--out-dir", required=True)
        p.add_argument("--name", default=None, help="output stem override")
        p.add_argument("--execute", action="store_true", help="actually call the provider (spends credits)")

    def transfer_opts(p) -> None:
        p.add_argument("--stability", type=float, default=None)
        p.add_argument("--similarity", type=float, default=None)
        p.add_argument("--style-amount", type=float, default=None, dest="style_amount")

    g = sub.add_parser("guide", help="stage 1: Google acted guide")
    common(g, needs_text=True)

    t = sub.add_parser("transfer", help="stage 2: Voice Changer onto Original C")
    t.add_argument("--guide", required=True)
    common(t, needs_text=False)
    transfer_opts(t)

    c = sub.add_parser("chain", help="both stages")
    common(c, needs_text=True)
    transfer_opts(c)

    m = sub.add_parser("mode", help="one calibration mode, chunked and joined")
    common(m, needs_text=True)
    transfer_opts(m)
    m.add_argument("--max-chars", type=int, default=MAX_GUIDE_CHARS, dest="max_chars")
    m.add_argument("--retries", type=int, default=2, help="retries on transient provider 502")
    m.add_argument("--force", action="store_true", help="regenerate chunks that already exist")

    args = parser.parse_args()
    if args.command == "guide":
        run_guide(args)
    elif args.command == "transfer":
        run_transfer(args)
    elif args.command == "mode":
        run_mode(args)
    else:
        run_chain(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
