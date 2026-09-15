# Visual translation lock: [episode]

Gate: **V7 — visual translation lock and Step 4 handoff**

Process version: proposed Step 3 v0.4

Use the v0.3 frozen-artifact, consistency, audio-only, runtime, unknown-classification, and Step 4
boundary rules unchanged. Add these upstream locks and checks.

## Application authorities this depends on

| Lock | Path | SHA-256 |
|---|---|---|
| Boundary Ledger manifest | `design-system/boundary-ledger/manifest.json` | |
| Boundary Ledger semantic core | `design-system/boundary-ledger/semantic-core.json` | |
| Provisional motion binding | `design-system/boundary-ledger/bindings/motion.json` | |
| Working Model illustration language | `design-system/boundary-ledger/illustration-language.md` | |
| Locked visual-language reference manifest | `design-system/boundary-ledger/illustration/episode-006/manifest.json` | |
| Locked visual-language reference asset | `design-system/boundary-ledger/illustration/episode-006/hotel-working-model.jpg` | |
| Boundary Ledger scene contract | `design-system/boundary-ledger/scene-contracts.md` | |
| Boundary Ledger production-skill authority | `design-system/boundary-ledger/production-skills.md` | |
| OE production-skill lock | `.agents/oe-skills-lock.json` | |

## Picture/audio consistency audit

| Check | Result |
|---|---|
| Every unit has one visual-world mode and one permitted picture/audio mode | pass / fail |
| Every mode/carrier/visible-speech/mute combination matches the V1 skill lock | pass / fail |
| Every unit binds exactly one `BO-*` or `EST-*` event and the applicable state domain matches | pass / fail |
| Every used picture/audio mode has a V5a treatment | pass / fail |
| V5b reflects the plan's picture/audio distribution | pass / fail |
| V6 labels both mode axes and does not claim to prove shot behavior | pass / fail |
| Step 4 shot-level fields remain unmade | pass / fail |

Gate V7 also requires all application-authority paths and hashes to match V1. Any drift invalidates
the lock. V7 still requires named human approval and is the only Step 3 decision that authorizes
Step 4.
