"""Run R9 signal QA and caption render in one producing sandbox lease."""
import base64,hashlib,json,subprocess,urllib.request
from pathlib import Path

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
c=json.loads(Path('inputs.json').read_text());v=json.loads(c['voice_report_json'])
for url,path,digest in [(c['video_url'],'candidate.mp4',c['video_sha256']),(v['upload']['url'],'voice.wav',v['output_sha256'])]:
    urllib.request.urlretrieve(url,path);assert sha(path)==digest
qa_bytes=subprocess.check_output(['python3','audio_qa.py','voice.wav','candidate.mp4'])
Path('AUDIO-QA.json').write_bytes(qa_bytes);qa=json.loads(qa_bytes)
assert qa['offset_at_search_boundary'] is False
assert abs(qa['audio_insertion_offset_seconds'])<=1/16000
assert qa['window_offset_spread_seconds']<=.002
assert min(qa['segment_correlations'].values())>=.99
assert qa['aligned_overlap_seconds']>=v['unpadded_duration_seconds']
assert qa['original_content_end_in_output_seconds']<=float(qa['probe']['format']['duration'])+.002
vs=next(s for s in qa['probe']['streams'] if s['codec_type']=='video')
assert (vs['width'],vs['height'],vs['r_frame_rate'])==(720,1280,'24/1')
c['audio_offset_seconds']=qa['audio_insertion_offset_seconds']
c['audio_alignment']={'video_sha256':c['video_sha256'],'source_voice_sha256':v['output_sha256'],'full_source_voice_preserved':True,'uniform_offset':True,'offset_seconds':qa['audio_insertion_offset_seconds'],'max_drift_seconds':qa['window_offset_spread_seconds'],'min_window_correlation':min(qa['segment_correlations'].values()),'evidence_sha256':sha('AUDIO-QA.json')}
Path('inputs.json').write_text(json.dumps(c))
print('AUDIO_QA_BASE64='+base64.b64encode(qa_bytes).decode(),flush=True)
print('AUDIO_QA_SUMMARY='+json.dumps(c['audio_alignment']),flush=True)
subprocess.run(['python3','render.py'],check=True)
