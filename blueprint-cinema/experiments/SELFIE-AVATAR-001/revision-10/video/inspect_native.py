"""Inspect native clips in the Higgsfield media sandbox; never run on the host.

Usage: python3 inspect_native.py inputs.json
Config: sources[{index,url,sha256(optional),voice_url,voice_sha256,script}],
contact_upload{media_id,upload_url,content_type}; optional paired full_voice_url /
full_voice_sha256, work_dir (fresh directory), max_offset_seconds (default 2).
Requires ffmpeg, ffprobe, numpy and Pillow. No assembly, generation or repair.
Downloads, exact scripts, frame PNGs, contact JPEG and REPORT.json stay local in
the sandbox work directory. Only the contact is PUT to the supplied upload URL.
Prints REPORT_BASE64 and SUMMARY. No provider credentials are read or sent.
"""
import base64
import hashlib
import json
import math
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

RATE = 16000
MIN_CORRELATION = 0.95
MAX_UNIFORM_SPREAD_SECONDS = 0.04
FRACTIONS = (0.10, 0.35, 0.65, 0.90)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def validate_url(value):
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Media and upload URLs must be HTTPS without user credentials')


def validate_digest(value):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value):
        raise ValueError('Expected a lowercase SHA-256 digest')


def validate_config(cfg):
    if not isinstance(cfg.get('sources'), list) or not cfg['sources']:
        raise ValueError('sources must be a nonempty array')
    indices = set()
    for item in cfg['sources']:
        if type(item.get('index')) is not int or item['index'] < 1 or item['index'] in indices:
            raise ValueError('Each source requires a unique positive integer index')
        indices.add(item['index'])
        for key in ('url', 'voice_url'):
            validate_url(item[key])
        validate_digest(item['voice_sha256'])
        if item.get('sha256') is not None:
            validate_digest(item['sha256'])
        if not isinstance(item.get('script'), str) or not item['script'].strip():
            raise ValueError('Each source requires its exact nonempty script string')
    full_keys = ('full_voice_url' in cfg, 'full_voice_sha256' in cfg)
    if any(full_keys) and not all(full_keys):
        raise ValueError('Supply full_voice_url and full_voice_sha256 together')
    if all(full_keys):
        validate_url(cfg['full_voice_url'])
        validate_digest(cfg['full_voice_sha256'])
    upload = cfg['contact_upload']
    validate_url(upload['upload_url'])
    if not isinstance(upload.get('media_id'), str) or not upload['media_id']:
        raise ValueError('contact_upload requires the supplied media_id')
    if upload.get('content_type') != 'image/jpeg':
        raise ValueError('Reserve contact_upload as image/jpeg for the JPEG contact')
    radius = float(cfg.get('max_offset_seconds', 2.0))
    if not math.isfinite(radius) or not 0.05 <= radius <= 10:
        raise ValueError('max_offset_seconds must be between 0.05 and 10')


def download(url, expected, destination):
    # No retries or credential headers. A fresh work directory prevents overwrite.
    with urllib.request.urlopen(url, timeout=60) as response:
        with destination.open('xb') as output:
            for block in iter(lambda: response.read(1024 * 1024), b''):
                output.write(block)
    actual = sha(destination)
    if expected is not None and actual != expected:
        raise ValueError(f'Hash mismatch for {destination.name}; file retained, not analyzed')
    return {'path': str(destination), 'url': url, 'sha256': actual,
            'bytes': destination.stat().st_size,
            'sha256_was_pinned': expected is not None}


def probe(path, count_frames=False):
    args = ['ffprobe', '-v', 'error']
    if count_frames:
        args += ['-count_frames']
    args += ['-show_entries',
             'format=duration,start_time:stream=index,codec_type,codec_name,width,height,'
             'r_frame_rate,avg_frame_rate,nb_frames,nb_read_frames,start_time,duration,'
             'sample_rate,channels,bits_per_sample', '-of', 'json', str(path)]
    return json.loads(subprocess.check_output(args, stderr=subprocess.PIPE))


def audio_samples(path):
    data = subprocess.check_output([
        'ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
        '-ac', '1', '-ar', str(RATE), '-f', 'f32le', 'pipe:1'],
        stderr=subprocess.PIPE)
    result = np.frombuffer(data, dtype='<f4').astype(np.float64)
    if len(result) < 2 or not np.all(np.isfinite(result)):
        raise ValueError('Audio decode is empty or contains non-finite samples')
    return result


