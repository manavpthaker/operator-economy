"""EP009 fix round 1, edit lane: re-cut presenter and film clips from existing sources.
No generation, no provider calls. Picture is re-windowed and re-cropped; audio is always the
sample-exact master excerpt upmixed at unity. Run with a python that has numpy.

  python edit_r1.py render            # render every planned clip (keeps r0 copies in <take>/qa/)
  python edit_r1.py render seg009     # one clip
  python edit_r1.py verify            # checks + stills + EDIT-R1.json per clip
"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parents[1]
B = P.parent
F = B / 'film'
R = next(x for x in P.parents if (x / '.agents').is_dir())
MASTER = R / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'
SHOT = json.loads((B / 'direction/SHOT-PLAN.json').read_text())
SEGS = {s['id']: s for s in SHOT['segments']}
TAKES = {t['take_id']: t for t in SHOT['presenter_takes']}
SR = 48000
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
fr = lambda t: int(round(t * 24))
def run(cmd): return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
def nframes(sid):
    s = SEGS[sid]
    return (29607 if s['master_out'] == 1233.602 else fr(s['master_out'])) - fr(s['master_in'])

# crop sizes in the 1920x1080 source, centred on the take's median nose x (face mesh, 2 fps sample)
NOSE = {'P01': 943, 'P02': 944, 'P03': 942, 'P04': 942, 'P05': 934, 'P06': 946, 'P07': 957, 'P08': 941,
        'P09': 930, 'P10': 952, 'P11': 941, 'P12': 941, 'P13': 957}
def rect(tid, size):
    if size == 'W': return None
    w, h, y = {'M': (1536, 864, 0), 'C': (1280, 720, 0), 'C2': (1152, 648, 24)}[size]
    x = max(0, min(1920 - w, NOSE[tid] - w // 2))
    return [w, h, x, y]

# Presenter plan: segment -> (take, restored start frame, [(segment_frame_from, size), ...]).
# The start frame is ALIGNMENT.json start_frame except P01 (A-07 picture slip, see CROP-PLAN-R1.md).
PRES = {
    'seg009': ('P01', 7, [(0, 'W')]),
    'seg012': ('P02', None, [(0, 'C'), (152, 'W')]),
    'seg019': ('P03', None, [(0, 'C'), (38, 'W'), (333, 'C')]),
    'seg021': ('P04', None, [(0, 'W'), (96, 'C'), (170, 'W')]),
    'seg028': ('P05', None, [(0, 'M')]),
    'seg035': ('P06', None, [(0, 'C'), (100, 'W')]),
    'seg037': ('P07', None, [(0, 'M'), (108, 'W')]),
    'seg044': ('P08', None, [(0, 'M'), (230, 'C2'), (350, 'W')]),
    'seg055': ('P09', None, [(0, 'M')]),
    'seg059': ('P10', None, [(0, 'W'), (33, 'C')]),
    'seg071': ('P11', None, [(0, 'W'), (30, 'C'), (97, 'W'), (449, 'C')]),
    'seg074': ('P13', None, [(0, 'W')]),
}
# Film plan: segment -> (take folder, [(segment_frame_from, source_frame_start, rect|None), ...]); source runs continuously.
FILM = {
    'seg002': ('F02-r2', [(0, 0, None), (76, 76, [1600, 900, 320, 90])]),
    'seg003': ('F03', [(0, 0, None)]),
    'seg049': ('F07', [(0, 20, [1280, 720, 640, 360])]),
    'seg067': ('F09', [(0, 108, [1632, 918, 0, 60])]),
}

def vf_crop(r):
    return 'scale=1280:720:flags=lanczos' if r is None else f'crop={r[0]}:{r[1]}:{r[2]}:{r[3]},scale=1280:720:flags=lanczos'

def encode(src, sid, parts, out, crf):
    """parts: [(seg_from, seg_to, src_from, rect)]"""
    s = SEGS[sid]; n = nframes(sid)
    chains = [f'[0:v]split={len(parts)}' + ''.join(f'[s{i}]' for i in range(len(parts))) if len(parts) > 1 else '[0:v]null[s0]']
    for i, (a, e, sa, r) in enumerate(parts):
        chains.append(f'[s{i}]trim=start_frame={sa}:end_frame={sa + e - a},setpts=PTS-STARTPTS,{vf_crop(r)},fps=24,setsar=1,format=yuv420p[v{i}]')
    chains.append(''.join(f'[v{i}]' for i in range(len(parts))) + f'concat=n={len(parts)}:v=1:a=0[vo]' if len(parts) > 1 else '[v0]null[vo]')
    s0, s1 = int(round(s['master_in'] * SR)), int(round(s['master_out'] * SR))
    chains.append(f'[1:a]atrim=start_sample={s0}:end_sample={s1},asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0[ao]')
    out.parent.mkdir(parents=True, exist_ok=True)
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(src), '-i', str(MASTER), '-filter_complex', ';'.join(chains), '-map', '[vo]', '-map', '[ao]',
         '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow', '-r', '24', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', str(out)])

def keep_r0(out):
    q = out.parents[1] / 'qa' / f'{out.stem}.r0.mp4'
    if not q.exists():
        q.parent.mkdir(exist_ok=True); shutil.copy2(out, q)
    return q

def plan_parts(sid):
    n = nframes(sid)
    if sid in PRES:
        tid, st, ranges = PRES[sid]
        al = json.loads((P / tid / 'ALIGNMENT.json').read_text())
        start = al['start_frame'] if st is None else st
        take0 = fr(TAKES[tid]['master_in']); f0 = fr(SEGS[sid]['master_in']) - take0
        parts = []
        for i, (a, size) in enumerate(ranges):
            e = ranges[i + 1][0] if i + 1 < len(ranges) else n
            parts.append((a, e, start + f0 + a, rect(tid, size), size))
        assert start + f0 + n <= int(al['probe']['nb_read_frames'])
        return P / tid / 'restored.mp4', P / tid / 'final' / f'{sid}.mp4', parts, 16, {'take': tid, 'start_frame': start, 'alignment_start_frame': al['start_frame']}
    take, ranges = FILM[sid]; parts = []
    for i, (a, sa, r) in enumerate(ranges):
        e = ranges[i + 1][0] if i + 1 < len(ranges) else n
        parts.append((a, e, sa, r, 'crop' if r else 'full'))
    assert parts[-1][2] + n - parts[-1][0] <= 193
    return F / take / 'raw.mp4', F / take / 'final' / f'{sid}.mp4', parts, 16, {'take': take}

def cmd_render(only=None):
    for sid in list(PRES) + list(FILM):
        if only and sid != only: continue
        src, out, parts, crf, meta = plan_parts(sid)
        if out.exists(): keep_r0(out)
        encode(src, sid, [(a, e, sa, r) for a, e, sa, r, _ in parts], out, crf)
        print(sid, 'rendered', out.relative_to(R))

def pcm(path, ch=1):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'], check=True, capture_output=True).stdout, '<f4').astype(np.float64)
    return a.reshape(-1, ch) if ch > 1 else a

def cmd_verify(only=None):
    for sid in list(PRES) + list(FILM):
        if only and sid != only: continue
        src, out, parts, crf, meta = plan_parts(sid); s = SEGS[sid]; n = nframes(sid)
        v = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries', 'stream=width,height,r_frame_rate,nb_read_frames', '-of', 'json', str(out)]))['streams'][0]
        a = json.loads(run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=channels,sample_rate', '-of', 'json', str(out)]))['streams'][0]
        s0, s1 = int(round(s['master_in'] * SR)), int(round(s['master_out'] * SR))
        m = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(MASTER), '-af', f'atrim=start_sample={s0}:end_sample={s1}', '-ac', '1', '-f', 'f32le', '-'], check=True, capture_output=True).stdout, '<f4').astype(np.float64)
        o = pcm(out, 2); k = min(len(m), len(o))
        corr = [float(np.dot(m[:k], o[:k, c]) / (np.linalg.norm(m[:k]) * np.linalg.norm(o[:k, c]))) for c in (0, 1)]
        ys = run(['ffmpeg', '-v', 'error', '-i', str(out), '-vf', 'signalstats,metadata=print:file=-', '-f', 'null', '-'])
        ymax = [float(l.split('=')[1]) for l in ys.splitlines() if 'YMAX=' in l]; ymin = [float(l.split('=')[1]) for l in ys.splitlines() if 'YMIN=' in l]
        uniform = sum(1 for x, y in zip(ymax, ymin) if x - y < 8)
        sd = out.parents[1] / 'qa' / 'stills-r1'; sd.mkdir(parents=True, exist_ok=True); stills = []
        picks = sorted({0, n - 1} | {p[0] for p in parts} | {max(0, p[0] - 1) for p in parts} | {(p[0] + p[1]) // 2 for p in parts})
        for f in picks:
            sp = sd / f'{sid}-f{f:04d}-m{s["master_in"] + f / 24:.3f}.png'
            run(['ffmpeg', '-y', '-v', 'error', '-i', str(out), '-vf', f'select=eq(n\\,{f})', '-frames:v', '1', str(sp)]); stills.append(str(sp.relative_to(R)))
        rec = {'segment': sid, **meta, 'path': str(out.relative_to(R)), 'sha256': sha(out), 'frames': int(v['nb_read_frames']), 'frames_expected': n,
               'frames_ok': int(v['nb_read_frames']) == n, 'size': [v['width'], v['height']], 'fps': v['r_frame_rate'],
               'audio': {'channels': a['channels'], 'sample_rate': a['sample_rate'], 'zero_lag_corr_lr': [round(c, 5) for c in corr], 'len_diff_samples': len(o) - len(m)},
               'uniform_frames': uniform, 'source': str(src.relative_to(R)), 'source_sha256': sha(src),
               'parts': [{'segment_frames': [p[0], p[1]], 'source_frames': [p[2], p[2] + p[1] - p[0]], 'crop_1920': p[3], 'size': p[4],
                          'master': [round(s['master_in'] + p[0] / 24, 3), round(s['master_in'] + p[1] / 24, 3)]} for p in parts],
               'r0': str((out.parents[1] / 'qa' / f'{out.stem}.r0.mp4').relative_to(R)), 'stills': stills}
        (out.parents[1] / f'EDIT-R1-{sid}.json').write_text(json.dumps(rec, indent=2) + '\n')
        print(json.dumps({k: rec[k] for k in ['segment', 'frames_ok', 'uniform_frames', 'audio']}))

if __name__ == '__main__':
    {'render': cmd_render, 'verify': cmd_verify}[sys.argv[1]](*sys.argv[2:])
