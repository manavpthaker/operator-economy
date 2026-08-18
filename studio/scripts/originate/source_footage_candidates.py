"""Source reviewable Pexels candidates for pending long-form footage beats.

This is a shortlist stage only. It never approves media or mutates the footage
manifest. Candidate proxies are local/ignored; provenance lives in JSON.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import subprocess
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

try:
    from _model import env_key
except ImportError:
    from ._model import env_key

LICENSE = "https://www.pexels.com/license/"


def request_json(url: str, key: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": key, "User-Agent": "Operator-Economy/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read())


def best_proxy(files: list[dict]) -> dict | None:
    mp4 = [f for f in files if f.get("file_type") == "video/mp4" and f.get("width") and f.get("height")]
    landscape = [f for f in mp4 if f["width"] > f["height"]]
    pool = landscape or mp4
    if not pool:
        return None
    # Review needs a useful image without downloading a 4K master.
    return min(pool, key=lambda f: (abs(f["width"] - 1280), -f["width"]))


def download(url: str, path: Path) -> None:
    if path.exists():
        return
    req = urllib.request.Request(url, headers={"User-Agent": "Operator-Economy/1.0"})
    with urllib.request.urlopen(req, timeout=90) as response, path.open("wb") as target:
        while chunk := response.read(1024 * 1024):
            target.write(chunk)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contact_sheet(proxy: Path, output: Path) -> None:
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(proxy),
        "-vf", "fps=1/3,scale=360:-1,tile=4x1:padding=6:margin=6",
        "-frames:v", "1", str(output),
    ], check=True)


def render_review(payload: dict, out: Path) -> None:
    groups = []
    for beat in payload["beats"]:
        cards = []
        for candidate in beat["candidates"]:
            proxy = html.escape(candidate["proxy_rel"])
            cards.append(f'''<article><video controls muted preload="metadata" poster="{html.escape(candidate['contact_sheet_rel'])}"><source src="{proxy}" type="video/mp4"></video><div class="copy"><strong>Pexels · {candidate['asset_id']}</strong><span>{candidate['duration_seconds']}s · {candidate['width']}×{candidate['height']}</span><p>{html.escape(candidate['creator'])}</p><a href="{html.escape(candidate['page_url'])}" target="_blank">Open canonical source ↗</a></div></article>''')
        groups.append(f'''<section><header><div><small>{html.escape(beat['role'])} · {html.escape(beat['id'])}</small><h2>{html.escape(beat['visual_intent'])}</h2><p>{html.escape(beat['narration_anchor'])}</p></div><ol>{''.join(f'<li>{html.escape(q)}</li>' for q in beat['query_variants'])}</ol></header><div class="grid">{''.join(cards) or '<b class="empty">NO SEMANTIC MATCH — source elsewhere</b>'}</div></section>''')
    out.write_text(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>EP006 footage candidates</title><style>:root{{--paper:#f5f0e6;--ink:#181817;--navy:#14263e;--gold:#b78b2d;--line:#cfc6b7}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.45 "Helvetica Neue",sans-serif}}body>header{{padding:44px 4vw;background:var(--navy);color:white}}h1{{font-size:clamp(36px,6vw,82px);line-height:.9;letter-spacing:-.06em;margin:10px 0}}body>header p{{color:#bdc7d2;max-width:800px}}section{{padding:38px 4vw;border-bottom:1px solid var(--line)}}section>header{{display:grid;grid-template-columns:1.7fr 1fr;gap:40px;margin-bottom:22px}}small{{font:700 11px ui-monospace,monospace;text-transform:uppercase;letter-spacing:.12em;color:var(--gold)}}h2{{font-size:25px;line-height:1.05;margin:9px 0}}ol{{font:12px ui-monospace,monospace;margin:0}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}article{{background:white;border:1px solid var(--line)}}video{{display:block;width:100%;aspect-ratio:16/9;background:#0d1724;object-fit:cover}}.copy{{padding:14px}}.copy span,.copy p{{display:block;color:#68645d;margin:4px 0}}a{{color:#214f85;font-weight:700}}.empty{{padding:30px;color:#943f35;border:1px solid #943f35}}@media(max-width:720px){{section>header{{grid-template-columns:1fr}}}}</style></head><body><header><small>Operator Blueprint №006 · footage gate</small><h1>Story-bearing media, not wallpaper.</h1><p>Shortlist only. Approve semantic match, faces, rights, trim, crop, and focal point in the manifest before any clip reaches Remotion.</p></header>{''.join(groups)}</body></html>''')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--per-beat", type=int, default=4)
    args = ap.parse_args()
    key = env_key("PEXELS_API_KEY")
    if not key:
        raise SystemExit("PEXELS_API_KEY is not configured")
    episode = Path(args.script).resolve().parent
    manifest = json.loads((episode / "footage_manifest.json").read_text())
    storyboard = json.loads((episode / "storyboard.json").read_text())
    by_id = {s["id"]: s for s in storyboard["screens"]}
    root = episode / "footage_candidates"
    root.mkdir(exist_ok=True)
    payload = {"schema_version": 1, "provider": "pexels", "license": LICENSE,
               "license_checked_at": date.today().isoformat(), "generated_at": datetime.now(timezone.utc).isoformat(), "beats": []}
    for entry in manifest["entries"]:
        if entry.get("approved"):
            continue
        screen = by_id.get(entry.get("screen_id"), {})
        queries = entry.get("query_variants") or [screen.get("search_query", "")]
        found: dict[str, dict] = {}
        for rank, query in enumerate(queries):
            url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": query, "per_page": 8, "orientation": "landscape"})
            for video in request_json(url, key).get("videos", []):
                proxy_file = best_proxy(video.get("video_files", []))
                if not proxy_file:
                    continue
                score = (3 - rank) * 10 + (3 if 5 <= video.get("duration", 0) <= 30 else 0) + (2 if proxy_file["width"] >= 1280 else 0)
                candidate = {"asset_id": str(video["id"]), "page_url": video.get("url", ""),
                             "creator": video.get("user", {}).get("name", "Unknown"), "duration_seconds": video.get("duration", 0),
                             "width": proxy_file["width"], "height": proxy_file["height"], "download_url": proxy_file["link"],
                             "matched_query": query, "query_rank": rank, "score": score}
                source_id = str(video["id"])
                if source_id not in found or score > found[source_id]["score"]:
                    found[source_id] = candidate
        chosen = sorted(found.values(), key=lambda c: (-c["score"], c["asset_id"]))[:args.per_beat]
        beat_dir = root / entry["id"]
        beat_dir.mkdir(exist_ok=True)
        for candidate in chosen:
            proxy = beat_dir / f"pexels-{candidate['asset_id']}.mp4"
            sheet = beat_dir / f"pexels-{candidate['asset_id']}.jpg"
            download(candidate.pop("download_url"), proxy)
            if not sheet.exists():
                contact_sheet(proxy, sheet)
            candidate.update({"provider": "pexels", "license": LICENSE, "license_checked_at": date.today().isoformat(),
                              "proxy_rel": str(proxy.relative_to(episode)), "contact_sheet_rel": str(sheet.relative_to(episode)),
                              "sha256": sha256(proxy)})
        payload["beats"].append({"id": entry["id"], "screen_id": entry.get("screen_id"), "role": entry["role"],
                                 "narration_anchor": entry["narration_anchor"], "visual_intent": screen.get("visual_intent", ""),
                                 "query_variants": queries, "candidates": chosen})
        print(f"{entry['id']}: {len(chosen)} candidates")
    json_path = episode / "footage_candidates.json"
    html_path = episode / "footage_candidates.html"
    json_path.write_text(json.dumps(payload, indent=2) + "\n")
    render_review(payload, html_path)
    print(f"Candidates → {json_path}\nReview → {html_path}")


if __name__ == "__main__":
    main()
