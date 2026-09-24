# Generation prompts — revision C continuity and future motion

## Latest scoped development: c03 narration-context edit

After the two-model comparison, the owner chose Kling and requested an edit relevant to the narration. One additional start-only Kling request produced c03. R3-KLING-RELEVANT-PROMPT.md and R3-KLING-RELEVANT-VERIFICATION.md record it; R3-RELEVANT-EDIT.md explains the changed job. The 17-second context review lives in reviews/r3-relevant-edit and does not change Revision C's composition. c03 is conditional editorial material, not a strict prompt-conformance pass: extra pencil gestures remain, and a constant review crop excludes an invented paper fragment at the right edge. No further paid requests were made.

The sections below preserve Revision C's original two-candidate route experiment; they do not describe the alternate c03 gesture edit.

## Status and use

Revision C currently uses generated still animatic plates inherited from revision B. It does **not** mount generated live-action video. Two R3 candidates, Veo Fast and Kling Pro, exist under the ignored `renders/candidates/` path. Both are rejected against the current ticket and remain unmounted. The exact historical prompts for inherited stills remain bound to their hashes in `SOURCE-MANIFEST.json`.

Two new `1672×941` R3 start/end control-frame candidates now exist at `public/media/r3-route-start.png` and `public/media/r3-route-end.png`. Their exact prompts, hashes, source-output identifiers, and one rejected intermediary are recorded in `R3-CONTROL-FRAMES.md`. They are non-evidentiary candidate controls, not selected footage or approval of a moving plate.

The prompts below are the revised plan for replacement stills or moving plates. R1 and R2 have not been executed. R3 was executed once with Veo and once with Kling; `R3-MOVING-PLATE-VERIFICATION.md` and `R3-KLING-PRO-VERIFICATION.md` record the results. Their purpose is narrower than revision B’s: generate a credible observable action against a blank page, then let post add one tracked nonlinguistic route mark before the cut and all exact writing, arithmetic, and explanatory geometry after it.

| Provenance field | Current value |
| --- | --- |
| Provider | `fal.ai` for both rejected R3 candidates; R1/R2 remain `UNKNOWN` |
| Model | `fal-ai/veo3.1/fast/first-last-frame-to-video` and `fal-ai/kling-video/v3/pro/image-to-video`; R1/R2 remain `UNKNOWN` |
| Version | `UNKNOWN`; provider response did not expose one |
| Request ID | Veo: `01a0793d-c955-77c1-9817-86db0109243a`; Kling: `01a079bf-683a-75c2-a73b-5959ee7e18f0` |
| Seed | Veo: requested `700703`; Kling: not exposed or sent |

Replace `UNKNOWN` only when the generation tool returns verifiable metadata. Do not infer any field from appearance, filename, application context, or model availability.

The flattened provider-ready packet is `R3-MOVING-PLATE-PROMPT.md`. On 2026-09-06 the owner authorized and the production run executed exactly one Veo 3.1 Fast request, list-priced at $0.80, at 8 seconds, 1080p, 16:9, and audio off. The technically valid output was rejected for a missing pre-action handle, a late second correction, no clean final settle, and page-plane deformation at frames 172–177. It remains an isolated 24 fps rejection record; generation authorization did not authorize integration, another attempt, or a 24-to-30 fps treatment.

The owner then requested another model and said continue. `R3-KLING-PRO-PROMPT.md` produced one Kling v3 Pro comparison using the identical image bytes, positive prompt, negative prompt, eight-second request, and audio-off setting; CFG was the native default 0.5. List price was $0.896. The output has a better opening hold and cleaner paper than the Veo take, but a late pencil correction still prevents the required 1.5-second final settle. It is rejected against the current ticket. The native source is 1916×1080, 24 fps, 193 frames, 8.041667 seconds. See `R3-KLING-PRO-VERIFICATION.md` for full evidence and the side-by-side review.

## Shared continuity prompt

```text
Use case: photorealistic-natural
Asset type: 16:9 narration-led documentary continuity plate for The Operator Economy
Primary request: Naturalistic editorial-documentary scene inside an established, profitable, owner-operated workshop on a bright overcast weekday morning.
Scene/backdrop: broad north-window daylight plus soft practical fill; a functioning workshop with one quiet purposeful employee in deep background.
Subject: Experienced woman owner, 55–65, visibly comfortable and at home here, faded warm-canvas work shirt, relaxed shoulders, open brow, calm competent attention. Male inspecting party, 45–60, soft steel-blue or gray overshirt, no suit, open nonjudgmental posture.
Composition/framing: They sit at adjacent sides of one corner of a pale worn maple worktable, both oriented toward the work rather than confronting each other. Natural 35–50mm documentary lens, f/5.6, eye-level or practical table height. Owner frame-left, inspecting party frame-right.
Lighting/mood: open midtones, readable shadow detail, neutral white balance, restrained contrast. Viewer feeling: respected competence and practical curiosity, not crisis.
Color palette/materials: closed deep-mineral-green binder, one warm ivory unlined sheet, plain graphite pencil, small steel key set, one plain unprinted work ticket. Oxide/red absent.
Constraints: no visible speech; no readable document contents; the ivory sheet and ticket remain blank; ordinary working business; enough depth to see a functioning environment.
Avoid: staged smile, stern stare, random gaze, anxiety, shame, defeat, direct face-off, clasped interrogation posture, black-dominant wardrobe, black binder, dark walnut filling frame, shallow-focus glamour, anamorphic look, vignette, film-grain effect, teal-orange grade, underexposure, chiaroscuro, tungsten-only light, prestige-drama mood, captions, logos, watermark, writing, figures, diagrams, lines, checkboxes, printed forms.
```

