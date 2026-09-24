#!/usr/bin/env python3
"""Search contextual footage proxies and promote a reviewed candidate.

Sources, by footage role (see docs/blueprint-cinema.md, Evidence, Footage, and Synthetic Media):

  human_context, outcome  pexels, pixabay, storyblocks, internet_archive, wikimedia
  market_force            internet_archive, wikimedia, plus manually added press kits
  proof, process          never searched; original capture or source evidence only

API providers run only when their keys are set (PEXELS_API_KEY, PIXABAY_API_KEY,
STORYBLOCKS_PUBLIC_KEY + STORYBLOCKS_PRIVATE_KEY + STORYBLOCKS_USER_ID +
STORYBLOCKS_PROJECT_ID), from the environment or the repo .env; the public-domain archives need none. Public-domain
results are limited to public domain, CC0, and CC BY, because uploader-asserted
licenses are unreliable: the license is checked again by a human at approve.

`add` registers a file downloaded by hand (a company press kit, or a Storyblocks
web download when the API is unavailable) with its provenance, so it goes
through the same review and approve path as searched candidates.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import html
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    from _model import env_key
    from footage_manifest import file_sha256, load_json, media_duration
except ImportError:
    from ._model import env_key
    from .footage_manifest import file_sha256, load_json, media_duration

PEXELS_API = "https://api.pexels.com/videos/search"
PEXELS_LICENSE = "https://www.pexels.com/license/"
PIXABAY_API = "https://pixabay.com/api/videos/"
PIXABAY_LICENSE = "https://pixabay.com/service/license-summary/"
STORYBLOCKS_API = "https://api.storyblocks.com"
STORYBLOCKS_LICENSE = "https://www.storyblocks.com/license"
ARCHIVE_SEARCH = "https://archive.org/advancedsearch.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "OperatorEconomy/1.0 (+https://theoperatoreconomy.com)"

STOCK_PROVIDERS = ["pexels", "pixabay", "storyblocks", "internet_archive", "wikimedia"]
ARCHIVAL_PROVIDERS = ["internet_archive", "wikimedia"]
ROLE_PROVIDERS = {
    "human_context": STOCK_PROVIDERS,
    "outcome": STOCK_PROVIDERS,
    "market_force": ARCHIVAL_PROVIDERS,
}
PRESS_ROLES = {"market_force", "human_context", "outcome"}


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


def get_json(url: str, headers: dict | None = None) -> dict:
    request = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT, "Accept": "application/json", **(headers or {})})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def search_pixabay(query: str, api_key: str, per_page: int = 15) -> list[dict]:
    payload = get_json(PIXABAY_API + "?" + urllib.parse.urlencode({
        "key": api_key, "q": query[:100], "per_page": per_page, "safesearch": "true"}))
    results = []
    for hit in payload.get("hits", []):
        sizes = [v for v in hit.get("videos", {}).values() if v.get("url")]
        if not sizes:
            continue
        selected = max(sizes, key=lambda v: v.get("width", 0) * v.get("height", 0))
        user = hit.get("user", "Unknown")
        results.append({
            "candidate_id": f"pixabay-{hit['id']}",
            "provider": "pixabay",
            "asset_id": str(hit["id"]),
            "page_url": hit.get("pageURL", ""),
            "creator": user,
            "creator_url": f"https://pixabay.com/users/{user}-{hit.get('user_id')}/",
            "license": "Pixabay Content License",
            "license_url": PIXABAY_LICENSE,
            "duration_seconds": hit.get("duration", 0),
            "width": selected.get("width", 0),
            "height": selected.get("height", 0),
            "download_url": selected["url"],
        })
    return results


def storyblocks_credentials() -> dict | None:
    names = ("STORYBLOCKS_PUBLIC_KEY", "STORYBLOCKS_PRIVATE_KEY",
             "STORYBLOCKS_USER_ID", "STORYBLOCKS_PROJECT_ID")
    values = {n: env_key(n) for n in names}
    return values if all(values.values()) else None


def storyblocks_get(path: str, params: dict, creds: dict) -> dict:
    # HMAC-SHA256 of the resource path, keyed by private key + expiry.
    expires = str(int(time.time()) + 3600)
    signature = hmac.new((creds["STORYBLOCKS_PRIVATE_KEY"] + expires).encode(),
                         path.encode(), hashlib.sha256).hexdigest()
    query = {**params, "APIKEY": creds["STORYBLOCKS_PUBLIC_KEY"], "EXPIRES": expires,
             "HMAC": signature, "user_id": creds["STORYBLOCKS_USER_ID"],
             "project_id": creds["STORYBLOCKS_PROJECT_ID"]}
    return get_json(STORYBLOCKS_API + path + "?" + urllib.parse.urlencode(query))


def search_storyblocks(query: str, creds: dict, per_page: int = 15) -> list[dict]:
    payload = storyblocks_get("/api/v2/videos/search", {
        "keywords": query, "results_per_page": per_page, "content_type": "footage"}, creds)
    results = []
    for item in payload.get("results", []):
        results.append({
            "candidate_id": f"storyblocks-{item['id']}",
            "provider": "storyblocks",
            "asset_id": str(item["id"]),
            "page_url": f"https://www.storyblocks.com/video/stock/{item['id']}",
            "creator": "Storyblocks",
            "license": "Storyblocks subscription license",
            "license_url": STORYBLOCKS_LICENSE,
            "duration_seconds": item.get("duration", 0),
            "width": 1920,
            "height": 1080,
            # Download links are minted per stock item and count against the
            # subscription, so review happens on the 720p preview first.
            "download_url": (item.get("preview_urls") or {}).get("_720p", ""),
            "proxy_only": True,
        })
    return [r for r in results if r["download_url"]]


def storyblocks_master(asset_id: str, creds: dict) -> str:
    payload = storyblocks_get(f"/api/v2/videos/stock-item/download/{asset_id}", {}, creds)
    mp4 = payload.get("MP4") or {}
    url = mp4.get("_1080p") or mp4.get("_2160p") or mp4.get("_720p")
    if not url:
        raise SystemExit(f"Storyblocks returned no MP4 for {asset_id}: {json.dumps(payload)[:300]}")
    return url


def open_license(license_url: str) -> str | None:
    url = (license_url or "").lower()
    if "publicdomain/zero" in url:
        return "CC0 1.0"
    if "publicdomain" in url:
        return "Public domain"
    if "/by/" in url:
        return "CC BY"
    return None


def archive_seconds(value) -> float:
    """archive.org lengths are either seconds ("83.4") or clock time ("01:23")."""
    try:
        parts = [float(p) for p in str(value or 0).split(":")]
    except ValueError:
        return 0.0
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + part
    return round(seconds, 1)


def search_internet_archive(query: str, per_page: int = 10) -> list[dict]:
    # Public domain only: CC BY claims on archive.org are often re-uploads of
    # someone else's work (TV rips, YouTube mirrors), so they are not trusted here.
    q = f"({query}) AND mediatype:movies AND licenseurl:*publicdomain*"
    payload = get_json(ARCHIVE_SEARCH + "?" + urllib.parse.urlencode([
        ("q", q), ("fl[]", "identifier"), ("fl[]", "title"), ("fl[]", "creator"),
        ("fl[]", "licenseurl"), ("rows", per_page), ("output", "json")]))
    results = []
    for doc in payload.get("response", {}).get("docs", []):
        license_name = open_license(doc.get("licenseurl", ""))
        if not license_name:
            continue
        identifier = doc["identifier"]
        files = get_json(f"https://archive.org/metadata/{identifier}").get("files", [])
        mp4s = [f for f in files if f.get("name", "").lower().endswith(".mp4")]
        if not mp4s:
            continue
        selected = max(mp4s, key=lambda f: int(f.get("size", 0) or 0))
        creator = doc.get("creator", "Unknown")
        results.append({
            "candidate_id": f"archive-{identifier}",
            "provider": "internet_archive",
            "asset_id": identifier,
            "page_url": f"https://archive.org/details/{identifier}",
            "creator": creator if isinstance(creator, str) else "; ".join(creator),
            "license": license_name,
            "license_url": doc.get("licenseurl", ""),
            "attribution_required": license_name == "CC BY",
            "duration_seconds": archive_seconds(selected.get("length")),
            "width": int(selected.get("width", 0) or 0),
            "height": int(selected.get("height", 0) or 0),
            "download_url": "https://archive.org/download/{}/{}".format(
                identifier, urllib.parse.quote(selected["name"])),
        })
    return results


def search_wikimedia(query: str, per_page: int = 10) -> list[dict]:
    payload = get_json(COMMONS_API + "?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"filetype:video {query}", "gsrnamespace": 6, "gsrlimit": per_page,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata|mime"}))
    results = []
    for page in payload.get("query", {}).get("pages", {}).values():
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        license_name = open_license(meta.get("LicenseUrl", {}).get("value", "")) or (
            "Public domain" if meta.get("License", {}).get("value", "") in {"pd", "cc0"} else None)
        if not license_name or not info.get("url"):
            continue
        artist = html.unescape(meta.get("Artist", {}).get("value", "Unknown"))
        results.append({
            "candidate_id": f"wikimedia-{page['pageid']}",
            "provider": "wikimedia",
            "asset_id": page["title"],
            "page_url": info.get("descriptionurl", ""),
            "creator": artist[:200],
            "license": license_name,
            "license_url": meta.get("LicenseUrl", {}).get("value", ""),
            "attribution_required": license_name == "CC BY",
            "duration_seconds": round(float(info.get("duration", 0) or 0), 1),
            "width": info.get("width", 0),
            "height": info.get("height", 0),
            "download_url": info["url"],
            "needs_transcode": not info.get("mime", "").endswith("mp4"),
        })
    return results


def provider_search(provider: str, query: str) -> list[dict]:
    if provider == "pexels":
        key = env_key("PEXELS_API_KEY")
        return search_pexels(query, key) if key else []
    if provider == "pixabay":
        key = env_key("PIXABAY_API_KEY")
        return search_pixabay(query, key) if key else []
    if provider == "storyblocks":
        creds = storyblocks_credentials()
        return search_storyblocks(query, creds) if creds else []
    if provider == "internet_archive":
        return search_internet_archive(query)
    if provider == "wikimedia":
        return search_wikimedia(query)
    raise SystemExit(f"Unknown provider {provider}")


def fetch_candidate(candidate: dict, destination: Path) -> None:
    """Download a candidate to an H.264 .mp4 the review page and edit can read."""
    if not candidate.get("needs_transcode"):
        download(candidate["download_url"], destination)
        return
    source = destination.with_suffix(".src")
    download(candidate["download_url"], source)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(source),
                    "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", str(destination)], check=True)
    source.unlink()


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


def search(script_path: Path, limit: int, providers: list[str] | None) -> None:
    episode_dir = script_path.parent
    manifest_path = episode_dir / "footage_manifest.json"
    manifest = load_json(manifest_path)
    active = [p for p in STOCK_PROVIDERS if not providers or p in providers]
    missing = [p for p, ok in (("pexels", env_key("PEXELS_API_KEY")),
                               ("pixabay", env_key("PIXABAY_API_KEY")),
                               ("storyblocks", storyblocks_credentials())) if p in active and not ok]
    for provider in missing:
        print(f"Skipping {provider}: credentials not set", file=sys.stderr)
    output_dir = episode_dir / "footage" / "candidates"
    output_dir.mkdir(parents=True, exist_ok=True)
    previous = {g["manifest_id"]: g for g in load_optional(episode_dir / "footage_candidates.json").get("entries", [])}
    ledger = {"episode": manifest.get("episode"), "generated_at": now_iso(), "entries": []}
    for entry in manifest.get("entries", []):
        role_providers = [p for p in ROLE_PROVIDERS.get(entry.get("role"), []) if p in active]
        manual = [c for c in previous.get(entry["id"], {}).get("candidates", []) if c.get("manual")]
        if not role_providers:
            ledger["entries"].append({
                "manifest_id": entry["id"], "route": "capture_or_artifact",
                "reason": f"{entry.get('role')} must use original capture, source evidence, or licensed brand material",
                "candidates": manual,
            })
            continue
        candidates_by_id = {}
        for query in [q for q in entry.get("query_variants", []) if q]:
            for provider in role_providers:
                try:
                    found = provider_search(provider, query)
                except (OSError, ValueError) as error:
                    print(f"{provider} search failed for {query!r}: {error}", file=sys.stderr)
                    continue
                for candidate in found:
                    candidate = candidates_by_id.setdefault(candidate["candidate_id"], candidate)
                    candidate.setdefault("matched_queries", []).append(query)
        ranked = sorted(candidates_by_id.values(), key=candidate_score, reverse=True)
        # A single staged shoot often occupies most of a provider's first page.
        # Cap each creator so the review surface contains genuinely distinct
        # visual hypotheses rather than nine angles from one production.
        creator_counts: dict[str, int] = {}
        provider_counts: dict[str, int] = {}
        candidates = []
        for candidate in ranked:
            creator = f"{candidate['provider']}:{candidate.get('creator', 'Unknown')}"
            if creator_counts.get(creator, 0) >= 2 or provider_counts.get(candidate["provider"], 0) >= limit:
                continue
            candidates.append(candidate)
            creator_counts[creator] = creator_counts.get(creator, 0) + 1
            provider_counts[candidate["provider"]] = provider_counts.get(candidate["provider"], 0) + 1
        fetched = []
        for candidate in candidates:
            destination = output_dir / f"{entry['id']}--{candidate['candidate_id']}.mp4"
            try:
                if not destination.exists():
                    fetch_candidate(candidate, destination)
            except (OSError, subprocess.CalledProcessError) as error:
                print(f"Download failed for {candidate['candidate_id']}: {error}", file=sys.stderr)
                continue
            candidate["local_path"] = str(destination.relative_to(episode_dir))
            candidate["sha256"] = file_sha256(destination)
            candidate["downloaded_at"] = now_iso()
            candidate.pop("download_url", None)
            fetched.append(candidate)
        ledger["entries"].append({
            "manifest_id": entry["id"], "route": "licensed_contextual_stock",
            "candidates": manual + fetched,
        })
    out = episode_dir / "footage_candidates.json"
    out.write_text(json.dumps(ledger, indent=2) + "\n")
    review = write_review(ledger, episode_dir, script_path)
    print(f"Wrote {out} and {review}; candidates remain unapproved")


def load_optional(path: Path) -> dict:
    return load_json(path) if path.exists() else {}


def add_manual(script_path: Path, manifest_id: str, file_path: Path, source: str,
               company: str, page_url: str, terms_url: str, terms: str) -> None:
    """Register a hand-downloaded file (press kit, Storyblocks web download) as a candidate."""
    episode_dir = script_path.parent
    manifest = load_json(episode_dir / "footage_manifest.json")
    entry = next((e for e in manifest.get("entries", []) if e.get("id") == manifest_id), None)
    if entry is None:
        raise SystemExit(f"Unknown manifest id: {manifest_id}")
    if source == "press_kit" and entry.get("role") not in PRESS_ROLES:
        raise SystemExit(f"Press material cannot fill a {entry.get('role')} beat; use capture or source evidence")
    if not file_path.is_file():
        raise SystemExit(f"No such file: {file_path}")
    output_dir = episode_dir / "footage" / "candidates"
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = "".join(ch if ch.isalnum() else "-" for ch in company.lower()).strip("-")
    candidate_id = f"{source.replace('_', '-')}-{slug}-{file_sha256(file_path)[:8]}"
    destination = output_dir / f"{manifest_id}--{candidate_id}{file_path.suffix.lower()}"
    shutil.copyfile(file_path, destination)
    candidate = {
        "candidate_id": candidate_id,
        "provider": source,
        "asset_id": file_path.name,
        "page_url": page_url,
        "creator": company,
        "license": terms,
        "license_url": terms_url,
        "duration_seconds": round(media_duration(destination), 1),
        "local_path": str(destination.relative_to(episode_dir)),
        "sha256": file_sha256(destination),
        "downloaded_at": now_iso(),
        "manual": True,
    }
    ledger_path = episode_dir / "footage_candidates.json"
    ledger = load_optional(ledger_path) or {"episode": manifest.get("episode"), "entries": []}
    group = next((g for g in ledger["entries"] if g.get("manifest_id") == manifest_id), None)
    if group is None:
        group = {"manifest_id": manifest_id, "route": "manual", "candidates": []}
        ledger["entries"].append(group)
    group["candidates"] = [c for c in group["candidates"] if c["candidate_id"] != candidate_id] + [candidate]
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")
    write_review(ledger, episode_dir, script_path)
    print(f"Added {candidate_id} to {manifest_id}; review it, then approve")


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
    if candidate.get("proxy_only"):
        # Only the approved Storyblocks select spends a subscription download.
        creds = storyblocks_credentials()
        if not creds:
            raise SystemExit("Storyblocks credentials are not set; cannot fetch the licensed master")
        master = episode_dir / candidate["local_path"].replace(".mp4", "--master.mp4")
        download(storyblocks_master(candidate["asset_id"], creds), master)
        candidate.update({"local_path": str(master.relative_to(episode_dir)),
                          "sha256": file_sha256(master), "downloaded_at": now_iso(),
                          "proxy_only": False})
        candidates_path.write_text(json.dumps(ledger, indent=2) + "\n")
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
        "attribution_required": candidate.get("attribution_required", False),
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
    search_p.add_argument("--limit", type=int, default=3, help="Candidates per provider per beat.")
    search_p.add_argument("--providers", nargs="+", choices=STOCK_PROVIDERS,
                          help="Restrict to these providers (default: every provider with credentials).")
    add_p = sub.add_parser("add", help="Register a hand-downloaded file with its provenance.")
    add_p.add_argument("script")
    add_p.add_argument("manifest_id")
    add_p.add_argument("file")
    add_p.add_argument("--source", required=True, choices=("press_kit", "storyblocks"))
    add_p.add_argument("--company", required=True, help="Rights holder, e.g. the company whose newsroom it came from.")
    add_p.add_argument("--page-url", required=True, help="Page the file was downloaded from.")
    add_p.add_argument("--terms-url", required=True, help="Media-use terms or written permission record.")
    add_p.add_argument("--terms", required=True, help='Short license statement, e.g. "Press kit: editorial use permitted".')
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
        search(script_path, args.limit, args.providers)
    elif args.command == "add":
        add_manual(script_path, args.manifest_id, Path(args.file).resolve(), args.source,
                   args.company, args.page_url, args.terms_url, args.terms)
    else:
        approve(script_path, args.manifest_id, args.candidate_id,
                args.faces_review, args.source_in, args.source_out)


if __name__ == "__main__":
    main()
