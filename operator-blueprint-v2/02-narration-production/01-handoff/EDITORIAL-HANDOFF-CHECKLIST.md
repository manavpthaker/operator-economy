# Editorial Handoff Checklist

Template version: proposed Step 2 v0.2.

Gate N1 accepts a complete Step 1 v1.5 package and creates the immutable spoken-text identity used
throughout Step 2. File existence or a matching word count alone is not acceptance.

## Episode and receipt identity

- Episode number and slug, or fixture ID:
- Candidate or promotion ID:
- Step 1 authority version: `operator-blueprint-v2-step1-v1.5`
- Editorial-lock path/revision/SHA-256:
- Narration-handoff path/status/SHA-256:
- Step 2 package-manifest path/SHA-256:
- Package received by/date:
- Checklist reviewer/date:

## Required Step 1 artifact verification

Record machine identities in `PACKAGE-MANIFEST.template.json`; repeat the observed result here for
human review.

| Artifact | Required | Path | Expected SHA-256 | Observed SHA-256 | Match/current |
| --- | --- | --- | --- | --- | --- |
| Editorial lock | yes | | | | |
| Narration handoff | yes | | | | |
| Locked script | yes | | | | |
| Episode Investment Thesis | yes | | | | |
| Episode beat sheet | yes | | | | |
| Editorial-voice conformity report | yes | | | | |
| Operator Canvas | yes | | | | |
| Claims map | yes | | | | |
| Narrative spine | yes | | | | |
| Episode outline | yes | | | | |
| Voice and comedy map | yes | | | | |
| Performance read-through | when named by lock | | | | |

## Reviewed live authority identities

These are reviewed dependencies, not files silently copied into the episode package.

| Authority | Reviewed path | Expected SHA-256 from Step 1 | Observed SHA-256 | Match |
| --- | --- | --- | --- | --- |
| Content OS voice | | | | |
| V2 Script Beat Research | | | | |
| V2 Voice Architecture | | | | |
| Studio speech profile | | | | |

## Deterministic spoken-text identity

- Specification: `SPOKEN-TEXT-IDENTITY-SPEC.md`
- Specification version: `oe-spoken-text-v1`
- Extractor implementation/version:
- Locked script SHA-256:
- `canonical-w.txt` path/SHA-256:
- `spoken-identity.json` path/SHA-256:
- First and last `W` IDs:
- Deterministic whitespace-token count:
- Step 1 recorded count and ordered-token SHA-256:
- Count and ordered-token SHA-256 match: yes / no
- Two clean runs are byte-identical: yes / no
- Unresolved extraction ambiguity: none / list and return to Step 1

For the AI Visibility v1.1 fixture only, the expected identity is 3,019 `W` tokens with ordered
token SHA-256 `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`.
Acoustic `alignment_parts` created later remain subordinate and cannot change this identity.

## Handoff content review

- Short public category title present: yes / no
- Exact short spoken company name present: yes / no
- One-sentence plain definition present: yes / no
- Company-level BUILD verdict present: yes / no
- Opportunity and operator acts/turns identified: yes / no
- Silent identity break or other intentional pause identified: yes / no
- Qualification register present: yes / no
- Pronunciation register present: yes / no
- Numbers, acronyms, proper nouns, negations, and qualifiers flagged: yes / no
- Performance cautions present: yes / no
- Explicitly non-verbatim passage: none / list and return to Step 1

## Rights, origin, and readiness

- Proposed narrator origin: human / synthetic / undecided
- Narrator authorization requirement identified: yes / no
- Synthetic voice or cloning involved: no / yes
- Rights/consent evidence required before N3:
- Synthetic-media disclosure expected downstream: no / yes / pending N3
- Unresolved factual blocker: no / yes
- Unresolved legal, permission, or source-integrity blocker: no / yes
- Unresolved owner decision: no / yes

## Fixture and production boundary

- Real promoted and numbered episode: yes / no
- Fixture identifier, when applicable:
- Fixture-only authorization permits N1: yes / no / not applicable
- Content OS public-fact clearance: pass / blocked / not applicable
- Visual, production, publishing, or release authority: no unless separately documented

Workflow Operations is historical and is expected to fail N1. Do not repair or upgrade its old
status inside Step 2.

## Gate N1 decision

- Package hashes all match: yes / no
- Spoken-text identity reproducible: yes / no
- Handoff status is `ready`: yes / no
- N1 gate result: pending / passed / failed / invalidated
- Workflow outcome: in_progress / returned_to_editorial / blocked
- Findings and required action:
- Narration producer/signature/date:

Step 2 does not repair or reinterpret an incomplete editorial package. A new Step 1 lock or any
required-artifact hash change invalidates this acceptance and every downstream Step 2 artifact.
