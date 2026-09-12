"""One revision-03 selfie audition, using current N4B request shapes; no retries."""
import base64
import datetime
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
MEDIA = REPO / 'blueprint-cinema/experiments/SELFIE-AVATAR-001/media/revision-03'
sys.path.insert(0, str(REPO / 'operator-blueprint-v2/02-narration-production/tools'))
import capture_n4b as capture
import calibrate as cal

EXPECTED_TEXT = 'A buyer is sitting across the table from a woman who has run the same business for twenty five years. It makes money.'
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda data: hashlib.sha256(data).hexdigest()


def save(path, data):
    with path.open('x') as output:
        json.dump(data, output, indent=2)
        output.write('\n')


def main():
    stage, label = sys.argv[1:3]
    assert stage in ('prepare', 'guide', 'transfer') and label == 'R3'
    text = (BASE / 'spoken-text.txt').read_text().strip()
    assert text == EXPECTED_TEXT and len(text.split()) == 23
    assert capture.GUIDE_VOICE == 'Algieba'
    assert cal.TRANSFER_VOICE_ID == 'scMbPZwQjr40V1MzL3Nj'
    folder = BASE / label
    folder.mkdir(exist_ok=True)
    MEDIA.mkdir(parents=True, exist_ok=True)
    style = json.loads((BASE / (label + '.style.json')).read_text())['style_instructions']
    guide = MEDIA / ('voice-' + label.lower() + '.guide.wav')
    final = MEDIA / ('voice-' + label.lower() + '.original-c.wav')
    request = cal.guide_body(text, style, capture.GUIDE_VOICE)
    if stage == 'prepare':
        save(folder / 'INPUT.json', {'scope': 'One guide plus one identity transfer, authorized selfie voice audition; canonical state unchanged',
            'label': label, 'text': text, 'word_count': 23, 'text_sha256': sha(text.encode()),
            'style_sha256': sha(style.encode()), 'guide_request': request,
            'guide_source': str(Path(capture.__file__).relative_to(REPO)),
            'guide_source_sha256': sha(Path(capture.__file__).read_bytes()),
            'request_helper_sha256': sha(Path(cal.__file__).read_bytes()),
            'transfer': {'model': cal.TRANSFER_MODEL, 'voice_id': cal.TRANSFER_VOICE_ID,
                'settings': cal.TRANSFER_VOICE_SETTINGS, 'seed': cal.TRANSFER_SEED,
                'output_format': cal.TRANSFER_OUTPUT_FORMAT, 'remove_background_noise': False},
            'force_duration': False, 'max_guide_calls': 1, 'max_transfer_calls': 1})
        print(json.dumps({'label': label, 'status': 'prepared', 'words': 23}), flush=True)
        return
    pinned = json.loads((folder / 'INPUT.json').read_text())
    assert pinned['guide_request'] == request
    assert pinned['request_helper_sha256'] == sha(Path(cal.__file__).read_bytes())
    assert pinned['guide_source_sha256'] == sha(Path(capture.__file__).read_bytes())
    save(folder / (stage.upper() + '-INTENT.json'), {'at': now(), 'label': label,
        'stage': stage, 'scope': 'One authorized attempt only; inspect this intent before any continuation'})
    if stage == 'guide':
        headers = {'Authorization': 'Bearer ' + cal.google_access_token(), 'Content-Type': 'application/json'}
        project = cal.google_quota_project()
        if not project:
            raise RuntimeError('Google quota project unavailable')
        headers['x-goog-user-project'] = project
        status, body = capture.guide_once(text, style, headers, retries=0)
        raw = MEDIA / ('voice-' + label.lower() + '.google-response.bin')
        with raw.open('xb') as output:
            output.write(body)
        receipt = {'at': now(), 'http_status': status, 'raw_body_path': str(raw.relative_to(REPO)), 'raw_body_sha256': sha(body)}
        if status == 200:
            payload = json.loads(body)
            audio = base64.b64decode(payload['audioContent'], validate=True)
            with guide.open('xb') as output:
                output.write(audio)
            receipt['guide'] = cal.probe(guide)
            receipt['guide']['path'] = str(guide.relative_to(REPO))
        else:
            receipt['error'] = body.decode(errors='replace')[:4000]
        save(folder / 'GUIDE-RECEIPT.json', receipt)
    else:
        previous = json.loads((folder / 'GUIDE-RECEIPT.json').read_text())
        assert previous['http_status'] == 200 and previous['guide']['sha256'] == sha(guide.read_bytes())
        guide_asr = json.loads((folder / 'GUIDE-ASR.json').read_text())
        assert guide_asr['normalized_exact_match'], 'Guide words unverified; do not transfer'
        api_key = cal.read_dotenv_key('ELEVENLABS_API_KEY')
        status, body = capture.transfer_once(guide, api_key)
        raw = MEDIA / ('voice-' + label.lower() + '.elevenlabs-response.pcm')
        with raw.open('xb') as output:
            output.write(body)
        receipt = {'at': now(), 'http_status': status, 'raw_body_path': str(raw.relative_to(REPO)), 'raw_body_sha256': sha(body), 'guide_sha256': sha(guide.read_bytes()),
            'guide_tail_warning': None if previous['guide']['ends_in_silence'] else 'Guide has residual endpoint energy despite complete ASR words. Audition only; ending requires listening. Original bytes retained.'}
        if status == 200:
            assert not final.exists()
            cal.wav_from_pcm(body, cal.TRANSFER_OUTPUT_RATE_HZ, final)
            receipt['voice'] = cal.probe(final)
            receipt['voice']['path'] = str(final.relative_to(REPO))
            receipt['transfer_duration_delta_seconds'] = receipt['voice']['duration_seconds'] - previous['guide']['duration_seconds']
        else:
            receipt['error'] = body.decode(errors='replace').replace(api_key, '[REDACTED]')[:4000]
        save(folder / 'TRANSFER-RECEIPT.json', receipt)
    print(json.dumps(receipt), flush=True)
    if status != 200:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
