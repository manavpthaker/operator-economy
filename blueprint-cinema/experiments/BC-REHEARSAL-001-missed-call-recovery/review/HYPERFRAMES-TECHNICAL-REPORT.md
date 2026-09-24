# HyperFrames technical validation

## Result

The renderable root composition passes the pinned HyperFrames `0.8.4` automated gates and produced a complete review MP4. This is technical validation, not creative approval.

## Project and toolchain

- Owning workflow: `general-video`
- HyperFrames CLI pin: `0.8.4`
- Node.js: `v25.6.1`
- FFmpeg / ffprobe: `8.1.1`
- Canvas: `1920x1080`
- Frame rate: `30 fps`
- Root duration: `61.411354 seconds`
- Root composition: `hyperframes/index.html`
- Final render: `hyperframes/renders/BC-REHEARSAL-001-directed-animatic-final.mp4`

The project invokes `npx --yes hyperframes@0.8.4`; the version is explicit rather than inherited from a global install. All fonts, GSAP, narration, and fixture material used at render time are local. The renderable composition contains no `http://`, `https://`, fetch, XHR, websocket, or narration-driven layout selection.

## Structural authoring gates

Command:

```text
npx --yes hyperframes@0.8.4 lint .
```

Result: `PASS` — 0 errors, 0 warnings.

Command:

```text
npx --yes hyperframes@0.8.4 check .
```

Result: `PASS`.

- Lint: 0 errors, 0 warnings; 10 non-blocking `pointer-events` information notes.
- Runtime: 0 errors, 0 warnings.
- Layout: 0 issues across 9 sampled frames.
- Motion: 0 errors, 0 warnings.
- Contrast: 62 of 62 tested pairs pass WCAG AA.

The Studio project browser also indexes standalone style-frame HTML and transported sub-composition templates, so its project-wide badge can show non-root discovery notes for their relative asset paths. Those files are not render-time network dependencies. The pinned CLI check against the renderable root and its mounted children passes.

## Preview and snapshot checks

- Studio preview opened the local root composition and showed seven adjacent clips plus one locked VO track.
- The playhead was scrubbed through the human-gate and stop/book section; the root persistent tag, card, and fixture disclosure updated with the intended shot-local action.
- Entry, action, consequence, midpoint, and exit snapshots exist for all seven shots under `hyperframes/snapshots/review/`.
- Each shot has a local contact sheet.
- The final rendered contact sheet is `hyperframes/renders/BC-REHEARSAL-001-contact-sheet-final.jpg`.
- The final 480x270 legibility pass is under `review/phone-legibility-final/`.

## Render command and result

```text
npx --yes hyperframes@0.8.4 render . \
  --output renders/BC-REHEARSAL-001-directed-animatic-final.mp4 \
  --fps 30 --quality standard --workers auto \
  --strict-all --no-best-effort --skill general-video
```

Result: `PASS` — 1,843 frames rendered in 48.6 seconds. HyperFrames self-verification passed its verification frames. The output contains one H.264 video stream and one AAC audio stream.

The first post-render agent pass found a stale `REVIEWED` tag after booking, a missing Shot 06 ticket label, incorrect subframe conform rounding, a zeroed opening time counter, and weak human-gate emphasis. Root integration corrected those issues, rendered a new hash-distinct final MP4, and issued two bounded final-verification work orders. Earlier MP4s remain as review history; they are not handoff references.

## Media probe

- Container: MP4 / ISO Base Media
- Video: H.264 High, yuv420p, progressive, 1920x1080, square pixels, Rec.709, 30/1 fps, 1,843 frames
- Video duration: `61.433333 seconds`
- Audio: AAC-LC, 48 kHz, stereo, `61.418000 seconds`
- Container duration: `61.433333 seconds`
- File size: `3,343,339 bytes`
- SHA-256: `a9f21223385ff12dd60b7c0f3572d1cd14e70e5fb72907ddc76ebe85cbe824b3`
- Decoded audio versus locked VO APSNR: approximately `165.054 dB`
- Audio peak: approximately `-1.61 dBFS`
- Audio RMS: approximately `-16.11 dBFS`
- Black-frame probe: no black interval of at least 0.10 seconds at the tested threshold.

The 0.021979-second difference between locked VO duration and container duration is the expected 30-fps whole-frame ceiling: `ceil(61.411354 × 30) = 1,843` frames. Audio remains within one video frame of the locked authority.

## Known tool metadata defect

The MP4 container tag says `hyperframes_version=0.0.0-dev`, although the executed CLI and project command pin are `0.8.4`. The command, package invocation, and CLI output prove the version used; the embedded tag is not accepted as version authority. This should be fixed upstream before an automated handoff trusts container metadata alone.

## Boundary

The complete render exists and is technically valid as a directed animatic. It is not a finished film, a public-evidence artifact, a Resolve conform, a creative approval, or a production-state advancement.
