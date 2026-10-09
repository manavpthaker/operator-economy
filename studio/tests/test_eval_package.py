import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

MODULE_DIR = Path(__file__).parents[1] / "scripts" / "originate"
sys.path.insert(0, str(MODULE_DIR))

import eval_package as ep


class EvalPackageShortsTests(unittest.TestCase):
    def valid_brief(self):
        return {
            "title": "The Thirty-Day Map",
            "section": "hook",
            "first_beat": 1,
            "last_beat": 1,
            "hook_line": (
                "You can build a service that helps an owner get a business "
                "ready to sell."
            ),
            "cold_viewer_context": (
                "This is a service that prepares an owner's business for a "
                "future sale before a buyer appears."
            ),
            "last_line": "That gives you a first dependency map.",
            "standalone_payoff": (
                "The viewer can identify owner-only dependencies and turn "
                "them into a first handoff map."
            ),
            "episode_extension": (
                "The episode tests the broader offer and whether an owner "
                "will pay before a buyer appears."
            ),
            "pinned_comment": (
                "The full episode builds and tests the broader practice."
            ),
            "why": "A complete narrow answer with optional deeper context.",
        }

    def run_gate(self, briefs):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            content.mkdir()

            # This is enough for eval_package.py to execute. Unrelated rubric
            # deductions do not affect the exit code; only kill-list hits do.
            script = {
                "sections": [{
                    "id": "hook",
                    "beats": [{
                        "beat": 1,
                        "vo_text": "Could this business run without its owner?",
                    }],
                }],
            }
            script_path = root / "script.json"
            script_path.write_text(json.dumps(script))
            (content / "shorts_briefs.json").write_text(json.dumps(briefs))

            output = io.StringIO()
            with patch.object(sys, "argv", ["eval_package.py", str(script_path)]):
                with redirect_stdout(output):
                    with self.assertRaises(SystemExit) as raised:
                        ep.main()
            return raised.exception.code, output.getvalue()

    def test_complete_narrow_answer_passes_without_cliffhanger(self):
        brief = self.valid_brief()
        self.assertNotIn("cliffhanger_line", brief)

        code, output = self.run_gate([brief])

        self.assertEqual(0, code, output)
        self.assertIn("standalone narrow payoff", output)
        self.assertNotIn("complete-answer Short", output)

    def test_missing_standalone_payoff_blocks(self):
        brief = self.valid_brief()
        del brief["standalone_payoff"]

        code, output = self.run_gate([brief])

        self.assertEqual(1, code, output)
        self.assertIn("missing standalone payoff", output)

    def test_episode_cta_cannot_be_the_standalone_payoff(self):
        for payoff in (
            "Watch the full episode for the answer.",
            "EP007 shows how to do it.",
        ):
            with self.subTest(payoff=payoff):
                brief = self.valid_brief()
                brief["standalone_payoff"] = payoff

                code, output = self.run_gate([brief])

                self.assertEqual(1, code, output)
                self.assertIn("episode CTA used as standalone payoff", output)

    def test_optional_distinct_episode_extension_is_accepted(self):
        with_extension = self.valid_brief()
        without_extension = self.valid_brief()
        del without_extension["episode_extension"]

        for brief in (with_extension, without_extension):
            with self.subTest(has_extension="episode_extension" in brief):
                code, output = self.run_gate([brief])
                self.assertEqual(0, code, output)

    def test_episode_extension_cannot_duplicate_or_withhold_the_payoff(self):
        duplicate = self.valid_brief()
        duplicate["episode_extension"] = duplicate["standalone_payoff"]
        deferred = self.valid_brief()
        deferred["episode_extension"] = "Watch the episode for the answer."

        for brief in (duplicate, deferred):
            with self.subTest(extension=brief["episode_extension"]):
                code, output = self.run_gate([brief])
                self.assertEqual(1, code, output)
                self.assertIn(
                    "episode extension is not additive and distinct", output
                )

    def test_legacy_cliffhanger_alone_does_not_satisfy_last_line_contract(self):
        brief = self.valid_brief()
        brief["cliffhanger_line"] = brief.pop("last_line")

        code, output = self.run_gate([brief])

        self.assertEqual(1, code, output)
        self.assertIn("missing Shorts last-line anchor", output)

    def test_missing_cold_viewer_context_blocks(self):
        brief = self.valid_brief()
        del brief["cold_viewer_context"]

        code, output = self.run_gate([brief])

        self.assertEqual(1, code, output)
        self.assertIn("missing cold-viewer topic context", output)

    def test_missing_pinned_comment_blocks(self):
        brief = self.valid_brief()
        del brief["pinned_comment"]

        code, output = self.run_gate([brief])

        self.assertEqual(1, code, output)
        self.assertIn("missing Shorts pinned comment", output)


if __name__ == "__main__":
    unittest.main()
