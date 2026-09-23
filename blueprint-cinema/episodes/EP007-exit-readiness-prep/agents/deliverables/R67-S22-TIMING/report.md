# R67 S22 timing and continuity audit

Status: independent timing proposal. No film sources or rendered assembly inspected. No approval claimed.

## Recommended cut

**Master [1047.0833333333333, 1068.9166666666667)**, exactly **524 frames / 21 5/6 seconds at24fps**. This retains the accepted S21 endpoint. S22's first aligned word starts1047.36; the incoming intake belongs to S22 and must remain.

The last aligned word, “inspectable,” runs1067.82–1068.62. Do not cut at1068.62: the tail remains. The proposed outpoint retains another296.667ms. Frames1068.875–1068.916667 and1068.916667–1068.958333 have RMS5.25 and5.70 in16-bit PCM, approximately−76dBFS, the quietest adjacent frame pair in this local interval. Samples immediately before/after the cut are0,1,1,1 |2,2,2,4. The cut therefore lands in a very low-energy valley with a one-count adjacent sample difference.

**This is not digital silence.** Both bins contain nonzero samples. Low-level activity continues after1068.958333, with another rise at1069.166667, and the initial S23 speech energy appears before its aligned1069.30 word start. Energy alone does not establish the exact physical boundary between final tail and next intake. This cut conservatively takes the earlier quiet valley after preserving the ending; normal-speed listening remains the final check. Keep the original continuous audio across the eventual S22/S23 seam. Do not mute the residual or retime speech to manufacture silence.

## Proposed editorial windows

These are scene-level timing windows, conditional on usable source action, not source in/out selections.

| Window | Master range | Frames | Required change |
|---|---|---:|---|
| A |1047.083333–1052.000000|118|Return to the recognizable original table before “Go back” at1047.36; let the repeated question run1049.38–1051.60. The seller has not yet repeated the old inability to answer.|
| B |1052.000000–1059.083333|170|Enter just before “And this time” at1052.02. She promptly accesses the available record, making its readiness legible by “does not stop” at1052.84–1053.54. Let the record enter his reading space on “It is written down” at1057.48–1058.60. Her hands then return to rest.|
| C |1059.083333–1068.916667|236|Enter just before “He can read it” at1059.12. Buyer takes responsibility for reading/checking; “check” lands1060.36. Continue independent inspection through “Nothing about the business changed” at1061.18 and “The only difference” at1065.59, ending on inspectability rather than a sale verdict.|

The first boundary separates the repeated question from the different response. The second separates supplying the answer from independently examining it. Keep the record's identity, location, orientation and custody coherent across that second cut. A source action may justify a few-frame cut adjustment inside the inter-phrase space; narration timing remains fixed.

## Hold and continuity risks

1. **Do not wait until1057.9 to begin the seller's meaningful response.** That would make her appear to search silently for aboutfive seconds under “this time she does not stop,” reversing the callback's intended contrast. Prompt access and later handoff are separate states.
2. The **9.833-second final inspection window** is the principal hold risk. It requires useful continuous reading/checking, not a frozen frame, repeated motion or a brief glance stretched into10seconds. A single coherent inspection can justify the hold while the narration limits the outcome. If the source cannot sustain it, root needs another motivated inspection view; this audit does not approve a retime or loop.
3. Do not cut away before the buyer has visibly begun checking, and do not reintroduce the owner's anxious pause as filler. The answer has moved out of her memory. Her hands at rest help make independent use legible.
4. The callback is an **illustrative replay**, not “weeks later the buyer returned.” Preserve opening table geometry, actors, clothing, action line, daylight and business. Do not imply that the prior walk-away was followed chronologically by a new successful meeting.
5. No handshake, celebratory smile, approval stamp, purchase signature or transaction verdict. R35 explicitly sets inspectability as the only payoff. Do not show increased profit or an improved business; the narrated claim is that the same business became inspectable.
6. Keep record contents oblique/unreadable unless exact approved operational content is supplied. No fabricated legible financial proof. A page/table insert can show access and custody without claiming documentary evidence.

## Picture/audio contract

Recommended `mode: narrated_dramatization`, `language_carrier: narrator`, `coverage_grammar: motivated_interaction`, `sound_intent.dialogue: none`. Face function is `task_focus` during access and checking. Visible speech may be prohibited for these non-speaking actions; do not claim exact lip sync for the question. Preserve illustrative framing. Mute viewing tests custody and independent inspection; actual audio supplies the meaning. No new generation or provider call was made or authorized here.

## Verification and limits

All three issued SHA-256 inputs match. Exact W002944–W003015 cues and sentence ranges are in `cues.json`; original PCM bins and adjacent cut samples are in `endpoint-audio.json`. The R35 scene-arc source and relevant directing authorities are hash-bound in `deliverable.json`. No film-source suitability, rendered frame continuity, or normal-speed listening verdict is claimed. Only this audit's owned deliverable folder was written.
