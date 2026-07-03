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
import os
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.parent
EPISODES_JSON = REPO_ROOT / "site" / "data" / "episodes.json"


def _notify_subscribers(slug: str, ep: dict) -> None:
    """Fire the "№00X is live" email to notify:{slug} subscribers via Resend.

    Requires RESEND_API_KEY, RESEND_FROM, and DATABASE_URL in the environment.
    Prints the recipient count and asks for confirmation before sending.
    """
    try:
        import psycopg
        from resend import Resend
    except ImportError as e:
        print(f"error: notify requires psycopg + resend Python packages ({e})", file=sys.stderr)
        print("  pip install 'psycopg[binary]' resend", file=sys.stderr)
        sys.exit(1)

    db_url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
    resend_key = os.environ.get("RESEND_API_KEY")
    resend_from = os.environ.get("RESEND_FROM", "The Operator Economy <hello@theoperatoreconomy.com>")
    site_url = os.environ.get("NEXT_PUBLIC_SITE_URL", "https://operator-economy.vercel.app")
    if not db_url or not resend_key:
        print("error: DATABASE_URL and RESEND_API_KEY must be set for --notify", file=sys.stderr)
        sys.exit(1)

    tag = f"notify:{slug}"
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "select email, unsubscribe_token from subscribers where tag = %s and unsubscribed_at is null",
                (tag,),
            )
            rows = cur.fetchall()

    if not rows:
        print(f"No active notify:{slug} subscribers — nothing to send.")
        return

    num = f"{ep.get('number', 0):03d}"
    title = ep.get("title", "the episode")
    ep_url = f"{site_url}/episodes/{slug}"

    print(f"About to email {len(rows)} subscribers that №{num} is live.")
    confirm = input("Send now? [y/N] ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        return

    resend = Resend(api_key=resend_key)
    sent = 0
    for email, token in rows:
        unsub = f"{site_url}/api/unsubscribe?token={token}"
        try:
            resend.emails.send(
                {
                    "from": resend_from,
                    "to": email,
                    "subject": f"№{num} is live — {title}",
                    "text": (
                        f"It shipped.\n\n"
                        f"№{num} — \"{title}\" — is live: {ep_url}\n\n"
                        f"The Operator Blueprint (PDF), full sources, and honest math are on the page.\n\n"
                        f"You're on the Monday note. Unsubscribe any time: {unsub}\n\n"
                        f"— The Operator Economy"
                    ),
                }
            )
            sent += 1
        except Exception as e:
            print(f"  ! failed to send to {email}: {e}", file=sys.stderr)

    print(f"✓ notified {sent}/{len(rows)} subscribers")


def main():
    parser = argparse.ArgumentParser(description="Publish an episode to the site")
    parser.add_argument("slug", help="Episode slug (matches script.json 'slug')")
    parser.add_argument("--rev", default="A", help="Blueprint revision letter (default: A)")
    parser.add_argument("--date", help="Publish month YYYY-MM (default: today's month)")
    parser.add_argument("--read-minutes", type=int, help="Estimated blueprint read time")
    parser.add_argument("--unpublish", action="store_true", help="Flip back to upcoming")
    parser.add_argument(
        "--notify",
        action="store_true",
        help="After flipping status=live, email notify:{slug} subscribers via Resend",
    )
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
        ep["status"] = "upcoming"
        ep.setdefault("stage", "production")
        for k in ("rev", "date", "read_minutes"):
            ep.pop(k, None)
        action = "unpublished"
    else:
        ep["status"] = "live"
        ep["rev"] = args.rev
        ep["date"] = args.date or date.today().strftime("%Y-%m")
        if args.read_minutes is not None:
            ep["read_minutes"] = args.read_minutes
        # Clear pipeline-position fields — they only apply to `upcoming` entries.
        ep.pop("stage", None)
        ep.pop("expected", None)
        action = f"published as №{ep.get('number', '??'):03d} Rev {ep['rev']} ({ep['date']})"

    data["updated"] = date.today().isoformat()

    with open(EPISODES_JSON, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"✓ {args.slug} {action}")

    if args.notify and not args.unpublish:
        _notify_subscribers(args.slug, ep)


if __name__ == "__main__":
    main()
