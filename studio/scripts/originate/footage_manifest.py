#!/usr/bin/env python3
"""Create, validate, and review the shared long-form footage manifest."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import subprocess
from datetime import date
from pathlib import Path

ROLES = {"human_context", "market_force", "proof", "process", "outcome"}
FACE_STATES = {"cleared", "not_applicable", "needs_review"}


def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_local_path(entry: dict, episode_dir: Path) -> Path | None:
    raw = entry.get("local_path")
    if not raw:
        return None
    path = Path(raw).expanduser()
    return path if path.is_absolute() else episode_dir / path


def media_duration(path: Path) -> float:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    if proc.returncode:
        raise ValueError(f"ffprobe failed for {path}: {proc.stderr.strip()}")
    return float(proc.stdout.strip())


def entry_index(manifest: dict) -> dict[str, dict]:
    return {entry["id"]: entry for entry in manifest.get("entries", []) if entry.get("id")}


def resolve_entry(manifest: dict, section: str, beat: int, asset: dict,
                  screen_id: str | None = None) -> dict | None:
    explicit = asset.get("manifest_id") or asset.get("footage_id")
    if explicit:
        return entry_index(manifest).get(explicit)
    if screen_id:
        by_screen = next((e for e in manifest.get("entries", [])
                          if e.get("screen_id") == screen_id), None)
        if by_screen:
            return by_screen
    return next((e for e in manifest.get("entries", [])
                 if e.get("section") == section and e.get("beat") == beat), None)


def validate_entry(entry: dict, episode_dir: Path, require_file: bool = True) -> list[str]:
    errors: list[str] = []
    label = entry.get("id", "<missing id>")
    required = ("id", "role", "narration_anchor", "provider", "license",
                "license_checked_at", "downloaded_at", "faces_review")
    for key in required:
        if not entry.get(key):
            errors.append(f"{label}: missing {key}")
    if entry.get("role") not in ROLES:
        errors.append(f"{label}: invalid role {entry.get('role')!r}")
    if entry.get("faces_review") not in FACE_STATES:
        errors.append(f"{label}: faces_review must be one of {sorted(FACE_STATES)}")
    if entry.get("faces_review") == "needs_review" and entry.get("approved"):
        errors.append(f"{label}: cannot approve while faces_review=needs_review")
    if not entry.get("approved"):
        errors.append(f"{label}: entry is not approved")
    path = resolve_local_path(entry, episode_dir)
    if require_file and (path is None or not path.is_file()):
        errors.append(f"{label}: local_path does not resolve to a file")
        return errors
    if path and path.is_file():
        try:
            duration = media_duration(path)
            source_in = float(entry.get("source_in", 0))
            source_out = float(entry.get("source_out", duration))
            if source_in < 0 or source_out <= source_in or source_out > duration + 0.05:
                errors.append(
                    f"{label}: invalid source range {source_in:.2f}-{source_out:.2f}s "
                    f"for {duration:.2f}s media")
        except (ValueError, TypeError) as exc:
            errors.append(f"{label}: {exc}")
        expected_hash = entry.get("sha256")
        if not expected_hash:
            errors.append(f"{label}: missing sha256")
        elif file_sha256(path) != expected_hash:
            errors.append(f"{label}: sha256 does not match local file")
    return errors


def validate_manifest(manifest: dict, episode_dir: Path, require_files: bool = True) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append("manifest: schema_version must be 1")
    ids = [e.get("id") for e in manifest.get("entries", [])]
    if len(ids) != len(set(ids)):
        errors.append("manifest: entry ids must be unique")
    for entry in manifest.get("entries", []):
        errors.extend(validate_entry(entry, episode_dir, require_files))
    return errors


def build_manifest(script_path: Path) -> dict:
    episode_dir = script_path.parent
    script = load_json(script_path)
    assets = load_json(episode_dir / "assets.json")
    storyboard_path = episode_dir / "storyboard.json"
    storyboard = None
    if storyboard_path.exists():
        storyboard = load_json(storyboard_path)
    beats = {(s["id"], b["beat"]): b for s in script["sections"] for b in s.get("beats", [])}
    entries = []
    if storyboard is not None:
        for screen in storyboard.get("screens", []):
            if screen.get("layout") != "broll" or not screen.get("reveals"):
                continue
            reveal = screen["reveals"][0]
            sid, beat = screen["section"], reveal["beat"]
            source_beat = beats.get((sid, beat), {})
            footage_id = f"{script['slug']}-{screen['id']}"
            query = (screen.get("search_query") or
                     (screen.get("custom") or {}).get("search_query") or
                     reveal.get("body") or reveal.get("title") or "")
            entries.append({
                "id": footage_id, "screen_id": screen["id"], "section": sid, "beat": beat,
                "role": screen.get("footage_role") or screen.get("preview_role", "human_context"),
                "narration_anchor": source_beat.get("vo_text", "")[:160],
                "preview_eligible": bool(screen.get("preview_eligible") or screen.get("start", 999) < 30),
                "query_variants": screen.get("query_variants") or (screen.get("custom") or {}).get("query_variants") or [query],
                "approved": False, "provider": "", "asset_id": "", "page_url": "",
                "creator": "", "license": "", "license_checked_at": "",
                "downloaded_at": "", "local_path": "", "sha256": "",
                "faces_review": "needs_review", "synthetic": False,
                "source_in": 0, "source_out": None, "crop": "cover",
                "focal_point": (screen.get("custom") or {}).get("focal_point", "center"),
            })
    else:
        for section in assets.get("sections", []):
          for item in section.get("assets", []):
            spec = item.get("spec", {})
            sid, beat = section["id"], item["beat"]
            if spec.get("type") != "broll":
                continue
            source_beat = beats.get((sid, beat), {})
            footage_id = f"{script['slug']}-{sid}-{beat:02d}"
            spec["manifest_id"] = footage_id
            entries.append({
                "id": footage_id,
                "section": sid,
                "beat": beat,
                "role": spec.get("role", "human_context"),
                "narration_anchor": source_beat.get("vo_text", "")[:160],
                "preview_eligible": False,
                "query_variants": spec.get("query_variants") or [spec.get("search_query", "")],
                "approved": False,
                "provider": "",
                "asset_id": "",
                "page_url": "",
                "creator": "",
                "license": "",
                "license_checked_at": "",
                "downloaded_at": "",
                "local_path": "",
                "sha256": "",
                "faces_review": "needs_review",
                "synthetic": False,
                "source_in": 0,
                "source_out": None,
                "crop": "cover",
                "focal_point": "center",
            })
    with (episode_dir / "assets.json").open("w") as f:
        json.dump(assets, f, indent=2)
        f.write("\n")
    return {
        "schema_version": 1,
        "episode": script["slug"],
        "created_at": date.today().isoformat(),
        "enforce_preview_gate": True,
        "entries": entries,
    }


def build_review(manifest: dict, episode_dir: Path) -> str:
    rows = []
    for e in manifest.get("entries", []):
        path = resolve_local_path(e, episode_dir)
        state = "READY" if e.get("approved") and path and path.is_file() else "BLOCKED"
        rows.append(
            "<tr>" + "".join(f"<td>{html.escape(str(v))}</td>" for v in (
                state, e.get("id", ""), e.get("role", ""),
                e.get("narration_anchor", ""), " · ".join(e.get("query_variants", [])),
                e.get("provider", ""), e.get("license", ""), e.get("faces_review", ""),
                e.get("local_path", ""),
            )) + "</tr>")
    return """<!doctype html><html><head><meta charset="utf-8"><title>Footage review</title>
