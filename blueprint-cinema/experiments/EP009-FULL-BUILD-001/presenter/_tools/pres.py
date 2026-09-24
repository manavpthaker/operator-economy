"""EP009 presenter lane: audio cuts, native offsets, trim, Fal Sync v3, alignment, conform, verify.
Paid calls (Fal) write ledger intent before submission and never resubmit an existing intent.
Run with a python that has numpy."""
import datetime, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parents[1]          # presenter/
B = P.parent                                       # EP009-FULL-BUILD-001/
R = next(x for x in P.parents if (x / '.agents').is_dir())
EP7 = R / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews'
MASTER = R / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'
MASTER_SHA = 'e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944'
WT = R / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/word-transcript.json'
SHOT = json.loads((B / 'direction/SHOT-PLAN.json').read_text())
TAKES = {t['take_id']: t for t in SHOT['presenter_takes']}
SEGS = {s['id']: s for s in SHOT['segments']}
WORDS = {w['w_id']: w for w in json.loads(WT.read_text())['words']}
LEDGER = B / 'ledger/presenter.jsonl'
FAL_CAP = 30.0
SR = 48000

now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
rj = lambda p: json.loads(Path(p).read_text())
def wj(p, d): Path(p).write_text(json.dumps(d, indent=2) + '\n')
def run(cmd): return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
def fr(t): return int(round(t * 24))

def transport():
    s = importlib.util.spec_from_file_location('fal_ops', EP7 / 'r32-performance-refinement/provider/fal_ops.py')
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def ledger(entry):
    entry = {'at': now(), 'lane': 'presenter', **entry}
    with LEDGER.open('a') as f: f.write(json.dumps(entry) + '\n')

def ledger_totals():
    rows = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]
    closed = {r['item'] for r in rows if r['status'] in ('done', 'failed')}
    cr = usd = 0.0
    for r in rows:
        if r['status'] in ('done', 'failed'):
            cr += r.get('actual_credits') or 0; usd += r.get('actual_usd') or 0
        elif r['status'] == 'intent' and r['item'] not in closed:
            cr += r.get('est_credits') or 0; usd += r.get('est_usd') or 0
    return cr, usd

def pcm(path, ch=1, start=None, dur=None):
    cmd = ['ffmpeg', '-v', 'error']
    if start is not None: cmd += ['-ss', str(start)]
    cmd += ['-i', str(path)]
    if dur is not None: cmd += ['-t', str(dur)]
    cmd += ['-vn', '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', 'pipe:1']
    a = np.frombuffer(subprocess.run(cmd, check=True, capture_output=True).stdout, dtype='<f4').astype(np.float64)
    return a.reshape(-1, ch) if ch > 1 else a

def master_excerpt(t0, t1):
    s0, s1 = int(round(t0 * SR)), int(round(t1 * SR))
    cmd = ['ffmpeg', '-v', 'error', '-i', str(MASTER), '-af', f'atrim=start_sample={s0}:end_sample={s1}', '-ac', '1', '-f', 'f32le', 'pipe:1']
    return np.frombuffer(subprocess.run(cmd, check=True, capture_output=True).stdout, dtype='<f4').astype(np.float64)

def excerpt_cmd(t0, t1, out, stereo=False):
    s0, s1 = int(round(t0 * SR)), int(round(t1 * SR))
    af = f'atrim=start_sample={s0}:end_sample={s1},asetpts=N/SR/TB'
    return ['ffmpeg', '-y', '-v', 'error', '-i', str(MASTER), '-af', af, '-ac', '1', str(out)]

def td(tid): return P / tid

def cmd_cut(tid):
    assert sha(MASTER) == MASTER_SHA
    t = TAKES[tid]; d = td(tid) / 'audio'; d.mkdir(parents=True, exist_ok=True)
    wav = d / 'narration.wav'; mp3 = d / 'narration.mp3'
    run(excerpt_cmd(t['master_in'], t['master_out'], wav))
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(wav), '-c:a', 'libmp3lame', '-b:a', '320k', str(mp3)])
    n = len(pcm(wav)); want = int(round(t['master_out'] * SR)) - int(round(t['master_in'] * SR))
    assert n == want, (n, want)
    info = {'master_range': [t['master_in'], t['master_out']], 'samples': n, 'wav': {'path': str(wav.relative_to(R)), 'sha256': sha(wav)}, 'mp3': {'path': str(mp3.relative_to(R)), 'sha256': sha(mp3)}}
    wj(d / 'AUDIO.json', info); print(json.dumps({'take': tid, 'samples': n, 'seconds': n / SR}))

