# Step 0.2 acceptance set

Status: approved and frozen 2026-08-21

Template version under test: `operator-blueprint-v2-step0.2`

This file defines the behavioral controls that justified the Step 0.2 lock. Fixtures are test-only and cannot create candidates, queue rows, episodes, public claims, or editorial authority.

## Locked controls

| Control | Expected behavior | Decision artifact | SHA-256 |
|---|---|---|---|
| Step 0.1 GEO baseline | Preserve as historical evidence that an exact-precedent gate was too restrictive; not a current pass criterion | `candidate-test-2026-08-21-geo-agency/06-promotion-decision.md` | `b858e24139412675e43eb32e464fe0216a88eabb7460fbae56171fa53134fc89` |
| Step 0.2 GEO adjacent-synthesis regression | `eligible`; both reviews pass every hard gate while direct service revenue, exact search volume, and realized economics remain unproven | `candidate-test-2026-08-21-geo-agency/step0.2-retest/08-promotion-decision.md` | `4b7a616277e59dbd9fb2470412810c33252555f616d716d2527def6caae9ead1` |
| Three-way discrimination suite | Positive -> `eligible`; incomplete but coherent -> `continue research`; out-of-format company breakdown -> `archive from Operator Blueprint format` | `step0.2-proof-suite/04-RESULTS.md` | `699fb420da37d49f92bd0af3977fbddfc8b0f7f6e5f59c578b41af99ef711451` |
| Legacy EP003 full calibration | `eligible`; prior publication gives no credit; weak old economics are discarded; primary and adversarial reviews remain on the same side of 70 | `legacy-episode-calibration-2026-08-21/08-promotion-decision.md` | `410cc54df922a559ac84b3819706ac8f11691b50acdda9ec36a8ee51f6339940` |
| Final calibration recommendation | Ready for owner approval when the two reviews agree on disposition and hard gates, scores are 81 and 72 with a nine-point delta, and no rule rewrite is needed | `legacy-episode-calibration-2026-08-21/09-calibration-verdict.md` | `da75896bc87394e5d4c524f4aefe7a2094fc39031fe7779a9af9a61a40b192f1` |

## Required behaviors

Step 0.2 must continue to satisfy all of the following:

1. An exact operating precedent is useful but not mandatory.
2. A novel candidate may pass only through explicit, bounded, one-hop transfers backed by the evidence floor.
3. Novelty, funding, valuation, tool popularity, or audience attention cannot substitute for the buyer, problem, offer, delivery, economics, go-to-market path, narrative, POV, and truth gates.
4. A coherent but incomplete opportunity remains in research rather than being promoted or discarded merely for a low provisional score.
5. An out-of-format media topic cannot enter the Operator Blueprint queue without an operator business.
6. Prior publication, an existing script, or a produced video gives a candidate no validation credit.
7. Unsupported historical economics must be rejected even when the underlying business survives.
8. Modeled economics remain clearly separate from observed performance and earnings forecasts.
9. A score never waives a hard gate or creates a queue row.
10. Scores from 65 through 75 require explicit owner review; 65-69 also requires an owner override.

## Change control

- A semantic change to a rule, score weight, threshold, calibration zone, evidence class, hard gate, artifact contract, early disposition, or promotion boundary requires a new Step 0 version.
- Rerun the full acceptance set before approving that version.
- Preserve these dated controls and their decision artifacts. Do not edit them to conform to a new rule.
- If a control depends on refreshed market evidence, add a new dated fixture and explain whether the old outcome changed because the evidence changed or because the rule changed.
- Exact reviewer scores may vary. Disposition, hard-gate interpretation, evidence class, and disclosure boundaries must remain explainable; a threshold-side change requires explicit owner review and a new decision record.

## Scope boundary

Passing this acceptance set approves Step 0 behavior only. It does not approve a candidate, populate the queue, assign an episode number, open Step 1, or make later V2 stages authoritative.
