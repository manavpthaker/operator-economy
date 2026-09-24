#!/usr/bin/env python3
"""Inspect encoded presenter joins, original crop cuts and protected scenes."""
import argparse, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
T = Path(__file__).resolve().parents[1]
A = T.parent / 'assembly'
sys.path.insert(0, str(A / '_tools'))
import numpy as np
from PIL import Image, ImageDraw
from build_r3 import bound, read, verify_bound, write
from inspect_r3_frames import extract, W, H

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build', type=Path)
    args = parser.parse_args()
    data = read(args.build)
    if data['record_type'] != 'ep009_r5_look_transfer_review_build' or data['mode'] != 'full':
        raise ValueError('Full look-transfer review required')
    out = verify_bound({'path': data['output'], 'sha256': data['output_sha256']})
    directory = out.parent / (out.stem + '-integration')
    if directory.exists():
        raise FileExistsError('Preserve existing evidence')
    directory.mkdir()
    groups = [
        {'id': 'locked-opening', 'frames': [0, 1, 43, 85, 86, 87, 134, 135]},
        {'id': 'locked-brand', 'frames': [1426, 1427, 1431, 1436, 1437, 1438, 1439, 1442]}
    ]
    cuts = {'seg012': [152], 'seg019': [38,333], 'seg021': [96,170],
            'seg035': [100], 'seg037': [108], 'seg044': [173],
            'seg059': [33], 'seg071': [30,97,449]}
    spans = []
    for row in data['all_75_rows']:
        for span in row['spans']:
            spans.append({**span, 'segment_id': row['id']})
    for e in data['replacements']:
        lo, hi = e['output_frames']
        frames = [max(0, lo-1), lo, (lo+hi)//2, hi-1]
        if hi < 29323:
            frames.append(hi)
        for cut in cuts.get(e['segment'], []):
            frames.extend([lo+cut-1, lo+cut])
        groups.append({'id': e['segment'], 'frames': sorted(set(frames))})
    for film in read(verify_bound(data['film_selections']))['selections']:
        parts = [s for s in spans if s.get('film_selection_id') == film['id']]
        if not parts:
            raise ValueError('Missing retained film ' + film['id'])
        lo, hi = parts[0]['output_frames'][0], parts[-1]['output_frames'][1]
        groups.append({'id': film['id'], 'frames': [lo-1,lo,(lo+hi)//2,hi-1,hi]})
    requested = sorted({f for g in groups for f in g['frames']})
    encoded = extract(out, requested)
    mappings, by_source = {}, {}
    for f in requested:
        s = next(s for s in spans if s['output_frames'][0] <= f < s['output_frames'][1])
        sf = s['source_start_frame'] + f - s['output_frames'][0]
        if s['kind'] != 'video':
            raise ValueError('Unexpected still in completed presenter review')
        mappings[f] = {'segment': s['segment_id'], 'source': s['source'], 'source_frame': sf}
        by_source.setdefault(s['source']['path'], {'bound': s['source'], 'frames': set()})['frames'].add(sf)
    images = {p: extract(verify_bound(v['bound']), v['frames']) for p,v in by_source.items()}
    comparisons = []
    for f,m in mappings.items():
        expected = images[m['source']['path']][m['source_frame']]
        diff = np.abs(encoded[f].astype(float) - expected.astype(float))
        comparisons.append({'output_frame': f, **m, 'mean_abs_rgb_difference': float(diff.mean()),
                            'fraction_pixels_mean_rgb_difference_above20': float((diff.mean(2)>20).mean())})
    sheets = []
    for g in groups:
        cols = 3
        rows = (len(g['frames'])+cols-1)//cols
        sheet = Image.new('RGB', (cols*W, rows*(H+30)+35), '#eeeeee')
        draw = ImageDraw.Draw(sheet)
        draw.text((10,10), g['id'] + ' - actual encoded integration frames', fill='black')
        for i,f in enumerate(g['frames']):
            x,y = (i%cols)*W,35+(i//cols)*(H+30)
            sheet.paste(Image.fromarray(encoded[f]), (x,y))
            draw.text((x+8,y+H+7), f'frame {f} | {f/24:.4f}s | {mappings[f]["segment"]}', fill='black')
        p = directory/(g['id']+'.jpg')
        sheet.save(p,quality=93)
        sheets.append(bound(p))
    report = {'record_type': 'ep009_look_transfer_encoded_integration', 'build': bound(args.build), 'output': bound(out),
              'groups': groups, 'frame_count': len(requested), 'comparisons': comparisons, 'sheets': sheets,
              'maximum_mean_abs_rgb_difference': max(x['mean_abs_rgb_difference'] for x in comparisons),
              'maximum_fraction_pixels_mean_rgb_difference_above20': max(x['fraction_pixels_mean_rgb_difference_above20'] for x in comparisons),
              'owner_accepted': False, 'limits': ['Exact-frame source comparisons at joints and protected cues, at 640x360. Encoding introduces small pixel differences.', 'Sampled frames do not establish continuous audiovisual review or mouth sync.']}
    write(directory/'FRAME-COMPARISON.json', report)
    print(json.dumps({'frames': len(requested), 'sheets': len(sheets), 'report': str(directory/'FRAME-COMPARISON.json')},indent=2))

if __name__ == '__main__':
    main()
