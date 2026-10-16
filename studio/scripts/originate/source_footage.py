#!/usr/bin/env python3
"""Search contextual footage proxies and promote a reviewed candidate.

Sources, by footage role (see docs/blueprint-cinema.md, Evidence, Footage, and Synthetic Media):

  human_context, outcome  pexels, pixabay, storyblocks, internet_archive, wikimedia, nasa,
                          plus stills (wikimedia_stills, met, artic, nasa_stills)
  market_force            internet_archive, wikimedia, nasa, the stills, plus manually added press kits
  proof, process          never searched; original capture or source evidence only

Stills are photographs and artworks from open collections. Each one is kept as the
original image (`still_path`, for HyperFrames builds that move it themselves) and
rendered into an 8-second 1920x1080 push-in (`local_path`), so review, approve,
validate and the Remotion B-roll scene treat it like any other clip.

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
import http.client
import json
import os
import re
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
NASA_API = "https://images-api.nasa.gov/search"
NASA_TERMS = "https://www.nasa.gov/nasa-brand-center/images-and-media/"
MET_SEARCH = "https://collectionapi.metmuseum.org/public/collection/v1.1/search"
MET_OBJECT = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
ARTIC_SEARCH = "https://api.artic.edu/api/v1/artworks/search"
CC0_URL = "https://creativecommons.org/publicdomain/zero/1.0/"
USER_AGENT = "OperatorEconomy/1.0 (+https://theoperatoreconomy.com)"
STILL_SECONDS = 8
STILL_FPS = 30
NASA_RIGHTS_NOTE = ("NASA media is not copyrighted, but NASA insignia may not appear, "
                    "identifiable people may not imply endorsement, and any third-party "
                    "credit in the description is not covered.")

STILL_PROVIDERS = ["wikimedia_stills", "met", "artic", "nasa_stills"]
ARCHIVAL_PROVIDERS = ["internet_archive", "wikimedia", "nasa"] + STILL_PROVIDERS
STOCK_PROVIDERS = ["pexels", "pixabay", "storyblocks"] + ARCHIVAL_PROVIDERS
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


def plain_text(value: str) -> str:
    """Commons metadata is HTML (artist links, bdi tags); keep the words."""
    return html.unescape(re.sub(r"<[^>]+>", "", value or "")).strip() or "Unknown"


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
        artist = plain_text(meta.get("Artist", {}).get("value", "Unknown"))
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


def search_wikimedia_stills(query: str, per_page: int = 10) -> list[dict]:
    payload = get_json(COMMONS_API + "?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"filetype:bitmap filew:>1599 {query}", "gsrnamespace": 6, "gsrlimit": per_page,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata|mime", "iiurlwidth": 1920}))
    results = []
    for page in payload.get("query", {}).get("pages", {}).values():
        info = (page.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        license_name = open_license(meta.get("LicenseUrl", {}).get("value", "")) or (
            "Public domain" if meta.get("License", {}).get("value", "") in {"pd", "cc0"} else None)
        if not license_name or not info.get("url"):
            continue
        artist = plain_text(meta.get("Artist", {}).get("value", "Unknown"))
        restrictions = meta.get("Restrictions", {}).get("value", "")
        results.append(still_candidate(
            f"wikimedia-still-{page['pageid']}", "wikimedia_stills", page["title"],
            info.get("descriptionurl", ""), artist[:200], license_name,
            meta.get("LicenseUrl", {}).get("value", ""), info.get("width", 0), info.get("height", 0),
            info.get("thumburl") or info["url"],
            f"Restrictions named on the source page: {restrictions}" if restrictions else ""))
    return results


def search_met(query: str, per_page: int = 8) -> list[dict]:
    """The Met's open-access objects: public domain works only, released as CC0."""
    payload = get_json(MET_SEARCH + "?" + urllib.parse.urlencode(
        {"q": query, "hasImages": "true", "limit": per_page * 2}))
    results = []
    for object_id in (payload.get("objectIDs") or [])[:per_page * 2]:
        try:
            obj = get_json(f"{MET_OBJECT}{object_id}")
        except (OSError, ValueError):
            continue
        if not obj.get("isPublicDomain") or not obj.get("primaryImage"):
            continue
        creator = obj.get("artistDisplayName") or obj.get("culture") or "The Metropolitan Museum of Art"
        results.append(still_candidate(
            f"met-{object_id}", "met", str(object_id),
            obj.get("objectURL") or f"https://www.metmuseum.org/art/collection/search/{object_id}",
            f"{creator}, {obj.get('title', 'Untitled')} ({obj.get('objectDate', 'n.d.')})"[:200],
            "CC0 1.0", CC0_URL, 0, 0, obj["primaryImage"]))
        if len(results) >= per_page:
            break
    return results


