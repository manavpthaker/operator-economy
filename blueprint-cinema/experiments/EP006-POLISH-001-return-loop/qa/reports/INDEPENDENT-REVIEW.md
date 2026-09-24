# Independent media and visual QA

Result: **PASS** for this bounded internal control. This is a separate post-render inspection of the Resolve-encoded deliverables, not creative approval, evidence approval, production-footage approval, publication authority, or an EP006 gate change.

## Encoded-media QA

- Authoritative review: `delivery/EP006_POLISH_001_RETURN_LOOP_REVIEW_FINAL.mp4`.
- Authoritative master: `delivery/EP006_POLISH_001_RETURN_LOOP_MASTER_FINAL_PCM.mov`.
- Both contain 1920×1080 picture at 30 fps and stereo 48 kHz audio.
- Picture is exactly 912 frames / 30.400 seconds. This is the legal 30 fps quantization of the requested 30.405-second VO window.
- The review container is 30.464 seconds because of AAC encoder padding; the picture and program content end at 30.400 seconds.
- Master is ProRes 422 HQ, 10-bit 4:2:2, with 24-bit LPCM. Review is H.264 High with AAC-LC.
- Both measure `-16.4 LUFS` integrated, `2.0 LU` LRA, and `-5.2 dBFS` true peak.
- Black detection at a 0.02-second threshold returns no events on the authoritative outputs.
- Silence detection at `-50 dB` for `0.75s` returns no events.
- Resolve applied Rec.709/Gamma 2.4 output settings. The files report TV range with bt709 matrix and primaries; FFmpeg leaves the transfer field unspecified rather than enumerating Gamma 2.4.

The first conform failed this pass because frames 131, 367, 610, and 753 were empty. The failure was traced to incorrect inclusive-end assumptions in the Resolve append API. The final timeline uses exclusive ends and no gaps; the rejected timeline and files remain labeled and are not deliverables.

## Visual inspection

Inspected from the final Resolve review, not from source HTML:

- Full-resolution frames at `0.200`, `2.188`, `6.800`, `9.200`, `11.500`, `15.756`, `18.300`, `22.722`, `29.500`, and `30.300` seconds.
- Six-frame final contact sheet at 2880×1080.
- Six-frame 480×270-per-frame legibility sheet.
- Early, middle, and late representative graded stills extracted from the final encoded review.

The 480×270 inspection preserves the thesis-bearing labels: `PERMISSION`, `SUPPRESSED`, `HUMAN REVIEW`, `FIRST STAY / OTA`, `DIRECT RETURN / VISUAL TEST`, and `NEXT APPROPRIATE STAY / DIRECT`. Minor annotations remain intentionally secondary.

## Creative acceptance

| # | Criterion | Result | Evidence |
|---:|---|---|---|
| 1 | Causal chain is explainable after one watch | PASS | physical handoff → permission → memory → suppression/review → direct return → outcome |
| 2 | One dominant visual priority per shot | PASS | contact sheet shows one primary object/action in every sample |
| 3 | Key tag remains unmistakably the same object | PASS | brass color, chamfered corner, hole, and vertical scratch persist |
| 4 | Reality, system, and proof feel authored together | PASS | shared palette, geometry, key-tag scale language, and hard-cut grammar |
| 5 | AI plates read as restrained documentary illustration | PASS | modest inn, partial bodies/hands, no luxury gloss, no readable data |
| 6 | Motion behaves editorially rather than as slides | PASS | movement expresses handoff, stop, gate, qualification, approval, and route activation |
| 7 | Resolve materially improves unity and finish | PASS | exact conform, shot-specific CDL matching, final cut repair, audio assembly, markers, and delivery |
| 8 | Permission, suppression, and judgment remain visible | PASS | closed/open gate proof, red stop proof, unresolved/resolved review proof |
| 9 | OTA is not treated as the enemy | PASS | `USEFUL ACQUISITION` / `USEFUL INTRODUCTION`; route retained, never red or crossed out |
| 10 | Outcome feels causally earned | PASS | direct route appears only after eligibility and human review |
| 11 | Final thesis holds long enough | PASS | final state is complete by frame 854 and holds 58 frames / 1.933 seconds |
| 12 | Sequence avoids template, node-map, and Prezi language | PASS | no map flyover, floating-card layout, decorative transition, or ambient drift |

## Evidence boundary

- `DIRECT RETURN / VISUAL TEST` is a designed fixture, not a booking confirmation, result, receipt, platform screen, or evidence.
- The fixture permanently says `NON-PUBLISHABLE FIXTURE · NOT EVIDENCE`.
- No guest identity, contact detail, message, interface, price, confirmation number, statistic, source document, or platform logo appears.
- Both environmental plates are fully synthetic stills. No generated-video claim is made.

## Decision

The experiment is suitable as an **internal production-language control** for the return-loop sequence. It is not approved production footage and does not authorize scaling the approach to the full episode without a separate approval.
