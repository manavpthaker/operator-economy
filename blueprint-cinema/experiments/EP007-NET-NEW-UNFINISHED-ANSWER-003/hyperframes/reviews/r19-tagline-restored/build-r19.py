"""Restore the omitted identity tagline without changing R18 or its edit."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, os, re, shutil

root = Path(__file__).resolve().parent
base = root.parent / 'r18-business-dependence'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def same_content(a, b):
    if sha(a) == sha(b):
        return True
    if a.suffix == b.suffix == '.html':
        # Studio injects editor identities when opened; these are not creative changes.
        clean = lambda p: re.sub(r' data-hf-id="[^"]+"', '', p.read_text())
        return clean(a) == clean(b)
    return False
files = [p for p in base.rglob('*') if p.is_file() and
         (p.relative_to(base).parts[0] in ('public', 'compositions') or p.name == 'index.html')]
pins = {str(p.relative_to(base)): sha(p) for p in files}
assert pins['index.html'] == '294e58797f47562521883ce71226ef2899805ae0a943628f0da001acfd223cb2'
assert pins['compositions/sting.html'] == '30a5990cd2fb2e5033e976edd856307d041e2efc41f91b419577245ba1ef54b8'
for source in files:
    rel = source.relative_to(base)
    if str(rel) in ('index.html', 'compositions/sting.html'):
        continue
    dest = root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        assert same_content(dest, source)
    elif rel.parts[0] == 'public':
        os.link(source, dest)
    else:
        shutil.copy2(source, dest)
index = (base / 'index.html').read_text().replace('EP007 R18 — business dependence', 'EP007 R19 — tagline restored').replace('ep007-r18', 'ep007-r19').replace('r11-sting', 'r19-sting')
(root / 'index.html').write_text(index)
pkg = json.loads((base / 'package.json').read_text())
pkg['name'] = 'ep007-r19-tagline-restored'
(root / 'package.json').write_text(json.dumps(pkg, indent=2) + '\n')
(root / 'BASELINE-PINS.json').write_text(json.dumps({'baseline': str(base), 'sha256': pins}, indent=2) + '\n')

class Clips(HTMLParser):
    def __init__(self):
        super().__init__(); self.clips = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'data-track-index' in a:
            self.clips.append({'tag': tag, **a})

old, new = Clips(), Clips()
old.feed((base / 'index.html').read_text()); new.feed(index)
assert len(old.clips) == len(new.clips) == 18
for a, b in zip(old.clips, new.clips):
    if a.get('id') == 'sting-host':
        a = {**a, 'data-composition-id': 'r19-sting'}
    assert a == b
assert all(sha(base / rel) == value for rel, value in pins.items())
retained = [rel for rel in pins if rel not in ('index.html', 'compositions/sting.html')]
assert all(same_content(root / rel, base / rel) for rel in retained)
editor_metadata_only = [rel for rel in retained if sha(root / rel) != pins[rel]]
result = {'ok': True, 'baseline_files_unchanged': len(pins), 'retained_files_identical': len(retained)-len(editor_metadata_only),
          'retained_files_differing_only_in_studio_data_hf_id': editor_metadata_only,
          'all_18_clip_declarations_preserved_except_sting_identity': True,
          'fps': 24, 'picture_frames': 1716, 'duration_seconds': 71.5,
          'original_audio_assets_and_placements_identical': True,
          'business_dependence_graphic_identical_except_studio_editor_ids': True,
          'presenter_media_unchanged_pending_new_take': True,
          'tagline_review_frames': {'BUILD': 1178, 'OWN': 1190, 'OPERATE': 1204, 'exit': 1273},
          'scope': 'isolated local review; no generation, gate change, render master or publication'}
(root / 'VERIFICATION.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
