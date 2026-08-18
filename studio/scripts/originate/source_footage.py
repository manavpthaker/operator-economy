#!/usr/bin/env python3
"""Search contextual footage proxies and promote a reviewed candidate."""

from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    from footage_manifest import file_sha256, load_json, media_duration
except ImportError:
    from .footage_manifest import file_sha256, load_json, media_duration

PEXELS_API = "https://api.pexels.com/videos/search"
PEXELS_LICENSE = "https://www.pexels.com/license/"
STOCK_ROLES = {"human_context", "outcome"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def search_pexels(query: str, api_key: str, per_page: int = 15) -> list[dict]:
    url = PEXELS_API + "?" + urllib.parse.urlencode({
        "query": query, "per_page": per_page, "orientation": "landscape"})
    request = urllib.request.Request(url, headers={
        "Authorization": api_key,
        "User-Agent": "OperatorEconomy/1.0 (+https://theoperatoreconomy.com)",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    results = []
    for video in payload.get("videos", []):
        files = [f for f in video.get("video_files", [])
                 if f.get("file_type") == "video/mp4" and f.get("link")]
        if not files:
            continue
        files.sort(key=lambda f: (f.get("width", 0) >= 1280,
                                  f.get("width", 0) * f.get("height", 0)), reverse=True)
        selected = files[0]
        results.append({
            "candidate_id": f"pexels-{video['id']}",
            "provider": "pexels",
            "asset_id": str(video["id"]),
            "page_url": video.get("url", ""),
            "creator": video.get("user", {}).get("name", "Unknown"),
            "creator_url": video.get("user", {}).get("url", ""),
            "license": "Pexels License",
            "license_url": PEXELS_LICENSE,
            "duration_seconds": video.get("duration", 0),
            "width": selected.get("width", 0),
            "height": selected.get("height", 0),
            "download_url": selected["link"],
        })
    return results


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "OperatorEconomy/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response, destination.open("wb") as out:
        shutil.copyfileobj(response, out)


def candidate_score(candidate: dict) -> tuple:
    duration = candidate.get("duration_seconds", 0)
    return (candidate.get("width", 0) >= 1920, 5 <= duration <= 30,
            candidate.get("width", 0) * candidate.get("height", 0))


def write_review(ledger: dict, episode_dir: Path, script_path: Path) -> Path:
    cards = []
    for group in ledger.get("entries", []):
        if not group.get("candidates"):
            cards.append(
                f"<section><h2>{html.escape(group['manifest_id'])}</h2>"
                f"<p class='route'>{html.escape(group.get('reason', group.get('route', '')))}</p></section>")
            continue
        candidates = []
        for candidate in group["candidates"]:
            src = html.escape(candidate["local_path"])
            command = (f"python scripts/originate/source_footage.py approve {script_path} "
                       f"{group['manifest_id']} {candidate['candidate_id']} "
                       "--faces-review cleared --source-in 0 --source-out SECONDS")
            candidates.append(
                f"<article><video controls muted preload='metadata' src='{src}'></video>"
                f"<h3>{html.escape(candidate['candidate_id'])}</h3>"
                f"<p>{html.escape(candidate.get('creator',''))} · "
                f"{candidate.get('width')}×{candidate.get('height')} · "
                f"{candidate.get('duration_seconds')}s</p>"
                f"<p>{html.escape(' · '.join(candidate.get('matched_queries', [])))}</p>"
                f"<a href='{html.escape(candidate.get('page_url',''))}'>Source page</a>"
                f"<code>{html.escape(command)}</code></article>")
        cards.append(f"<section><h2>{html.escape(group['manifest_id'])}</h2>"
                     f"<div class='grid'>{''.join(candidates)}</div></section>")
    document = """<!doctype html><html><head><meta charset="utf-8"><title>Footage candidates</title>
<style>body{font:14px system-ui;margin:32px;background:#f5f0e6;color:#171714}section{border-top:1px solid #bdb4a5;padding:28px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}article{background:white;padding:14px;border:1px solid #d2c8b8}video{width:100%;aspect-ratio:16/9;background:#14263e}h3{font-family:ui-monospace,monospace}code{display:block;white-space:normal;margin-top:12px;padding:10px;background:#171714;color:#f5f0e6}.route{color:#9b3e2e}</style></head><body>
<h1>Footage candidate review</h1><p>No candidate is approved automatically. Review semantic match, faces, rights, crop, and exact source range.</p>""" + "".join(cards) + "</body></html>"
    path = episode_dir / "footage_candidates.html"
    path.write_text(document)
    return path


def search(script_path: Path, limit: int) -> None:
    episode_dir = script_path.parent
    manifest_path = episode_dir / "footage_manifest.json"
    manifest = load_json(manifest_path)
    api_key = os.environ.get("PEXELS_API_KEY")
    if not api_key:
        raise SystemExit("PEXELS_API_KEY is not set; no network search was performed")
    output_dir = episode_dir / "footage" / "candidates"
    output_dir.mkdir(parents=True, exist_ok=True)
    ledger = {"episode": manifest.get("episode"), "generated_at": now_iso(), "entries": []}
    for entry in manifest.get("entries", []):
        if entry.get("role") not in STOCK_ROLES:
            ledger["entries"].append({
                "manifest_id": entry["id"], "route": "capture_or_artifact",
                "reason": f"{entry.get('role')} must use original capture, source evidence, or licensed brand material",
                "candidates": [],
            })
            continue
        candidates_by_id = {}
        for query in [q for q in entry.get("query_variants", []) if q]:
            for candidate in search_pexels(query, api_key):
                candidate.setdefault("matched_queries", []).append(query)
                candidates_by_id.setdefault(candidate["candidate_id"], candidate)
        ranked = sorted(candidates_by_id.values(), key=candidate_score, reverse=True)
        # A single staged shoot often occupies most of Pexels' first page.
        # Cap each creator so the review surface contains genuinely distinct
        # visual hypotheses rather than nine angles from one production.
        creator_counts: dict[str, int] = {}
        candidates = []
        for candidate in ranked:
            creator = candidate.get("creator", "Unknown")
            if creator_counts.get(creator, 0) >= 2:
                continue
            candidates.append(candidate)
            creator_counts[creator] = creator_counts.get(creator, 0) + 1
            if len(candidates) >= limit:
                break
        for candidate in candidates:
            destination = output_dir / f"{entry['id']}--{candidate['candidate_id']}.mp4"
            if not destination.exists():
                download(candidate["download_url"], destination)
            candidate["local_path"] = str(destination.relative_to(episode_dir))
            candidate["sha256"] = file_sha256(destination)
            candidate["downloaded_at"] = now_iso()
            candidate.pop("download_url", None)
        ledger["entries"].append({
            "manifest_id": entry["id"], "route": "licensed_contextual_stock",
            "candidates": candidates,
        })
    out = episode_dir / "footage_candidates.json"
    out.write_text(json.dumps(ledger, indent=2) + "\n")
    review = write_review(ledger, episode_dir, script_path)
    print(f"Wrote {out} and {review}; candidates remain unapproved")


def approve(script_path: Path, manifest_id: str, candidate_id: str,
            faces_review: str, source_in: float, source_out: float | None) -> None:
    episode_dir = script_path.parent
    manifest_path = episode_dir / "footage_manifest.json"
    candidates_path = episode_dir / "footage_candidates.json"
    manifest = load_json(manifest_path)
    ledger = load_json(candidates_path)
    entry = next((e for e in manifest.get("entries", []) if e.get("id") == manifest_id), None)
    if entry is None:
        raise SystemExit(f"Unknown manifest id: {manifest_id}")
    group = next((g for g in ledger.get("entries", []) if g.get("manifest_id") == manifest_id), None)
    candidate = next((c for c in (group or {}).get("candidates", [])
                      if c.get("candidate_id") == candidate_id), None)
    if candidate is None:
        raise SystemExit(f"Unknown candidate {candidate_id} for {manifest_id}")
    local_path = episode_dir / candidate["local_path"]
    duration = media_duration(local_path)
    selected_out = duration if source_out is None else source_out
    if source_in < 0 or selected_out <= source_in or selected_out > duration + 0.05:
        raise SystemExit(f"Invalid source range for {duration:.2f}s candidate")
    entry.update({
        "approved": True,
        "provider": candidate["provider"],
        "asset_id": candidate["asset_id"],
        "page_url": candidate["page_url"],
        "creator": candidate["creator"],
        "license": candidate["license"],
        "license_url": candidate["license_url"],
        "license_checked_at": datetime.now(timezone.utc).date().isoformat(),
        "downloaded_at": candidate["downloaded_at"],
        "local_path": candidate["local_path"],
        "sha256": candidate["sha256"],
        "faces_review": faces_review,
        "source_in": source_in,
        "source_out": round(selected_out, 3),
    })
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Approved {candidate_id} for {manifest_id}; run footage_manifest.py validate")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    search_p = sub.add_parser("search")
    search_p.add_argument("script")
    search_p.add_argument("--limit", type=int, default=3)
    approve_p = sub.add_parser("approve")
    approve_p.add_argument("script")
    approve_p.add_argument("manifest_id")
    approve_p.add_argument("candidate_id")
    approve_p.add_argument("--faces-review", required=True,
                           choices=("cleared", "not_applicable"))
    approve_p.add_argument("--source-in", type=float, default=0)
    approve_p.add_argument("--source-out", type=float)
    args = parser.parse_args()
    script_path = Path(args.script).resolve()
    if args.command == "search":
        search(script_path, args.limit)
    else:
        approve(script_path, args.manifest_id, args.candidate_id,
                args.faces_review, args.source_in, args.source_out)


if __name__ == "__main__":
    main()
