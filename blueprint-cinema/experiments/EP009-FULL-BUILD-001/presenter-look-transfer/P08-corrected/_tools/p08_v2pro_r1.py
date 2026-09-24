"""One authorized A-only Sync 2 Pro repair; immutable receipts, no automatic retries."""
import datetime, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
D = Path(__file__).resolve().parents[1]
R = next(p for p in D.parents if (p / '.agents').is_dir())
G = D / 'repair-v2pro-r1'; A = G / 'P08r3a'; F = A / 'fal'
MODEL = 'fal-ai/sync-lipsync/v2/pro'
ITEM = 'look-transfer-P08r3a-fal-v2pro-repair-r1'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
read = lambda p: json.loads(Path(p).read_text())
bind = lambda p: {'path': str(Path(p).relative_to(R)), 'sha256': sha(p)}
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p, d):
    with p.open('x') as f: json.dump(d, f, indent=2); f.write('\n')
spec = importlib.util.spec_from_file_location('regen', D.parents[1] / 'presenter-regen/_tools/regen.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
r.G = G
plan = read(G / 'PLAN.json')
assert plan['part_id'] == 'P08r3a' and plan['model'] == MODEL
assert plan['frames'] == 173 and plan['narration_samples'] == 346000
assert plan['max_call_usd'] == 1 and plan['shared_fal_cap_usd'] == 30
for v in plan['bindings'].values(): assert sha(R / v['path']) == v['sha256'], v['path']
assert sha(A/'audio/narration.wav') == plan['bindings']['locked_audio']['sha256']
assert sha(A/'native-trim.mp4') == plan['bindings']['retimed_native']['sha256']
gate = read(R / plan['bindings']['native_drift_measurement']['path'])
assert gate['native']['sha256'] == plan['bindings']['retimed_native']['sha256']
assert gate['narration']['sha256'] == plan['bindings']['locked_audio']['sha256']
assert not gate['drifted'] and gate['spread_s'] <= .30
assert max(w['native_minus_narration_s'] for w in gate['windows']) - min(w['native_minus_narration_s'] for w in gate['windows']) <= .30

def submit():
    assert not (F/'SUBMISSION-INTENT.json').exists(), 'Existing intent: never resubmit'
    tr = r.transport(); cost = plan['estimated_usd']
    assert cost <= 1 and r.ledger_totals()[1] + cost <= 30
    for name in ('video', 'audio'): (F/name).mkdir(parents=True, exist_ok=True)
    vu = tr.upload(A/'input-picture.mp4', F/'video', 'video/mp4')
    au = tr.upload(A/'audio/narration.wav', F/'audio', 'audio/wav')
    payload = {'video_url':vu, 'audio_url':au, 'sync_mode':'cut_off'}
    assert r.ledger_totals()[1] + cost <= 30
    intent = {'at':now(), 'model':MODEL, 'payload':payload, 'plan':bind(G/'PLAN.json'),
              'authority':plan['bindings']['authority'], 'visible_defect':plan['visible_defect'],
              'estimated_usd':cost, 'max_call_usd':1, 'shared_fal_cap_usd':30,
              'rate':'$5 per minute', 'rate_source':plan['rate_source'], 'no_retry':True}
    write(F/'SUBMISSION-INTENT.json', intent)
    r.ledger({'item':ITEM, 'provider':'fal', 'model':MODEL, 'status':'intent', 'est_credits':0,
              'est_usd':cost, 'reason':'One A-only visual-lipsync repair of documented internal-pause anticipation',
              'plan':bind(G/'PLAN.json'), 'intent':bind(F/'SUBMISSION-INTENT.json')})
    try: job = tr.api('https://queue.fal.run/'+MODEL, payload)
    except Exception as err:
        write(F/'ERROR.json', {'at':now(), 'error':str(err), 'submission_status':'uncertain', 'retry':False})
        raise
    write(F/'JOB.json', job)
    print(json.dumps({'part':'P08r3a', 'request_id':job['request_id'], 'estimated_usd':cost}), flush=True)

def result():
    tr = r.transport(); job = read(F/'JOB.json'); st = tr.api(job['status_url'])
    if st.get('status') != 'COMPLETED':
        print(json.dumps({'request_id':job['request_id'], 'status':st.get('status')})); return
    res = tr.api(job['response_url']); raw = tr.get(res['video']['url'])
    out = A/'restored.mp4'
    if out.exists(): assert sha(out) == hashlib.sha256(raw).hexdigest()
    else:
        with out.open('xb') as f: f.write(raw)
    if not (F/'RESULT.json').exists(): write(F/'RESULT.json', res)
    if not (F/'TERMINAL.json').exists(): write(F/'TERMINAL.json', {'at':now(), 'status':st, 'result':bind(F/'RESULT.json'), 'output':bind(out)})
    r.ledger({'item':ITEM, 'provider':'fal', 'model':MODEL, 'status':'done', 'actual_credits':0,
              'actual_usd':plan['estimated_usd'], 'request_id':job['request_id'],
              'reason':'Completed; cost calculated at posted $5/min, not provider invoice', 'plan':bind(G/'PLAN.json')})
    print(json.dumps({'request_id':job['request_id'], 'status':'COMPLETED', 'output':bind(out)}))

if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'submit': submit()
    elif command == 'result': result()
    elif command in ('align','gate','nose'):
        name = {'align':'ALIGNMENT.json', 'gate':'SYNC-GATE.json', 'nose':'NOSE.json'}[command]
        assert not (A/name).exists(), 'Preserve previous diagnostic'
        getattr(r, 'cmd_'+command)('P08r3a')
    elif command == 'check': print(json.dumps({'inputs':'verified', 'scope':'A only', 'estimated_usd':plan['estimated_usd'], 'shared_fal_accounting_usd':r.ledger_totals()[1]}))
    else: raise ValueError('Operation not allowed')
