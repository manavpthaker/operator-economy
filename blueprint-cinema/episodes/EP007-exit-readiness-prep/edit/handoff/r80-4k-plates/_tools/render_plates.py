#!/usr/bin/env python3
"""EP007 R80: re-render every R79 leaf at 4K, keep only a 1920x1080 plate per leaf.

Disk-constrained serial driver (owner event ep007-finishing-4k-rerender-v1):
  per job: disk guard -> scratch copy of the HyperFrames project (repo untouched) ->
  4K render -> ffmpeg cut of each leaf range to a 1920x1080 H.264 plate -> delete the
  4K render and scratch copy -> verify plate against R79 (720p SSIM/PSNR + 1-frame shift).
Media leaves are rebuilt from the highest-resolution original directly at 1920x1080.

Usage: render_plates.py [--only JOB ...] [--list] [--crf N] [--force]
"""
import argparse, datetime, hashlib, json, os, pathlib, re, shutil, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
PLATE_ROOT = HERE.parent
REPO = HERE.parents[6]
EXP = REPO / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003'
REV = EXP / 'hyperframes/reviews'
DEL = REPO / 'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables'
R79 = EXP / 'assembly/r79-full-conform/qa/ep007-r79-full-review.mp4'
R79_SHA = 'adff0911728de87f5388fbbdaee4d288a077e3b18530c6528d25465eb88e6671'
R79_FRAMES = 27241
SCRATCH = pathlib.Path(os.environ.get('R80_SCRATCH', '/private/tmp/claude-501/-Users-brownmanbrain-GitHub-operator-economy/a41aa8bb-cc59-4eab-9ffd-21e9735a6ca3/scratchpad/r80work'))
OUT = pathlib.Path('/Users/brownmanbrain/Movies/OE/EP007-plates-1080')
MANIFEST = PLATE_ROOT / 'PLATES-MANIFEST.json'
MIN_FREE_GB = 4.0
CRF_4K = 12          # 4K intermediate only (deleted right after the cut)
PLATE_CRF = 14
SSIM_MEAN_MIN, SSIM_FRAME_MIN = 0.985, 0.95

# ---------------------------------------------------------------- job table
def hf(job, project, ver, plates, **kw):
    return dict(id=job, kind='hf', project=project, ver=ver, plates=plates, **kw)
def media(job, src, a, b, frames, **kw):
    return dict(id=job, kind='media', src=src, plates=[(a, b, frames[0])], src_end=frames[1], **kw)

S14_DEV_FLAG = 'S14 projects: package.json pins 0.8.36 but the locked renders carry hyperframes_version=0.0.0-dev (local dev build); rendered with closest published pin 0.8.36'
KLING_FLAG = 'source is 1916x1080 Kling native (below 4K); horizontal stretch x1.0021 to 1920, as in review builds'
PRES_FLAG = 'presenter source is 1920x1080 (below 4K); plate is native 1080p, no upscale'

