#!/usr/bin/env python3
"""Verify sources, exact reference WAVs and diagnostic audio policy; never grant approval."""
import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
import wave
from html.parser import HTMLParser
from pathlib import Path

PROJECT = Path(__file__).resolve().parent


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []

    def handle_starttag(self, tag, attrs):
        self.items.append((tag, dict(attrs)))


def read_pcm(path, start=0, count=None):
    with wave.open(str(path), 'rb') as stream:
        fmt = (stream.getframerate(), stream.getnchannels(), stream.getsampwidth())
        stream.setpos(start)
        return fmt, stream.readframes(stream.getnframes() - start if count is None else count)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--allow-pending', action='store_true')
    parser.add_argument('--decode', action='store_true')
    parser.add_argument('--require-reviewed-selects', action='store_true',
                        help='Block preview while source selection remains pending; reviewed failed diagnostics are permitted.')
    args = parser.parse_args()
    errors, pending, media = [], [], []
    source_manifest = json.loads((PROJECT.parent / 'INPUT-MANIFEST.json').read_text())
    sources = {entry['id']: entry for entry in source_manifest['assets']}
    staged = json.loads((PROJECT / 'STAGED-ASSETS.json').read_text())
    for entry in staged['assets']:
        local = PROJECT / entry['local_path']
        if not local.is_file():
            errors.append(f'Missing retained asset: {entry["local_path"]}')
        elif sha(local) != entry['sha256']:
            errors.append(f'Retained asset changed: {entry["local_path"]}')
    master = Path(sources['narration_master']['path'])
    if sha(master) != sources['narration_master']['sha256']:
        errors.append('Authoritative narration master hash changed')
    for local_name, start, count in [('opening-exact.wav', 524160, 1612000),
                                      ('presenter-exact.wav', 28370400, 268800)]:
        if read_pcm(PROJECT / 'public/audio' / local_name) != read_pcm(master, start, count):
            errors.append(f'{local_name}: PCM or format mismatch')
    page = Elements()
    page.feed((PROJECT / 'index.html').read_text())
    by_id = {attr.get('id'): (tag, attr) for tag, attr in page.items if attr.get('id')}
    root = by_id['hg-root'][1]
    total = float(root['data-duration'])
    if root.get('data-fps') != '24' or not math.isclose(total * 24, 975, abs_tol=1e-7):
        errors.append('Diagnostic review total is not 975 frames at24fps')
    picture = sorted((float(attr['data-start']), float(attr['data-duration']), attr.get('id'))
                     for _, attr in page.items if attr.get('data-track-index') == '1')
    cursor = 0.0
    for start, duration, ident in picture:
        if not math.isclose(start, cursor, abs_tol=1e-8):
            errors.append(f'Picture gap/overlap before {ident}: {cursor} to {start}')
        cursor = start + duration
    if not math.isclose(cursor, total, abs_tol=1e-8):
        errors.append('Picture does not cover complete review')
    audio_windows = [(float(attr['data-start']), float(attr['data-duration']))
                     for tag, attr in page.items if tag == 'audio']
    wanted_audio = [(0, 806/24), (830/24, 5.952)]
    if len(audio_windows) != 2 or any(not math.isclose(x, y, abs_tol=1e-8)
            for got, want in zip(audio_windows, wanted_audio) for x, y in zip(got, want)):
        errors.append('Opening narration or raw provider-audio windows changed')
    sound_sources = [attr.get('src') for tag,attr in page.items if tag == 'audio']
    if sound_sources != ['public/audio/opening-exact.wav','public/media/higgsfield-p-presenter.mp4']:
        errors.append('Diagnostic sound policy changed: P must use its own returned audio, never exact-WAV dubbing')
    decisions = json.loads((PROJECT / 'EDIT-DECISIONS.json').read_text())
    for select in decisions['selections']:
        attr = by_id[select['html_id']][1]
        if select.get('source_sha256') and (PROJECT / attr['src']).is_file() and sha(PROJECT / attr['src']) != select['source_sha256']:
            errors.append(f'{select["html_id"]}: reviewed source hash changed')
        for field, expected in [('data-start',select['record_in']),
                                ('data-duration',select['record_duration']),
                                ('data-media-start',select['source_in'])]:
            if not math.isclose(float(attr[field]), expected, abs_tol=1e-8):
                errors.append(f'{select["html_id"]}: {field} disagrees with edit decisions')
    for tag, attr in page.items:
        for key in ('src', 'data-composition-src'):
            if key not in attr:
                continue
            value = attr[key]
            if re.match(r'^[a-z]+://', value):
                errors.append(f'Remote render dependency: {value}')
            path = PROJECT / value
            if not path.is_file():
                if path.name in {'higgsfield-c-owner-response.mp4','higgsfield-p-presenter.mp4'}:
                    pending.append(value)
                else:
                    errors.append(f'Missing dependency: {value}')
            elif tag == 'video':
                probe = subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,text=True)
                if probe.returncode:
                    errors.append(f'Probe failed: {value}')
                    continue
                data = json.loads(probe.stdout)
                video = next((s for s in data['streams'] if s['codec_type']=='video'), None)
                if not video:
                    errors.append(f'No picture stream: {value}')
                    continue
                duration = float(video.get('duration', data['format'].get('duration', 0)))
                required = float(attr.get('data-media-start',0)) + float(attr['data-duration'])
                if duration + 1e-6 < required:
                    errors.append(f'Source too short: {value}, {duration} < {required}')
                if 'muted' not in attr:
                    errors.append(f'Embedded source sound enabled: {value}')
                report = {'path':value,'sha256':sha(path),'duration_seconds':duration,
                          'width':video['width'],'height':video['height'],'frame_rate':video['r_frame_rate'],
                          'source_in':float(attr.get('data-media-start',0)),
                          'source_out_exclusive':required,'audio_streams':sum(s['codec_type']=='audio' for s in data['streams'])}
                if args.decode:
                    decoded = subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-f','null','-'],capture_output=True,text=True)
                    report['full_decode_passed'] = decoded.returncode == 0 and not decoded.stderr.strip()
                    if not report['full_decode_passed']:
                        errors.append(f'Decode errors: {value}: {decoded.stderr[:500]}')
                media.append(report)
    model = (PROJECT / 'compositions/owner-dependency.html').read_text()
    if sha(PROJECT / 'compositions/owner-dependency.html') != sources['working_model_composition']['sha256']:
        errors.append('Working Model changed from pinned R9 input')
    if 'data-composition-id="ep007-r9-owner-dependency"' not in model:
        errors.append('Working Model host identity mismatch')
    ids = [attr['id'] for _,attr in page.items if 'id' in attr]
    for composition in (PROJECT / 'compositions').glob('*.html'):
        child = Elements();child.feed(composition.read_text())
        ids += [attr['id'] for _,attr in child.items if 'id' in attr]
    if len(ids) != len(set(ids)):
        errors.append('Global DOM ids collide')
    unreviewed = [entry['html_id'] for entry in decisions['selections'] if not entry['reviewed']]
    if args.require_reviewed_selects and unreviewed:
        errors.append('Source performance/audio review still pending: ' + ', '.join(unreviewed))
    result = {'status':'failed' if errors else ('pending_media' if pending else 'mechanical_inputs_passed'),
              'errors':errors,'pending_media':sorted(set(pending)), 'source_selects_pending_review':unreviewed,
              'picture_contiguous':not any('gap/overlap' in e for e in errors),
              'review_fps':24,'review_frames':975,'duration_seconds':total,
              'reference_wavs_pcm_match_master':not any('PCM' in e for e in errors),
              'audio_policy':'Original opening narration; full raw P uses its own returned sound. Original presenter WAV is reference-only.',
              'presenter_exact_audio_fidelity':'FAIL; shown as diagnostic, not dubbed',
              'working_model_byte_identical':not any('Working Model changed' in e for e in errors),
              'retained_assets_checked':len(staged['assets']),'media':media,
              'composition_sha256':sha(PROJECT/'index.html'),
              'edit_decisions_sha256':sha(PROJECT/'EDIT-DECISIONS.json'),
              'subcomposition_sha256':{str(p.relative_to(PROJECT)):sha(p) for p in sorted((PROJECT/'compositions').glob('*.html'))},
              'creativeApproval':False,'productionGateAdvance':False,'rendered':False,
              'note':'Mechanical input checks do not establish performance, lip sync, owner preference or full HyperFrames runtime validity.'}
    (PROJECT/'reports').mkdir(exist_ok=True)
    (PROJECT/'reports/verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return 1 if errors else (2 if pending and not args.allow_pending else 0)


if __name__ == '__main__':
    sys.exit(run())
