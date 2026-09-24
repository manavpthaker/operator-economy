"""Record known preflight intents or returned jobs; does not call providers."""
import datetime,json,sys
from pathlib import Path
T=Path(__file__).resolve().parents[1];LEDGER=T.parent/'ledger/presenter-regen.jsonl'
def save(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 assert not p.exists(),p
 p.write_text(json.dumps(d,indent=2)+'\n')
mode,stage,batch=sys.argv[1:4];rows=json.loads(Path(batch).read_text())
if mode=='intent':
 for r in rows:
  d=T/stage/r['segment'];item='look-transfer-'+r['segment']+'-'+stage
  e={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lane':'presenter-regen','item':item,'provider':'higgsfield','model':r['params']['model'],'est_credits':r['estimate']['cost']['credits'],'est_usd':0,'status':'intent','reason':r.get('reason','Bounded exact-performance appearance edit under owner scope and existing1800creditcap; each output requires QA.')}
  save(d/'REQUEST.json',r);save(d/'SUBMISSION-INTENT.json',e)
  with LEDGER.open('a') as f:f.write(json.dumps(e)+'\n')
  print(item,e['est_credits'])
elif mode=='jobs':
 assert all(r.get('job_id') and r.get('status')!='submission_failed' for r in rows),'No submitted job IDs; record provider rejection separately'
 for r in rows:
  d=T/stage/r['segment'];req=json.loads((d/'REQUEST.json').read_text());r['est_credits']=req['estimate']['cost']['credits'];r['model']=req['params']['model'];r['source']=req['params']['medias'][0]['value']
  save(d/'JOB.json',r)
  with LEDGER.open('a') as f:f.write(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lane':'presenter-regen','item':'look-transfer-'+r['segment']+'-'+stage,'provider':'higgsfield','model':r['model'],'est_credits':r['est_credits'],'est_usd':0,'status':'submitted','request_id':r['job_id']})+'\n')
  print(r['segment'],r['job_id'])
else:raise ValueError(mode)
