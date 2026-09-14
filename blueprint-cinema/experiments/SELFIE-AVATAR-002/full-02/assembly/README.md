# Week 2 full-02: continuous opening

This revision removes the cut at “But” by using one continuous source for the
first 524 frames. The closing is the exact existing prepared full-01 source.
All full-01 files remain untouched.

Rendered: `renders/week2-full02-uncaptioned.mp4`, SHA-256
`adf61f3bb7790ce2039d4bffadf8992d3eaba9039a593232502407c0adc28677`.
HyperFrames check passed with no findings. Exact encoded source-frame
comparisons, final decode, 933-frame probe and protected prior-media hashes
passed. Root's 39-window audio check passed with zero drift; its authoritative
record is `../FINAL-AUDIO-QA.json`.
Owner review remains separate. See `reports/DELIVERY.json`.

| Input | Timeline | Source |
|---|---|---|
| `public/media/opening-continuous.mp4` | [0,524) | Link to confirmed `../media/opening-prepared.mp4` |
| `public/media/closing.mp4` | [524,933) | Link to exact full-01 `closing-prepared.mp4` |
| `public/audio/original-c.wav` | 0–38.87020833333333s | Link to unchanged full Original C master |

Inputs must be aligned and framed before entering this assembly. Source time is
zero for both clips. No additional crop, source offset, audio timing change or
transformation is introduced here. The protected prior-media hashes are in
`reports/PROTECTED-BASELINE.json`; the local links and input hashes are in
`INPUTS.json`.

The project reuses HyperFrames 0.8.38, its prior verified composition structure
and local GSAP. Output remains 720 × 1280, 24 fps, 933 frames / 38.875 seconds.
To reproduce this authorized candidate, run from this directory:

```sh
HYPERFRAMES_RUN_ID=selfie-week2-full02 npm run check -- --at 0,3,6,6.2,14,21.79,21.84,30,38.83 --json
HYPERFRAMES_RUN_ID=selfie-week2-full02 npx --yes hyperframes@0.8.38 snapshot --at 3,6,6.2,14,21.79,21.84,30,38.83
HYPERFRAMES_RUN_ID=selfie-week2-full02 npm run render
npm run finish
ffprobe -v error -show_streams -show_format -of json renders/week2-full02-uncaptioned.mp4
```

`render` writes `renders/week2-full02-hyperframes-audio.mp4`, using one worker,
high quality and CRF 16. The required `finish` step copies that exact video
bitstream and encodes the untouched Original C WAV directly as mono 48 kHz AAC
at 192 kb/s. This retains the voice's original level; full-01 demonstrated that
the HyperFrames mix could raise it despite an authored volume of one.

`finish` uses no filters, normalization, gain, stretching or audio splicing and
refuses to overwrite an existing final. Expected final:
`renders/week2-full02-uncaptioned.mp4`.

Verification must establish all 933 frames, correct source boundaries, no cut
at “But”, unchanged video packets after audio finishing, Original C level within
0.1 dB, no clipping and zero measured audio drift. Root owns full-window voice
QA, continuous visual performance review and delivery. A technical pass is not
owner acceptance.

The opening source SHA-256 is
`a36b6644b44d867cc8b570d9d72bce4bf8922b69619f5c6084baf0102931fc33`.
Root retained restored source frames [2,526), accounting for the measured
69.4375 ms returned audio offset with a +13.895833 ms picture quantization
residual. No spatial transform was applied. See `../PICTURE-ALIGNMENT.json`
and `../opening/PREPARED.json`; the assembly adds no further offset.
