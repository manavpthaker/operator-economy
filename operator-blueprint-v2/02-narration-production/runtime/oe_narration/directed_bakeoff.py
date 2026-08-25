"""Execute the frozen ElevenLabs directed bakeoff, and nothing broader.

The v0.3 bakeoff compiler is the authority for words, tags, paragraph
boundaries, voice, model, settings, destinations, and fallback requests.  This
module is deliberately only a transport: it recompiles that contract, requires
an exact active authorization, consumes it before the first network call, and
writes immutable local evidence.

It cannot generate an episode, mutate a voice, upload media, follow redirects,
retry a failed request, or silently substitute a lossy response.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO

from .audio import inspect_audio
from .bakeoff import (
    ELEVEN_ALLOWED_TAGS,
    dry_run_provider_bakeoff,
    validate_provider_action_authorization,
)
from .core import (
    ValidationError,
    read_canonical_w,
    read_json,
    sha256_bytes,
    sha256_file,
)


API_ORIGIN = "https://api.elevenlabs.io"
AUTHORIZATION_SCOPE = "elevenlabs_calibration"
CONSUMPTION_SCHEMA = "oe-provider-authorization-consumption-v1"
RUN_RECEIPT_SCHEMA = "oe-elevenlabs-directed-bakeoff-run-v1"
FAILURE_RECEIPT_SCHEMA = "oe-elevenlabs-directed-bakeoff-failure-v1"
PCM_FAILURE_SCHEMA = "oe-pcm-capability-failure-v1"
PCM_REJECTION_SCHEMA = "oe-pcm-capability-rejection-v1"

# These are deliberately calibration-sized ceilings independent of whatever a
# malformed authorization might claim.  The frozen control has two passages,
# two candidates per passage, and one possible capability fallback per call.
MAX_PRIMARY_REQUESTS = 4
MAX_PASSAGES = 2
MAX_CALLS = 8
MAX_OUTPUTS = 4
MAX_AUTHORIZED_CHARACTERS = 20_000
MAX_RESPONSE_BYTES = 100_000_000
MAX_ERROR_RESPONSE_BYTES = 1_000_000
MAX_SEED = 4_294_967_295

_REQUEST_KEYS = frozenset(
    {
        "request_id",
        "provider",
        "provider_id",
        "passage_id",
        "candidate_ids",
        "method",
        "url_path",
        "query",
        "required_header_names",
        "start_token",
        "end_token",
        "spoken_text_sha256",
        "tag_insertions",
        "provider_text_sha256",
        "provider_text_character_count",
        "request_body",
        "request_body_serialization",
        "request_body_sha256",
        "planned_call_count",
        "planned_output_count",
        "estimated_billable_character_count",
        "estimated_public_rate_usd_per_1000_characters",
        "estimated_public_rate_cost_usd",
        "destinations",
        "execution_ready",
        "blockers",
        "fallback_request",
    }
)
_FALLBACK_KEYS = frozenset(
    {
        "enabled",
        "method",
        "url_path",
        "query",
        "request_body",
        "request_body_sha256",
        "destination",
        "planned_additional_call_count",
        "estimated_additional_billable_character_count",
        "estimated_additional_public_rate_cost_usd",
        "requires",
        "execution_ready",
    }
)
_BODY_KEYS = frozenset({"text", "model_id", "seed", "voice_settings"})
_VOICE_SETTING_KEYS = frozenset({"stability", "similarity_boost", "style"})
_PCM_MIMES = frozenset({"application/octet-stream", "audio/l16", "audio/pcm"})
_MP3_MIMES = frozenset({"audio/mp3", "audio/mpeg"})
_REQUEST_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_BRACKET_DIRECTION_RE = re.compile(r"\[[^\]\r\n]+\]")
_REQUEST_ID_HEADERS = (
    "request-id",
    "x-request-id",
    "xi-request-id",
    "history-item-id",
)


@dataclass(frozen=True)
class DirectedBakeoffContract:
    """Validated, credential-free execution contract."""

    authorization_path: Path
    artifact_root: Path
    authorization: dict[str, Any]
    dry_run: dict[str, Any]
    requests: tuple[dict[str, Any], ...]
    canonical_tokens: tuple[str, ...]
    fixed_seeds: dict[str, int]
    seed_map_sha256: str
    consumption_path: Path
    run_receipt_path: Path
    failure_receipt_path: Path

    def public_dict(self) -> dict[str, Any]:
        return {
            "valid": True,
            "scope": AUTHORIZATION_SCOPE,
            "authorization_sha256": sha256_file(self.authorization_path),
            "compiled_dry_run_sha256": sha256_file(
                self.artifact_root / "compiled" / "provider-bakeoff-dry-run.json"
            ),
            "request_set_sha256": self.dry_run["request_set_sha256"],
            "request_ids": [request["request_id"] for request in self.requests],
            "primary_request_count": len(self.requests),
            "passage_count": len({request["passage_id"] for request in self.requests}),
            "fixed_seeds": dict(self.fixed_seeds),
            "seed_map_sha256": self.seed_map_sha256,
            "network_called": False,
            "credentials_accessed": False,
            "audio_files_created": 0,
            "creative_approved": False,
            "step3_authorized": False,
        }


@dataclass(frozen=True)
class _HttpResponse:
    data: bytes
    mime_type: str
    headers: dict[str, str]
    provider_identifiers: dict[str, str]
    character_cost: dict[str, Any]


class _HttpFailure(Exception):
    """Credential-free, bounded evidence about one failed POST."""

    def __init__(
        self,
        code: str,
        *,
        http_status: int | None = None,
        provider_code: str | None = None,
        response_sha256: str | None = None,
        pcm_capability_unavailable: bool = False,
        provider_identifiers: dict[str, str] | None = None,
        character_cost: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.http_status = http_status
        self.provider_code = provider_code
        self.response_sha256 = response_sha256
        self.pcm_capability_unavailable = pcm_capability_unavailable
        self.provider_identifiers = provider_identifiers or {}
        self.character_cost = character_cost or {
            "header": "character-cost",
            "present": False,
            "value": None,
            "unit": "provider_reported_character_cost",
        }
        super().__init__(code)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Never forward the ElevenLabs credential to a redirected endpoint."""

    def redirect_request(  # type: ignore[override]
        self,
        req: urllib.request.Request,
        fp: BinaryIO,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _receipt_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _exclusive_write(path: Path, data: bytes) -> None:
    """Create one immutable artifact without following the final symlink."""

    path.parent.mkdir(parents=True, exist_ok=True)
    _reject_symlink_components(path.parent, path, "immutable artifact")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise ValidationError(f"refusing to overwrite immutable artifact: {path}") from exc
    except OSError as exc:
        raise ValidationError(f"cannot create immutable directed-bakeoff artifact: {path}") from exc


def _reject_symlink_components(root: Path, candidate: Path, label: str) -> None:
    """Reject every existing symlink from an authorized root to a candidate."""

    if root.is_symlink():
        raise ValidationError(f"{label} root may not be a symlink")
    try:
        resolved_root = root.resolve(strict=True)
        relative = candidate.relative_to(root)
    except (OSError, ValueError) as exc:
        raise ValidationError(f"{label} escapes its authorized root") from exc
    current = root
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise ValidationError(f"{label} may not traverse a symlink")
        if current.exists() and current != candidate and not current.is_dir():
            raise ValidationError(f"{label} parent is not a directory")
    try:
        resolved_candidate = candidate.resolve(strict=False)
    except OSError as exc:
        raise ValidationError(f"cannot safely resolve {label}") from exc
    if not resolved_candidate.is_relative_to(resolved_root):
        raise ValidationError(f"{label} escapes its authorized root")


def _safe_new_relative(
    root: Path,
    relative_value: Any,
    label: str,
    *,
    prefix: str,
    suffix: str,
) -> Path:
    if not isinstance(relative_value, str) or not relative_value:
        raise ValidationError(f"{label} must be a non-empty relative path")
    relative = Path(relative_value)
    if relative.is_absolute() or not relative.parts or relative.parts[0] != prefix:
        raise ValidationError(f"{label} must remain under {prefix}/")
    if any(part in {"", ".", "..", "~"} for part in relative.parts):
        raise ValidationError(f"{label} contains an unsafe path component")
    if relative.suffix.lower() != suffix:
        raise ValidationError(f"{label} must end in {suffix}")
    candidate = root / relative
    _reject_symlink_components(root, candidate, label)
    if candidate.exists():
        raise ValidationError(f"{label} already exists; overwrite is forbidden")
    return candidate


def _safe_consumption_path(authorization_path: Path, value: Any) -> Path:
    root = authorization_path.parent
    if not isinstance(value, str) or not value:
        raise ValidationError("consumption.record_path must be a non-empty relative path")
    relative = Path(value)
    if relative.is_absolute() or any(part in {"", ".", "..", "~"} for part in relative.parts):
        raise ValidationError("consumption.record_path is unsafe")
    # Use one canonical spelling of macOS' /var -> /private/var path so later
    # relative-path receipts cannot disagree with the resolved authorization.
    resolved_root = root.resolve(strict=True)
    candidate = resolved_root / relative
    _reject_symlink_components(resolved_root, candidate, "consumption.record_path")
    if candidate.exists():
        raise ValidationError("authorization consumption record already exists")
    return candidate


def _strict_keys(value: Any, allowed: frozenset[str], label: str) -> None:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ValidationError(f"{label} contains unsupported keys: {', '.join(unknown)}")


def _resolve_canonical_w(envelope_path: Path, envelope: dict[str, Any], fixtures_root: Path) -> Path:
    binding = envelope.get("canonical_w")
    if not isinstance(binding, dict) or not isinstance(binding.get("path"), str):
        raise ValidationError("performance envelope lacks canonical_w.path")
    declared = Path(binding["path"])
    if declared.is_absolute():
        raise ValidationError("canonical_w.path must remain portable and relative")
    try:
        path = (envelope_path.parent / declared).resolve(strict=True)
        root = fixtures_root.resolve(strict=True)
    except OSError as exc:
        raise ValidationError("cannot resolve canonical W") from exc
    if not path.is_relative_to(root) or not path.is_file() or path.is_symlink():
        raise ValidationError("canonical W must be a regular file under the narration fixtures root")
    return path


def _frozen_seed_map(
    plan: dict[str, Any], requests: list[dict[str, Any]]
) -> tuple[dict[str, int], str]:
    """Read seeds only from the exact plan and compare to hash-bound bodies."""

    providers = plan.get("providers")
    if not isinstance(providers, list):
        raise ValidationError("provider bakeoff plan lacks providers")
    eleven = next(
        (
            provider
            for provider in providers
            if isinstance(provider, dict) and provider.get("provider") == "elevenlabs"
        ),
        None,
    )
    plan_requests = eleven.get("requests") if isinstance(eleven, dict) else None
    if not isinstance(plan_requests, list):
        raise ValidationError("provider bakeoff plan lacks frozen ElevenLabs requests")
    plan_by_id = {
        item.get("request_id"): item
        for item in plan_requests
        if isinstance(item, dict) and isinstance(item.get("request_id"), str)
    }
    request_ids = [request["request_id"] for request in requests]
    if set(plan_by_id) != set(request_ids) or len(plan_by_id) != len(plan_requests):
        raise ValidationError("frozen seed plan must exactly cover compiled request_ids")
    normalized: dict[str, int] = {}
    for request in requests:
        request_id = request["request_id"]
        seed = plan_by_id[request_id].get("fixed_seed")
        body_seed = request.get("request_body", {}).get("seed")
        if seed != body_seed:
            raise ValidationError(
                f"compiled seed for {request_id} does not equal the exact frozen plan seed"
            )
        normalized[request_id] = seed
    for request_id, seed in normalized.items():
        if not isinstance(seed, int) or isinstance(seed, bool):
            raise ValidationError("frozen fixed_seed values must be integers")
        if seed < 0 or seed > MAX_SEED:
            raise ValidationError(f"fixed seed for {request_id} is outside 0..{MAX_SEED}")

    # The control uses candidate A and B across two passages.  Reusing the A
    # seed and the B seed makes the comparison intentional rather than random.
    by_suffix: dict[str, set[int]] = {"A": set(), "B": set()}
    for request_id, seed in normalized.items():
        suffix = request_id.rsplit("-", 1)[-1]
        if suffix not in by_suffix:
            raise ValidationError("fixed-seed bakeoff request_ids must end in -A or -B")
        by_suffix[suffix].add(seed)
    if any(len(values) != 1 for values in by_suffix.values()):
        raise ValidationError("each candidate letter must reuse one fixed seed across passages")
    if next(iter(by_suffix["A"])) == next(iter(by_suffix["B"])):
        raise ValidationError("candidate A and B must use different fixed seeds")
    ordered = {request_id: normalized[request_id] for request_id in request_ids}
    return ordered, sha256_bytes(_json_bytes(ordered))


def _validate_compiled_request(request: dict[str, Any], tokens: list[str]) -> None:
    request_id = request.get("request_id")
    if not isinstance(request_id, str) or _REQUEST_ID_RE.fullmatch(request_id) is None:
        raise ValidationError("compiled ElevenLabs request_id is unsafe")
    _strict_keys(request, _REQUEST_KEYS, f"request {request_id}")
    if request.get("provider") != "elevenlabs" or request.get("method") != "POST":
        raise ValidationError(f"request {request_id} is not an approved ElevenLabs POST")
    if request.get("planned_call_count") != 1 or request.get("planned_output_count") != 1:
        raise ValidationError(f"request {request_id} must represent exactly one call and one output")
    if request.get("execution_ready") is not False:
        raise ValidationError(f"compiled dry run {request_id} may not self-authorize execution")
    if request.get("required_header_names") != ["Content-Type", "xi-api-key"]:
        raise ValidationError(f"request {request_id} header contract changed")
    url_path = request.get("url_path")
    if (
        not isinstance(url_path, str)
        or not url_path.startswith("/v1/text-to-speech/")
        or "?" in url_path
        or "#" in url_path
        or ".." in url_path
    ):
        raise ValidationError(f"request {request_id} URL path is not the frozen TTS endpoint")
    if request.get("query") != {"output_format": "pcm_48000"}:
        raise ValidationError(f"request {request_id} must request pcm_48000 first")

    body = request.get("request_body")
    _strict_keys(body, _BODY_KEYS, f"request {request_id}.request_body")
    assert isinstance(body, dict)
    if body.get("model_id") != "eleven_v3":
        raise ValidationError(f"request {request_id} model drifted")
    seed = body.get("seed")
    if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0 or seed > MAX_SEED:
        raise ValidationError(f"request {request_id} lacks a valid frozen fixed seed")
    _strict_keys(
        body.get("voice_settings"),
        _VOICE_SETTING_KEYS,
        f"request {request_id}.voice_settings",
    )
    text = body.get("text")
    if not isinstance(text, str) or not text or len(text) > 5000:
        raise ValidationError(f"request {request_id} text is empty or exceeds 5000 characters")
    if sha256_bytes(text.encode("utf-8")) != request.get("provider_text_sha256"):
        raise ValidationError(f"request {request_id} provider text hash mismatch")
    if len(text) != request.get("provider_text_character_count"):
        raise ValidationError(f"request {request_id} provider text character count mismatch")
    if sha256_bytes(_json_bytes(body)) != request.get("request_body_sha256"):
        raise ValidationError(f"request {request_id} body hash mismatch")
    found_tags = _BRACKET_DIRECTION_RE.findall(text)
    if any(tag not in ELEVEN_ALLOWED_TAGS for tag in found_tags):
        raise ValidationError(f"request {request_id} contains an unsupported direction tag")
    stripped = text
    for tag in ELEVEN_ALLOWED_TAGS:
        stripped = stripped.replace(tag, " ")
    start, end = request.get("start_token"), request.get("end_token")
    if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool):
        raise ValidationError(f"request {request_id} token range is invalid")
    if start < 0 or end <= start or end > len(tokens):
        raise ValidationError(f"request {request_id} token range is outside canonical W")
    if stripped.split() != tokens[start:end]:
        raise ValidationError(f"request {request_id} changes canonical W after tags are stripped")

    destinations = request.get("destinations")
    if not isinstance(destinations, list) or len(destinations) != 1:
        raise ValidationError(f"request {request_id} must have one immutable PCM destination")
    fallback = request.get("fallback_request")
    _strict_keys(fallback, _FALLBACK_KEYS, f"request {request_id}.fallback_request")
    assert isinstance(fallback, dict)
    if fallback.get("enabled") is not True or fallback.get("execution_ready") is not False:
        raise ValidationError(f"request {request_id} fallback contract changed")
    if fallback.get("method") != "POST" or fallback.get("url_path") != url_path:
        raise ValidationError(f"request {request_id} fallback endpoint changed")
    if fallback.get("query") != {"output_format": "mp3_44100_192"}:
        raise ValidationError(f"request {request_id} fallback must be mp3_44100_192")
    if fallback.get("request_body") != body or fallback.get("request_body_sha256") != request.get(
        "request_body_sha256"
    ):
        raise ValidationError(f"request {request_id} fallback changes the approved body")
    required = set(fallback.get("requires", []))
    expected_requirements = {
        "documented_pcm_capability_rejection_receipt",
        "new_hash_bound_fallback_request",
        "verified_actual_mp3_codec",
        "verified_actual_bitrate_at_least_192000_bps",
        "active_authorization_caps_include_fallback",
    }
    if required != expected_requirements:
        raise ValidationError(f"request {request_id} fallback requirements changed")


