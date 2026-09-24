"""R52 bounded Fal operation: one v5 handshake take. Every paid intent is exclusive; never retry submission."""
import datetime, hashlib, json, re, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = next(p for p in BASE.parents if (p / '.agents').is_dir())
DIRECTION = REPO / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/direction/r52-walkout'
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
read = lambda p: json.loads(p.read_text())
def save(p, d): p.write_text(json.dumps(d, indent=2) + '\n')
def key():
    for line in (REPO / '.env').read_text().splitlines():
        m = re.match(r'^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$', line)
        if m: return m.group(1).strip().strip('"').strip("'")
    raise RuntimeError('Fal credential unavailable')
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs): return None
OPENER = urllib.request.build_opener(NoRedirect())
def api(url, body=None):
    u = urllib.parse.urlsplit(url)
    assert u.scheme == 'https' and u.hostname in {'queue.fal.run', 'rest.fal.ai'}
    req = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(), headers={'Authorization':'Key '+key(), 'Content-Type':'application/json', 'X-Fal-No-Retry':'1', 'x-app-fal-disable-fallback':'1'})
    try:
        with OPENER.open(req, timeout=45) as res: return json.load(res)
    except urllib.error.HTTPError as err:
        raise RuntimeError('Fal HTTP '+str(err.code)+': '+err.read(8000).decode(errors='replace').replace(key(), '[REDACTED]')) from None
def get(url):
    assert urllib.parse.urlsplit(url).scheme == 'https'
    with OPENER.open(url, timeout=55) as res: return res.read()
def upload(path, folder, mime):
    raw = path.read_bytes(); receipt = folder / 'UPLOAD.json'
    if receipt.exists():
        d = read(receipt); assert d['status'] == 'verified' and d['sha256'] == sha(raw); return d['file_url']
    ack = api('https://rest.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3', {'content_type':mime,'file_name':'ep007-r52-'+sha(raw)[:16]+path.suffix})
    assert urllib.parse.urlsplit(ack['upload_url']).scheme == 'https'
    save(receipt, {'status':'uploading','sha256':sha(raw),'file_url':ack['file_url'],'at':now()})
    req = urllib.request.Request(ack['upload_url'], data=raw, method='PUT', headers={'Content-Type':mime})
    with OPENER.open(req, timeout=55) as res: res.read()
    assert sha(get(ack['file_url'])) == sha(raw)
    save(receipt, {'status':'verified','sha256':sha(raw),'file_url':ack['file_url'],'at':now()})
    return ack['file_url']
def main():
    auth = read(BASE/'GENERATION-AUTHORIZATION-v5.json')
    assert auth['caps'] == {'fal_total_usd':1.0,'requests':1,'automatic_retries':0}
    reqpath = DIRECTION/'HANDSHAKE.request.json'
    assert sha(reqpath.read_bytes()) == auth['bound_request']['sha256'], 'Request changed since authorization'
    folder = BASE/'handshake-v5'; mode = sys.argv[1]
    if mode == 'submit':
        assert not (folder/'SUBMISSION-INTENT.json').exists(), 'Existing intent; never duplicate'
        p = read(reqpath); path = REPO/p['local_start_image']; assert sha(path.read_bytes()) == p['start_image_sha256']
        assert p['input']['duration'] == '8' and p['input']['generate_audio'] is False and 8*0.112 <= auth['caps']['fal_total_usd']
        payload = dict(p['input']); payload['start_image_url'] = upload(path, folder, 'image/png')
        save(folder/'REQUEST.json', {'model':p['model'],'input':payload})
        with (folder/'SUBMISSION-INTENT.json').open('x') as f:
            json.dump({'at':now(),'model':p['model'],'payload':payload,'estimated_usd':0.896,'authorization_sha256':sha((BASE/'GENERATION-AUTHORIZATION-v5.json').read_bytes()),'no_retry':True}, f, indent=2)
        try: result = api('https://queue.fal.run/'+p['model'], payload)
        except Exception as err:
            save(folder/'ERROR.json', {'at':now(),'error':str(err),'submission_status':'uncertain','retry':False}); raise
        save(folder/'JOB.json', result); print(json.dumps({'request_id':result['request_id'],'status':result.get('status')}))
    elif mode in {'status','result'}:
        job = read(folder/'JOB.json'); result = api(job['status_url'] if mode == 'status' else job['response_url'])
        save(folder/('STATUS.json' if mode == 'status' else 'RESULT.json'), result)
        if mode == 'result':
            data = get(result['video']['url']); target = folder/'native.mp4'
            if target.exists(): assert sha(target.read_bytes()) == sha(data)
            else: target.write_bytes(data)
            print(json.dumps({'sha256':sha(data),'bytes':len(data)}))
        else: print(json.dumps({'status':result.get('status'),'queue_position':result.get('queue_position')}))
    else: raise ValueError('Unknown operation')
if __name__ == '__main__': main()
