import base64, difflib, gzip, hashlib, json, re, sys, urllib.request
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

def norm(t):
    t=t.lower().replace('’', "'")
    t=re.sub(r'\bgotta\b','got to',t)
    t=re.sub(r'\bwanna\b','want to',t)
    t=re.sub(r'\ba\s*\.?\s*i\.?\b','ai',t)
    t=re.sub(r'\bg\s*\.?\s*t\s*\.?\s*m\.?\b','gtm',t)
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?",t)

def stats(values):
    a=np.asarray(values)
    return {k:float(v) for k,v in zip(['min','p10','median','p90','max'],np.percentile(a,[0,10,50,90,100]))} if len(a) else None

cfg=json.loads(Path(sys.argv[1]).read_text())
folder=Path(sys.argv[1]).parent
model=WhisperModel('small.en',device='cpu',compute_type='int8')
reports=[]
for section in cfg['sections']:
    path=folder/f"native-{section['index']}.mp4"
    with urllib.request.urlopen(section['native_url'],timeout=45) as r:
        data=r.read()
    digest=hashlib.sha256(data).hexdigest()
    assert digest==section['native_sha256'], 'native bytes changed'
    path.write_bytes(data)
    segments,info=model.transcribe(str(path),beam_size=5,word_timestamps=True,vad_filter=True,condition_on_previous_text=False,language='en')
    raw=[]; segdata=[]
    for s in segments:
        segdata.append({'start':s.start,'end':s.end,'text':s.text,'avg_logprob':s.avg_logprob,'no_speech_prob':s.no_speech_prob})
        raw.extend({'word':w.word,'start':w.start,'end':w.end,'probability':w.probability} for w in s.words or [])
    expected=[]; exp_owner=[]
    for j,w in enumerate(section['source_words']):
        tokens=norm(w['text']);expected.extend(tokens);exp_owner.extend([j]*len(tokens))
    actual=[]; act_owner=[]
    for j,w in enumerate(raw):
        tokens=norm(w['word']);actual.extend(tokens);act_owner.extend([j]*len(tokens))
    assert norm(section['script'])==expected, 'section text differs from source canonical words'
    matcher=difflib.SequenceMatcher(None,expected,actual,autojunk=False)
    aligned={}; differences=[]
    for op,a,b,c,d in matcher.get_opcodes():
        if op=='equal':
            aligned.update({x:y for x,y in zip(range(a,b),range(c,d))})
        else:
            differences.append({'operation':op,'expected_token_range':[a,b],'actual_token_range':[c,d],'expected':expected[a:b],'actual':actual[c:d]})
    comparisons=[]
    for j,w in enumerate(section['source_words']):
        tokens=[k for k,owner in enumerate(exp_owner) if owner==j]
        if not all(k in aligned for k in tokens):
            comparisons.append({'word_index':w['word_index'],'text':w['text'],'fully_matched':False});continue
        ids=sorted(set(act_owner[aligned[k]] for k in tokens));nw=[raw[k] for k in ids]
        start=min(x['start'] for x in nw);end=max(x['end'] for x in nw)
        ss=w['start']-section['source_offset'];se=w['end']-section['source_offset']
        comparisons.append({'word_index':w['word_index'],'text':w['text'],'fully_matched':True,'source_start':ss,'source_end':se,'native_start':start,'native_end':end,'onset_lag_seconds':start-ss,'end_lag_seconds':end-se,'native_asr_words':[x['word'] for x in nw],'minimum_native_probability':min(x['probability'] for x in nw)})
    matched=[w for w in comparisons if w['fully_matched']]
    onsets=[w['onset_lag_seconds'] for w in matched]
    ends=[w['end_lag_seconds'] for w in matched]
    third=max(1,len(matched)//3)
    groups={'early':matched[:third],'middle':matched[third:2*third],'late':matched[2*third:]}
    laggroups={k:stats([w['onset_lag_seconds'] for w in v]) for k,v in groups.items()}
    summary={'index':section['index'],'exact_normalized_text':expected==actual,'matched_canonical_words':len(matched),'expected_canonical_words':len(comparisons),'onset_lag_seconds':stats(onsets),'end_lag_seconds':stats(ends),'onset_lag_by_third':laggroups,'median_centered_absolute_onset_p90_seconds':float(np.percentile(np.abs(np.asarray(onsets)-np.median(onsets)),90)) if onsets else None,'last_source_word':comparisons[-1], 'differences':differences}
    reports.append({'summary':summary,'native_url':section['native_url'],'native_sha256':digest,'native_bytes':len(data),'source_offset_seconds':section['source_offset'],'authored_text':section['script'],'native_transcript':''.join(w['word'] for w in raw).strip(),'raw_segments':segdata,'raw_words':raw,'word_comparisons':comparisons,'whisper_info':{'duration':info.duration,'duration_after_vad':info.duration_after_vad,'language':info.language,'language_probability':info.language_probability}})
report={'scope':'One small.en ASR pass for each of three R10 native videos; model loaded once; no paid generation, retiming, repair or lip-sync pass.','source_sha256':cfg['source_sha256'],'script_sha256':cfg['script_sha256'],'method':'faster-whisper small.en CPU int8; beam5; VAD; word timestamps; language en; no previous-text conditioning; no initial prompt. Exact normalized token sequence or explicit matched runs only.','normalization':'Case/punctuation/apostrophe style; AI/GTM spelling; gotta=got to, wanna=want to. No other wording equivalence.','lag_sign':'Positive means native word occurs later than source word within its exact section.','limitations':'ASR boundaries are estimates. Differences demonstrate speech-clock changes only when coherent across words; they do not measure visemes, prove mouth alignment, establish audible identity, or grant subjective acceptance. Same script does not imply same waveform.','sections':reports}
payload=json.dumps(report,indent=2).encode()
print('REPORT_GZIP_BASE64='+base64.b64encode(gzip.compress(payload)).decode())
print('SUMMARY='+json.dumps([s['summary'] for s in reports]))
