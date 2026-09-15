from pathlib import Path
import sys, json, hashlib, urllib.request, urllib.error, datetime, base64, math

ROOT = Path('/Users/brownmanbrain/GitHub/operator-economy')
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'operator-blueprint-v2/02-narration-production/tools'))
import calibrate as cal
WO = ROOT / 'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/work-orders/r39-callback-production.json'
work = json.loads(WO.read_text())
for item in work['inputs']:
    assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'], item['path']
PROVIDER = ROOT / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r39-question-performance/provider'
auth=json.loads((PROVIDER/'GENERATION-AUTHORIZATION.json').read_text())
assert auth['retries']==0 and auth['caps']['google_usd']==0.05 and auth['caps']['elevenlabs_credits']==250

def save(name, obj):
    (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')

def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def safe_request(url, method='GET', headers=None, body=None):
    req=urllib.request.Request(url,data=body,headers=headers or {},method=method)
    try:
        with urllib.request.urlopen(req,timeout=600) as res:
            raw=res.read()
            return res.status, raw, {k.lower():v for k,v in res.headers.items() if k.lower() in ['request-id','x-request-id','character-cost','x-character-cost','content-type']}
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(), {}

def account(name):
    key=cal.read_dotenv_key('ELEVENLABS_API_KEY')
    status, raw, headers=safe_request('https://api.elevenlabs.io/v1/user/subscription',headers={'xi-api-key':key})
    assert status==200, f'Account read HTTP{status}'
    d=json.loads(raw)
    selected={k:d.get(k) for k in ['tier','character_count','character_limit','can_extend_character_limit','next_character_count_reset_unix']}
    save(name,{'at_utc':stamp(),'http_status':status,'account':selected})
    return selected

mode=sys.argv[1]
if mode=='preflight':
    before=account('ELEVEN-ACCOUNT-BEFORE.json')
    key=cal.read_dotenv_key('ELEVENLABS_API_KEY')
    status,raw,headers=safe_request('https://api.elevenlabs.io/v1/voices/scMbPZwQjr40V1MzL3Nj',headers={'xi-api-key':key})
    assert status==200,f'Voice read HTTP{status}'
    d=json.loads(raw)
    selected={k:d.get(k) for k in ['voice_id','name','category','is_owner','available_for_tiers','high_quality_base_model_ids','sharing','credit_cost_multiplier','rate_multiplier']}
    if selected.get('sharing'):
        selected['sharing']={k:v for k,v in selected['sharing'].items() if k in ['status','rate','financial_rewards_enabled','is_rate_allowed','enabled_in_library','original_voice_id']}
    save('ELEVEN-VOICE-PREFLIGHT.json',{'at_utc':stamp(),'http_status':status,'voice':selected})
    print(json.dumps({'account':before,'voice':selected},indent=2))

elif mode=='google':
    assert not (OUT/'GOOGLE-SUBMISSION-INTENT.json').exists(),'Previous attempt exists; no retry'
    body=(PROVIDER/'GOOGLE-CALLBACK-GUIDE-BODY.json').read_bytes()
    req=json.loads(body)
    assert req['voice']['name']=='Algieba' and req['voice']['modelName']=='gemini-2.5-pro-tts'
    token=cal.google_access_token()
    headers={'Authorization':f'Bearer {token}','Content-Type':'application/json; charset=utf-8'}
    project=cal.google_quota_project()
    if project:headers['x-goog-user-project']=project
    save('GOOGLE-SUBMISSION-INTENT.json',{'at_utc':stamp(),'request':req,'body_sha256':hashlib.sha256(body).hexdigest(),'work_order_sha256':hashlib.sha256(WO.read_bytes()).hexdigest(),'authorization':work['inputs'][0],'cap_usd':0.05,'max_attempts':1,'rate_basis':{'usd_per_million_input_tokens':1,'usd_per_million_audio_tokens':20,'audio_tokens_per_second':25},'expected_output_seconds':[7,12],'conservative_estimate_usd':len(req['input']['prompt']+req['input']['text'])/1000000+12*25*20/1000000})
    try:
        status,raw,safe_headers=safe_request('https://us-texttospeech.googleapis.com/v1/text:synthesize','POST',headers,body)
    except Exception as e:
        save('GOOGLE-ERROR.json',{'at_utc':stamp(),'error_class':type(e).__name__,'submission_outcome':'uncertain_no_retry'})
        raise SystemExit('Google transport error; no retry.')
    if status!=200:
        save('GOOGLE-ERROR.json',{'at_utc':stamp(),'http_status':status,'body':raw.decode('utf-8','replace'),'no_retry':True})
        raise SystemExit(f'Google HTTP{status}; no retry.')
    result=json.loads(raw)
    wav=base64.b64decode(result.pop('audioContent'))
    p=OUT/'context-guide.wav';p.write_bytes(wav);p.chmod(0o600)
    info=cal.probe(p)
    cost=info['duration_seconds']*25*20/1000000+len(req['input']['prompt']+req['input']['text'])/1000000
    save('GOOGLE-RECEIPT.json',{'at_utc':stamp(),'http_status':status,'headers':safe_headers,'metadata':result,'media':info,'output_path':str(p.relative_to(ROOT)),'estimated_cost_usd_conservative_input_tokens':cost,'cost_is_invoice':False,'calls':1,'retries':0})
    print(json.dumps({'google_status':status,'media':info,'estimated_cost_usd':cost}))

elif mode=='transfer':
    assert not (OUT/'ELEVEN-SUBMISSION-INTENT.json').exists(),'Previous attempt exists; no retry'
    guide=OUT/'context-guide.wav';info=cal.probe(guide)
    pf=json.loads((OUT/'ELEVEN-VOICE-PREFLIGHT.json').read_text())['voice']
    assert pf['voice_id']=='scMbPZwQjr40V1MzL3Nj'
    multiplier=json.loads((OUT/'TRANSFER-COST-DECISION.json').read_text())['verified_multiplier']
    credits=math.ceil(info['duration_seconds']*1000/60*multiplier)
    assert credits<=250,f'Transfer would exceed cap: {credits}'
    acct=account('ELEVEN-ACCOUNT-IMMEDIATE-BEFORE.json')
    assert acct['character_limit']-acct['character_count']>=credits,'Insufficient included credit balance'
    request=json.loads((PROVIDER/'CALLBACK-PICKUP-REQUEST.json').read_text())['transfer']
    fields=request['fields'];body,content_type=cal.multipart(fields,guide.name,guide.read_bytes())
    key=cal.read_dotenv_key('ELEVENLABS_API_KEY')
    save('ELEVEN-SUBMISSION-INTENT.json',{'at_utc':stamp(),'url':request['url'],'fields':fields,'guide':info,'guide_path':str(guide.relative_to(ROOT)),'body_sha256':hashlib.sha256(body).hexdigest(),'authorization':work['inputs'][0],'cap_credits':250,'estimated_credits_ceiling':credits,'verified_multiplier':multiplier,'calls':1,'retries':0})
    try:
        status,raw,safe_headers=safe_request(request['url'],'POST',{'xi-api-key':key,'Content-Type':content_type,'Accept':'*/*'},body)
    except Exception as e:
        save('ELEVEN-ERROR.json',{'at_utc':stamp(),'error_class':type(e).__name__,'submission_outcome':'uncertain_no_retry'})
        raise SystemExit('ElevenLabs transport error; no retry.')
    if status!=200:
        save('ELEVEN-ERROR.json',{'at_utc':stamp(),'http_status':status,'body':raw.decode('utf-8','replace'),'no_retry':True})
        raise SystemExit(f'ElevenLabs HTTP{status}; no retry.')
    p=OUT/'context-original-c.wav';cal.wav_from_pcm(raw,48000,p);p.chmod(0o600)
    save('ELEVEN-RECEIPT.json',{'at_utc':stamp(),'http_status':status,'headers':safe_headers,'media':cal.probe(p),'output_path':str(p.relative_to(ROOT)),'calls':1,'retries':0})
    after=account('ELEVEN-ACCOUNT-AFTER.json')
    delta=after['character_count']-acct['character_count']
    save('COST-RECONCILIATION.json',{'google':json.loads((OUT/'GOOGLE-RECEIPT.json').read_text()),'elevenlabs':{'character_cost_header':safe_headers.get('character-cost') or safe_headers.get('x-character-cost'),'account_usage_delta':delta,'account_delta_attribution':'May include concurrent account use; prefer exact response header if present.','preflight_estimated_credits_ceiling':credits,'cap_credits':250},'calls':{'google':1,'elevenlabs':1},'retries':0})
    print(json.dumps({'eleven_status':status,'media':cal.probe(p),'headers':safe_headers,'account_delta':delta}))
