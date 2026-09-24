from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from oe_narration.core import (
    ValidationError,
    canonical_w_bytes,
    sha256_file,
    token_identity,
    validate_state,
    validate_transcript,
)


def make_master(path: Path, duration: float = 2.0) -> None:
    completed = subprocess.run(
        [
            "ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i",
            f"sine=frequency=330:duration={duration}", "-ar", "48000", "-ac", "1",
            "-c:a", "pcm_s24le", str(path),
        ],
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr)


class TranscriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.tokens = ["Do", "not", "drift."]
        self.w_path = self.root / "canonical-w.txt"
        self.w_path.write_bytes(canonical_w_bytes(self.tokens))
        self.master = self.root / "master.wav"
        make_master(self.master)
        self.transcript_path = self.root / "transcript.json"
        self.transcript = {
            "schema_version": "oe-word-transcript-v1",
            "base_dir": ".",
            "spoken_identity": token_identity(self.tokens),
            "master": {"path": "master.wav", "sha256": sha256_file(self.master), "duration_ms": 2000},
            "words": [
                {"index": 0, "w_id": "w000000", "canonical_token": "Do", "start_ms": 0, "end_ms": 500, "review_state": "approved"},
                {
                    "index": 1,
                    "w_id": "w000001",
                    "canonical_token": "not",
                    "start_ms": 550,
                    "end_ms": 1000,
                    "review_state": "approved",
                    "alignment_parts": [
                        {"start_ms": 550, "end_ms": 750, "label": "n"},
                        {"start_ms": 750, "end_ms": 1000, "label": "ot"},
                    ],
                },
                {"index": 2, "w_id": "w000002", "canonical_token": "drift.", "start_ms": 1100, "end_ms": 1800, "review_state": "approved"},
            ],
            "unresolved_mismatches": 0,
        }
        self.write_transcript()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_transcript(self) -> None:
        self.transcript_path.write_text(json.dumps(self.transcript), encoding="utf-8")

    def test_valid_master_bound_transcript(self) -> None:
        result = validate_transcript(self.transcript_path, self.w_path)
        self.assertTrue(result["technical_pass"])
        self.assertFalse(result["creative_approved"])

    def test_missing_not_fails(self) -> None:
        del self.transcript["words"][1]
        self.transcript["words"][1]["index"] = 1
        self.write_transcript()
        with self.assertRaises(ValidationError) as raised:
            validate_transcript(self.transcript_path, self.w_path)
        self.assertTrue(any("word count mismatch" in error or "token mismatch" in error for error in raised.exception.errors))

    def test_master_mutation_invalidates_transcript(self) -> None:
        with self.master.open("ab") as handle:
            handle.write(b"mutation")
        with self.assertRaisesRegex(ValidationError, "master hash mismatch"):
            validate_transcript(self.transcript_path, self.w_path)

    def test_path_traversal_and_symlink_escape_fail(self) -> None:
        outside = self.root.parent / f"{self.root.name}-outside.wav"
        make_master(outside)
        try:
            self.transcript["master"]["path"] = "../outside.wav"
            self.write_transcript()
            with self.assertRaisesRegex(ValidationError, "must not be absolute or contain"):
                validate_transcript(self.transcript_path, self.w_path)
            link = self.root / "escaped.wav"
            os.symlink(outside, link)
            self.transcript["master"] = {"path": "escaped.wav", "sha256": sha256_file(outside), "duration_ms": 2000}
            self.write_transcript()
            with self.assertRaisesRegex(ValidationError, "escapes base_dir"):
                validate_transcript(self.transcript_path, self.w_path)
        finally:
            outside.unlink(missing_ok=True)


class StateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.state_path = self.root / "state.json"
        self.identity = "a" * 64
        self.state = {
            "schema_version": "oe-narration-state-v1",
            "base_dir": ".",
            "workflow_status": "draft",
            "gates": {f"N{index}": {"result": "pending"} for index in range(1, 8)},
            "technical_pass": False,
            "creative_approval": {"approved": False},
            "active_invalidations": [],
            "identities": {"script_sha256": "b" * 64, "spoken_text_sha256": self.identity},
            "audio_origin": None,
            "fallback_reason": None,
            "master": None,
            "transcript": None,
            "intentional_pause_map": None,
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_state(self) -> None:
        self.state_path.write_text(json.dumps(self.state), encoding="utf-8")

    def lock_state(self) -> tuple[Path, Path, Path]:
        master = self.root / "master.wav"
        master.write_bytes(b"master")
        transcript = self.root / "transcript.json"
        transcript.write_text("{}", encoding="utf-8")
        pause = self.root / "pauses.json"
        pause.write_text("[]", encoding="utf-8")
        master_hash = sha256_file(master)
        self.state.update(
            {
                "workflow_status": "locked",
                "gates": {f"N{index}": {"result": "passed"} for index in range(1, 8)},
                "technical_pass": True,
                "creative_approval": {
                    "approved": True,
                    "set_by_type": "human",
                    "approved_by": "Owner",
                    "approved_at": "2026-08-23T12:00:00Z",
                },
                "audio_origin": "native_pcm",
                "fallback_reason": None,
                "master": {"path": "master.wav", "sha256": master_hash},
                "transcript": {
                    "path": "transcript.json",
                    "sha256": sha256_file(transcript),
                    "master_sha256": master_hash,
                    "spoken_text_sha256": self.identity,
                },
                "intentional_pause_map": {
                    "path": "pauses.json", "sha256": sha256_file(pause), "master_sha256": master_hash
                },
            }
        )
        return master, transcript, pause

    def test_draft_state_is_valid_but_not_approved(self) -> None:
        self.write_state()
        result = validate_state(self.state_path)
        self.assertTrue(result["valid"])
        self.assertFalse(result["technical_pass"])
        self.assertFalse(result["creative_approved"])

    def test_automation_cannot_set_creative_approval(self) -> None:
        self.state["creative_approval"] = {
            "approved": True, "set_by_type": "automation", "approved_by": "CLI", "approved_at": "now"
        }
        self.write_state()
        with self.assertRaisesRegex(ValidationError, "only be set_by_type=human"):
            validate_state(self.state_path)

    def test_locked_state_and_master_mutation(self) -> None:
        master, _, _ = self.lock_state()
        self.write_state()
        self.assertEqual(validate_state(self.state_path)["workflow_status"], "locked")
        master.write_bytes(b"changed")
        with self.assertRaisesRegex(ValidationError, "master is missing or its hash changed"):
            validate_state(self.state_path)

    def test_pause_map_binding_and_lossy_disclosure_are_required(self) -> None:
        self.lock_state()
        self.state["intentional_pause_map"]["master_sha256"] = "c" * 64
        self.write_state()
        with self.assertRaisesRegex(ValidationError, "pause map is not bound"):
            validate_state(self.state_path)
        self.lock_state()
        self.state["audio_origin"] = "lossy_mp3"
        self.state["fallback_reason"] = None
        self.write_state()
        with self.assertRaisesRegex(ValidationError, "requires fallback_reason"):
            validate_state(self.state_path)


if __name__ == "__main__":
    unittest.main()