def env(x, hop=480):  # 10 ms RMS envelope
    n = len(x) // hop
    return np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)

def best_lag(a, b, lo, hi):
    """lag (in env units) maximising corr of a[i] with b[i+lag]."""
    best = (-2, 0)
    for lag in range(lo, hi + 1):
        i0 = max(0, -lag); i1 = min(len(a), len(b) - lag)
        if i1 - i0 < 50: continue
        x = a[i0:i1] - a[i0:i1].mean(); y = b[i0 + lag:i1 + lag] - b[i0 + lag:i1 + lag].mean()
        c = float(np.dot(x, y) / (np.sqrt(np.dot(x, x) * np.dot(y, y)) + 1e-12))
        if c > best[0]: best = (c, lag)
    return best

def cmd_native(tid):
    t = TAKES[tid]; d = td(tid); nat = d / 'native.mp4'
    nar = pcm(d / 'audio/narration.wav'); nv = pcm(nat)
    en, ev = env(nar), env(nv)
    # windows: thirds of the speech span inside the excerpt
    w0 = WORDS[t['first_word_id']]['start'] - t['master_in']; w1 = min(WORDS[t['last_word_id']]['end'], t['master_out']) - t['master_in']
    edges = np.linspace(w0, w1, 4); wins = []
    for i in range(3):
        a0, a1 = int(edges[i] * 100), int(edges[i + 1] * 100)
        seg = en[a0:a1]; best = (-2, 0)
        for lag in range(-40, 151):
            b0 = a0 + lag
            if b0 < 0 or b0 + len(seg) > len(ev): continue
            y = ev[b0:b0 + len(seg)]; x = seg
            c = float(np.dot(x - x.mean(), y - y.mean()) / (np.linalg.norm(x - x.mean()) * np.linalg.norm(y - y.mean()) + 1e-12))
            if c > best[0]: best = (c, lag)
        wins.append({'narration_window_s': [round(edges[i], 3), round(edges[i + 1], 3)], 'native_minus_narration_s': best[1] / 100, 'envelope_corr': round(best[0], 3)})
    probe = json.loads(run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,r_frame_rate,nb_frames:format=duration', '-of', 'json', str(nat)]))
    info = {'native': {'path': str(nat.relative_to(R)), 'sha256': sha(nat)}, 'probe': probe, 'windows': wins, 'narration_s': len(nar) / SR}
    wj(d / 'NATIVE-OFFSETS.json', info); print(json.dumps({'take': tid, 'windows': wins, 'duration': probe['format']['duration']}))

def cmd_trim(tid, frames):
    frames = int(frames); d = td(tid); t = TAKES[tid]
    dur = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(d / 'native.mp4')]))
    assert frames >= 0 and dur - frames / 24 >= t['audio_seconds'] + 0.1, (dur, frames)
    out = d / 'native-trim.mp4'
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(d / 'native.mp4'), '-vf', f'trim=start_frame={frames},setpts=PTS-STARTPTS', '-af', f'atrim=start={frames/24},asetpts=PTS-STARTPTS',
         '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', '24', '-c:a', 'aac', '-b:a', '256k', str(out)])
    nd = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(out)]))
    wj(d / 'TRIM.json', {'trim_frames': frames, 'trim_seconds': frames / 24, 'native_trim': {'path': str(out.relative_to(R)), 'sha256': sha(out), 'duration': nd}})
    print(json.dumps({'take': tid, 'trim_frames': frames, 'duration': nd}))

