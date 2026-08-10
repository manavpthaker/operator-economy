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

The prompt encodes the composition so it arrives usable rather than needing a
rescue crop: subject waist-up on the RIGHT, caught mid-sentence addressing the
camera, with the LEFT of the frame plain and unbusy because that is where the
text block sits. Register stays documentary per brand/brand.md — animated and
direct, never hyped, never stock-posed.

Describe the action, never the mood. Mood adjectives ("worn", "resigned",
"muted") leak across the whole frame and are what made three earlier passes
come back depressing.

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
# Ten models scored against the scene rubric, 2026-08-10 (model_bakeoff.py):
#   seedream4      CHOSEN. imagen4-ultra scored marginally higher on face size
#                  and clean output, but seedream4's frames read as somebody's
#                  actual workplace rather than a set: t-shirt not a uniform,
#                  real shop, unstaged. Context beat polish.
#   imagen4-ultra  best raw quality, largest face, zero artefacts. Alternate.
#   imagen4        good, smaller face, garbled shirt logos.
#   seedream3      photoreal but busier frames and more signage.
#   flux-ultra     reads rendered rather than photographed.
#   ideogram3      subject turns away, frame busy on both sides.
#   recraft3       cinematic and lovely, subject far too small for a thumbnail.
#
# Per-family quirks worth knowing:
#   imagen*   reads "empty left third" LITERALLY and returns a white block. Say
#             "the background continues as a plain shadowed wall".
#   seedream* takes image_size, not aspect_ratio, and honours negative_prompt.
DEFAULT_MODEL = "fal-ai/bytedance/seedream/v4/text-to-image"
ALTERNATE_MODEL = "fal-ai/imagen4/preview/ultra"

# Sizing differs by family. Anything unlisted falls back to aspect_ratio.
MODEL_PARAMS = {
    "seedream": {"image_size": {"width": 1280, "height": 720}},
    "imagen":   {"aspect_ratio": "16:9"},
    "flux":     {"aspect_ratio": "16:9"},
    "recraft":  {"image_size": {"width": 1280, "height": 720}},
    "ideogram": {"image_size": {"width": 1280, "height": 720}},
}

# Every model invents lettering on clothing and signage, and it is the clearest
# tell that an image was generated. Two things fix it, and both are needed:
# a negative prompt where the family supports one, and describing surfaces as
# positively blank in CONSTRAINTS. Diffusion models follow "plain unbranded
# t-shirt" far more reliably than "no logos".
NEGATIVE = (
    "text, lettering, writing, words, letters, numbers, logos, brand names, "
    "signage, signs, posters, labels, stickers, banners, printed t-shirt, "
    "embroidered logo, watermark, captions, license plate"
)

PREAMBLE = (
    "Candid editorial photograph for a business magazine, available light, "
    "shot on a 50mm lens. "
)
# Four passes to get here. The failures are worth keeping, because each one
# looks reasonable in isolation and each produced an unusable thumbnail.
#
#   1. wide + environmental      the room ends up larger than the person, so
#                                the subject reads as someone the situation
#                                happened to. Depressing on episodes about
#                                opportunity.
#   2. tight portrait, grim words  still depressing. The vocabulary was grim end
#                                to end (muted, desaturated, shadow, film grain,
#                                unsmiling, worn) and asking for "composed and
#                                knowing" alongside all that does not survive.
#                                Tone words dominate everything else. The
#                                rim-light-on-heavy-bokeh also reads as rendered.
#   3. "absorbed and pleased"    swung to corporate stock: people beaming at a
#                                laptop. No curiosity gap, reads as an advert.
#   4. mid-sentence to camera    correct.
#
# What the feed rewards is none of the first three. Hormozi, Adam Ivy, the DOAC
# tiles: all caught MID-SENTENCE, addressing the viewer, hands moving. An
# unfinished sentence is interesting. A finished mood is not.
#
# Two lessons that generalise: describe the ACTION, not the mood, because mood
# adjectives leak into the whole frame; and available light with real skin
# texture is what sells an image as photographed rather than rendered.
CONSTRAINTS = (
    " They wear plain unbranded everyday clothes with no printing on them. The "
    "surfaces behind them are bare: unlabelled boxes, loose parts and plain "
    "painted walls with nothing hung on them. Waist-up framing, subject toward "
    "the right of the frame, caught mid-sentence addressing the camera directly, "
    "one hand raised mid-gesture in explanation, animated, confident and warm "
    "without grinning, eye contact with the lens, eyebrows and mouth active as "
    "though speaking. Bright natural daylight, clean true-to-life colour, "
    "realistic skin texture with visible pores and fine lines. On the left the "
    "background continues as a plain shadowed wall with little detail, reserved "
    "for overlaid text. Photographed, not rendered: no studio lighting, no rim "
    "light, no heavy bokeh, no glossy skin retouching. Nobody sad, tired or "
    "defeated, and nobody posed smiling at a laptop like a stock photograph."
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


def size_params(model: str) -> dict:
    for family, params in MODEL_PARAMS.items():
        if family in model:
            return params
    return {"aspect_ratio": "16:9"}


def generate(prompt: str, model: str, n: int, key: str) -> list[str]:
    payload = {"prompt": prompt, "num_images": n, **size_params(model)}
    # Only seedream honours it; sending it elsewhere is a 422.
    if "seedream" in model:
        payload["negative_prompt"] = NEGATIVE
    body = json.dumps(payload).encode()
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
