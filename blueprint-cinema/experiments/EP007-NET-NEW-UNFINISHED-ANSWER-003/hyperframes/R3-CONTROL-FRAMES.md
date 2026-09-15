# R3 moving-plate control frames

## Status

These are non-evidentiary start/end control frames used for one rejected Veo R3 moving-plate test and one user-requested Kling comparison. They do not approve production use, Step 3, or publication. The same pair is retained for the comparison to hold inputs fixed; its nonidentical page geometry remains a known risk.

| Role | Project path | SHA-256 | Dimensions | Status |
| --- | --- | --- | --- | --- |
| Start | `public/media/r3-route-start.png` | `5e13a9a45965a39d260dc7a25bd7d713c671619fa76dc5e8b384b6419bc639a7` | `1672×941` | used in Veo/Kling comparisons; retain as provenance |
| End | `public/media/r3-route-end.png` | `6becc345680fa00281e56aedb56528aa04bf5fd958fe44cc93994154a8db1ac4` | `1672×941` | used in Veo/Kling comparisons; page geometry remains a known risk |

Both files were generated with the built-in `image_gen` workflow on 2026-09-06. The tool did not expose provider, model, version, request ID, or seed; those fields remain `UNKNOWN` rather than inferred.

## Continuity references

| Path | SHA-256 | Role |
| --- | --- | --- |
| `public/media/master-wide.png` | `082f7a51fdbb9e5cf16c47e2a1cc82df74aa98f42b9899bd9c4070af6dda2608` | identity, wardrobe, location, light, object, and screen-direction reference |
| `public/media/writing-over-shoulder.png` | `624ceae83f9f21e328bdcd424fdfdc276d42f81d1db4165b6e6d9c2c5f02226a` | high three-quarter framing and prop reference only; its three generated graphite marks were explicitly excluded |

## Start-frame generation record

- Output identifier: `exec-61c0343c-b292-424e-8487-164c4e7f1e13.png`
- Source output: `$CODEX_HOME/generated_images/01a078b6-acf7-76a2-ab00-4c2cff805684/exec-61c0343c-b292-424e-8487-164c4e7f1e13.png`
- Selected project copy: `public/media/r3-route-start.png`

### Prompt

```text
Use case: identity-preserve
Asset type: non-evidentiary 16:9 first-frame control still for EP007 R3 moving-plate test
Input images: Image 1 is the identity, wardrobe, workshop, lighting, prop, and owner/buyer geography reference. Image 2 is the high three-quarter camera, pale worn maple table, blank ivory sheet, mineral-green binder, steel keys, graphite pencil, sleeve, and framing reference; its three graphite marks must NOT survive.
Primary request: Derive a photorealistic natural documentary start frame of the same workshop moment, from a high three-quarter hand-dominant view on the woman owner's side. Crop both faces completely out. The warm-canvas-sleeved owner has two anatomically natural hands visible: one hand calmly holds the plain graphite pencil above the sheet as a pointer, while the other hand is just beginning to guide exactly one small plain unprinted off-white work ticket from the work side of the sheet toward her side. The work ticket begins near the right/work side of the blank ivory sheet and is clearly separate from the sheet. It contains no printing, marks, ruled lines, logos, or texture that reads as writing.
Composition/framing: Locked-tripod 16:9 frame, practical 35–50mm documentary lens character, deep enough focus for both hands, ticket, pencil, blank page, binder edge, and keys. Warm-canvas owner sleeves enter from frame-left; the steel-blue buyer sleeve remains at frame-right but the buyer does nothing. The blank sheet remains the shared center with generous clean space for later planar tracking.
Lighting/mood: Preserve bright overcast north-window daylight, open midtones, neutral white balance, restrained contrast, real skin and fabric texture, calm routine competence.
Change only what is required to establish the start action. Preserve the same pale maple table, deep-mineral-green binder at lower-left, steel key set at lower-right, ivory sheet perspective, bright exposure, material texture, and owner/buyer screen direction.
Constraints: exactly one ticket; page completely blank and unlined; ticket completely blank and unprinted; pencil tip does not touch the page or ticket; no visible speech; no faces; no semantic content; no route mark; no writing; no diagram; no captions; no logo; no watermark.
Avoid: the three existing graphite marks, any letters or numbers, extra tickets, forms, checkboxes, labels, writing hand pose, pencil touching paper, tapping, crossing out, second gesture, dark grade, shallow-focus glamour, vignette, dramatic lighting, altered binder color, altered wardrobe, extra people, malformed hands, duplicate fingers.
```

## End-frame generation record

- Output identifier: `exec-80c5e590-2e03-4a98-8e84-d7e215a65ce0.png`
- Source output: `$CODEX_HOME/generated_images/01a078b6-acf7-76a2-ab00-4c2cff805684/exec-80c5e590-2e03-4a98-8e84-d7e215a65ce0.png`
- Selected project copy: `public/media/r3-route-end.png`

