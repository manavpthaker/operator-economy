# EP007 callback in context — revision 2

Status: **rendered and independently checked for user review. This is not V4, a Step 4
authorization, a production select, a gate pass, or publication approval.**

## What this test shows

The 37.9-second passage now reads as one causal callback:

1. The buyer asks what happens if the owner is gone. The wide holds the whole question; the close
   catches her attempted answer and stop.
2. The rough Boundary Ledger model translates that pause into the business-versus-job mechanism.
   One short oxide overtrace marks the active owner-dependency path.
3. The same table returns later. The binder is present, one divider turns, the buyer settles into a
   read, and the final face cut lands on “He can read it. He can check it.”

There are no captions, claim IDs, source labels, title cards, music, effects, slow motion, synthetic
camera moves, or explanatory film overlays. Generated people and paperwork are illustrative
context, never evidence.

## Review artifact

- Film: `../hyperframes/renders/EP007-BL-CALLBACK-IN-CONTEXT-001-r2.mp4`
- SHA-256: `0dc991b4ec87a3cfdfd8f84b6fd2c05b89697aabe893f698a6e83a0e9d7fa74d`
- Size: 37,217,874 bytes
- Picture: H.264 High, 1920×1080, progressive BT.709, constant 24 fps
- Duration: 910 frames / 37.916667 seconds
- Sound: AAC-LC stereo, 48 kHz, −16.2 LUFS integrated, −3.7 dBTP

The narration is copied from exact ranges `14.750–27.000`, `255.400–267.650`, and
`1047.360–1060.760` of the locked master. It was not regenerated or retimed.

## Repairs from revision 1

- Removed the competence insert from the question so the geography and question remain continuous.
- Enlarged and darkened the rough model for phone viewing.
- Replaced the model's long terminal freeze with broken oxide dependency strokes; only a four-frame
  terminal hold remains.
- Replaced the pen-heavy binder wide with a clean no-pen version.
- Entered the OTS after its failed binder-lift opening and retained one divider turn only.
- Added a real source-angle cut to the buyer's reading face; no digital punch-in animation is used.

## Verification result

HyperFrames 0.8.29 check: **pass**.

- lint: 0 errors, 0 warnings
- runtime: 0 errors, 0 warnings
- layout: 0 issues across 9 samples
- motion: 0 errors, 0 warnings

Independent encoded-media check: **pass for review**.

- strict video and audio decode passed
- 910 continuous frame timestamps at exactly 24 fps
- no black frames
- no frozen generated-film passage
- audio packets are continuous and both narration seams are below click-scale discontinuity
- all six source windows match the declared frame ranges
- all five picture seams contain valid images and preserve usable continuity at normal speed

Independent story check: **pass for user review**. The question/stop, causal model, and later
inspectable answer are legible with narration. The two ending cuts read as motivated coverage rather
than a digital zoom. At 360-pixel phone width the object/action shapes remain clear; the tiny
handwritten labels are marginal, so they remain supporting rather than load-bearing.

## Known limitations

- The MP4 embeds `hyperframes_version=0.0.0-dev` although the package and render command pin
  `0.8.29`. The external manifest records the real tool pin. Fix the embedded tag before an
  authoritative render.
- The rough source has sparse keyframes. HyperFrames warned about them but extracted all 910
  intended output frames; the encoded film is intact.
- Minor generated-human tells remain. Human review, not machine QA, decides whether they are
  acceptable in the larger episode.
- No approved Bergen live or avatar plate exists. The optional return at master
  `263.960–267.650` remains intentionally unfilled.

Exact source windows, hashes, generation records, rejected ranges, and composition hashes are in
`../render-manifest.r2.json`.

## Boundary

No approval was inferred, no gate changed status, nothing was committed, V4 was not advanced, and
no asset was selected for production.
