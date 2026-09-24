# Independent Technical QA

Verdict: **PASS WITH LIMITATIONS — the typography-rerendered delivery passes the objective picture, cadence, audio, decode, local-media, Resolve-project, sampled 480x270 legibility, and manifest checks performed here.** Captions remain sidecar-only; the FCPXML package was not refreshed after the cadence relink; clean-room rerendering and broader visual-quality judgments are not independently certified by this report.

Scope: read-only re-audit of the accepted delivery filenames after cadence, PCM, and alpha-typography correction; the locked inputs; motion-compensated handoff media; HyperFrames alpha renders; sampled 480x270 legibility evidence; final DRP/OTIO/log evidence; and final manifests. This is a technical review only. It does not approve creative quality, continuity, visual storytelling, interpolation aesthetics, or documentary truthfulness.

## Final accepted delivery

### Mezzanine master

File: `delivery/EP006_POLISH_002_COVERAGE_FIRST_RETURN_LOOP_MASTER.mov`

- SHA-256: `0836f23edd88214729021bcbe06aaa4b68a26ff6ce4b08d7a059190eac083839`.
- Video: ProRes 422 HQ-class stream, 1920x1080, 10-bit 4:2:2, limited-range BT.709.
- Frame rate: exact `30/1` fps.
- Picture count and duration: exactly 912 decoded frames and 30.400 seconds.
- Timecode: `01:00:00:00`.
- Audio: stereo PCM signed 24-bit little-endian, 48 kHz, exactly 1,459,200 samples per channel and 30.400 seconds.
- Integrated loudness: `-15.0 LUFS`.
- Loudness range: `2.0 LU`.
- True peak: `-3.2 dBFS`; sample peak `-3.184 dBFS`. No level clipping is indicated.
- Full video/audio decode completed with exit status 0.
- Black detector found no interval at `d=0.01`, `pix_th=0.02`, `pic_th=0.98`.
- Silence detector found only the ending interval `00:29.932688–00:30.400`, approximately 0.467 seconds. This is within the final picture hold; whether its dramatic length is appropriate is a creative/audio-mix judgment.

### H.264 review

File: `delivery/EP006_POLISH_002_COVERAGE_FIRST_RETURN_LOOP_REVIEW.mp4`

- SHA-256: `5ed3cda048c4240652476b4414fd60da0be24047054314005d3551036da9b6d8`.
- Video: H.264, 1920x1080, 8-bit 4:2:0, limited-range BT.709.
- Frame rate, picture count, and picture duration: exact `30/1` fps, 912 decoded frames, 30.400 seconds.
- Timecode: `01:00:00:00`.
- Audio: stereo AAC, 48 kHz. The AAC/container duration is 30.464 seconds because of codec padding; picture remains exactly 30.400 seconds.
- Integrated loudness: `-15.0 LUFS`; loudness range `2.0 LU`; true peak `-3.2 dBFS`.
- Decoder reports no NaNs, infinities, or denormals in decoded audio.
- Full video/audio decode completed with exit status 0.
- Black detector found no qualifying black interval.

The corrected loudness and PCM master satisfy the requested approximately `-14 to -16 LUFS`, no-higher-than `-1 dBTP`, 48 kHz, exact-picture-duration, and no-clipped-samples targets.

## Cadence and duplicate-frame audit

The Resolve timeline is now relinked to 13 files under `resolve/handoff/video_interpolated/`. These are 30 fps ProRes intermediates created from the frozen 25 fps moving originals with motion-compensated interpolation. OTIO references the interpolated paths, and `resolve-cadence-pcm-correction-render-log.txt` records all 13 relinks before the final render jobs.

I generated frame MD5s for every interpolated intermediate:

| Interpolated select | Frames | Adjacent exact duplicates |
|---|---:|---:|
| `pexels-7820463-select.mov` | 129 | 0 |
| `pexels-7820464-select.mov` | 111 | 0 |
| `pexels-7820468-select.mov` | 99 | 0 |
| `pexels-7820469-select.mov` | 129 | 0 |
| `pexels-7820470-select.mov` | 216 | 0 |
| `pexels-7820473-select.mov` | 105 | 0 |
| `pexels-7820474-select.mov` | 114 | 0 |
| `pexels-7820475-select.mov` | 90 | 0 |
| `pexels-7820477-select.mov` | 108 | 0 |
| `pexels-7820505-select.mov` | 126 | 0 |
| `pexels-7820516-select.mov` | 120 | 0 |
| `pexels-7820549-select.mov` | 96 | 0 |
| `pexels-7820551-select.mov` | 90 | 0 |

The accepted master contains 12 adjacent exact duplicate transitions, all in one run from frames 477 through 489. That run is inside the declared full-frame S09 suppression insert at frames 460–490 (`00:15.333–00:16.333`). Outside that deliberately held schematic interruption, the accepted master contains **zero adjacent exact duplicate transitions**. The earlier approximately six-frame repeated cadence is gone.

