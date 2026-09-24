#!/usr/bin/env python3
"""Build and inspect this bounded review candidate. Writes only beside this script."""
from pathlib import Path
import array
import hashlib
import json
import math
import subprocess
import wave

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
REVIEWS = ROOT / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews'
MASTER = ROOT / 'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
COMMANDS = []


def run(args, capture=False):
    COMMANDS.append(args)
    r = subprocess.run(args, check=True, stdout=subprocess.PIPE if capture else subprocess.DEVNULL, stderr=subprocess.PIPE)
    return r.stdout


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_entries', 'stream=index,codec_name,width,height,r_frame_rate,duration,nb_frames,sample_rate,channels', '-show_entries', 'format=duration,size', '-of', 'json', str(path)], True))


def decoded_audio(path, ss=0, duration=54.5):
    data = run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', str(path), '-t', str(duration), '-vn', '-af', 'pan=mono|c0=c0', '-ar', '8000', '-f', 'f32le', '-'], True)
    result = array.array('f')
    result.frombytes(data)
    return result


def audio_comparison(path, master_start, duration):
    a, b = decoded_audio(path, duration=duration), decoded_audio(MASTER, ss=master_start, duration=duration)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    aa, bb = sum(x*x for x in a), sum(x*x for x in b)
    return {'sample_rate_for_comparison': 8000, 'samples': n, 'zero_lag_correlation': sum(x*y for x,y in zip(a,b))/math.sqrt(aa*bb), 'left_channel_level_delta_dB': 10*math.log10(aa/bb), 'max_abs_error': max(abs(x-y) for x,y in zip(a,b))}


def rgb_frame(path, seconds, scale=None):
    args = ['ffmpeg', '-v', 'error', '-ss', str(seconds), '-i', str(path), '-frames:v', '1']
    if scale:
        args += ['-vf', 'scale=' + scale]
    return run(args + ['-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'], True)


def mean_error(a, b):
    assert len(a) == len(b)
    return sum(abs(x-y) for x,y in zip(a,b))/len(a)


