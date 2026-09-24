# Short-Round Bakeoff Consolidation

Status: template; complete only after both scorer-local records are signed, frozen, and hashed

## Bound evidence

- Fixture ID: `step2-v0.3-ai-visibility-v1.1-provider-bakeoff`
- Locked W SHA-256: `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`
- Performance-envelope path/SHA-256:
- Compiled dry-run and acquisition-receipt path/SHA-256:
- Owner signed scorecard path/SHA-256:
- Independent-listener signed scorecard path/SHA-256:
- Sealed blind-map path/SHA-256:
- Both scorecard hashes frozen before map opened: yes / no
- Map opened by/date:

## Per-candidate consolidation

A hard-gate failure by either required scorer disqualifies the clip. For each eligible clip, the
frozen clip score is the arithmetic mean of the owner total and independent-listener total.
Keep full precision through clip selection and provider-score calculation. Display clip means,
provider short scores, and provider differences to two decimal places; do not round intermediate
values.

| Blind clip | Passage | Owner gates pass | Independent gates pass | Eligible | Owner /100 | Independent /100 | Frozen mean /100 | Provider/generation after unseal |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| B01 |  | yes / no | yes / no | yes / no |  |  |  |  |
| B02 |  | yes / no | yes / no | yes / no |  |  |  |  |
| B03 |  | yes / no | yes / no | yes / no |  |  |  |  |
| B04 |  | yes / no | yes / no | yes / no |  |  |  |  |
| B05 |  | yes / no | yes / no | yes / no |  |  |  |  |
| B06 |  | yes / no | yes / no | yes / no |  |  |  |  |
| B07 |  | yes / no | yes / no | yes / no |  |  |  |  |
| B08 |  | yes / no | yes / no | yes / no |  |  |  |  |

## Provider passage selects and frozen short scores

Select each provider's highest-scoring eligible P01 candidate and highest-scoring eligible P02
candidate independently. If neither generation passes one passage, that provider is ineligible.
The provider short score is `(selected P01 mean + selected P02 mean) / 2`.

| Provider | P01 gen 1 | P01 gen 2 | Selected eligible P01 | P02 gen 1 | P02 gen 2 | Selected eligible P02 | Frozen provider short score /100 |
| --- | ---: | ---: | --- | ---: | ---: | --- | ---: |
| ElevenLabs |  |  |  |  |  |  |  |
| Hume |  |  |  |  |  |  |  |

- Only hard-gate-passing generations were selected: yes / no
- Highest passing generation selected independently for each passage: yes / no
- ElevenLabs score at least 80: yes / no
- Hume score at least 80: yes / no
- Absolute frozen score difference:
- Short-round leader:
- Leader advanced to long-form confirmation:
- Runner-up within 5.0 points and also advanced, or `none`:

## Operational evidence, not score

These facts may identify a reliability or production blocker. They may not rescue a disqualified
clip, change the frozen means, or create bonus points.

| Provider | Calls attempted / succeeded / failed | Hard-gate pass count /4 | Generation variance | Acquisition and processing time | Manual cleanup | Actual billed characters and cost | Provenance completeness | Pickup/continuity evidence |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| ElevenLabs |  |  |  |  |  |  |  |  |
| Hume |  |  |  |  |  |  |  |  |

- Error, retry, or rate-limit receipts:
- Returned container/codec differences:
- Any strong result that could not be reproduced:
- Operational reason an otherwise eligible path must stop:

## Advancement and asymmetric rule record

Long-form continuity and the several-hours-later same-word pickup are later pass/fail confirmation;
they never rescore or alter the frozen short scores.

- If neither provider reaches 80: advance neither.
- Retain ElevenLabs when it is eligible, passes confirmation, and leads Hume or is within 5.0
  points of Hume.
- Adopt Hume only when it scores at least 80, leads ElevenLabs by more than 5.0 points, and passes
  confirmation.
- If the favored provider fails confirmation or the comparison is unavailable: select neither.

- Consolidation decision:
- Custodian/signature/date:
- Frozen consolidation path/SHA-256:

This record cannot authorize long-form generation, full capture, an episode, or Step 3.
