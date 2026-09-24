"""EP009 film lane operations. Fal transport adapted from EP007 r52 fal_ops_v5.py.
Every paid submit writes a ledger intent first and refuses to run if a job already exists for the take folder."""
import datetime, hashlib, json, re, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
FILM = BASE.parent
BUILD = FILM.parent
REPO = next(p for p in BASE.parents if (p / '.agents').is_dir())
LEDGER = BUILD / 'ledger/film.jsonl'
MODEL = 'fal-ai/kling-video/v3/pro/image-to-video'
FAL_CAP = 10.0
CREDIT_CAP = 120
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
read = lambda p: json.loads(Path(p).read_text())
def save(p, d): Path(p).write_text(json.dumps(d, indent=2) + '\n')

def key():
    for line in (REPO / '.env').read_text().splitlines():
        m = re.match(r'^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$', line)
        if m: return m.group(1).strip().strip('"').strip("'")
    raise RuntimeError('Fal credential unavailable')

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
OPENER = urllib.request.build_opener(NoRedirect())

def api(url, body=None):
    u = urllib.parse.urlsplit(url)
    assert u.scheme == 'https' and u.hostname in {'queue.fal.run', 'rest.fal.ai'}
    req = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), headers={'Authorization': 'Key ' + key(), 'Content-Type': 'application/json', 'X-Fal-No-Retry': '1', 'x-app-fal-disable-fallback': '1'})
    try:
        with OPENER.open(req, timeout=45) as res: return json.load(res)
    except urllib.error.HTTPError as err:
        raise RuntimeError('Fal HTTP ' + str(err.code) + ': ' + err.read(8000).decode(errors='replace').replace(key(), '[REDACTED]')) from None

def get(url):
    assert urllib.parse.urlsplit(url).scheme == 'https'
    with OPENER.open(url, timeout=120) as res: return res.read()

def ledger_lines():
    if not LEDGER.exists(): return []
    return [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]

def committed():
    """Sum of done/failed actuals plus open intents at estimate."""
    usd = cr = 0.0; open_ = {}
    for e in ledger_lines():
        k = e['item']
        if e['status'] == 'intent': open_[k] = e
        else:
            open_.pop(k, None)
            usd += e.get('actual_usd') or 0; cr += e.get('actual_credits') or 0
    for e in open_.values():
        usd += e.get('est_usd') or 0; cr += e.get('est_credits') or 0
    return round(usd, 3), cr

def append(entry):
    entry = {'at': now(), 'lane': 'film', **entry}
    with LEDGER.open('a') as f: f.write(json.dumps(entry) + '\n')
    return entry

def upload(path, folder, mime='image/png'):
    raw = Path(path).read_bytes(); receipt = folder / 'UPLOAD.json'
    if receipt.exists():
        d = read(receipt)
        if d['status'] == 'verified' and d['sha256'] == sha(raw): return d['file_url']
    ack = api('https://rest.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3', {'content_type': mime, 'file_name': 'ep009-film-' + sha(raw)[:16] + Path(path).suffix})
    save(receipt, {'status': 'uploading', 'sha256': sha(raw), 'file_url': ack['file_url'], 'at': now()})
    req = urllib.request.Request(ack['upload_url'], data=raw, method='PUT', headers={'Content-Type': mime})
    with OPENER.open(req, timeout=120) as res: res.read()
    assert sha(get(ack['file_url'])) == sha(raw)
    save(receipt, {'status': 'verified', 'sha256': sha(raw), 'file_url': ack['file_url'], 'at': now()})
    return ack['file_url']

def submit(folder, reason):
    folder = Path(folder); req = read(folder / 'REQUEST.local.json')
    assert not (folder / 'SUBMISSION-INTENT.json').exists(), 'Existing intent; never duplicate'
    assert req['input']['duration'] == '8' and req['input']['generate_audio'] is False
    est = 0.896
    usd, _ = committed()
    if usd + est > FAL_CAP: raise SystemExit(f'CAP: committed {usd} + {est} exceeds {FAL_CAP}')
    start = REPO / req['local_start_image']; assert sha(start.read_bytes()) == req['start_image_sha256']
    payload = dict(req['input']); payload['start_image_url'] = upload(start, folder)
    save(folder / 'REQUEST.json', {'model': MODEL, 'input': payload})
    item = folder.name
    append({'item': item, 'provider': 'fal', 'model': MODEL, 'est_credits': 0, 'est_usd': est, 'reason': reason, 'status': 'intent'})
    with (folder / 'SUBMISSION-INTENT.json').open('x') as f:
        json.dump({'at': now(), 'model': MODEL, 'payload': payload, 'estimated_usd': est, 'no_retry': True}, f, indent=2)
    try: result = api('https://queue.fal.run/' + MODEL, payload)
    except Exception as err:
        save(folder / 'ERROR.json', {'at': now(), 'error': str(err), 'submission_status': 'uncertain', 'retry': False}); raise
    save(folder / 'JOB.json', result); print(json.dumps({'request_id': result['request_id']}))

def fetch(folder):
    folder = Path(folder); job = read(folder / 'JOB.json')
    st = api(job['status_url']); save(folder / 'STATUS.json', st)
    if st.get('status') != 'COMPLETED':
        print(json.dumps({'status': st.get('status'), 'queue_position': st.get('queue_position')})); return
    res = api(job['response_url']); save(folder / 'RESULT.json', res)
    data = get(res['video']['url']); target = folder / 'raw.mp4'
    if not target.exists(): target.write_bytes(data)
    assert sha(target.read_bytes()) == sha(data)
    if not any(e['item'] == folder.name and e['status'] in ('done', 'failed') for e in ledger_lines()):
        append({'item': folder.name, 'provider': 'fal', 'model': MODEL, 'est_credits': 0, 'est_usd': 0.896, 'actual_usd': 0.896, 'actual_credits': 0, 'actual_basis': 'listed $0.112/s x 8 s; account debit not returned by API', 'request_id': job['request_id'], 'status': 'done'})
    print(json.dumps({'status': 'COMPLETED', 'sha256': sha(data), 'bytes': len(data)}))

if __name__ == '__main__':
    op = sys.argv[1]
    if op == 'committed': print(committed())
    elif op == 'submit': submit(sys.argv[2], sys.argv[3])
    elif op == 'fetch': fetch(sys.argv[2])
    elif op == 'append': print(json.dumps(append(json.loads(sys.argv[2]))))
    else: raise ValueError(op)