def pearson(x, y):
    if len(x) < 2 or len(x) != len(y):
        return None
    x, y = x - np.mean(x), y - np.mean(y)
    denominator = float(np.sqrt(np.dot(x, x) * np.dot(y, y)))
    return float(np.clip(np.dot(x, y) / denominator, -1, 1)) if denominator > 1e-15 else None


def energy_plan(a):
    """Energy is a window-selection heuristic, not a speech/word detector."""
    block = RATE // 50  # 20 ms, retaining the short final block.
    starts = np.arange(0, len(a), block)
    counts = np.minimum(block, len(a) - starts)
    energy = np.add.reduceat(a * a, starts) / counts
    rms = np.sqrt(energy)
    threshold = max(1e-4, float(np.max(rms)) * 0.04)
    active = np.flatnonzero(rms >= threshold)
    result = {'method': '20 ms RMS above max(0.0001, 4 percent of peak RMS); '
                        'three disjoint thirds of the source active extent; '
                        'highest-energy window within each third',
              'threshold_rms': threshold, 'peak_rms': float(np.max(rms)),
              'source_energy_start_seconds': None, 'source_energy_end_seconds': None,
              'windows': []}
    if not len(active):
        return result
    first = int(starts[active[0]])
    last = int(min(len(a), starts[active[-1]] + block))
    result.update(source_energy_start_seconds=first / RATE,
                  source_energy_end_seconds=last / RATE)
    bounds = np.rint(np.linspace(first, last, 4)).astype(int)
    power_sum = np.concatenate(([0.0], np.cumsum(a * a)))
    for name, left, right in zip(('early', 'middle', 'late'), bounds[:-1], bounds[1:]):
        width = min(3 * RATE, int(right - left))
        if width < RATE // 4:
            continue
        candidates = np.unique(np.append(np.arange(left, right - width + 1, block), right - width))
        totals = power_sum[candidates + width] - power_sum[candidates]
        selected = int(candidates[int(np.argmax(totals))])
        x = a[selected:selected + width]
        result['windows'].append({'name': name, 'sample_start': selected,
                                  'sample_end': selected + width,
                                  'source_window_seconds': [selected / RATE, (selected + width) / RATE],
                                  'rms': float(np.sqrt(np.mean(x * x)))})
    return result


def match_window(a, b, window, radius):
    """Search exact normalized Pearson scores for all complete candidate windows."""
    left, right = window['sample_start'], window['sample_end']
    x = a[left:right]
    n = len(x)
    first = max(0, left - radius)
    last = min(len(b) - n, left + radius)
    result = {**window, 'candidate_offset_seconds': None, 'correlation': None,
              'zero_offset_correlation': pearson(x, b[left:right]) if right <= len(b) else None,
              'high_confidence_waveform_match': False}
    if last < first:
        return {**result, 'status': 'insufficient_complete_candidate_window'}
    y = b[first:last + n]
    centered = x - np.mean(x)
    x_variance_sum = float(np.dot(centered, centered))
    if x_variance_sum <= 1e-15:
        return {**result, 'status': 'source_window_has_no_variance'}
    size = 1 << (len(y) + n - 2).bit_length()
    conv = np.fft.irfft(np.fft.rfft(y, size) * np.fft.rfft(centered[::-1], size), size)
    dots = conv[n - 1:len(y)]
    sums = np.concatenate(([0.0], np.cumsum(y)))
    squares = np.concatenate(([0.0], np.cumsum(y * y)))
    variance = np.maximum(0, squares[n:] - squares[:-n] - (sums[n:] - sums[:-n]) ** 2 / n)
    denominator = np.sqrt(variance * x_variance_sum)
    scores = np.full(len(dots), -np.inf)
    np.divide(dots, denominator, out=scores, where=denominator > 1e-15)
    if not np.any(np.isfinite(scores)):
        return {**result, 'status': 'candidate_windows_have_no_variance'}
    best = int(np.argmax(scores))
    offset = first + best - left
    score = float(np.clip(scores[best], -1, 1))
    at_search_boundary = abs(offset) >= radius
    at_available_edge = best in (0, last - first)
    return {**result, 'status': 'measured', 'candidate_offset_seconds': offset / RATE,
            'candidate_window_seconds': [(first + best) / RATE, (first + best + n) / RATE],
            'correlation': score, 'offset_search_boundary_hit': at_search_boundary,
            'candidate_available_range_edge': at_available_edge,
            'high_confidence_waveform_match': score >= MIN_CORRELATION and not at_search_boundary and not at_available_edge}


