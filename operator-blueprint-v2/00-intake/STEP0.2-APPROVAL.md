# Step 0.2 approval and lock decision

Decision status: approved and locked

Effective date: 2026-08-21

Approved by: Manav Thaker

Template and rule version: `operator-blueprint-v2-step0.2`

## Owner decision

Step 0.2 is the canonical authority for new Operator Blueprint V2 opportunity intake, research, validation, early disposition, eligibility, and promotion into editorial development.

This approval is based on the completed Step 0.2 discrimination suite and final legacy-episode calibration. It does not approve a candidate, populate the queue, assign an episode number, open Step 1, or make the remaining Operator Blueprint V2 lifecycle authoritative.

## Locked decision model

The approved system retains these rules:

- Exact operating precedent is useful but not required.
- Evidence is classified as `verified`, `qualified model`, `hypothesis`, or `not usable` and related to the opportunity as `direct`, `adjacent`, `component`, or `context only`.
- A novel business may qualify as an `adjacent synthesis` or `frontier hypothesis` only through explicit, limited, one-hop transfers that pass the evidence floor.
- The readiness threshold is 70/100.
- Every hard gate remains non-waivable.
- Scores from 65 through 75 require explicit owner review; scores of 65-69 also require an owner override.
- Search volume is one demand signal, not a universal gate.
- A complete business Canvas does not substitute for narrative and audience pull.
- Modeled economics must show formulas, sensitivities, costs, and the disclosure `modeled scenario, not observed performance or an earnings forecast`.
- A coherent but incomplete candidate remains in research; an out-of-format idea can exit early; neither should be forced through all seven promotion artifacts.
- `Eligible` and `promoted` are distinct. No score or automated review creates a queue row.
- Candidate IDs remain descriptive until promotion. Episode numbering begins only after the approved handoff into editorial development.

## Acceptance evidence

| Evidence | Locked finding | Path | SHA-256 |
|---|---|---|---|
| Step 0.2 GEO retest | Adjacent synthesis can qualify without exact operating precedent when all evidence, Canvas, narrative, audience, POV, truth, and permission gates pass; 82/76, eligible | `fixtures/candidate-test-2026-08-21-geo-agency/step0.2-retest/08-promotion-decision.md` | `4b7a616277e59dbd9fb2470412810c33252555f616d716d2527def6caae9ead1` |
| Three-way proof suite | Correctly distinguished eligible, continue research, and archive outcomes; 3/3 expected decisions | `fixtures/step0.2-proof-suite/04-RESULTS.md` | `699fb420da37d49f92bd0af3977fbddfc8b0f7f6e5f59c578b41af99ef711451` |
| Legacy EP003 full calibration | Prior publication received no credit; unsupported historical economics were rejected; rebuilt operating premise passed both reviews; 81/72, eligible | `fixtures/legacy-episode-calibration-2026-08-21/08-promotion-decision.md` | `410cc54df922a559ac84b3819706ac8f11691b50acdda9ec36a8ee51f6339940` |
| Final lock recommendation | Both reviews agreed on disposition, gates, evidence class, and disclosure; score delta 9; no rule rewrite required | `fixtures/legacy-episode-calibration-2026-08-21/09-calibration-verdict.md` | `da75896bc87394e5d4c524f4aefe7a2094fc39031fe7779a9af9a61a40b192f1` |
| Frozen acceptance contract | Defines the expected behaviors and change-control procedure | `fixtures/ACCEPTANCE-SET.md` | `28e7343c7d1879abe7f9938ca0f8ffa915b08a50401e314794758e068a18afa7` |

## Approved authority hashes

These hashes identify the exact rule and template state approved by this decision. A later semantic edit requires a new version and decision record rather than silently changing Step 0.2.

