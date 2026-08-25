"""Command-line interface for the Step 2 narration runtime."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from .audio import convert_working, inspect_audio, inspect_provider_raw_pcm
from .bakeoff import (
    dry_run_provider_bakeoff,
    validate_performance_envelope,
    validate_provider_action_authorization,
    validate_provider_adapter,
    validate_provider_bakeoff_plan,
)
from .core import (
    ValidationError,
    extract_step1_script,
    validate_capture_plan,
    validate_state,
    validate_transcript,
    verify_package,
    write_extraction,
)
from .directed_bakeoff import (
    execute_directed_bakeoff,
    validate_directed_bakeoff_execution,
)
from .provider import dry_run_capture, execute_capture
from .performance_transfer import (
    dry_run_synthetic_guide,
    dry_run_voice_transfer,
    execute_synthetic_guide,
    validate_performance_transfer_plan,
    validate_synthetic_guide_authorization,
)
from .retrieval import (
    dry_run_metadata_inventory,
    dry_run_named_sample_batch,
    dry_run_retrieval,
    execute_metadata_inventory,
    execute_named_sample_batch,
    execute_retrieval,
)
from .voice_remix import (
    dry_run_voice_remix_preview,
    dry_run_voice_remix_save,
    execute_voice_remix_preview,
    execute_voice_remix_save,
    validate_voice_remix_preview_authorization,
    validate_voice_remix_save_authorization,
)


def _path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _audio_path(value: str) -> Path:
    """Preserve path components so audio safety checks can detect symlinks."""

    return Path(value).expanduser().absolute()


def _contract_path(value: str) -> Path:
    """Preserve components so authority validators can reject symlink traversal."""

    return Path(value).expanduser().absolute()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="oe-narration", description="Operator Blueprint V2 narration controls")
    parser.add_argument("--version", action="version", version="oe-narration 0.5.0")
    sub = parser.add_subparsers(dest="command", required=True)

    extract = sub.add_parser("extract", help="derive canonical W from a locked Step 1 script")
    extract.add_argument("--script", type=_path, required=True)
    extract.add_argument("--out", type=_path)

    package = sub.add_parser("verify-package", help="verify hashes and the single spoken-text authority")
    package.add_argument("--manifest", type=_path, required=True)

    plan = sub.add_parser("validate-capture-plan", help="validate bounded calibration or full capture")
    plan.add_argument("--plan", type=_path, required=True)
    plan.add_argument("--canonical-w", type=_path, required=True)

    inspect = sub.add_parser("inspect-audio", help="inspect the actual codec and production properties")
    inspect.add_argument("--input", type=_audio_path, required=True)
    inspect.add_argument("--receipt", type=_audio_path, help="required only for headerless provider PCM")
    inspect.add_argument("--part-id")

    convert = sub.add_parser("convert-working", help="perform the one permitted raw-to-working WAV conversion")
    convert.add_argument("--input", type=_audio_path, required=True)
    convert.add_argument("--output", type=_audio_path, required=True)
    convert.add_argument("--receipt", type=_audio_path)
    convert.add_argument("--part-id")
    convert.add_argument("--record", type=_audio_path)

    transcript = sub.add_parser("validate-transcript", help="bind exact W timing to the exact master")
    transcript.add_argument("--transcript", type=_path, required=True)
    transcript.add_argument("--canonical-w", type=_path, required=True)
    transcript.add_argument("--master", type=_path)

    state = sub.add_parser("validate-state", help="validate gates, invalidation, technical pass, and human approval")
    state.add_argument("--state", type=_path, required=True)

    capture = sub.add_parser("capture-elevenlabs", help="dry-run by default; provider calls require --execute and authorization")
    capture.add_argument("--plan", type=_path, required=True)
    capture.add_argument("--canonical-w", type=_path, required=True)
    capture.add_argument("--output-dir", type=_path)
    capture.add_argument("--execute", action="store_true")
    capture.add_argument("--authorization", type=_path)
    capture.add_argument("--record", type=_path, help="write an immutable dry-run receipt")
    capture.add_argument("--timeout", type=float, default=60.0)

    envelope = sub.add_parser(
        "validate-performance-envelope",
        help="validate a provider-neutral performance envelope against canonical W",
    )
    envelope.add_argument("--envelope", type=_path, required=True)
    envelope.add_argument("--canonical-w", type=_path, required=True)

    adapter = sub.add_parser(
        "validate-provider-adapter",
        help="validate one provider adapter without accessing credentials",
    )
    adapter.add_argument("--adapter", type=_path, required=True)
    adapter.add_argument("--envelope", type=_path, required=True)
    adapter.add_argument("--canonical-w", type=_path, required=True)

    bakeoff_plan = sub.add_parser(
        "validate-provider-bakeoff-plan",
        help="validate and compile-check a provider bakeoff plan without external action",
    )
    bakeoff_plan.add_argument("--plan", type=_path, required=True)
    bakeoff_plan.add_argument("--envelope", type=_path, required=True)
    bakeoff_plan.add_argument("--canonical-w", type=_path, required=True)

    bakeoff = sub.add_parser(
        "dry-run-provider-bakeoff",
        help="compile credential-free provider request bodies; never calls a provider",
    )
    bakeoff.add_argument("--plan", type=_path, required=True)
    bakeoff.add_argument("--envelope", type=_path, required=True)
    bakeoff.add_argument("--canonical-w", type=_path, required=True)
    bakeoff.add_argument("--record", type=_path)

    action_auth = sub.add_parser(
        "validate-provider-action-authorization",
        help="validate one exact provider action scope and its unconsumed authority",
    )
    action_auth.add_argument("--authorization", type=_path, required=True)

    retrieval = sub.add_parser(
        "retrieve-elevenlabs-sample",
        help="dry-run by default; consume one exact AUTH-01 before two read-only GETs",
    )
    retrieval.add_argument("--authorization", type=_path, required=True)
    retrieval.add_argument("--execute", action="store_true")
    retrieval.add_argument("--record", type=_path, help="write an immutable dry-run record")
    retrieval.add_argument("--timeout", type=float, default=60.0)

    inventory = sub.add_parser(
        "inventory-elevenlabs-samples",
        help="dry-run by default; consume one exact AUTH-01B before one metadata-only GET",
    )
    inventory.add_argument("--authorization", type=_path, required=True)
    inventory.add_argument("--execute", action="store_true")
    inventory.add_argument("--record", type=_path, help="write an immutable dry-run record")
    inventory.add_argument("--timeout", type=float, default=60.0)

    named_batch = sub.add_parser(
        "retrieve-elevenlabs-named-sample-batch",
        help="dry-run by default; consume exact AUTH-01C before three named sample GETs",
    )
    named_batch.add_argument("--authorization", type=_path, required=True)
    named_batch.add_argument("--execute", action="store_true")
    named_batch.add_argument("--record", type=_path, help="write an immutable dry-run record")
    named_batch.add_argument("--timeout", type=float, default=60.0)

    remix_preview = sub.add_parser(
        "remix-elevenlabs-voice",
        help="dry-run by default; consume one exact authorization for one private remix-preview batch",
    )
    remix_preview.add_argument("--authorization", type=_path, required=True)
    remix_preview.add_argument("--execute", action="store_true")
    remix_preview.add_argument("--record", type=_path, help="write an immutable dry-run record")
    remix_preview.add_argument("--timeout", type=float, default=60.0)

    remix_save = sub.add_parser(
        "save-elevenlabs-remix",
        help="dry-run by default; save one explicitly owner-selected remix as a new voice",
    )
    remix_save.add_argument("--authorization", type=_path, required=True)
    remix_save.add_argument("--execute", action="store_true")
    remix_save.add_argument("--record", type=_path, help="write an immutable dry-run record")
    remix_save.add_argument("--timeout", type=float, default=60.0)

    directed_bakeoff = sub.add_parser(
        "directed-elevenlabs-bakeoff",
        help="dry-run by default; an exact active authorization binds every voice, seed, request, and output",
    )
    directed_bakeoff.add_argument("--authorization", type=_path, required=True)
    directed_bakeoff.add_argument("--execute", action="store_true")
    directed_bakeoff.add_argument("--timeout", type=float, default=60.0)

    transfer_plan = sub.add_parser(
        "validate-performance-transfer-plan",
        help="validate and compile the credential-free synthetic-guide to voice-transfer plan",
    )
    transfer_plan.add_argument("--plan", type=_contract_path, required=True)
    transfer_plan.add_argument("--canonical-w", type=_contract_path, required=True)

    synthetic_guide = sub.add_parser(
        "synthetic-guide",
        help="dry-run by default; consume one exact active G1 for two one-shot Gemini guide requests",
    )
    synthetic_guide.add_argument("--plan", type=_contract_path, required=True)
    synthetic_guide.add_argument("--canonical-w", type=_contract_path, required=True)
    synthetic_guide.add_argument("--authorization", type=_contract_path)
    synthetic_guide.add_argument("--record", type=_path)
    synthetic_guide.add_argument("--execute", action="store_true")
    synthetic_guide.add_argument("--timeout", type=float, default=60.0)

    voice_transfer = sub.add_parser(
        "elevenlabs-voice-transfer",
        help="dry-run the blocked or exact selected-guide Voice Changer request; external execution is not implemented",
    )
    voice_transfer.add_argument("--plan", type=_contract_path, required=True)
    voice_transfer.add_argument("--canonical-w", type=_contract_path, required=True)
    voice_transfer.add_argument("--authorization", type=_contract_path)
    voice_transfer.add_argument("--record", type=_path)
    voice_transfer.add_argument("--execute", action="store_true")
    return parser


def _write_json(path: Path, value: dict[str, Any]) -> None:
    if path.exists():
        raise ValidationError(f"refusing to overwrite record: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def dispatch(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "extract":
        extraction = extract_step1_script(args.script)
        if args.out:
            return write_extraction(extraction, args.out, args.script)
        return extraction.as_dict(str(args.script))
    if args.command == "verify-package":
        return verify_package(args.manifest)
    if args.command == "validate-capture-plan":
        return validate_capture_plan(args.plan, args.canonical_w)
    if args.command == "inspect-audio":
        if args.receipt:
            return inspect_provider_raw_pcm(args.input, args.receipt, args.part_id)
        return inspect_audio(args.input)
    if args.command == "convert-working":
        return convert_working(
            args.input,
            args.output,
            args.receipt,
            args.part_id,
            args.record,
        )
    if args.command == "validate-transcript":
        return validate_transcript(args.transcript, args.canonical_w, args.master)
    if args.command == "validate-state":
        return validate_state(args.state)
    if args.command == "capture-elevenlabs":
        if not args.execute:
            result = dry_run_capture(args.plan, args.canonical_w)
            if args.record:
                _write_json(args.record, result)
                result["record"] = str(args.record)
            return result
        if args.record is not None:
            raise ValidationError("--record is for dry runs; execution writes its own capture receipt")
        if args.authorization is None:
            raise ValidationError("--execute requires --authorization")
        if args.output_dir is None:
            raise ValidationError("--execute requires --output-dir")
        if args.timeout <= 0:
            raise ValidationError("--timeout must be positive")
        return execute_capture(
            args.plan,
            args.canonical_w,
            args.output_dir,
            args.authorization,
            args.timeout,
        )
    if args.command == "validate-performance-envelope":
        return validate_performance_envelope(args.envelope, args.canonical_w)
    if args.command == "validate-provider-adapter":
        return validate_provider_adapter(args.adapter, args.envelope, args.canonical_w)
    if args.command == "validate-provider-bakeoff-plan":
        return validate_provider_bakeoff_plan(args.plan, args.envelope, args.canonical_w)
    if args.command == "dry-run-provider-bakeoff":
        result = dry_run_provider_bakeoff(args.plan, args.envelope, args.canonical_w)
        if args.record:
            _write_json(args.record, result)
            result["record"] = str(args.record)
        return result
    if args.command == "validate-provider-action-authorization":
        return validate_provider_action_authorization(args.authorization)
    if args.command == "retrieve-elevenlabs-sample":
        if not args.execute:
            result = dry_run_retrieval(args.authorization)
            if args.record:
                _write_json(args.record, result)
                result["record"] = str(args.record)
            return result
        if args.record is not None:
            raise ValidationError("--record is for dry runs; execution uses authorized receipt destinations")
        if args.timeout <= 0:
            raise ValidationError("--timeout must be positive")
        return execute_retrieval(args.authorization, args.timeout)
    if args.command == "inventory-elevenlabs-samples":
        if not args.execute:
            result = dry_run_metadata_inventory(args.authorization)
            if args.record:
                _write_json(args.record, result)
                result["record"] = str(args.record)
            return result
        if args.record is not None:
            raise ValidationError("--record is for dry runs; execution uses the authorized receipt destination")
        if args.timeout <= 0:
            raise ValidationError("--timeout must be positive")
        return execute_metadata_inventory(args.authorization, args.timeout)
    if args.command == "retrieve-elevenlabs-named-sample-batch":
        if not args.execute:
            result = dry_run_named_sample_batch(args.authorization)
            if args.record:
                _write_json(args.record, result)
                result["record"] = str(args.record)
            return result
        if args.record is not None:
            raise ValidationError("--record is for dry runs; execution uses authorized receipt destinations")
        if args.timeout <= 0:
            raise ValidationError("--timeout must be positive")
        return execute_named_sample_batch(args.authorization, args.timeout)
    if args.command == "remix-elevenlabs-voice":
        if not args.execute:
            validate_voice_remix_preview_authorization(args.authorization)
            result = dry_run_voice_remix_preview(args.authorization)
            if args.record:
                _write_json(args.record, result)
                result["record"] = str(args.record)
            return result
        if args.record is not None:
            raise ValidationError("--record is for dry runs; execution uses authorized receipt destinations")
        if args.timeout <= 0:
            raise ValidationError("--timeout must be positive")
        return execute_voice_remix_preview(args.authorization, timeout=args.timeout)
    if args.command == "save-elevenlabs-remix":
        if not args.execute:
            validate_voice_remix_save_authorization(args.authorization)
            result = dry_run_voice_remix_save(args.authorization)
            if args.record:
                _write_json(args.record, result)
                result["record"] = str(args.record)
            return result
        if args.record is not None:
            raise ValidationError("--record is for dry runs; execution uses authorized receipt destinations")
        if args.timeout <= 0:
            raise ValidationError("--timeout must be positive")
        return execute_voice_remix_save(args.authorization, timeout=args.timeout)
    if args.command == "directed-elevenlabs-bakeoff":
        if not args.execute:
            return validate_directed_bakeoff_execution(args.authorization).public_dict()
        if args.timeout <= 0:
            raise ValidationError("--timeout must be positive")
        return execute_directed_bakeoff(args.authorization, timeout=args.timeout)
    if args.command == "validate-performance-transfer-plan":
        return validate_performance_transfer_plan(args.plan, args.canonical_w)
    if args.command == "synthetic-guide":
        if args.execute:
            if args.record is not None:
                raise ValidationError("--record is for dry runs; execution writes its own immutable receipt")
            if args.authorization is None:
                raise ValidationError("--execute requires --authorization")
            if args.timeout <= 0 or args.timeout > 300:
                raise ValidationError("--timeout must be greater than zero and at most 300 seconds")
            return execute_synthetic_guide(
                args.authorization,
                args.plan,
                args.canonical_w,
                timeout=args.timeout,
            )
        if args.authorization:
            result = validate_synthetic_guide_authorization(
                args.authorization,
                args.plan,
                args.canonical_w,
            )
        else:
            result = dry_run_synthetic_guide(args.plan, args.canonical_w)
        if args.record:
            _write_json(args.record, result)
            result["record"] = str(args.record)
        return result
    if args.command == "elevenlabs-voice-transfer":
        if args.execute:
            raise ValidationError(
                "elevenlabs-voice-transfer external execution is intentionally unavailable in v0.5; "
                "this runtime performs credential-free validation and dry-run only"
            )
        result = dry_run_voice_transfer(
            args.plan,
            args.canonical_w,
            args.authorization,
        )
        if args.record:
            _write_json(args.record, result)
            result["record"] = str(args.record)
        return result
    raise ValidationError(f"unsupported command: {args.command}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = dispatch(args)
    except ValidationError as exc:
        print(json.dumps({"valid": False, "errors": exc.errors}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
