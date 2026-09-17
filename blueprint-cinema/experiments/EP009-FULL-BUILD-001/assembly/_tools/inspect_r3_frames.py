#!/usr/bin/env python3
"""Extract actual r3 frames at six film inserts and the locked correction seams.

Creates source-comparison metrics and contact sheets. Stills are not playback QA.
Run only after the full r3 output has finished, using syncenv Python.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
from PIL import Image, ImageDraw
from build_r3 import A, R, FPS, read, bound, verify_bound, write

W, H = 640, 360


def expression(frames):
    terms = [f'eq(n,{f})' for f in frames]
    while len(terms) > 1:
        terms = [f'({terms[i]}+{terms[i+1]})' if i+1 < len(terms) else terms[i] for i in range(0, len(terms), 2)]
    return terms[0]


def extract(path, frames):
    frames = sorted(set(frames))
    cmd = ['ffmpeg', '-v', 'error', '-threads', '2', '-i', str(path), '-vf',
           f"select='{expression(frames)}',scale={W}:{H}", '-frames:v', str(len(frames)),
           '-fps_mode', 'passthrough', '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-']
    raw = subprocess.check_output(cmd)
    pictures = np.frombuffer(raw, dtype=np.uint8).reshape(-1, H, W, 3)
    if len(pictures) != len(frames):
        raise ValueError(f'Frame extraction shortfall: {path}')
    return dict(zip(frames, pictures))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('manifest', type=Path)
    ap.add_argument('--directory', type=Path, default=A / 'qa/r3/integration-frames')
    a = ap.parse_args()
    data = read(a.manifest)
    if data['scope'] != 'full' or data['status'] != 'encoded_unverified_review_only':
        raise ValueError('Full encoded r3 build required')
    output = verify_bound({'path': data['output'], 'sha256': data['output_sha256']})
    directory = a.directory.resolve(); directory.relative_to(A)
    if directory.exists():
        raise FileExistsError('Preserve existing frame evidence')
    directory.mkdir(parents=True)
    spans = data['source_spans']
    selections = read(verify_bound(data['film_selections']))['selections']
    groups = []
    for film in selections:
        parts = [s for s in spans if s.get('film_selection_id') == film['id']]
        lo, hi = parts[0]['output_frames'][0], parts[-1]['output_frames'][1]
        groups.append({'id': film['id'], 'label': film.get('label', film['id']),
                       'frames': [lo-1, lo, (lo+hi)//2, hi-1, hi]})
    groups += [
        {'id': 'locked-brand', 'label': 'Locked brand reveal and excision seam',
         'frames': [1426, 1427, 1431, 1436, 1437, 1438, 1439, 1442]},
        {'id': 'locked-hospitality', 'label': 'Locked paragraph and labeled still boundaries',
         'frames': [15919, 15920, 15926, 16091, 16262, 16263]},
    ]
    requested = sorted({f for group in groups for f in group['frames']})
    encoded = extract(output, requested)
    expected, mappings, by_source = {}, {}, {}
    for frame in requested:
        s = next(s for s in spans if s['output_frames'][0] <= frame < s['output_frames'][1])
        source_frame = s['source_start_frame'] + frame - s['output_frames'][0]
        mappings[frame] = {'segment': s['segment_id'], 'kind': s['kind'], 'source': s['source'],
                           'source_frame': source_frame, 'film_selection': s.get('film_selection_id')}
        if s['kind'] == 'video':
            by_source.setdefault(s['source']['path'], set()).add(source_frame)
    source_images = {}
    for path, frames in by_source.items():
        info = next(m['source'] for m in mappings.values() if m['source']['path'] == path)
        source_images[path] = extract(verify_bound(info), frames)
    for frame, m in mappings.items():
        if m['kind'] == 'video':
            expected[frame] = source_images[m['source']['path']][m['source_frame']]
    # For the static corrected passage, compare to the exact owner-locked context.
    lock = read(verify_bound(data['owner_scoped_lock']))
    hospital = verify_bound(lock['hospitality_preview'])
    still_frames = [f for f in requested if mappings[f]['kind'] == 'still']
    preview_frames = {f: f - 15920 + 120 for f in still_frames}
    still_images = extract(hospital, list(preview_frames.values()))
    for frame, preview_frame in preview_frames.items():
        expected[frame] = still_images[preview_frame]
        mappings[frame]['comparison_reference'] = {'accepted_context': lock['hospitality_preview'], 'frame': preview_frame}
    comparisons = []
    for frame in requested:
        image = encoded[frame]
        diff = np.abs(image.astype(float) - expected[frame].astype(float))
        comparisons.append({'output_frame': frame, 'output_seconds': frame/FPS, **mappings[frame],
                            'mean_abs_rgb_difference': float(diff.mean()),
                            'fraction_pixels_mean_rgb_difference_above20': float((diff.mean(2)>20).mean())})
        Image.fromarray(image).save(directory / f'frame-{frame:05d}.png')
    sheets = []
    for group in groups:
        cols = 3 if len(group['frames']) <= 6 else 4
        rows = (len(group['frames']) + cols - 1) // cols
        sheet = Image.new('RGB', (cols*W, rows*(H+35)+40), '#eeeeee')
        draw = ImageDraw.Draw(sheet)
        draw.text((12, 10), group['label'], fill='black')
        for i, frame in enumerate(group['frames']):
            x, y = (i%cols)*W, 40 + (i//cols)*(H+35)
            sheet.paste(Image.fromarray(encoded[frame]), (x, y))
            draw.text((x+10, y+H+7), f"r3 frame {frame} | {frame/FPS:.6f}s | {mappings[frame]['segment']}", fill='black')
        path = directory / (group['id']+'.jpg'); sheet.save(path, quality=94); sheets.append(bound(path))
    report = {'record_type': 'ep009_r3_encoded_frame_integration', 'build': bound(a.manifest), 'output': bound(output),
              'method': 'Exact decoded output frame indexes at each film entry/midpoint/exit, including previous and next unchanged frames. Source frames selected through bound manifest ranges. Static P08 compared to owner-locked context. RGB comparisons use640x360decodedimages; differences include the full-output encoding pass.',
              'frame_count': len(requested), 'groups': groups, 'sheets': sheets, 'comparisons': comparisons,
              'maximum_mean_abs_rgb_difference': max(c['mean_abs_rgb_difference'] for c in comparisons),
              'maximum_fraction_pixels_mean_rgb_difference_above20': max(c['fraction_pixels_mean_rgb_difference_above20'] for c in comparisons),
              'limits': ['Metrics do not judge film behavior or creative acceptance.', 'Stills cannot establish normal-speed comprehension or mouth sync.', 'The scoped brand/experience owner lock does not accept the new film or final presenter delivery.']}
    write(directory / 'FRAME-COMPARISON.json', report)
    print(json.dumps({'directory': str(directory), 'frames': len(requested), 'sheets': len(sheets),
                      'max_mean_abs_rgb_difference': report['maximum_mean_abs_rgb_difference']}, indent=2))


if __name__ == '__main__':
    main()
