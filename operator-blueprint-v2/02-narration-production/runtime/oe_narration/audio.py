"""Fail-closed audio inspection and the single permitted working conversion."""

from __future__ import annotations

import json
import os
import stat
import subprocess
from pathlib import Path
from typing import Any

from .core import ValidationError, read_json, sha256_bytes, sha256_file


_CAPTURE_RUN_SCHEMA = "oe-provider-capture-run-v1"
_DIRECTED_RUN_SCHEMA = "oe-elevenlabs-directed-bakeoff-run-v1"


def _no_symlink_path(path: Path, label: str, *, must_exist: bool) -> Path:
    """Return a lexical absolute path only when no component is a symlink."""

    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for component in absolute.parts[1:]:
        current = current / component
        if current.is_symlink():
            raise ValidationError(f"{label} may not contain a symlink component")
        if must_exist and not current.exists():
            raise ValidationError(f"{label} does not exist")
    if must_exist and not absolute.is_file():
        raise ValidationError(f"{label} must be a regular file")
    return absolute


def _bound_existing_file(
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
    if (
        relative.is_absolute()
        or not relative.parts
        or relative.parts[0] != prefix
        or any(part in {"", ".", "..", "~"} for part in relative.parts)
        or relative.suffix.lower() != suffix
    ):
        raise ValidationError(f"{label} escapes its authorized boundary")
    candidate = _no_symlink_path(root / relative, label, must_exist=True)
    if not candidate.is_relative_to(root):
        raise ValidationError(f"{label} escapes its authorized boundary")
    return candidate


def _same_open_regular_file(path: Path, descriptor: int, label: str) -> None:
    """Prove the path still names the exact regular file held by descriptor."""

    safe_path = _no_symlink_path(path, label, must_exist=True)
    path_stat = os.stat(safe_path, follow_symlinks=False)
    descriptor_stat = os.fstat(descriptor)
    if (
        not stat.S_ISREG(path_stat.st_mode)
        or not stat.S_ISREG(descriptor_stat.st_mode)
        or (path_stat.st_dev, path_stat.st_ino)
        != (descriptor_stat.st_dev, descriptor_stat.st_ino)
    ):
        raise ValidationError(f"{label} changed after exclusive reservation")


def _unlink_reserved_if_same(path: Path | None, descriptor: int | None) -> None:
    if path is None or descriptor is None:
        return
    try:
        path_stat = os.stat(path, follow_symlinks=False)
        descriptor_stat = os.fstat(descriptor)
    except OSError:
        return
    if (path_stat.st_dev, path_stat.st_ino) == (
        descriptor_stat.st_dev,
        descriptor_stat.st_ino,
    ):
        try:
            path.unlink()
        except OSError:
            pass


def _validate_directed_authorization_chain(
    artifact_root: Path,
    receipt_path: Path,
    receipt: dict[str, Any],
    bindings: dict[str, Any],
    request_ids: list[Any],
) -> None:
    authorization_hash = receipt.get("authorization_sha256")
    authorization_root = artifact_root / "authorizations"
    _no_symlink_path(authorization_root, "directed authorization root", must_exist=False)
    if not authorization_root.is_dir():
        raise ValidationError("directed authorization root does not exist")
    matches: list[Path] = []
    for candidate in authorization_root.glob("*.json"):
        safe_candidate = _no_symlink_path(
            candidate, "directed authorization", must_exist=True
        )
        if sha256_file(safe_candidate) == authorization_hash:
            matches.append(safe_candidate)
    if len(matches) != 1:
        raise ValidationError(
            "directed receipt must match exactly one local authorization file"
        )
    authorization_path = matches[0]
    authorization = read_json(authorization_path)
    action = authorization.get("action")
    authorization_bindings = authorization.get("bindings")
    authorization_consumption = authorization.get("consumption")
    authorization_id = authorization.get("authorization_id")
    if (
        authorization.get("schema_version") != "oe-provider-action-authorization-v1"
        or authorization.get("scope") != "elevenlabs_calibration"
        or authorization.get("provider") != "elevenlabs"
        or authorization.get("approved") is not True
        or authorization.get("execution_ready") is not True
        or not isinstance(action, dict)
        or action.get("kind") != "bounded_tts_calibration"
        or action.get("request_ids") != request_ids
        or action.get("preferred_output_format") != "pcm_48000"
        or not isinstance(authorization_bindings, dict)
        or authorization_bindings.get("compiled_dry_run_sha256")
        != bindings["compiled_dry_run_sha256"]
        or authorization.get("authorized_limits") != receipt.get("authorization_limits")
        or not isinstance(authorization_consumption, dict)
        or not isinstance(authorization_id, str)
        or receipt_path.name != f"{authorization_id}-directed-bakeoff-run.json"
    ):
        raise ValidationError("directed authorization does not semantically bind the run")

    consumption_binding = receipt.get("authorization_consumption")
    assert isinstance(consumption_binding, dict)
    if consumption_binding.get("path") != authorization_consumption.get("record_path"):
        raise ValidationError("directed consumption path differs from its authorization")
    consumption_path = _bound_existing_file(
        authorization_root,
        consumption_binding.get("path"),
        "directed authorization consumption",
        prefix="consumed",
        suffix=".json",
    )
    if sha256_file(consumption_path) != consumption_binding.get("sha256"):
        raise ValidationError("directed authorization-consumption hash mismatch")
    consumption = read_json(consumption_path)
    if (
        consumption.get("schema_version")
        != "oe-provider-authorization-consumption-v1"
        or consumption.get("authorization_id") != authorization_id
        or consumption.get("authorization_sha256") != authorization_hash
        or consumption.get("scope") != "elevenlabs_calibration"
        or consumption.get("status") != "consumed"
        or consumption.get("request_set_sha256") != bindings["request_set_sha256"]
        or consumption.get("seed_map_sha256") != bindings["seed_map_sha256"]
    ):
        raise ValidationError(
            "directed authorization consumption does not semantically bind the run"
        )


def _inspect_directed_raw_pcm(
    path: Path,
    receipt_path: Path,
    receipt: dict[str, Any],
    raw_hash: str,
    part_id: str | None,
) -> dict[str, Any]:
    if part_id is None:
        raise ValidationError("directed raw PCM requires its exact request_id")
    resolved_receipt = _no_symlink_path(
        receipt_path, "directed PCM receipt", must_exist=True
    )
    if (
        resolved_receipt.parent.name != "elevenlabs"
        or resolved_receipt.parent.parent.name != "receipts"
    ):
        raise ValidationError("directed PCM receipt must remain under receipts/elevenlabs/")
    artifact_root = resolved_receipt.parents[2]
    if (
        receipt.get("network_called") is not True
        or receipt.get("retries_made") != 0
        or not isinstance(receipt.get("results"), list)
        or receipt.get("outputs_received") != len(receipt["results"])
    ):
        raise ValidationError("directed PCM receipt is not an exact successful run")

    bindings = receipt.get("bindings")
    consumption = receipt.get("authorization_consumption")
    if (
        not isinstance(bindings, dict)
        or any(
            not isinstance(bindings.get(field), str)
            or len(bindings[field]) != 64
            for field in (
                "compiled_dry_run_sha256",
                "request_set_sha256",
                "seed_map_sha256",
            )
        )
        or not isinstance(receipt.get("authorization_sha256"), str)
        or len(receipt["authorization_sha256"]) != 64
        or not isinstance(consumption, dict)
        or not isinstance(consumption.get("sha256"), str)
        or len(consumption["sha256"]) != 64
    ):
        raise ValidationError("directed PCM receipt lacks request bindings")
    compiled_path = _no_symlink_path(
        artifact_root / "compiled" / "provider-bakeoff-dry-run.json",
        "directed compiled request",
        must_exist=True,
    )
    if (
        sha256_file(compiled_path) != bindings["compiled_dry_run_sha256"]
    ):
        raise ValidationError("directed compiled-request hash does not match the receipt")
    compiled = read_json(compiled_path)
    compiled_requests = compiled.get("requests")
    if (
        compiled.get("schema_version") != "oe-provider-bakeoff-dry-run-v1"
        or compiled.get("request_set_sha256") != bindings["request_set_sha256"]
        or not isinstance(compiled_requests, list)
    ):
        raise ValidationError("directed compiled request set does not match the receipt")
    compiled_request_ids = [
        request.get("request_id")
        for request in compiled_requests
        if isinstance(request, dict) and request.get("provider") == "elevenlabs"
    ]
    receipt_request_ids = [
        item.get("request_id") for item in receipt["results"] if isinstance(item, dict)
    ]
    if compiled_request_ids != receipt_request_ids:
        raise ValidationError("directed receipt does not contain the exact compiled request set")
    _validate_directed_authorization_chain(
        artifact_root,
        resolved_receipt,
        receipt,
        bindings,
        compiled_request_ids,
    )

    resolved_raw = _no_symlink_path(path, "directed PCM source", must_exist=True)
    if not resolved_raw.is_relative_to(artifact_root):
        raise ValidationError("directed PCM source is outside its artifact root")
    relative_raw = resolved_raw.relative_to(artifact_root).as_posix()
    relative = Path(relative_raw)
    if (
        not relative.parts
        or relative.parts[0] != "outputs"
        or any(component in {"", ".", "..", "~"} for component in relative.parts)
        or relative.suffix.lower() != ".pcm"
    ):
        raise ValidationError("directed PCM source is outside outputs/ or is not .pcm")
    matches = []
    for item in receipt["results"]:
        if not isinstance(item, dict):
            continue
        raw_output = item.get("raw_output")
        if (
            isinstance(raw_output, dict)
            and raw_output.get("path") == relative_raw
            and raw_output.get("sha256") == raw_hash
            and item.get("request_id") == part_id
        ):
            matches.append(item)
    if len(matches) != 1:
        raise ValidationError(
            "directed raw PCM source/hash/request does not match exactly one receipt result"
        )
    item = matches[0]
    requests = [
        request
        for request in compiled_requests
        if isinstance(request, dict) and request.get("request_id") == part_id
    ]
    if len(requests) != 1:
        raise ValidationError("directed PCM request is not unique in the compiled run")
    request = requests[0]
    expected_result = {
        "requested_output_format": "pcm_48000",
        "actual_output_format": "pcm_48000",
        "actual_codec": "pcm_s16le",
        "container": "raw",
        "sample_rate_hz": 48_000,
        "channels": 1,
        "bit_depth": 16,
        "lossy_origin": False,
        "comparison_eligible": True,
        "pcm_capability_failure_receipt": None,
    }
    errors = [
        f"directed PCM receipt {key} mismatch"
        for key, value in expected_result.items()
        if item.get(key) != value
    ]
    if (
        not isinstance(item.get("candidate_ids"), list)
        or not item["candidate_ids"]
        or not isinstance(item.get("spoken_text_sha256"), str)
        or len(item["spoken_text_sha256"]) != 64
        or not isinstance(item.get("compiled_request_body_sha256"), str)
        or len(item["compiled_request_body_sha256"]) != 64
        or item.get("execution_request_body_sha256")
        != item.get("compiled_request_body_sha256")
    ):
        errors.append("directed PCM receipt request binding mismatch")
    request_body = request.get("request_body")
    if (
        request.get("provider") != "elevenlabs"
        or request.get("query") != {"output_format": "pcm_48000"}
        or request.get("destinations") != [relative_raw]
        or not isinstance(request_body, dict)
        or sha256_bytes(
            json.dumps(
                request_body,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        )
        != request.get("request_body_sha256")
        or any(
            item.get(field) != request.get(field)
            for field in (
                "passage_id",
                "candidate_ids",
                "start_token",
                "end_token",
                "spoken_text_sha256",
            )
        )
        or item.get("compiled_request_body_sha256")
        != request.get("request_body_sha256")
        or item.get("fixed_seed") != request_body.get("seed")
    ):
        errors.append("directed PCM receipt does not match the compiled request")
    if item.get("raw_output", {}).get("byte_count") != resolved_raw.stat().st_size:
        errors.append("directed PCM receipt byte count mismatch")
    if errors:
        raise ValidationError(errors)
    return item


def _reserve_private_file(path: Path, label: str) -> tuple[Path, int]:
    """Reserve one new owner-only file without following symlinks."""

    requested = _no_symlink_path(path, label, must_exist=False)
    if requested.exists() or requested.is_symlink():
        raise ValidationError(f"refusing to overwrite {label}: {requested}")
    requested.parent.mkdir(parents=True, exist_ok=True)
    absolute = _no_symlink_path(requested, label, must_exist=False)
    if not absolute.parent.is_dir():
        raise ValidationError(f"{label} parent is not a directory")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor: int | None = None
    try:
        descriptor = os.open(absolute, flags, 0o600)
        os.fchmod(descriptor, 0o600)
    except FileExistsError as exc:
        raise ValidationError(f"refusing to overwrite {label}: {absolute}") from exc
    except OSError as exc:
        if descriptor is not None:
            os.close(descriptor)
        if absolute.exists() and not absolute.is_symlink():
            absolute.unlink()
        raise ValidationError(f"cannot reserve {label}: {absolute}") from exc
    assert descriptor is not None
    return absolute, descriptor


def _run(
    command: list[str], *, pass_fds: tuple[int, ...] = ()
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
            pass_fds=pass_fds,
        )
    except OSError as exc:
        raise ValidationError(f"cannot run {command[0]}: {exc}") from exc


def inspect_audio(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValidationError(f"audio file does not exist: {path}")
    result = _run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(path),
        ]
    )
    if result.returncode != 0:
        raise ValidationError(f"ffprobe rejected {path}: {result.stderr.strip()}")
    try:
        probe = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"ffprobe returned invalid JSON for {path}") from exc
    streams = [stream for stream in probe.get("streams", []) if stream.get("codec_type") == "audio"]
    if len(streams) != 1:
        raise ValidationError(f"expected exactly one audio stream, got {len(streams)}")
    stream = streams[0]
    codec = str(stream.get("codec_name", ""))
    try:
        sample_rate = int(stream.get("sample_rate"))
        channels = int(stream.get("channels"))
        duration = float(stream.get("duration") or probe.get("format", {}).get("duration"))
    except (TypeError, ValueError) as exc:
        raise ValidationError("ffprobe omitted required sample-rate, channel, or duration data") from exc
    bit_rate_raw = stream.get("bit_rate") or probe.get("format", {}).get("bit_rate")
    try:
        bit_rate = int(bit_rate_raw) if bit_rate_raw is not None else None
    except (TypeError, ValueError):
        bit_rate = None
    bits_raw = stream.get("bits_per_raw_sample") or stream.get("bits_per_sample")
    try:
        bit_depth = int(bits_raw) if bits_raw else None
    except (TypeError, ValueError):
        bit_depth = None
    codec_depths = {
        "pcm_s16le": 16,
        "pcm_s24le": 24,
        "pcm_s32le": 32,
        "pcm_f32le": 32,
        "pcm_f64le": 64,
    }
    bit_depth = bit_depth or codec_depths.get(codec)
    format_name = str(probe.get("format", {}).get("format_name", ""))
    if codec.startswith("pcm_"):
        origin_class = "native_pcm"
    elif codec == "mp3":
        origin_class = "lossy_mp3"
    else:
        origin_class = "unsupported"
    is_approved_mp3 = (
        codec == "mp3"
        and sample_rate == 44_100
        and channels == 1
        and bit_rate is not None
        and 190_000 <= bit_rate <= 194_000
    )
    is_working_master = (
        codec == "pcm_s24le"
        and sample_rate == 48_000
        and channels == 1
        and "wav" in format_name.split(",")
    )
    return {
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "codec_name": codec,
        "container": format_name,
        "sample_rate_hz": sample_rate,
        "channels": channels,
        "bit_depth": bit_depth,
        "bit_rate_bps": bit_rate,
        "duration_seconds": duration,
        "origin_class": origin_class,
        "is_approved_mp3_fallback": is_approved_mp3,
        "is_working_master": is_working_master,
    }