def search_artic(query: str, per_page: int = 8) -> list[dict]:
    """Art Institute of Chicago: public domain works, released as CC0."""
    params = {"query": {"bool": {
        "must": [{"multi_match": {"query": query, "type": "cross_fields", "operator": "and",
                                  "fields": ["title^3", "subject_titles^2", "term_titles^2",
                                             "classification_titles", "place_of_origin"]}}],
        "filter": [{"term": {"is_public_domain": True}}, {"exists": {"field": "image_id"}}]}},
        "fields": ["id", "title", "artist_display", "date_display", "image_id",
                   "is_public_domain", "thumbnail"], "limit": per_page}
    payload = get_json(ARTIC_SEARCH + "?" + urllib.parse.urlencode({"params": json.dumps(params)}),
                       headers={"AIC-User-Agent": USER_AGENT})
    iiif = (payload.get("config") or {}).get("iiif_url", "https://www.artic.edu/iiif/2")
    results = []
    for item in payload.get("data", []):
        if not item.get("image_id") or item.get("is_public_domain") is False:
            continue
        thumb = item.get("thumbnail") or {}
        width = min(int(thumb.get("width") or 1686), 1686)
        height = round(int(thumb.get("height") or 0) * width / int(thumb.get("width") or 1)) if thumb.get("height") else 0
        artist = str(item.get("artist_display") or "Unknown").split("\n")[0]
        results.append(still_candidate(
            f"artic-{item['id']}", "artic", str(item["id"]),
            f"https://www.artic.edu/artworks/{item['id']}",
            f"{artist}, {item.get('title', 'Untitled')} ({item.get('date_display', 'n.d.')})"[:200],
            "CC0 1.0", CC0_URL, width, height,
            f"{iiif}/{item['image_id']}/full/{width},/0/default.jpg"))
    return results


def nasa_items(query: str, media_type: str, per_page: int) -> list[tuple[dict, list[str]]]:
    payload = get_json(NASA_API + "?" + urllib.parse.urlencode(
        {"q": query, "media_type": media_type, "page_size": per_page}))
    items = []
    for item in payload.get("collection", {}).get("items", []):
        data = (item.get("data") or [{}])[0]
        text = " ".join(str(data.get(k, "")) for k in ("description", "secondary_creator", "photographer"))
        if "©" in text or "copyright" in text.lower():
            continue  # third-party material inside NASA's library is not NASA's to release
        try:
            files = get_json(nasa_url(item["href"]))
        except (OSError, ValueError, KeyError, http.client.HTTPException):
            continue
        items.append((data, [nasa_url(f) for f in files]))
    return items


def nasa_url(url: str) -> str:
    """NASA's asset paths carry raw spaces; keep existing escapes, encode the rest."""
    return urllib.parse.quote(str(url).replace("http://", "https://", 1), safe=":/~%?=&")


def nasa_credit(data: dict) -> str:
    return (data.get("photographer") or data.get("secondary_creator")
            or f"NASA {data.get('center', '')}".strip())[:200]


def search_nasa(query: str, per_page: int = 6) -> list[dict]:
    results = []
    for data, files in nasa_items(query, "video", per_page):
        mp4 = next((f for suffix in ("~large.mp4", "~orig.mp4", "~medium.mp4")
                    for f in files if f.endswith(suffix)), None)
        if not mp4:
            continue
        results.append({
            "candidate_id": f"nasa-{data['nasa_id']}", "provider": "nasa",
            "asset_id": data["nasa_id"], "title": data.get("title", ""),
            "page_url": f"https://images.nasa.gov/details/{urllib.parse.quote(data['nasa_id'])}",
            "creator": nasa_credit(data), "license": "Public domain (NASA media guidelines)",
            "license_url": NASA_TERMS, "attribution_required": False,
            "rights_notes": NASA_RIGHTS_NOTE, "duration_seconds": 0, "width": 0, "height": 0,
            "download_url": mp4,
        })
    return results


