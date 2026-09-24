"""Download known completed appearance edits and record cost once. No generation."""
import concurrent.futures,datetime,hashlib,json,subprocess,sys,urllib.request
from pathlib import Path
T=Path(__file__).resolve().parents[1];LEDGER=T.parent/'ledger/presenter-regen.jsonl'
stage,resultfile=sys.argv[1:3]
assert stage in ('wardrobe-guarded-r2','room-r1','room-r2')
def read(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def collect(r):
 matches=[p for p in (T/stage).glob('*/JOB.json') if read(p).get('job_id')==r['job_id']]
 assert len(matches)==1,'Unknown or duplicate job'
 d=matches[0].parent;j=read(matches[0]);p=d/'native.mp4'
 if r['status']!='completed':return
 assert r['result_url'].startswith('https://d8j0ntlcm91z4.cloudfront.net/')
 if (d/'DOWNLOAD.json').exists():
  rec=read(d/'DOWNLOAD.json');assert p.exists() and rec['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
  return rec,j
 save(d/'RESULT.json',r)
 if not p.exists():
  with urllib.request.urlopen(r['result_url'],timeout=60) as f:data=f.read()
  with p.open('xb') as f:f.write(data)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames,duration','-of','json',str(p)]))
 rec={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'segment':d.name,'job_id':j['job_id'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'probe':probe,'status':'downloaded_not_reviewed'}
 save(d/'DOWNLOAD.json',rec);return rec,j
rows=read(Path(resultfile));rows=rows['jobs'] if isinstance(rows,dict) else rows
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for x in pool.map(collect,rows):
  if x is None:continue
  rec,j=x;item='look-transfer-'+rec['segment']+'-'+stage
  previous=[json.loads(s) for s in LEDGER.read_text().splitlines()]
  if not any(e.get('item')==item and e.get('status')=='done' for e in previous):
   with LEDGER.open('a') as f:f.write(json.dumps({'at':rec['at'],'lane':'presenter-regen','item':item,'provider':'higgsfield','model':'kling_video_edit','actual_credits':j['est_credits'],'actual_usd':0,'status':'done','request_id':j['job_id'],'reason':'Known completed appearance output downloaded and probed; performance acceptance remains separate.'})+'\n')
  print(json.dumps(rec),flush=True)
