"""R6: one guarded Sync v3 submission per matched section; no automatic retry."""
import datetime
import hashlib
import io
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import wave
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
MEDIA = REPO / 'blueprint-cinema/experiments/SELFIE-AVATAR-001/media/revision-06'
CONFIG = json.loads((BASE / 'INPUT.json').read_text())
SHA = lambda data: hashlib.sha256(data).hexdigest()
NOW = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()


def save(directory, name, value, exclusive=False):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / name).open('x' if exclusive else 'w') as output:
        json.dump(value, output, indent=2)
        output.write('\n')


def read(directory, name):
    return json.loads((directory / name).read_text())


def credential():
    for line in (REPO / '.env').read_text().splitlines():
        match = re.match(r'^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$', line)
        if match:
            return match.group(1).strip().strip('"').strip("'")
    raise ValueError('FAL_KEY unavailable')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect())


def api(directory, url, payload=None):
    parsed = urllib.parse.urlsplit(url)
    assert parsed.scheme == 'https' and parsed.hostname == 'queue.fal.run'
    key = credential()
    request = urllib.request.Request(url,
        data=None if payload is None else json.dumps(payload).encode(),
        headers={'Authorization': 'Key ' + key, 'Content-Type': 'application/json',
            'X-Fal-No-Retry': '1', 'x-app-fal-disable-fallback': '1'})
    try:
        with OPENER.open(request, timeout=45) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read(8000).decode(errors='replace').replace(key, '[REDACTED]')
        save(directory, 'ERROR.json', {'at': NOW(), 'http_status': error.code,
            'detail': detail, 'is_submission': payload is not None,
            'instruction': 'Stop and report. Preserve intent; no additional paid call or retry is authorized by this error.'})
        raise SystemExit('Fal returned an error; inspect the section ERROR.json without resubmitting')
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        save(directory, 'TRANSPORT-UNCERTAIN.json', {'at': NOW(),
            'exception_type': type(error).__name__, 'request_url': url,
            'is_submission': payload is not None,
            'instruction': 'Do not retry submission; inspect preserved intent and provider state.'}, exclusive=True)
        raise SystemExit('Outcome uncertain; do not submit again')


def fetch(url):
    parsed = urllib.parse.urlsplit(url)
    assert parsed.scheme == 'https' and parsed.hostname
    with OPENER.open(url, timeout=45) as response:
        return response.read()


def pcm(data, expected_count):
    with wave.open(io.BytesIO(data)) as audio:
        assert (audio.getframerate(), audio.getnchannels(), audio.getsampwidth(), audio.getnframes()) == (
            48000, 1, 2, expected_count)
        assert audio.getcomptype() == 'NONE'
        return audio.readframes(expected_count)


def source_pcm():
    source = CONFIG['source_audio']
    data = (REPO / source['local_path']).read_bytes()
    assert SHA(data) == source['sha256']
    script = CONFIG['script']
    assert SHA((REPO / script['local_path']).read_bytes()) == script['sha256']
    return pcm(data, source['sample_count'])


def media_local(item):
    path = (REPO / item['local_path']).resolve()
    assert path.is_relative_to(MEDIA.resolve()), 'R6 input must live inside ignored media/revision-06'
    assert re.fullmatch(r'[0-9a-f]{64}', item['sha256'])
    data = path.read_bytes()
    assert SHA(data) == item['sha256'], 'Local input hash mismatch'
    return data


def validate_section(section, expected, source, hosted):
    assert section['index'] == expected['index']
    video, audio = section['video'], section['audio']
    for key, value in CONFIG['picture'].items():
        assert video[key] == value, key
    frames = expected['frame_count']
    count = expected['audio_sample_count']
    assert video['frame_count'] == frames
    assert abs(video['duration_seconds'] - frames / 24) < .000001
    assert audio['sample_count'] == count
    assert count == frames * 2000
    assert (audio['sample_rate_hz'], audio['channels'], audio['sample_width_bytes']) == (48000, 1, 2)
    video_data, audio_data = media_local(video), media_local(audio)
    start, end = expected['source_sample_range']
    required = source[start*2:end*2] + b'\x00\x00' * expected['tail_zero_samples']
    assert pcm(audio_data, count) == required, 'Section PCM differs from unchanged source range plus allowed tail silence'
    if hosted:
        assert SHA(fetch(video['url'])) == SHA(video_data), 'Hosted video mismatch'
        hosted_audio = fetch(audio['url'])
        assert SHA(hosted_audio) == SHA(audio_data), 'Hosted audio mismatch'
        assert pcm(hosted_audio, count) == required
    return {'source_sample_range': [start, end], 'tail_zero_samples': expected['tail_zero_samples'],
        'exact_source_pcm_verified': True, 'source_pcm_sha256': SHA(source[start*2:end*2]),
        'matched_audio_pcm_sha256': SHA(required), 'duration_seconds': count / 48000}


