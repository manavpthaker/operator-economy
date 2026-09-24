#!/usr/bin/env python3
"""Refresh only the r3 review page from its immutable revision and encoded builds."""
import argparse
import html
import json
from pathlib import Path

from build_r3 import A, B, D, R, REVISION, FPS, read, verify_bound, mapping


def clock(seconds):
    s = int(seconds)
    return f'{s//60}:{s%60:02d}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, help='Explicit completed full r3 build')
    args = parser.parse_args()
    revision = read(REVISION)
    rows = read(verify_bound(revision['sources']))
    lock_path = B / 'direction/r3-owner-revisions/OWNER-LOCK.json'
    locked = False
    if lock_path.exists():
        lock = read(lock_path)
        for key in ('source', 'brand_preview', 'hospitality_preview', 'selected_paragraph_audio', 'selected_script', 'time_map', 'master_carrier'):
            verify_bound(lock[key])
        locked = lock.get('status') == 'locked_by_owner'
    builds = []
    for path in D.glob('*-BUILD.json'):
        data = read(path)
        if data.get('status') == 'encoded_unverified_review_only' and data.get('record_type') == 'ep009_r3_review_build':
            if verify_bound(data['revision']) != REVISION:
                raise ValueError('Build belongs to another revision')
            verify_bound({'path': data['output'], 'sha256': data['output_sha256']})
            builds.append((path, data))
    if args.build:
        full = next(d for p, d in builds if p.resolve() == args.build.resolve() and d['scope'] == 'full')
    else:
        fulls = [(p, d) for p, d in builds if d['scope'] == 'full']
        full = max(fulls, key=lambda pair: pair[0].stat().st_mtime)[1] if fulls else None
    def url(data):
        return html.escape(str((R / data['output']).relative_to(A / 'qa')))
    videos = ''
    for scope, title in [('brand', 'Shorter brand pause'), ('hospitality', 'Corrected experience, with surrounding narration')]:
        candidates = [(p, d) for p, d in builds if d['scope'] == scope]
        if candidates:
            data = max(candidates, key=lambda pair: pair[0].stat().st_mtime)[1]
            badge = ' <span class="locked">Locked by owner</span>' if locked else ''
            videos += f'<section><h2>{title}{badge}</h2><video controls preload="metadata" src="{url(data)}"></video><p class="muted">{data["total_frames"]/FPS:.2f} seconds · review excerpt</p></section>'
    if full:
        primary = f'<video aria-label="Full episode revision 3" id="episode" controls preload="metadata" src="{url(full)}"></video>'
        state = 'Full revision 3 review draft. The shortened brand pause, corrected experience and new film selections are integrated.'
    else:
        primary = ''
        state = 'The two corrections are ready to review below. The full r3 assembly is waiting for the new film selections.'
    buttons = ''
    for sid, label in [('seg010', 'Brand'), ('seg044', 'Corrected experience'), ('seg057', 'Economics')]:
        row = next(r for r in rows if r['id'] == sid)
        t = max(0, row['output_seconds'][0] - (3 if sid == 'seg044' else 0))
        buttons += f'<button data-time="{t:.9f}" {"" if full else "disabled"}>{label} · {clock(t)}</button>'
    if full and full.get('film_selections'):
        selections = read(verify_bound(full['film_selections']))['selections']
        for selection in sorted(selections, key=lambda s: s['original_frames'][0]):
            t = mapping(selection['original_frames'][0], revision['pickup_frames']) / FPS
            label = html.escape(selection.get('label', selection['id']))
            buttons += f'<button data-time="{t:.9f}">{label} · {clock(t)}</button>'
    all_cues = ''.join(f'<button data-time="{row["output_seconds"][0]:.9f}" {"" if full else "disabled"}>{row["id"]} · {clock(row["output_seconds"][0])}</button>' for row in rows)
    page = f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EP009 · revision 3 review</title>
<style>
:root{{color-scheme:dark;font:16px/1.5 system-ui;background:#111713;color:#f1efdf}}body{{max-width:1120px;margin:0 auto;padding:28px}}h1{{font-size:24px;margin:0 0 8px}}h2{{font-size:18px}}p{{max-width:900px}}.notice{{border-left:4px solid #dbb06b;background:#29251d;padding:12px 18px;margin:16px 0;color:#f0dbb8}}video{{display:block;width:100%;background:#000;border-radius:5px}}nav{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}}button{{background:#25372c;color:#f1efdf;border:1px solid #56735f;border-radius:5px;padding:10px 14px;cursor:pointer}}button:hover{{background:#36533f}}button:disabled{{opacity:.45;cursor:default}}.muted{{color:#b7c0b6;font-size:14px}}a{{color:#c4dfca}}.clips{{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:24px}}details{{margin:24px 0}}
</style>
<style>.locked{{display:inline-block;font-size:12px;font-weight:600;letter-spacing:.02em;background:#234b38;color:#d9efdb;border:1px solid #4f8061;border-radius:4px;padding:3px 7px;margin-left:6px;vertical-align:middle}}</style>
<h1>EP009 · Direct booking recovery</h1>
<p>Revision 3 · {clock(round(revision['total_frames']/FPS))} runtime</p>
<p>{state}</p>
<div class="notice"><strong>Presenter production is unfinished.</strong> Fourteen presenter segments retain the r1 footage. The corrected hospitality paragraph uses the locked L3 still with a visible “corrected narration · presenter pending” label. These are review placeholders, not finished presenter delivery. Lip-sync restoration remains pending.</div>
{primary}<nav aria-label="Jump to revised passages">{buttons}</nav>
<div class="clips">{videos}</div>
<details><summary>All 75 mapped segment starts</summary><nav aria-label="Every mapped segment">{all_cues}</nav></details>
<p>The brand pause is 3.25 seconds shorter. The experience paragraph now states ten years in hospitality, including Ace Hotel and Standard Hotels, while keeping the uncertainty about selling this specific service.</p>
<p class="muted">{'Brand pause and corrected experience are locked. Presenter delivery and new film remain under review.' if locked else 'Presenter delivery and new film remain under review.'} <a href="ep009-r2-review.html">Original r2 is retained.</a></p>
<script>const episode=document.getElementById('episode');document.querySelectorAll('[data-time]').forEach(b=>b.addEventListener('click',()=>{{if(episode){{episode.currentTime=Number(b.dataset.time);episode.play();}}}}));</script>
</html>'''
    path = A / 'qa/ep009-r3-review.html'
    path.write_text(page)
    print(json.dumps({'page': str(path), 'full_video_available': full is not None, 'mapped_jump_count': 75, 'total_frames': revision['total_frames']}))


if __name__ == '__main__':
    main()
