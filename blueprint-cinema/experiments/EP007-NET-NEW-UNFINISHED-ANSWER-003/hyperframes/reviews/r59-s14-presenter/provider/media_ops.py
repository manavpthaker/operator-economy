"""R59 S14 presenter restorations: one Fal Sync v3 call per take on the trimmed native; no retries."""
from pathlib import Path
import importlib.util, json, hashlib, sys, datetime, subprocess
P=Path(__file__).resolve().parent
R=next(x for x in P.parents if (x/'.agents').exists())
s=importlib.util.spec_from_file_location('transport',P.parents[1]/'r32-performance-refinement/provider/fal_ops.py')
t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text()); save=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n')
AUTH=read(P/'GENERATION-AUTHORIZATION.json'); CAP_TOTAL=AUTH['caps']['fal_usd']
TRIM={'a':16,'c1':5,'c3':12}
mode,take=sys.argv[1],sys.argv[2]; T=P/take; out=T/'restoration'
if mode=='upload':
    v=T/'native-trim.mp4'; vu=t.upload(v,T,'video/mp4')
    a=R/AUTH['takes'][take.upper()]['audio_wav']['path']; (T/'audio').mkdir(exist_ok=True)
    au=t.upload(a,T/'audio','audio/wav'); print(json.dumps({'video':vu,'audio':au}))
elif mode=='submit':
    out.mkdir(exist_ok=True); assert not (out/'SUBMISSION-INTENT.json').exists(),'no retry'
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(T/'native-trim.mp4')],capture_output=True,text=True).stdout)
    cost=dur*8/60
    spent=sum(read(p)['estimated_usd'] for p in P.glob('*/restoration/SUBMISSION-INTENT.json'))
    assert spent+cost<=CAP_TOTAL,(spent,cost)
    vid=read(T/'UPLOAD.json'); aud=read(T/'audio/UPLOAD.json')
    assert vid['status']=='verified' and aud['status']=='verified'
    payload={'video_url':vid['file_url'],'audio_url':aud['file_url'],'sync_mode':'silence'}
    with (out/'SUBMISSION-INTENT.json').open('x') as f:
        json.dump({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model':'fal-ai/sync-lipsync/v3','payload':payload,'trim_frames':TRIM[take],'native_trim_seconds':dur,'estimated_usd':cost,'cap_total_usd':CAP_TOTAL,'owner_statement':AUTH['owner_statement'],'no_retry':True},f,indent=2)
    try: job=t.api('https://queue.fal.run/fal-ai/sync-lipsync/v3',payload)
    except Exception as e: save(out/'ERROR.json',{'submission_status':'uncertain','error':str(e),'retry':False});raise
    save(out/'JOB.json',job);print(json.dumps({'take':take,'request_id':job['request_id'],'estimated_usd':round(cost,3)}))
elif mode in ['status','result']:
    job=read(out/'JOB.json'); data=t.api(job['status_url'] if mode=='status' else job['response_url'])
    save(out/('STATUS.json' if mode=='status' else 'RESULT.json'),data)
    if mode=='status': print(json.dumps({'take':take,'status':data.get('status')}))
    else:
        raw=t.get(data['video']['url']); f=out/'restored.mp4'
        if f.exists(): assert sha(f)==hashlib.sha256(raw).hexdigest()
        else: f.write_bytes(raw)
        print(json.dumps({'take':take,'sha256':sha(f),'bytes':len(raw)}))
