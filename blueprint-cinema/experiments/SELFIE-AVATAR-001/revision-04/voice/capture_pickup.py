"""Single authorized exact-contraction pickup; preceding hobby paragraph is context."""
import sys,json,base64
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import capture_r4 as r
stage=sys.argv[1]
assert stage in ('prepare','guide')
raw=r.SCRIPT.read_bytes()
assert r.sha(raw)==r.EXPECTED_SHA
text='\n\n'.join(raw.decode('utf-8').strip().split('\n\n')[-2:])
assert text.endswith('So you guys tell me, what made you decide to turn something you’d built into a business?')
style=json.loads((r.BASE/'R4.style.json').read_text())['style_instructions']
style=style.replace('around sixty-five to seventy seconds for the complete passage','around eleven to thirteen seconds for this short passage')
style += " This pickup begins with the unchanged hobby paragraph as conversational context, followed by the exact last question. Match the same comfortably close voice, brisk connected phrases and relaxed energy throughout. In the final question, keep the precise contraction you’d before built. Make its brief final d audibly present before the b without adding a syllable or separating the words unnaturally. Do not change you’d to you, you had or you would. The question remains an easy, genuine invitation, not a pronunciation exercise. Speak the exact text supplied and finish business completely."
request=r.cal.guide_body(text,style,r.capture.GUIDE_VOICE)
folder=r.BASE/'R4'
if stage=='prepare':
    r.save(folder/'PICKUP-INPUT.json',{'scope':'One additional bounded pickup authorized by root: unchanged hobby context plus exact final question; no full regeneration',
        'script_sha256':r.EXPECTED_SHA,'text':text,'word_count':len(text.split()),'style_sha256':r.sha(style.encode()),'guide_request':request,
        'guide_source_sha256':r.sha(Path(r.capture.__file__).read_bytes()),
        'request_helper_sha256':r.sha(Path(r.cal.__file__).read_bytes()),'max_guide_calls':1,'target_duration_seconds':[11,13]})
    print(json.dumps({'status':'prepared','words':len(text.split())}))
else:
    pin=json.loads((folder/'PICKUP-INPUT.json').read_text())
    assert pin['guide_request']==request
    r.save(folder/'PICKUP-GUIDE-INTENT.json',{'at':r.now(),'scope':'One authorized pickup attempt; no retry'})
    headers={'Authorization':'Bearer '+r.cal.google_access_token(),'Content-Type':'application/json'}
    quota=r.cal.google_quota_project()
    if not quota: raise RuntimeError('No quota project')
    headers['x-goog-user-project']=quota
    status,body=r.capture.guide_once(text,style,headers,retries=0)
    source=r.MEDIA/'voice-r4.pickup-google-response.bin'
    with source.open('xb') as out: out.write(body)
    receipt={'at':r.now(),'http_status':status,'raw_body_path':str(source.relative_to(r.REPO)),'raw_body_sha256':r.sha(body)}
    if status==200:
        wav=r.MEDIA/'voice-r4.pickup-guide.wav'
        audio=base64.b64decode(json.loads(body)['audioContent'],validate=True)
        with wav.open('xb') as out: out.write(audio)
        receipt['guide']=r.cal.probe(wav); receipt['guide']['path']=str(wav.relative_to(r.REPO))
    else: receipt['error']=body.decode(errors='replace')[:4000]
    r.save(folder/'PICKUP-GUIDE-RECEIPT.json',receipt)
    print(json.dumps(receipt),flush=True)
    if status!=200: raise SystemExit(1)

