#!/usr/bin/env python3
"""Fail-closed one-shot Fal Sync v3 runner for EP007 Shorts 03 and 04.

`check` is entirely local/read-only. `submit` creates immutable request and
intent evidence before one Fal POST. Existing evidence blocks any retry.
The two Higgsfield submissions that failed before job creation remain blocked.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = next(path for path in (HERE, *HERE.parents) if path.name == "operator-economy")
PLAN_PATH = HERE / "SYNC-PLAN-V1.json"
PLAN_SHA = "ca68601f8b036c22a8e369e4094abc0e00abb28be475f832adbb974fe7a37413"
MODEL = "fal-ai/sync-lipsync/v3"
SUBMIT_URL = f"https://queue.fal.run/{MODEL}"
ACCOUNT_PREFIX = "/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/"
AUDIO_HOST = "d2ol7oe51mr4n9.cloudfront.net"
VIDEO_HOST = "d8j0ntlcm91z4.cloudfront.net"
RATE_CENTS_PER_MINUTE = 800
MAX_SYNC_INTENTS = 4
MAX_FORECAST_CENTS = 1500
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
VIDEO_BASENAME_RE = re.compile(r"^hf_[0-9]{8}_[0-9]{6}_([0-9a-f-]{36})\.mp4$")
FAL_QUEUE_PATH_RE = re.compile(r"^/fal-ai/sync-lipsync/requests/([0-9a-f-]{36})(?:/status)?$")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(REPO))


def fail(message: str) -> None:
    raise SystemExit(message)


def expect(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_x(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
    except BaseException:
        raise


def bound_file(value: str, base: Path) -> Path:
    expect(isinstance(value, str), "Evidence path missing")
    path = (REPO / value).resolve()
    expect(path.is_relative_to(base.resolve()) and path.is_file(), f"Evidence missing or outside {rel(base)}: {value}")
    return path


def verified_ref(ref: dict[str, Any], base: Path) -> Path:
    expect(isinstance(ref, dict) and isinstance(ref.get("path"), str), "Evidence reference missing")
    path = bound_file(ref["path"], base)
    expect(ref.get("sha256") == sha(path), f"Evidence SHA changed: {rel(path)}")
    return path


def load_plan() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    expect(PLAN_PATH.is_file() and sha(PLAN_PATH) == PLAN_SHA, "Pinned Fal sync plan missing or changed")
    plan = read_json(PLAN_PATH)
    expect(plan.get("model") == MODEL and plan.get("sync_mode") == "silence", "Fal model or sync mode changed")
    expect(plan.get("submit_endpoint") == SUBMIT_URL, "Fal submit endpoint changed")
    scope = plan.get("runner_scope") or {}
    expect(scope.get("maximum_fal_submission_intents") == MAX_SYNC_INTENTS and scope.get("maximum_forecast_usd_including_all_prior_intents") == 15.0, "Runner limits changed")
    authority = plan.get("owner_authority") or {}
    owner = verified_ref(authority, REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions")
    event = read_json(owner)
    authorized = ((event.get("data") or {}).get("authorized") or {})
    limits = ((event.get("data") or {}).get("agent_execution_limits_not_owner_quoted") or {})
    expect("lip-sync if needed" in (authorized.get("stages") or []) and limits.get("fal_lip_sync_calls_max_if_needed") == 6, "Fal stage or owner call cap changed")
    expect(limits.get("fal_operational_spend_cap_usd") == 15 and limits.get("automatic_retries") == 0, "Owner spend/no-retry cap changed")
    batch_path = verified_ref(plan.get("higgsfield_batch_source_of_truth") or {}, REPO / "blueprint-cinema/experiments/EP007-SHORT03-PRESENTER-001")
    batch = read_json(batch_path)
    expect(batch.get("submitted_count") == 2 and batch.get("failed_count") == 2, "Higgsfield partial-batch snapshot changed")
    targets = plan.get("targets") or []
    expect(len(targets) == MAX_SYNC_INTENTS and len({row.get("key") for row in targets}) == MAX_SYNC_INTENTS, "Fal target set changed")
    expect(sum(float(row["audio_seconds"]) for row in targets) == 33.0, "Audio duration baseline changed")
    for row in targets:
        project = (REPO / row["project_dir"]).resolve()
        expect(project.is_relative_to((REPO / "blueprint-cinema/experiments").resolve()), "Target project escaped experiment scope")
        segdir = project / row["segment_dir"]
        expect(segdir.is_dir(), f"Target segment directory missing: {row['key']}")
        intent = segdir / "SUBMISSION-INTENT.json"
        expect(intent.is_file() and sha(intent) == row["higgsfield_generation_intent_sha256"], f"Higgsfield intent changed: {row['key']}")
        upload = project / "UPLOAD-RECEIPT-V1.json"
        expect(upload.is_file() and sha(upload) == row["audio_upload_receipt_sha256"], f"Audio upload receipt changed: {row['key']}")
        uploads = read_json(upload).get("uploads") or []
        matching = [item for item in uploads if item.get("media_id") == row["audio_media_id"]]
        expect(len(matching) == 1 and matching[0].get("byte_identical") is True and matching[0].get("source_sha256") == row["audio_local_sha256"], f"Audio upload not verified: {row['key']}")
        audio = bound_file(row["audio_local_path"], segdir)
        expect(sha(audio) == row["audio_local_sha256"], f"Local Original C audio changed: {row['key']}")
        expect(UUID_RE.fullmatch(row["audio_media_id"]) is not None, "Audio media ID malformed")
        batch_row = (batch.get("jobs") or [])[row["higgsfield_batch_index"]]
        expect(batch_row.get("job_id") == row["higgsfield_job_id"], f"Batch job ID changed: {row['key']}")
        expect((batch_row.get("status") == "pending") == (row["higgsfield_job_id"] is not None), f"Batch job state changed: {row['key']}")
    return plan, {row["key"]: row for row in targets}


def validate_url(url: str, *, host: str, suffix: str) -> urllib.parse.SplitResult:
    expect(isinstance(url, str), "Media URL missing")
    parsed = urllib.parse.urlsplit(url)
    expect(parsed.scheme == "https" and parsed.hostname == host and parsed.port in (None, 443), f"Unapproved {suffix} host")
    expect(not parsed.username and not parsed.password and not parsed.query and not parsed.fragment, f"{suffix} URL has credentials, query or fragment")
    expect(parsed.path.startswith(ACCOUNT_PREFIX) and parsed.path.endswith(suffix) and "%" not in parsed.path, f"Unapproved {suffix} URL path")
    return parsed


def audio_url(row: dict[str, Any]) -> str:
    url = f"https://{AUDIO_HOST}{ACCOUNT_PREFIX}{row['audio_media_id']}.mp3"
    validate_url(url, host=AUDIO_HOST, suffix=".mp3")
    return url


def validate_video_url(url: str, job_id: str) -> None:
    parsed = validate_url(url, host=VIDEO_HOST, suffix=".mp4")
    name = parsed.path.rsplit("/", 1)[-1]
    match = VIDEO_BASENAME_RE.fullmatch(name)
    expect(bool(match) and match.group(1) == job_id, "Video URL filename does not bind the exact Higgsfield job")


def local_video_probe(path: Path) -> dict[str, Any]:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,duration:format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, timeout=30, check=False,
    )
    expect(proc.returncode == 0, "Local generated video ffprobe failed")
    payload = json.loads(proc.stdout)
    streams = payload.get("streams") or []
    expect(len(streams) == 1, "Generated video must have one primary video stream")
    stream = streams[0]
    seconds = float(stream.get("duration") or (payload.get("format") or {}).get("duration"))
    expect(math.isfinite(seconds) and seconds > 0, "Generated video duration invalid")
    decoded = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0", "-f", "null", "-"],
        capture_output=True, text=True, timeout=120, check=False,
    )
    expect(decoded.returncode == 0 and not decoded.stderr.strip(), "Generated video failed independent full decode")
    return {"width": stream.get("width"), "height": stream.get("height"), "video_seconds": seconds}


def verify_video_and_need(row: dict[str, Any], video_url: str, plan: dict[str, Any]) -> tuple[Path, Path, float]:
    expect(row["higgsfield_job_id"] is not None, f"{row['key']} had no Higgsfield job; no Fal source and no retry authority")
    validate_video_url(video_url, row["higgsfield_job_id"])
    segdir = (REPO / row["project_dir"] / row["segment_dir"]).resolve()
    source_path = segdir / "VIDEO-SOURCE.json"
    expect(source_path.is_file(), f"{row['key']}: exact completed VIDEO-SOURCE.json missing")
    source = read_json(source_path)
    expect(source.get("short_id") == row["short_id"] and source.get("segment") == row["segment"], "VIDEO-SOURCE target mismatch")
    expect(source.get("status") == "completed" and source.get("job_id") == row["higgsfield_job_id"], "VIDEO-SOURCE is not the exact completed job")
    expect(source.get("result_url") == video_url, "Video URL differs from completed source")
    intent_hash = (source.get("generation_intent") or {}).get("sha256") or source.get("generation_intent_sha256")
    expect(intent_hash == row["higgsfield_generation_intent_sha256"], "VIDEO-SOURCE generation intent mismatch")
    # The pinned plan independently verifies the batch receipt, job index and
    # exact job ID; the source record binds that job and its generation intent.
    local_video = verified_ref(source.get("download") or {}, segdir)
    probe = local_video_probe(local_video)
    declared = (source.get("probe") or {}).get("video_duration_seconds")
    expect(isinstance(declared, (int, float)) and abs(float(declared) - probe["video_seconds"]) <= 0.15, "VIDEO-SOURCE duration differs from decoded local file")
    expect(probe["width"] == 1080 and probe["height"] == 1920, "Generated source is not native 1080x1920 portrait")
    expect(float(row["audio_seconds"]) - 0.2 <= probe["video_seconds"] <= float(row["requested_higgsfield_seconds"]) + 0.5, "Generated source duration outside approved clip bounds")
    expect((source.get("download") or {}).get("full_decode") == "pass", "Full generated-video decode not recorded as passed")
    need_path = segdir / "SYNC-NEED.json"
    expect(need_path.is_file(), f"{row['key']}: lip-sync necessity decision missing")
    need = read_json(need_path)
    expect(need.get("status") == "needed" and need.get("short_id") == row["short_id"] and need.get("segment") == row["segment"], "Lip-sync need not established for exact segment")
    expect(need.get("video_source_sha256") == sha(source_path) and isinstance(need.get("reason"), str) and len(need["reason"].strip()) >= 24, "Lip-sync need does not bind source and concrete reason")
    return source_path, need_path, probe["video_seconds"]


def output_dir(key: str) -> Path:
    return HERE / "targets" / key


def prior_forecast(current: str) -> tuple[int, int]:
    other_short02 = list((REPO / "blueprint-cinema/experiments").glob("EP007-SHORT02-PRESENTER-*/**/SYNC-SUBMISSION-INTENT.json"))
    expect(not other_short02, "Short02 Fal submission evidence appeared; reconcile the shared $15 cap before this runner continues")
    count = 0
    cents = 0
    for key in ("short03-a", "short03-b", "short04-a", "short04-b"):
        base = output_dir(key)
        intent = base / "SYNC-SUBMISSION-INTENT.json"
        if not intent.exists():
            continue
        expect(key != current, f"Existing intent blocks any retry for {key}")
        record = read_json(intent)
        expect(record.get("target") == key and record.get("automatic_retries") == 0, f"Prior Fal intent invalid: {key}")
        job = base / "SYNC-JOB.json"
        expect(job.is_file(), f"Prior Fal outcome uncertain: {key}; stop all further submissions")
        count += 1
        cents += int(record.get("forecast_cents", MAX_FORECAST_CENTS + 1))
    expect(count < MAX_SYNC_INTENTS, "Four-job Fal runner cap reached")
    return count, cents


def checked_spec(key: str, video_url: str) -> dict[str, Any]:
    plan, targets = load_plan()
    expect(key in targets, "Unknown target key")
    row = targets[key]
    source_path, need_path, seconds = verify_video_and_need(row, video_url, plan)
    prior_calls, prior_cents = prior_forecast(key)
    base = output_dir(key)
    existing = [name for name in ("SYNC-REQUEST.json", "SYNC-SUBMISSION-INTENT.json", "SYNC-JOB.json", "SYNC-ERROR.json", "SYNC-RESULT.json") if (base / name).exists()]
    expect(not existing, f"Existing Fal evidence blocks a new submission: {key}: {existing}")
    forecast_cents = math.ceil(max(seconds, float(row["audio_seconds"])) * RATE_CENTS_PER_MINUTE / 60)
    expect(prior_cents + forecast_cents <= MAX_FORECAST_CENTS, "Shared $15 operational forecast cap would be exceeded")
    return {
        "target": key,
        "short_id": row["short_id"],
        "segment": row["segment"],
        "model": MODEL,
        "endpoint": SUBMIT_URL,
        "input": {"video_url": video_url, "audio_url": audio_url(row), "sync_mode": "silence"},
        "video_source": {"path": rel(source_path), "sha256": sha(source_path), "decoded_seconds": seconds},
        "sync_need": {"path": rel(need_path), "sha256": sha(need_path)},
        "audio_source": {"path": row["audio_local_path"], "sha256": row["audio_local_sha256"], "media_id": row["audio_media_id"], "seconds": row["audio_seconds"]},
        "plan_sha256": PLAN_SHA,
        "prior_fal_intents": prior_calls,
        "prior_forecast_cents": prior_cents,
        "forecast_cents": forecast_cents,
        "aggregate_forecast_cents": prior_cents + forecast_cents,
        "cap_cents": MAX_FORECAST_CENTS,
        "provider_enforced_spend_cap": False,
        "network_called_by_check": False,
    }


def key_from_env() -> str:
    env = os.environ.get("FAL_KEY", "").strip()
    if env:
        return env
    env_file = REPO / ".env"
    expect(env_file.is_file(), "FAL_KEY unavailable; no intent was written")
    for line in env_file.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$", line)
        if match:
            value = match.group(1).strip().strip('"').strip("'")
            if value:
                return value
    fail("FAL_KEY unavailable; no intent was written")


def validate_fal_api_url(url: str, *, submission: bool = False, request_id: str | None = None) -> None:
    parsed = urllib.parse.urlsplit(url)
    expect(parsed.scheme == "https" and parsed.hostname == "queue.fal.run" and parsed.port in (None, 443), "Unapproved Fal API host")
    expect(not parsed.username and not parsed.password and not parsed.query and not parsed.fragment, "Fal URL has credentials, query or fragment")
    if submission:
        expect(url == SUBMIT_URL, "Fal submit endpoint changed")
    else:
        match = FAL_QUEUE_PATH_RE.fullmatch(parsed.path)
        expect(bool(match) and UUID_RE.fullmatch(match.group(1)) is not None and match.group(1) == request_id, "Fal queue URL is not bound to this request ID")


def api_call(url: str, *, key: str, body: dict[str, Any] | None = None, request_id: str | None = None) -> Any:
    validate_fal_api_url(url, submission=body is not None, request_id=request_id)
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Key " + key, "Content-Type": "application/json", "Accept": "application/json"},
        method="POST" if body is not None else "GET",
    )
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(request, timeout=45) as response:
        raw = response.read(4_000_000)
        expect(len(raw) < 4_000_000, "Fal response too large")
        return json.loads(raw)


def submit(key: str, video_url: str) -> dict[str, Any]:
    # Serialize the shared slate cap check and one POST; concurrent invocations
    # must not both pass against the same prior-intent count.
    lock_fd = os.open(HERE / ".sync-submit.lock", os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        return submit_locked(key, video_url)
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)


def submit_locked(key: str, video_url: str) -> dict[str, Any]:
    spec = checked_spec(key, video_url)
    secret = key_from_env()
    base = output_dir(key)
    request_path = base / "SYNC-REQUEST.json"
    intent_path = base / "SYNC-SUBMISSION-INTENT.json"
    job_path = base / "SYNC-JOB.json"
    write_json_x(request_path, spec)
    write_json_x(intent_path, {
        "record_type": "ep007_fal_sync_v3_one_shot_submission_intent_v1",
        "at_utc": now(), "target": key, "short_id": spec["short_id"], "segment": spec["segment"],
        "model": MODEL, "request_path": rel(request_path), "request_sha256": sha(request_path),
        "plan_sha256": PLAN_SHA, "video_source_sha256": spec["video_source"]["sha256"],
        "sync_need_sha256": spec["sync_need"]["sha256"], "forecast_cents": spec["forecast_cents"],
        "aggregate_forecast_cents": spec["aggregate_forecast_cents"], "owner_cap_cents": MAX_FORECAST_CENTS,
        "automatic_retries": 0, "provider_calls_before_this_intent": spec["prior_fal_intents"],
        "submission_state": "intent_persisted_before_one_POST",
        "program_audio_rule": "Continuous exact Original C master remains the only delivered voice; Fal audio is not program audio.",
    })
    try:
        response = api_call(SUBMIT_URL, key=secret, body=spec["input"])
    except BaseException as error:
        detail = str(error).replace(secret, "[REDACTED]")
        write_json_x(base / "SYNC-ERROR.json", {"at_utc": now(), "status": "uncertain_or_failed_no_retry", "error_class": type(error).__name__, "detail": detail[:2000]})
        fail(f"Fal submission outcome failed or uncertain for {key}; no retry")
    write_json_x(job_path, response)
    request_id = response.get("request_id") if isinstance(response, dict) else None
    expect(isinstance(request_id, str) and UUID_RE.fullmatch(request_id) is not None, "Fal returned an unrecognized job response; preserved, no retry")
    return {"target": key, "status": "submitted_pending_result", "request_id": request_id, "forecast_usd": spec["forecast_cents"] / 100}


def read_job(key: str) -> tuple[dict[str, Any], str]:
    _, targets = load_plan()
    expect(key in targets, "Unknown Fal target")
    base = output_dir(key)
    job_path = base / "SYNC-JOB.json"
    intent_path = base / "SYNC-SUBMISSION-INTENT.json"
    request_path = base / "SYNC-REQUEST.json"
    expect(intent_path.is_file() and request_path.is_file(), "Fal job lacks prior local submission intent/request")
    intent = read_json(intent_path)
    request = read_json(request_path)
    expect(intent.get("target") == key and intent.get("plan_sha256") == PLAN_SHA and intent.get("request_sha256") == sha(request_path), "Fal intent binding changed")
    expect(request.get("target") == key and request.get("plan_sha256") == PLAN_SHA, "Fal request binding changed")
    expect(job_path.is_file(), f"No Fal job recorded for {key}")
    job = read_json(job_path)
    request_id = job.get("request_id") if isinstance(job, dict) else None
    expect(isinstance(request_id, str) and UUID_RE.fullmatch(request_id) is not None, "Fal request ID missing or malformed")
    return job, request_id


def status(key: str) -> dict[str, Any]:
    job, request_id = read_job(key)
    url = job.get("status_url")
    expect(isinstance(url, str), "Fal status URL missing")
    secret = key_from_env()
    response = api_call(url, key=secret, request_id=request_id)
    base = output_dir(key)
    prior = sorted(base.glob("SYNC-STATUS-[0-9][0-9][0-9][0-9].json"))
    output = base / f"SYNC-STATUS-{len(prior)+1:04d}.json"
    write_json_x(output, {"at_utc": now(), "target": key, "request_id": request_id, "provider": response})
    return {"target": key, "status": response.get("status") if isinstance(response, dict) else None, "evidence": rel(output)}


def result(key: str) -> dict[str, Any]:
    job, request_id = read_job(key)
    base = output_dir(key)
    statuses = sorted(base.glob("SYNC-STATUS-[0-9][0-9][0-9][0-9].json"))
    expect(statuses and (read_json(statuses[-1]).get("provider") or {}).get("status") == "COMPLETED", "Fal job has no recorded COMPLETED status")
    result_path = base / "SYNC-RESULT.json"
    expect(not result_path.exists(), "Fal result already fetched; no overwrite")
    url = job.get("response_url")
    expect(isinstance(url, str), "Fal response URL missing")
    secret = key_from_env()
    response = api_call(url, key=secret, request_id=request_id)
    write_json_x(result_path, {"at_utc": now(), "target": key, "request_id": request_id, "provider": response, "accepted_for_picture": False, "owner_listening": "pending"})
    return {"target": key, "status": "result_preserved_pending_video_qc", "evidence": rel(result_path)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "submit", "status", "result"))
    parser.add_argument("target", choices=("short03-a", "short03-b", "short04-a", "short04-b"))
    parser.add_argument("--video-url", help="Exact URL from the matching completed Higgsfield job; required for check/submit")
    args = parser.parse_args()
    if args.command in ("check", "submit"):
        expect(bool(args.video_url), "--video-url is required")
        payload = checked_spec(args.target, args.video_url) if args.command == "check" else submit(args.target, args.video_url)
    elif args.command == "status":
        payload = status(args.target)
    else:
        payload = result(args.target)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, IndexError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        fail(str(error))