JOBS = [
    # ---------------- PREFIX [0,13376)
    hf('r36-buyer-demand', REV/'r36-buyer-demand', '0.8.34', [(0, 5872, 0)],
       flags=['pinned 0.8.34 (package.json devDependency, no lockfile); original locked render used quality draft',
              'embedded presenter/Kling media are 1920x1080 / 1916x1080 (below 4K); punch-ins enlarge 1080p sources']),
    hf('r39-question-performance', REV/'r39-question-performance', '0.8.34', [(5872, 6408, 5872)],
       patch='r39_question_fullres',
       flags=['pinned 0.8.34; whole 293.6 s composition rendered (no frame-range flag), only [5872,6408) kept',
              'scratch copy: public/media/question-r39-aligned.mp4 (1280x720 proxy) replaced by a 1920x1080 re-conform of provider/restoration/restored.mp4 frames 10..136 (PICTURE-CONFORM.json recipe without the downscale)',
              'owner exception inherited: R39 callback/performance verdict unspecified; R39 animation under unresolved revise']),
    hf('r46-revenue-machine', REV/'r46-revenue-machine', '0.8.36', [(6408, 6895, 0)]),
    hf('r47-transfer-criterion', REV/'r47-transfer-criterion', '0.8.36', [(6895, 7164, 0)],
       flags=[PRES_FLAG + ' (embedded restored-source.mp4)', 'restored-source.mp4 has sparse keyframes (seek risk)',
              'owner exception inherited: R47 performance has no owner verdict']),
    hf('r48-relationships', REV/'r48-relationships', '0.8.36', [(7164, 7379, 0)]),
    hf('r49-concentration', REV/'r49-concentration', '0.8.36', [(7379, 7542, 0)]),
    hf('r50-records', REV/'r50-records', '0.8.36', [(7542, 7744, 0)],
       flags=['index.html is a rebuild of a lost original (event r50-records-source-rebuilt-v1): up to 1.23/255 drift vs accepted bytes']),
    hf('r51-underlying', REV/'r51-underlying', '0.8.36', [(7744, 7983, 0)]),
    media('r52-handshake-v5', REV/'r52-walkout/provider/handshake-v5/native.mp4', 7983, 8131, (0, 148), stretch=True, flags=[KLING_FLAG]),
    media('r52-walkout', REV/'r52-walkout/provider/walkout/native.mp4', 8131, 8163, (112, 144), stretch=True, flags=[KLING_FLAG]),
    media('r53-presenter-a', REV/'r53-s10/provider/presenter-a/restoration/restored.mp4', 8163, 8351, (15, 203), flags=[PRES_FLAG, '10-bit source converted to 8-bit yuv420p']),
    hf('r53-s10-evidence', REV/'r53-s10-evidence', '0.8.36', [(8351, 8897, 0)]),
    media('r53-presenter-c-v2', REV/'r53-s10/provider/presenter-c-v2/resync-shift/restored.mp4', 8897, 9104, (12, 219), flags=[PRES_FLAG]),
    hf('r54-s11a', REV/'r54-s11a', '0.8.36', [(9104, 9749, 0)]),
    hf('r54-s11b', REV/'r54-s11b', '0.8.36', [(9749, 10260, 0)]),
    hf('r54-s11cd', REV/'r54-s11cd', '0.8.36', [(10260, 10824, 0)]),
    media('r55-s12a-pickup', REV/'r55-s12a-pickup/provider/restoration/restored.mp4', 10824, 11089, (0, 265), flags=[PRES_FLAG, '10-bit source converted to 8-bit yuv420p']),
    hf('r55-s12bc', REV/'r55-s12bc', '0.8.36', [(11089, 11976, 0)]),
    hf('r55-s12d', REV/'r55-s12d', '0.8.36', [(11976, 12481, 0)]),
    hf('r57-s13ab', REV/'r57-s13ab', '0.8.36', [(12481, 12791, 0)]),
    hf('r57-s13cd', REV/'r57-s13cd', '0.8.36', [(12791, 13376, 0)]),
    # ---------------- S14-S26 [13376,27241)
    media('s14-presenter-a', REV/'r59-s14-presenter/provider/a/restoration/restored.mp4', 13376, 13694, (1, 319), flags=[PRES_FLAG]),
    hf('r59-s14b', REV/'r59-s14b', '0.8.36', [(13694, 14102, 0)], flags=[S14_DEV_FLAG, 'locked look includes grey-label defect (r59-s14-accent-label-finding-v1); reproduced, not fixed']),
    media('s14-presenter-c1', REV/'r59-s14-presenter/provider/c1/restoration/restored.mp4', 14102, 14375, (4, 277), flags=[PRES_FLAG]),
    hf('r59-s14c2', REV/'r59-s14c2', '0.8.36', [(14375, 14582, 0)], flags=[S14_DEV_FLAG, 'locked look includes grey-label defect; reproduced, not fixed']),
    media('s14-presenter-c3', REV/'r59-s14-presenter/provider/c3/restoration/restored.mp4', 14582, 14858, (0, 276), flags=[PRES_FLAG]),
    hf('r59-s14d', REV/'r59-s14d', '0.8.36', [(14858, 15146, 0)], flags=[S14_DEV_FLAG, 'locked look includes grey-label defect; reproduced, not fixed']),
    hf('r60-s15-p1', REV/'r60-s15-p1', '0.8.36', [(15146, 15746, 0)], flags=['r60 render version never logged; pin 0.8.36 used']),
    hf('r60-s15-p2', REV/'r60-s15-p2', '0.8.36', [(15746, 15754, 0), (16038, 16514, 292)],
       flags=['r60 render version never logged; pin 0.8.36 used', 'R79 16038 was an R78 seam-hold PNG of this leaf frame 292; plate uses the 4K render frame 292 directly']),
    hf('r78-s15-mobile', DEL/'R78-TOOL-INSERT-MOBILE-BUILD/projects/s15-mobile', '0.8.50', [(15754, 15826, 608), (15826, 16038, 680)],
       patch='r78_captures', captures='S15', frame_format='png',
       flags=['ChatGPT screen recording raw 3840x1946 VFR; used window 2000x1036 raw px -> 1.82x upscale into the 4K capture box (below 4K)',
              'R77 crop+fps24 and R78 moving crop recomputed from RAW in one lossless pipe (skips the two crf16 generations); capture scaled lanczos to the 4K content box 3642x1884']),
    hf('r61-s16-p1', REV/'r61-s16-p1', '0.8.36', [(16514, 16727, 0), ('hold', 17380, 17390, 866)],
       flags=['r61 render version never logged; pin 0.8.36 used',
              'return still [17380,17390) = this leaf frame 866 held 10 frames; R79 17380-17381 were renderer boundary composites (~33.6 dB vs still)']),
    hf('r78-s16-mobile-r7', DEL/'R78-TOOL-INSERT-MOBILE-BUILD/projects/s16-mobile-r7', '0.8.50',
       [(16727, 16871, 213), (16871, 17087, 357), (17087, 17285, 573), (17285, 17380, 771)],
       patch='r78_captures', captures='S16', frame_format='png',
       flags=['Sheets screen recording raw 3840x1946 VFR; used window 1100x570 raw px -> 3.32x upscale into the 4K capture box (well below 4K; worst leaf)',
              'R77 crop+fps24 and R78 moving crop recomputed from RAW in one lossless pipe; capture scaled lanczos to 3642x1884']),
    hf('r61-s16-p2', REV/'r61-s16-p2', '0.8.36', [(17390, 17807, 0)], flags=['r61 render version never logged; pin 0.8.36 used']),
    hf('r62-s17-p1', REV/'r62-s17-p1', '0.8.36', [(17807, 18518, 0)], flags=['r62 render version never logged; pin 0.8.36 used']),
    media('s17-presenter-c', REV/'r76-s17-presenter/provider/restoration/restored.mp4', 18518, 18710, (8, 200), flags=[PRES_FLAG]),
    hf('r62-s17-p2', REV/'r62-s17-p2', '0.8.36', [(18710, 19418, 0)], flags=['r62 render version never logged; pin 0.8.36 used']),
    hf('r63-s18', REV/'r63-s18', '0.8.36', [(19418, 20198, 0)], flags=['r63 render version never logged; pin 0.8.36 used']),
    hf('r64b-s19-title-swap', DEL/'R64B-S19-TITLE-SWAP', '0.8.46', [(20198, 21314, 0)],
       flags=['public/ is a symlink to r64-s19/public; dereferenced into the scratch copy', 'owner lock pins the mp4, not index.html']),
    hf('r65-s20-economics', REV/'r65-s20-economics', '0.8.46', [(21314, 23588, 0)]),
    hf('r66-s21-hard-part', REV/'r66-s21-hard-part', '0.8.46', [(23588, 25060, 0)]),
    hf('r69-s22-film', REV/'r69-s22-film', '0.8.46', [(25060, 25115, 0), (25115, 25223, 55), (25223, 25320, 163), (25320, 25584, 260)],
       flags=['hyperframes.json media.autoProxy set false in scratch copy (originals, not proxies)', 'Kling clips 1916x1080 (below 4K), object-fit cover',
              'establishing.mp4 has sparse keyframes (seek risk)']),
    hf('r70-s23-payoff', REV/'r70-s23-payoff', '0.8.46', [(25584, 25814, 0)]),
    hf('r71-s24-verdict', REV/'r71-s24-verdict', '0.8.46', [(25814, 26366, 0)]),
    hf('r72-s25-first-action', REV/'r72-s25-first-action', '0.8.46', [(26366, 27092, 0)]),
    hf('r75-s26-boundary-close', REV/'r75-s26-boundary-close', '0.8.46', [(27092, 27241, 0)]),
]