def inspect_provider_raw_pcm(path: Path, receipt_path: Path, part_id: str | None = None) -> dict[str, Any]:
    """Inspect headerless provider PCM only when bound to a capture receipt.

    Raw S16LE has no self-describing header. Its byte geometry and immutable
    hash are checked here; codec/rate/channel claims must also match the
    credential-free provider receipt generated by this runtime.
    """
    path = _no_symlink_path(path, "raw PCM source", must_exist=True)
    receipt_path = _no_symlink_path(
        receipt_path, "raw PCM receipt", must_exist=True
    )
    receipt = read_json(receipt_path)
    schema_version = receipt.get("schema_version")
    if schema_version not in {_CAPTURE_RUN_SCHEMA, _DIRECTED_RUN_SCHEMA}:
        raise ValidationError(
            "raw PCM requires an exact provider-capture or directed-bakeoff run receipt"
        )
    raw_hash = sha256_file(path)
    if schema_version == _DIRECTED_RUN_SCHEMA:
        item = _inspect_directed_raw_pcm(path, receipt_path, receipt, raw_hash, part_id)
    else:
        matches = [
            item
            for item in receipt.get("results", [])
            if isinstance(item, dict)
            and item.get("raw_sha256") == raw_hash
            and (part_id is None or item.get("part_id") == part_id)
        ]
        if len(matches) != 1:
            raise ValidationError(
                "raw PCM hash/part does not match exactly one provider receipt result"
            )
        item = matches[0]
    expected = {
        "requested_output_format": "pcm_48000",
        "actual_codec": "pcm_s16le",
        "container": "raw",
        "sample_rate_hz": 48_000,
        "channels": 1,
        "bit_depth": 16,
        "lossy_origin": False,
    }
    errors = [f"raw PCM receipt {key} mismatch" for key, value in expected.items() if item.get(key) != value]
    size = path.stat().st_size
    if size == 0 or size % 2:
        errors.append("raw PCM byte length is empty or not aligned to signed 16-bit samples")
    if errors:
        raise ValidationError(errors)
    return {
        "path": str(path.resolve()),
        "sha256": raw_hash,
        "codec_name": "pcm_s16le",
        "container": "raw",
        "sample_rate_hz": 48_000,
        "channels": 1,
        "bit_depth": 16,
        "bit_rate_bps": 768_000,
        "duration_seconds": size / (48_000 * 2),
        "origin_class": "native_pcm",
        "is_approved_mp3_fallback": False,
        "is_working_master": False,
        "capture_receipt_schema_version": schema_version,
        "capture_receipt_sha256": sha256_file(receipt_path),
        "part_id": item.get("part_id") or item.get("request_id"),
    }


