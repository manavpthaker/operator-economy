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
import zlib
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
CONSTRAINTS_PERSON = (
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

# Added 2026-08-11, because the block above is written entirely for a human
# subject — clothes, waist-up framing, eye contact, skin texture — and the
# rubric it now serves has stopped asking for one. Amendment A8 retired the
# hero number and measurement put `object` and `verdict` at the top of the
# register lane; run through the person constraints, "a single vintage barber
# chair" comes back as somebody sitting in a barber chair. The archetype has to
# pick the block.
#
# What carries across all three, because it was expensive to learn: describe the
# ACTION or the STATE, never the mood, since mood adjectives leak across the
# whole frame; available light and real material texture is what sells an image
# as photographed rather than rendered; and every surface is positively blank,
# because diffusion models garble any lettering they invent.
CONSTRAINTS_OBJECT = (
    " No people anywhere in the frame, and no hands. The object is the whole "
    "subject, filling most of the frame, sitting where it is actually used "
    "rather than arranged for a photograph. Every surface is bare and "
    "unlabelled: no signage, no packaging, no printed markings, no screens "
    "showing anything. Real material texture — worn metal, scuffed paint, dust "
    "in the seams, marks from use. Bright natural daylight, clean true-to-life "
    "colour. The object sits in the RIGHT half of the frame and the "
    "BOTTOM-LEFT quarter is empty floor or plain wall with nothing in it, "
    "because that is exactly where the text block lands. Photographed, not "
    "rendered: no studio sweep, no seamless backdrop, no rim light, no heavy "
    "bokeh, no product-catalogue gloss, no gradient background."
)
CONSTRAINTS_SCENE = (
    " A press photograph of a real working place, not a set. If a person is "
    "present they are incidental and mid-task, never addressing the camera and "
    "never centred. Every surface is bare and unlabelled: no signage, no "
    "printed markings, no screens showing anything, no branded clothing. One "
    "element is sharp and unmistakably the subject; everything else falls away. "
    "Available light, clean true-to-life colour, real material texture. The "
    "sharp subject sits in the RIGHT half of the frame and the BOTTOM-LEFT "
    "quarter is left empty, because that is where the text block lands. "
    "Photographed, not rendered: no studio lighting, no rim light, no heavy "
    "bokeh. Nothing staged, nobody posed, and nobody sad or defeated."
)

# Added 2026-08-11, copied deliberately from one measured thumbnail rather than
# reasoned from principles: Modern MBA's THE ECONOMICS OF COOKIES, 8.21x its
# channel median and the highest multiple in the register lane.
#
# What that frame actually does, decomposed: overhead flat-lay; TWO HANDS
# entering from the bottom edge, one holding a phone; every object rotated,
# overlapping and BLEEDING OFF the frame edges so nothing is contained; branded
# packets scattered among the real objects at different sizes; crumbs and mess
# on the surface. It is dense to the edges and nothing is squared up. Our four
# earlier attempts were single objects centred in empty rooms, which is the
# opposite frame, and no thumbnail in the 78-image comp set looks like that.
#
# The branded packets are the part that generalises. In the original they are
# Mrs Fields, Famous Amos and a Crumbl box; ours are the episode's actual stack,
# composited by fetch_logos.py rather than generated, since diffusion garbles
# lettering. The scene must therefore leave surface FOR them.
# The framing was hardcoded to one shot -- straight down, two hands from the
# bottom edge, phone in the left -- so every flat-lay in the set came back as the
# same photograph with the props swapped. Similar design, identical image.
#
# These are the variations that all still satisfy the invariants: dense to every
# edge, a human in frame, bare patches left for the marks. What varies is the
# camera, which hands enter and from where, and how tight the crop is. Chosen
# deterministically from the slug so an episode keeps its framing across
# re-runs, and overridable with --framing.
# Six framings were added here first, and they were all variations on ONE shot:
# overhead, hands from the bottom. Nine episodes came back as nine overhead
# flat-lays, because that is what the archetype means. Moving the camera within
# a flat-lay does not make a different photograph.
#
# These are actual shot types. A flat-lay is now one of six rather than the
# house style, and which one an episode gets is decided by
# `assign_shots.py` across the whole set, not per episode in isolation -- the
# sameness was never visible from inside a single episode, only from the sheet.
SHOTS = [
    ("flatlay",
     "Shot straight down from directly overhead, flat-lay. Two hands enter from "
     "the bottom edge, one holding a phone upright, the other reaching in "
     "mid-action."),

    ("over-shoulder",
     "Shot at eye level from just behind and over the shoulder of a person at "
     "work, their shoulder and upper arm soft in the near foreground, what they "
     "are working on sharp beyond it, the room falling away behind."),

    ("low-raking",
     "Shot low and raking across the working surface, lens almost level with it, "
     "one object large and sharp in the immediate foreground and the rest of the "
     "scene compressing away behind it into soft focus."),

    ("macro-detail",
     "Shot very close on a single detail of the work — a hand on a tool, a mark "
     "on a docket, a connector being seated — filling most of the frame, the "
     "wider room reduced to soft shape and colour behind it."),

    ("wide-room",
     "Shot wide from across the room at standing height, the whole working space "
     "visible with the person small inside it and their work legible on the "
     "surface, foreground objects cutting into the bottom of the frame."),

    ("frontal-counter",
     "Shot straight on at working height from the customer's side of the "
     "counter, as if standing at it, the surface running left to right across "
     "the frame and the person behind it mid-task."),
]
SHOT_INDEX = {name: i for i, (name, _) in enumerate(SHOTS)}

CONSTRAINTS_FLATLAY_TAIL = (
    " The surface is crowded to every edge and objects are cut off by all four "
    "frame edges, rotated at loose angles, overlapping each other, casually "
    "placed rather than arranged. Leave two or three empty patches of bare "
    "surface among the objects, each roughly a hand's width. Real mess: crumbs, "
    "dust, a stray paper clip, marks on the surface. Every surface is bare and "
    "unlabelled — no signage, no printed text, no packaging copy, no screens "
    "showing anything. Bright even daylight, clean true-to-life colour, strong "
    "material texture. Photographed, not rendered: no studio sweep, no seamless "
    "backdrop, no gradient background, nothing centred or symmetrical."
)


def flatlay_constraints(slug: str, shot: str | int | None) -> str:
    """Shot description + the invariants that hold whatever the camera does."""
    if shot is None:
        # Falling back to a hash is what produced nine overhead flat-lays. Say so
        # rather than silently picking one.
        i = zlib.crc32(slug.encode()) % len(SHOTS)
        print(f"  note: no --shot given, defaulting to `{SHOTS[i][0]}`. Shot "
              f"variety is a property of the SET, so prefer assign_shots.py.")
    elif isinstance(shot, int):
        i = shot % len(SHOTS)
    else:
        i = SHOT_INDEX[shot]
    return " " + SHOTS[i][1] + CONSTRAINTS_FLATLAY_TAIL


# Archetypes are defined in thumbnail_spec.py; this maps each to the block that
# can actually render it. Keep in step if that list changes.
# `practitioner` means two different things in the two halves of this system.
# thumbnail_spec.py scores it as "a person doing the work"; CONSTRAINTS_PERSON
# describes a presenter addressing the lens. Handed a scene that said "the hands
# the only human presence in frame", the constraint won and the model rendered
# BOTH briefs — a man gesturing at the camera next to a pair of hands under a
# desk. Two subjects, because two specs.
#
# This is the archetype for work being done rather than described: nobody
# performs to camera, nobody is selling anything, and the action is the subject.
CONSTRAINTS_AT_WORK = (
    " One person only, absorbed in the task and unaware of the camera — NO eye "
    "contact with the lens, no gesturing toward it, no addressing the viewer, "
    "not posed. Framed close on the work itself: hands, forearms and as much of "
    "the body as the action needs, the face incidental or out of frame entirely. "
    "One continuous action, mid-motion, with the tool or device actually in "
    "contact with the thing being worked on. They wear plain unbranded everyday "
    "clothes with no printing. Every surface and device is bare and unlabelled — "
    "no signage, no printed text, no packaging copy, no screens showing anything, "
    "no brand marks on any equipment. Bright natural daylight, clean true-to-life "
    "colour, realistic skin texture. Photographed, not rendered: no studio "
    "lighting, no rim light, no glossy retouching. Nobody sad, tired or defeated, "
    "and nobody posed smiling at a laptop like a stock photograph."
)

# Added 2026-08-13. Every block above ends "photographed, not rendered", which is
# right for documentary frames and fatal for a deliberate SCALE METAPHOR — the
# one composition where the picture is supposed to be impossible. `object` also
# bans hands outright, so "a tower in a palm" cannot be asked for at all.
#
# This exists because the register's honest documentary frames kept reading as
# too implicit at browse width: the surprise was a thing you had to notice.
# A scale collision is legible in one glance, which is all 120px gives you.
CONSTRAINTS_GRAPHIC = (
    " A deliberate scale collision, photographed convincingly rather than drawn: "
    "the large thing rendered small and solid and physically present, held in or "
    "resting on the human hand, with true contact shadows where they meet and "
    "consistent daylight across both. ONE hand and ONE object, nothing else in "
    "frame. Sharp focus throughout, real material texture on both the skin and "
    "the object. The background is a single plain uncluttered surface in one flat "
    "tone — a plain wall or open sky — with nothing else in it, so the silhouette "
    "reads at a glance and the upper third is clear for a text block. Every "
    "surface is bare and unlabelled: no signage, no printed markings, no screens "
    "showing anything. Clean true-to-life colour, no gradient background, no "
    "studio sweep, no glow, no lens flare, not a cartoon and not an illustration."
)

ARCHETYPE_CONSTRAINTS = {
    "practitioner": CONSTRAINTS_PERSON,
    "at-work":      CONSTRAINTS_AT_WORK,
    "graphic":      CONSTRAINTS_GRAPHIC,
    "object":       CONSTRAINTS_OBJECT,
    "product":      CONSTRAINTS_OBJECT,
    "verdict":      CONSTRAINTS_SCENE,
    "scene-wide":   CONSTRAINTS_SCENE,
}


def fal_key() -> str:
    env = REPO / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("FAL_KEY="):
                return line.split("=", 1)[1].strip()
    raise SystemExit("no FAL_KEY in .env")


def scene_from_spec(slug: str, rank: int) -> tuple[str, str] | None:
    """Highest-scoring spec from thumbnail_spec.py, with its archetype.

    This is the join between the two halves of the system. thumbnail_spec.py
    scores concepts and writes them to disk; until now nothing read that file
    and generation still went via script.json's free-text thumbnail_concepts,
    so the scored winner was never the thing generated.
    """
    f = ROOT / "originate" / slug / "render_data" / "thumbnail_specs.json"
    if not f.exists():
        return None
    specs = sorted(json.loads(f.read_text()).get("specs", []),
                   key=lambda s: -s.get("total", 0))
    if rank >= len(specs):
        raise SystemExit(f"{slug} has {len(specs)} specs; --rank {rank} is out of range")
    s = specs[rank]
    print(f"  scene from thumbnail_specs.json rank {rank} "
          f"({s.get('total')}/100, {s.get('archetype')})")
    return s.get("scene", ""), s.get("archetype", "")


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
    ap.add_argument("--scene", help="scene description; overrides the scored spec")
    # `flatlay` is a legal archetype but is NOT a key in ARCHETYPE_CONSTRAINTS —
    # its constraints are built per-shot by flatlay_constraints(). Deriving the
    # choices from that dict alone made the house layout the one archetype you
    # could not ask for, reachable only by whatever thumbnail_specs.json happened
    # to propose.
    ap.add_argument("--archetype", choices=sorted([*ARCHETYPE_CONSTRAINTS, "flatlay"]),
                    help="which constraint block to use; inferred from the spec "
                         "when --scene is not given. `flatlay` means the busy, "
                         "crowded-to-the-edges ground — pair it with --shot to "
                         "get that treatment WITHOUT the overhead camera")
    ap.add_argument("--shot", choices=[n for n, _ in SHOTS],
                    help="which shot type to use. Assign these ACROSS the set "
                         "with assign_shots.py rather than per episode: nine "
                         "episodes each independently picking a sensible shot "
                         "is how they all ended up overhead.")
    ap.add_argument("--tag",
                    help="name the output thumbs/<slug>-<tag>.png instead of "
                         "-a/-b/-c. Required when generating several variants "
                         "for one episode, which otherwise overwrite each other.")
    ap.add_argument("--rank", type=int, default=0,
                    help="which scored spec to generate, 0 = highest (default 0)")
    ap.add_argument("--n", type=int, default=2, help="candidates (default 2)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--dry-run", action="store_true", help="print the prompt, generate nothing")
    a = ap.parse_args()

    archetype = a.archetype
    if a.scene:
        scene = a.scene
    else:
        picked = scene_from_spec(a.slug, a.rank)
        if picked:
            scene, spec_archetype = picked
            archetype = archetype or spec_archetype
        else:
            scene = scene_from_script(a.slug)

    if not archetype:
        raise SystemExit(
            "cannot tell what kind of frame this is. Pass --archetype "
            f"({'|'.join(sorted(ARCHETYPE_CONSTRAINTS))}), or run "
            f"thumbnail_spec.py on {a.slug} first so the archetype comes with "
            "the scene. Guessing here produces a person in a barber chair.")
    if archetype == "flatlay":
        constraints = flatlay_constraints(a.slug, a.shot)
    else:
        constraints = ARCHETYPE_CONSTRAINTS[archetype]
    prompt = PREAMBLE + scene.rstrip(".") + "." + constraints

    print(f"{a.slug} — {a.model} — {archetype}")
    print(f"  prompt: {prompt[:150]}...")
    if a.dry_run:
        print("\n--- full prompt ---\n" + prompt)
        return 0

    urls = generate(prompt, a.model, a.n, fal_key())
    if not urls:
        raise SystemExit("no images returned")

    for i, url in enumerate(urls):
        # Without --tag every run of an episode lands on -a and silently
        # clobbers the previous variant. That cost 27 generations once.
        suffix = a.tag if a.tag else ""
        letter = chr(ord("a") + i)
        stem = f"{a.slug}-{suffix}" if suffix else f"{a.slug}-{letter}"
        if suffix and len(urls) > 1:
            stem = f"{stem}-{letter}"
        dest = THUMBS / f"{stem}.png"
        fetch_and_fit(url, dest)
        print(f"  wrote {dest.relative_to(REPO)}")

    print(f"\nNext: set bgImage in render_data, render the `photo` variant, then\n"
          f"  check_thumbnail.py on the result. The scene is the ground, not the\n"
          f"  thumbnail — the text still has to pass the shrink test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
