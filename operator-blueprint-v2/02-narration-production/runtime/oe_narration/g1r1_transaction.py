"""One-shot G1R1 recovery transaction with mandatory temporary-IAM cleanup.

This is intentionally specific to the committed G1R1 authorization.  It does
not grant IAM access.  It proves the already-present, hash-bound direct role,
invokes the existing synthetic-guide executor exactly once, and removes that
exact role in a ``finally`` path before returning.

Raw IAM members, IAM policies, etags, ADC material, and access tokens remain in
process memory only.  The durable transaction receipt contains hashes and
bounded counts only.
"""

from __future__ import annotations

import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any
import urllib.error
import urllib.parse
import urllib.request

from .performance_transfer import (
    ValidationError,
    _exclusive_fixture_write,
    _load_google_access_token,
    _open_parent_descriptor,
    _preflight_google_adc,
    _scan_for_secrets,
    _verify_private_fixture_artifact,
    validate_synthetic_guide_authorization,
)


AUTHORIZATION_ID = "AUTH-G1R1-ai-visibility-v1.1-p01-synthetic-guide-20260826T003835Z"
ROLE = "roles/aiplatform.user"
PROJECT_SHA256 = "68a5cdeb9918bf84d3f59c3f428e8e12a40b33f1ab0d0eaee19276be6761c0f2"
MEMBER_SHA256 = "405db2f71219f52e2f9a0a7763cad8b3c0591ccf9274a8757ff3ea1a1f61c31f"
AUTHORIZATION_SHA256 = "4dca079b5022d184d080b401225fd819d988851ef40f08d80e3df62ae9825310"
IAM_AUTHORITY_SHA256 = "c2468d049eebd7098df66eb685a9a6f43a0754c6631bd0dcccfd59ffe2eb9809"
OWNER_RECOVERY_SHA256 = "e7547e62f2227ea3deec70fa7ba136c5738dff52e3823cf03f9e1b3dd89541be"
PLAN_SHA256 = "f73f42e1221753d394ba5de31550094a9aa98e950987e415cb4b0f0c85365f53"
REQUEST_SET_SHA256 = "ed1aa73a04db602b8ed2611731346e3f0bfae9d48d55a4f94bb5110da85c0cba"

PRODUCTION_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = PRODUCTION_ROOT.parents[1]
FIXTURE = (
    PRODUCTION_ROOT
    / "fixtures"
    / "step2-v0.5-ai-visibility-v1.1-synthetic-guide-to-saved-c-transfer-microtest"
)
AUTHORIZATION = FIXTURE / "authorizations" / "03-google-synthetic-guide-recovery.ACTIVE.20260826T003835Z.json"
IAM_AUTHORITY = FIXTURE / "evidence" / "G1R1-TEMPORARY-IAM-AUTHORITY-AND-STATE.20260826T003835Z.md"
OWNER_RECOVERY = FIXTURE / "evidence" / "G1R1-OWNER-RECOVERY-AUTHORIZATION.20260826T003835Z.md"
PLAN = FIXTURE / "performance-transfer-plan.json"
CANONICAL_W = PRODUCTION_ROOT / "fixtures" / "step2-v0.2-ai-visibility-v1.1" / "identity" / "canonical-w.txt"
CONSUMPTION = FIXTURE / "authorizations" / "consumed" / f"{AUTHORIZATION_ID}.consumed.json"
RUN_RECEIPT = FIXTURE / "receipts" / "google" / f"{AUTHORIZATION_ID}.run.json"
FAILURE_RECEIPT = FIXTURE / "receipts" / "google" / f"{AUTHORIZATION_ID}.failure.json"
TRANSACTION_RECEIPT = FIXTURE / "evidence" / "G1R1-IAM-AND-GUIDE-TRANSACTION.20260826T003835Z.json"
TRANSACTION_RECEIPT_RELATIVE = "evidence/G1R1-IAM-AND-GUIDE-TRANSACTION.20260826T003835Z.json"
OUTPUTS = (
    FIXTURE / "outputs" / "raw" / "google" / "P01-W0030-W0110" / "candidate-A.wav",
    FIXTURE / "outputs" / "raw" / "google" / "P01-W0030-W0110" / "candidate-B.wav",
)

