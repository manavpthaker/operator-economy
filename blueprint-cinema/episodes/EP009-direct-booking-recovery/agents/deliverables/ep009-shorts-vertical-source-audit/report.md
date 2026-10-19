# EP009 r8 vertical-source audit

## Result

The locked r8 picture can support 9:16 shorts now, but the long-form carrier should not be center-cropped wholesale. Presenter and most film shots can reuse their exact component MP4s. Every designed, evidence, title, and software-tool span needs a directed portrait treatment so the decisive state remains visible.

All six issued work-order inputs recomputed to their declared SHA-256 values. All 53 picture sources bound by the r8 build exist, recompute to their build hashes, and probe as 1280×720 at 24 fps. No bound video is higher resolution than the carrier.

The complete 75-segment, 87-span binding and reframe contract is in `vertical-source-map.json`.

## Locked carrier

- Picture: H.264 High, 1280×720, square pixels, 24 fps, 29,323 frames, 1,221.791667 seconds.
- Audio: AAC-LC, stereo, 48 kHz, 1,221.791 seconds.
- Audio authority: `assembly/r3/narration-master-r3.wav`, SHA-256 `0f0d5d326262813cb5ff5392fb263f15f6a8e871ad22e54c1274ff974037ca85`.
- The master is mono PCM at 48 kHz. The carrier is its unity stereo upmix over the mapped excerpt, with planned final zero padding and AAC encoder padding.
- Verification compared 58,646,000 samples. Full-channel correlation is 0.9999885; minimum voiced-window correlation is 0.9999701. Shorts should inherit the r8 carrier audio or an exact excerpt from this master. Component audio must not be used.

## Source-quality finding

Reusing component MP4s avoids cropping and re-encoding the assembled review file, but it does not add resolution: every presenter, film, graphic, and tool video is 1280×720.

Two source classes are better than the flattened carrier:

1. The Node-RED native still is 2560×1440 and hash-valid. It should drive the overview and static tool-detail shots.
2. Twenty-one bound designed-scene roots retain HyperFrames `index.html` source. Their exact current hashes and matching build manifests are in the map. They can be re-laid out and rendered at 1080×1920 without scaling a finished 16:9 page.

## Presenter treatment

Use the exact selected presenter component for each span. The default portrait treatment is a fixed 720×720 crop from source `[280,0,720,720]`, scaled 1.5× into target `[0,420,1080,1080]` on the 1080×1920 stage. This preserves the face, table, hand movement, shirt, and inn environment while avoiding the 2.667× enlargement of a full-height 9:16 cover crop.

If a hand crosses source x=280 or x=1000, widen to `[200,0,880,720]` and place it at `[0,518,1080,884]`. Keep framing fixed within each source span. Change framing only at an existing editorial cut. Do not face-track, interpolate, retime, regenerate, or extend the environment.

The default target ranges are:

- hair top: y=480–650;
- eyes: y=650–800;
- visible hands: no lower than y=1450.

These are review targets, not automatic tracking rules. P08's existing A/B crop and every internal presenter punch-in remain part of the locked source.

## Film treatment

Centered one-person actions use the same 720×720, 1.5× square window. F04/seg007 uses a right-weighted source window `[560,0,720,720]` to keep the innkeeper on screen.

The following two-person shots cannot use a 405-pixel center cover crop:

- F01/seg001 checkout;
- F02/seg002 guest exit and owner reaction;
- F08/seg066 return visit;
- F09/seg067 guest-book signing.

Use source `[160,0,960,720]` into target `[0,555,1080,810]`. This retains both people and the action line with only 1.125× enlargement. Keep the crop static unless a motivated shot-boundary reframe is explicitly authored.

## Designed and evidence scenes

Every `/scenes/` binding should be re-authored from its hash-pinned HyperFrames source at 1080×1920. A center crop of the 16:9 render retains only 405 source pixels across and hides evidence, labels, inputs, outputs, or state transitions.

Portrait recomposition may change geometry, line breaks, and path orientation. It may not change:

- numbers, claims, citations, uncertainty labels, or source context;
- object identities, causal order, or business state;
- narration cues or duration;
- separation between paired evidence sources.

Paired evidence cards should stack vertically with separate provenance. Horizontal routes can become vertical routes only when their direction, inputs, handoffs, and result remain identical. One decisive relationship should occupy each portrait frame.

## Software demonstration

The real-tool sequence is r8 output frames `[16752,17458)`, 11:38.000–12:07.417. A blind portrait crop would hide the native tool chrome and side-state. Use the existing nine-phase sequence from the r7/r8 manifests:

1. Node-RED overview `[0,42)`.
2. Tight OpenAI request branch `[42,102)` from the 2560×1440 still, crop `[480,240,640,360]`.
3. Returned fictional draft `[102,162)`.
4. Checkout-plus-one-day rule `[162,210)`.
5. Queued draft, awaiting human review, no sending `[210,261)`.
6. Recorded human edit and reading hold `[261,400)`.
7. One-draft approval `[400,552)`.
8. Seasonal exclusion `[552,622)`.
9. Human-control boundary `[622,706)`.

Display each exact 16:9 tool crop as a 1080×608 panel on the portrait stage and cut at these frame boundaries. The panel remains actual UI. Any explanation sits outside it and cannot imitate tool chrome. Preserve the order, holds, fictional-fixture boundary, and no-send state. Do not imply a graphical OpenAI dashboard or a fresh provider call.

## Portrait safety and captions

The map defines a 1080×1920, 24 fps stage centered at `[540,960]` with conservative project margins:

- action safe: `[60,120,900,1620]`;
- critical text and evidence: `[96,180,804,1420]`;
- platform UI avoidance: 180 px right, 300 px bottom, 120 px top;
- preferred caption rail: `[96,1450,804,210]`.

These are production margins for cross-platform review, not a claim that every client uses the same overlay geometry.

Captions remain an overlay. Do not shift the composition upward or reserve a dead lower band. Use the locked r3 word timings, a one-line rail when possible, two lines maximum, and at most one earned embedded word per beat. Captions do not replace readable diagram labels, source citations, or software state.

## Deterministic build order

1. Choose a short's in/out on the r8 24 fps frame clock.
2. Keep the corresponding r8 audio or extract the identical r3 master interval.
3. Replace picture span-by-span from the exact bindings in `vertical-source-map.json`.
4. Apply the named presenter or film preset, or re-author the bound HyperFrames scene at portrait size.
5. Rebuild the software demonstration only from the listed real-source frames and crops.
6. Add captions from the locked transcript.
7. Check first, midpoint, decisive action, final-minus-hold, and final frames.
8. Review the complete short at normal speed with original audio before any approval.

No media was rendered, generated, modified, uploaded, or sent in this audit. No canonical episode file or review decision was changed.

## Open limits

- `blueprint-cinema/episodes/EP009-direct-booking-recovery/` does not contain the normally required `README.md`, `episode.json`, or `input-lock.json`. This packet therefore binds only to the six issued work-order inputs and the exact sources named by the r8 build.
- The actual short scripts and editorial in/out choices belong to the shorts production packet. This audit makes the existing picture reusable; it does not choose publishable excerpts.
- Platform overlays must be checked on real YouTube Shorts and Instagram review exports because client and device chrome varies.
