"""Same single test through the already-authenticated HeyGen CLI subscription.

Shares the API helper's submission intent, job, and result files. Never log in,
refresh credentials explicitly, upload, purchase, repeat a POST, or repair media.
"""

import json
import os
import re
import subprocess
import sys
import uuid

import run_test as common

CLI = "/Users/brownmanbrain/.local/bin/heygen"
EXPECTED_USER = "637de3ad0fc24abe8ba97408d72dcc4f"


def cli(args, operation, body=None):
    common.require(not os.environ.get("HEYGEN_API_KEY"),
                   "Runtime API key would override the reviewed OAuth billing route")
    try:
        result = subprocess.run([CLI, *args], input=body, text=True, capture_output=True, timeout=60)
        common.require(result.returncode == 0, "CLI returned an error")
        data = json.loads(result.stdout)
        common.require(isinstance(data, dict), "CLI response is not an object")
        common.require(not data.get("error"), "CLI returned a provider error")
        return data
    except (subprocess.SubprocessError, OSError, ValueError) as error:
        common.save("ERROR-" + uuid.uuid4().hex + ".json", {
            "at": common.now(), "operation": operation, "exception_type": type(error).__name__,
            "instruction": "CLI outcome failed or is uncertain. Preserve shared intent and reconcile provider state; never rerun submit."})
        raise RuntimeError("CLI response failed or is uncertain; preserve intent and do not resubmit.") from None


def account():
    response = cli(["auth", "status"], "account")
    credential = response.get("credential", {})
    data = response.get("data", {})
    remaining = data.get("subscription", {}).get("credits", {}).get("premium_credits", {}).get("remaining")
    common.require(credential.get("type") == "oauth" and credential.get("source") == "file"
                   and data.get("billing_type") == "subscription" and data.get("username") == EXPECTED_USER,
                   "CLI account or billing route differs from the verified owner subscription")
    common.require(isinstance(remaining, (int, float)) and remaining >= 3,
                   "Fewer than three existing subscription credits remain; stop without buying")
    return {"at": common.now(), "username": EXPECTED_USER, "billing_type": "subscription",
            "credential_type": "oauth", "plan": data["subscription"].get("plan"),
            "remaining_subscription_credits": remaining, "estimated_credits_before_rounding": 7 * 16 / 60,
            "rate_basis": "Published Avatar IV Photo Look 16 credits per minute; actual provider charge requires readback",
            "api_cash_balance_used": False, "new_cash_purchase": False}


def main():
    common.require(len(sys.argv) == 2 and sys.argv[1] in ("preflight", "submit", "status", "result", "download"),
                   "Use preflight, submit, status, result, or download")
    mode = sys.argv[1]
    if mode == "download":
        common.main()
        return
    if mode in ("preflight", "submit"):
        if mode == "submit":
            common.require(not (common.BASE / "SUBMISSION-INTENT.json").exists()
                           and not (common.BASE / "JOB.json").exists(),
                           "A shared API or OAuth submission intent already exists. Do not resubmit.")
        request_raw, payload = common.validate_inputs()
        current = account()
        if mode == "preflight":
            print(json.dumps({"status": "validated_no_submission", **current}))
            return
        common.save("ACCOUNT-BEFORE.json", current)
        common.save("SUBMISSION-INTENT.json", {
            "at": common.now(), "request_sha256": common.sha(request_raw),
            "input_sha256": common.sha((common.BASE / "INPUT.json").read_bytes()),
            "route": "existing HeyGen CLI OAuth subscription", "username": EXPECTED_USER,
            "single_cli_submission": True, "helper_automatic_retry": False})
        response = cli(["video", "create", "--data", "-"], "submit", body=request_raw.decode())
        common.save("SUBMISSION-RESPONSE.json", response)
        data = response.get("data", {})
        video_id = data.get("video_id") or data.get("id")
        common.require(re.fullmatch(r"[A-Za-z0-9_-]{1,100}", video_id or ""),
                       "Provider omitted video id; reconcile receipt without resubmission")
        common.save("JOB.json", {"at": common.now(), "video_id": video_id})
        print(json.dumps({"status": "submitted", "video_id": video_id, "billing_type": "subscription"}))
    else:
        video_id = common.stored_job()
        response = cli(["video", "get", video_id], mode)
        common.save("STATUS-" + uuid.uuid4().hex + ".json", {"at": common.now(), "response": response})
        data = response.get("data", {})
        if mode == "result":
            common.require(data.get("status") == "completed" and data.get("video_url"),
                           "Video is not completed with a downloadable result")
            if not (common.BASE / "RESULT.json").exists():
                common.save("RESULT.json", response)
        print(json.dumps({"video_id": video_id, "status": data.get("status"),
                          "duration": data.get("duration"), "video_url": data.get("video_url")}))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        print(json.dumps({"status": "stopped", "reason": str(error)}))
        sys.exit(1)
