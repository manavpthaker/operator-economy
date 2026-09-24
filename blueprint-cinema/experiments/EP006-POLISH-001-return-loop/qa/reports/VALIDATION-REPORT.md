# EP006 Polished Control 001 — Validation report

Status: **PASS — polished EP006 control completed through Resolve**

This report covers only `/blueprint-cinema/experiments/EP006-POLISH-001-return-loop/`. The experiment is an internal visual-language and finishing control; it is not evidence, not approved production footage, not public, and not an EP006 gate advancement.

## What was actually made

- A locked, word-cued five-scene direction contract for the 849.517–879.922 narration window.
- Two fully synthetic environmental/human-context still plates: checkout handoff and operator judgment.
- One HyperFrames 0.8.5 project with a thin root and five bounded sub-compositions.
- Fifteen entry/action/exit snapshots, midpoint and causal-proof sheets, a 480×270 legibility sheet, a full directed reference, and five opaque ProRes HQ Resolve plates.
- A local sound package with the locked narration, six motivated SFX, and synthetic room tone; no music.
- An isolated Resolve project, final timeline, markers, track map, SRT, OTIO, FCPXML, graded stills, ProRes master, and H.264 review.

## What Resolve actually performed

DaVinci Resolve 21.0.4.5 created and saved project `EP006_POLISH_001_RETURN_LOOP`. Because the external scripting handle was unavailable and the installed Python console could not start, the minimum UI operation opened Resolve’s internal Lua console. Resolve itself then:

- imported the five local HyperFrames plates and eight local audio sources;
- created the five-video/four-audio/one-subtitle-track timeline;
- conformed the exact scene/audio structure against the locked VO;
- applied custom DaVinci YRGB Color Managed v2 Rec.709/Gamma 2.4 input, timeline, and output settings;
- exposed all picture sources as `Rec.709 (Scene)` and rejected scripting attempts to rewrite that read-only property;
- applied five shot-specific CDL primary corrections and no LUT;
- assembled locked VO, restrained SFX, and ambience;
- added twelve editorial/causal markers;
- corrected the first conform’s four one-frame gaps in a new 912-frame final timeline;
- rendered the authoritative H.264 review and ProRes 422 HQ / 24-bit LPCM master;
- exported the `.drp`, OTIO, and FCPXML interchange.

No Resolve conform or export is inferred from a handoff file: completed Resolve render job IDs and logs are preserved in `resolve/reports/`.

## Locked timing verification

- Source in/out: `849.517–879.922` seconds.
- Source window: `30.405` seconds.
- Word-table span: word 1775 `Now` through word 1847 `forever`.
- Intentional handle: `0.146` seconds before canonical `sequence-economics-05`, preserving `Now`.
- Narration was decoded losslessly to 24-bit/48 kHz WAV. It was not rewritten, regenerated, stretched, or replaced.
- Final 30 fps picture: 912 frames / `30.400` seconds. Difference from source window: `-0.005` seconds, solely frame quantization.
- Five final scene ranges: `0–131`, `131–367`, `367–610`, `610–753`, `753–912`, using exclusive ends. No gaps or overlaps.

## Validation matrix

