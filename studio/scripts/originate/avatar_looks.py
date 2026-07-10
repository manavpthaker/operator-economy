"""
Avatar look management — wardrobe + backdrop variants for the digital twin.

HeyGen "looks" are prompt-generated photo variants of the avatar group
(clothing, backdrop, lighting). They animate via the photo-avatar engine
(character type talking_photo), unlike the trained video avatar which
replays real footage motion. Use for brand-matched wardrobe/backdrop;
eyeball motion quality before adopting a look (docs/avatar-decision.md).

The group must be photo-trained once before looks can be generated
(`train`, ~5-20 min).

Usage:
    python scripts/originate/avatar_looks.py list
    python scripts/originate/avatar_looks.py train
    python scripts/originate/avatar_looks.py status
    python scripts/originate/avatar_looks.py generate "prompt text" \
        [--orientation vertical] [--pose half_body] [--style Realistic]
    python scripts/originate/avatar_looks.py generation-status <generation_id>

Then set config/blueprint.json -> avatar.look_id to the chosen look's id
(or pass --look to generate_avatar.py for a per-episode override).
"""

import argparse
import json
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "blueprint.json"
API_BASE = "https://api.heygen.com"

sys.path.insert(0, str(Path(__file__).parent))
from generate_avatar import api_key, load_env_file  # noqa: E402


def hdrs() -> dict:
    return {"x-api-key": api_key(), "Content-Type": "application/json"}


def group_id() -> str:
    cfg = json.loads(CONFIG.read_text()).get("avatar", {})
    gid = cfg.get("group_id")
    if not gid:
        print("Error: avatar.group_id missing in config/blueprint.json.",
              file=sys.stderr)
        sys.exit(1)
    return gid


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("train")
    sub.add_parser("status")
    g = sub.add_parser("generate")
    g.add_argument("prompt")
    g.add_argument("--orientation", default="vertical")
    g.add_argument("--pose", default="half_body")
    g.add_argument("--style", default="Realistic")
    gs = sub.add_parser("generation-status")
    gs.add_argument("generation_id")
    args = ap.parse_args()

    load_env_file()
    gid = group_id()

    if args.cmd == "list":
        r = requests.get(f"{API_BASE}/v2/avatar_group/{gid}/avatars",
                         headers=hdrs(), timeout=30)
        r.raise_for_status()
        for a in (r.json().get("data") or {}).get("avatar_list", []):
            # Trained video avatar rows use avatar_id; photo looks use id.
            kind = "video-avatar " if a.get("avatar_id") else "look         "
            aid = a.get("avatar_id") or a.get("id")
            name = a.get("avatar_name") or a.get("name")
            status = a.get("status", "-")
            print(f"{kind} {aid}  [{status}]  {name}")

    elif args.cmd == "train":
        r = requests.post(f"{API_BASE}/v2/photo_avatar/train",
                          headers=hdrs(), json={"group_id": gid}, timeout=30)
        print(r.text)

    elif args.cmd == "status":
        r = requests.get(f"{API_BASE}/v2/photo_avatar/train/status/{gid}",
                         headers=hdrs(), timeout=30)
        print(r.text)

    elif args.cmd == "generate":
        r = requests.post(f"{API_BASE}/v2/photo_avatar/look/generate",
                          headers=hdrs(), timeout=60,
                          json={"group_id": gid, "prompt": args.prompt,
                                "orientation": args.orientation,
                                "pose": args.pose, "style": args.style})
        print(r.text)

    elif args.cmd == "generation-status":
        r = requests.get(
            f"{API_BASE}/v2/photo_avatar/generation/{args.generation_id}",
            headers=hdrs(), timeout=30)
        print(r.text)


if __name__ == "__main__":
    main()
