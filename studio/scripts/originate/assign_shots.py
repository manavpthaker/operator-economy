#!/usr/bin/env python3
"""
Originate: assign each episode a DIFFERENT shot, across the whole set.

Why this is a separate script (2026-08-12). Sameness is not visible from inside
an episode. Every one of the nine thumbnails was a defensible choice on its own
and the contact sheet was nine overhead flat-lays, because `flatlay` was made the
house layout and six "framings" were all variations on the same camera. Twice.

So shot choice cannot be a per-episode decision. It is a property of the SET, and
nothing in the pipeline held the set — thumbnail_spec.py scores one episode,
generate_scene.py renders one episode, and the collision only appears in a grid
neither of them builds. That is also the cross-episode gap left open when
amendment A8 retired `unrepeatable`: the reasoning was that the subject must be
episode-specific while the format repeats, and the check for the first half was
never written. This is it.

The rule is simple and only needs the set to enforce: **no two episodes share a
shot until every shot has been used**, then it wraps. Assignment is stable for a
fixed list of slugs, so re-running does not reshuffle work already approved.

    assign_shots.py                     # show the plan
    assign_shots.py --write             # write shot into each thumb-flatlay.json
    assign_shots.py --lock <slug> <shot>  # pin one episode, others work around it

Prints the generate_scene.py commands to run.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))

# Imported rather than duplicated: two lists of shot names WILL drift.
from generate_scene import SHOTS  # noqa: E402

NAMES = [n for n, _ in SHOTS]

# Shot assignment alone was not enough, and the second attempt proved it. Six
# real camera types inside `flatlay` still converged, because the archetype's
# own constraints — surface crowded to every edge, hands in frame, bare patches
# for the marks — describe the frame more strongly than the camera does. Nine
# episodes came back as nine variations of looking down at a work surface.
#
# The variety was already sitting in the set. `verdict` gives a documentary
# photograph, `object` gives the thing at scale, `practitioner` gives a person
# mid-action: three genuinely different pictures, all scored, all rendered. What
# made the sheet uniform was choosing `flatlay` as every episode's PRIMARY.
#
# So the assignment is over archetypes first and shots second. Shots vary the
# camera within an archetype; archetypes vary the picture.
ARCHETYPES = ["flatlay", "verdict", "object"]


def episodes() -> list[str]:
    return sorted(d.name for d in (ROOT / "originate").iterdir()
                  if (d / "script.json").exists())


def assign(slugs: list[str], locked: dict[str, str], names: list[str]) -> dict[str, str]:
    """Round-robin so the set spans every shot before repeating any.

    Deliberately not a hash of the slug. A hash is stable and independent, which
    sounds right and is exactly wrong here — crc32 across nine slugs put three of
    them on the same shot, because independent choices cannot spread themselves.
    """
    out = dict(locked)
    used = [s for s in out.values()]
    pool = [n for n in names if n not in used] or list(names)
    i = 0
    for slug in slugs:
        if slug in out:
            continue
        if not pool:
            pool = list(names)
        out[slug] = pool[i % len(pool)]
        pool.pop(i % len(pool))
        i = 0
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dimension", choices=["archetype", "shot"], default="archetype",
                    help="what to spread across the set. `archetype` varies the "
                         "PICTURE (default, and the one that actually works); "
                         "`shot` varies the camera inside flatlay.")
    ap.add_argument("--write", action="store_true",
                    help="record the shot in each episode's thumb-flatlay.json")
    ap.add_argument("--lock", nargs=2, action="append", metavar=("SLUG", "SHOT"),
                    default=[], help="pin an episode to a shot; repeatable")
    a = ap.parse_args()

    locked = {}
    for slug, shot in a.lock:
        if shot not in NAMES + ARCHETYPES:
            raise SystemExit(f"unknown value {shot!r}")
        locked[slug] = shot

    pool_names = ARCHETYPES if a.dimension == "archetype" else NAMES
    slugs = episodes()
    plan = assign(slugs, locked, pool_names)

    print(f"{len(slugs)} episodes, {len(pool_names)} {a.dimension}s\n")
    for slug in slugs:
        pin = "  (locked)" if slug in locked else ""
        print(f"  {slug:30s} {plan[slug]}{pin}")

    from collections import Counter
    dupes = {s: c for s, c in Counter(plan.values()).items() if c > 1}
    print(f"\n{a.dimension}s used: {len(set(plan.values()))}/{len(pool_names)}"
          + (f"   repeated (more episodes than shots): {dupes}" if dupes else ""))

    if a.write:
        for slug, shot in plan.items():
            f = ROOT / "originate" / slug / "render_data" / "thumb-flatlay.json"
            if not f.exists():
                continue
            d = json.loads(f.read_text())
            d[a.dimension] = shot
            f.write_text(json.dumps(d, indent=1))
        print("\nwritten to thumb-flatlay.json")

    print("\nregenerate:")
    for slug in slugs:
        print(f"  generate_scene.py {slug} --tag flatlay --shot {plan[slug]} --n 1 --rank <N>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
