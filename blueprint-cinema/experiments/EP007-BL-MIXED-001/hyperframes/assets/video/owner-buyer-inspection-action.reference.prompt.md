# Owner–buyer inspection action · reference frame

## Purpose

Continuity-preserving start frame for a bounded generated-film test. This is illustrative narrative context, not evidence, and does not depict a real owner, buyer, business, or transaction.

## Generator and edit chain

OpenAI built-in image generation. The selected reference is a two-stage edit:

1. `../images/owner-buyer-context.generated.png` → `owner-buyer-inspection-action.reference-stage-1.png`
2. `owner-buyer-inspection-action.reference-stage-1.png` → `owner-buyer-inspection-action.reference.png`

## Stage 1 prompt

Use case: photorealistic-natural

Asset type: first frame for a restrained 16:9 documentary image-to-video shot

Primary request: Edit the supplied scene so the buyer is unmistakably inspecting the business rather than merely listening. Preserve the same woman owner, same male buyer, their identities, apparent ages, clothing, workshop office, worn wooden table, lighting, and natural documentary realism. Change only the buyer's attention and the paper interaction: he looks down with focused concentration and holds the existing black pencil naturally in his right hand, the pencil tip touching one checkbox on an open diligence worksheet. The page contains only non-readable horizontal lines, a few simple boxes, and one small process diagram; no legible words, numbers, signatures, prices, logos, or confidential information. The woman remains composed and capable, watching calmly from across the table.

Composition/framing: cinematic medium-wide table-level 16:9 frame, 50mm documentary lens, the buyer's hand and worksheet clearly visible in the lower-right foreground while both people remain visible; horizontal table edge remains clear across the lower third for the later match cut.

Lighting/mood: soft late-afternoon window light, quiet observational documentary, natural skin and cloth texture, subtle shallow depth of field, restrained rather than dramatic.

Constraints: keep exactly two people; keep both people on their own sides of the table; believable anatomy and hand-to-pencil contact; no visible speech; no staged advertising polish.

Avoid: handshake, reaching across the table, contract signing, sale, agreement, celebration, confused or incompetent owner, dramatic reaction, third person, extra fingers, distorted hands, readable text, watermark, caption, logo, slow-motion aesthetic.

## Stage 2 refinement prompt

Use case: precise-object-edit

Asset type: first frame for a restrained 16:9 documentary image-to-video shot

Primary request: Change only the buyer's right-hand and worksheet interaction. Move his pencil tip so it is physically touching the second empty square checkbox in the existing left-hand checkbox column, poised to make one small check mark. Place one index finger lightly along that same horizontal row as if tracking it. Keep the worksheet abstract and non-confidential: blank lines, simple boxes, and the existing tiny process diagram only.

Invariants: preserve the exact same two people, faces, apparent ages, expressions, body positions, clothing, workshop office, furniture, cup, camera framing, table, natural late-afternoon lighting, color, texture, and documentary realism. Keep the woman calm, competent, and unchanged. Keep exactly two people and believable hand anatomy.

Avoid: moving the pencil to a signature line; signing; readable words or numbers; logos; contract cues; sale cues; handshake; reaching across the table; extra fingers; warped paper; captions; watermark; any other change.

## Intermediate generator output

`/Users/brownmanbrain/.codex/generated_images/01a05efd-fd21-78d0-98a4-9ad04ce96df2/exec-7f135dc4-6d30-4c43-9f3a-949159129fd4.png`

## Selected generator output

`/Users/brownmanbrain/.codex/generated_images/01a05efd-fd21-78d0-98a4-9ad04ce96df2/exec-3c7b277d-463b-47e2-bb59-5440eec7222c.png`