def cmd_fal_submit(tid):
    tr = transport(); d = td(tid); f = d / 'fal'; f.mkdir(exist_ok=True)
    assert not (f / 'SUBMISSION-INTENT.json').exists(), 'existing intent: never resubmit'
    (f / 'video').mkdir(exist_ok=True); (f / 'audio').mkdir(exist_ok=True)
    vu = tr.upload(d / 'native-trim.mp4', f / 'video', 'video/mp4')
    au = tr.upload(d / 'audio/narration.wav', f / 'audio', 'audio/wav')
    dur = rj(d / 'TRIM.json')['native_trim']['duration']; cost = round(dur * 8 / 60, 4)
    cr, usd = ledger_totals(); assert usd + cost <= FAL_CAP, (usd, cost)
    payload = {'video_url': vu, 'audio_url': au, 'sync_mode': 'silence'}
    item = f'{tid}-fal-sync'
    ledger({'item': item, 'provider': 'fal', 'model': 'fal-ai/sync-lipsync/v3', 'est_credits': 0, 'est_usd': cost, 'reason': f'{tid} restoration of trimmed native to the master excerpt', 'status': 'intent'})
    with (f / 'SUBMISSION-INTENT.json').open('x') as h:
        json.dump({'at': now(), 'model': 'fal-ai/sync-lipsync/v3', 'payload': payload, 'native_trim_seconds': dur, 'estimated_usd': cost, 'rate': '$8 per minute (Fal pricing API 2026-09-16)', 'no_retry': True}, h, indent=2)
    try: job = tr.api('https://queue.fal.run/fal-ai/sync-lipsync/v3', payload)
    except Exception as e:
        wj(f / 'ERROR.json', {'at': now(), 'error': str(e), 'submission_status': 'uncertain', 'retry': False})
        ledger({'item': item, 'provider': 'fal', 'model': 'fal-ai/sync-lipsync/v3', 'actual_credits': 0, 'actual_usd': cost, 'reason': 'submission error; charged at estimate until known', 'status': 'failed'}); raise
    wj(f / 'JOB.json', job); print(json.dumps({'take': tid, 'request_id': job['request_id'], 'est_usd': cost}))

def cmd_fal_result(tid):
    tr = transport(); f = td(tid) / 'fal'; job = rj(f / 'JOB.json')
    st = tr.api(job['status_url']); wj(f / 'STATUS.json', st)
    if st.get('status') != 'COMPLETED': print(json.dumps({'take': tid, 'status': st.get('status')})); return
    res = tr.api(job['response_url']); wj(f / 'RESULT.json', res)
    raw = tr.get(res['video']['url']); out = td(tid) / 'restored.mp4'
    if out.exists(): assert sha(out) == hashlib.sha256(raw).hexdigest()
    else: out.write_bytes(raw)
    est = rj(f / 'SUBMISSION-INTENT.json')['estimated_usd']
    ledger({'item': f'{tid}-fal-sync', 'provider': 'fal', 'model': 'fal-ai/sync-lipsync/v3', 'actual_credits': 0, 'actual_usd': est, 'request_id': job['request_id'], 'reason': 'completed; usd from native-trim duration at $8/min (Fal bills output minutes)', 'status': 'done'})
    print(json.dumps({'take': tid, 'status': 'COMPLETED', 'sha256': sha(out), 'bytes': len(raw)}))

