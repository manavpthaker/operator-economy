"""Independent ASR/endpoint QA. Run in Higgsfield sandbox with cfg JSON."""
import difflib,hashlib,io,json,re,sys,urllib.request,wave
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

def norm(text):
    text=text.lower().replace('’',"'")
    text=re.sub(r'\bgotta\b','got to',text)
    text=re.sub(r'\bwanna\b','want to',text)
    text=re.sub(r'\ba\s*\.?\s*i\.?\b','ai',text)
    text=re.sub(r'\bg\s*\.?\s*t\s*\.?\s*m\.?\b','gtm',text)
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?",text)

cfg=json.loads(Path(sys.argv[1]).read_text())
expected=cfg['script']
assert hashlib.sha256(expected.encode()).hexdigest()==cfg['script_sha256']
url=cfg['audio_url']
with urllib.request.urlopen(url,timeout=45) as r: data=r.read()
digest=hashlib.sha256(data).hexdigest()
assert digest==cfg['audio_sha256']
path=Path('/home/user/r10-'+cfg['stage']+'-qa.wav');path.write_bytes(data)
with wave.open(io.BytesIO(data)) as w:
 rate,channels,width,count=w.getframerate(),w.getnchannels(),w.getsampwidth(),w.getnframes()
 assert channels==1 and width==2
 samples=np.frombuffer(w.readframes(count),dtype='<i2').astype(float)/32768
model_name=cfg.get('model','small.en')
model=WhisperModel(model_name,device='cpu',compute_type='int8')
segments,info=model.transcribe(str(path),beam_size=5,word_timestamps=True,vad_filter=True,
 condition_on_previous_text=False,language='en')
segments=list(segments)
transcript=''.join(s.text for s in segments).strip()
words=[{'text':w.word,'start':w.start,'end':w.end,'probability':w.probability} for s in segments for w in (s.words or [])]
en,rn=norm(expected),norm(transcript)
exact=en==rn
differences=[{'operation':tag,'expected':en[i:j],'recognized':rn[k:l]} for tag,i,j,k,l in difflib.SequenceMatcher(a=en,b=rn,autojunk=False).get_opcodes() if tag!='equal']
timings=[];pos=0;map_complete=False
if exact:
 for index,word in enumerate(expected.split(),1):
  match=None
  for group_count in range(1,5):
   group=words[pos:pos+group_count]
   if len(group)==group_count and norm(' '.join(w['text'] for w in group))==norm(word):
    match=group;break
  if match is None:break
  timings.append({'word_index':index,'text':word,'start':match[0]['start'],'end':match[-1]['end'],
   'asr_words':[w['text'].strip() for w in match],
   'minimum_asr_probability':round(min(w['probability'] for w in match),4)})
  pos+=len(match)
 map_complete=len(timings)==len(expected.split()) and pos==len(words)
def rms(window):
 a=samples[-round(rate*window):]
 return float(np.sqrt(np.mean(a*a)))
result={'stage':cfg['stage'],'source_url':url,'source_sha256':digest,'script_sha256':cfg['script_sha256'],
 'duration_seconds':count/rate,'sample_count':count,'sample_rate_hz':rate,
 'transcript':transcript,'normalized_exact_match':exact,'expected_word_count':len(expected.split()),
 'differences':differences,'word_timing_map_complete':map_complete,'script_word_timings':timings,
 'words':[[w['text'],w['start'],w['end'],round(w['probability'],4)] for w in words],
 'engine':'faster-whisper '+model_name+'; beam5; VAD; no previous-text conditioning; no initial prompt',
 'normalization':'Punctuation/case/apostrophe style; spelled AI/GTM; gotta/got to and wanna/want to only. No omission or paraphrase allowance; contractions such as you\'d remain required.',
 'audio_probe':{'sample_rate_hz':rate,'sample_count':count,'duration_seconds':count/rate,
  'final_sample':float(samples[-1]),'last10ms_rms':rms(.01),'last60ms_rms':rms(.06),'last300ms_rms':rms(.3),
  'peak_absolute_amplitude':float(np.max(abs(samples))),'full_scale_sample_count':int(np.count_nonzero((samples>=32767/32768)|(samples<=-1)))},
 'perceptual_review':'Not performed. ASR supports words, not naturalness or identity acceptance.'}
result['split_candidates_24fps']=[]
if map_complete:
 for end_index in (60,129):
  prev,nxt=timings[end_index-1],timings[end_index]
  lo,hi=prev['end']+.04,nxt['start']-.04
  candidates=[]
  for frame in range(int(np.ceil(lo*24)),int(np.floor(hi*24))+1):
   t=frame/24
   window=samples[max(0,round((t-.025)*rate)):min(count,round((t+.025)*rate))]
   energy=float(np.sqrt(np.mean(window*window)))
   candidates.append({'frame':frame,'seconds':t,'sample':round(t*rate),'rms_50ms':energy,'dbfs':float(20*np.log10(max(energy,1e-12)))})
  selected=min(candidates,key=lambda x:x['rms_50ms']) if candidates else None
  result['split_candidates_24fps'].append({'after_word_index':end_index,'previous_word':prev,'next_word':nxt,'search_gap_seconds':[lo,hi],'selected':selected,'candidates':candidates})
import base64,gzip
report_bytes=(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode()
Path('/home/user/r10-'+cfg['stage']+'-qa-report.json').write_bytes(report_bytes)
print('REPORT_GZIP_BASE64='+base64.b64encode(gzip.compress(report_bytes)).decode(),flush=True)
print('SUMMARY='+json.dumps({k:result[k] for k in ['stage','source_sha256','duration_seconds','normalized_exact_match','word_timing_map_complete','differences','audio_probe']}),flush=True)

