"""Deterministic spoken-text, package, capture-plan, transcript, and state checks."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


SPOKEN_SCHEMA = "oe-spoken-text-v1"
PACKAGE_SCHEMA = "oe-narration-package-v1"
CAPTURE_PLAN_SCHEMA = "oe-capture-plan-v1"
TRANSCRIPT_SCHEMA = "oe-word-transcript-v1"
STATE_SCHEMA = "oe-narration-state-v1"


class ValidationError(Exception):
    """A fail-closed contract violation with all discovered reasons."""

    def __init__(self, errors: str | Iterable[str]):
        if isinstance(errors, str):
            errors = [errors]
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"JSON root must be an object: {path}")
    return value


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ValidationError(f"cannot hash {path}: {exc}") from exc
    return digest.hexdigest()


def canonical_w_bytes(tokens: list[str]) -> bytes:
    """Serialize W as UTF-8, one token per LF, including the final LF."""
    if not tokens:
        return b""
    return ("\n".join(tokens) + "\n").encode("utf-8")


def token_identity(tokens: list[str]) -> dict[str, Any]:
    return {
        "schema_version": SPOKEN_SCHEMA,
        "tokenization": "python-str-split-whitespace",
        "serialization": "utf8-one-token-per-lf-with-terminal-lf",
        "token_count": len(tokens),
        "sha256": sha256_bytes(canonical_w_bytes(tokens)),
    }


@dataclass(frozen=True)
class SpokenBlock:
    block_id: str
    start_token: int
    end_token: int
    tokens: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        identity = token_identity(list(self.tokens))
        return {
            "id": self.block_id,
            "start_token": self.start_token,
            "end_token": self.end_token,
            "token_count": len(self.tokens),
            "sha256": identity["sha256"],
            "authority": "subordinate_part",
        }


@dataclass(frozen=True)
class SpokenExtraction:
    script_sha256: str
    tokens: tuple[str, ...]
    blocks: tuple[SpokenBlock, ...]

    @property
    def identity(self) -> dict[str, Any]:
        return token_identity(list(self.tokens))

    def as_dict(self, script_path: str | None = None) -> dict[str, Any]:
        value: dict[str, Any] = {
            "schema_version": SPOKEN_SCHEMA,
            "script_sha256": self.script_sha256,
            "spoken_identity": self.identity,
            "blocks": [block.as_dict() for block in self.blocks],
        }
        if script_path is not None:
            value["script_path"] = script_path
        return value


_SCENE_RE = re.compile(r"^##\s+(S\d{2,}):")


def extract_step1_script(path: Path) -> SpokenExtraction:
    """Extract only `### Narration` bodies from ordered Step 1 scene blocks."""
    try:
        source_text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValidationError(f"cannot read Step 1 script {path}: {exc}") from exc
    if unicodedata.normalize("NFC", source_text) != source_text:
        raise ValidationError("locked script is not Unicode NFC; refuse silent identity drift")
    lines = source_text.splitlines()

    blocks_text: list[tuple[str, str]] = []
    current_scene: str | None = None
    narration_scene: str | None = None
    narration_lines: list[str] = []

    def finish_narration() -> None:
        nonlocal narration_scene, narration_lines
        if narration_scene is not None:
            body = "\n".join(narration_lines).strip()
            if body:
                blocks_text.append((narration_scene, body))
        narration_scene = None
        narration_lines = []

    for line in lines:
        scene_match = _SCENE_RE.match(line)
        if scene_match:
            finish_narration()
            current_scene = scene_match.group(1)
            continue
        if line.startswith("## "):
            finish_narration()
            current_scene = None
            continue
        if line.strip() == "### Narration":
            finish_narration()
            if current_scene is None:
                raise ValidationError("Narration heading appears outside a Step 1 scene")
            narration_scene = current_scene
            continue
        if line.startswith("### "):
            finish_narration()
            continue
        if narration_scene is not None:
            narration_lines.append(line)
    finish_narration()

    if not blocks_text:
        raise ValidationError("no Step 1 `### Narration` blocks found")
    seen: set[str] = set()
    tokens: list[str] = []
    blocks: list[SpokenBlock] = []
    for block_id, body in blocks_text:
        if block_id in seen:
            raise ValidationError(f"duplicate narrated scene: {block_id}")
        seen.add(block_id)
        artifact_patterns = {
            "merge-conflict marker": r"(?m)^(?:<<<<<<<|=======|>>>>>>>)",
            "placeholder": r"(?i)(?:\bTBD\b|\bTODO\b|\bTK\b|\{\{[^}]+\}\}|\[placeholder[^]]*\])",
            "HTML": r"</?[A-Za-z][^>]*>",
            "Markdown image": r"!\[[^]]*\]\([^)]*\)",
            "Markdown link": r"(?<!!)\[[^]]+\]\([^)]*\)",
            "footnote": r"\[\^[^]]+\]",
            "URL": r"https?://\S+",
            "inline direction": r"(?i)\[(?:pause|beat|emphasis|slow|faster|whisper|direction|pronounce)[^]]*\]",
        }
        for label, pattern in artifact_patterns.items():
            if re.search(pattern, body):
                raise ValidationError(f"narration block {block_id} contains forbidden {label}")
        block_tokens = body.split()
        start = len(tokens)
        tokens.extend(block_tokens)
        blocks.append(SpokenBlock(block_id, start, len(tokens), tuple(block_tokens)))
    return SpokenExtraction(sha256_file(path), tuple(tokens), tuple(blocks))


def extract_readthrough_tokens(path: Path) -> list[str]:
    """Extract the clean read-through body used by the v1.5 fixture."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ValidationError(f"cannot read read-through {path}: {exc}") from exc
    body: list[str] = []
    started = False
    for line in lines:
        if not started:
            stripped = line.strip()
            if not stripped or stripped.startswith("# ") or stripped.startswith("Status:"):
                continue
            started = True
        if line.startswith("## "):
            break
        body.append(line)
    tokens = "\n".join(body).split()
    if not tokens:
        raise ValidationError("read-through contains no spoken tokens")
    return tokens


