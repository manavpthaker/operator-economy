"""One authorized React-1 submission; status reads never resubmit."""
from pathlib import Path
import datetime, hashlib, json, re, sys, urllib.error, urllib.parse, urllib.request, wave

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[6]
sha=lambda b:hashlib.sha256(b).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(name):return json.loads((ROOT/name).read_text())
def save(name,data):(ROOT/name).write_text(json.dumps(data,indent=2)+'\n')
P=read('PROPOSED-REQUEST.json');A=read('GENERATION-AUTHORIZATION.json')
assert A['status']=='authorized' and A['maximum_submissions']==1 and A['automatic_retries']==0
assert A['model']==P['model']=='fal-ai/sync-lipsync/react-1'
assert sha((ROOT/'PROPOSED-REQUEST.json').read_bytes())==A['proposal_sha256']
assert A['expected_usd']==P['proposed_limits']['nominal_estimated_usd']<=A['estimated_usd_ceiling']==3
for kind in ('video','audio'):
    f=P['input_files'][kind];assert sha((ROOT/f['local_path']).read_bytes())==f['sha256']
with wave.open(str(ROOT/P['input_files']['audio']['local_path']),'rb') as w:
    assert (w.getframerate(),w.getnframes(),w.getnchannels(),w.getsampwidth())==(48000,578000,1,2)
assert A['parameters']=={'emotion':'neutral','model_mode':'lips','lipsync_mode':'cut_off','temperature':0.5}

def credential():
    for line in (REPO/'.env').read_text().splitlines():
        m=re.match(r'^\s*(?:export\s+)?FAL_KEY\s*=\s*(.*?)\s*$',line)
        if m:
            value=m.group(1)
            if len(value)>1 and value[0] in '\"\'' and value[-1]==value[0]:value=value[1:-1]
            else:value=value.split(' #',1)[0].strip()
            if value:return value
    raise RuntimeError('FAL_KEY unavailable; no submission made')
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=urllib.request.build_opener(NoRedirect())
def api(url,payload=None):
    u=urllib.parse.urlsplit(url)
    assert u.scheme=='https' and u.hostname in ('queue.fal.run','rest.fal.ai','api.fal.ai')
    request=urllib.request.Request(url,data=None if payload is None else json.dumps(payload).encode(),headers={'Authorization':'Key '+credential(),'Content-Type':'application/json','X-Fal-No-Retry':'1','x-app-fal-disable-fallback':'1'})
    with OPENER.open(request,timeout=45) as response:return json.load(response)
def public_get(url):
    assert urllib.parse.urlsplit(url).scheme=='https'
    with OPENER.open(url,timeout=60) as response:return response.read()

mode=sys.argv[1]
if mode=='verify':
    credential()
    print(json.dumps({'inputs_and_authorization_verified':True,'credential_available':True,'expected_usd':A['expected_usd'],'ceiling_usd':3,'submission_attempt_exists':(ROOT/'SUBMISSION-ATTEMPT.json').exists()}))
elif mode=='upload':
    manifest=read('UPLOADS.json') if (ROOT/'UPLOADS.json').exists() else {}
    for kind,mime,ext in [('video','video/mp4','.mp4'),('audio','audio/wav','.wav')]:
        f=P['input_files'][kind]
        if kind in manifest:
            assert manifest[kind]['status']=='verified' and manifest[kind]['sha256']==f['sha256']
            continue
        raw=(ROOT/f['local_path']).read_bytes()
        manifest[kind]={'status':'initiating','sha256':sha(raw),'bytes':len(raw),'at':now()};save('UPLOADS.json',manifest)
        ack=api('https://rest.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3',{'content_type':mime,'file_name':'ep007-r28-'+kind+'-'+sha(raw)[:12]+ext})
        assert urllib.parse.urlsplit(ack['upload_url']).scheme=='https' and urllib.parse.urlsplit(ack['file_url']).scheme=='https'
        manifest[kind].update(status='uploading',file_url=ack['file_url']);save('UPLOADS.json',manifest)
        req=urllib.request.Request(ack['upload_url'],data=raw,method='PUT',headers={'Content-Type':mime})
        with OPENER.open(req,timeout=60) as response:response.read()
        assert sha(public_get(ack['file_url']))==sha(raw)
        manifest[kind].update(status='verified',verified_at=now());save('UPLOADS.json',manifest)
        print(json.dumps({'input':kind,'status':'verified','sha256':sha(raw)}),flush=True)
elif mode=='submit':
    uploads=read('UPLOADS.json');payload=dict(A['parameters'])
    for kind in ('video','audio'):
        assert uploads[kind]['status']=='verified' and uploads[kind]['sha256']==P['input_files'][kind]['sha256']
        payload[kind+'_url']=uploads[kind]['file_url']
    with (ROOT/'SUBMISSION-ATTEMPT.json').open('x') as f:
        json.dump({'started_at':now(),'model':A['model'],'submission_number':1,'automatic_retries':0,'proposal_sha256':A['proposal_sha256'],'authorization_sha256':sha((ROOT/'GENERATION-AUTHORIZATION.json').read_bytes()),'payload':payload,'payload_sha256':sha(json.dumps(payload).encode()),'estimated_usd':A['expected_usd'],'may_retry':False},f,indent=2)
    try:job=api('https://queue.fal.run/'+A['model'],payload)
    except Exception as error:
        detail=error.read().decode(errors='replace') if isinstance(error,urllib.error.HTTPError) else str(error)
        save('ERROR.json',{'at':now(),'outcome':'failed_or_uncertain','http_status':getattr(error,'code',None),'detail':detail.replace(credential(),'[REDACTED]'),'may_retry':False})
        raise SystemExit('Submission failed or uncertain; receipt saved; no retry permitted.')
    save('JOB.json',job);print(json.dumps({'request_id':job['request_id'],'status':job.get('status'),'estimated_usd':A['expected_usd']}))
elif mode in ('status','result'):
    job=read('JOB.json');url=job['status_url' if mode=='status' else 'response_url']
    if mode=='status':url+='?logs=1'
    result=api(url);save(mode.upper()+'.json',result)
    if mode=='status':print(json.dumps({'request_id':job['request_id'],'status':result.get('status'),'queue_position':result.get('queue_position'),'metrics':result.get('metrics')}))
    else:print(json.dumps({'request_id':job['request_id'],'result_received':True,'video_present':bool(result.get('video',{}).get('url'))}))
elif mode=='download':
    result=read('RESULT.json');raw=public_get(result['video']['url']);dest=ROOT/'presenter-generated-raw.mp4'
    with dest.open('xb') as f:f.write(raw)
    receipt={'request_id':read('JOB.json')['request_id'],'at':now(),'path':dest.name,'sha256':sha(raw),'bytes':len(raw),'source_url':result['video']['url']};save('DOWNLOAD.json',receipt)
    print(json.dumps({k:v for k,v in receipt.items() if k!='source_url'}))
else:raise SystemExit('Use verify, upload, submit, status, result or download')