def validate_pcm_failure_receipt(receipt_path: Path, raw_path: Path) -> dict[str, Any]:
    receipt = read_json(receipt_path)
    errors: list[str] = []
    if receipt.get("schema_version") != "oe-pcm-capability-failure-v1":
        errors.append("fallback receipt must use oe-pcm-capability-failure-v1")
    if receipt.get("provider") != "elevenlabs":
        errors.append("fallback receipt provider must be elevenlabs")
    if receipt.get("attempted_output_format") != "pcm_48000":
        errors.append("fallback receipt must document a pcm_48000 attempt")
    if receipt.get("fallback_output_format") != "mp3_44100_192":
        errors.append("fallback receipt must authorize only mp3_44100_192")
    failure = receipt.get("failure")
    if not isinstance(failure, dict):
        errors.append("fallback receipt.failure must be an object")
        failure = {}
    status = failure.get("http_status")
    if status not in {400, 404, 422}:
        errors.append("fallback requires an explicit non-retryable 400, 404, or 422 PCM capability response")
    if failure.get("kind") != "pcm_capability_unavailable":
        errors.append("fallback failure.kind must be pcm_capability_unavailable")
    if failure.get("retryable") is not False:
        errors.append("fallback failure must explicitly be non-retryable")
    for field in ("provider_code", "message", "occurred_at"):
        if not isinstance(failure.get(field), str) or not failure.get(field):
            errors.append(f"fallback receipt.failure.{field} is required")
    raw = receipt.get("raw_output")
    if not isinstance(raw, dict):
        errors.append("fallback receipt.raw_output must be an object")
        raw = {}
    if raw.get("sha256") != sha256_file(raw_path):
        errors.append("fallback receipt raw-output hash does not match the immutable MP3")
    if errors:
        raise ValidationError(errors)
    return receipt