`freezedetect` reports the deliberate one-second suppression hold and a separate 0.200-second low-motion interval at approximately `00:14.767–00:14.967`. The latter is not an exact frame-repeat run; machine analysis alone cannot determine whether it is an intended pause or perceptually distracting.

The 29.4 seconds of reality coverage originates in genuinely moving 25 fps source clips. Motion-compensated frames added for the 30 fps conform are synthesized temporal intermediates, not additional source-native events. This conversion now passes the explicit no-broken-duplicate-cadence check; visual artifacts from interpolation still require normal-speed human inspection.

## Locked-input identity

- Canonical VO MP3 SHA-256: `95e90a1ebb5dfbc6e13bc2efd12915cea9f15807199b0301cd3f63d59cb8e468` — exact match.
- `inputs/locked-return-loop.wav`: SHA-256 `7dd5386afd0e1bfc267b7ae8424dd4e87f7fa534cfd98c0dca410f33b2ea3fb5`, 48 kHz mono PCM s24le, 30.405 seconds — exact match.
- `inputs/locked-narration.txt`: SHA-256 `1000f18386bc6b9e7004cd2dbb458f444151174d6cac7b7687bc91ee4acb2d93` — matches the corrected manifest.
- `inputs/word-cues.json`: SHA-256 `f5bd3c323b6373f08ec0b597e672ea70365a5a65b4e56af0435c234a44b2f1c3` — matches the corrected manifest.
- Episode engine, world, visual plan, and production-state locators now exist and their current hashes match `canonical-inputs.json`.

The Resolve/OTIO evidence retains the locked VO source separately on A1 and the final mix print separately on A6. This proves the correct locked file is present in the conform. It does not permit a mathematically isolated comparison of VO samples after the final mix because ambience, foley, and design are intentionally combined in the delivery.

## HyperFrames and alpha evidence

- `EP006_002_GRAPHICS_ALPHA.mov`: ProRes alpha (`yuva444p12le`), 1920x1080, 30 fps, 912 frames, 30.400 seconds; SHA-256 `8052dc1e94b9c420a08a51179f100d65bd6228eedb55969b1848b97470ac3013`; decode passes.
- `EP006_002_DISCLOSURE_ALPHA.mov`: ProRes alpha (`yuva444p12le`), 1920x1080, 30 fps, 912 frames, 30.400 seconds; SHA-256 `2ec6cefa3f6e3c77a96eeb66ed6b784406862b4ca0c163c9016dfae977c4abdb`; decode passes.
- `hyperframes-plates.json` now records both hashes, job IDs, V3/V4 assignments, 912-frame timing, and zero remote HTML dependencies.
- HyperFrames lint: 0 errors and one reviewed `timeline_track_too_dense` warning.
- HyperFrames check: passed; runtime 0 errors/warnings, layout 0 issues across 9 samples, and motion 0 errors/warnings.

The automated HyperFrames check had snapshots disabled and reported `0/0` contrast checks. I separately inspected `qa/final-frames/accepted-480x270-legibility-grid.png`, which presents nine accepted frames as actual 480x270 panels. In that sampled grid, the synthetic-visualization disclosure, primary operational labels, subordinate annotations, and direct-confirmation label are readable at the target size; their navy/cream treatments remain distinguishable against picture. This is a sample-based legibility pass, not exhaustive proof for every animated frame or every compression state. Alpha-edge aesthetics and thin-rule behavior between the sampled frames still require normal-speed review.

## Resolve project, conform, and render evidence

- Final DRP SHA-256: `93eeead059a78b4cbc6e30575a3af52f6d820af4c9d0bc2e2bdbcbfdfc0291b2`.
- The DRP is a valid ZIP archive; `unzip -t` reports no archive errors.
- Final OTIO SHA-256: `cc1e82b279bb028b70ff1700dc0a61d3d9bede0b59bf3f4c47443f47aad5f915`.
- OTIO parses as `Timeline.1`, contains 11 named tracks, and references the 13 cadence-corrected local intermediates.
- Track structure: V1 primary reality, V2 cutaways/inserts, V3 HyperFrames graphics, V4 disclosure/title, V5 caption review; A1 locked VO, A2 ambience, A3 foley, A4 deliberately unused music, A5 design accents, and A6 final Fairlight mix print with source stems retained.
- All OTIO media target paths existed during this review.
- Corrected cadence/PCM Resolve render log records project relink of all 13 sources, final timeline length 912 frames, five video tracks, six audio tracks, and successful DRP export. The later legibility render log records relink of both enlarged HyperFrames alpha plates, another 912-frame completion, and export of the currently accepted DRP.
- Final typography master render job `71e67606-bb0f-4f4f-9d38-e1b7de29eb10`: Complete.
- Final typography review render job `7fd14352-0587-442e-8708-56a609d3ae00`: Complete.
- Pre-cadence and pre-loudness DRPs and rejected outputs are preserved rather than overwritten.

