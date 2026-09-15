# Wave 3 technical, continuity, evidence, and disclosure review

Review completed: `2026-08-20T20:41:21Z`  
Work order: `wave3-technical-continuity-evidence`  
Reviewed render: `hyperframes/renders/BC-REHEARSAL-001-directed-animatic.mp4`  
Reviewed render SHA-256: `091e8be81d196a8e27e9322a5664201204cbc3ac644a17af558371b1e5cccca8`

## Independent result

The rendered file is real, playable, correctly sized, frame-rate-correct, and carries the locked synthetic narration. The seven-shot causal chain is visually continuous: the same `CALL-R01 / 20:47` tag survives the missed-call path, recovery rail, human gate, fork, and measurement view; `WO-R01` advances only after human release; the decline rail ends at `STOP`; and the fixture warning is exact and persistent once evidence enters. No fake company, customer identity, phone number, result, or external asset appears.

This packet is complete as an independent review, but it does **not** approve any gate. Two major direction-to-render discrepancies and one major Resolve-handoff timing risk remain. The render is suitable as a rehearsal review artifact after those findings are explicitly accepted or corrected; it is not public evidence or a finished production asset.

## Pin verification

Every work-order pin was recomputed before review and matched exactly.

| Pinned path | Recomputed SHA-256 | Result |
|---|---|---|
| `input-lock.json` | `d5b7f0dc2b7c387bc0e32c3a74daacd4a575fd9f0fb0aa973db82f4f4290a3b2` | PASS |
| `direction-lock.json` | `287b1c1ae2f9389905ce3a1149380b311703fa089d8f7bf8927eeb5c0ef0c9ca` | PASS |
| `direction/world.json` | `512775e52efd3466426aeada597532e6848335bca21ff38ae8834fd7efbd183b` | PASS |
| `direction/asset-tickets.json` | `598b8e01ffd760219005c416ffb71eb355228246340f0fa109af3c39bb37f05a` | PASS |
| `assets/fixtures/fixture-missed-call-log.csv` | `2ab69fcdd524f45d096fd1339447d484dc8e473a2630d07960226b2e485f40f4` | PASS |
| `hyperframes/index.html` | `d4a7587b83b00c642255b6d41d39c4e6c0e80db22c2dd45e91b79724a2eb7c62` | PASS |
| directed animatic MP4 | `091e8be81d196a8e27e9322a5664201204cbc3ac644a17af558371b1e5cccca8` | PASS |
| rendered contact sheet | `dd6cf528cf09d175d3ec5c6529bb09501722a130cdbd5b8c5faf9889d4baa6ef` | PASS |

The owned deliverable directory contained neither `review.md` nor `deliverable.json` before work began.

## Media probe

| Property | Observed | Result |
|---|---:|---|
| Container | MP4 | PASS |
| Video | H.264 High, progressive, `yuv420p`, BT.709 | PASS for a review reference |
| Dimensions | `1920×1080`, SAR 1:1, DAR 16:9 | PASS |
| Frame rate | `30/1` average and nominal | PASS |
| Frames | `1843`; final presentation timestamp `61.400000` | PASS |
| Video duration | `61.433333 s` | PASS; `0.021979 s` beyond the `61.411354 s` lock, less than one 30 fps frame |
| Audio | AAC LC, 48 kHz, two-channel | PASS with handoff caveat below |
| Audio duration | `61.418000 s` | PASS; `0.006646 s` beyond the lock |
| Audio presence/content check | Decoded MP4 channel against locked `vo.wav`: APSNR `165.062 dB` over the locked duration | PASS; consistent with the locked narration after AAC encoding |
| Integrated loudness | `-13.6 LUFS`, LRA `1.8 LU` | Informational only; synthetic rehearsal VO is not a mastered delivery track |
| File size / bitrate | `3,322,047 bytes`; video about `233 kb/s`, audio about `192 kb/s` | PASS for mostly static line art; not a finishing master |

`blackdetect` found no black interval in the actual MP4. A 2 fps compression scan and direct inspection of full-render frame sheets found no visible macroblocking, missing glyphs, broken font loads, or corrupted frames. The last black cell in the supplied 4×3 contact sheet is an unused tile, not a black frame in the video.

## Pass 1 — continuity and persistent identity

### What passed

- `00:02.63–61:40`: the single red token retains `CALL-R01`, `20:47`, color, proportions, and screen-direction identity. No duplicate customer token appears.
- `00:00.00–37.87`: `WO-R01` remains visibly `EMPTY` through the unanswered call, voicemail loss, route construction, and human hold.
- `00:37.88`: the card becomes `OFFERED` only after the visible `RELEASE` action.
- `00:45.11`: the same card becomes `SCHEDULED` as the accepted tag reaches it.
- `00:58.68`: the card becomes `MEASURED`, without adding a fabricated result.
- Across the six shot boundaries, object handoffs preserve direction. Shot 07 changes from navy to paper while the tag, card, and proof pin remain recognizable in their established right-side relationship.
- The same branch point first exposes `DECLINE → STOP`, then carries the single persistent tag along `ACCEPT` to `WO-R01`. `STOP` has no outgoing route.

