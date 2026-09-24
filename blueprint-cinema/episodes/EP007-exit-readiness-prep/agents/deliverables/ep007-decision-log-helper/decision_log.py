#!/usr/bin/env python3
"""Append-only local direction history. No renderer, provider, or approval actions."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

EPISODE = re.compile(r"EP[0-9]{3}-[a-z0-9]+(?:-[a-z0-9]+)*\Z")
SHA256 = re.compile(r"[a-f0-9]{64}\Z")
PAYLOAD_KEYS = {"event_id", "decision_id", "event_type", "tags", "data", "evidence"}
ENVELOPE_KEYS = {"episode_id", "captured_at", "previous_hash", "event_hash"}
VERDICTS = {"accept", "revise", "reject", "defer", "reopen", "unclear"}


class RecordError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise RecordError(message)


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label} must be nonempty text")
    return value


def mapping(value, label):
    require(isinstance(value, dict), f"{label} must be an object")
    return value


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


def event_hash(event):
    return hashlib.sha256(canonical({k: v for k, v in event.items() if k != "event_hash"})).hexdigest()


def inside(root, path):
    resolved = path.resolve()
    require(resolved.is_relative_to(root), f"Path escapes repository: {path}")
    return resolved


def evidence_path(root, value):
    text(value, "evidence.path")
    require(not value.startswith("/") and "\\" not in value and ":" not in value,
            f"Evidence path must be repo-relative: {value}")
    require(all(part not in {"", ".", ".."} for part in value.split("/")),
            f"Evidence path traversal or empty component: {value}")
    path = inside(root, root / value)
    require(path.exists() and stat.S_ISREG(path.stat().st_mode), f"Evidence is not a regular file: {value}")
    return path


def validate_evidence_shape(entries):
    require(isinstance(entries, list), "evidence must be a list")
    for entry in entries:
        mapping(entry, "evidence entry")
        require(set(entry) == {"path", "sha256", "locator"}, "Evidence requires only path, sha256 and locator")
        text(entry["path"], "evidence.path")
        text(entry["locator"], "evidence.locator")
        require(isinstance(entry["sha256"], str) and SHA256.fullmatch(entry["sha256"]), "Evidence sha256 is invalid")


def evidence_findings(events, root):
    root = Path(root).resolve()
    findings = []
    for event in events:
        bindings = [("evidence", entry) for entry in event["evidence"]]
        bindings += [("artifact", entry) for entry in event["data"].get("artifact_hashes", [])]
        for binding_type, entry in bindings:
            try:
                path = evidence_path(root, entry["path"])
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                if actual != entry["sha256"]:
                    findings.append({"event_id": event["event_id"], "binding_type": binding_type, "path": entry["path"],
                                     "status": "stale", "expected_sha256": entry["sha256"], "actual_sha256": actual})
            except (RecordError, OSError) as exc:
                findings.append({"event_id": event["event_id"], "binding_type": binding_type, "path": entry["path"], "status": "unavailable", "error": str(exc)})
    return findings


def artifact_hashes(value, label):
    require(isinstance(value, list), f"{label} must be an array of path/sha256 objects")
    paths_seen = set()
    for entry in value:
        mapping(entry, label + " entry")
        require(set(entry) == {"path", "sha256"}, f"{label} entries require only path and sha256")
        name = text(entry["path"], label + ".path")
        digest = entry["sha256"]
        require(name not in paths_seen, f"Duplicate artifact binding: {name}")
        paths_seen.add(name)
        require(isinstance(digest, str) and SHA256.fullmatch(digest), f"{label}.{name} must be a SHA256")


def validate_payload(event, seen, latest_decisions):
    mapping(event, "event")
    require(PAYLOAD_KEYS <= set(event), "Missing event envelope fields")
    require(set(event) <= PAYLOAD_KEYS | {"supersedes"}, "Unknown payload/envelope fields; capture fields are assigned by helper")
    event_id = text(event["event_id"], "event_id")
    decision_id = text(event["decision_id"], "decision_id")
    require(event_id not in seen, f"Duplicate event_id: {event_id}")
    kind = event["event_type"]
    require(kind in {"decision", "feedback", "verification", "lesson"}, "Invalid event_type")
    tags = event["tags"]
    require(isinstance(tags, list) and all(isinstance(t, str) and t.strip() for t in tags), "tags must be a list of nonempty strings")
    require(len(tags) == len(set(tags)), "Duplicate tags")
    validate_evidence_shape(event["evidence"])
    data = mapping(event["data"], "data")
    if kind == "decision":
        for key in ("choice", "reason"):
            text(data.get(key), f"data.{key}")
        context = mapping(data.get("context"), "data.context")
        for key in ("narrative_job", "viewer_before", "viewer_after"):
            text(context.get(key), f"data.context.{key}")
        alternatives = data.get("alternatives")
        require(isinstance(alternatives, list) and bool(alternatives), "At least one meaningful simpler alternative is required")
        for alternative in alternatives:
            mapping(alternative, "alternative")
            text(alternative.get("choice"), "alternative.choice")
            text(alternative.get("reason_not_selected"), "alternative.reason_not_selected")
        reuse = mapping(data.get("reuse"), "data.reuse")
        require(reuse.get("kind") in {"episode_specific", "conditional_precedent", "existing_authority", "technical_invariant"}, "Invalid reuse.kind")
        for key in ("applies_when", "avoid_when"):
            text(reuse.get(key), f"reuse.{key}")
        nuance = mapping(data.get("nuance"), "data.nuance")
        require(bool(nuance), "nuance must retain concrete direction details")
        if "cut_cues" in nuance:
            require(isinstance(nuance["cut_cues"], list), "cut_cues must be a list")
            for cue in nuance["cut_cues"]:
                mapping(cue, "cut cue")
                text(cue.get("cue_id"), "cut cue.cue_id")
                text(cue.get("phrase"), "cut cue.phrase")
                text(cue.get("relation"), "cut cue.relation")
        previous = latest_decisions.get(decision_id)
        if previous:
            require(event.get("supersedes") == previous["event_id"], "A revision must supersede the current decision event")
        else:
            require("supersedes" not in event, "Unknown supersedes: first decision cannot supersede an event")
    else:
        require("supersedes" not in event, "Only decisions may supersede a decision revision")
        if kind in {"feedback", "verification"}:
            target_id = text(data.get("decision_event_id"), "data.decision_event_id")
            target = seen.get(target_id)
            require(target is not None and target["event_type"] == "decision", "Unknown or non-decision feedback/verification target")
            require(target["decision_id"] == decision_id, "Feedback/verification target belongs to a different decision_id")
            text(data.get("scope"), "data.scope")
            artifact_hashes(data.get("artifact_hashes"), "data.artifact_hashes")
        if kind == "feedback":
            require(data.get("actor") in {"owner", "reviewer"}, "Feedback actor must be owner or reviewer")
            for key in ("verbatim", "interpretation"):
                text(data.get(key), f"data.{key}")
            require(data.get("verdict") in VERDICTS, "Invalid feedback verdict")
            if data["actor"] == "owner" and data["verdict"] == "accept":
                require(bool(data["artifact_hashes"]), "Owner acceptance must bind at least one exact artifact hash")
            if data["verdict"] == "defer":
                text(data.get("deferred_until"), "data.deferred_until")
        elif kind == "verification":
            text(data.get("method"), "data.method")
            require(data.get("result") in {"pass", "fail", "not_run"}, "Invalid verification result")
            text(data.get("limitations"), "data.limitations")
        else:
            for key in ("insight", "applies_when", "avoid_when"):
                text(data.get(key), f"data.{key}")
            require(data.get("confidence") in {"tentative", "supported", "repeated"}, "Invalid lesson confidence")
            require(data.get("status") == "candidate", "A lesson is only a candidate")


def validate_chain(events, episode):
    seen, latest, previous_hash = {}, {}, None
    for number, event in enumerate(events, 1):
        mapping(event, f"line {number}")
        require(ENVELOPE_KEYS <= set(event), f"Missing hash envelope at line {number}")
        require(event["episode_id"] == episode, f"Wrong episode at line {number}")
        require(event["previous_hash"] == previous_hash, f"Broken previous_hash at line {number}")
        require(isinstance(event["captured_at"], str), f"Missing captured_at at line {number}")
        try:
            captured = datetime.fromisoformat(event["captured_at"].replace("Z", "+00:00"))
            require(captured.tzinfo is not None, "captured_at must have a timezone")
        except ValueError as exc:
            raise RecordError(f"Invalid captured_at at line {number}") from exc
        require(event["event_hash"] == event_hash(event), f"Event hash mismatch at line {number}")
        payload = {k: v for k, v in event.items() if k not in ENVELOPE_KEYS}
        validate_payload(payload, seen, latest)
        seen[event["event_id"]] = event
        if event["event_type"] == "decision":
            latest[event["decision_id"]] = event
        previous_hash = event["event_hash"]
    return seen, latest


def load_events(path, episode):
    if not path.exists():
        return []
    require(not path.is_symlink() and path.is_file(), "Log must be a regular file, not a symlink")
    raw = path.read_bytes()
    if raw:
        require(raw.endswith(b"\n"), "Log ends with an incomplete line")
    events = []
    for number, line in enumerate(raw.splitlines(), 1):
        require(bool(line.strip()), f"Empty event line {number}")
        try:
            events.append(json.loads(line))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise RecordError(f"Invalid JSON at line {number}") from exc
    validate_chain(events, episode)
    return events


def paths(root, episode):
    require(isinstance(episode, str) and EPISODE.fullmatch(episode), "Invalid episode folder")
    root = Path(root).resolve()
    require(root.is_dir(), "Repository root must exist")
    directory = inside(root, root / "blueprint-cinema" / "episodes" / episode / "review" / "decisions")
    return root, directory, directory / "events.jsonl"


@contextmanager
def locked(directory):
    directory.mkdir(parents=True, exist_ok=True)
    lock_path = directory / ".events.lock"
    require(not lock_path.is_symlink(), "Lock may not be a symlink")
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(lock_path, flags, 0o600)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def append(root, episode, supplied):
    root, directory, path = paths(root, episode)
    batch = supplied if isinstance(supplied, list) else [supplied]
    require(bool(batch), "Append array cannot be empty")
    with locked(directory):
        inside(root, path)
        events = load_events(path, episode)
        seen, latest = validate_chain(events, episode)
        previous_hash = events[-1]["event_hash"] if events else None
        additions = []
        for candidate in batch:
            validate_payload(candidate, seen, latest)
            findings = evidence_findings([candidate], root)
            require(not findings, "Evidence validation failed: " + json.dumps(findings))
            event = dict(candidate, episode_id=episode,
                         captured_at=datetime.now(timezone.utc).isoformat(), previous_hash=previous_hash)
            event["event_hash"] = event_hash(event)
            additions.append(event)
            seen[event["event_id"]] = event
            if event["event_type"] == "decision":
                latest[event["decision_id"]] = event
            previous_hash = event["event_hash"]
        # Validate the entire proposed chain before any event bytes are appended.
        validate_chain(events + additions, episode)
        payload = b"".join(canonical(event) + b"\n" for event in additions)
        flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags, 0o600)
        original_size = os.fstat(fd).st_size
        try:
            require(os.write(fd, payload) == len(payload), "Incomplete append write")
            os.fsync(fd)
        except BaseException:
            # Roll back only this uncommitted tail; old event bytes are never rewritten.
            os.ftruncate(fd, original_size)
            os.fsync(fd)
            raise
        finally:
            os.close(fd)
        return {"appended": len(additions), "event_ids": [x["event_id"] for x in additions],
                "last_hash": previous_hash, "log_path": str(path)}


def latest_matching(events, decision_event_id, kind=None, actor=None):
    for event in reversed(events):
        if kind and event["event_type"] != kind:
            continue
        if event["data"].get("decision_event_id") != decision_event_id:
            continue
        if actor and event["data"].get("actor") != actor:
            continue
        return event
    return None


def decision_status(decision, events):
    owner = latest_matching(events, decision["event_id"], "feedback", "owner")
    reviewer = latest_matching(events, decision["event_id"], "feedback", "reviewer")
    verification = latest_matching(events, decision["event_id"], "verification")
    historical = decision["data"]["nuance"].get("source_basis") == "historical_reconstruction"
    review_state = "owner_" + owner["data"]["verdict"] + "_recorded" if owner else (
        "historical_reconstruction_no_new_owner_verdict" if historical else "no_owner_verdict_for_revision")
    return {"decision_id": decision["decision_id"], "latest_decision_event": decision,
            "record_kind": "historical_reconstruction" if historical else "current_decision",
            "review_state": review_state,
            "applicable_owner_feedback": owner, "reviewer_recommendation": reviewer,
            "latest_verification": verification,
            "deferred_until": owner["data"].get("deferred_until") if owner and owner["data"]["verdict"] == "defer" else None,
            "historical_reconstruction": historical,
            "canonical_approval": False}


def statuses(events, episode):
    _, latest = validate_chain(events, episode)
    return [decision_status(decision, events) for decision in latest.values()]


def query(events, episode, tags=None, query_text=None, limit=5):
    require(isinstance(limit, int) and 1 <= limit <= 1000, "limit must be between1 and1000")
    tags = {tag.casefold() for tag in (tags or [])}
    terms = (query_text or "").casefold().split()
    _, latest = validate_chain(events, episode)
    # Superseded choices retain negative examples and their own exact feedback.
    candidates = [e for e in events if e["event_type"] in {"decision", "lesson"}]
    positions = {event["event_id"]: i for i, event in enumerate(events)}
    results = []
    for event in candidates:
        matched = sorted(tags & {tag.casefold() for tag in event["tags"]})
        if tags and not matched:
            continue
        if terms and not all(term in json.dumps(event, ensure_ascii=False).casefold() for term in terms):
            continue
        data = event["data"]
        result = {"event": event, "tag_match_count": len(matched), "matched_tags": matched,
                  "context": data.get("context"), "applies_when": data.get("reuse", {}).get("applies_when", data.get("applies_when")),
                  "exceptions": data.get("reuse", {}).get("avoid_when", data.get("avoid_when")),
                  "is_current_revision": latest.get(event["decision_id"], {}).get("event_id") == event["event_id"],
                  "latest_feedback": latest_matching(events, event["event_id"], "feedback"),
                  "decision_status": decision_status(event, events) if event["event_type"] == "decision" else None}
        results.append(result)
    results.sort(key=lambda result: (result["tag_match_count"], positions[result["event"]["event_id"]]), reverse=True)
    return {"ranking": "tag_overlap_then_record_recency_only_not_creative_quality", "results": results[:limit]}


def infer_root():
    for parent in Path(__file__).resolve().parents:
        if (parent / "blueprint-cinema").is_dir() and (parent / ".agents").is_dir():
            return parent
    raise RecordError("Cannot infer repository root; provide --root")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("append", "query", "status", "validate"):
        command = sub.add_parser(name)
        command.add_argument("--episode", required=True)
        command.add_argument("--root", type=Path)
        if name == "append":
            command.add_argument("--event", type=Path, required=True)
        elif name == "query":
            command.add_argument("--tags", nargs="*", default=[])
            command.add_argument("--query")
            command.add_argument("--limit", type=int, default=5)
        elif name == "validate":
            command.add_argument("--evidence", action="store_true")
    args = parser.parse_args(argv)
    try:
        root, directory, path = paths(args.root or infer_root(), args.episode)
        if args.command == "append":
            result = append(root, args.episode, json.loads(args.event.read_text()))
        else:
            if directory.exists():
                with locked(directory):
                    events = load_events(path, args.episode)
            else:
                events = []
            if args.command == "status":
                result = {"episode_id": args.episode, "decisions": statuses(events, args.episode), "canonical_approval": False}
            elif args.command == "query":
                tags = [t.strip() for group in args.tags for t in group.split(",") if t.strip()]
                result = query(events, args.episode, tags, args.query, args.limit)
            else:
                findings = evidence_findings(events, root) if args.evidence else []
                result = {"episode_id": args.episode, "chain_valid": True, "event_count": len(events),
                          "evidence_checked": args.evidence, "evidence_findings": findings,
                          "evidence_current": not findings if args.evidence else None}
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return 1 if findings else 0
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (RecordError, OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
