# OmniHuman native QA: two completed samples

Both native SHA256s match the parent's handoff. No source media was modified.

| Result | Native picture | Audio alignment | Checked ending |
|---|---|---|---|
| omnihuman-01 | 1248×704, 25fps, 141 frames, 5.640s; full decode passes | 0ms lag in overall, early, late and final-word windows; early/late correlations 0.999980/0.999975 | 0.290s picture margin after the checked 4.95–5.35s final-word window |
| omnihuman-02 | 1248×704, 25fps, 141 frames, 5.640s; full decode passes | 0ms lag in overall, early, late and final-word windows; early/late correlations 0.999980/0.999975 | 0.290s picture margin after the checked 4.95–5.35s final-word window |

Both have a native 5.600s 48kHz mono AAC stream. The decoded analysis buffer includes codec padding; it is not an altered master duration. The source waveform is strongly matched; no inter-sentence lag difference was measured. These findings establish audio correspondence, not visual lip sync.

Contact sheets inspected: 14 native-PTS samples per clip, source diagnostic times 0.00/0.76/0.92/1.04/1.20/2.80/3.20/3.60/4.16/4.32/4.44/4.64/5.20 plus the final frame at 5.60s. No extra frame alignment or geometry correction was applied.

Sampled observations in both clips:
- Head/upper body visibly dip and lean forward across 0.92–1.20s, near “straight.” The hand is higher at 0.76s than the resting later samples. These movements remain relevant to the owner's restraint request.
- Mouth is open at some quiet-pause samples, notably 3.20 and 3.60s. This can be flagged for moving review; stills cannot distinguish anticipation/breathing from a mismatched talking reaction.
- The room shelves remain substantially straight in the sampled images. Hands remain attached; the moving right hand is softer in some early frames. No unequivocal extra limb or gross head/neck separation is visible at contact-sheet scale.
- The two samples have similar broad poses/actions but differ in expression, including the ending. Distinct file hashes do not alone establish independent motion sampling.

No fresh continuous audiovisual playback was possible through this review surface. **Visual lip sync, naturalness and owner preference remain unverified.** Neither a smaller mouth opening nor waveform correlation can pass the second-sentence sync requirement.

Technical reports:
- [OmniHuman 01](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/omnihuman-01/technical-review.json)
- [OmniHuman 02](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/omnihuman-02/technical-review.json)

Contact sheets:
- [OmniHuman 01](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/omnihuman-01/contact-sheet.jpg)
- [OmniHuman 02](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/omnihuman-02/contact-sheet.jpg)

InfiniteTalk outputs are still pending this report. No automatic retry, alternate render or correction is initiated by QA.

