# Blueprint Cinema Production Standard

**Status:** Canonical creative and production direction
**Effective:** August 2026

The Operator Economy is an actionable business blueprint being assembled, operated, tested, and handed to the viewer. It is not an animated deck or a conventional documentary with diagrams added between footage.

> Motion graphics are the operating model. Evidence proves it. Rendered scenes create the world. B-roll reconnects it to reality.

This standard governs production after research, script approval, and final voiceover. Content truth, voice, release gates, and publishing remain controlled by `../content-os/`.

Blueprint Cinema owns the creative decisions and production contracts. HyperFrames is the canonical designed-scene, motion-graphics, directed-animatic, and deterministic-render runtime. DaVinci Resolve is the canonical final editorial and finishing environment. See `../blueprint-cinema/TOOLCHAIN.md` for the exact ownership and handoff boundary.

## Viewer Promise

By the end of an episode, the viewer must understand the operator and customer; the value being lost, created, or recovered; the current mechanism; the counter-system; its components, costs, handoffs, and human judgment points; its failure modes; and the first concrete action to take.

If the viewer remembers only a thesis, statistic, or stack of tools, the episode has failed as a blueprint.

## Visual Model

Use this mix as a starting point, not a quota:

| Layer | Share | Job |
|---|---:|---|
| Living blueprint / system world | 60% | Assemble, operate, and stress-test the business |
| Evidence and interfaces | 20% | Prove claims and demonstrate implementation |
| Rendered scenes | 10% | Establish stakes, metaphors, impossible views, and outcomes |
| Real B-roll and archival | 10% | Restore human, physical, historical, and market reality |

Every designed beat primarily occupies one of three persistent spaces:

- **Reality world:** people, places, objects, market surfaces, and outcomes.
- **System world:** actors, inputs, workflows, handoffs, tools, money, capacity, human gates, and failures.
- **Proof bench:** source documents, interfaces, pricing, receipts, charts, and operational artifacts.

The rendered world creates interest. The blueprint creates understanding. Evidence creates trust. Real footage creates contact with reality. Never ask one layer to perform another layer's job.

## Episode Engine

Every episode must define its own mechanically honest visual engine before coverage planning:

- Operator
- Customer or subject
- Owned value
- Constraint
- Counter-system
- Outcome object
- Primary visual mechanic
- Primary motion verbs
- Reality-world visual bible

Reuse renderer primitives, not finished compositions. An engine may behave like a leak and recovery loop, queue and escalation path, assembly line, capacity system, retention orbit, routing network, toll gate, feedback loop, or automated path with human gates. Do not use a flywheel, gravity field, or compounding effect unless the business actually behaves that way.

## Direction Package

The engine states what the episode means. The direction package decides how the audience will see, feel, and understand it. Before a builder animates a scene, approve:

- an episode direction bible covering visual thesis, reality treatment, system treatment, proof treatment, typography, camera, motion, documentary footage, AI plates, sound, and negative rules;
- a whole-episode rhythm map covering energy, information density, visual mode, proof, human contact, sound, and transitions;
- style frames and one representative motion test proving the episode-specific visual language;
- a sequence treatment and static shot board with the real text and truthful placeholder geometry;
- shot-level scene directions with entry, action, consequence, settle, and handoff states;
- continuity, cognitive-load, evidence, asset, and review checks.

This is a directing layer, not another screenplay and not an open-ended image prompt. `../blueprint-cinema/references/DIRECTION-SYSTEM.md` defines the full contract; `../blueprint-cinema/references/SHOT-GRAMMAR.md` defines the reusable causal shot grammar.

## Narrative Waveform

1. **Failure or tension in motion (0–3%):** begin inside a concrete action or contradiction. Overlay title and brand on continuing motion.
2. **Current machine (3–8%):** move from reality into the operating model and expose the unresolved mechanism.
3. **Proof (8–20%):** attach evidence, examples, and parameters to the parts of the machine they validate.
4. **Counter-system (20–60%):** causally build customer, job, offer, intake, workflow, tools, human review, output, and retention.
5. **Economics (60–78%):** run revenue, costs, time, capacity, margin, ranges, and changed assumptions through the model.
6. **Stress test (78–90%):** activate breakage, exceptions, consent, approvals, fragile assumptions, and disqualifiers.
7. **Installation and agency (90–100%):** show the first move, first proof, and first repeatable loop; pull back to the completed blueprint.

