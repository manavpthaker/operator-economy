#!/usr/bin/env python3
"""Prove fixture-only case metadata cannot make a production episode validator return PASS."""

import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile


HERE = pathlib.Path(__file__).resolve().parent
REPOSITORY_ROOT = HERE.parents[2]
VALIDATOR = HERE / "validate.py"
EPISODES = REPOSITORY_ROOT / "operator-blueprint-v2/episodes"
SOURCE_EPISODE = EPISODES / "EP007-exit-readiness-prep"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    temporary_episode = pathlib.Path(tempfile.mkdtemp(prefix=".step3-v04-case-", dir=EPISODES))
    try:
        os.symlink(SOURCE_EPISODE / "01-editorial", temporary_episode / "01-editorial")
        os.symlink(SOURCE_EPISODE / "02-narration-production", temporary_episode / "02-narration-production")
        stage = temporary_episode / "03-visual-translation"
        stage.mkdir()

        alternate_process = stage / "alternate-process.json"
        alternate_process.write_text(
            json.dumps({"process_version": "0.4", "kind": "process-amendment"}) + "\n",
            encoding="utf-8",
        )

        source_lock = SOURCE_EPISODE / "03-visual-translation/input-lock.json"
        lock = json.loads(source_lock.read_text(encoding="utf-8"))
        lock["process_lock"] = {
            "path": "alternate-process.json",
            "sha256": sha256(alternate_process),
        }
        lock["input_lock"]["operator_canvas"]["sha256"] = "a" * 64
        (stage / "input-lock.json").write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")

        # Before the production guard, this turns a real V1 defect into an expected test result and
        # redefines the alternate process as canonical, causing the validator to exit successfully.
        (stage / "case.json").write_text(
            json.dumps(
                {
                    "canonical_process_path": "alternate-process.json",
                    "expect_failures": ["V1"],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--through", "V1", str(stage)],
            text=True,
            capture_output=True,
        )
        if result.returncode == 0:
            print(result.stdout.rstrip())
            print("production case.json was incorrectly accepted", file=sys.stderr)
            return 1
        return 0
    finally:
        shutil.rmtree(temporary_episode)


if __name__ == "__main__":
    raise SystemExit(main())
