# Technical validation

Verdict: **PASS WITH LIMITATIONS**. The accepted Resolve renders clear the picture, cadence, audio, local-media, and interchange tests. Captions remain sidecar-only, and the final Resolve render was not repeated inside a network-isolated sandbox.

## Accepted artifacts

- Master: `delivery/EP006_POLISH_002_COVERAGE_FIRST_RETURN_LOOP_MASTER.mov` — SHA-256 `0836f23edd88214729021bcbe06aaa4b68a26ff6ce4b08d7a059190eac083839`.
- Review: `delivery/EP006_POLISH_002_COVERAGE_FIRST_RETURN_LOOP_REVIEW.mp4` — SHA-256 `5ed3cda048c4240652476b4414fd60da0be24047054314005d3551036da9b6d8`.
- Resolve project: `resolve/project/EP006_POLISH_002_COVERAGE_FIRST_RETURN_LOOP.drp` — SHA-256 `93eeead059a78b4cbc6e30575a3af52f6d820af4c9d0bc2e2bdbcbfdfc0291b2`.

## Input identity

- Canonical MP3 SHA-256: `95e90a1ebb5dfbc6e13bc2efd12915cea9f15807199b0301cd3f63d59cb8e468` — exact expected match.
- Extracted locked WAV: PCM s24le, mono, 48 kHz, 30.405 s; SHA-256 `7dd5386afd0e1bfc267b7ae8424dd4e87f7fa534cfd98c0dca410f33b2ea3fb5`.
- Picture quantization: 912 frames at 30 fps, 30.400 seconds. The 0.005-second source-window remainder is intentionally outside the valid picture frame grid; narration was not retimed or time-stretched.
- Locked narration and word-cue hashes were independently recomputed and corrected in `inputs/canonical-inputs.json`.

## Picture and cadence

- Master and review: 1920×1080, progressive 30/1 fps, exactly 912 decoded video frames, start timecode `01:00:00:00`.
- Master: ProRes 422 HQ, 10-bit 4:2:2, exact 30.400-second container.
- Review: H.264 High, 4:2:0; AAC priming extends container/audio metadata to 30.464 seconds, but decoded picture remains exactly 912 frames/30.400 seconds.
- All 13 final moving-source intermediates contain zero exact adjacent duplicate transitions. The rejected simple 25→30 cadence proxies and their rejected Resolve renders are preserved as QC evidence.
- Final accepted review contains zero exact adjacent duplicate transitions. Low-motion detection identifies 0.100 seconds at 15.000–15.100 and the authored S09 schematic hold at 15.333–16.333; neither is a broken repeated-frame cadence.
- Black/flash detection found no qualifying black interval. Boundary samples show no one-frame gap at S09 entry/exit or the exclusive picture end.
- Both deliveries decode end to end without error. A real-time `-re` decode of the accepted review completed all 912 frames at normal speed.

## Audio

- Master: PCM s24le, stereo, 48 kHz, exact 30.400 seconds.
- Review: AAC stereo, 48 kHz; picture remains exact despite codec padding.
- Integrated loudness: `-15.0 LUFS`.
- True peak: `-3.2 dBFS`.
- No NaNs, infinities, clipped samples, or audible decode discontinuity were detected.
- The terminal 0.487-second low-level/silence detector event is the intentional resolved end hold after narration, not an accidental mid-cut dropout.
- A1/A2/A3/A5 remain separately editable in Resolve and disabled after the first mix measured too loud. A6 is the accepted normalized mix print derived from those retained stems. A4 remains deliberately unused because no restrained, rights-cleared music improved the observational sequence.

## Graphics, text, and alpha

- HyperFrames full check: 0 errors; one reviewed warning for seven timed elements on the master overlay track. Runtime, layout, and motion checks pass.
- Final graphics alpha: ProRes 4444 `yuva444p12le`, 1920×1080, 30 fps, 912 frames; SHA-256 `8052dc1e94b9c420a08a51179f100d65bd6228eedb55969b1848b97470ac3013`.
- Final disclosure alpha: ProRes 4444 `yuva444p12le`, 1920×1080, 30 fps, 912 frames; SHA-256 `2ec6cefa3f6e3c77a96eeb66ed6b784406862b4ca0c163c9016dfae977c4abdb`.
- Thin rules and alpha edges survive the accepted H.264 compression sample. The final 480×270 legibility grid confirms the disclosure and operational labels are readable after the typography correction.
- All authored HTML files were scanned for remote URLs, CDN imports, and runtime network dependencies; none remains. Fonts, GSAP, audio, and graphics are local and hash-pinned.

## Resolve and interchange

- Project: `EP006_POLISH_002_COVERAGE_FIRST_RETURN_LOOP`.
- Timeline: `EP006_POLISH_002_COVERAGE_FIRST_RETURN_LOOP_FINAL`.
- Timeline evidence: 912 frames, exclusive end 108912, five video tracks, six audio tracks after retained-stem mix correction, one subtitle-review track.
- Final Resolve render jobs: master `71e67606-bb0f-4f4f-9d38-e1b7de29eb10`; review `7fd14352-0587-442e-8708-56a609d3ae00`.
- `.drp` and final OTIO are authoritative. The FCPXML package predates the cadence/legibility relinks and is retained as non-authoritative interchange evidence.
- Completed render jobs, successful local relinks, full decodes, and the final DRP support no-missing-media/no-offline-frame status.

## Limitations

- The exact authored SRT is present and timed, and Resolve contains a subtitle-review track, but free Resolve rejected scripted auto-caption creation behind a Studio purchase modal. No purchase was made; accepted exports do not embed captions.
- All HyperFrames dependency checks and renders were local-only, and Resolve used only local relinked assets. A separately controlled network-isolated final Resolve rerender was not performed, so clean-room status is not independently verified.
- Motion-compensated 25→30 intermediates remove broken duplicate cadence but introduce interpolated temporal frames; their aesthetics remain subject to the creative review.

Evidence: `qa/reports/final-master-ffprobe.json`, `qa/reports/final-review-ffprobe.json`, `qa/reports/accepted-ebur128.log`, `qa/motion-audit/accepted-black-freeze-detect.log`, `qa/motion-audit/accepted-exact-duplicates.txt`, `qa/final-frames/accepted-480x270-legibility-grid.png`, Resolve build/correction logs, and `qa/reports/INDEPENDENT-TECHNICAL-QA.md`.
