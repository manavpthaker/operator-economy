# EP007 Boundary Ledger narration-first A/B arm

Status: bounded comparison candidate; Review Cut 007 rendered for owner review; not a V4 gate pass,
production select, or publication approval.

## Question

Does a shot sequence derived from narration and directing principles before any footage exists fit
the story better than an edit developed by reacting to generated clips?

## Clean-room boundary

The directing pass was produced in an isolated context from only:

- the locked narration passage and its word/pause timings;
- EP007 portrayal and claim guardrails;
- Boundary Ledger semantic roles;
- `smixs/visual-skills` dramaturgy and editor-mode references;
- `Nagacash/narrative-film-direction` coverage and screen-direction references.

The directing pass did not inspect or reuse Variant A's storyboard, prompts, stills, generated film,
selections, compositions, or manifest. Its two-shot sequence was locked before image generation.

Implementation is not blind: the primary builder knows Variant A. It may conform the locked plan to
exact word timing and reject defective generated frames, but it may not change the two-shot logic in
response to Variant A before the first B render.

## Controlled passage

- Excerpt asset SHA-256: `1dea3844a964ca6ed0afa6b662205e04a0143fb0fdb0717e683254b7c6c64bf0`
- Narration master SHA-256: `d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9`
- Word transcript SHA-256: `f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7`
- Pause map SHA-256: `0176614eb0902d945165956af8fa7ef890906d5f2e15692d14c9e0d9d8b8bdaa`
- Excerpt-local range: `18.16–25.90`
- Narration-master range: `247.66–255.40`
- Words: `W000712–W000736`

> The problem is what happens when somebody finally looks. Back to her question, then. What
> happens here if you are not around for a month.

## Rendered comparison

- Variant A context: `hyperframes/renders/EP007-A-CLIP-FIRST-context-17.5-27.5.mp4`
- Variant B context: `hyperframes/renders/EP007-B-NARRATION-FIRST-context-17.5-27.5.mp4`
- Variant B6 context: `hyperframes/renders/EP007-B6-NARRATION-FIRST-context-17.5-27.5.mp4`
- Review Cut 007 context: `hyperframes/renders/EP007-REVIEW-CUT-007-context-17.5-27.5.mp4`
- Result: `AB-RESULT.md`
- Blind review: `qa/BLIND-AB-REVIEW.md`
- Technical and shot-plan review: `qa/TECHNICAL-VERIFICATION.md`
- B6 execution review: `qa/B6-VERIFICATION.md`
- Review Cut 007 verification: `qa/REVIEW-CUT-007-VERIFICATION.md`

The blind review selected B's direction. B6 was the strongest execution in that original test: it
removed the fake dialogue and moved scrutiny into the operation on the intended phrase, but its
30–40° head turn and blink failed the predeclared 3–5° eyes-first action. Shot 2 also retained a
perceptual synthetic-softness risk.

Review Cut 007 is a separate, post-feedback execution test. It replaces the face-only gaze beat
with three performed causes: completed work, a staff exception routed through the owner, and the
owner's recognition close-up. It was not part of the blind A/B and remains an internal candidate
until the owner judges it in context.

## Independent variable

Variant A begins with generated footage and improves it through editorial diagnosis. Variant B
locks the dramatic question, shot jobs, geography, action, eyelines, and cuts before generating a
new cast, workplace, or frame.
