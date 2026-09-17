import json, subprocess, hashlib, os, re, math, datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = '/Users/brownmanbrain/GitHub/operator-economy'
B = ROOT + '/blueprint-cinema/experiments/EP009-FULL-BUILD-001'
A = B + '/assembly'
MASTER_REL = 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'
MASTER = ROOT + '/' + MASTER_REL
WT = ROOT + '/operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/word-transcript.json'
OUT = A + '/qa/ep009-full.mp4'
FPS = 24
W, H = 1280, 720
SW, SH = 320, 180

plan = json.load(open(B + '/direction/SHOT-PLAN.json'))
rows = json.load(open(A + '/_tools/sources.json'))
words = json.load(open(WT))['words']
TOTAL = rows[-1]['out'][1]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for ch in iter(lambda: f.read(1 << 20), b''):
            h.update(ch)
    return h.hexdigest()


def tc(frame):
    s = frame / FPS
    return f"{int(s // 60)}:{s % 60:06.3f}"


def font(sz):
    for p in ['/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Helvetica.ttc']:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


ver = {
    'record_type': 'ep009_full_assembly_verification',
    'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'agent-verified, not owner accepted',
}

# ---------------- probe ----------------
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_packets', '-show_entries',
                                         'stream=codec_type,codec_name,width,height,r_frame_rate,nb_read_packets,duration,sample_rate,channels,sample_aspect_ratio,pix_fmt:format=duration',
                                         '-of', 'json', OUT]))
vs = [s for s in pr['streams'] if s['codec_type'] == 'video'][0]
au = [s for s in pr['streams'] if s['codec_type'] == 'audio'][0]
master_dur = plan['master']['duration_seconds']
ver['output'] = {
    'path': 'assembly/qa/ep009-full.mp4', 'sha256': sha(OUT),
    'video': {k: vs.get(k) for k in ['codec_name', 'width', 'height', 'r_frame_rate', 'pix_fmt', 'sample_aspect_ratio', 'nb_read_packets', 'duration']},
    'audio': {k: au.get(k) for k in ['codec_name', 'sample_rate', 'channels', 'duration']},
}
ver['timing'] = {
    'plan_total_frames': TOTAL,
    'encoded_video_frames': int(vs['nb_read_packets']),
    'frames_match_plan': int(vs['nb_read_packets']) == TOTAL,
    'picture_seconds': TOTAL / FPS,
    'master_seconds': master_dur,
    'picture_minus_master_seconds': round(TOTAL / FPS - master_dur, 6),
    'within_one_frame': abs(TOTAL / FPS - master_dur) < 1 / FPS,
    'segments_contiguous': all(a['out'][1] == b['out'][0] for a, b in zip(rows, rows[1:])),
    'segment_count': len(rows),
}

# ---------------- full decode: uniform frames + small signatures ----------------
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', OUT, '-map', '0:v:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=1 << 24)
fsz = W * H * 3
stds = np.zeros(TOTAL + 10, dtype=np.float32)
ranges = np.zeros(TOTAL + 10, dtype=np.float32)
means = np.zeros(TOTAL + 10, dtype=np.float32)
keep = set()
for r in rows:
    f0, f1 = r['out']
    for f in (f0, min(f0 + 12, f1 - 1), f1 - 1):
        keep.add(f)
kept = {}
full = {}
n = 0
while True:
    buf = p.stdout.read(fsz)
    if len(buf) < fsz:
        break
    fr = np.frombuffer(buf, dtype=np.uint8).reshape(H, W, 3)
    g = fr[::4, ::4].astype(np.float32).mean(axis=2)
    stds[n] = g.std()
    lo, hi = np.percentile(g, [0.5, 99.5])
    ranges[n] = hi - lo
    means[n] = g.mean()
    if n in keep:
        kept[n] = fr[::4, ::4].copy()
        full[n] = fr.copy()
    n += 1
p.wait()
decoded = n
uniform = [int(i) for i in np.where(ranges[:decoded] < 2.0)[0]]


def seg_for(frame):
    for r in rows:
        if r['out'][0] <= frame < r['out'][1]:
            return r
    return None


# group uniform frames into runs
runs = []
for f in uniform:
    if runs and f == runs[-1][1] + 1:
        runs[-1][1] = f
    else:
        runs.append([f, f])
