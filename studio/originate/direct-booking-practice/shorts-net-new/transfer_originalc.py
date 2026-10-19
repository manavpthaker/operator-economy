#!/usr/bin/env python3
"""EP009 stage 2: ElevenLabs Voice Changer transfer of each accepted guide onto Original C.

The four accepted guides live in three frozen run directories, two of them as
append-silence derivatives, so this stage selects its sources explicitly by hash
rather than by convention. Everything is written into narration-v4; narration-v1,
v2 and v3 are read only.

Governance mirrors EP007: a written intent before every provider call and an
immutable receipt after, zero automatic retries, an aggregate credit cap, a live
balance re-read before each call, and every source required to pass both the
tail gate and an exact-copy check before any transfer is submitted.

The Voice Changer stage is seeded, so a retry returns identical audio
(finding N4B-3). There is nothing to gain from one and it is not authorized.

Stages: sources | gate <id> | preflight | transfer <id> | summary
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import math
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

BASE = Path(__file__).resolve().parent
REPO = next(p for p in (BASE, *BASE.parents) if p.name == "operator-economy")
WORK = BASE / "narration-v4"
SPOKEN = BASE / "SPOKEN-TEXT-V1.json"
AUTH = (REPO / "blueprint-cinema/episodes/EP009-direct-booking-recovery/review/source-records"
        / "2026-10-08-owner-repair-02-and-transfer.json")
MANIFEST = WORK / "TRANSFER-MANIFEST.json"
PREFLIGHT = WORK / "TRANSFER-BATCH-PREFLIGHT.json"
CAL_PATH = REPO / "operator-blueprint-v2/02-narration-production/tools/calibrate.py"

_spec = importlib.util.spec_from_file_location("oe_calibrate", CAL_PATH)
cal = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cal)

_cn = importlib.util.spec_from_file_location("oe_capture", BASE / "capture_narration.py")
cn = importlib.util.module_from_spec(_cn)
_cn.loader.exec_module(cn)

CREDITS_PER_MINUTE = 1000
ASR_TOOL, ASR_ENGINE = "hyperframes@0.8.59", "whisper"
ENDPOINT = "https://api.elevenlabs.io/v1/speech-to-speech/scMbPZwQjr40V1MzL3Nj"

# Each accepted guide, named by the run that produced it and whether the transfer
# source is the raw guide or its append-silence derivative.
SOURCES = {
    "01": ("narration-v1/01-book-your-own-room", "media/guide.wav", "native tail pass 0.0002"),
    "02": ("narration-v4/02-sounds-like-marketing", "media/guide-derived-pad500ms.wav",
           "append-silence repair of narration-v2, source tail 0.0224"),
    "03": ("narration-v3/03-the-guest-book", "media/guide-derived-pad500ms.wav",
           "append-silence repair of narration-v3, source tail 0.1626"),
    "04": ("narration-v1/04-four-numbers", "media/guide.wav", "native tail pass 0.0116"),
}
ORDER = ["01", "02", "03", "04"]


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha_bytes(p.read_bytes())


def rel(p: Path) -> str:
    return str(p.relative_to(REPO))


def save_x(p: Path, data: bytes) -> None:
    if p.exists():
        raise SystemExit(f"refusing to overwrite immutable evidence {rel(p)}")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def save_json_x(p: Path, obj: Any) -> None:
    save_x(p, (json.dumps(obj, indent=1) + "\n").encode())


def auth() -> dict:
    if not AUTH.exists():
        raise SystemExit(f"no owner authorization at {rel(AUTH)}; nothing submitted")
    a = json.loads(AUTH.read_text())
    t = (a.get("authorized") or {}).get("elevenlabs_transfers")
    if not t or int(t.get("calls", 0)) != 4 or int(t.get("automatic_retries", 1)) != 0:
        raise SystemExit("the owner record does not authorize four no-retry transfers")
    return a


def cap() -> int:
    return int(auth()["authorized"]["elevenlabs_transfers"]["credit_cap"])


def spoken(short_id: str) -> dict:
    for s in json.loads(SPOKEN.read_text())["scripts"]:
        if s["id"] == short_id:
            return s
    raise SystemExit(f"unknown short {short_id}")


def wdir(short_id: str) -> Path:
    return WORK / Path(SOURCES[short_id][0]).name


def source_path(short_id: str) -> Path:
    run, media, _ = SOURCES[short_id]
    return BASE / run / media


def count(name: str) -> int:
    return sum(1 for s in ORDER if (wdir(s) / name).exists())


def assert_batch_clear() -> None:
    for s in ORDER:
        d = wdir(s)
        if ((d / "ELEVEN-SUBMISSION-INTENT.json").exists()
                and not (d / "ELEVEN-RECEIPT.json").exists()
                and not (d / "ELEVEN-ERROR.json").exists()):
            raise SystemExit(f"batch stopped by unresolved intent in {rel(d)}")


def key() -> str:
    return cal.read_dotenv_key("ELEVENLABS_API_KEY")


def balance() -> tuple[int, dict]:
    r = urllib.request.Request("https://api.elevenlabs.io/v1/user/subscription",
                               headers={"xi-api-key": key()})
    with urllib.request.urlopen(r, timeout=60) as resp:
        sub, hdrs = json.loads(resp.read()), dict(resp.headers)
    return int(sub["character_limit"]) - int(sub["character_count"]), {
        "tier": sub.get("tier"), "character_count": sub.get("character_count"),
        "character_limit": sub.get("character_limit"),
        "next_reset_unix": sub.get("next_character_count_reset_unix"),
        "response_headers": hdrs}


def est_credits(p: Path) -> int:
    return math.ceil(float(cal.probe(p)["duration_seconds"]) * CREDITS_PER_MINUTE / 60)


# ---------------------------------------------------------------- sources

def sources() -> None:
    a = auth()
    rows = []
    for s in ORDER:
        p = source_path(s)
        if not p.exists():
            raise SystemExit(f"missing transfer source for {s}: {rel(p)}")
        pr = cal.probe(p)
        if not pr.get("ends_in_silence"):
            raise SystemExit(f"source for {s} does not end in silence; it is not transfer-eligible")
        rows.append({"short_id": s, "slug": wdir(s).name,
                     "source_path": rel(p), "source_sha256": sha_file(p),
                     "basis": SOURCES[s][2],
                     "duration_seconds": pr["duration_seconds"],
                     "tail_energy": pr.get("tail_energy"),
                     "ends_in_silence": True,
                     "estimated_credits": est_credits(p)})
    total = sum(r["estimated_credits"] for r in rows)
    if total > cap():
        raise SystemExit(f"sources forecast {total} credits, above the {cap()} cap")
    save_json_x(MANIFEST, {
        "at_utc": now(), "stage": "elevenlabs_voice_transfer",
        "owner_authority": {"path": rel(AUTH), "sha256": sha_file(AUTH),
                            "verbatim": a.get("verbatim")},
        "target_voice": "Original C", "target_voice_id": "scMbPZwQjr40V1MzL3Nj",
        "model_id": "eleven_multilingual_sts_v2", "seed": "2026082501",
        "output_format": "pcm_48000",
        "credit_cap": cap(), "estimated_credits_total": total,
        "automatic_retries": 0, "order": ORDER, "sources": rows,
        "note": ("Two sources are append-silence derivatives and two are raw guides. Every one ends in "
                 "digital silence, which is the condition the tail gate tests.")})
    for s in ORDER:
        d = wdir(s)
        d.mkdir(parents=True, exist_ok=True)
        if not (d / "SCRIPT.txt").exists():
            save_x(d / "SCRIPT.txt", spoken(s)["spoken_text"].encode())
        if not (d / "TRANSFER-INPUT.json").exists():
            save_json_x(d / "TRANSFER-INPUT.json", {
                "endpoint": ENDPOINT, "target_voice_id": "scMbPZwQjr40V1MzL3Nj",
                "output_format": "pcm_48000",
                "fields": {"model_id": "eleven_multilingual_sts_v2",
                           "remove_background_noise": "false", "seed": "2026082501",
                           "voice_settings": json.dumps({"similarity_boost": 0.8, "speed": 1.0,
                                                         "stability": 0.4, "style": 0.0,
                                                         "use_speaker_boost": True}, sort_keys=True),
                           "file_format": "other"}})
    print(json.dumps({"sources": [{k: r[k] for k in ("short_id", "duration_seconds", "tail_energy",
                                                     "estimated_credits")} for r in rows],
                      "estimated_credits_total": total, "credit_cap": cap()}, indent=1))


# ---------------------------------------------------------------- exact-copy gate on the source

def gate(short_id: str, model: str = "medium.en") -> None:
    d = wdir(short_id)
    p = source_path(short_id)
    d.mkdir(parents=True, exist_ok=True)
    out = d / f"SOURCE-ASR.{model}.json"
    if out.exists():
        raise SystemExit(f"source ASR already recorded for {short_id}")
    save_json_x(d / f"SOURCE-ASR-INTENT.{model}.json", {
        "at_utc": now(), "source_media": rel(p), "source_media_sha256": sha_file(p),
        "tool": ASR_TOOL, "engine": ASR_ENGINE, "model": model,
        "purpose": "exact-copy verification of the transfer source against the bound spoken text"})
    # -d is required: without it the transcriber writes beside the input, and three of the
    # four sources live in run directories that are deliberately read only.
    r = subprocess.run(["npx", "--yes", ASR_TOOL, "transcribe", str(p),
                        "--engine", ASR_ENGINE, "--model", model, "--json", "-d", str(d)],
                       capture_output=True, cwd=str(d), timeout=1800)
    save_x(d / f"asr-stdout.{model}.json", r.stdout)
    tp = next((q for q in (d / "transcript.json", d / "media/transcript.json") if q.exists()), None)
    if tp is None:
        raise SystemExit(f"no ASR transcript produced for {short_id}")
    tj = json.loads(tp.read_text())
    items = tj if isinstance(tj, list) else (tj.get("words") or [])
    words = [str(w.get("text", w.get("word", ""))) for w in items if isinstance(w, dict)]
    if not words:
        raise SystemExit(f"could not read words from the transcript for {short_id}")
    exp = cn.norm(spoken(short_id)["spoken_text"])
    act = cn.norm(" ".join(words))
    diffs, und = cn.classify(exp, act)
    tp_new = d / f"transcript.{model}.json"
    if tp.name == "transcript.json" and not tp_new.exists():
        tp.rename(tp_new)
        tp = tp_new
    res = {"at_utc": now(), "source_media": rel(p), "source_media_sha256": sha_file(p),
           "script_sha256": sha_file(d / "SCRIPT.txt"), "asr_model": model,
           "transcript_path": rel(tp), "transcript_sha256": sha_file(tp),
           "expected_token_count": len(exp), "actual_token_count": len(act),
           "declared_orthography_differences": [x for x in diffs if x["declared"]],
           "undeclared_differences": und,
           "exact_match": not und, "accepted": not und,
           "limitations": "ASR cannot prove an unclipped final phoneme and does not replace owner listening."}
    save_json_x(out, res)
    print(json.dumps({"short_id": short_id, "model": model, "exact_match": res["exact_match"],
                      "tokens": f"{len(exp)}/{len(act)}",
                      "declared": len(res["declared_orthography_differences"]),
                      "undeclared": [(x["expected"], x["actual"]) for x in und]}))
    if und:
        raise SystemExit(f"exact-copy gate failed on the transfer source for {short_id}; no transfer")


# ---------------------------------------------------------------- preflight

def preflight() -> None:
    auth()
    assert_batch_clear()
    if not MANIFEST.exists():
        raise SystemExit("run sources first")
    man = json.loads(MANIFEST.read_text())
    bindings, total = [], 0
    for s in ORDER:
        d = wdir(s)
        p = source_path(s)
        row = next(r for r in man["sources"] if r["short_id"] == s)
        if row["source_sha256"] != sha_file(p):
            raise SystemExit(f"source for {s} changed since the manifest")
        asr = next((json.loads(q.read_text()) for q in sorted(d.glob("SOURCE-ASR.*.json"))
                    if json.loads(q.read_text()).get("accepted")), None)
        basis = "single_model_exact"
        if asr is None:
            # No single model read this source cleanly. An explicit, owner-backed
            # resolution naming every disputed token is the only other way through.
            rp = d / "EXACT-COPY-RESOLUTION.json"
            if not rp.exists():
                raise SystemExit(f"no accepted exact-copy record or resolution for the {s} transfer source")
            rr = json.loads(rp.read_text())
            if not rr.get("accepted") or rr.get("transfer_source_sha256") != sha_file(p):
                raise SystemExit(f"exact-copy resolution for {s} is not accepted or binds different bytes")
            if not rr.get("token_by_token_resolution"):
                raise SystemExit(f"exact-copy resolution for {s} names no tokens")
            asr = {"asr_model": "+".join(sorted(rr["reads"])), "source_media_sha256": sha_file(p)}
            basis = rr.get("accepted_basis", "resolution")
        if asr["source_media_sha256"] != sha_file(p):
            raise SystemExit(f"exact-copy record for {s} binds different bytes")
        total += row["estimated_credits"]
        bindings.append({"short_id": s, "source_sha256": row["source_sha256"],
                         "asr_accepted": True, "asr_model": asr["asr_model"],
                         "exact_copy_basis": basis,
                         "transfer_input_sha256": sha_file(d / "TRANSFER-INPUT.json"),
                         "script_sha256": sha_file(d / "SCRIPT.txt"),
                         "estimated_credits": row["estimated_credits"]})
    if total > cap():
        raise SystemExit(f"forecast {total} credits above the {cap()} cap")
    remaining, acct = balance()
    if remaining < total:
        raise SystemExit("live balance does not cover the batch")
    save_json_x(PREFLIGHT, {
        "at_utc": now(), "status": "pass_transfer_submission_allowed_once_per_short",
        "manifest_sha256": sha_file(MANIFEST), "approved_credit_cap": cap(),
        "transfer_rate_multiplier": 1, "estimated_credits_total": total,
        "live_balance_remaining": remaining, "account": acct, "short_bindings": bindings})
    print(json.dumps({"status": "pass", "estimated_credits_total": total,
                      "credit_cap": cap(), "live_balance_remaining": remaining}, indent=1))


# ---------------------------------------------------------------- transfer

def transfer(short_id: str) -> None:
    auth()
    assert_batch_clear()
    if not PREFLIGHT.exists():
        raise SystemExit("preflight has not passed")
    pf = json.loads(PREFLIGHT.read_text())
    if pf.get("status") != "pass_transfer_submission_allowed_once_per_short":
        raise SystemExit("preflight is not a pass")
    if pf.get("approved_credit_cap") != cap() or pf.get("transfer_rate_multiplier") != 1:
        raise SystemExit("preflight cap or rate binding changed")
    if pf.get("manifest_sha256") != sha_file(MANIFEST):
        raise SystemExit("manifest changed after preflight")
    d = wdir(short_id)
    intent = d / "ELEVEN-SUBMISSION-INTENT.json"
    if intent.exists():
        raise SystemExit(f"transfer intent already exists for {short_id}; no retry authorized")
    if count("ELEVEN-SUBMISSION-INTENT.json") >= 4:
        raise SystemExit("transfer call cap already reached")
    p = source_path(short_id)
    want = next(b for b in pf["short_bindings"] if b["short_id"] == short_id)
    if (want["source_sha256"] != sha_file(p)
            or want["transfer_input_sha256"] != sha_file(d / "TRANSFER-INPUT.json")
            or want["script_sha256"] != sha_file(d / "SCRIPT.txt")):
        raise SystemExit(f"evidence for {short_id} changed after preflight")
    spent = sum(int(json.loads((wdir(s) / "ELEVEN-RECEIPT.json").read_text()).get("actual_credits_charged", 0))
                for s in ORDER if (wdir(s) / "ELEVEN-RECEIPT.json").exists())
    pending = sum(b["estimated_credits"] for b in pf["short_bindings"]
                  if not (wdir(b["short_id"]) / "ELEVEN-RECEIPT.json").exists())
    if spent + pending > cap():
        raise SystemExit(f"actual {spent} plus pending {pending} would exceed the {cap()} cap")
    remaining, acct = balance()
    if remaining < pending:
        raise SystemExit("live balance no longer covers the unsubmitted transfers")
    ti = json.loads((d / "TRANSFER-INPUT.json").read_text())
    body, ctype = cal.multipart(ti["fields"], p.name, p.read_bytes())
    url = f"{ti['endpoint']}?output_format={ti['output_format']}&enable_logging=true"
    save_json_x(d / "ELEVEN-ACCOUNT-BEFORE.json", {
        "at_utc": now(), "account": acct, "live_balance_remaining": remaining,
        "actual_credits_spent_so_far": spent, "pending_estimated_credits": pending})
    save_json_x(intent, {
        "at_utc": now(), "stage": "elevenlabs_voice_transfer", "short_id": short_id, "url": url,
        "fields": ti["fields"], "request_body_sha256": sha_bytes(body),
        "source_path": rel(p), "source_sha256": sha_file(p),
        "preflight_sha256": sha_file(PREFLIGHT),
        "account_before_sha256": sha_file(d / "ELEVEN-ACCOUNT-BEFORE.json"),
        "provider_generation_attempt": 1, "automatic_retries": 0,
        "estimated_credits_ceiling": want["estimated_credits"], "credit_cap": cap(),
        "seeded_provider_note": "Voice Changer is seeded; a retry returns identical audio (finding N4B-3)",
        "submission_outcome_policy": "an uncertain or failed outcome stops the batch and cannot be retried"})
    k = key()
    r = urllib.request.Request(url, method="POST", data=body,
                               headers={"xi-api-key": k, "Content-Type": ctype, "Accept": "audio/pcm"})
    try:
        with urllib.request.urlopen(r, timeout=900) as resp:
            status, raw, hdrs = resp.status, resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as e:
        status, raw, hdrs = e.code, e.read(), dict(e.headers or {})
    except Exception as exc:
        save_json_x(d / "ELEVEN-ERROR.json", {"at_utc": now(), "error_class": type(exc).__name__,
                                              "submission_outcome": "uncertain_no_retry"})
        raise SystemExit(f"transport outcome uncertain for {short_id}; no retry")
    receipt: dict[str, Any] = {
        "at_utc": now(), "http_status": status, "calls": 1, "retries": 0,
        "response_headers": {kk: vv for kk, vv in hdrs.items() if kk.lower() != "set-cookie"}}
    if status != 200:
        msg = raw.decode("utf-8", "replace")[:2000].replace(k, "[REDACTED]")
        receipt |= {"error": msg, "accepted": False}
        save_json_x(d / "ELEVEN-RECEIPT.json", receipt)
        raise SystemExit(f"ElevenLabs HTTP {status} for {short_id}; no retry")
    pcm = d / "media/original-c.pcm"
    save_x(pcm, raw)
    wav = d / "media/original-c.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "s16le", "-ar", "48000", "-ac", "1",
                    "-i", str(pcm), "-c:a", "pcm_s16le", str(wav)], check=True, timeout=900)
    pr = cal.probe(wav)
    src = cal.probe(p)
    delta = float(pr["duration_seconds"]) - float(src["duration_seconds"])
    after, acct_after = balance()
    actual = max(0, remaining - after)
    receipt |= {"final": pr | {"path": rel(wav)}, "pcm_sha256": sha_bytes(raw),
                "source_duration_seconds": src["duration_seconds"],
                "duration_delta_seconds": round(delta, 3),
                "duration_within_half_second": abs(delta) <= 0.5,
                "tail_energy_threshold": cal.TAIL_ENERGY_THRESHOLD,
                "ends_in_silence": bool(pr.get("ends_in_silence")),
                "estimated_credits_ceiling": want["estimated_credits"],
                "actual_credits_charged": actual, "account_after": acct_after,
                "accepted": True}
    save_json_x(d / "ELEVEN-RECEIPT.json", receipt)
    print(json.dumps({"short_id": short_id, "seconds": pr["duration_seconds"],
                      "delta_vs_source": round(delta, 3),
                      "tail_energy": pr.get("tail_energy"),
                      "ends_in_silence": receipt["ends_in_silence"],
                      "actual_credits": actual}))
    if not receipt["duration_within_half_second"]:
        raise SystemExit(f"transferred duration drifted {delta:.3f}s for {short_id}; batch stopped")


# ---------------------------------------------------------------- verify the transferred audio

def verify(short_id: str, model: str = "medium.en") -> None:
    """Exact-copy check on the Original C result. The transfer should preserve words; this
    is what establishes that it did, rather than assuming it."""
    d = wdir(short_id)
    wav = d / "media/original-c.wav"
    rec = json.loads((d / "ELEVEN-RECEIPT.json").read_text())
    if not rec.get("accepted") or rec["final"]["sha256"] != sha_file(wav):
        raise SystemExit(f"transferred media does not match its receipt for {short_id}")
    out = d / f"FINAL-ASR.{model}.json"
    if out.exists():
        raise SystemExit(f"final ASR already recorded for {short_id}")
    save_json_x(d / f"FINAL-ASR-INTENT.{model}.json", {
        "at_utc": now(), "media": rel(wav), "media_sha256": sha_file(wav),
        "provider_receipt_sha256": sha_file(d / "ELEVEN-RECEIPT.json"),
        "tool": ASR_TOOL, "engine": ASR_ENGINE, "model": model,
        "purpose": "confirm the Voice Changer transfer preserved the locked word sequence"})
    sub = d / f"final-asr-{model}"
    sub.mkdir(exist_ok=True)
    r = subprocess.run(["npx", "--yes", ASR_TOOL, "transcribe", str(wav),
                        "--engine", ASR_ENGINE, "--model", model, "--json", "-d", str(sub)],
                       capture_output=True, cwd=str(sub), timeout=1800)
    save_x(sub / "stdout.json", r.stdout)
    tp = next((q for q in (sub / "transcript.json", sub / "media/transcript.json") if q.exists()), None)
    if tp is None:
        raise SystemExit(f"no final ASR transcript for {short_id}")
    tj = json.loads(tp.read_text())
    items = tj if isinstance(tj, list) else (tj.get("words") or [])
    words = [str(w.get("text", w.get("word", ""))) for w in items if isinstance(w, dict)]
    exp = cn.norm(spoken(short_id)["spoken_text"])
    act = cn.norm(" ".join(words))
    diffs, und = cn.classify(exp, act)
    res = {"at_utc": now(), "media": rel(wav), "media_sha256": sha_file(wav),
           "asr_model": model, "transcript_path": rel(tp), "transcript_sha256": sha_file(tp),
           "expected_token_count": len(exp), "actual_token_count": len(act),
           "declared_orthography_differences": [x for x in diffs if x["declared"]],
           "undeclared_differences": und, "exact_match": not und, "accepted": not und,
           "limitations": ("Confirms the word sequence survived the transfer. It says nothing about "
                           "voice match, performance or register, which are owner judgements.")}
    save_json_x(out, res)
    print(json.dumps({"short_id": short_id, "exact_match": res["exact_match"],
                      "tokens": f"{len(exp)}/{len(act)}",
                      "declared": [x["kind"] for x in diffs if x["declared"]],
                      "undeclared": [(x["expected"], x["actual"]) for x in und]}))


# ---------------------------------------------------------------- summary

def summary() -> None:
    rows, credits = [], 0
    for s in ORDER:
        d = wdir(s)
        rp = d / "ELEVEN-RECEIPT.json"
        er = json.loads(rp.read_text()) if rp.exists() else {}
        credits += int(er.get("actual_credits_charged", 0))
        rows.append({"short_id": s, "slug": d.name,
                     "source": SOURCES[s][1], "source_basis": SOURCES[s][2],
                     "final_path": er.get("final", {}).get("path"),
                     "final_sha256": er.get("final", {}).get("sha256"),
                     "seconds": er.get("final", {}).get("duration_seconds"),
                     "delta_vs_source": er.get("duration_delta_seconds"),
                     "tail_energy": er.get("final", {}).get("tail_energy"),
                     "ends_in_silence": er.get("ends_in_silence"),
                     "actual_credits": er.get("actual_credits_charged")})
    man = json.loads(MANIFEST.read_text())
    est = man["estimated_credits_total"]
    out = {"at_utc": now(), "episode": "EP009", "stage": "elevenlabs_voice_transfer",
           "target_voice": "Original C", "model_id": "eleven_multilingual_sts_v2",
           "transfer_calls": count("ELEVEN-SUBMISSION-INTENT.json"), "automatic_retries": 0,
           "estimated_credits_total": est, "credit_cap": cap(), "within_cap": est <= cap(),
           "measured_balance_delta": credits,
           "cost_caveat": ("The receipts record actual_credits_charged 0 because the subscription endpoint's "
                           "character_count did not move: it counts text-to-speech characters and does not "
                           "appear to track speech-to-speech usage. EP007's transfer receipts recorded only an "
                           "estimated ceiling for the same reason. Treat " + str(est) + " as the estimate and 0 "
                           "as unmeasurable from this endpoint, not as free. The invoice is the authority."),
           "shorts": rows,
           "open_check": ("Voice match, performance and register are owner judgements on this audio and have "
                          "not been made. Nothing here is acceptance, and no render, release or publication "
                          "is authorized.")}
    save_json_x(WORK / "TRANSFER-SUMMARY.json", out)
    print(json.dumps(out, indent=1))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("stage", choices=["sources", "gate", "preflight", "transfer", "verify", "summary"])
    ap.add_argument("short_id", nargs="?")
    ap.add_argument("--model", default="medium.en")
    a = ap.parse_args()
    if a.stage in {"gate", "transfer", "verify"}:
        if not a.short_id:
            raise SystemExit(f"{a.stage} needs a short id")
        if a.stage == "gate":
            gate(a.short_id, a.model)
        elif a.stage == "verify":
            verify(a.short_id, a.model)
        else:
            transfer(a.short_id)
    else:
        {"sources": sources, "preflight": preflight, "summary": summary}[a.stage]()


if __name__ == "__main__":
    main()
