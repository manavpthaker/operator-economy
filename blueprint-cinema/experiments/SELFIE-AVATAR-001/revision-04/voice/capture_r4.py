"""One whole R4 guide then one Original C transfer; immutable input, no retries."""
import base64, datetime, hashlib, json, sys, urllib.request, urllib.error
from pathlib import Path
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
SCRIPT = BASE.parent / 'SCRIPT.txt'
MEDIA = REPO / 'blueprint-cinema/experiments/SELFIE-AVATAR-001/media/revision-04'
sys.path.insert(0, str(REPO / 'operator-blueprint-v2/02-narration-production/tools'))
import capture_n4b as capture
import calibrate as cal
EXPECTED_SHA = '3eb28bd243f2c169b5906852f3b055553d1bc0e0520a029082fa5bf41a36fbe3'
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda data: hashlib.sha256(data).hexdigest()
def save(path, data):
    with path.open('x') as output:
        json.dump(data, output, indent=2, ensure_ascii=False)
        output.write('\n')
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs): return None
def safe_post(url, data, headers):
    from urllib.parse import urlparse
    assert urlparse(url).scheme == 'https'
    assert urlparse(url).hostname in ('us-texttospeech.googleapis.com', 'api.elevenlabs.io')
    request = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=600) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
cal.post = safe_post
def main():
    stage = sys.argv[1]
    assert stage in ('prepare', 'guide', 'transfer')
    raw_text = SCRIPT.read_bytes()
    assert sha(raw_text) == EXPECTED_SHA
    text = raw_text.decode('utf-8')
    assert len(text.split()) == 184
    assert capture.GUIDE_VOICE == 'Algieba'
    assert cal.TRANSFER_VOICE_ID == 'scMbPZwQjr40V1MzL3Nj'
    folder = BASE / 'R4'
    folder.mkdir(exist_ok=True)
    MEDIA.mkdir(parents=True, exist_ok=True)
    style = json.loads((BASE / 'R4.style.json').read_text())['style_instructions']
    assert len(text.encode()) <= 4000 and len(style.encode()) <= 4000
    guide = MEDIA / 'voice-r4.guide.wav'
    final = MEDIA / 'voice-r4.original-c.wav'
    request = cal.guide_body(text, style, capture.GUIDE_VOICE)
    if stage == 'prepare':
        save(folder / 'INPUT.json', {
            'scope':'One full authorized R4 guide plus one Original C transfer; no segmentation, processing, retry or canonical edit',
            'script_path':str(SCRIPT.relative_to(REPO)), 'script_sha256':EXPECTED_SHA,
            'text':text, 'word_count':184, 'style_sha256':sha(style.encode()), 'guide_request':request,
            'guide_source':str(Path(capture.__file__).relative_to(REPO)),
            'guide_source_sha256':sha(Path(capture.__file__).read_bytes()),
            'request_helper_sha256':sha(Path(cal.__file__).read_bytes()),
            'transfer':{'model':cal.TRANSFER_MODEL,'voice_id':cal.TRANSFER_VOICE_ID,
                'settings':cal.TRANSFER_VOICE_SETTINGS,'seed':cal.TRANSFER_SEED,
                'output_format':cal.TRANSFER_OUTPUT_FORMAT,'remove_background_noise':False},
            'force_duration':False,'max_guide_calls':1,'max_transfer_calls':1,
            'credential_redirect_policy':'deny','transport_timeout_seconds':600})
        print(json.dumps({'stage':stage,'status':'prepared','words':184}),flush=True)
        return
    pinned=json.loads((folder/'INPUT.json').read_text())
    assert pinned['guide_request']==request
    assert pinned['request_helper_sha256']==sha(Path(cal.__file__).read_bytes())
    assert pinned['guide_source_sha256']==sha(Path(capture.__file__).read_bytes())
    if stage == 'transfer':
        guide = MEDIA / 'voice-r4.corrected-guide.wav'
        previous=json.loads((folder/'CORRECTED-GUIDE-RECEIPT.json').read_text())
        assert previous['status']=='verified' and previous['guide']['sha256']==sha(guide.read_bytes())
        asr=json.loads((folder/'CORRECTED-GUIDE-ASR.json').read_text())
        assert asr['normalized_exact_match'] and asr['source_sha256']==sha(guide.read_bytes())
        save(folder/'TRANSFER-INPUT.json',{'at':now(),'script_sha256':EXPECTED_SHA,
            'guide_sha256':sha(guide.read_bytes()),'guide_path':str(guide.relative_to(REPO)),
            'correction_recipe_sha256':sha((folder/'GUIDE-CORRECTION.json').read_bytes()),
            'asr_sha256':sha((folder/'CORRECTED-GUIDE-ASR.json').read_bytes()),
            'scope':'One whole Original C transfer of corrected R4 guide; raw non-silent pickup ending retained for listening'})
    save(folder/(stage.upper()+'-INTENT.json'),{'at':now(),'stage':stage,
        'script_sha256':EXPECTED_SHA,'scope':'One authorized attempt; uncertain outcomes require inspection, never duplicate submission'})
    if stage == 'guide':
        headers={'Authorization':'Bearer '+cal.google_access_token(),'Content-Type':'application/json'}
        project=cal.google_quota_project()
        if not project: raise RuntimeError('Google quota project unavailable')
        headers['x-goog-user-project']=project
        status,body=capture.guide_once(text,style,headers,retries=0)
        raw=MEDIA/'voice-r4.google-response.bin'
        with raw.open('xb') as output: output.write(body)
        receipt={'at':now(),'http_status':status,'raw_body_path':str(raw.relative_to(REPO)),'raw_body_sha256':sha(body)}
        if status==200:
            audio=base64.b64decode(json.loads(body)['audioContent'],validate=True)
            with guide.open('xb') as output: output.write(audio)
            receipt['guide']=cal.probe(guide)
            receipt['guide']['path']=str(guide.relative_to(REPO))
        else: receipt['error']=body.decode(errors='replace')[:4000]
        save(folder/'GUIDE-RECEIPT.json',receipt)
    else:
        api_key=cal.read_dotenv_key('ELEVENLABS_API_KEY')
        status,body=capture.transfer_once(guide,api_key)
        raw=MEDIA/'voice-r4.elevenlabs-response.pcm'
        with raw.open('xb') as output: output.write(body)
        receipt={'at':now(),'http_status':status,'raw_body_path':str(raw.relative_to(REPO)),
            'raw_body_sha256':sha(body),'guide_sha256':sha(guide.read_bytes())}
        if status==200:
            assert not final.exists()
            cal.wav_from_pcm(body,cal.TRANSFER_OUTPUT_RATE_HZ,final)
            receipt['voice']=cal.probe(final)
            receipt['voice']['path']=str(final.relative_to(REPO))
            receipt['transfer_duration_delta_seconds']=receipt['voice']['duration_seconds']-previous['guide']['duration_seconds']
        else: receipt['error']=body.decode(errors='replace').replace(api_key,'[REDACTED]')[:4000]
        save(folder/'TRANSFER-RECEIPT.json',receipt)
    print(json.dumps(receipt),flush=True)
    if status!=200: raise SystemExit(1)
if __name__=='__main__': main()