| Authority | SHA-256 |
|---|---|
| `../README.md` | `b9955407eafbb9a8ac553d7c9ee051af3529ad873bb0e7761e35725e65fcb24b` |
| `README.md` | `845407447306392a78a703bd1936943c09b4fb9bb9be3e484d9a24853c219d9a` |
| `AUTHORITY-MAP.md` | `49556f74a5b389e61699c8ec7795e1c9240fc51181e0713c3f83cfe1317d45b0` |
| `01-candidates/CANDIDATE.template.md` | `6ceaf1093fc1419d6dadb78c648ddfa17f140b821ef15c0bb702a6adc141b931` |
| `02-research/RESEARCH-BRIEF.template.md` | `7d94263e526fc32834b3f347790d67f14d66a67f97a1208f3aeb552a4af6a18e` |
| `03-validation/EVIDENCE-STANDARD.md` | `14f6ba77a691af80e782deb93ed2014e54ade8aa58008d9ea55edf4ebffde24b` |
| `03-validation/ANALOGY-MAP.template.md` | `d4caca545debbd416c6514550057c63acb1da35dda2ddf953bb1cad6bb63a7eb` |
| `03-validation/CANVAS-FEASIBILITY-GATE.md` | `74a7d05709d4f068ef9be965082dda7ace59f0df37e1a8fc120badceb1bcb064` |
| `03-validation/EDITORIAL-POTENTIAL-GATE.md` | `ea6988fa518f41681de15033399b5f028cea34fe4379afddd151604cc50293b5` |
| `03-validation/SCORECARD.template.md` | `1f6343c47837bbe280e9a65c29de0880f5f2d3d49067ee00ec290a2e73820a70` |
| `03-validation/DISPOSITION-RECORD.template.md` | `20b988d3b6ba90d21fbde4f2061aa45b4b998f920c1b5af811b6595de781a004` |
| `04-queue/PROMOTION-RECORD.template.md` | `96bbdbfd3e3b47c13efd0481798e8a08822233837d6070487af08d2f2fc376ed` |
| `04-queue/QUEUE.md` | `540dead0aac9e27d8e5be91c28416bfff4903646f4d14a7be6426f5b307397f1` |
| `fixtures/ACCEPTANCE-SET.md` | `28e7343c7d1879abe7f9938ca0f8ffa915b08a50401e314794758e068a18afa7` |

## External authority boundary

Step 0 owns opportunity research and the promotion decision. It does not replace the Content OS control plane:

- [`content-os/facts.md`](../../../content-os/facts.md) remains authoritative for every public number, name, date, title, URL, contradiction, and do-not-state rule.
- [`content-os/voice.md`](../../../content-os/voice.md) remains authoritative for public voice.
- [`content-os/rubric.md`](../../../content-os/rubric.md) remains authoritative for public content scoring.
- [`content-os/flow.md`](../../../content-os/flow.md) and [`content-os/bin/doctor.sh`](../../../content-os/bin/doctor.sh) remain authoritative for release.

Historical references under `references/` and `05-archive/` remain reference-only. Their old scores, statuses, search estimates, production assumptions, and factual claims do not become current because Step 0 is approved.

## State at lock

- Active V2 candidates: 0
- Active V2 queue rows: 0
- V2 episode directories: 0
- Episode numbers assigned: 0
- Step 1 status: boundary only; not yet ported or authoritative
- Stages 2-7 status: boundary only; not yet ported or authoritative
- V1 `studio/` and `blueprint-cinema/`: preserved in place
- Root `AGENTS.md`: unchanged by this approval

## Change control

The following require a new Step 0 version, updated authority hashes, a full acceptance rerun, and a new owner decision:

- score weights, threshold, or calibration zone;
- evidence statuses, relationships, evidence floor, or inference limit;
- Canvas, narrative, audience, POV, truth, legal, permission, access, or guest gates;
- evidence classes or public disclosure requirements;
- artifact count, required fields, path contract, hashing, invalidation, early disposition, promotion, or numbering rules.

Editorial corrections that do not change meaning may retain Step 0.2, but the authority hash must be refreshed in a dated amendment. Frozen fixtures must not be rewritten to manufacture compatibility with a changed rule.

## Approval boundary

Owner approval recorded: yes

Step 0.2 locked: yes

Active candidate created: no

Queue populated: no

Step 1 authorized generally: no

Operator Blueprint V2 declared end-to-end canonical: no
