#!/usr/bin/env python3
"""
Originate: generate the thumbnail scene photograph via fal.ai.

Why this exists (2026-08-10). `prepare_thumbnail.py` hard-fails when
`remotion/public/thumbs/<slug>-a.png` is missing, and that file has always
come from outside the system. So every episode either got a hand-made image
or fell back to a typographic card. EP003 got nothing and drew 0.0% CTR on
142 impressions.

The direction was settled by looking at what YouTube actually surfaces on a
cold, logged-out feed: near enough every tile is a photograph of a person with
a legible expression, carrying bold overlaid text. Not one tile in that feed
was a flat-colour card with a number on it, which is what the channel has been
shipping.

The overlay is NOT generated here. Text is set in Remotion's `photo` variant,
where we control the typeface and can guarantee it survives the shrink test.
Image models set type badly. This step produces the ground only.

The prompt preamble encodes thumbnail-rubric.md so the composition arrives
usable rather than needing a crop:
  rule 3 — real scene, expressive face, eyes near the upper third
  rule 4 — lower-left kept clear, because that is where the text block anchors
  rule 5 — subject separated from ground, directional light
  register — documentary, per brand/brand.md. No hype, no stock gloss.

    generate_scene.py <slug> --scene "a plumber in a work van ..." [--n 2]
    generate_scene.py <slug>            # scene from script.json thumbnail_concepts[0]

Output is cropped to exactly 1280x720 and written to remotion/public/thumbs/.
Requires FAL_KEY in the repo .env, and ffmpeg on PATH.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # studio/
REPO = ROOT.parent
THUMBS = ROOT / "remotion" / "public" / "thumbs"
DEFAULT_MODEL = "fal-ai/flux-pro/v1.1-ultra"

PREAMBLE = (
    "Editorial portrait photograph, shot on an 85mm lens at f/2. "
)
# Framing is the whole game, and it is what the first pass got wrong.
#
# A wide environmental shot makes the room larger than the person, so the
# subject reads as someone the situation happened to. That is why the first
# batch came back depressing on episodes that are about opportunity. A tight
# head-and-shoulders portrait makes the person larger than the room, and the
# identical serious expression then reads as someone who knows something.
#
# Checked against what YouTube actually surfaces in Wealth and Thoughts on a
# logged-out feed: the stern tiles outperform, but every one of them is a close
# portrait with the head filling roughly a third of the frame. Seriousness is
# fine. Smallness is not.
CONSTRAINTS = (
    " Tight head-and-shoulders portrait, cropped at the chest, the head filling "
    "about a third of the frame. The subject is placed toward the right of the "
    "frame, looking directly into the lens with a composed, self-possessed, "
    "knowing expression: serious and unsmiling, but confident rather than sad, "
    "defeated or pitiable. Directional key light with a subtle rim separating "
    "the head and shoulders from a much darker, heavily out-of-focus background. "
    "Muted colour, fine film grain. The left third of the frame is dark and free "
    "of detail, reserved for overlaid text. Absolutely no text, no lettering, no "
    "numbers, no logos, no watermarks, no signage, no branded clothing. Not stock "
    "photography, not advertising, no glossy retouching, no exaggerated "
    "expression."
)


def fal_key() -> str:
    env = REPO / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("FAL_KEY="):
                return line.split("=", 1)[1].strip()
    raise SystemExit("no FAL_KEY in .env")


def scene_from_script(slug: str) -> str:
    sp = ROOT / "originate" / slug / "script.json"
    if not sp.exists():
        raise SystemExit(f"no script.json for {slug}; pass --scene")
    concepts = json.loads(sp.read_text()).get("thumbnail_concepts") or []
    if not concepts:
        raise SystemExit(f"{slug} has no thumbnail_concepts; pass --scene")
    print(f"  scene from script.json thumbnail_concepts[0]")
    return concepts[0]


def generate(prompt: str, model: str, n: int, key: str) -> list[str]:
    body = json.dumps({
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "num_images": n,
        "output_format": "jpeg",
        "safety_tolerance": "5",
    }).encode()
    req = urllib.request.Request(
        f"https://fal.run/{model}", data=body,
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            out = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"fal {e.code}: {e.read().decode()[:500]}")
    return [im["url"] for im in out.get("images", [])]


def fetch_and_fit(url: str, dest: Path) -> None:
    """Centre-crop to exactly 1280x720. fal returns 16:9-ish, not 16:9 exact."""
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.jpg"
        urllib.request.urlretrieve(url, raw)
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-vf",
             "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720",
             str(dest)], check=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--scene", help="scene description; overrides script.json")
    ap.add_argument("--n", type=int, default=2, help="candidates (default 2)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--dry-run", action="store_true", help="print the prompt, generate nothing")
    a = ap.parse_args()

    scene = a.scene or scene_from_script(a.slug)
    prompt = PREAMBLE + scene.rstrip(".") + "." + CONSTRAINTS

    print(f"{a.slug} — {a.model}")
    print(f"  prompt: {prompt[:150]}...")
    if a.dry_run:
        print("\n--- full prompt ---\n" + prompt)
        return 0

    urls = generate(prompt, a.model, a.n, fal_key())
    if not urls:
        raise SystemExit("no images returned")

    for i, url in enumerate(urls):
        letter = chr(ord("a") + i)
        dest = THUMBS / f"{a.slug}-{letter}.png"
        fetch_and_fit(url, dest)
        print(f"  wrote {dest.relative_to(REPO)}")

    print(f"\nNext: set bgImage in render_data, render the `photo` variant, then\n"
          f"  check_thumbnail.py on the result. The scene is the ground, not the\n"
          f"  thumbnail — the text still has to pass the shrink test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
