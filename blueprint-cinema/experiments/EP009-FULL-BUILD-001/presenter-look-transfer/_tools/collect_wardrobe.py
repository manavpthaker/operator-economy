"""Collect completed, known wardrobe jobs only. Never submits or retries generation."""
import concurrent.futures, datetime, hashlib, json, subprocess, sys, urllib.request
from pathlib import Path

T = Path(__file__).resolve().parents[1]
B = T.parent
LEDGER = B / 'ledger/presenter-regen.jsonl'
def read(p): return json.loads(p.read_text())
def save(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def collect(row):
    matches=[p for p in (T/'wardrobe').glob('*/JOB.json') if read(p).get('job_id')==row['job_id']]
    if len(matches)!=1: raise RuntimeError('Unknown or duplicate job')
    p=matches[0].parent;j=read(matches[0]);target=p/'native.mp4'
    if row['status']!='completed': return
    if not row['result_url'].startswith('https://d8j0ntlcm91z4.cloudfront.net/'): raise RuntimeError('Unexpected output host')
    save(p/'RESULT.json',row)
    if not target.exists():
        with urllib.request.urlopen(row['result_url'],timeout=55) as r: data=r.read()
        with target.open('xb') as f:f.write(data)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames,duration','-of','json',str(target)]))
    receipt={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'segment':p.name,'job_id':row['job_id'],'sha256':sha(target),'bytes':target.stat().st_size,'probe':probe,'status':'downloaded_not_reviewed'}
    save(p/'DOWNLOAD.json',receipt)
    return receipt,j

rows=read(Path(sys.argv[1])); rows=rows['jobs'] if isinstance(rows,dict) else rows
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for result in pool.map(collect,rows):
        if result is None: continue
        receipt,j=result;item='look-transfer-'+receipt['segment']+'-wardrobe-r1'
        existing=[readline for readline in (json.loads(line) for line in LEDGER.read_text().splitlines()) if readline.get('item')==item and readline.get('status')=='done']
        if not existing:
            e={'at':receipt['at'],'lane':'presenter-regen','item':item,'provider':'higgsfield','model':'kling_video_edit','actual_credits':j['est_credits'],'actual_usd':0,'status':'done','request_id':j['job_id'],'reason':'Completed wardrobe-stage output downloaded and probed; not performance/room approved. Cost from live preflight.'}
            with LEDGER.open('a') as f:f.write(json.dumps(e)+'\n')
        print(json.dumps(receipt),flush=True)
