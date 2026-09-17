"""EP009 presenter regeneration: per-part audio cut, native offsets, trim, Fal Sync v3, alignment,
sync gate, multi-part conform, verify, TAKE.json and INDEX.json. Adapted from presenter/_tools/pres.py.
Paid calls write a ledger intent first and never resubmit an existing intent.
Run with the syncenv python (numpy, cv2, mediapipe 0.10.14)."""
import datetime, fcntl, hashlib, importlib.util, json, math, os, subprocess, sys, tempfile
from pathlib import Path
import numpy as np

sys.dont_write_bytecode = True
G = Path(__file__).resolve().parents[1]           # presenter-regen/
B = G.parent
R = next(x for x in G.parents if (x / '.agents').is_dir())
EP7 = R / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews'
MASTER = R / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'
MASTER_SHA = 'e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944'
WT = R / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/word-transcript.json'
SHOT = json.loads((B / 'direction/SHOT-PLAN.json').read_text())
SEGS = {s['id']: s for s in SHOT['segments']}
BASE_PLAN_PATH = G / 'TAKE-PLAN.json'
PLAN_PATH = BASE_PLAN_PATH
if (G / 'ACTIVE-PLAN.json').exists():
    selected = json.loads((G / 'ACTIVE-PLAN.json').read_text())
    PLAN_PATH = (R / selected['path']).resolve()
    if not PLAN_PATH.is_relative_to(G) or hashlib.sha256(PLAN_PATH.read_bytes()).hexdigest() != selected['sha256']:
        raise RuntimeError('Active presenter plan missing, outside lane, or stale')
    if hashlib.sha256(BASE_PLAN_PATH.read_bytes()).hexdigest() != selected['base_plan_sha256']:
        raise RuntimeError('Active presenter plan binds a stale base plan')
PLAN = json.loads(PLAN_PATH.read_text())
PARTS = {p['part_id']: p for p in PLAN['parts']}
ORDER = [p['part_id'] for p in PLAN['parts']]
LEDGER = B / 'ledger/presenter-regen.jsonl'
CREDIT_CAP, FAL_CAP = 1800.0, 30.0            # lane allocation (includes the 50 credits of look stills)
SR = 48000
CROP_PLAN = {  # segment -> list of (master_seconds_from, size)
    'seg009': [(50.291667, 'W')], 'seg012': [(73.541667, 'C'), (79.666667, 'W')], 'seg019': [(188.666667, 'M'), (194.75, 'C')],
    'seg021': [(226.208333, 'W')], 'seg028': [(368.0, 'M')], 'seg035': [(469.291667, 'C')], 'seg037': [(520.416667, 'W'), (523.708333, 'M')],
    'seg044': [(666.583333, 'W'), (676.041667, 'C'), (681.041667, 'M')], 'seg055': [(879.166667, 'W')], 'seg059': [(976.541667, 'M')],
    'seg071': [(1175.041667, 'C'), (1186.166667, 'W')], 'seg072': [(1196.458333, 'M')], 'seg073': [(1204.416667, 'W')],
    'seg074': [(1213.875, 'M'), (1223.833333, 'W')], 'seg075': [(1225.875, 'M')]}
SIZE_SCALE = {'W': 1.0, 'M': 1.25, 'C': 1.5}
for sid, rows in PLAN.get('crop_overrides', {}).items():
    if sid not in CROP_PLAN:
        raise RuntimeError('Unknown presenter segment in crop override')
    CROP_PLAN[sid] = [(row[0], row[1]) for row in rows]

now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
rj = lambda p: json.loads(Path(p).read_text())
rel = lambda p: str(Path(p).resolve().relative_to(R))
def wj(p, d): Path(p).write_text(json.dumps(d, indent=2) + '\n')
def run(cmd): return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
def fr(t): return int(round(t * 24))
def seg_frames(s): return (29607 if s['master_out'] == 1233.602 else fr(s['master_out'])) - fr(s['master_in'])
def pd(pid): return G / pid

def transport():
    s = importlib.util.spec_from_file_location('fal_ops', EP7 / 'r32-performance-refinement/provider/fal_ops.py')
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def ledger(entry):
    entry = {'at': now(), 'lane': 'presenter-regen', **entry}
    with LEDGER.open('a+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        rows = [json.loads(l) for l in f if l.strip()]
        if entry['status'] == 'done':
            done = [r for r in rows if r['item'] == entry['item'] and r['status'] == 'done']
            if done:
                previous = done[-1]
                for key in ('request_id', 'actual_credits', 'actual_usd'):
                    if previous.get(key) != entry.get(key):
                        raise RuntimeError(f"conflicting completion for {entry['item']}: {key}")
                return
        f.write(json.dumps(entry) + '\n')
        f.flush()

def ledger_totals():
    rows = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]
    # An uncertain submission may later be reconciled as completed. Charge its
    # latest state once, rather than adding both the estimate and completion.
    latest = {r['item']: r for r in rows}
    cr = usd = 0.0
    for r in latest.values():
        if r['status'] in ('done', 'failed'):
            cr += r.get('actual_credits') or 0; usd += r.get('actual_usd') or 0
        elif r['status'] == 'intent':
            cr += r.get('est_credits') or 0; usd += r.get('est_usd') or 0
    return cr, usd

def publish_media(tmp, out):
    """Install a complete file without replacing any existing provider artifact."""
    tmp, out = Path(tmp), Path(out)
    try:
        os.link(tmp, out)
    except FileExistsError:
        if sha(tmp) != sha(out):
            raise RuntimeError(f'existing media differs; preserve it and use a new path: {out}')

def media_temp(out):
    return tempfile.NamedTemporaryFile(prefix='.' + out.stem + '-', suffix=out.suffix, dir=out.parent)