LEAF_NAMES = {  # per-plate leaf id suffix where a job yields several plates
    ('r60-s15-p2', 15746): 'r60-s15-p2-head', ('r60-s15-p2', 16038): 'r60-s15-p2-tail',
    ('r78-s15-mobile', 15754): 's15-chatgpt-insert-a', ('r78-s15-mobile', 15826): 's15-chatgpt-insert-b',
    ('r61-s16-p1', 16514): 'r61-s16-p1-head', ('r61-s16-p1', 17380): 'r61-s16-p1-return-still-866',
    ('r78-s16-mobile-r7', 16727): 's16-sheets-insert-00', ('r78-s16-mobile-r7', 16871): 's16-sheets-insert-01',
    ('r78-s16-mobile-r7', 17087): 's16-sheets-insert-02', ('r78-s16-mobile-r7', 17285): 's16-sheets-insert-03',
    ('r69-s22-film', 25060): 's22-establishing', ('r69-s22-film', 25115): 's22-buyer-question',
    ('r69-s22-film', 25223): 's22-owner-record-take-a', ('r69-s22-film', 25320): 's22-buyer-response-take-b',
}

# R77 selection (source_in_seconds, frames) + R77 crop + R78 moving crop, per capture slot
CAPTURES = {
    'S15': dict(raw=REV/'r77-tool-recordings/qa/chatgpt-raw-01.mp4',
                raw_sha='c8673bae989394575a96535560508efc38450c0a796f98741decb20e5330e475',
                crop1=(2880, 1620, 600, 300),
                slots=[('capture-mobile-00.mp4', 0.0, 72, (2000, 1036, (200, 260), (350, 340))),
                       ('capture-mobile-01.mp4', 60.0, 212, (2000, 1036, (480, 140), (600, 210)))]),
    'S16': dict(raw=REV/'r77-tool-recordings/qa/sheets-package-state-03.mp4',
                raw_sha='77eb57434edd45b2589cdfad4b7edd308b1c9981b11930892554aee862b0dc86',
                crop1=(1588, 823, 300, 150),
                slots=[('capture-mobile-00.mp4', 0.0, 144, (1100, 570, (0, 100), (0, 118))),
                       ('capture-mobile-01.mp4', 10.5, 216, (1100, 570, (0, 100), (0, 100))),
                       ('capture-mobile-02.mp4', 21.0, 198, (1100, 570, (0, 100), (0, 100))),
                       ('capture-mobile-03.mp4', 34.0, 97, (1100, 570, (0, 100), (0, 118)))]),
}
CAPTURE_BOX_4K = (3642, 1884)   # .capture 1216x630 CSS border-box minus 1px border each side, x3 DPR

