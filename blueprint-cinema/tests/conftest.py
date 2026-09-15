from __future__ import annotations

import copy
from pathlib import Path

import pytest

from blueprint_cinema.hashes import sha256_file
from blueprint_cinema.paths import BLUEPRINT_ROOT, EpisodeIdentity
from blueprint_cinema.validation import load_json


EPISODE_PATH = BLUEPRINT_ROOT / "episodes" / "EP006-direct-booking-recovery"


@pytest.fixture
def episode_path() -> Path:
    return EPISODE_PATH


@pytest.fixture
def identity() -> EpisodeIdentity:
    return EpisodeIdentity.from_init("EP006", "direct-booking-recovery")


@pytest.fixture
def current_artifacts(episode_path: Path) -> dict:
    names = [
        "input-lock.json",
        "episode-engine.json",
        "world.json",
        "visual-plan.json",
        "asset-tickets.json",
    ]
    return {name: load_json(episode_path / name) for name in names}


@pytest.fixture
def cloned_artifacts(current_artifacts: dict) -> dict:
    return copy.deepcopy(current_artifacts)


def current_hashes(episode_path: Path) -> dict[str, str]:
    return {
        name: sha256_file(episode_path / name)
        for name in (
            "input-lock.json",
            "episode-engine.json",
            "world.json",
            "visual-plan.json",
            "asset-tickets.json",
        )
    }

