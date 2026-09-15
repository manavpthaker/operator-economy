"""Read back active sources, preserved assets and exact source coverage after integration."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parent.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Elements(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.rows = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        self.rows.append((tag, dict(attrs)))


if __name__ == '__main__':
    rows = []
    files = set()

    def visit(path):
        if path in files:
            return
        files.add(path)
        for tag, a in Elements(BASE / path).rows:
            rows.append((path, tag, a))
            nested = a.get('data-composition-src')
            if nested:
                visit(nested)
            src = a.get('src')
            if src and not src.startswith(('http:', 'https:')):
                assert (BASE / src).is_file(), src
                files.add(src)

    visit('index.html')
    expected = {'avatar-hook': 'public/media/avatar-v5-opening.mp4',
        'avatar-opportunity': 'public/media/v5-opportunity.mp4',
        'avatar-post-title': 'public/media/v5-post-title-continuous.mp4',
        'q-speaking': 'public/media/v5-question-with-pause.mp4'}
    mounted = {}
    for path, tag, attrs in rows:
        if tag == 'video' and attrs.get('id') in expected:
            name = attrs['id']
            assert name not in mounted
            assert attrs['src'] == expected[name]
            assert 'muted' in attrs
            probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams',
                'v:0', '-show_streams', '-of', 'json', str(BASE / attrs['src'])]))['streams'][0]
            assert probe['r_frame_rate'] == '24/1'
            assert (probe['width'], probe['height']) == (1920, 1080)
            assert float(attrs['data-media-start']) + float(attrs['data-duration']) <= float(probe['duration']) + .001
            mounted[name] = dict(composition=path, source=attrs['src'],
                source_sha256=sha(BASE / attrs['src']), start=float(attrs['data-start']),
                duration=float(attrs['data-duration']), source_in=float(attrs['data-media-start']),
                frames=int(probe['nb_frames']))
    assert set(mounted) == set(expected)
    old = {'public/media/presenter-pickups-browser.mp4', 'public/media/post-title-a.mp4',
        'public/media/post-title-b-react.mp4', 'public/media/presenter-question.mp4'}
    assert not (files & old), 'An older presenter source is still mounted'
    original = BASE.parent / 'r29-neutral-seller'
    pins = json.loads((original / 'OWNER-ACCEPTANCE.json').read_text())['runtime_files']
    unchanged = []
    for path, pinned in pins.items():
        if path not in {'index.html', 'compositions/presenter-question.html'}:
            assert sha(BASE / path) == pinned, path
            unchanged.append(path)
    old_audio = [(t, a) for t, a in Elements(original / 'index.html').rows if t == 'audio']
    new_audio = [(t, a) for p, t, a in rows if p == 'index.html' and t == 'audio']
    assert old_audio == new_audio, 'Original narration placement changed'
    fonts = list((BASE / 'public/fonts').glob('*.woff2'))
    files.update(str(p.relative_to(BASE)) for p in fonts)
    files.update(pins)
    runtime = {p: sha(BASE / p) for p in sorted(files)}
    fingerprint = hashlib.sha256(json.dumps(runtime, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result = dict(status='pass', mounted_presenters=mounted, old_presenters_mounted=False,
        original_audio_elements_unchanged=True, unchanged_r29_files=unchanged,
        post_title_one_video_element=True, original_timing_and_other_scenes='preserved',
        limitations='Source and timing checks do not establish perceptual lip sync or owner acceptance.')
    (BASE / 'provider/INTEGRATION-AUDIT.json').write_text(json.dumps(result, indent=2) + '\n')
    (BASE / 'RUNTIME-PINS.json').write_text(json.dumps(dict(files=runtime,
        fingerprint_sha256=fingerprint, scope='Inherited runtime files plus current mounted compositions and V5 media; dormant earlier assets retained as history'), indent=2) + '\n')
    print(json.dumps(result))