def native_gate(pid):
    d = pd(pid); no = rj(d / 'NATIVE-OFFSETS.json')
    if no['native']['sha256'] != sha(d / 'native.mp4'):
        raise RuntimeError(f'{pid}: native offsets are stale for this video')
    if no.get('narration', {}).get('sha256') != sha(d / 'audio/narration.wav'):
        raise RuntimeError(f'{pid}: native offsets are stale or unbound for this narration')
    wins = no.get('windows', [])
    if len(wins) != 3 or any(not math.isfinite(w['envelope_corr']) or w['envelope_corr'] <= -1 for w in wins):
        raise RuntimeError(f'{pid}: native offsets do not have three valid measurement windows')
    offsets = [w['native_minus_narration_s'] for w in wins]
    if any(not math.isfinite(v) for v in offsets) or not math.isfinite(no['median_offset_s']):
        raise RuntimeError(f'{pid}: non-finite native timing measurement')
    if no.get('drifted') is not False or not math.isfinite(no['spread_s']) or no['spread_s'] > 0.30 or max(offsets) - min(offsets) > 0.300001:
        raise RuntimeError(f'{pid}: native timing drift exceeds 0.30 s; no paid Sync submission')
    return no

def pcm(path, ch=1):
    cmd = ['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', 'pipe:1']
    a = np.frombuffer(subprocess.run(cmd, check=True, capture_output=True).stdout, dtype='<f4').astype(np.float64)
    return a.reshape(-1, ch) if ch > 1 else a

def master_excerpt(t0, t1):
    s0, s1 = int(round(t0 * SR)), int(round(t1 * SR))
    cmd = ['ffmpeg', '-v', 'error', '-i', str(MASTER), '-af', f'atrim=start_sample={s0}:end_sample={s1}', '-ac', '1', '-f', 'f32le', 'pipe:1']
    return np.frombuffer(subprocess.run(cmd, check=True, capture_output=True).stdout, dtype='<f4').astype(np.float64)

def env(x, hop=480):
    n = len(x) // hop
    return np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)

def ncorr(x, y):
    x = x - x.mean(); y = y - y.mean()
    return float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-12))

# ---------- steps ----------
def cmd_cut(pid):
    assert sha(MASTER) == MASTER_SHA
    p = PARTS[pid]; d = pd(pid) / 'audio'; d.mkdir(parents=True, exist_ok=True)
    wav, mp3 = d / 'narration.wav', d / 'narration.mp3'
    s0, s1 = int(round(p['master_in'] * SR)), int(round(p['master_out'] * SR))
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(MASTER), '-af', f'atrim=start_sample={s0}:end_sample={s1},asetpts=N/SR/TB', '-ac', '1', str(wav)])
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(wav), '-c:a', 'libmp3lame', '-b:a', '320k', str(mp3)])
    n = len(pcm(wav)); assert n == s1 - s0 == p['samples'], (n, s1 - s0)
    wj(d / 'AUDIO.json', {'master_range': [p['master_in'], p['master_out']], 'samples': n, 'seconds': n / SR, 'wav': {'path': rel(wav), 'sha256': sha(wav)}, 'mp3': {'path': rel(mp3), 'sha256': sha(mp3)}})
    print(json.dumps({'part': pid, 'samples': n, 'seconds': n / SR, 'mp3': str(mp3)}))

def cmd_put(pid, url):
    mp3 = pd(pid) / 'audio/narration.mp3'
    code = run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-X', 'PUT', '-H', 'Content-Type: audio/mpeg', '--data-binary', f'@{mp3}', url])
    print(code)

def cmd_record_upload(pid, media_id, http_code, url=''):
    mp3 = pd(pid) / 'audio/narration.mp3'
    wj(pd(pid) / 'audio/HIGGSFIELD-UPLOAD.json', {'media_id': media_id, 'url': url, 'put_http': http_code, 'sha256': sha(mp3)}); print('ok')

def cmd_ledger(json_str):
    ledger(json.loads(json_str)); cr, usd = ledger_totals(); print(json.dumps({'lane_credits': cr, 'lane_usd': round(usd, 4)}))

def cmd_totals():
    cr, usd = ledger_totals(); print(json.dumps({'lane_credits': cr, 'credit_cap': CREDIT_CAP, 'lane_usd': round(usd, 4), 'fal_cap': FAL_CAP}))

def cmd_job(pid, json_str):
    """record the Higgsfield job (merge)."""
    f = pd(pid) / 'HIGGSFIELD-JOB.json'; cur = rj(f) if f.exists() else {}
    cur.update(json.loads(json_str)); wj(f, cur); print('ok')

def cmd_download(pid, url, name='native.mp4'):
    out = pd(pid) / name
    with media_temp(out) as tmp:
        run(['curl', '-s', '-f', '-o', tmp.name, url])
        publish_media(tmp.name, out)
    print(json.dumps({'part': pid, 'sha256': sha(out), 'bytes': out.stat().st_size}))

def speech_bounds(e, thr_ratio=0.08):
    thr = max(np.percentile(e, 20) * 3, e.max() * thr_ratio)
    idx = np.where(e > thr)[0]
    return (idx[0] / 100, idx[-1] / 100) if len(idx) else (None, None)

