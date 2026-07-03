"""
Flip an episode from `in_research` to `live` in site/data/episodes.json.

The derive step upserts the entry with figures pulled from script.json,
but leaves status=in_research until the operator says the video is live.
This is that flip.

Usage:
    python scripts/originate/publish.py <slug> [--rev A] [--date 2026-07]
    python scripts/originate/publish.py <slug> --unpublish   # flip back
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.parent
EPISODES_JSON = REPO_ROOT / "site" / "data" / "episodes.json"


def main():
    parser = argparse.ArgumentParser(description="Publish an episode to the site")
    parser.add_argument("slug", help="Episode slug (matches script.json 'slug')")
    parser.add_argument("--rev", default="A", help="Blueprint revision letter (default: A)")
    parser.add_argument("--date", help="Publish month YYYY-MM (default: today's month)")
    parser.add_argument("--read-minutes", type=int, help="Estimated blueprint read time")
    parser.add_argument("--unpublish", action="store_true", help="Flip back to in_research")
    args = parser.parse_args()

    if not EPISODES_JSON.exists():
        print(f"error: {EPISODES_JSON} not found", file=sys.stderr)
        sys.exit(1)

    with open(EPISODES_JSON) as f:
        data = json.load(f)

    ep = next((e for e in data.get("episodes", []) if e.get("slug") == args.slug), None)
    if ep is None:
        print(f"error: no entry for slug '{args.slug}' — run derive_content.py first", file=sys.stderr)
        sys.exit(1)

    if args.unpublish:
        ep["status"] = "in_research"
        for k in ("rev", "date", "read_minutes"):
            ep.pop(k, None)
        action = "unpublished"
    else:
        ep["status"] = "live"
        ep["rev"] = args.rev
        ep["date"] = args.date or date.today().strftime("%Y-%m")
        if args.read_minutes is not None:
            ep["read_minutes"] = args.read_minutes
        ep.setdefault("pdf_href", "#capture")
        ep.setdefault("episode_href", "#library")
        action = f"published as №{ep.get('number', '??'):03d} Rev {ep['rev']} ({ep['date']})"

    data["updated"] = date.today().isoformat()

    with open(EPISODES_JSON, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"✓ {args.slug} {action}")


if __name__ == "__main__":
    main()
