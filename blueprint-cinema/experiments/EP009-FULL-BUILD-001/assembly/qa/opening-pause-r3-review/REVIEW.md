# Opening pause review

Recommendation: remove 3.25 seconds from the completed logo hold. This leaves about 0.7 to 0.8 seconds between the question and the spoken brand introduction, preserves the full logo reveal, and removes no nonzero narration samples. This is a pacing proposal for owner review, not a playback acceptance.

## Review clips

- `before-full-question.mp4`: original source frames [1306,1680), 15.583333 seconds, 374 frames.
- `after-full-question.mp4`: original source frames [1306,1438) followed by [1516,1680), 12.333333 seconds, 296 frames.

Both start in the pause before the complete question and continue through the brand introduction. Both contain the current r2 draft's retained r1 presenter. Earlier 55-second-start preview clips are retained, but the full-question pair is the preferred comparison.

## What causes the wait

The presenter asks, “So what did that second stay actually cost her, and who gets paid to stop it?” Actual speech decays around 59.26 seconds. The word transcript gives the final “it?” as 59.24 to 59.42 seconds. The presenter ends at frame 1426, 59.416667 seconds.

The brand field starts at frame 1427, 59.458333 seconds. THE appears first, then Operator Economy; the lockup is complete at frame 1436, 59.833333 seconds. It sits unchanged until the narration resumes. “This” begins around 63.29 seconds on the waveform, or 63.38 seconds in the word transcript. Thus the long delay is before the spoken introduction, while the logo is already visible.

The old direction deliberately preserved this pause with “Do not trim the 4 s room.” The new owner feedback is a request to revise that pacing choice.

## Exact proposed edit

| Item | Source range | Amount |
|---|---|---|
| Picture | frames [1438,1516) | 78 frames |
| Locked master | samples [2876000,3032000) | 156000 samples at 48 kHz |
| Time | [59.9166667,63.1666667) seconds | 3.25 seconds |

Every removed audio sample is exactly zero. The contiguous zero run is samples [2854412,3035018), or 59.4669167 to 63.2295417 seconds. No fade, crossfade, speed change, syllable cut or narration rewrite is needed.

The cut joins original frames 1437 and 1516, both the completed static lockup. Their mean RGB difference at 640x360 is 0.00434 on a 0–255 scale, attributable to encoding variation. The entire nine-frame logo entrance remains. The transcript's 3.96-second inter-word gap becomes 0.71 seconds; the waveform estimate falls from 4.03 to 0.78 seconds. This preserves a short identity beat and lets the spoken introduction carry the logo hold.

## Verification and limits

Read 12 actual encoded-source stills across the presenter exit, reveal, proposed cut and narration return. See `encoded-boundaries.jpg`. The preferred clips decode to 374 and 296 frames at 1280x720 and 24 fps; audio is 48 kHz stereo, checked per channel against the corresponding unchanged source samples, with zero-lag correlation above 0.999. Exact hashes and measurements are in `FULL-QUESTION-VERIFICATION.json`. Normal-speed audiovisual pacing remains to be reviewed.

`EDIT-PROPOSAL.json` contains the source bindings and exact edit map. Full assembly, master, SHOT-PLAN and scene files remain unchanged. Applying this to the episode requires a new editorial timing revision: all subsequent cues advance 78 frames, making the picture 29529 frames / 1230.375 seconds. Retain the original master and bind the derived soundtrack separately; it would no longer have the locked master hash.