def cmd_native(pid, name='native.mp4'):
    p = PARTS[pid]; d = pd(pid); nat = d / name
    nar = pcm(d / 'audio/narration.wav'); nv = pcm(nat)
    en, ev = env(nar), env(nv)
    s0, s1 = speech_bounds(en)
    edges = np.linspace(s0, s1, 4); wins = []
    for i in range(3):
        a0, a1 = int(edges[i] * 100), int(edges[i + 1] * 100); seg = en[a0:a1]; best = (-2, 0)
        for lag in range(-60, 201):
            b0 = a0 + lag
            if b0 < 0 or b0 + len(seg) > len(ev): continue
            c = ncorr(seg, ev[b0:b0 + len(seg)])
            if c > best[0]: best = (c, lag)
        wins.append({'narration_window_s': [round(edges[i], 3), round(edges[i + 1], 3)], 'native_minus_narration_s': best[1] / 100, 'envelope_corr': round(best[0], 3)})
    offs = [w['native_minus_narration_s'] for w in wins]
    n0, n1 = speech_bounds(ev)
    probe = json.loads(run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,r_frame_rate,nb_frames:format=duration', '-of', 'json', str(nat)]))
    info = {'native': {'path': rel(nat), 'sha256': sha(nat)}, 'narration': {'path': rel(d / 'audio/narration.wav'), 'sha256': sha(d / 'audio/narration.wav')}, 'probe': probe, 'windows': wins, 'median_offset_s': float(np.median(offs)),
            'spread_s': round(max(offs) - min(offs), 3), 'drifted': (max(offs) - min(offs)) > 0.30,
            'onsets': {'narration_speech': [s0, s1], 'native_speech': [n0, n1], 'onset_diff': round(n0 - s0, 2), 'end_diff': round(n1 - s1, 2)},
            'narration_s': len(nar) / SR}
    out = d / ('NATIVE-OFFSETS.json' if name == 'native.mp4' else f'NATIVE-OFFSETS-{Path(name).stem}.json')
    wj(out, info); print(json.dumps({'part': pid, 'offsets': offs, 'corr': [w['envelope_corr'] for w in wins], 'median': info['median_offset_s'], 'spread': info['spread_s'], 'drifted': info['drifted'], 'onsets': info['onsets'], 'duration': probe['format']['duration']}))

def cmd_trim(pid):
    d = pd(pid); p = PARTS[pid]; no = native_gate(pid)
    source_sha, audio_sha = no['native']['sha256'], sha(d / 'audio/narration.wav')
    out = d / 'native-trim.mp4'
    if out.exists():
        record = rj(d / 'TRIM.json')
        if record.get('native_sha256') != source_sha or record.get('audio_sha256') != audio_sha or record.get('offsets_sha256') != sha(d / 'NATIVE-OFFSETS.json') or record['native_trim']['sha256'] != sha(out):
            raise RuntimeError(f'{pid}: existing trim differs or lacks provenance; preserve it and use a new part path')
        print(json.dumps({'part': pid, 'status': 'existing_verified_trim', 'trim_frames': record['trim_frames'], 'duration': record['native_trim']['duration']})); return
    dur = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(d / 'native.mp4')]))
    if dur < p['audio_seconds']:
        raise RuntimeError(f'{pid}: native clip is shorter than its narration')
    want = int(round(no['median_offset_s'] * 24))
    maxf = int(math.floor((dur - p['audio_seconds'] - 0.1) * 24))
    frames = max(0, min(want, maxf))
    with media_temp(out) as tmp:
        run(['ffmpeg', '-y', '-v', 'error', '-i', str(d / 'native.mp4'), '-vf', f'fps=24,trim=start_frame={frames},setpts=PTS-STARTPTS', '-af', f'atrim=start={frames/24},asetpts=PTS-STARTPTS',
             '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', '24', '-c:a', 'aac', '-b:a', '256k', tmp.name])
        publish_media(tmp.name, out)
    nd = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(out)]))
    wj(d / 'TRIM.json', {'median_offset_s': no['median_offset_s'], 'wanted_frames': want, 'max_frames': maxf, 'trim_frames': frames, 'trim_seconds': frames / 24,
                         'native_sha256': source_sha, 'audio_sha256': audio_sha, 'offsets_sha256': sha(d / 'NATIVE-OFFSETS.json'),
                         'method': 'normalize picture to 24 fps first, then trim both picture and audio by the median of the three-window native-minus-narration offsets, rounded to 24 fps frames, clamped to [0, cover audio + 0.1 s]',
                         'native_trim': {'path': rel(out), 'sha256': sha(out), 'duration': nd}})
    print(json.dumps({'part': pid, 'trim_frames': frames, 'wanted': want, 'duration': nd}))

def cmd_fal_submit(pid):
    d = pd(pid); no = native_gate(pid); trim = rj(d / 'TRIM.json')
    if trim.get('native_sha256') != no['native']['sha256'] or trim.get('offsets_sha256') != sha(d / 'NATIVE-OFFSETS.json') or trim.get('audio_sha256') != sha(d / 'audio/narration.wav') or trim['native_trim']['sha256'] != sha(d / 'native-trim.mp4'):
        raise RuntimeError(f'{pid}: trim/audio provenance changed; no paid Sync submission')
    tr = transport(); f = d / 'fal'; f.mkdir(exist_ok=True)
    assert not (f / 'SUBMISSION-INTENT.json').exists(), 'existing intent: never resubmit'
    (f / 'video').mkdir(exist_ok=True); (f / 'audio').mkdir(exist_ok=True)
    dur = rj(d / 'TRIM.json')['native_trim']['duration']; cost = round(dur * 8 / 60, 4)
    cr, usd = ledger_totals(); assert usd + cost <= FAL_CAP, (usd, cost)
    vu = tr.upload(d / 'native-trim.mp4', f / 'video', 'video/mp4')
    au = tr.upload(d / 'audio/narration.wav', f / 'audio', 'audio/wav')
    payload = {'video_url': vu, 'audio_url': au, 'sync_mode': 'silence'}
    item = f'{pid}-fal-sync'
    ledger({'item': item, 'provider': 'fal', 'model': 'fal-ai/sync-lipsync/v3', 'est_credits': 0, 'est_usd': cost, 'reason': f'{pid} restoration of trimmed native to the master excerpt', 'status': 'intent'})
    with (f / 'SUBMISSION-INTENT.json').open('x') as h:
        json.dump({'at': now(), 'model': 'fal-ai/sync-lipsync/v3', 'payload': payload, 'native_trim_seconds': dur, 'estimated_usd': cost, 'rate': '$8 per minute', 'no_retry': True}, h, indent=2)
    try: job = tr.api('https://queue.fal.run/fal-ai/sync-lipsync/v3', payload)
    except Exception as e:
        wj(f / 'ERROR.json', {'at': now(), 'error': str(e), 'submission_status': 'uncertain', 'retry': False})
        ledger({'item': item, 'provider': 'fal', 'model': 'fal-ai/sync-lipsync/v3', 'actual_credits': 0, 'actual_usd': cost, 'reason': 'submission error; charged at estimate until known', 'status': 'failed'}); raise
    wj(f / 'JOB.json', job); print(json.dumps({'part': pid, 'request_id': job['request_id'], 'est_usd': cost}))

