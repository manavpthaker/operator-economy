from __future__ import annotations

import ast
import copy
import io
import json
import os
import stat
import tempfile
import unittest
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from oe_narration.core import ValidationError, sha256_bytes, sha256_file
from oe_narration import google_service_enablement as se


class _Response:
    def __init__(
        self,
        payload: bytes,
        *,
        status: int = 200,
        url: str,
        content_type: str = "application/json",
        content_encoding: str = "identity",
        declared_length: int | None = None,
        chunks: list[bytes] | None = None,
        headers: object | None = None,
        on_first_read: object | None = None,
    ) -> None:
        self.payload = payload
        self.offset = 0
        self.status = status
        self.url = url
        self.closed = False
        self.chunks = list(chunks) if chunks is not None else None
        self.on_first_read = on_first_read
        self.read_started = False
        self.headers = headers or {
            "Content-Type": content_type,
            "Content-Encoding": content_encoding,
            "Content-Length": str(len(payload) if declared_length is None else declared_length),
        }

    def read(self, size: int = -1) -> bytes:
        if not self.read_started:
            self.read_started = True
            if callable(self.on_first_read):
                self.on_first_read()
        if self.chunks is not None:
            return self.chunks.pop(0) if self.chunks else b""
        if size < 0:
            size = len(self.payload) - self.offset
        result = self.payload[self.offset : self.offset + size]
        self.offset += len(result)
        return result

    def getcode(self) -> int:
        return self.status

    def geturl(self) -> str:
        return self.url

    def close(self) -> None:
        self.closed = True


class _DuplicateHeaders:
    def items(self):
        return [
            ("Content-Type", "application/json"),
            ("Content-Length", "2"),
            ("content-length", "2"),
        ]


