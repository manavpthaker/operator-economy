# Boundary Ledger cross-media authority

Status: canonical semantic authority, version 2.0.0. Individual medium bindings retain their own
implementation and verification status.

## The system

Boundary Ledger is not a palette. It assigns durable meaning to a small set of roles, then binds
those roles differently in color, motion, sound, type, space, and material.

> **The surface stays composed. The model stays provisional.**

The sentence changes by medium without changing its meaning:

- **Web and print:** The page stays composed. The model stays rough.
- **Motion:** The frame establishes a stable world. Only the accountable change moves.
- **Audio-first:** The voice sets the clock. Sound and motion mark the argument, not the beat.

“Composed” means controlled hierarchy, one focal point, and a readable consequence. It does not mean
low energy. A cold open can begin mid-failure, mid-handoff, or mid-reroute. The drama must come from
the business operation—not camera shake, glow, frantic cuts, or decorative scribbling.

## Authority stack

| Layer | Owns | Does not own |
| --- | --- | --- |
| Content OS | Claims, evidence, voice, editorial state, release | Visual treatment or animation implementation |
| Boundary Ledger | Cross-media identity and semantic expression rules | Episode argument, runtime, final edit, or publication |
| Step 3 visual translation | Episode-specific world, direction, rhythm, and selected causal operations derived from Boundary Ledger | New brand semantics or medium bindings |
| Blueprint Cinema | Scene purpose, causal shot grammar, continuity, evidence timing, and application of the episode direction | Replacement brand semantics |
| HyperFrames | Deterministic designed-scene, motion-graphic, caption, and audio-linked implementation | Creative authority or editorial truth |
| Resolve | Conform, edit, color, mix, captions, online, and delivery | Undocumented redesign |

The design system is runtime-neutral. OE’s production toolchain may specify a runtime without moving
creative authority into that runtime.

## Semantic roles

The normative definitions live in [`semantic-core.json`](./semantic-core.json). The short form is:

| Role | Meaning |
| --- | --- |
| `humanContext` | People, place, possibility, and unresolved work |
| `accountableEvidence` | Sourced claims, dates, status, and institutional records |
| `activeCommitment` | One commitment, exception, correction, or owned thesis path |
| `externalDependency` | Rented capability, dependency, and the current route |
| `verifiedStatus` | A state that has actually been checked |
| `actualRisk` | A sourced contradiction, failed condition, or material negative exception |

Color, motion, and sound bindings live in [`bindings/`](./bindings/). A binding can change without
redefining the semantic role.

### Rev D research crosswalk

Rev D independently found partial expressions of three roles. They survive as documented research
aliases, not as a second vocabulary or canonical operation IDs:

| Boundary Ledger role | Color expression | Rev D motion research | Rev D sound research | Canonical treatment now |
| --- | --- | --- | --- | --- |
| `humanContext` | Warm ledger paper | — | `motif.human` | Establish or settle the human world; room tone, tactile contact, or an imperfect close motif |
| `externalDependency` | Perimeter steel | `motion.gravity` | `motif.constraint` | Trace or route the current dependency; restrained mechanical current or descending constraint phrase |
| `activeCommitment` | Core oxide | `motion.activate`, `motion.reverse` | `motif.counter` | Interrupt, correct, or return along one owned path; one contact event or answering phrase |
| `accountableEvidence` | Deep mineral | — | — | Pin and hold sourced evidence; usually silence |
| `verifiedStatus` | Sage | — | — | Resolve once only after verification; normally silence |
| `actualRisk` | Risk | — | — | Interrupt the actual failed condition once; never alarm theater |

This crosswalk preserves the useful discovery while preventing the old names from competing with
the fixed operations in the semantic core.

## Invariant classification

### Universal