uni_runs = []
for a, b in runs:
    r = seg_for(a)
    local = a - r['out'][0]
    uni_runs.append({
        'output_frames_inclusive': [a, b], 'count': b - a + 1, 'timecode': tc(a), 'segment': r['id'], 'lane': r['lane'],
        'segment_local_frames_inclusive': [local, b - r['out'][0]], 'mean_luma': round(float(means[a]), 2),
        'source_path': r['path'], 'source_frames_inclusive': [r['src_start'] + local, r['src_start'] + b - r['out'][0]],
    })
ver['decode'] = {
    'method': 'ffmpeg decode of every frame of the encoded file at 1280x720 RGB, statistics on every 4th pixel; uniform = gray 0.5 to 99.5 percentile range under 2/255',
    'decoded_frames': decoded, 'decode_errors': p.returncode,
    'uniform_frame_count': len(uniform), 'uniform_runs': uni_runs,
}

# ---------------- seams ----------------
os.makedirs(A + '/qa/seams', exist_ok=True)
continuous_pairs = {('seg010', 'seg011'), ('seg064', 'seg065'), ('seg072', 'seg073'), ('seg074', 'seg075')}
model_lanes = {'model', 'evidence', 'screen', 'sting'}
boundary_frames = []
for a, b in zip(rows, rows[1:]):
    boundary_frames += [a['out'][1] - 1, b['out'][0]]
seams = []
for i, (a, b) in enumerate(zip(rows, rows[1:])):
    name = f"{i + 1:02d}-{a['id']}-{b['id']}"
    pa = f'{A}/qa/seams/{name}-a.png'
    pb = f'{A}/qa/seams/{name}-b.png'
    Image.fromarray(full[a['out'][1] - 1]).save(pa)
    Image.fromarray(full[b['out'][0]]).save(pb)
    ia = np.asarray(Image.open(pa).convert('RGB')).astype(np.float32)
    ib = np.asarray(Image.open(pb).convert('RGB')).astype(np.float32)
    d = np.abs(ia - ib)
    mad = float(d.mean())
    pct20 = float((d.mean(axis=2) > 20).mean() * 100)
    fb = b['out'][0]
    fb12 = min(fb + 12, b['out'][1] - 1)
    s_in = float(stds[fb]); s_12 = float(stds[fb12])
    d_in12 = float(np.abs(kept[fb].astype(np.float32) - kept[fb12].astype(np.float32)).mean())
    same_src = a['path'] == b['path'] and a['src_start'] + a['frames'] == b['src_start']
    if same_src:
        kind = 'same-source continuous'
    elif (a['id'], b['id']) in continuous_pairs:
        kind = 'planned continuous (crop change)'
    elif a['lane'] in model_lanes and b['lane'] in model_lanes:
        kind = 'model-to-model handoff across projects'
    else:
        kind = 'lane cut'
    flags = []
    should_be_continuous = kind != 'lane cut'
    if should_be_continuous and a['lane'] in model_lanes and b['lane'] in model_lanes and mad > 20:
        flags.append('model handoff differs by more than 20/255')
    if (a['id'], b['id']) in continuous_pairs and mad > 20:
        flags.append('planned continuous boundary differs by more than 20/255')
    if ranges[fb] < 2.0:
        flags.append('incoming frame uniform (blank)')
    elif s_in < 0.6 * s_12 and d_in12 > 10:
        flags.append('incoming frame possibly half-drawn (much less content than 0.5 s later)')
    seams.append({
        'boundary': name, 'output_frame': fb, 'timecode': tc(fb), 'outgoing': a['id'], 'incoming': b['id'],
        'lanes': [a['lane'], b['lane']], 'kind': kind,
        'diff_mean_abs_rgb_255': round(mad, 2), 'pct_pixels_over_20': round(pct20, 2),
        'incoming_std_frame0': round(s_in, 2), 'incoming_std_frame12': round(s_12, 2), 'incoming_frame0_vs_frame12_diff': round(d_in12, 2),
        'png_a': f'assembly/qa/seams/{name}-a.png', 'png_b': f'assembly/qa/seams/{name}-b.png',
        'flags': flags,
    })