def validate_directed_bakeoff_execution(
    authorization_path: Path,
    *,
    now: datetime | None = None,
) -> DirectedBakeoffContract:
    """Validate one active, exact, calibration-only execution without I/O.

    This function never reads a credential, writes a file, or opens the
    network. Seeds are never accepted from the caller: each request must carry
    the seed already frozen in the plan and compiled request body, both of
    which the exact authorization binds by hash.
    """

    authorization_path = Path(authorization_path)
    if authorization_path.is_symlink() or not authorization_path.is_file():
        raise ValidationError("authorization must be a regular, non-symlink file")
    validate_provider_action_authorization(authorization_path, now=now)
    authorization = read_json(authorization_path)
    if authorization.get("scope") != AUTHORIZATION_SCOPE:
        raise ValidationError(f"directed bakeoff requires exact scope {AUTHORIZATION_SCOPE}")
    if authorization.get("target", {}).get("kind") != "fixture":
        raise ValidationError("directed bakeoff is calibration-only and refuses episode targets")

    artifact_root = authorization_path.parent.parent
    if artifact_root.is_symlink() or not artifact_root.is_dir():
        raise ValidationError("provider artifact root must be a regular directory")
    artifact_root = artifact_root.resolve(strict=True)
    fixtures_root = artifact_root.parent.resolve(strict=True)
    envelope_path = artifact_root / "performance-envelope.json"
    plan_path = artifact_root / "provider-bakeoff-plan.json"
    compiled_path = artifact_root / "compiled" / "provider-bakeoff-dry-run.json"
    envelope = read_json(envelope_path)
    canonical_w_path = _resolve_canonical_w(envelope_path, envelope, fixtures_root)
    canonical_tokens = read_canonical_w(canonical_w_path)
    plan = read_json(plan_path)
    expected_dry_run = dry_run_provider_bakeoff(plan_path, envelope_path, canonical_w_path)
    tracked_dry_run = read_json(compiled_path)
    if tracked_dry_run != expected_dry_run:
        raise ValidationError("compiled dry run does not equal deterministic compilation")

    requests = [
        request
        for request in tracked_dry_run.get("requests", [])
        if isinstance(request, dict) and request.get("provider") == "elevenlabs"
    ]
    action_request_ids = authorization.get("action", {}).get("request_ids")
    request_ids = [request.get("request_id") for request in requests]
    if request_ids != action_request_ids:
        raise ValidationError("compiled ElevenLabs requests do not exactly match the authorization")
    if not requests or len(requests) > MAX_PRIMARY_REQUESTS:
        raise ValidationError("directed bakeoff exceeds the calibration primary-request ceiling")
    if len({request.get("passage_id") for request in requests}) > MAX_PASSAGES:
        raise ValidationError("directed bakeoff exceeds the two-passage calibration ceiling")
    for request in requests:
        _validate_compiled_request(request, canonical_tokens)

    totals = tracked_dry_run.get("totals", {}).get("by_provider", {}).get("elevenlabs", {})
    primary = totals.get("primary_lossless", {})
    maximum = totals.get("maximum_with_one_fallback_per_request", {})
    if primary.get("planned_call_count") != len(requests):
        raise ValidationError("compiled primary-call total does not match the request set")
    if maximum.get("max_call_count", MAX_CALLS + 1) > MAX_CALLS:
        raise ValidationError("directed bakeoff exceeds the hard call ceiling")
    if maximum.get("expected_output_count", MAX_OUTPUTS + 1) > MAX_OUTPUTS:
        raise ValidationError("directed bakeoff exceeds the hard output ceiling")
    if maximum.get("max_billable_character_count", MAX_AUTHORIZED_CHARACTERS + 1) > MAX_AUTHORIZED_CHARACTERS:
        raise ValidationError("directed bakeoff exceeds the hard character ceiling")

    normalized_seeds, seed_hash = _frozen_seed_map(plan, requests)
    consumption_path = _safe_consumption_path(
        authorization_path, authorization.get("consumption", {}).get("record_path")
    )
    safe_id = authorization.get("authorization_id")
    if not isinstance(safe_id, str) or _REQUEST_ID_RE.fullmatch(safe_id) is None:
        raise ValidationError("authorization_id is unsafe for immutable receipt names")
    run_receipt_path = _safe_new_relative(
        artifact_root,
        f"receipts/elevenlabs/{safe_id}-directed-bakeoff-run.json",
        "run receipt",
        prefix="receipts",
        suffix=".json",
    )
    failure_receipt_path = _safe_new_relative(
        artifact_root,
        f"receipts/elevenlabs/{safe_id}-directed-bakeoff-failure.json",
        "failure receipt",
        prefix="receipts",
        suffix=".json",
    )

    # Validate every possible output and fallback receipt before consumption.
    seen_destinations: set[Path] = set()
    for request in requests:
        primary_path = _safe_new_relative(
            artifact_root,
            request["destinations"][0],
            f"{request['request_id']} PCM destination",
            prefix="outputs",
            suffix=".pcm",
        )
        fallback_path = _safe_new_relative(
            artifact_root,
            request["fallback_request"]["destination"],
            f"{request['request_id']} MP3 destination",
            prefix="outputs",
            suffix=".mp3",
        )
        fallback_receipt = _safe_new_relative(
            artifact_root,
            f"receipts/elevenlabs/{safe_id}-{request['request_id']}-pcm-capability.json",
            f"{request['request_id']} PCM capability receipt",
            prefix="receipts",
            suffix=".json",
        )
        fallback_rejection = _safe_new_relative(
            artifact_root,
            f"receipts/elevenlabs/{safe_id}-{request['request_id']}-pcm-capability-rejection.json",
            f"{request['request_id']} pre-fallback rejection receipt",
            prefix="receipts",
            suffix=".json",
        )
        for destination in (
            primary_path,
            fallback_path,
            fallback_receipt,
            fallback_rejection,
        ):
            if destination in seen_destinations:
                raise ValidationError("directed bakeoff destinations must be globally unique")
            seen_destinations.add(destination)

    return DirectedBakeoffContract(
        authorization_path=authorization_path.resolve(strict=True),
        artifact_root=artifact_root,
        authorization=authorization,
        dry_run=tracked_dry_run,
        requests=tuple(requests),
        canonical_tokens=tuple(canonical_tokens),
        fixed_seeds=normalized_seeds,
        seed_map_sha256=seed_hash,
        consumption_path=consumption_path,
        run_receipt_path=run_receipt_path,
        failure_receipt_path=failure_receipt_path,
    )