These states replace automatic title/statistic/list/chapter-card sequencing. Several narration beats may unfold inside one persistent composition.

## Motion and Transition Grammar

Motion must express a business verb: capture, route, qualify, compare, assign, approve, reject, retry, escalate, hand off, price, deliver, recover, retain, measure, or compound. Every meaningful animation needs a readable before state, operation, and after state.

Preserve object permanence. Customers, tools, values, and evidence remain recognizable while the relevant state changes. Use a human camera for hands, faces, objects, and outcomes; use a system camera for relationships, flow, and capacity. Do not drift merely to keep the frame moving.

The default transition is a cut. Design a transition only when it explains a relationship: reality resolves into blueprint geometry; evidence pins to a node; a sourced value changes system behavior; the camera follows work through a handoff; a working connection fails; or the camera reveals the accumulated system. Random wipes, transition packs, repeated elastic motion, and decorative cross-dissolves are prohibited.

Text labels components and parameters; it does not reproduce narration. Use kinetic type only for a genuine thesis, reversal, or warning.

## Evidence, Footage, and Synthetic Media

Use the evidence pattern:

`source appears -> relevant element highlighted -> value extracted -> value enters system -> behavior changes -> source remains pinned`

Every footage ticket has exactly one role: `human_context`, `market_force`, `proof`, `process`, or `outcome`. Prefer original capture for proof/process, permissioned or licensed company material for market forces, specific licensed stock for human context/outcomes, and generated plates only when reality cannot reasonably be captured.

`studio/scripts/originate/source_footage.py` does the sourcing. `search` routes each ticket by role:

- **human context and outcome:** Pexels, Pixabay, Storyblocks (subscription), and public-domain archives (Internet Archive, Wikimedia Commons).
- **market force:** the public-domain archives only.
- **proof and process:** never searched.

`add` registers files downloaded by hand, with their page, rights holder and terms: company press-kit footage for market force, human context or outcome beats, and Storyblocks web downloads. They then go through the same review and `approve`.

Storyblocks candidates are previews. Only an approved select spends a subscription download.

Archive licenses are uploader-asserted. The search takes only items marked public domain from the Internet Archive, and only public domain, CC0 or CC BY from Commons. The license is still checked by a person at approval.

AI renders are never evidence. Build one coherent rendered world per episode, normally with three or four purposeful sequences rather than a clip per sentence. Generate environmental plates; composite accurate text, interfaces, prices, documents, and brand marks afterward. Record synthetic status and required upload disclosure in the manifest.

Every external asset must retain its canonical source, creator or rights holder, license and check date, download date, checksum, face/release review, in/out points, crop, focal position, timeline uses, and reconstruction/synthetic status. The edit references manifest IDs, never raw URLs or untracked downloads.

## Production Order

```text
locked script
  -> final VO and word-level transcript
  -> episode engine and persistent world
  -> full-timeline visual plan
  -> direction bible and rhythm map
  -> look development and representative motion test
  -> presenter look lock (owner gate, before any presenter generation)
  -> sequence treatments, shot boards, and scene directions
  -> whole-episode directed animatic in HyperFrames
  -> exact asset tickets, candidates, selects, and production
  -> HyperFrames graphic and scene plates
  -> Resolve conform and rough cut
  -> picture lock
  -> Resolve color, Fusion, Fairlight, captions, and online
  -> delivery validation
```

Voiceover is the timing authority. A beat is not automatically a shot. The visual plan records actual timing, narrative state, mode, action, carry, focus, approved evidence, asset requirements, audio state, and production status. The shot board and scene directions then turn each persistent sequence into exact audience frames and actions without changing the plan's meaning.