# ---------------------------------------------------------------- helpers
def log(*a):
    print(time.strftime('%H:%M:%S'), *a, flush=True)
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def run(args, **kw):
    return subprocess.run([str(x) for x in args], check=True, **kw)
def free_gb():
    st = os.statvfs('/')
    return st.f_bavail * st.f_frsize / 1e9
def probe(p):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=width,height,nb_frames,r_frame_rate,pix_fmt,profile,color_space,color_primaries,color_transfer',
        '-of', 'json', str(p)], text=True))['streams'][0]
def ffmpeg_version():
    return subprocess.check_output(['ffmpeg', '-version'], text=True).splitlines()[0]
def plate_path(a, b, leaf):
    return OUT / f'r79_{a:06d}-{b:06d}_{leaf}.mp4'

PLATE_ENC = ['-an', '-c:v', 'libx264', '-profile:v', 'high', '-preset', 'slow', '-pix_fmt', 'yuv420p',
             '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv',
             '-r', '24', '-fps_mode', 'cfr', '-video_track_timescale', '12288', '-movflags', '+faststart']

def load_manifest():
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text())
    return {'record_type': 'ep007_r80_1080_plates_manifest', 'owner_event': 'ep007-finishing-4k-rerender-v1',
            'r79_reference': {'path': str(R79.relative_to(REPO)), 'sha256': R79_SHA, 'frames': R79_FRAMES, 'fps': 24},
            'frame_ranges': 'half-open [a,b)', 'plates_dir': str(OUT), 'plates': []}
def save_manifest(m):
    m['plates'].sort(key=lambda p: p['r79_frames'][0])
    m['updated'] = datetime.datetime.now().isoformat(timespec='seconds')
    tmp = MANIFEST.with_suffix('.tmp'); tmp.write_text(json.dumps(m, indent=2) + '\n'); tmp.replace(MANIFEST)
def upsert(m, entry):
    m['plates'] = [p for p in m['plates'] if p['r79_frames'] != entry['r79_frames']] + [entry]
    save_manifest(m)

# ---------------------------------------------------------------- verification
def _stats(path, key):
    vals = []
    for line in open(path):
        mt = re.search(key + r':(\S+)', line)
        if mt and mt.group(1) not in ('inf',):
            vals.append(float(mt.group(1)))
        elif mt:
            vals.append(99.0)
    return vals

