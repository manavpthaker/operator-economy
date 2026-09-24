# Generated-film attempt log

No attempt below is evidence. The output is illustrative narrative context only.

## 2026-09-03 · image-to-video reference attempt

- Model: `bytedance/seedance-2.5/image-to-video`
- Result: rejected before generation with a provider likeness/privacy validation error.
- Output: none.

## 2026-09-03 · direct text-to-video attempt

- Model: `bytedance/seedance-2.5/text-to-video`
- Requested: 8 seconds, 720p, 16:9, audio off.
- Result: the direct synchronous connection timed out before returning headers.
- Output: unknown; no recoverable request ID or video URL was returned.
- Resolution: subsequent attempts use the provider's queued endpoint and persist the request ID immediately.

## 2026-09-03 · queued Seedance text-to-video attempt

- Model: `bytedance/seedance-2.5/text-to-video`
- Request ID: `01a0697e-d9c4-7583-8dd4-4b56cf73627f`
- Result: generation completed, but the provider rejected its own output during copyright review.
- Output: none delivered.

## 2026-09-03 · LTX text-to-video proof

- Model: `fal-ai/ltx-2.3-22b/text-to-video`
- Request ID: `01a06982-20e8-7772-8b57-8afa2068494c`
- Result: technically valid 8.04-second moving clip; rejected editorially because it introduced a third person and failed the owner/buyer casting.
- Disposition: preserved under `assets/video/rejected/`; never used in the composition.

## 2026-09-03 · LTX image-to-video full proof

- Model: `fal-ai/ltx-2.3-22b/image-to-video`
- Request ID: `01a06985-6c44-7493-af5d-e86f286f516c`
- Result: preserved the owner and buyer for the usable opening but introduced a third person and a handshake in the generated tail.
- Disposition: full generation and provenance preserved under `assets/video/source/`. The composition uses a separately encoded 0.00–4.00-second excerpt at native 24 fps and 1× speed; the third person and reach never enter the used asset.

## 2026-09-03 · LTX image-to-video inspection insert

- Model: `fal-ai/ltx-2.3-22b/image-to-video`
- Request ID: `01a06989-ef9d-7902-b155-8bec1904bedd`
- Result: technically and editorially usable 5.04-second insert. Two people remain separated; no new person, sale, handshake, contract, price, or outcome appears.
- Edit use: the separately encoded 0.00–3.74-second excerpt is used at native 24 fps and 1× speed. The later arm extension is excluded. The final rough table-edge trace is authored in HyperFrames, not generated into the clip.
- Creative assessment: technically usable as human context, but still reads more as a serious consultation than an unmistakable inspection. The buyer does not visibly read, write, or turn a page, so this remains a test plate rather than a locked production shot.

## 2026-09-04 · LTX checklist-inspection replacement

- Model: `fal-ai/ltx-2.3-22b/image-to-video`
- Request ID: `01a06cb6-7044-7022-a113-d193b615ddb0`
- Seed: `1597657617`
- Reference: continuity-preserving OpenAI image edit with the same owner, buyer, workshop, wardrobe, and light; the buyer begins with a pencil over an unlabeled operating checklist.
- Reference chain: original context still → `owner-buyer-inspection-action.reference-stage-1.png` (`0ae4c757…`) → selected `owner-buyer-inspection-action.reference.png` (`fad0a104…`). Both exact edit prompts are preserved in `owner-buyer-inspection-action.reference.prompt.md` (`99a790c2…`).
- Generation records: video prompt `fbd63c0e…`; full source `324761c1…`; provider response `2ad9a37a…`.
- Result: source frames 0–82 preserve both people and make the buyer's inspection legible through a short mark, a row scan, and a look back to the owner. The locked camera avoids another synthetic pan or slow-motion cue.
- Editorial exclusion: generated frames 83–120 are rejected because an unrelated page with synthetic text and a figure begins entering from frame right. They are retained only in the full source and never appear in the selected clip.
- Edit use: source frames 0–82 play at native 24 fps, followed by a seven-frame hold on frame 82 to complete the existing 3.74-second timeline window. No interpolation or speed change is used. The authored pencil trace begins during that 0.29-second settle.
- Selection record: `owner-buyer-context-shot-02-inspection-r2.selection.json` (`1edf24f5…`) binds the exact transform and `inspection-r2` output (`d5b0e31e…`).
- Rejected edit: v008 used frames 0–85; encoded review found the synthetic page edge at master 25.625–25.875 seconds, so that edit was not retained as the clean test.
- Disposition: the corrected `inspection-r2` edit is selected for the bounded v009 test render only. It is not production-approved and does not depict evidence or a real transaction.