### Prompt

```text
Use case: precise-object-edit
Asset type: corrected last-frame control still for EP007 R3 moving-plate test
Input images: Image 1 is the exact edit target.
Primary request: Correct only the paper-object continuity and the final hand placement. There must be exactly TWO paper objects in the entire image: (1) one large uninterrupted blank ivory sheet in the center, with a clean continuous rectangular outline and no notch, tab, overlap, or second sheet at its upper-left edge; and (2) exactly one small plain blank rectangular work ticket, settled fully on top of the large sheet near the woman's frame-left side. Remove every other paper scrap, slip, layer, notch, and duplicate edge. Move the owner's free warm-canvas-sleeved hand only as much as needed so its fingertips rest naturally beside the single ticket after guiding it leftward. Keep the graphite-pencil hand and make the pencil tip hover approximately five millimeters above the uninterrupted blank sheet immediately beyond the ticket, without touching.
Preserve everything else as exactly as possible: locked camera and crop, 1672×941 16:9 composition, same two owner hands and identity, anatomy, warm-canvas sleeves, steel-blue buyer sleeve and arm at frame-right, pale worn maple table, deep-mineral-green binder at lower-left, steel keys at lower-right, large sheet position and perspective, bright overcast daylight, open midtones, neutral white balance, restrained contrast, shadows, and texture. Buyer remains completely still.
Constraints: exactly one large sheet plus exactly one small ticket; both completely blank and unlined; no third paper shape; no route mark; no graphite mark; no writing; no letters; no numbers; no diagram; no logo; no watermark; no face; no malformed fingers; no duplicate hand.
Avoid: notch in the main sheet, extra paper corner under the resting hand, extra ticket, overlapping duplicate sheet, pencil contact with paper, writing pose, tapping, dark grade, camera change, binder or key movement, altered wardrobe.
```

## Rejected intermediary

`exec-b0caf1c2-ed54-4282-9eec-b1edc3b201aa.png` (`a06f4704b826a6e0d3730c2b295a94bce63bcdc2b6db95131db5892f6c900eed`) was rejected because it introduced an extra paper edge/scrap and did not leave the free hand credibly settled beside the one ticket.

## Candidate review

- Side-by-side review evidence: `snapshots/r3-control-frames/start-end.jpg`, SHA-256 `58d364e7fd976a96e403051fcf008375f09b6a594859ac9d1b16470e3c7d4261`.
- The selected start and end frames contain no readable text, route mark, or generated evidence.
- Both keep faces outside frame and retain the owner-left / buyer-right geography.
- Both are dimension-matched at `1672×941`.
- Pre-generation endpoint review found exactly one ticket and one large sheet in each frame; the ticket moved work/right to owner/left; the pencil remained off the page; binder, keys, buyer, table, light, and framing appeared stable enough for one interpolation test.
- The images are not pixel-identical outside the intended moving anatomy and ticket. The video generator must keep the camera, table, binder, keys, page plane, buyer, light, and grade stable; any drift is a rejection.
- The first Veo output failed the required action and continuity: it began before the required handle, added a late corrective gesture, deformed the page boundary at frames `172–177`, and never produced the required final settle. One sample does not establish that the endpoint pair is unusable or isolate the cause.
- The endpoint pair may have contributed to the late convergence because the end-state anatomy and page geometry ask the model to reconcile more than the one ticket route. That is an inference from the observed output, not a provider-exposed diagnosis.
- Resulting video: `renders/candidates/r3-route.veo-fast.full-generated.mp4`; request ID `01a0793d-c955-77c1-9817-86db0109243a`; SHA-256 `a8525034600f2837f0e01476f6dc82726a9e2789e15c9cbd10abdab0085c6b5e`.
- Full result and evidence: `R3-MOVING-PLATE-VERIFICATION.md`.
- Veo asset disposition: rejected, preserved unmounted, no approved select. The earlier recommendation to redesign before any further test was too categorical; on 2026-09-06 the user requested another model and then said continue.
- Controlled comparison: `R3-KLING-PRO-PROMPT.md`; one `fal-ai/kling-video/v3/pro/image-to-video` request, ID `01a079bf-683a-75c2-a73b-5959ee7e18f0`, same image bytes and prompt, 8 seconds, audio off, CFG 0.5, list-priced at `$0.896`. Submitted packet SHA-256 `6f038477f8207adc854257d7fe7b5ff938187b1551d8bc56c0b0b73ad0c628ab`.
- Kling result: technically valid, cleaner paper and improved opening hold, but late pencil reposition and insufficient final settle; rejected against the current ticket. Source SHA-256 `f9023d50357b645e016d1cc54825ccd60091dff6557065a4849d7496e4631f76`; full review `R3-KLING-PRO-VERIFICATION.md`. Neither source has an approved select.