def _header_map(headers: Any) -> dict[str, str]:
    try:
        return {str(key).lower(): str(value) for key, value in headers.items()}
    except (AttributeError, TypeError, ValueError):
        return {}


def _normalized_mime(headers: dict[str, str]) -> str:
    return headers.get("content-type", "").split(";", 1)[0].strip().lower()


def _provider_identifiers(headers: dict[str, str], credential: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for name in _REQUEST_ID_HEADERS:
        value = headers.get(name)
        if value and credential not in value:
            result[name] = value[:1024]
    return result


def _character_cost(headers: dict[str, str], credential: str) -> dict[str, Any]:
    """Normalize only ElevenLabs' official character-cost usage header."""

    raw = headers.get("character-cost")
    evidence: dict[str, Any] = {
        "header": "character-cost",
        "present": raw is not None,
        "value": None,
        "unit": "provider_reported_character_cost",
    }
    if raw is None:
        return evidence
    if credential in raw or re.fullmatch(r"[0-9]+", raw) is None:
        raise _HttpFailure("invalid_character_cost_header")
    value = int(raw)
    if value > 1_000_000_000:
        raise _HttpFailure("invalid_character_cost_header")
    evidence["value"] = value
    return evidence


def _read_bounded(response: Any, maximum: int) -> bytes:
    headers = _header_map(response.headers)
    content_length = headers.get("content-length")
    if content_length:
        try:
            declared = int(content_length)
        except ValueError as exc:
            raise _HttpFailure("invalid_content_length") from exc
        if declared < 0 or declared > maximum:
            raise _HttpFailure("response_size_ceiling_exceeded")
    data = response.read(maximum + 1)
    if len(data) > maximum:
        raise _HttpFailure("response_size_ceiling_exceeded")
    return data


def _parse_http_failure(exc: urllib.error.HTTPError, credential: str) -> _HttpFailure:
    headers = _header_map(exc.headers)
    character_cost = _character_cost(headers, credential)
    try:
        body = exc.read(MAX_ERROR_RESPONSE_BYTES + 1)
    except OSError:
        body = b""
    if len(body) > MAX_ERROR_RESPONSE_BYTES:
        body = body[:MAX_ERROR_RESPONSE_BYTES]
    provider_code: str | None = None
    capability_text = ""
    try:
        payload = json.loads(body.decode("utf-8"))
        detail = payload.get("detail", payload) if isinstance(payload, dict) else payload
        if isinstance(detail, dict):
            raw_code = detail.get("status") or detail.get("code")
            raw_message = detail.get("message")
            if isinstance(raw_code, str) and credential not in raw_code:
                provider_code = raw_code[:255]
            if isinstance(raw_message, str) and credential not in raw_message:
                capability_text = raw_message[:2048]
        elif isinstance(detail, str) and credential not in detail:
            capability_text = detail[:2048]
    except (UnicodeError, json.JSONDecodeError):
        pass
    haystack = f"{provider_code or ''} {capability_text}".lower()
    mentions_pcm = any(term in haystack for term in ("pcm", "output_format", "output format"))
    unavailable = any(
        term in haystack
        for term in (
            "unsupported",
            "not supported",
            "unavailable",
            "not available",
            "not allowed",
            "invalid output",
        )
    )
    capability = exc.code in {400, 404, 422} and mentions_pcm and unavailable
    return _HttpFailure(
        "pcm_capability_unavailable" if capability else "provider_http_failure",
        http_status=exc.code,
        provider_code=provider_code,
        response_sha256=sha256_bytes(body),
        pcm_capability_unavailable=capability,
        provider_identifiers=_provider_identifiers(headers, credential),
        character_cost=character_cost,
    )


def _post_once(
    *,
    url_path: str,
    query: dict[str, str],
    body: bytes,
    api_key: str,
    timeout: float,
) -> _HttpResponse:
    """Make exactly one POST through an opener that refuses redirects."""

    if url_path.startswith("//") or not url_path.startswith("/v1/text-to-speech/"):
        raise ValidationError("refusing a non-ElevenLabs TTS path")
    url = f"{API_ORIGIN}{url_path}?{urllib.parse.urlencode(query)}"
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Accept": "application/octet-stream",
            "Content-Type": "application/json",
            "xi-api-key": api_key,
        },
    )
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as response:
            headers = _header_map(response.headers)
            if headers.get("content-encoding", "identity").lower() not in {"", "identity"}:
                raise _HttpFailure("encoded_audio_response_forbidden")
            data = _read_bounded(response, MAX_RESPONSE_BYTES)
            return _HttpResponse(
                data=data,
                mime_type=_normalized_mime(headers),
                headers=headers,
                provider_identifiers=_provider_identifiers(headers, api_key),
                character_cost=_character_cost(headers, api_key),
            )
    except urllib.error.HTTPError as exc:
        raise _parse_http_failure(exc, api_key) from exc
    except _HttpFailure:
        raise
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        # Do not include a provider URL, response body, or credential in errors.
        raise _HttpFailure("provider_transport_failure") from exc