## Shared moving-plate envelope

```text
Natural real-time motion, 30 fps, normal shutter. Locked tripod. One-second pre-action handle, one authored foreground action, then a clean settle. No slow motion, dolly, push-in, pan, tilt, rack focus, handheld float, idle looping, dialogue, lip motion, random head turn, reciprocal reaction, or invented page content. Do not attempt the transition into graphics; deliver a clean blank-page endpoint for deterministic post work.
```

## Moving shot prompts

### R1 — ordinary review

```text
Wide three-quarter two-shot at the table corner with generous breathing room. Buyer turns one already-reviewed page once; both people follow that same page with task-focused eyes. Owner handles familiar objects with easy confidence. One low-salience employee may cross once in deep background. No one speaks. End with both people settled on the work.
```

### R2 — financial evidence to operating question

```text
Medium three-quarter table view. Buyer slides the closed deep-mineral-green binder aside once, revealing the warm blank sheet as the shared center. Owner's eyes follow the revealed sheet because it moved; no reciprocal eyeline. The sheet remains entirely blank and unlined. End settled. No theatrics, pointing, tapping, or dialogue.
```

### R3 — one work route and arrested pencil

```text
High three-quarter hand-dominant view from the owner side; crop both faces completely out. Begin with one plain unprinted work ticket near the work side of the blank ivory sheet. The owner calmly guides that single ticket from the work side back to her side while using the graphite pencil only as a pointer that follows the route. The ticket settles near her hand. The pencil stops five millimeters above the still-blank sheet and holds. The movement is familiar and practical, as if demonstrating how an ordinary item comes back to her for action. No writing, marks, labels, numbers, diagram, tapping, crossing out, extra tickets, or second gesture. The page must remain blank through the final hold.
```

## Still replacement prompt for the R3 endpoint

Use only if the animatic needs a clean still before moving footage exists.

```text
Use the approved continuity master as identity, wardrobe, location, lighting, geography, and prop reference. Create the settled endpoint of R3: high three-quarter hand-dominant view from the owner's side, both faces cropped out, one plain unprinted work ticket resting near her hand, graphite pencil tip arrested five millimeters above a completely blank warm ivory sheet. Preserve the deep-mineral binder edge, steel keys, pale maple table, bright even daylight, and practical documentary texture. No writing, marks, lines, numbers, diagrams, form printing, captions, logos, watermark, dark grade, or dramatic lighting.
```

## Post-only page-plane transition

This is an editorial/compositing operation, not a generation prompt:

1. Planar-track the blank R3 source page and composite one rough, nonlinguistic `ticket → owner checkpoint → unfinished leg` mark beneath the hand. This is a transition carrier, not the arithmetic itself.
2. Align the ticket and pencil action to that route; hold the stopped endpoint until the spoken word “stops” finishes at `00:26.80`.
3. From `00:26.80–00:27.92`, make one finite Z-forward approach into the page while preserving the route mark.
4. At `00:27.92`, replace the physical page with Boundary Ledger paper on one frame, preserving the mark, center, scale, and Z-forward velocity.
5. Decelerate and settle the incoming paper, then expand that same mark into the explicit owner-absence equation and its three explanatory conditions.
6. Typeset and animate all exact words only after the cut. Do not ask a video or image model to render them.

## Authored post content

The following content belongs only in the controlled Working Model:

```text
BUSINESS AS IT RUNS TODAY
− OWNER FOR 30 DAYS
= ?

UNDOCUMENTED PROCESS
OWNER-HELD RELATIONSHIPS
RECORDS A BUYER CANNOT VERIFY
```

These are not prompts for generated page text. Institutional language remains typeset; rough pencil objects and dependency routes are authored around it according to Boundary Ledger.

## Rejection conditions

Reject any result that introduces visible speech, lip movement, reciprocal reaction, random gaze, extra foreground actions, fabricated readable page content, a pre-drawn route, extra tickets, changed prop colors, a confrontational face-off, crisis-coded exposure, slow motion, camera drift, unrequested camera movement, or continuity drift. Reject any R3 result whose page is not blank at the endpoint.

A visually impressive result that breaks the picture job is still a failed plate. Nothing in this prompt record approves a generated plate, provider, model, actor identity, Step 3 gate, or publication.