## 2026-09-04 · LTX owner close-up cut-in

- Model: `fal-ai/ltx-2.3-22b/image-to-video`
- Request ID: `01a06ec5-3120-7332-bd43-ece12a1ed6fa`
- Seed: `1056257326`
- Reference: OpenAI continuity edit of the original owner–buyer context still into a dedicated
  owner-only medium close-up. It preserves the same woman, apparent age, loose bun, hoop earrings,
  teal work shirt, workshop, screen-right eyeline, and natural light.
- Reference records: selected still `0ecd1c0…`; exact reference prompt `de336acd…`; source continuity
  still `a34a8751…`.
- Generation records: video prompt `88650706…`; untouched 121-frame source `dc466f41…`; provider
  response `5e46db0d…`.
- Result: the camera remains locked and the owner stays silent, capable, and reflective. Source
  frames 48–82 begin and end open-eyed and contain one complete restrained blink near the center.
  No other person, readable text, transaction cue, dramatic reaction, or anatomy drift appears in
  the selected window.
- Editorial selection: source frames 48–82 inclusive, equivalent to `[2.000000, 3.458333)` seconds.
  Frames 0–47 and 83–120 remain in the full source but are excluded from this edit. No endpoint hold,
  interpolation, or speed change is used.
- Edit use: `owner-closeup.selected.mp4` (`33d0b558…`) supplies a 1.44-second timeline window at
  master 20.72–22.16, native 24 fps and 1×. The exact transform and contact-sheet binding live in
  `owner-closeup.selection.json` (`8e034f1a…`).
- Disposition: selected for the bounded v010 comparison only. It is generated narrative context,
  not evidence, a real owner, a production approval, or a gate pass.

## 2026-09-04 · Narration-directed owner selection

- Directing test: the shared shot establishes scrutiny; the owner close-up holds the human
  consequence; the checklist shot makes the operating test physical. The cut points are derived
  from the locked narration rather than added for visual variety.
- Editorial selection: source frames 42–98 inclusive, equivalent to `[1.750000, 4.125000)`
  seconds. The 57-frame window begins and ends open-eyed, includes one restrained blink, and
  preserves the locked camera, screen-right eyeline, competent expression, wardrobe, and room.
- Edit use: `owner-closeup.directed.mp4` (`5bc8d577…`) supplies a 2.36-second timeline window at
  master 20.72–23.08, native 24 fps and 1×. There is no endpoint hold, interpolation, speed change,
  or post-production camera move.
- Selection record: `owner-closeup.directed.selection.json` (`050e75e1…`) binds the exact source
  range, transform, output, timeline range, and contact sheet (`bff1b7fe…`).
- Inspection return: the existing `inspection-r2` asset begins eight frames into its selected
  output at master 23.08. The mounted 2.82-second interval retains the mark, row scan, and return
  gaze while ending before the asset's seven-frame endpoint hold.
- Rejected additions: no buyer-face close-up and no empty-chair cutaway. Neither adds business
  information; both would manufacture drama beyond the narration.
- Disposition: mounted only in the bounded v011 directing comparison. It remains generated human
  context, not evidence, a real owner, a production approval, or a gate pass.
