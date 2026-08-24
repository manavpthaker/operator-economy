# Blind Provider Bakeoff Scorecard

Template version: proposed Step 2 v0.3.

Complete one signed copy per scorer. The scorer must not see provider, model, voice, settings,
filename, generation order, or raw receipt until every scorecard is frozen.

## Blind review identity

- Fixture or episode ID:
- Round: short provider bakeoff
- Scorer/role:
- Scorecard revision:
- Locked script and `W` SHA-256:
- Performance-envelope path/SHA-256:
- Review-copy manifest SHA-256:
- Blind-map custodian:
- Scoring started/completed:
- Provider identity remained sealed through signature: yes / no

## Hard gates per clip

| Blind clip | Consent/provenance/tier | Exact words; no spoken tags | Names/numbers/negations/qualifications | PCM/WAV-first provenance | No watery consonants, brittle sibilance, or synthetic/codec artifact | Understandable without music/visuals | Eligible |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | pass / fail | yes / no |

A failed hard gate disqualifies that clip regardless of score. Record findings and timecodes:

-

## 100-point creative score per eligible clip

Give each dimension a whole-number rating from 1 to 5. Convert that rating into the points
available for the dimension with `(rating / 5) x allocated points`. For example, a rating of `4`
on a 25-point dimension contributes `20` points. Sum the six dimension-point values for the
`/100` total. Keep full precision while calculating and round only the final total to two decimal
places.

| Blind clip | OE identity 25 | Camera-ready energy 25 | Documented turns 20 | Natural/credible/sustainable 15 | Evidence/caveats/action/verdict distinction 10 | Editability/pickup 5 | Total 100 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| | | | | | | | |

## Signed scorer decision

- Best blind clip(s) and why:
- Unacceptable artifacts or delivery failures:
- Recommendation: advance / do_not_advance / revise
- Signature/date:

This scorecard cannot set N4A, `technical_pass`, `creative_approved`, N4B authority, narration lock,
or Step 3 authority. After signature, hash this file and record its digest in the curator
consolidation. Do not write the digest back into this file, add consolidation, or add unblinded
provider information after signature.