def cmd_align(tid):
    d = td(tid); nar = pcm(d / 'audio/narration.wav'); rs = pcm(d / 'restored.mp4')
    # coarse on envelope, then sample-exact via FFT xcorr around it
    c, lag_env = best_lag(env(nar), env(rs), -60, 60)
    coarse = lag_env * 480; best = None
    wins = []
    n = len(nar); thirds = [(0, n // 3), (n // 3, 2 * n // 3), (2 * n // 3, n)]
    for a0, a1 in thirds:
        x = nar[a0:a1]; bestw = (-2, 0)
        for lag in range(coarse - 960, coarse + 961):
            b0 = a0 + lag
            if b0 < 0 or b0 + len(x) > len(rs): continue
            y = rs[b0:b0 + len(x)]
            cc = float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-12))
            if cc > bestw[0]: bestw = (cc, lag)
        wins.append({'window_samples': [a0, a1], 'lag_samples': bestw[1], 'corr': round(bestw[0], 5)})
    lags = [w['lag_samples'] for w in wins]
    L = int(np.median(lags)); start = int(round(L / 2000))
    probe = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries', 'stream=width,height,r_frame_rate,nb_read_frames', '-of', 'json', str(d / 'restored.mp4')]))['streams'][0]
    info = {'restored': {'path': str((d / 'restored.mp4').relative_to(R)), 'sha256': sha(d / 'restored.mp4')}, 'probe': probe, 'windows': wins,
            'restored_audio_lag_samples': L, 'start_frame': start, 'picture_minus_audio_ms': round((start * 2000 - L) / 48, 2), 'restored_audio_s': len(rs) / SR}
    wj(d / 'ALIGNMENT.json', info); print(json.dumps({'take': tid, **{k: info[k] for k in ['windows', 'restored_audio_lag_samples', 'start_frame', 'picture_minus_audio_ms']}, 'frames': probe['nb_read_frames'], 'fps': probe['r_frame_rate']}))

def crop_filter(rect):
    if rect is None: return 'scale=1280:720:flags=lanczos'
    w, h, x, y = rect
    return f'crop={w}:{h}:{x}:{y},scale=1280:720:flags=lanczos'