class GoogleServiceEnablementTests(unittest.TestCase):
    PROJECT = "test-project"
    PROJECT_NUMBER = "123456789012"
    TOKEN = "ya29.test-secret-access-token-material"

    @classmethod
    def setUpClass(cls) -> None:
        cls.production_root = Path(__file__).resolve().parents[2]
        cls.source_fixture = (
            cls.production_root
            / "fixtures"
            / "step2-v0.5-ai-visibility-v1.1-synthetic-guide-to-saved-c-transfer-microtest"
        )

    @staticmethod
    def _write_json(path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def _system(self) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        fixture = Path(temporary.name).resolve() / "fixture"
        (fixture / "authorizations").mkdir(parents=True)
        (fixture / "evidence").mkdir()

        project_sha = sha256_bytes(self.PROJECT.encode())
        number_sha = sha256_bytes(self.PROJECT_NUMBER.encode())

        diagnosis_source = self.source_fixture / "evidence" / "G1R2-403-DIAGNOSIS.20260826T014109Z.json"
        diagnosis = json.loads(diagnosis_source.read_text(encoding="utf-8"))
        diagnosis["recorded_at"] = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
        diagnosis["live_readback"]["project"]["project_sha256"] = project_sha
        diagnosis["live_readback"]["project"]["project_number_sha256"] = number_sha
        diagnosis_path = fixture / "evidence" / "diagnosis.json"
        self._write_json(diagnosis_path, diagnosis)

        readiness_source = (
            self.source_fixture
            / "evidence"
            / "G1R2-AIPLATFORM-SERVICE-ENABLEMENT-READINESS.20260826T015909Z.json"
        )
        readiness = json.loads(readiness_source.read_text(encoding="utf-8"))
        readiness["recorded_at"] = (datetime.now(timezone.utc) - timedelta(minutes=4)).isoformat()
        readiness["target"]["project_sha256"] = project_sha
        readiness["target"]["project_number_sha256"] = number_sha
        readiness_path = fixture / "evidence" / "readiness.json"
        self._write_json(readiness_path, readiness)

        auth_id = "DRAFT-SVC-test-aiplatform"
        authorization = {
            "schema_version": se.AUTH_SCHEMA,
            "authorization_id": auth_id,
            "status": "draft",
            "approved": False,
            "scope": se.SCOPE,
            "target": {
                "project_sha256": project_sha,
                "project_number_sha256": number_sha,
                "service": se.SERVICE,
            },
            "diagnosis_binding": {
                "path": "evidence/diagnosis.json",
                "sha256": sha256_file(diagnosis_path),
                "project_sha256": project_sha,
                "reported_current_state": "DISABLED",
                "causal_status": "only_confirmed_configuration_anomaly_not_proven_403_cause",
            },
            "readiness_binding": {
                "path": "evidence/readiness.json",
                "sha256": sha256_file(readiness_path),
                "project_sha256": project_sha,
                "project_number_sha256": number_sha,
                "permission": "serviceusage.services.enable",
                "permission_granted": True,
            },
            "runtime_bindings": se._expected_runtime_bindings(draft=True),
            "action": copy.deepcopy(se._ACTION),
            "prospective_active_limits": copy.deepcopy(se._ACTIVE_LIMITS),
            "authorized_limits": copy.deepcopy(se._ZERO_LIMITS),
            "artifacts": se._expected_artifacts(auth_id),
            "required_success_evidence": copy.deepcopy(se._REQUIRED_SUCCESS_EVIDENCE),
            "approved_by": "",
            "approved_at": "",
            "expires_at": "",
            "execution_ready": False,
            "blockers": ["owner approval required"],
            "authority": copy.deepcopy(se._DRAFT_AUTHORITY),
        }
        auth_path = fixture / "authorizations" / "service.DRAFT.json"
        self._write_json(auth_path, authorization)
        return temporary, fixture, auth_path

    def _activate(self, fixture: Path, draft_path: Path) -> Path:
        value = json.loads(draft_path.read_text(encoding="utf-8"))
        now = datetime.now(timezone.utc)
        auth_id = "AUTH-SVC-test-aiplatform"
        value.update(
            {
                "authorization_id": auth_id,
                "status": "active",
                "approved": True,
                "approved_by": "Manav Thaker",
                "approved_at": (now - timedelta(minutes=1)).isoformat(),
                "expires_at": (now + timedelta(hours=1)).isoformat(),
                "execution_ready": True,
                "blockers": [],
                "authorized_limits": copy.deepcopy(se._ACTIVE_LIMITS),
                "authority": copy.deepcopy(se._ACTIVE_AUTHORITY),
                "artifacts": se._expected_artifacts(auth_id),
                "runtime_bindings": {
                    **se._expected_runtime_bindings(draft=False),
                    "git_commit": "a" * 40,
                },
            }
        )
        active = fixture / "authorizations" / f"{auth_id}.json"
        self._write_json(active, value)
        return active

    @staticmethod
    def _json_bytes(value: dict) -> bytes:
        return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()

    def _response_set(
        self,
        *,
        pre_state: str = "DISABLED",
        pre_number: str | None = None,
        final_state: str = "ENABLED",
        polls: int = 1,
    ) -> list[_Response]:
        number = pre_number or self.PROJECT_NUMBER
        service_url, enable_url = se._service_urls(self.PROJECT_NUMBER)

        def operation(done: bool) -> dict:
            value: dict = {"name": "operations/acat.test", "done": done}
            if done:
                value["response"] = {
                    "@type": "type.googleapis.com/google.api.serviceusage.v1.EnableServiceResponse",
                    "service": {
                        "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                        "state": "ENABLED",
                    },
                }
            return value

        result = [
            _Response(
                self._json_bytes(
                    {
                        "name": f"projects/{number}/services/{se.SERVICE}",
                        "state": pre_state,
                    }
                ),
                url=service_url,
            ),
            _Response(
                self._json_bytes(operation(polls == 0)),
                url=enable_url,
            ),
        ]
        for index in range(polls):
            result.append(
                _Response(
                    self._json_bytes(
                        operation(index == polls - 1)
                    ),
                    url=f"{se.BASE_ENDPOINT}/operations/acat.test",
                )
            )
        result.append(
            _Response(
                self._json_bytes(
                    {
                        "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                        "state": final_state,
                    }
                ),
                url=service_url,
            )
        )
        return result

    def _execute(
        self,
        fixture: Path,
        active: Path,
        responses: list[object],
        *,
        sleep_side_effect: object | None = None,
    ) -> tuple[dict, list[object]]:
        calls: list[object] = []
        consumption = se._expected_artifacts("AUTH-SVC-test-aiplatform")["consumption_record_path"]

        def token_loader(_gcloud: str, _timeout: float) -> str:
            self.assertTrue((fixture / consumption).is_file())
            return self.TOKEN

        def opener(request, _timeout):
            self.assertTrue((fixture / consumption).is_file())
            calls.append(request)
            if not responses:
                raise AssertionError("unexpected provider call")
            value = responses.pop(0)
            if isinstance(value, BaseException):
                raise value
            return value

        environment = {
            se.PROJECT_ENV: self.PROJECT,
            se.PROJECT_NUMBER_ENV: self.PROJECT_NUMBER,
            "ELEVENLABS_API_KEY": "xi-unrelated-secret-must-not-be-used",
        }
        with (
            mock.patch.dict(os.environ, environment, clear=True),
            mock.patch.object(se, "_verify_committed_runtime", return_value={"git_head": "b" * 40, "runtime_commit": "a" * 40}),
            mock.patch.object(se.pt, "_preflight_google_adc", return_value="/safe/gcloud"),
            mock.patch.object(se.pt, "_load_google_access_token", side_effect=token_loader),
            mock.patch.object(se, "_open_service_usage_request", side_effect=opener),
            mock.patch.object(se, "_sleep", side_effect=sleep_side_effect),
        ):
            result = se.execute_google_service_enablement(active, timeout=30)
        return result, calls

    def test_draft_is_credential_free_and_zero_authority(self) -> None:
        temporary, _fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        with (
            mock.patch.object(se.pt, "_preflight_google_adc") as adc,
            mock.patch.object(se, "_open_service_usage_request") as network,
        ):
            result = se.dry_run_google_service_enablement(draft)
        self.assertTrue(result["valid"])
        self.assertEqual(result["authorization_status"], "draft")
        self.assertFalse(result["provider_action_authorized"])
        self.assertFalse(result["credentials_accessed"])
        self.assertFalse(result["network_called"])
        self.assertEqual(result["authorized_limits"], se._ZERO_LIMITS)
        adc.assert_not_called()
        network.assert_not_called()

    def test_active_success_exact_calls_urls_headers_and_private_artifacts(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        responses = self._response_set(polls=1)
        result, calls = self._execute(fixture, active, responses)
        self.assertEqual(result["outcome"], "success")
        self.assertEqual(result["calls"]["http_calls_total"], 4)
        self.assertEqual(result["calls"]["enable_attempts"], 1)
        self.assertEqual([request.get_method() for request in calls], ["GET", "POST", "GET", "GET"])
        service_url, enable_url = se._service_urls(self.PROJECT_NUMBER)
        self.assertEqual(
            [request.full_url for request in calls],
            [service_url, enable_url, f"{se.BASE_ENDPOINT}/operations/acat.test", service_url],
        )
        self.assertIsNone(calls[0].data)
        self.assertEqual(calls[1].data, b"")
        for request in calls:
            headers = dict(request.header_items())
            self.assertEqual(headers["X-goog-user-project"], self.PROJECT)
            self.assertEqual(headers["Authorization"], f"Bearer {self.TOKEN}")
            self.assertNotIn(self.PROJECT, request.full_url)
        consumption = fixture / result["run_receipt"]["path"].replace(".run.json", "")
        del consumption
        artifacts = se._expected_artifacts("AUTH-SVC-test-aiplatform")
        for relative in (
            artifacts["consumption_record_path"],
            artifacts["success_receipt_path"],
        ):
            path = fixture / relative
            self.assertTrue(path.is_file())
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            raw = path.read_bytes()
            self.assertNotIn(self.PROJECT.encode(), raw)
            self.assertNotIn(self.PROJECT_NUMBER.encode(), raw)
            self.assertNotIn(self.TOKEN.encode(), raw)
            self.assertNotIn(b"xi-unrelated-secret", raw)
        self.assertFalse((fixture / artifacts["failure_receipt_path"]).exists())
        receipt = json.loads((fixture / artifacts["success_receipt_path"]).read_text())
        self.assertEqual(receipt["pre_enable_readback"]["state"], "DISABLED")
        self.assertEqual(receipt["post_enable_readback"]["state"], "ENABLED")
        self.assertEqual(receipt["operation_completion"]["poll_count"], 1)
        self.assertNotIn("operations/acat.test", json.dumps(receipt))
        self.assertFalse(receipt["synthetic_guide_generation_authorized"])
        self.assertFalse(receipt["iam_mutation_authorized"])
        self.assertFalse(receipt["billing_mutation_authorized"])

    def test_exact_twice_readback_and_once_mutation_with_immediate_operation(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        result, calls = self._execute(fixture, active, self._response_set(polls=0))
        self.assertEqual(len(calls), 3)
        self.assertEqual(result["calls"]["pre_enable_state_readbacks"], 1)
        self.assertEqual(result["calls"]["enable_attempts"], 1)
        self.assertEqual(result["calls"]["operation_polls"], 0)
        self.assertEqual(result["calls"]["post_enable_state_readbacks"], 1)

    def test_wrong_project_number_readback_fails_before_enable(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        with self.assertRaisesRegex(ValidationError, "service_readback_resource_invalid"):
            self._execute(fixture, active, self._response_set(pre_number="999999999999"))
        artifacts = se._expected_artifacts("AUTH-SVC-test-aiplatform")
        failure = json.loads((fixture / artifacts["failure_receipt_path"]).read_text())
        self.assertEqual(failure["calls"]["http_calls_total"], 1)
        self.assertEqual(failure["calls"]["enable_attempts"], 0)
        self.assertEqual(
            failure["provider_response_bytes_total"],
            failure["failed_response_bytes"],
        )

    def test_pre_enabled_state_refuses_mutation(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        with self.assertRaisesRegex(ValidationError, "service_readback_state_unexpected"):
            self._execute(fixture, active, self._response_set(pre_state="ENABLED"))
        failure = json.loads(
            (fixture / se._expected_artifacts("AUTH-SVC-test-aiplatform")["failure_receipt_path"]).read_text()
        )
        self.assertEqual(failure["calls"]["enable_attempts"], 0)

    def test_final_disabled_state_fails_without_retry_or_disable(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        with self.assertRaisesRegex(ValidationError, "service_readback_state_unexpected"):
            self._execute(fixture, active, self._response_set(final_state="DISABLED"))
        failure = json.loads(
            (fixture / se._expected_artifacts("AUTH-SVC-test-aiplatform")["failure_receipt_path"]).read_text()
        )
        self.assertEqual(failure["calls"]["enable_attempts"], 1)
        self.assertEqual(failure["calls"]["post_enable_state_readbacks"], 1)
        self.assertEqual(failure["retries_made"], 0)
        self.assertFalse(failure["service_disablement_authorized"])

    def test_poll_ceiling_stops_then_uses_only_authorized_resolution_readback(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        service_url, enable_url = se._service_urls(self.PROJECT_NUMBER)
        responses: list[object] = [
            _Response(self._json_bytes({"name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}", "state": "DISABLED"}), url=service_url),
            _Response(self._json_bytes({"name": "operations/acat.test", "done": False}), url=enable_url),
        ]
        responses.extend(
            _Response(self._json_bytes({"name": "operations/acat.test", "done": False}), url=f"{se.BASE_ENDPOINT}/operations/acat.test")
            for _ in range(se.MAX_OPERATION_POLLS)
        )
        with self.assertRaisesRegex(ValidationError, "operation_poll_ceiling_exhausted"):
            self._execute(fixture, active, responses)
        failure = json.loads(
            (fixture / se._expected_artifacts("AUTH-SVC-test-aiplatform")["failure_receipt_path"]).read_text()
        )
        self.assertEqual(failure["calls"]["operation_polls"], 12)
        self.assertEqual(failure["calls"]["http_calls_total"], 15)
        self.assertEqual(failure["calls"]["post_enable_state_readbacks"], 1)
        self.assertEqual(failure["reason_code"], "operation_poll_ceiling_exhausted")
        self.assertEqual(
            failure["resolution_readback_failure"]["code"],
            "provider_transport_failure",
        )
        self.assertEqual(failure["service_state_resolution"], "indeterminate_after_attempt")
        self.assertTrue(failure["operation_may_still_be_running"])
        self.assertTrue(failure["manual_readback_required"])

    def test_ambiguous_enable_http_failure_gets_one_readback_without_post_retry(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        service_url, enable_url = se._service_urls(self.PROJECT_NUMBER)
        error_raw = self._json_bytes(
            {
                "error": {
                    "code": 503,
                    "status": "UNAVAILABLE",
                    "message": f"private {self.TOKEN} {self.PROJECT_NUMBER}",
                }
            }
        )
        enable_error = urllib.error.HTTPError(
            enable_url,
            503,
            "private provider message",
            {"Content-Type": "application/json", "Content-Length": str(len(error_raw))},
            io.BytesIO(error_raw),
        )
        responses: list[object] = [
            _Response(
                self._json_bytes(
                    {
                        "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                        "state": "DISABLED",
                    }
                ),
                url=service_url,
            ),
            enable_error,
            _Response(
                self._json_bytes(
                    {
                        "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                        "state": "ENABLED",
                    }
                ),
                url=service_url,
            ),
        ]
        with self.assertRaisesRegex(ValidationError, "provider_http_failure"):
            self._execute(fixture, active, responses)
        artifacts = se._expected_artifacts("AUTH-SVC-test-aiplatform")
        receipt_raw = (fixture / artifacts["failure_receipt_path"]).read_bytes()
        receipt = json.loads(receipt_raw)
        self.assertEqual(receipt["calls"]["http_calls_total"], 3)
        self.assertEqual(receipt["calls"]["enable_attempts"], 1)
        self.assertEqual(receipt["calls"]["post_enable_state_readbacks"], 1)
        self.assertEqual(receipt["primary_failure"]["phase"], "enable")
        self.assertEqual(receipt["primary_failure"]["http_status"], 503)
        self.assertIsNone(receipt["resolution_readback_failure"])
        self.assertEqual(receipt["post_enable_readback"]["state"], "ENABLED")
        self.assertEqual(receipt["service_state_resolution"], "enabled_confirmed")
        self.assertTrue(receipt["enablement_may_have_completed"])
        self.assertTrue(receipt["operation_may_still_be_running"])
        self.assertFalse(receipt["manual_readback_required"])
        self.assertEqual(receipt["retries_made"], 0)
        self.assertNotIn(self.TOKEN.encode(), receipt_raw)
        self.assertNotIn(self.PROJECT_NUMBER.encode(), receipt_raw)

    def test_terminal_operation_error_and_disabled_readback_are_distinguished(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        service_url, enable_url = se._service_urls(self.PROJECT_NUMBER)
        operation_error = {
            "name": "operations/acat.test",
            "done": True,
            "error": {
                "code": 7,
                "status": "PERMISSION_DENIED",
                "message": f"private {self.TOKEN} {self.PROJECT}",
                "details": [
                    {
                        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
                        "reason": "IAM_PERMISSION_DENIED",
                        "domain": "serviceusage.googleapis.com",
                        "metadata": {
                            "service": "serviceusage.googleapis.com",
                            "permission": "serviceusage.services.enable",
                        },
                    }
                ],
            },
        }
        responses: list[object] = [
            _Response(
                self._json_bytes(
                    {
                        "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                        "state": "DISABLED",
                    }
                ),
                url=service_url,
            ),
            _Response(self._json_bytes(operation_error), url=enable_url),
            _Response(
                self._json_bytes(
                    {
                        "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                        "state": "DISABLED",
                    }
                ),
                url=service_url,
            ),
        ]
        with self.assertRaisesRegex(ValidationError, "enable_operation_failed"):
            self._execute(fixture, active, responses)
        receipt_path = fixture / se._expected_artifacts("AUTH-SVC-test-aiplatform")["failure_receipt_path"]
        receipt_raw = receipt_path.read_bytes()
        receipt = json.loads(receipt_raw)
        self.assertEqual(receipt["calls"]["http_calls_total"], 3)
        self.assertEqual(receipt["service_state_resolution"], "disabled_confirmed")
        self.assertFalse(receipt["enablement_may_have_completed"])
        self.assertFalse(receipt["operation_may_still_be_running"])
        self.assertFalse(receipt["manual_readback_required"])
        self.assertEqual(
            receipt["primary_failure"]["provider_error"]["error_info"],
            [
                {
                    "reason": "IAM_PERMISSION_DENIED",
                    "domain": "serviceusage.googleapis.com",
                    "service": "serviceusage.googleapis.com",
                    "permission": "serviceusage.services.enable",
                }
            ],
        )
        self.assertNotIn(self.TOKEN.encode(), receipt_raw)
        self.assertNotIn(self.PROJECT.encode(), receipt_raw)

    def test_resolution_readback_failure_is_separate_and_counted_once(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        service_url, enable_url = se._service_urls(self.PROJECT_NUMBER)
        error_raw = self._json_bytes(
            {"error": {"code": 503, "status": "UNAVAILABLE", "message": self.TOKEN}}
        )
        responses: list[object] = [
            _Response(
                self._json_bytes(
                    {
                        "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                        "state": "DISABLED",
                    }
                ),
                url=service_url,
            ),
            _Response(
                self._json_bytes({"name": "operations/acat.test", "done": False}),
                url=enable_url,
            ),
            TimeoutError("primary poll transport failed"),
            urllib.error.HTTPError(
                service_url,
                503,
                "private",
                {"Content-Type": "application/json", "Content-Length": str(len(error_raw))},
                io.BytesIO(error_raw),
            ),
        ]
        with self.assertRaisesRegex(ValidationError, "provider_transport_failure"):
            self._execute(fixture, active, responses)
        receipt_path = fixture / se._expected_artifacts("AUTH-SVC-test-aiplatform")["failure_receipt_path"]
        receipt_raw = receipt_path.read_bytes()
        receipt = json.loads(receipt_raw)
        resolution = receipt["resolution_readback_failure"]
        self.assertEqual(receipt["reason_code"], "provider_transport_failure")
        self.assertEqual(receipt["primary_failure"]["phase"], "operation_poll")
        self.assertEqual(receipt["primary_failure"]["response_bytes"], 0)
        self.assertEqual(resolution["code"], "provider_http_failure")
        self.assertEqual(resolution["http_status"], 503)
        self.assertEqual(resolution["response_bytes"], len(error_raw))
        self.assertEqual(resolution["response_sha256"], sha256_bytes(error_raw))
        self.assertIsNotNone(resolution["request_started_at"])
        self.assertIsNotNone(resolution["request_completed_at"])
        expected_total = (
            receipt["pre_enable_readback"]["response_bytes"]
            + receipt["enable_operation"]["response_bytes"]
            + len(error_raw)
        )
        self.assertEqual(receipt["provider_response_bytes_total"], expected_total)
        self.assertNotIn(self.TOKEN.encode(), receipt_raw)

    def test_http_error_is_bounded_redacted_and_not_retried(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        service_url, _enable_url = se._service_urls(self.PROJECT_NUMBER)
        raw = self._json_bytes(
            {
                "error": {
                    "code": 403,
                    "status": "PERMISSION_DENIED",
                    "message": f"secret {self.TOKEN} project {self.PROJECT}",
                    "details": [
                        {
                            "@type": "type.googleapis.com/google.rpc.ErrorInfo",
                            "reason": "SERVICE_DISABLED",
                            "domain": "serviceusage.googleapis.com",
                            "metadata": {"service": se.SERVICE, "consumer": self.PROJECT},
                        }
                    ],
                }
            }
        )
        error = urllib.error.HTTPError(
            service_url,
            403,
            "forbidden",
            {"Content-Type": "application/json", "Content-Length": str(len(raw))},
            io.BytesIO(raw),
        )
        with self.assertRaisesRegex(ValidationError, "provider_http_failure"):
            self._execute(fixture, active, [error])
        failure_path = fixture / se._expected_artifacts("AUTH-SVC-test-aiplatform")["failure_receipt_path"]
        receipt_raw = failure_path.read_bytes()
        self.assertNotIn(self.TOKEN.encode(), receipt_raw)
        self.assertNotIn(self.PROJECT.encode(), receipt_raw)
        receipt = json.loads(receipt_raw)
        self.assertEqual(receipt["calls"]["http_calls_total"], 1)
        self.assertEqual(receipt["provider_error"]["status"], "PERMISSION_DENIED")
        self.assertEqual(receipt["failed_response_sha256"], sha256_bytes(raw))
        self.assertEqual(receipt["retries_made"], 0)

    def test_redirect_mime_encoding_duplicate_headers_and_truncation_fail(self) -> None:
        cases = [
            _Response(b"{}", url="https://example.invalid/redirected"),
            _Response(b"{}", url=se._service_urls(self.PROJECT_NUMBER)[0], content_type="text/plain"),
            _Response(b"{}", url=se._service_urls(self.PROJECT_NUMBER)[0], content_encoding="gzip"),
            _Response(b"{}", url=se._service_urls(self.PROJECT_NUMBER)[0], headers=_DuplicateHeaders()),
            _Response(b"{}", url=se._service_urls(self.PROJECT_NUMBER)[0], declared_length=50),
        ]
        for response in cases:
            with self.subTest(response=response):
                temporary, fixture, draft = self._system()
                active = self._activate(fixture, draft)
                with self.assertRaises(ValidationError):
                    self._execute(fixture, active, [response])
                temporary.cleanup()

    def test_short_first_chunk_plus_trailing_bytes_is_not_ignored(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        service_url, _ = se._service_urls(self.PROJECT_NUMBER)
        first = self._json_bytes({"name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}", "state": "DISABLED"})
        response = _Response(
            first + b"forbidden-trailing",
            url=service_url,
            chunks=[first, b"forbidden-trailing", b""],
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaisesRegex(ValidationError, "provider_response_json_invalid"):
            self._execute(fixture, active, [response])

    def test_operation_result_union_and_terminal_service_binding_are_strict(self) -> None:
        resource = f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}"
        invalid_payloads = (
            {"name": "operations/acat.test", "done": True},
            {
                "name": "operations/acat.test",
                "done": False,
                "response": {},
            },
            {
                "name": "operations/acat.test",
                "done": True,
                "error": {},
                "response": {},
            },
            {
                "name": "operations/acat.test",
                "done": True,
                "response": {
                    "@type": "type.googleapis.com/google.api.serviceusage.v1.EnableServiceResponse",
                    "service": {
                        "name": f"projects/999999999999/services/{se.SERVICE}",
                        "state": "ENABLED",
                    },
                },
            },
            {
                "name": "operations/acat.test",
                "done": True,
                "response": {
                    "@type": "type.googleapis.com/google.api.serviceusage.v1.OtherResponse",
                    "service": {"name": resource, "state": "ENABLED"},
                },
            },
        )
        for payload in invalid_payloads:
            with self.subTest(payload=payload), self.assertRaises(se._ServiceFailure):
                raw = self._json_bytes(payload)
                se._operation_state(
                    se._ServiceResponse(
                        response_bytes=len(raw),
                        response_sha256=sha256_bytes(raw),
                        payload=payload,
                        provider_identifiers={},
                        provider_usage={},
                    ),
                    expected_name=None,
                    expected_resource_name=resource,
                )

    def test_terminal_poll_crossing_operation_elapsed_cap_fails_and_reconciles(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        service_url, enable_url = se._service_urls(self.PROJECT_NUMBER)
        clock = [datetime.now(timezone.utc)]

        def cross_elapsed_cap() -> None:
            clock[0] += timedelta(seconds=se.MAX_OPERATION_ELAPSED_SECONDS + 1)

        terminal = {
            "name": "operations/acat.test",
            "done": True,
            "response": {
                "@type": "type.googleapis.com/google.api.serviceusage.v1.EnableServiceResponse",
                "service": {
                    "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                    "state": "ENABLED",
                },
            },
        }
        responses: list[object] = [
            _Response(
                self._json_bytes(
                    {
                        "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                        "state": "DISABLED",
                    }
                ),
                url=service_url,
            ),
            _Response(
                self._json_bytes({"name": "operations/acat.test", "done": False}),
                url=enable_url,
            ),
            _Response(
                self._json_bytes(terminal),
                url=f"{se.BASE_ENDPOINT}/operations/acat.test",
                on_first_read=cross_elapsed_cap,
            ),
            _Response(
                self._json_bytes(
                    {
                        "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                        "state": "ENABLED",
                    }
                ),
                url=service_url,
            ),
        ]
        with (
            mock.patch.object(se, "_now", side_effect=lambda: clock[0]),
            self.assertRaisesRegex(ValidationError, "operation_elapsed_ceiling_exhausted"),
        ):
            self._execute(fixture, active, responses)
        receipt = json.loads(
            (
                fixture
                / se._expected_artifacts("AUTH-SVC-test-aiplatform")["failure_receipt_path"]
            ).read_text()
        )
        self.assertEqual(receipt["calls"]["operation_polls"], 1)
        self.assertEqual(receipt["calls"]["http_calls_total"], 4)
        self.assertEqual(receipt["reason_code"], "operation_elapsed_ceiling_exhausted")
        self.assertEqual(receipt["service_state_resolution"], "enabled_confirmed")
        self.assertFalse(receipt["manual_readback_required"])
        self.assertFalse(
            (
                fixture
                / se._expected_artifacts("AUTH-SVC-test-aiplatform")["success_receipt_path"]
            ).exists()
        )

    def test_poll_at_exact_operation_elapsed_ceiling_is_rejected_before_network(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        service_url, enable_url = se._service_urls(self.PROJECT_NUMBER)
        clock = [datetime.now(timezone.utc)]

        def reach_exact_ceiling(_seconds: float) -> None:
            clock[0] += timedelta(seconds=se.MAX_OPERATION_ELAPSED_SECONDS)

        responses: list[object] = [
            _Response(
                self._json_bytes(
                    {
                        "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                        "state": "DISABLED",
                    }
                ),
                url=service_url,
            ),
            _Response(
                self._json_bytes({"name": "operations/acat.test", "done": False}),
                url=enable_url,
            ),
            _Response(
                self._json_bytes(
                    {
                        "name": f"projects/{self.PROJECT_NUMBER}/services/{se.SERVICE}",
                        "state": "ENABLED",
                    }
                ),
                url=service_url,
            ),
        ]
        with (
            mock.patch.object(se, "_now", side_effect=lambda: clock[0]),
            self.assertRaisesRegex(ValidationError, "operation_elapsed_ceiling_exhausted"),
        ):
            self._execute(
                fixture,
                active,
                responses,
                sleep_side_effect=reach_exact_ceiling,
            )
        receipt = json.loads(
            (
                fixture
                / se._expected_artifacts("AUTH-SVC-test-aiplatform")["failure_receipt_path"]
            ).read_text()
        )
        self.assertEqual(receipt["calls"]["operation_polls"], 0)
        self.assertEqual(receipt["calls"]["http_calls_total"], 3)
        self.assertEqual(receipt["calls"]["post_enable_state_readbacks"], 1)
        self.assertEqual(receipt["service_state_resolution"], "enabled_confirmed")

    def test_oversize_response_fails_at_one_call(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        service_url, _ = se._service_urls(self.PROJECT_NUMBER)
        response = _Response(
            b"x" * (se.MAX_RESPONSE_BYTES_PER_CALL + 1),
            url=service_url,
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaisesRegex(ValidationError, "provider_response_byte_cap_exceeded"):
            self._execute(fixture, active, [response])
        failure = json.loads(
            (fixture / se._expected_artifacts("AUTH-SVC-test-aiplatform")["failure_receipt_path"]).read_text()
        )
        self.assertEqual(failure["calls"]["http_calls_total"], 1)
        self.assertEqual(failure["calls"]["enable_attempts"], 0)

    def test_missing_or_mismatched_private_bindings_fail_before_consumption(self) -> None:
        for environment in (
            {},
            {se.PROJECT_ENV: self.PROJECT},
            {se.PROJECT_ENV: "wrong-project", se.PROJECT_NUMBER_ENV: self.PROJECT_NUMBER},
            {se.PROJECT_ENV: self.PROJECT, se.PROJECT_NUMBER_ENV: "999999999999"},
        ):
            with self.subTest(environment=environment):
                temporary, fixture, draft = self._system()
                active = self._activate(fixture, draft)
                with (
                    mock.patch.dict(os.environ, environment, clear=True),
                    mock.patch.object(se, "_verify_committed_runtime") as source,
                    mock.patch.object(se.pt, "_preflight_google_adc") as adc,
                    mock.patch.object(se, "_open_service_usage_request") as network,
                    self.assertRaisesRegex(ValidationError, "setup failed closed"),
                ):
                    se.execute_google_service_enablement(active)
                self.assertFalse((fixture / se._expected_artifacts("AUTH-SVC-test-aiplatform")["consumption_record_path"]).exists())
                source.assert_not_called()
                adc.assert_not_called()
                network.assert_not_called()
                temporary.cleanup()

    def test_source_or_adc_preflight_failure_is_preconsumption(self) -> None:
        for seam in ("source", "adc"):
            with self.subTest(seam=seam):
                temporary, fixture, draft = self._system()
                active = self._activate(fixture, draft)
                environment = {se.PROJECT_ENV: self.PROJECT, se.PROJECT_NUMBER_ENV: self.PROJECT_NUMBER}
                source_effect = ValidationError("dirty") if seam == "source" else {"git_head": "b" * 40, "runtime_commit": "a" * 40}
                adc_effect = ValidationError("unsafe") if seam == "adc" else "/safe/gcloud"
                with (
                    mock.patch.dict(os.environ, environment, clear=True),
                    mock.patch.object(se, "_verify_committed_runtime", side_effect=source_effect if isinstance(source_effect, Exception) else None, return_value=None if isinstance(source_effect, Exception) else source_effect),
                    mock.patch.object(se.pt, "_preflight_google_adc", side_effect=adc_effect if isinstance(adc_effect, Exception) else None, return_value=None if isinstance(adc_effect, Exception) else adc_effect),
                    mock.patch.object(se.pt, "_load_google_access_token") as token,
                    mock.patch.object(se, "_open_service_usage_request") as network,
                    self.assertRaisesRegex(ValidationError, "setup failed closed"),
                ):
                    se.execute_google_service_enablement(active)
                self.assertFalse((fixture / se._expected_artifacts("AUTH-SVC-test-aiplatform")["consumption_record_path"]).exists())
                token.assert_not_called()
                network.assert_not_called()
                temporary.cleanup()

    def test_descendant_head_change_to_unbound_import_fails_source_gate(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        contract = se._validate_authorization(active, require_active=True)
        repository = Path(temporary.name).resolve()
        auth_relative = active.relative_to(repository).as_posix()
        forbidden_delta = (
            auth_relative.encode("utf-8")
            + b"\x00"
            + se.CLI_RELATIVE.replace("cli.py", "audio.py").encode("utf-8")
            + b"\x00"
        )
        with (
            mock.patch.object(se, "_repository_root", return_value=repository),
            mock.patch.object(
                se,
                "_git",
                side_effect=[b"b" * 40 + b"\n", b"", forbidden_delta],
            ),
            self.assertRaisesRegex(
                ValidationError,
                "delta must be exactly the active authorization path",
            ),
        ):
            se._verify_committed_runtime(contract)

    def test_failure_receipt_timestamp_rejects_backward_clock(self) -> None:
        baseline = datetime.now(timezone.utc)
        with self.assertRaisesRegex(ValidationError, "clock moved backwards"):
            se._failure_timestamp(
                baseline - timedelta(microseconds=1),
                (baseline, None),
            )

    def test_token_failure_consumes_authority_and_writes_redacted_failure(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        environment = {se.PROJECT_ENV: self.PROJECT, se.PROJECT_NUMBER_ENV: self.PROJECT_NUMBER}
        with (
            mock.patch.dict(os.environ, environment, clear=True),
            mock.patch.object(se, "_verify_committed_runtime", return_value={"git_head": "b" * 40, "runtime_commit": "a" * 40}),
            mock.patch.object(se.pt, "_preflight_google_adc", return_value="/safe/gcloud"),
            mock.patch.object(se.pt, "_load_google_access_token", side_effect=se.pt._GuideExecutionFailure("google_adc_token_refresh_failed")),
            mock.patch.object(se, "_open_service_usage_request") as network,
            self.assertRaisesRegex(ValidationError, "unexpected_sanitized_failure"),
        ):
            se.execute_google_service_enablement(active)
        artifacts = se._expected_artifacts("AUTH-SVC-test-aiplatform")
        self.assertTrue((fixture / artifacts["consumption_record_path"]).exists())
        failure_raw = (fixture / artifacts["failure_receipt_path"]).read_bytes()
        self.assertNotIn(self.TOKEN.encode(), failure_raw)
        failure = json.loads(failure_raw)
        self.assertTrue(failure["credential_refresh_attempted"])
        self.assertTrue(failure["network_called"])
        self.assertEqual(failure["calls"]["http_calls_total"], 0)
        network.assert_not_called()

    def test_existing_artifact_and_expired_authority_fail_before_provider_access(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        active = self._activate(fixture, draft)
        failure_path = fixture / se._expected_artifacts("AUTH-SVC-test-aiplatform")["failure_receipt_path"]
        failure_path.parent.mkdir(parents=True)
        failure_path.write_text("collision")
        with (
            mock.patch.object(se.pt, "_preflight_google_adc") as adc,
            mock.patch.object(se, "_open_service_usage_request") as network,
            self.assertRaises(ValidationError),
        ):
            se.execute_google_service_enablement(active)
        adc.assert_not_called()
        network.assert_not_called()

        failure_path.unlink()
        value = json.loads(active.read_text())
        now = datetime.now(timezone.utc)
        value["approved_at"] = (now - timedelta(hours=2)).isoformat()
        value["expires_at"] = (now - timedelta(hours=1)).isoformat()
        self._write_json(active, value)
        with self.assertRaises(ValidationError):
            se.validate_google_service_enablement_authorization(active)

    def test_authority_type_coercion_unknown_keys_and_permission_tamper_fail(self) -> None:
        mutators = [
            lambda value: value["authority"].__setitem__("service_enablement_authorized", 1),
            lambda value: value["authorized_limits"].__setitem__("max_enable_attempts", True),
            lambda value: value.__setitem__("network_override", True),
            lambda value: value["readiness_binding"].__setitem__("permission_granted", False),
            lambda value: value["target"].__setitem__("service", "other.googleapis.com"),
            lambda value: value["runtime_bindings"].__setitem__(
                "cli_path", "runtime/other-cli.py"
            ),
            lambda value: value["required_success_evidence"].__setitem__(
                "raw_project_number_forbidden", False
            ),
        ]
        for mutate in mutators:
            with self.subTest(mutate=mutate):
                temporary, _fixture, draft = self._system()
                value = json.loads(draft.read_text())
                mutate(value)
                self._write_json(draft, value)
                with self.assertRaises(ValidationError):
                    se.validate_google_service_enablement_authorization(draft)
                temporary.cleanup()

    def test_readiness_hash_semantics_and_symlink_are_enforced(self) -> None:
        temporary, fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        value = json.loads(draft.read_text())
        readiness_path = fixture / value["readiness_binding"]["path"]
        readiness = json.loads(readiness_path.read_text())
        readiness["readiness"]["permission_granted"] = False
        self._write_json(readiness_path, readiness)
        value["readiness_binding"]["sha256"] = sha256_file(readiness_path)
        self._write_json(draft, value)
        with self.assertRaises(ValidationError):
            se.validate_google_service_enablement_authorization(draft)

        readiness_path.unlink()
        outside = Path(temporary.name) / "outside.json"
        self._write_json(outside, readiness)
        readiness_path.symlink_to(outside)
        with self.assertRaises(ValidationError):
            se.validate_google_service_enablement_authorization(draft)

    def test_duplicate_keys_in_authority_and_evidence_fail_closed(self) -> None:
        for target in ("authorization", "diagnosis", "readiness"):
            with self.subTest(target=target):
                temporary, fixture, draft = self._system()
                try:
                    authorization = json.loads(draft.read_text(encoding="utf-8"))
                    if target == "authorization":
                        raw = draft.read_text(encoding="utf-8")
                        raw = raw.replace(
                            '  "approved": false,',
                            '  "approved": false,\n  "approved": false,',
                            1,
                        )
                        draft.write_text(raw, encoding="utf-8")
                    else:
                        binding_key = f"{target}_binding"
                        evidence_path = fixture / authorization[binding_key]["path"]
                        raw = evidence_path.read_text(encoding="utf-8")
                        schema_value = json.loads(raw)["schema_version"]
                        raw = raw.replace(
                            f'  "schema_version": "{schema_value}",',
                            (
                                f'  "schema_version": "{schema_value}",\n'
                                f'  "schema_version": "{schema_value}",'
                            ),
                            1,
                        )
                        evidence_path.write_text(raw, encoding="utf-8")
                        authorization[binding_key]["sha256"] = sha256_file(evidence_path)
                        self._write_json(draft, authorization)
                    with self.assertRaises(ValidationError):
                        se.validate_google_service_enablement_authorization(draft)
                finally:
                    temporary.cleanup()

    def test_receipt_source_contains_no_duplicate_literal_dict_keys(self) -> None:
        source_path = Path(se.__file__).resolve()
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        duplicates: list[tuple[int, str]] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            keys = [
                key.value
                for key in node.keys
                if isinstance(key, ast.Constant) and isinstance(key.value, str)
            ]
            for key in set(keys):
                if keys.count(key) > 1:
                    duplicates.append((node.lineno, key))
        self.assertEqual(duplicates, [])

    def test_runtime_binding_contract_includes_direct_module_and_all_imported_authority_code(self) -> None:
        bindings = se._expected_runtime_bindings(draft=True)
        self.assertEqual(
            set(bindings),
            {
                "git_commit",
                "executor_path",
                "executor_sha256",
                "credential_runtime_path",
                "credential_runtime_sha256",
                "cli_path",
                "cli_sha256",
                "core_path",
                "core_sha256",
                "init_path",
                "init_sha256",
                "schema_path",
                "schema_sha256",
            },
        )
        self.assertEqual(bindings["cli_path"], se.CLI_RELATIVE)
        self.assertEqual(bindings["init_path"], se.INIT_RELATIVE)

    def test_schema_json_parses_and_cli_wiring_defaults_to_dry_run(self) -> None:
        schema = self.production_root / "schemas" / "google-service-enablement-authorization.schema.json"
        value = json.loads(schema.read_text(encoding="utf-8"))
        self.assertEqual(value["properties"]["schema_version"]["const"], se.AUTH_SCHEMA)
        self.assertIn("cli_path", value["$defs"]["runtimeBindings"]["required"])
        self.assertIn("init_path", value["$defs"]["runtimeBindings"]["required"])
        self.assertEqual(
            value["$defs"]["action"]["properties"]["enable"]["const"]["body_bytes"],
            0,
        )
        from oe_narration.cli import build_parser, dispatch

        temporary, _fixture, draft = self._system()
        self.addCleanup(temporary.cleanup)
        args = build_parser().parse_args(["google-service-enablement", "--authorization", str(draft)])
        with mock.patch.object(se, "_open_service_usage_request") as network:
            result = dispatch(args)
        self.assertEqual(result["authorization_status"], "draft")
        network.assert_not_called()


if __name__ == "__main__":
    unittest.main()
