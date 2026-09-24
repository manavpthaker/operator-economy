"""One hook guide then one Original C transfer for motion-test-01; no retries."""
import base64, datetime, hashlib, json, sys, urllib.request, urllib.error
from pathlib import Path
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
sys.path.insert(0, str(REPO / 'operator-blueprint-v2/02-narration-production/tools'))
import capture_n4b as capture
import calibrate as cal
MEDIA = BASE.parent / 'media'
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda d: hashlib.sha256(d).hexdigest()
def save(p, d):
    with p.open('x') as o: json.dump(d, o, indent=2, ensure_ascii=False); o.write('\n')
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
def safe_post(url, data, headers):
    from urllib.parse import urlparse
    assert urlparse(url).scheme == 'https' and urlparse(url).hostname in ('us-texttospeech.googleapis.com', 'api.elevenlabs.io')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=600) as r: return r.status, r.read()
    except urllib.error.HTTPError as e: return e.code, e.read()
cal.post = safe_post
def meta(p):
    import wave
    with wave.open(str(p)) as h:
        return {'sha256': sha(p.read_bytes()), 'sample_rate_hz': h.getframerate(), 'channels': h.getnchannels(), 'duration_seconds': h.getnframes()/h.getframerate()}
stage = sys.argv[1]; assert stage in ('guide', 'transfer')
text = (BASE.parent / 'HOOK.txt').read_text()
style = json.loads((BASE / 'style.json').read_text())['style_instructions']
guide, final = MEDIA / 'hook.guide.wav', MEDIA / 'hook.original-c.wav'
save(BASE / (stage.upper() + '-INTENT.json'), {'at': now(), 'stage': stage, 'text_sha256': sha(text.encode()), 'guide_voice': capture.GUIDE_VOICE, 'transfer_voice_id': cal.TRANSFER_VOICE_ID})
if stage == 'guide':
    h = {'Authorization': 'Bearer ' + cal.google_access_token(), 'Content-Type': 'application/json'}
    proj = cal.google_quota_project()
    if not proj: raise RuntimeError('Google quota project unavailable')
    h['x-goog-user-project'] = proj
    status, body = capture.guide_once(text, style, h, retries=0)
    rec = {'at': now(), 'http_status': status}
    if status == 200:
        guide.write_bytes(base64.b64decode(json.loads(body)['audioContent'], validate=True)); rec['guide'] = meta(guide)
    else: rec['error'] = body.decode(errors='replace').replace(h['Authorization'], '[REDACTED]')[:3000]
    save(BASE / 'GUIDE-RECEIPT.json', rec)
else:
    key = cal.read_dotenv_key('ELEVENLABS_API_KEY')
    status, body = capture.transfer_once(guide, key)
    rec = {'at': now(), 'http_status': status, 'guide_sha256': sha(guide.read_bytes()), 'model': cal.TRANSFER_MODEL, 'settings': cal.TRANSFER_VOICE_SETTINGS, 'seed': cal.TRANSFER_SEED}
    if status == 200:
        cal.wav_from_pcm(body, cal.TRANSFER_OUTPUT_RATE_HZ, final); rec['voice'] = meta(final)
    else: rec['error'] = body.decode(errors='replace').replace(key, '[REDACTED]')[:3000]
    save(BASE / 'TRANSFER-RECEIPT.json', rec)
print(json.dumps(rec)); sys.exit(0 if status == 200 else 1)
