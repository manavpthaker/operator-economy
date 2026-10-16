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


if __name__ == "__main__":
    unittest.main()
