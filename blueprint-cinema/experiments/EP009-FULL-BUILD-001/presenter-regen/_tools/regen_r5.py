"""EP009 r5 adapter: fixed r3 narration coordinates; no implicit activation.
Use the existing syncenv Python. `check` is offline and does not require activation.
All operational commands require ACTIVE-PLAN to bind this exact immutable plan.
Old plans, pilot executions, inputs and final/ outputs remain preserved.
"""
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import wave

sys.dont_write_bytecode = True
G = Path(__file__).resolve().parents[1]
R = next(p for p in G.parents if (p / '.agents').is_dir())
B = G.parent
PLAN_PATH = G / 'EXECUTION-PLAN-r5.json'
FINAL = G / 'final-r5'
RETIRED = {'P01', 'P08a', 'P08b', 'P08c'}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
rj = lambda p: json.loads(Path(p).read_text())
rel = lambda p: str(Path(p).resolve().relative_to(R))

def bound(b):
    if not isinstance(b, dict) or not b.get('path') or not b.get('sha256'):
        raise RuntimeError('Missing bound path/hash')
    p = (R / b['path']).resolve()
    if not p.is_relative_to(R) or not p.is_file() or sha(p) != b['sha256']:
        raise RuntimeError('Missing or stale artifact: ' + str(p))
    return p

def binding(p):
    return {'path': rel(p), 'sha256': sha(p)}

def write_new(p, obj):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, indent=2) + '\n'
    if p.exists():
        if p.read_text() != text:
            raise RuntimeError('Preserve existing artifact: ' + str(p))
        return
    with p.open('x') as f:
        f.write(text)

def wav_bytes(p):
    with wave.open(str(p)) as w:
        if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (48000, 1, 2):
            raise RuntimeError('Expected mono PCM16 48kHz: ' + str(p))
        return w.readframes(w.getnframes())

PLAN = rj(PLAN_PATH)
MASTER = bound(PLAN['master'])
MASTER_PCM = wav_bytes(MASTER)
PARTS = {p['part_id']: p for p in PLAN['parts']}
if len(PARTS) != 22 or set(PARTS) & RETIRED:
    raise RuntimeError('Incorrect r5 part inventory')
for key in ('timemap', 'revision', 'owner_scoped_lock', 'owner_opening', 'base_plan', 'previous_plan', 'base_helper'):
    bound(PLAN[key])
if bound(PLAN['adapter']) != Path(__file__).resolve():
    raise RuntimeError('Plan does not bind this adapter')

spec = importlib.util.spec_from_file_location('ep009_regen_r5_base', bound(PLAN['base_helper']))
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.MASTER, base.MASTER_SHA = MASTER, PLAN['master']['sha256']
base.WT = bound(PLAN['word_transcript'])
base.PLAN_PATH, base.PLAN = PLAN_PATH, PLAN
base.PARTS, base.ORDER = PARTS, list(PARTS)
base.SEGS = {s['id']: s for s in PLAN['segments']}
base.CROP_PLAN = {k: [(x[0] / 24, x[1]) for x in v] for k, v in PLAN['crop_frames'].items()}
base.seg_frames = lambda s: s['output_frames'][1] - s['output_frames'][0]
_original_resolve = base.resolve_execution


def check_part(pid):
    if pid not in PARTS or pid in RETIRED:
        raise RuntimeError('Unknown or retired r5 part: ' + pid)
    p = PARTS[pid]
    for key in ('restoration_wav', 'guidance_mp3', 'prompt_binding', 'audio_record'):
        bound(p[key])
    audio = wav_bytes(bound(p['restoration_wav']))
    s0, s1 = p['master_samples']
    if audio != MASTER_PCM[s0 * 2:s1 * 2] or len(audio) != p['samples'] * 2:
        raise RuntimeError(pid + ': narration no longer matches exact r3 samples')
    if sha(bound(p['restoration_wav'])) != p['restoration_wav']['sha256']:
        raise RuntimeError(pid + ': changed WAV')
    if not 0 < p['generation_seconds'] <= 12:
        raise RuntimeError(pid + ': generation exceeds 12 seconds')
    if p.get('reusable_upload'):
        upload = rj(bound(p['reusable_upload']))
        if not upload_matches_audio(upload, p, audio):
            raise RuntimeError(pid + ': uploaded guidance lacks matching PCM provenance')
    return p


