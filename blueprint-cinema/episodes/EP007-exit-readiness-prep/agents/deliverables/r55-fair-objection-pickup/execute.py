"""R55 fair-objection pickup: one Google guide read, one ElevenLabs transfer. No retries."""
from pathlib import Path
import sys, json, hashlib, urllib.request, urllib.error, datetime, base64, math
ROOT=Path('/Users/brownmanbrain/GitHub/operator-economy'); OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'operator-blueprint-v2/02-narration-production/tools')); import calibrate as cal
DIR=ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/direction/r55-s12-other-scales/presenter-a'
R39=ROOT/'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r39-question-performance/provider/CALLBACK-PICKUP-REQUEST.json'
auth=json.loads((DIR/'PICKUP-AUTHORIZATION.json').read_text()); assert auth['caps']=={'google_usd':0.05,'elevenlabs_credits':250,'fal_usd':2.0,'retries':0}
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
save=lambda n,o:(OUT/n).write_text(json.dumps(o,indent=2)+'\n')
def req(url,method='GET',headers=None,body=None):
    r=urllib.request.Request(url,data=body,headers=headers or {},method=method)
    try:
        with urllib.request.urlopen(r,timeout=600) as res:
            return res.status,res.read(),{k.lower():v for k,v in res.headers.items() if k.lower() in ['request-id','x-request-id','character-cost','x-character-cost','content-type']}
    except urllib.error.HTTPError as e: return e.code,e.read(),{}
def account(name):
    s,raw,_=req('https://api.elevenlabs.io/v1/user/subscription',headers={'xi-api-key':cal.read_dotenv_key('ELEVENLABS_API_KEY')}); assert s==200
    d=json.loads(raw); sel={k:d.get(k) for k in ['tier','character_count','character_limit']}; save(name,{'at_utc':stamp(),'account':sel}); return sel
mode=sys.argv[1]
if mode=='google':
    assert not (OUT/'GOOGLE-SUBMISSION-INTENT.json').exists(),'no retry'
    body=(DIR/'GOOGLE-PICKUP-GUIDE-BODY.json').read_bytes(); b=json.loads(body)
    h={'Authorization':f'Bearer {cal.google_access_token()}','Content-Type':'application/json; charset=utf-8'}
    p=cal.google_quota_project()
    if p: h['x-goog-user-project']=p
    save('GOOGLE-SUBMISSION-INTENT.json',{'at_utc':stamp(),'body_sha256':hashlib.sha256(body).hexdigest(),'cap_usd':0.05,'max_attempts':1})
    try: s,raw,sh=req('https://us-texttospeech.googleapis.com/v1/text:synthesize','POST',h,body)
    except Exception as e: save('GOOGLE-ERROR.json',{'error_class':type(e).__name__,'no_retry':True}); raise SystemExit('transport error; no retry')
    if s!=200: save('GOOGLE-ERROR.json',{'http_status':s,'body':raw.decode('utf-8','replace'),'no_retry':True}); raise SystemExit(f'Google HTTP{s}')
    res=json.loads(raw); wav=base64.b64decode(res.pop('audioContent')); f=OUT/'context-guide.wav'; f.write_bytes(wav)
    info=cal.probe(f); cost=info['duration_seconds']*25*20/1e6+len(b['input']['prompt']+b['input']['text'])/1e6
    save('GOOGLE-RECEIPT.json',{'at_utc':stamp(),'http_status':s,'headers':sh,'metadata':res,'media':info,'estimated_cost_usd':cost,'calls':1,'retries':0}); print(json.dumps({'media':info,'usd':cost}))
elif mode=='transfer':
    assert not (OUT/'ELEVEN-SUBMISSION-INTENT.json').exists(),'no retry'
    g=OUT/'context-guide.wav'; info=cal.probe(g); credits=math.ceil(info['duration_seconds']*1000/60); assert credits<=250,credits
    before=account('ELEVEN-ACCOUNT-BEFORE.json'); assert before['character_limit']-before['character_count']>=credits
    t=json.loads(R39.read_text())['transfer']; body,ct=cal.multipart(t['fields'],g.name,g.read_bytes())
    save('ELEVEN-SUBMISSION-INTENT.json',{'at_utc':stamp(),'url':t['url'],'fields':t['fields'],'guide':info,'body_sha256':hashlib.sha256(body).hexdigest(),'estimated_credits':credits,'cap_credits':250,'calls':1,'retries':0})
    try: s,raw,sh=req(t['url'],'POST',{'xi-api-key':cal.read_dotenv_key('ELEVENLABS_API_KEY'),'Content-Type':ct,'Accept':'*/*'},body)
    except Exception as e: save('ELEVEN-ERROR.json',{'error_class':type(e).__name__,'no_retry':True}); raise SystemExit('transport error; no retry')
    if s!=200: save('ELEVEN-ERROR.json',{'http_status':s,'body':raw.decode('utf-8','replace'),'no_retry':True}); raise SystemExit(f'Eleven HTTP{s}')
    f=OUT/'context-original-c.wav'; cal.wav_from_pcm(raw,48000,f); after=account('ELEVEN-ACCOUNT-AFTER.json')
    save('ELEVEN-RECEIPT.json',{'at_utc':stamp(),'http_status':s,'headers':sh,'media':cal.probe(f),'account_delta':after['character_count']-before['character_count'],'calls':1,'retries':0})
    print(json.dumps({'media':cal.probe(f),'headers':sh,'delta':after['character_count']-before['character_count']}))
