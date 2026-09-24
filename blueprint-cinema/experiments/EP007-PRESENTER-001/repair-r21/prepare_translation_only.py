#!/usr/bin/env python3
"""Prepare one conservative Q repair, with no added scale or rotation."""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'repair-r20'


def main():
    cfg = json.loads((PRIOR / 'stabilization-config.json').read_text())
    cfg['output'] = str(HERE.parent / 'media/repair-r21/test-t-no-scale-gentle-head-1080p.mp4')
    records = cfg['transforms']
    cx, cy = cfg['reference_eye_xy']
    raw = [(3 * math.tanh(.30 * (cx-r['smoothed_source_eye_center'][0])/3),
            5 * math.tanh(.30 * (cy-r['smoothed_source_eye_center'][1])/5))
           for r in records]
    # Smooth only the correction; facial frames and their timing never change.
    kernel = [math.exp(-.5 * (i/2.5)**2) for i in range(-5, 6)]
    norm = sum(kernel)
    for i, r in enumerate(records):
        dx, dy = [sum(w * raw[min(max(i+j-5, 0), len(raw)-1)][axis]
                       for j, w in enumerate(kernel))/norm for axis in (0, 1)]
        sx, sy = r['smoothed_source_eye_center']
        r.update(target_eye_center=[sx+dx, sy+dy], angle_degrees=0.0, scale=1.0,
                 translation_px=[dx, dy],
                 forward_matrix_2x3=[[1.0, 0.0, dx], [0.0, 1.0, dy]],
                 inverse_matrix_2x3=[[1.0, 0.0, -dx], [0.0, 1.0, -dy]])
    cfg.update(motion_residual_fraction=None, scale_correction_cap=[1.0, 1.0],
               angle_correction_cap_degrees=[0.0, 0.0],
               translation_cap_px={'x': 3.0, 'y': 5.0},
               smoothing='Q tracked center: prior median/binomial; correction: 11-frame Gaussian sigma2.5',
               method='Small translation only from Q; no scale, roll, or perspective correction',
               parent_test_s_rejected=True)
    assert all(r['scale'] == 1.0 and r['angle_degrees'] == 0.0 for r in records)
    assert all(abs(r['translation_px'][0]) <= 3 and abs(r['translation_px'][1]) <= 5 for r in records)
    (HERE / 'stabilization-config.json').write_text(json.dumps(cfg, indent=2)+'\n')
    print(json.dumps({'frames': len(records), 'scale': 1.0, 'rotation': 0.0,
                      'max_abs_translation_px': [max(abs(r['translation_px'][a]) for r in records) for a in (0, 1)]}))


if __name__ == '__main__':
    main()