def upload_matches_audio(upload, p, audio):
    if upload.get('put_http') not in (200, '200') or not upload.get('uploaded_mp3_hash_verified_after_confirmation'):
        return False
    pcm_match = upload.get('source_pcm_identity', {}).get('sha256') == hashlib.sha256(audio).hexdigest()
    exact_local_encoding = upload.get('source_wav_sha256') == p['restoration_wav']['sha256'] and upload.get('sha256') == p['guidance_mp3']['sha256']
    return pcm_match or exact_local_encoding


def require_active():
    selected = rj(G / 'ACTIVE-PLAN.json')
    if bound(selected) != PLAN_PATH or selected.get('base_plan_sha256') != PLAN['base_plan']['sha256']:
        raise RuntimeError('r5 is prepared but not activated; root must bind ACTIVE-PLAN')
    if selected.get('revision_hold', {}).get('invalidated_parts'):
        if set(selected['revision_hold']['invalidated_parts']) & set(PARTS):
            raise RuntimeError('Active revision hold invalidates an r5 part')
    clearance = rj(bound(selected.get('bulk_clearance')))
    if clearance.get('status') != 'cleared' or clearance.get('selected_plan') != binding(PLAN_PATH) or not clearance.get('pilot_review_evidence'):
        raise RuntimeError('Bulk processing requires explicit current pilot-review clearance')
    for evidence in clearance['pilot_review_evidence']:
        bound(evidence)


def resolve_execution(pid):
    p = check_part(pid)
    ex_path = G / pid / 'EXECUTION.json'
    prior = p.get('prior_execution')
    selected_path = PLAN_PATH
    if prior:
        if bound(prior['execution']) != ex_path:
            raise RuntimeError(pid + ': prior execution binding changed')
        selected_path = bound(prior['selected_plan'])
    elif p.get('prior_generation'):
        selected_path = bound(p['prior_generation']['selected_plan'])
    old_path = base.PLAN_PATH
    try:
        base.PLAN_PATH = selected_path
        ex, paths, job, upload = _original_resolve(pid)
    finally:
        base.PLAN_PATH = old_path
    if paths['prompt'] != bound(p['prompt_binding']):
        raise RuntimeError(pid + ': execution prompt differs from selected r5 input')
    if p.get('prior_generation'):
        generation = p['prior_generation']
        if ex['job_id'] != generation['job_id'] or paths['higgsfield_job'] != bound(generation['job']):
            raise RuntimeError(pid + ': standalone job differs from the explicitly retained generation')
    gen = ex['generation']
    for key in ('generation_seconds', 'resolution', 'est_credits'):
        if gen.get(key) != p[key]:
            raise RuntimeError(pid + ': execution generation parameters differ: ' + key)
    if not prior:
        expected = PLAN['provider']
        for k in ('model', 'mode', 'aspect_ratio', 'generate_audio'):
            if gen.get(k) != expected[k]:
                raise RuntimeError(pid + ': execution provider differs: ' + k)
        refs = {(m['role'], m['value']) for m in gen.get('medias', []) if m['role'] != 'audio'}
        if refs != {('image', PLAN['look']['image_reference']), ('video', PLAN['behavior_references'][0])}:
            raise RuntimeError(pid + ': execution references differ from r5 role lock')
        if not upload_matches_audio(upload, p, wav_bytes(bound(p['restoration_wav']))):
            raise RuntimeError(pid + ': upload must bind exact restoration PCM provenance')
    return ex, paths, job, upload

base.resolve_execution = resolve_execution


