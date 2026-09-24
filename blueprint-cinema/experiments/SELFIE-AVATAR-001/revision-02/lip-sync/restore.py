"""One new revision-02 voice-B restoration; no old seven-second inputs or intents."""
import datetime
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
MEDIA = REPO / 'blueprint-cinema/experiments/SELFIE-AVATAR-001/media/revision-02'
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
        raise SystemExit('Fal returned an error; inspect revision-02/lip-sync/ERROR.json')


def fetch(url):
    parsed = urllib.parse.urlsplit(url)
    assert parsed.scheme == 'https'
    with OPENER.open(url, timeout=45) as response:
        return response.read()


def main():
    mode = sys.argv[1]
    local_audio = REPO / INPUT['audio_local_path']
    assert SHA(local_audio.read_bytes()) == INPUT['audio_sha256']
    if mode == 'prepare':
        assert not (BASE / 'SUBMISSION-INTENT.json').exists()
        url = sys.argv[2]
        parsed = urllib.parse.urlsplit(url)
        assert parsed.scheme == 'https' and parsed.hostname.endswith('.cloudfront.net')
        assert INPUT['native_higgsfield_job_id'] in parsed.path
        assert SHA(fetch(INPUT['audio_url'])) == INPUT['audio_sha256']
        result = {'model': INPUT['model'], 'input': {'video_url': url,
            'audio_url': INPUT['audio_url'], 'sync_mode': INPUT['sync_mode']},
            'input_record_sha256': SHA((BASE / 'INPUT.json').read_bytes())}
        save('REQUEST.json', result, exclusive=True)
    elif mode == 'submit':
        assert not (BASE / 'JOB.json').exists()
        request = json.loads((BASE / 'REQUEST.json').read_text())
        assert request['input_record_sha256'] == SHA((BASE / 'INPUT.json').read_bytes())
        save('SUBMISSION-INTENT.json', {'at': NOW(), 'scope': INPUT['scope'],
            'model': request['model'], 'request_sha256': SHA((BASE / 'REQUEST.json').read_bytes()),
            'audio_sha256': INPUT['audio_sha256'], 'retry': False}, exclusive=True)
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
        path = MEDIA / 'home-olive-voice-b-sync.mp4'
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