MAX_IAM_RESPONSE_BYTES = 10_000_000
MAX_G1_STDIO_BYTES = 1_000_000
MAX_IAM_GET_ATTEMPTS = 6
MAX_IAM_SET_ATTEMPTS = 2


class TransactionError(RuntimeError):
    """Sanitized transaction failure."""

    def __init__(self, code: str, *, http_status: int | None = None):
        super().__init__(code)
        self.code = code
        self.http_status = http_status


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha_text(value: str) -> str:
    return _sha_bytes(value.encode("utf-8"))


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha_file(path: Path) -> str:
    return _sha_bytes(path.read_bytes())


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _strict_json(raw: bytes, label: str) -> Any:
    if not raw or len(raw) > MAX_IAM_RESPONSE_BYTES:
        raise TransactionError(f"{label}_malformed")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise TransactionError(f"{label}_duplicate_key")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=reject_duplicates)
    except TransactionError:
        raise
    except Exception:
        raise TransactionError(f"{label}_malformed") from None


def _require_regular_no_symlink(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current / part
        try:
            info = current.lstat()
        except OSError:
            raise TransactionError("bound_path_missing_or_unsafe") from None
        if stat.S_ISLNK(info.st_mode):
            raise TransactionError("bound_path_missing_or_unsafe")
    if not stat.S_ISREG(absolute.stat().st_mode):
        raise TransactionError("bound_path_missing_or_unsafe")


def _require_absent_no_symlink(path: Path) -> None:
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:-1]:
        current = current / part
        if not current.exists():
            continue
        try:
            info = current.lstat()
        except OSError:
            raise TransactionError("destination_parent_unsafe") from None
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise TransactionError("destination_parent_unsafe")
    if os.path.lexists(absolute):
        raise TransactionError("destination_already_exists")


def _git_output(*args: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=False,
            timeout=15,
        )
    except Exception:
        raise TransactionError("git_preflight_failed") from None
    if result.returncode != 0 or len(result.stdout) > 1_000_000 or len(result.stderr) > 1_000_000:
        raise TransactionError("git_preflight_failed")
    return result.stdout


def _preflight_local_state() -> dict[str, Any]:
    expected = {
        AUTHORIZATION: AUTHORIZATION_SHA256,
        IAM_AUTHORITY: IAM_AUTHORITY_SHA256,
        OWNER_RECOVERY: OWNER_RECOVERY_SHA256,
        PLAN: PLAN_SHA256,
    }
    for path, digest in expected.items():
        _require_regular_no_symlink(path)
        if _sha_file(path) != digest:
            raise TransactionError("committed_binding_hash_mismatch")
    status = _git_output("status", "--porcelain=v1", "--untracked-files=all")
    if status:
        raise TransactionError("worktree_not_clean")
    head = _git_output("rev-parse", "HEAD").strip()
    upstream = _git_output("rev-parse", "@{u}").strip()
    if not head or head != upstream:
        raise TransactionError("commit_not_pushed_or_not_bound")
    source_path = Path(__file__).resolve()
    try:
        source_relative = source_path.relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        raise TransactionError("transaction_source_outside_repository") from None
    committed_source = _git_output("show", f"HEAD:{source_relative}")
    source_bytes = source_path.read_bytes()
    if not committed_source or committed_source != source_bytes:
        raise TransactionError("transaction_source_not_committed_exactly")
    for path in (CONSUMPTION, RUN_RECEIPT, FAILURE_RECEIPT, TRANSACTION_RECEIPT, *OUTPUTS):
        _require_absent_no_symlink(path)
    try:
        dry = validate_synthetic_guide_authorization(AUTHORIZATION, PLAN, CANONICAL_W)
    except ValidationError:
        raise TransactionError("g1r1_offline_validation_failed") from None
    if (
        dry.get("valid") is not True
        or dry.get("authorization_id") != AUTHORIZATION_ID
        or dry.get("authorization_sha256") != AUTHORIZATION_SHA256
        or dry.get("plan_sha256") != PLAN_SHA256
        or dry.get("request_set_sha256") != REQUEST_SET_SHA256
        or dry.get("provider_action_authorized") is not True
        or dry.get("network_authorized") is not True
        or dry.get("execution_transport_available") is not True
        or dry.get("credentials_accessed") is not False
        or dry.get("network_called") is not False
        or dry.get("audio_files_created") != 0
    ):
        raise TransactionError("g1r1_offline_validation_failed")
    project = os.environ.get("GOOGLE_CLOUD_QUOTA_PROJECT")
    if not isinstance(project, str) or not project or project != project.strip() or _sha_text(project) != PROJECT_SHA256:
        raise TransactionError("quota_project_binding_mismatch")
    return {
        "project": project,
        "head": head.decode("ascii", errors="strict"),
        "executor_source_sha256": _sha_bytes(source_bytes),
    }


