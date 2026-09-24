# R9 illustration recovery audit

Reviewer: independent QA/recovery agent. Date: 2026-09-08. Status: complete read-only comparison, not a creative approval or production gate.

## Recommendation

Recover **the pencil-study's line construction**, combine it with **net-new 001's large business-to-owner staging**, and borrow only **R3's owner-absence consequence**. None of those old compositions is a complete drop-in answer for the new film-to-illustration transition. The user's remembered version cannot be uniquely identified from the available request.

The clearest recovered style reference is the **right-hand drawing** in `experiments/EP007-BL-MOTION-001/pencil-study/renders/pencil-detail-comparison.png`: unequal short overlapping contours, real gaps, local pressure variation, and sparse cross-hatching. This is visibly different from a clean heavy outline duplicated once.

All paths below are relative to `blueprint-cinema/`.

## Three useful candidates

### 1. Pencil study: best recovered rough-pencil construction

- Source: `experiments/EP007-BL-MOTION-001/pencil-study/index.html`
- SHA-256: `c580485d42941e10652b4b71e3e344c1140323fee0af717086ee16e102ce33e2`
- Inspected comparison: `experiments/EP007-BL-MOTION-001/pencil-study/renders/pencil-detail-comparison.png`
- Comparison SHA-256: `81dbea57d70bf62f417b05b82752f4f0fcab839679b290ab8687ecfa3252081f`
- Existing rendered file: `experiments/EP007-BL-MOTION-001/pencil-study/renders/EP007-BL-PENCIL-001.mp4`
- Render SHA-256, recomputed: `f9a5701b9a1fdf96099a4b4f1737b52b23eaaaac6f66f0a335e4f4f47dcfe587`

Observed: owner figure connects to pricing judgment, how work happens, customer ties, and an owner-only item. Later frames add baseline, records, written support, relationship visibility, and diligence package. The linework is materially rougher than the marker-like baseline: broken silhouettes, multiple unequal passes, hatching that follows object shape.

Source evidence: `pencil-build.json` records 2,920 fixed vector strokes and 27 reveal masks; its output hash matches the current HTML. Inspected compiler segment uses short fixed strokes, 2–3 overlapping passes, varying width/opacity, actual gaps, and hidden reveal masks. Existing review calls this an internal style test, not approval. Compiler SHA: `c592416ea034da1bff45594089483f8eb103d2a73bdea8099d96badfedc3c6b5`.

Reuse boundary: line construction and owner silhouette are strong references. Do not restore the entire composed worksheet, internal headers, four-card list, or diligence-solution sequence into the opening. Those introduce later-stage information. Fine hatching recedes at reduced size; prioritize readable primary contours.

### 2. Net-new 001 model exposure: best roomy composition

- Source: `experiments/EP007-NET-NEW-UNFINISHED-ANSWER-001/hyperframes/compositions/sequences/03-model-exposure.html`
- SHA-256: `0d1297cddaf0eb8b8fd87d9dec89198bbb6c0677a5c15b83efb7d3032ce54c39`
- Inspected encoded contact: `experiments/EP007-NET-NEW-UNFINISHED-ANSWER-001/hyperframes/qa/encoded-001/contact.png`
- Contact SHA-256: `b1a4728def1e43b5ea60faedc55a55a9fc44554804835ba76219c756bdeb7774`

Observed: a large three-bay business structure occupies the left, an upright owner at a work surface occupies the right, and three routes converge on the owner's hand. The composition gives the illustration enough screen area and avoids a dominant equation.

Source evidence: independent construction marks, segmented contour passes, and hatching are present. Main stroke classes reach 5.8 px, substantially heavier than R3's 2.55 px maximum. The timeline draws business, owner, then dependencies and settles.

Reuse boundary: recover scale and spatial relationship, not the old film/pencil match-cut premise. It shows dependency but does not itself demonstrate owner absence or the unresolved consequence. The three operating bays are unlabeled and can read as a building; new direction must make their business function legible. Keep her competence and do not collapse the entire business merely to dramatize risk.

### 3. R3 revised model: useful causal operation, weak hierarchy

- Source: `experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r3-relevant-edit/compositions/model-exposure.html`
- SHA-256: `0d4fa07954d85e9f70e4f0f5c6405a0c9e479b442ac2fe706f3d9fd7bc6ee82a`
- Inspected reveal sheet: `experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r3-relevant-edit/snapshots/sketch-reveal/contact-sheet.jpg`
- Sheet SHA-256: `3a7da1d602f2a671f838fb32a87fdb4c3da74d8bd623ec6acf91adb8ed77ede7`

Observed: a large equation dominates; small relationship/process/record marks converge on an owner checkpoint below. The owner moves aside and a work item stops before the empty checkpoint. Thin linework exists but the explanatory drawing is subordinate to text and small icons.

Source evidence: stroke widths 1.0–2.55 px; opacity-preserving reveal fixes a documented old behavior that forced faint correction marks to full opacity. At local 4.72 seconds the owner shifts right; a work token moves at 4.86 and settles at the checkpoint; the unresolved state then holds. These are source-code timing facts, not a continuous playback review.

Reuse boundary: borrow the operation, not the equation, crowded labels, or socket-like metaphor. For R9, the paths must remain visibly unresolved when she is unavailable. Unknown continuity is not established catastrophic failure. Its labels also assert specific deficiencies that need the new scene's upstream support; do not import them just because they already exist.

## Other versions inspected and excluded

- Net-new 002 encoded contact: four month/work boxes route to a tiny owner and later sit inside a larger rectangular business. Relevant dependency idea, but its repeated anonymous boxes and small figure are less immediate than 001; not a better recovery source.
- R4 root explicitly replaces the model with `unanswered-equation.html`; not an illustration recovery candidate.
- R5 `rough-question.html` and final-byte-check contact: thin overlapping table, chair, binder, paper, question mark. The rough style is real, but the empty chair repeats the question rather than explaining which work depends on her. The user previously rejected its meaning; roughness alone does not solve that.
- Callback Arc, Callback Keepers, and Callback In Context sheets are principally film coverage, not the missing illustration.
- BL Mixed review frames contain a rough owner/business/buyer treatment, but the inspected early sheet has title/diagram collisions and later thesis/transfer states; the later seam sheet is cleaner but too schematic to displace the three candidates above.

## Verification and limits

- All five work-order input hashes matched before inspection and again at completion.
- Visually inspected existing encoded/snapshot contact sheets and comparison images, plus relevant source/review files. No fresh render, preview server, audio listening, full-motion pass, source editing, paid call, asset generation, or canonical-state mutation.
- Existing files are historical review evidence. Current source hashes do not alone prove every old screenshot was produced from today's source. The pencil-study's own build record binds its current source hash; other source/appearance comparisons are qualified accordingly.
- The target canonical episode README, episode.json, and input-lock.json are absent. This report therefore makes no `inputs_locked` or canonical approval claim; it uses only the issued frozen experiment inputs for the owner-authorized recovery audit.
- HyperFrames, general-video, media-use, and CLI skills were inspected for the audit boundary. No skill refresh, media adoption, or runtime upgrade was performed because this worker is read-only outside its deliverable folder.
- Root owns final scene meaning, film-to-model timing, asset choice, implementation, and review. The historical preferred illustration remains uncertain until the user recognizes the reference or approves the new trial.
