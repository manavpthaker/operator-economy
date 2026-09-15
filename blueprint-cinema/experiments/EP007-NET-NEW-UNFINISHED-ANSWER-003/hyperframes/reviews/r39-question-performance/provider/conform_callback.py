"""Replace only the authorized first sentence; preserve all later original PCM."""
from pathlib import Path
import json, hashlib, wave

P = Path(__file__).resolve().parent
R = next(p for p in P.parents if (p / '.agents').is_dir())
V = P.parent
D = R / 'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/r39-callback-production'
cut = json.loads((D / 'CALLBACK-CUT.json').read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
pickup = R / cut['level_derivative']['path']
assert sha(pickup) == cut['level_derivative']['sha256']
original = V / 'public/audio/owner-dependency-narration.wav'
assert sha(original) == '1e80e680839594bf200839dfc75c5f00d9cec4dfbc91043b15ccca2ae2a52d82'
with wave.open(str(original)) as w:
    params, old = w.getparams(), w.readframes(w.getnframes())
with wave.open(str(pickup)) as w:
    assert (w.getframerate(), w.getnchannels(), w.getsampwidth()) == (48000, 1, 2)
    new = w.readframes(w.getnframes())
assert len(new) == 86000 * 2
assert (params.framerate, params.nchannels, params.sampwidth) == (48000, 1, 2)
out = V / 'public/audio/owner-dependency-his-r39.wav'
with wave.open(str(out), 'wb') as w:
    w.setparams(params)
    w.writeframes(new + old[len(new):])
with wave.open(str(out)) as w:
    actual = w.readframes(w.getnframes())
assert actual[len(new):] == old[len(new):]
master = R / 'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
assert sha(master) == 'd8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9'
record = {
    'callback_cut': {'path': str((D / 'CALLBACK-CUT.json').relative_to(R)), 'sha256': sha(D / 'CALLBACK-CUT.json')},
    'output': {'path': str(out.relative_to(R)), 'sha256': sha(out)},
    'original_s08_sha256': sha(original),
    'replacement_samples_half_open': [0, 86000],
    'replacement_review_seconds': [247.625, 249.41666666666666],
    'gain_db': -2.56, 'retime': False, 'timeline_shift_seconds': 0,
    'duration_seconds': len(actual)/96000,
    'all_original_pcm_after_callback_preserved': True,
    'canonical_master_unchanged': True,
    'limitations': 'Measured level and local transcription do not establish perceptual voice-match acceptance.'
}
(P / 'CALLBACK-CONFORM.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record, indent=2))
