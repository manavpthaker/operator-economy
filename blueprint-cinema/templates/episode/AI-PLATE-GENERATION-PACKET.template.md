# AI plate generation packet: `<asset-ticket-id>`

This packet creates a non-evidentiary environmental, metaphorical, reconstruction, or impossible-view plate. It does not authorize fake proof, fake interfaces, fake documents, factual text, or synthetic people presented as real participants.

## Control block

- Episode:
- Ticket ID:
- Sequence / shot IDs:
- Work-order ID:
- Required production state:
- Direction-bible hash:
- Shot-board hash:
- Scene-direction hash:
- Asset-ticket hash:
- Approved continuity references and hashes:
- Model / provider:
- Model version:
- Paid generation authorized: `yes/no`
- Synthetic-media disclosure owner:
- Status:

## Editorial job

- Asset role: `environment | metaphor | reconstruction | impossible_view | transition_plate`
- Viewer inference:
- Why existing reality cannot reasonably be captured or licensed:
- Exact timeline use and duration:
- Relationship to narration:
- Scene context — situation, scene form and reason, stakes or absence, emotional arc:
- Editorial intent — selected techniques, why this shot, entry/exit triggers, hold intent, simpler alternative, review question:
- Picture/audio mode: `narrated_observation | narrated_dramatization | sync_dialogue | presenter_address | natural_sound_observation | silent_graphic`
- Language carrier:
- Visible speech rule:
- Coverage grammar:
- Face function: `none | task_focus | caused_reaction | dramatic_performance | dialogue_exchange | sync_delivery | source_delivery | presenter_delivery | environmental_presence`
- What the picture carries that the audio does not:
- Mute diagnostic and reason (planned or observed; do not claim unreviewed footage passed):
- For narrated dramatization — illustrative representation, narration-carried meaning, disclosure plan, and actual-audio review check:
- Relationship to persistent objects:
- What the plate must never imply:
- Evidence prohibition:

`source_delivery` is valid only for `natural_sound_observation` with synchronized source speech; it must record that the source line disappears on mute. A natural-sound shot without `source_delivery` must not depend on a missing line. Under `narrated_observation`, visible speech and delivery-shaped face functions remain prohibited. Explicit `narrated_dramatization` permits motivated conversational behavior, reciprocal eyelines, and an answer beat without audible character lines. Use illustrative_only or prohibited speech per shot; the narrator supplies essential meaning. Do not append observation's no-conversation negatives to this mode.

## Shot and continuity

- Scene location:
- Time of day:
- Weather / atmosphere:
- Persistent subject or object IDs:
- Master/setup role: `master | setup | standalone`
- Declared master shot ID or asset-ticket ID listed on this setup, required for `setup` and otherwise `null`:
- Exact relationship to the declared master shot or listed asset ticket:
- Identity traits that must match prior plates:
- Wardrobe, prop, architecture, and material continuity:
- Subject screen direction:
- Action line:
- Camera side:
- Continuity anchors and the exact property each preserves:
- Starting composition:
- Ending composition:
- Initial image:
- Final image:
- Entry handoff:
- Exit handoff:
- Required empty or trackable regions for later graphics:
- Required clean plate:

## Camera

- Output type: `still | video | start_end_video | plate_set`
- Aspect ratio and resolution:
- Shot size:
- Camera height and angle:
- Camera position:
- Subject distance:
- Lens or field-of-view character:
- Depth of field:
- Camera movement:
- Movement start, path, speed, and settle:
- Stabilization character:
- Shutter / motion-blur character:
- Horizon and perspective rules:
- Forbidden camera behavior:

## Blocking and action

- Primary subject placement:
- Secondary subject placement:
- Foreground / midground / background:
- Eye line and gaze:
- Why any close view of a face is necessary:
- Subject movement path:
- Prop movement:
- Environmental movement:
- Starting state:
- Trigger:
- Ordered action phases:
- Consequence:
- Ending state:
- Required hold and handles:
- What stays still throughout the action:
- Motion that must not occur:
- Mode-specific speech/performance permissions and behavior that must not occur:

## Light, color, and material

