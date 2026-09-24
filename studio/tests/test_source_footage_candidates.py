import sys
import unittest
from pathlib import Path

MODULE_DIR = Path(__file__).parents[1] / "scripts" / "originate"
sys.path.insert(0, str(MODULE_DIR))

import source_footage_candidates as sfc


class SourceFootageCandidateTests(unittest.TestCase):
    def test_best_proxy_prefers_landscape_near_review_resolution(self):
        files = [
            {"file_type": "video/mp4", "width": 1080, "height": 1920},
            {"file_type": "video/mp4", "width": 3840, "height": 2160},
            {"file_type": "video/mp4", "width": 1280, "height": 720},
        ]
        self.assertEqual(1280, sfc.best_proxy(files)["width"])

    def test_query_preference_outweighs_technical_quality(self):
        preferred = sfc.candidate_score(
            {"duration": 12}, {"width": 1280, "height": 720}, 0)
        later_4k = sfc.candidate_score(
            {"duration": 12}, {"width": 3840, "height": 2160}, 1)
        self.assertGreater(preferred, later_4k)

    def test_portrait_and_too_short_are_penalized(self):
        useful = sfc.candidate_score(
            {"duration": 10}, {"width": 1280, "height": 720}, 0)
        weak = sfc.candidate_score(
            {"duration": 2}, {"width": 1080, "height": 1920}, 0)
        self.assertGreater(useful, weak)


if __name__ == "__main__":
    unittest.main()
