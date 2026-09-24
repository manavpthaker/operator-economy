#!/usr/bin/env python3
"""One-shot Fal Sync submission for the two owner-approved Higgsfield recoveries.

Reuses the pinned Fal endpoint, URL/account validators, caps, and later status/result
commands in sync_one_shot.py. `check` makes no provider call. `submit` writes intent
before one POST and cannot retry an existing target.
"""

from __future__ import annotations

import argparse
import fcntl
import math
import os
from pathlib import Path

import sync_one_shot as base


ROOT = base.REPO
HERE = base.HERE
RECOVERY_AUTH = ROOT / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-owner-approve-two-bounded-recovery-calls-20260923.json"
RECOVERY_AUTH_SHA = "8aa69611a23acdfa7c76b5a5fbb0f89c688ab29dcc40fc19d1a9d7bbb3c7a64e"
TARGETS = {
    "short03-b": {
        "project": "EP007-SHORT03-PRESENTER-001",
        "segment_dir": "segment-b",
        "short_id": "short-03-how-you-charge",
        "segment": "segment-b-return",
        "job_id": "cac6a333-3224-4f5a-8604-aa7bd3ebd1a2",
        "batch_index": 1,
        "native_sha256": "208729f3ce55821aed42d351a61569929519dcf534ad8ef751fde09cb730777f",
        "source_sha256": "08c84977e6062bc91e26cf8a0368a3f9843e7b480ac5edaf437a165e4aacf957",
        "need_sha256": "e31a51bf8757c632e8d8f3e980f735bcb3cf398600a37edd68431b42fe96f96e",
        "audio_file": "original-c-segment-b.mp3",
        "audio_media_id": "bf553cb5-8177-4b48-9b1f-5bf230e11dd1",
        "audio_sha256": "ec65257cd60f3b9748dd1f801c2bb74c06d423564ff737ff5ce48f68a7a6275b",
        "audio_seconds": 7,
    },
    "short04-a": {
        "project": "EP007-SHORT04-PRESENTER-001",
        "segment_dir": "segment-a",
        "short_id": "short-04-test-the-front-door",
        "segment": "segment-a-opening",
        "job_id": "061008bb-d659-4f68-8876-19120b05f3b8",
        "batch_index": 2,
        "native_sha256": "068965e3cf47c376888229d1219236bd93a8ad8baff57182c594d44459ad0fe8",
        "source_sha256": "4dfe8c572cc2ee403225bd6de20be64df9ed8056679de4137415eb0f38d21841",
        "need_sha256": "9da7cc7355db4880c151a1e4311f6071a9752c5a078cf966e8b272020d87531b",
        "audio_file": "original-c-opening.mp3",
        "audio_media_id": "5a58a74d-8977-40dc-86c0-c766fe4c221e",
        "audio_sha256": "38120fa6462e7715fba73b192926ccd79d6e7f5978ad55fe49be138e484e69a6",
        "audio_seconds": 9,
    },
}