def inspect_audio(a, b, video_duration, max_offset_seconds,
                  native_audio_start=None, native_video_start=None):
    plan = energy_plan(a)
    radius = round(max_offset_seconds * RATE)
    windows = [match_window(a, b, w, radius) for w in plan['windows']]
    measured = [w['candidate_offset_seconds'] for w in windows if w['candidate_offset_seconds'] is not None]
    strong = len(windows) == 3 and all(w['high_confidence_waveform_match'] for w in windows)
    spread = max(measured) - min(measured) if len(measured) == 3 else None
    uniform = strong and spread <= MAX_UNIFORM_SPREAD_SECONDS
    best_lag = round(float(np.median(measured)) * RATE) if len(measured) == 3 else None
    overlap_correlation, overlap_seconds = None, None
    if best_lag is not None:
        aa, bb = max(0, -best_lag), max(0, best_lag)
        count = min(len(a) - aa, len(b) - bb)
        if count > 0:
            overlap_correlation = pearson(a[aa:aa + count], b[bb:bb + count])
            overlap_seconds = count / RATE
    supported = bool(uniform and overlap_correlation is not None and overlap_correlation >= MIN_CORRELATION)
    status = ('supported_uniform_waveform_clock' if supported else
              'strong_local_matches_with_variable_offsets' if strong and not uniform else
              'unverified_waveform_clock')
    starts_known = native_audio_start is not None and native_video_start is not None
    start_delta = native_audio_start - native_video_start if starts_known else None
    coverage = {'status': 'unverified_without_supported_uniform_waveform_clock',
                'source_full_end_in_decoded_native_audio_seconds': None,
                'source_energy_end_in_decoded_native_audio_seconds': None,
                'source_full_end_in_picture_clock_seconds': None,
                'source_energy_end_in_picture_clock_seconds': None,
                'full_source_duration_covered_by_audio': None,
                'source_energy_extent_covered_by_audio': None,
                'source_energy_extent_covered_by_picture': None,
                'picture_after_source_energy_end_seconds': None}
    if supported:
        offset = best_lag / RATE
        full_end = len(a) / RATE + offset
        energy_start = plan['source_energy_start_seconds'] + offset
        energy_end = plan['source_energy_end_seconds'] + offset
        coverage.update(status='conditional_on_supported_waveform_clock' if starts_known else 'audio_extent_only_picture_start_times_unavailable',
                        source_full_end_in_decoded_native_audio_seconds=full_end,
                        source_energy_end_in_decoded_native_audio_seconds=energy_end,
                        full_source_duration_covered_by_audio=(offset >= -1 / RATE and full_end <= len(b) / RATE + 1 / RATE),
                        source_energy_extent_covered_by_audio=(energy_start >= -1 / RATE and energy_end <= len(b) / RATE + 1 / RATE))
        if starts_known:
            coverage.update(source_full_end_in_picture_clock_seconds=full_end + start_delta,
                            source_energy_end_in_picture_clock_seconds=energy_end + start_delta,
                            source_energy_extent_covered_by_picture=(energy_start + start_delta >= -1 / RATE and energy_end + start_delta <= video_duration + 1 / RATE),
                            picture_after_source_energy_end_seconds=video_duration - energy_end - start_delta)
    return {'analysis_sample_rate_hz': RATE, 'source_duration_seconds': len(a) / RATE,
            'native_audio_duration_seconds': len(b) / RATE,
            'energy_selection': {k: v for k, v in plan.items() if k != 'windows'},
            'offset_search_range_seconds': [-max_offset_seconds, max_offset_seconds],
            'windows': windows, 'clock_status': status,
            'minimum_window_correlation': min(w['correlation'] for w in windows) if len(windows) == 3 and all(w['correlation'] is not None for w in windows) else None,
            'candidate_offset_spread_seconds': spread,
            'reliable_local_offset_spread_seconds': spread if strong else None,
            'median_candidate_offset_seconds': best_lag / RATE if best_lag is not None else None,
            'supported_uniform_offset_seconds': best_lag / RATE if supported else None,
            'supported_source_to_picture_offset_seconds': best_lag / RATE + start_delta if supported and starts_known else None,
            'stream_start_evidence': {'native_audio_start_seconds': native_audio_start,
                                      'native_video_start_seconds': native_video_start,
                                      'audio_start_minus_video_start_seconds': start_delta},
            'full_overlap_correlation_at_median_candidate_offset': overlap_correlation,
            'overlap_duration_at_median_candidate_offset_seconds': overlap_seconds,
            'coverage': coverage,
            'lag_sign': 'Window and uniform offsets compare decoded audio sample clocks: positive means native samples occur later. '
                        'The source-to-picture offset additionally includes audio stream start minus video stream start.',
            'limits': 'Energy selects signal windows, not phonemes. Weak correlations produce only untrusted lag candidates. '
                      'Waveform matches do not establish visual lip sync, audible identity, exact words or perceptual quality.'}


