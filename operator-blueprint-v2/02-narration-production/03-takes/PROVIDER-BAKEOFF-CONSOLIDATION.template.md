# Provider Bakeoff Curator Consolidation

Template version: proposed Step 2 v0.3.

Complete only after every blind short scorecard is signed, immutable, and hashed. This record—not a
scorer's sheet—unseals provider identity and computes advancement.

## Frozen blind inputs

- Fixture or episode ID:
- Locked script and `W` SHA-256:
- Performance envelope path/SHA-256:
- Review-copy manifest path/SHA-256:
- Sealed blind-map path/SHA-256:
- Owner scorecard path/SHA-256:
- Independent-listener scorecard path/SHA-256:
- Both scorecards were signed before unsealing: yes / no
- Curator did not score: yes / no
- Unsealed at/by:

## Candidate arithmetic

Each clip score is the arithmetic mean of the matching owner and independent-listener totals.
Keep full precision through clip selection and provider-score calculation. Display clip means,
provider scores, and provider differences to two decimal places; do not round intermediate values.

| Blind clip | Provider | Passage | Generation | Owner total | Independent total | Mean clip score | Hard gates pass | Eligible select |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| | | | | | | | | |

## Provider passage selects

For each provider, select the highest-scoring hard-gate-passing generation independently for P1
and P2. A disqualified generation cannot be selected. If neither generation passes one passage,
the provider is ineligible.

| Provider | Selected P1 generation/score | Selected P2 generation/score | Provider score: mean of P1/P2 | At least 80 | Eligible |
| --- | --- | --- | ---: | --- | --- |
| ElevenLabs | | | | | |
| Hume | | | | | |

## Advancement

- Highest eligible provider:
- Leader advances to later AUTH-05: yes / no
- Runner-up score:
- Difference from leader:
- Runner-up is eligible and within 5.0 points: yes / no
- Runner-up also advances: yes / no
- If no provider reaches 80, stop recorded: yes / no / not applicable

## Operational evidence, not creative-score adjustment

| Provider | Disqualified or unselected generations | Score/output variance | Call failures | Acquisition/processing time | Cleanup | Provenance completeness |
| --- | --- | --- | --- | --- | --- | --- |
| ElevenLabs | | | | | | |
| Hume | | | | | | |

- Operational evidence was not added to or subtracted from creative scores: yes / no
- Curator findings:

## Consolidation decision

- AUTH-05 may be drafted for these provider(s):
- Full capture remains unauthorized: yes
- N4A remains unpassed: yes
- Curator signature/date:

This record cannot set `creative_approved`, select the final method, authorize N4B, or authorize
Step 3. After signature, hash this file and bind that digest in the provider-method selection. Do
not write its own digest back into this record.
