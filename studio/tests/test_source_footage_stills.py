import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_DIR = Path(__file__).parents[1] / "scripts" / "originate"
sys.path.insert(0, str(MODULE_DIR))

import source_footage as sf


class StillProviderTests(unittest.TestCase):
    def test_met_keeps_only_public_domain_objects_with_images(self):
        objects = {
            1: {"isPublicDomain": True, "primaryImage": "https://images.met/1.jpg",
                "artistDisplayName": "A", "title": "Market", "objectDate": "1890",
                "objectURL": "https://met/1"},
            2: {"isPublicDomain": False, "primaryImage": "https://images.met/2.jpg"},
            3: {"isPublicDomain": True, "primaryImage": ""},
        }

        def fake_get(url, headers=None):
            if url.startswith(sf.MET_SEARCH):
                return {"objectIDs": [1, 2, 3]}
            return objects[int(url.rsplit("/", 1)[1])]

        with patch.object(sf, "get_json", side_effect=fake_get):
            found = sf.search_met("market")
        self.assertEqual(["met-1"], [c["candidate_id"] for c in found])
        self.assertEqual("still", found[0]["media_kind"])
        self.assertEqual("CC0 1.0", found[0]["license"])
        self.assertEqual(sf.STILL_SECONDS, found[0]["duration_seconds"])

    def test_nasa_skips_third_party_copyright(self):
        search = {"collection": {"items": [
            {"href": "https://nasa/a.json", "data": [{"nasa_id": "a", "description": "Launch"}]},
            {"href": "https://nasa/b.json", "data": [{"nasa_id": "b", "description": "Photo © Getty"}]},
        ]}}

        def fake_get(url, headers=None):
            if url.startswith(sf.NASA_API):
                return search
            return ["http://images-assets.nasa.gov/image/a/a~large.jpg"]

        with patch.object(sf, "get_json", side_effect=fake_get):
            found = sf.search_nasa_stills("launch")
        self.assertEqual(["nasa-still-a"], [c["candidate_id"] for c in found])
        self.assertTrue(found[0]["download_url"].startswith("https://"))
        self.assertIn("insignia", found[0]["rights_notes"])

    def test_every_still_provider_is_routed_for_market_force(self):
        for provider in sf.STILL_PROVIDERS + ["nasa"]:
            self.assertIn(provider, sf.ROLE_PROVIDERS["market_force"])
            self.assertIn(provider, sf.ROLE_PROVIDERS["human_context"])

    @unittest.skipUnless(shutil.which("ffmpeg"), "needs ffmpeg")
    def test_still_renders_to_an_eight_second_1080p_clip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            still = root / "beat--met-1--still.jpg"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "lavfi", "-i",
                            "testsrc=size=900x1200", "-frames:v", "1", str(still)], check=True)
            clip = root / "beat--met-1.mp4"
            sf.fetch_candidate({"media_kind": "still", "download_url": "unused"}, clip)
            probe = json.loads(subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                 "stream=width,height:format=duration", "-of", "json", str(clip)],
                check=True, capture_output=True, text=True).stdout)
            self.assertEqual((1920, 1080), (probe["streams"][0]["width"], probe["streams"][0]["height"]))
            self.assertAlmostEqual(sf.STILL_SECONDS, float(probe["format"]["duration"]), delta=0.1)

    @unittest.skipUnless(shutil.which("ffmpeg"), "needs ffmpeg")
    def test_approve_rerenders_a_still_to_fill_a_longer_screen(self):
        with tempfile.TemporaryDirectory() as tmp:
            ep = Path(tmp)
            cand = ep / "footage" / "candidates"
            cand.mkdir(parents=True)
            still = cand / "beat--met-1--still.jpg"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "lavfi", "-i",
                            "testsrc=size=1600x900", "-frames:v", "1", str(still)], check=True)
            clip = cand / "beat--met-1.mp4"
            sf.fetch_candidate({"media_kind": "still", "download_url": "unused"}, clip)
            candidate = {"candidate_id": "met-1", "provider": "met", "asset_id": "1",
                         "media_kind": "still", "page_url": "https://met/1", "creator": "A",
                         "license": "CC0 1.0", "license_url": "", "downloaded_at": "now",
                         "local_path": str(clip.relative_to(ep)),
                         "still_path": str(still.relative_to(ep)), "sha256": "old"}
            (ep / "footage_manifest.json").write_text(json.dumps({"entries": [{"id": "beat"}]}))
            (ep / "footage_candidates.json").write_text(json.dumps(
                {"entries": [{"manifest_id": "beat", "candidates": [candidate]}]}))
            sf.approve(ep / "script.json", "beat", "met-1", "not_applicable", 0, 15.5)
            entry = json.loads((ep / "footage_manifest.json").read_text())["entries"][0]
            self.assertEqual(15.5, entry["source_out"])
            self.assertAlmostEqual(15.5, sf.media_duration(clip), delta=0.1)
            self.assertEqual(sf.file_sha256(clip), entry["sha256"])


if __name__ == "__main__":
    unittest.main()
