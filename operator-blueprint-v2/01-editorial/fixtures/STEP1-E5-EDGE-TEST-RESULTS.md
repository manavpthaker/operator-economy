# Step 1 Gate E5 edge-test results

Status: negative-and-recovery calibration complete; proposed v0.5 amendments applied; Step 1 not authoritative

Test date: 2026-08-21

Test: reviewed script with plausible unsupported claims

Result: `E5_FAIL_THEN_FIXTURE_PASS_AFTER_EXACT_RESTORE`

Episode workspaces created: zero

Script lock authorized: no

Narration authorized: no

## Plain-English verdict

The claims sounded plausible. None was supported.

The test added a large annual-cost number, a majority willingness-to-pay statement, a $3,000 market-price floor, and language describing modeled sales volume as realistic. Gate E5 caught all of them even though they were written in the same calm register as the rest of the script.

The episode did not need those claims. The correct recovery was to remove them, not commission broad research merely to preserve stronger-sounding lines.

## Claims tested

| Mutation | Why it sounded useful | Why it failed | Recovery |
|---|---|---|---|
| Agencies lose more than $100,000 a year from broken onboarding | Creates financial stakes | No relevant population, cost definition, methodology, model, or approved source | removed |
| Most small agencies will pay at least $3,000 | Connects category proof to demand | Partner programs do not establish prevalence, willingness to pay, or a price floor | removed |
| $3,000 is conservative and two monthly sprints are realistic | Makes the model sound achievable | C009 permits only a modeled scenario; no market-price or acquisition evidence exists | restored to explicit assumptions |

## Hedging test

These alternatives also failed:

- `can cost up to`
- `many agencies may pay`
- `around $3,000`
- `a conservative price`
- `should be achievable`

Hedging changes certainty. It does not create evidence.

## Return-to-Step-0 behavior

The system prepared three bounded amendment questions identifying the exact proposed wording, missing evidence, required source quality, and decision if support was absent.

It did not submit them because the central argument works without the claims. If a future owner decides one is load-bearing, only that exact request may reopen; the rest of Step 0 remains locked.

Bounded request: `step1-edge-unsupported-claim-2026-08-21/05-bounded-step0-amendment-request.md`

## Identity recovery

| Script state | Words | SHA-256 | E5 result |
|---|---:|---|---|
| Frozen accepted base | 1,018 | `42b03e49d212edbb35fdb0c2a1197ea9654c06e14ad7a2638275071144a3a5c1` | pass as prior fixture candidate |
| Derived unsupported mutation | 1,052 | `f28dd3afcd291eadb5cd435d27c8ce7957edd2642981fad4414be20ae32a9a66` | fail |
| Recovered exact base | 1,018 | `42b03e49d212edbb35fdb0c2a1197ea9654c06e14ad7a2638275071144a3a5c1` | pass in fixture mode |

The recovery did not hide a rewrite. It returned to the exact prior script identity and matching performance read-through.

## Artifact identities

| Artifact | SHA-256 |
|---|---|
| Test record | `b652b0013151ac54ea22aaf13e97d16b5ab3cc127f5f0c0241a1235e3cd6b836` |
| Verified base | `6090bfafa4951c1dc387781e6e53d3a830820e398194223e04dcaf1c58bca57a` |
| Mutation record | `600cd88436eb3fec539af956b99cf274c6befcec2b641c3c74f17e3e57b166a7` |
| Claims review | `35d0fdc2dd2c21162c113a25b580b08a2d651d7651f7f74568008057330ebade` |
| E5 failure decision | `5ae3635c3e3a9d24d7e5de6fa21f81aa062160e2494b39fd94b9f21ad6377128` |
| Bounded Step 0 request | `6202c273b2ba29b748cb3f950c7142322fd644259732b2bb173de7e1a94a06f1` |
| Recovery record | `330d782c5761800f287eda965fd58df17fed702f2e8e415b309e0eceac42e550` |
| E5 retest decision | `0e9ecea1472073f8f385a206a125b06c06239036247b0352f65362f6f2dfb4ec` |

## Rule gap exposed

Proposed v0.4 prohibited new unsupported claims but did not require a claim-level diff against the previous accepted script. It also did not explicitly state that cautious adjectives and modal verbs cannot convert an unsupported claim into an admissible one.

Without those rules, a familiar topic could acquire a new magnitude, typicality, demand signal, or price interpretation during ordinary prose polishing.

## Proposed v0.5 amendments

- Added a claim-change audit to every script revision.
- Expanded mandatory claim inventory to numbers, populations, prevalence, demand, willingness to pay, market-price typicality, acquisition pace, companies, comparisons, causality, outcomes, legal meaning, and modeled economics.
- Explicitly stated that hedging does not replace provenance.
- Required unsupported nonessential claims to be removed.
- Added a bounded Step 0 amendment template for essential claims.
- Prohibited read-through, lock, narration, and downstream production while E5 is failed.

## Proposed v0.5 rule identities

| Rule or template | SHA-256 |
|---|---|
| `EDITORIAL-STANDARD.md` | `d9cc0de4ac9a535cd7cc787833580253098754312fe0b5fd925a02d89d4bf19a` |
| `STAGE-GATES.md` | `c26ba0f88728ee3f14fef43d8d33f445674ea732b9ba56810f3e0eb010a9b828` |
| `TEAM-WORKFLOW.md` | `fa5f901b4f7d4e75aeb69c44cbffa7c3761babad701cf24a971ae331180b4c4a` |
| `EDITORIAL-CONTRACT.template.md` | `9b84575e45ac29b43635597db6bdbfeddd85b79a10c670b7fd0ad9aa23b20919` |
| `OPERATOR-CANVAS.template.md` | `dc582364bfd8c9a79d8a0882a145a1f9a7680b7b1a0a19eedee535d4bb5a153b` |
| `NARRATIVE-SPINE.template.md` | `fb0b8f8a06063ee1c5634c5b0042e7139cf6c1946d93ae7cce8bde2b95857383` |
| `EPISODE-OUTLINE.template.md` | `b897580bed85bb4fca66fe6ad7ac7f80e951453b43a291f48570c66fea535c1c` |
| `CLAIMS-MAP.template.md` | `ecccccc357bf58203e922ce02611f2943bca19795e67b3a78b4ebc98a3ef54c7` |
| `STEP0-AMENDMENT-REQUEST.template.md` | `fc875be85bf4eef6c975818c39eeb212401843c3dcbf7060af8960e1be5d6469` |
| `SCRIPT-STANDARD.md` | `62364d4670f256c8c44d94a099c1e1414c771c4a4c9813b71a357ba791636d33` |
| `SCRIPT.template.md` | `b882a55a2f56eb0bd1855b3fb29d1dc74e2faa7be457ca05e7904cf51faa0cd7` |
| `EDITORIAL-LOCK.template.md` | `01e38c663b67bf8ad49457cd269cafffb362bfd444d3dad0aea4e1137403b8e5` |

## What this test proves—and does not prove

Proved: Gate E5 rejects plausible unsupported claims, refuses hedging as a substitute for evidence, produces bounded Step 0 questions, and can recover by restoring an exact accepted script identity.

Not proved: A real approved Step 0 amendment returning through invalidation, a fully isolated economics-only failure, Step 2 lexical change control, or a genuinely promoted production handoff.