def compare(plate, a, n, shift, work, with_psnr=False):
    """SSIM (and PSNR) of plate[pa,pb) scaled to 720p vs R79[a+pa+shift, a+pb+shift)."""
    pa = max(0, -(a + shift)); pb = min(n, R79_FRAMES - a - shift)
    ra = a + pa + shift; rb = a + pb + shift
    t0 = max(0.0, (ra - 48) / 24)
    ss_file = work / f'ssim_{shift}.log'; ps_file = work / f'psnr_{shift}.log'
    pflt = f'[0:v]trim=start_frame={pa}:end_frame={pb},setpts=N/(24*TB),scale=1280:720:flags=area,format=yuv420p'
    rflt = f'[1:v]trim=start={(ra - 0.5) / 24:.6f}:end={(rb - 0.5) / 24:.6f},setpts=N/(24*TB),format=yuv420p'
    if with_psnr:
        fc = (f'{pflt},split[p1][p2];{rflt},split[r1][r2];[p1][r1]ssim=stats_file={ss_file}[o1];'
              f'[p2][r2]psnr=stats_file={ps_file}[o2]')
        maps = ['-map', '[o1]', '-f', 'null', '-', '-map', '[o2]', '-f', 'null', '-']
    else:
        fc = f'{pflt}[p];{rflt}[r];[p][r]ssim=stats_file={ss_file}[o1]'
        maps = ['-map', '[o1]', '-f', 'null', '-']
    run(['ffmpeg', '-v', 'error', '-nostdin', '-i', plate, '-copyts', '-ss', f'{t0:.6f}', '-i', R79,
         '-filter_complex', fc] + maps)
    ss = _stats(ss_file, 'All')
    ps = _stats(ps_file, 'psnr_avg') if with_psnr else []
    assert len(ss) == pb - pa, (plate, shift, len(ss), pb - pa)
    return ss, ps

def verify(plate, a, b, work):
    n = b - a
    ss, ps = compare(plate, a, n, 0, work, with_psnr=True)
    sm1, _ = compare(plate, a, n, -1, work)
    sp1, _ = compare(plate, a, n, +1, work)
    mean = sum(ss) / len(ss); mn = min(ss)
    worst = sorted(range(len(ss)), key=lambda i: ss[i])[:5]
    m_m1 = sum(sm1) / len(sm1); m_p1 = sum(sp1) / len(sp1)
    margin = mean - max(m_m1, m_p1)
    align_ok = margin > 0
    align_note = 'aligned' if margin > 1e-4 else ('indeterminate (static content: shift within 1e-4)' if margin > -1e-5 else 'MISALIGNED')
    if align_note.startswith('indeterminate'):
        align_ok = True
    passed = mean >= SSIM_MEAN_MIN and mn >= SSIM_FRAME_MIN and align_ok
    reasons = []
    if mean < SSIM_MEAN_MIN: reasons.append(f'mean SSIM {mean:.5f} < {SSIM_MEAN_MIN}')
    if mn < SSIM_FRAME_MIN: reasons.append(f'min SSIM {mn:.5f} < {SSIM_FRAME_MIN} at r79 frame {a + ss.index(mn)}')
    if not align_ok: reasons.append(f'one-frame shift scores higher (shift -1 {m_m1:.5f}, +1 {m_p1:.5f})')
    psf = [p for p in ps if p < 99]
    return {
        'method': 'plate scaled to 1280x720 (area) vs R79 frames, ffmpeg ssim/psnr per frame',
        'ssim_mean': round(mean, 6), 'ssim_min': round(mn, 6),
        'ssim_min_r79_frame': a + ss.index(mn),
        'ssim_worst_frames': [[a + i, round(ss[i], 5)] for i in worst],
        'frames_below_0_95': sum(1 for x in ss if x < SSIM_FRAME_MIN),
        'psnr_mean_db': round(sum(psf) / len(psf), 2) if psf else None,
        'psnr_min_db': round(min(psf), 2) if psf else None,
        'shift_minus1_ssim_mean': round(m_m1, 6), 'shift_plus1_ssim_mean': round(m_p1, 6),
        'alignment': align_note, 'pass': passed, 'fail_reasons': reasons,
    }

# ---------------------------------------------------------------- builders
def cut_plate(src4k, plate, pa, pb, crf, hold=None):
    if hold is not None:
        frame, count = hold
        vf = (f'trim=start_frame={frame}:end_frame={frame + 1},setpts=N/(24*TB),'
              f'loop=loop={count - 1}:size=1:start=0,setpts=N/(24*TB),')
        nframes = count
    else:
        vf = f'trim=start_frame={pa}:end_frame={pb},setpts=N/(24*TB),'
        nframes = pb - pa
    vf += 'scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int,setsar=1,format=yuv420p'
    run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', src4k, '-vf', vf, '-frames:v', nframes, '-crf', crf] + PLATE_ENC + [plate])
    return nframes

