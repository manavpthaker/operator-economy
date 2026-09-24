"""Prepare exact-duration R6 inputs in the media sandbox; no speech retiming."""
import hashlib,json,subprocess,sys,urllib.request,wave
from pathlib import Path

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(a): return subprocess.check_output(a)
def put(p,s):
    r=urllib.request.Request(s['upload_url'],data=Path(p).read_bytes(),method='PUT',headers={'Content-Type':s['content_type']})
    with urllib.request.urlopen(r) as h: assert h.status==200
    return {'url':s['url'],'media_id':s['media_id'],'sha256':sha(p),'bytes':Path(p).stat().st_size,'upload_http':200}

def main(cfg):
    for source in cfg['sources']:
        urllib.request.urlretrieve(source['url'],source['path'])
        assert sha(source['path'])==source['sha256']
    with wave.open('source.wav') as w:
        assert (w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes())==(1,2,48000,2536734)
        pcm=w.readframes(w.getnframes())
    frame_counts=[484,378,431]; starts=[0,484,862]
    sample_starts=[0,968000,1724000]; sample_ends=[968000,1724000,2536734]
    sections=[]
    for i,n in enumerate(frame_counts):
        vp=f'picture-{i+1}.mp4';ap=f'voice-{i+1}.wav';count=n*2000
        run(['ffmpeg','-v','error','-y','-i','native.mp4','-vf',f'trim=start_frame={starts[i]}:end_frame={starts[i]+n},setpts=PTS-STARTPTS','-an','-c:v','libx264','-preset','fast','-crf','15','-pix_fmt','yuv420p','-tag:v','avc1','-r','24','-movflags','+faststart',vp])
        probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',vp]))
        assert len(probe['streams'])==1
        v=probe['streams'][0];assert v['codec_type']=='video' and int(v['nb_frames'])==n and (v['width'],v['height'],v['r_frame_rate'])==(720,1280,'24/1')
        part=pcm[sample_starts[i]*2:sample_ends[i]*2];zeros=count-len(part)//2
        assert zeros==([0,0,49266][i]);part+=b'\0'*(zeros*2)
        with wave.open(ap,'wb') as w:
            w.setparams((1,2,48000,count,'NONE','not compressed'));w.writeframes(part)
        vr=put(vp,cfg['slots'][i*2]);ar=put(ap,cfg['slots'][i*2+1])
        vr.update({'width':720,'height':1280,'frame_rate':'24/1','frame_count':n,'duration_seconds':n/24,'audio_stream_count':0,'local_path':f'blueprint-cinema/experiments/SELFIE-AVATAR-001/media/revision-06/picture-{i+1}.mp4'})
        ar.update({'sample_rate_hz':48000,'sample_count':count,'channels':1,'sample_width_bytes':2,'duration_seconds':count/48000,'source_sample_range':[sample_starts[i],sample_ends[i]],'tail_silence_samples':zeros,'actual_container':'RIFF WAV PCM signed16 little-endian','host_note':'Higgsfield audio reservation uses an mp3 URL and audio/mpeg header; uploaded body remains the verified WAV bytes.','local_path':f'blueprint-cinema/experiments/SELFIE-AVATAR-001/media/revision-06/voice-{i+1}.wav'})
        sections.append({'index':i+1,'video':vr,'audio':ar})
    print(json.dumps({'sections':sections,'source_voice_sha256':sha('source.wav'),'native_sha256':sha('native.mp4'),'speech_retimed':False,'only_added_samples':49266}),flush=True)

if __name__=='__main__':main(json.loads(Path('inputs.json').read_text()))
