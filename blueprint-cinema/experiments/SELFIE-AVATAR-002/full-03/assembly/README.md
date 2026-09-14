# Week 2 full-03: motion-conditioned continuation

Rendered: `renders/week2-full03-uncaptioned.mp4`, SHA-256
`a1d380ca1f6378ce0df50b66dd968726196226a891c04b14d0eca0726050ac1b`.
HyperFrames check, the 933-frame probe, strict decode, picture packet identity
through finishing and all eight protected prior-media hashes passed. Assembled
snapshots at the join and preparatory/body boundary were inspected. Root owns
the final encoded seam and full-window audio review; owner approval remains
separate. See `reports/DELIVERY.json`.

The exact full-02 opening is retained for frames [0,524). Root's forward video
extension supplies [524,933), conditioned on the actual opening motion.
The entire Original C recording remains continuous and unchanged.

| Input | Timeline | Binding |
|---|---|---|
| `public/media/opening-continuous.mp4` | [0,524) | Exact full-02 `opening-prepared.mp4` |
| `public/media/extension.mp4` | [524,933) | Confirmed `../media/extension-prepared.mp4` |
| `public/audio/original-c.wav` | 0–38.87020833333333s | Original full master |

The input links are read-only. All transformations and timing corrections must
already be included in root's prepared extension. The assembly reads source
time zero and adds no crop, offset or retiming. `INPUTS.json` records hashes
and links; `reports/PROTECTED-BASELINE.json` pins eight prior critical media
files. Every write by this worker remains inside full-03/assembly.

HyperFrames 0.8.38, 720 × 1280, 24 fps, 933 frames / 38.875 seconds. Once root
confirms the new input, use the existing check/render/finish sequence:

```sh
HYPERFRAMES_RUN_ID=selfie-week2-full03 npm run check -- --at 0,3,6,14,21.79,21.84,22.1,30,38.83 --json
HYPERFRAMES_RUN_ID=selfie-week2-full03 npx --yes hyperframes@0.8.38 snapshot --at 3,14,21.6,21.79,21.84,22.1,30,38.83
HYPERFRAMES_RUN_ID=selfie-week2-full03 npm run render
npm run finish
ffprobe -v error -show_streams -show_format -of json renders/week2-full03-uncaptioned.mp4
```

Before render, inspect the actual prepared join in motion. After render,
inspect the encoded join again, including frames around 523→524. Head pose,
face scale, shoulders, expression and motion direction must remain credible.
Matching framing, waveform, timestamps or a low frame-difference statistic
alone cannot clear `reports/CREATIVE-SEAM-REVIEW.json`.

`render` uses one worker, high quality and CRF 16, writing
`renders/week2-full03-hyperframes-audio.mp4`. The required `finish` step copies
the same picture bitstream and directly encodes Original C as mono 48 kHz AAC
at 192 kb/s. It avoids the unwanted level change observed in HyperFrames' mix.
No filters, normalization, gain, stretching or audio splices are applied.
`finish` refuses to overwrite the final file.

Expected final: `renders/week2-full03-uncaptioned.mp4`. Verify all 933 frames,
strict decode, identical video packets before/after audio finishing, unchanged
prior-media hashes, source voice level within 0.1 dB, no clipping and zero
measured audio drift. Root owns complete voice QA, seam review and delivery;
owner approval remains separate.

The final output contains 933 picture packets and 1,824 audio packets. Audio
packet payloads and timestamps are identical to the verified full-02 final
master, preserving the same Original C level and clock through direct audio
finishing. This technical result does not establish that the new visual join
feels continuous; that verdict belongs in the creative seam review.

The prepared extension SHA-256 is
`b274c7de439dc42148b8ad679339f3d0ca80b6057067865b79217e246cf0df2f`.
Root's restoration inserted 321.0625 ms before the source voice. To retain the
matching first pose and complete preparatory blink, root mapped restored
source frames [0,20) into extension output [0,12), then used [20,417) at 1×
for [12,409). Only the first half-second of picture is compressed; the complete
Original C recording remains unchanged. The later picture rounding residual
is +12.270833 ms. Root and independent diagnosis reviewed this prepared join.
See `../PICTURE-ALIGNMENT.json`; this assembly adds no further timing change.