def selected_native_offsets():
    """Optional P00-only evidence selection; never rewrite the failed measurement."""
    path = G / 'P00/NATIVE-OFFSETS-SELECTION.json'
    if not path.exists():
        return None
    selection = rj(path)
    if selection.get('record_type') != 'presenter_native_offset_selection' or selection.get('part_id') != 'P00' or selection.get('status') != 'selected_for_processing':
        raise RuntimeError('Invalid P00 native-offset selection')
    original = bound(selection.get('original_offsets'))
    chosen = bound(selection.get('selected_offsets'))
    if original != G / 'P00/NATIVE-OFFSETS.json' or chosen == original or chosen.parent != G / 'P00' or not chosen.name.startswith('NATIVE-OFFSETS-'):
        raise RuntimeError('Selected offsets must be a separate version beside preserved original')
    audit_path = bound(selection.get('independent_lexical_audit'))
    audit = rj(audit_path)
    if audit.get('status') != 'verified' or audit.get('part_id') != 'P00' or audit.get('word_sequence_verified') is not True or audit.get('wrong_phrase_alias_excluded') is not True:
        raise RuntimeError('Independent lexical audit has not resolved phrase identity')
    if sha(bound(audit.get('native'))) != sha(G / 'P00/native.mp4') or sha(bound(audit.get('narration'))) != PARTS['P00']['restoration_wav']['sha256']:
        raise RuntimeError('Lexical audit binds different media')
    domain = selection.get('lag_domain_seconds')
    if not isinstance(domain, list) or len(domain) != 2 or not all(isinstance(x, (float, int)) and math.isfinite(x) for x in domain) or domain[0] >= domain[1] or audit.get('lag_domain_seconds') != domain:
        raise RuntimeError('Missing independently established lag domain')
    evidence = audit.get('independent_method_evidence', [])
    if len(evidence) < 2 or len({str(bound(x)) for x in evidence}) < 2:
        raise RuntimeError('Two distinct independent method evidence bindings required')
    record = rj(chosen)
    if record.get('method') != 'lexically-anchored-envelope-windows' or record.get('independent_lexical_audit') != selection['independent_lexical_audit'] or record.get('original_offsets') != selection['original_offsets']:
        raise RuntimeError('Selected measurement lacks original/lexical provenance')
    offsets = [w['native_minus_narration_s'] for w in record.get('windows', [])]
    if len(offsets) != 3 or any(not domain[0] <= x <= domain[1] for x in offsets):
        raise RuntimeError('Selected offsets escape the verified phrase lag domain')
    # base.native_gate still validates all three windows, media hashes and <=0.30s spread.
    return {'selection': binding(path), 'selected_offsets': binding(chosen), 'independent_lexical_audit': binding(audit_path)}


def cmd_check():
    for pid in PARTS:
        check_part(pid)
    if len(MASTER_PCM) // 2 != PLAN['master_samples']:
        raise RuntimeError('Changed r3 master length')
    if sum(p['est_credits'] for p in PARTS.values() if p['new_generation_required']) != PLAN['budget']['remaining_generation_credits']:
        raise RuntimeError('Wrong generation reserve')
    print(json.dumps({'status': 'offline_inputs_verified', 'parts': len(PARTS), 'new_generation_parts': sum(p['new_generation_required'] for p in PARTS.values()), 'master': PLAN['master'], 'projected_credits': PLAN['budget']['projected_total_credits'], 'active': rj(G / 'ACTIVE-PLAN.json').get('sha256') == sha(PLAN_PATH)}))


def cmd_take(pid):
    check_part(pid)
    # Reuse complete provenance serialization; intercept only the output path.
    original_write = base.wj
    def save(path, record):
        if Path(path) != G / pid / 'TAKE.json':
            raise RuntimeError('Unexpected base take output')
        record.update({'record_type': 'presenter_r5_part_take', 'selected_plan': binding(PLAN_PATH), 'master_source': PLAN['master'], 'master_frames': PARTS[pid]['master_frames'], 'master_samples': PARTS[pid]['master_samples'], 'prior_execution': PARTS[pid].get('prior_execution'), 'coordinate_note': 'Top-level ranges use r3; preserved source AUDIO and prior execution records retain their original provenance.'})
        if pid == 'P00':
            record['native_offset_selection'] = selected_native_offsets()
        write_new(G / pid / 'TAKE-r5.json', record)
    try:
        base.wj = save
        base.cmd_take(pid)
    finally:
        base.wj = original_write


def part_review(pid):
    try:
        check_part(pid)
        take = rj(G / pid / 'TAKE-r5.json')
        if bound(take['selected_plan']) != PLAN_PATH or take['master_source'] != PLAN['master'] or take['master_frames'] != PARTS[pid]['master_frames']:
            raise RuntimeError('Stale r5 take coordinates')
        if pid == 'P00' and take.get('native_offset_selection') != selected_native_offsets():
            raise RuntimeError('Stale P00 native offset selection')
        old_read = base.rj
        def read(path):
            p = Path(path)
            return rj(G / pid / 'TAKE-r5.json' if p == G / pid / 'TAKE.json' else p)
        try:
            base.rj = read
            state = base.part_review_state(pid)
        finally:
            base.rj = old_read
        if state['complete']:
            state['take'] = binding(G / pid / 'TAKE-r5.json')
        return state
    except (OSError, ValueError, KeyError, RuntimeError) as e:
        return {'complete': False, 'reason': str(e)}