def checked(key: str, video_url: str) -> dict:
    row = TARGETS[key]
    base.expect(base.sha(RECOVERY_AUTH) == RECOVERY_AUTH_SHA, "Owner recovery authority changed")
    event = base.read_json(RECOVERY_AUTH)
    allowed = event.get("authorized") or {}
    base.expect(allowed.get("higgsfield_short03_return_attempts_max") == 1 and allowed.get("higgsfield_short04_opening_attempts_max") == 1, "Recovery scope changed")
    plan, _ = base.load_plan()
    batch_path = ROOT / plan["higgsfield_batch_source_of_truth"]["path"]
    batch_row = base.read_json(batch_path)["jobs"][row["batch_index"]]
    base.expect(batch_row.get("status") == "submission_failed" and batch_row.get("job_id") is None, "Original batch was not a no-job rejection")
    seg = ROOT / "blueprint-cinema/experiments" / row["project"] / row["segment_dir"]
    recovery = seg / "RECOVERY-SUBMISSION-20260923.json"
    base.expect(recovery.is_file(), "Recovery submission receipt missing")
    record = base.read_json(recovery)
    base.expect(record.get("job_id") == row["job_id"] and record.get("new_attempt_count") == 1 and record.get("further_generation_retry_authorized") is False, "Recovery job binding changed")
    base.validate_video_url(video_url, row["job_id"])
    source_path = seg / "VIDEO-SOURCE.json"
    source = base.read_json(source_path)
    base.expect(base.sha(source_path) == row["source_sha256"] and source.get("status") == "completed" and source.get("job_id") == row["job_id"] and source.get("result_url") == video_url, "Completed source changed")
    native = seg / "media/generated-native.mp4"
    base.expect(base.sha(native) == row["native_sha256"] and source["download"]["sha256"] == row["native_sha256"], "Native video bytes changed")
    probe = base.local_video_probe(native)
    base.expect(probe["width"] == 1080 and probe["height"] == 1920 and row["audio_seconds"] - 0.2 <= probe["video_seconds"] <= row["audio_seconds"] + 0.5, "Native video probe outside expected portrait clip")
    need_path = seg / "SYNC-NEED.json"
    need = base.read_json(need_path)
    base.expect(base.sha(need_path) == row["need_sha256"] and need.get("status") == "needed" and need.get("video_source_sha256") == row["source_sha256"], "Sync need changed")
    audio = seg / "media" / row["audio_file"]
    base.expect(base.sha(audio) == row["audio_sha256"], "Original C audio changed")
    uploads = base.read_json(seg.parent / "UPLOAD-RECEIPT-V1.json").get("uploads") or []
    matches = [item for item in uploads if item.get("media_id") == row["audio_media_id"] and item.get("source_sha256") == row["audio_sha256"] and item.get("byte_identical") is True]
    base.expect(len(matches) == 1, "Original C upload was not verified")
    prior_calls, prior_cents = base.prior_forecast(key)
    forecast = math.ceil(max(probe["video_seconds"], row["audio_seconds"]) * base.RATE_CENTS_PER_MINUTE / 60)
    base.expect(prior_cents + forecast <= base.MAX_FORECAST_CENTS, "Shared Fal forecast exceeds $15 cap")
    outdir = base.output_dir(key)
    existing = [name for name in ("SYNC-REQUEST.json", "SYNC-SUBMISSION-INTENT.json", "SYNC-JOB.json", "SYNC-ERROR.json", "SYNC-RESULT.json") if (outdir / name).exists()]
    base.expect(not existing, f"Existing Fal evidence blocks any retry: {existing}")
    return {
        "target": key,
        "short_id": row["short_id"],
        "segment": row["segment"],
        "model": base.MODEL,
        "endpoint": base.SUBMIT_URL,
        "input": {"video_url": video_url, "audio_url": base.audio_url(row), "sync_mode": "silence"},
        "video_source": {"path": base.rel(source_path), "sha256": row["source_sha256"], "decoded_seconds": probe["video_seconds"]},
        "sync_need": {"path": base.rel(need_path), "sha256": row["need_sha256"]},
        "audio_source": {"path": base.rel(audio), "sha256": row["audio_sha256"], "media_id": row["audio_media_id"], "seconds": row["audio_seconds"]},
        "owner_recovery_authority_sha256": RECOVERY_AUTH_SHA,
        "prior_fal_intents": prior_calls,
        "prior_forecast_cents": prior_cents,
        "forecast_cents": forecast,
        "aggregate_forecast_cents": prior_cents + forecast,
        "cap_cents": base.MAX_FORECAST_CENTS,
        "provider_enforced_spend_cap": False,
        "network_called_by_check": False,
    }


def submit(key: str, video_url: str) -> dict:
    lock_fd = os.open(HERE / ".sync-submit.lock", os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        spec = checked(key, video_url)
        secret = base.key_from_env()
        outdir = base.output_dir(key)
        request = outdir / "SYNC-REQUEST.json"
        intent = outdir / "SYNC-SUBMISSION-INTENT.json"
        base.write_json_x(request, spec)
        base.write_json_x(intent, {
            "record_type": "ep007_fal_sync_v3_recovery_one_shot_submission_intent",
            "at_utc": base.now(), "target": key, "short_id": spec["short_id"], "segment": spec["segment"],
            "model": base.MODEL, "request_path": base.rel(request), "request_sha256": base.sha(request),
            "video_source_sha256": spec["video_source"]["sha256"], "sync_need_sha256": spec["sync_need"]["sha256"],
            "forecast_cents": spec["forecast_cents"], "aggregate_forecast_cents": spec["aggregate_forecast_cents"],
            "owner_cap_cents": base.MAX_FORECAST_CENTS, "automatic_retries": 0,
            "provider_calls_before_this_intent": spec["prior_fal_intents"],
            "submission_state": "intent_persisted_before_one_POST",
            "program_audio_rule": "Continuous exact Original C master remains the only delivered voice; Fal audio is not program audio.",
        })
        try:
            response = base.api_call(base.SUBMIT_URL, key=secret, body=spec["input"])
        except BaseException as error:
            base.write_json_x(outdir / "SYNC-ERROR.json", {"at_utc": base.now(), "status": "uncertain_or_failed_no_retry", "error_class": type(error).__name__, "detail": str(error).replace(secret, "[REDACTED]")[:2000]})
            base.fail(f"Fal submission outcome uncertain for {key}; no retry")
        base.write_json_x(outdir / "SYNC-JOB.json", response)
        request_id = response.get("request_id") if isinstance(response, dict) else None
        base.expect(isinstance(request_id, str) and base.UUID_RE.fullmatch(request_id) is not None, "Fal returned unrecognized job response; preserved, no retry")
        return {"target": key, "status": "submitted_pending_result", "request_id": request_id, "forecast_usd": spec["forecast_cents"] / 100}
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "submit"))
    parser.add_argument("target", choices=TARGETS)
    parser.add_argument("--video-url", required=True)
    args = parser.parse_args()
    spec = checked(args.target, args.video_url) if args.command == "check" else submit(args.target, args.video_url)
    print(base.json.dumps(spec, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
