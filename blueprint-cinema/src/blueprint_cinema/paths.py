from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


BLUEPRINT_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = BLUEPRINT_ROOT.parent
EPISODES_ROOT = BLUEPRINT_ROOT / "episodes"
SCHEMAS_ROOT = BLUEPRINT_ROOT / "schemas"
RENDERER_ROOT = BLUEPRINT_ROOT / "renderer"

EPISODE_CODE_RE = re.compile(r"^EP(?P<number>[0-9]{3})$")
EPISODE_FOLDER_RE = re.compile(r"^(?P<code>EP[0-9]{3})-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class PathContractError(ValueError):
    pass


@dataclass(frozen=True)
class EpisodeIdentity:
    episode_number: int
    episode_code: str
    slug: str
    folder_name: str

    @classmethod
    def from_init(cls, episode_code: str, slug: str) -> "EpisodeIdentity":
        match = EPISODE_CODE_RE.fullmatch(episode_code)
        if not match:
            raise PathContractError("episode code must be exactly EP###")
        if not SLUG_RE.fullmatch(slug):
            raise PathContractError("slug must be lowercase kebab-case")
        number = int(match.group("number"))
        if number < 1:
            raise PathContractError("episode number must be a positive integer")
        derived_code = f"EP{number:03d}"
        if derived_code != episode_code:
            raise PathContractError(f"episode code must be canonical: {derived_code}")
        return cls(number, derived_code, slug, f"{derived_code}-{slug}")

    @classmethod
    def from_folder(cls, folder_name: str) -> "EpisodeIdentity":
        match = EPISODE_FOLDER_RE.fullmatch(folder_name)
        if not match:
            raise PathContractError("episode folder must be EP###-kebab-case-slug")
        return cls.from_init(match.group("code"), match.group("slug"))

    @classmethod
    def from_dict(cls, value: dict) -> "EpisodeIdentity":
        required = ("episode_number", "episode_code", "slug", "folder_name")
        if any(key not in value for key in required):
            raise PathContractError("episode identity is incomplete")
        derived = cls.from_init(value["episode_code"], value["slug"])
        actual = cls(
            value["episode_number"],
            value["episode_code"],
            value["slug"],
            value["folder_name"],
        )
        if actual != derived:
            raise PathContractError(
                "episode number, code, slug, and derived folder name disagree"
            )
        return actual

    def as_dict(self) -> dict:
        return {
            "episode_number": self.episode_number,
            "episode_code": self.episode_code,
            "slug": self.slug,
            "folder_name": self.folder_name,
        }


def episode_dir(folder_name: str) -> Path:
    identity = EpisodeIdentity.from_folder(folder_name)
    path = (EPISODES_ROOT / identity.folder_name).resolve()
    if path.parent != EPISODES_ROOT.resolve():
        raise PathContractError("episode path escapes the episodes root")
    return path


def load_episode_identity(folder_name: str) -> tuple[EpisodeIdentity, Path, dict]:
    path = episode_dir(folder_name)
    project_path = path / "episode.json"
    if not project_path.is_file():
        raise PathContractError(f"missing episode project: {project_path}")
    project = json.loads(project_path.read_text(encoding="utf-8"))
    identity = EpisodeIdentity.from_dict(project)
    if identity.folder_name != folder_name or path.name != identity.folder_name:
        raise PathContractError(
            "folder, episode number, code, slug, and episode.json identity disagree"
        )
    return identity, path, project


def blueprint_relative(path: Path) -> str:
    return path.resolve().relative_to(BLUEPRINT_ROOT.resolve()).as_posix()


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()

