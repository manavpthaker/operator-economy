from __future__ import annotations

from pathlib import Path

from . import WORKFLOW_VERSION
from .hashes import sha256_file, write_json_atomic
from .paths import EpisodeIdentity
from .validation import validate_schema


PALETTE = {
    "ink": "#1A1A1A",
    "paper": "#F5F0E6",
    "schematic_navy": "#14263E",
    "drafting_blue": "#1F3A5F",
    "ledger_gold": "#C4A45F",
    "sage": "#7B9E87",
    "negative": "#9B3E2E",
}


def compile_render_data(
    identity: EpisodeIdentity,
    episode_path: Path,
    lock: dict,
    world: dict,
    plan: dict,
    tickets: dict,
) -> dict:
    source_files = {
        "input_lock": episode_path / "input-lock.json",
        "episode_engine": episode_path / "episode-engine.json",
        "world": episode_path / "world.json",
        "visual_plan": episode_path / "visual-plan.json",
        "asset_tickets": episode_path / "asset-tickets.json",
    }
    audio_artifact = next(
        item for item in lock["artifacts"] if item["role"] == "assembled_vo"
    )
    source_hashes = {name: sha256_file(path) for name, path in source_files.items()}
    source_hashes["assembled_vo"] = audio_artifact["sha256"]
    data = {
        "schema_version": "1.0.0",
        "workflow_version": WORKFLOW_VERSION,
        "episode": identity.as_dict(),
        "duration_seconds": lock["audio_duration_seconds"],
        "fps": 30,
        "width": 1920,
        "height": 1080,
        "audio_file": f"generated/{identity.folder_name}/full-episode.mp3",
        "source_hashes": source_hashes,
        "palette": PALETTE,
        "objects": world["objects"],
        "edges": world["edges"],
        "evidence": world["evidence"],
        "cameras": world["cameras"],
        "tickets": tickets["tickets"],
        "units": plan["units"],
    }
    validate_schema(data, "render-data.schema.json", "greybox_ready")
    return data


def write_render_data(path: Path, data: dict) -> str:
    write_json_atomic(path, data)
    return sha256_file(path)