def convert_working(
    raw_path: Path,
    output_path: Path,
    receipt_path: Path | None = None,
    part_id: str | None = None,
    record_path: Path | None = None,
) -> dict[str, Any]:
    raw_path = _no_symlink_path(raw_path, "raw audio source", must_exist=True)
    if receipt_path is not None:
        receipt_path = _no_symlink_path(
            receipt_path, "audio provenance receipt", must_exist=True
        )
    output_path = _no_symlink_path(output_path, "working audio", must_exist=False)
    if record_path is not None:
        record_path = _no_symlink_path(
            record_path, "conversion record", must_exist=False
        )
    if output_path.exists() or output_path.is_symlink():
        raise ValidationError(f"refusing to overwrite working audio: {output_path}")
    if record_path is not None and (record_path.exists() or record_path.is_symlink()):
        raise ValidationError(f"refusing to overwrite conversion record: {record_path}")
    before_hash = sha256_file(raw_path)
    raw_pcm = False
    try:
        source = inspect_audio(raw_path)
    except ValidationError as probe_error:
        if receipt_path is None:
            raise probe_error
        source = inspect_provider_raw_pcm(raw_path, receipt_path, part_id)
        raw_pcm = True
    lossy_origin = source["origin_class"] == "lossy_mp3"
    fallback_receipt_hash: str | None = None
    if lossy_origin:
        if not source["is_approved_mp3_fallback"]:
            raise ValidationError("lossy input must be mono MP3 at exactly 44.1 kHz and 192 kbps")
        if receipt_path is None:
            raise ValidationError("MP3 fallback requires an actual PCM-capability-failure receipt")
        validate_pcm_failure_receipt(receipt_path, raw_path)
        fallback_receipt_hash = sha256_file(receipt_path)
    elif source["origin_class"] != "native_pcm":
        raise ValidationError(f"unsupported source codec: {source['codec_name']}")
    if (
        source.get("capture_receipt_schema_version") == _DIRECTED_RUN_SCHEMA
        and record_path is None
    ):
        raise ValidationError("directed PCM conversion requires an immutable conversion record")
    if record_path is not None and Path(os.path.abspath(record_path)) == Path(
        os.path.abspath(output_path)
    ):
        raise ValidationError("working audio and conversion record must be different files")

    reserved_output: Path | None = None
    reserved_record: Path | None = None
    output_descriptor: int | None = None
    record_descriptor: int | None = None
    try:
        if record_path is not None:
            reserved_record, record_descriptor = _reserve_private_file(
                record_path, "conversion record"
            )
        reserved_output, output_descriptor = _reserve_private_file(
            output_path, "working audio"
        )
        command = [
            "ffmpeg",
            "-nostdin",
            "-v",
            "error",
        ]
        if raw_pcm:
            command.extend(["-f", "s16le", "-ar", "48000", "-ac", "1"])
        command.extend([
            "-i",
            str(raw_path),
            "-map_metadata",
            "-1",
            "-vn",
            "-ac",
            "1",
            "-ar",
            "48000",
            "-c:a",
            "pcm_s24le",
            "-f",
            "wav",
            f"pipe:{output_descriptor}",
        ])
        result = _run(command, pass_fds=(output_descriptor,))
        if result.returncode != 0:
            raise ValidationError(f"ffmpeg conversion failed: {result.stderr.strip()}")
        os.fsync(output_descriptor)
        _same_open_regular_file(reserved_output, output_descriptor, "working audio")
        if sha256_file(raw_path) != before_hash:
            raise ValidationError("raw source changed during conversion")
        converted = inspect_audio(reserved_output)
        if not converted["is_working_master"]:
            raise ValidationError("converted output is not 48 kHz, 24-bit, mono PCM WAV")
        _same_open_regular_file(reserved_output, output_descriptor, "working audio")
        conversion = {
            "schema_version": "oe-working-conversion-v1",
            "raw": source,
            "raw_immutable_sha256": before_hash,
            "fallback_receipt_sha256": fallback_receipt_hash,
            "lossy_origin": lossy_origin,
            "conversion_count_from_raw": 1,
            "working": converted,
        }
        if record_descriptor is not None and reserved_record is not None:
            _same_open_regular_file(
                reserved_record, record_descriptor, "conversion record"
            )
            payload = (json.dumps(conversion, indent=2, sort_keys=True) + "\n").encode(
                "utf-8"
            )
            written = 0
            while written < len(payload):
                written += os.write(record_descriptor, payload[written:])
            os.fsync(record_descriptor)
            _same_open_regular_file(
                reserved_record, record_descriptor, "conversion record"
            )
            conversion["record"] = str(reserved_record)
        _same_open_regular_file(reserved_output, output_descriptor, "working audio")
        os.close(output_descriptor)
        output_descriptor = None
        if record_descriptor is not None:
            os.close(record_descriptor)
            record_descriptor = None
        return conversion
    except BaseException:
        _unlink_reserved_if_same(reserved_output, output_descriptor)
        _unlink_reserved_if_same(reserved_record, record_descriptor)
        if output_descriptor is not None:
            os.close(output_descriptor)
        if record_descriptor is not None:
            os.close(record_descriptor)
        raise
