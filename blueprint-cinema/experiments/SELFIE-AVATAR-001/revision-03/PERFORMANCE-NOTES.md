# R3 home-selfie performance proposal

Date: 2026-09-12. Reviewer: `avatar_sources`.

Owner feedback supplied by the orchestrator: the voice is better but should be slightly quicker and more varied; the eyes and facial expression feel flat. This revises the performance direction without reopening the selected home setting or olive outfit.

**Recommended performance paragraph**

He is sharing a concrete story with one familiar person, visibly engaged rather than reciting. Preserve the IMAGE's appearance, not its frozen expression. Begin with attentive near-lens eyes and an easy face. As he describes the woman who has run the same business, let his eyes briefly move just beside the lens as he brings the detail to mind, with the head nearly still; reconnect before “twenty five years,” allowing a small asymmetric brow lift and a light lift through the cheeks that then relax. These changes should read at normal phone size without becoming a held smile or widened-eye pose. Deliver “It makes money” with steady eye contact and quiet, matter-of-fact emphasis, then settle naturally. Let the new audio lead small, irregular expression changes across whole thoughts. Keep the phone arm steady; avoid repetitive nods, brow pumping, theatrical concern, a fixed grin, or a blank face with only the mouth moving.

**Reference choice and tradeoff**

Use the exact olive image for appearance, room, wardrobe and framing, and the new audio for speech timing. Omitting the r2 video is a reasonable bounded test: it avoids asking the model to preserve a performance the owner finds flat. It also removes an anchor for the accepted handheld behavior and personal mannerisms, so camera/head motion or likeness may drift. This is a hypothesis, not evidence that the old reference caused the problem. Do not compensate with a long list of stronger expressions; check the new output before adding another performance reference.

The simpler alternative is retaining r2 video with an instruction to change only expression. That better protects continuity but gives competing behavioral signals. For this revision, the requested expressive change justifies the image-plus-audio test. The reference image already fixes the selected room and close selfie viewpoint; the request should explicitly retain those anchors.

**Scene contract and review**

- Form and mode: one continuous `presenter_address` selfie; face function `presenter_delivery`; visible speech synchronized to the new exact audio.
- Exact 23-word text: “A buyer is sitting across the table from a woman who has run the same business for twenty five years. It makes money.”
- Viewer effect: a person actively telling the opening story, with a small thought-to-emphasis progression. No impersonation of the buyer or woman and no acted sales outcome.
- Primary visual change: brief recollective eye movement into renewed near-lens engagement and released emphasis on the tenure detail. The setup, clothes and supporting arm stay consistent.
- Beginning/end: attentive speaking engagement into an easy settled face after the actual final word; do not manufacture a held neutral stare throughout a long tail.
- Focused playback question: do the eyes and upper face now participate in the thought at ordinary phone size, without repeated nods, a broad grin or a prolonged look-away?

Evidence inspected: r2 native/restored side-by-side frame samples at 0.5, 4.5, 8.9 and 9.5 seconds, plus the prior 12-frame native contact sheet and exact olive reference. The stills show preserved appearance and little upper-face variation in the later sampled images; they cannot establish whole-clip acting quality or whether restoration caused flatness. The owner's playback feedback supplies the current performance verdict.

Artifact pins: olive reference SHA-256 `f407e60b8f132931c70e103f761a7e336045d8244be2e7264f19a165d0715cb0`; r2 native SHA-256 `a8a2a506dff0df23ebc6d2bb3fc822f1002aeff5da9047452df5b630480faafe`; r2 restored SHA-256 `d5e4e908ad7e6a134f3d2f5fd3afb178853a71fa6ee9cb345cb5de28c9197b8e`.

This is a directing proposal only. No generation, audio edit, canonical decision-log write, acceptance change or commit was performed. The orchestrator owns the revision event and new video request.