def cmd_fal_result(pid):
    tr = transport(); f = pd(pid) / 'fal'; job = rj(f / 'JOB.json')
    st = tr.api(job['status_url']); wj(f / 'STATUS.json', st)
    if st.get('status') != 'COMPLETED': print(json.dumps({'part': pid, 'status': st.get('status')})); return
    res = tr.api(job['response_url']); wj(f / 'RESULT.json', res)
    raw = tr.get(res['video']['url']); out = pd(pid) / 'restored.mp4'
    with media_temp(out) as tmp:
        tmp.write(raw); tmp.flush(); publish_media(tmp.name, out)
    est = rj(f / 'SUBMISSION-INTENT.json')['estimated_usd']
    ledger({'item': f'{pid}-fal-sync', 'provider': 'fal', 'model': 'fal-ai/sync-lipsync/v3', 'actual_credits': 0, 'actual_usd': est, 'request_id': job['request_id'], 'reason': 'completed; usd from native-trim duration at $8/min', 'status': 'done'})
    print(json.dumps({'part': pid, 'status': 'COMPLETED', 'sha256': sha(out), 'bytes': len(raw)}))

def cmd_align(pid):
    d = pd(pid); nar = pcm(d / 'audio/narration.wav'); rs = pcm(d / 'restored.mp4')
    en, er = env(nar), env(rs); best = (-2, 0)
    for lag in range(-60, 61):
        i0 = max(0, -lag); i1 = min(len(en), len(er) - lag)
        if i1 - i0 < 50: continue
        c = ncorr(en[i0:i1], er[i0 + lag:i1 + lag])
        if c > best[0]: best = (c, lag)
    coarse = best[1] * 480; wins = []
    n = len(nar)
    for a0, a1 in [(0, n // 3), (n // 3, 2 * n // 3), (2 * n // 3, n)]:
        x = nar[a0:a1]; bw = (-2, 0)
        for lag in range(coarse - 960, coarse + 961):
            b0 = a0 + lag
            if b0 < 0 or b0 + len(x) > len(rs): continue
            y = rs[b0:b0 + len(x)]
            cc = float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-12))
            if cc > bw[0]: bw = (cc, lag)
        wins.append({'window_samples': [a0, a1], 'lag_samples': bw[1], 'corr': round(bw[0], 5)})
    L = int(np.median([w['lag_samples'] for w in wins])); start = int(round(L / 2000))
    probe = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries', 'stream=width,height,r_frame_rate,nb_read_frames', '-of', 'json', str(d / 'restored.mp4')]))['streams'][0]
    num, den = map(int, probe['r_frame_rate'].split('/'))
    if num != 24 * den:
        raise RuntimeError(f'{pid}: restored video is {probe["r_frame_rate"]}, expected 24 fps before frame-based alignment')
    info = {'restored': {'path': rel(d / 'restored.mp4'), 'sha256': sha(d / 'restored.mp4')}, 'probe': probe, 'windows': wins, 'restored_audio_lag_samples': L,
            'start_frame': start, 'picture_minus_audio_ms': round((start * 2000 - L) / 48, 2), 'restored_audio_s': len(rs) / SR}
    wj(d / 'ALIGNMENT.json', info); print(json.dumps({'part': pid, 'windows': wins, 'L': L, 'start_frame': start, 'frames': probe['nb_read_frames'], 'size': [probe['width'], probe['height']]}))

# ---------- sync gate (logic of presenter/_tools/sync_onsets.py and sync_whose_voice.py) ----------
def _sa():
    s = importlib.util.spec_from_file_location('sync_audit', B / 'presenter/_tools/sync_audit.py')
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def _onsets(wav):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(wav), '-ac', '1', '-ar', '48000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.int16).astype(float); hop = 480
    e = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
    thr = max(np.percentile(e, 20) * 3, np.max(e) * 0.06); out = []; quiet = 0
    for i, l in enumerate(e > thr):
        if not l: quiet += 1
        else:
            if quiet >= 25: out.append(i * hop / 48000.0)
            quiet = 0
    return out

def _rises(sa, m):
    m = sa.smooth(m, 3); closed = np.nanpercentile(m, 25); openv = np.nanpercentile(m, 70)
    thr = closed + 0.35 * (openv - closed)
    return np.array([i for i in range(3, len(m)) if m[i] > thr and np.all(m[i - 3:i] <= thr)])

def _corr_near(m, a, k=4):
    best = -2
    for lag in range(-k, k + 1):
        vv, aa = (m[lag:], a[:len(a) - lag]) if lag >= 0 else (m[:lag], a[-lag:])
        n = min(len(vv), len(aa)); vv, aa = vv[:n], aa[:n]
        if n > 24 and vv.std() > 1e-9 and aa.std() > 1e-9: best = max(best, float(np.corrcoef(vv, aa)[0, 1]))
    return best

