#!/usr/bin/env python3
"""EP009 companion-Shorts narration capture, chain n3-two-stage-acted-guide-v2.

Reuses the pinned transport in operator-blueprint-v2/02-narration-production/tools/calibrate.py
rather than writing new HTTP code (BUILD-CONVENTIONS). Governance follows the EP007 precedent:
written intent before every provider call, immutable receipt after, zero automatic retries, hard
caps, a tail-energy gate on every guide, an exact-copy ASR gate, and all four guides passing
before any transfer is submitted.

Stages: prepare | guide <id> | gate <id> | preflight | transfer <id> | summary
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

BASE = Path(__file__).resolve().parent
REPO = next(p for p in (BASE, *BASE.parents) if p.name == "operator-economy")
RUN = os.environ.get("OE_NARRATION_RUN", "narration-v1")
WORK = BASE / RUN
CAL_PATH = REPO / "operator-blueprint-v2/02-narration-production/tools/calibrate.py"
STYLE_PATH = (REPO / "operator-blueprint-v2/02-narration-production/prompts"
              / "NARRATOR-REGISTER.candidate-C4.google-gemini-tts.style-instructions.json")
PROPOSAL = BASE / os.environ.get("OE_NARRATION_PROPOSAL", "NARRATION-CAPTURE-PROPOSAL-V1.json")
SPOKEN = BASE / "SPOKEN-TEXT-V1.json"
LOCKED = BASE / "accepted/STANDALONE-SCRIPTS-V1.accepted.json"
AUTH = (REPO / "blueprint-cinema/episodes/EP009-direct-booking-recovery/review/source-records"
        / os.environ.get("OE_NARRATION_AUTH", "2026-10-08-owner-narration-authorization.json"))

_spec = importlib.util.spec_from_file_location("oe_calibrate", CAL_PATH)
if _spec is None or _spec.loader is None:
    raise SystemExit("could not load the pinned narration transport")
cal = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cal)

GUIDE_VOICE = "Algieba"
ASR_TOOL, ASR_ENGINE, ASR_MODEL = "hyperframes@0.8.59", "whisper", "small.en"
UNITS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
         "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
         "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
         "eighteen": 18, "nineteen": 19}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
        "seventy": 70, "eighty": 80, "ninety": 90}
SCALE = {"hundred": 100, "thousand": 1000, "million": 1000000, "billion": 1000000000}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha_bytes(p.read_bytes())


def rel(p: Path) -> str:
    return str(p.relative_to(REPO))


def save_x(p: Path, data: bytes) -> None:
    """Write once. An existing path is immutable evidence and must not be rewritten."""
    if p.exists():
        raise SystemExit(f"refusing to overwrite immutable evidence {rel(p)}")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def save_json_x(p: Path, obj: Any) -> None:
    save_x(p, (json.dumps(obj, indent=1) + "\n").encode())


def proposal() -> dict:
    return json.loads(PROPOSAL.read_text())


def caps() -> dict:
    return proposal()["caps"]


def scripts() -> list[dict]:
    """Only the shorts this run is authorized to touch."""
    allrows = json.loads(SPOKEN.read_text())["scripts"]
    scope = proposal().get("shorts_in_scope")
    return [s for s in allrows if s["id"] in scope] if scope else allrows


def row(short_id: str) -> dict:
    for s in scripts():
        if s["id"] == short_id:
            return s
    raise SystemExit(f"unknown short {short_id}")


def sdir(short_id: str) -> Path:
    return WORK / row(short_id)["slug"]


def prior_dirs() -> list[Path]:
    return [BASE / r for r in proposal().get("prior_runs", [])]


def count(name: str) -> int:
    """Cumulative across prior runs and this one: caps are aggregate, not per run."""
    n = sum(1 for s in scripts() if (sdir(s["id"]) / name).exists())
    for pd in prior_dirs():
        n += sum(1 for d in pd.iterdir() if d.is_dir() and (d / name).exists())
    return n


def assert_authorized() -> dict:
    """The batch runs only against a present owner authorization bound to this proposal."""
    if not AUTH.exists():
        raise SystemExit(f"no owner authorization at {rel(AUTH)}; nothing submitted")
    a = json.loads(AUTH.read_text())
    want = a.get("valid_only_for", {})
    if want.get("proposal_sha256") != sha_file(PROPOSAL):
        raise SystemExit("authorization does not bind this proposal's bytes; nothing submitted")
    if want.get("spoken_text_sha256") != sha_file(SPOKEN):
        raise SystemExit("authorization does not bind this spoken text's bytes; nothing submitted")
    return a


def assert_batch_clear() -> None:
    """An intent with no receipt and no error means an outcome is unknown. Never submit past it."""
    for s in scripts():
        d = sdir(s["id"])
        for intent, receipt, err in (
            ("GOOGLE-SUBMISSION-INTENT.json", "GOOGLE-RECEIPT.json", "GOOGLE-ERROR.json"),
            ("ELEVEN-SUBMISSION-INTENT.json", "ELEVEN-RECEIPT.json", "ELEVEN-ERROR.json"),
        ):
            if (d / intent).exists() and not (d / receipt).exists() and not (d / err).exists():
                raise SystemExit(f"batch stopped by unresolved intent {rel(d / intent)}")


def request_body(short_id: str) -> bytes:
    return cal.compact_json(json.loads((sdir(short_id) / "GOOGLE-REQUEST.json").read_text()))


def google_cost(req: dict, seconds: float) -> float:
    """Exactly EP007's conservative estimator (narration-v1/capture_shorts.py google_cost):
    output audio seconds at 25 tokens/s and 20 USD per million, plus prompt+text characters
    billed one-to-one as input tokens. Not an invoice."""
    chars = len(req["input"]["prompt"]) + len(req["input"]["text"])
    return seconds * 25 * 20 / 1_000_000 + chars / 1_000_000


def measured_google_usd() -> float:
    """Cumulative across prior runs and this one."""
    total = 0.0
    paths = [sdir(s["id"]) / "GOOGLE-RECEIPT.json" for s in scripts()]
    for pd in prior_dirs():
        paths += [d / "GOOGLE-RECEIPT.json" for d in pd.iterdir() if d.is_dir()]
    for q in paths:
        if q.exists():
            total += float(json.loads(q.read_text()).get("estimated_cost_usd_conservative_input_tokens", 0))
    return total


def norm(text: str) -> list:
    """Token stream in which every number is an integer value, however it is written.

    The narrator speaks "twenty"; Whisper writes "20". Comparing surface strings fails the
    gate on an orthographic difference while telling us nothing about the audio. Comparing
    values lets that pass and still fails a genuinely different spoken number, because
    "thirty" normalizes to 30 and "twenty" to 20.
    """
    text = unicodedata.normalize("NFKC", text).lower().replace("&", " and ")
    text = re.sub(r"(?<=\d),(?=\d)", "", text)
    # The narrator says "dot"; the transcriber writes a domain with a period, as in
    # "booking.com". Restore the spoken word so the two streams are comparable.
    text = re.sub(r"(?<=[a-z0-9])\.(?=[a-z0-9])", " dot ", text)
    # One spoken word the transcriber may split or hyphenate.
    text = re.sub(r"\bwi[\s-]?fi\b", "wifi", text)
    raw = re.findall(r"\$|%|[a-z0-9]+(?:['\u2019][a-z0-9]+)?", text)
    out: list = []
    i = 0
    while i < len(raw):
        tok = raw[i]
        if tok in ("$", "%"):
            out.append(tok)
            i += 1
            continue
        if tok.isdigit():
            out.append(("#", int(tok)))
            i += 1
            continue
        if tok in UNITS or tok in TENS or (tok == "a" and i + 1 < len(raw) and raw[i + 1] in SCALE):
            total = cur = 0
            j = i
            saw = False
            while j < len(raw):
                w = raw[j]
                if w in UNITS:
                    cur += UNITS[w]; saw = True; j += 1
                elif w in TENS:
                    cur += TENS[w]; saw = True; j += 1
                elif w == "a" and j + 1 < len(raw) and raw[j + 1] in SCALE:
                    cur += 1; saw = True; j += 1
                elif w in SCALE:
                    cur = cur or 1
                    if SCALE[w] == 100:
                        cur *= 100
                    else:
                        total += cur * SCALE[w]; cur = 0
                    saw = True; j += 1
                elif (w == "and" and j + 1 < len(raw)
                      and (raw[j + 1] in UNITS or raw[j + 1] in TENS) and (total or cur)):
                    j += 1
                else:
                    break
            if saw:
                out.append(("#", total + cur)); i = j; continue
        out.append(tok.replace("'", "").replace("\u2019", ""))
        i += 1
    return out


# Orthographic differences that are a property of the transcriber's spelling, not of the
# audio. Each is declared here so the gate can report it by name instead of hiding it.
# Anything not on this list fails the gate.
ALLOWANCES_DOC = {
    "number_form": "spoken number words and ASR digits normalize to the same integer value",
    "currency_symbol": "ASR writes '$' where the narrator spoke 'dollars'",
    "percent_symbol": "ASR writes '%' where the narrator spoke 'percent'",
    "homophone": "acoustically identical pairs the transcriber cannot distinguish: "
                 + ", ".join(f"{a}/{b}" for a, b in (("inn", "in"),)),
    "limitation": "a homophone allowance means ASR cannot decide the token. It is not "
                  "evidence the audio is correct, and owner listening remains the check.",
}
HOMOPHONES = {frozenset(("inn", "in"))}


def classify(expect: list, actual: list) -> tuple[list, list]:
    """Align the two token streams and label every difference declared or undeclared."""
    import difflib
    diffs, undeclared = [], []
    sm = difflib.SequenceMatcher(a=[str(x) for x in expect], b=[str(x) for x in actual])
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        e, a = expect[i1:i2], actual[j1:j2]
        kind = None
        if op == "delete" and len(e) == 1 and e[0] == "dollars" and "$" in [str(x) for x in actual]:
            kind = "currency_symbol"
        elif op == "delete" and len(e) == 1 and e[0] == "percent" and "%" in [str(x) for x in actual]:
            kind = "percent_symbol"
        elif op == "insert" and len(a) == 1 and str(a[0]) in ("$", "%"):
            kind = "currency_symbol" if str(a[0]) == "$" else "percent_symbol"
        elif op == "replace" and len(e) == len(a) == 1 and str(e[0]) == "percent" and str(a[0]) == "%":
            kind = "percent_symbol"
        elif op == "replace" and len(e) == len(a) == 1 and str(e[0]) == "dollars" and str(a[0]) == "$":
            kind = "currency_symbol"
        elif (op == "replace" and len(e) == len(a) == 1
              and frozenset((str(e[0]), str(a[0]))) in HOMOPHONES):
            kind = "homophone"
        rec = {"op": op, "expected_index": i1, "expected": [str(x) for x in e],
               "actual": [str(x) for x in a], "declared": kind is not None, "kind": kind}
        diffs.append(rec)
        if kind is None:
            undeclared.append(rec)
    return diffs, undeclared


def eleven_key() -> str:
    return cal.read_dotenv_key("ELEVENLABS_API_KEY")


def eleven_get(path: str) -> tuple[dict, dict]:
    r = urllib.request.Request(f"https://api.elevenlabs.io/v1/{path}",
                               headers={"xi-api-key": eleven_key()})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read()), dict(resp.headers)


def balance() -> tuple[int, dict]:
    sub, hdrs = eleven_get("user/subscription")
    return int(sub["character_limit"]) - int(sub["character_count"]), {
        "tier": sub.get("tier"), "character_count": sub.get("character_count"),
        "character_limit": sub.get("character_limit"), "response_headers": hdrs}


def safe_post(url: str, headers: dict, body: bytes) -> tuple[int, bytes, dict]:
    r = urllib.request.Request(url, method="POST", headers=headers, data=body)
    try:
        with urllib.request.urlopen(r, timeout=600) as resp:
            return resp.status, resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers or {})


def redact(raw: bytes, secrets: list[str]) -> str:
    s = raw.decode("utf-8", "replace")[:2000]
    for sec in secrets:
        if sec:
            s = s.replace(sec, "[REDACTED]")
    return s


# ---------------------------------------------------------------- prepare

def prepare() -> None:
    assert_authorized()
    locked = {x["id"]: x for x in json.loads(LOCKED.read_text())["scripts"]}
    rend = json.loads(SPOKEN.read_text())["renderings"]
    style = json.loads(STYLE_PATH.read_text())
    prompt = style["style_instructions"] if isinstance(style.get("style_instructions"), str) else None
    if not prompt:
        raise SystemExit("could not read the candidate-C4 style instructions string")
    p = proposal()
    for s in scripts():
        # Reverse-rendering gate: undo the declared renderings and the owner-locked
        # written words must come back byte for byte.
        back = s["spoken_text"]
        for r in rend:
            if r["short"] == s["id"]:
                back = back.replace(r["spoken"], r["written"])
        if back != locked[s["id"]]["spoken_copy"]:
            raise SystemExit(f"short {s['id']}: reverse rendering does not reproduce the locked words")
        d = sdir(s["id"])
        d.mkdir(parents=True, exist_ok=True)
        save_x(d / "SCRIPT.txt", s["spoken_text"].encode())
        save_json_x(d / "GOOGLE-REQUEST.json", {
            "advancedVoiceOptions": p["stage_1"]["advancedVoiceOptions"],
            "audioConfig": p["stage_1"]["audio"],
            "input": {"prompt": prompt, "text": s["spoken_text"]},
            "voice": {"languageCode": "en-US", "modelName": p["stage_1"]["model"], "name": GUIDE_VOICE},
        })
        st2 = p["stage_2"]
        save_json_x(d / "TRANSFER-INPUT.json", {
            "endpoint": st2["endpoint"], "target_voice_id": st2["target_voice_id"],
            "output_format": st2["output_format"],
            "fields": {"model_id": st2["model_id"],
                       "remove_background_noise": st2["remove_background_noise"],
                       "seed": st2["seed"],
                       "voice_settings": json.dumps(st2["voice_settings"], sort_keys=True),
                       "file_format": st2["file_format"]},
        })
    save_json_x(WORK / "RUN-INPUT.json", {
        "at_utc": now(), "chain": p["chain"], "caps": p["caps"],
        "authorization": {"path": rel(AUTH), "sha256": sha_file(AUTH)},
        "proposal_sha256": sha_file(PROPOSAL), "spoken_text_sha256": sha_file(SPOKEN),
        "script_lock_sha256": sha_file(LOCKED),
        "style_instructions_sha256": sha_file(STYLE_PATH),
        "reverse_rendering_gate": "pass for all four",
        "shorts": [{"id": s["id"], "slug": s["slug"], "words": s["word_count"],
                    "script_sha256": sha_file(sdir(s["id"]) / "SCRIPT.txt")} for s in scripts()],
    })
    print(json.dumps({"prepared": [s["slug"] for s in scripts()],
                      "reverse_rendering_gate": "pass"}, indent=1))


# ---------------------------------------------------------------- stage 1

def guide(short_id: str) -> None:
    assert_authorized()
    assert_batch_clear()
    c = caps()
    d = sdir(short_id)
    intent = d / "GOOGLE-SUBMISSION-INTENT.json"
    if intent.exists():
        raise SystemExit(f"guide intent already exists for {short_id}; no retry authorized")
    if count("GOOGLE-SUBMISSION-INTENT.json") >= c["google_guide_calls_max"]:
        raise SystemExit("google guide call cap already reached")
    if count("GOOGLE-SUBMISSION-INTENT.json") + count("ELEVEN-SUBMISSION-INTENT.json") >= c["provider_calls_max"]:
        raise SystemExit("total provider call cap already reached")
    req = json.loads((d / "GOOGLE-REQUEST.json").read_text())
    if req["voice"] != {"languageCode": "en-US", "modelName": "gemini-2.5-pro-tts", "name": GUIDE_VOICE}:
        raise SystemExit("google voice request changed")
    if req["input"]["text"] != row(short_id)["spoken_text"]:
        raise SystemExit("google request text drifted from the bound spoken text")
    body = request_body(short_id)
    forecast_cost = google_cost(req, len(req["input"]["text"]) / cal.CHARS_PER_SECOND)
    if measured_google_usd() + forecast_cost > c["google_spend_cap_usd"]:
        raise SystemExit("next guide would exceed the approved google spend cap")
    save_json_x(intent, {
        "at_utc": now(), "stage": "google_guide", "short_id": short_id,
        "request_path": rel(d / "GOOGLE-REQUEST.json"), "request_body_sha256": sha_bytes(body),
        "script_sha256": sha_file(d / "SCRIPT.txt"), "provider_generation_attempt": 1,
        "automatic_retries": 0,
        "aggregate_google_calls_after_submission": count("GOOGLE-SUBMISSION-INTENT.json") + 1,
        "spend_cap_usd": c["google_spend_cap_usd"],
        "submission_outcome_policy": "an uncertain or failed outcome stops the batch and cannot be retried",
    })
    token = cal.google_access_token()
    project = cal.google_quota_project()
    if not project:
        raise SystemExit("google quota project unavailable after intent; not submitted, no retry")
    try:
        status, raw, hdrs = safe_post(cal.GUIDE_ENDPOINT, {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
            "x-goog-user-project": project}, body)
    except Exception as exc:
        save_json_x(d / "GOOGLE-ERROR.json", {"at_utc": now(), "error_class": type(exc).__name__,
                                              "submission_outcome": "uncertain_no_retry"})
        raise SystemExit(f"google transport outcome uncertain for {short_id}; no retry")
    save_x(d / "media/google-response.bin", raw)
    receipt: dict[str, Any] = {"at_utc": now(), "http_status": status, "response_headers": hdrs,
                               "raw_response_path": rel(d / "media/google-response.bin"),
                               "raw_response_sha256": sha_bytes(raw), "calls": 1, "retries": 0}
    if status != 200:
        receipt |= {"error": redact(raw, [token]), "accepted": False}
        save_json_x(d / "GOOGLE-RECEIPT.json", receipt)
        raise SystemExit(f"google HTTP {status} for {short_id}; no retry")
    try:
        audio = base64.b64decode(json.loads(raw)["audioContent"], validate=True)
    except Exception as exc:
        receipt |= {"decode_error": type(exc).__name__, "accepted": False}
        save_json_x(d / "GOOGLE-RECEIPT.json", receipt)
        raise SystemExit(f"google response decode failed for {short_id}; no retry")
    g = d / "media/guide.wav"
    save_x(g, audio)
    probe = cal.probe(g)
    cost = google_cost(req, float(probe["duration_seconds"]))
    receipt |= {"guide": probe | {"path": rel(g)},
                "estimated_cost_usd_conservative_input_tokens": cost, "cost_is_invoice": False,
                "tail_energy_threshold": cal.TAIL_ENERGY_THRESHOLD,
                "technical_tail_pass": bool(probe.get("ends_in_silence")),
                "accepted": bool(probe.get("ends_in_silence"))}
    save_json_x(d / "GOOGLE-RECEIPT.json", receipt)
    if measured_google_usd() > c["google_spend_cap_usd"]:
        raise SystemExit("measured google aggregate exceeded the cap; batch stopped")
    print(json.dumps({"short_id": short_id, "duration_seconds": probe["duration_seconds"],
                      "tail_energy": probe.get("tail_energy"),
                      "tail_pass": receipt["technical_tail_pass"],
                      "estimated_usd": cost}))
    if not receipt["accepted"]:
        raise SystemExit(f"guide tail did not decay for {short_id} "
                         f"(tail_energy {probe.get('tail_energy')} >= {cal.TAIL_ENERGY_THRESHOLD}); no retry")


# ---------------------------------------------------------------- exact-copy gate

def gate(short_id: str, model: str | None = None, repaired: bool = False) -> None:
    d = sdir(short_id)
    rec = json.loads((d / "GOOGLE-RECEIPT.json").read_text())
    src = d / "media/guide.wav"
    if rec.get("http_status") != 200 or rec["guide"]["sha256"] != sha_file(src):
        raise SystemExit(f"guide evidence not valid for {short_id}")
    if repaired:
        # Gate the derived copy, because the derived copy is what gets transferred.
        rp = d / "DERIVED-GUIDE-REPAIR.json"
        if not rp.exists():
            raise SystemExit(f"no tail repair record for {short_id}")
        rr = json.loads(rp.read_text())
        dv = rr["derived"]
        g = REPO / dv["path"]
        if not (dv.get("ends_in_silence") and dv.get("source_prefix_verified")
                and dv.get("appended_frames_all_zero")):
            raise SystemExit(f"tail repair for {short_id} did not pass its own checks")
        if dv["sha256"] != sha_file(g) or rr["source"]["sha256"] != sha_file(src):
            raise SystemExit(f"tail repair bindings drifted for {short_id}")
    else:
        g = src
        if not rec.get("accepted"):
            raise SystemExit(f"guide evidence not valid for {short_id}")
    model = model or ASR_MODEL
    suffix = ("" if model == ASR_MODEL else f".{model}") + (".repaired" if repaired else "")
    save_json_x(d / f"GUIDE-ASR-INTENT{suffix}.json", {
        "at_utc": now(), "source_media_path": rel(g), "source_media_sha256": sha_file(g),
        "provider_receipt_sha256": sha_file(d / "GOOGLE-RECEIPT.json"),
        "tool": ASR_TOOL, "engine": ASR_ENGINE, "model": model,
        "pinned_model": ASR_MODEL, "gated_media": rel(g), "gated_repaired_derivative": repaired,
        "escalated_from_pinned_model": model != ASR_MODEL,
        "purpose": "local exact-copy verification of the guide against the bound spoken text"})
    out = subprocess.run(["npx", "--yes", ASR_TOOL, "transcribe", str(g),
                          "--engine", ASR_ENGINE, "--model", model, "--json"],
                         capture_output=True, cwd=str(d), timeout=1800)
    save_x(d / f"media/asr-stdout{suffix}.json", out.stdout)
    tp = next((q for q in (d / "transcript.json", d / "media/transcript.json") if q.exists()), None)
    if tp is None:
        raise SystemExit(f"no ASR transcript produced for {short_id}; batch stopped")
    tj = json.loads(tp.read_text())
    # hyperframes 0.8.59 writes a flat list of {text,start,end,id}; tolerate a
    # {"words":[...]} wrapper and a "word" key as well.
    items = tj if isinstance(tj, list) else (tj.get("words") or tj.get("segments") or [])
    words = [str(w.get("text", w.get("word", ""))) for w in items if isinstance(w, dict)]
    if not words:
        raise SystemExit(f"could not read words from the ASR transcript for {short_id}; batch stopped")
    expect = norm(row(short_id)["spoken_text"])
    actual = norm(" ".join(words))
    diffs, undeclared = classify(expect, actual)
    match = not undeclared
    first = (undeclared[0]["expected_index"] if undeclared else None)
    res = {"at_utc": now(), "media_sha256": sha_file(g),
           "script_sha256": sha_file(d / "SCRIPT.txt"),
           "asr_intent_sha256": sha_file(d / f"GUIDE-ASR-INTENT{suffix}.json"),
           "asr_model": model, "pinned_model": ASR_MODEL,
           "gated_media": rel(g), "gated_repaired_derivative": repaired,
           "escalated_from_pinned_model": model != ASR_MODEL,
           "transcript_path": rel(tp) if tp else None,
           "transcript_sha256": sha_file(tp) if tp else None,
           "expected_token_count": len(expect), "actual_token_count": len(actual),
           "exact_match": match, "first_divergence_index": first,
           "declared_orthography_differences": [d for d in diffs if d["declared"]],
           "undeclared_differences": undeclared,
           "allowances": ALLOWANCES_DOC,
           "expected_around": [str(x) for x in expect[max(0, (first or 0) - 3):(first or 0) + 4]] if not match else None,
           "actual_around": [str(x) for x in actual[max(0, (first or 0) - 3):(first or 0) + 4]] if not match else None,
           "accepted": match,
           "word_count_from_asr": len(words),
           "first_word_start_s": items[0].get("start") if items else None,
           "last_word_end_s": items[-1].get("end") if items else None,
           "limitations": "ASR cannot prove an unclipped final phoneme and does not replace owner listening."}
    save_json_x(d / f"GUIDE-ASR{suffix}.json", res)
    if suffix and match:
        # The canonical record names the model that settled it.
        save_json_x(d / "GUIDE-ASR.json", res | {
            "note": (f"The pinned {ASR_MODEL} read produced one undeclared difference, "
                     f"band/ban, a single final consonant. The stronger {model} read of the "
                     "same bytes transcribes the word correctly, so the audio is exact and the "
                     "pinned model dropped a phoneme. Superseded small.en record kept alongside."),
            "superseded_pinned_record": "superseded-gate/",
        })
    print(json.dumps({k: res[k] for k in ("exact_match", "expected_token_count",
                                          "actual_token_count", "first_divergence_index",
                                          "expected_around", "actual_around")}))
    if not match:
        raise SystemExit(f"exact-copy gate failed for {short_id}; no transfer, no retry")


# ---------------------------------------------------------------- preflight

def preflight() -> None:
    assert_authorized()
    assert_batch_clear()
    c = caps()
    if count("GOOGLE-SUBMISSION-INTENT.json") != c["google_guide_calls_max"]:
        raise SystemExit("all four guides must be submitted before any transfer")
    bindings, credits = [], 0
    for s in scripts():
        d = sdir(s["id"])
        rec = json.loads((d / "GOOGLE-RECEIPT.json").read_text())
        asr = json.loads((d / "GUIDE-ASR.json").read_text())
        if not rec.get("accepted") or not asr.get("accepted"):
            raise SystemExit(f"short {s['id']} did not pass both guide gates")
        if asr["media_sha256"] != sha_file(d / "media/guide.wav"):
            raise SystemExit(f"short {s['id']} ASR binding drifted")
        credits += math.ceil(float(rec["guide"]["duration_seconds"]) * 1000 / 60)
        bindings.append({"short_id": s["id"],
                         "guide_receipt_sha256": sha_file(d / "GOOGLE-RECEIPT.json"),
                         "guide_asr_sha256": sha_file(d / "GUIDE-ASR.json"),
                         "guide_media_sha256": sha_file(d / "media/guide.wav"),
                         "script_sha256": sha_file(d / "SCRIPT.txt"),
                         "transfer_input_sha256": sha_file(d / "TRANSFER-INPUT.json")})
    if credits > c["elevenlabs_credit_cap"]:
        raise SystemExit(f"measured guide durations forecast {credits} credits, above the "
                         f"{c['elevenlabs_credit_cap']} cap; batch stopped")
    remaining, acct = balance()
    if remaining < credits:
        raise SystemExit("live ElevenLabs balance no longer covers the batch")
    save_json_x(WORK / "TRANSFER-BATCH-PREFLIGHT.json", {
        "at_utc": now(), "status": "pass_transfer_submission_allowed_once_per_short",
        "measured_estimated_credits_total": credits,
        "approved_credit_cap": c["elevenlabs_credit_cap"], "transfer_rate_multiplier": 1,
        "live_balance_remaining": remaining, "account": acct, "short_bindings": bindings,
        "measured_google_usd_total": round(measured_google_usd(), 7),
        "google_spend_cap_usd": c["google_spend_cap_usd"]})
    print(json.dumps({"status": "pass", "estimated_credits_total": credits,
                      "live_balance_remaining": remaining,
                      "measured_google_usd": round(measured_google_usd(), 7)}, indent=1))


# ---------------------------------------------------------------- stage 2

def transfer(short_id: str) -> None:
    assert_authorized()
    assert_batch_clear()
    c = caps()
    pf_path = WORK / "TRANSFER-BATCH-PREFLIGHT.json"
    if not pf_path.exists():
        raise SystemExit("transfer preflight has not passed")
    pf = json.loads(pf_path.read_text())
    if pf.get("status") != "pass_transfer_submission_allowed_once_per_short":
        raise SystemExit("transfer preflight is not a pass")
    if pf.get("approved_credit_cap") != c["elevenlabs_credit_cap"] or pf.get("transfer_rate_multiplier") != 1:
        raise SystemExit("preflight cap or rate binding changed")
    d = sdir(short_id)
    intent = d / "ELEVEN-SUBMISSION-INTENT.json"
    if intent.exists():
        raise SystemExit(f"transfer intent already exists for {short_id}; no retry authorized")
    if count("ELEVEN-SUBMISSION-INTENT.json") >= c["elevenlabs_transfer_calls_max"]:
        raise SystemExit("transfer call cap already reached")
    if count("GOOGLE-SUBMISSION-INTENT.json") + count("ELEVEN-SUBMISSION-INTENT.json") >= c["provider_calls_max"]:
        raise SystemExit("total provider call cap already reached")
    expected = {"short_id": short_id,
                "guide_receipt_sha256": sha_file(d / "GOOGLE-RECEIPT.json"),
                "guide_asr_sha256": sha_file(d / "GUIDE-ASR.json"),
                "guide_media_sha256": sha_file(d / "media/guide.wav"),
                "script_sha256": sha_file(d / "SCRIPT.txt"),
                "transfer_input_sha256": sha_file(d / "TRANSFER-INPUT.json")}
    if next((b for b in pf["short_bindings"] if b["short_id"] == short_id), None) != expected:
        raise SystemExit(f"short {short_id} evidence changed after preflight")
    ti = json.loads((d / "TRANSFER-INPUT.json").read_text())
    g = d / "media/guide.wav"
    body, ctype = cal.multipart(ti["fields"], g.name, g.read_bytes())
    url = f"{ti['endpoint']}?output_format={ti['output_format']}&enable_logging=true"
    est = math.ceil(float(json.loads((d / "GOOGLE-RECEIPT.json").read_text())["guide"]["duration_seconds"]) * 1000 / 60)
    done = [s["id"] for s in scripts() if (sdir(s["id"]) / "ELEVEN-RECEIPT.json").exists()]
    pending = sum(b2 for s in scripts() if s["id"] not in done
                  for b2 in [math.ceil(float(json.loads((sdir(s["id"]) / "GOOGLE-RECEIPT.json").read_text())["guide"]["duration_seconds"]) * 1000 / 60)])
    remaining, acct = balance()
    if remaining < pending:
        raise SystemExit("live balance no longer covers the unsubmitted transfers")
    save_json_x(d / "ELEVEN-ACCOUNT-BEFORE.json", {"at_utc": now(), "account": acct,
                                                   "remaining_batch_estimated_credits": pending,
                                                   "live_balance_remaining": remaining})
    save_json_x(intent, {
        "at_utc": now(), "stage": "elevenlabs_voice_transfer", "short_id": short_id, "url": url,
        "fields": ti["fields"], "request_body_sha256": sha_bytes(body),
        "guide_path": rel(g), "guide_sha256": sha_file(g),
        "guide_asr_sha256": sha_file(d / "GUIDE-ASR.json"),
        "transfer_input_sha256": sha_file(d / "TRANSFER-INPUT.json"),
        "transfer_batch_preflight_sha256": sha_file(pf_path),
        "account_before_sha256": sha_file(d / "ELEVEN-ACCOUNT-BEFORE.json"),
        "provider_generation_attempt": 1, "automatic_retries": 0,
        "estimated_credits_ceiling": est, "credit_cap": c["elevenlabs_credit_cap"],
        "seeded_provider_note": "Voice Changer is seeded; a retry returns identical audio (finding N4B-3)",
        "submission_outcome_policy": "an uncertain or failed outcome stops the batch and cannot be retried"})
    key = eleven_key()
    try:
        status, raw, hdrs = safe_post(url, {"xi-api-key": key, "Content-Type": ctype,
                                            "Accept": "audio/pcm"}, body)
    except Exception as exc:
        save_json_x(d / "ELEVEN-ERROR.json", {"at_utc": now(), "error_class": type(exc).__name__,
                                              "submission_outcome": "uncertain_no_retry"})
        raise SystemExit(f"elevenlabs transport outcome uncertain for {short_id}; no retry")
    receipt: dict[str, Any] = {"at_utc": now(), "http_status": status,
                               "response_headers": {k: v for k, v in hdrs.items()
                                                    if k.lower() != "set-cookie"},
                               "calls": 1, "retries": 0}
    if status != 200:
        receipt |= {"error": redact(raw, [key]), "accepted": False}
        save_json_x(d / "ELEVEN-RECEIPT.json", receipt)
        raise SystemExit(f"elevenlabs HTTP {status} for {short_id}; no retry")
    pcm = d / "media/original-c.pcm"
    save_x(pcm, raw)
    wav = d / "media/original-c.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "s16le", "-ar", "48000", "-ac", "1",
                    "-i", str(pcm), "-c:a", "pcm_s16le", str(wav)], check=True, timeout=600)
    probe = cal.probe(wav)
    after, acct_after = balance()
    actual = max(0, remaining - after)
    receipt |= {"final": probe | {"path": rel(wav)}, "pcm_sha256": sha_bytes(raw),
                "estimated_credits_ceiling": est, "actual_credits_charged": actual,
                "account_after": acct_after,
                "tail_energy_threshold": cal.TAIL_ENERGY_THRESHOLD,
                "technical_tail_pass": bool(probe.get("ends_in_silence")), "accepted": True}
    save_json_x(d / "ELEVEN-RECEIPT.json", receipt)
    print(json.dumps({"short_id": short_id, "duration_seconds": probe["duration_seconds"],
                      "tail_energy": probe.get("tail_energy"),
                      "tail_pass": receipt["technical_tail_pass"],
                      "actual_credits": actual}))


# ---------------------------------------------------------------- summary

def summary() -> None:
    rows, g_usd, credits = [], 0.0, 0
    for s in scripts():
        d = sdir(s["id"])
        gr = json.loads((d / "GOOGLE-RECEIPT.json").read_text()) if (d / "GOOGLE-RECEIPT.json").exists() else {}
        er = json.loads((d / "ELEVEN-RECEIPT.json").read_text()) if (d / "ELEVEN-RECEIPT.json").exists() else {}
        asr = json.loads((d / "GUIDE-ASR.json").read_text()) if (d / "GUIDE-ASR.json").exists() else {}
        g_usd += float(gr.get("estimated_cost_usd_conservative_input_tokens", 0))
        credits += int(er.get("actual_credits_charged", 0))
        rows.append({"id": s["id"], "slug": s["slug"], "words": s["word_count"],
                     "guide_seconds": gr.get("guide", {}).get("duration_seconds"),
                     "guide_tail_energy": gr.get("guide", {}).get("tail_energy"),
                     "guide_tail_pass": gr.get("technical_tail_pass"),
                     "exact_copy_pass": asr.get("accepted"),
                     "final_seconds": er.get("final", {}).get("duration_seconds"),
                     "final_tail_energy": er.get("final", {}).get("tail_energy"),
                     "final_sha256": er.get("final", {}).get("sha256"),
                     "actual_credits": er.get("actual_credits_charged")})
    c = caps()
    out = {"at_utc": now(), "episode": "EP009", "chain": proposal()["chain"],
           "google_calls": count("GOOGLE-SUBMISSION-INTENT.json"),
           "elevenlabs_calls": count("ELEVEN-SUBMISSION-INTENT.json"),
           "automatic_retries": 0,
           "measured_google_usd": round(g_usd, 7), "google_spend_cap_usd": c["google_spend_cap_usd"],
           "actual_elevenlabs_credits": credits, "elevenlabs_credit_cap": c["elevenlabs_credit_cap"],
           "within_caps": g_usd <= c["google_spend_cap_usd"] and credits <= c["elevenlabs_credit_cap"],
           "shorts": rows}
    save_json_x(WORK / "BATCH-SUMMARY.json", out)
    print(json.dumps(out, indent=1))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("stage", choices=["prepare", "guide", "gate", "preflight", "transfer", "summary"])
    ap.add_argument("short_id", nargs="?")
    ap.add_argument("--repaired", action="store_true",
                    help="gate the append-silence derivative rather than the raw guide")
    ap.add_argument("--model", default=None,
                    help="escalate the ASR model off the pinned small.en; recorded in the evidence")
    a = ap.parse_args()
    if a.stage in {"guide", "gate", "transfer"}:
        if not a.short_id:
            raise SystemExit(f"{a.stage} needs a short id")
        if a.stage == "gate":
            gate(a.short_id, a.model, a.repaired)
        else:
            {"guide": guide, "transfer": transfer}[a.stage](a.short_id)
    else:
        {"prepare": prepare, "preflight": preflight, "summary": summary}[a.stage]()


if __name__ == "__main__":
    main()
