# EP007-BL-MIXED-001 verification

Status: **rendered mixed-media test; not a gate pass, production authorization, or publication approval.**

## Current render

- Artifact: `renders/EP007-BL-MIXED-009.mp4`
- SHA-256: `44a72464d9982a7932574c38eac38999683088479dfdcf566d8f97ce6668be9d`
- Size: 14,685,038 bytes
- Container: H.264 High, 1920×1080, constant 24 fps, BT.709 SDR, 67.458333 seconds
- Audio: AAC-LC, 48 kHz stereo, 67.456 seconds
- Renderer: HyperFrames 0.8.27, high quality
- Focus review: `renders/EP007-BL-MIXED-009-focus-17.5-27.5.mp4`, SHA-256
  `a32ed164a6ec31ae9ea69985f4cb7b532a662b970ebb53239549b65b69a5d053`
- Machine-readable encoded evidence: `qa/encoded-009/verification.json`

## What this revision resolves

- The former consultation-only second film shot is replaced by a locked-camera inspection insert.
  The buyer visibly marks and follows an unlabeled operating checklist, then looks back to the
  competent owner. The combined passage now reads as scrutiny without relying on narration.
- The v008 edit was rejected because a fragment of an unrelated synthetic page entered at the far
  right from 25.625–25.875 seconds. V009 selects source frames 0–82, excludes frames 83–120, and
  uses a declared seven-frame endpoint hold under the moving pencil overtrace. The leak is gone.
- The former abstract outlines and generic folder are replaced by a competent owner, a four-part
  operating structure, a recognisable checklist, and a buyer actively marking and tracing it.
- `business` and `job` arrive with the corresponding narration. They are semantic annotations, not
  claim IDs or production labels.
- The resolved inspection question holds through the reflective sentence, then cuts directly to
  `Revenue`. There is no second blank folder.
- `Revenue` remains alone until the spoken word “is,” when `is the evidence` begins.
- `Revenue` crossfades into the operating structure without an empty ledger-paper flash.
- `job` now uses the same source size as `business`; it no longer reads as a subordinate footnote.

## Encoded-film timing

- 18.1667–22.125 seconds: restrained owner–buyer establishing shot.
- 22.1667 seconds: hard cut to the buyer actively marking and reviewing the checklist.
- About 24.5 seconds: the buyer has looked back to the owner after the document scan.
- 25.125 seconds: the rough pencil overtrace first appears over the live-action table.
- 25.625–25.875 seconds: declared seven-frame hold on the last safe generated frame; the authored
  overtrace continues moving across it.
- 25.875 seconds: final generated-film frame.
- 25.917 seconds: rough ledger-paper inspection begins.
- 26.4–27.0 seconds: owner, structure, checklist, and buyer are recognisable.
- 28.88–30.30 seconds: pencil, check mark, and trace establish buyer inspection as an action.
- 31.24–31.48 seconds: `business` enters and becomes legible.
- 32.68 seconds: the owner tether begins.
- 33.125–33.333 seconds: `job` enters and becomes fully opaque.
- 34.56–34.90 seconds: buyer and checklist dim; the resolved business/job comparison remains.
- 38.125 seconds: final complete inspection frame.
- 38.1667 seconds: first model frame is the fully visible `Revenue` record.
- 41.4167 seconds: `Revenue` is still alone.
- 41.4583 seconds: `is the evidence` begins on the first encoded frame after spoken “is” at about
  41.44 seconds; it is fully legible around 41.75 seconds.
- 43.2083 seconds: final Revenue-only frame.
- 43.250–43.4583 seconds: the operating structure draws beneath the fading record.
- 43.500 seconds: the record has cleared while the structure remains.
- 43.5417 seconds: `The operating structure` begins, after the record has cleared.

There is no empty flash, black frame, duplicate folder, or text collision. The receipt overlaps only
the emerging structure drawing, never the structure title.

## Encoded-output integrity

- All 1,619 declared frames were read and decoded.
- Full-stream decode passed.
- Black-frame detection found no interval of 0.10 seconds or longer.
- Every frame interval is 0.041666–0.041667 seconds at constant 24 fps. The moving portions of both
  generated shots contain no near-duplicate cadence. The only near-static run is the declared
  seven-frame endpoint hold, and the composed frame continues changing through the pencil trace.
- A full-video paper-only scan found no interval, including the Revenue-to-structure transition.
- Downstream motion cues retain their previous narration alignment; no cumulative timing drift was
  introduced.

The internally rendered v005 was rejected because frames 916–1041 contained 5.25 seconds of
meaningless warm paper. The interim v006 restored `Revenue` but retained a three-frame empty flash
after it. V007 closed both encoded-output defects. V008 introduced the replacement inspection plate
but leaked a fragment of its rejected generated tail at the far right. V009 removes that final leak.

## Automated source checks

The final source check sampled all content cues and the revised seams, including 28.88, 30.30,
31.48, 33.32, 38.13, 38.17, 41.44, 41.75, 43.17, 43.29, 43.38, 43.46, 43.58, 49.70,
54.00, 60.75, 64.38, and 67.10 seconds.

- Lint: 0 errors, 0 warnings
- Runtime: 0 errors, 0 warnings
- Layout: 0 issues across 20 samples
- Motion: 0 errors, 0 warnings
- Contrast: 15 of 15 sampled text checks passed WCAG AA
- Frame-boundary audit: passed at error severity

## Rough-build bindings

- Inspection: 21 authored paths expanded at build time into 659 fixed pencil fragments and 15
  reveal masks. Compiled SHA-256:
  `082e57a6cc80e6b9ab01b90ba7dadf72534514b5929ed00795af3f3b6e76e866`.
- Working Model: 36 authored paths expanded at build time into 1,478 fixed pencil fragments and 15
  reveal masks. Compiled SHA-256:
  `1f60a29e02208381f9e65c30d6deba384bdb9f73518c73e855e0ca51c90fe599`.
- The compiler is deterministic. Neither composition uses runtime jitter or a roughening filter.

## Audio inspection

The locked PCM excerpt remains the only audio.

- Locked WAV SHA-256: `1dea3844a964ca6ed0afa6b662205e04a0143fb0fdb0717e683254b7c6c64bf0`
- Source mean / peak: -18.8 dBFS / -2.9 dBFS
- Rendered mean / peak: -18.8 dBFS / -2.8 dBFS
- Decoded PCM SHA-256: `e7c35086f7d886e78ca32368f7772aaa0fb80f5047ff618fd3c25413b5834d7b`

This verifies timing and level preservation through AAC encode. It is not loudness-mastering
approval.

## Remaining boundaries

At a 390-pixel-wide presentation, the structure and checking action remain discernible, but the
handwritten `business` and `job` labels resolve to about seven pixels high. They are secondary
reinforcement, not reliable glance-readable phone copy. A true vertical or square derivative still
needs its own composition rather than scaling this 16:9 master.

The first four film seconds still read as a serious owner conversation when isolated. In sequence,
the second shot makes the inspection meaning unmistakable. The near-axis cut is slightly more like a
deliberate jump cut than a true insert; that is acceptable for this test, but remains a look-development
choice rather than a production rule. The plate is AI-generated human context and still needs the
formal production asset packet before any production promotion.

This test does not approve a full episode, avatar performance, vertical or square delivery, music,
sound design, captions, final loudness, V4–V7, Step 4, or publication.
