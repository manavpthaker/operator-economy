"""R76 one-pass source narration restoration; current authorization, no retries."""
from pathlib import Path
import datetime, hashlib, importlib.util, json, subprocess, sys
D=Path(__file__).resolve().parent
E=D.parents[1]
P=E/'hyperframes/reviews/r76-s17-presenter/provider'
R=next(p for p in D.parents if (p/'.agents').is_dir())
spec=importlib.util.spec_from_file_location('transport',E/'hyperframes/reviews/r32-performance-refinement/provider/fal_ops.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
def save(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
auth=read(D/'AUTHORIZATION.json')
assert auth['owner_statement']=='yea that works'
assert auth['caps']=={'higgsfield_credits':90,'fal_usd':1.6,'retries':0}
mode=sys.argv[1]
if mode=='audio-upload':
    audio=R/auth['audio_wav']['path']; assert sha(audio)==auth['audio_wav']['sha256']
    url=t.upload(audio,P/'audio','audio/wav')
    print(json.dumps({'url':url,'sha256':sha(audio)}))
elif mode=='submit':
    out=P/'restoration';out.mkdir(exist_ok=True)
    assert not (out/'SUBMISSION-INTENT.json').exists(), 'No retries'
    native=P/'native-trim.mp4'
    dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(native)]))
    estimate=dur*8/60
    assert estimate<=auth['caps']['fal_usd']
    video_url=t.upload(native,P,'video/mp4')
    audio=read(P/'audio/UPLOAD.json');assert audio['status']=='verified'
    assert audio['sha256']==sha(P/'audio/c.wav')==auth['audio_wav']['sha256']
    assert read(P/'UPLOAD.json')['sha256']==sha(native)
    payload={'video_url':video_url,'audio_url':audio['file_url'],'sync_mode':'silence'}
    with (out/'SUBMISSION-INTENT.json').open('x') as f:
        json.dump({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model':'fal-ai/sync-lipsync/v3','payload':payload,'native_sha256':sha(native),'native_seconds':dur,'estimated_usd':estimate,'authorization_sha256':sha(D/'AUTHORIZATION.json'),'no_retry':True},f,indent=2)
    try: job=t.api('https://queue.fal.run/fal-ai/sync-lipsync/v3',payload)
    except Exception as err:
        save(out/'ERROR.json',{'submission_status':'uncertain','error':str(err),'retry':False});raise
    save(out/'JOB.json',job);print(json.dumps({'request_id':job['request_id'],'estimated_usd':estimate}))
elif mode in {'status','result'}:
    out=P/'restoration';job=read(out/'JOB.json')
    data=t.api(job['status_url'] if mode=='status' else job['response_url'])
    save(out/('STATUS.json' if mode=='status' else 'RESULT.json'),data)
    if mode=='result':
        raw=t.get(data['video']['url']);path=out/'restored.mp4'
        if path.exists(): assert sha(path)==hashlib.sha256(raw).hexdigest()
        else: path.write_bytes(raw)
        print(json.dumps({'bytes':len(raw),'sha256':sha(path)}))
    else: print(json.dumps({'status':data.get('status')}))
