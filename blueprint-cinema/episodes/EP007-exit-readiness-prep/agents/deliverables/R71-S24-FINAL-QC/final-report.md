# R71 S24 bounded final QC

**No source-clock, trim, cue-position or sampled-layout defect found.** This report binds the actual 552-frame S24 and 744-frame / 31-second context that root says the owner accepted. The proposed 782-frame wrapper was not built and is not claimed here. No approval or production-state action is performed by this audit.

## Bound outputs

- S24 index: `a7727975f424cd0f4ef26eae363d4b55b16cedd1262ab3f869032c8ed9c94f05`
- S24 MP4: `c9945847aa4e4b281379e7331bb1fe097d3397530c08e97eea7c8551ae84a0a8`
- Context MP4: `1d2cb8332856467934365f516178d25cca0e1f45f1ec8094b9955184366fef32`

All three hashes match supplied pins. Actual decoded counts are 552 and 744, 1280×720 at 24 fps. Context uses S23 frames [38,230) then S24 [0,552). Continuous source audio is master samples [51384000,52872000), 31 seconds. Scene PCM is exactly the master's 1104000 samples [51768000,52872000), mono PCM16 at 48 kHz. The final displayed frame begins at master1101.458333 and ends at1101.5.

## Actual cue and image evidence

Selected source/context comparisons verify both lead-in endpoints, S24 endpoints, reveal boundaries and condition switch; the largest 32×18 mean gray-value difference is 0.08334 out of255. Inspected encoded frames show the intended sparse “My verdict” opening, then fixed “Build / To find out.” The first word reveal begins on scene frame45, the research finding on163, personal-model finding on258, and the condition group on358. Each entrance lasts six frames.

At frame358 the evidence clears and conditions start at zero opacity; the fixed verdict remains visible throughout. Conditions are fully visible at364 and hold for188 frames /7.833333seconds. No sampled blank, overlap, clipping or off-screen qualifier was found. The group preserves “either,” OR, “true locally” and “Neither established here.” The research limit remains “in my research”; the base-case shortfall remains “my target.” Early display of both conditions supplies sufficient reading time without making them observed facts.

## Findings and limits retained

1. **Review-only opening truncation.** The requested exact eight-second lead-in starts at master1070.5 inside aligned S23 “work” (1070.44–1070.68), excluding60ms of its onset. This affects the isolated context opening, not the S23→S24 seam or complete episode. Root closed the unbuilt full-S23-wrapper proposal after owner advancement; this report preserves the actual reviewed context.
2. **Narrow audio metric below the initial generic threshold.** The0.75-second seam window (context7.5–8.25, master1078–1078.75) produces zero-lag correlation0.9985668, below the initial0.999 check. That check failed and is not relabeled as passed. Level differs by−0.01049dB; residual RMS is−62.96dBFS versus source RMS−37.53dBFS. Zero lag is the best tested offset (±1,2,4,8,16samples); adjacent seam samples remain near source zero. These results do not indicate a displaced seam, but cannot alone establish the subjective absence of an audible encoding artifact. Root's full-clip audio checks are separate and were not broadly repeated.

No continuous normal-speed listening was performed. Root's full-frame blank scan was not independently repeated; the present review used actual decoded counts and selected encoded image comparisons. All writes remain inside this deliverable directory. No provider call, shared source/log edit, gate change, or synthetic generation occurred.