def conform_spec(sid):
    if sid == 'opening-P00':
        return PLAN['opening']['output_frames'], [[0, 'W']], ['P00']
    if sid not in PLAN['crop_frames']:
        raise RuntimeError('Not a full presenter segment; use conform-opening for P00')
    s = base.SEGS[sid]
    return s['output_frames'], PLAN['crop_frames'][sid], [p['part_id'] for p in PARTS.values() if sid in p['segment_ids']]


def cmd_conform(sid):
    (lo, hi), crops, pids = conform_spec(sid)
    reviews = {pid: part_review(pid) for pid in pids}
    if not all(x['complete'] for x in reviews.values()):
        raise RuntimeError('Incomplete technical review: ' + json.dumps(reviews))
    pieces = []
    for f in range(lo, hi):
        matching = [p for p in PARTS.values() if p['part_id'] in pids and p['master_frames'][0] <= f < p['master_frames'][1]]
        if len(matching) != 1:
            raise RuntimeError('Ambiguous or missing r5 coverage at frame ' + str(f))
        p = matching[0]; size = [sz for start, sz in crops if start <= f][-1]
        if pieces and pieces[-1]['part'] == p['part_id'] and pieces[-1]['size'] == size:
            pieces[-1]['end'] = f + 1
        else:
            pieces.append({'part': p['part_id'], 'size': size, 'start': f, 'end': f + 1})
    FINAL.mkdir(exist_ok=True)
    out = FINAL / (sid + '.mp4')
    if out.exists() or (FINAL / (sid + '-CONFORM.json')).exists():
        raise RuntimeError('Existing r5 conform preserved; verify it or use a new revision')
    inputs, chains, labels, records = [], [], [], []
    for i, piece in enumerate(pieces):
        pid = piece['part']; p = PARTS[pid]; al = rj(G / pid / 'ALIGNMENT.json')
        if bound(al['restored']) != G / pid / 'restored.mp4':
            raise RuntimeError('Alignment source changed')
        a = al['start_frame'] + piece['start'] - p['master_frames'][0]
        z = a + piece['end'] - piece['start']; total = int(al['probe']['nb_read_frames'])
        if a < 0 or z > total:
            raise RuntimeError(pid + ': insufficient restored coverage; no cloned or retimed picture')
        rect = base.rect_for(pid, piece['size'])
        inputs += ['-i', str(G / pid / 'restored.mp4')]
        chains.append(f'[{i}:v]trim=start_frame={a}:end_frame={z},setpts=N/(24*TB),{base.crop_filter(rect)},setsar=1,format=yuv420p[v{i}]')
        labels.append(f'[v{i}]')
        records.append({**piece, 'source_frames': [a, z], 'rect': rect, 'restored': binding(G / pid / 'restored.mp4'), 'alignment': binding(G / pid / 'ALIGNMENT.json'), 'take': binding(G / pid / 'TAKE-r5.json')})
    n = len(pieces); samples = (hi - lo) * 2000
    chains.append(''.join(labels) + (f'concat=n={n}:v=1:a=0[vo]' if n > 1 else 'null[vo]'))
    chains.append(f'[{n}:a]atrim=start_sample={lo*2000}:end_sample={min(hi*2000, PLAN["master_samples"])},asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0,apad=whole_len={samples},atrim=end_sample={samples}[ao]')
    command = ['ffmpeg', '-n', '-v', 'error', *inputs, '-i', str(MASTER), '-filter_complex', ';'.join(chains), '-map', '[vo]', '-map', '[ao]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-r', '24', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', str(out)]
    record = {'record_type': 'presenter_r5_conform', 'selected_plan': binding(PLAN_PATH), 'master': PLAN['master'], 'output_frames': [lo, hi], 'frames': hi-lo, 'pieces': records, 'part_reviews': reviews, 'owner_accepted': False, 'command': command}
    write_new(FINAL / (sid + '-CONFORM-INTENT.json'), record)
    base.run(command)
    record['output'] = binding(out)
    write_new(FINAL / (sid + '-CONFORM.json'), record)
    print(json.dumps({'output': record['output'], 'frames': hi-lo}))


def cmd_verify(sid):
    (lo, hi), _, _ = conform_spec(sid)
    out = FINAL / (sid + '.mp4'); conform = rj(FINAL / (sid + '-CONFORM.json'))
    if bound(conform['output']) != out or bound(conform['selected_plan']) != PLAN_PATH or conform['master'] != PLAN['master']:
        raise RuntimeError('Stale conform')
    streams = json.loads(base.run(['ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=codec_type,width,height,r_frame_rate,nb_read_frames,channels,sample_rate', '-of', 'json', str(out)]))['streams']
    v = next(s for s in streams if s['codec_type']=='video'); a = next(s for s in streams if s['codec_type']=='audio')
    n = (hi-lo)*2000; np = base.np
    ref = np.frombuffer(MASTER_PCM[lo*4000:min(hi*4000,len(MASTER_PCM))], dtype='<i2').astype(float)/32768
    ref = np.pad(ref,(0,n-len(ref))); audio = base.pcm(out,2)
    errors=[]
    if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames'])) != (1280,720,'24/1',hi-lo): errors.append('picture_format_or_frames')
    if (a['sample_rate'],a['channels']) != ('48000',2): errors.append('audio_format')
    if not n <= len(audio) <= n+2048: errors.append('audio_length')
    correlations=[]; gains=[]
    for start in range(0,n,48000):
        x=ref[start:min(start+96000,n)]; stop=start+len(x)
        if len(x)<2400 or stop>len(audio) or np.sqrt(np.mean(x*x))<1e-4: continue
        for ch in (0,1):
            y=audio[start:stop,ch]; correlations.append(float(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)+1e-12)));gains.append(float(20*np.log10((np.linalg.norm(y)+1e-12)/(np.linalg.norm(x)+1e-12))))
    if not correlations or min(correlations)<.995: errors.append('master_audio_correlation')
    if not gains or max(abs(x) for x in gains)>.25: errors.append('master_audio_gain')
    stats=base.run(['ffmpeg','-v','error','-i',str(out),'-vf','signalstats,metadata=print:file=-','-f','null','-'])
    ymax=[float(x.split('=')[1]) for x in stats.splitlines() if 'signalstats.YMAX=' in x];ymin=[float(x.split('=')[1]) for x in stats.splitlines() if 'signalstats.YMIN=' in x]
    uniform=sum(hi_y-lo_y<8 for hi_y,lo_y in zip(ymax,ymin))
    if len(ymax)!=hi-lo or uniform: errors.append('uniform_or_missing_frames')
    surplus=audio[n:];surplus_peak=float(np.max(np.abs(surplus))) if len(surplus) else 0
    if surplus_peak>.0032: errors.append('non_silent_aac_padding')
    record={'status':'pass' if not errors else 'fail','errors':errors,'path':rel(out),'sha256':sha(out),'selected_plan':binding(PLAN_PATH),'master':PLAN['master'],'output_frames':[lo,hi],'frames':int(v['nb_read_frames']),'frames_ok':int(v['nb_read_frames'])==hi-lo,'program_samples':n,'decoded_samples':len(audio),'minimum_voiced_window_correlation':min(correlations) if correlations else None,'maximum_absolute_gain_db':max(abs(x) for x in gains) if gains else None,'uniform_frames':uniform,'aac_surplus_peak':surplus_peak,'owner_accepted':False,'conform':binding(FINAL/(sid+'-CONFORM.json'))}
    write_new(FINAL/(sid+'-VERIFY.json'),record)
    print(json.dumps(record))
    if errors: raise RuntimeError('r5 encoded verification failed')


