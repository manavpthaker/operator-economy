import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_DIR = Path(__file__).parents[1] / "scripts" / "originate"
sys.path.insert(0, str(MODULE_DIR))

import footage_manifest as fm


class FootageManifestTests(unittest.TestCase):
    def valid_entry(self, media: Path) -> dict:
        return {
            "id": "episode-hook-01",
            "section": "hook",
            "beat": 1,
            "role": "human_context",
            "narration_anchor": "The operator greets the guest.",
            "approved": True,
            "provider": "original",
            "license": "owned",
            "license_checked_at": "2026-08-18",
            "downloaded_at": "2026-08-18T12:00:00Z",
            "faces_review": "cleared",
            "local_path": media.name,
            "sha256": fm.file_sha256(media),
            "source_in": 0,
            "source_out": 2,
        }

    @patch.object(fm, "media_duration", return_value=3.0)
    def test_valid_approved_local_entry_passes(self, _duration):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / "clip.mp4"
            media.write_bytes(b"fixture")
            manifest = {"schema_version": 1, "entries": [self.valid_entry(media)]}
            self.assertEqual([], fm.validate_manifest(manifest, root))

    @patch.object(fm, "media_duration", return_value=3.0)
    def test_hash_and_face_review_block_approval(self, _duration):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / "clip.mp4"
            media.write_bytes(b"fixture")
            entry = self.valid_entry(media)
            entry["sha256"] = "wrong"
            entry["faces_review"] = "needs_review"
            errors = fm.validate_entry(entry, root)
            self.assertTrue(any("sha256" in error for error in errors))
            self.assertTrue(any("cannot approve" in error for error in errors))

    def test_explicit_manifest_id_wins_over_section_match(self):
        manifest = {"entries": [
            {"id": "a", "section": "hook", "beat": 1},
            {"id": "b", "section": "other", "beat": 2},
        ]}
        self.assertEqual("b", fm.resolve_entry(
            manifest, "hook", 1, {"manifest_id": "b"})["id"])

    def test_init_derives_manifest_and_updates_asset_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = {
                "slug": "hotel-test",
                "sections": [{"id": "hook", "beats": [
                    {"beat": 1, "vo_text": "The operator greets the guest."}
                ]}],
            }
            assets = {"sections": [{"id": "hook", "assets": [
                {"beat": 1, "spec": {"type": "broll", "search_query": "hotel checkin"}}
            ]}]}
            (root / "script.json").write_text(json.dumps(script))
            (root / "assets.json").write_text(json.dumps(assets))
            manifest = fm.build_manifest(root / "script.json")
            rewritten = fm.load_json(root / "assets.json")
            self.assertEqual("hotel-test-hook-01", manifest["entries"][0]["id"])
            self.assertEqual("hotel-test-hook-01",
                             rewritten["sections"][0]["assets"][0]["spec"]["manifest_id"])


if __name__ == "__main__":
    unittest.main()
