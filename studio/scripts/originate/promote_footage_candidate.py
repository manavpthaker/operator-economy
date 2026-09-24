"""Promote one explicitly approved candidate into the footage manifest."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from footage_manifest import file_sha256, media_duration


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("entry_id")
    ap.add_argument("asset_id")
    ap.add_argument("--faces-review", choices=("cleared", "not_applicable"), required=True)
    ap.add_argument("--source-in", type=float, default=0.0)
    ap.add_argument("--source-out", type=float)
    ap.add_argument("--focal-point", default="center")
    args = ap.parse_args()
    episode = Path(args.script).resolve().parent
    candidate_data = json.loads((episode / "footage_candidates.json").read_text())
    manifest_path = episode / "footage_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    beat = next((b for b in candidate_data["beats"] if b["id"] == args.entry_id), None)
    candidate = next((c for c in (beat or {}).get("candidates", []) if c["asset_id"] == args.asset_id), None)
    entry = next((e for e in manifest["entries"] if e["id"] == args.entry_id), None)
    if not candidate or not entry:
        raise SystemExit("Candidate or manifest entry not found")
    source = episode / candidate["proxy_rel"]
    if file_sha256(source) != candidate["sha256"]:
        raise SystemExit("Candidate checksum mismatch")
    target_dir = episode / "footage" / "candidates"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{args.entry_id}--pexels-{args.asset_id}.mp4"
    shutil.copy2(source, target)
    duration = media_duration(target)
    source_out = min(args.source_out if args.source_out is not None else duration, duration)
    entry.update({
        "approved": True, "provider": "pexels", "asset_id": args.asset_id,
        "page_url": candidate["page_url"], "creator": candidate["creator"],
        "license": "Pexels License", "license_url": candidate["license"],
        "license_checked_at": candidate["license_checked_at"],
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "local_path": str(target.relative_to(episode)), "sha256": file_sha256(target),
        "faces_review": args.faces_review, "synthetic": False,
        "source_in": args.source_in, "source_out": source_out,
        "crop": "cover", "focal_point": args.focal_point,
    })
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Approved {args.asset_id} → {entry['id']} ({source_out - args.source_in:.2f}s)")


if __name__ == "__main__":
    main()
