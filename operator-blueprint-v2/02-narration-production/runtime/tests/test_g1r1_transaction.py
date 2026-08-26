from __future__ import annotations

import copy
import hashlib
from pathlib import Path
import unittest
from unittest.mock import patch

from oe_narration import g1r1_transaction as transaction


MEMBER = "fixture-member-A"
MEMBER_SHA = hashlib.sha256(MEMBER.encode("utf-8")).hexdigest()


def policy_with_role(*, etag: str = "grant-etag") -> dict:
    return {
        "version": 1,
        "etag": etag,
        "bindings": [
            {"role": "roles/viewer", "members": [MEMBER, "fixture-member-B"]},
            {"role": transaction.ROLE, "members": [MEMBER]},
            {"role": "roles/storage.objectViewer", "members": ["fixture-member-C"]},
        ],
    }


def policy_without_role(*, etag: str = "final-etag") -> dict:
    value = policy_with_role(etag=etag)
    value["bindings"].pop(1)
    return value


class G1R1TransactionTests(unittest.TestCase):
    def test_hash_lookup_and_revoke_preserve_unrelated_policy(self) -> None:
        original = policy_with_role()
        with patch.object(transaction, "MEMBER_SHA256", MEMBER_SHA):
            member = transaction._member_from_hash(original)
            changed, present = transaction._remove_exact_role(original, member)
        self.assertTrue(present)
        self.assertEqual(member, MEMBER)
        self.assertEqual(original, policy_with_role())
        self.assertEqual(changed, policy_without_role(etag="grant-etag"))

    def test_conditioned_or_duplicate_target_role_is_rejected(self) -> None:
        conditioned = policy_with_role()
        conditioned["bindings"][1]["condition"] = {"title": "not-authorized"}
        with self.assertRaises(transaction.TransactionError):
            transaction._remove_exact_role(conditioned, MEMBER)

        duplicate = policy_with_role()
        duplicate["bindings"].append({"role": transaction.ROLE, "members": [MEMBER]})
        with self.assertRaises(transaction.TransactionError):
            transaction._remove_exact_role(duplicate, MEMBER)

        duplicate_entry = policy_with_role()
        duplicate_entry["bindings"][1]["members"].append(MEMBER)
        with self.assertRaises(transaction.TransactionError):
            transaction._remove_exact_role(duplicate_entry, MEMBER)

    def test_post_run_artifact_cardinality_is_fail_closed(self) -> None:
        success_values = [
            {"exists": True},
            {"exists": True},
            {"exists": False},
            {"exists": True},
            {"exists": True},
        ]
        with patch.object(transaction, "_artifact_summary", side_effect=success_values):
            artifacts, error, succeeded = transaction._collect_and_validate_artifacts(
                {"invoked": True, "exit_code": 0, "outcome": "executor_returned_success"}
            )
        self.assertIsNone(error)
        self.assertTrue(succeeded)
        self.assertTrue(artifacts["run_receipt"]["exists"])

        invalid_values = [
            {"exists": True},
            {"exists": True},
            {"exists": True},
            {"exists": True},
            {"exists": True},
        ]
        with patch.object(transaction, "_artifact_summary", side_effect=invalid_values):
            _artifacts, error, succeeded = transaction._collect_and_validate_artifacts(
                {"invoked": True, "exit_code": 0, "outcome": "executor_returned_success"}
            )
        self.assertEqual(error, "invoked_g1_receipt_cardinality_invalid")
        self.assertFalse(succeeded)

    def test_g1_failure_still_revokes_and_verifies_final_absence(self) -> None:
        captured: dict = {}

        def capture_receipt(value: dict) -> str:
            captured.update(copy.deepcopy(value))
            return "a" * 64

        with (
            patch.object(transaction, "MEMBER_SHA256", MEMBER_SHA),
            patch.object(transaction, "_preflight_local_state", return_value={"project": "fixture-project", "head": "b" * 40, "executor_source_sha256": "1" * 64}),
            patch.object(transaction, "_preflight_google_adc", return_value="/safe/gcloud"),
            patch.object(transaction, "_load_google_access_token", return_value="fixture-token-never-emitted"),
            patch.object(
                transaction,
                "_get_policy",
                side_effect=[policy_with_role(), policy_with_role(etag="revoke-etag"), policy_without_role()],
            ),
            patch.object(transaction, "_invoke_g1_once", side_effect=transaction.TransactionError("fixture_g1_failure")),
            patch.object(transaction, "_set_policy", return_value=policy_without_role()),
            patch.object(transaction, "_collect_and_validate_artifacts", return_value=({"failure_receipt": {"exists": True}}, None, False)),
            patch.object(transaction, "_write_private_receipt", side_effect=capture_receipt),
        ):
            with self.assertRaisesRegex(transaction.TransactionError, "G1R1_TRANSACTION_FAILED_BEFORE_INVOCATION"):
                transaction.execute()

        self.assertEqual(captured["transaction_error"], "fixture_g1_failure")
        self.assertEqual(captured["iam_calls"]["set_policy"], 1)
        self.assertTrue(captured["cleanup_verified"])
        self.assertFalse(captured["security_block_role_still_possible"])

    def test_cleanup_retries_only_one_etag_conflict(self) -> None:
        captured: dict = {}

        def capture_receipt(value: dict) -> str:
            captured.update(copy.deepcopy(value))
            return "c" * 64

        conflict = transaction.TransactionError("iam_http_failure", http_status=412)
        policies = [
            policy_with_role(),
            policy_with_role(etag="revoke-etag-1"),
            policy_with_role(etag="revoke-etag-2"),
            policy_without_role(),
        ]
        with (
            patch.object(transaction, "MEMBER_SHA256", MEMBER_SHA),
            patch.object(transaction, "_preflight_local_state", return_value={"project": "fixture-project", "head": "d" * 40, "executor_source_sha256": "2" * 64}),
            patch.object(transaction, "_preflight_google_adc", return_value="/safe/gcloud"),
            patch.object(transaction, "_load_google_access_token", return_value="fixture-token-never-emitted"),
            patch.object(transaction, "_get_policy", side_effect=policies),
            patch.object(transaction, "_invoke_g1_once", return_value={"invoked": True, "exit_code": 2, "outcome": "executor_returned_failure"}),
            patch.object(transaction, "_set_policy", side_effect=[conflict, policy_without_role()]),
            patch.object(transaction, "_collect_and_validate_artifacts", return_value=({"failure_receipt": {"exists": True}}, None, False)),
            patch.object(transaction, "_write_private_receipt", side_effect=capture_receipt),
        ):
            result = transaction.execute()

        self.assertTrue(result["cleanup_verified"])
        self.assertEqual(captured["iam_calls"]["set_policy"], 2)
        self.assertEqual(captured["iam_calls"]["cleanup_retry_count"], 1)

    def test_non_conflict_cleanup_failure_sets_security_block(self) -> None:
        captured: dict = {}

        def capture_receipt(value: dict) -> str:
            captured.update(copy.deepcopy(value))
            return "e" * 64

        with (
            patch.object(transaction, "MEMBER_SHA256", MEMBER_SHA),
            patch.object(transaction, "_preflight_local_state", return_value={"project": "fixture-project", "head": "f" * 40, "executor_source_sha256": "3" * 64}),
            patch.object(transaction, "_preflight_google_adc", return_value="/safe/gcloud"),
            patch.object(transaction, "_load_google_access_token", return_value="fixture-token-never-emitted"),
            patch.object(transaction, "_get_policy", side_effect=[policy_with_role(), policy_with_role(etag="revoke-etag")]),
            patch.object(transaction, "_invoke_g1_once", return_value={"invoked": True, "exit_code": 0, "outcome": "executor_returned_success"}),
            patch.object(transaction, "_set_policy", side_effect=transaction.TransactionError("iam_transport_failure")),
            patch.object(transaction, "_collect_and_validate_artifacts", return_value=({"run_receipt": {"exists": True}}, None, True)),
            patch.object(transaction, "_write_private_receipt", side_effect=capture_receipt),
        ):
            with self.assertRaisesRegex(transaction.TransactionError, "SECURITY_BLOCK_ROLE_STILL_POSSIBLE"):
                transaction.execute()

        self.assertFalse(captured["cleanup_verified"])
        self.assertTrue(captured["security_block_role_still_possible"])
        self.assertEqual(captured["iam_calls"]["cleanup_retry_count"], 0)

    def test_committed_source_contains_no_raw_principal(self) -> None:
        source = Path(transaction.__file__).read_text(encoding="utf-8")
        self.assertNotIn("@mpthaker", source)
        self.assertNotIn("manav@", source)


if __name__ == "__main__":
    unittest.main()