def extract_frames(native, native_probe, directory):
    streams = [s for s in native_probe['streams'] if s['codec_type'] == 'video']
    if len(streams) != 1:
        raise ValueError('Expected exactly one native video stream')
    stream = streams[0]
    fps = float(Fraction(stream['avg_frame_rate']))
    count = int(stream.get('nb_read_frames') or stream.get('nb_frames'))
    if count < 1 or fps <= 0:
        raise ValueError('Native video has no measured frames or valid frame rate')
    indices = sorted(set(round(fraction * (count - 1)) for fraction in FRACTIONS))
    expression = '+'.join(f'eq(n\\,{index})' for index in indices)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(native), '-map', '0:v:0',
                    '-vf', f'select={expression}', '-fps_mode', 'vfr',
                    str(directory / 'frame-%02d.png')], check=True, stderr=subprocess.PIPE)
    frames = []
    for number, frame_index in enumerate(indices, 1):
        path = directory / f'frame-{number:02}.png'
        with Image.open(path) as source:
            dimensions = list(source.size)
        frames.append({'frame_index': frame_index, 'sample_seconds_at_average_frame_rate': frame_index / fps,
                       'path': str(path), 'sha256': sha(path), 'dimensions': dimensions})
    return {'fps': fps, 'measured_frame_count': count,
            'video_duration_seconds': float(stream.get('duration') or native_probe['format']['duration']),
            'timing_limit': 'Exact frame indices extracted; displayed times use average frame rate. Inspect probe before treating variable-rate timing as exact.',
            'frames': frames}


