"""Read-only regression comparison; emits findings to stdout only."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
REVIEWS = ROOT / 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews'
BEFORE = REVIEWS / 'r13-unanswered-job'
AFTER = REVIEWS / 'r14-opening-bridge'
PIN = '8e814b137d6ff1696050834e216bfdf880a0c22f75674040325f3a6876944da5'

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

assert digest(BEFORE/'index.html') == PIN, 'Stale R13 input: stop'

class Declarations(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.primary = []
        self.extra = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = {k: v for k,v in attrs if k != 'data-hf-id'}
        if attrs.get('data-track-index') == '1' or tag == 'audio':
            self.primary.append({'tag':tag, 'attributes':attrs})
        elif 'data-track-index' in attrs:
            self.extra.append({'tag':tag, 'attributes':attrs})

old, new = [Declarations((p/'index.html').read_text()) for p in (BEFORE, AFTER)]
asset_results = []
for directory in ('public/media','public/audio','public/fonts','public/vendor','compositions'):
    old_paths = {str(p.relative_to(BEFORE)) for p in (BEFORE/directory).rglob('*') if p.is_file()}
    new_paths = {str(p.relative_to(AFTER)) for p in (AFTER/directory).rglob('*') if p.is_file()}
    for name in sorted(old_paths | new_paths):
        a = digest(BEFORE/name) if name in old_paths else None
        b = digest(AFTER/name) if name in new_paths else None
        asset_results.append({'path':name, 'before_sha256':a, 'after_sha256':b, 'unchanged':a == b})

print(json.dumps({'baseline_pin_matches':True, 'r14_index_sha256':digest(AFTER/'index.html'), 'primary_declarations_equal':old.primary == new.primary, 'baseline_picture_count':sum(d['attributes'].get('data-track-index') == '1' for d in old.primary), 'baseline_audio_count':sum(d['tag']=='audio' for d in old.primary), 'r13_declarations':old.primary, 'r14_declarations':new.primary, 'new_extra_tracks':new.extra, 'assets':asset_results},indent=2))