ver['seams'] = {
    'method': 'Last outgoing and first incoming frames taken by frame index from the full decode of the encoded ep009-full.mp4; difference = mean absolute RGB difference in 0-255 at 1280x720; half-drawn heuristic = incoming frame gray std under 0.6x the std 12 frames later with more than 10/255 change.',
    'count': len(seams), 'flagged': [s for s in seams if s['flags']], 'all': seams,
}

# ---------------- audio ----------------
def dec(path, ch):
    return np.frombuffer(subprocess.check_output(['ffmpeg', '-v', 'error', '-i', path, '-map', '0:a:0', '-ac', str(ch), '-f', 'f32le', '-']), dtype=np.float32)

m = dec(MASTER, 1).astype(np.float64)
prog = dec(OUT, 2).reshape(-1, 2).astype(np.float64)
db = lambda x: 20 * math.log10(math.sqrt(float(np.mean(x * x))) + 1e-15)
N = len(m)
L, R = prog[:N, 0], prog[:N, 1]


def corr(x, y):
    return float(np.dot(x, y) / math.sqrt(float(np.dot(x, x) * np.dot(y, y)) + 1e-20))

windows = []
starts = np.linspace(5, master_dur - 15, 20)
for s in starts:
    a0 = int(round(s * 48000)); a1 = a0 + 10 * 48000
    mm = m[a0:a1]
    windows.append({'start_s': round(float(s), 3), 'len_s': 10,
                    'corr_L': round(corr(L[a0:a1], mm), 6), 'corr_R': round(corr(R[a0:a1], mm), 6),
                    'rms_L_minus_master_db': round(db(L[a0:a1]) - db(mm), 3), 'rms_R_minus_master_db': round(db(R[a0:a1]) - db(mm), 3),
                    'master_rms_dbfs': round(db(mm), 1)})
tail = prog[N:]
ver['audio'] = {
    'method': 'Program audio decoded from ep009-full.mp4 (48 kHz stereo float); master decoded from the WAV; zero-lag Pearson correlation and RMS difference per channel in 20 evenly spaced 10 s windows and over the full master length.',
    'master_sha256': sha(MASTER), 'master_sha256_expected': plan['master']['sha256'],
    'master_samples': N, 'program_samples': int(prog.shape[0]), 'expected_program_samples': TOTAL * 2000,
    'full_length': {'corr_L': round(corr(L, m), 6), 'corr_R': round(corr(R, m), 6),
                    'rms_L_minus_master_db': round(db(L) - db(m), 3), 'rms_R_minus_master_db': round(db(R) - db(m), 3),
                    'L_minus_R_max_abs': float(np.max(np.abs(L - R)))},
    'tail_after_master': {'samples': int(tail.shape[0]), 'max_abs': float(np.max(np.abs(tail))) if tail.size else 0.0},
    'windows': windows,
    'min_window_corr': min(min(w['corr_L'], w['corr_R']) for w in windows),
    'max_abs_window_rms_diff_db': max(max(abs(w['rms_L_minus_master_db']), abs(w['rms_R_minus_master_db'])) for w in windows),
}
del prog, L, R

# ---------------- loudness ----------------
def loud(path):
    e = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-map', '0:a:0', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    summ = e[e.rfind('Summary:'):]
    g = lambda pat: float(re.search(pat, summ, re.S).group(1))
    return {'integrated_lufs': g(r'I:\s+(-?[\d.]+) LUFS'), 'loudness_range_lu': g(r'LRA:\s+(-?[\d.]+) LU'), 'true_peak_dbtp': g(r'Peak:\s+(-?[\d.]+) dBFS')}

ver['loudness'] = {'method': 'ffmpeg ebur128 peak=true', 'program': loud(OUT), 'master_mono_reference': loud(MASTER),
                   'note': 'Recorded only; no normalization applied. Mono master measures about 3 LU lower than its unity stereo upmix under BS.1770 channel summing.'}