def _execution_body(request: dict[str, Any]) -> tuple[bytes, str]:
    body = request["request_body"]
    serialized = _json_bytes(body)
    digest = sha256_bytes(serialized)
    if digest != request["request_body_sha256"]:
        raise ValidationError("execution body is not the exact compiled request body")
    return serialized, digest


def _validate_pcm_response(response: _HttpResponse) -> None:
    if response.mime_type not in _PCM_MIMES:
        raise _HttpFailure("pcm_response_mime_mismatch")
    data = response.data
    if not data or len(data) % 2:
        raise _HttpFailure("pcm_response_not_s16le_aligned")
    if (
        data.startswith((b"ID3", b"fLaC", b"OggS", b"\x1aE\xdf\xa3"))
        or (len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WAVE")
        or (len(data) >= 2 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0)
    ):
        raise _HttpFailure("pcm_response_contains_a_container_or_lossy_signature")


def _validate_mp3_signature(response: _HttpResponse) -> None:
    if response.mime_type not in _MP3_MIMES:
        raise _HttpFailure("mp3_response_mime_mismatch")
    data = response.data
    if not (
        data.startswith(b"ID3")
        or (len(data) >= 2 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0)
    ):
        raise _HttpFailure("mp3_response_signature_mismatch")


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def execute_directed_bakeoff(
    authorization_path: Path,
    *,
    timeout: float = 60.0,
) -> dict[str, Any]:
    """Execute only the four frozen ElevenLabs calibration requests.

    The exact authorization is consumed before ``_post_once`` can run.  A
    network, HTTP, MIME, codec, cap, or filesystem failure aborts the run; no
    retry occurs.  MP3 is attempted at most once for a request and only after
    an explicit 400/404/422 PCM-capability rejection has already been written
    as immutable evidence.
    """

    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0 or timeout > 300:
        raise ValidationError("timeout must be greater than zero and at most 300 seconds")
    contract = validate_directed_bakeoff_execution(Path(authorization_path))
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if (
        not isinstance(api_key, str)
        or not api_key
        or api_key != api_key.strip()
        or any(character in api_key for character in "\r\n\x00")
        or len(api_key) > 4096
    ):
        raise ValidationError("ELEVENLABS_API_KEY is required only for execution and is malformed or absent")

    # Recheck every destination after credential lookup and immediately before
    # consuming authority.  This keeps preflight failures non-consuming.
    contract = validate_directed_bakeoff_execution(Path(authorization_path))
    authorization = contract.authorization
    authorization_hash = sha256_file(contract.authorization_path)
    consumption = {
        "schema_version": CONSUMPTION_SCHEMA,
        "authorization_id": authorization["authorization_id"],
        "authorization_sha256": authorization_hash,
        "scope": AUTHORIZATION_SCOPE,
        "status": "consumed",
        "consumed_at": _utc_now(),
        "reason": "directed bakeoff provider execution began; no retry is authorized",
        "request_set_sha256": contract.dry_run["request_set_sha256"],
        "seed_map_sha256": contract.seed_map_sha256,
    }
    _exclusive_write(contract.consumption_path, _receipt_bytes(consumption))

    limits = authorization["authorized_limits"]
    attempted_calls = 0
    attempted_characters = 0
    attempted_modeled_spend = 0.0
    outputs_received = 0
    results: list[dict[str, Any]] = []
    usage_evidence: list[dict[str, Any]] = []
    current_request_id: str | None = None
    current_output_format: str | None = None

    def charge(*, characters: int, modeled_spend: float) -> None:
        nonlocal attempted_calls, attempted_characters, attempted_modeled_spend
        next_calls = attempted_calls + 1
        next_characters = attempted_characters + characters
        next_spend = round(attempted_modeled_spend + modeled_spend, 9)
        if next_calls > limits["max_calls"] or next_calls > MAX_CALLS:
            raise ValidationError("authorization call ceiling exhausted before network")
        if next_characters > limits["max_characters"] or next_characters > MAX_AUTHORIZED_CHARACTERS:
            raise ValidationError("authorization character ceiling exhausted before network")
        if next_spend > float(limits["max_spend_usd"]) + 1e-9:
            raise ValidationError("authorization modeled-spend ceiling exhausted before network")
        attempted_calls = next_calls
        attempted_characters = next_characters
        attempted_modeled_spend = next_spend

    def failure_receipt(reason_code: str) -> None:
        if contract.failure_receipt_path.exists():
            return
        value = {
            "schema_version": FAILURE_RECEIPT_SCHEMA,
            "authorization_sha256": authorization_hash,
            "authorization_consumption": {
                "path": contract.consumption_path.relative_to(
                    contract.authorization_path.parent
                ).as_posix(),
                "sha256": sha256_file(contract.consumption_path),
            },
            "compiled_dry_run_sha256": sha256_file(
                contract.artifact_root / "compiled" / "provider-bakeoff-dry-run.json"
            ),
            "request_set_sha256": contract.dry_run["request_set_sha256"],
            "seed_map_sha256": contract.seed_map_sha256,
            "failed_request_id": current_request_id,
            "reason_code": reason_code,
            "attempted_calls": attempted_calls,
            "attempted_characters": attempted_characters,
            "attempted_modeled_spend_usd": attempted_modeled_spend,
            "outputs_received": outputs_received,
            "partial_results": results,
            "provider_usage_evidence": usage_evidence,
            "network_called": attempted_calls > 0,
            "retries_made": 0,
            "creative_approved": False,
            "step3_authorized": False,
            "failed_at": _utc_now(),
        }
        _exclusive_write(contract.failure_receipt_path, _receipt_bytes(value))

    try:
        for request in contract.requests:
            current_request_id = request["request_id"]
            current_output_format = "pcm_48000"
            seed = contract.fixed_seeds[current_request_id]
            body, execution_body_hash = _execution_body(request)
            base_result = {
                "request_id": current_request_id,
                "passage_id": request["passage_id"],
                "candidate_ids": request["candidate_ids"],
                "start_token": request["start_token"],
                "end_token": request["end_token"],
                "spoken_text_sha256": request["spoken_text_sha256"],
                "compiled_request_body_sha256": request["request_body_sha256"],
                "execution_request_body_sha256": execution_body_hash,
                "fixed_seed": seed,
            }
            charge(
                characters=request["estimated_billable_character_count"],
                modeled_spend=request["estimated_public_rate_cost_usd"],
            )
            try:
                response = _post_once(
                    url_path=request["url_path"],
                    query=request["query"],
                    body=body,
                    api_key=api_key,
                    timeout=float(timeout),
                )
                usage_evidence.append(
                    {
                        "request_id": current_request_id,
                        "output_format": "pcm_48000",
                        **response.character_cost,
                    }
                )
                _validate_pcm_response(response)
                raw_path = _safe_new_relative(
                    contract.artifact_root,
                    request["destinations"][0],
                    f"{current_request_id} PCM destination",
                    prefix="outputs",
                    suffix=".pcm",
                )
                _exclusive_write(raw_path, response.data)
                result = {
                    **base_result,
                    "requested_output_format": "pcm_48000",
                    "actual_output_format": "pcm_48000",
                    "actual_codec": "pcm_s16le",
                    "container": "raw",
                    "sample_rate_hz": 48_000,
                    "channels": 1,
                    "bit_depth": 16,
                    "response_mime_type": response.mime_type,
                    "provider_identifiers": response.provider_identifiers,
                    "provider_usage_evidence": response.character_cost,
                    "raw_output": {
                        "path": _relative(contract.artifact_root, raw_path),
                        "sha256": sha256_file(raw_path),
                        "byte_count": len(response.data),
                    },
                    "lossy_origin": False,
                    "comparison_eligible": True,
                    "comparison_exclusion_reason": None,
                    "pcm_capability_failure_receipt": None,
                }
            except _HttpFailure as primary_failure:
                if not primary_failure.pcm_capability_unavailable:
                    raise
                usage_evidence.append(
                    {
                        "request_id": current_request_id,
                        "output_format": "pcm_48000",
                        **primary_failure.character_cost,
                    }
                )
                fallback = request["fallback_request"]
                fallback_receipt_path = _safe_new_relative(
                    contract.artifact_root,
                    f"receipts/elevenlabs/{authorization['authorization_id']}-{current_request_id}-pcm-capability.json",
                    f"{current_request_id} PCM capability receipt",
                    prefix="receipts",
                    suffix=".json",
                )
                rejection_receipt_path = _safe_new_relative(
                    contract.artifact_root,
                    f"receipts/elevenlabs/{authorization['authorization_id']}-{current_request_id}-pcm-capability-rejection.json",
                    f"{current_request_id} pre-fallback rejection receipt",
                    prefix="receipts",
                    suffix=".json",
                )
                failure_evidence = {
                    "http_status": primary_failure.http_status,
                    "kind": "pcm_capability_unavailable",
                    "retryable": False,
                    "provider_code": primary_failure.provider_code or "unavailable",
                    "message": "provider explicitly rejected pcm output capability",
                    "occurred_at": _utc_now(),
                    "response_sha256": primary_failure.response_sha256,
                    "attempted_call_number": attempted_calls,
                    "provider_identifiers": primary_failure.provider_identifiers,
                    "provider_usage_evidence": primary_failure.character_cost,
                }
                pcm_rejection_receipt = {
                    "schema_version": PCM_REJECTION_SCHEMA,
                    "provider": "elevenlabs",
                    "request_id": current_request_id,
                    "attempted_output_format": "pcm_48000",
                    "fallback_output_format": "mp3_44100_192",
                    "failure": failure_evidence,
                    "fallback_request_body_sha256": execution_body_hash,
                    "fallback_attempted": False,
                }
                # The capability evidence exists before the sole fallback POST.
                _exclusive_write(
                    rejection_receipt_path, _receipt_bytes(pcm_rejection_receipt)
                )
                charge(
                    characters=fallback["estimated_additional_billable_character_count"],
                    modeled_spend=fallback["estimated_additional_public_rate_cost_usd"],
                )
                current_output_format = "mp3_44100_192"
                fallback_response = _post_once(
                    url_path=fallback["url_path"],
                    query=fallback["query"],
                    body=body,
                    api_key=api_key,
                    timeout=float(timeout),
                )
                usage_evidence.append(
                    {
                        "request_id": current_request_id,
                        "output_format": "mp3_44100_192",
                        **fallback_response.character_cost,
                    }
                )
                _validate_mp3_signature(fallback_response)
                raw_path = _safe_new_relative(
                    contract.artifact_root,
                    fallback["destination"],
                    f"{current_request_id} MP3 destination",
                    prefix="outputs",
                    suffix=".mp3",
                )
                _exclusive_write(raw_path, fallback_response.data)
                audio = inspect_audio(raw_path)
                if not audio.get("is_approved_mp3_fallback"):
                    raise _HttpFailure("mp3_response_is_not_mono_44100_192kbps")
                pcm_failure_receipt = {
                    "schema_version": PCM_FAILURE_SCHEMA,
                    "provider": "elevenlabs",
                    "request_id": current_request_id,
                    "attempted_output_format": "pcm_48000",
                    "fallback_output_format": "mp3_44100_192",
                    "failure": failure_evidence,
                    "capability_rejection": {
                        "path": _relative(contract.artifact_root, rejection_receipt_path),
                        "sha256": sha256_file(rejection_receipt_path),
                        "written_before_fallback": True,
                    },
                    "raw_output": {
                        "path": _relative(contract.artifact_root, raw_path),
                        "sha256": sha256_file(raw_path),
                    },
                }
                _exclusive_write(fallback_receipt_path, _receipt_bytes(pcm_failure_receipt))
                result = {
                    **base_result,
                    "requested_output_format": "pcm_48000",
                    "actual_output_format": "mp3_44100_192",
                    "actual_codec": "mp3",
                    "container": audio.get("container"),
                    "sample_rate_hz": audio.get("sample_rate_hz"),
                    "channels": audio.get("channels"),
                    "bit_rate_bps": audio.get("bit_rate_bps"),
                    "response_mime_type": fallback_response.mime_type,
                    "provider_identifiers": fallback_response.provider_identifiers,
                    "provider_usage_evidence": fallback_response.character_cost,
                    "raw_output": {
                        "path": _relative(contract.artifact_root, raw_path),
                        "sha256": sha256_file(raw_path),
                        "byte_count": len(fallback_response.data),
                    },
                    "lossy_origin": True,
                    "comparison_eligible": False,
                    "comparison_exclusion_reason": "lossy fallback cannot be blind-scored against native PCM",
                    "pcm_capability_failure_receipt": {
                        "path": _relative(contract.artifact_root, fallback_receipt_path),
                        "sha256": sha256_file(fallback_receipt_path),
                        "state": "documented_before_fallback",
                        "pre_fallback_rejection_path": _relative(
                            contract.artifact_root, rejection_receipt_path
                        ),
                    },
                }
            outputs_received += 1
            if outputs_received > limits["max_outputs"] or outputs_received > MAX_OUTPUTS:
                raise ValidationError("authorization output ceiling exceeded")
            result["lexical_hard_gate"] = {
                "status": "pending",
                "exact_words_verified": False,
                "spoken_direction_tag_risk": "unresolved",
                "requirement": "forced alignment or human review must prove no tag was spoken and canonical W did not drift",
            }
            result["creative_approved"] = False
            results.append(result)
    except _HttpFailure as exc:
        if not usage_evidence or (
            usage_evidence[-1].get("request_id") != current_request_id
            or usage_evidence[-1].get("output_format") != current_output_format
        ):
            usage_evidence.append(
                {
                    "request_id": current_request_id,
                    "output_format": current_output_format or "unknown_or_failed",
                    **exc.character_cost,
                }
            )
        failure_receipt(exc.code)
        raise ValidationError(
            f"directed bakeoff stopped after a non-retryable provider failure: {exc.code}"
        ) from exc
    except ValidationError as exc:
        failure_receipt("local_validation_or_cap_failure")
        raise

    run_receipt = {
        "schema_version": RUN_RECEIPT_SCHEMA,
        "created_at": _utc_now(),
        "authorization_sha256": authorization_hash,
        "authorization_consumption": {
            "path": contract.consumption_path.relative_to(
                contract.authorization_path.parent
            ).as_posix(),
            "sha256": sha256_file(contract.consumption_path),
        },
        "bindings": {
            "compiled_dry_run_sha256": sha256_file(
                contract.artifact_root / "compiled" / "provider-bakeoff-dry-run.json"
            ),
            "request_set_sha256": contract.dry_run["request_set_sha256"],
            "seed_map_sha256": contract.seed_map_sha256,
        },
        "authorization_limits": dict(limits),
        "attempted_calls": attempted_calls,
        "attempted_characters": attempted_characters,
        "attempted_modeled_spend_usd": attempted_modeled_spend,
        "outputs_received": outputs_received,
        "results": results,
        "provider_usage_evidence": usage_evidence,
        "blind_comparison_eligible": all(
            result.get("comparison_eligible") is True for result in results
        ),
        "comparison_rule": "Any MP3 fallback candidate is excluded; mixed-codec A/B scoring is forbidden.",
        "network_called": attempted_calls > 0,
        "redirects_followed": 0,
        "retries_made": 0,
        "fallback_policy": "one documented mp3_44100_192 capability fallback per primary request only",
        "lexical_hard_gate": {
            "status": "pending",
            "spoken_direction_tag_risk": "unresolved",
            "all_candidates_require_review": True,
        },
        "creative_approved": False,
        "step3_authorized": False,
        "full_episode_authorized": False,
    }
    _exclusive_write(contract.run_receipt_path, _receipt_bytes(run_receipt))
    return {
        "mode": "execute",
        "network_called": True,
        "receipt": _relative(contract.artifact_root, contract.run_receipt_path),
        **run_receipt,
    }
