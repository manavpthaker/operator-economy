# Rendered linework review

Artifact: `../renders/EP007-BL-PENCIL-001.mp4`

SHA-256: `f9a5701b9a1fdf96099a4b4f1737b52b23eaaaac6f66f0a335e4f4f47dcfe587`

Scope: internal style test. No production, process, gate or release approval is implied.

## What was inspected

- Encoded 1920x1080 frames at 0.8, 3.9, 6.4, 10.7, 14.5, 17.4, 20.2, 23.6, 25.8 and 27.6 seconds,
  split between the integrator and an independent reviewer.
- Original/revised encoded crops at 3.9 seconds, displayed side by side.
- A 640x360 downscaled frame at 20.2 seconds for line survival. This is not a physical-phone test or
  a recomposed portrait deliverable.
- Two early-reveal regression frames re-inspected after the final render: 0.8 and 25.8 seconds.

## Findings and disposition

1. Paper fills initially covered card hatching. Fixed by putting hatching above fills.
2. Wide, round-ended reveal masks exposed short pencil fragments before their cues. Found by
   independent encoded-frame review, not by the passing automated check. Fixed by using butt ends
   on hidden masks only. The third checklist mark is absent at 0.8s; the Still open line is absent
   at 25.8s in the corrected render. Visible pencil strokes keep their own round ends.
3. Rougher strokes are lighter than the original marker-like contours. The oxide stroke weight was
   increased relative to other pencil marks. At 640px the principal objects and orange route remain
   discernible; fine hatching recedes and the final package miniatures are not intended to be read.

## Judgment

The encoded result is visibly less formed: open silhouettes, unequal corners, overlapping marks,
local pressure changes and sparse cross-hatching. It preserves recognizable object identities.
The palette, typography, words and overall layout remain intentionally composed. Whether this is
the preferred final degree of roughness remains the user's aesthetic decision.

## Limits

This was sampled-frame visual review, not an audience comprehension test, continuous real-time
playback review or independent listening test. The full voice was mechanically verified as
decoded-audio-identical to the baseline. The strict HyperFrames check passed, but its early-reveal
miss demonstrates why it does not certify visual correctness on its own.
