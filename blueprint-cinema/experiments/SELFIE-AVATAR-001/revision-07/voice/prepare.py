"""R7 first-section audio edit. Root runs this in the Higgsfield media sandbox.

Usage: python3 prepare.py inputs.json
inputs.json must contain uploads[0]: upload_url, content_type, url, media_id.
No TTS, voice transfer, video generation or provider retry is performed.
"""
import base64
import hashlib
import io
import json
import math
import subprocess
import sys
import urllib.error
import urllib.request
import wave
from pathlib import Path

RATE = 48000
SOURCE_URL = 'https://v3b.fal.media/files/b/0aaa2fe9/0g2B6ygqc2BCtUFM0scTp_selfie-r4-final-b2c10c8e5b3267a4.wav'
SOURCE_SHA = 'b2c10c8e5b3267a43f8aaa4b3aba2132f4b20d6df6cd22fbfdcf0dc831e7e3b3'
SCRIPT_SHA = '3eb28bd243f2c169b5906852f3b055553d1bc0e0520a029082fa5bf41a36fbe3'
SOURCE_SAMPLES = 2536734
START, PAUSE, END, SECTION_END = 534480, 782640, 955200, 968000
TEMPO = 0.90
PAUSE_SAMPLES = 5760
SHA = lambda value: hashlib.sha256(value).hexdigest()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect())


def read_wav(data):
    with wave.open(io.BytesIO(data)) as audio:
        assert (audio.getframerate(), audio.getnchannels(), audio.getsampwidth(),
                audio.getcomptype()) == (RATE, 1, 2, 'NONE')
        count = audio.getnframes()
        pcm = audio.readframes(count)
        assert len(pcm) == count * 2
        return pcm, count


def write_wav(path, pcm):
    assert len(pcm) % 2 == 0
    with wave.open(str(path), 'wb') as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(RATE)
        audio.writeframes(pcm)


def stretch(pcm, label):
    src = Path(f'r7-{label}-source.wav')
    dst = Path(f'r7-{label}-tempo.wav')
    write_wav(src, pcm)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(src),
        '-map', '0:a:0', '-af', 'atempo=0.90', '-ar', str(RATE), '-ac', '1',
        '-c:a', 'pcm_s16le', '-map_metadata', '-1', str(dst)], check=True)
    output, count = read_wav(dst.read_bytes())
    assert len(pcm) / 2 < count < len(pcm) / 2 * 1.2, 'Unexpected tempo output length'
    return output


