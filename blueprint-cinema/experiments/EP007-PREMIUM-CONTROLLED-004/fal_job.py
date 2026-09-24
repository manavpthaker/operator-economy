import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

base = Path(__file__).resolve().parent
repo = base.parents[2]
key = None
for line in (repo / '.env').read_text().splitlines():
    if line.strip().startswith('FAL_KEY='):
        key = line.split('=', 1)[1].strip().strip('\"').strip("'")
        break
if not key:
    raise SystemExit('FAL_KEY unavailable')

def call(url, body=None):
    if urllib.parse.urlparse(url).hostname != 'queue.fal.run':
        raise ValueError('Unexpected Fal API host')
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, headers={'Authorization': 'Key ' + key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode('utf-8', errors='replace').replace(key, '[REDACTED]')
        failure = {'http_status': error.code, 'detail': detail, 'job_submitted': False}
        (base / (prefix + '-ERROR.json')).write_text(json.dumps(failure, indent=2) + '\n')
        raise SystemExit(json.dumps(failure))

mode = sys.argv[1]
prefix = sys.argv[2] if len(sys.argv) > 2 else 'FAL'
if prefix not in {'FAL', 'FAL-KLING', 'FAL-SYNC'}:
    raise SystemExit('Unknown request prefix')
record = base / (prefix + '-JOB.json')
if mode == 'submit':
    if record.exists():
        raise SystemExit('Existing job record; refusing duplicate submission')
    spec = json.loads((base / (prefix + '-REQUEST.json')).read_text())
    result = call('https://queue.fal.run/' + spec['model'], spec['input'])
    record.write_text(json.dumps(result, indent=2) + '\n')
elif mode == 'status':
    job = json.loads(record.read_text())
    result = call(job['status_url'])
    (base / (prefix + '-STATUS.json')).write_text(json.dumps(result, indent=2) + '\n')
elif mode == 'result':
    job = json.loads(record.read_text())
    result = call(job['response_url'])
    (base / (prefix + '-RESULT.json')).write_text(json.dumps(result, indent=2) + '\n')
else:
    raise SystemExit('Mode must be submit, status or result')
print(json.dumps(result))