def cmd_gate(pid):
    sa = _sa(); d = pd(pid); al = rj(d / 'ALIGNMENT.json'); L = al['restored_audio_lag_samples']
    m_rest = sa.mouth_series(str(d / 'restored.mp4'))
    ons = _onsets(d / 'audio/narration.wav'); r = _rises(sa, m_rest); diffs = []
    for o in ons:
        f = (o + L / 48000.0) * 24; near = r[(r > f - 12) & (r < f + 12)] if len(r) else r
        if len(near): diffs.append(float(near[np.argmin(np.abs(near - f))] - f))
    med = round(float(np.median(diffs)), 2) if diffs else None
    n = len(m_rest); narr = sa.audio_series(str(d / 'restored.mp4'), n); own = sa.audio_series(str(d / 'native-trim.mp4'), n)
    k = min(n, len(narr), len(own)); mm = sa.smooth(m_rest[:k])
    cn, co = _corr_near(mm, sa.smooth(narr[:k])), _corr_near(mm, sa.smooth(own[:k]))
    nm = sa.smooth(sa.mouth_series(str(d / 'native-trim.mp4'))[:k]); base = _corr_near(nm, sa.smooth(own[:k]))
    faces = int(np.sum(~np.isnan(m_rest)))
    res = {'status': 'diagnostics-complete', 'owner_accepted': False,
           'artifacts': {name: {'path': rel(d / name), 'sha256': sha(d / name)} for name in ('restored.mp4', 'native-trim.mp4', 'ALIGNMENT.json', 'audio/narration.wav')},
           'mouth_minus_onset_frames': {'median': med, 'n_onsets_matched': len(diffs), 'n_onsets': len(ons), 'diffs': diffs},
           'restored_mouth_corr': {'narration': round(cn, 3), 'generator_voice': round(co, 3), 'native_mouth_vs_own_voice': round(base, 3)},
           'face_detected_frames': [faces, n],
           'pass_signals': {'narration_over_generator': cn > co, 'onset_median_in_minus3_plus2': (med is not None and -3 <= med <= 2)},
           'limitation': 'Weak metrics (mouth-opening correlations 0.1 to 0.5; few onsets per part). A failing number is a flag, not proof; a passing number does not certify sync.'}
    wj(d / 'SYNC-GATE.json', res); print(json.dumps({'part': pid, **{k2: res[k2] for k2 in ('mouth_minus_onset_frames', 'restored_mouth_corr', 'pass_signals')}}))

def cmd_nose(pid):
    """median nose x (landmark 1) and top of head y on sampled restored frames."""
    import cv2, mediapipe as mp
    d = pd(pid); cap = cv2.VideoCapture(str(d / 'restored.mp4')); fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)
    xs, tops, i = [], [], 0; W = H = None
    while True:
        ok, frm = cap.read()
        if not ok: break
        if i % 8 == 0:
            H, W = frm.shape[:2]; r = fm.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
            if r.multi_face_landmarks:
                lm = r.multi_face_landmarks[0].landmark; xs.append(lm[1].x * W); tops.append(lm[10].y * H)
        i += 1
    info = {'nose_x_median': float(np.median(xs)), 'forehead_y_median': float(np.median(tops)), 'width': W, 'height': H, 'samples': len(xs)}
    wj(d / 'NOSE.json', info); print(json.dumps({'part': pid, **info}))

def rect_for(pid, size):
    n = rj(pd(pid) / 'NOSE.json'); W, H = n['width'], n['height']
    s = SIZE_SCALE[size]
    if size == 'W': return None
    assert not (H <= 720 and size == 'C'), '720p parts stay W or M'
    cw, ch = int(round(W / s / 2) * 2), int(round(H / s / 2) * 2)
    x = int(round(n['nose_x_median'] - cw / 2)); x = max(0, min(W - cw, x)); x -= x % 2
    return (cw, ch, x, 0)

def crop_filter(rect):
    if rect is None: return 'scale=1280:720:flags=lanczos'
    w, h, x, y = rect
    return f'crop={w}:{h}:{x}:{y},scale=1280:720:flags=lanczos'

