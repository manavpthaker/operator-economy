"""R7 media-sandbox-only trim and frame QA for one opening."""
import base64,hashlib,json,subprocess,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(a):return subprocess.check_output(a)
def put(p,s):
    r=urllib.request.Request(s['upload_url'],data=Path(p).read_bytes(),method='PUT',headers={'Content-Type':s['content_type']})
    with urllib.request.urlopen(r) as h:assert h.status==200
    return {'url':s['url'],'media_id':s['media_id'],'sha256':sha(p),'bytes':Path(p).stat().st_size,'upload_http':200}

c=json.loads(Path('inputs.json').read_text())
urllib.request.urlretrieve(c['native_url'],'native.mp4')
n=c['frame_count']
probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json','native.mp4']))
v=next(x for x in probe['streams'] if x['codec_type']=='video')
assert int(v['nb_frames'])>=n
run(['ffmpeg','-v','error','-y','-i','native.mp4','-vf',f'trim=start_frame=0:end_frame={n},setpts=PTS-STARTPTS','-an','-c:v','libx264','-preset','fast','-crf','15','-pix_fmt','yuv420p','-tag:v','avc1','-r','24','-movflags','+faststart','picture.mp4'])
p=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json','picture.mp4']))
assert len(p['streams'])==1
v=p['streams'][0]
assert int(v['nb_frames'])==n and (v['width'],v['height'],v['r_frame_rate'])==(720,1280,'24/1')
run(['ffmpeg','-v','error','-xerror','-i','picture.mp4','-f','null','-'])
vr=put('picture.mp4',c['slots'][0]);vr.update({'frame_count':n,'frame_rate':'24/1','width':720,'height':1280,'duration_seconds':n/24,'audio_stream_count':0,'local_path':'blueprint-cinema/experiments/SELFIE-AVATAR-001/media/revision-07/picture.mp4'})
times=[3.5,3.875,4.25,4.5,4.875,5.25,5.667,6.125]
sheet=Image.new('RGB',(960,840),'#eeeeee');d=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
    f=f'frame-{i}.png';run(['ffmpeg','-v','error','-y','-ss',str(t),'-i','picture.mp4','-frames:v','1',f])
    im=Image.open(f);im.thumbnail((240,396));x=(i%4)*240;y=(i//4)*420;sheet.paste(im,(x,y+22));d.text((x+8,y+3),f'{t:.3f}s',fill='black')
sheet.save('smile-contact.jpg',quality=92)
ir=put('smile-contact.jpg',c['slots'][1])
report={'video':vr,'native':{'url':c['native_url'],'sha256':sha('native.mp4'),'probe':probe},'matched_probe':p,'contact':ir,'limits':'Still frames describe facial shape only; no synchronized perceptual lip-sync verdict.'}
b=(json.dumps(report,indent=2)+'\n').encode();Path('VIDEO-QA.json').write_bytes(b)
print(json.dumps({'report_sha256':hashlib.sha256(b).hexdigest(),'report_base64':base64.b64encode(b).decode(),'video':vr,'contact':ir}),flush=True)
