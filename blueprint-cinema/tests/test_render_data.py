from __future__ import annotations

import json
import subprocess

from blueprint_cinema.hashes import canonical_json_bytes, sha256_file
from blueprint_cinema.input_lock import stage_locked_audio
from blueprint_cinema.paths import RENDERER_ROOT
from blueprint_cinema.render_data import compile_render_data
from blueprint_cinema.validation import load_json, validate_schema


def test_render_data_is_deterministic_and_hash_bound(current_artifacts, identity, episode_path):
    first = compile_render_data(
        identity,
        episode_path,
        current_artifacts["input-lock.json"],
        current_artifacts["world.json"],
        current_artifacts["visual-plan.json"],
        current_artifacts["asset-tickets.json"],
    )
    second = compile_render_data(
        identity,
        episode_path,
        current_artifacts["input-lock.json"],
        current_artifacts["world.json"],
        current_artifacts["visual-plan.json"],
        current_artifacts["asset-tickets.json"],
    )
    assert canonical_json_bytes(first) == canonical_json_bytes(second)
    assert first["source_hashes"]["visual_plan"] == sha256_file(episode_path / "visual-plan.json")
    assert first["source_hashes"]["assembled_vo"] == next(
        item["sha256"] for item in current_artifacts["input-lock.json"]["artifacts"] if item["role"] == "assembled_vo"
    )


def test_generated_render_data_schema_and_current_hashes(episode_path):
    data = load_json(episode_path / "render-data" / "greybox.json")
    validate_schema(data, "render-data.schema.json", "test")
    assert data["source_hashes"]["input_lock"] == sha256_file(episode_path / "input-lock.json")
    assert data["source_hashes"]["episode_engine"] == sha256_file(episode_path / "episode-engine.json")
    assert data["source_hashes"]["world"] == sha256_file(episode_path / "world.json")


def test_overview_and_focus_remotion_frames_smoke(tmp_path, current_artifacts, identity, episode_path):
    staged = RENDERER_ROOT / "public" / "generated" / identity.folder_name / "full-episode.mp3"
    stage_locked_audio(current_artifacts["input-lock.json"], staged)
    outputs = []
    for name, frame in (("overview.png", 0), ("focus.png", 450)):
        output = tmp_path / name
        result = subprocess.run(
            [
                "npx", "remotion", "still", "src/index.ts", "BlueprintCinema", str(output),
                f"--props={episode_path / 'render-data' / 'greybox.json'}", f"--frame={frame}", "--overwrite",
            ],
            cwd=RENDERER_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert output.is_file() and output.stat().st_size > 1000
        outputs.append(output)
    assert sha256_file(outputs[0]) != sha256_file(outputs[1])


def test_camera_uses_authored_focus_and_not_narration_routing():
    source = (RENDERER_ROOT / "src" / "camera.ts").read_text(encoding="utf-8")
    assert "unit.focus" in source
    assert "unit.camera_anchor" in source
    assert "narration_anchor" not in source


def test_deck_prototype_uses_persistent_objects_without_network_map(
    tmp_path, current_artifacts, identity, episode_path
):
    staged = RENDERER_ROOT / "public" / "generated" / identity.folder_name / "full-episode.mp3"
    stage_locked_audio(current_artifacts["input-lock.json"], staged)
    source = (RENDERER_ROOT / "src" / "DeckPrototype.tsx").read_text(encoding="utf-8")
    assert 'id="stay-key-tag"' in source
    assert 'id="ota-booking-gate"' in source
    assert 'id="hotel-stay-node"' in source
    assert 'data-bookend="show-identity"' in source
    assert 'data-bookend="episode-title"' in source
    assert "BrandIdentitySlide" in source
    assert "Build.</span><span>Own.</span><span>Operate." in source
    assert "Direct Booking" in source
    assert "props.edges" not in source
    assert "OverviewMap" not in source

    outputs = []
    for name, frame in (
        ("stay.png", 90),
        ("leak.png", 570),
        ("show-identity.png", 915),
        ("episode-title.png", 1110),
        ("handoffs.png", 2610),
    ):
        output = tmp_path / name
        result = subprocess.run(
            [
                "npx", "remotion", "still", "src/index.ts", "BlueprintCinemaDeckPrototype", str(output),
                f"--props={episode_path / 'render-data' / 'greybox.json'}", f"--frame={frame}", "--overwrite",
            ],
            cwd=RENDERER_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert output.is_file() and output.stat().st_size > 1000
        outputs.append(output)
    assert len({sha256_file(output) for output in outputs}) == len(outputs)