- Key direction and quality:
- Fill and contrast:
- Practical sources:
- Time-of-day behavior:
- Exposure target:
- White-balance character:
- Episode palette relationship:
- Skin-tone requirement when applicable:
- Surface and material specificity:
- Texture and grain target:
- Atmospheric depth:
- Elements reserved for Resolve matching:
- Prohibited generic cinematic treatments:

## Image integrity

- Anatomical risks:
- Hands and object-interaction requirements:
- Text, logo, signage, and interface exclusions:
- Reflection and shadow requirements:
- Physics and scale requirements:
- Architecture and geography requirements:
- Period accuracy when applicable:
- Face and release implications:
- Reconstruction label requirement:
- Disclosure requirement:

## Positive prompt

Write one production-specific prompt using the approved details above. It must describe subject, environment, blocking, camera, lens character, action order, lighting, material, color, temporal behavior, continuity anchors, and clean compositing needs. Do not add unsupported story details.

`<compiled positive prompt>`

## Negative prompt

Include episode negatives plus shot-specific failure prevention.

`<compiled negative prompt>`

At minimum exclude:

- generic luxury or corporate wallpaper;
- illegible or invented text, logos, documents, interfaces, and prices;
- anatomy or hand errors;
- warped architecture, props, reflections, and shadows;
- unmotivated camera drift, speed ramps, and excessive depth of field;
- dark, melodramatic, cyberpunk, glossy-ad, or AI-demo treatment unless explicitly approved;
- fake documentary authenticity or identifiable real-person implication;
- competing focal points and crowded negative space reserved for graphics;
- word-shaped mouth movement, reciprocal conversational eyelines, question-and-answer blocking, or reaction coverage that implies an unheard line when the approved mode is `narrated_observation`;
- a face close-up without a mode-appropriate task, caused reaction, or dramatic turn.

## Generation controls

- Seed or continuity control:
- Reference-image strength:
- Character or object reference:
- Start frame:
- End frame:
- Motion strength:
- Camera control:
- Style control:
- Duration:
- Frame rate:
- Resolution:
- Variations requested:
- Maximum generation attempts:
- Stop conditions:

## Candidate record

| Candidate ID | Provider job ID | Seed/settings | Local path | Hash | Technical result | Editorial result | Continuity result | Rights/disclosure | Decision |
|---|---|---|---|---|---|---|---|---|---|
| `<id>` | `<id>` | `<settings>` | `<path>` | `<hash>` | `<result>` | `<result>` | `<result>` | `<result>` | `reject | hold | recommend` |

## Review checks

- [ ] The plate performs the ticket's exact editorial job.
- [ ] It cannot be mistaken for evidence or a verified real case.
- [ ] Subject, object, wardrobe, place, light, scale, and screen direction match approved continuity.
- [ ] Camera behavior matches the shot direction and includes required handles.
- [ ] Picture, performance, and coverage obey the declared picture/audio mode.
- [ ] The actual narration supplies essential meaning; the selected mode's mute diagnostic is recorded. Dramatization is not failed merely for conversational mouth movement.
- [ ] Each facial close-up serves a motivated task, caused reaction, or dramatic turn; important performance and pauses survive the planned edit.
- [ ] The candidate preserves the declared master/setup relationship, screen direction, continuity anchors, still elements, initial image, and final image.
- [ ] The intended graphic area is usable and uncontaminated.
- [ ] There is no invented legible text, logo, interface, document, price, or factual claim.
- [ ] Anatomy, hands, interactions, physics, architecture, reflections, and shadows survive frame-by-frame review.
- [ ] Compression, flicker, warping, temporal consistency, and resolution are acceptable.
- [ ] Synthetic and reconstruction metadata are complete.
- [ ] The local frozen select, checksum, derivatives, and manifest record exist.

## Selection and handoff

- Recommended candidate:
- Rejection reasons for alternatives:
- Approved crop / in / out:
- Clean plate:
- Matte / depth / auxiliary passes:
- Upscale or interpolation:
- Grain / denoise status:
- Source color information:
- Resolve interpretation note:
- HyperFrames use note:
- Disclosure label and timeline placement:
- Select approval:

Generation is not selection. Selection is not approval. No candidate enters HyperFrames or Resolve until its manifest record, synthetic status, local hash, and explicit select decision are complete.
