# R21 private review

Implemented the local editorial changes requested on 2026-09-10:

- At 35.083333, “That pause…” cuts to the buyer's silent attention. The existing shot E source range 4.75–9.75 is unchanged; a fixed right-side crop makes the consequence visible. This line remains within the scene, not a heading.
- At 40.083333, the presenter returns for “And there is a business…”.
- At 62.916667, the existing two-pickup cut becomes a clearly closer shot for “By the end.” The edit is inside the gap between “anything” and “By”; no words are cut.
- At 67.916667, a second fixed reframe emphasizes “one number,” then holds through the end. Source B is continuous across this cut, with frames [0,120) followed by [120,206).
- Build · Own · Operate remains after the show title.

The preview remains 71.5 seconds, 24 fps. Narration and all source media are unchanged. This version adds visual emphasis only; it does not claim a lip-sync repair or new vocal stress.

## Verification

The final strict HyperFrames check passed: zero lint, runtime, layout or contrast findings; 5/5 sampled contrast checks passed. The motion module was disabled and is not claimed as a separate motion test. Picture declarations are contiguous and frame-aligned. All 27 R20 baseline files remain unchanged, and 26 retained files in R21 are byte-identical to R20.

Final snapshots were inspected at the buyer hold, both sides of the presenter cuts and the final clause. Presenter crops were adjusted to retain headroom. Chrome playback was sampled at 1x, with narration unmuted: owner around 33 seconds, buyer around 36, presenter around 42, restored tagline around 52, closer final-sentence shot around 67, and emphasis shot around 68. These observations confirm the displayed picture and framing at those times; they are not a complete audiovisual or perceptual lip-sync certification.

Private player: http://100.101.49.30:3037/. Chrome tab 1454456730 was marked as the deliverable and left paused around 34 seconds, immediately before the buyer cut. All 20 runtime routes returned HTTP 200; source/staging hashes and media response hashes matched. Only runtime files are served, not provider records or production documents.

The independent final-line audit rules out an introduced fixed conform offset, but does not certify synthesized mouth shapes. Actual vocal stress should be settled before paying for another lip-sync pass. The previous paid generation grant is exhausted; no paid call was made for R21. No canonical state, narration lock or publication gate changed.
