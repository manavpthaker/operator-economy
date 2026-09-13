"""One R5 picture restoration using retained full R4 voice; fresh request and intent."""
import datetime
import hashlib
import json
import re
import sys
import wave
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
MEDIA = REPO / 'blueprint-cinema/experiments/SELFIE-AVATAR-001/media/revision-05'
INPUT = json.loads((BASE / 'INPUT.json').read_text())
SHA = lambda b: hashlib.sha256(b).hexdigest()
NOW = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()


def save(name, data, exclusive=False):
    with (BASE / name).open('x' if exclusive else 'w') as output:
        json.dump(data, output, indent=2)
        output.write('\n')


def credential():
    for line in (REPO / '.env').read_text().splitlines():
        match = re.match(r'^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$', line)
        if match:
            return match.group(1).strip().strip('\"').strip("'")
    raise ValueError('FAL_KEY unavailable')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect())


def api(url, payload=None):
    parsed = urllib.parse.urlsplit(url)
    assert parsed.scheme == 'https' and parsed.hostname == 'queue.fal.run'
    key = credential()
    req = urllib.request.Request(url, data=None if payload is None else json.dumps(payload).encode(),
        headers={'Authorization': 'Key ' + key, 'Content-Type': 'application/json',
            'X-Fal-No-Retry': '1', 'x-app-fal-disable-fallback': '1'})
    try:
        with OPENER.open(req, timeout=45) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read(8000).decode(errors='replace').replace(key, '[REDACTED]')
        save('ERROR.json', {'at': NOW(), 'http_status': error.code, 'detail': detail,
            'instruction': 'Inspect preserved intent/job before continuing. Do not duplicate an uncertain submission.'})
        raise SystemExit('Fal returned an error; inspect revision-05/lip-sync/ERROR.json')
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        save('TRANSPORT-UNCERTAIN.json', {'at': NOW(), 'exception_type': type(error).__name__,
            'request_url': url, 'is_submission': payload is not None,
            'instruction': 'Do not retry a submission. Inspect the preserved intent and provider state first.'}, exclusive=True)
        raise SystemExit('Fal request outcome uncertain; inspect intent and provider state without resubmission')


def fetch(url):
    parsed = urllib.parse.urlsplit(url)
    assert parsed.scheme == 'https'
    with OPENER.open(url, timeout=45) as response:
        return response.read()


def main():
    mode = sys.argv[1]
    local_audio = REPO / INPUT['audio_local_path']
    assert SHA(local_audio.read_bytes()) == INPUT['audio_sha256']
    assert SHA((REPO / INPUT['script_path']).read_bytes()) == INPUT['script_sha256']
    with wave.open(str(local_audio)) as handle:
        assert (handle.getframerate(), handle.getnchannels(), handle.getsampwidth(), handle.getnframes()) == (
            INPUT['audio_sample_rate_hz'], INPUT['audio_channels'], INPUT['audio_sample_width_bytes'], INPUT['audio_sample_count'])
    if mode == 'preflight':
        result = {'status':'prepared_no_submission','audio_sha256':INPUT['audio_sha256'],
            'audio_duration_seconds':INPUT['audio_duration_seconds'],'expected_native':INPUT['expected_native']}
    elif mode == 'prepare':
        assert not (BASE / 'SUBMISSION-INTENT.json').exists()
        incoming_path = Path(sys.argv[2]).resolve()
        manifest = json.loads(incoming_path.read_text())
        expected = INPUT['expected_native']
        for field in ('width','height','frame_rate','frame_count','segment_frame_counts','audio_stream_count'):
            assert manifest[field] == expected[field], field
        assert abs(manifest['video_duration_seconds'] - expected['video_duration_seconds']) < .00001
        assert manifest['video_duration_seconds'] >= INPUT['audio_duration_seconds']
        assert manifest['frame_count'] == sum(manifest['segment_frame_counts'])
        assert manifest['sha256'] and len(manifest['sha256']) == 64
        video = (REPO / manifest['local_path']).resolve()
        assert video.is_relative_to(MEDIA.resolve())
        assert SHA(video.read_bytes()) == manifest['sha256']
        url = manifest['video_url']
        parsed = urllib.parse.urlsplit(url)
        assert parsed.scheme == 'https' and parsed.hostname
        assert SHA(fetch(url)) == manifest['sha256'], 'Hosted native differs from local assembly'
        assert SHA(fetch(INPUT['audio_url'])) == INPUT['audio_sha256']
        save('NATIVE-INPUT.json', manifest, exclusive=True)
        result = {'model': INPUT['model'], 'input': {'video_url': url,
            'audio_url': INPUT['audio_url'], 'sync_mode': INPUT['sync_mode']},
            'input_record_sha256': SHA((BASE / 'INPUT.json').read_bytes()),
            'native_input_sha256': SHA((BASE / 'NATIVE-INPUT.json').read_bytes())}
        save('REQUEST.json', result, exclusive=True)
    elif mode == 'submit':
        assert not (BASE / 'JOB.json').exists()
        request = json.loads((BASE / 'REQUEST.json').read_text())
        assert request['input_record_sha256'] == SHA((BASE / 'INPUT.json').read_bytes())
        assert request['native_input_sha256'] == SHA((BASE / 'NATIVE-INPUT.json').read_bytes())
        native = json.loads((BASE / 'NATIVE-INPUT.json').read_text())
        assert SHA((REPO / native['local_path']).read_bytes()) == native['sha256']
        save('SUBMISSION-INTENT.json', {'at': NOW(), 'scope': INPUT['scope'],
            'model': request['model'], 'request_sha256': SHA((BASE / 'REQUEST.json').read_bytes()),
            'audio_sha256': INPUT['audio_sha256'], 'native_sha256': native['sha256'], 'retry': False}, exclusive=True)
        result = api('https://queue.fal.run/' + request['model'], request['input'])
        save('JOB.json', result, exclusive=True)
    elif mode in ('status', 'result'):
        job = json.loads((BASE / 'JOB.json').read_text())
        result = api(job['status_url'] if mode == 'status' else job['response_url'])
        save('STATUS.json' if mode == 'status' else 'RESULT.json', result)
    elif mode == 'download':
        result = json.loads((BASE / 'RESULT.json').read_text())
        url = result['video']['url']
        data = fetch(url)
        path = MEDIA / 'home-olive-gtm-r5-sync.mp4'
        if path.exists():
            assert SHA(path.read_bytes()) == SHA(data)
        else:
            with path.open('xb') as output:
                output.write(data)
        result = {'url': url, 'path': str(path.relative_to(REPO)), 'bytes': len(data), 'sha256': SHA(data)}
        save('DOWNLOAD.json', result)
    else:
        raise ValueError('Unknown operation')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()

