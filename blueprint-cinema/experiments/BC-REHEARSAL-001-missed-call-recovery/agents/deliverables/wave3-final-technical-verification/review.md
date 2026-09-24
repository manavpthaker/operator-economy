# Wave 3 final technical correction verification

Review completed: `2026-08-20T20:58:30Z`  
Work order: `wave3-final-technical-verification`  
Final render: `hyperframes/renders/BC-REHEARSAL-001-directed-animatic-final.mp4`  
Final render SHA-256: `a9f21223385ff12dd60b7c0f3572d1cd14e70e5fb72907ddc76ebe85cbe824b3`

## Result

The final render resolves all three major findings from the initial technical review. `CALL-R01` changes from `REVIEWED` to `BOOKED` on the same first rendered frame that changes `WO-R01` from `OFFERED` to `SCHEDULED`, then remains `BOOKED` through the final measured frame. Shot 06 visibly identifies its hand-shaped rehearsal substitute as `AST-OPERATOR-003 / HUMAN REVIEW PLATE`. The handoff conform uses the first 30 fps frame at or after every authored shot boundary, contains seven adjacent events with no gap or overlap, points to the final corrected MP4, and ends at exclusive frame `1843`.

No new blocking or major technical regression was found. The exact synthetic warning, work-order disclosure, human release ordering, decline terminal, persistent identities, evidence choreography, final audio, and no-black-frame result remain intact.

This is an independent correction-verification packet, not creative approval, gate approval, production-state advancement, or permission to publish.

## Fail-closed retry record

The first verification attempt stopped without writing either owned output when `handoff/timeline-events.json` changed after the initial pin check. The root reissued the work order with the corrected file pinned at `36198b483666b05998ddfa33461b94e86ffb02bdeeda528bba9fd97280eb0e6f`. This review restarted from zero, re-read the work order, confirmed the owned directory was empty, and recomputed all ten pins before inspecting the final render.

## Pin verification

| Pinned path | Recomputed SHA-256 | Result |
|---|---|---|
| `input-lock.json` | `d5b7f0dc2b7c387bc0e32c3a74daacd4a575fd9f0fb0aa973db82f4f4290a3b2` | PASS |
| `direction/visual-plan.json` | `572f00ae1e51225ea7b161811e356c361eb8734c6f06903642a30049bc0a259c` | PASS |
| `direction/asset-tickets.json` | `598b8e01ffd760219005c416ffb71eb355228246340f0fa109af3c39bb37f05a` | PASS |
| initial Wave 3 technical review | `223fc3395645489c4a9cab0b279be6a48a62ece63bb9189d94ddedc346c0c133` | PASS |
| `hyperframes/index.html` | `25c5e9816cfdfcf8691437c58595105ecf797a63bec72a1a91c669d9a0cd2442` | PASS |
| `hyperframes/compositions/shots/shot-06.html` | `28af95375d837aaa02e9b6c7c0005062bfc861763da624dde4a07361e568de43` | PASS |
| `handoff/timeline-events.json` | `36198b483666b05998ddfa33461b94e86ffb02bdeeda528bba9fd97280eb0e6f` | PASS |
| `handoff/markers.csv` | `9918929c15ce8e5ce54c1808d96dc9c5d5525df8a0574b2ed87694a136a58f92` | PASS |
| final directed-animatic MP4 | `a9f21223385ff12dd60b7c0f3572d1cd14e70e5fb72907ddc76ebe85cbe824b3` | PASS |
| final rendered contact sheet | `683d084e547fc6ef16b842337d8e0fcf5f748311d8d6246490d95d983cce955f` | PASS |

All ten values were recomputed again immediately before authoring this report and remained stable.

## Independent media probe

| Property | Observed | Result |
|---|---:|---|
| Container | MP4 | PASS |
| Video | H.264, `1920×1080`, 30/1 fps | PASS |
| Video frames | `1843` | PASS |
| Video duration | `61.433333 s` | PASS; less than one frame beyond the `61.411354 s` timing lock |
| Final frame | frame `1842`, PTS `61.400000 s` | PASS |
| Audio | AAC, 48 kHz, two-channel | PASS for review reference |
| Audio duration | `61.418000 s` | PASS |
| Locked-VO comparison | decoded channel APSNR `165.062 dB` over `61.411354 s` | PASS; consistent with the locked local VO after AAC encoding |
| File size | `3,343,339 bytes` | Informational |
| Black-frame scan | no interval detected at a one-frame minimum | PASS |
| Silence scan | no silence interval of at least `0.5 s` below `-50 dB` | PASS |

The actual MP4, not only its HTML source or contact sheet, was sampled at the correction frames, every shot boundary, all evidence stages, the human release, and the final frame.

## Original-major reclassification

### M1 — visible tag state lagged at REVIEWED

**Prior status:** major, open.  
**Current status:** **RESOLVED**.

- Frame `1353`, PTS `45.100000 s`, still correctly shows `REVIEWED / OFFERED` because it precedes the authored `45.11 s` state change.
- Frame `1354`, PTS `45.133333 s`, is the first rendered frame at or after `45.11 s` and shows `BOOKED / SCHEDULED`.
- Frames `1431`, `1682`, and final frame `1842` retain `BOOKED` while the card remains `SCHEDULED` and later becomes `MEASURED`.
- The pinned root owns exactly one `tag-state-booked` layer and switches it on at `45.11 s` while switching `tag-state-reviewed` off.

The persistent customer state now agrees with the visual plan's `call-tag-red: booked` state.

### M2 — Shot 06 operator placeholder lacked ticket identity

**Prior status:** major, open.  
**Current status:** **RESOLVED**.