def cmd_conform(tid, plan_name='CROP-PLAN.json', outdir='final', only=None):
    d = td(tid); t = TAKES[tid]; al = rj(d / 'ALIGNMENT.json'); plan = rj(d / plan_name)
    total = int(al['probe']['nb_read_frames']); start = al['start_frame']
    take0 = fr(t['master_in']); outs = []
    (d / outdir).mkdir(parents=True, exist_ok=True)
    for sid in t['segment_ids']:
        if only and sid != only: continue
        s = SEGS[sid]; f0 = fr(s['master_in']) - take0; N = fr(s['master_out']) - fr(s['master_in'])
        if s['master_out'] == 1233.602: N = 29607 - fr(s['master_in'])
        # crop ranges in take-relative frames: [[from_frame, rect|null], ...]
        ranges = sorted(plan['ranges'], key=lambda r: r[0])
        parts = []; k = f0
        while k < f0 + N:
            cur = [r for r in ranges if r[0] <= k][-1]; nxt = [r[0] for r in ranges if r[0] > k] + [f0 + N]
            e = min(nxt[0], f0 + N); parts.append((k, e, cur[1])); k = e
        src0 = start + f0; need_end = start + f0 + N
        pad_front = max(0, -src0); pad_end = max(0, need_end - total)
        chains = []; vlabels = []
        base = '[0:v]'
        if pad_front or pad_end:
            chains.append(f'[0:v]tpad=start_mode=clone:start={pad_front}:stop_mode=clone:stop={pad_end}[vp]'); base = '[vp]'
        sp = len(parts)
        chains.append(f'{base}split={sp}' + ''.join(f'[s{i}]' for i in range(sp)) if sp > 1 else f'{base}null[s0]')
        for i, (a, e, rect) in enumerate(parts):
            sa, se = a + start + pad_front, e + start + pad_front
            chains.append(f'[s{i}]trim=start_frame={sa}:end_frame={se},setpts=PTS-STARTPTS,{crop_filter(rect)},fps=24,setsar=1,format=yuv420p[v{i}]'); vlabels.append(f'[v{i}]')
        chains.append(''.join(vlabels) + f'concat=n={sp}:v=1:a=0[vo]' if sp > 1 else '[v0]null[vo]')
        s0, s1 = int(round(s['master_in'] * SR)), int(round(s['master_out'] * SR))
        chains.append(f'[1:a]atrim=start_sample={s0}:end_sample={s1},asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0[ao]')
        out = d / outdir / (f'{sid}.mp4' if outdir == 'final' else f'{sid}-{Path(plan_name).stem.lower()}.mp4')
        run(['ffmpeg', '-y', '-v', 'error', '-i', str(d / 'restored.mp4'), '-i', str(MASTER), '-filter_complex', ';'.join(chains), '-map', '[vo]', '-map', '[ao]',
             '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-r', '24', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', str(out)])
        outs.append({'segment': sid, 'frames_expected': N, 'source_frames': [src0, need_end], 'pad_front': pad_front, 'pad_end': pad_end, 'parts': parts, 'path': str(out.relative_to(R))})
    wj(d / ('CONFORM.json' if outdir == 'final' else f'CONFORM-{Path(plan_name).stem}.json'), {'start_frame': start, 'plan': plan_name, 'outputs': outs}); print(json.dumps(outs))

def cmd_verify(tid):
    d = td(tid); t = TAKES[tid]; res = []
    for sid in t['segment_ids']:
        s = SEGS[sid]; out = d / 'final' / f'{sid}.mp4'
        N = (29607 if s['master_out'] == 1233.602 else fr(s['master_out'])) - fr(s['master_in'])
        pr = json.loads(run(['ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=codec_type,width,height,r_frame_rate,nb_read_frames,channels,sample_rate', '-of', 'json', str(out)]))['streams']
        v = [x for x in pr if x['codec_type'] == 'video'][0]; a = [x for x in pr if x['codec_type'] == 'audio'][0]
        m = master_excerpt(s['master_in'], s['master_out'])
        o = pcm(out, 2)
        n = min(len(m), len(o)); win = []
        for w0 in range(0, n - SR, 2 * SR):
            mm = m[w0:w0 + 2 * SR]; rm = np.sqrt((mm ** 2).mean())
            if rm < 1e-4: continue
            for ch in (0, 1):
                ro = np.sqrt((o[w0:w0 + 2 * SR, ch] ** 2).mean()); win.append(20 * np.log10(ro / rm))
        corr = float(np.dot(m[:n], o[:n, 0]) / (np.linalg.norm(m[:n]) * np.linalg.norm(o[:n, 0])))
        yst = run(['ffmpeg', '-v', 'error', '-i', str(out), '-vf', 'signalstats,metadata=print:key=lavfi.signalstats.YMAX:file=-', '-f', 'null', '-'])
        ymax = [float(l.split('=')[1]) for l in yst.splitlines() if 'YMAX' in l]
        yst2 = run(['ffmpeg', '-v', 'error', '-i', str(out), '-vf', 'signalstats,metadata=print:key=lavfi.signalstats.YMIN:file=-', '-f', 'null', '-'])
        ymin = [float(l.split('=')[1]) for l in yst2.splitlines() if 'YMIN' in l]
        uniform = sum(1 for a_, b_ in zip(ymax, ymin) if a_ - b_ < 8)
        r = {'segment': sid, 'path': str(out.relative_to(R)), 'sha256': sha(out), 'frames': int(v['nb_read_frames']), 'frames_expected': N, 'frames_ok': int(v['nb_read_frames']) == N,
             'size': [v['width'], v['height']], 'fps': v['r_frame_rate'], 'audio': {'channels': a['channels'], 'sample_rate': a['sample_rate']},
             'rms_vs_master_db_2s': {'min': round(min(win), 3), 'max': round(max(win), 3), 'windows': len(win)}, 'zero_lag_corr_left': round(corr, 5), 'audio_len_diff_samples': len(o) - len(m), 'uniform_frames': uniform}
        res.append(r)
    wj(d / 'VERIFY.json', res); print(json.dumps(res, indent=1))

def cmd_stills(tid):
    d = td(tid); t = TAKES[tid]; sd = d / 'stills'; sd.mkdir(exist_ok=True)
    segs = [(sid, (29607 if SEGS[sid]['master_out'] == 1233.602 else fr(SEGS[sid]['master_out'])) - fr(SEGS[sid]['master_in'])) for sid in t['segment_ids']]
    total = sum(n for _, n in segs); paths = []
    for i in range(6):
        f = int((i + 0.5) * total / 6); acc = 0
        for sid, n in segs:
            if f < acc + n:
                lf = f - acc; out = sd / f'still-{i+1}-{sid}-f{lf:04d}.png'
                run(['ffmpeg', '-y', '-v', 'error', '-i', str(d / 'final' / f'{sid}.mp4'), '-vf', f'select=eq(n\\,{lf})', '-frames:v', '1', str(out)]); paths.append(str(out.relative_to(R))); break
            acc += n
    al = rj(d / 'ALIGNMENT.json'); n = int(al['probe']['nb_read_frames']); cols = 8; rows = int(np.ceil(n / 12 / cols))
    cs = sd / 'contact-2fps.jpg'
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(d / 'restored.mp4'), '-vf', f"fps=2,scale=320:-2,tile={cols}x{rows}", '-frames:v', '1', '-q:v', '3', str(cs)])
    paths.append(str(cs.relative_to(R)))
    for old in sd.glob('still-*.png'):
        if str(old.relative_to(R)) not in paths: old.unlink()
    tile = sd / 'stills-tile.jpg'; ins = []
    for p in paths[:6]: ins += ['-i', str(R / p)]
    run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', '[0][1][2][3][4][5]xstack=inputs=6:layout=0_0|w0_0|w0+w1_0|0_h0|w0_h0|w0+w1_h0,scale=1920:-2', str(tile)])
    print(json.dumps(paths))

