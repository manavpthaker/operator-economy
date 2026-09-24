# R69 S22 final independent QC

**Technical checks pass for this exact review candidate.** No timing, audio, blank-frame or source-order defect requiring a change was found. This is not owner acceptance or release approval.

## Verified output

- Scene:524decoded frames,1280×720,24fps,21.833333seconds. Context:716decoded frames,29.833333seconds, with192frames of locked S21 before S22.
- Scene intervals are contiguous **[0,55),[55,163),[163,260),[260,524)**. No intended overlap or uncovered frame. HTML and selected native windows agree: establishing108–162, question0–107, A96–192, B1–264, all inclusive at native24fps. The malformed A opening is excluded. B's duplicated frame0 seed is excluded.
- Independent all-frame source comparisons and seven candidate timing-offset checks identify zero-frame offset for every segment. No scene adjacent-frame pair was identical under the tiny-image RMSE threshold0.05. There is no evidence of an edited loop, freeze or speed change. Comparisons are downscaled image evidence, not pixel identity: resampling and re-encoding change pixels. Static pairs in the preceding locked S21 graphic are expected and lie outside S22.
- All-frame luminance variation detects no near-uniform blank candidate. Minimum frame SD is46.04 for S22 and11.69 for context, above the declared3 threshold. Exact seam samples are also visually populated.
- Staged narration PCM is **byte-identical** to locked master samples50260000–51308000, corresponding to1047.083333–1068.916667. The endpoint remains low-energy nonzero audio; no claim of digital silence.
- Encoded scene versus master: correlation0.9998284, level−0.02342dB. Context:0.9999207,−0.01296dB. The context entry seam window7.75–8.25seconds independently compares at0.9996414 and+0.002845dB. These are encoding differences, not evidence of a shifted or replaced narration track.
- The context's first192frames match the expected locked S21 tail; its remaining524match the scene. Browser cue values8,14.791667 and18.833333 correspond to S22, the open record and buyer inspection.

## Picture and narration

The revised question handle works as listener coverage. In inspected source frames it settles before “she does not stop,” allowing the owner to prepare the record off-screen. The selected A begins on the causal explanation at master1053.875, with the record already open. The edit does **not** show the binder opening and should not be described as doing so.

A's sampled progression is: open written-record view → owner points to the right-hand passage → her hand withdraws → both attend to the record. The A/B seam at scene259/260 retains the open record, object arrangement, actors and her resting hands. It does not repeat the removed opening.

B enters at master1057.916667, within “written.” The buyer reaches toward the record during “He can read it” and his fingertip is beside the passage in the sample at master1060.416667, within “check.” Her hands remain at rest. The later sample at master1067.083333 shows his restrained positive response toward her after several seconds of inspection; the final sample shows him attending to the record again. This sequence supports acknowledgment of the answer rather than a transaction conclusion. No handshake, signature, payment or completed-sale action appears in the inspected assembly samples.

The record's apparent content, hands and generated-source artifacts remain the independent source reviewer's responsibility. This timing review does not turn small printed marks into verified operational facts or certify every intermediate generated detail.

## Evidence and limits

`technical-qc.json` retains probes, selected intervals, all-frame variation summaries, source mapping errors, hashes and audio measurements. `scene_seams.png`, `action-a.png`, `action-b.png`, `context_entry.png` and their accompanying index files bind sampled visual judgments. `timing-revision.md` has been preserved unchanged after root pinned it.

No continuous normal-speed listening verdict is claimed by this reviewer. Technical audio comparisons establish alignment and level; sampled visual inspection establishes the reported frame states and timing, not every motion transition or owner comprehension. Root's normal-speed playback and the owner's creative review remain distinct.

## Exact candidate hashes

- HTML:29350c543cee864086cae7582395ce313abbb9e6d543d88c293f40a7c99d6f98
- S22 MP4:c3352c537fa560667c29c08614312eca78d9172b30f0ef8fb52da49760f8067f
- Context MP4:06f0571f21643069c19f443fef9ccff2dbb7fb9bcffb3bc20ac0b1916b0bc3a9

Only the authorized R69-S22-FINAL-QC directory was written. No shared source, request, provider call, production log, gate or canonical state was changed.
