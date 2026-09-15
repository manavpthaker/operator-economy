# R11 avatar recovery QA

Review date: 2026-09-09. Reviewer: r11_avatar_qa, independent local technical and sampled image review. Scope: exact downloaded Sync 3 recovery asset, not the assembled R11 preview, a production gate, or final delivery approval.

## Result

The downloaded pickup is usable for the planned source intervals. Audio matches the exact pickup WAV with zero measured lag and no drift across five windows. Matched-frame inspection preserves the selected Seedance 404 performance outside the mouth region. Two integration controls are required: a browser-compatible 8-bit derivative or verified proxy, and the planned bottom-edge crop.

Normal-speed audiovisual and phoneme-level fidelity remain untested in this packet. Do not equate audio correlation with correct lip articulation.

## Bound inputs

| Input | SHA-256 |
|---|---|
| R11 public/media/presenter-pickups.mp4 | 6fb42c381d17d8dd2130e71a6986845f995f90d7e4f3c4a1a957b8973fbaf81f |
| R11 public/audio/presenter-pickups.wav | a6259d08e382661f35d66961e0ecfe02ee65f3467a70def3c4acea69b63106fd |
| Premium 004 review-media/404.mp4 | a0de31c36bde22219a1e067178b86cf750e7da1f11a69a775c370c82df6f29dd |

All three hashes were checked before diagnostics. The reproducible check-media.py rechecks these pins before every run.

## Technical facts

- New pickup: 1920×1080, progressive 24/1 fps, 275 frames, picture duration 11.458333 seconds. H.264 High 10, yuv420p10le, BT.709 tags, limited range.
- Embedded pickup audio: AAC, 48 kHz mono, 11.458 seconds. Reference WAV: signed 16-bit PCM, 48 kHz mono, 11.458333 seconds.
- Selected 404 source: 1920×1080, 24/1 fps, 289 picture frames, 12.041667 seconds. HEVC 10-bit source; its generated audio is not the narration authority.
- Full new-asset FFmpeg decode passed with exit code 0 and no error output.
- First planned picture use [0, 4.041667) consumes frames 0–96. Second use [6.666667, 11.083333) consumes frames 160–265. Both fit; the second has nine picture frames (0.375 seconds) after its exclusive out.
- Diagnostic tools: FFmpeg and FFprobe 8.1.1; bundled Python with NumPy. No network, model call, upload, credential read, or source write.

## Audio alignment

Both sources were decoded to 16 kHz mono float PCM. A normalized cross-correlation search tested every sample within ±100 ms for each window.

| Reference window | Best lag | Correlation |
|---|---:|---:|
| 0.300000–2.000000 | 0 samples / 0 ms | 0.9997442553 |
| 2.000000–4.041667 | 0 samples / 0 ms | 0.9998583617 |
| 4.100000–6.100000 | 0 samples / 0 ms | 0.9998179033 |
| 6.666667–8.600000 | 0 samples / 0 ms | 0.9997719177 |
| 8.600000–11.083333 | 0 samples / 0 ms | 0.9997777801 |

No provider lag compensation is indicated. In particular, do not import the older Test Q offset. Final sound must still come from the continuous original narration master; this provider-only concatenation is not the final soundtrack.

## Sampled picture review

Contact sheets compare output and 404 at frame numbers 0, 24, 48, 72, 96, 160, 186, 212, 238, and 265. These correspond to source seconds 0, 1, 2, 3, 4, 6.666667, 7.75, 8.833333, 9.916667, and 11.041667.

- The selected framing, head position, glasses, hair, wardrobe, background geometry and lighting remain consistent at the inspected matched frames.
- Mouth shapes change as intended; no obvious doubled lip, displaced jaw, broken glasses, or sampled face discontinuity was visible.
- Hands remain mostly below frame. A small fingertip enters at the bottom in the return range. This is not sufficient coverage to approve hand articulation or gesture quality.
- The first frame already has a slightly parted mouth. Its suitability at speech onset must be evaluated in the full-speed opening, not decided from the still alone.

### Findings

1. **Major, integration control: bottom-edge RGB artifact.** Enlarged bottom-strip inspections at frames 0, 160, and 265 show roughly the last three source rows corrupted by colored pixel stripes. The intended top-anchored 1280×724 cover treatment clipped to a 1280×720 frame removes more than this affected area. The orchestrator should confirm the actual composed frame after that treatment. No source repair was performed.
2. **Major, technical integration risk: H.264 High 10.** The provider output is 10-bit H.264, not a broadly browser-compatible 8-bit delivery source. Use a documented 8-bit derivative or validate the runtime proxy explicitly. FFmpeg decode alone does not establish Chrome/Studio playback.
3. **Observation: sampled performance retention is not temporal approval.** Ten matched samples show no unwanted non-mouth performance replacement, but cannot detect every shimmer, blink transition, finger artifact, or poor phoneme boundary.

## Evidence and limitations

Ignored diagnostics include measurements.json, output/source matched-frame contact sheets, enlarged face sheet, and bottom-strip sheet. The diagnostic images are not newly generated creative media and are not staged into the episode.

No normal-speed browser playback, complete sound listen, phoneme scoring, final-composition seek test, browser-proxy check, full R11 render, or post-encode delivery QA was performed. The parent orchestrator owns those checks while assembling the preview. Status is partial for audiovisual approval, not blocked: the source ranges, waveform timing, full decode, and requested sampled inspection are complete.

The episode-level README.md, episode.json, and input-lock.json are absent in this isolated agent workspace, consistent with the earlier source-audit packet. This review binds to the work order's three explicit input hashes and does not claim an episode gate exists or passed.
