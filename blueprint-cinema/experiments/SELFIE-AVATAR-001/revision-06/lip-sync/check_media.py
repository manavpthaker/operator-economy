"""Probe full new native/result and decode; run in the media sandbox, without writing media."""
import hashlib,json,subprocess,sys
from pathlib import Path
native,result=map(Path,sys.argv[1:3])
section=int(sys.argv[3]) if len(sys.argv)>3 else None
assert section in (None,1,2,3)
expected_frames={1:484,2:378,3:431}.get(section,1293)
probes=[]
for p in (native,result):
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames',
        '-show_entries','stream=index,codec_name,codec_type,width,height,pix_fmt,r_frame_rate,duration,nb_read_frames,sample_rate,channels',
        '-show_entries','format=duration','-of','json',str(p)]))
    probes.append({'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'probe':probe})
for item in probes:
    video=next(stream for stream in item['probe']['streams'] if stream['codec_type']=='video')
    assert (video['width'],video['height'],video['r_frame_rate'],int(video['nb_read_frames']))==(720,1280,'24/1',expected_frames)
    assert abs(float(video['duration'])-expected_frames/24)<.00001
subprocess.check_call(['ffmpeg','-v','error','-xerror','-i',str(result),'-f','null','-'])
print(json.dumps({'section':section,'expected_frames':expected_frames,'media_probes':probes,'strict_full_decode':'passed',
    'native_soundtrack_comparison':'Not applicable: new native assembly contains video only.'}))