def main():
    cfg = json.loads(Path(sys.argv[1] if len(sys.argv) > 1 else 'inputs.json').read_text())
    slot = cfg['uploads'][0]
    assert all(slot.get(key) for key in ('upload_url', 'content_type', 'url', 'media_id'))
    with OPENER.open(SOURCE_URL, timeout=45) as response:
        source_bytes = response.read()
    assert SHA(source_bytes) == SOURCE_SHA
    source, count = read_wav(source_bytes)
    assert count == SOURCE_SAMPLES

    prefix = source[:START*2]
    left = stretch(source[START*2:PAUSE*2], 'gtm-through-code')
    pause = b'\x00\x00' * PAUSE_SAMPLES
    right = stretch(source[PAUSE*2:END*2], 'then-researches')
    unchanged_tail = source[END*2:SECTION_END*2]
    pieces = [
        ('copy_exact_pcm', 0, START, prefix),
        ('pitch_preserving_tempo', START, PAUSE, left),
        ('insert_silence', PAUSE, PAUSE, pause),
        ('pitch_preserving_tempo', PAUSE, END, right),
        ('copy_exact_pcm', END, SECTION_END, unchanged_tail),
    ]
    sample_map = []
    cursor = 0
    output_parts = []
    for operation, source_start, source_end, pcm in pieces:
        n = len(pcm) // 2
        source_n = source_end - source_start
        sample_map.append({
            'operation': operation,
            'source_samples': [source_start, source_end],
            'output_samples': [cursor, cursor+n],
            'source_sample_count': source_n,
            'output_sample_count': n,
            'empirical_duration_ratio': n / source_n if source_n else None,
            'tempo_factor': TEMPO if operation == 'pitch_preserving_tempo' else None,
            'output_pcm_sha256': SHA(pcm),
        })
        cursor += n
        output_parts.append(pcm)
    unpadded_count = cursor
    frame_count = math.ceil(cursor / 2000)
    pad_count = frame_count * 2000 - cursor
    padding = b'\x00\x00' * pad_count
    sample_map.append({
        'operation': 'pad_to_video_frame',
        'source_samples': [SECTION_END, SECTION_END],
        'output_samples': [cursor, cursor+pad_count],
        'source_sample_count': 0,
        'output_sample_count': pad_count,
        'empirical_duration_ratio': None,
        'tempo_factor': None,
        'output_pcm_sha256': SHA(padding),
    })
    output_parts.append(padding)
    final_pcm = b''.join(output_parts)
    output_count = len(final_pcm) // 2
    assert output_count == frame_count * 2000
    assert final_pcm[:START*2] == prefix == source[:START*2]
    tail_map = sample_map[4]
    a, b = tail_map['output_samples']
    assert final_pcm[a*2:b*2] == unchanged_tail == source[END*2:SECTION_END*2]
    assert not pad_count or final_pcm[-pad_count*2:] == b'\x00\x00' * pad_count

    output_path = Path('r7-first-section.original-c.wav')
    write_wav(output_path, final_pcm)
    output_bytes = output_path.read_bytes()
    reread, reread_count = read_wav(output_bytes)
    assert reread == final_pcm and reread_count == output_count
    # Uploaded body remains RIFF WAV even if the host reservation uses an mp3 suffix.
    request = urllib.request.Request(slot['upload_url'], data=output_bytes, method='PUT',
        headers={'Content-Type': slot['content_type']})
    try:
        with OPENER.open(request, timeout=90) as response:
            upload_http = response.status
    except urllib.error.HTTPError as error:
        raise SystemExit(f'Audio upload failed HTTP {error.code}; no retry performed')
    assert upload_http == 200

    report = {
        'status': 'first_section_prepared_uploaded_pending_readback_asr_and_listening',
        'sample_rate_hz': RATE,
        'channels': 1,
        'sample_width_bytes': 2,
        'actual_container': 'RIFF WAV PCM signed16 little-endian',
        'source_url': SOURCE_URL,
        'source_sha256': SOURCE_SHA,
        'source_sample_count': SOURCE_SAMPLES,
        'script_sha256': SCRIPT_SHA,
        'source_section_samples': [0, SECTION_END],
        'source_section_word_count': 68,
        'requested_tempo_factor': TEMPO,
        'inserted_pause_samples': PAUSE_SAMPLES,
        'inserted_pause_seconds': PAUSE_SAMPLES / RATE,
        'sample_map': sample_map,
        'output_sha256': SHA(output_bytes),
        'output_pcm_sha256': SHA(final_pcm),
        'output_bytes': len(output_bytes),
        'output_sample_count': output_count,
        'output_duration_seconds': output_count / RATE,
        'unpadded_sample_count': unpadded_count,
        'unpadded_duration_seconds': unpadded_count / RATE,
        'frame_count': frame_count,
        'frame_rate': '24/1',
        'frame_padding_zero_samples': pad_count,
        'duration_increase_seconds': (output_count-SECTION_END) / RATE,
        'copy_proofs': [
            {'source_samples': [0, START], 'output_samples': [0, START],
             'pcm_sha256': SHA(prefix), 'byte_identical': True},
            {'source_samples': [END, SECTION_END], 'output_samples': tail_map['output_samples'],
             'pcm_sha256': SHA(unchanged_tail), 'byte_identical': True},
        ],
        'retained_suffix_for_later_integration': {
            'source_samples': [SECTION_END, SOURCE_SAMPLES],
            'pcm_sha256': SHA(source[SECTION_END*2:]),
            'operation': 'copy_exact_pcm_when_integrating_no_speed_or_gain_change',
        },
        'zero_padding_verified': True,
        'filters': ['atempo=0.90 applied separately to the two declared source ranges'],
        'fades_gain_eq_or_noise_added': False,
        'perceptual_quality': 'Not assessed. Quiet joins and preserved copied PCM do not establish naturalness or exact ASR recognition.',
        'upload': {'media_id': slot['media_id'], 'url': slot['url'],
            'reservation_content_type': slot['content_type'], 'upload_http': upload_http},
    }
    report_bytes = (json.dumps(report, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    Path('R7-VOICE-REPORT.json').write_bytes(report_bytes)
    print('REPORT_BASE64=' + base64.b64encode(report_bytes).decode(), flush=True)
    print('SUMMARY=' + json.dumps({
        'media_id': slot['media_id'], 'url': slot['url'],
        'output_sha256': report['output_sha256'],
        'report_sha256': SHA(report_bytes),
        'sample_count': output_count, 'duration_seconds': output_count / RATE,
        'unpadded_sample_count': unpadded_count, 'frame_count': frame_count,
        'frame_padding_zero_samples': pad_count, 'upload_http': upload_http,
    }), flush=True)


if __name__ == '__main__':
    main()

