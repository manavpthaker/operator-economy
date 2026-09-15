"""Bounded original-audio restoration for the three authorized V5 passages."""
import concurrent.futures
import datetime
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = Path(__file__).resolve().parent
ROOT = next(p for p in BASE.parents if (p / '.agents').is_dir())


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def credential():
    for line in (ROOT / '.env').read_text().splitlines():
        m = re.match(r'^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$', line)
        if m:
            return m.group(1).strip().strip('\"').strip("'")
    raise RuntimeError('FAL_KEY unavailable')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def call(url, body=None):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname != 'queue.fal.run':
        raise ValueError('Unexpected API host')
    key = credential()
    request = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
        headers={'Authorization': 'Key ' + key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=45) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read(8000).decode(errors='replace').replace(key, '[REDACTED]')
        raise RuntimeError(f'Fal HTTP {error.code}: {detail}') from None


def process(row, mode):
    folder = BASE / row['take']
    folder.mkdir(exist_ok=True)
    intent = folder / 'SYNC-SUBMISSION-INTENT.json'
    job_path = folder / 'SYNC-JOB.json'
    if mode == 'submit':
        if intent.exists() or job_path.exists():
            return {'take': row['take'], 'status': 'existing_intent_no_duplicate_submission'}
        request = {'model': 'fal-ai/sync-lipsync/v3', 'input': {
            'video_url': row['video_url'], 'audio_url': row['audio_url'], 'sync_mode': 'silence'}}
        write(folder / 'SYNC-REQUEST.json', request)
        write(intent, {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'scope': 'One original-WAV restoration under GENERATION-AUTHORIZATION.json',
            'native_video_sha256': row['native_video_sha256'], 'audio_sha256': row['audio_sha256']})
        try:
            result = call('https://queue.fal.run/' + request['model'], request['input'])
        except Exception as error:
            write(folder / 'SYNC-ERROR.json', {'error': str(error), 'retry': 'No automatic retry; inspect intent first'})
            return {'take': row['take'], 'status': 'submission_uncertain', 'error': str(error)}
        write(job_path, result)
    else:
        job = json.loads(job_path.read_text())
        result = call(job['status_url'] if mode == 'status' else job['response_url'])
        write(folder / ('SYNC-STATUS.json' if mode == 'status' else 'SYNC-RESULT.json'), result)
    return {'take': row['take'], 'result': result}


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode not in {'submit', 'status', 'result'}:
        raise SystemExit('Expected submit, status or result')
    rows = json.loads((BASE / 'RESTORATION-BATCH.json').read_text())
    authorization = json.loads((BASE / 'GENERATION-AUTHORIZATION.json').read_text())
    allowed = {'v5-opportunity', 'v5-post-title-continuous', 'v5-question'}
    assert 1 <= len(rows) <= 3
    assert len({r['take'] for r in rows}) == len(rows)
    assert {r['take'] for r in rows} <= allowed
    assert sum(r['native_duration_seconds'] for r in rows) * 8 / 60 <= authorization['caps']['fal_restoration_usd']
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda row: process(row, mode), rows))
    print(json.dumps(results))
