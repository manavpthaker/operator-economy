"""
Automated subset of docs/post-rubric.md — the LLM-watermark ban + banned openers.

Checks what a machine can check (punctuation, banned lexicon, openers, income
promises). The register/rhythm judgments stay human. Exit 1 on any hard fail.

Usage:
    python scripts/originate/rubric_check.py <file.md> [--surface feed|carousel|dm|group]
    python scripts/originate/rubric_check.py originate/<slug>/content/launch_linkedin.md

Surfaces: em dashes are a HARD FAIL in feed/dm/group copy; allowed in carousel.
Markdown headings (#), link URLs, and the "## First comment" sources block are
scanned too — the ban applies to everything that ships.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BANNED_WORDS = [
    "delve", "tapestry", "testament", "multifaceted", "cutting-edge",
    "revolutionary", "pivotal", "meticulous", "intricate", "vibrant",
    "robust", "nuanced", "holistic", "synergy", "utilize", "foster",
    "garner", "underscore", "bolster", "illuminate", "facilitate",
    "harness", "seamlessly", "realm", "beacon", "endeavor", "embark",
    "moreover", "furthermore", "additionally", "certainly", "indeed",
    "notably",
]
# words banned only in specific senses — flagged as warnings, human judges
WARN_WORDS = ["leverage", "landscape", "empower"]

BANNED_PHRASES = [
    "i'd love to", "really resonates", "ever-evolving", "it's important to note",
    "harness the power", "game-changing", "is a testament to", "empowering people to",
    "unlocking the potential", "whether you're",
    "ai-powered", "passive income", "side hustle",
    "hustle", "grind", "hack", "skyrocket", "insane",
    "stumbled onto", "stumbled upon", "came across this gem", "found this channel",
]

BANNED_OPENERS = [
    r"^hot take\b", r"^unpopular opinion\b", r"^what if you",
    r"^most \w+ starts? with the wrong", r"^here'?s how to make \$",
]

INCOME_PROMISE = re.compile(
    r"you (could|can|will) (be )?(mak(e|ing)|earn)[^.]{0,40}\$", re.I)


def check(text: str, surface: str) -> tuple[list[str], list[str]]:
    fails, warns = [], []
    lines = text.splitlines()

    if surface != "carousel":
        for i, ln in enumerate(lines, 1):
            # ignore pure markdown structure lines
            if ln.strip().startswith(("#", "|", "```", ">")):
                continue
            if "—" in ln or "–" in ln:
                fails.append(f"line {i}: em/en dash in {surface} copy (rubric §2, #1 AI tell)")

    low = text.lower()
    for w in BANNED_WORDS:
        for m in re.finditer(rf"\b{re.escape(w)}\b", low):
            i = low[: m.start()].count("\n") + 1
            fails.append(f"line {i}: banned word '{w}'")
    for w in WARN_WORDS:
        if re.search(rf"\b{re.escape(w)}\b", low):
            warns.append(f"'{w}' present — banned as verb/metaphor, check sense")
    for p in BANNED_PHRASES:
        if p in low:
            i = low[: low.find(p)].count("\n") + 1
            fails.append(f"line {i}: banned phrase '{p}'")

    # first non-empty, non-heading line = the hook
    hook = next((ln.strip() for ln in lines
                 if ln.strip() and not ln.strip().startswith(("#", "|", ">"))), "")
    for pat in BANNED_OPENERS:
        if re.search(pat, hook, re.I):
            fails.append(f"hook: banned opener ({pat!r}): {hook[:60]}")
    if hook.endswith("?"):
        warns.append(f"hook is a question — OE asserts, then earns it: {hook[:60]}")

    if INCOME_PROMISE.search(text):
        fails.append("income-promise pattern ('you could be making ... $')")

    # structural tells (warnings — human judges)
    para = [p for p in text.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    short = [p for p in para if len(p.split()) <= 25]
    if len(para) >= 5 and len(short) == len(para):
        warns.append("every paragraph is 1–2 short sentences — rhythm tell, vary it")

    return fails, warns


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--surface", default="feed",
                    choices=["feed", "carousel", "dm", "group"])
    args = ap.parse_args()

    text = Path(args.file).read_text()
    fails, warns = check(text, args.surface)

    for w in warns:
        print(f"  WARN  {w}")
    for f in fails:
        print(f"  FAIL  {f}")
    if fails:
        print(f"\n{len(fails)} hard fail(s) — revise, don't rationalize (rubric §5).")
        sys.exit(1)
    print(f"OK ({args.surface}): no watermark/opener violations. "
          "Human checks still required: read aloud, byline test, tap test, guru test.")


if __name__ == "__main__":
    main()