- One primary focal point and one active commitment at a time.
- Roughness remains in the Working Model layer. Captions, evidence, metadata, and controls stay typeset.
- Evidence stays attributable and visually distinct from estimates.
- Motion represents causality or state change, then settles.
- Sound marks a meaningful event; it does not sonify every color, word, or beat.
- A current dependency is represented fairly before an operator-controlled alternative appears.
- New aspect ratios preserve relationship equivalence through recomposition, not cropping.
- Generated imagery may establish a world but cannot become documentary evidence.
- A specimen, lock, or render does not imply production, editorial, or publication approval.

### Surface-specific

- `16px` docket attachment, `24px` mobile gutter, the 3:2 static master, `object-fit: contain`, DOM
  order, keyboard focus, and browser reduced-motion behavior belong to the web binding.
- Frame rate, title-safe margins, line-weight survival, codec, color management, loudness, and social
  UI collision zones belong to motion, audio, and distribution bindings.
- Documentary footage is permitted in Blueprint Cinema’s Reality World. Photography cannot replace
  the signature Working Model on static episode-identity surfaces.

### Requires translation and proof

- Authored rough strokes over time without vector-perfect draw-ons or faux wobble.
- Oxide-path activation, evidence pinning, and the docket’s temporal forms.
- Purpose-built 16:9, 9:16, and 1:1 Working Model compositions.
- Caption rail versus scarce kinetic thesis type.
- Actual-audio utterance traces and semantic sound events.
- Encoded-video, phone-scale, and final-mix behavior.

The current specifications describe these translations. They become verified implementation only
after their stated specimens and QA pass.

## Rev C and Rev D disposition

### Rev C

Rev C is **retired as forward design authority**. It remains a frozen compatibility implementation
for consumers that still load its root tokens, components, grid, or `studio/config/brand.json`.
Those consumers migrate individually; compatibility does not grant Rev C new-work authority.

### Rev D

Rev D is **retired as an active design-system direction** and retained as narrative research. Its
useful inputs survive: human stakes, a real constraint, reversal from dependency to control,
operating-model expansion, agency, and structural use of silence. Its cobalt/gold semantics,
sinkhole imagery, breathing photos, glow, orbit, generic node builds, and Remotion promotion target
do not survive.

The unresolved restraint conflict is settled here: Boundary Ledger may dramatize a clear operation.
The composition remains controlled while the business state changes. It does not inherit Rev D’s
decorative energy devices.

## Migration blockers by surface

| Surface | Authority now | Implementation status | Retirement blocker |
| --- | --- | --- | --- |
| Reference web specimen | Boundary Ledger | Verified reference | Production site has not migrated |
| Static episode identity | Boundary Ledger | One locked hospitality model | Two non-hospitality proofs are still required |
| Long-form designed scenes | Boundary Ledger + Blueprint Cinema | Specified | Needs a representative Boundary motion test and style frames |
| Motion graphics | Boundary Ledger | Specified | Needs encoded primitive and transition proofs |
| Audio-led clips | Boundary Ledger | Browser proof in this package | Needs reviewed 9:16 and 1:1 encoded deliverables and final audio QA |
| Existing site/video/newsletter/PDF | Rev C compatibility implementation | Unmigrated | Each consumer must be ported and verified |
| Rev D prototype and derived consumers | Historical research | Retired as authority, still implemented in places | Migrate the Rev-D-derived score, opening, sting, and route behavior still referenced by studio configuration and scripts; preserve source history |

“Migration required” is not a permanent status. A surface leaves the table only after the named
consumer is changed, inspected in its final runtime or encoded output, and its compatibility path is
removed or explicitly retained for a dated reason.

## Step 3 dependency

Step 3 derives its semantic motion vocabulary from [`semantic-core.json`](./semantic-core.json) and
[`bindings/motion.json`](./bindings/motion.json). It may choose and apply episode-specific operations,
but it may not invent replacement meanings for gravity, dependency, evidence, commitment, risk, or
resolution. Blueprint Cinema remains the causal directing reference; Boundary Ledger owns the
cross-media meaning those directions express.
