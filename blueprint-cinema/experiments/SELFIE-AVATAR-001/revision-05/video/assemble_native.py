"""Exact-frame standalone review assembly; run in the Higgsfield media sandbox.

Configuration is supplied at execution. Upload credentials must not be persisted
in repository records. No speech retiming, picture looping, or synthetic holds.
"""
import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw


def probe(path):
    data = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format',
        '-of', 'json', str(path)]))
    return data


def put(path, slot):
    data = path.read_bytes()
    request = urllib.request.Request(slot['upload_url'], data=data, method='PUT',
        headers={'Content-Type': slot['content_type']})
    with urllib.request.urlopen(request) as response:
        status = response.status
    assert status == 200
    return {'media_id': slot['media_id'], 'sha256': hashlib.sha256(data).hexdigest(),
        'bytes': len(data), 'upload_http': status}


def main(cfg):
    counts = [484, 378, 431]
    native = []
    for i, source in enumerate(cfg['sources']):
        path = Path(f'native-{i+1}.mp4')
        urllib.request.urlretrieve(source['url'], path)
        metadata = probe(path)
        video = next(s for s in metadata['streams'] if s['codec_type'] == 'video')
        assert (video['width'], video['height']) == (720, 1280)
        assert video['r_frame_rate'] == '24/1'
        assert int(video['nb_frames']) >= counts[i]
        native.append({'index': i+1, 'url': source['url'],
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'bytes': path.stat().st_size,
            'width': video['width'], 'height': video['height'],
            'frame_rate': video['r_frame_rate'], 'frame_count': int(video['nb_frames']),
            'duration_seconds': float(video['duration']), 'selected_frames': counts[i]})
    filters = ';'.join(f'[{i}:v]trim=end_frame={n},setpts=PTS-STARTPTS,setsar=1[v{i}]'
        for i, n in enumerate(counts))
    filters += ';[v0][v1][v2]concat=n=3:v=1:a=0[outv]'
    cmd = ['ffmpeg', '-y', '-v', 'error']
    for i in range(3):
        cmd += ['-i', f'native-{i+1}.mp4']
    cmd += ['-filter_complex', filters, '-map', '[outv]', '-an', '-c:v', 'libx264',
        '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', '-tag:v', 'avc1',
        '-r', '24', '-movflags', '+faststart', 'assembled-native.mp4']
    subprocess.run(cmd, check=True)
    metadata = probe('assembled-native.mp4')
    video = metadata['streams'][0]
    assert len(metadata['streams']) == 1 and video['codec_type'] == 'video'
    assert int(video['nb_frames']) == 1293
    assert abs(float(video['duration']) - 53.875) < 0.00001
    frames = [12, 72, 100, 142, 168, 350, 483, 484, 650, 790, 821, 861, 862, 910, 1025, 1100, 1160, 1220, 1268, 1292]
    selection = '+'.join(f'eq(n\\,{frame})' for frame in frames)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'assembled-native.mp4',
        '-vf', f'select={selection},scale=270:480', '-fps_mode', 'vfr',
        '-frames:v', str(len(frames)), 'qa-%02d.png'], check=True)
    sheet = Image.new('RGB', (1080, 2560), '#eeeeee')
    draw = ImageDraw.Draw(sheet)
    for i, frame in enumerate(frames):
        path = Path(f'qa-{i+1:02d}.png')
        col, row = i % 4, i // 4
        sheet.paste(Image.open(path).convert('RGB'), (col*270, row*512+32))
        draw.text((col*270+6, row*512+10), f'Frame {frame} | {frame/24:.3f}s', fill='#111111')
    sheet.save('native-contact.jpg', quality=92)
    output = put(Path('assembled-native.mp4'), cfg['video_upload'])
    contact = put(Path('native-contact.jpg'), cfg['contact_upload'])
    output.update({'width': 720, 'height': 1280, 'frame_rate': '24/1',
        'frame_count': 1293, 'video_duration_seconds': 53.875,
        'segment_frame_counts': counts, 'audio_streams': 0,
        'encoding': 'libx264 CRF17 fast yuv420p avc1 video-only faststart'})
    print(json.dumps({'native_sources': native, 'assembled': output, 'contact': contact}))


if __name__ == '__main__':
    main(json.loads(sys.argv[1]))
