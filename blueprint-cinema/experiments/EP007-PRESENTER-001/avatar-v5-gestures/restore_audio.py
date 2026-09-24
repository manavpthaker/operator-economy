import datetime
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent

def credential():
    for line in Path('/Users/brownmanbrain/GitHub/operator-economy/.env').read_text().splitlines():
        match = re.match(r'^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$', line)
        if match:
            return match.group(1).strip().strip('\"').strip("'")
    raise ValueError('FAL_KEY unavailable')

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

def write(name, data):
    (BASE / name).write_text(json.dumps(data, indent=2) + '\n')

def call(url, body=None):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname != 'queue.fal.run':
        raise ValueError('Unapproved API host')
    key = credential()
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
        headers={'Authorization': 'Key ' + key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.build_opener(NoRedirect()).open(req, timeout=45) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read(8000).decode(errors='replace').replace(key, '[REDACTED]')
        write('SYNC-ERROR.json', {'http_status': error.code, 'detail': detail,
            'submission_state': 'inspect before retry; no automatic duplicate'})
        raise SystemExit('Fal request failed; inspect SYNC-ERROR.json')

mode = sys.argv[1]
record = BASE / 'SYNC-JOB.json'
if mode == 'submit':
    if record.exists() or (BASE / 'SYNC-SUBMISSION-INTENT.json').exists():
        raise SystemExit('Existing submission record or intent: inspect before retry')
    spec = json.loads((BASE / 'SYNC-REQUEST.json').read_text())
    write('SYNC-SUBMISSION-INTENT.json', {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope': 'One authorized audio restoration pass', 'model': spec['model']})
    result = call('https://queue.fal.run/' + spec['model'], spec['input'])
    write('SYNC-JOB.json', result)
elif mode in ('status', 'result'):
    job = json.loads(record.read_text())
    result = call(job['status_url'] if mode == 'status' else job['response_url'])
    write('SYNC-STATUS.json' if mode == 'status' else 'SYNC-RESULT.json', result)
else:
    raise SystemExit('Unknown operation')
print(json.dumps(result))