def build_captures(which, dest_media, work):
    """R77 (crop1 + fps=24 output-seek) -> lossless pipe -> R78 moving crop -> lanczos to 4K content box."""
    spec = CAPTURES[which]
    assert sha(spec['raw']) == spec['raw_sha'], spec['raw']
    info = []
    W, H = CAPTURE_BOX_4K
    for name, t_in, frames, (cw, ch, (x0, y0), (x1, y1)) in spec['slots']:
        c1w, c1h, c1x, c1y = spec['crop1']
        def interp(s, e):
            return str(s) if s == e else f"trunc(({s}+({e}-{s})*n/{frames - 1})/2)*2"
        p1 = subprocess.Popen(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(spec['raw']), '-ss', str(t_in),
                               '-t', f'{frames / 24:.9f}', '-vf', f'crop={c1w}:{c1h}:{c1x}:{c1y},fps=24,setsar=1',
                               '-an', '-frames:v', str(frames), '-pix_fmt', 'yuv420p', '-c:v', 'rawvideo', '-f', 'nut', '-'],
                              stdout=subprocess.PIPE)
        out = dest_media / name
        vf2 = (f"crop=w={cw}:h={ch}:x='{interp(x0, x1)}':y='{interp(y0, y1)}',"
               f"scale={W}:{H}:flags=lanczos+accurate_rnd+full_chroma_int,setsar=1,format=yuv420p")
        run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-f', 'nut', '-i', '-', '-vf', vf2, '-an', '-frames:v', frames,
             '-c:v', 'libx264', '-crf', '8', '-preset', 'medium', '-g', '24', '-pix_fmt', 'yuv420p',
             '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-movflags', '+faststart', out],
            stdin=p1.stdout)
        p1.stdout.close(); assert p1.wait() == 0
        pr = probe(out)
        assert int(pr['nb_frames']) == frames and (int(pr['width']), int(pr['height'])) == (W, H), pr
        info.append({'slot': name, 'raw_in_seconds': t_in, 'frames': frames, 'r77_crop': f'crop={c1w}:{c1h}:{c1x}:{c1y},fps=24',
                     'r78_crop': vf2.split(',scale')[0], 'scaled_to': [W, H], 'sha256': sha(out)})
    return info

def patch_r39(copy):
    src = REV / 'r39-question-performance/provider/restoration/restored.mp4'
    assert sha(src) == '670ad1dc7c4f31759cc12eaf8deb64949c27a25fc93e3563f84826fb058a4207'
    out = copy / 'public/media/question-r39-aligned.mp4'
    out.unlink()
    run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', src, '-vf',
         'fps=24,trim=start_frame=10:end_frame=137,setpts=PTS-STARTPTS,format=yuv420p', '-an',
         '-c:v', 'libx264', '-crf', '10', '-preset', 'medium', '-g', '24', '-pix_fmt', 'yuv420p',
         '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-movflags', '+faststart', out])
    pr = probe(out); assert int(pr['nb_frames']) == 127 and pr['width'] == 1920, pr
    return {'replaced': 'public/media/question-r39-aligned.mp4', 'from': str(src.relative_to(REPO)),
            'recipe': 'fps24, trim frames 10..136 inclusive, reset timestamps, 1920x1080 (no downscale), h264 crf10 yuv420p',
            'sha256': sha(out)}

def copy_project(src, dst):
    if dst.exists(): shutil.rmtree(dst)
    ignore = shutil.ignore_patterns('qa', 'snapshots', 'renders', 'node_modules', '.waveform-cache', 'provider', 'tmp', '.debug')
    shutil.copytree(src, dst, symlinks=False, ignore=ignore)
    hj = dst / 'hyperframes.json'
    changed = False
    if hj.exists():
        d = json.loads(hj.read_text())
        if d.get('media', {}).get('autoProxy') is True:
            d['media']['autoProxy'] = False; hj.write_text(json.dumps(d, indent=2) + '\n'); changed = True
    return changed

def hf_render(job, copy, out4k, logf):
    ver = job['ver']
    quality = 'delivery' if tuple(map(int, ver.split('.'))) >= (0, 8, 46) else 'high'
    cmd = ['npx', '--yes', f'hyperframes@{ver}', 'render', str(copy), '--output', str(out4k), '--fps', '24',
           '--resolution', 'landscape-4k', '--quality', quality, '--crf', str(CRF_4K), '--low-memory-mode',
           '--workers', '1', '--frames-cache-dir', 'off']
    if job.get('frame_format'):
        cmd += ['--video-frame-format', job['frame_format']]
    t = time.time()
    with open(logf, 'w') as lf:
        lf.write(' '.join(cmd) + '\n'); lf.flush()
        subprocess.run(cmd, check=True, stdout=lf, stderr=subprocess.STDOUT, cwd=copy)
    return cmd, time.time() - t

def leaf_name(job, a):
    return LEAF_NAMES.get((job['id'], a), job['id'])