def main():
    mode = sys.argv[1]
    original = source_pcm()
    if mode == 'preflight':
        print(json.dumps({'status': 'ready_waiting_for_root_matched_manifest',
            'sections': CONFIG['sections'], 'submitted_sections': [
                x.name for x in BASE.glob('section-*') if (x / 'SUBMISSION-INTENT.json').exists()]}))
        return
    if mode == 'bind':
        assert not (BASE / 'MANIFEST.json').exists()
        incoming_path = Path(sys.argv[2]).resolve()
        incoming = read(incoming_path.parent, incoming_path.name)
        assert len(incoming['sections']) == 3
        assert [s['index'] for s in incoming['sections']] == [1, 2, 3]
        checks = []
        for section, expected in zip(incoming['sections'], CONFIG['sections']):
            directory = BASE / f"section-{section['index']:02d}"
            assert not directory.exists(), 'An existing section directory prevents rebinding'
            checks.append(validate_section(section, expected, original, hosted=True))
        manifest = {'root_manifest_path': str(incoming_path.relative_to(REPO)),
            'root_manifest_sha256': SHA(incoming_path.read_bytes()),
            'input_record_sha256': SHA((BASE / 'INPUT.json').read_bytes()),
            'matched_sections': incoming['sections'], 'verified_at': NOW(), 'checks': checks}
        save(BASE, 'MANIFEST.json', manifest, exclusive=True)
        for section, check in zip(incoming['sections'], checks):
            directory = BASE / f"section-{section['index']:02d}"
            save(directory, 'INPUT.json', {'section': section, 'source_check': check}, exclusive=True)
            save(directory, 'REQUEST.json', {'model': CONFIG['model'],
                'input': {'video_url': section['video']['url'], 'audio_url': section['audio']['url'],
                    'sync_mode': CONFIG['sync_mode']},
                'configuration_sha256': SHA((BASE / 'INPUT.json').read_bytes()),
                'manifest_sha256': SHA((BASE / 'MANIFEST.json').read_bytes()),
                'section_input_sha256': SHA((directory / 'INPUT.json').read_bytes())}, exclusive=True)
        print(json.dumps({'status': 'three_inputs_bound_no_submission', 'checks': checks}))
        return

    index = int(sys.argv[2])
    assert 1 <= index <= 3
    directory = BASE / f'section-{index:02d}'
    if mode == 'submit':
        assert not (directory / 'JOB.json').exists()
        assert not (directory / 'SUBMISSION-INTENT.json').exists()
        assert not list(BASE.glob('section-*/ERROR.json')), 'Existing provider error requires root review'
        assert not list(BASE.glob('section-*/TRANSPORT-UNCERTAIN.json')), 'Uncertainty requires root review'
        request = read(directory, 'REQUEST.json')
        assert request['model'] == CONFIG['model'] == 'fal-ai/sync-lipsync/v3'
        assert request['input']['sync_mode'] == CONFIG['sync_mode'] == 'cut_off'
        assert set(request['input']) == {'video_url', 'audio_url', 'sync_mode'}
        for key, path in [
            ('configuration_sha256', BASE / 'INPUT.json'), ('manifest_sha256', BASE / 'MANIFEST.json'),
            ('section_input_sha256', directory / 'INPUT.json')]:
            assert request[key] == SHA(path.read_bytes()), key
        section = read(directory, 'INPUT.json')['section']
        validate_section(section, CONFIG['sections'][index-1], original, hosted=False)
        assert request['input']['video_url'] == section['video']['url']
        assert request['input']['audio_url'] == section['audio']['url']
        save(directory, 'SUBMISSION-INTENT.json', {'at': NOW(), 'index': index,
            'scope': CONFIG['scope'], 'model': CONFIG['model'], 'retry': False,
            'request_sha256': SHA((directory / 'REQUEST.json').read_bytes()),
            'video_sha256': section['video']['sha256'], 'audio_sha256': section['audio']['sha256']}, exclusive=True)
        result = api(directory, 'https://queue.fal.run/' + request['model'], request['input'])
        save(directory, 'JOB.json', result, exclusive=True)
    elif mode in ('status', 'result'):
        job = read(directory, 'JOB.json')
        result = api(directory, job['status_url'] if mode == 'status' else job['response_url'])
        save(directory, 'STATUS.json' if mode == 'status' else 'RESULT.json', result)
    elif mode == 'download':
        url = read(directory, 'RESULT.json')['video']['url']
        data = fetch(url)
        destination = MEDIA / f'home-olive-gtm-r6-section-{index:02d}-sync.mp4'
        if destination.exists():
            assert SHA(destination.read_bytes()) == SHA(data)
        else:
            with destination.open('xb') as output:
                output.write(data)
        result = {'url': url, 'local_path': str(destination.relative_to(REPO)),
            'sha256': SHA(data), 'bytes': len(data)}
        save(directory, 'DOWNLOAD.json', result)
    else:
        raise ValueError('Unknown operation')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()

