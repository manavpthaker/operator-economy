"""Bounded P08 processing only; does not activate or process any other presenter."""
import hashlib, importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
D = Path(__file__).resolve().parents[1]
B = D.parents[1]
R = next(p for p in D.parents if (p/'.agents').is_dir())
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
read = lambda p: json.loads(Path(p).read_text())
PLAN = D/'PLAN.json'
assert sha(PLAN) == '84f5d71bad33d17b08fe9b10b6747108954b40c74160be429d47406e989fd75d'
plan = read(PLAN)
for binding in [plan['scope'], plan['master'], plan['source_preparation']]:
    assert sha(R/binding['path']) == binding['sha256']
base = B/'presenter-regen/_tools/regen.py'
assert sha(base) == 'd358d9d1342c9e4ef50f353bdd406768c4e78c628ef37f8a8457223edb4f02e8'
spec = importlib.util.spec_from_file_location('ep009_p08_base', base)
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
r.G = D
r.PLAN_PATH = PLAN
r.PLAN = plan
r.PARTS = {p['part_id']:p for p in plan['parts']}
r.MASTER = R/plan['master']['path']
r.MASTER_SHA = plan['master']['sha256']
r.WT = B/'assembly/r3/word-transcript-r3.json'
assert set(r.PARTS) == {'P08r3a','P08r3b'}
original_ledger = r.ledger
def scoped_ledger(entry):
    assert entry['item'] in {'P08r3a-fal-sync','P08r3b-fal-sync'}
    original_ledger({**entry, 'item':'look-transfer-'+entry['item'],
                     'scope':plan['scope'], 'processing_plan':{'path':r.rel(PLAN),'sha256':sha(PLAN)}})
r.ledger = scoped_ledger

def main():
    command, pid = sys.argv[1:]
    assert pid in r.PARTS, 'Only the two scoped P08 parts are permitted'
    p=r.PARTS[pid]; d=D/pid
    for key in ('restoration_wav','guidance_mp3','audio_record','prompt_binding','reusable_upload'):
        binding=p[key]; assert sha(R/binding['path']) == binding['sha256']
    if command == 'check':
        print(json.dumps({'part':pid,'status':'scope_and_inputs_verified','old_bulk_active':False})); return
    terminal=read(d/'TERMINAL.json')
    assert terminal['status']=='completed' and terminal['native']['sha256']==sha(d/'native.mp4')
    assert terminal['job_id']==read(d/'HIGGSFIELD-JOB.json')['job_id']
    outputs={'native':'NATIVE-OFFSETS.json','align':'ALIGNMENT.json','gate':'SYNC-GATE.json','nose':'NOSE.json'}
    if command in outputs:
        assert not (d/outputs[command]).exists(), 'Preserve existing measurement'
    if command=='fal-submit':
        assert not (d/'fal/SUBMISSION-INTENT.json').exists(), 'Existing intent: never resubmit'
        r.native_gate(pid)
        trim=read(d/'TRIM.json'); projected=round(trim['native_trim']['duration']*8/60,4)
        reserved=0
        for other in r.PARTS:
            intent=D/other/'fal/SUBMISSION-INTENT.json'
            if intent.exists():reserved+=read(intent)['estimated_usd']
        assert reserved+projected<=3, 'Scoped Fal allowance exceeded'
        (d/'fal').mkdir(exist_ok=True)
        r.wj(d/'fal/SCOPED-PREFLIGHT.json',{'plan':{'path':r.rel(PLAN),'sha256':sha(PLAN)},'scope':plan['scope'],
              'native_trim_sha256':sha(d/'native-trim.mp4'),'duration_seconds':trim['native_trim']['duration'],
              'quoted_rate_usd_per_minute':8,'estimated_usd':projected,'other_reserved_usd':reserved,
              'cap_usd':3,'basis':'Existing EP009 Sync v3 production quote; duration measured from bound local trim.',
              'no_retry':True})
    actions={'native':r.cmd_native,'trim':r.cmd_trim,'fal-submit':r.cmd_fal_submit,
             'fal-result':r.cmd_fal_result,'align':r.cmd_align,'gate':r.cmd_gate,'nose':r.cmd_nose}
    if command=='sheet':
        assert not (d/'stills/contact-native-2fps.jpg').exists()
        r.cmd_sheet(pid); return
    assert command in actions, 'Command outside bounded workflow'
    actions[command](pid)

if __name__=='__main__':main()
