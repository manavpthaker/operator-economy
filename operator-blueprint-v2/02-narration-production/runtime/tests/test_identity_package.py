from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path

from oe_narration.core import (
    SPOKEN_SCHEMA,
    ValidationError,
    canonical_w_bytes,
    extract_step1_script,
    read_canonical_w,
    sha256_file,
    token_identity,
    verify_package,
    write_extraction,
)


EXPECTED_AI_VISIBILITY_HASH = "096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a"
EXPECTED_SCRIPT_HASH = "74048b55ed15ed6ed679abb5a6c892def8a8a40e75e7cebeafdfde319dd67efa"
EXPECTED_BLOCKS = ["S00", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12"]


def tiny_script(body: str = "We do not rewrite words.") -> str:
    scenes = []
    for index in range(12):
        scene_id = index if index == 0 else index + 1
        scenes.append(f"## S{scene_id:02d}: scene\n\n### Narration\n\n{body} {index}\n")
    return "# Script\n\n" + "\n".join(scenes) + "\n## Production boundary\n\nNone.\n"


class IdentityTests(unittest.TestCase):
    def test_locked_ai_visibility_identity(self) -> None:
        repo = Path(__file__).resolve().parents[4]
        relative = Path("operator-blueprint-v2/01-editorial/fixtures/step1-v1.4-e2e-ai-visibility-2026-08-22/122-script-v1.1-HORIZONTAL-PITCH-CANDIDATE.md")
        candidates = [repo / relative, repo.parent / "operator-economy-step1-e2e" / relative]
        script = next((path for path in candidates if path.is_file()), None)
        self.assertIsNotNone(script, "Step 1 v1.5 AI Visibility fixture must be present in an integration checkout")
        extraction_a = extract_step1_script(script)  # type: ignore[arg-type]
        extraction_b = extract_step1_script(script)  # type: ignore[arg-type]
        self.assertEqual(extraction_a, extraction_b)
        self.assertEqual(extraction_a.script_sha256, EXPECTED_SCRIPT_HASH)
        self.assertEqual(len(extraction_a.tokens), 3019)
        self.assertEqual(extraction_a.identity["sha256"], EXPECTED_AI_VISIBILITY_HASH)
        self.assertEqual([block.block_id for block in extraction_a.blocks], EXPECTED_BLOCKS)

    def test_terminal_lf_is_part_of_identity(self) -> None:
        tokens = ["do", "not", "drift"]
        with_lf = hashlib.sha256(b"do\nnot\ndrift\n").hexdigest()
        without_lf = hashlib.sha256(b"do\nnot\ndrift").hexdigest()
        self.assertEqual(token_identity(tokens)["sha256"], with_lf)
        self.assertNotEqual(with_lf, without_lf)

    def test_canonical_w_requires_terminal_lf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "w.txt"
            path.write_bytes(b"do\nnot")
            with self.assertRaisesRegex(ValidationError, "end with LF"):
                read_canonical_w(path)

    def test_extractor_rejects_artifacts_and_non_nfc(self) -> None:
        bad_values = [
            "See [source](https://example.com).",
            "This is [pause] directed.",
            "This is TODO later.",
            "<<<<<<< ours",
            "This has <em>HTML</em>.",
            "This has a footnote[^1].",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "script.md"
            for body in bad_values:
                path.write_text(tiny_script(body), encoding="utf-8")
                with self.assertRaises(ValidationError, msg=body):
                    extract_step1_script(path)
            path.write_text(tiny_script("Cafe\u0301"), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "not Unicode NFC"):
                extract_step1_script(path)

    def test_written_identity_is_portable_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "script.md"
            script.write_text(tiny_script(), encoding="utf-8")
            extraction = extract_step1_script(script)
            first = root / "first"
            second = root / "second"
            write_extraction(extraction, first, script.resolve())
            write_extraction(extraction, second, script.resolve())
            first_receipt = (first / "spoken-identity.json").read_bytes()
            second_receipt = (second / "spoken-identity.json").read_bytes()
            self.assertEqual(first_receipt, second_receipt)
            self.assertNotIn(b"script_path", first_receipt)
            self.assertNotIn(str(root).encode("utf-8"), first_receipt)


class PackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        (self.root / ".git").mkdir()
        self.script = self.root / "script.md"
        self.script.write_text(tiny_script(), encoding="utf-8")
        self.extraction = extract_step1_script(self.script)
        self.readthrough = self.root / "readthrough.md"
        spoken = " ".join(self.extraction.tokens)
        self.readthrough.write_text(f"# Readthrough\n\nStatus: locked\n\n{spoken}\n\n## Review\n\nNo.\n", encoding="utf-8")
        self.manifest = Path(self.temp.name) / "package.json"
        self.value = {
            "schema_version": "oe-narration-package-v1",
            "roots": [{"id": "repo", "path": "repo"}],
            "sources": [
                {"id": "script", "root_id": "repo", "path": "script.md", "sha256": sha256_file(self.script)},
                {"id": "readthrough", "root_id": "repo", "path": "readthrough.md", "sha256": sha256_file(self.readthrough)},
            ],
            "authority": {
                "script_source_id": "script",
                "readthrough_source_id": "readthrough",
                "spoken_identity": self.extraction.identity,
                "block_count": 12,
                "block_ids": EXPECTED_BLOCKS,
            },
            "derived_parts": [],
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_manifest(self) -> None:
        self.manifest.write_text(json.dumps(self.value), encoding="utf-8")

    def test_valid_package(self) -> None:
        self.write_manifest()
        result = verify_package(self.manifest)
        self.assertTrue(result["valid"])
        self.assertEqual(result["block_count"], 12)

    def test_hash_tamper_fails(self) -> None:
        self.write_manifest()
        self.script.write_text(self.script.read_text() + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValidationError, "source hash mismatch"):
            verify_package(self.manifest)

    def test_missing_not_fails_even_with_updated_file_hash(self) -> None:
        text = self.readthrough.read_text().replace(" do not rewrite", " do rewrite", 1)
        self.readthrough.write_text(text, encoding="utf-8")
        self.value["sources"][1]["sha256"] = sha256_file(self.readthrough)
        self.write_manifest()
        with self.assertRaisesRegex(ValidationError, "not exactly identical"):
            verify_package(self.manifest)

    def test_competing_identity_is_rejected(self) -> None:
        self.value["alternate_spoken_identity"] = {"token_count": 3043}
        self.write_manifest()
        with self.assertRaisesRegex(ValidationError, "forbidden"):
            verify_package(self.manifest)

    def test_absolute_and_parent_source_paths_are_rejected(self) -> None:
        for bad_path in (str(self.script), "../repo/script.md"):
            self.value["sources"][0]["path"] = bad_path
            self.write_manifest()
            with self.assertRaisesRegex(ValidationError, "must not be absolute or contain"):
                verify_package(self.manifest)

    def test_symlink_escape_is_rejected(self) -> None:
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text(self.script.read_text(), encoding="utf-8")
        link = self.root / "link.md"
        os.symlink(outside, link)
        self.value["sources"][0] = {
            "id": "script", "root_id": "repo", "path": "link.md", "sha256": sha256_file(outside)
        }
        self.write_manifest()
        with self.assertRaisesRegex(ValidationError, "escapes declared root"):
            verify_package(self.manifest)


if __name__ == "__main__":
    unittest.main()