### Major finding M1 — the call tag's visible state stops at REVIEWED

**Timestamp:** `00:45.11–61:40`  
**Direction requirement:** `visual-plan.json` changes `call-tag-red` to `booked` in Shot 05 and carries that state through Shots 06–07.  
**Rendered observation:** the tag's subordinate state strip remains `REVIEWED` after it attaches to a `SCHEDULED` card and through the `MEASURED` end frame. The card communicates booking, so the overall inference still works, but the persistent customer's visible state lags the locked business state.  
**Required disposition:** either add an approved `BOOKED` tag state at the booked contact, or document that the tag state intentionally freezes at `REVIEWED` and that the card alone owns the booking state. Do not leave the world model and render semantically divergent.

## Pass 2 — motion and transition discipline

### What passed

- Cuts are the default; the actual render does not fly a camera among boxes and does not keep a full-world overview inset.
- The only camera-scale move is Shot 06's controlled `1.12 → 1.00` pullback over `0.85 s`, within the directed 12 percent bound.
- No repeated, yoyo, elastic, bouncing, random, clock-driven, or ambient animation is present in the authored render path.
- The visible actions map to operational verbs: tag, fall, open the relationship gap, highlight/extract, classify, acknowledge, hold, review, release, stop, book, attach, remove bypass, and measure.
- Readable holds are real. Frame-difference scanning found extended stable intervals instead of meaningless camera drift; the final causal bracket holds through the last word.
- No transition exists only to decorate. The paper/navy mode cuts and the persistent-object handoffs explain reality/system/proof changes.

No blocking motion defect was found.

## Pass 3 — evidence choreography and disclosure

### What passed

- `00:27.80`: the source arrives as source context with the exact warning `SYNTHETIC TEST FIXTURE — NOT EVIDENCE`.
- `00:29.87`: only `call_time = 20:47` is highlighted.
- `00:30.36`: `20:47 VERIFIED` is extracted and attached to the persistent tag while the source remains visible.
- `00:31.34–37.64`: the attached field changes system behavior: the tag becomes uncertain, enters the human hold, and cannot reach an offer until the explicit release.
- `00:33.60–61:40`: the exact fixture warning persists as a right-edge proof pin through the gate, fork, blueprint, and measurement shots.
- The fixture CSV itself repeats the exact warning on every fictional record. The render invents no real entity, PII, performance number, revenue result, testimonial, or interface.
- `WO-R01` carries `AST-OUTCOME-004` and `SYNTHETIC WORK ORDER — NOT EVIDENCE` in every visible state.

The fixture remains a rehearsal-only synthetic artifact. Treating it as public evidence would block delivery.

## Pass 4 — placeholder and asset-ticket honesty

### What passed

- Shot 01 uses a conspicuous `AST-REALITY-001` human-context slate marked synthetic and missing.
- Shot 02 visibly registers `AST-DISPATCH-002`; Shot 03 replaces abstraction with the clearly warned local synthetic fixture.
- Shot 04 labels the human-action placeholder `AST-OPERATOR-003` and makes the placeholder cause the release.
- The persistent work-order card visibly carries `AST-OUTCOME-004` plus its synthetic/not-evidence warning.
- `AST-AMBIENCE-005` and `AST-SFX-006` remain silent ticket intentions; the MP4 contains one VO track and no attractive audio stand-in, stock, music, or decorative effects.

### Major finding M2 — Shot 06's human placeholder drops its ticket identity

**Timestamp:** `00:47.68–49.83`  
**Ticket requirement:** `AST-OPERATOR-003` is required in Shots 04 and 06, and rehearsal substitutes must remain conspicuously tied to exact ticket IDs.  
**Rendered observation:** Shot 06 uses a literal hand-shaped graphic labeled `OPERATOR HAND` to remove `AUTOMATE ALL`, but it does not display `AST-OPERATOR-003` or state that it is a placeholder. Shot 04's version is correctly ticketed; Shot 06's is not.  
**Risk:** the Shot 06 hand can be mistaken for an approved final graphic rather than a missing operator-action plate.  
**Required disposition:** keep the action and add the exact ticket ID plus placeholder treatment, or replace the hand with the same conspicuous `AST-OPERATOR-003` action slate used by the asset contract.

## Pass 5 — rendered compression

### What passed