def _read_capped(response: Any) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(65_536, MAX_IAM_RESPONSE_BYTES + 1 - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > MAX_IAM_RESPONSE_BYTES:
            raise TransactionError("iam_response_too_large")
    return b"".join(chunks)


def _iam_post(project: str, action: str, body: dict[str, Any], token: str) -> dict[str, Any]:
    encoded_project = urllib.parse.quote(project, safe="")
    url = f"https://cloudresourcemanager.googleapis.com/v1/projects/{encoded_project}:{action}"
    request = urllib.request.Request(
        url,
        data=_canonical_bytes(body),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
            "X-Goog-User-Project": project,
        },
    )
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        with opener.open(request, timeout=30) as response:
            if response.status != 200:
                raise TransactionError("iam_http_failure", http_status=int(response.status))
            raw = _read_capped(response)
    except urllib.error.HTTPError as exc:
        try:
            exc.read(MAX_IAM_RESPONSE_BYTES + 1)
        except Exception:
            pass
        raise TransactionError("iam_http_failure", http_status=int(exc.code)) from None
    except TransactionError:
        raise
    except Exception:
        raise TransactionError("iam_transport_failure") from None
    value = _strict_json(raw, "iam_response")
    if not isinstance(value, dict):
        raise TransactionError("iam_response_malformed")
    return value


def _get_policy(project: str, token: str) -> dict[str, Any]:
    policy = _iam_post(project, "getIamPolicy", {"options": {"requestedPolicyVersion": 3}}, token)
    if type(policy.get("version", 1)) is not int or policy.get("version", 1) not in {1, 3}:
        raise TransactionError("iam_policy_version_invalid")
    if not isinstance(policy.get("etag"), str) or not policy["etag"]:
        raise TransactionError("iam_policy_etag_missing")
    bindings = policy.get("bindings")
    if not isinstance(bindings, list):
        raise TransactionError("iam_policy_bindings_invalid")
    for binding in bindings:
        if not isinstance(binding, dict) or not isinstance(binding.get("role"), str):
            raise TransactionError("iam_policy_binding_invalid")
        members = binding.get("members")
        if not isinstance(members, list) or any(not isinstance(member, str) for member in members):
            raise TransactionError("iam_policy_members_invalid")
    return policy


def _member_from_hash(policy: dict[str, Any]) -> str:
    matches = {
        member
        for binding in policy["bindings"]
        for member in binding["members"]
        if _sha_text(member) == MEMBER_SHA256
    }
    if len(matches) != 1:
        raise TransactionError("hash_bound_member_not_unique")
    return next(iter(matches))


def _role_matches(policy: dict[str, Any], member: str) -> tuple[list[int], list[int], int, int]:
    unconditional: list[int] = []
    conditioned: list[int] = []
    unconditional_entries = 0
    conditioned_entries = 0
    for index, binding in enumerate(policy["bindings"]):
        if binding.get("role") != ROLE:
            continue
        occurrences = sum(candidate == member for candidate in binding["members"])
        if not occurrences:
            continue
        if "condition" in binding:
            conditioned.append(index)
            conditioned_entries += occurrences
        else:
            unconditional.append(index)
            unconditional_entries += occurrences
    return unconditional, conditioned, unconditional_entries, conditioned_entries


