#!/usr/bin/env python3
"""Verify and transfer the replacement Short 02 guide once to Original C.

Reuses the pinned v5 transfer transport, cost and receipt logic, but supplies a
replacement-specific guide verifier and counts the v5 Short 03/04 costs. The
old failed Short 02 guide is never promoted. No automatic retry exists.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import wave
from pathlib import Path


sys.dont_write_bytecode = True
SELF = Path(__file__).resolve()
HERE = SELF.parent
REPO = next(p for p in SELF.parents if p.name == "operator-economy")
BASE = HERE / "short-02-operations-business"
V5_BASE = HERE.parent / "narration-v5"
V5_RUNNER = V5_BASE / "transfer_shorts_02_04.py"
OWNER = REPO / "blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/ep007-owner-approve-two-bounded-recovery-calls-20260923.json"
EXPECTED_OWNER_SHA = "8aa69611a23acdfa7c76b5a5fbb0f89c688ab29dcc40fc19d1a9d7bbb3c7a64e"
SHORT_ID = "short-02-operations-business"
SCRIPT = HERE.parent / "narration-v3" / SHORT_ID / "SCRIPT.txt"
CONFIG = HERE.parent / "narration-v3" / SHORT_ID / "TRANSFER-INPUT.json"
SELECTION = BASE / "GUIDE-TRANSFER-SELECTION.json"
GUIDE_ASR = BASE / "GUIDE-ASR.json"
REPAIR = BASE / "DERIVED-GUIDE-REPAIR.json"
RESOLUTION = BASE / "GUIDE-HOLD-RESOLUTION.json"
RECEIPT = BASE / "GOOGLE-RECEIPT.json"
INTENT = BASE / "GOOGLE-SUBMISSION-INTENT.json"
HOLD = BASE / "HOLD.json"
SOURCE_GUIDE = BASE / "media/guide.wav"
SELECTED_GUIDE = BASE / "media/guide-derived-pad500ms.wav"
TRANSCRIPT = BASE / "diagnostic-asr-derived-small/transcript.json"
SOURCE_SHA = "aa64af5193083c9a905aac0794b43be2a49d9248c7e31c87e5fab1ee674ed497"
SELECTED_SHA = "a634d73f36df812f3e206f8d11c5fb0323a95538e914601a323db77a06a22a14"
SCRIPT_SHA = "aee361d4542ed450365a50c70577f6b1bddd61c30de0571d770cbd91b0ed5542"

spec = importlib.util.spec_from_file_location("ep007_short02_v5_transfer_base", V5_RUNNER)
if spec is None or spec.loader is None:
    raise SystemExit("Pinned base transfer runner unavailable")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref_is(value: dict, path: Path) -> bool:
    return value == {"path": base.rel(path), "sha256": sha(path)}


def fail(message: str) -> None:
    raise SystemExit(message)


def verify_replacement_guide(short_id: str) -> dict:
    if short_id != SHORT_ID:
        fail("This runner only transfers Short 02")
    base.assert_global_pins()
    if sha(OWNER) != EXPECTED_OWNER_SHA or sha(SCRIPT) != SCRIPT_SHA:
        fail("Owner replacement approval or locked script changed")
    owner = json.loads(OWNER.read_text())
    if (owner.get("owner_verbatim") != "approved" or
            owner.get("authorized", {}).get("short02_replacement_google_guide_calls_max") != 1 or
            not owner.get("authorized", {}).get("continue_existing_private_review_pipeline")):
        fail("Replacement source does not authorize this continuation")
    required = (SELECTION, GUIDE_ASR, REPAIR, RESOLUTION, RECEIPT, INTENT, HOLD,
                SOURCE_GUIDE, SELECTED_GUIDE, TRANSCRIPT, CONFIG)
    if not all(p.is_file() for p in required):
        fail("Replacement guide evidence incomplete")
    if sha(SOURCE_GUIDE) != SOURCE_SHA or sha(SELECTED_GUIDE) != SELECTED_SHA:
        fail("Replacement source/selected guide changed")
    intent = json.loads(INTENT.read_text())
    receipt = json.loads(RECEIPT.read_text())
    if (intent.get("owner_source_sha256") != EXPECTED_OWNER_SHA or
            intent.get("provider_generation_attempt") != 2 or
            intent.get("new_calls_under_this_approval") != 1 or
            intent.get("automatic_retries") != 0 or
            receipt.get("http_status") != 200 or
            receipt.get("calls_under_this_approval") != 1 or
            receipt.get("retries") != 0 or
            receipt.get("guide_sha256") != SOURCE_SHA):
        fail("Replacement provider attempt/receipt changed")
    selection = json.loads(SELECTION.read_text())
    if (selection.get("status") != "pass_selected_for_original_c_preflight_only" or
            selection.get("short_id") != SHORT_ID or
            not ref_is(selection.get("replacement_owner_source") or {}, OWNER) or
            not ref_is(selection.get("source_guide") or {}, SOURCE_GUIDE) or
            not ref_is(selection.get("selected_guide") or {}, SELECTED_GUIDE) or
            not ref_is(selection.get("google_receipt") or {}, RECEIPT) or
            not ref_is(selection.get("guide_asr") or {}, GUIDE_ASR) or
            not ref_is(selection.get("derived_repair") or {}, REPAIR) or
            not ref_is(selection.get("hold_resolution") or {}, RESOLUTION)):
        fail("Immutable selected-guide record changed")
    resolution = json.loads(RESOLUTION.read_text())
    if (resolution.get("status") != "pass_resolved_with_preserved_evidence_for_transfer_preflight_only" or
            not ref_is(resolution.get("prior_hold") or {}, HOLD) or
            not ref_is(resolution.get("derived_repair") or {}, REPAIR) or
            not ref_is(resolution.get("guide_asr") or {}, GUIDE_ASR)):
        fail("Technical hold not explicitly resolved")
    prior_failed_qc = V5_BASE / SHORT_ID / "GUIDE-QC-V1.json"
    if (not ref_is(resolution.get("failed_old_guide_not_rehabilitated") or {}, prior_failed_qc) or
            json.loads(prior_failed_qc.read_text()).get("status") != "hold_exact_copy_failure_at_opening"):
        fail("Old failed guide was not preserved as a failure")
    repair = json.loads(REPAIR.read_text())
    if (repair.get("provider_call") is not False or
            repair.get("operation", {}).get("type") != "append_digital_silence_to_derived_copy" or
            repair.get("operation", {}).get("appended_frames") != 12000 or
            repair.get("derived", {}).get("appended_frames_all_zero") is not True or
            repair.get("source", {}).get("sha256") != SOURCE_SHA or
            repair.get("derived", {}).get("sha256") != SELECTED_SHA):
        fail("Lossless tail repair record changed")
    with wave.open(str(SOURCE_GUIDE), "rb") as original, wave.open(str(SELECTED_GUIDE), "rb") as derived:
        if original.getparams()[:3] != derived.getparams()[:3] or original.getparams()[:3] != (1, 2, 24000):
            fail("Guide PCM format changed")
        before = original.readframes(original.getnframes())
        after = derived.readframes(derived.getnframes())
        if derived.getnframes() - original.getnframes() != 12000 or after[:len(before)] != before or after[len(before):] != bytes(24000):
            fail("Derived guide is not an unchanged PCM prefix plus 500 ms zero tail")
    qc = json.loads(GUIDE_ASR.read_text())
    if (qc.get("status") != "pass_exact_normalized_locked_words_and_timing_within_derived_media" or
            qc.get("accepted_for_transfer_preflight") is not True or
            qc.get("media", {}).get("sha256") != SELECTED_SHA or
            qc.get("script", {}).get("sha256") != SCRIPT_SHA):
        fail("Exact-copy local guide QC not selected")
    expected = base.normalize_tokens(SCRIPT.read_text())
    for row in qc.get("transcripts", []):
        path = REPO / row.get("path", "")
        if not path.is_file() or row.get("sha256") != sha(path):
            fail("Guide ASR transcript changed")
        words = json.loads(path.read_text())
        actual = base.normalize_tokens(" ".join(str(w.get("text", "")) for w in words))
        if actual != expected:
            fail("Guide ASR differs from locked copy")
    words = json.loads(TRANSCRIPT.read_text())
    probe = base.cap.cal.probe(SELECTED_GUIDE)
    if (len(expected) != 104 or not probe.get("ends_in_silence") or
            not all(isinstance(w.get("start"), (float, int)) and isinstance(w.get("end"), (float, int)) and
                    0 <= w["start"] <= w["end"] <= probe["duration_seconds"] for w in words) or
            not all(words[i]["start"] >= words[i - 1]["start"] for i in range(1, len(words)))):
        fail("Guide exact-copy timing/tail check failed")
    return {"short_id": SHORT_ID, "selected": SELECTED_GUIDE, "selection": SELECTION,
            "qc": GUIDE_ASR, "script": SCRIPT, "config": CONFIG, "probe": probe}


def prior_usage(current_id: str) -> tuple[int, int]:
    if current_id != SHORT_ID:
        fail("Wrong short")
    if (BASE / "ELEVEN-SUBMISSION-INTENT.json").exists():
        fail("Short 02 transfer already attempted; no retry")
    if (V5_BASE / SHORT_ID / "ELEVEN-SUBMISSION-INTENT.json").exists():
        fail("Old failed guide was transferred; stop")
    cost = 0
    for short in ("short-03-how-you-charge", "short-04-test-the-front-door"):
        prior = V5_BASE / short
        if not (prior / "ELEVEN-SUBMISSION-INTENT.json").is_file():
            fail(f"Prior {short} transfer intent missing")
        receipt = json.loads((prior / "ELEVEN-RECEIPT.json").read_text())
        if receipt.get("http_status") != 200 or receipt.get("actual_credit_cost_verified") is not True:
            fail(f"Prior {short} actual credits unverified")
        cost += int(receipt["actual_credit_cost"])
    if cost != 1015:
        fail("Prior 03/04 cost changed; inspect before transfer")
    return 2, cost


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("check", "preflight", "transfer"))
    args = parser.parse_args()
    base.HERE = HERE
    base.RUNNER = SELF
    base.work = lambda short_id: BASE if short_id == SHORT_ID else fail("Wrong short")
    base.verify_guide = verify_replacement_guide
    base.prior_usage = prior_usage
    if args.command == "check":
        data = base.check(SHORT_ID)
        print(json.dumps({"status": "pass", "short_id": SHORT_ID,
                          "selected_guide_sha256": sha(data["selected"]),
                          "forecast_credits": data["forecast_credits"],
                          "prior_actual_credits": data["prior_credits"],
                          "provider_calls_made": 0}))
    elif args.command == "preflight":
        base.preflight(SHORT_ID)
    else:
        base.transfer(SHORT_ID)


if __name__ == "__main__":
    main()
