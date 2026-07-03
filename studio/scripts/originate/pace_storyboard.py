"""
Originate Step 3.5: the PACING PASS.

Reads storyboard.json (auto or hand-tuned) and stages the content each
screen ALREADY carries across its time window, so no composition sits
still. Emits per-screen `events` — timed visual cues the renderer
performs — and never invents new text:

  fragment  — one "·"-separated fragment of a reveal's body appears
              (progressive disclosure; Mayer segmenting principle)
  item      — one internal item of a custom card appears (risk bullets,
              artifact nodes, case-file rows, offer fields)
  pulse     — accent flash on a highlight word, anchored to the actual
              VO word timing from vo/words.json
  focus     — chart/ladder attention cycle: re-highlight data point i
              (a chart-reading moment, not a decoration)

Rationale: docs/faceless-video-editing-research.md cadence rules —
"internal animation or annotation every 3–6 seconds" in dense sections,
"avoid any single static composition above 20 seconds unless it is
actively building." The v1 pilot render broke these inside screens
(stack 43.9s/4 reveals, charts 24s/1 reveal) even though the screen-level
grammar was right.

Idempotent: recomputes `events` from scratch each run (safe to re-run
after hand-tuning or VO regeneration).

Usage:
    python scripts/originate/pace_storyboard.py originate/<slug>/script.json

Reads:   storyboard.json, script.json, vo/words.json
Rewrites: storyboard.json (adds `events` per screen)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Impact frames are short by design (1.2–4s) — they ARE the event.
IMPACT_LAYOUTS = {"quote", "chapter_reset"}

# Self-building layouts get a build window at screen start during which
# the renderer animates entrance (bars grow, nodes drop) without data.
SELF_BUILD_S = {"chart": 6.0, "ladder": 6.0, "gap": 5.0, "proof_card": 4.0,
                "schematic": 4.0}

MIN_EVENT_SPACING = 1.2   # merge/drop events closer than this (s)
PULSE_MIN_SPACING = 4.0   # pulses are accents, not strobes
PULSE_CAP_PER_SCREEN = 4
FOCUS_LEAD_FRACTION = 0.35  # focus cycles start after the build settles


def _norm(w: str) -> str:
    stripped = re.sub(r"[^\w']", "", w)
    return stripped.strip("'").lower()


# ---------------------------------------------------------------------
# Event derivation per screen
# ---------------------------------------------------------------------

def fragment_events(screen: dict) -> list[dict]:
    """Stage each reveal's '·'-separated body fragments across the
    reveal window. Fragment 0 shows with the reveal itself; the rest
    land at word-budget-proportional points, finishing by 90% of the
    window so the last fragment isn't cut off by the next reveal."""
    events = []
    for r in screen.get("reveals", []):
        body = r.get("body") or ""
        fragments = [f.strip() for f in body.split("·") if f.strip()]
        if len(fragments) < 2:
            continue
        span = max(r["end"] - r["at"], 0.1)
        for i in range(1, len(fragments)):
            at = r["at"] + span * (i / len(fragments)) * 0.9
            events.append({"at": round(at, 2), "kind": "fragment",
                           "beat": r.get("beat"), "index": i})
    return events


CUSTOM_ITEM_KEYS = {
    # custom-block key → (list path | fixed row count)
    "risk": ("bullets", None),
    "artifact": ("nodes", None),
    "caseFile": (None, 3),   # problem / workflow / result
    "offer": (None, 4),      # problem / deliverable / price / deadline
    "ladder": ("steps", None),
}


def item_events(screen: dict) -> list[dict]:
    """Stage internal items of custom cards across the screen window."""
    custom = screen.get("custom") or {}
    events = []
    for key, (list_key, fixed) in CUSTOM_ITEM_KEYS.items():
        block = custom.get(key)
        if not block:
            continue
        n = len(block.get(list_key) or []) if list_key else fixed
        if not n or n < 2:
            continue
        start, end = screen["start"], screen["end"]
        span = max(end - start, 0.1)
        lead = SELF_BUILD_S.get(screen["layout"], 0.0) * 0.5
        for i in range(1, n):
            at = start + lead + (span - lead) * (i / n) * 0.85
            events.append({"at": round(at, 2), "kind": "item",
                           "block": key, "index": i})
    return events


def pulse_events(screen: dict, highlights_by_section: dict,
                 words_by_section: dict) -> list[dict]:
    """Accent pulses at the VO moments where highlight words are spoken
    inside this screen's window."""
    sid = screen["section"]
    hl = highlights_by_section.get(sid) or set()
    if not hl:
        return []
    events = []
    last_at = -1e9
    for w in words_by_section.get(sid, []):
        if not (screen["start"] <= w["start"] < screen["end"]):
            continue
        if _norm(w["word"]) not in hl:
            continue
        if w["start"] - last_at < PULSE_MIN_SPACING:
            continue
        events.append({"at": round(w["start"], 2), "kind": "pulse",
                       "word": w["word"].strip(".,!?")})
        last_at = w["start"]
        if len(events) >= PULSE_CAP_PER_SCREEN:
            break
    return events


