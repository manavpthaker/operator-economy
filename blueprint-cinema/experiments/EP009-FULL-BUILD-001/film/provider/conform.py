"""Contact sheets and exact-frame conform for EP009 film takes.
contact <take>                      -> <take>/contact.jpg (4 fps, labelled with source frame and seconds)
frames <take> <sec> [<sec> ...]     -> <take>/frames/src_<sec>.png full-res stills for inspection
conform <take> <seg> <src_start_s>  -> <take>/final/<seg>.mp4 (exact frames, 1280x720 24 fps, master excerpt stereo)
lastframe <take> <src_s> <out.png>  -> 1920x1080 still at that source time (next take start frame)
"""
import hashlib, json, subprocess, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent; FILM = BASE.parent; BUILD = FILM.parent
REPO = next(p for p in BASE.parents if (p / '.agents').is_dir())
MASTER = REPO / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'
PLAN = json.loads((BUILD / 'direction/SHOT-PLAN.json').read_text())
sh = lambda *a: subprocess.run(a, check=True, capture_output=True, text=True).stdout
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

def probe(p):
    d = json.loads(sh('ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries', 'stream=width,height,r_frame_rate,nb_read_frames,duration', '-of', 'json', str(p)))['streams'][0]
    n, dd = d['r_frame_rate'].split('/'); d['fps'] = float(n) / float(dd); return d

def seg(sid): return next(s for s in PLAN['segments'] if s['id'] == sid)

def contact(take):
    raw = FILM / take / 'raw.mp4'; fps = probe(raw)['fps']
    vf = "fps=4,scale=384:216,tile=8x4:padding=4"  # tile i = source second i/4, row-major
    sh('ffmpeg', '-loglevel', 'error', '-y', '-i', str(raw), '-vf', vf, '-frames:v', '1', str(FILM / take / 'contact.jpg'))
    print(json.dumps(probe(raw)))

def frames(take, secs):
    out = FILM / take / 'frames'; out.mkdir(exist_ok=True)
    for s in secs:
        sh('ffmpeg', '-loglevel', 'error', '-y', '-ss', s, '-i', str(FILM / take / 'raw.mp4'), '-frames:v', '1', '-vf', 'scale=1280:720', str(out / f'src_{s}.jpg'))

def lastframe(take, s, outp):
    sh('ffmpeg', '-loglevel', 'error', '-y', '-ss', s, '-i', str(FILM / take / 'raw.mp4'), '-frames:v', '1', '-vf', 'scale=1920:1080:flags=lanczos', str(outp))
    print(sha(outp))

def conform_frames(take, sid, spec):
    """spec like '78-170,169-147,148-191' (inclusive, descending ranges play in reverse, no speed change)."""
    import shutil, tempfile
    idx = []
    for part in spec.split(','):
        a, b = map(int, part.split('-'))
        idx += list(range(a, b + 1)) if a <= b else list(range(a, b - 1, -1))
    s = seg(sid); n = s['frames'][1] - s['frames'][0]
    assert len(idx) == n, f'spec gives {len(idx)} frames, segment needs {n}'
    tmp = Path(tempfile.mkdtemp(dir=FILM / take))
    sh('ffmpeg', '-loglevel', 'error', '-i', str(FILM / take / 'raw.mp4'), '-vsync', '0', str(tmp / 'f%04d.png'))
    seqd = tmp / 'seq'; seqd.mkdir()
    for i, k in enumerate(idx): (seqd / f's{i:04d}.png').symlink_to(tmp / f'f{k + 1:04d}.png')
    seqmp4 = FILM / take / 'seq.tmp.mp4'
    sh('ffmpeg', '-loglevel', 'error', '-y', '-framerate', '24', '-i', str(seqd / 's%04d.png'), '-c:v', 'libx264', '-crf', '8', '-pix_fmt', 'yuv420p', str(seqmp4))
    shutil.rmtree(tmp)
    res = conform(take, sid, '0', raw_override=seqmp4)
    seqmp4.unlink()
    res['source_window'] = {"frame_spec": spec, "native_fps": 24.0, "speed_change": False, "reversed_ranges": [p for p in spec.split(',') if int(p.split('-')[0]) > int(p.split('-')[1])]}
    (FILM / take / f'CONFORM-{sid}.json').write_text(json.dumps(res, indent=2) + '\n')
    print(json.dumps(res['source_window']))

