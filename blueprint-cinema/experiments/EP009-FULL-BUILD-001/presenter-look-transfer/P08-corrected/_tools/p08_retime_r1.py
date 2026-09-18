"""Only derived P08 retime-r1 processing; no generation, acceptance or bulk activation."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parents[1];G=D/'retime-r1';R=next(p for p in D.parents if (p/'.agents').is_dir())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
assert sha(G/'PLAN.json')=='1de5d83a8b73bdc9faffb120c697e024bd39999fd7b6e07a978beb206214be19'
s=importlib.util.spec_from_file_location('bounded_p08',D/'_tools/p08.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);r=m.r
plan=read(G/'PLAN.json');r.G=G;r.PLAN_PATH=G/'PLAN.json';r.PLAN=plan;r.PARTS={p['part_id']:p for p in plan['parts']}
oldledger=m.original_ledger
def ledger(row):
 assert row['item'] in {'P08r3a-fal-sync','P08r3b-fal-sync'}
 oldledger({**row,'item':'look-transfer-'+row['item'],'scope':plan['scope'],'picture_recovery_plan':{'path':r.rel(G/'PLAN.json'),'sha256':sha(G/'PLAN.json')}})
r.ledger=ledger

def main():
 command,pid=sys.argv[1:];assert pid in r.PARTS,'Only corrected P08 parts allowed'
 p=r.PARTS[pid];d=G/pid
 for key in ['picture_edit','derived_picture','restoration_wav']:
  b=p[key];assert sha(R/b['path'])==b['sha256'],key
 ed=read(d/'EDIT-DECISION.json');assert ed['fit']['max_local_rate']<=1.3 and ed['guide']['diagnostic_only'] is True
 assert sha(R/ed['source_native']['path'])==ed['source_native']['sha256']
 assert sha(d/'audio/narration.wav')==sha(D/pid/'audio/narration.wav')
 outputs={'native':'NATIVE-OFFSETS.json','align':'ALIGNMENT.json','gate':'SYNC-GATE.json','nose':'NOSE.json'}
 if command in outputs:assert not(d/outputs[command]).exists(),'Preserve prior measurements'
 if command=='check':print(json.dumps({'part':pid,'derived_inputs':'verified','max_rate':ed['fit']['max_local_rate']}));return
 if command=='fal-submit':
  r.native_gate(pid)
  assert read(d/'MOTION-REVIEW.json')['status']=='eligible_for_restoration_candidate'
  assert not list(D.glob(f'**/{pid}/fal/SUBMISSION-INTENT.json')),'Existing intent anywhere in scoped recovery: no retry'
  reserved=sum(read(q)['estimated_usd'] for q in D.glob('**/fal/SUBMISSION-INTENT.json'))
  estimate=round(read(d/'TRIM.json')['native_trim']['duration']*8/60,4)
  assert reserved+estimate<=3,'P08 total Fal cap exceeded'
 actions={'native':r.cmd_native,'trim':r.cmd_trim,'fal-submit':r.cmd_fal_submit,'fal-result':r.cmd_fal_result,'align':r.cmd_align,'gate':r.cmd_gate,'nose':r.cmd_nose}
 assert command in actions,'Not allowed by bounded recovery'
 actions[command](pid)
if __name__=='__main__':main()
