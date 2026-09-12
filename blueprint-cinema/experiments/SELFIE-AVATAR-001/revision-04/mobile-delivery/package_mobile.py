"""Lossless mobile remux and representative-frame QA in the media sandbox."""
import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw


def stream_hash(path):
    return subprocess.check_output(['ffmpeg', '-v', 'error', '-xerror', '-i', path,
        '-map', '0:v:0', '-map', '0:a:0', '-f', 'streamhash', '-hash', 'sha256', '-'],
        text=True).strip()


def upload(path, slot):
    data = Path(path).read_bytes()
    request = urllib.request.Request(slot['upload_url'], data=data, method='PUT',
        headers={'Content-Type': slot['content_type']})
    with urllib.request.urlopen(request) as response:
        code = response.status
    assert code == 200
    return {'media_id': slot['media_id'], 'url': slot['url'], 'upload_http': code,
        'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def main(cfg):
    urllib.request.urlretrieve(cfg['source_url'], 'raw-sync.mp4')
    assert hashlib.sha256(Path('raw-sync.mp4').read_bytes()).hexdigest() == cfg['source_sha256']
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'raw-sync.mp4',
        '-map', '0:v:0', '-map', '0:a:0', '-c', 'copy', '-movflags', '+faststart',
        'mobile.mp4'], check=True)
    source_streams = stream_hash('raw-sync.mp4')
    mobile_streams = stream_hash('mobile.mp4')
    assert source_streams == mobile_streams
    metadata = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-show_streams', '-show_format', '-of', 'json', 'mobile.mp4']))
    v, a = metadata['streams']
    assert v['codec_type'] == 'video' and a['codec_type'] == 'audio'
    assert (v['width'], v['height'], int(v['nb_frames'])) == (720, 1280, 1293)
    assert v['r_frame_rate'] == '24/1' and v['codec_name'] == 'h264' and a['codec_name'] == 'aac'
    frames = [12, 192, 360, 483, 484, 650, 861, 862, 1008, 1160, 1268, 1292]
    selection = '+'.join(f'eq(n\\,{frame})' for frame in frames)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'mobile.mp4',
        '-vf', f'select={selection},scale=270:480', '-fps_mode', 'vfr',
        '-frames:v', str(len(frames)), 'restored-%02d.png'], check=True)
    sheet = Image.new('RGB', (1080, 1536), '#eeeeee')
    draw = ImageDraw.Draw(sheet)
    for i, frame in enumerate(frames):
        col, row = i % 4, i // 4
        sheet.paste(Image.open(f'restored-{i+1:02d}.png').convert('RGB'), (col*270, row*512+32))
        draw.text((col*270+6, row*512+10), f'Frame {frame} | {frame/24:.3f}s', fill='#111111')
    sheet.save('restored-contact.jpg', quality=92)
    result = upload('mobile.mp4', cfg['video_upload'])
    result.update({'width': v['width'], 'height': v['height'],
        'frame_count': int(v['nb_frames']), 'video_duration_seconds': float(v['duration']),
        'container_duration_seconds': float(metadata['format']['duration']),
        'video_codec': v['codec_name'], 'audio_codec': a['codec_name'],
        'frame_rate': v['r_frame_rate'], 'video_first': True, 'faststart': True,
        'source_stream_hashes': source_streams, 'output_stream_hashes': mobile_streams,
        'decoded_streams_identical': True})
    contact = upload('restored-contact.jpg', cfg['contact_upload'])
    print(json.dumps({'source_url': cfg['source_url'], 'source_sha256': cfg['source_sha256'],
        'mobile': result, 'contact': contact}))


if __name__ == '__main__':
    main(json.loads(sys.argv[1]))