# ---------------------------------------------------------------- main
def process(job, m, crf, force):
    work = SCRATCH / job['id']
    specs = []
    for p in job['plates']:
        if p[0] == 'hold':
            _, a, b, fr = p; specs.append(dict(a=a, b=b, hold=(fr, b - a), src_a=fr))
        else:
            a, b, s = p; specs.append(dict(a=a, b=b, src_a=s, src_b=s + (b - a)))
    done = {tuple(pl['r79_frames']) for pl in m['plates'] if pl.get('status') == 'done'}
    if not force and all((s['a'], s['b']) in done and plate_path(s['a'], s['b'], leaf_name(job, s['a'])).exists() for s in specs):
        log('skip (done)', job['id']); return
    fg = free_gb()
    if fg < MIN_FREE_GB:
        log(f'DISK GUARD: {fg:.2f} GB free < {MIN_FREE_GB} GB before {job["id"]}; stopping')
        raise SystemExit(3)
    log(f'== {job["id"]} ({job["kind"]}) free {fg:.2f} GB')
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True)
    extra = {}; tool = {'ffmpeg': ffmpeg_version()}
    t_all = time.time()
    try:
        if job['kind'] == 'hf':
            copy = work / 'project'
            proxy_off = copy_project(job['project'], copy)
            if proxy_off: extra['autoProxy_disabled_in_scratch'] = True
            if job.get('patch') == 'r39_question_fullres':
                extra['scratch_patch'] = patch_r39(copy)
            if job.get('patch') == 'r78_captures':
                extra['scratch_patch'] = {'captures_rebuilt_from_raw': build_captures(job['captures'], copy / 'public/media', work),
                                          'raw': str(CAPTURES[job['captures']]['raw'].relative_to(REPO)),
                                          'raw_sha256': CAPTURES[job['captures']]['raw_sha']}
            out4k = work / 'render-4k.mp4'
            cmd, secs = hf_render(job, copy, out4k, work / 'render.log')
            pr = probe(out4k)
            extra['render_4k'] = {'cmd': ' '.join(cmd[:4]) + ' ... ' + ' '.join(cmd[5:]).replace(str(copy), '<scratch copy>'),
                                  'seconds': round(secs, 1), 'width': pr['width'], 'height': pr['height'], 'frames': int(pr['nb_frames']),
                                  'bytes': out4k.stat().st_size}
            tool['hyperframes'] = job['ver']
            log(f'   4K render {pr["width"]}x{pr["height"]} {pr["nb_frames"]} f in {secs:.0f}s, {out4k.stat().st_size / 1e6:.0f} MB')
            assert (pr['width'], pr['height']) == (3840, 2160), pr
            idx = job['project'] / 'index.html'
            source = {'project': str(job['project'].relative_to(REPO)), 'index_html_sha256': sha(idx)}
            for s in specs:
                s['plate'] = plate_path(s['a'], s['b'], leaf_name(job, s['a']))
                if s.get('hold'):
                    cut_plate(out4k, s['plate'], None, None, crf, hold=s['hold'])
                    s['recipe'] = f'4K render frame {s["hold"][0]} held {s["hold"][1]} frames -> lanczos 1920x1080'
                else:
                    assert s['src_b'] <= int(pr['nb_frames']), (s, pr['nb_frames'])
                    cut_plate(out4k, s['plate'], s['src_a'], s['src_b'], crf)
                    s['recipe'] = f'4K render frames [{s["src_a"]},{s["src_b"]}) -> lanczos 1920x1080'
            out4k.unlink(); log('   4K render deleted')
            shutil.rmtree(copy)
        else:
            src = job['src']; pr = probe(src)
            source = {'media': str(src.relative_to(REPO)), 'sha256': sha(src), 'width': pr['width'], 'height': pr['height'], 'pix_fmt': pr['pix_fmt']}
            s = specs[0]; s['plate'] = plate_path(s['a'], s['b'], job['id'])
            fa, fb = s['src_a'], job['src_end']; assert fb - fa == s['b'] - s['a']
            scale = 'scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int,' if job.get('stretch') or (int(pr['width']), int(pr['height'])) != (1920, 1080) else ''
            vf = f'trim=start_frame={fa}:end_frame={fb},setpts=N/(24*TB),{scale}setsar=1,format=yuv420p'
            run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', src, '-vf', vf, '-frames:v', fb - fa, '-crf', crf] + PLATE_ENC + [s['plate']])
            s['recipe'] = f'source frames [{fa},{fb}) ' + ('-> lanczos stretch to 1920x1080' if scale else 'at native 1920x1080') + ', 8-bit yuv420p'
        for s in specs:
            pl = s['plate']; pr = probe(pl)
            nf = int(pr['nb_frames'])
            ver = verify(pl, s['a'], s['b'], work)
            flags = list(job.get('flags', []))
            if nf != s['b'] - s['a']:
                flags.append(f'FRAME COUNT MISMATCH {nf} != {s["b"] - s["a"]}'); ver['pass'] = False
            entry = {'r79_frames': [s['a'], s['b']], 'frames': nf, 'leaf': leaf_name(job, s['a']), 'job': job['id'],
                     'kind': job['kind'], 'plate': pl.name, 'bytes': pl.stat().st_size, 'sha256': sha(pl),
                     'format': {'codec': 'h264', 'profile': pr.get('profile'), 'pix_fmt': pr['pix_fmt'], 'size': [pr['width'], pr['height']],
                                'fps': pr['r_frame_rate'], 'color': [pr.get('color_space'), pr.get('color_primaries'), pr.get('color_transfer')], 'crf': int(crf)},
                     'source': source, 'recipe': s['recipe'], 'tool_versions': tool, **extra,
                     'verification': ver, 'pass': ver['pass'], 'flags': flags, 'status': 'done',
                     'built': datetime.datetime.now().isoformat(timespec='seconds')}
            upsert(m, entry)
            log(f'   plate {pl.name}: {nf} f, {pl.stat().st_size / 1e6:.1f} MB, SSIM mean {ver["ssim_mean"]:.5f} min {ver["ssim_min"]:.5f}, '
                f'shift {ver["shift_minus1_ssim_mean"]:.5f}/{ver["shift_plus1_ssim_mean"]:.5f} {ver["alignment"]} -> {"PASS" if ver["pass"] else "FAIL " + "; ".join(ver["fail_reasons"])}')
    except Exception as e:
        log(f'   ERROR {job["id"]}: {e!r}')
        for s in specs:
            upsert(m, {'r79_frames': [s['a'], s['b']], 'leaf': leaf_name(job, s['a']), 'job': job['id'], 'kind': job['kind'],
                       'status': 'error', 'pass': False, 'error': repr(e)[:2000], 'flags': job.get('flags', []),
                       'built': datetime.datetime.now().isoformat(timespec='seconds')})
    finally:
        for f in work.glob('*.mp4'):
            f.unlink()
        if (work / 'project').exists(): shutil.rmtree(work / 'project')
    log(f'   job {job["id"]} {time.time() - t_all:.0f}s; free {free_gb():.2f} GB')