def cmd_take(tid):
    d = td(tid); t = TAKES[tid]; g = lambda n: rj(d / n) if (d / n).exists() else None
    notes = g('NOTES.json') or {}
    take = {'take_id': tid, 'segment_ids': t['segment_ids'], 'master': [t['master_in'], t['master_out']], 'words': t['words'],
            'prompt': {'path': str((d / 'AVATAR-PROMPT.txt').relative_to(R)), 'sha256': sha(d / 'AVATAR-PROMPT.txt')},
            'audio': g('audio/AUDIO.json'), 'higgsfield_upload': g('audio/HIGGSFIELD-UPLOAD.json'), 'higgsfield_job': g('HIGGSFIELD-JOB.json'),
            'native_offsets': g('NATIVE-OFFSETS.json'), 'trim': g('TRIM.json'),
            'fal': {'intent': g('fal/SUBMISSION-INTENT.json'), 'job': g('fal/JOB.json'), 'status': g('fal/STATUS.json')},
            'alignment': g('ALIGNMENT.json'), 'crop_plan': g('CROP-PLAN.json'), 'conform': g('CONFORM.json'), 'verify': g('VERIFY.json'),
            'stills': sorted(str(x.relative_to(R)) for x in (d / 'stills').glob('*')) if (d / 'stills').exists() else [],
            **notes}
    wj(d / 'TAKE.json', take); print('ok')

def cmd_index():
    idx = {'record_type': 'presenter_index', 'updated_at': now(), 'segments': {}}
    fb = rj(P / 'FALLBACKS.json') if (P / 'FALLBACKS.json').exists() else {'fallbacks': []}
    fbs = {f['segment_id']: f for f in fb.get('fallbacks', [])}
    for tid, t in TAKES.items():
        for sid in t['segment_ids']:
            f = td(tid) / 'final' / f'{sid}.mp4'; v = rj(td(tid) / 'VERIFY.json') if (td(tid) / 'VERIFY.json').exists() else []
            vr = next((x for x in v if x['segment'] == sid), None)
            if sid in fbs: idx['segments'][sid] = {'take_id': tid, 'status': 'fallback', 'fallback': fbs[sid]}
            elif f.exists() and vr and vr['frames_ok'] and vr['sha256'] == sha(f):
                idx['segments'][sid] = {'take_id': tid, 'status': 'done', 'path': str(f.relative_to(R)), 'sha256': vr['sha256'], 'frames': vr['frames']}
            else: idx['segments'][sid] = {'take_id': tid, 'status': 'pending'}
    wj(P / 'INDEX.json', idx); print(json.dumps({k: v['status'] for k, v in idx['segments'].items()}))

if __name__ == '__main__':
    fn = {'cut': cmd_cut, 'native': cmd_native, 'trim': cmd_trim, 'fal-submit': cmd_fal_submit, 'fal-result': cmd_fal_result, 'align': cmd_align, 'conform': cmd_conform, 'verify': cmd_verify, 'stills': cmd_stills, 'take': cmd_take, 'index': cmd_index}[sys.argv[1]]
    fn(*sys.argv[2:])
