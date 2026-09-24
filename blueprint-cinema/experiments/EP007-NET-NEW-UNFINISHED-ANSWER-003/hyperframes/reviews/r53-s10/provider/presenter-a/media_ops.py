"""R53 presenter A authorized single-attempt restoration; no paid retries."""
from pathlib import Path
import importlib.util, json, hashlib, sys, datetime
P=Path(__file__).resolve().parent
R=next(x for x in P.parents if (x/'.agents').exists())
s=importlib.util.spec_from_file_location('transport',P.parents[2]/'r32-performance-refinement/provider/fal_ops.py')
t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
save=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n')
PLAN=R/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/direction/r53-s10-schedule/presenter-a/AVATAR-TAKE-PLAN.json'
CAP_USD=2.0
mode=sys.argv[1]
if mode=='upload-audio':
    a=P/'audio/fine-owner-says.wav'; assert sha(a)==read(PLAN)['audio']['sha256']
    url=t.upload(a,P/'audio','audio/wav'); print(json.dumps({'file_url':url,'sha256':sha(a)}))
elif mode=='restore-submit':
    out=P/'restoration';out.mkdir(exist_ok=True)
    assert not (out/'SUBMISSION-INTENT.json').exists(),'Existing attempt: do not duplicate'
    native=read(P/'NATIVE-MEDIA.json');assert sha(P/'native.mp4')==native['sha256']
    cost=native['duration_seconds']*8/60;assert cost<=CAP_USD
    audio=read(P/'audio/UPLOAD.json');assert audio['status']=='verified'
    assert hashlib.sha256(t.get(audio['file_url'])).hexdigest()==audio['sha256']
    payload={'video_url':native['url'],'audio_url':audio['file_url'],'sync_mode':'silence'}
    with (out/'SUBMISSION-INTENT.json').open('x') as f:
        json.dump({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model':'fal-ai/sync-lipsync/v3','payload':payload,'estimated_usd':cost,'cap_usd':CAP_USD,'owner_statement':'yes submit it','no_retry':True},f,indent=2)
    try: job=t.api('https://queue.fal.run/fal-ai/sync-lipsync/v3',payload)
    except Exception as e:
        save(out/'ERROR.json',{'submission_status':'uncertain','error':str(e),'retry':False});raise
    save(out/'JOB.json',job);print(json.dumps({'request_id':job['request_id'],'estimated_usd':cost}))
elif mode in ['restore-status','restore-result']:
    out=P/'restoration';job=read(out/'JOB.json')
    data=t.api(job['status_url'] if mode=='restore-status' else job['response_url'])
    save(out/('STATUS.json' if mode=='restore-status' else 'RESULT.json'),data)
    if mode=='restore-status':print(json.dumps({'status':data.get('status'),'queue_position':data.get('queue_position')}))
    else:
        raw=t.get(data['video']['url']);f=out/'restored.mp4'
        if f.exists():assert sha(f)==hashlib.sha256(raw).hexdigest()
        else:f.write_bytes(raw)
        print(json.dumps({'sha256':sha(f),'bytes':len(raw)}))
else:raise ValueError('Unknown mode')
