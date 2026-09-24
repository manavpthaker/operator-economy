# R22 follow-up: choppiness before “one number”

Date: 2026-09-10 UTC. Read-only assessment of the R21 source and the orchestrator's proposed R22 repair. No R22, source, audio, or provider mutation was made.

**Recommendation: keep B in one continuous video element and change only its untimed framing wrapper at the existing emphasis boundary.** This removes an unnecessary browser decoder handoff while retaining both close-up crop states and the accepted edit timing. It is a well-supported narrow repair; the exact cause of the user's observed hitch remains an inference until normal-speed browser playback is checked.

## Verified facts

- R21 `index.html` SHA-256: `1d1b8dbd521b45dd7b9f1b7da4eeeeab807de0105822e17f0693cbbde7496200`.
- R21 `BASELINE-PINS.json` SHA-256: `d793c74305c854cd1554890f4e43bc4d8c641761bf746598a725d5dd40e7ad3b`.
- B media still matches the pinned `6bebb793f25e39b4c5577559f7e25b91a39270f904755bc6872586579935147a`.
- The extended narration still matches `ec2a42a7f0e3e09c044ef50bead4b0a91a264bd918a300aa0c34f22950d59605`.
- B is split across two separate `<video>` elements: review 62.916667–67.916667 from source 0–5 seconds, then review 67.916667–71.5 from source 5–8.583333 seconds. Source frame continuity is correct: `[0,120)` then `[120,206)`.
- **There is no audio splice at review 67.916667.** `original-narration-explanation` is one element spanning review 56.5–71.5, sourced continuously from master 59.5–74.5. At the emphasis cut it is simply passing master 70.916667, within the pause before “one” starts at 70.94.
- `ffprobe -show_frames` finds exactly one keyframe in B, at source frame 0. Source frame 120 at 5.0 seconds is a non-keyframe B-frame. A newly active second element must seek/decode into that stream; its earlier reference pictures are not eliminated by declaring a contiguous source range.

## Cause and fix assessment

The second media element creates a separate decoding and scheduling boundary exactly where the user notices choppiness. The lack of a keyframe at its source entry strengthens the explanation. It does not prove that this browser actually stalled; preloading and scheduling can sometimes hide the handoff, and a deliberately hard change in scale is itself visible.

One continuous B element, starting review 62.916667 at source zero and running for 8.583333 seconds, avoids seeking or switching media when the crop changes at review 67.916667. Keep the audio element unchanged. No fresh lip-sync or voice generation is needed for this local playback repair.

Use a sized, block-level **untimed inner wrapper**, with an outer 1280×720 clipping viewport. Keep timing and `.clip` ownership on the video alone. The two old rectangles are reproduced exactly by transforms of a 1280×724 base picture with transform origin `0 0`:

| State | Wrapper x | Wrapper y | Scale | Resulting picture size |
|---|---:|---:|---:|---|
| Promise | -160 | -24 | 1.25 | 1600×905 |
| One number | -256 | -42 | 1.4 | 1792×1013.6 |

Register synchronous `tl.set` state changes on the root's single paused timeline at **global time**, with the emphasis set at frame **1630 / 24 = 67.916667**. Do not change video dimensions, currentTime, play state, visibility lifecycle, or media-start at that point. Do not add a timed wrapper or a second timeline driving the same transforms.

## Verification and remaining risks

1. Check the baseline crop explicitly, then the exact boundary and the following frame. Seek in both directions—e.g. 68.5 → 67.0 → 0 → 68.5—to prove the GSAP sets restore each state rather than retaining a stale transform. Direct random-time snapshots must agree with sequential playback framing.
2. Play across roughly review 65–70 at normal speed in the same private browser player used by the owner, with actual narration. The accepted hard crop change should remain; a decoder freeze, extra repeated frame, or lost mouth motion should not. Static snapshots and a render cannot alone prove this preview-specific repair because rendering uses FFmpeg frame extraction instead of the live browser playback path.
3. Keep source and soundtrack hashes, source-in, total duration, 24 fps record range, and exact crop rectangles unchanged. No source picture trim or vocal emphasis repair is implied.
4. A single video still can stall at its initial entry, during network starvation, or if the player repeatedly seeks media rather than letting it run. The crop no longer needs a decoder handoff, but this change does not certify every runtime behavior. If the hitch remains, distinguish those scheduling issues from an intentional hard reframe before altering editorial timing.

Checks completed: R21 source inspection, audio declaration continuity, pinned asset hash verification, and source keyframe/frame-timestamp inspection. No normal-speed R22 playback verdict was issued by this worker.