def index_entry(sid):
    frames,_,pids=conform_spec(sid);reviews={pid:part_review(pid) for pid in pids};flags=[p for p,v in reviews.items() if v.get('flagged')]
    out=FINAL/(sid+'.mp4');vf=FINAL/(sid+'-VERIFY.json')
    entry={'status':'pending','output_frames':frames,'frames':frames[1]-frames[0],'parts_used':pids,'part_reviews':reviews,'flagged_parts':flags,'technical_complete':False,'owner_accepted':False}
    if out.exists() and vf.exists():
        v=rj(vf);fresh=v.get('sha256')==sha(out) and v.get('selected_plan')==binding(PLAN_PATH) and v.get('master')==PLAN['master']
        complete=fresh and v.get('status')=='pass' and all(x['complete'] for x in reviews.values())
        entry.update({'path':rel(out),'sha256':sha(out),'verification':binding(vf),'technical_complete':complete,'status':('review-ready-flagged' if flags else 'review-ready') if complete else 'pending-review'})
    return entry


def cmd_index():
    FINAL.mkdir(exist_ok=True)
    index={'record_type':'presenter_r5_index','plan':binding(PLAN_PATH),'master':PLAN['master'],'look':PLAN['look'],'owner_accepted':False,'segments':{sid:index_entry(sid) for sid in PLAN['crop_frames']},'opening_insert':index_entry('opening-P00')}
    path=FINAL/'INDEX.json';tmp=FINAL/'.INDEX.json.tmp'
    with tmp.open('w') as f: json.dump(index,f,indent=2);f.write('\n')
    tmp.replace(path)
    print(json.dumps({**{k:v['status'] for k,v in index['segments'].items()},'opening-P00':index['opening_insert']['status']}))


