# V4 wider avatar experiment

Status: **complete and ready for owner review**. [Open the comparison viewer](http://192.168.1.159:53833/) on the same local network.

The finished [wide-to-closer edit](media/wide-with-question-crop.mp4) and [continuous wide version](media/wide-phone-clean.mp4) are both 1920×1080, 24 fps, 505 frames and 21.042 seconds. The edit changes framing at frame 429, 17.875 seconds, using a 1.30× top-anchored crop. A tiny overscan removes corrupted bottom rows in the generated source. The original mono AAC narration is preserved; all 20.9 seconds of the approved passage are present.

The edited video completed browser playback at normal speed with sound enabled and no playback error. Face/hand frame review found no blocking visual defect in the inspected samples. Naturalness and perceptual lip sync remain for owner review; V3 remains the accepted baseline. See [QA.json](QA.json) and [OUTPUT-MANIFEST.json](OUTPUT-MANIFEST.json) for exact results and hashes.

Owner instruction on 2026-09-11: “lets try that”, referring to the wider still and same 21-second EP007 opening with one closer crop on the buyer question.

The [accepted V3 recipe](../avatar-v3-lock/ACCEPTANCE.json) remains the performance baseline. This experiment changes the composition to include both forearms and complete resting hands, permits one modest gesture, and requests 1080p instead of 720p. A new generation is stochastic; the preserved recipe is not a guarantee of identical delivery.

## Inputs and execution

- [Wider reference still](media/wide-study-reference.png): generated with the built-in image tool from the accepted study portrait. Full prompt is in [IMAGE-PROMPT.txt](IMAGE-PROMPT.txt).
- `SUBMISSION-INTENT.json`: exact Seedance 2.5 request, existing reference media IDs, current model constraints, cost estimate and balance before submission.
- `JOB.json`: generation receipt. One authorized 21-second 1080p take; estimated 189 Higgsfield credits.
- `approved-opening-00m00s-00m20.9s.wav`: exact original narration for restoration and verification. No retiming.
- [PROMPT.txt](PROMPT.txt): exact generation prompt. The camera stays fixed during generation; the closer crop belongs to the edit.
- `STATUS.json`: current progress only, not owner acceptance.

## Review target

Preserve the accepted face, study, visible articulation and natural settling while adding believable resting hands and one small explanatory gesture. Compare the continuous wide take with an edited take that changes to a closer, upper-anchored crop just before “What happens here if you are not around for a month.” Final cut timing must use V4's own measured original-audio placement, not V3's offset.

This is an isolated review experiment. Canonical episode picture/audio, upstream narration and publication state remain unchanged. Media and renders stay ignored by Git.
