# R73 S26 independent final QC

**No blocking trim, cue, layout, source-tail or padding defect found.** Final scene and context have149/305decoded frames, at1280×720 and24fps. This report binds the actual final hashes; it does not grant creative acceptance or claim continuous listening.

## Pinned outputs

- S26 HTML: `d78dfd06bf417877321adf0b9a3781d4255606c5d293dc9c2108a3d6e1c60acb`
- S26 MP4: `a70380c107d36a626b83195c3c31ab54a62763062fb8797e30e69b4bca705341`
- Context MP4: `5b00a3deba876218969e066886da6dda091922b8679ece98f71885d4b251783c`

All supplied hashes match. Accepted S25 index and video hashes also match. The staged-audio hash remains unchanged from the independent pre-render check.

## Complete source and exact ending

The staged S26 mono48kHz PCM16 WAV contains all296519original master samples [54324000,54620519), byte-identical, followed by exactly1481zero samples. It totals298000samples,149frames /6.208333seconds. The last nonzero source sample is staged index295774, local6.161958. The149th picture frame contains only original trailing zero samples and post-EOF padding.

Context assembly uses accepted S25 [570,726) then S26 [0,149). S26 begins at contextframe156 /6.5seconds. Continuous original context audio is [54012000,54620519),608519samples, followed by1481zeros:610000samples /305frames. The final picture endpoint is master1137.958333; its last frame begins1137.916667. This preserves the full original source ending at1137.927479.

Container precision detail: AAC stream durations are reported as6.208000 and12.708000seconds,333microseconds shorter than their picture durations. Standalone scene decoding yields16fewer samples than the298000-sample staged WAV, entirely within added post-EOF silence; the decoded context comparison includes the full requested pad. No original source-tail interval is lost. Byte-exact and exactly1481zero assertions apply to staged PCM, not lossy AAC.

## Encoded seam, final word and picture

The original-pause seam window, context6.25–7.25 /master1131.5–1132.5, has zero-lag correlation0.99998652, level difference−0.00569dB and residual RMS−59.62dBFS. The final-word/tail window beginning S26local5.4 compares against the verified staged PCM at correlation0.99970920 for scene and0.99987622 for context; levels differ by−0.04709 and−0.01799dB. These support retained source timing through “subscribe” and its tail, not a subjective listening verdict.

Decoded post-EOF padding contains only very low-level codec residual: scene RMS−125.67dBFS/peak−109.25dBFS; context RMS−134.14dBFS/peak−117.01dBFS. These values are recorded as measurements without requiring compressed audio to be bit-identical to PCM silence.

Eleven selected scene frames, including entry, “arithmetic,” “subscribe,” tail and final frame, match their context positions to within0.040mean gray levels out of255 at32×18. Both lead-in endpoints match the intended S25 trim. Encoded seam, first frame and full-resolution final scene/context frames show a clean cut and readable wordmark, description and invitation; no clipping, overlapping text or black ending was found in these samples.

The card is honestly declared static with `data-no-timeline`; no artificial animation is required. “Subscribe” is visible from the first frame, so the spoken final word lands on an established invitation rather than a late reveal. Sampled first-to-last variation is0.00348gray levels at32×18, consistent with compressed rendering of the same held card. There is no late fade that could obscure the final word.

## Limits

This agent did not continuously listen at normal speed or repeat root's full-frame blank scan. Source timing, encoded metrics and sampled pictures are separate from owner approval. No source, shared log, canonical state or gate was changed. All writes are confined to this deliverable folder; no provider calls or paid generation occurred.
