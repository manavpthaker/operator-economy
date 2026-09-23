"""Bounded R68 two-take operation. Never retry a paid submission."""
import datetime,hashlib,importlib.util,json,sys,urllib.parse,urllib.request
from pathlib import Path
BASE=Path(__file__).resolve().parent
REPO=next(p for p in BASE.parents if (p/'.agents').is_dir())
EXP=REPO/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
D=EXP/'direction/r68-s22-buyer-response'
helper=EXP/'hyperframes/reviews/r52-walkout/provider/fal_ops_v5.py'
spec=importlib.util.spec_from_file_location('prior_fal_ops',helper)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def upload(path,folder):
 raw=path.read_bytes();receipt=folder/'UPLOAD.json'
 if receipt.exists():
  r=read(receipt);assert r['status']=='verified' and r['sha256']==sha(raw);return r['file_url']
 ack=old.api('https://rest.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3',{'content_type':'image/png','file_name':'ep007-r68-'+sha(raw)[:16]+'.png'})
 assert urllib.parse.urlsplit(ack['upload_url']).scheme=='https'
 save(receipt,{'status':'uploading','sha256':sha(raw),'file_url':ack['file_url'],'at':now()})
 req=urllib.request.Request(ack['upload_url'],data=raw,method='PUT',headers={'Content-Type':'image/png'})
 with old.OPENER.open(req,timeout=55) as res:res.read()
 assert sha(old.get(ack['file_url']))==sha(raw)
 save(receipt,{'status':'verified','sha256':sha(raw),'file_url':ack['file_url'],'at':now()})
 return ack['file_url']
def main():
 name=sys.argv[1].upper();mode=sys.argv[2];assert name in ['A','B']
 auth=read(BASE/'GENERATION-AUTHORIZATION.json')
 assert auth['caps']=={'fal_total_usd':2.25,'requests':2,'automatic_retries':0}
 for k in ['bound_direction','bound_cost']:
  assert sha((REPO/auth[k]['path']).read_bytes())==auth[k]['sha256']
 reqpath=REPO/auth['bound_requests'][name]['path']
 assert sha(reqpath.read_bytes())==auth['bound_requests'][name]['sha256']
 req=read(reqpath);folder=BASE/('take-'+name.lower());folder.mkdir(exist_ok=True)
 if mode=='submit':
  assert not (folder/'SUBMISSION-INTENT.json').exists(),'Existing intent: no duplicate or retry.'
  assert req['model']=='fal-ai/kling-video/v3/pro/image-to-video'
  assert req['input']['duration']==('8' if name=='A' else '11') and req['input']['generate_audio'] is False
  if name=='A':path=REPO/req['local_start_image'];expected=req['start_image_sha256']
  else:
   gate=read(BASE/'take-a/REVIEW.json');assert gate['result']=='pass_for_dependent_take_b'
   assert gate['source_sha256']==sha((BASE/'take-a/native.mp4').read_bytes())
   seed=read(folder/'SEED.json');path=REPO/seed['path'];expected=seed['sha256']
   assert seed['source_sha256']==gate['source_sha256']
  assert sha(path.read_bytes())==expected
  spent=sum(read(p)['estimated_usd'] for p in BASE.glob('take-*/SUBMISSION-INTENT.json'))
  cost=int(req['input']['duration'])*.112
  assert len(list(BASE.glob('take-*/SUBMISSION-INTENT.json')))<2 and spent+cost<=2.25
  payload=dict(req['input']);payload['start_image_url']=upload(path,folder)
  save(folder/'REQUEST.json',{'model':req['model'],'input':payload,'bound_request_sha256':sha(reqpath.read_bytes())})
  with (folder/'SUBMISSION-INTENT.json').open('x') as f:
   json.dump({'at':now(),'model':req['model'],'payload':payload,'estimated_usd':cost,'authorization_sha256':sha((BASE/'GENERATION-AUTHORIZATION.json').read_bytes()),'no_retry':True},f,indent=2)
  try:result=old.api('https://queue.fal.run/'+req['model'],payload)
  except Exception as err:
   save(folder/'ERROR.json',{'at':now(),'error':str(err),'submission_status':'uncertain','retry':False});raise
  save(folder/'JOB.json',result);print(json.dumps({'take':name,'request_id':result['request_id'],'status':result.get('status'),'estimate_usd':cost}))
 elif mode in ['status','result']:
  job=read(folder/'JOB.json');result=old.api(job['status_url'] if mode=='status' else job['response_url'])
  save(folder/('STATUS.json' if mode=='status' else 'RESULT.json'),result)
  if mode=='result':
   data=old.get(result['video']['url']);target=folder/'native.mp4'
   if target.exists():assert sha(target.read_bytes())==sha(data)
   else:target.write_bytes(data)
   print(json.dumps({'take':name,'sha256':sha(data),'bytes':len(data)}))
  else:print(json.dumps({'take':name,'status':result.get('status'),'queue_position':result.get('queue_position')}))
 else:raise ValueError('Unknown operation')
if __name__=='__main__':main()

