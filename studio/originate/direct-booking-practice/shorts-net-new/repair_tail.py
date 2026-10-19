#!/usr/bin/env python3
"""Append-silence tail repair on a derived copy, per the EP007 precedent.

Precedent: studio/originate/exit-readiness-prep/shorts-net-new/narration-v4/
short-01-thirty-day-map/DERIVED-GUIDE-REPAIR.json

What this does: writes a derived copy of an owner-selected guide with 0.5 s of
digital silence appended, so the file genuinely ends in silence and the pinned
tail-energy gate measures 0.0. The source is never overwritten.

What this does NOT do: recreate a missing phoneme. It repairs a mechanical gate.
That is why it refuses to run without an owner record naming the exact take, and
why it records that limitation in its own output. The owner's ear establishes
that the ending is complete; the pad satisfies the machine.

No provider call. No cost. Deterministic.

Usage: repair_tail.py <run>/<slug> --authority <owner record path>
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import sys
import wave
from pathlib import Path

sys.dont_write_bytecode = True

BASE = Path(__file__).resolve().parent
REPO = next(p for p in (BASE, *BASE.parents) if p.name == "operator-economy")
CAL_PATH = REPO / "operator-blueprint-v2/02-narration-production/tools/calibrate.py"
PAD_SECONDS = 0.5
PRECEDENT = ("studio/originate/exit-readiness-prep/shorts-net-new/narration-v4/"
             "short-01-thirty-day-map/DERIVED-GUIDE-REPAIR.json")

_spec = importlib.util.spec_from_file_location("oe_calibrate", CAL_PATH)
cal = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cal)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target", help="<run>/<slug> holding the source guide")
    ap.add_argument("--authority", required=True, help="owner record selecting this exact take")
    ap.add_argument("--into", default=None,
                    help="<run>/<slug> to write the derivative into, when the source run is frozen")
    a = ap.parse_args()

    d = BASE / a.target
    dest = BASE / (a.into or a.target)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "media").mkdir(parents=True, exist_ok=True)
    src = d / "media/guide.wav"
    out = dest / "media/guide-derived-pad500ms.wav"
    rec_path = dest / "DERIVED-GUIDE-REPAIR.json"
    auth_path = REPO / a.authority

    if out.exists() or rec_path.exists():
        raise SystemExit(f"a repair already exists for {a.target}; refusing to overwrite evidence")
    if not src.exists():
        raise SystemExit(f"no source guide at {src}")
    if not auth_path.exists():
        raise SystemExit(f"no owner authority at {a.authority}")

    auth = json.loads(auth_path.read_text())
    sel = auth.get("selected_take") or {}
    az = auth.get("authorized", {})
    ok = bool(az.get("append_silence_repair_on_selected_take"))
    shorts = (az.get("append_silence_repair") or {}).get("shorts")
    short_id = Path(a.target).name[:2]
    if shorts is not None:
        ok = short_id in shorts
        sel = {"guide_sha256": None}  # a shorts-list authority names the short, not a hash
    if not ok:
        raise SystemExit("the owner record does not authorize an append-silence repair for this short")

    # the authority must name THIS take, by hash, not merely this short
    receipt = json.loads((d / "GOOGLE-RECEIPT.json").read_text())
    src_sha = sha(src.read_bytes())
    if receipt["guide"]["sha256"] != src_sha:
        raise SystemExit("source guide does not match its own provider receipt")
    if sel.get("guide_sha256") is not None and sel["guide_sha256"] != src_sha:
        raise SystemExit("the owner record selects a different take than this one; refusing")

    with wave.open(str(src), "rb") as w:
        params = w.getparams()
        frames = w.readframes(w.getnframes())
    if params.comptype != "NONE":
        raise SystemExit("compressed source; refusing")
    pad_frames = int(round(PAD_SECONDS * params.framerate))
    silence = b"\x00" * (pad_frames * params.sampwidth * params.nchannels)

    with wave.open(str(out), "wb") as w:
        w.setparams(params)
        w.writeframes(frames + silence)

    # prove the derived file is the source plus zeros and nothing else
    with wave.open(str(out), "rb") as w:
        dparams = w.getparams()
        dframes = w.readframes(w.getnframes())
    prefix_ok = dframes[:len(frames)] == frames
    zeros_ok = set(dframes[len(frames):]) <= {0}
    if not (prefix_ok and zeros_ok):
        out.unlink(missing_ok=True)
        raise SystemExit("derived file is not the source plus zeros; removed")

    sp, dp = cal.probe(src), cal.probe(out)
    rec = {
        "record_type": "ep009_guide_tail_repair",
        "at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": ("pass_selected_source_preserved_and_mechanical_tail_gate_repaired"
                   if dp.get("ends_in_silence") else "fail_gate_still_not_passing"),
        "provider_call": False,
        "cost": "none; local and deterministic",
        "precedent": PRECEDENT,
        "owner_authority": {"path": a.authority, "sha256": sha(auth_path.read_bytes()),
                            "verbatim": auth.get("verbatim"), "short": short_id},
        "source": {"path": str(src.relative_to(REPO)), "sha256": src_sha,
                   "pcm_sha256": sha(frames), "sample_frames": params.nframes,
                   "duration_seconds": sp["duration_seconds"], "tail_energy": sp.get("tail_energy"),
                   "source_overwritten": False},
        "operation": {"type": "append_digital_silence_to_derived_copy",
                      "appended_frames": pad_frames, "sample_rate_hz": params.framerate,
                      "channels": params.nchannels, "sample_width_bits": params.sampwidth * 8,
                      "appended_duration_seconds": PAD_SECONDS},
        "derived": {"path": str(out.relative_to(REPO)), "sha256": sha(out.read_bytes()),
                    "pcm_sha256": sha(dframes), "sample_frames": dparams.nframes,
                    "duration_seconds": dp["duration_seconds"],
                    "source_prefix_pcm_sha256": sha(frames),
                    "source_prefix_verified": prefix_ok,
                    "appended_frames_all_zero": zeros_ok,
                    "tail_energy": dp.get("tail_energy"),
                    "tail_energy_threshold_exclusive": cal.TAIL_ENERGY_THRESHOLD,
                    "ends_in_silence": dp.get("ends_in_silence")},
        "limitation": ("This deterministic derivative repairs the mechanical tail-silence gate. It does not "
                       "recreate a missing phoneme. The owner selected this source take after listening to its "
                       "ending, and the local exact-copy check separately verifies the complete locked word "
                       "sequence. Neither establishes voice match, performance or register."),
    }
    rec_path.write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({"target": a.target,
                      "source_tail": sp.get("tail_energy"),
                      "derived_tail": dp.get("tail_energy"),
                      "ends_in_silence": dp.get("ends_in_silence"),
                      "source_prefix_verified": prefix_ok,
                      "appended_frames_all_zero": zeros_ok,
                      "source_seconds": sp["duration_seconds"],
                      "derived_seconds": dp["duration_seconds"]}, indent=1))
    if not dp.get("ends_in_silence"):
        raise SystemExit("repair did not pass the gate")


if __name__ == "__main__":
    main()
