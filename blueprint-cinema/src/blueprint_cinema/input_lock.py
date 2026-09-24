from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from . import WORKFLOW_VERSION
from .hashes import sha256_file, write_json_atomic
from .paths import REPO_ROOT, EpisodeIdentity, repo_relative


class InputLockError(ValueError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def probe_duration(path: Path) -> float:
    executable = shutil.which("ffprobe")
    if not executable:
        raise InputLockError("ffprobe is required but was not found on PATH")
    result = subprocess.run(
        [
            executable,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise InputLockError(f"ffprobe failed for {path}: {result.stderr.strip()}")
    try:
        return round(float(result.stdout.strip()), 6)
    except ValueError as error:
        raise InputLockError(f"ffprobe returned an invalid duration for {path}") from error


def _artifact(
    path: Path,
    role: str,
    locked_at: str,
    *,
    section_id: str | None = None,
    duration_seconds: float | None = None,
) -> dict:
    if not path.is_file():
        raise InputLockError(f"required upstream artifact is missing: {path}")
    value = {
        "path": repo_relative(path),
        "role": role,
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
        "locked_at": locked_at,
    }
    if section_id is not None:
        value["section_id"] = section_id
    if duration_seconds is not None:
        value["duration_seconds"] = duration_seconds
    return value


def build_input_lock(identity: EpisodeIdentity, project: dict) -> dict:
    locked_at = utc_now()
    upstream = (REPO_ROOT / project["upstream_workspace"]).resolve()
    expected_upstream = (REPO_ROOT / "studio" / "originate" / identity.slug).resolve()
    if upstream != expected_upstream:
        raise InputLockError(
            f"upstream workspace must resolve to {repo_relative(expected_upstream)}"
        )

    script_path = upstream / "script.json"
    full_audio_path = upstream / "vo" / "full-episode.mp3"
    words_path = upstream / "vo" / "words.json"
    timeline_path = upstream / "vo" / "timeline.json"
    approval_path = upstream / "production_state.json"

    for required in (script_path, full_audio_path, words_path, timeline_path, approval_path):
        if not required.is_file():
            raise InputLockError(f"required upstream artifact is missing: {required}")

    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    approved_script_hash = approval.get("script_sha256")
    current_script_hash = sha256_file(script_path)
    if approved_script_hash != current_script_hash:
        raise InputLockError(
            "current script hash does not match the upstream approved script hash"
        )

    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
    words = json.loads(words_path.read_text(encoding="utf-8"))
    if not isinstance(words, list) or not words:
        raise InputLockError("vo/words.json must be a non-empty word array")
    if not isinstance(timeline.get("sections"), list) or not timeline["sections"]:
        raise InputLockError("vo/timeline.json must contain non-empty sections")

    full_duration = probe_duration(full_audio_path)
    declared_duration = float(timeline.get("total_seconds", -1))
    if abs(full_duration - declared_duration) > 0.05:
        raise InputLockError(
            f"assembled VO duration {full_duration:.3f}s disagrees with timeline "
            f"{declared_duration:.3f}s"
        )

    artifacts = [
        _artifact(script_path, "script", locked_at),
        _artifact(
            full_audio_path,
            "assembled_vo",
            locked_at,
            duration_seconds=full_duration,
        ),
    ]
    expected_start = 0.0
    seen_sections: set[str] = set()
    for section in timeline["sections"]:
        section_id = section.get("section")
        audio_name = section.get("audio")
        if not isinstance(section_id, str) or not section_id:
            raise InputLockError("timeline section is missing a stable section ID")
        if section_id in seen_sections:
            raise InputLockError(f"duplicate timeline section: {section_id}")
        seen_sections.add(section_id)
        if Path(str(audio_name)).name != audio_name or not str(audio_name).endswith(".mp3"):
            raise InputLockError(f"invalid mastered section audio path: {audio_name}")
        start = float(section.get("start", -1))
        duration = float(section.get("duration", -1))
        if abs(start - expected_start) > 0.01 or duration <= 0:
            raise InputLockError(
                f"timeline section {section_id} is not contiguous at {expected_start:.3f}s"
            )
        audio_path = upstream / "vo" / audio_name
        actual_duration = probe_duration(audio_path)
        if abs(actual_duration - duration) > 0.05:
            raise InputLockError(
                f"mastered section {section_id} duration {actual_duration:.3f}s "
                f"disagrees with timeline {duration:.3f}s"
            )
        artifacts.append(
            _artifact(
                audio_path,
                "mastered_section",
                locked_at,
                section_id=section_id,
                duration_seconds=actual_duration,
            )
        )
        expected_start = round(start + duration, 6)
    if abs(expected_start - full_duration) > 0.05:
        raise InputLockError("mastered section assembly does not end at the full VO duration")

    previous_end = -1.0
    timeline_section_ids = {section["section"] for section in timeline["sections"]}
    for index, word in enumerate(words):
        start = float(word.get("start", -1))
        end = float(word.get("end", -1))
        if start < 0 or end < start or end > full_duration + 0.001:
            raise InputLockError(f"word {index} has invalid timing bounds")
        if start + 0.05 < previous_end:
            raise InputLockError(f"word {index} moves backward in time")
        if word.get("section") not in timeline_section_ids:
            raise InputLockError(f"word {index} references an unknown timeline section")
        previous_end = end

    artifacts.extend(
        [
            _artifact(words_path, "word_transcript", locked_at),
            _artifact(timeline_path, "timeline", locked_at),
        ]
    )
    return {
        "$schema": "../../schemas/input-lock.schema.json",
        "schema_version": "1.0.0",
        "workflow_version": WORKFLOW_VERSION,
        **identity.as_dict(),
        "upstream_workspace": repo_relative(upstream) + "/",
        "approved_script_sha256": approved_script_hash,
        "audio_duration_seconds": full_duration,
        "locked_at": locked_at,
        "artifacts": artifacts,
    }


def source_path(artifact: dict) -> Path:
    return (REPO_ROOT / artifact["path"]).resolve()


def stage_locked_audio(lock: dict, destination: Path) -> Path:
    artifact = next(
        (item for item in lock["artifacts"] if item["role"] == "assembled_vo"), None
    )
    if artifact is None:
        raise InputLockError("input lock has no assembled VO")
    source = source_path(artifact)
    if sha256_file(source) != artifact["sha256"]:
        raise InputLockError("assembled VO hash changed; refusing to stage audio")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    if sha256_file(destination) != artifact["sha256"]:
        destination.unlink(missing_ok=True)
        raise InputLockError("staged audio failed hash verification")
    return destination