- Actual decoded frames at shot entries, action states, consequences, boundaries, and the final hold show crisp primary labels, stable colors, and no visible compression breakup.
- Flat paper/navy fields do not band visibly in the reviewed frame sheets.
- The video reaches the locked end without a rendered black frame; the final frame remains the measured bracket.
- H.264 4:2:0 and the low video bitrate are acceptable for this internally reviewed animatic because the content is predominantly static shapes. They are not suitable evidence of finishing-master quality.

### Minor finding m1 — contact-sheet filler can be misread

The pinned 4×3 contact sheet contains eleven sampled render frames and one unlabeled black filler tile. The MP4 itself has no black interval, but the contact sheet should label the cell `UNUSED TILE` or use an eleven-cell layout so reviewers do not infer a black ending.

## Pass 6 — Resolve-handoff risks

The Resolve handoff was not a hash-pinned input to this work order. Concurrently assembled handoff files were therefore not treated as authoritative review inputs and were not edited. The following risks arise directly from the pinned direction and probed MP4 and must be resolved in the root handoff package.

### Major finding M3 — authored shot seconds are not all frame boundaries

**Affected boundaries:** `13.64`, `26.37`, `39.88`, `47.68`, and `56.05 s`.  
At 30 fps, those seconds fall between frames. The actual rendered first frames of the next shots are approximately:

| Shot start | Authored seconds | Actual rendered start frame / PTS |
|---|---:|---:|
| Shot 02 | `13.64` | frame `410` / `13.666667 s` |
| Shot 03 | `26.37` | frame `792` / `26.400000 s` |
| Shot 04 | `34.20` | frame `1026` / `34.200000 s` |
| Shot 05 | `39.88` | frame `1197` / `39.900000 s` |
| Shot 06 | `47.68` | frame `1431` / `47.700000 s` |
| Shot 07 | `56.05` | frame `1682` / `56.066667 s` |

The handoff must declare one rounding policy and use actual rendered frame starts for Resolve markers while preserving the exact narration timing separately. Copying the authored decimal seconds directly into a 30 fps timeline can move a boundary by one frame.

### Minor finding m2 — container version metadata is misleading

The MP4 metadata reports `hyperframes_version: 0.0.0-dev`, while the rehearsal records HyperFrames `0.8.4`. The external output manifest must identify the pinned CLI version and render command as authority; Resolve or archive automation must not infer the build version from the MP4 tag.

### Minor finding m3 — audio/channel and plate assumptions must stay explicit

The locked source VO is mono, while the review MP4 contains a two-channel AAC encode. Resolve should receive the locked `vo.wav` as the authoritative VO source, not extract audio from the review MP4. The MP4 has no alpha or plate tracks and no embedded timecode/data stream; the handoff must classify alpha/plates as absent and drive sequence/shot markers from validated external data.

## Ranked findings

### Blocking

None in the pinned render review. This is not a gate approval.

### Major

1. **M1 — `00:45.11–61:40`:** the tag remains visibly `REVIEWED` although the locked world/plan says it becomes `booked`.
2. **M2 — `00:47.68–49.83`:** Shot 06's operator-hand placeholder omits `AST-OPERATOR-003` and its placeholder status.
3. **M3 — Resolve handoff:** five authored shot boundaries are subframe decimals and require an explicit actual-frame rounding policy.

### Minor

1. **m1:** the contact sheet's unlabeled black filler tile can be mistaken for a black final frame.
2. **m2:** MP4 metadata says HyperFrames `0.0.0-dev`, not the recorded `0.8.4` tool version.
3. **m3:** the review MP4 is stereo AAC with no alpha/timecode/data track; the handoff must use the locked mono WAV and external marker/plate manifests.

## Commands and checks executed

- SHA-256 recomputation with `shasum -a 256` for all eight work-order pins.
- `ffprobe` stream, format, frame-count, duration, time-base, and final-PTS probes.
- `ffmpeg` black-frame, freeze/stable-interval, silence, block/blur, loudness, and decoded-audio comparison passes.
- Direct inspection of the pinned rendered contact sheet and independently decoded actual-MP4 sheets for all shot boundaries; detailed source/extraction/gate, stop/book, pullback, and final-measurement states were sampled from the MP4 without writing additional artifacts.
- Static trace of the pinned root and bounded shot compositions for persistent IDs, state-change times, exact warning text, asset-ticket IDs, route terminals, network calls, repeat/yoyo motion, and camera scale.

## Authority boundary

`complete` means this isolated review packet satisfies its work order. It does not approve a rehearsal gate, change experiment or production state, validate concurrently changing handoff files, authorize publication, or convert any synthetic fixture or placeholder into evidence. No canonical experiment artifact was edited.