def conform(take, sid, src_start, raw_override=None):
    s = seg(sid); f0, f1 = s['frames']; n = f1 - f0
    mi, mo = s['master_in'], s['master_out']
    a0, a1 = round(mi * 48000), round(mo * 48000)
    raw = raw_override or (FILM / take / 'raw.mp4'); info = probe(raw)
    src_start = float(src_start); need = n / 24
    assert src_start + need <= float(info['duration']) + 1e-3, f'window {src_start}+{need} exceeds source {info["duration"]}'
    outd = FILM / take / 'final'; outd.mkdir(exist_ok=True); out = outd / f'{sid}.mp4'
    vf = f"trim=start={src_start},setpts=PTS-STARTPTS,fps=24,scale=1280:720:flags=lanczos,setsar=1,trim=end_frame={n},setpts=PTS-STARTPTS"
    af = f"atrim=start_sample={a0}:end_sample={a1},asetpts=N/SR/TB,pan=stereo|c0=c0|c1=c0"
    sh('ffmpeg', '-loglevel', 'error', '-y', '-i', str(raw), '-i', str(MASTER), '-filter_complex', f'[0:v]{vf}[v];[1:a]{af}[a]',
       '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '24',
       '-c:a', 'pcm_s16le', '-ar', '48000', '-movflags', '+faststart', str(out.with_suffix('.tmp.mov')))
    # mp4 with PCM is poorly supported; use AAC at high bitrate only if needed. Keep PCM in mov, then remux to mp4 with aac 320k.
    sh('ffmpeg', '-loglevel', 'error', '-y', '-i', str(out.with_suffix('.tmp.mov')), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-movflags', '+faststart', str(out))
    tmp = out.with_suffix('.tmp.mov')
    # checks
    vinfo = probe(out)
    ainfo = json.loads(sh('ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=sample_rate,channels,duration', '-of', 'json', str(out)))['streams'][0]
    # audio correlation vs master excerpt (PCM intermediate is sample exact; aac checked by correlation)
    import array, wave
    def pcm(path, extra):
        return sh('ffmpeg', '-loglevel', 'error', '-i', str(path), *extra, '-f', 's16le', '-ac', '1', '-ar', '48000', '-')
    def corr(x, y):
        m = min(len(x), len(y)); x = x[:m]; y = y[:m]
        sx = sum(x) / m; sy = sum(y) / m
        num = sum((a - sx) * (b - sy) for a, b in zip(x, y))
        den = (sum((a - sx) ** 2 for a in x) * sum((b - sy) ** 2 for b in y)) ** 0.5
        return num / den if den else 0.0
    ref = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', str(MASTER), '-af', f'atrim=start_sample={a0}:end_sample={a1}', '-f', 's16le', '-ac', '1', '-'], check=True, capture_output=True).stdout
    got_mov = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', str(tmp), '-map', '0:a', '-af', 'pan=mono|c0=c0', '-f', 's16le', '-'], check=True, capture_output=True).stdout
    got_mp4 = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', str(out), '-map', '0:a', '-af', 'pan=mono|c0=c0', '-f', 's16le', '-'], check=True, capture_output=True).stdout
    r = array.array('h', ref); g1 = array.array('h', got_mov); g2 = array.array('h', got_mp4)
    pcm_exact = (bytes(r) == bytes(g1[:len(r)])) and len(g1) >= len(r)
    step = 4
    c = corr(r[::step], g2[:len(r)][::step])
    # uniform frames
    stats = sh('ffmpeg', '-loglevel', 'error', '-i', str(out), '-vf', 'signalstats,metadata=print:key=lavfi.signalstats.YMAX:file=-', '-f', 'null', '-')
    ymax = [float(l.split('=')[1]) for l in stats.splitlines() if 'YMAX' in l]
    stats2 = sh('ffmpeg', '-loglevel', 'error', '-i', str(out), '-vf', 'signalstats,metadata=print:key=lavfi.signalstats.YMIN:file=-', '-f', 'null', '-')
    ymin = [float(l.split('=')[1]) for l in stats2.splitlines() if 'YMIN' in l]
    uniform = sum(1 for a, b in zip(ymax, ymin) if a - b < 8)
    tmp.unlink()
    res = {"segment_id": sid, "path": str(out.relative_to(REPO)), "sha256": sha(out), "frames_expected": n, "frames": int(vinfo['nb_read_frames']),
           "frames_ok": int(vinfo['nb_read_frames']) == n, "size": [vinfo['width'], vinfo['height']], "fps": vinfo['fps'],
           "audio": {"sample_rate": int(ainfo['sample_rate']), "channels": ainfo['channels'], "master_samples": [a0, a1],
                     "pcm_intermediate_sample_exact": pcm_exact, "aac_corr_zero_lag_vs_master_excerpt": round(c, 5)},
           "uniform_frames": uniform,
           "source_window": {"source_in_s": src_start, "source_out_s": round(src_start + need, 4), "native_fps": info['fps'], "speed_change": False},
           "master_in": mi, "master_out": mo, "segment_frames": [f0, f1]}
    (FILM / take / f'CONFORM-{sid}.json').write_text(json.dumps(res, indent=2) + '\n')
    print(json.dumps(res))
    return res

if __name__ == '__main__':
    op = sys.argv[1]
    if op == 'contact': contact(sys.argv[2])
    elif op == 'frames': frames(sys.argv[2], sys.argv[3:])
    elif op == 'conform': conform(sys.argv[2], sys.argv[3], sys.argv[4])
    elif op == 'conform_frames': conform_frames(sys.argv[2], sys.argv[3], sys.argv[4])
    elif op == 'lastframe': lastframe(sys.argv[2], sys.argv[3], sys.argv[4])
