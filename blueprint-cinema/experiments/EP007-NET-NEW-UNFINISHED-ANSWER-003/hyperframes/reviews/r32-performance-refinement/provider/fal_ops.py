"""R32 bounded Fal operations. Every paid intent is exclusive; never retry submission."""
import datetime, hashlib, json, re, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = next(p for p in BASE.parents if (p / '.agents').is_dir())
PREP = BASE.parent / 'provider-preparation'
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
    ack = api('https://rest.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3', {'content_type':mime,'file_name':'ep007-r32-'+sha(raw)[:16]+path.suffix})
    assert urllib.parse.urlsplit(ack['upload_url']).scheme == 'https'
    save(receipt, {'status':'uploading','sha256':sha(raw),'file_url':ack['file_url'],'at':now()})
    req = urllib.request.Request(ack['upload_url'], data=raw, method='PUT', headers={'Content-Type':mime})
    with OPENER.open(req, timeout=55) as res: res.read()
    assert sha(get(ack['file_url'])) == sha(raw)
    save(receipt, {'status':'verified','sha256':sha(raw),'file_url':ack['file_url'],'at':now()})
    return ack['file_url']
def submit(folder, model, payload, estimated_usd):
    assert not (folder/'JOB.json').exists()
    with (folder/'SUBMISSION-INTENT.json').open('x') as f:
        json.dump({'at':now(),'model':model,'payload':payload,'estimated_usd':estimated_usd,'authorization_sha256':sha((BASE/'GENERATION-AUTHORIZATION.json').read_bytes()),'no_retry':True},f,indent=2)
    try: result = api('https://queue.fal.run/'+model,payload)
    except Exception as err:
        save(folder/'ERROR.json', {'at':now(),'error':str(err),'submission_status':'uncertain','retry':False}); raise
    save(folder/'JOB.json',result)
    print(json.dumps({'take':folder.name,'request_id':result['request_id'],'status':result.get('status')}),flush=True)
def main():
    auth=read(BASE/'GENERATION-AUTHORIZATION.json'); assert auth['caps']=={'higgsfield_credits':252,'fal_total_usd':6}
    mode=sys.argv[1]
    if mode=='buyer-submit':
        p=read(PREP/'buyer-reaction.request.json'); folder=BASE/'buyer-reaction'; folder.mkdir(exist_ok=True)
        assert not (folder/'SUBMISSION-INTENT.json').exists(), 'Existing intent; never duplicate'
        path=REPO/p['local_start_image']; assert sha(path.read_bytes())==p['start_image_sha256']
        assert p['input']['duration']=='6' and p['input']['generate_audio'] is False
        payload=dict(p['input']);payload['start_image_url']=upload(path,folder,'image/png')
        save(folder/'REQUEST.json',{'model':p['model'],'input':payload})
        submit(folder,p['model'],payload,0.672)
    elif mode=='restore-submit':
        rows=read(BASE/'RESTORATION-BATCH.json')
        assert 1 <= len(rows) <= 2 and len({x['take'] for x in rows}) == len(rows)
        assert {x['take'] for x in rows} <= {'post-title-lens-contact','question-pensive'}
        assert sum(x['native_duration_seconds'] for x in rows)*8/60+0.672<=6
        for row in rows:
            folder=BASE/row['take']; assert sha((folder/'native.mp4').read_bytes())==row['native_video_sha256']
            if (folder/'SUBMISSION-INTENT.json').exists():
                print(json.dumps({'take':row['take'],'status':'existing_restoration_intent_not_resubmitted'})); continue
            assert sha(get(row['audio_url']))==row['audio_sha256']
            payload={'video_url':row['video_url'],'audio_url':row['audio_url'],'sync_mode':'silence'}
            submit(folder,'fal-ai/sync-lipsync/v3',payload,row['native_duration_seconds']*8/60)
    elif mode in {'status','result'}:
        name=sys.argv[2]; assert name in {'buyer-reaction','post-title-lens-contact','question-pensive'}
        folder=BASE/name; job=read(folder/'JOB.json'); result=api(job['status_url'] if mode=='status' else job['response_url'])
        save(folder/('STATUS.json' if mode=='status' else 'RESULT.json'),result)
        if mode=='result':
            url=result['video']['url']; data=get(url); target=folder/('native.mp4' if name=='buyer-reaction' else 'restored.mp4')
            if target.exists(): assert sha(target.read_bytes())==sha(data)
            else: target.write_bytes(data)
            print(json.dumps({'take':name,'sha256':sha(data),'bytes':len(data)}))
        else: print(json.dumps({'take':name,'status':result.get('status'),'queue_position':result.get('queue_position')}))
    else: raise ValueError('Unknown operation')
if __name__=='__main__':main()
