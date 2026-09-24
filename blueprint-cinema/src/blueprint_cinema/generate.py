"""Paid generation: one entry point for Higgsfield and fal jobs.

Every job is gated, capped, and ledgered before money moves:

- presenter jobs require an owner-locked look (presenter/LOOK-LOCK.json), and any
  image reference they send must be one of the locked references;
- if ledger/SPEND-LEDGER.json allocates a `<provider>_usd` cap to the lane, the
  job's estimate must fit under it;
- an intent row is appended to ledger/<lane>.jsonl before submit, and a done or
  failed row (job id, outputs, sha256) after.

Neither provider returns a per-job price, so `actual_usd` stays null and the
estimate is the reconciliation handle against the billing page.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .hashes import sha256_file, write_json_atomic
from .validation import ValidationFailure, load_json


LOOK_LOCK = Path("presenter") / "LOOK-LOCK.json"
SPEND_LEDGER = Path("ledger") / "SPEND-LEDGER.json"
IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp")
MEDIA_SUFFIXES = IMAGE_SUFFIXES + (".mp4", ".mov", ".webm", ".mp3", ".wav", ".m4a")

PROVIDERS = {
    "higgsfield": {
        "submit": "https://api.higgsfield.ai/{model}",
        "env": ("HF_KEY",),
        "done": {"completed"},
        "failed": {"failed", "nsfw", "canceled"},
    },
    "fal": {
        "submit": "https://queue.fal.run/{model}",
        "env": ("FAL_KEY", "FAL_API_KEY"),
        "done": {"COMPLETED"},
        "failed": set(),
    },
}

RequestJson = Callable[[str, str, dict | None], dict]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# --- presenter look lock -------------------------------------------------------


def lock_look(
    episode_dir: Path,
    references: list[tuple[Path, str]],
    location: str,
    outfit: str,
    locked_by: str,
    supersede_reason: str | None = None,
) -> dict:
    """Record the owner-selected presenter look. Re-locking is deliberate and costed."""
    if not references:
        raise ValidationFailure("look_lock", ["at least one --ref path=url is required"])
    errors = [f"reference file is missing: {path}" for path, _ in references if not path.is_file()]
    errors += [f"reference URL must be http(s): {url}" for _, url in references if not url.startswith("http")]
    if errors:
        raise ValidationFailure("look_lock", errors)

    lock_path = episode_dir / LOOK_LOCK
    history: list[dict] = []
    version = 1
    if lock_path.is_file():
        previous = load_json(lock_path)
        if not supersede_reason:
            spent = _presenter_jobs_since(episode_dir, previous["locked_at"])
            raise ValidationFailure(
                "look_lock",
                [
                    f"look v{previous['version']} was locked {previous['locked_at']} by {previous['locked_by']}",
                    f"{spent} presenter job(s) were generated against it and would be redone",
                    "re-run with --supersede \"<reason>\" if the owner is deliberately changing the look",
                ],
            )
        history = previous.get("history", []) + [
            {
                "version": previous["version"],
                "locked_at": previous["locked_at"],
                "location": previous["location"],
                "outfit": previous["outfit"],
                "superseded_at": utc_now(),
                "reason": supersede_reason,
                "presenter_jobs_orphaned": _presenter_jobs_since(episode_dir, previous["locked_at"]),
            }
        ]
        version = previous["version"] + 1

    lock = {
        "record_type": "presenter_look_lock",
        "version": version,
        "locked_at": utc_now(),
        "locked_by": locked_by,
        "location": location,
        "outfit": outfit,
        "references": [
            {
                "path": os.path.relpath(path.resolve(), episode_dir.resolve()),
                "sha256": sha256_file(path),
                "url": url,
            }
            for path, url in references
        ],
        "history": history,
    }
    write_json_atomic(lock_path, lock)
    return lock


def check_look_lock(episode_dir: Path, arguments: Any) -> dict:
    lock_path = episode_dir / LOOK_LOCK
    if not lock_path.is_file():
        raise ValidationFailure(
            "look_lock",
            [
                f"no presenter look lock at {lock_path}",
                "generate look candidates as stills, get the owner's pick, then run oe-cinema lock-look",
            ],
        )
    lock = load_json(lock_path)
    errors: list[str] = []
    for reference in lock["references"]:
        path = (episode_dir / reference["path"]).resolve()
        if not path.is_file():
            errors.append(f"locked reference is missing: {reference['path']}")
        elif sha256_file(path) != reference["sha256"]:
            errors.append(f"locked reference changed after lock: {reference['path']}")
    locked_urls = {reference["url"] for reference in lock["references"]}
    for url in _urls(arguments):
        if urllib.parse.urlparse(url).path.lower().endswith(IMAGE_SUFFIXES) and url not in locked_urls:
            errors.append(f"image reference is not part of the locked look: {url}")
    if errors:
        raise ValidationFailure("look_lock", errors)
    return lock


def _presenter_jobs_since(episode_dir: Path, since: str) -> int:
    return sum(
        1
        for row in _ledger_rows(episode_dir / "ledger" / "presenter.jsonl")
        if row.get("status") == "done" and row.get("at", "") >= since
    )


# --- spend ---------------------------------------------------------------------


def _ledger_rows(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _append(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        handle.write(json.dumps(row) + "\n")


def check_cap(episode_dir: Path, lane: str, provider: str, est_usd: float) -> str | None:
    spend_path = episode_dir / SPEND_LEDGER
    if not spend_path.is_file():
        return None
    cap = load_json(spend_path).get("lane_allocations", {}).get(lane, {}).get(f"{provider}_usd")
    if cap is None:
        return None
    committed = sum(
        row.get("est_usd") or 0
        for row in _ledger_rows(episode_dir / "ledger" / f"{lane}.jsonl")
        if row.get("status") == "intent" and row.get("provider") == provider
    )
    if committed + est_usd > cap:
        raise ValidationFailure(
            "spend_cap",
            [f"{lane} {provider} cap ${cap:.2f}: committed ${committed:.2f} + this ${est_usd:.2f} exceeds it"],
        )
    return f"{lane} {provider}: ${committed + est_usd:.2f} of ${cap:.2f} after this job"


# --- providers -----------------------------------------------------------------


def _api_key(provider: str) -> str:
    for name in PROVIDERS[provider]["env"]:
        if os.environ.get(name):
            return os.environ[name]
    raise ValidationFailure("credentials", [f"set {' or '.join(PROVIDERS[provider]['env'])}"])


def http_json(key: str) -> RequestJson:
    def request(method: str, url: str, body: dict | None) -> dict:
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.loads(response.read() or b"{}")
        except urllib.error.HTTPError as error:
            raise ValidationFailure("provider", [f"{method} {url} -> {error.code}: {error.read().decode()[:500]}"])

    return request


def run_job(
    provider: str,
    model: str,
    arguments: dict,
    request: RequestJson,
    poll_seconds: float = 5.0,
    timeout_seconds: float = 1800.0,
) -> tuple[str, dict]:
    spec = PROVIDERS[provider]
    submitted = request("POST", spec["submit"].format(model=model), arguments)
    job_id = submitted["request_id"]
    status_url = submitted["status_url"]
    deadline = time.monotonic() + timeout_seconds
    while True:
        status = request("GET", status_url, None)
        state = status.get("status")
        if state in spec["done"]:
            break
        if state in spec["failed"]:
            raise ValidationFailure("provider", [f"{provider} job {job_id} ended {state}: {json.dumps(status)[:500]}"])
        if time.monotonic() > deadline:
            raise ValidationFailure("provider", [f"{provider} job {job_id} still {state} after {timeout_seconds:.0f}s"])
        time.sleep(poll_seconds)
    # Higgsfield returns the result on the status URL; fal on a separate response URL.
    result = request("GET", submitted["response_url"], None) if provider == "fal" else status
    return job_id, result


def _urls(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if value.startswith(("http://", "https://")) else []
    if isinstance(value, dict):
        return [url for item in value.values() for url in _urls(item)]
    if isinstance(value, list):
        return [url for item in value for url in _urls(item)]
    return []


def output_urls(result: dict) -> list[str]:
    urls = [url for url in _urls(result) if urllib.parse.urlparse(url).path.lower().endswith(MEDIA_SUFFIXES)]
    return list(dict.fromkeys(urls))


def download(url: str, destination: Path) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as response:
        destination.write_bytes(response.read())
    return {"path": str(destination), "url": url, "sha256": sha256_file(destination)}


# --- entry point ---------------------------------------------------------------


def generate(
    episode_dir: Path,
    provider: str,
    model: str,
    arguments: dict,
    lane: str,
    item: str,
    reason: str,
    est_usd: float,
    out_dir: Path,
    dry_run: bool = False,
    request: RequestJson | None = None,
) -> dict:
    if provider not in PROVIDERS:
        raise ValidationFailure("generate", [f"unknown provider {provider}; use {', '.join(PROVIDERS)}"])
    lock = check_look_lock(episode_dir, arguments) if lane == "presenter" else None
    budget = check_cap(episode_dir, lane, provider, est_usd)
    plan = {
        "provider": provider,
        "model": model,
        "lane": lane,
        "item": item,
        "est_usd": est_usd,
        "look_version": lock["version"] if lock else None,
        "budget": budget,
    }
    if dry_run:
        return {"dry_run": True, **plan}

    ledger = episode_dir / "ledger" / f"{lane}.jsonl"
    base = {"lane": lane, "item": item, "provider": provider, "model": model, "look_version": plan["look_version"]}
    _append(ledger, {"at": utc_now(), **base, "est_usd": est_usd, "reason": reason, "arguments": arguments, "status": "intent"})
    started = time.monotonic()
    try:
        job_id, result = run_job(provider, model, arguments, request or http_json(_api_key(provider)))
        urls = output_urls(result)
        if not urls:
            raise ValidationFailure("provider", [f"no media URL in result: {json.dumps(result)[:500]}"])
        outputs = []
        for index, url in enumerate(urls):
            suffix = Path(urllib.parse.urlparse(url).path).suffix
            name = f"{item}{suffix}" if len(urls) == 1 else f"{item}-{index + 1:02d}{suffix}"
            outputs.append(download(url, out_dir / name))
        write_json_atomic(out_dir / f"{item}.result.json", result)
    except (ValidationFailure, OSError) as error:
        _append(ledger, {"at": utc_now(), **base, "status": "failed", "error": getattr(error, "errors", [str(error)])})
        raise
    row = {
        "at": utc_now(),
        **base,
        "status": "done",
        "job_id": job_id,
        "actual_usd": None,
        "seconds": round(time.monotonic() - started, 1),
        "outputs": outputs,
    }
    _append(ledger, row)
    return row
