# Fresh EP007 Phase 2 → Higgsfield → HyperFrames test

Private opening test, built from the locked narration master, its word timing, and the upstream editorial handoff. Scope is the first 59.86 seconds of EP007, not the full episode. The video container is 1796 frames at 30 fps (59.866667 seconds); the original narration is unchanged.

[Watch the test](review-media/ep007-fresh-higgsfield-hyperframes-test.mp4) · [Editable Studio](http://localhost:3024/#project/hyperframes) · [Direction packet](DIRECTION-PACKET.md)

| Stage | What it supplied in this test |
| --- | --- |
| Phase 2 | Locked narration, word timing, the approved story and operating question. All 13 upstream source hashes were verified. |
| Film and editing references | Across-table geography; wide, buyer and owner coverage; narrated dramatization; an uninterrupted answer-to-pause performance; a protected silence; motivated cuts into the Working Model and presenter. |
| Higgsfield | Fresh cast and meeting images, three generated scene clips, and a new 12-second avatar performance from the approved HeyGen portrait plus the exact 11.34-second introduction audio. |
| HyperFrames | Original Working Model illustration and animation, identity typography, presenter label, timed assembly and the local review MP4. |

No earlier film cast, footage, prompts, composition, or Working Model was imported. The approved avatar portrait was the sole reused visual reference. Brand semantics and runtime implementation knowledge were retained.

The cut is wide meeting (0–14.77), buyer question (14.77–21.28), owner answer and pause (21.28–35.08), Working Model and show identity (35.08–48.52), then the avatar introduction (48.52–59.86). Exact source ranges and hashes are in `EDIT-MANIFEST.json`.

## What the result establishes

- The hybrid can produce an inspectable, timed opening using the locked Phase 2 handoff. Higgsfield supplies performance and footage; HyperFrames supplies precise graphics and assembly.
- The first text-to-video generation placed the people beside one another. An image edit also failed to correct the seating. A fresh master image with explicit table geometry, followed by reference-derived camera setups, produced the selected coverage. This supports reference-led generation for continuity; a detailed prompt alone did not reliably establish it.
- Sampled owner frames show the answer gesture, then a closed-mouth thinking hold. The late source contains distinct decoded frames, so it is not a literal repeated-frame freeze. This does not itself establish convincing acting at normal speed.
- The generated avatar retained the approved appearance in the inspected frames. Speech recognition found all 31 introduction words in order, without added words. Its returned audio tracks the reference at zero measured lag (whole-clip correlation 0.99975). This is strong timing evidence; it does not independently prove natural lip motion.

## Verification and limits

All four selected source clips and the exported MP4 were fully decoded. HyperFrames lint, runtime, layout and contrast checks passed. Exported frames were inspected across the scene changes, graphic transformation, avatar and final frame. The original opening WAV is the only assembly audio source; every generated clip is muted. Detailed encoded-audio measurements are in `review-media/final-audio-review.json`.

The initial export exposed one blank terminal frame. The presenter visibility was extended to the video frame boundary and an unnecessary terminal hide was removed before re-rendering. This changed no narration samples or editorial timing.

The animation-map diagnostic duplicated child and rebased timeline entries, producing collision and offscreen flags. The authored timelines and inspected frames were checked directly; automated motion checking was disabled in the ordinary check report. Sparse source-keyframe warnings remain recorded, with no observed exported-frame freeze requiring new source encodes.

This is a 720p review test. Whole-episode continuity, repeated avatar performance, compressed phone readability, final sound mix, color and editorial finish have not been established. DaVinci Resolve remains the canonical final editorial and delivery stage. No creative approval, canonical gate advancement or publication follows from this test.

**Cost: 105.5 Higgsfield credits**, including the two rejected attempts. Balance moved from 1119 to 1013.5, within the 150-credit first-pass ceiling. All nine generation jobs completed. Exact prompts, IDs, result URLs and selection decisions are preserved in `GENERATION-RUN.json` and `GENERATION-RECEIPT.json`.

My assessment: this is a workable division of responsibilities worth judging from the actual cut. The key unresolved decision is performance quality and iteration burden, not whether the two tools can be connected.
