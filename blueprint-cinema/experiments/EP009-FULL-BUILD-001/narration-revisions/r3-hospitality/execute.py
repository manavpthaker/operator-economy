"""One scoped EP009 contextual pickup. One call per stage; never retry an intent."""
import base64, datetime, hashlib, importlib.util, json, math, sys, urllib.error, urllib.request
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path('/Users/brownmanbrain/GitHub/operator-economy')
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'blueprint-cinema/episodes/EP009-direct-booking-recovery/review/source-records/2026-09-17-owner-r2-feedback.json'
HELPER = ROOT / 'operator-blueprint-v2/02-narration-production/tools/calibrate.py'
STYLE = ROOT / 'operator-blueprint-v2/02-narration-production/prompts/NARRATOR-REGISTER.candidate-C4.google-gemini-tts.style-instructions.json'
PARAGRAPH = "I spent ten years in hospitality, including Ace Hotel and Standard Hotels. I know this business from the inside out. I haven't sold this particular service, though. What a thirty room inn will pay for it is still something I'd have to test."
CONTEXT = 'Start with properties you can drive to and owners you can sit across from.'
TEXT = PARAGRAPH + '\n\n' + CONTEXT
spec = importlib.util.spec_from_file_location('cal', HELPER)
cal = importlib.util.module_from_spec(spec); spec.loader.exec_module(cal)
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
bind = lambda p: {'path': str(p.relative_to(ROOT)), 'sha256': sha(p)}

def save(name, value):
    with (OUT / name).open('x') as f: json.dump(value, f, indent=2); f.write('\n')

def fetch(url, headers, body=None):
    request = urllib.request.Request(url, data=body, headers=headers, method='POST' if body is not None else 'GET')
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            return response.status, response.read(), {k.lower(): v for k,v in response.headers.items() if k.lower() in ('request-id','x-request-id','character-cost','x-character-cost','content-type','date')}
    except urllib.error.HTTPError as e:
        return e.code, e.read(), {}

def account(name):
    status, raw, _ = fetch('https://api.elevenlabs.io/v1/user/subscription', {'xi-api-key': cal.read_dotenv_key('ELEVENLABS_API_KEY')})
    if status != 200: raise RuntimeError(f'account read failed: HTTP {status}')
    data = json.loads(raw)
    selected = {k:data.get(k) for k in ('tier','status','character_count','character_limit','can_extend_character_limit')}
    save(name, {'at_utc':now(), 'http_status':status, 'account':selected})
    if data['status'] != 'active': raise RuntimeError('ElevenLabs subscription not active')
    return selected

def authorization():
    auth = json.loads((OUT / 'PICKUP-AUTHORIZATION.json').read_text())
    if auth['owner_source'] != bind(SOURCE): raise RuntimeError('owner source changed')
    if auth['helper'] != bind(HELPER) or auth['register'] != bind(STYLE): raise RuntimeError('recipe changed')
    if auth['paragraph'] != PARAGRAPH or auth['context'] != CONTEXT: raise RuntimeError('pickup text changed')
    return auth

def submit(name, url, headers, body):
    try: status, raw, response_headers = fetch(url, headers, body)
    except Exception as e:
        save(name + '-ERROR.json', {'at_utc':now(), 'exception_class':type(e).__name__, 'outcome':'uncertain; intent retained; no retry'})
        raise
    if status != 200:
        save(name + '-ERROR.json', {'at_utc':now(),'http_status':status,'response':raw.decode('utf-8','replace'),'no_retry':True})
        raise RuntimeError(f'{name} returned HTTP {status}; no retry')
    return raw, response_headers

mode = sys.argv[1]
if mode == 'prepare':
    if sha(HELPER) != 'd59303278dbb79bef6fe0080f1d2b6c1e701e9228e95c7b3cdea4f3eec78cc00': raise RuntimeError('helper changed')
    if sha(STYLE) != 'b747d7b0afa4469b2be05c20eb16306a25bb5185b9fa8b12e2d4aa4ddd8d3efc': raise RuntimeError('register changed')
    style, label, aliases = cal.load_style(STYLE)
    body = cal.guide_body(TEXT, cal.compose_style(style, aliases, TEXT), 'Algieba')
    save('PICKUP-AUTHORIZATION.json', {
        'record_type':'scoped_owner_correction_pickup', 'at_utc':now(), 'owner_source':bind(SOURCE),
        'authority':'Current owner correction to the hospitality passage, delegated by root for one contextual Algieba to Original C pickup; not reused N4B authorization.',
        'paragraph':PARAGRAPH, 'context':CONTEXT, 'context_use':'Generate in connected delivery; select paragraph only before context.',
        'helper':bind(HELPER), 'register':bind(STYLE), 'guide':body,
        'transfer':{'model':cal.TRANSFER_MODEL,'voice_id':cal.TRANSFER_VOICE_ID,'seed':cal.TRANSFER_SEED,'voice_settings':cal.TRANSFER_VOICE_SETTINGS,'remove_background_noise':False,'output_format':cal.TRANSFER_OUTPUT_FORMAT},
        'call_limits':{'google':1,'elevenlabs':1,'automatic_retries':0},
        'cost_plan':{'google_budget_usd':0.05,'elevenlabs_credit_cap':750,'guide_estimated_seconds':[20,35],
                     'google_rate':'$1 per million input tokens plus $20 per million audio tokens; 25 audio tokens per second',
                     'elevenlabs_rate':'1000 credits per minute',
                     'verified_2026_09_17_sources':['https://cloud.google.com/text-to-speech/pricing','https://help.elevenlabs.io/hc/en-us/articles/24938328105873-How-much-does-Voice-Changer-cost']},
        'preserve_original_master':True,'canonical_master_plan_assembly_writes':False,'retime':False})
    save('GOOGLE-REQUEST.json', body)
    with (OUT/'paragraph.txt').open('x') as f: f.write(PARAGRAPH+'\n')
    with (OUT/'contextual-text.txt').open('x') as f: f.write(TEXT+'\n')
    print(json.dumps({'prepared':True,'words':len(TEXT.split()),'paragraph_words':len(PARAGRAPH.split())}))
