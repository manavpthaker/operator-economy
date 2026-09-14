---
workflow: general-video
flow: companion
storyboard: no
---

# Week 2 motion-conditioned continuation

The owner rejected the remaining join at “For”. Root is generating a forward
video extension conditioned on the actual full-02 opening motion, then preparing
its timing and voice restoration. This revision tests that continuation.

Retain the exact full-02 opening prepared video for global frames [0,524).
Use root's new prepared extension for [524,933). The opening SHA-256 is
`a36b6644b44d867cc8b570d9d72bce4bf8922b69619f5c6084baf0102931fc33`.

Canvas 720 × 1280, 24 fps, 933 frames / 38.875 seconds. Root supplies
`../media/extension-prepared.mp4`, 409 frames, already framed and aligned.
Consume source time zero for both inputs; add no crop or source offset.
The complete Original C master remains continuous and unretimed from zero
through 38.87020833333333 seconds, including complete opening and final words.

The seam remains pending creative review until the actual new joined
performance is inspected. Matching framing, waveform, duration or automated
checks cannot establish that the join feels continuous.

No captions, music, graphics, end card, camera moves, designed transitions,
color treatment, speech stretching or voice changes. Render only after root
confirms the prepared extension input. Preserve every prior version. This
worker owns only full-03/assembly and performs no provider calls, uploads,
publishing, staging or commits.