def _policy_without_etag(policy: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(policy)
    value.pop("etag", None)
    return value


def _safe_policy_summary(policy: dict[str, Any], member: str) -> dict[str, Any]:
    unconditional, conditioned, unconditional_entries, conditioned_entries = _role_matches(policy, member)
    return {
        "policy_sha256": _sha_bytes(_canonical_bytes(policy)),
        "etag_sha256": _sha_text(policy["etag"]),
        "version": policy.get("version", 1),
        "binding_count": len(policy["bindings"]),
        "member_entry_count": sum(len(binding["members"]) for binding in policy["bindings"]),
        "target_unconditional_binding_count": len(unconditional),
        "target_conditioned_binding_count": len(conditioned),
        "target_unconditional_member_entry_count": unconditional_entries,
        "target_conditioned_member_entry_count": conditioned_entries,
    }


def _remove_exact_role(policy: dict[str, Any], member: str) -> tuple[dict[str, Any], bool]:
    unconditional, conditioned, unconditional_entries, conditioned_entries = _role_matches(policy, member)
    if conditioned or conditioned_entries or len(unconditional) > 1 or unconditional_entries > 1:
        raise TransactionError("temporary_role_shape_ambiguous")
    if not unconditional and unconditional_entries == 0:
        return copy.deepcopy(policy), False
    if len(unconditional) != 1 or unconditional_entries != 1:
        raise TransactionError("temporary_role_shape_ambiguous")
    changed = copy.deepcopy(policy)
    index = unconditional[0]
    binding = changed["bindings"][index]
    binding["members"] = [candidate for candidate in binding["members"] if candidate != member]
    if not binding["members"]:
        changed["bindings"].pop(index)
    return changed, True


def _set_policy(project: str, policy: dict[str, Any], token: str) -> dict[str, Any]:
    return _iam_post(
        project,
        "setIamPolicy",
        {"policy": policy, "updateMask": "bindings,etag"},
        token,
    )


def _g1_environment(project: str) -> dict[str, str]:
    allowed = ("PATH", "HOME", "CLOUDSDK_CONFIG", "LANG", "LC_ALL", "LC_CTYPE")
    result = {key: value for key in allowed if isinstance((value := os.environ.get(key)), str) and value}
    result["CLOUDSDK_CORE_DISABLE_PROMPTS"] = "1"
    result["GOOGLE_CLOUD_QUOTA_PROJECT"] = project
    result["PYTHONDONTWRITEBYTECODE"] = "1"
    result["PYTHONPATH"] = str(PRODUCTION_ROOT / "runtime")
    return result


def _invoke_g1_once(project: str) -> dict[str, Any]:
    command = [
        sys.executable,
        "-m",
        "oe_narration.cli",
        "synthetic-guide",
        "--plan",
        str(PLAN),
        "--canonical-w",
        str(CANONICAL_W),
        "--authorization",
        str(AUTHORIZATION),
        "--execute",
        "--timeout",
        "60",
    ]
    try:
        result = subprocess.run(
            command,
            cwd=PRODUCTION_ROOT / "runtime",
            env=_g1_environment(project),
            check=False,
            capture_output=True,
            text=False,
            timeout=150,
        )
    except subprocess.TimeoutExpired:
        return {"invoked": True, "exit_code": None, "outcome": "indeterminate_host_timeout"}
    except Exception:
        return {"invoked": True, "exit_code": None, "outcome": "local_invocation_failure"}
    if len(result.stdout) > MAX_G1_STDIO_BYTES or len(result.stderr) > MAX_G1_STDIO_BYTES:
        return {"invoked": True, "exit_code": result.returncode, "outcome": "stdio_cap_exceeded"}
    return {
        "invoked": True,
        "exit_code": result.returncode,
        "outcome": "executor_returned_success" if result.returncode == 0 else "executor_returned_failure",
    }


def _artifact_summary(path: Path) -> dict[str, Any]:
    try:
        relative = path.absolute().relative_to(FIXTURE).as_posix()
        parent_fd, name = _open_parent_descriptor(FIXTURE, relative, create_parents=False)
    except (ValueError, ValidationError):
        raise TransactionError("post_run_artifact_path_unsafe") from None
    descriptor: int | None = None
    try:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        try:
            descriptor = os.open(name, flags, dir_fd=parent_fd)
        except FileNotFoundError:
            return {"exists": False}
        before = os.fstat(descriptor)
        mode = stat.S_IMODE(before.st_mode)
        if not stat.S_ISREG(before.st_mode) or mode != 0o600 or before.st_size > 10_000_000:
            raise TransactionError("post_run_artifact_not_private_or_bounded")
        chunks: list[bytes] = []
        received = 0
        while True:
            chunk = os.read(descriptor, min(65_536, 10_000_001 - received))
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            if received > 10_000_000:
                raise TransactionError("post_run_artifact_not_private_or_bounded")
        after = os.fstat(descriptor)
        if (
            received != before.st_size
            or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        ):
            raise TransactionError("post_run_artifact_changed_during_read")
        data = b"".join(chunks)
        return {"exists": True, "sha256": _sha_bytes(data), "bytes": received, "mode": mode}
    except TransactionError:
        raise
    except OSError:
        raise TransactionError("post_run_artifact_path_unsafe") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_fd)


