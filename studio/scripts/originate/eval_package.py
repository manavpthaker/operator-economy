"""
Craft evals (content rubric, docs/content-rubric.md): the AUTO-checkable
subset of the 100-point pre-publish rubric, scored from script.json alone.

47 of 100 points are automatable pre-publish; the rest are human judgment
(listed at the end of the report). Kill-list hits are hard failures.

Usage:
    python scripts/originate/eval_package.py originate/<slug>/script.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

BANNED_OPENERS = ["hey", "welcome", "today we", "today i", "in this video",
                  "what's up", "hello everyone", "before we start"]
WRAPUP_PHRASES = ["in conclusion", "thank you for watching", "thanks for watching",
                  "to wrap up", "that's all for", "so that's how", "and that is how"]
KILL_PHRASES = ["you won't believe", "shocking truth", "will blow your mind",
                "get rich", "guaranteed income"]
TITLE_SLOP = ["unlocking", "revolutionizing", "mastering", "delve", "tapestry",
              "a new era", "shattering", "the future of", "game-chang", "ultimate guide"]
LOOP_MARKERS = ["?", " but ", "here's", "here is", "that's where", "that's when",
                "which brings", "to understand", "next", "coming up", "the only",
                "turns out", "the catch", "and that", "remember"]
# Spelled-out numerals — kept in sync with eval_script.py's NUMWORD_RE.
NUMWORD_RE = re.compile(
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"
    r"thousand|million|billion|half|double|triple)\b", re.IGNORECASE)
STOPWORDS = {"the", "a", "an", "of", "to", "in", "for", "and", "you", "your", "is", "it"}


class Rubric:
    def __init__(self):
        self.rows, self.kills = [], []

    def score(self, name, got, maximum, detail=""):
        self.rows.append((name, got, maximum, detail))

    def kill(self, name, detail):
        self.kills.append((name, detail))

    def report(self, human_pending):
        print(f"\n{'='*74}\n  CRAFT RUBRIC — automated subset\n{'='*74}")
        total = maxpts = 0
        for name, got, maximum, detail in self.rows:
            total += got; maxpts += maximum
            flag = "✓" if got == maximum else ("~" if got > 0 else "✗")
            print(f"  [{flag}] {got}/{maximum}  {name}" + (f" — {detail}" if detail else ""))
        print(f"\n  AUTO SCORE: {total}/{maxpts}  (+{100-maxpts} pts human-judged: {human_pending})")
        if self.kills:
            print(f"\n  KILL-LIST HITS (publish blocked):")
            for name, detail in self.kills:
                print(f"    ✗ {name} — {detail}")
        est = "PROJECTED PASS" if (total / maxpts) >= 0.8 and not self.kills else "AT RISK / BLOCKED"
        print(f"  Publish gate needs ≥80/100 overall + zero kills → {est}\n{'='*74}\n")
        return 1 if self.kills else 0


def words(t):
    return t.split()


def content_words(t):
    return {w.strip(".,!?()'\"").lower() for w in t.split()} - STOPWORDS


def main():
    parser = argparse.ArgumentParser(description="Automated craft rubric checks")
    parser.add_argument("script")
    args = parser.parse_args()
    with open(args.script) as f:
        script = json.load(f)

    r = Rubric()
    sections = {s["id"]: s for s in script["sections"]}
    all_text = " ".join(b["vo_text"] for s in script["sections"] for b in s["beats"]).lower()

    # ---- KILL LIST ----
    for p in KILL_PHRASES + WRAPUP_PHRASES:
        if p in all_text:
            r.kill("banned phrase", f"'{p}'")

    # ---- HOOK (auto: 20 of 25) ----
    # Archetype-signal check, NOT numbers-only: any of number / question /
    # quote / contrast pivot counts (approved archetypes don't all use numbers;
    # forcing one pattern = formulaic = inauthentic-content risk).
    # Beat 0 = series open (brand furniture, 2026-07-05) — excluded from hook checks.
    hook_text = " ".join(b["vo_text"] for b in sections.get("hook", {}).get("beats", [])
                         if b.get("beat", 1) != 0)
    first37 = " ".join(words(hook_text)[:37]).lower()

    def tension_signals(t):
        sig = []
        if re.search(r"\d|billion|million|thousand", t, re.I):
            sig.append("number")
        elif len({m.lower() for m in NUMWORD_RE.findall(t)}) >= 2:
            # VO spells numerals ("six seats", not "6 seats"). One number word
            # alone is not a signal — "one of the" would rubber-stamp the check.
            # Two distinct quantities is a comparison, which is the real signal.
            # Mirrors eval_script.py's rule; keep the two in sync. (2026-07-31)
            sig.append("number (spelled)")
        if "?" in t: sig.append("question")
        if re.search(r"[\"“”'][^\"“”']{8,}[\"“”']", t): sig.append("quote")
        if any(w in t.lower() for w in [" but ", " yet ", "however", "instead",
                                        "not because", "is not ", "isn't ",
                                        " another ", " while ", " meanwhile "]):
            sig.append("contrast")
        return sig

    sig15 = tension_signals(first37)
    if sig15:
        r.score("hook: archetype tension by 0:15", 10, 10, f"signals: {sig15}")
    elif tension_signals(hook_text):
        r.score("hook: archetype tension by 0:15", 5, 10,
                f"tension lands after ~15s: {tension_signals(hook_text)}")
    else:
        r.score("hook: archetype tension by 0:15", 0, 10,
                "no number/question/quote/contrast in hook")
    opener = hook_text.lower()[:60]
    bad = [b for b in BANNED_OPENERS if opener.startswith(b) or f" {b}" in opener[:30]]
    r.score("hook: no housekeeping opener", 0 if bad else 5, 5, f"found {bad}" if bad else "")
    if bad:
        r.kill("housekeeping opener", str(bad))
    first2 = " ".join(re.split(r"(?<=[.!?])\s+", hook_text)[:2])
    r.score("hook: tension in first two sentences",
            5 if tension_signals(first2) else 0, 5, f"{tension_signals(first2)}")

    # ---- TITLE (auto: 7 of 15; scored on best option, all options reported) ----
    titles = script.get("title_options", [])
    def title_issues(t):
        issues = []
        if len(t) > 60: issues.append(f"{len(t)} chars")
        if ":" in t or ";" in t: issues.append("colon/semicolon")
        low = t.lower()
        issues += [w for w in TITLE_SLOP if w in low]
        caps = [w for w in t.split() if len(w) > 3 and w.isupper()]
        if caps: issues.append(f"ALL-CAPS {caps}")
        if re.search(r"[\U0001F300-\U0001FAFF]", t): issues.append("emoji")
        return issues
    per = {t: title_issues(t) for t in titles}
    clean = [t for t, i in per.items() if not i]
    r.score("title: ≥1 option clean (≤60 chars, no slop/colon/caps/emoji)",
            7 if clean else 0, 7,
            "; ".join(f"'{t[:40]}…': {i}" for t, i in per.items() if i) or "all clean")

    # ---- THUMBNAIL (auto: 7 of 15) ----
    thumb_opts = script.get("thumbnail_text_options") or []
    if not thumb_opts:
        # fall back: quoted strings inside thumbnail_concepts (avoid apostrophes)
        for c in script.get("thumbnail_concepts", []):
            thumb_opts += [m.strip() for m in re.findall(r"(?<![A-Za-z])'([^']{1,40})'", c)
                           if m.strip() and not m.startswith(" ")]
    if thumb_opts:
        ok_len = [t for t in thumb_opts if len(words(t)) <= 3]
        r.score("thumbnail: ≥1 text option ≤3 words", 4 if ok_len else 0, 4,
                f"options: {thumb_opts}")
        title_wordset = content_words(" ".join(titles))
        no_dup = [t for t in (ok_len or thumb_opts)
                  if not (content_words(t) & title_wordset)]
        r.score("thumbnail: text doesn't duplicate title words", 3 if no_dup else 0, 3,
                "" if no_dup else "all options share title words")
    else:
        r.score("thumbnail: ≥1 text option ≤3 words", 0, 4, "no thumbnail text specified")
        r.score("thumbnail: text doesn't duplicate title words", 0, 3, "n/a")

    # ---- STRUCTURE (auto: 16 of 25) ----
    body_ids = [s["id"] for s in script["sections"] if s["id"] not in ("hook", "cta")]
    looped = []
    for sid in body_ids:
        last = sections[sid]["beats"][-1]["vo_text"].lower()
        if any(m in last for m in LOOP_MARKERS):
            looped.append(sid)
    frac = len(looped) / max(1, len(body_ids))
    r.score("structure: sections end on micro-open loops (heuristic)",
            6 if frac == 1 else (3 if frac >= 0.5 else 0), 6,
            f"{len(looped)}/{len(body_ids)} sections ({sorted(set(body_ids)-set(looped))} lack markers)")
    r.score("structure: no wrap-up signals", 4 if not any(p in all_text for p in WRAPUP_PHRASES) else 0, 4)
    long_beats = [f"{s['id']}#{b['beat']}" for s in script["sections"]
                  for b in s["beats"] if len(words(b["vo_text"])) > 110]
    r.score("structure: no beat >110 words (~45s)", 3 if not long_beats else 0, 3,
            f"long: {long_beats}" if long_beats else "")
    charts_unsourced = [f"{s['id']}#{b['beat']}" for s in script["sections"] for b in s["beats"]
                        if b.get("asset_hint", "").strip().lower().startswith("chart")
                        and not b.get("source")]
    r.score("structure: every chart beat carries a source", 3 if not charts_unsourced else 0, 3,
            f"unsourced charts: {charts_unsourced}" if charts_unsourced else "")

    # Semantic density, not cut-counting: stock b-roll runs are the slop signal.
    asset_types = [(s["id"], b["beat"], b.get("asset_hint", "").split(":")[0].strip().lower())
                   for s in script["sections"] for b in s["beats"]]
    run, worst = 0, 0
    for _, _, t in asset_types:
        run = run + 1 if t.startswith("broll") else 0
        worst = max(worst, run)
    r.score("semantic density: no 3+ consecutive b-roll beats", 3 if worst < 3 else 0, 3,
            f"longest b-roll run: {worst}")
    ARTIFACTS = ("chart", "screen_rec", "screen rec", "document", "slide")
    missing_artifacts = [sid for sid in ("evidence", "economics") if sid in sections and not any(
        b.get("asset_hint", "").lower().startswith(ARTIFACTS)
        for b in sections[sid]["beats"])]
    r.score("semantic density: evidence artifact in evidence + economics sections",
            3 if not missing_artifacts else 0, 3,
            f"sections without artifacts: {missing_artifacts}" if missing_artifacts else "")

    # ---- CTA (auto: 7 of 10) ----
    early_ids = [i for i in ("hook", "thesis", "evidence", "stack") if i in sections]
    early_text = " ".join(b["vo_text"].lower() for i in early_ids for b in sections[i]["beats"])
    # Word-boundary match, not substring (fixed 2026-07-31). The bare `in`
    # test fired on "multi-million-SUBSCRIBEr audience" and kill-listed an
    # episode that had no CTA anywhere before the payoff. For a channel that
    # covers audience businesses, "subscriber" is going to keep showing up.
    early_cta = bool(re.search(r"\b(?:subscribe|blueprint|link below|download)\b", early_text))
    r.score("cta: nothing before first payoff (hook→stack clean)", 4 if not early_cta else 0, 4)
    if early_cta:
        r.kill("early CTA", "subscribe/blueprint mention before the payoff sections")
    mid_ids = [i for i in ("playbook", "economics") if i in sections]
    mid_text = " ".join(b["vo_text"].lower() for i in mid_ids for b in sections[i]["beats"])
    r.score("cta: soft blueprint mention in 55–75% window", 3 if "blueprint" in mid_text else 0, 3,
            "" if "blueprint" in mid_text else "no mid-video mention (end-only reaches ~16%)")

    # ---- SHORTS BRIEFS (information-gap strategy) ----
    shorts_path = Path(args.script).parent / "content" / "shorts_briefs.json"
    if shorts_path.exists():
        with open(shorts_path) as f:
            briefs = json.load(f)
        no_gap, no_pin = [], []
        for i, b in enumerate(briefs):
            cliff = (b.get("cliffhanger_line") or "").strip()
            pin = (b.get("pinned_comment") or "").lower()
            if not cliff:
                no_gap.append(i)
            if "full" not in pin and "breakdown" not in pin and "link" not in pin:
                no_pin.append(i)
        r.score("shorts: every brief ends on a cliffhanger (information gap)",
                4 if not no_gap else 0, 4, f"briefs missing cliffhanger: {no_gap}" if no_gap else "")
        r.score("shorts: every brief has a pinned comment pointing to the long-form",
                3 if not no_pin else 0, 3, f"briefs missing pin: {no_pin}" if no_pin else "")
        if no_gap:
            r.kill("complete-answer Short", "a Short that resolves the question kills conversion")
    else:
        print("  (shorts_briefs.json not present yet — shorts checks run after derive step)")

    # ---- TRAILER BRIEF (pre-launch teaser: pure information gap) ----
    trailer_path = Path(args.script).parent / "content" / "trailer_brief.json"
    if trailer_path.exists():
        with open(trailer_path) as f:
            tb = json.load(f)
        segs = tb.get("segments") or []
        sec_ids = {s.get("section") for s in segs}
        r.score("trailer: 2-4 segments from >=2 different sections",
                3 if 2 <= len(segs) <= 4 and len(sec_ids) >= 2 else 0, 3,
                "" if 2 <= len(segs) <= 4 and len(sec_ids) >= 2
                else f"{len(segs)} segments across {len(sec_ids)} sections")
        card = f"{tb.get('end_card_title', '')} {tb.get('end_card_sub', '')}".lower()
        r.score("trailer: end card announces the Monday drop",
                2 if "monday" in card else 0, 2,
                "" if "monday" in card else "end card doesn't carry the drop date")
        # Thesis leakage: the trailer must not contain the thesis section's payoff.
        thesis_beats = sections.get("thesis", {}).get("beats", [])
        thesis_text = " ".join(b["vo_text"].lower() for b in thesis_beats)
        leaked = [i for i, s in enumerate(segs)
                  if s.get("section") == "thesis"
                  and (s.get("last_line") or "").lower() in thesis_text
                  and thesis_text.strip().endswith((s.get("last_line") or "").lower())]
        if leaked:
            r.kill("trailer resolves the thesis",
                   f"segment(s) {leaked} run to the thesis payoff — a trailer that answers "
                   "the question cannibalizes the Monday watch")

    human = ("archetype quality, thumbnail art/contrast/legibility, previewed-payoff arc, "
             "on-screen text in hook, honest-title judgment, voice direction, variation")
    sys.exit(r.report(human))


if __name__ == "__main__":
    main()