<style>body{font:14px system-ui;margin:32px;background:#f5f0e6;color:#171714}table{border-collapse:collapse;width:100%;background:#fff}th,td{border:1px solid #c8c0b2;padding:9px;vertical-align:top}th{background:#14263e;color:#fff;text-align:left}td:first-child{font-weight:700}</style></head><body>
<h1>Episode footage review</h1><p>Approve semantic match, rights, faces, source range, and crop before rendering.</p>
<table><thead><tr><th>State</th><th>ID</th><th>Role</th><th>Narration</th><th>Queries</th><th>Provider</th><th>License</th><th>Faces</th><th>File</th></tr></thead>
<tbody>""" + "".join(rows) + "</tbody></table></body></html>"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "validate", "review"))
    parser.add_argument("script", help="Path to episode script.json")
    parser.add_argument("--no-files", action="store_true", help="Skip local media checks")
    args = parser.parse_args()
    script_path = Path(args.script).resolve()
    episode_dir = script_path.parent
    manifest_path = episode_dir / "footage_manifest.json"
    if args.command == "init":
        if manifest_path.exists():
            existing = load_json(manifest_path)
            planned = build_manifest(script_path)
            old_by_id = entry_index(existing)
            # Storyboard is authoritative for the required footage beats;
            # reviewed selections survive when their stable screen id survives.
            manifest = {
                **planned,
                "created_at": existing.get("created_at", planned["created_at"]),
                "entries": [
                    {
                        **entry,
                        **old_by_id.get(entry["id"], {}),
                        # Storyboard-owned planning fields must evolve even
                        # after a candidate has been reviewed. Selection and
                        # rights fields above survive; the production brief
                        # below stays current.
                        **{key: entry[key] for key in (
                            "screen_id", "section", "beat", "role",
                            "narration_anchor", "preview_eligible",
                            "query_variants", "crop", "focal_point",
                        ) if key in entry},
                    }
                    for entry in planned["entries"]
                ],
            }
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
            added = len(set(entry_index(manifest)) - set(old_by_id))
            retired = len(set(old_by_id) - set(entry_index(manifest)))
            print(f"Synced {manifest_path}: {len(manifest['entries'])} required, "
                  f"{added} added, {retired} retired")
        else:
            manifest = build_manifest(script_path)
            if not manifest["entries"]:
                print("No b-roll assets; footage manifest not required")
                return
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
            print(f"Created {manifest_path} with {len(manifest['entries'])} footage beats")
    else:
        if not manifest_path.exists():
            raise SystemExit(f"Missing {manifest_path}; run init first")
        manifest = load_json(manifest_path)
    if args.command in {"init", "review"}:
        review = episode_dir / "footage_review.html"
        review.write_text(build_review(manifest, episode_dir))
        print(f"Wrote {review}")
    if args.command == "validate":
        errors = validate_manifest(manifest, episode_dir, not args.no_files)
        if errors:
            print("FOOTAGE GATE: BLOCKED")
            for error in errors:
                print(f"- {error}")
            raise SystemExit(1)
        print(f"FOOTAGE GATE: PASS ({len(manifest.get('entries', []))} entries)")


if __name__ == "__main__":
    main()