def focus_events(screen: dict) -> list[dict]:
    """Chart/ladder attention cycles: after the build settles, walk the
    data points again one at a time. Only fires on long holds — a 10s
    chart doesn't need a re-read; a 20s one does."""
    layout = screen["layout"]
    if layout not in ("chart", "ladder"):
        return []
    dur = screen["end"] - screen["start"]
    if dur < 12:
        return []
    custom = screen.get("custom") or {}
    n = len((custom.get("ladder") or {}).get("steps") or []) or 3
    t0 = screen["start"] + max(dur * FOCUS_LEAD_FRACTION, SELF_BUILD_S.get(layout, 6.0))
    t1 = screen["end"] - 2.0
    if t1 - t0 < 4:
        return []
    events = []
    for i in range(n):
        at = t0 + (t1 - t0) * (i / max(n - 1, 1))
        events.append({"at": round(at, 2), "kind": "focus", "index": i})
    return events


# ---------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------

def dedupe(events: list[dict]) -> list[dict]:
    events.sort(key=lambda e: e["at"])
    out = []
    for e in events:
        if out and e["at"] - out[-1]["at"] < MIN_EVENT_SPACING:
            # keep the more content-bearing event (fragment/item > focus > pulse)
            rank = {"fragment": 3, "item": 3, "focus": 2, "pulse": 1}
            if rank.get(e["kind"], 0) > rank.get(out[-1]["kind"], 0):
                out[-1] = e
            continue
        out.append(e)
    return out


def max_gap(screen: dict) -> float:
    """Longest visually-dead stretch on this screen: no reveal, no event,
    no self-build activity."""
    cues = [screen["start"] + SELF_BUILD_S.get(screen["layout"], 0.0)]
    cues += [r["at"] for r in screen.get("reveals", [])]
    cues += [e["at"] for e in screen.get("events", [])]
    cues = sorted(set(round(c, 2) for c in cues if c <= screen["end"]))
    cues.append(screen["end"])
    return max(b - a for a, b in zip(cues, cues[1:])) if len(cues) > 1 else 0.0


def main():
    ap = argparse.ArgumentParser(description="Pacing pass: stage screen content over time")
    ap.add_argument("script", help="Path to script.json (storyboard.json must exist beside it)")
    args = ap.parse_args()

    script_path = Path(args.script)
    base = script_path.parent if script_path.name != "storyboard.json" else script_path.parent
    sb_path = base / "storyboard.json"
    if not sb_path.exists():
        print("Error: storyboard.json not found — run storyboard.py (or the hand-tune) first.",
              file=sys.stderr)
        sys.exit(1)

    script = json.loads((base / "script.json").read_text())
    sb = json.loads(sb_path.read_text())
    words = json.loads((base / "vo" / "words.json").read_text())

    words_by_section: dict[str, list[dict]] = {}
    for w in words:
        words_by_section.setdefault(w["section"], []).append(w)

    highlights_by_section: dict[str, set] = {}
    for s in script.get("sections", []):
        toks = set()
        for b in s.get("beats", []):
            for h in b.get("highlight_words", []):
                for t in h.lower().split():
                    toks.add(_norm(t))
        highlights_by_section[s["id"]] = toks

    print(f"Pacing pass → {sb_path.name}")
    print(f"  {'screen':<16} {'layout':<12} {'dur':>6} {'events':>7} {'max gap':>8}")
    worst = 0.0
    for screen in sb.get("screens", []):
        if screen["layout"] in IMPACT_LAYOUTS:
            screen["events"] = []
            continue
        events = (fragment_events(screen)
                  + item_events(screen)
                  + pulse_events(screen, highlights_by_section, words_by_section)
                  + focus_events(screen))
        # Clamp inside the window and dedupe.
        events = [e for e in events if screen["start"] < e["at"] < screen["end"]]
        screen["events"] = dedupe(events)
        g = max_gap(screen)
        worst = max(worst, g)
        dur = screen["end"] - screen["start"]
        flag = "  ⚠" if g > 10 else ""
        print(f"  {screen['id']:<16} {screen['layout']:<12} {dur:5.1f}s "
              f"{len(screen['events']):>7} {g:7.1f}s{flag}")

    sb_path.write_text(json.dumps(sb, indent=2))
    print(f"✓ events written · worst dead stretch: {worst:.1f}s "
          f"(target ≤10s; renderer ambient drift covers the residue)")


if __name__ == "__main__":
    main()
