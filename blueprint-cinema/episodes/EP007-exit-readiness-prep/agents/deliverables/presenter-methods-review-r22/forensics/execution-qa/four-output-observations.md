# Four native outputs: completed technical and sampled review

All four expected native file hashes were verified before and after read-only QA. Every file passes complete decode. No media was resized, remuxed, retimed or geometrically corrected.

| Native result | Picture | Source-audio lag early / late | Correlation early / late |
|---|---|---|---|
| OmniHuman 01 | 1248×704, 25fps, 141 frames, 5.640s | 0 / 0ms | 0.999980 / 0.999975 |
| OmniHuman 02 | 1248×704, 25fps, 141 frames, 5.640s | 0 / 0ms | 0.999980 / 0.999975 |
| InfiniteTalk 01 | 1280×704, 25fps, 137 frames, 5.480s | 0 / 0ms | 0.999274 / 0.999762 |
| InfiniteTalk 02 | 1280×704, 25fps, 137 frames, 5.480s | 0 / 0ms | 0.999274 / 0.999762 |

No inter-sentence lag difference was measured. OmniHuman audio is native 48kHz mono AAC, 5.600s; InfiniteTalk audio is 44.1kHz mono AAC, 5.480s. These are provider outputs, not altered masters.

Both InfiniteTalk samples preserve the source ending through 5.48s. The missing 5.48–5.60s source tail measures RMS −107.54dBFS / peak −90.31dBFS. Their extracted AAC payloads are identical, with matching stream timing, so the separately measured InfiniteTalk 01 ending evidence also applies to 02. See [audio equivalence](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/infinitalk-audio-equivalence.json) and [ending check](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/infinitalk-01/ending-audio-review.json). The native clips remain 0.12s shorter than the 5.600s input; no duration-equality claim is made.

## Sampled comparison

- **OmniHuman 01/02:** noticeable forward head dip near 0.92–1.20s; one early right-hand lift, with quieter hands in later samples. Similar broad actions across both outputs, with differing expressions.
- **InfiniteTalk 01:** less dramatic first-sentence head dip in the sampled sheets, but both palms lift/open across 0.76–1.20s, then another right-hand lift around 4.16s.
- **InfiniteTalk 02:** avoids 01's broad two-palm opening in the first sentence, using a right-hand lift instead. Its second sentence has a more conspicuous right-hand lift and later head/side lean. Later samples also change room/window-edge details, including dark edge marks; inspect for background drift in playback.
- All four have some open-mouth quiet-pause samples. InfiniteTalk 01's 3.60s opening is especially clear; whether this is anticipation or an inappropriate speech reaction requires moving audiovisual review.
- No clear restrained-motion winner is established by these stills. The two InfiniteTalk outputs trade first-sentence gesture behavior against later expressiveness.

## Review boundary

Each contact sheet contains 14 native-PTS samples. This reviewer did **not** perform continuous audiovisual playback. Actual mouth/word sync, second-sentence sync, naturalness and owner acceptance remain unverified in all four review records. Source-audio correspondence does not pass any of those criteria. No further generation is requested or initiated by this QA packet.

Contact sheets:
- [OmniHuman 01](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/omnihuman-01/contact-sheet.jpg)
- [OmniHuman 02](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/omnihuman-02/contact-sheet.jpg)
- [InfiniteTalk 01](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/infinitalk-01/contact-sheet.jpg)
- [InfiniteTalk 02](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/infinitalk-02/contact-sheet.jpg)

[Four review records](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/review-records.json) · [Deliverable manifest](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-methods-review-r22/forensics/execution-qa/deliverable.json)

