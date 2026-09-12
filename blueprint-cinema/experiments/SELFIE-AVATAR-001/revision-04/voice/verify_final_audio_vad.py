import sys,json,re,hashlib,urllib.request,wave,contextlib
from pathlib import Path
from faster_whisper import WhisperModel
expected="It’s hard to leave an app alone when it looks like something you could sell.\n\nI’ve gotta get better at that. With AI, I can get something looking pretty good before I’ve worked out why anyone would actually use it.\n\nSo I’m building this GTM Engine to help me work through that. It looks at the code, then researches who might use it and what they’re doing already. Because if they’ve already got a way that works, why would they bother with mine?\n\nBut I still wanna let someone try it on something they actually need to do. Do they choose mine, or go back to what they were using before?\n\nMaybe I’ve gotta build a bit more to find that out. That’s fine. But I’ve got other projects I wanna work on too, so I want more to go on than how good this one looks.\n\nAnd if I just enjoy using it myself, I can leave it at that. It’s okay to have a hobby.\n\nSo you guys tell me, what made you decide to turn something you’d built into a business?\n"
url,stage=sys.argv[1:3]
audio=Path('/home/user/r4-'+stage+'.wav')
with urllib.request.urlopen(url) as response: audio.write_bytes(response.read())
def norm(s):
    s=s.lower().replace('’',"'")
    s=re.sub(r'\bgotta\b','got to',s)
    s=re.sub(r'\bwanna\b','want to',s)
    s=re.sub(r'\ba\s*\.?\s*i\.?\b','ai',s)
    s=re.sub(r'\bg\s*\.?\s*t\s*\.?\s*m\.?\b','gtm',s)
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?",s)
model=WhisperModel('small.en',device='cpu',compute_type='int8')
segments,info=model.transcribe(str(audio),beam_size=5,word_timestamps=True,vad_filter=True,condition_on_previous_text=False,language='en')
segments=list(segments)
text=''.join(s.text for s in segments).strip()
words=[{'text':w.word,'start':w.start,'end':w.end,'probability':w.probability} for s in segments for w in (s.words or [])]
with wave.open(str(audio)) as f: duration=f.getnframes()/f.getframerate()
result={'stage':stage,'source_url':url,'source_sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),
'transcript':text,'normalized_exact_match':norm(text)==norm(expected),'expected_word_count':len(expected.split()),
'expected_normalized_words':norm(expected),'recognized_normalized_words':norm(text),
'words':words,'duration_seconds':duration,'engine':'faster-whisper small.en; beam_size=5; VAD; no previous-text conditioning; no initial prompt',
'normalization':'Lowercase, apostrophe style, punctuation, equivalent AI/GTM letters, and owner-workflow accepted colloquial spelling equivalents gotta/got to and wanna/want to. The final contraction you’d must remain.',
'perceptual_review':'Not performed; ASR supports transcript accuracy, not voice naturalness or identity approval.'}

import numpy as np
with wave.open(str(audio)) as w:
 rate=w.getframerate(); sample_count=w.getnframes()
 samples=np.frombuffer(w.readframes(sample_count),dtype='<i2').astype(float)/32768.
bounds=[]
for label,ending in [('after_word_68','already.'),('after_word_124','fine.')]:
 idx=next(i for i,w in enumerate(words) if w['text'].strip().lower()==ending)
 previous,nextword=words[idx],words[idx+1]
 lo,hi=previous['end']+.06,nextword['start']-.06
 if hi<=lo:
  bounds.append({'label':label,'status':'no_safe_ASR_gap','previous':previous,'next':nextword}); continue
 candidates=[]
 for frame in range(int(np.ceil(lo*24)),int(np.floor(hi*24))+1):
  t=frame/24
  win=samples[max(0,round((t-.025)*rate)):min(sample_count,round((t+.025)*rate))]
  rms=float(np.sqrt(np.mean(win*win)))
  candidates.append({'frame_index':frame,'seconds':t,'sample_index':round(t*rate),'rms_50ms':rms,
   'peak_50ms':float(abs(win).max()),'rms_dbfs':20*np.log10(max(rms,1e-12))})
 if candidates:
  quiet=[c for c in candidates if c['rms_dbfs']<=-55]
  pool=quiet or candidates
  choice=min(pool,key=lambda c:abs(c['seconds']-(lo+.75*(hi-lo)))) if quiet else min(pool,key=lambda c:c['rms_50ms'])
  bounds.append({'label':label,'status':'quiet_candidate' if quiet else 'lowest_energy_candidate','previous':previous,'next':nextword,'safe_ASR_gap':[lo,hi],'selected':choice,'candidates':candidates})
result['split_candidates_24fps']=bounds
result['audio_probe']={'sample_rate_hz':rate,'sample_count':sample_count,'duration_seconds':sample_count/rate,
'final_sample':float(samples[-1]),'last10ms_rms':float(np.sqrt(np.mean(samples[-round(rate*.01):]**2))),
'last60ms_rms':float(np.sqrt(np.mean(samples[-round(rate*.06):]**2))),
'last300ms_rms':float(np.sqrt(np.mean(samples[-round(rate*.3):]**2)))}

result.pop('expected_normalized_words'); result.pop('recognized_normalized_words'); result['words']=[[w['text'],w['start'],w['end'],round(w['probability'],4)] for w in words]; print(json.dumps(result))

