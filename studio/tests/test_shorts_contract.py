import copy
import json
import sys
import unittest
from pathlib import Path


MODULE_DIR = Path(__file__).parents[1] / "scripts" / "originate"
sys.path.insert(0, str(MODULE_DIR))

import shorts_contract as contract


REPO_ROOT = Path(__file__).parents[2]
EP007_LOCK = (
    REPO_ROOT
    / "studio"
    / "originate"
    / "exit-readiness-prep"
    / "shorts-net-new"
    / "STANDALONE-SCRIPTS-V3.json"
)


class ShortsContractTests(unittest.TestCase):
    def direct_manifest(self):
        hook = (
            "You can build a service that helps an owner get a business "
            "ready to sell."
        )
        payoff = "That gives you a first dependency map."
        closing = "Now you know where the preparation service starts."
        return {
            "standalone_contract": {
                "context_rule": (
                    "The opening identifies the sale-readiness service, "
                    "owner and operator opportunity for a cold viewer."
                )
            },
            "scripts": [{
                "title": "The Thirty-Day Map",
                "hook_line": hook,
                "payoff_line": payoff,
                "closing_line": closing,
                "spoken_copy": f"{hook} {payoff} {closing}",
                "standalone_payoff": (
                    "The viewer can create a first dependency map."
                ),
            }],
        }

    def test_current_ep007_lock_passes_direct_contract(self):
        payload = json.loads(EP007_LOCK.read_text())

        result = contract.validate_payload(payload)

        self.assertTrue(result.ok, result.as_dict())
        self.assertEqual("direct", result.source_kind)
        self.assertEqual(4, result.record_count)
        self.assertFalse(result.require_pinned_comment)

    def test_direct_script_with_complete_payoff_needs_no_episode_bridge(self):
        result = contract.validate_payload(self.direct_manifest())

        self.assertTrue(result.ok, result.as_dict())

    def test_distinct_episode_bridge_after_payoff_passes(self):
        payload = self.direct_manifest()
        record = payload["scripts"][0]
        bridge = "The episode tests the broader offer and economics."
        record["episode_bridge_line"] = bridge
        record["spoken_copy"] = (
            f"{record['hook_line']} {record['payoff_line']} "
            f"{bridge} {record['closing_line']}"
        )

        result = contract.validate_payload(payload)

        self.assertTrue(result.ok, result.as_dict())

    def test_episode_bridge_before_payoff_fails(self):
        payload = self.direct_manifest()
        record = payload["scripts"][0]
        bridge = "The episode tests the broader offer and economics."
        record["episode_bridge_line"] = bridge
        record["spoken_copy"] = (
            f"{record['hook_line']} {bridge} "
            f"{record['payoff_line']} {record['closing_line']}"
        )

        result = contract.validate_payload(payload)

        self.assertFalse(result.ok)
        self.assertIn(
            "episode_bridge_before_payoff",
            {issue.code for issue in result.issues},
        )

    def test_direct_script_requires_exact_payoff_line(self):
        payload = self.direct_manifest()
        del payload["scripts"][0]["payoff_line"]

        result = contract.validate_payload(payload)

        self.assertFalse(result.ok)
        self.assertIn("missing_payoff_line", {issue.code for issue in result.issues})

    def test_cliffhanger_cannot_replace_terminal_or_payoff(self):
        payload = self.direct_manifest()
        record = payload["scripts"][0]
        record["cliffhanger_line"] = record.pop("closing_line")
        del record["payoff_line"]

        result = contract.validate_payload(payload)

        codes = {issue.code for issue in result.issues}
        self.assertFalse(result.ok)
        self.assertIn("missing_payoff_line", codes)
        self.assertIn("missing_terminal_line", codes)

    def test_exact_anchors_must_occur_in_spoken_copy(self):
        payload = self.direct_manifest()
        payload["scripts"][0]["payoff_line"] = "A line that was never spoken."

        result = contract.validate_payload(payload)

        self.assertFalse(result.ok)
        self.assertIn(
            "phrase_not_in_spoken_copy",
            {issue.code for issue in result.issues},
        )

    def test_empty_and_malformed_containers_fail_closed(self):
        cases = (
            ([], "empty_records"),
            ({}, "malformed_container"),
            ({"scripts": "not-a-list"}, "malformed_records"),
            ({"scripts": ["not-an-object"]}, "malformed_record"),
        )

        for payload, expected_code in cases:
            with self.subTest(payload=payload):
                result = contract.validate_payload(copy.deepcopy(payload))
                self.assertFalse(result.ok)
                self.assertIn(expected_code, {issue.code for issue in result.issues})


if __name__ == "__main__":
    unittest.main()
