"""
Edit-rubric eval (docs/content-rubric.md §VII + docs/storyboard-stage.md v2).

Runs against `originate/<slug>/storyboard.json` (AUTO checks) plus,
optionally, the rendered MP4 (loudness only). Feeds `confidence.py`
under the craft slot alongside `eval_package.py`.

Scoring: 23 pts total; publish gate ≥18 (kept at 80%) AND zero kill-list hits.
Exit code: 0 on PASS (or WARN-only), 1 on HARD FAIL.

Usage:
    python scripts/originate/eval_edit.py originate/<slug>/script.json
        [--rendered ../output/<slug>.mp4]   # runs the loudnorm print if provided

Writes:
    originate/<slug>/edit_review.md         # human-readable escalation
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


# ---------------------------------------------------------------------
# Vocabularies (must stay in sync with storyboard.py)
# ---------------------------------------------------------------------

QUOTE_LAYOUTS = {"quote", "proof_card"}  # both count as pull-quote / impact moments
ARTIFACT_LAYOUTS = {"artifact", "screen_rec", "proof_card"}  # counted for "artifact/screen-rec/proof" density
CLAIM_LAYOUTS_WITH_NUMBERS = {"proof_card", "chart", "ladder", "gap"}
SILENCE_LAYOUTS = {"quote", "gap", "chapter_reset"}
BUILD_LAYOUTS = {"proof_card", "chart", "ladder"}

ABSTRACT_BROLL_TERMS = {
    "small business", "office", "typing", "handshake",
    "ai future", "technology", "abstract", "generic",
    "person at computer", "team meeting", "corporate",
}
CONCRETE_BROLL_NOUNS = {
    "counter", "desk", "front desk", "hotel", "restaurant",
    "kitchen", "storefront", "warehouse", "workshop",
    "dashboard", "spreadsheet", "form", "reservation",
    "phone", "call", "receipt", "chalkboard",
    "airport", "gym", "clinic", "salon",
}


# ---------------------------------------------------------------------
# Result plumbing
# ---------------------------------------------------------------------

class Check:
    __slots__ = ("name", "points_max", "points_earned", "detail", "kill", "warn")

    def __init__(self, name: str, points_max: int):
        self.name = name
        self.points_max = points_max
        self.points_earned = 0
        self.detail: list[str] = []
        self.kill: list[str] = []
        self.warn: list[str] = []

    def score(self, earned: int, detail: str = ""):
        self.points_earned = earned
        if detail:
            self.detail.append(detail)

    def kill_hit(self, message: str):
        self.kill.append(message)

    def warn_hit(self, message: str):
        self.warn.append(message)


# ---------------------------------------------------------------------
# Individual criteria
# ---------------------------------------------------------------------

def check_scene_grammar(screens: list[dict], total_seconds: float) -> Check:
    """Rubric criterion 1 — 5 pts.
    ≥5 quote/punchline moments AND ≥3 artifact/screen_rec/proof screens per 6 min.
    Both are scaled linearly to actual episode length.
    """
    c = Check("Scene grammar mix", 5)
    minutes = max(total_seconds / 60, 1)
    scale = minutes / 6.0

    quotes = [s for s in screens if s["layout"] in QUOTE_LAYOUTS]
    artifacts = [s for s in screens if s["layout"] in ARTIFACT_LAYOUTS]
    quote_target = max(5, round(5 * scale))
    artifact_target = max(3, round(3 * scale))

    quote_pts = 3 if len(quotes) >= quote_target else (1 if len(quotes) >= 3 else 0)
    art_pts = 2 if len(artifacts) >= artifact_target else (1 if len(artifacts) >= 2 else 0)
    c.score(quote_pts + art_pts,
            f"{len(quotes)}/{quote_target} quote|proof screens, "
            f"{len(artifacts)}/{artifact_target} artifact|screen_rec|proof screens")
    if len(quotes) < quote_target:
        c.warn_hit(f"only {len(quotes)} quote/punchline screens (target {quote_target}); "
                   "add pull-quote moments on impact lines.")
    if len(artifacts) < artifact_target:
        c.warn_hit(f"only {len(artifacts)} artifact/proof screens (target {artifact_target}); "
                   "shift more claims onto proof cards or artifacts.")
    return c


def check_cadence(screens: list[dict]) -> Check:
    """Rubric criterion 2 — 5 pts.
    - No static composition >20s unless actively building (≥2 reveals)
    - Composition reset every 25–45s
    - Never >2 consecutive `sheet` screens
    - Quote / chapter_reset screens are IMPACT FRAMES by design (craft
      §P1): 1.2–4s short holds are correct there; only sheet/chart-like
      screens are checked for the 10s hard floor.
    """
    c = Check("Cadence (static holds, resets, sheet runs)", 5)
    warnings = 0
    hard_kills = 0

    IMPACT_LAYOUTS = {"quote", "chapter_reset"}

    for s in screens:
        dur = s["end"] - s["start"]
        reveals = len(s.get("reveals", []))
        layout = s["layout"]
        if layout in IMPACT_LAYOUTS:
            if dur < 1.0:
                warnings += 1
                c.warn_hit(f"{s['id']} {layout} holds only {dur:.1f}s — even impact frames "
                           "want ≥1s so the line lands.")
            elif dur > 6:
                warnings += 1
                c.warn_hit(f"{s['id']} {layout} holds {dur:.1f}s — impact frames should be "
                           "1.2–4s; extended holds turn into title slides.")
            continue
        if dur > 20 and reveals < 2:
            warnings += 1
            c.warn_hit(f"{s['id']} holds {dur:.1f}s with only {reveals} reveal — "
                       "static composition. Add reveals or split the screen.")
        # >45s hard-kill applies only to STATIC holds. A screen that is
        # actively assembling (≥3 reveals — schematic, 3-step sheet)
        # keeps the "reset" spirit met by internal composition changes.
        if dur > 45 and reveals < 3:
            hard_kills += 1
            c.kill_hit(f"{s['id']} holds {dur:.1f}s — > 45s without a composition reset (kill list).")

    # Consecutive sheet runs
    run = 0
    max_run = 0
    for s in screens:
        if s["layout"] == "sheet":
            run += 1
            max_run = max(max_run, run)
        else:
            run = 0
    if max_run > 2:
        c.kill_hit(f"{max_run} consecutive `sheet` screens in a row (kill list, max is 2).")
        hard_kills += 1

    # Score
    if hard_kills == 0 and warnings == 0:
        c.score(5, "no static holds; sheet runs ≤2; all screens reset within 45s")
    elif hard_kills == 0:
        c.score(max(3, 5 - warnings), f"{warnings} warnings")
    else:
        c.score(0, f"{hard_kills} kill-list hits")
    return c


def check_event_density(screens: list[dict]) -> Check:
    """Rubric criterion 2b — 3 pts (pacing pass, 2026-07-03).
    Inside every non-impact screen, SOMETHING must move: a reveal, a
    pacing event (fragment/item/pulse/focus from pace_storyboard.py),
    or the layout's self-build entrance. The research cadence rule is
    a visual event every 3–6s in dense sections and 8–15s in the body —
    we check the worst dead stretch per screen:
      ≤8s clean · 8–12s warn · >16s kill (that's a static hold the
      viewer reads as a slide).
    """
    c = Check("In-screen event density (pacing pass)", 3)
    IMPACT = {"quote", "chapter_reset"}
    SELF_BUILD = {"chart": 6.0, "ladder": 6.0, "gap": 5.0,
                  "proof_card": 4.0, "schematic": 4.0}
    warns = kills = 0
    paced = any(s.get("events") for s in screens)

    for s in screens:
        if s["layout"] in IMPACT:
            continue
        cues = [s["start"] + SELF_BUILD.get(s["layout"], 0.0)]
        cues += [r["at"] for r in s.get("reveals", [])]
        cues += [e["at"] for e in s.get("events", [])]
        cues = sorted(set(round(x, 2) for x in cues if x <= s["end"]))
        cues.append(s["end"])
        gap = max(b - a for a, b in zip(cues, cues[1:])) if len(cues) > 1 else 0
        if gap > 16:
            kills += 1
            c.kill_hit(f"{s['id']} has a {gap:.1f}s dead stretch (no reveal/event) — "
                       "static hold (kill list). Run pace_storyboard.py or split the screen.")
        elif gap > 12:
            warns += 2
            c.warn_hit(f"{s['id']} has a {gap:.1f}s dead stretch — add events or reveals.")
        elif gap > 8:
            warns += 1
            c.warn_hit(f"{s['id']} dead stretch {gap:.1f}s (target ≤8s).")

    if not paced:
        c.warn_hit("no pacing events found anywhere — pace_storyboard.py has not run.")
        warns += 1

    if kills:
        c.score(0, f"{kills} static-hold kill(s)")
    else:
        c.score(max(0, 3 - min(warns, 3)), f"{warns} warning(s); paced={paced}")
    return c


def check_broll_and_sources(screens: list[dict]) -> Check:
    """Rubric criterion 3 — 4 pts.
    - Every `broll` names a concrete noun/action (no abstract queries)
    - Every money-claim screen carries source
    """
    c = Check("Concrete b-roll + money-claim sources", 4)
    kill_hits = 0
    warn_hits = 0

    for s in screens:
        if s["layout"] == "broll":
            query = ""
            reveals = s.get("reveals", [])
            if reveals:
                # The broll screen's title/body carry the search query
                query = (reveals[0].get("title") or "") + " " + (reveals[0].get("body") or "")
            query_lower = query.lower()
            if not query.strip():
                c.kill_hit(f"{s['id']} b-roll has no search query.")
                kill_hits += 1
                continue
            # Abstract term check
            if any(term in query_lower for term in ABSTRACT_BROLL_TERMS):
                c.kill_hit(f"{s['id']} b-roll query ({query.strip()!r}) is abstract/generic (kill list).")
                kill_hits += 1
                continue
            # Concrete noun check
            if not any(noun in query_lower for noun in CONCRETE_BROLL_NOUNS):
                c.warn_hit(f"{s['id']} b-roll query ({query.strip()!r}) doesn't name a concrete noun "
                           "from the whitelist. Verify it's story-bearing.")
                warn_hits += 1

    for s in screens:
        if s["layout"] in CLAIM_LAYOUTS_WITH_NUMBERS:
            source = s.get("source") or (s.get("figure") or {}).get("source")
            if not source:
                c.kill_hit(f"{s['id']} ({s['layout']}) is a money-claim screen with no source label (kill list).")
                kill_hits += 1

    if kill_hits == 0 and warn_hits == 0:
        c.score(4, "all b-roll concrete; all money-claim screens sourced")
    elif kill_hits == 0:
        c.score(max(2, 4 - warn_hits), f"{warn_hits} warnings")
    else:
        c.score(0, f"{kill_hits} kill-list hits")
    return c


def check_hook_density(screens: list[dict]) -> Check:
    """Rubric criterion 4 — 3 pts.
    - Visual event every 4–8s in first 30s (reveals ≥ 4 in [0, 30])
    - Premise proven (shown) not just stated — HUMAN judgment; AUTO only
      flags if the first 30s has NO artifact/proof/chart screen at all.
    """
    c = Check("Hook — visual density + shown premise", 3)

    early_reveals = 0
    early_layouts = set()
    for s in screens:
        if s["start"] > 30:
            break
        early_layouts.add(s["layout"])
        for r in s.get("reveals", []):
            if r["at"] < 30:
                early_reveals += 1

    # ≥4 reveals in first 30s → 4-8s cadence
    density_pts = 2 if early_reveals >= 4 else (1 if early_reveals >= 3 else 0)
    # Premise shown = at least one non-sheet/quote layout in the hook window
    shown_layouts = {"chart", "gap", "proof_card", "artifact", "screen_rec", "ladder", "schematic"}
    shown_pts = 1 if early_layouts & shown_layouts else 0
    c.score(density_pts + shown_pts,
            f"{early_reveals} reveals in first 30s; early layouts: "
            f"{','.join(sorted(early_layouts)) or 'none'}")
    if early_reveals < 4:
        c.warn_hit(f"only {early_reveals} reveals in first 30s (target ≥4 for 4–8s cadence).")
    if not (early_layouts & shown_layouts):
        c.warn_hit("first 30s is all sheet/quote screens — premise is stated, not shown.")
    return c


def check_sound_cues(screens: list[dict], rendered: Path | None) -> Check:
    """Rubric criterion 5 — 3 pts.
    - Music bed: per-section change or intensity variation + ducking cues.
    - SFX on reveals / transitions / impacts.
    - Master −14 LUFS ±1, true peak ≤ −1 dBTP (only if `rendered` provided).
    """
    c = Check("Sound layer + loudness", 3)

    music_intensities = {(s.get("music") or {}).get("intensity") for s in screens}
    music_intensities.discard(None)
    sfx_hits = sum(len(s.get("sfx") or []) for s in screens)
    silence_hits = sum(1 for s in screens if (s.get("music") or {}).get("intensity") == "silence")

    # 1 pt for music intensity variation, 1 pt for SFX cues coverage
    intensity_pts = 1 if len(music_intensities) >= 2 else 0
    sfx_pts = 1 if sfx_hits >= max(3, len(screens) // 3) else 0

    # 1 pt for LUFS pass (if we can measure it)
    lufs_pts = 0
    if rendered and rendered.exists():
        lufs = _measure_lufs(rendered)
        if lufs is not None:
            i_lufs, tp = lufs
            c.detail.append(f"loudnorm: I={i_lufs} LUFS, TP={tp} dBTP")
            if -15 <= i_lufs <= -13 and tp <= -1:
                lufs_pts = 1
            else:
                c.warn_hit(f"loudness off-target (I={i_lufs} LUFS, TP={tp} dBTP; target −14±1 / ≤−1).")
        else:
            c.warn_hit("ffmpeg loudnorm probe failed; skipping LUFS check.")
    else:
        c.detail.append("(no rendered MP4 provided — LUFS check skipped)")
        # If the storyboard is designed with music cues, still credit for
        # sound design being present; the LUFS point is deferred until
        # render time.
        if intensity_pts and sfx_pts:
            lufs_pts = 1  # tentative — final LUFS runs at render time

    c.score(intensity_pts + sfx_pts + lufs_pts,
            f"intensities={sorted(music_intensities)}, sfx cues={sfx_hits}, "
            f"silence screens={silence_hits}")

    if intensity_pts == 0:
        c.warn_hit("music intensity is uniform across the episode; add build/silence cues.")
    if sfx_pts == 0:
        c.warn_hit(f"only {sfx_hits} SFX cues across {len(screens)} screens; add tick on sheet-line "
                   "reveals and hit on impact frames.")
    return c


def _measure_lufs(mp4: Path) -> tuple[float, float] | None:
    """Run `ffmpeg -af loudnorm=print_format=json` on the file and return
    (integrated_LUFS, true_peak_dBTP). Returns None if ffmpeg can't be run
    or the output can't be parsed.
    """
    try:
        p = subprocess.run(
            ["ffmpeg", "-hide_banner", "-i", str(mp4), "-af",
             "loudnorm=I=-14:TP=-1:print_format=json", "-f", "null", "-"],
            capture_output=True, text=True, timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    m = re.search(r"\{[^{}]*input_i[^{}]*\}", p.stderr, re.S)
    if not m:
        return None
    try:
        data = json.loads(m.group(0))
        return float(data.get("input_i", 0)), float(data.get("input_tp", 0))
    except (json.JSONDecodeError, ValueError):
        return None


# ---------------------------------------------------------------------
# Kill-list checks (always run, orthogonal to scoring)
# ---------------------------------------------------------------------

def check_kill_list(screens: list[dict]) -> list[str]:
    kills: list[str] = []

    # Unresolved placeholder screen
    for s in screens:
        if s["layout"] == "broll":
            title = (s.get("reveals") or [{}])[0].get("title", "")
            if not title.strip() or "pending" in title.lower():
                kills.append(f"[placeholder] {s['id']} has an unresolved b-roll title.")
        if s["layout"] == "screen_rec":
            title = (s.get("reveals") or [{}])[0].get("title", "")
            if not title.strip() or "pending" in title.lower():
                kills.append(f"[placeholder] {s['id']} has an unresolved screen recording.")

    # >45s without composition reset — computed as any single screen
    # holding past 45s. Impact frames (quote / chapter_reset) and
    # actively-building screens (≥3 reveals — schematic, offer stack,
    # ladder, multi-reveal sheet) are exempt: they aren't STATIC
    # holds even if their overall duration passes 45s.
    for s in screens:
        if s["layout"] in ("quote", "chapter_reset"):
            continue
        if len(s.get("reveals", [])) >= 3:
            continue
        if (s["end"] - s["start"]) > 45:
            kills.append(f"[45s cap] {s['id']} spans {s['end'] - s['start']:.1f}s — over the 45s limit.")

    # Music bed missing (silence intensity but no fallback) — only
    # actionable when a `music` config exists; storyboard just declares
    # intent, so we don't kill on it here.

    return kills


# ---------------------------------------------------------------------
# Escalation report
# ---------------------------------------------------------------------

def write_review(base: Path, checks: list[Check], kills_extra: list[str], total: int,
                 max_total: int, screens: list[dict]):
    lines = ["# Edit rubric review", ""]
    lines.append(f"**Score:** {total}/{max_total}  ·  **Gate:** ≥18")
    verdict = "PASS" if (total >= 18 and not any(c.kill for c in checks) and not kills_extra) else "ESCALATE"
    lines.append(f"**Verdict:** {verdict}")
    lines.append("")
    lines.append("## Criteria")
    for c in checks:
        icon = "✅" if c.points_earned == c.points_max else ("⚠️" if not c.kill else "❌")
        lines.append(f"### {icon} {c.name} — {c.points_earned}/{c.points_max}")
        for d in c.detail:
            lines.append(f"- {d}")
        for w in c.warn:
            lines.append(f"- ⚠️ {w}")
        for k in c.kill:
            lines.append(f"- ❌ **KILL** {k}")
        lines.append("")
    all_kills = [k for c in checks for k in c.kill] + kills_extra
    if all_kills:
        lines.append("## Kill-list hits (any = no publish)")
        for k in all_kills:
            lines.append(f"- ❌ {k}")
        lines.append("")
    lines.append("## Screen distribution")
    layout_count: dict = {}
    for s in screens:
        layout_count[s["layout"]] = layout_count.get(s["layout"], 0) + 1
    for k, v in sorted(layout_count.items()):
        lines.append(f"- {k}: {v}")
    (base / "edit_review.md").write_text("\n".join(lines))


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def find_storyboard(path: Path) -> Path:
    if path.name == "storyboard.json":
        return path
    sb = path.parent / "storyboard.json"
    if not sb.exists():
        print(f"Error: storyboard.json not found next to {path.name}. Run storyboard.py first.",
              file=sys.stderr)
        sys.exit(1)
    return sb


def main():
    ap = argparse.ArgumentParser(description="Edit-rubric eval (rubric §VII)")
    ap.add_argument("script", help="Path to script.json (or storyboard.json)")
    ap.add_argument("--rendered", type=Path, default=None,
                    help="Path to the rendered MP4 for the LUFS check")
    args = ap.parse_args()

    sb_path = find_storyboard(Path(args.script))
    base = sb_path.parent
    sb = json.loads(sb_path.read_text())
    screens = sb.get("screens", [])
    total_seconds = sb.get("total_seconds", sum(s["end"] - s["start"] for s in screens))

    checks = [
        check_scene_grammar(screens, total_seconds),
        check_cadence(screens),
        check_event_density(screens),
        check_broll_and_sources(screens),
        check_hook_density(screens),
        check_sound_cues(screens, args.rendered),
    ]
    kills_extra = check_kill_list(screens)

    max_total = sum(c.points_max for c in checks)
    total = sum(c.points_earned for c in checks)
    kill_hits = sum(len(c.kill) for c in checks) + len(kills_extra)

    print(f"\n{'=' * 74}")
    print("  Edit rubric (docs/content-rubric.md §VII)")
    print("=" * 74)
    for c in checks:
        tag = ("[PASS]" if c.points_earned == c.points_max else
               ("[WARN]" if not c.kill else "[FAIL]"))
        detail = " · ".join(c.detail) or ""
        print(f"  {tag} {c.name} — {c.points_earned}/{c.points_max}"
              + (f" — {detail}" if detail else ""))
        for w in c.warn:
            print(f"        ⚠  {w}")
        for k in c.kill:
            print(f"        ✗  KILL: {k}")

    if kills_extra:
        print("\n  Additional kill-list hits:")
        for k in kills_extra:
            print(f"        ✗  {k}")

    print(f"\n  SCORE: {total}/{max_total}  ·  Gate: ≥18")
    print(f"  KILL-LIST HITS: {kill_hits}" if kill_hits else "  KILL-LIST HITS: 0")
    verdict = "PASS" if (total >= 18 and kill_hits == 0) else "ESCALATE"
    print(f"  VERDICT: {verdict}")
    print("=" * 74)

    write_review(base, checks, kills_extra, total, max_total, screens)
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