def write_extraction(extraction: SpokenExtraction, out_dir: Path, script_path: Path) -> dict[str, Any]:
    if out_dir.exists() and any(out_dir.iterdir()):
        raise ValidationError(f"extraction output directory is not empty: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    w_path = out_dir / "canonical-w.txt"
    identity_path = out_dir / "spoken-identity.json"
    w_path.write_bytes(canonical_w_bytes(list(extraction.tokens)))
    # Keep the tracked identity receipt portable across worktrees. The locked
    # source is identified by its SHA-256 and the package manifest, not by a
    # machine-specific absolute path.
    identity = extraction.as_dict()
    identity["canonical_w_sha256"] = sha256_file(w_path)
    identity_path.write_text(json.dumps(identity, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "canonical_w": str(w_path),
        "identity": str(identity_path),
        "source_script": str(script_path),
        **identity,
    }


def read_canonical_w(path: Path) -> list[str]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ValidationError(f"cannot read canonical W {path}: {exc}") from exc
    if data and not data.endswith(b"\n"):
        raise ValidationError("canonical W must end with LF")
    try:
        text = data.decode("utf-8")
    except UnicodeError as exc:
        raise ValidationError("canonical W must be UTF-8") from exc
    tokens = text.splitlines()
    if any(not token or token != token.strip() or any(ch.isspace() for ch in token) for token in tokens):
        raise ValidationError("canonical W must contain exactly one non-empty whitespace-delimited token per line")
    if canonical_w_bytes(tokens) != data:
        raise ValidationError("canonical W has non-canonical line endings or serialization")
    return tokens


def _resolve_base(document_path: Path, document: dict[str, Any]) -> Path:
    base = document.get("base_dir", ".")
    if not isinstance(base, str) or not base:
        raise ValidationError("base_dir must be a non-empty string")
    base_path = Path(base)
    if base_path.is_absolute() or ".." in base_path.parts:
        raise ValidationError("base_dir must not be absolute or contain '..'")
    resolved = (document_path.parent / base_path).resolve()
    if not resolved.is_dir():
        raise ValidationError(f"base_dir does not exist: {resolved}")
    return resolved


def _safe_relative_path(value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label} must be a non-empty relative path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValidationError(f"{label} must not be absolute or contain '..'")
    return path


def _resolve_under_base(base: Path, value: Any, label: str) -> Path:
    relative = _safe_relative_path(value, label)
    resolved = (base / relative).resolve()
    if not resolved.is_relative_to(base):
        raise ValidationError(f"{label} escapes base_dir through a symlink")
    return resolved


def _manifest_roots(manifest_path: Path, manifest: dict[str, Any]) -> dict[str, Path]:
    roots_value = manifest.get("roots")
    errors: list[str] = []
    roots: dict[str, Path] = {}
    if not isinstance(roots_value, list) or not roots_value:
        raise ValidationError("roots must be a non-empty array of declared repository roots")
    for index, root in enumerate(roots_value):
        if not isinstance(root, dict):
            errors.append(f"roots[{index}] must be an object")
            continue
        root_id, raw_path = root.get("id"), root.get("path")
        if not isinstance(root_id, str) or not root_id or root_id in roots:
            errors.append(f"roots[{index}] has a missing or duplicate id")
            continue
        if not isinstance(raw_path, str) or not raw_path or Path(raw_path).is_absolute():
            errors.append(f"roots[{index}].path must be relative to the manifest")
            continue
        resolved = (manifest_path.parent / raw_path).resolve()
        if not resolved.is_dir():
            errors.append(f"declared root does not exist: {root_id} ({resolved})")
            continue
        if not (resolved / ".git").exists():
            errors.append(f"declared root is not a repository root: {root_id} ({resolved})")
            continue
        roots[root_id] = resolved
    if errors:
        raise ValidationError(errors)
    return roots


def _check_identity(actual: dict[str, Any], expected: Any, label: str, errors: list[str]) -> None:
    if not isinstance(expected, dict):
        errors.append(f"{label} identity must be an object")
        return
    for key in ("schema_version", "token_count", "sha256"):
        if expected.get(key) != actual.get(key):
            errors.append(f"{label} {key} mismatch: expected {expected.get(key)!r}, got {actual.get(key)!r}")


def verify_package(manifest_path: Path) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    errors: list[str] = []
    if manifest.get("schema_version") != PACKAGE_SCHEMA:
        errors.append(f"schema_version must be {PACKAGE_SCHEMA}")
    for forbidden in ("alternate_spoken_identity", "acoustic_identity", "alignment_identity"):
        if forbidden in manifest:
            errors.append(f"{forbidden} is forbidden; W is the only spoken-word authority")

    try:
        roots = _manifest_roots(manifest_path, manifest)
    except ValidationError as exc:
        errors.extend(exc.errors)
        roots = {}
    sources = manifest.get("sources")
    source_paths: dict[str, Path] = {}
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty array")
        sources = []
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"sources[{index}] must be an object")
            continue
        source_id = source.get("id")
        rel = source.get("path")
        root_id = source.get("root_id")
        expected_hash = source.get("sha256")
        if not isinstance(source_id, str) or not isinstance(rel, str) or not isinstance(root_id, str) or not isinstance(expected_hash, str):
            errors.append(f"sources[{index}] requires string id, root_id, path, and sha256")
            continue
        if source_id in source_paths:
            errors.append(f"duplicate source id: {source_id}")
            continue
        if root_id not in roots:
            errors.append(f"sources[{index}] references undeclared root_id {root_id!r}")
            continue
        try:
            safe_rel = _safe_relative_path(rel, f"sources[{index}].path")
        except ValidationError as exc:
            errors.extend(exc.errors)
            continue
        root_path = roots[root_id]
        resolved = (root_path / safe_rel).resolve()
        if not resolved.is_relative_to(root_path):
            errors.append(f"source escapes declared root through a symlink: {source_id}")
            continue
        source_paths[source_id] = resolved
        if not resolved.is_file():
            errors.append(f"source missing: {source_id} ({resolved})")
            continue
        actual_hash = sha256_file(resolved)
        if actual_hash != expected_hash:
            errors.append(f"source hash mismatch for {source_id}: expected {expected_hash}, got {actual_hash}")

    authority = manifest.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority must be an object")
        authority = {}
    script_id = authority.get("script_source_id")
    expected_identity = authority.get("spoken_identity")
    extraction: SpokenExtraction | None = None
    if isinstance(script_id, str) and script_id in source_paths and source_paths[script_id].is_file():
        extraction = extract_step1_script(source_paths[script_id])
        _check_identity(extraction.identity, expected_identity, "spoken", errors)
        expected_blocks = authority.get("block_ids")
        if expected_blocks is not None and expected_blocks != [b.block_id for b in extraction.blocks]:
            errors.append("narrated block IDs do not match the manifest")
        expected_block_count = authority.get("block_count")
        if expected_block_count is not None and expected_block_count != len(extraction.blocks):
            errors.append("narrated block count does not match the manifest")
    else:
        errors.append("authority.script_source_id does not resolve to a valid source")

    readthrough_id = authority.get("readthrough_source_id")
    if readthrough_id is not None:
        if not isinstance(readthrough_id, str) or readthrough_id not in source_paths or not source_paths[readthrough_id].is_file():
            errors.append("authority.readthrough_source_id does not resolve to a valid source")
        elif extraction is not None:
            readthrough_tokens = extract_readthrough_tokens(source_paths[readthrough_id])
            if readthrough_tokens != list(extraction.tokens):
                errors.append("read-through tokens are not exactly identical to canonical W")

    parts = manifest.get("derived_parts", [])
    if not isinstance(parts, list):
        errors.append("derived_parts must be an array")
        parts = []
    if extraction is not None:
        for index, part in enumerate(parts):
            if not isinstance(part, dict):
                errors.append(f"derived_parts[{index}] must be an object")
                continue
            if part.get("authority") != "subordinate_part":
                errors.append(f"derived_parts[{index}] must declare authority=subordinate_part")
            start, end = part.get("start_token"), part.get("end_token")
            if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start or end > len(extraction.tokens):
                errors.append(f"derived_parts[{index}] has an invalid token range")
                continue
            actual_part_hash = token_identity(list(extraction.tokens[start:end]))["sha256"]
            if part.get("sha256") != actual_part_hash:
                errors.append(f"derived_parts[{index}] hash mismatch")

    if errors:
        raise ValidationError(errors)
    assert extraction is not None
    return {
        "valid": True,
        "manifest_sha256": sha256_file(manifest_path),
        "source_count": len(source_paths),
        "block_count": len(extraction.blocks),
        "spoken_identity": extraction.identity,
    }


def validate_capture_plan(plan_path: Path, canonical_w_path: Path) -> dict[str, Any]:
    plan = read_json(plan_path)
    tokens = read_canonical_w(canonical_w_path)
    actual_identity = token_identity(tokens)
    errors: list[str] = []
    if plan.get("schema_version") != CAPTURE_PLAN_SCHEMA:
        errors.append(f"schema_version must be {CAPTURE_PLAN_SCHEMA}")
    _check_identity(actual_identity, plan.get("spoken_identity"), "spoken", errors)
    if plan.get("creative_approved") is True:
        errors.append("capture plans and automation may not set creative_approved")

    phase = plan.get("capture_phase")
    if phase not in {"calibration", "full"}:
        errors.append("capture_phase must be calibration or full")
    if "authorization" in plan:
        errors.append("provider authorization must be a separate hashed artifact, never embedded in the capture plan")
    if not isinstance(plan.get("script_sha256"), str) or not plan.get("script_sha256"):
        errors.append("script_sha256 is required")
    target = plan.get("target")
    if (
        not isinstance(target, dict)
        or target.get("kind") not in {"fixture", "episode"}
        or not isinstance(target.get("id"), str)
        or not target.get("id")
    ):
        errors.append("target requires kind fixture|episode and a non-empty id")
    bindings = plan.get("bindings")
    if not isinstance(bindings, dict):
        errors.append("bindings must freeze the N1, N2, and N3 artifacts")
        bindings = {}
    plan_base = plan_path.parent.resolve()
    for field in ("package_manifest", "performance_direction", "voice_capture_lock"):
        binding = bindings.get(field)
        if not isinstance(binding, dict):
            errors.append(f"bindings.{field} must be a path/hash object")
            continue
        expected_hash = binding.get("sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            errors.append(f"bindings.{field}.sha256 must be a lowercase SHA-256")
        try:
            bound_path = _resolve_under_base(plan_base, binding.get("path"), f"bindings.{field}.path")
        except ValidationError as exc:
            errors.extend(exc.errors)
            continue
        if not bound_path.is_file():
            errors.append(f"bindings.{field}.path is missing: {bound_path}")
        elif isinstance(expected_hash, str):
            actual_hash = sha256_file(bound_path)
            if actual_hash != expected_hash:
                errors.append(
                    f"bindings.{field} hash mismatch: expected {expected_hash}, got {actual_hash}"
                )

    provider = plan.get("provider")
    if not isinstance(provider, dict):
        errors.append("provider must be an object")
        provider = {}
    if provider.get("name") != "elevenlabs":
        errors.append("provider.name must be elevenlabs")
    for field in ("voice_id", "model_id"):
        if not isinstance(provider.get(field), str) or not provider.get(field):
            errors.append(f"provider.{field} is required")
    settings = provider.get("voice_settings")
    if not isinstance(settings, dict):
        errors.append("provider.voice_settings must be an object")

    policy = plan.get("format_policy")
    if not isinstance(policy, dict):
        errors.append("format_policy must be an object")
        policy = {}
    if policy.get("preferred") != "pcm_48000":
        errors.append("format_policy.preferred must be pcm_48000")
    if policy.get("fallback") != "mp3_44100_192":
        errors.append("the only permitted fallback is mp3_44100_192")
    if policy.get("fallback_requires") != "pcm_capability_unavailable":
        errors.append("MP3 fallback must require pcm_capability_unavailable")

    parts = plan.get("parts")
    if not isinstance(parts, list) or not parts:
        errors.append("parts must be a non-empty array")
        parts = []
    ranges: list[tuple[int, int]] = []
    modes: set[str] = set()
    part_ids: set[str] = set()
    for index, part in enumerate(parts):
        if not isinstance(part, dict):
            errors.append(f"parts[{index}] must be an object")
            continue
        part_id = part.get("id")
        if not isinstance(part_id, str) or not part_id or part_id in part_ids:
            errors.append(f"parts[{index}] has a missing or duplicate id")
        else:
            part_ids.add(part_id)
        start, end = part.get("start_token"), part.get("end_token")
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start or end > len(tokens):
            errors.append(f"parts[{index}] has an invalid token range")
            continue
        ranges.append((start, end))
        actual_hash = token_identity(tokens[start:end])["sha256"]
        if part.get("spoken_text_sha256") != actual_hash:
            errors.append(f"parts[{index}] spoken_text_sha256 mismatch")
        mode = part.get("calibration_mode")
        if isinstance(mode, str):
            modes.add(mode)
    if len(ranges) != len(set(ranges)):
        errors.append("duplicate capture ranges are forbidden")
    if phase == "full" and sorted(ranges) != _contiguous_ranges(len(tokens), sorted(ranges)):
        errors.append("full capture parts must cover canonical W exactly once, contiguously")
    if phase == "calibration":
        required_modes = {"cold_open", "evidence", "economics", "pronunciation"}
        missing = sorted(required_modes - modes)
        if missing:
            errors.append(f"calibration modes missing: {', '.join(missing)}")
    if errors:
        raise ValidationError(errors)
    return {
        "valid": True,
        "plan_sha256": sha256_file(plan_path),
        "capture_phase": phase,
        "part_count": len(parts),
        "spoken_identity": actual_identity,
    }


def _contiguous_ranges(total: int, ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    expected: list[tuple[int, int]] = []
    cursor = 0
    for start, end in ranges:
        if start != cursor:
            return []
        expected.append((start, end))
        cursor = end
    return expected if cursor == total else []


def validate_transcript(transcript_path: Path, canonical_w_path: Path, master_override: Path | None = None) -> dict[str, Any]:
    # Imported lazily to keep spoken-text validation independent of ffmpeg.
    from .audio import inspect_audio

    transcript = read_json(transcript_path)
    tokens = read_canonical_w(canonical_w_path)
    actual_identity = token_identity(tokens)
    errors: list[str] = []
    if transcript.get("schema_version") != TRANSCRIPT_SCHEMA:
        errors.append(f"schema_version must be {TRANSCRIPT_SCHEMA}")
    _check_identity(actual_identity, transcript.get("spoken_identity"), "spoken", errors)
    base = _resolve_base(transcript_path, transcript)
    master = transcript.get("master")
    if not isinstance(master, dict):
        errors.append("master must be an object")
        master = {}
    if master_override is not None:
        master_path = master_override.resolve()
    else:
        rel = master.get("path")
        try:
            master_path = _resolve_under_base(base, rel, "master.path")
        except ValidationError as exc:
            errors.extend(exc.errors)
            master_path = Path("__missing__")
    duration_ms = 0
    if not master_path.is_file():
        errors.append(f"master missing: {master_path}")
    else:
        actual_master_hash = sha256_file(master_path)
        if master.get("sha256") != actual_master_hash:
            errors.append("master hash mismatch; transcript is invalidated")
        try:
            audio = inspect_audio(master_path)
            duration_ms = round(audio["duration_seconds"] * 1000)
            if not audio["is_working_master"]:
                errors.append("transcript master must be PCM WAV, 48 kHz, 24-bit, mono")
        except ValidationError as exc:
            errors.extend(exc.errors)
    if not isinstance(master.get("duration_ms"), int) or master.get("duration_ms") != duration_ms:
        errors.append(f"master.duration_ms must equal inspected duration {duration_ms}")

    words = transcript.get("words")
    if not isinstance(words, list):
        errors.append("words must be an array")
        words = []
    if len(words) != len(tokens):
        errors.append(f"word count mismatch: expected {len(tokens)}, got {len(words)}")
    previous_end = 0
    for index, expected_token in enumerate(tokens):
        if index >= len(words):
            break
        word = words[index]
        if not isinstance(word, dict):
            errors.append(f"words[{index}] must be an object")
            continue
        if word.get("index") != index:
            errors.append(f"words[{index}].index must be {index}")
        if word.get("canonical_token") != expected_token:
            errors.append(f"words[{index}] token mismatch: expected {expected_token!r}, got {word.get('canonical_token')!r}")
        start, end = word.get("start_ms"), word.get("end_ms")
        if not isinstance(start, int) or not isinstance(end, int):
            errors.append(f"words[{index}] timing must use integer milliseconds")
        elif start < previous_end or start >= end or end > duration_ms:
            errors.append(f"words[{index}] has invalid or overlapping half-open timing")
        else:
            previous_end = end
        if word.get("review_state") != "approved":
            errors.append(f"words[{index}] has unresolved review state")
        if "w_id" in word and word.get("w_id") != f"w{index:06d}":
            errors.append(f"words[{index}].w_id must be w{index:06d}")
        alignment_parts = word.get("alignment_parts", [])
        if not isinstance(alignment_parts, list):
            errors.append(f"words[{index}].alignment_parts must be an array")
        else:
            alignment_end = start if isinstance(start, int) else 0
            for part_index, part in enumerate(alignment_parts):
                if not isinstance(part, dict):
                    errors.append(f"words[{index}].alignment_parts[{part_index}] must be an object")
                    continue
                part_start, part_end = part.get("start_ms"), part.get("end_ms")
                if (
                    not isinstance(part_start, int)
                    or not isinstance(part_end, int)
                    or part_start < alignment_end
                    or part_start >= part_end
                    or (isinstance(start, int) and part_start < start)
                    or (isinstance(end, int) and part_end > end)
                ):
                    errors.append(f"words[{index}].alignment_parts[{part_index}] has invalid subordinate timing")
                else:
                    alignment_end = part_end
    if transcript.get("unresolved_mismatches") not in (0, []):
        errors.append("transcript has unresolved lexical mismatches")
    if errors:
        raise ValidationError(errors)
    return {
        "valid": True,
        "technical_pass": True,
        "creative_approved": False,
        "transcript_sha256": sha256_file(transcript_path),
        "master_sha256": sha256_file(master_path),
        "duration_ms": duration_ms,
        "spoken_identity": actual_identity,
    }


def validate_state(state_path: Path) -> dict[str, Any]:
    state = read_json(state_path)
    errors: list[str] = []
    if state.get("schema_version") != STATE_SCHEMA:
        errors.append(f"schema_version must be {STATE_SCHEMA}")
    status = state.get("workflow_status")
    allowed_status = {"draft", "blocked", "returned_to_editorial", "abandoned", "in_progress", "locked"}
    if status not in allowed_status:
        errors.append("invalid workflow_status")
    gates = state.get("gates")
    if not isinstance(gates, dict):
        errors.append("gates must be an object")
        gates = {}
    allowed_results = {"pending", "passed", "failed", "invalidated"}
    for gate_id in (f"N{i}" for i in range(1, 8)):
        gate = gates.get(gate_id)
        if not isinstance(gate, dict) or gate.get("result") not in allowed_results:
            errors.append(f"{gate_id} must have result pending|passed|failed|invalidated")
    creative = state.get("creative_approval")
    if not isinstance(creative, dict):
        errors.append("creative_approval must be an object")
        creative = {}
    creative_approved = creative.get("approved") is True
    if creative_approved:
        if creative.get("set_by_type") != "human":
            errors.append("creative approval can only be set_by_type=human")
        for field in ("approved_by", "approved_at"):
            if not isinstance(creative.get(field), str) or not creative.get(field):
                errors.append(f"creative_approval.{field} is required")
    active_invalidations = state.get("active_invalidations")
    if not isinstance(active_invalidations, list):
        errors.append("active_invalidations must be an array")
        active_invalidations = ["invalid"]

    base = _resolve_base(state_path, state)
    identities = state.get("identities")
    if not isinstance(identities, dict):
        errors.append("identities must be an object")
        identities = {}
    else:
        for field in ("script_sha256", "spoken_text_sha256"):
            if not isinstance(identities.get(field), str) or not re.fullmatch(r"[0-9a-f]{64}", identities[field]):
                errors.append(f"identities.{field} must be a lowercase SHA-256")
    master = state.get("master")
    transcript = state.get("transcript")
    pause_map = state.get("intentional_pause_map")
    if master is not None and not isinstance(master, dict):
        errors.append("master must be an object or null")
    if transcript is not None and not isinstance(transcript, dict):
        errors.append("transcript must be an object or null")
    if pause_map is not None and not isinstance(pause_map, dict):
        errors.append("intentional_pause_map must be an object or null")
    if isinstance(master, dict) and isinstance(transcript, dict):
        master_path_value = master.get("path")
        transcript_path_value = transcript.get("path")
        try:
            master_path = _resolve_under_base(base, master_path_value, "master.path")
            transcript_path = _resolve_under_base(base, transcript_path_value, "transcript.path")
        except ValidationError as exc:
            errors.extend(exc.errors)
            master_path = transcript_path = Path("__missing__")
        if not master_path.is_file() or master.get("sha256") != (sha256_file(master_path) if master_path.is_file() else None):
            errors.append("master is missing or its hash changed; downstream state is invalidated")
        if not transcript_path.is_file() or transcript.get("sha256") != (sha256_file(transcript_path) if transcript_path.is_file() else None):
            errors.append("transcript is missing or its hash changed")
        if transcript.get("master_sha256") != master.get("sha256"):
            errors.append("transcript is not bound to the current master hash")
        if transcript.get("spoken_text_sha256") != identities.get("spoken_text_sha256"):
            errors.append("transcript is not bound to the current spoken-text identity")
        if isinstance(pause_map, dict):
            pause_path_value = pause_map.get("path")
            try:
                pause_path = _resolve_under_base(base, pause_path_value, "intentional_pause_map.path")
            except ValidationError as exc:
                errors.extend(exc.errors)
                pause_path = Path("__missing__")
            if not pause_path.is_file() or pause_map.get("sha256") != (sha256_file(pause_path) if pause_path.is_file() else None):
                errors.append("intentional pause map is missing or its hash changed")
            if pause_map.get("master_sha256") != master.get("sha256"):
                errors.append("intentional pause map is not bound to the current master hash")

    if status == "locked":
        if any(not isinstance(gates.get(f"N{i}"), dict) or gates[f"N{i}"].get("result") != "passed" for i in range(1, 8)):
            errors.append("locked state requires N1 through N7 passed")
        if state.get("technical_pass") is not True:
            errors.append("locked state requires technical_pass=true")
        if not creative_approved:
            errors.append("locked state requires explicit human creative approval")
        if active_invalidations:
            errors.append("locked state cannot have active invalidations")
        if not isinstance(master, dict) or not isinstance(transcript, dict) or not isinstance(pause_map, dict):
            errors.append("locked state requires master, transcript, and intentional_pause_map artifacts")
        origin = state.get("audio_origin")
        fallback_reason = state.get("fallback_reason")
        if origin not in {"native_pcm", "lossy_mp3"}:
            errors.append("locked state requires audio_origin native_pcm or lossy_mp3")
        if origin == "native_pcm" and fallback_reason is not None:
            errors.append("native_pcm origin requires fallback_reason=null")
        if origin == "lossy_mp3" and fallback_reason != "pcm_capability_unavailable":
            errors.append("lossy_mp3 origin requires fallback_reason=pcm_capability_unavailable")
    if errors:
        raise ValidationError(errors)
    return {
        "valid": True,
        "workflow_status": status,
        "technical_pass": state.get("technical_pass") is True,
        "creative_approved": creative_approved,
    }
