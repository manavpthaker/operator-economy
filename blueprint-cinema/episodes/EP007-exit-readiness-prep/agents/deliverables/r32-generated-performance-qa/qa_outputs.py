#!/usr/bin/env python3
"""Read pinned R32 outputs; write diagnostics only beside this file. No services."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw

REPO = Path('/Users/brownmanbrain/GitHub/operator-economy')
OUT = Path(__file__).resolve().parent
WORK = REPO / 'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/work-orders/r32-generated-performance-qa.json'
W = json.loads(WORK.read_text())
RATE = 16000
REF_INDEX = {'post-title-lens-contact': 4, 'question-pensive': 5}


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def call(args):
    return subprocess.check_output(args)


def probe(path):
    return json.loads(call(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))


def audio(path):
    raw = call(['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-ac', '1', '-ar', str(RATE), '-f', 'f32le', '-'])
    return np.frombuffer(raw, dtype='<f4').astype(np.float64)


def corr(a, b):
    if len(a) != len(b) or len(a) < 2 or not np.std(a) or not np.std(b):
        return None
    return float(np.corrcoef(a, b)[0, 1])


def offset(a, b, lower, upper):
    size = 1 << (len(a) + len(b) - 2).bit_length()
    convolution = np.fft.irfft(np.fft.rfft(b, size) * np.fft.rfft(a[::-1], size), size)
    lo = max(0, len(a)-1+lower)
    hi = min(len(a)+len(b)-1, len(a)-1+upper+1)
    lag = int(np.argmax(convolution[lo:hi]) + lo - len(a) + 1)
    return lag


def compare(reference, candidate, fps, video_duration):
    a, b = audio(reference), audio(candidate)
    lag = offset(a, b, -2*RATE, 2*RATE)
    ia, ib = max(0, -lag), max(0, lag)
    count = min(len(a)-ia, len(b)-ib)
    aligned = corr(a[ia:ia+count], b[ib:ib+count])
    windows = []
    half = int(min(1.2, len(a)/RATE*.12)*RATE)
    for name, fraction in [('early', .15), ('middle', .5), ('late', .83)]:
        center = int(len(a)*fraction)
        al, ar = max(0, center-half), min(len(a), center+half)
        bl, br = max(0, al+lag-int(.25*RATE)), min(len(b), ar+lag+int(.25*RATE))
        segment = a[al:ar]
        search = b[bl:br]
        if len(search) < len(segment):
            windows.append({'name': name, 'status': 'insufficient overlap'})
            continue
        local = offset(segment, search, 0, len(search)-len(segment))
        measured = (bl+local-al)/RATE
        windows.append({'name': name, 'reference_seconds': [al/RATE, ar/RATE],
            'independent_insertion_seconds': measured,
            'aligned_correlation': corr(segment, search[local:local+len(segment)])})
    trusted = aligned is not None and aligned >= .97 and abs(lag) < 2*RATE
    frame = round(lag/RATE*fps) if trusted else None
    with wave.open(str(reference), 'rb') as reference_wav:
        reference_duration = reference_wav.getnframes()/reference_wav.getframerate()
    required = frame/fps+reference_duration if frame is not None else None
    return {'insertion_seconds': lag/RATE, 'aligned_correlation': aligned,
        'search_boundary': abs(lag)==2*RATE, 'reference_duration_seconds': reference_duration,
        'candidate_audio_seconds': len(b)/RATE, 'independent_windows': windows,
        'waveform_match_for_mapping': trusted, 'nearest_source_frame_for_review_only': frame,
        'quantization_residual_seconds': lag/RATE-frame/fps if frame is not None else None,
        'picture_seconds_required_for_reference': required,
        'has_picture_for_complete_reference_at_rounded_offset':
            required is not None and frame >= 0 and video_duration+1e-6 >= required,
        'interpretation': 'Waveform placement only. Neither correlation nor quantized source frame proves visual lip synchronization.'}


def frame_audit(path):
    p = json.loads(call(['ffprobe','-v','error','-select_streams','v','-show_frames',
        '-show_entries','frame=best_effort_timestamp_time','-of','json',str(path)]))['frames']
    times = [float(x['best_effort_timestamp_time']) for x in p]
    data = call(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-f','framemd5','-']).decode()
    hashes = [x.split(',')[-1].strip() for x in data.splitlines() if x and not x.startswith('#')]
    steps = np.diff(times)
    return {'decoded_frames': len(times), 'first_pts': times[0], 'last_pts': times[-1],
        'interval_min': float(np.min(steps)), 'interval_max': float(np.max(steps)),
        'duplicate_or_backwards_pts': int(np.count_nonzero(steps<=0)),
        'exact_adjacent_repeat_frames': [i for i in range(1,len(hashes)) if hashes[i]==hashes[i-1]],
        'limit': 'Distinct decoded frames do not certify natural motion or exclude sub-frame jitter.'}


def contacts(path, take, stage, tag, duration, fps, insertion):
    last = max(0, round(duration*fps)-1)
    positions = [0, duration*.2, duration*.4, duration*.6, duration*.8, last/fps]
    anchors = {'post-title-lens-contact': [9.5,10,10.5,10.75,11,11.25,11.5,11.75,12,12.25,12.5,13,14,14.75],
        'question-pensive': [2.5,3,8.5,8.75,9,9.25,9.5,10,10.5,11,11.5,11.75,12,12.25,12.5]}
    positions += [t+(insertion or 0) for t in anchors.get(take, [])]
    frames = sorted(set(min(last,max(0,round(t*fps))) for t in positions if t < duration))
    folder = OUT/(tag+'-frames')
    folder.mkdir(exist_ok=False)
    expression = '+'.join(f'eq(n,{n})' for n in frames)
    call(['ffmpeg','-v','error','-n','-i',str(path),'-an','-vf',f'select={expression.replace(",", chr(92)+",")}',
        '-fps_mode','vfr','-q:v','2',str(folder/'%03d.jpg')])
    paths = sorted(folder.glob('*.jpg'))
    assert len(paths)==len(frames), 'Unexpected frame selection count'
    outputs = []
    for kind, face in [('performance',False),('face',True)]:
        if face and take=='buyer-reaction':
            continue  # Buyer composition and face position require its actual direction/output.
        width,height,caption = (384,216,36) if not face else (320,250,36)
        sheet = Image.new('RGB',(4*width,math.ceil(len(paths)/4)*(height+caption)),'#eeeae2')
        for i,(p,n) in enumerate(zip(paths,frames)):
            im=Image.open(p).convert('RGB')
            if face:
                w,h=im.size
                im=im.crop((int(w*.36),int(h*.04),int(w*.64),int(h*.44)))
            im.thumbnail((width,height));x=i%4*width;y=i//4*(height+caption)
            sheet.paste(im,(x+(width-im.width)//2,y+(height-im.height)//2))
            reference = f' | ref {n/fps-insertion:.3f}' if insertion is not None else ''
            ImageDraw.Draw(sheet).text((x+4,y+height+4),f'source frame {n}: {n/fps:.3f}s{reference}',fill='black')
        target=OUT/f'{tag}-{kind}.jpg';sheet.save(target,quality=95)
        outputs.append({'path':str(target.relative_to(REPO)),'sha256':digest(target)})
    return {'sheets':outputs,'source_frame_indices':frames,'source_seconds':[n/fps for n in frames],
        'reference_offset_seconds':insertion,'raw_frame_directory':str(folder.relative_to(REPO)),
        'anchor_limit': 'Native anchors approximate source positions; only restored waveform measurements provide reference-audio placement.'}


def prepare():
    for pin in W['inputs']:
        assert digest(REPO/pin['path'])==pin['sha256'],pin['path']
    result={'preparation_only':True,'work_order_id':W['work_order_id'],'inputs':W['inputs'],
        'versions':{name:call([name,'-version']).decode().splitlines()[0] for name in ['ffmpeg','ffprobe']},
        'audio_probes':{name:probe(REPO/W['inputs'][index]['path']) for name,index in REF_INDEX.items()},
        'actual_output_inspections':'not_run; output path and SHA-256 must be explicitly supplied'}
    (OUT/'preparation-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print('All six preparation pins verified. Actual generated outputs not inspected.')


def inspect(args):
    path=Path(args.input).expanduser().resolve()
    assert path.is_file(), 'Missing output; stop, do not poll or generate'
    assert digest(path)==args.sha256, 'Output hash mismatch; stop'
    tag=args.tag or f'{args.take}-{args.stage}'
    assert re.fullmatch(r'[a-z0-9][a-z0-9-]*',tag), 'Invalid local artifact tag'
    target=OUT/(tag+'-metrics.json')
    assert not target.exists() and not (OUT/(tag+'-frames')).exists(), 'Preserve prior QA; choose a new tag'
    p=probe(path);v=next(s for s in p['streams'] if s['codec_type']=='video')
    numerator,denominator=map(int,v['r_frame_rate'].split('/'));fps=numerator/denominator
    duration=float(v.get('duration',p['format']['duration']))
    decoded=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-f','null','-'],capture_output=True)
    result={'take':args.take,'stage':args.stage,'input_path':str(path),'sha256':args.sha256,
        'probe':p,'full_decode':{'exit_code':decoded.returncode,'stderr':decoded.stderr.decode()},
        'frame_audit':frame_audit(path),'reference_audio':None,'audio_comparison':None,
        'perceptual_review':'not_run; inspect contacts and normal-speed synchronized result separately',
        'owner_acceptance_claimed':False}
    insertion=None
    if args.take in REF_INDEX:
        pin=W['inputs'][REF_INDEX[args.take]];reference=REPO/pin['path']
        assert digest(reference)==pin['sha256'],'Original audio pin changed; stop'
        result['reference_audio']=pin
        if args.stage=='restored':
            assert any(s['codec_type']=='audio' for s in p['streams']),'Restored output has no audio to measure'
            result['audio_comparison']=compare(reference,path,fps,duration)
            if result['audio_comparison']['waveform_match_for_mapping']:
                insertion=result['audio_comparison']['insertion_seconds']
        else:
            result['native_audio_limit']='Regenerated native speech is not the original voice; no final lip-sync inference.'
    result['contacts']=contacts(path,args.take,args.stage,tag,duration,fps,insertion)
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(str(target))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    commands.add_parser('prepare')
    sub=commands.add_parser('inspect')
    sub.add_argument('--take',required=True,choices=['post-title-lens-contact','question-pensive','buyer-reaction'])
    sub.add_argument('--stage',required=True,choices=['native','restored'])
    sub.add_argument('--input',required=True)
    sub.add_argument('--sha256',required=True)
    sub.add_argument('--tag')
    a=parser.parse_args()
    if a.command=='prepare':prepare()
    else:inspect(a)
