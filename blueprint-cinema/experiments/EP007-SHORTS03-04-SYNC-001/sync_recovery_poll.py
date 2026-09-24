#!/usr/bin/env python3
"""Read terminal status/result for previously submitted Fal recovery jobs only."""

from __future__ import annotations

import argparse
import sys

sys.dont_write_bytecode = True
import sync_one_shot as base
import sync_recovery_submit as recovery


def bound_job(key: str) -> tuple[dict, dict, str]:
    base.expect(key in recovery.TARGETS, "Unknown recovery target")
    folder = base.output_dir(key)
    request_file = folder / "SYNC-REQUEST.json"
    intent_file = folder / "SYNC-SUBMISSION-INTENT.json"
    job_file = folder / "SYNC-JOB.json"
    base.expect(request_file.is_file() and intent_file.is_file() and job_file.is_file(), "Recovery Fal request, intent or job missing")
    request = base.read_json(request_file)
    intent = base.read_json(intent_file)
    job = base.read_json(job_file)
    base.expect(request.get("target") == key and request.get("owner_recovery_authority_sha256") == recovery.RECOVERY_AUTH_SHA, "Recovery request binding changed")
    base.expect(intent.get("target") == key and intent.get("request_sha256") == base.sha(request_file) and intent.get("automatic_retries") == 0, "Recovery intent binding changed")
    request_id = job.get("request_id")
    base.expect(isinstance(request_id, str) and base.UUID_RE.fullmatch(request_id) is not None, "Fal request ID missing or malformed")
    return request, job, request_id


def status(key: str) -> dict:
    _, job, request_id = bound_job(key)
    url = job.get("status_url")
    base.expect(isinstance(url, str), "Fal status URL missing")
    response = base.api_call(url, key=base.key_from_env(), request_id=request_id)
    folder = base.output_dir(key)
    prior = sorted(folder.glob("SYNC-STATUS-[0-9][0-9][0-9][0-9].json"))
    output = folder / f"SYNC-STATUS-{len(prior)+1:04d}.json"
    base.write_json_x(output, {"at_utc": base.now(), "target": key, "request_id": request_id, "provider": response})
    return {"target": key, "status": response.get("status") if isinstance(response, dict) else None, "evidence": base.rel(output)}


def result(key: str) -> dict:
    _, job, request_id = bound_job(key)
    folder = base.output_dir(key)
    prior = sorted(folder.glob("SYNC-STATUS-[0-9][0-9][0-9][0-9].json"))
    base.expect(prior and (base.read_json(prior[-1]).get("provider") or {}).get("status") == "COMPLETED", "Fal job has no recorded COMPLETED status")
    output = folder / "SYNC-RESULT.json"
    base.expect(not output.exists(), "Fal result already fetched; no overwrite")
    url = job.get("response_url")
    base.expect(isinstance(url, str), "Fal response URL missing")
    response = base.api_call(url, key=base.key_from_env(), request_id=request_id)
    base.write_json_x(output, {"at_utc": base.now(), "target": key, "request_id": request_id, "provider": response, "accepted_for_picture": False, "owner_listening": "pending"})
    return {"target": key, "status": "result_preserved_pending_video_qc", "evidence": base.rel(output)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("status", "result"))
    parser.add_argument("target", choices=recovery.TARGETS)
    args = parser.parse_args()
    value = status(args.target) if args.command == "status" else result(args.target)
    print(base.json.dumps(value, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
