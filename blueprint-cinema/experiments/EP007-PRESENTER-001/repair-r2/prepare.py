#!/usr/bin/env python3
import hashlib
import json
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
ROOT = PACKET.parents[2]
EP = ROOT / 'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production'
master = EP / 'master/narration-master.v4.wav'
words_path = EP / 'word-transcript.json'
expected_master = 'd8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9'
expected_words = 'f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7'
assert hashlib.sha256(master.read_bytes()).hexdigest() == expected_master
assert hashlib.sha256(words_path.read_bytes()).hexdigest() == expected_words
words = json.loads(words_path.read_text())['words'][1663:1679]
assert words[0]['start'] == 591.3 and words[-1]['end'] == 596.4
dest = PACKET / 'media/repair-r2'
dest.mkdir(exist_ok=True)
wav = dest / 'scope-two-sentences.wav'
with wave.open(str(master), 'rb') as src:
    params = src.getparams()
    start, end = round(591.05 * params.framerate), round(596.65 * params.framerate)
    src.setpos(start)
    data = src.readframes(end - start)
    with wave.open(str(wav), 'wb') as out:
        out.setparams(params)
        out.writeframes(data)
with wave.open(str(wav), 'rb') as check:
    assert check.readframes(check.getnframes()) == data
manifest = {
    'status': 'audio_prepared_performance_unverified',
    'master_sha256': expected_master,
    'transcript_sha256': expected_words,
    'source_in_seconds': 591.05,
    'source_out_seconds': 596.65,
    'duration_seconds': 5.6,
    'source_in_sample': start,
    'source_out_sample_exclusive': end,
    'word_ids': [w['w_id'] for w in words],
    'text': ' '.join(w['token'] for w in words),
    'audio_path': str(wav.relative_to(PACKET)),
    'audio_sha256': hashlib.sha256(wav.read_bytes()).hexdigest(),
    'pcm_matches_source': True,
    'look_sha256': '59309d2925b85cfba8a6a411dce1ecea67a03607f8a05933f4a2f6cb6af27754',
}
(HERE / 'input-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest, indent=2))
