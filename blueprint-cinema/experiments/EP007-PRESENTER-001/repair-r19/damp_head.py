#!/usr/bin/env python3
"""Apply a bounded vertical inverse warp to a source video, retaining its audio."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image


def digest(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config', type=Path)
    args = ap.parse_args()
    cfg = json.loads(args.config.read_text())
    source, output = Path(cfg['source']), Path(cfg['output'])
    if digest(source) != cfg['source_sha256']:
        raise ValueError('Source hash changed')
    if output.exists():
        raise FileExistsError(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    width, height = cfg['dimensions']
    rate = cfg['fps']
    shifts = {r['frame']: r['output_dy_px'] for r in cfg['frame_shifts']}
    core_x0, core_y0, core_x1, core_y1 = cfg['mask']['rigid_core_xyxy']
    outer_x0, outer_y0, outer_x1, outer_y1 = cfg['mask']['outer_bounds_xyxy']
    x0, y0, x1, y1 = cfg['processing_roi_xyxy']
    step = cfg.get('mesh_step_px', 12)

    def weight(x, y):
        wx = smoothstep((x - outer_x0) / (core_x0 - outer_x0))
        wx *= 1 - smoothstep((x - core_x1) / (outer_x1 - core_x1))
        wy = smoothstep((y - outer_y0) / (core_y0 - outer_y0))
        wy *= 1 - smoothstep((y - core_y1) / (outer_y1 - core_y1))
        return float(wx * wy)

    def mesh_for(shift):
        mesh = []
        for y in range(y0, y1, step):
            for x in range(x0, x1, step):
                xx, yy = min(x + step, x1), min(y + step, y1)
                # Pillow QUAD order: top-left, bottom-left, bottom-right, top-right.
                quad = []
                for sx, sy in ((x, y), (x, yy), (xx, yy), (xx, y)):
                    quad.extend((sx - x0, sy - y0 - shift * weight(sx, sy)))
                mesh.append(((x - x0, y - y0, xx - x0, yy - y0), tuple(quad)))
        return mesh

    decoder = subprocess.Popen(
        ['ffmpeg', '-v', 'error', '-i', str(source), '-map', '0:v:0',
         '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
        stdout=subprocess.PIPE)
    encoder = subprocess.Popen(
        ['ffmpeg', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
         '-s', f'{width}x{height}', '-r', str(rate), '-i', '-', '-i', str(source),
         '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-preset', 'medium',
         '-crf', '15', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
         '-movflags', '+faststart', str(output)], stdin=subprocess.PIPE)
    frame_bytes = width * height * 3
    frame_index = 0
    altered = []
    while True:
        raw = decoder.stdout.read(frame_bytes)
        if not raw:
            break
        if len(raw) != frame_bytes:
            raise ValueError('Truncated decoded frame')
        shift = shifts.get(frame_index, 0)
        if abs(shift) > 1e-6:
            im = Image.frombytes('RGB', (width, height), raw)
            crop = im.crop((x0, y0, x1, y1))
            warped = crop.transform(crop.size, Image.Transform.MESH,
                                    mesh_for(shift), Image.Resampling.BICUBIC)
            im.paste(warped, (x0, y0))
            raw = im.tobytes()
            altered.append(frame_index)
        encoder.stdin.write(raw)
        frame_index += 1
    decoder.stdout.close()
    encoder.stdin.close()
    if decoder.wait() or encoder.wait():
        raise RuntimeError('Decode or encode failed')
    if frame_index != cfg['expected_frames']:
        raise ValueError(f'Unexpected frame count {frame_index}')
    report = {
        'source_sha256': cfg['source_sha256'], 'output_sha256': digest(output),
        'output_bytes': output.stat().st_size, 'frames': frame_index,
        'spatially_altered_frames': altered,
        'audio_mode': 'copy source audio bitstream',
        'temporal_changes': False, 'mouth_reshaping': False,
        'field': 'vertical translation in head core, smooth spatial falloff',
        'limitations': ['Does not remove 3D pitch or eyelid expression',
                       'Blend region may affect nearby background/neck; review required',
                       'Video is re-encoded; outside-region pixels have codec differences']
    }
    args.config.with_name('render-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