def _dispatch(command,args):
    if command=='check': return cmd_check()
    if command=='totals': return base.cmd_totals()
    if command=='index': return cmd_index()
    standalone_commands = {'native','trim','fal-submit','fal-result','align','gate','nose','download','take'}
    standalone = (command in standalone_commands and args and args[0]=='P00') or command in ('conform-opening','verify-opening')
    if standalone:
        p=check_part('P00'); generation=p.get('prior_generation',{})
        bound(generation.get('selected_plan')); bound(generation.get('job')); bound(PLAN['owner_opening'])
        if generation.get('processing_scope') != 'P00-only-through-opening-review':
            raise RuntimeError('Standalone P00 processing scope missing')
    else:
        require_active()
    if command=='conform-opening': return cmd_conform('opening-P00')
    if command=='verify-opening': return cmd_verify('opening-P00')
    if command=='conform': return cmd_conform(*args)
    if command=='verify': return cmd_verify(*args)
    if not args: raise RuntimeError('Part ID required')
    pid=args[0];check_part(pid)
    if command=='take': return cmd_take(pid)
    if command=='fal-submit': resolve_execution(pid)
    functions={'native':base.cmd_native,'trim':base.cmd_trim,'fal-submit':base.cmd_fal_submit,'fal-result':base.cmd_fal_result,'align':base.cmd_align,'gate':base.cmd_gate,'nose':base.cmd_nose,'download':base.cmd_download}
    if command not in functions: raise RuntimeError('Unsupported r5 command')
    outputs={'native':'NATIVE-OFFSETS.json','trim':'TRIM.json','align':'ALIGNMENT.json','gate':'SYNC-GATE.json','nose':'NOSE.json'}
    if command in outputs and (G/pid/outputs[command]).exists(): raise RuntimeError('Preserve existing diagnostic; use bound result or prepare a new revision')
    return functions[command](*args)


def dispatch(command, args):
    selected = selected_native_offsets() if command not in ('check', 'totals', 'native', 'download') else None
    if not selected:
        return _dispatch(command, args)
    original_path = G / 'P00/NATIVE-OFFSETS.json'
    selected_path = bound(selected['selected_offsets'])
    old_read, old_sha, old_write = base.rj, base.sha, base.wj
    def offset_path(path):
        return selected_path if Path(path).resolve() == original_path else path
    def write(path, record):
        if Path(path).parent == G / 'P00' and Path(path).name in ('TRIM.json', 'SYNC-GATE.json'):
            record = {**record, 'native_offset_selection': selected}
        old_write(path, record)
    try:
        base.rj = lambda path: old_read(offset_path(path))
        base.sha = lambda path: old_sha(offset_path(path))
        base.wj = write
        base.native_gate('P00')
        return _dispatch(command, args)
    finally:
        base.rj, base.sha, base.wj = old_read, old_sha, old_write

if __name__=='__main__':
    if len(sys.argv)<2:
        raise SystemExit('Usage: regen_r5.py check|totals|native|trim|fal-submit|fal-result|align|gate|nose|download|take|conform|verify|conform-opening|verify-opening|index [part/segment]')
    dispatch(sys.argv[1],sys.argv[2:])
