"""
Gate 1 eval: deterministic quality checks on a generated script.json.

Two modes:
  --mode draft     (default) fresh AI output — POV tokens EXPECTED (>=2)
  --mode approved  post-human-pass — POV tokens must be ZERO

Exit code 0 = all hard checks pass; 1 = failures (originate.py blocks on this).

Usage:
    python scripts/originate/eval_script.py originate/<slug>/script.json [--mode draft|approved]
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

WORDS_PER_SECOND = 2.5  # ~150 wpm VO pace
DURATION_TOLERANCE = 0.35

HYPE_WORDS = [
    "insane", "crazy", "secret", "game-changer", "game changing", "mind-blowing",
    "guaranteed", "get rich", "passive income machine", "life-changing",
    "hack the", "exploded", "skyrocket", "unbelievable", "you won't believe",
]

PROMISE_PATTERNS = [
    r"you (?:will|'ll) (?:make|earn)\s+\$?\d",
    r"guarantee[ds]?\b.{0,30}\$",
    r"easy money",
]

REQUIRED_TOP_KEYS = ["topic", "working_title", "title_options", "thumbnail_concepts",
                     "description_draft", "sections", "sources", "blueprint_summary"]
REQUIRED_SUMMARY_KEYS = ["idea", "who_its_for", "evidence_companies", "tool_stack",
                         "first_customer_plan", "realistic_economics"]

MONEY_RE = re.compile(
    r"\$\s?\d|\b(?:\w+\s)?(?:thousand|million|billion)\b|\b\d[\d,.]*\s?(?:dollars|percent margins?)",
    re.IGNORECASE)


class Eval:
    def __init__(self):
        self.results = []

    def check(self, name, ok, detail="", hard=True):
        self.results.append((name, ok, detail, hard))

    def report(self):
        hard_fail = False
        print(f"\n{'='*74}")
        for name, ok, detail, hard in self.results:
            tag = "PASS" if ok else ("FAIL" if hard else "WARN")
            if not ok and hard:
                hard_fail = True
            print(f"  [{tag}] {name}" + (f" — {detail}" if detail else ""))
        n_pass = sum(1 for _, ok, _, _ in self.results if ok)
        print(f"{'='*74}\n  {n_pass}/{len(self.results)} checks passed\n")
        return 1 if hard_fail else 0


def beat_text(script):
    for s in script["sections"]:
        for b in s.get("beats", []):
            yield s["id"], b


def main():
    parser = argparse.ArgumentParser(description="Gate 1 script evals")
    parser.add_argument("script")
    parser.add_argument("--mode", choices=["draft", "approved"], default="draft")
    parser.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    args = parser.parse_args()

    with open(args.script) as f:
        script = json.load(f)
    with open(args.config) as f:
        config = json.load(f)

    ev = Eval()

    # 1. Schema
    missing = [k for k in REQUIRED_TOP_KEYS if k not in script]
    ev.check("schema: required top-level keys", not missing, f"missing: {missing}")
    ms = [k for k in REQUIRED_SUMMARY_KEYS if k not in script.get("blueprint_summary", {})]
    ev.check("schema: blueprint_summary complete", not ms, f"missing: {ms}")

    # 2. Section coverage + order vs config
    want = [s["id"] for s in config["format"]["sections"]]
    got = [s["id"] for s in script.get("sections", [])]
    ev.check("format: sections match config order", got == want, f"want {want}, got {got}")

    # 3. Duration fit per section (word count vs target_seconds)
    targets = {s["id"]: s["target_seconds"] for s in config["format"]["sections"]}
    for s in script.get("sections", []):
        words = sum(len(b["vo_text"].split()) for b in s.get("beats", []))
        tgt = targets.get(s["id"], 0) * WORDS_PER_SECOND
        if not tgt:
            continue
        ratio = words / tgt
        ok = (1 - DURATION_TOLERANCE) <= ratio <= (1 + DURATION_TOLERANCE)
        ev.check(f"duration: '{s['id']}' within ±35% of target",
                 ok, f"{words} words vs ~{tgt:.0f} target ({ratio:.0%})", hard=False)

    # 4. Hook: concrete tension in first two sentences (number OR question OR
    # quote OR contrast pivot — any approved archetype qualifies; forcing
    # numbers-only produces formulaic hooks, which is itself a slop signal)
    hook = next((s for s in script["sections"] if s["id"] == "hook"), None)
    if hook and hook.get("beats"):
        # Beat 0 is the series open ("Welcome in. This is The Operator
        # Economy...") — fixed brand furniture added 2026-07-05 (EP001),
        # not hook content. Hook checks run on beats >= 1.
        hook_text = " ".join(b["vo_text"] for b in hook["beats"] if b.get("beat", 1) != 0)
        first_two = " ".join(re.split(r"(?<=[.!?])\s+", hook_text)[:2])
        low2 = first_two.lower()
        signals = []
        if MONEY_RE.search(first_two) or re.search(r"\d", first_two):
            signals.append("number")
        if "?" in first_two:
            signals.append("question")
        if re.search(r"[\"“”']{1}[^\"“”']{8,}[\"“”']{1}", first_two):
            signals.append("quote")
        if any(w in low2 for w in [" but ", " yet ", "however", "instead", "not because", "isn't ", "is not "]):
            signals.append("contrast")
        ev.check("hook: concrete tension in first two sentences (number/question/quote/contrast)",
                 bool(signals), f"signals: {signals or 'NONE'} — {first_two[:70]}")
        ev.check("hook: contains a number somewhere (evidence-first house style)",
                 bool(MONEY_RE.search(hook_text) or re.search(r"\d", hook_text)),
                 "", hard=False)
        ev.check("hook: <= 60 words", len(hook_text.split()) <= 60,
                 f"{len(hook_text.split())} words", hard=False)

    # 5. POV tokens
    raw = json.dumps(script)
    pov_count = raw.count("[POV:")
    if args.mode == "draft":
        ev.check("POV: >=2 insertion points marked for the human pass", pov_count >= 2,
                 f"found {pov_count}")
    else:
        ev.check("POV: zero tokens remain (Gate 1 complete)", pov_count == 0,
                 f"found {pov_count}")

    # 6. Hype lexicon + income promises
    low = raw.lower()
    found_hype = [w for w in HYPE_WORDS if w in low]
    ev.check("tone: no hype lexicon", not found_hype, f"found: {found_hype}")
    promises = [p for p in PROMISE_PATTERNS if re.search(p, low)]
    ev.check("compliance: no income-promise patterns", not promises, f"matched: {promises}")

    # 7. Source coverage on money claims
    unsourced = []
    for sid, b in beat_text(script):
        if MONEY_RE.search(b["vo_text"]):
            src = (b.get("source") or "").lower()
            if not src:
                unsourced.append(f"{sid}#{b['beat']}")
    ev.check("rigor: every money-claim beat has a source or estimate marker",
             not unsourced, f"unsourced: {unsourced}")

    # 8. Unverified claims flagged in-text (reported/estimate language near weak sources)
    weak_unflagged = []
    for sid, b in beat_text(script):
        src = (b.get("source") or "").lower()
        if "public pricing" in src:  # benign tool-pricing claims don't need spoken hedging
            continue
        if any(w in src for w in ["unverified", "reported", "estimate", "directional", "anecdote"]):
            vo = b["vo_text"].lower()
            if not any(w in vo for w in ["reported", "estimate", "careful", "unverified",
                                          "directionally", "not audited", "flagging",
                                          "marketing artifact", "converge"]):
                weak_unflagged.append(f"{sid}#{b['beat']}")
    ev.check("rigor: weak sources hedged in the spoken text", not weak_unflagged,
             f"unhedged: {weak_unflagged}", hard=False)

    # 9. Highlights: 2-4 per beat, present in vo_text
    bad_hl = []
    for sid, b in beat_text(script):
        hl = b.get("highlight_words", [])
        if not (2 <= len(hl) <= 4) or any(h.lower() not in b["vo_text"].lower() for h in hl):
            bad_hl.append(f"{sid}#{b['beat']}")
    ev.check("captions: 2-4 highlight words per beat, all present in vo_text",
             not bad_hl, f"bad: {bad_hl}")

    # 10. Titles
    titles = script.get("title_options", [])
    ev.check("packaging: 3 title options", len(titles) == 3, f"got {len(titles)}")
    ev.check("packaging: >=1 title contains a number",
             any(re.search(r"\d", t) for t in titles), hard=False)

    # 11. Evidence balance: low end AND high end present (thesis format requirement)
    ev_section = next((s for s in script["sections"] if s["id"] == "evidence"), None)
    if ev_section:
        txt = " ".join(b["vo_text"].lower() for b in ev_section["beats"])
        has_high = "billion" in txt or "enterprise" in txt
        has_low = any(w in txt for w in ["solo", "freelancer", "one person", "small"])
        ev.check("thesis format: evidence spans low end AND high end",
                 has_high and has_low, f"high={has_high}, low={has_low}")

    sys.exit(ev.report())


if __name__ == "__main__":
    main()
