"""
write_shorts_scenes.py — pin motion-graphics scene scripts into each short's
render_data JSON.

Time-mapped to the VO cues from prepare_shorts.py so scene beats hit the same
seconds as the words they visualize. Idempotent: rewrites `scenes` and
`cold_open_seconds` on every run.

Usage:  python scripts/originate/write_shorts_scenes.py voice-agent-agency
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


# ────────────────────────────────────────────────────────────────────────
# Per-episode scene scripts. Add another dict entry when EP003 ships; the
# runner falls back to raising if a slug isn't scripted here yet (safer than
# silently producing v1 shorts when the user asked for v2).
# ────────────────────────────────────────────────────────────────────────

VOICE_AGENT_AGENCY = {
    # SHORT-01 — 38%/62% split → $11B
    # VO: "One study found only 38% ... 62% voicemail or nowhere ... solo
    # operators fix that ... $300-1,000/mo ... $11B valuation."
    "short-01": {
        "cold_open_seconds": 1.5,
        "scenes": [
            {"kind": "bignumber", "start": 0.0, "duration": 1.5,
             "kicker": "ONE STUDY FOUND", "value": "38%", "size": "hero"},
            {"kind": "barsplit", "start": 1.5, "duration": 4.0,
             "kicker": "OF CALLS TO SMALL BUSINESSES",
             "left": {"value": 38, "label": "ANSWERED", "display": "38%"},
             "right": {"value": 62, "label": "MISSED", "display": "62%"},
             "highlight": "right"},
            {"kind": "bignumber", "start": 5.5, "duration": 5.1,
             "value": "62%", "label": "OF CALLS", "sub": ["Voicemail.", "Or nowhere."]},
            {"kind": "stamp", "start": 10.6, "duration": 2.1,
             "text": "SOLO OPERATORS", "sub": "FIX THAT"},
            {"kind": "bignumber", "start": 12.7, "duration": 3.9,
             "kicker": "PER CLIENT",
             "value": "$300 — $1,000", "label": "/ MO"},
            {"kind": "bignumber", "start": 16.6, "duration": 5.8,
             "kicker": "ELEVENLABS · JUST RAISED",
             "value": "$11B", "label": "VALUATION", "accent": True, "size": "hero"},
        ],
    },

    # SHORT-02 — "This voice is AI"
    # VO: "you're listening to the proof ... this voice ... that's an AI voice
    # ... same stack ... didn't notice / that's the point ... where the seams
    # still show."
    "short-02": {
        "cold_open_seconds": 1.5,
        "scenes": [
            {"kind": "waveform", "start": 0.0, "duration": 4.7,
             "headline": "THIS VOICE", "sub": "LISTENING TO THE PROOF",
             "bars": 32},
            {"kind": "stamp", "start": 4.7, "duration": 4.0,
             "text": "= AI VOICE", "sub": "AN ELEVENLABS RENDER",
             "size": "hero"},
            {"kind": "stack", "start": 8.7, "duration": 3.5,
             "headline": "Running on the same stack.",
             "nodes": ["ELEVENLABS · RETELL", "THIS EPISODE"]},
            {"kind": "wordkill", "start": 12.2, "duration": 4.0,
             "crossed": "Did you notice?",
             "replacement": "That's the point."},
            {"kind": "stamp", "start": 16.2, "duration": 4.5,
             "text": "“GOOD ENOUGH”", "sub": "EXACTLY HOW GOOD"},
            {"kind": "stamp", "start": 20.7, "duration": 2.9,
             "text": "SEAMS STILL SHOW", "sub": "WHERE THE STACK BREAKS"},
        ],
    },

    # SHORT-03 — Missed-call math (long, 44.18s)
    # VO: "plumber missing 15 calls a week at $350 ... six figures a year
    # ... $500/mo answering service is a rounding error ... sales call math
    # ... 85% never call back / 62% call competitor / 80% won't leave a
    # message ... reported not audited but owners nod ... their own missed-
    # call screen."
    "short-03": {
        "cold_open_seconds": 1.5,
        "scenes": [
            {"kind": "counter", "start": 0.0, "duration": 1.5,
             "kicker": "ONE PLUMBER · ONE WEEK",
             "from": 0, "to": 15, "format": "int",
             "label": "MISSED CALLS"},
            {"kind": "bignumber", "start": 1.5, "duration": 4.0,
             "kicker": "15 CALLS · $350 EACH",
             "value": "$5,250", "label": "PER WEEK LEFT ON THE TABLE"},
            {"kind": "counter", "start": 5.5, "duration": 4.0,
             "kicker": "SIX FIGURES A YEAR",
             "from": 5250, "to": 273000, "format": "money",
             "suffix": "/ YR", "label": "PLUMBER · SINGLE OPERATOR"},
            {"kind": "barsplit", "start": 9.5, "duration": 4.8,
             "kicker": "AGAINST THAT NUMBER",
             "left": {"value": 500, "label": "ANSWERING SERVICE", "display": "$500", "sub": "PER MONTH"},
             "right": {"value": 273000, "label": "MISSED", "display": "$273K", "sub": "PER YEAR"},
             "highlight": "right"},
            {"kind": "stamp", "start": 14.3, "duration": 2.0,
             "text": "THE SALES CALL", "sub": "LOW-END AGENCY MATH"},
            {"kind": "rings", "start": 16.3, "duration": 12.4,
             "kicker": "BEHAVIORAL NUMBERS · REPORTED RESEARCH",
             "rings": [
                 {"value": 85, "label": "NEVER CALL BACK"},
                 {"value": 62, "label": "CALL A COMPETITOR"},
                 {"value": 80, "label": "WON'T LEAVE A MSG"},
             ]},
            {"kind": "stamp", "start": 28.7, "duration": 5.3,
             "text": "OWNERS NOD", "sub": "REPORTED, NOT AUDITED"},
            {"kind": "bignumber", "start": 34.0, "duration": 8.4,
             "kicker": "MATCHES THEIR OWN",
             "value": "MISSED", "label": "· MISSED · MISSED",
             "size": "medium"},
        ],
    },

    # SHORT-04 — Platform / Agency / Plumber, agency at risk
    # VO: "the open question isn't whether small businesses will pay ... the
    # missed-call math answers that ... it's whether the agency layer
    # survives 18 months ... or whether ElevenLabs and Retell just sell it
    # themselves."
    "short-04": {
        "cold_open_seconds": 1.5,
        "scenes": [
            {"kind": "stack", "start": 0.0, "duration": 5.0,
             "headline": "The question everyone asks:",
             "nodes": ["PLATFORM", "AGENCY", "PLUMBER"], "emphasis": 1},
            {"kind": "wordkill", "start": 5.0, "duration": 3.5,
             "crossed": "Will businesses pay?",
             "replacement": "The math already did."},
            {"kind": "stack", "start": 8.5, "duration": 6.5,
             "headline": "The real question:",
             "nodes": ["PLATFORM", "AGENCY · 18 MONTHS?", "PLUMBER"],
             "emphasis": 1},
            {"kind": "stack", "start": 15.0, "duration": 7.5,
             "headline": "Or do they cut the middle?",
             "nodes": ["ELEVENLABS · RETELL", "AGENCY", "PLUMBER"],
             "emphasis": 1, "bypass": [0, 2]},
        ],
    },
}

SCENE_SCRIPTS = {
    "voice-agent-agency": VOICE_AGENT_AGENCY,
}


def patch_short(json_path: Path, patch: dict) -> None:
    data = json.loads(json_path.read_text())
    data["cold_open_seconds"] = patch["cold_open_seconds"]
    data["scenes"] = patch["scenes"]
    json_path.write_text(json.dumps(data))
    print(f"  patched {json_path.name}: cold_open={patch['cold_open_seconds']}s, "
          f"{len(patch['scenes'])} scenes")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    args = ap.parse_args()

    scripts = SCENE_SCRIPTS.get(args.slug)
    if scripts is None:
        raise SystemExit(f"no scene scripts authored for slug={args.slug!r}. "
                         f"Add a dict to write_shorts_scenes.py and re-run.")

    root = Path(__file__).resolve().parents[2]
    rd_dir = root / "originate" / args.slug / "render_data"
    for name, patch in scripts.items():
        p = rd_dir / f"{name}.json"
        if not p.exists():
            print(f"  skip {name}: {p} not found")
            continue
        patch_short(p, patch)
    print(f"\nDone. Re-render with:")
    for name in scripts:
        print(f"  npx remotion render src/index.ts Short out/{name}.mp4 "
              f"--props=../originate/{args.slug}/render_data/{name}.json")


if __name__ == "__main__":
    main()
