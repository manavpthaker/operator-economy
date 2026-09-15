"""Approved single R35 restoration. Exclusive paid intent; no resubmission or fallback."""
from pathlib import Path
import importlib.util, json, hashlib, datetime, sys, subprocess

BASE = Path(__file__).resolve().parent
REPO = next(p for p in BASE.parents if (p / '.agents').is_dir())
source = BASE.parents[1] / 'r32-performance-refinement/provider/fal_ops.py'
spec = importlib.util.spec_from_file_location('bounded_fal_transport', source)
transport = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transport)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())
save = lambda p, d: p.write_text(json.dumps(d, indent=2) + '\n')

def main():
    mode = sys.argv[1]
    folder = BASE / 'restoration'
    folder.mkdir(exist_ok=True)
    if mode == 'submit':
        auth = read(BASE / 'GENERATION-AUTHORIZATION.json')
        assert auth['caps'] == {'higgsfield_credits': 54, 'fal_total_usd': 1}
        assert auth['max_fal_restoration_jobs'] == 1 and auth['paid_retries'] == 0
        assert not (folder / 'JOB.json').exists()
        native = read(BASE / 'NATIVE-MEDIA.json')
        assert sha(BASE / 'native.mp4') == native['sha256']
        price = read(BASE / 'FAL-PRICE-PREFLIGHT.json')
        cost = native['duration_seconds'] * price['usd_per_minute'] / 60
        assert 0 < cost <= auth['caps']['fal_total_usd']
        audio = read(BASE / 'audio/UPLOAD.json')
        assert audio['status'] == 'verified'
        assert hashlib.sha256(transport.get(audio['file_url'])).hexdigest() == audio['sha256']
        payload = {'video_url': native['url'], 'audio_url': audio['file_url'], 'sync_mode': 'silence'}
        with (folder / 'SUBMISSION-INTENT.json').open('x') as f:
            json.dump({'at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'model': 'fal-ai/sync-lipsync/v3', 'payload': payload, 'estimated_usd': cost, 'authorization_sha256': sha(BASE / 'GENERATION-AUTHORIZATION.json'), 'no_retry': True}, f, indent=2)
        try:
            job = transport.api('https://queue.fal.run/fal-ai/sync-lipsync/v3', payload)
        except Exception as exc:
            save(folder / 'ERROR.json', {'submission_status': 'uncertain', 'retry': False, 'error': str(exc)})
            raise
        save(folder / 'JOB.json', job)
        print(json.dumps({'request_id': job['request_id'], 'estimated_usd': cost}))
    elif mode in {'status', 'result'}:
        job = read(folder / 'JOB.json')
        result = transport.api(job['status_url'] if mode == 'status' else job['response_url'])
        save(folder / ('STATUS.json' if mode == 'status' else 'RESULT.json'), result)
        if mode == 'result':
            data = transport.get(result['video']['url'])
            with (folder / 'restored.mp4').open('xb') as f: f.write(data)
            print(json.dumps({'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}))
        else:
            print(json.dumps({'status': result.get('status'), 'queue_position': result.get('queue_position')}))
    else:
        raise ValueError('Unsupported operation')

if __name__ == '__main__': main()