def _collect_and_validate_artifacts(g1: dict[str, Any]) -> tuple[dict[str, Any], str | None, bool]:
    artifacts = {
        "consumption": _artifact_summary(CONSUMPTION),
        "run_receipt": _artifact_summary(RUN_RECEIPT),
        "failure_receipt": _artifact_summary(FAILURE_RECEIPT),
        "candidate_a": _artifact_summary(OUTPUTS[0]),
        "candidate_b": _artifact_summary(OUTPUTS[1]),
    }
    if g1.get("invoked") is not True:
        if any(value.get("exists") is True for value in artifacts.values()):
            return artifacts, "unexpected_artifact_without_g1_invocation", False
        return artifacts, None, False
    if artifacts["consumption"].get("exists") is not True:
        return artifacts, "invoked_g1_missing_consumption_record", False
    receipt_count = sum(
        artifacts[key].get("exists") is True for key in ("run_receipt", "failure_receipt")
    )
    if receipt_count != 1:
        return artifacts, "invoked_g1_receipt_cardinality_invalid", False
    run_exists = artifacts["run_receipt"].get("exists") is True
    failure_exists = artifacts["failure_receipt"].get("exists") is True
    candidate_a = artifacts["candidate_a"].get("exists") is True
    candidate_b = artifacts["candidate_b"].get("exists") is True
    if run_exists:
        if not candidate_a or not candidate_b:
            return artifacts, "successful_g1_receipt_missing_outputs", False
        if g1.get("exit_code") != 0 or g1.get("outcome") != "executor_returned_success":
            return artifacts, "successful_g1_receipt_child_status_mismatch", False
        return artifacts, None, True
    if failure_exists:
        if candidate_b and not candidate_a:
            return artifacts, "failed_g1_output_order_invalid", False
        if g1.get("exit_code") == 0 or g1.get("outcome") == "executor_returned_success":
            return artifacts, "failed_g1_receipt_child_status_mismatch", False
        return artifacts, None, False
    return artifacts, "invoked_g1_outcome_unknown", False


def _write_private_receipt(receipt: dict[str, Any]) -> str:
    if _scan_for_secrets(receipt, "g1r1_transaction_receipt"):
        raise TransactionError("transaction_receipt_secret_scan_failed")
    data = json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"
    try:
        _exclusive_fixture_write(FIXTURE, TRANSACTION_RECEIPT_RELATIVE, data)
        _verify_private_fixture_artifact(
            FIXTURE,
            TRANSACTION_RECEIPT_RELATIVE,
            data,
            "G1R1 transaction receipt",
        )
    except ValidationError:
        raise TransactionError("transaction_receipt_write_failed") from None
    return _sha_bytes(data)