def cmd_conform(sid):
    s = SEGS[sid]; N = seg_frames(s); S0 = fr(s['master_in'])
    plan = CROP_PLAN[sid]; pieces = []
    for k in range(S0, S0 + N):
        t = k / 24 + 1e-6
        part = next(p for p in PLAN['parts'] if fr(p['master_in']) <= k < fr(p['master_out']) or (p['master_out'] == 1233.602 and k >= fr(p['master_in'])))
        size = [sz for (t0, sz) in plan if fr(t0) <= k][-1]
        if pieces and pieces[-1]['part'] == part['part_id'] and pieces[-1]['size'] == size: pieces[-1]['end'] = k + 1
        else: pieces.append({'part': part['part_id'], 'size': size, 'start': k, 'end': k + 1})
    inputs, chains, labels, recs = [], [], [], []
    for i, pc in enumerate(pieces):
        pid = pc['part']; p = PARTS[pid]; al = rj(pd(pid) / 'ALIGNMENT.json'); total = int(al['probe']['nb_read_frames'])
        a = al['start_frame'] + (pc['start'] - fr(p['master_in'])); e = a + (pc['end'] - pc['start'])
        pad_front, pad_end = max(0, -a), max(0, e - total)
        inputs += ['-i', str(pd(pid) / 'restored.mp4')]
        rect = rect_for(pid, pc['size'])
        pre = f'tpad=start_mode=clone:start={pad_front}:stop_mode=clone:stop={pad_end},' if (pad_front or pad_end) else ''
        chains.append(f'[{i}:v]{pre}trim=start_frame={a + pad_front}:end_frame={e + pad_front},setpts=PTS-STARTPTS,{crop_filter(rect)},fps=24,setsar=1,format=yuv420p[v{i}]')
        labels.append(f'[v{i}]')
        recs.append({**pc, 'segment_frames': [pc['start'] - S0, pc['end'] - S0], 'source_frames': [a, e], 'pad_front': pad_front, 'pad_end': pad_end, 'rect': rect})
    npc = len(pieces)
    chains.append(''.join(labels) + (f'concat=n={npc}:v=1:a=0[vo]' if npc > 1 else 'null[vo]'))
    s0, s1 = int(round(s['master_in'] * SR)), int(round(s['master_out'] * SR))
    chains.append(f'[{npc}:a]atrim=start_sample={s0}:end_sample={s1},asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0[ao]')
    out = G / 'final' / f'{sid}.mp4'; out.parent.mkdir(exist_ok=True)
    run(['ffmpeg', '-y', '-v', 'error', *inputs, '-i', str(MASTER), '-filter_complex', ';'.join(chains), '-map', '[vo]', '-map', '[ao]',
         '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-r', '24', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', str(out)])
    cf = G / 'final' / 'CONFORM.json'; allc = rj(cf) if cf.exists() else {}
    allc[sid] = {'frames_expected': N, 'pieces': recs, 'path': rel(out)}; wj(cf, allc)
    print(json.dumps({'segment': sid, 'pieces': [(r['part'], r['size'], r['segment_frames'], r['source_frames'], r['pad_front'], r['pad_end']) for r in recs]}))

def cmd_verify(sid):
    s = SEGS[sid]; out = G / 'final' / f'{sid}.mp4'; N = seg_frames(s)
    pr = json.loads(run(['ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=codec_type,width,height,r_frame_rate,nb_read_frames,channels,sample_rate', '-of', 'json', str(out)]))['streams']
    v = [x for x in pr if x['codec_type'] == 'video'][0]; a = [x for x in pr if x['codec_type'] == 'audio'][0]
    m = master_excerpt(s['master_in'], s['master_out']); o = pcm(out, 2); n = min(len(m), len(o)); win = []
    for w0 in range(0, n - SR, 2 * SR):
        mm = m[w0:w0 + 2 * SR]; rm = np.sqrt((mm ** 2).mean())
        if rm < 1e-4: continue
        for ch in (0, 1): win.append(20 * np.log10(np.sqrt((o[w0:w0 + 2 * SR, ch] ** 2).mean()) / rm))
    corr = float(np.dot(m[:n], o[:n, 0]) / (np.linalg.norm(m[:n]) * np.linalg.norm(o[:n, 0])))
    ys = run(['ffmpeg', '-v', 'error', '-i', str(out), '-vf', 'signalstats,metadata=print:file=-', '-f', 'null', '-'])
    ymax = [float(l.split('=')[1]) for l in ys.splitlines() if 'signalstats.YMAX=' in l]; ymin = [float(l.split('=')[1]) for l in ys.splitlines() if 'signalstats.YMIN=' in l]
    r = {'segment': sid, 'path': rel(out), 'sha256': sha(out), 'frames': int(v['nb_read_frames']), 'frames_expected': N, 'frames_ok': int(v['nb_read_frames']) == N,
         'size': [v['width'], v['height']], 'fps': v['r_frame_rate'], 'audio': {'channels': a['channels'], 'sample_rate': a['sample_rate']},
         'rms_vs_master_db_2s': {'min': round(min(win), 3), 'max': round(max(win), 3), 'windows': len(win)}, 'zero_lag_corr_left': round(corr, 5),
         'audio_len_diff_samples': len(o) - len(m), 'uniform_frames': sum(1 for x, y in zip(ymax, ymin) if x - y < 8)}
    vf = G / 'final' / 'VERIFY.json'; allv = rj(vf) if vf.exists() else {}; allv[sid] = r; wj(vf, allv); print(json.dumps(r))

def cmd_sheet(pid, src='native.mp4', fps='2'):
    d = pd(pid); sd = d / 'stills'; sd.mkdir(exist_ok=True)
    out = sd / f'contact-{Path(src).stem}-{fps}fps.jpg'
    duration = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(d / src)]))
    rate = float(fps)
    if not math.isfinite(rate) or rate <= 0: raise ValueError('sheet fps must be positive')
    cols = 6; rows = max(1, math.ceil(duration * rate / cols))
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(d / src), '-vf', f'fps={rate},scale=400:-2,tile={cols}x{rows}', '-frames:v', '1', '-q:v', '3', str(out)])
    wj(out.with_suffix('.json'), {'source': {'path': rel(d / src), 'sha256': sha(d / src)}, 'sampling_fps': rate,
                                'source_duration_seconds': duration, 'columns': cols, 'rows': rows,
                                'reading_order': 'left to right, then top to bottom; ffmpeg fps samples at the requested rate',
                                'contact_sheet': {'path': rel(out), 'sha256': sha(out)}})
    print(str(out))

def cmd_segstills(sid):
    s = SEGS[sid]; N = seg_frames(s); sd = G / 'final' / 'stills'; sd.mkdir(parents=True, exist_ok=True)
    out = sd / f'{sid}-tile.jpg'; picks = [int((i + 0.5) * N / 6) for i in range(6)]
    sel = '+'.join(f'eq(n\\,{k})' for k in picks)
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(G / 'final' / f'{sid}.mp4'), '-vf', f"select='{sel}',scale=640:-2,tile=3x2", '-frames:v', '1', '-q:v', '3', str(out)])
    print(str(out))

def bound_artifact(binding, label):
    if not isinstance(binding, dict) or not binding.get('path') or not binding.get('sha256'):
        raise RuntimeError(f'{label}: missing artifact path or hash')
    path = (R / binding['path']).resolve()
    if not path.is_relative_to(R.resolve()) or not path.is_file():
        raise RuntimeError(f'{label}: artifact path missing or outside repository')
    if sha(path) != binding['sha256']:
        raise RuntimeError(f'{label}: artifact hash is stale')
    return path