Build a directed animatic of the entire episode before expensive generation or licensing. It uses the actual VO, real text, approved composition, truthful placeholder geometry, explicit camera and motion timing, and visible asset IDs. It must prove comprehension, rhythm, continuity, shot relationships, and the persistent operating model. It is intentionally unfinished, but it cannot be vague. Asset placeholders are exact tickets, not attractive stand-ins that can be mistaken for finished work.

The final film is conformed and finished in Resolve. Resolve may refine editorial timing within approved intent, but changes to shot purpose, evidence timing, business state, object continuity, or transition meaning return to Blueprint Cinema for a direction revision. A Resolve timeline is never the only record of an approved creative change.

## Presenter Look Lock

Each episode gives the presenter a new location and outfit. The look is chosen as still images, before any presenter video is generated, and then locked. Changing it later means regenerating every presenter shot. EP009's look change after the fact cost 1,281.5 credits.

1. Generate look candidates as stills only, from the accepted likeness references. They cost cents, so explore freely here.
2. The owner picks one. Then run:
   `blueprint-cinema/bin/oe-cinema lock-look <episode_dir> --ref <still>=<hosted url> --location "..." --outfit "..." --locked-by Manav`
   This writes `presenter/LOOK-LOCK.json` with the reference hashes.
3. `oe-cinema generate` refuses any `--lane presenter` job when the lock is missing, when a locked reference file has changed, or when the job sends an image reference that is not locked.
4. Re-locking needs `--supersede "<reason>"`. The lock's history records the reason and how many presenter jobs the old look orphaned. Changing the look is allowed, but it has to be deliberate and its cost has to be on record.

Only the behavior references and the performance recipe carry over between episodes.

All paid Higgsfield and fal calls go through `oe-cinema generate`. It checks the lane's `<provider>_usd` cap in `ledger/SPEND-LEDGER.json` when one is set. It appends an intent row to `ledger/<lane>.jsonl` before submitting, and a done or failed row after, carrying the job ID, outputs and sha256. Use `--dry-run` to check the gates without spending. Neither provider reports a price for each job, so reconcile the estimates against the billing page.

## Cadence and Legibility

- Opening: meaningful change every 3–6 seconds.
- Dense proof: annotation or internal change every 3–6 seconds.
- Standard explanation: meaningful change every 5–8 seconds.
- A longer composition is valid while it is actively building or running.
- An unexplained static hold beyond 8 seconds is a warning; 16 seconds is a hard failure.
- Validate essential content at 50% scale and on a phone-sized preview.

At 1920×1080, begin around 72–108 px for headlines, 140–240 px for critical numbers, 44–60 px for explanatory labels, and 26–34 px for sources. Keep essential content within approximately 7% horizontal and 6% vertical safe margins.

## Reusable Visual Vocabulary

The production system should converge on a small, strong set of behavioral primitives:

- `BlueprintWorld`
- `SystemNode`
- `FlowConnector`
- `ActorToken`
- `EvidencePin`
- `HumanGate`
- `CostMeter`
- `FailureState`
- `CameraMove`
- `RealityPlate`

The episode data describes arrangement, state, timing, and behavior. Components must not infer finished screen designs from narration strings. Reuse the behavior and interface of these primitives, not a fixed layout, finished scene, generic dashboard, or motion-template aesthetic.

## Department Contracts

The detailed operating canon lives under `../blueprint-cinema/`:

- `PRODUCTION-TEAM.md` separates showrunning, editorial, direction, evidence, production design, art direction, information design, typography, asset, HyperFrames, Resolve, color, sound, caption, and QA decisions.
- `references/DIRECTION-SYSTEM.md` defines direction artifacts and the path from VO to buildable shot recipes.
- `references/ASSET-MEDIA-CONTRACT.md` defines ticketing, provenance, rights, candidates, selects, generated media, and local media control.
- `references/EDIT-SOUND-FINISHING.md` defines edit construction, HyperFrames plate handoff, Resolve conform, picture lock, Fusion, color, Fairlight, captions, and delivery.
- `references/REVIEW-QA.md` defines evidence-bound review gates and blocking criteria.

## Completion Test

The episode should feel like a real operating problem entered the frame, its mechanism was exposed, a better system was assembled, evidence was connected, the system was run and challenged, a human regained agency, and the viewer left with the blueprint.
