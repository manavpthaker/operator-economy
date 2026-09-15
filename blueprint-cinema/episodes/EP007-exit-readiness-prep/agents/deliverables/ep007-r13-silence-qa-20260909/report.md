# R13 silence-cut QA

2026-09-09 · Independent QA reviewer r11_avatar_qa · Proposed review-only splice, not a final render or gate approval.

## Result

The proposed removal of master [45, 48) seconds removes only digital silence. All 144,000 removed PCM samples are exactly zero. No transcript word intersects the cut. The join is zero to zero, so it introduces no sample discontinuity; a corrective fade is not required for this splice.

The original narration file was read only. This review checks the proposed operation, not the as-built R13 audio file or its playback.

## Bound inputs

| Input | SHA-256 |
|---|---|
| R12 index.html | 146b3c747e5fa84f33ac9a90c7ef797a3362fa3e9c3fb14b2e3b5988ff5ea65a |
| narration-master.v4.wav | d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9 |
| word-transcript.json | f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7 |

All pins match. R12 was inspected only for existing root, identity, title and audio timing. No broader asset audit was performed.

## Sample-level measurements

Master format: 48,000 Hz, signed 16-bit PCM, one channel.

| Measurement | Result |
|---|---:|
| Removed sample interval, zero-based and end-exclusive | [2,160,000, 2,304,000) |
| Removed samples | 144,000 |
| Nonzero removed samples | 0 |
| Removed peak / RMS | 0 / 0; negative-infinity dBFS |
| Last retained sample before cut | 0 |
| First retained sample after cut | 0 |
| Join amplitude step | 0 |
| 10 ms immediately before and after both cut boundaries | All samples zero |

The last nonzero sample before the cut is master sample 2,139,207 at 44.5668125 seconds. The first nonzero sample after the cut is master sample 2,327,151 at 48.4823125 seconds. After removal, the continuous digital-zero run still contains 43,943 samples, or 0.915479167 seconds. This retains the late tail of the preceding phrase and the early waveform onset before the transcript's 48.52-second word cue.

No timed words intersect [45, 48). The preceding word is “running.” at 44.16–44.50. The following word is “This” at 48.52–48.68. These word boundaries are transcript timings, not sample-level speech-onset claims.

## Exact edit and cue mapping

Keep master samples [0, 2,160,000), then [2,304,000, 2,856,000). Concatenate without resampling, stretching, normalization, rewritten words or crossfades.

The result is 2,712,000 samples = 56.5 seconds = 1,356 frames at 24 fps. Exactly 72 picture frames of time are removed. The mapping is unchanged before review 45 seconds; for review time at or after 45 seconds, source time is review time + 3 seconds.

| Cue | Original master / R12 | R13 review |
|---|---:|---:|
| Identity screen begins | 44.500000 | 44.500000 |
| “This” narration starts | 48.520000 | 45.520000 |
| “The Operator Economy” | 48.860000–49.880000 | 45.860000–46.880000 |
| “build” | 52.080000 | 49.080000 |
| “own” | 52.600000 | 49.600000 |
| “operate” | 53.160000 | 50.160000 |
| Introduction's “one.” ends | 55.420000 | 52.420000 |
| Spoken “Today” begins | 56.040000 | 53.040000 |
| Existing title picture cut, frame-aligned | 56.041666667, frame 1345 | 53.041666667, frame 1273 |
| “practice.” ends | 59.230000 | 56.230000 |
| Review end | 59.500000, frame 1428 | 56.500000, frame 1356 |

The pre-speech branding hold becomes 1.02 seconds from the identity picture cue to the transcript's “This” cue. The complete identity picture slot becomes 8.541666667 seconds if the existing title boundary is retained; it is not a one-second screen overall.

## Findings and limits

No blocking or major finding in the proposed silence-only operation. Sample continuity does not establish the final encoded file, browser playback, narrative pacing, or sound mix. The orchestrator should verify the actual R13 PCM equals these two source intervals and listen once across the completed join. This packet did not create audio, listen to playback, inspect the new handoff sketch, or approve any production state.

Commands performed: shasum -a 256 on all three pins; read-only R12 timing inspection with rg; bundled Python wave/NumPy inspection of PCM sample values and zero runs; transcript interval intersection and arithmetic checks. Only this report and deliverable.json were authored in the assigned packet.