The FCPXML package still has SHA-256 `9cd1bd132843299035377a4a641f37bb0bd38ebc9b9705724e0f92103140dd85`, unchanged from the pre-cadence export, and references the older `resolve/handoff/video/` files rather than `video_interpolated/`. All its paths exist, but it is not a faithful final-state interchange after the cadence relink. The updated OTIO and final DRP are the authoritative final interchange/project evidence; the FCPXML should be labeled pre-correction or re-exported if final-state parity is required.

The original build report also recorded `timelinePlaybackFrameRate` as 24 while timeline rate, monitor format, OTIO, final renders, and exact output cadence are 30 fps. The corrected output is objectively 30 fps, but this stale build-setting field was not superseded by a structured final settings dump.

## Manifests and provenance

The required manifests are now populated and internally coherent:

- `asset-provenance.json`: complete provider/license summary, disclosure, original and intermediate full SHA-256 values, page URLs, creator, timeline shot, and temporal-conform method for all 13 sources.
- Every intermediate hash in the provenance manifest matches the corresponding local file.
- `source-selects.json`: 14 exclusive-end shot uses, 13 distinct moving sources, 29.4 seconds of moving coverage, and 1.0 second graphic-only picture.
- `hyperframes-plates.json`: both validated alpha outputs and Resolve tracks.
- `resolve-handoff.json`: final project/timeline/track map, caption limitation, interchange paths, and corrected render job IDs.
- `finishing-manifest.json`: final typography-rerender delivery hashes, picture/audio specifications, loudness, cadence result, ported-utility provenance, preserved rejected renders, and explicit non-public/non-canonical status.

The provenance manifest states that Pexels licensing was reviewed on 2026-08-21 and no paid media was used. This audit verifies that the local manifest is complete and hash-consistent; it did not independently re-adjudicate the legal meaning of the external license or the correctness of every page title.

## Captions and remaining verification limits

Neither accepted export contains an embedded subtitle stream. The authored SRT exists, contains seven non-overlapping cues, begins at `00:00:00.000`, and ends at the exact picture boundary `00:00:30.400`. Resolve evidence reports a caption/subtitle review track, but `resolve-handoff.json` truthfully records that scripted auto-captioning was rejected behind a Studio upgrade modal and no purchase was made. Captions therefore remain sidecar/review-track material rather than an embedded delivery stream.

The following are outside what these machine checks can certify and require visual, aural, clean-room, or direct Resolve-UI review:

- interpolation warping, contact distortion, or other temporal artifacts introduced by motion compensation;
- continuity and truthfulness of key tag, people, wardrobe, environment, actions, and claimed return/direct outcome;
- exhaustive alpha-edge, text-collision, safe-margin, and thin-rule compression behavior outside the sampled 480x270 legibility grid;
- shot-to-shot exposure/white-balance match, natural skin/brass handling, scopes, and Gamma 2.4 display appearance;
- whether the 0.200-second low-motion interval and final 0.467-second audio tail are editorially appropriate;
- direct Resolve-UI absence of a “Media Offline” indicator. Successful local path resolution, final renders, exact picture continuity, and clean decodes are strong contrary evidence, but not a UI inspection;
- clean-room offline rerendering. The manifest reports zero remote HTML dependencies, but no independently executed clean-room final Resolve render is evidenced here.

## Gate disposition

| Gate | Result |
|---|---|
| Canonical MP3 and locked-input hashes | PASS |
| 1920x1080, 30 fps NDF evidence, 912 picture frames | PASS |
| Master PCM s24le stereo, 48 kHz, exact 30.400 seconds | PASS |
| Loudness / peak / clipping risk | PASS (`-15.0 LUFS`, `-3.2 dBFS`) |
| End-to-end video/audio decode | PASS |
| Black/flash-frame detector | PASS |
| No broken repeated-frame source cadence | PASS — zero exact adjacent duplicates in all 13 corrected intermediates and zero outside the deliberate S09 hold in the master |
| No unintended freeze | PARTIAL — only the intentional one-second hold is a confirmed exact-frame run; a separate 0.200-second low-motion interval needs visual judgment |
| Resolve project, editable tracks, relink, final render jobs | PASS |
| OTIO final-state interchange | PASS |
| FCPXML final-state interchange | PARTIAL — present but stale after cadence relink |
| HyperFrames technical validation | PASS with one non-blocking density warning |
| Sampled 480x270 operational-label legibility | PASS across the nine-panel accepted grid; not an exhaustive every-frame certification |
| Asset hashes/provenance/rights manifest | PASS for local completeness and hash consistency; external legal interpretation not re-reviewed |
| Captions | PARTIAL — valid SRT and Resolve track evidence; no embedded subtitle stream |
| Missing media / offline frames | PASS for path existence and delivered-picture analysis; Resolve UI not directly inspected |
| Clean-room offline final render | NOT VERIFIED |

The objective technical failures identified in the prior audit—repeated-frame cadence, stale manifests, incorrect input hashes/locators, non-PCM mezzanine audio, and undersized sampled typography—are corrected in the stabilized output. The final typography rerender does not change the technical verdict: **PASS WITH LIMITATIONS**. This result must not override the independent creative verdict or be described as evidence of a polished creative full pass.
