#!/usr/bin/env python3
"""
Originate: distil the episode script into thumbnail scene prompts.

Why this exists (2026-08-10). Every thumbnail so far was built from a scene
somebody invented at thumbnail time, disconnected from the episode. That is how
four back-catalogue drafts ended up as the same photograph: a person standing at
a counter mid-sentence, four times, because the template came from the feed
rather than from the episodes.

The script already contains the specific, unrepeatable images. EP003 says "you
build the plumbing between them", "an owner losing three hours a day to
copy-paste between systems", "the unglamour is the moat". Those are thumbnails.
No other episode could use them, which is exactly the point: distinctiveness
between episodes comes free when the source is the episode.

This reads script.json and returns N concepts, each spanning a different
composition archetype so a set never collapses into one look:

    subject-left       subject hard left, clean right half for text
    subject-right      mirrored
    object             the thing itself, no person (a tangle of cable, a wall
                       of sticky notes) — the variety valve
    two-shot           operator and client, tension between them
    scene-wide         the environment IS the argument (an empty office)

Rules it inherits: every number must already appear in the script (facts.md
governs downstream), overlay text is 2-3 words that interpret rather than
label, and the scene description never names text, logos or signage because
the image model will render them garbled.

    derive_thumbnail_prompt.py originate/<slug>/script.json [--n 5]

Writes render_data/thumbnail_prompts.json for generate_scene.py to consume.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent

ARCHETYPES = ["subject-left", "subject-right", "object", "two-shot", "scene-wide"]

SYSTEM = """You design YouTube thumbnail concepts for The Operator Economy, a \
documentary channel about businesses one person can build. Register is analytical \
and restrained: no hype, no shock, no exclamation. It reads like a business \
magazine, not a creator channel.

You will be given one episode's script. Return concepts drawn ONLY from that \
script's specific content. The test: could this concept be reused on a different \
episode? If yes, it is wrong. Use the episode's own metaphors, its named people, \
places, objects and numbers.

Hard rules:
- Overlay text is 2 to 3 words that INTERPRET a number, never label it. \
"$500 EVERY MONTH" not "$500". "3 HOURS A DAY" not "TIME SAVED".
- Any number in overlay text must appear verbatim in the script.
- Overlay text must NOT repeat words from the episode title.
- The scene description must never mention text, writing, signage, logos, \
screens with readable content, or branded clothing. Image models render those \
as garbled nonsense and it is the clearest tell that a picture was generated. \
Describe surfaces as positively blank: plain unbranded clothing, bare walls, \
unlabelled boxes.
- Describe ACTION, never mood. Mood adjectives ("weary", "hopeful", "muted") \
leak across the whole frame and produce depressing pictures. Say what the \
person is DOING.
- Nobody is sad, defeated, or posed smiling at a laptop.
- These episodes are about opportunity. Where a person appears they are \
competent and mid-action, already doing the thing the episode teaches.

Return STRICT JSON, no prose, no code fence:
{"concepts":[{"archetype":"one of the given archetypes","overlay_big":"the \
number or short phrase","overlay_label":"2-3 interpreting words","scene":"one \
paragraph describing the photograph, composition first","from_script":"the \
exact line or fact this came from","why":"one sentence on the curiosity gap"}]}"""


def load_script(p: Path) -> dict:
    return json.loads(p.read_text())


def episode_digest(s: dict) -> str:
    """Everything a concept could legitimately be built from."""
    out = [f"TITLE OPTIONS: {json.dumps(s.get('title_options', []))}",
           f"APPROVED THUMBNAIL CONCEPTS: {json.dumps(s.get('thumbnail_concepts', []))}",
           f"APPROVED OVERLAY TEXT: {json.dumps(s.get('thumbnail_text_options', []))}"]
    for sec in s.get("sections", []):
        beats = " ".join(b.get("vo_text") or b.get("text") or ""
                         for b in sec.get("beats", []))
        if beats.strip():
            out.append(f"\n[{sec.get('id', '?').upper()}]\n{beats.strip()}")
    return "\n".join(out)


def call_claude(digest: str, n: int, model: str) -> dict:
    try:
        import anthropic
    except ImportError:
        raise SystemExit("pip install anthropic")
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        for line in (REPO / ".env").read_text().splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                key = line.split("=", 1)[1].strip()
    if not key:
        raise SystemExit("no ANTHROPIC_API_KEY")

    msg = anthropic.Anthropic(api_key=key).messages.create(
        model=model, max_tokens=4000, system=SYSTEM,
        messages=[{"role": "user", "content":
                   f"Episode script:\n\n{digest}\n\n"
                   f"Return exactly {n} concepts, each a DIFFERENT archetype from: "
                   f"{', '.join(ARCHETYPES[:n])}. At least one must be `object` "
                   f"(no person in frame) — a set of talking heads all looks the same."}])
    text = "".join(b.text for b in msg.content if b.type == "text").strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
    return json.loads(text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", type=Path)
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--model", default="claude-sonnet-5")
    a = ap.parse_args()

    s = load_script(a.script)
    slug = s.get("slug") or a.script.parent.name
    data = call_claude(episode_digest(s), a.n, a.model)

    dest = a.script.parent / "render_data" / "thumbnail_prompts.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({"slug": slug, **data}, indent=2))

    for i, c in enumerate(data.get("concepts", []), 1):
        print(f"\n{i}. [{c.get('archetype')}]  "
              f"{c.get('overlay_big')} / {c.get('overlay_label')}")
        print(f"   from: {(c.get('from_script') or '')[:96]}")
        print(f"   why:  {(c.get('why') or '')[:96]}")
    try:
        shown = dest.resolve().relative_to(REPO)
    except ValueError:
        shown = dest.resolve()
    print(f"\nwrote {shown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
