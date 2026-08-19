#!/usr/bin/env python3
"""Small, fail-closed state ledger for the VO-first episode workflow."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


STAGES = [
    "script_locked",
    "vo_complete",
    "coverage_approved",
    "assets_selected",
    "rough_cut_approved",
    "visual_lock",
    "final_mix_complete",
]


def script_hash(script: Path) -> str:
    return hashlib.sha256(script.read_bytes()).hexdigest()


def state_path(script: Path) -> Path:
    return script.parent / "production_state.json"


def load(script: Path) -> dict:
    path = state_path(script)
    if not path.exists():
        return {"workflow": "vo-first-v1", "slug": script.parent.name, "stages": {}}
    return json.loads(path.read_text())


def save(script: Path, state: dict) -> None:
    state_path(script).write_text(json.dumps(state, indent=2) + "\n")


def complete(script: Path, stage: str) -> None:
    if stage not in STAGES:
        raise SystemExit(f"Unknown stage: {stage}")
    state = load(script)
    index = STAGES.index(stage)
    if index and not state.get("stages", {}).get(STAGES[index - 1], {}).get("complete"):
        raise SystemExit(f"BLOCKED: {STAGES[index - 1]} must be complete before {stage}.")
    if stage != "script_locked":
        locked = state.get("script_sha256")
        current = script_hash(script)
        if not locked or locked != current:
            raise SystemExit("BLOCKED: script.json changed after approval. Re-run lock-script before proceeding.")
    now = datetime.now(timezone.utc).isoformat()
    if stage == "script_locked":
        state["script_sha256"] = script_hash(script)
        # A newly locked script invalidates every downstream approval.
        state["stages"] = {}
    state.setdefault("stages", {})[stage] = {"complete": True, "completed_at": now}
    state["current_stage"] = stage
    save(script, state)
    print(f"✓ {stage}: {state_path(script)}")


def require(script: Path, stage: str) -> None:
    state = load(script)
    if not state.get("stages", {}).get(stage, {}).get("complete"):
        raise SystemExit(f"BLOCKED: {stage} is not complete for {script.parent.name}.")
    if state.get("script_sha256") != script_hash(script):
        raise SystemExit("BLOCKED: script.json changed after approval. Re-run lock-script.")
    print(f"✓ required stage present: {stage}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    for name in ("complete", "require"):
        cmd = sub.add_parser(name)
        cmd.add_argument("script")
        cmd.add_argument("stage", choices=STAGES)
    status = sub.add_parser("status")
    status.add_argument("script")
    args = ap.parse_args()
    script = Path(args.script)
    if args.command == "complete":
        complete(script, args.stage)
    elif args.command == "require":
        require(script, args.stage)
    else:
        state = load(script)
        print(json.dumps(state, indent=2))
        if state.get("script_sha256") and state["script_sha256"] != script_hash(script):
            print("\nSTALE: script.json differs from the locked hash.")


if __name__ == "__main__":
    main()
