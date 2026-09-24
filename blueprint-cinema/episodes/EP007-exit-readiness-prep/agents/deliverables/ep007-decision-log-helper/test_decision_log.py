import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("decision_log.py")
spec = importlib.util.spec_from_file_location("decision_log", SCRIPT)
log = importlib.util.module_from_spec(spec)
spec.loader.exec_module(log)
EPISODE = "EP007-test-episode"


class DecisionLogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source.txt"
        self.source.write_text("Frozen owner feedback and decision evidence.\n")
        self.digest = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.path = self.root / "blueprint-cinema" / "episodes" / EPISODE / "review" / "decisions" / "events.jsonl"

    def decision(self, event_id="form-v1", decision_id="form"):
        return {"event_id": event_id, "decision_id": decision_id, "event_type": "decision",
                "tags": ["animation", "cut-timing"], "data": {
                    "context": {"narrative_job": "Explain the payment gap.", "viewer_before": "All roles seem paid.", "viewer_after": "Readiness lacks a paid role."},
                    "choice": "Draw the fee return to the sale team.", "reason": "The connection makes the incentive visible.",
                    "alternatives": [{"choice": "Narrator hold", "reason_not_selected": "The relationship is harder to compare without a diagram."}],
                    "reuse": {"kind": "conditional_precedent", "applies_when": "A supported payment asymmetry explains the gap.", "avoid_when": "The fee would imply an unsupported universal claim."},
                    "nuance": {"animation": {"form": "conditional return path"}, "source_basis": "agent_proposal"}},
                "evidence": [{"path": "source.txt", "sha256": self.digest, "locator": "line1"}]}

    def feedback(self, event_id="owner-v1", target="form-v1", actor="owner", verdict="accept"):
        return {"event_id": event_id, "decision_id": "form", "event_type": "feedback", "tags": ["animation"],
                "data": {"decision_event_id": target, "actor": actor, "verbatim": "This version works.",
                         "interpretation": "Private preview selected.", "verdict": verdict, "scope": "Only the preview prefix.",
                         "artifact_hashes": [{"path": "source.txt", "sha256": self.digest}]},
                "evidence": [{"path": "source.txt", "sha256": self.digest, "locator": "line1"}]}

    def events(self):
        return log.load_events(self.path, EPISODE)

    def run_cli(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPT), *arguments, "--root", str(self.root), "--episode", EPISODE], text=True, capture_output=True)

    def test_successful_append_query_and_context(self):
        result = log.append(self.root, EPISODE, [self.decision(), self.feedback()])
        self.assertEqual(result["appended"], 2)
        events = self.events()
        self.assertEqual(events[1]["previous_hash"], events[0]["event_hash"])
        result = log.query(events, EPISODE, ["animation"], "payment", 5)
        self.assertEqual(len(result["results"]), 1)
        case = result["results"][0]
        self.assertEqual(case["context"]["viewer_after"], "Readiness lacks a paid role.")
        self.assertIn("unsupported", case["exceptions"])
        self.assertEqual(case["latest_feedback"]["event_id"], "owner-v1")
        self.assertEqual(case["tag_match_count"], 1)

    def test_tampered_event_detected(self):
        log.append(self.root, EPISODE, self.decision())
        self.path.write_bytes(self.path.read_bytes().replace(b"fee return", b"new payment"))
        with self.assertRaisesRegex(log.RecordError, "hash mismatch"):
            self.events()

    def test_duplicate_transaction_leaves_old_bytes(self):
        log.append(self.root, EPISODE, self.decision())
        original = self.path.read_bytes()
        with self.assertRaisesRegex(log.RecordError, "Duplicate"):
            log.append(self.root, EPISODE, self.decision())
        self.assertEqual(self.path.read_bytes(), original)

    def test_atomic_batch_rejects_later_incomplete_record(self):
        log.append(self.root, EPISODE, self.decision())
        original = self.path.read_bytes()
        good = self.decision("other-v1", "other")
        bad = self.decision("broken-v1", "broken")
        del bad["data"]["context"]["viewer_after"]
        with self.assertRaisesRegex(log.RecordError, "viewer_after"):
            log.append(self.root, EPISODE, [good, bad])
        self.assertEqual(self.path.read_bytes(), original)

    def test_failed_first_batch_creates_no_event_log(self):
        first = self.decision()
        with self.assertRaisesRegex(log.RecordError, "Duplicate"):
            log.append(self.root, EPISODE, [first, copy.deepcopy(first)])
        self.assertFalse(self.path.exists())

    def test_stale_evidence_rejected_on_append_without_repinning(self):
        event = self.decision()
        self.source.write_text("Changed evidence")
        with self.assertRaisesRegex(log.RecordError, "Evidence validation failed"):
            log.append(self.root, EPISODE, event)
        self.assertFalse(self.path.exists())
        self.assertEqual(event["evidence"][0]["sha256"], self.digest)

    def test_validate_reports_historical_staleness_without_mutation(self):
        log.append(self.root, EPISODE, self.decision())
        original = self.path.read_bytes()
        self.source.write_text("Later source changed")
        result = self.run_cli("validate", "--evidence")
        self.assertEqual(result.returncode, 1, result.stderr)
        output = json.loads(result.stdout)
        self.assertTrue(output["chain_valid"])
        self.assertEqual(output["evidence_findings"][0]["status"], "stale")
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(self.run_cli("validate").returncode, 0)

    def test_unknown_and_nonlatest_supersedes_rejected(self):
        event = self.decision()
        event["supersedes"] = "missing"
        with self.assertRaisesRegex(log.RecordError, "Unknown supersedes"):
            log.append(self.root, EPISODE, event)
        log.append(self.root, EPISODE, self.decision())
        revision = self.decision("form-v2")
        revision["supersedes"] = "form-v1"
        log.append(self.root, EPISODE, revision)
        third = self.decision("form-v3")
        third["supersedes"] = "form-v1"
        with self.assertRaisesRegex(log.RecordError, "current decision"):
            log.append(self.root, EPISODE, third)

    def test_old_feedback_cannot_approve_new_revision(self):
        log.append(self.root, EPISODE, [self.decision(), self.feedback()])
        revision = self.decision("form-v2")
        revision["supersedes"] = "form-v1"
        log.append(self.root, EPISODE, revision)
        late_old = self.feedback("late-owner-v1", "form-v1")
        log.append(self.root, EPISODE, late_old)
        status = log.statuses(self.events(), EPISODE)[0]
        self.assertEqual(status["latest_decision_event"]["event_id"], "form-v2")
        self.assertIsNone(status["applicable_owner_feedback"])
        self.assertEqual(status["review_state"], "no_owner_verdict_for_revision")

    def test_reviewer_acceptance_is_recommendation_only(self):
        log.append(self.root, EPISODE, [self.decision(), self.feedback(actor="reviewer")])
        status = log.statuses(self.events(), EPISODE)[0]
        self.assertIsNone(status["applicable_owner_feedback"])
        self.assertEqual(status["reviewer_recommendation"]["data"]["verdict"], "accept")
        self.assertFalse(status["canonical_approval"])

    def test_deferred_trigger_required_and_reported(self):
        log.append(self.root, EPISODE, self.decision())
        feedback = self.feedback(verdict="defer")
        with self.assertRaisesRegex(log.RecordError, "deferred_until"):
            log.append(self.root, EPISODE, feedback)
        feedback["data"]["deferred_until"] = "Next avatar recording"
        log.append(self.root, EPISODE, feedback)
        self.assertEqual(log.statuses(self.events(), EPISODE)[0]["deferred_until"], "Next avatar recording")

    def test_owner_acceptance_requires_exact_artifact(self):
        log.append(self.root, EPISODE, self.decision())
        feedback = self.feedback()
        feedback["data"]["artifact_hashes"] = []
        with self.assertRaisesRegex(log.RecordError, "exact artifact"):
            log.append(self.root, EPISODE, feedback)

    def test_feedback_target_must_exist_and_match_decision(self):
        log.append(self.root, EPISODE, self.decision())
        for target, decision_id in (("unknown", "form"), ("form-v1", "other")):
            feedback = self.feedback(target=target)
            feedback["decision_id"] = decision_id
            with self.assertRaises(log.RecordError):
                log.append(self.root, EPISODE, feedback)

    def test_path_traversal_and_absolute_paths_rejected(self):
        for value in ("../source.txt", "/tmp/source.txt", "nested/../source.txt", "C:\\source.txt"):
            with self.subTest(value=value):
                event = self.decision()
                event["evidence"][0]["path"] = value
                with self.assertRaisesRegex(log.RecordError, "Evidence validation failed"):
                    log.append(self.root, EPISODE, event)
        with self.assertRaisesRegex(log.RecordError, "Invalid episode"):
            log.append(self.root, "../../elsewhere", self.decision())

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "source.txt"
            target.write_bytes(self.source.read_bytes())
            (self.root / "escape.txt").symlink_to(target)
            event = self.decision()
            event["evidence"][0]["path"] = "escape.txt"
            with self.assertRaisesRegex(log.RecordError, "escapes repository"):
                log.append(self.root, EPISODE, event)

    def test_historical_reconstruction_is_not_implicit_acceptance(self):
        event = self.decision()
        event["data"]["nuance"]["source_basis"] = "historical_reconstruction"
        event["data"]["historical_disposition"] = "accepted"
        log.append(self.root, EPISODE, event)
        status = log.statuses(self.events(), EPISODE)[0]
        self.assertTrue(status["historical_reconstruction"])
        self.assertEqual(status["review_state"], "historical_reconstruction_no_new_owner_verdict")
        self.assertEqual(status["record_kind"], "historical_reconstruction")

    def test_artifact_binding_invalid_path_and_stale_hash(self):
        log.append(self.root, EPISODE, self.decision())
        original = self.path.read_bytes()
        for binding in ({"path": "../source.txt", "sha256": self.digest},
                        {"path": "source.txt", "sha256": "0" * 64}):
            feedback = self.feedback()
            feedback["data"]["artifact_hashes"] = [binding]
            with self.assertRaisesRegex(log.RecordError, "Evidence validation failed"):
                log.append(self.root, EPISODE, feedback)
            self.assertEqual(self.path.read_bytes(), original)

    def test_acceptance_binds_exact_file_and_reports_later_staleness(self):
        log.append(self.root, EPISODE, [self.decision(), self.feedback()])
        status = log.statuses(self.events(), EPISODE)[0]
        self.assertEqual(status["applicable_owner_feedback"]["data"]["artifact_hashes"],
                         [{"path": "source.txt", "sha256": self.digest}])
        original = self.path.read_bytes()
        self.source.write_text("Revised runtime bytes")
        findings = log.evidence_findings(self.events(), self.root)
        self.assertTrue(any(x["binding_type"] == "artifact" and x["status"] == "stale" for x in findings))
        self.assertEqual(self.path.read_bytes(), original)

    def test_query_keeps_superseded_negative_examples(self):
        reject = self.feedback(verdict="reject")
        log.append(self.root, EPISODE, [self.decision(), reject])
        revision = self.decision("form-v2")
        revision["supersedes"] = "form-v1"
        log.append(self.root, EPISODE, revision)
        result = log.query(self.events(), EPISODE, ["animation"])
        old = next(x for x in result["results"] if x["event"]["event_id"] == "form-v1")
        self.assertFalse(old["is_current_revision"])
        self.assertEqual(old["latest_feedback"]["data"]["verdict"], "reject")

    def test_cli_append_query_and_concurrent_writers(self):
        files = []
        for i in range(2):
            file = self.root / f"event-{i}.json"
            file.write_text(json.dumps(self.decision(f"parallel-{i}", f"decision-{i}")))
            files.append(file)
        commands = [[sys.executable, str(SCRIPT), "append", "--root", str(self.root), "--episode", EPISODE, "--event", str(file)] for file in files]
        processes = [subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for cmd in commands]
        for process in processes:
            stdout, stderr = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 0, stderr)
            self.assertEqual(json.loads(stdout)["appended"], 1)
        self.assertEqual(len(self.events()), 2)
        result = self.run_cli("query", "--tags", "animation,cut-timing", "--limit", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["results"][0]["tag_match_count"], 2)


if __name__ == "__main__":
    unittest.main()
