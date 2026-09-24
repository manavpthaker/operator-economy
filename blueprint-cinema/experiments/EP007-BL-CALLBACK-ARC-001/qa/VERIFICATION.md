# EP007 recurring human-scene test

Status: **rendered for internal review. This is not a gate pass, production select, Step 4 authorization, or publication approval.**

## What this test asks

Does the owner-buyer scene work when it is viewed as a recurring story across the episode rather
than as one isolated AI-generated clip?

The cut now shows one complete arc:

1. **Opening:** the audience sees that the owner is competent. The buyer asks the operating
   question. The owner begins to answer, stops, and has to calculate.
2. **Middle:** the existing Review Cut 007 returns after the audience already knows the people and
   the unresolved question.
3. **Ending:** the same people return to the same table. The answer is now in a binder the buyer can
   open and inspect. The owner's competence has not changed; where the operating knowledge lives has.

The repeated competence shot is intentional. It makes the before/after distinction about the
business system, not about repairing an incompetent owner.

## Review artifact

- Film: `../hyperframes/renders/EP007-BL-CALLBACK-ARC-001.mp4`
- SHA-256: `2c6beebad9901a227cc1d039b4017698886854e8be1cbb800c2355eb32df6afa`
- Size: 62,880,976 bytes
- Picture: H.264 High, 1920×1080, constant 24 fps, 1,765 frames, 73.541667 seconds
- Sound: AAC-LC stereo, 48 kHz, 73.541 seconds

The film contains the exact locked narration excerpts from 0.000–44.500, 247.660–255.400, and
1047.360–1068.620 seconds of `narration-master.v4.wav`. Narration was not regenerated or retimed.
Generated source audio is disabled. There are no captions, claim IDs, source annotations, music,
sound effects, slow motion, or post-production camera moves.

## What changed from the isolated middle test

- The current RC007 woman, man, and workshop are now the continuity authority for all three scenes.
- The opening contains an observable performance action: a short answer begins, breaks, and does not
  resume. The buyer waits without turning the pause into humiliation.
- The middle is the already reviewed 7.75-second causal plate, not a newly invented replacement.
- The ending pays off the same question with a physical, inspectable record.
- The existing middle plate was normalized to 24 fps H.264 with keyframes no farther than one second
  apart. This closes the sparse-keyframe condition that could make a nested render look frozen or
  choppy without changing its editorial timing.

## Machine verification

The exact current composition passed `npm run check` with HyperFrames 0.8.28:

- lint: 0 errors, 0 warnings
- runtime: 0 errors, 0 warnings
- layout: 0 issues across 9 samples
- motion: 0 errors, 0 warnings
- black-frame scan: no interval of 0.10 seconds or longer reported

Render contact sheet: `render-contact-sheet.jpg`. Machine-readable provenance and hashes are in
`../render-manifest.json`.

## What still requires human judgment

The technical checks cannot answer the actual creative question: **does the performance feel human
and does the answer-and-stop moment carry the scene without looking generated?** The contact-sheet
review confirms continuity, readable actions, and the intended before/middle/after construction. It
does not prove believable acting at normal playback.

Review the full 73.5 seconds once without pausing. If it fails, identify the first exact moment that
feels false. That tells us whether to regenerate one performance beat, recut its duration, or reject
the generated-human approach. It would be premature to redesign the whole edit from still frames.

## Boundary

No approval was inferred, no process or episode gate changed status, nothing was committed, and V4
was not advanced. The generated film remains illustrative human context, not evidence.
