# EP009 r4 opening review candidate

The full candidate and 10.5-second opening context pass encoded technical checks. **Opening lip sync remains flagged and unresolved.** This is a reversible review artifact, not an eligible final presenter selection, owner acceptance, bulk clearance or release approval.

## Exact candidate

- Full video: `assembly/qa/r4/ep009-full-r4-opening-candidate.mp4`
- SHA-256: `c60d5d111cbea3346203a15b842d521f09070c975627c0dd7f500c9f412fcbee`
- Full BUILD SHA-256: `fad999994483aa029f045a4b1ac6286ca42e7aef91b43fcb454822e5363bec02`
- Opening context: `assembly/qa/r4/ep009-r4-opening-context-candidate.mp4`
- Context SHA-256: `8c88fc8eef66767f2ed75dc453242d14a7c1dfc3594d2d73a6f9baa317ae7df1`
- Review page: <http://localhost:3070/ep009-r4-review.html>

The separate candidate builder binds the exact root instruction, recorded candidate decision, flagged P00 private preview and frozen r3 dependencies. It changes only picture frames [0, 86), then resumes F01 source frame 86 and F02 at output 135. All remaining 29,237 source assignments, all 75 segment/cue fields, the six film inserts, the corrected-experience still and the locked narration/timing remain unchanged. Full duration is 29,323 frames / 20:21.791667. The source narration master and both owner-locked preview files retain their original bytes.

The source plates feed a new single assembly encode. The full r3 movie is not used as an intermediate. The 252-frame opening context is independently encoded from the same source assignments and unchanged master samples [0, 504000).

## Verification

Both `*-VERIFICATION.json` files report `technical_checks_passed_lipsync_unresolved_review_candidate`, with zero errors.

- Full video: all 29,323 encoded frames decoded, 1280×720 at 24 fps; only the planned uniform brand frame 1427. No unplanned uniform frames or decode error.
- Full audio: all 58,646,000 planned stereo program samples compared against the frozen r3 master plus its planned 1,080-sample final zero pad. Full channel correlation ≥ 0.9999885449; lowest voiced five-second correlation 0.9999701467; maximum absolute voiced level difference 0.013568 dB. The 528 additional decoded AAC samples are silent.
- Measured −19.5 LUFS integrated, 3.7 LU loudness range, −5.7 dBTP; no normalization or final-mix acceptance.
- The 252-frame context passes exact picture count, audio format and complete audio identity/level checks.
- The existing r4 eligibility tools, r5 helper/plan, active plan, final-r5 index, P00 notes and sync gate retain their pre-render hashes. No presenter eligibility or gate changed.

## Encoded picture inspection

`assembly/qa/r4/candidate-integration-frames/FRAME-COMPARISON.json` binds 62 decoded output frames and 10 contact sheets. All 10 sheets were inspected. Samples include the first/last opening picture, output 85/86, the retained F01/F02 join 134/135, F02/F03 join 251/252, the brand and corrected-experience boundaries, and entry/middle/exit with surrounding unchanged frames at all six later film inserts.

The presenter is settled at 85; the innkeeper reaches from 86, then picks up and holds the key through 134. Frame 135 retains the held-key position at the next shot. The retained F02/F03 join appears at 252. Expected brand imagery, labeled P08 still and six selected film sources appear at their planned boundaries. No sampled assembly placement defect was found.

At 640×360 decoded RGB, maximum mean absolute source difference is 2.123567/255; the largest fraction of pixels with mean RGB difference above 20 is 0.000004340278. These comparisons include the output encoding pass and do not measure perceptual lip sync.

## Rationale and limits

The recorded decision authorizes full-context review because the source is mechanically intact and dense-frame review did not demonstrate a sustained gross mismatch. That judgment does not establish correct phoneme timing. P00 retains `no_qualifying_onsets:true`, zero matched onsets, narration-mouth correlation 0.343 and guide-mouth correlation 0.382. Both diagnostic pass signals remain false. The final-r5 opening index stays pending.

There was no normal-speed audiovisual perception certification or full episode watch-through in this assembly check. Fourteen other presenter sections retain r1 footage; corrected P08 remains the labeled L3 still. Brand timing and corrected experience retain their scoped owner locks. P00, remaining presenter delivery, new film performance and final release remain under review.

The exact instruction is preserved in `assembly/r4/P00-CANDIDATE-INSTRUCTION.json`; root's decision is `direction/r3-owner-revisions/P00-CANDIDATE-DECISION.json`. The candidate BUILD, technical verifications, frame comparisons and final QA JSON bind the exact artifacts and limitations.