elif mode == 'google':
    auth=authorization(); body=(OUT/'GOOGLE-REQUEST.json').read_bytes(); parsed=json.loads(body)
    if parsed != auth['guide']: raise RuntimeError('guide request changed')
    headers={'Authorization':'Bearer '+cal.google_access_token(),'Content-Type':'application/json; charset=utf-8'}
    project=cal.google_quota_project()
    if project: headers['x-goog-user-project']=project
    save('GOOGLE-SUBMISSION-INTENT.json', {'at_utc':now(),'authorization':bind(OUT/'PICKUP-AUTHORIZATION.json'), 'body_sha256':hashlib.sha256(body).hexdigest(),'endpoint':cal.GUIDE_ENDPOINT,'calls':1,'retries':0,'estimated_usd_cap':0.05})
    raw, headers=submit('GOOGLE',cal.GUIDE_ENDPOINT,headers,body)
    data=json.loads(raw); wav=base64.b64decode(data.pop('audioContent'),validate=True)
    with (OUT/'context-guide.wav').open('xb') as f:f.write(wav)
    info=cal.probe(OUT/'context-guide.wav')
    estimate=info['duration_seconds']*0.0005+len(parsed['input']['prompt']+parsed['input']['text'])/1e6
    save('GOOGLE-RECEIPT.json',{'at_utc':now(),'http_status':200,'response_headers':headers,'response_metadata':data,'full_response_sha256':hashlib.sha256(raw).hexdigest(),'response_body_bytes':len(raw),'media':info,'estimated_cost_usd_upper_input_character_bound':estimate,'calls':1,'retries':0})
    print(json.dumps({'stage':'google',**info,'estimated_usd':estimate}))
elif mode == 'transfer':
    auth=authorization(); guide=OUT/'paragraph-guide.wav'; info=cal.probe(guide)
    receipt=json.loads((OUT/'GOOGLE-RECEIPT.json').read_text())
    selection=json.loads((OUT/'GUIDE-SELECTION.json').read_text())
    if sha(OUT/'context-guide.wav') != receipt['media']['sha256']: raise RuntimeError('contextual guide changed')
    if info['sha256'] != selection['selected']['sha256'] or selection['source']['sha256'] != receipt['media']['sha256']: raise RuntimeError('selected guide changed')
    check=json.loads((OUT/'GUIDE-ASR-CHECK.json').read_text())
    if check['selected_sha256'] != info['sha256'] or check['normalized_exact_match'] is not True: raise RuntimeError('paragraph ASR not current and exact')
    if info['tail_energy'] >= .02: raise RuntimeError('guide not complete; no transfer')
    credit_estimate=math.ceil(info['duration_seconds']*1000/60)
    if credit_estimate > auth['cost_plan']['elevenlabs_credit_cap']: raise RuntimeError('guide exceeds scoped transfer cap')
    before=account('ELEVEN-ACCOUNT-BEFORE.json')
    if before['character_limit']-before['character_count'] < credit_estimate: raise RuntimeError('insufficient credits')
    fields={'model_id':cal.TRANSFER_MODEL,'remove_background_noise':'false','seed':str(cal.TRANSFER_SEED),'voice_settings':json.dumps(cal.TRANSFER_VOICE_SETTINGS,sort_keys=True),'file_format':'other'}
    body,content_type=cal.multipart(fields,guide.name,guide.read_bytes())
    url=cal.TRANSFER_ENDPOINT+'?output_format=pcm_48000&enable_logging=true'
    save('ELEVEN-SUBMISSION-INTENT.json',{'at_utc':now(),'authorization':bind(OUT/'PICKUP-AUTHORIZATION.json'),'url':url,'fields':fields,'guide':bind(guide),'guide_probe':info,'guide_selection':bind(OUT/'GUIDE-SELECTION.json'),'guide_text_check':bind(OUT/'GUIDE-ASR-CHECK.json'),'body_sha256':hashlib.sha256(body).hexdigest(),'estimated_credits':credit_estimate,'cap_credits':750,'calls':1,'retries':0})
    raw,headers=submit('ELEVEN',url,{'xi-api-key':cal.read_dotenv_key('ELEVENLABS_API_KEY'),'Content-Type':content_type,'Accept':'*/*'},body)
    if (OUT/'paragraph-original-c.wav').exists():raise RuntimeError('transfer output exists')
    cal.wav_from_pcm(raw,48000,OUT/'paragraph-original-c.wav')
    media=cal.probe(OUT/'paragraph-original-c.wav')
    save('ELEVEN-RECEIPT.json',{'at_utc':now(),'http_status':200,'response_headers':headers,'raw_pcm_sha256':hashlib.sha256(raw).hexdigest(),'raw_pcm_bytes':len(raw),'output':bind(OUT/'paragraph-original-c.wav'),'media':media,'estimated_credits':credit_estimate,'calls':1,'retries':0})
    after=account('ELEVEN-ACCOUNT-AFTER.json')
    save('ELEVEN-USAGE-DELTA.json',{'at_utc':now(),'account_delta':after['character_count']-before['character_count'],'attribution_limit':'Concurrent account usage could affect this delta; provider character-cost header is preferred when present.'})
    print(json.dumps({'stage':'transfer',**media,'account_delta':after['character_count']-before['character_count'],'response_headers':headers}))
else: raise SystemExit('prepare | google | transfer')
