"""Scale native masks, bind all inputs, and make alignment-only QA overlays."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    reused_report = json.loads((HERE / 'reused-r19-records.json').read_text())
    native_report = json.loads((HERE / 'native-segmentation-report.json').read_text())
    reused = {r['frame']: r for r in reused_report['records']}
    new = {r['frame']: r for r in native_report['records']}
    assert set(reused).isdisjoint(new)
    assert set(reused) | set(new) == set(range(140))
    records = []
    for frame in range(140):
        record = dict((reused if frame in reused else new)[frame])
        source = HERE / f'frame-{frame:03}.png'
        native_path = HERE / f'alpha-native-{frame:03}.png'
        full_path = HERE / f'mask-full-{frame:03}.png'
        native = Image.open(native_path)
        assert native.mode == 'L'
        assert native.size == (record['native_width'], record['native_height'])
        if frame not in reused:
            native.resize((1920, 1080), Image.Resampling.BILINEAR).save(full_path)
        full = Image.open(full_path)
        rgb = Image.open(source)
        assert full.mode == 'L' and full.size == (1920, 1080)
        assert rgb.mode == 'RGB' and rgb.size == (1920, 1080)
        a = np.asarray(full)
        assert a.min() == 0 and a.max() == 255
        record.update({
            'source': source.name, 'native_mask': native_path.name,
            'full_mask': full_path.name, 'full_width': 1920, 'full_height': 1080,
            'mode': 'L', 'reused_verified_r19_result': frame in reused,
            'resampling': 'Pillow BILINEAR, direct normalized full extent; no crop, flip, thresholding or morphology',
            'rgb_sha256': sha(source), 'native_sha256': sha(native_path),
            'full_mask_sha256': sha(full_path),
            'alpha_min': int(a.min()), 'alpha_max': int(a.max()),
            'alpha_nonzero_pixels': int((a > 0).sum())
        })
        records.append(record)
    report = {
        'status': 'complete_awaiting_sampled_alignment_review',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'source_sha256': reused_report['source_sha256'],
        'source_dimensions': [1920, 1080], 'source_fps': 25,
        'source_frame_count': 140, 'output_frame_count': len(records),
        'source_rgb_validation': 'All 140 frames decoded in order from verified Q. Reused RGB bytes compared exactly to current decoded Q.',
        'framework': 'Apple Vision',
        'request': 'VNGeneratePersonSegmentationRequest',
        'quality': 'accurate',
        'full_mask_pattern': 'mask-full-NNN.png',
        'source_pattern': 'frame-NNN.png',
        'alpha_use': 'Read grayscale and divide by 255. These are confidence masks, not RGBA. Native masks retained unchanged.',
        'reused_count': len(reused), 'newly_segmented_count': len(new),
        'reuse_provenance': reused_report['source_manifest'],
        'reuse_provenance_sha256': reused_report['source_manifest_sha256'],
        'records': records,
        'visual_qa': {'overlay_frames_created': [0, 70, 139], 'review_pending': True},
        'provider_calls': 0, 'installs': 0, 'productionGateAdvance': False
    }
    for frame in [0, 70, 139]:
        rgb = np.asarray(Image.open(HERE / f'frame-{frame:03}.png'), dtype=float)
        a = np.asarray(Image.open(HERE / f'mask-full-{frame:03}.png'), dtype=float) / 255
        tint = np.zeros_like(rgb)
        tint[:] = [30, 230, 40]
        overlay = np.rint(rgb * (1-a[..., None]*.3) + tint * (a[..., None]*.3)).astype('uint8')
        Image.fromarray(overlay).save(HERE / f'qa-overlay-{frame:03}.png')
    (HERE / 'segmentation-manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'frames': len(records), 'reused': len(reused), 'new': len(new),
                      'native_sizes': sorted(set((r['native_width'], r['native_height']) for r in records)),
                      'manifest': str(HERE / 'segmentation-manifest.json')}))


if __name__ == '__main__':
    main()