def execute() -> dict[str, Any]:
    started_at = _iso_now()
    preflight = _preflight_local_state()
    project = preflight.pop("project")
    gcloud = ""
    token = ""
    iam_get_calls = 0
    iam_set_calls = 0
    cleanup_retry_count = 0
    g1 = {"invoked": False, "exit_code": None, "outcome": "blocked_before_invocation"}
    grant_readback: dict[str, Any] | None = None
    pre_revoke: dict[str, Any] | None = None
    final_readback: dict[str, Any] | None = None
    cleanup_verified = False
    security_block = False
    transaction_error: str | None = None
    member = ""
    grant_readback_at: str | None = None
    g1_completed_at: str | None = None
    pre_revoke_at: str | None = None
    cleanup_completed_at: str | None = None

    def counted_get_policy() -> dict[str, Any]:
        nonlocal iam_get_calls
        if iam_get_calls >= MAX_IAM_GET_ATTEMPTS:
            raise TransactionError("iam_get_attempt_cap_exhausted")
        iam_get_calls += 1
        return _get_policy(project, token)

    def counted_set_policy(policy: dict[str, Any]) -> dict[str, Any]:
        nonlocal iam_set_calls
        if iam_set_calls >= MAX_IAM_SET_ATTEMPTS:
            raise TransactionError("iam_set_attempt_cap_exhausted")
        iam_set_calls += 1
        return _set_policy(project, policy, token)

    try:
        gcloud = _preflight_google_adc()
        token = _load_google_access_token(gcloud, 30.0)
        policy = counted_get_policy()
        member = _member_from_hash(policy)
        unconditional, conditioned, unconditional_entries, conditioned_entries = _role_matches(policy, member)
        grant_readback = _safe_policy_summary(policy, member)
        if (
            conditioned
            or conditioned_entries
            or len(unconditional) != 1
            or unconditional_entries != 1
        ):
            raise TransactionError("temporary_role_readback_failed")
        grant_readback_at = _iso_now()
        g1 = _invoke_g1_once(project)
        g1_completed_at = _iso_now()
    except TransactionError as exc:
        transaction_error = exc.code
    except ValidationError:
        transaction_error = "credential_preflight_or_refresh_failed"
    except Exception:
        transaction_error = "unexpected_sanitized_transaction_failure"
    finally:
        # Cleanup uses a fresh policy snapshot and the same in-memory, hash-bound
        # member.  A single etag-conflict retry is the only cleanup retry.
        try:
            if not token:
                raise TransactionError("temporary_role_cleanup_token_unavailable")
            if not member:
                policy = counted_get_policy()
                member = _member_from_hash(policy)
            attempts = 0
            while True:
                current = counted_get_policy()
                if _sha_text(member) != MEMBER_SHA256:
                    raise TransactionError("temporary_member_hash_drift")
                pre_revoke = _safe_policy_summary(current, member)
                pre_revoke_at = _iso_now()
                changed, role_present = _remove_exact_role(current, member)
                expected_without_etag = _sha_bytes(_canonical_bytes(_policy_without_etag(changed)))
                if role_present:
                    try:
                        counted_set_policy(changed)
                    except TransactionError as exc:
                        if exc.http_status in {409, 412} and attempts == 0:
                            attempts += 1
                            cleanup_retry_count = 1
                            continue
                        raise
                final_policy = counted_get_policy()
                final_readback = _safe_policy_summary(final_policy, member)
                unconditional, conditioned, unconditional_entries, conditioned_entries = _role_matches(final_policy, member)
                final_without_etag = _sha_bytes(_canonical_bytes(_policy_without_etag(final_policy)))
                cleanup_verified = (
                    not unconditional
                    and not conditioned
                    and unconditional_entries == 0
                    and conditioned_entries == 0
                    and final_without_etag == expected_without_etag
                )
                if not cleanup_verified:
                    raise TransactionError("temporary_role_cleanup_not_proven")
                cleanup_completed_at = _iso_now()
                break
        except Exception as exc:
            cleanup_verified = False
            security_block = True
            if transaction_error is None:
                transaction_error = exc.code if isinstance(exc, TransactionError) else "temporary_role_cleanup_failed"

    token = ""
    member = ""
    artifact_coherence_error: str | None = None
    g1_succeeded = False
    try:
        artifacts, artifact_coherence_error, g1_succeeded = _collect_and_validate_artifacts(g1)
    except TransactionError as exc:
        artifacts = {"inspection_failed": True}
        artifact_coherence_error = exc.code
    if artifact_coherence_error is not None and transaction_error is None:
        transaction_error = artifact_coherence_error
    g1_failed_closed = (
        g1.get("invoked") is True
        and artifact_coherence_error is None
        and artifacts.get("failure_receipt", {}).get("exists") is True
        and not g1_succeeded
    )
    completed_at = _iso_now()
    receipt = {
        "schema_version": "oe-g1r1-iam-and-guide-transaction-v1",
        "transaction_id": "G1R1-IAM-AND-GUIDE-20260826T003835Z",
        "authorization_id": AUTHORIZATION_ID,
        "authorization_sha256": AUTHORIZATION_SHA256,
        "iam_authority_sha256": IAM_AUTHORITY_SHA256,
        "owner_recovery_sha256": OWNER_RECOVERY_SHA256,
        "project_sha256": PROJECT_SHA256,
        "member_sha256": MEMBER_SHA256,
        "role": ROLE,
        "grant_preceded_authority_record": True,
        "process_deviation_disclosed": True,
        "git_head": preflight["head"],
        "executor_source_sha256": preflight["executor_source_sha256"],
        "started_at": started_at,
        "grant_readback_at": grant_readback_at,
        "g1_completed_at": g1_completed_at,
        "pre_revoke_at": pre_revoke_at,
        "cleanup_completed_at": cleanup_completed_at,
        "completed_at": completed_at,
        "iam_calls": {
            "get_policy": iam_get_calls,
            "set_policy": iam_set_calls,
            "max_get_policy": MAX_IAM_GET_ATTEMPTS,
            "max_set_policy": MAX_IAM_SET_ATTEMPTS,
            "cleanup_retry_count": cleanup_retry_count,
            "grant_write_in_this_executor": 0,
        },
        "grant_readback": grant_readback,
        "g1_execution": g1,
        "pre_revoke": pre_revoke,
        "final_readback": final_readback,
        "cleanup_verified": cleanup_verified,
        "security_block_role_still_possible": security_block,
        "transaction_error": transaction_error,
        "artifact_coherence_error": artifact_coherence_error,
        "artifacts": artifacts,
        "transaction_closed": cleanup_verified,
        "g1_succeeded": g1_succeeded,
        "g1_failed_closed": g1_failed_closed,
        "retry_authorized": False,
        "voice_transfer_authorized": False,
        "full_capture_authorized": False,
        "step3_authorized": False,
        "sharing_authorized": False,
        "publication_authorized": False,
    }
    receipt_sha = _write_private_receipt(receipt)
    result = {
        "schema_version": "oe-g1r1-transaction-result-v1",
        "authorization_id": AUTHORIZATION_ID,
        "g1_outcome": g1["outcome"],
        "transaction_closed": cleanup_verified,
        "g1_succeeded": g1_succeeded,
        "g1_failed_closed": g1_failed_closed,
        "cleanup_verified": cleanup_verified,
        "security_block_role_still_possible": security_block,
        "transaction_receipt": str(TRANSACTION_RECEIPT.relative_to(FIXTURE)),
        "transaction_receipt_sha256": receipt_sha,
    }
    if not cleanup_verified:
        raise TransactionError("SECURITY_BLOCK_ROLE_STILL_POSSIBLE")
    if g1.get("invoked") is not True:
        raise TransactionError("G1R1_TRANSACTION_FAILED_BEFORE_INVOCATION")
    if artifact_coherence_error is not None:
        raise TransactionError("G1R1_ARTIFACT_COHERENCE_FAILED")
    return result


def main() -> int:
    try:
        result = execute()
    except TransactionError as exc:
        print(json.dumps({"valid": False, "error": exc.code}, sort_keys=True))
        return 3
    except Exception:
        print(json.dumps({"valid": False, "error": "unexpected_sanitized_failure"}, sort_keys=True))
        return 3
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
