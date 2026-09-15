"""One authorized Sync v3 run on the trimmed native take; never retry."""
from pathlib import Path
import importlib.util, json, hashlib, sys, datetime
R=Path(__file__).resolve().parent; P=R.parent
s=importlib.util.spec_from_file_location('t',P.parents[2]/'r32-performance-refinement/provider/fal_ops.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest(); read=lambda p:json.loads(p.read_text()); save=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n')
auth=read(R/'GENERATION-AUTHORIZATION.json'); vid=R/'native-shift15.mp4'; assert sha(vid)==auth['input_video']['sha256']
mode=sys.argv[1]
if mode=='submit':
    assert not (R/'SUBMISSION-INTENT.json').exists(),'Existing intent; never duplicate'
    vurl=t.upload(vid,R,'video/mp4')
    audio=read(P/'audio/UPLOAD.json'); assert audio['status']=='verified'
    dur=float(__import__('subprocess').check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(vid)]))
    cost=dur*8/60; assert cost<=auth['caps']['fal_usd']
    payload={'video_url':vurl,'audio_url':audio['file_url'],'sync_mode':'silence'}
    with (R/'SUBMISSION-INTENT.json').open('x') as f: json.dump({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'payload':payload,'estimated_usd':cost,'no_retry':True},f,indent=2)
    try: job=t.api('https://queue.fal.run/fal-ai/sync-lipsync/v3',payload)
    except Exception as e: save(R/'ERROR.json',{'error':str(e),'submission_status':'uncertain','retry':False}); raise
    save(R/'JOB.json',job); print(json.dumps({'request_id':job['request_id'],'estimated_usd':cost}))
elif mode in ('status','result'):
    job=read(R/'JOB.json'); data=t.api(job['status_url'] if mode=='status' else job['response_url']); save(R/('STATUS.json' if mode=='status' else 'RESULT.json'),data)
    if mode=='status': print(json.dumps({'status':data.get('status')}))
    else:
        raw=t.get(data['video']['url']); f=R/'restored.mp4'
        if f.exists(): assert sha(f)==hashlib.sha256(raw).hexdigest()
        else: f.write_bytes(raw)
        print(json.dumps({'sha256':sha(f),'bytes':len(raw)}))
