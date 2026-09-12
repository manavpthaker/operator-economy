import sys,json,re,hashlib,urllib.request,wave,contextlib
from pathlib import Path
from faster_whisper import WhisperModel
expected="It’s hard to leave an app alone when it looks like something you could sell.\n\nI’ve gotta get better at that. With AI, I can get something looking pretty good before I’ve worked out why anyone would actually use it.\n\nSo I’m building this GTM Engine to help me work through that. It looks at the code, then researches who might use it and what they’re doing already. Because if they’ve already got a way that works, why would they bother with mine?\n\nBut I still wanna let someone try it on something they actually need to do. Do they choose mine, or go back to what they were using before?\n\nMaybe I’ve gotta build a bit more to find that out. That’s fine. But I’ve got other projects I wanna work on too, so I want more to go on than how good this one looks.\n\nAnd if I just enjoy using it myself, I can leave it at that. It’s okay to have a hobby.\n\nSo you guys tell me, what made you decide to turn something you’d built into a business?\n"
url,stage=sys.argv[1:3]
audio=Path('/home/user/r4-'+stage+'.wav')
with urllib.request.urlopen(url) as response: audio.write_bytes(response.read())
def norm(s):
    s=s.lower().replace('’',"'")
    s=re.sub(r'\ba\s*\.?\s*i\.?\b','ai',s)
    s=re.sub(r'\bg\s*\.?\s*t\s*\.?\s*m\.?\b','gtm',s)
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?",s)
model=WhisperModel('base.en',device='cpu',compute_type='int8')
segments,info=model.transcribe(str(audio),beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=True,language='en')
segments=list(segments)
text=''.join(s.text for s in segments).strip()
words=[{'text':w.word,'start':w.start,'end':w.end,'probability':w.probability} for s in segments for w in (s.words or [])]
with wave.open(str(audio)) as f: duration=f.getnframes()/f.getframerate()
result={'stage':stage,'source_url':url,'source_sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),
'transcript':text,'normalized_exact_match':norm(text)==norm(expected),'expected_word_count':len(expected.split()),
'expected_normalized_words':norm(expected),'recognized_normalized_words':norm(text),
'words':words,'duration_seconds':duration,'engine':'faster-whisper base.en; beam_size=5; no initial prompt',
'normalization':'Lowercase, apostrophe style, punctuation and equivalent spelled acronym letters AI/GTM only; no synonyms or omitted-word allowances.',
'perceptual_review':'Not performed; ASR supports transcript accuracy, not voice naturalness or identity approval.'}
print(json.dumps(result))

