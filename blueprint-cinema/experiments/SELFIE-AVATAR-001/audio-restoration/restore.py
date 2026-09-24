"""Isolated SELFIE-AVATAR-001 restoration using the accepted V5 Fal route."""
import datetime
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[3]
AUDIO_URL = 'https://d2ol7oe51mr4n9.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/1c10910f-7a81-4620-bad8-34619b3b3911.mp3'
MODEL = 'fal-ai/sync-lipsync/v3'


def credential():
    for line in (REPO / '.env').read_text().splitlines():
        match = re.match(r'^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$', line)
        if match:
            return match.group(1).strip().strip('\"').strip("'")
    raise ValueError('FAL_KEY unavailable')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def call(url, output, body=None):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname != 'queue.fal.run':
        raise ValueError('Unapproved API host')
    key = credential()
    request = urllib.request.Request(url,
        data=json.dumps(body).encode() if body is not None else None,
        headers={'Authorization': 'Key ' + key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=45) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read(8000).decode(errors='replace').replace(key, '[REDACTED]')
        write(output / 'SYNC-ERROR.json', {'http_status': error.code, 'detail': detail,
            'submission_state': 'Inspect existing intent/job before retry; no automatic duplicate.'})
        raise SystemExit('Fal request failed; inspect scoped SYNC-ERROR.json')


def main():
    mode, label = sys.argv[1:3]
    if label not in ('home', 'outdoors', 'cafe'):
        raise ValueError('Unknown authorized test label')
    output = BASE / label
    output.mkdir(exist_ok=True)
    record = output / 'SYNC-JOB.json'
    intent = output / 'SYNC-SUBMISSION-INTENT.json'
    if mode == 'prepare':
        if record.exists() or intent.exists():
            raise SystemExit('Submission exists; do not alter this request')
        url = sys.argv[3]
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != 'https' or not parsed.hostname.endswith('.cloudfront.net'):
            raise ValueError('Expected confirmed Higgsfield video URL')
        result = {'model': MODEL, 'input': {'video_url': url,
            'audio_url': AUDIO_URL, 'sync_mode': 'silence'},
            'scope': 'One authorized original-audio restoration for the isolated selfie experiment; preserve native output.'}
        write(output / 'SYNC-REQUEST.json', result)
    elif mode == 'submit':
        if record.exists() or intent.exists():
            raise SystemExit('Existing submission record or intent: inspect before retry')
        spec = json.loads((output / 'SYNC-REQUEST.json').read_text())
        write(intent, {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'scope': spec['scope'], 'model': spec['model']})
        result = call('https://queue.fal.run/' + spec['model'], output, spec['input'])
        write(record, result)
    elif mode in ('status', 'result'):
        job = json.loads(record.read_text())
        result = call(job['status_url'] if mode == 'status' else job['response_url'], output)
        write(output / ('SYNC-STATUS.json' if mode == 'status' else 'SYNC-RESULT.json'), result)
    else:
        raise ValueError('Unknown operation')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