def validate_derivation(pid, ex, paths):
    """Bind a reused provider prefix separately from its restoration narration."""
    derivation = ex.get('derivation')
    if derivation is None:
        return
    if not isinstance(derivation, dict) or derivation.get('method') != 'prefix-frame-selection-no-retime':
        raise RuntimeError(f'{pid}: unsupported native derivation method')
    source = bound_artifact(derivation.get('source_native'), 'derivation source_native')
    derived = bound_artifact(derivation.get('derived_native'), 'derivation derived_native')
    restoration = bound_artifact(derivation.get('restoration_audio'), 'derivation restoration_audio')
    if source == derived or derived != paths['native']:
        raise RuntimeError(f'{pid}: derived native must be the selected native and preserve its separate source')
    if restoration != (pd(pid) / 'audio/narration.wav').resolve():
        raise RuntimeError(f'{pid}: derivation binds a different restoration narration')
    frames = derivation.get('source_frames')
    count = derivation.get('source_frame_count')
    fps = derivation.get('source_fps')
    if (not isinstance(frames, list) or len(frames) != 2 or any(type(n) is not int for n in frames)
            or type(count) is not int or not 0 == frames[0] < frames[1] <= count or fps != 24):
        raise RuntimeError(f'{pid}: invalid original-speed 24 fps prefix range')
    for label, path, expected in (('source', source, count), ('derived', derived, frames[1] - frames[0])):
        probe = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
                               '-show_entries', 'stream=r_frame_rate,avg_frame_rate,nb_read_frames', '-of', 'json', str(path)]))
        streams = probe.get('streams', [])
        if len(streams) != 1:
            raise RuntimeError(f'{pid}: {label} native has no unique video stream')
        video = streams[0]
        for field in ('r_frame_rate', 'avg_frame_rate'):
            numerator, denominator = (int(n) for n in video[field].split('/'))
            if denominator <= 0 or numerator != fps * denominator:
                raise RuntimeError(f'{pid}: {label} native frame rate disagrees with derivation')
        if int(video['nb_read_frames']) != expected:
            raise RuntimeError(f'{pid}: {label} native frame count disagrees with derivation')

def resolve_execution(pid):
    """Require the selected execution, never guess it from numbered attempts."""
    d = pd(pid); path = d / 'EXECUTION.json'; ex = rj(path)
    if ex.get('record_type') != 'presenter_part_execution' or ex.get('part_id') != pid:
        raise RuntimeError(f'{pid}: wrong execution record type or part')
    if bound_artifact(ex.get('base_plan'), 'base_plan') != (G / 'TAKE-PLAN.json').resolve():
        raise RuntimeError(f'{pid}: execution binds a different base plan')
    if PLAN_PATH != BASE_PLAN_PATH and bound_artifact(ex.get('selected_plan'), 'selected_plan') != PLAN_PATH:
        raise RuntimeError(f'{pid}: execution binds a different active plan')
    artifacts = ex.get('artifacts', {})
    paths = {name: bound_artifact(artifacts.get(name), name) for name in ('prompt', 'higgsfield_job', 'higgsfield_upload', 'native')}
    if paths['native'] != (d / 'native.mp4').resolve():
        raise RuntimeError(f'{pid}: execution native differs from the measured native path')
    validate_derivation(pid, ex, paths)
    job = rj(paths['higgsfield_job']); upload = rj(paths['higgsfield_upload']); gen = ex.get('generation', {})
    rows = job.get('results', [job])
    matches = [row for row in rows if (row.get('id') or row.get('job_id')) == ex.get('job_id')]
    if not ex.get('job_id') or len(matches) != 1:
        raise RuntimeError(f'{pid}: execution job ID is not unique in the bound receipt')
    actual = matches[0]; params = actual.get('params', actual)
    if gen.get('model') != actual.get('model'):
        raise RuntimeError(f'{pid}: generation model disagrees with provider receipt')
    for requested, returned in (('mode', 'mode'), ('resolution', 'resolution'), ('aspect_ratio', 'aspect_ratio'), ('generation_seconds', 'duration'), ('generate_audio', 'generate_audio')):
        if requested not in gen or gen[requested] != params.get(returned):
            raise RuntimeError(f'{pid}: generation {requested} disagrees with provider receipt')
    if not isinstance(gen.get('est_credits'), (int, float)) or gen['est_credits'] < 0:
        raise RuntimeError(f'{pid}: missing generation credit estimate')
    if paths['prompt'].read_text().strip() != params.get('prompt', '').strip():
        raise RuntimeError(f'{pid}: active prompt disagrees with provider receipt')
    medias = gen.get('medias', [])
    audio_ids = [x.get('value') for x in medias if x.get('role') in ('audio', 'audio_references')]
    if audio_ids != [upload.get('media_id')] or not audio_ids[0]:
        raise RuntimeError(f'{pid}: generation audio does not match the bound upload')
    returned_ids = []
    for name in ('reference_images', 'reference_videos', 'reference_audio', 'image_references', 'video_references', 'audio_references'):
        returned_ids.extend(params.get(name, []))
    if sorted(x['value'] for x in medias) != sorted(returned_ids):
        raise RuntimeError(f'{pid}: media IDs disagree with provider receipt')
    return ex, paths, job, upload