# ---------------- presenter sync strips ----------------
os.makedirs(A + '/qa/sync', exist_ok=True)
sync = []
fnt = font(18)
for take, sid in [('P01', 'seg009'), ('P03', 'seg019'), ('P05', 'seg028')]:
    r = [x for x in rows if x['id'] == sid][0]
    w0 = [w for w in words if w['start'] >= r['master_in']][0]
    near = [w for w in words if w0['start'] - 0.01 <= w['start'] < w0['start'] + 2.0]
    t0 = w0['start'] - 2.0
    f_start = int(math.floor(t0 * FPS)); f_end = int(math.floor((w0['start'] + 2.0) * FPS))
    frames = list(range(f_start + (f_start % 2), f_end, 2))
    d = f"{A}/qa/sync/{take}-{sid}-first-word-{w0['w_id']}-{re.sub(r'[^A-Za-z]', '', w0['token'])}-onset-{w0['start']:.3f}s"
    os.makedirs(d, exist_ok=True)
    for fn in os.listdir(d):
        os.remove(os.path.join(d, fn))
    subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-i', OUT, '-map', '0:v:0', '-vf', f"trim=start_frame={frames[0]}:end_frame={frames[-1] + 1},select='not(mod(n\\,2))'", '-fps_mode', 'passthrough', d + '/tmp%03d.png'])
    tmp = sorted(f for f in os.listdir(d) if f.startswith('tmp'))
    tiles = []
    for f, fn in zip(frames, tmp):
        t = f / FPS
        rel = int(round((t - w0['start']) * 1000))
        active = [w for w in words if w['start'] <= t + 1 / 48 and w['end'] > t - 1 / 48]
        wlab = '_'.join(re.sub(r'[^A-Za-z0-9]', '', w['token']) for w in active) or 'silence'
        newn = f"f{f:05d}-t{t:08.3f}-rel{rel:+05d}ms-{wlab}.png"
        os.replace(os.path.join(d, fn), os.path.join(d, newn))
        tiles.append((newn, t, rel, wlab))
    # annotated contact strip, face-area crop-free at 320x180
    cols = 8
    rws = math.ceil(len(tiles) / cols)
    sheet = Image.new('RGB', (cols * 320, rws * 206), (20, 20, 20))
    dr = ImageDraw.Draw(sheet)
    for k, (fn, t, rel, wlab) in enumerate(tiles):
        im = Image.open(os.path.join(d, fn)).convert('RGB').resize((320, 180))
        x, y = (k % cols) * 320, (k // cols) * 206
        sheet.paste(im, (x, y))
        col = (255, 220, 80) if abs(rel) <= 42 else (230, 230, 230)
        dr.text((x + 4, y + 182), f"{t:.3f}s {rel:+d}ms {wlab[:14]}", fill=col, font=fnt)
    strip = f"{d}.png"
    sheet.save(strip)
    clip = f"{d}.mp4"
    subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-t', '4', '-i', OUT, '-c:v', 'libx264', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', clip])
    json.dump({'take': take, 'segment': sid, 'segment_master_in': r['master_in'], 'first_word': w0, 'words_next_2s': near,
               'strip_frames_12fps': [x[0] for x in tiles]}, open(f'{d}/WORDS.json', 'w'), indent=1)
    sync.append({'take': take, 'segment': sid, 'first_word': w0, 'window_s': [round(t0, 3), round(t0 + 4, 3)],
                 'frames_dir': os.path.relpath(d, B + '/..').replace('EP009-FULL-BUILD-001/', 'blueprint-cinema/experiments/EP009-FULL-BUILD-001/', 1) if False else 'assembly/qa/sync/' + os.path.basename(d),
                 'strip': 'assembly/qa/sync/' + os.path.basename(strip), 'clip_with_sound': 'assembly/qa/sync/' + os.path.basename(clip),
                 'judged': 'not judged by agent; reviewer compares mouth-opening onset to word onset (tile label rel ms is frame time minus first-word start)'})
ver['presenter_sync_risk'] = {'reason': 'Fal restorations placed audio 0.39 to 0.53 s late in P01, P03, P05 (presenter INDEX assembler_notes); picture follows each file\'s own audio.', 'strips': sync}

json.dump(ver, open(A + '/_tools/verify_partial.json', 'w'), indent=1)
print(json.dumps({k: ver[k] for k in ['timing']}, indent=1))
print('uniform runs', ver['decode']['uniform_runs'])
print('flagged seams', json.dumps(ver['seams']['flagged'], indent=1))
print('audio', json.dumps({k: ver['audio'][k] for k in ['full_length', 'min_window_corr', 'max_abs_window_rms_diff_db', 'tail_after_master', 'program_samples', 'expected_program_samples']}, indent=1))
print('loud', ver['loudness'])