def main():
    assert (ROOT / 'blueprint-cinema').is_dir(), ROOT
    qa = HERE / 'qa'
    candidate = qa / 'r64b-s19.mp4'
    s18 = REVIEWS / 'r63-s18/qa/r63-s18.mp4'
    old = REVIEWS / 'r64-s19/qa/r64-s19.mp4'
    old_context = REVIEWS / 'r64-s19-context/qa/context.mp4'
    original_inputs = json.loads((HERE / 'INPUTS.json').read_text())
    assert all(digest(ROOT / p) == sha for p,sha in original_inputs.items()), 'Original input changed'
    original_inputs[str(s18.relative_to(ROOT))] = digest(s18)
    (HERE / 'INPUTS.json').write_text(json.dumps(original_inputs, indent=2) + '\n')

    run(['ffmpeg', '-v', 'error', '-y', '-ss', '836.5', '-i', str(MASTER), '-t', '54.5', '-c:a', 'pcm_s16le', str(qa/'audio.wav')])
    with wave.open(str(MASTER), 'rb') as w:
        w.setpos(round(836.5*w.getframerate()))
        expected = w.readframes(round(54.5*w.getframerate()))
    with wave.open(str(qa/'audio.wav'), 'rb') as w:
        actual = w.readframes(w.getnframes())
    assert expected == actual, 'Context PCM differs from locked master'

    run(['ffmpeg', '-v', 'error', '-y', '-ss', '24.5', '-i', str(s18), '-i', str(candidate), '-i', str(qa/'audio.wav'), '-filter_complex', '[0:v]trim=end_frame=192,setpts=PTS-STARTPTS[v0];[1:v]trim=end_frame=1116,setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[v];[2:a]pan=stereo|c0=c0|c1=c0[a]', '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '24', '-frames:v', '1308', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', '54.5', '-movflags', '+faststart', str(qa/'context.mp4')])

    videos = {}
    for name, path, frames, duration in [('standalone',candidate,1116,46.5),('context',qa/'context.mp4',1308,54.5)]:
        metadata = probe(path)
        video = next(x for x in metadata['streams'] if x['codec_name']=='h264')
        assert (video['width'],video['height'],video['r_frame_rate'],int(video['nb_frames'])) == (1280,720,'24/1',frames)
        assert float(video['duration']) == duration
        run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'])
        videos[name] = {'path': str(path.relative_to(ROOT)), 'sha256': digest(path), 'probe': metadata, 'strict_decode': 'pass'}

    raw = run(['ffmpeg', '-v', 'error', '-i', str(qa/'context.mp4'), '-vf', 'scale=160:90', '-pix_fmt', 'gray', '-f', 'rawvideo', '-'], True)
    frame_bytes = 160*90
    stats = []
    for i in range(0,len(raw),frame_bytes):
        b = raw[i:i+frame_bytes]
        mean = sum(b)/len(b)
        stats.append(math.sqrt(sum(x*x for x in b)/len(b)-mean*mean))
    assert len(stats)==1308 and min(stats)>0

    comparisons = []
    for seconds in [0,9,18.8,23.4,28,30.5,38]:
        comparisons.append({'standalone_seconds':seconds,'mean_abs_rgb_error_0_255':mean_error(rgb_frame(old,seconds,'320:180'),rgb_frame(candidate,seconds,'320:180'))})

    for name,path,frame in [('original-title-collision',old_context,895),('corrected-before-title-cut',qa/'context.mp4',894),('corrected-after-title-cut',qa/'context.mp4',895),('corrected-title-settled',qa/'context.mp4',906),('corrected-final-card',qa/'context.mp4',1293)]:
        run(['ffmpeg','-v','error','-y','-i',str(path),'-vf',f'select=eq(n\\,{frame})','-frames:v','1',str(qa/'stills'/f'{name}.png')])
    seam_frames = [893,894,895,896,897,900,905,906]
    expr = '+'.join(f'eq(n,{f})' for f in seam_frames)
    run(['ffmpeg','-v','error','-y','-i',str(qa/'context.mp4'),'-vf',f"select='{expr}',scale=480:270,tile=4x2",'-frames:v','1',str(qa/'stills/title-seam-contact.png')])

    result = {
        'status':'technical_review_candidate',
        'owner_approval':False,
        'original_inputs_unchanged':True,
        'videos':videos,
        'audio': {'context_pcm_master_range':[836.5,891.0],'context_pcm_bit_exact':True,'context_encoded':audio_comparison(qa/'context.mp4',836.5,54.5),'standalone_encoded':audio_comparison(candidate,844.5,46.5)},
        'picture_scan':{'frames':len(stats),'uniform_frames':sum(x==0 for x in stats),'minimum_scaled_gray_std':min(stats),'title_seam_minimum_scaled_gray_std':min(stats[893:907]),'analysis_resolution':[160,90]},
        'unchanged_scene_comparison_to_original_encoded_render':comparisons,
        'title_swap':{'cue_master_seconds':873.76,'cue_standalone_seconds':29.26,'cue_context_seconds':37.26,'last_old_heading_frame':894,'first_new_heading_frame':895,'first_new_heading_frame_seconds':895/24,'quote_fade_seconds':[37.26,37.71]},
        'limitations':['Owner review pending.','Strict checker retains four informational connector endpoint guesses; rendered graph endpoints inspected.','Lossy encodes are compared numerically, not claimed byte-identical.','No canonical production or publication gate advanced.']
    }
    (qa/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    (qa/'ffmpeg-commands.json').write_text(json.dumps(COMMANDS,indent=2)+'\n')
    (HERE/'review.html').write_text('<!doctype html><html><head><meta charset="utf-8"><title>EP007 S19 corrected title transition</title><style>body{margin:0;background:#111;color:#eee;font:15px system-ui}video{display:block;width:100%;max-height:92vh;background:#000}p{padding:8px 14px;margin:0}</style></head><body><video controls preload="metadata" src="qa/context.mp4"></video><p>Review candidate: original S18 tail (8 s), then S19. At 0:37.26, The risk replaces the old heading without overlap; the quote keeps its original fade. Item 1 on the final card uses the existing secondary ink for readable contrast. S19 remains awaiting owner review.</p></body></html>\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
