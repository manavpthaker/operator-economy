#!/usr/bin/env python3
"""
Originate: thumbnail candidates → render_data/thumbnail-{a,b}.json

Why this exists (2026-07-31): the thumbnail was a manual ritual with no
pipeline step. EP001 shipped a photo thumbnail (82 views, the channel's
best). EP002 got a hand-written rework with two candidates and a note
(0.7% CTR). EP003 got *nothing* — no thumbnail.json, no image, no note —
so YouTube fell back to the title-card frame and the episode drew
**0.0% CTR on 142 recommended impressions**. Nothing in the pipeline
noticed.

This step makes the artifact a build output and, more importantly, makes
its ABSENCE loud: no scene image → non-zero exit, with the prompt you
need to go generate one. Gates are only useful if they fail.

Rules enforced (docs/thumbnail-rubric.md):
  2. ≤4 words, and zero words shared with the title
  1. no kicker / channel mark / episode number on the thumbnail
  photo variant preferred (rule 3: real scene, expressive face)

Usage:
    python scripts/originate/prepare_thumbnail.py originate/<slug>/script.json
    python scripts/originate/prepare_thumbnail.py originate/<slug>/script.json --allow-numbers
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
THUMBS_DIR = ROOT / "remotion" / "public" / "thumbs"
STOPWORDS = {"the", "a", "an", "of", "to", "in", "for", "and", "or", "is",
             "it", "on", "at", "you", "your", "with", "that", "this"}


def words_of(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9']+", text.lower()) if w not in STOPWORDS}


def check_text(label: str, title: str) -> list[str]:
    """Rubric rule 2 — ≤4 words, no overlap with the title."""
    problems = []
    n = len(label.split())
    if n > 4:
        problems.append(f"{n} words (rule 2: ≤4)")
    shared = words_of(label) & words_of(title)
    if shared:
        problems.append(f"shares {sorted(shared)} with the title (rule 2)")
    return problems


def split_comparison(text: str) -> tuple[str, str, str] | None:
    """'850 vs 1' → ('850', 'vs', '1'). Returns None if it isn't a comparison."""
    m = re.match(r"^\s*([$\d][\w$.,%/-]*)\s*(vs\.?|versus|→|->)\s*([$\d][\w$.,%/-]*)\s*$",
                 text, re.IGNORECASE)
    if not m:
        return None
    conn = "→" if m.group(2) in {"→", "->"} else "vs"
    return m.group(1), conn, m.group(3)


def scene_images(slug: str) -> list[Path]:
    if not THUMBS_DIR.exists():
        return []
    return sorted(p for p in THUMBS_DIR.iterdir()
                  if p.stem.startswith(slug) and p.suffix.lower() in {".png", ".jpg", ".jpeg"})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--allow-numbers", action="store_true",
                    help="Emit the numbers/versus variant without a scene image. "
                         "Rule 3 requires a written reason — put it in launch/thumbnail-note.md.")
    args = ap.parse_args()

    script_path = Path(args.script).resolve()
    script = json.loads(script_path.read_text())
    base = script_path.parent
    slug = script.get("slug", base.name)
    title = script.get("working_title", "")

    texts = script.get("thumbnail_text_options") or []
    concepts = script.get("thumbnail_concepts") or []
    if len(texts) < 2:
        print(f"✗ script.json has {len(texts)} thumbnail_text_options; the rubric "
              f"requires two candidates per episode.", file=sys.stderr)
        return 1

    # Rank the generated options: rubric-clean first, then shortest.
    ranked = sorted(texts, key=lambda t: (len(check_text(t, title)), len(t.split())))
    picks = ranked[:2]
    for t in picks:
        problems = check_text(t, title)
        flag = "✓" if not problems else "⚠"
        print(f"  {flag} \"{t}\"" + (f" — {'; '.join(problems)}" if problems else ""))

    images = scene_images(slug)
    rd = base / "render_data"
    rd.mkdir(exist_ok=True)

    variant = "photo" if images else ("versus" if args.allow_numbers else None)
    if variant is None:
        note = base / "launch" / "thumbnail-note.md"
        print(f"\n✗ No scene image for '{slug}' in remotion/public/thumbs/.\n"
              f"  The rubric's standing concept is the install moment: this week's\n"
              f"  business being delivered to a real customer, expressive face, viewer\n"
              f"  as hero. Locked concept from script.json:\n", file=sys.stderr)
        for c in concepts:
            print(f"    · {c}", file=sys.stderr)
        print(f"\n  Generate the scene, save it as remotion/public/thumbs/{slug}-a.png,\n"
              f"  and re-run. Write the reasoning into {note.relative_to(ROOT.parent)}.\n"
              f"  To ship a numbers thumbnail instead, pass --allow-numbers AND record\n"
              f"  the written reason (rule 3).\n", file=sys.stderr)
        return 2

    clean = [t for t in ranked if not check_text(t, title)]
    if len(clean) < 2:
        print(f"\n⚠ Only {len(clean)} of {len(texts)} generated text options are "
              f"rubric-clean; the rest duplicate words from the title \"{title}\".\n"
              f"  The rubric wants two DISTINCT candidates to compare. Write a second\n"
              f"  by hand before the shrink test, or the A/B is theatre.", file=sys.stderr)

    out = []
    for i, (letter, text) in enumerate(zip("ab", picks)):
        props: dict = {
            "variant": variant,
            "label": text,
            # Rule 1: no kicker, no channel mark, no episode number.
            "kicker": "",
        }
        if variant == "photo":
            props["bgImage"] = f"thumbs/{images[min(i, len(images) - 1)].name}"
        else:
            # The versus variant needs two figures. If a text option is itself
            # a comparison ("850 vs 1"), it IS the numbers — using it as the
            # word label would render blank figures, which ships worse than
            # nothing. Split it and let another option carry the words.
            pair = split_comparison(text)
            if not pair:
                pair = next((p for t in picks if (p := split_comparison(t))), None)
            if not pair:
                print(f"✗ versus variant needs a comparison ('850 vs 1') in "
                      f"thumbnail_text_options; none found.", file=sys.stderr)
                return 1
            big, connector, small = pair
            props["big"], props["connector"], props["small"] = big, connector, small
            if split_comparison(text):
                # this option was the numbers — find words for the label
                words_opt = next((t for t in ranked if not split_comparison(t)), "")
                props["label"] = words_opt
        p = rd / f"thumbnail-{letter}.json"
        p.write_text(json.dumps(props, indent=2))
        out.append(p)
        print(f"  ✓ {p.relative_to(base)}  ({variant})")

    print("\nRender both, then judge at 320px AND 168px (rubric rule 6):")
    for letter in "ab":
        print(f"  npx remotion still src/index.ts Thumbnail out/thumb-{slug}-{letter}.png "
              f"--props=../originate/{slug}/render_data/thumbnail-{letter}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