def cmd_take(pid):
    d = pd(pid); p = PARTS[pid]; g = lambda n: rj(d / n) if (d / n).exists() else None
    ex, paths, job, upload = resolve_execution(pid)
    notes = g('NOTES.json') or {}
    take = {'part_id': pid, 'take_id': p['take_id'], 'segment_ids': p['segment_ids'], 'master': [p['master_in'], p['master_out']], 'words': p['words'],
            'base_plan': {k: p[k] for k in ('generation_seconds', 'resolution', 'est_credits', 'gesture')},
            'plan': {**{k: p[k] for k in ('generation_seconds', 'resolution', 'est_credits', 'gesture')}, **{k: ex['generation'][k] for k in ('generation_seconds', 'resolution', 'est_credits')}},
            'execution': {'path': rel(d / 'EXECUTION.json'), 'sha256': sha(d / 'EXECUTION.json'), 'job_id': ex['job_id'], 'generation': ex['generation'], 'artifacts': ex['artifacts'], 'selected_plan': ex.get('selected_plan'), 'derivation': ex.get('derivation')},
            'prompt': ex['artifacts']['prompt'],
            'provider_source': {'kind': 'derived-prefix' if ex.get('derivation') else 'direct-generation',
                                'job_id': ex['job_id'], 'job': ex['artifacts']['higgsfield_job'],
                                'guidance_audio_upload': ex['artifacts']['higgsfield_upload'],
                                'native': ex['derivation']['source_native'] if ex.get('derivation') else ex['artifacts']['native']},
            'restoration_audio': {'path': rel(d / 'audio/narration.wav'), 'sha256': sha(d / 'audio/narration.wav'),
                                  'role': 'locked narration used for restoration; no identity with provider guidance is asserted'},
            'audio': g('audio/AUDIO.json'), 'higgsfield_upload': upload, 'higgsfield_job': job,
            'native_offsets': g('NATIVE-OFFSETS.json'), 'trim': g('TRIM.json'),
            'fal': {'intent': g('fal/SUBMISSION-INTENT.json'), 'job': g('fal/JOB.json'), 'status': g('fal/STATUS.json')},
            'alignment': g('ALIGNMENT.json'), 'sync_gate': g('SYNC-GATE.json'), 'nose': g('NOSE.json'),
            'stills': sorted(rel(x) for x in (d / 'stills').glob('*')) if (d / 'stills').exists() else [], 'notes': notes,
            'review_artifacts': {name: {'path': rel(d / name), 'sha256': sha(d / name)} for name in ('SYNC-GATE.json', 'NOTES.json', 'ALIGNMENT.json', 'restored.mp4') if (d / name).exists()},
            'owner_accepted': False}
    wj(d / 'TAKE.json', take); print('ok')

def part_review_state(pid):
    """Completed diagnostics and scoped review are required, not an acceptance."""
    d = pd(pid)
    try:
        resolve_execution(pid)
        take = rj(d / 'TAKE.json'); gate = rj(d / 'SYNC-GATE.json'); notes = rj(d / 'NOTES.json')
        if bound_artifact(take.get('execution'), 'take execution') != (d / 'EXECUTION.json').resolve():
            raise RuntimeError('take binds a different execution')
        for name in ('SYNC-GATE.json', 'NOTES.json', 'ALIGNMENT.json', 'restored.mp4'):
            if bound_artifact(take.get('review_artifacts', {}).get(name), 'take ' + name) != (d / name).resolve():
                raise RuntimeError('take binds a different review artifact')
        if gate.get('status') != 'diagnostics-complete': raise RuntimeError('sync diagnostics incomplete')
        for name in ('restored.mp4', 'native-trim.mp4', 'ALIGNMENT.json', 'audio/narration.wav'):
            if bound_artifact(gate.get('artifacts', {}).get(name), 'gate ' + name) != (d / name).resolve():
                raise RuntimeError('gate binds a different input')
        if notes.get('review_status') != 'complete' or not isinstance(notes.get('flagged'), bool):
            raise RuntimeError('review notes incomplete')
        for name in ('reviewer', 'method', 'review_limitations'):
            if not notes.get(name): raise RuntimeError('review notes missing ' + name)
        for name, filename in (('execution_sha256', 'EXECUTION.json'), ('restored_sha256', 'restored.mp4'), ('sync_gate_sha256', 'SYNC-GATE.json')):
            if notes.get(name) != sha(d / filename): raise RuntimeError('review notes stale: ' + name)
        signals = gate.get('pass_signals')
        required = ('narration_over_generator', 'onset_median_in_minus3_plus2')
        if not isinstance(signals, dict) or any(not isinstance(signals.get(k), bool) for k in required):
            raise RuntimeError('sync diagnostic signals incomplete')
        return {'complete': True, 'flagged': notes['flagged'] or not all(signals[k] for k in required)}
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as e:
        return {'complete': False, 'reason': str(e)}

def cmd_index():
    idx = {'record_type': 'presenter_regen_index', 'updated_at': now(), 'look': PLAN['look'], 'segments': {}}
    vf = G / 'final' / 'VERIFY.json'; allv = rj(vf) if vf.exists() else {}
    for sid in CROP_PLAN:
        parts = [p['part_id'] for p in PLAN['parts'] if sid in p['segment_ids']]
        f = G / 'final' / f'{sid}.mp4'; vr = allv.get(sid)
        reviews = {pid: part_review_state(pid) for pid in parts}
        flags = [pid for pid, review in reviews.items() if review.get('flagged')]
        if f.exists() and vr and vr['frames_ok'] and vr['sha256'] == sha(f):
            complete = all(review['complete'] for review in reviews.values())
            idx['segments'][sid] = {'status': ('review-ready-flagged' if flags else 'review-ready') if complete else 'pending-review',
                                    'technical_complete': complete, 'owner_accepted': False, 'path': rel(f), 'sha256': vr['sha256'], 'frames': vr['frames'],
                                    'parts_used': parts, 'flagged_parts': flags, 'part_reviews': reviews}
        else: idx['segments'][sid] = {'status': 'pending', 'parts_used': parts}
    wj(G / 'INDEX.json', idx); print(json.dumps({k: v['status'] for k, v in idx['segments'].items()}))

if __name__ == '__main__':
    fn = {'cut': cmd_cut, 'put': cmd_put, 'record-upload': cmd_record_upload, 'ledger': cmd_ledger, 'totals': cmd_totals, 'job': cmd_job, 'download': cmd_download,
          'native': cmd_native, 'trim': cmd_trim, 'fal-submit': cmd_fal_submit, 'fal-result': cmd_fal_result, 'align': cmd_align, 'gate': cmd_gate, 'nose': cmd_nose,
          'conform': cmd_conform, 'verify': cmd_verify, 'sheet': cmd_sheet, 'segstills': cmd_segstills, 'take': cmd_take, 'index': cmd_index}[sys.argv[1]]
    fn(*sys.argv[2:])
