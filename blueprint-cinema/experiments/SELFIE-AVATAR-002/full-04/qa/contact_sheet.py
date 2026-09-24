#!/usr/bin/env python3
"""Inspect generated laptop footage; never alter a production source.

Example:
  python contact_sheet.py --video ../media/folders-native.mp4 \
    --label folders --seconds 0 .5 1 1.5 2 2.5 3 4 5 5.9

Outputs full-phone and larger UI-region contact sheets plus an input receipt
in this script's directory by default. The UI crop is inspection-only.
"""

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw


def run(*args):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', required=True, type=Path)
    parser.add_argument('--label', required=True)
    parser.add_argument('--seconds', nargs='+', type=float,
                        default=[0, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 5.9])
    parser.add_argument('--out', type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    source = args.video.resolve(strict=True)
    info = json.loads(run('ffprobe', '-v', 'error', '-show_streams',
                          '-show_format', '-of', 'json', str(source)))
    stream = next(x for x in info['streams'] if x['codec_type'] == 'video')
    numerator, denominator = map(int, stream['avg_frame_rate'].split('/'))
    fps = numerator / denominator
    total = int(stream.get('nb_frames',
                           round(float(info['format']['duration']) * fps)))
    frames = sorted(set(round(t * fps) for t in args.seconds
                        if 0 <= round(t * fps) < total))
    if not frames:
        parser.error('No requested sample lands inside this source.')
    args.out.mkdir(parents=True, exist_ok=True)
    source_images = []
    for frame in frames:
        data = run('ffmpeg', '-v', 'error', '-i', str(source), '-vf',
                   f'select=eq(n\\,{frame})', '-frames:v', '1', '-f',
                   'image2pipe', '-vcodec', 'png', '-')
        source_images.append(Image.open(io.BytesIO(data)).convert('RGB'))
    for mode, cell_width, columns in [('phone', 240, 4), ('ui', 540, 3)]:
        samples = []
        for original in source_images:
            sample = original.copy()
            if mode == 'ui':
                width, height = sample.size
                sample = sample.crop((int(.01 * width), int(.29 * height),
                                      int(.995 * width), int(.69 * height)))
            sample.thumbnail((cell_width, 1000), Image.Resampling.LANCZOS)
            samples.append(sample)
        cell_height = max(x.height for x in samples) + 28
        sheet = Image.new('RGB', (columns * cell_width,
                                 math.ceil(len(frames) / columns) * cell_height),
                          (22, 22, 22))
        draw = ImageDraw.Draw(sheet)
        for index, (frame, sample) in enumerate(zip(frames, samples)):
            x = index % columns * cell_width
            y = index // columns * cell_height
            sheet.paste(sample, (x, y + 28))
            draw.text((x + 8, y + 8),
                      f'{args.label} frame {frame} | {frame / fps:.3f}s',
                      fill='white')
        sheet.save(args.out / f'{args.label}-{mode}.jpg', quality=95)
    receipt = {'source': str(source),
               'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
               'fps': fps, 'frames_total': total,
               'dimensions': [stream['width'], stream['height']],
               'sample_frames': frames,
               'purpose': 'Inspection only; no production crop or edit.'}
    (args.out / f'{args.label}-inspection.json').write_text(
        json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
