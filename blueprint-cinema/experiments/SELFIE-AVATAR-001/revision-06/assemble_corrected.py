"""Assemble matched R6 picture results with one continuous source soundtrack.

Run only in the media sandbox after all per-section returned audio clocks are
verified. No source speech time stretch or sample removal is permitted.
"""
import hashlib,json,subprocess,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(a):return subprocess.check_output(a)
def probe(p):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]))
def put(p,s):
    req=urllib.request.Request(s['upload_url'],data=Path(p).read_bytes(),method='PUT',headers={'Content-Type':s['content_type']})
    with urllib.request.urlopen(req) as response:assert response.status==200
    return {'url':s['url'],'media_id':s['media_id'],'sha256':sha(p),'bytes':Path(p).stat().st_size,'upload_http':200}

def main(cfg):
    counts=[484,378,431]
    for i,source in enumerate(cfg['sections']):
        assert abs(source['measured_audio_offset_seconds'])<=.0000625
        assert source['audio_correlation']>=.99
        path=f'sync-{i+1}.mp4';urllib.request.urlretrieve(source['url'],path)
        assert sha(path)==source['sha256']
        stream=next(s for s in probe(path)['streams'] if s['codec_type']=='video')
        assert (stream['width'],stream['height'],stream['r_frame_rate'])==(720,1280,'24/1')
        assert int(stream['nb_frames'])==counts[i]
    urllib.request.urlretrieve(cfg['voice_url'],'source.wav')
    assert sha('source.wav')==cfg['voice_sha256']
    command=['ffmpeg','-y','-v','error']
    for i in range(3):command+=['-i',f'sync-{i+1}.mp4']
    command+=['-i','source.wav']
    fc=';'.join(f'[{i}:v]trim=end_frame={n},setpts=PTS-STARTPTS,setsar=1[v{i}]' for i,n in enumerate(counts))
    fc+=';[v0][v1][v2]concat=n=3:v=1:a=0[v];[3:a]apad=whole_len=2586000[a]'
    command+=['-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-tag:v','avc1','-r','24','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','r6-clean.mp4']
    run(command)
    metadata=probe('r6-clean.mp4');v=next(s for s in metadata['streams'] if s['codec_type']=='video')
    assert int(v['nb_frames'])==1293 and abs(float(v['duration'])-53.875)<.00001
    run(['ffmpeg','-v','error','-xerror','-i','r6-clean.mp4','-f','null','-'])
    qa=json.loads(run(['python3','compare_audio.py','source.wav','r6-clean.mp4']))
    assert qa['aligned_overlap_seconds']==qa['reference_duration_seconds']
    assert abs(qa['audio_insertion_offset_seconds'])<=.0000625
    assert min(qa['segment_correlations'].values())>=.99
    assert qa['window_offset_spread_seconds']<=.0000625
    Path('AUDIO-QA.json').write_text(json.dumps(qa,indent=2)+'\n')
    frames=[107,111,169,180,184,189,197,201,794,799,801,805,808,812,1234,1238,1254,1258,1263,1292]
    selection='+'.join(f'eq(n\\,{f})' for f in frames)
    run(['ffmpeg','-v','error','-i','r6-clean.mp4','-vf',f'select={selection},scale=270:480','-fps_mode','vfr','-frames:v',str(len(frames)),'qa-%02d.png'])
    sheet=Image.new('RGB',(1080,2560),'#eeeeee');draw=ImageDraw.Draw(sheet)
    for i,f in enumerate(frames):
        x,y=i%4*270,i//4*512;sheet.paste(Image.open(f'qa-{i+1:02d}.png').convert('RGB'),(x,y+32));draw.text((x+6,y+10),f'Frame {f} | {f/24:.3f}s',fill='#111111')
    sheet.save('r6-contact.jpg',quality=94)
    output=put('r6-clean.mp4',cfg['video_upload']);contact=put('r6-contact.jpg',cfg['contact_upload'])
    output.update({'width':720,'height':1280,'frame_rate':'24/1','frame_count':1293,'duration_seconds':53.875,'source_audio_continuous':True,'only_added_audio_samples':49266})
    print(json.dumps({'output':output,'contact':contact,'audio_qa':qa,'audio_qa_sha256':sha('AUDIO-QA.json'),'probe':metadata,'strict_full_decode':'passed','per_section_evidence_sha256':cfg['per_section_evidence_sha256']}),flush=True)

if __name__=='__main__':main(json.loads(Path('inputs.json').read_text()))
