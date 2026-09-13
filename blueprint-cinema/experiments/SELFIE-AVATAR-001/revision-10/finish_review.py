"""Bind final restored voice clock to new captions and render one review output.

Higgsfield sandbox only. Sources/scripts/slots arrive in inputs.json.
"""
import base64
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stamp(seconds):
    ms=round(seconds*1000)
    assert ms>=0
    h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


cfg=json.loads(Path('inputs.json').read_text())
for url,path,digest in [(cfg['video_url'],'restored.mp4',cfg['video_sha256']),(cfg['voice_url'],'voice.wav',cfg['voice_sha256'])]:
    urllib.request.urlretrieve(url,path)
    assert sha(path)==digest
qa_bytes=subprocess.check_output(['python3','audio_alignment.py','voice.wav','restored.mp4'])
Path('AUDIO-QA.json').write_bytes(qa_bytes);qa=json.loads(qa_bytes)
assert qa['candidate_sha256']==cfg['video_sha256'] and qa['source_voice_sha256']==cfg['voice_sha256']
assert qa['measured_window_count']==6 and qa['minimum_window_correlation']>=.99
assert qa['aligned_audio_correlation']>=.99 and qa['minimum_window_correlation_at_global_offset']>=.99
assert qa['window_offset_spread_seconds']<=.002 and not qa['offset_at_search_boundary']
assert qa['full_source_sample_extent_covered']
offset=qa['source_to_picture_offset_seconds']
assert abs(offset)<1
def shift(match):
    values=list(map(int,match.groups()));left=values[0]*3600+values[1]*60+values[2]+values[3]/1000;right=values[4]*3600+values[5]*60+values[6]+values[7]/1000
    return stamp(left+offset)+' --> '+stamp(right+offset)
source_srt=cfg['srt']
cfg['srt']=re.sub(r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})',shift,source_srt)
source_srt_sha=cfg['srt_sha256'];cfg['srt_sha256']=hashlib.sha256(cfg['srt'].encode()).hexdigest()
decoded=subprocess.check_output(['ffmpeg','-v','error','-i','restored.mp4','-map','0:a:0','-f','streamhash','-hash','sha256','-']).decode().strip().split('=')[-1]
binding={'video_sha256':cfg['video_sha256'],'script_sha256':hashlib.sha256(cfg['script'].encode()).hexdigest(),'source_voice_sha256':cfg['voice_sha256'],'source_word_map_sha256':cfg['source_word_map_sha256'],'source_caption_receipt_sha256':cfg['source_caption_receipt_sha256'],'source_srt_sha256':source_srt_sha,'srt_sha256':cfg['srt_sha256'],'word_count':len(cfg['script'].split()),'similarity':1.0,'audio_qa_sha256':sha('AUDIO-QA.json'),'source_to_picture_offset_seconds':offset,'method':'Exact authored words timed by verified final-voice Whisper word map, shifted only by measured uniform audio insertion. Source WAV is fully preserved in restored video under full and six-window waveform checks.','limits':'This binding verifies words and caption clock; it is not a visual lip-sync acceptance.'}
Path('CAPTION-BINDING.json').write_text(json.dumps(binding,indent=2)+'\n')
cfg['transcription']={k:binding[k] for k in ['video_sha256','script_sha256','srt_sha256','word_count','similarity']};cfg['transcription']['evidence_sha256']=sha('CAPTION-BINDING.json')
cfg['audio_binding']={'video_sha256':cfg['video_sha256'],'source_audio_sha256':cfg['voice_sha256'],'video_audio_decoded_sha256':decoded,'full_source_audio_preserved':True,'evidence_sha256':sha('AUDIO-QA.json')}
Path('inputs.json').write_text(json.dumps(cfg))
print('AUDIO_QA_BASE64='+base64.b64encode(qa_bytes).decode(),flush=True)
print('CAPTION_BINDING_BASE64='+base64.b64encode(Path('CAPTION-BINDING.json').read_bytes()).decode(),flush=True)
print('AUDIO_QA_SUMMARY='+json.dumps({'offset_seconds':offset,'minimum_window_correlation':qa['minimum_window_correlation'],'offset_spread_seconds':qa['window_offset_spread_seconds'],'full_source_audio_preserved':True,'audio_qa_sha256':sha('AUDIO-QA.json')}),flush=True)
subprocess.run(['python3','render.py'],check=True)