def build_contact(records, path):
    width, image_height, row_height = 240, 427, 490
    canvas = Image.new('RGB', (width * 4, row_height * len(records)), '#202426')
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
    except OSError:
        font = ImageFont.load_default()
    for row, record in enumerate(records):
        top = row * row_height
        draw.text((8, top + 5), f"Clip {record['index']} | {record.get('status', 'unknown')}", font=font, fill='white')
        for column, frame in enumerate(record.get('picture', {}).get('frames', [])):
            x = column * width
            label = f"{frame['sample_seconds_at_average_frame_rate']:.3f}s | frame {frame['frame_index']}"
            draw.text((x + 8, top + 29), label, font=font, fill='white')
            with Image.open(frame['path']) as image:
                image = image.convert('RGB')
                image.thumbnail((width, image_height), Image.Resampling.LANCZOS)
                canvas.paste(image, (x + (width - image.width) // 2, top + 56 + (image_height - image.height) // 2))
    canvas.save(path, quality=94)


def inspect_source(item, work, max_offset_seconds):
    directory = work / f"section-{item['index']:02}"
    directory.mkdir()
    script = directory / 'SCRIPT.txt'
    script.write_text(item['script'], encoding='utf-8')
    record = {'index': item['index'], 'status': 'inspection_error',
              'script': {'path': str(script), 'sha256': sha(script), 'text': item['script']}}
    try:
        native, voice = directory / 'native.mp4', directory / 'voice.wav'
        record['native'] = download(item['url'], item.get('sha256'), native)
        record['voice'] = download(item['voice_url'], item['voice_sha256'], voice)
        record['native_probe'] = probe(native, count_frames=True)
        record['voice_probe'] = probe(voice)
        record['picture'] = extract_frames(native, record['native_probe'], directory)
        a = audio_samples(voice)
        audio_streams = [s for s in record['native_probe']['streams'] if s['codec_type'] == 'audio']
        if audio_streams:
            b = audio_samples(native)
            video_stream = next(s for s in record['native_probe']['streams'] if s['codec_type'] == 'video')
            def start_time(stream):
                try:
                    value = float(stream['start_time'])
                    return value if math.isfinite(value) else None
                except (KeyError, TypeError, ValueError):
                    return None
            record['audio_analysis'] = inspect_audio(a, b, record['picture']['video_duration_seconds'], max_offset_seconds,
                                                     start_time(audio_streams[0]), start_time(video_stream))
        else:
            record['audio_analysis'] = {'clock_status': 'unverified_no_native_audio_stream',
                                        'source_duration_seconds': len(a) / RATE,
                                        'source_energy': energy_plan(a)}
        record['status'] = 'inspected_not_accepted'
    except Exception as exc:
        record['error_type'] = type(exc).__name__
        # Errors deliberately omit URLs, response bodies and signed upload queries.
        record['error'] = str(exc) if isinstance(exc, ValueError) else 'Inspection step failed; inspect retained sandbox files.'
    return record


def main():
    cfg = json.loads(Path(sys.argv[1]).read_text())
    validate_config(cfg)
    work = Path(cfg.get('work_dir', 'native-inspection')).resolve()
    work.mkdir(parents=True, exist_ok=False)
    records = [inspect_source(item, work, float(cfg.get('max_offset_seconds', 2))) for item in cfg['sources']]
    report = {'scope': 'Native video and exact source-slice inspection only; no assembly or repair.',
              'sources': records, 'thresholds': {'minimum_waveform_correlation': MIN_CORRELATION,
                                               'maximum_uniform_offset_spread_seconds': MAX_UNIFORM_SPREAD_SECONDS},
              'full_voice': None,
              'limits': 'No hearing, word verification, visual lip-sync acceptance, native voice acceptance or owner approval is claimed.'}
    if 'full_voice_url' in cfg:
        try:
            full = work / 'full-voice.wav'
            report['full_voice'] = download(cfg['full_voice_url'], cfg['full_voice_sha256'], full)
            report['full_voice']['probe'] = probe(full)
            report['full_voice']['decoded_duration_seconds'] = len(audio_samples(full)) / RATE
            report['full_voice']['status'] = 'inspected_integrity_and_duration_only'
            report['full_voice']['limits'] = 'No source sample map was supplied, so slice concatenation is not proved.'
        except Exception as exc:
            report['full_voice'] = {'status': 'inspection_error', 'error_type': type(exc).__name__,
                                    'error': str(exc) if isinstance(exc, ValueError) else 'Full-voice inspection failed; inspect retained sandbox files.'}
    contact = work / 'contact.jpg'
    build_contact(records, contact)
    upload = cfg['contact_upload']
    report['contact'] = {'path': str(contact), 'sha256': sha(contact), 'bytes': contact.stat().st_size,
                         'media_id': upload['media_id'], 'content_type': 'image/jpeg', 'upload_status': 'pending'}
    # Preserve the report before PUT; the presigned destination is never printed.
    report_path = work / 'REPORT.json'
    report_path.write_text(json.dumps(report, indent=2, allow_nan=False))
    try:
        request = urllib.request.Request(upload['upload_url'], data=contact.read_bytes(),
                                        headers={'Content-Type': upload['content_type']}, method='PUT')
        with urllib.request.urlopen(request, timeout=60) as response:
            report['contact']['upload_http_status'] = response.status
            report['contact']['upload_status'] = 'uploaded' if 200 <= response.status < 300 else 'failed'
    except Exception as exc:
        report['contact']['upload_status'] = 'failed'
        report['contact']['error_type'] = type(exc).__name__
    report_bytes = json.dumps(report, indent=2, allow_nan=False).encode('utf-8')
    report_path.write_bytes(report_bytes)
    summary = {'sources': [{'index': r['index'], 'status': r['status'],
                            'native_sha256': r.get('native', {}).get('sha256'),
                            'clock_status': r.get('audio_analysis', {}).get('clock_status'),
                            'minimum_window_correlation': r.get('audio_analysis', {}).get('minimum_window_correlation'),
                            'supported_uniform_offset_seconds': r.get('audio_analysis', {}).get('supported_uniform_offset_seconds'),
                            'reliable_local_offset_spread_seconds': r.get('audio_analysis', {}).get('reliable_local_offset_spread_seconds')}
                           for r in records], 'contact': report['contact'], 'report_sha256': sha(report_path)}
    print('REPORT_BASE64=' + base64.b64encode(report_bytes).decode(), flush=True)
    print('SUMMARY=' + json.dumps(summary, allow_nan=False), flush=True)
    full_ok = report['full_voice'] is None or report['full_voice'].get('status') != 'inspection_error'
    return 0 if full_ok and all(r['status'] == 'inspected_not_accepted' for r in records) and report['contact']['upload_status'] == 'uploaded' else 2


if __name__ == '__main__':
    raise SystemExit(main())
