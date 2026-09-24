"""Assemble measured native picture sections against the full new voice.

Run in Higgsfield sandbox. No synthesized mouth pass or voice speed processing.
Config supplies pinned native sources, exact frame counts, full WAV, and output slot.
"""
import base64
import hashlib
import json
import math
from pathlib import Path
import subprocess
import urllib.request
import wave
import numpy as np


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(args):
    return subprocess.check_output(args)


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def samples(path):
    return np.frombuffer(run(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype='<f4').astype(np.float64)


def main(cfg):
    urllib.request.urlretrieve(cfg['voice_url'],'voice.wav')
    assert sha('voice.wav') == cfg['voice_sha256']
    with wave.open('voice.wav') as w:
        rate,count=w.getframerate(),w.getnframes()
        assert (rate,w.getnchannels(),w.getsampwidth())==(48000,1,2)
    total_frames=math.ceil(count/rate*24)
    assert sum(s['selected_frames'] for s in cfg['sources'])==total_frames
    source_records=[]
    for i,s in enumerate(cfg['sources']):
        path=f'native-{i+1}.mp4'
        urllib.request.urlretrieve(s['url'],path)
        assert sha(path)==s['sha256']
        meta=probe(path);v=next(t for t in meta['streams'] if t['codec_type']=='video')
        assert (v['width'],v['height'],v['r_frame_rate'])==(720,1280,'24/1')
        first=s.get('start_frame',0);n=s['selected_frames']
        assert first>=0 and int(v['nb_frames'])>=first+n
        source_records.append({'index':i+1,'url':s['url'],'sha256':sha(path),'native_frames':int(v['nb_frames']),'selected_start_frame':first,'selected_frames':n})
    filters=[]
    args=['ffmpeg','-v','error','-y']
    for i,s in enumerate(cfg['sources']):
        args+=['-i',f'native-{i+1}.mp4']
        first=s.get('start_frame',0)
        filters.append(f'[{i}:v]trim=start_frame={first}:end_frame={first+s["selected_frames"]},setpts=PTS-STARTPTS,setsar=1[v{i}]')
    n=len(cfg['sources']);args+=['-i','voice.wav']
    filters.append(''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[outv]')
    args+=['-filter_complex_threads','1','-filter_complex',';'.join(filters),'-map','[outv]','-map',f'{n}:a:0','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-tag:v','avc1','-r','24','-c:a','aac','-b:a','256k','-map_metadata','-1','-movflags','+faststart','clean.mp4']
    run(args)
    after=probe('clean.mp4');v=next(t for t in after['streams'] if t['codec_type']=='video');a=next(t for t in after['streams'] if t['codec_type']=='audio')
    assert int(v['nb_frames'])==total_frames
    assert abs(float(v['duration'])-total_frames/24)<1e-5
    assert abs(float(a['duration'])-count/rate)<.002
    run(['ffmpeg','-v','error','-xerror','-i','clean.mp4','-f','null','-'])
    ref,got=samples('voice.wav'),samples('clean.mp4')
    assert len(got)>=len(ref)-2
    limit=min(len(ref),len(got));global_corr=float(np.corrcoef(ref[:limit],got[:limit])[0,1]);checks=[]
    for i,window in enumerate(np.array_split(np.arange(limit),6)):
        x,y=ref[window],got[window]
        corr=float(np.corrcoef(x,y)[0,1])
        checks.append({'index':i+1,'start_seconds':int(window[0])/16000,'end_seconds':int(window[-1]+1)/16000,'zero_offset_correlation':corr})
    assert min(w['zero_offset_correlation'] for w in checks)>.99
    decoded_hash=run(['ffmpeg','-v','error','-i','clean.mp4','-map','0:a:0','-f','streamhash','-hash','sha256','-']).decode().strip().split('=')[-1]
    report={'status':'assembled_native_picture_original_voice_pending_perceptual_review','native_sources':source_records,'source_audio_sha256':cfg['voice_sha256'],'source_audio_sample_rate':rate,'source_audio_sample_count':count,'source_audio_duration_seconds':count/rate,'full_source_audio_preserved':True,'voice_processing':'AAC encoding only; no time processing, gain, fades, EQ or music','picture_processing':'Selected contiguous native frames joined at measured voice pauses; no synthesized mouth pass','video_sha256':sha('clean.mp4'),'video_bytes':Path('clean.mp4').stat().st_size,'video_duration_seconds':float(v['duration']),'audio_duration_seconds':float(a['duration']),'frame_count':total_frames,'width':720,'height':1280,'fps':24,'video_audio_decoded_sha256':decoded_hash,'zero_offset_correlation':global_corr,'audio_windows':checks,'strict_decode_passed':True,'limits':'Soundtrack preservation is not proof of visual lip sync or expressive naturalness. Native per-section timing QA is retained separately.'}
    Path('ASSEMBLY.json').write_text(json.dumps(report,indent=2)+'\n')
    slot=cfg['video_upload'];request=urllib.request.Request(slot['upload_url'],data=Path('clean.mp4').read_bytes(),headers={'Content-Type':slot['content_type']},method='PUT')
    with urllib.request.urlopen(request) as response: status=response.status
    assert status==200
    print('UPLOAD_OK clean.mp4 200',flush=True)
    print('ASSEMBLY_BASE64='+base64.b64encode(Path('ASSEMBLY.json').read_bytes()).decode(),flush=True)
    print('ASSEMBLY_SUMMARY='+json.dumps({'sha256':report['video_sha256'],'bytes':report['video_bytes'],'duration_seconds':report['video_duration_seconds'],'frame_count':total_frames,'media_id':slot['media_id'],'min_window_correlation':min(w['zero_offset_correlation'] for w in checks)}),flush=True)


if __name__=='__main__':
    main(json.loads(Path('inputs.json').read_text()))
