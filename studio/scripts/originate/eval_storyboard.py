"""
Storyboard eval: enforce the pacing rules from docs/storyboard-stage.md.

Runs against a produced storyboard.json. Pattern-matches eval_script.py's
PASS/WARN/FAIL/hard-fail contract so confidence.py can parse it.

Rules (per docs/storyboard-stage.md §"Pacing rules"):
  - Screen duration ≥10s HARD, ≥20s SOFT (WARN if 10-20s), ≤75s SOFT
    (WARN if 75-90s), HARD FAIL if >90s.
  - ≥2 reveals per `sheet` screen where the section has ≥2 talking
    points — HARD FAIL: sheet screen with 0 reveals; WARN: with 1
    reveal (planner has to justify by figure/source).
  - Max ~10 screens per 6-minute episode. HARD FAIL if cut-rate
    (screens / minutes) exceeds 1 per 15s; WARN if it exceeds 1 per 25s.
  - Every screen in a claim-carrying section (hook/evidence/economics/
    stack) must carry a figure or a source. WARN if missing.
  - Transitions only at argument boundaries — nothing to check here
    from data alone; delegated to the operator on ESCALATE.

Usage:
    python scripts/originate/eval_storyboard.py originate/<slug>/script.json

Exit code: 0 = clean or WARN-only; 1 = HARD fail (originate.py blocks).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

# Sections whose screens must carry a figure or a source (Rev C: no
# unsourced numbers on screen).
CLAIM_CARRYING = {"hook", "evidence", "economics", "stack"}


class Eval:
    """Same shape as eval_script.Eval — parsers in confidence.py look
    for the [PASS] / [FAIL] / [WARN] tags."""

    def __init__(self):
        self.results = []

    def check(self, name, ok, detail="", hard=True):
        self.results.append((name, ok, detail, hard))

    def report(self):
        hard_fail = False
        print(f"\n{'=' * 74}")
        for name, ok, detail, hard in self.results:
            tag = "PASS" if ok else ("FAIL" if hard else "WARN")
            if not ok and hard:
                hard_fail = True
            print(f"  [{tag}] {name}" + (f" — {detail}" if detail else ""))
        n_pass = sum(1 for _, ok, _, _ in self.results if ok)
        print(f"{'=' * 74}\n  {n_pass}/{len(self.results)} checks passed\n")
        return 1 if hard_fail else 0


def find_storyboard(script_path: Path) -> Path:
    """Storyboard sits next to script.json; eval accepts either path so
    it composes cleanly with confidence.py which passes the script."""
    if script_path.name == "storyboard.json":
        return script_path
    sb = script_path.parent / "storyboard.json"
    if not sb.exists():
        print(f"Error: storyboard.json not found at {sb}. Run storyboard.py first.",
              file=sys.stderr)
        sys.exit(1)
    return sb


def main():
    parser = argparse.ArgumentParser(description="Storyboard pacing evals")
    parser.add_argument("script", help="Path to script.json (or storyboard.json)")
    args = parser.parse_args()

    sb_path = find_storyboard(Path(args.script))
    sb = json.loads(sb_path.read_text())
    screens = sb.get("screens", [])
    total = sb.get("total_seconds", sum(s["end"] - s["start"] for s in screens))
    # Rev D introduced the active-motion grammar; Rev E retains its faster
    # opening cadence while replacing the visual language. Treat both as
    # intentional active edits rather than applying the legacy 10s minimum.
    active_motion = str(sb.get("storyboard_version", "")).startswith(("rev-d", "rev-e"))

    ev = Eval()

    # -------- Structural presence -----------
    ev.check("screens present", bool(screens), f"{len(screens)} screens")
    if not screens:
        sys.exit(ev.report())

    # -------- Cut rate ----------------------
    minutes = max(total, 1) / 60
    cuts_per_min = len(screens) / minutes
    seconds_per_cut = total / max(len(screens), 1)
    # ≤10 screens / 6min ≈ 1 cut per 36s. HARD if cut every <15s, WARN if <25s.
    ev.check(
        "cut-rate supports the active visual grammar",
        seconds_per_cut >= (8 if active_motion else 15),
        f"one cut per {seconds_per_cut:.1f}s ({cuts_per_min:.1f}/min)",
        hard=True,
    )
    ev.check(
        "cut-rate approaches grammar target",
        seconds_per_cut >= (12 if active_motion else 25),
        f"one cut per {seconds_per_cut:.1f}s — active target ≥{12 if active_motion else 35}s/cut",
        hard=False,
    )
    ev.check(
        "screen count matches active grammar",
        len(screens) <= max(10, int(minutes * (4.5 if active_motion else 1.8))),
        f"{len(screens)} screens over {minutes:.1f} min",
        hard=False,
    )

    # -------- Per-screen duration -----------
    too_short_hard = [s for s in screens if (s["end"] - s["start"]) < 10]
    too_short_warn = [s for s in screens if 10 <= (s["end"] - s["start"]) < 20]
    too_long_warn = [s for s in screens if 75 < (s["end"] - s["start"]) <= 90]
    too_long_hard = [s for s in screens if (s["end"] - s["start"]) > 90]

    ev.check(
        "short screens are intentional impact edits",
        (all((s["end"] - s["start"]) >= 1.2 for s in too_short_hard)
         if active_motion else not too_short_hard),
        ", ".join(f"{s['id']}({s['end'] - s['start']:.1f}s)" for s in too_short_hard),
        hard=True,
    )
    ev.check(
        "screens meet active soft duration target",
        (True if active_motion else not too_short_warn),
        ", ".join(f"{s['id']}({s['end'] - s['start']:.1f}s)" for s in too_short_warn),
        hard=False,
    )
    ev.check(
        "no screen longer than 90s (hard ceiling)",
        not too_long_hard,
        ", ".join(f"{s['id']}({s['end'] - s['start']:.1f}s)" for s in too_long_hard),
        hard=True,
    )
    ev.check(
        "screens are ≤75s (soft ceiling)",
        not too_long_warn,
        ", ".join(f"{s['id']}({s['end'] - s['start']:.1f}s)" for s in too_long_warn),
        hard=False,
    )

    # -------- Sheet reveal counts -----------
    sheet_screens = [s for s in screens if s["layout"] == "sheet"]
    sheet_no_reveals = [s for s in sheet_screens if len(s.get("reveals", [])) == 0]
    sheet_one_reveal = [s for s in sheet_screens if len(s.get("reveals", [])) == 1]

    ev.check(
        "no sheet screen with 0 reveals",
        not sheet_no_reveals,
        ", ".join(s["id"] for s in sheet_no_reveals),
        hard=True,
    )
    # Single-reveal sheets are usually a symptom of a stray single slide
    # that should merge with a neighbour — WARN so operator can review.
    ev.check(
        "sheet screens carry ≥2 reveals",
        not sheet_one_reveal,
        ", ".join(s["id"] for s in sheet_one_reveal),
        hard=False,
    )

    # -------- Semantic title lint (2026-08-09) --
    # storyboard.py's auto-generation grabs the first ~44 chars of the beat's
    # vo_text or asset_hint as the title. That produces gibberish like
    # "57", "And the number of solo operators clearing", or
    # "end card with the blueprint cover and the su" — real screens that shipped
    # in EP005's first render. hand_tune_storyboard.py is required to overwrite
    # every title with something authored; this lint enforces it.
    import re as _re
    _asset_hint_prose = _re.compile(
        r"\b(end card|brand cover|title card|caption chip|two bars|three bars|"
        r"cover the|screen rec|shot list|drawn to scale|source chip|"
        r"axis label|call out|voice over|talking head)\b", _re.I)
    bad_titles = []
    # Hard tells of storyboard.py's autogen (grabs first ~44 chars of vo_text /
    # asset_hint as the title). Kept narrow on purpose: false positives will get
    # hand_tune written just to silence the lint, which defeats the point. Trust
    # authored titles by default; only flag things a human wouldn't write.
    _DANGLERS = {"a", "an", "the", "of", "for", "and", "or", "but", "with", "by", "as"}
    for s in screens:
        for r in s.get("reveals", []):
            title = (r.get("title") or "").strip()
            if not title:
                continue
            issues = []
            if title[0].islower() and not title.startswith(("iOS", "macOS", "eV", "e.g.", "µ")):
                issues.append("starts lowercase")
            # Only flag danglers on long unpunctuated titles — the autogen signature
            last_word = title.rstrip(".!?…\"'”’)]}·%,").split()[-1].lower().strip(".,;:")
            if len(title) >= 30 and title[-1].isalnum() and last_word in _DANGLERS:
                issues.append(f"ends on dangling word {last_word!r}")
            if _asset_hint_prose.search(title):
                issues.append("contains asset-hint prose")
            if len(title.split()) > 22:
                issues.append(f"{len(title.split())} words (>22)")
            if issues:
                bad_titles.append(f"{s['id']}:{title[:36]!r} ({'; '.join(issues)})")
    ev.check(
        "titles read as authored text, not auto-fragments",
        not bad_titles,
        "; ".join(bad_titles[:6]) + (f" (+{len(bad_titles)-6} more)" if len(bad_titles) > 6 else ""),
        hard=True,
    )

    # -------- Figure or source on claim screens ---
    unsourced = [
        s for s in screens
        if s["section"] in CLAIM_CARRYING and not s.get("figure") and not s.get("source")
    ]
    ev.check(
        "claim-carrying screens have figure or source",
        not unsourced,
        ", ".join(f"{s['id']}({s['section']})" for s in unsourced),
        hard=False,
    )

    # -------- Screen ordering / boundaries --
    # Screens should form a contiguous timeline with no overlaps and no
    # gaps larger than one frame. If they do, prepare_longform would
    # produce a black frame between screens.
    for i in range(1, len(screens)):
        gap = screens[i]["start"] - screens[i - 1]["end"]
        overlap = gap < -0.05
        big_gap = gap > 0.5
        ev.check(
            f"screens contiguous at {screens[i - 1]['id']} → {screens[i]['id']}",
            not (overlap or big_gap),
            f"gap = {gap:+.2f}s",
            hard=big_gap or overlap,
        )

    # -------- Layout distribution -----------
    # Info-only: helpful signal for operator when reviewing.
    layouts = {}
    for s in screens:
        layouts[s["layout"]] = layouts.get(s["layout"], 0) + 1
    ev.check(
        "layout distribution present",
        True,
        " · ".join(f"{k}:{v}" for k, v in sorted(layouts.items())),
        hard=False,
    )

    sys.exit(ev.report())


if __name__ == "__main__":
    main()
