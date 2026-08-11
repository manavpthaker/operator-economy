#!/usr/bin/env python3
"""
Originate: fetch the real brand marks for an episode's stack.

Why this exists (2026-08-11). A8 recorded a gap it could not close: one
recognisable mark at scale is the strongest single pattern in the measured comp
set — MagnatesMedia's entire top quartile, and the best survivor of the 120px
shrink — and text-to-image cannot make one. Diffusion models garble lettering,
which is why `generate_scene.py` forbids naming a logo at all. So the archetype
was narrowed to `product` and the pattern was left unreachable.

This closes it from the other side. The mark is not generated, it is FETCHED and
composited, the same way the overlay text is set in Remotion rather than drawn by
the image model. Marks come from Simple Icons (CC0, https://simpleicons.org),
which ships official brand colours alongside each path.

The distinction the comp set actually supports, and it is narrow:

    a logo COLLAGE as the subject       5 instances measured, 5 bottom quartile
    one mark at scale, or marks as a
    supporting layer under a dominant
    subject                             MagnatesMedia's top quartile; Greg
                                        Isenberg's LOCAL AI IS TAKING OVER (1.80x)

So this writes assets. It does not decide composition, and nothing here permits
a row of marks to become the subject — see the strip cap in ThumbnailComposition.

    fetch_logos.py <slug> [--names Zapier Make Notion] [--mono] [--max 4]

Reads the episode's `stack` section when --names is not given. Writes PNGs to
remotion/public/logos/ and a manifest to render_data/logos.json. Names that have
no mark are REPORTED AND SKIPPED, never substituted: a wrong logo on a thumbnail
is worse than no logo.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # studio/
LOGOS = ROOT / "remotion" / "public" / "logos"
CACHE = ROOT / ".cache" / "simple-icons.json"
DATA_URL = "https://cdn.jsdelivr.net/npm/simple-icons@15/data/simple-icons.json"
SVG_URL = "https://cdn.jsdelivr.net/npm/simple-icons@15/icons/{slug}.svg"

# Simple Icons' own slug rules, enough of them to resolve our stacks.
SLUG_FIXES = {".": "dot", "+": "plus", "&": "and"}

# Where a script's everyday name is not the brand's registered title.
ALIASES = {
    "chatgpt": "openai", "gpt": "openai", "gpt-4": "openai", "gpt-5": "openai",
    "claude code": "claude", "anthropic claude": "claude",
    "google sheets": "googlesheets", "sheets": "googlesheets",
    "google docs": "googledocs", "next.js": "nextdotjs", "cal.com": "caldotcom",
    "make.com": "make", "notebook lm": "notebooklm",
}

# Words the stack-section scraper picks up that are not tools. Kept explicit
# rather than clever: a silent miss here puts a wrong mark on a thumbnail.
NOT_TOOLS = {
    "all", "the", "this", "that", "which", "where", "both", "none", "here",
    "only", "small", "somebody", "knowing", "look", "across", "ready", "plan",
    "path", "form", "prompt", "credits", "underneath", "code", "crm", "faqs",
    "gdp", "inc", "assessment", "verify", "fluency", "reframe", "next",
    "march", "december", "tuesday", "austin", "you", "your", "a", "an", "ai",
    "i", "it", "we", "they", "so", "but", "and", "if", "when", "then", "now",
}


def load_index() -> dict:
    """Slug + official hex for every mark, cached after the first call."""
    if CACHE.exists():
        raw = json.loads(CACHE.read_text())
    else:
        with urllib.request.urlopen(DATA_URL, timeout=60) as r:
            raw = json.loads(r.read().decode())
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(raw))
    icons = raw.get("icons", raw) if isinstance(raw, dict) else raw
    out = {}
    for ic in icons:
        title = ic.get("title", "")
        slug = ic.get("slug") or slugify(title)
        out[title.lower()] = (slug, ic.get("hex", "FFFFFF"))
        out[slug] = (slug, ic.get("hex", "FFFFFF"))
    return out


def slugify(name: str) -> str:
    s = name.lower().strip()
    for k, v in SLUG_FIXES.items():
        s = s.replace(k, v)
    return re.sub(r"[^a-z0-9]", "", s)


def resolve(name: str, index: dict) -> tuple[str, str] | None:
    key = name.lower().strip()
    if key in NOT_TOOLS:
        return None
    key = ALIASES.get(key, key)
    return index.get(key) or index.get(slugify(key))


def names_from_stack(slug: str) -> list[str]:
    p = ROOT / "originate" / slug / "script.json"
    if not p.exists():
        raise SystemExit(f"no script.json for {slug}; pass --names")
    for sec in json.loads(p.read_text()).get("sections", []):
        if sec.get("id") != "stack":
            continue
        txt = " ".join(b.get("vo_text") or b.get("text") or ""
                       for b in sec.get("beats", []))
        # Proper nouns and dotted names, in the order the script introduces them,
        # because that is the order the episode argues for them.
        seen, out = set(), []
        for m in re.findall(r"\b[A-Z][a-zA-Z0-9]*(?:\.[a-z]{2,3})?\b", txt):
            if m.lower() not in seen:
                seen.add(m.lower())
                out.append(m)
        return out
    raise SystemExit(f"{slug} has no `stack` section; pass --names")


def render(slug: str, hex_: str, mono: bool, dest: Path) -> None:
    """Write the SVG itself. Remotion renders in Chromium, which rasterises
    vectors natively at whatever size the composition asks for — so there is no
    reason to bake a PNG, and a baked one would only lose quality on the 4K
    master A7 calls for. (ffmpeg cannot do this anyway on a build without
    librsvg, which is the common case.)"""
    with urllib.request.urlopen(SVG_URL.format(slug=slug), timeout=30) as r:
        svg = r.read().decode()
    fill = "#F5F0E6" if mono else f"#{hex_.lstrip('#')}"
    # The packaged SVGs carry no fill attribute; set it so --mono and full
    # colour take the same path and neither depends on the CDN variant.
    svg = re.sub(r'\sfill="[^"]*"', "", svg, count=1)
    svg = svg.replace("<svg", f'<svg fill="{fill}"', 1)
    dest.write_text(svg)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("--names", nargs="*", help="override the stack section")
    ap.add_argument("--mono", action="store_true",
                    help="render in brand paper instead of official brand colour")
    ap.add_argument("--max", type=int, default=4,
                    help="cap on marks written (default 4). A row of marks is a "
                         "supporting layer; past about four it becomes the subject, "
                         "which is a measured bottom-quartile pattern.")
    a = ap.parse_args()

    index = load_index()
    names = a.names or names_from_stack(a.slug)
    LOGOS.mkdir(parents=True, exist_ok=True)

    found, missed = [], []
    for n in names:
        if len(found) >= a.max:
            break
        hit = resolve(n, index)
        if not hit:
            if n.lower() not in NOT_TOOLS:
                missed.append(n)
            continue
        slug, hex_ = hit
        dest = LOGOS / f"{slug}.svg"
        if not dest.exists():
            render(slug, hex_, a.mono, dest)
        found.append({"name": n, "slug": slug, "hex": f"#{hex_.lstrip('#')}",
                      "file": f"logos/{dest.name}"})

    # Scraping proper nouns out of prose produces FALSE POSITIVES, and a wrong
    # mark on a thumbnail is a factual claim about somebody else's product.
    # too-small-to-bother's `stack` section argues about venture funding rather
    # than listing tools, and the scraper duly returned Google and Zillow. When
    # the hit rate is this low the section is prose, not a stack.
    ratio = len(found) / max(len(found) + len(missed), 1)
    if names is not a.names and (ratio < 0.5 or len(found) < 2):
        print(f"  ! {len(found)} of {len(found)+len(missed)} candidates resolved. "
              f"This section reads as prose rather than a tool list, so these "
              f"marks are probably wrong.\n"
              f"    Check them, or re-run with an explicit --names list. Passing "
              f"--names is always the reliable path;\n"
              f"    the scraper is a convenience, not a source of truth.")

    out = ROOT / "originate" / a.slug / "render_data" / "logos.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"logos": found}, indent=2))

    print(f"{a.slug} — {len(found)} mark(s) → {out.relative_to(ROOT)}")
    for f in found:
        print(f"  {f['name']:16s} {f['slug']:16s} {f['hex']}")
    if missed:
        print(f"\n  no mark in Simple Icons, skipped rather than substituted:")
        print(f"    {', '.join(missed)}")
        print(f"  If one of these is load-bearing, add the file to "
              f"{LOGOS.relative_to(ROOT)} by hand and edit logos.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
