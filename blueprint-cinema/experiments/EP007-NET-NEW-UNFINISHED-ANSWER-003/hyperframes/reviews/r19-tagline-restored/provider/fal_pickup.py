"""Execute the exact authorized one-take proposal. Submission is never retried."""
from pathlib import Path
import base64, datetime, hashlib, json, sys, urllib.error, urllib.parse, urllib.request

root = Path(__file__).resolve().parent
repo = Path(__file__).resolve().parents[7]
proposal = json.loads((root / 'PROPOSED-REQUEST.json').read_text())
auth = json.loads((root / 'GENERATION-AUTHORIZATION.json').read_text())
assert auth['status'] == 'authorized' and auth['maximum_submissions'] == 1
assert proposal['model'] == auth['model'] == 'fal-ai/kling-video/ai-avatar/v2/pro'
key = None
for line in (repo / '.env').read_text().splitlines():
    if line.strip().startswith('FAL_KEY='):
        key = line.split('=', 1)[1].strip().strip('"').strip("'")
        break
if not key:
    raise SystemExit('FAL_KEY unavailable; no submission made')

def save(name, value):
    (root / name).write_text(json.dumps(value, indent=2) + '\n')

def call(url, payload=None):
    assert urllib.parse.urlparse(url).hostname == 'queue.fal.run'
    request = urllib.request.Request(url, data=json.dumps(payload).encode() if payload else None,
        headers={'Authorization': 'Key ' + key, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)

mode = sys.argv[1]
if mode == 'submit':
    assert proposal['expected_cost_usd'] <= auth['estimated_usd_ceiling']
    payload = {'prompt': proposal['prompt']}
    for field, mime in [('image', 'image/png'), ('audio', 'audio/wav')]:
        data = (root / proposal[field + '_local_path']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == proposal[field + '_sha256']
        payload[field + '_url'] = 'data:' + mime + ';base64,' + base64.b64encode(data).decode()
    # Exclusive marker is written before network I/O, including uncertain outcomes.
    with (root / 'SUBMISSION-ATTEMPT.json').open('x') as marker:
        json.dump({'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'model': auth['model'], 'submission_number': 1, 'automatic_retries': 0,
                   'proposal_sha256': hashlib.sha256((root / 'PROPOSED-REQUEST.json').read_bytes()).hexdigest(),
                   'payload_sha256': hashlib.sha256(json.dumps(payload).encode()).hexdigest()}, marker, indent=2)
    try:
        result = call('https://queue.fal.run/' + auth['model'], payload)
    except Exception as error:
        detail = error.read().decode('utf-8', errors='replace') if isinstance(error, urllib.error.HTTPError) else str(error)
        failure = {'submission_attempted': True, 'outcome': 'failed_or_uncertain',
                   'http_status': getattr(error, 'code', None), 'detail': detail.replace(key, '[REDACTED]'),
                   'may_retry': False}
        save('ERROR.json', failure)
        raise SystemExit(json.dumps(failure))
    save('JOB.json', result)
elif mode in ('status', 'result'):
    job = json.loads((root / 'JOB.json').read_text())
    result = call(job['status_url' if mode == 'status' else 'response_url'])
    save(mode.upper() + '.json', result)
else:
    raise SystemExit('Use submit, status or result')
print(json.dumps(result, indent=2))
