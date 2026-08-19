#!/usr/bin/env python3
"""Build a source-and-footage candidate review from an episode candidate ledger."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def find_candidate(base: Path, pexels_id: str, suffix: str) -> Path | None:
    matches = sorted((base / "footage_candidates").glob(f"*/pexels-{pexels_id}.{suffix}"))
    return matches[0] if matches else None


def rel(path: Path | None, base: Path) -> str | None:
    return path.relative_to(base).as_posix() if path else None


def build(base: Path) -> Path:
    data = json.loads((base / "source_candidates.json").read_text())
    source_cards = []
    for source in data["sources"]:
        source_cards.append(
            f"""<article class=\"source-card\">
  <div class=\"eyebrow\">{h(source['kind'].replace('_', ' '))} · {h(source['id'])}</div>
  <h2>{h(source['title'])}</h2>
  <p>{h(source['use'])}</p>
  <dl><dt>Publisher</dt><dd>{h(source['publisher'])}</dd><dt>Rights</dt><dd>{h(source['rights_status'].replace('_', ' '))}</dd><dt>Coverage</dt><dd>{h(', '.join(source['asset_ids']))}</dd></dl>
  <a href=\"{h(source['canonical_url'])}\" target=\"_blank\" rel=\"noreferrer\">Open canonical source ↗</a>
</article>"""
        )

    footage_groups = []
    for group in data["footage_candidates"]:
        decision = group.get("decision", "unreviewed")
        selected_id = group.get("selected_id")
        cards = []
        for pexels_id in group["pexels_ids"]:
            image = rel(find_candidate(base, pexels_id, "jpg"), base)
            video = rel(find_candidate(base, pexels_id, "mp4"), base)
            if not image and not video:
                cards.append(f'<div class="clip missing"><strong>Pexels · {h(pexels_id)}</strong><span>Proxy not found locally</span></div>')
                continue
            media = f'<video controls muted preload="metadata" poster="{h(image or "")}" src="{h(video or "")}"></video>' if video else f'<img src="{h(image)}" alt="Contact sheet for Pexels {h(pexels_id)}">'
            selected = pexels_id == selected_id
            state = '<span class="clip-state">Selected</span>' if selected else ''
            cards.append(f'<div class="clip{" selected" if selected else ""}">{media}<strong>Pexels · {h(pexels_id)}</strong>{state}</div>')
        footage_groups.append(
            f"""<section class=\"footage-group\"><div class=\"group-head\"><div><h2>{h(group['asset_id'])}</h2><span class=\"decision {h(decision)}\">{h(decision.replace('_', ' '))}</span></div><p>{h(group['review_note'])}</p></div><div class=\"clip-grid\">{''.join(cards)}</div></section>"""
        )

    document = f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>EP006 source review</title>
<style>
:root{{--ink:#14263e;--paper:#f6f1e7;--white:#fff;--line:#c9c1b4;--accent:#f0a847;--red:#a23a32}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:#171714;font:15px/1.45 Inter,system-ui,sans-serif}}header{{background:var(--ink);color:var(--white);padding:32px clamp(20px,5vw,72px)}}header h1{{font-size:clamp(30px,5vw,58px);margin:0 0 8px}}header p{{max-width:760px;margin:0;color:#d9e0e7}}main{{padding:32px clamp(20px,5vw,72px) 80px}}.status{{display:inline-block;background:var(--accent);color:#171714;padding:5px 9px;font-weight:800;text-transform:uppercase;letter-spacing:.06em;font-size:12px;margin-bottom:18px}}h2{{line-height:1.1}}.section-title{{font-size:28px;margin:42px 0 16px}}.source-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}}.source-card{{background:var(--white);border:1px solid var(--line);padding:20px}}.source-card h2{{font-size:20px;margin:8px 0}}.eyebrow{{text-transform:uppercase;letter-spacing:.08em;font-size:11px;font-weight:800;color:#536273}}dl{{display:grid;grid-template-columns:80px 1fr;gap:5px 10px;font-size:13px}}dt{{font-weight:800}}dd{{margin:0}}a{{color:#174d7d;font-weight:800}}.footage-group{{border-top:2px solid var(--ink);padding-top:16px;margin-top:28px}}.group-head{{display:grid;grid-template-columns:100px 1fr;gap:18px;align-items:start}}.group-head h2,.group-head p{{margin:0}}.clip-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin-top:14px}}.clip{{background:var(--white);border:1px solid var(--line);padding:8px;display:grid;gap:7px}}video,img{{width:100%;aspect-ratio:16/9;object-fit:cover;background:#111}}.clip.selected{{border:4px solid #2d7548}}.clip-state,.decision{{display:inline-block;text-transform:uppercase;letter-spacing:.06em;font-size:11px;font-weight:900}}.clip-state{{color:#2d7548}}.decision{{margin-top:5px;padding:3px 6px;background:#ddd}}.decision.selected{{background:#cce7d6;color:#174a2d}}.decision.shortlisted{{background:#f5ddae;color:#62440b}}.decision.resourcing_required{{background:#f0c5c1;color:#79241d}}.decision.unreviewed{{background:#dfe3e8;color:#46515d}}.missing{{min-height:150px;place-content:center;color:var(--red)}}.warning{{border-left:5px solid var(--accent);background:var(--white);padding:14px 18px;max-width:900px}}@media(max-width:600px){{.group-head{{grid-template-columns:1fr}}}}
</style></head><body>
<header><div class=\"status\">Selection required</div><h1>EP006 source review</h1><p>Coverage is approved. This surface reviews exact evidence, archival context, and footage candidates before any asset advances to selected.</p></header>
<main><div class=\"warning\"><strong>Approval rule:</strong> a source link is not a media license. Historical imagery marked “rights check required” stays blocked until its permitted use is recorded.</div>
<h2 class=\"section-title\">Evidence and archival candidates</h2><div class=\"source-grid\">{''.join(source_cards)}</div>
<h2 class=\"section-title\">Human and property footage</h2>{''.join(footage_groups)}
</main></body></html>"""
    output = base / "SOURCE-REVIEW.html"
    output.write_text(document)
    print(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode_dir", type=Path)
    args = parser.parse_args()
    build(args.episode_dir.resolve())


if __name__ == "__main__":
    main()