def tiling(m):
    plates = sorted((p for p in m['plates'] if p.get('status') == 'done'), key=lambda p: p['r79_frames'][0])
    cur = 0; gaps = []; overlaps = []
    for p in plates:
        a, b = p['r79_frames']
        if a > cur: gaps.append([cur, a])
        if a < cur: overlaps.append([a, cur])
        cur = max(cur, b)
    if cur < R79_FRAMES: gaps.append([cur, R79_FRAMES])
    return {'range': [0, R79_FRAMES], 'plates_done': len(plates), 'gaps': gaps, 'overlaps': overlaps,
            'frames_sum': sum(p['frames'] for p in plates), 'exact_tiling': not gaps and not overlaps and sum(p['frames'] for p in plates) == R79_FRAMES}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', nargs='*'); ap.add_argument('--list', action='store_true')
    ap.add_argument('--crf', default=str(PLATE_CRF)); ap.add_argument('--force', action='store_true')
    args = ap.parse_args()
    if args.list:
        for j in JOBS: print(j['id'], j['kind'], j['plates'])
        return
    assert sha(R79) == R79_SHA
    OUT.mkdir(parents=True, exist_ok=True); SCRATCH.mkdir(parents=True, exist_ok=True)
    m = load_manifest()
    jobs = [j for j in JOBS if not args.only or j['id'] in args.only]
    for j in jobs:
        process(j, m, args.crf, args.force)
    m['tiling_check'] = tiling(m)
    done = [p for p in m['plates'] if p.get('status') == 'done']
    m['summary'] = {'plates': len(m['plates']), 'pass': sum(1 for p in m['plates'] if p.get('pass')),
                    'fail': sum(1 for p in m['plates'] if not p.get('pass')),
                    'total_bytes': sum(p.get('bytes', 0) for p in done), 'free_gb_at_end': round(free_gb(), 2)}
    save_manifest(m)
    log('summary', json.dumps(m['summary']), 'tiling', json.dumps(m['tiling_check']))

if __name__ == '__main__':
    main()