| Check | Result | Evidence |
|---|---|---|
| Canonical hashes pinned | PASS | nine live SHA-256 values in `manifests/canonical-inputs.json` |
| Canonical hashes unchanged after production | PASS | all nine recomputed values match, including `production-state.json` |
| Current authority internally consistent | PASS | live state `greybox_ready`; engine/world/plan/tickets/state hashes agree |
| Exact VO and word alignment | PASS | locked WAV, word cues, SRT, direction lock |
| HyperFrames current-version probe | PASS | actual/pinned version `0.8.5` |
| HyperFrames strict final check | PASS | 0 lint/runtime/motion issues; 0 layout issues across 216 samples; 14/14 contrast |
| Render-time media local | PASS | local imagery, fonts, audio, and GSAP; no authored remote asset references |
| Five scenes cover requested window | PASS | 912 continuous final frames; fractional boundaries quantized and recorded |
| Persistent key-tag identity | PASS | full-resolution and contact-sheet inspection |
| Permission before memory | PASS | gate open/resolved at 9.200s; `STAY CONTEXT` appears later at 11.500s |
| Ineligible path stops | PASS | red suppression stop inspected at 15.756s |
| Human review before outbound | PASS | review resolved at 18.300s; direct route activates only after review cue |
| OTA remains useful | PASS | acquisition route retained and labeled useful; never destroyed or villain-colored |
| Outcome cannot be mistaken for evidence | PASS | permanent `VISUAL TEST` and `NON-PUBLISHABLE … NOT EVIDENCE` warning |
| No fabricated document/interface/result/identity | PASS | visual and provenance inspection |
| HyperFrames reference and plates probed | PASS | 1920×1080, 30 fps, expected streams, opaque ProRes HQ plates, bt709 |
| Resolve imported and conformed media | PASS | build and final-rebuild logs; timeline item records |
| Resolve rendered review and master | PASS | completed jobs in final-rebuild and PCM-master logs |
| Picture and audio present | PASS | both authoritative outputs contain video and stereo 48 kHz audio |
| No unintended black frames | PASS | final blackdetect returned no events; first-conform defect corrected |
| No unintended silence | PASS | no ≥0.75s region at or below -50 dB |
| Loudness and true peak | PASS | `-16.4 LUFS` integrated, `2.0 LU` LRA, `-5.2 dBFS` true peak |
| Resolution and color configuration | PASS | 1920×1080; TV-range bt709 matrix/primaries; Resolve Gamma 2.4 configuration applied |
| Early/middle/late visual inspection | PASS | final encoded review stills and contact sheet |
| 480×270 legibility | PASS | thesis-bearing labels readable; minor annotations secondary |
| Blueprint Cinema tests | PASS | 43 of 43 relevant tests passed after production |
| Experiment isolation | PASS | every new production artifact remains under the experiment directory |
| EP006 state unchanged | PASS | `production-state.json` hash remains `09460a…8efb`; state remains `greybox_ready` |

## Media probes

### Master

`EP006_POLISH_001_RETURN_LOOP_MASTER_FINAL_PCM.mov`

- 1920×1080, 30/1 fps, 912 frames, 30.400 seconds.
- Apple ProRes 422 HQ, `yuv422p10le`, TV range, bt709 matrix and primaries.
- 24-bit LPCM stereo, 48 kHz.
- SHA-256 `1f41ba8936e02710a9f0d0e77cd3c33f1fb2232edec0558ed9c039163a8b222c`.

### Review

`EP006_POLISH_001_RETURN_LOOP_REVIEW_FINAL.mp4`

- 1920×1080, 30/1 fps, 912 frames, 30.400 seconds of picture.
- H.264 High, `yuv420p`, TV range, bt709 matrix and primaries.
- AAC-LC stereo, 48 kHz; container duration 30.464 seconds from AAC padding.
- SHA-256 `95ec2e46ac135d7fd57866e90410f86071efcdd4361cfa33ddef116441fe28d4`.

Resolve accepted `GammaTag = Gamma 2.4` on both render jobs. FFmpeg enumerates matrix and primaries as bt709 but reports the transfer field as unspecified rather than naming Gamma 2.4; this probe limitation is preserved rather than hidden.

## Test commands

HyperFrames:

```text
npm run check -- --at-transitions --max-issues=120 --strict
```

Blueprint Cinema:

```text
blueprint-cinema/.venv/bin/python -m pytest -q \
  blueprint-cinema/tests/test_agent_packets.py \
  blueprint-cinema/tests/test_clean_room.py \
  blueprint-cinema/tests/test_episode_engine.py \
  blueprint-cinema/tests/test_input_lock.py \
  blueprint-cinema/tests/test_render_data.py \
  blueprint-cinema/tests/test_scene_prompts.py \
  blueprint-cinema/tests/test_schemas.py \
  blueprint-cinema/tests/test_state_machine.py \
  blueprint-cinema/tests/test_visual_plan.py \
  blueprint-cinema/tests/test_world.py
```

Result: 43 collected, 43 passed. No pre-existing failure was waived and no experiment regression was found.

## Fixture-only material and services

- Both AI environmental plates are synthetic stills with deterministic motion, not generated video.
- `DIRECT RETURN / VISUAL TEST` is a non-publishable outcome fixture, not evidence or a real confirmation.
- The ambience is an offline synthetic room-tone fixture, not a location recording.
- No paid or authenticated external service was used. No provider was installed, authenticated, or charged.

## Final decision

This is suitable as the bounded **internal production-language control** requested. It is not a creative approval, release approval, ticket fulfillment, production-state advancement, or authorization to modify the full episode.