def search_nasa_stills(query: str, per_page: int = 6) -> list[dict]:
    results = []
    for data, files in nasa_items(query, "image", per_page):
        jpg = next((f for suffix in ("~large.jpg", "~orig.jpg", "~medium.jpg")
                    for f in files if f.endswith(suffix)), None)
        if not jpg:
            continue
        results.append(still_candidate(
            f"nasa-still-{data['nasa_id']}", "nasa_stills", data["nasa_id"],
            f"https://images.nasa.gov/details/{urllib.parse.quote(data['nasa_id'])}",
            nasa_credit(data), "Public domain (NASA media guidelines)", NASA_TERMS, 0, 0, jpg,
            NASA_RIGHTS_NOTE))
    return results


def still_candidate(candidate_id: str, provider: str, asset_id: str, page_url: str, creator: str,
                    license_name: str, license_url: str, width: int, height: int,
                    image_url: str, rights_notes: str = "") -> dict:
    return {
        "candidate_id": candidate_id, "provider": provider, "asset_id": asset_id,
        "media_kind": "still", "page_url": page_url, "creator": creator,
        "license": license_name, "license_url": license_url,
        "attribution_required": license_name == "CC BY",
        "rights_notes": rights_notes, "duration_seconds": STILL_SECONDS,
        "width": width, "height": height, "download_url": image_url,
    }


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
    if provider == "wikimedia_stills":
        return search_wikimedia_stills(query)
    if provider == "met":
        return search_met(query)
    if provider == "artic":
        return search_artic(query)
    if provider == "nasa":
        return search_nasa(query)
    if provider == "nasa_stills":
        return search_nasa_stills(query)
    raise SystemExit(f"Unknown provider {provider}")


def fetch_candidate(candidate: dict, destination: Path) -> None:
    """Download a candidate to an H.264 .mp4 the review page and edit can read."""
    if candidate.get("media_kind") == "still":
        still = still_path_for(destination)
        if not still.exists():
            download(candidate["download_url"], still)
        render_push_in(still, destination)
        return
    if not candidate.get("needs_transcode"):
        download(candidate["download_url"], destination)
        return
    source = destination.with_suffix(".src")
    download(candidate["download_url"], source)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(source),
                    "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", str(destination)], check=True)
    source.unlink()


def still_path_for(clip: Path) -> Path:
    return clip.with_name(clip.stem + "--still.jpg")


def render_push_in(still: Path, destination: Path) -> None:
    """A slow 8% push-in over STILL_SECONDS, cropped to fill 16:9.

    A tall picture is cropped from its upper third, where faces and horizons sit,
    and rendered at twice the output size first so the zoom does not step."""
    frames = STILL_SECONDS * STILL_FPS
    zoom = f"zoompan=z='1+0.08*on/{frames}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(still), "-vf",
        "scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160:(iw-3840)/2:(ih-2160)/3,"
        f"{zoom}:s=1920x1080:fps={STILL_FPS},format=yuv420p",
        "-frames:v", str(frames), "-c:v", "libx264", "-crf", "16", "-an", str(destination)],
        check=True)


def download(url: str, destination: Path) -> None:
    headers = {"User-Agent": USER_AGENT}
    if urllib.parse.urlparse(url).hostname == "www.artic.edu":
        headers["AIC-User-Agent"] = USER_AGENT  # its image server refuses requests without it
    request = urllib.request.Request(url, headers=headers)
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
            kind = " · still, push-in" if candidate.get("media_kind") == "still" else ""
            notes = (f"<p class='route'>{html.escape(candidate['rights_notes'])}</p>"
                     if candidate.get("rights_notes") else "")
            candidates.append(
                f"<article><video controls muted preload='metadata' src='{src}'></video>"
                f"<h3>{html.escape(candidate['candidate_id'])}{kind}</h3>{notes}"
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
            if candidate.get("media_kind") == "still":
                candidate["still_path"] = str(still_path_for(destination).relative_to(episode_dir))
            elif not candidate.get("duration_seconds"):
                candidate["duration_seconds"] = round(media_duration(destination), 1)
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
        "media_kind": candidate.get("media_kind", "video"),
        "faces_review": faces_review,
        "source_in": source_in,
        "source_out": round(selected_out, 3),
    })
    for key in ("still_path", "rights_notes"):
        if candidate.get(key):
            entry[key] = candidate[key]
        else:
            entry.pop(key, None)
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
