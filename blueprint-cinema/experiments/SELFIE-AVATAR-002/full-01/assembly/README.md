# Week 2 full-01 assembly

Rendered: `renders/week2-full01-uncaptioned.mp4`, SHA-256
`ccdc0922a4e088fcbd3501aedede32df95be99018b65fc357ef7ccc1af059db9`.
HyperFrames check, exact frame-count probe and strict decode passed. The
encoded opening, both cut boundaries, midpoints and last frame were inspected;
`qa/encoded-contact.png` records the sampled output. Root's final audio QA and
owner review remain separate. See `reports/DELIVERY.json` for complete evidence.

HyperFrames 0.8.38, Node 25.6.1, local FFmpeg. The project is source-local and
uses a single capture worker to limit memory. No provider or upload is needed.

All inputs are copied byte-for-byte and hash-pinned in `INPUTS.json`, including
root's selected 720 × 1280, 24 fps derived sources:

- `public/media/middle.mp4`, 378 frames / 15.75 seconds.
- `public/media/closing.mp4`, 409 frames / 17.041666666666668 seconds.

Their source times must begin at the voice windows 6.083333333333333 and
21.833333333333332 seconds respectively. Do not pass a clip with extra leading
handles without updating its `data-media-start` deliberately.

Verify and render from this directory:

```sh
HYPERFRAMES_RUN_ID=selfie-week2-full01 npm run check -- --at 0,3,6.0416666667,6.0833333333,14,21.7916666667,21.8333333333,30,38.8333333333 --json
HYPERFRAMES_RUN_ID=selfie-week2-full01 npx --yes hyperframes@0.8.38 snapshot --at 3,14,30
HYPERFRAMES_RUN_ID=selfie-week2-full01 npm run render
npm run finish
ffprobe -v error -show_streams -show_format -of json renders/week2-full01-uncaptioned.mp4
```

The render command pins 24 fps, one worker, high quality and CRF 16. It writes
`renders/week2-full01-hyperframes-audio.mp4`; the required `finish` command
copies its picture bitstream while directly encoding the Original C WAV as
192 kb/s mono 48 kHz AAC into the final uncaptioned file. Root owns
the final audio and frame QA, sample review, delivery and approvals. Check the
actual delivered video for 933 frames, continuous Original C audio and clean
cuts; a successful render is not evidence of convincing facial performance.

Initialization used `HYPERFRAMES_SKIP_SKILLS=1` because this worker may only
write inside this folder. It read the installed HyperFrames, core, CLI,
general-video and media-use instructions. Root subsequently completed
`npx hyperframes skills update general-video` successfully with 0.8.38.

Root's B generation includes the initial “But” onset at source-master sample
291590 (6.074791666667 seconds). Root measures each restored source's audio
placement before selecting its source-frame in-point. The prepared input
must incorporate that measured restoration offset and frame quantization.
This supersedes native-only rounding assumptions. This composition consumes
the prepared B and C from source time zero and adds no further offset or
transformation. Audio remains on the exact master clock. Final source-frame
in-points and residual errors belong in root's alignment receipts.

The supplied prepared B retains restored source frames [2,380), accounting
for a measured 94.375 ms audio insertion plus the 8.541667 ms boundary
difference; residual picture quantization is −19.583333 ms. Prepared C
retains restored frames [8,417), accounting for a 334.9375 ms audio insertion;
its residual is −1.604167 ms. Both crops are already baked into the inputs.
See `../PICTURE-ALIGNMENT.json`. No additional trim, crop or offset is applied here.

## Audio finishing

The first HyperFrames render preserved timing but changed the voice's level:
root measured +2.17214 dB RMS and a decoded peak above full scale. That render
is preserved at `renders/week2-full01-hyperframes-audio.mp4`; it is not the final
audio authority. The finishing step replaces only its audio using the original
WAV, without filters, normalization, gain, stretching or speech splicing:

```sh
ffmpeg -v error -n -i renders/week2-full01-hyperframes-audio.mp4 -i public/audio/original-c.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -ac 1 -ar 48000 -movflags +faststart renders/week2-full01-uncaptioned.mp4
```

All 933 picture packet payload hashes and PTS/DTS/duration fields are identical
before and after this step. The final audio starts at zero, measures −0.00403 dB
RMS relative to the master, has peak 0.921297 and zero lag in the tested 1–5 second
window. Global zero-lag waveform correlation is 0.99998847. Root owns the full
39-window voice check. See `reports/AUDIO-FINISHING.json`.

`finish` refuses to overwrite an existing final file. For a future authorized
revision, preserve the existing version under a new name before running it.
