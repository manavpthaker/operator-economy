# Visual translation input lock: [episode]

Gate: **V1 — input lock**

Process version: proposed Step 3 v0.4

Use the v0.3 thirteen-input Step 1/Step 2 table unchanged. Add the following exact application
freeze.

## Boundary Ledger semantic and application lock

| Authority | Path | Version/status | SHA-256 | Matches disk |
|---|---|---|---|---|
| Boundary Ledger manifest | `design-system/boundary-ledger/manifest.json` | | | yes / no |
| Semantic core | `design-system/boundary-ledger/semantic-core.json` | | | yes / no |
| Motion binding | `design-system/boundary-ledger/bindings/motion.json` | provisional | | yes / no |
| Illustration language | `design-system/boundary-ledger/illustration-language.md` | canonical | | yes / no |
| Locked illustration manifest | `design-system/boundary-ledger/illustration/episode-006/manifest.json` | visual-language-only | | yes / no |
| Locked illustration image | `design-system/boundary-ledger/illustration/episode-006/hotel-working-model.jpg` | reference-only | | yes / no |
| Scene contract | `design-system/boundary-ledger/scene-contracts.md` | runtime-neutral | | yes / no |
| Production-skill authority | `design-system/boundary-ledger/production-skills.md` | locked | | yes / no |
| OE production-skill lock | `.agents/oe-skills-lock.json` | locked | | yes / no |

- Boundary Ledger validator: pass / fail
- OE production-skill lock validator: pass / fail
- All six lock-declared local files match: yes / no
- Source ledger is `reference-only` and contains the four expected source IDs: yes / no
- No external runtime or provider became Step 3 authority: confirmed / violation
- Motion and sound implementation status remains provisional: confirmed / violation

Any changed path, hash, status, lock membership, or expected source ID invalidates V1 until
compatibility is reviewed and the full v0.4 acceptance set runs again.

## Carried Step 2 delivery limits

Record working-master status, loudness/headroom limits, tail-energy disclosure, independent-listen
status, local-only media availability, and the rule that a sample-level master change invalidates
the timing handoff. These do not become visual claims or disappear because Step 2 is locked.

## Gate V1 decision

Result: mechanically verified candidate / fail

This result does not approve the v0.4 process or any creative episode artifact.