- Actual final-render frames `1431` through the bypass-removal action visibly show `AST-OPERATOR-003` and `HUMAN REVIEW PLATE` below the hand-shaped placeholder.
- The pinned Shot 06 composition records `data-placeholder="operator-hand"` and `data-ticket-id="AST-OPERATOR-003"` on the same object.
- The exact ticket remains legible while `AUTOMATE ALL` is struck and removed; the hand can no longer be mistaken for an approved production asset.

### M3 — authored shot boundaries lacked a declared frame conform

**Prior status:** major, open.  
**Current status:** **RESOLVED**.

The pinned event file declares a ceiling policy: preserve source seconds and word ranges, but begin each shot on the first rendered 30 fps frame whose timestamp is at or after its authored boundary. The event and marker frames agree:

| Event | Authored start | Prior frame PTS | First allowed/rendered PTS | Record frame | Exclusive out |
|---|---:|---:|---:|---:|---:|
| S01 | `0.000000` | — | `0.000000` | `0` | `410` |
| S02 | `13.640000` | `13.633333` | `13.666667` | `410` | `792` |
| S03 | `26.370000` | `26.366667` | `26.400000` | `792` | `1026` |
| S04 | `34.200000` | `34.166667` | `34.200000` | `1026` | `1197` |
| S05 | `39.880000` | `39.866667` | `39.900000` | `1197` | `1431` |
| S06 | `47.680000` | `47.666667` | `47.700000` | `1431` | `1682` |
| S07 | `56.050000` | `56.033333` | `56.066667` | `1682` | `1843` |

Machine checks confirmed:

- every `record_in_frame` equals `ceil(authored_seconds × 30)`;
- each event starts exactly at the prior event's exclusive out;
- the seven durations sum to `1843` frames;
- the last event ends at exclusive frame `1843`;
- every marker frame and shot ID matches its event;
- every event source points to `hyperframes/renders/BC-REHEARSAL-001-directed-animatic-final.mp4`.

The CSV retains authored seconds alongside actual frames/timecodes. Downstream import must treat `frame` and `timecode` as the 30 fps conform positions and `seconds` as the source narration boundary, consistent with the pinned policy.

## Regression review

### Persistent objects and business state

- `CALL-R01 / 20:47` remains one recognizable red tag through all seven shots.
- `WO-R01` remains one card and still advances `EMPTY → OFFERED → SCHEDULED → MEASURED`.
- `OFFERED` remains impossible before visible human `RELEASE`.
- The decline rail still terminates at `STOP` with no outgoing continuation.
- No result number, customer identity, phone number, company, revenue, testimonial, or interface was introduced by the corrections.

Result: **PASS; no continuity or honesty regression**.

### Evidence and disclosure

- The source enters in context with `SYNTHETIC TEST FIXTURE — NOT EVIDENCE`.
- `call_time = 20:47` is highlighted, extracted as `20:47 VERIFIED`, attached to the tag, and used to drive uncertain classification and human review.
- The exact fixture warning remains pinned after source collapse through final frame `1842`.
- The outcome card continuously displays `AST-OUTCOME-004 / SYNTHETIC WORK ORDER — NOT EVIDENCE`.
- Shot 04 still displays `AST-OPERATOR-003`; the Shot 06 correction now matches that ticket discipline.

Result: **PASS; no evidence, disclosure, or ticket regression**.

### Motion, compression, and ending

- The correction adds state/ticket text only; it does not introduce camera drift, decorative transition, duplicate object, bounce, or ambient loop.
- No black interval, missing final frame, broken glyph, or visible correction-frame compression defect was observed.
- Final frame `1842` still displays the booked tag, measured card, CALL/REPLY/BOOKED APPT bracket, and exact synthetic warning.

Result: **PASS; no motion or rendered-output regression**.

## Remaining non-major observations

These do not reopen the three corrected major findings:

1. **Open minor — contact-sheet filler:** the final `1960×842` contact sheet still contains one unlabeled black filler tile. The MP4 itself has no black interval, but the filler can still be mistaken for a black ending.
2. **Open minor — container metadata:** the final MP4 still reports `hyperframes_version: 0.0.0-dev`. The pinned project/tool report and external output manifest must remain the version authority, not this container tag.
3. **Known handoff characteristic:** the locked source VO is mono, while the review MP4 is stereo AAC and carries no alpha or embedded timecode/data track. This final work order did not pin the track-map or plate-behavior documents, so their downstream handling is outside this packet. Resolve should continue using the locked WAV and external frame/timecode conform rather than extracting authority from the MP4.

No blocking or major finding remains in the correction scope.

## Commands and checks run

- `shasum -a 256` for all ten pins at restart and again before report authoring.
- `ffprobe` codec, dimensions, frame rate, frame count, duration, stream, metadata, and exact PTS checks.
- `ffmpeg` decoded-VO APSNR comparison, one-frame black detection, silence detection, and direct final-MP4 frame extraction without writing additional review artifacts.
- Direct visual inspection of frames immediately before and after the booked transition, Shot 06 entry/action, Shot 07 entry, final frame, source context, highlight, extraction, classification, persistent proof pin, and human release.
- Independent JSON/CSV conform calculation for ceiling frames, adjacency, source path, marker correspondence, and exclusive frame `1843`.
- Static inspection of the pinned root/Shot 06 files for single ownership, exact state/ticket text, and event times.

## Authority boundary

`complete` means only that this isolated verification packet satisfies its correction-review work order. It does not claim creative approval, gate approval, state advancement, canonical integration, Resolve import validation, public-evidence status, publication readiness, or release authorization. No canonical experiment, handoff, render, direction, review, real episode, or production-state file was edited by this worker.
