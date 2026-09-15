#!/usr/bin/env python3
"""Hash-verify and stage EP006's locked VO plus existing local OE fonts."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


EXPECTED_SHA256 = "95e90a1ebb5dfbc6e13bc2efd12915cea9f15807199b0301cd3f63d59cb8e468"
FONT_HASHES = {
    "boska-700.woff2": "f77e750b53ece9138eb12b6d35e97d832d332cd109600fd91452d9f9988f35c5",
    "supreme-400.woff2": "ca2227b5145226ca24bb601053e609e96ddaedb59ebc14fa920065bf934a5dd5",
    "supreme-500.woff2": "ce86616b5f35f7e3a0cded1375b9811e34bf66bdeaa3ffabb5ce6ad7e01c66d2",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    project_root = Path(__file__).resolve().parent
    repo_root = project_root.parents[3]
    source = repo_root / "studio/originate/direct-booking-recovery/vo/full-episode.mp3"
    destination = project_root / "assets/ep006-locked-vo.mp3"

    if not source.is_file():
        raise SystemExit(f"missing locked VO: {source}")
    source_hash = sha256(source)
    if source_hash != EXPECTED_SHA256:
        raise SystemExit(
            f"locked VO hash mismatch: expected {EXPECTED_SHA256}, got {source_hash}"
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    staged_hash = sha256(destination)
    if staged_hash != EXPECTED_SHA256:
        destination.unlink(missing_ok=True)
        raise SystemExit(
            f"staged VO hash mismatch: expected {EXPECTED_SHA256}, got {staged_hash}"
        )

    staged_fonts: list[dict[str, object]] = []
    fonts_destination = project_root / "assets/fonts"
    fonts_destination.mkdir(parents=True, exist_ok=True)
    for filename, expected_hash in FONT_HASHES.items():
        font_source = repo_root / "site/public/fonts" / filename
        font_destination = fonts_destination / filename
        if not font_source.is_file():
            raise SystemExit(f"missing local OE font: {font_source}")
        if sha256(font_source) != expected_hash:
            raise SystemExit(f"local OE font hash mismatch: {font_source}")
        shutil.copy2(font_source, font_destination)
        if sha256(font_destination) != expected_hash:
            font_destination.unlink(missing_ok=True)
            raise SystemExit(f"staged OE font hash mismatch: {font_destination}")
        staged_fonts.append(
            {
                "source": str(font_source.relative_to(repo_root)),
                "destination": str(font_destination.relative_to(repo_root)),
                "sha256": expected_hash,
                "bytes": font_destination.stat().st_size,
            }
        )

    print(
        json.dumps(
            {
                "vo": {
                    "source": str(source.relative_to(repo_root)),
                    "destination": str(destination.relative_to(repo_root)),
                    "sha256": staged_hash,
                    "bytes": destination.stat().st_size,
                },
                "fonts": staged_fonts,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
