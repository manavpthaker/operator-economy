# Gate V1: input lock — EP007

Status: **MECHANICALLY PASSED.** A machine verification of upstream hashes. Not an owner decision;
none is required. Upstream inputs are unchanged, so this was regenerated without owner review.

## Complete governing input set

All **13** artifacts the V1 gate names — both locks, and every Step 1 and Step 2 artifact a
later gate reads from. Earlier revisions froze a seven-file subset, which meant the freeze could not
invalidate work that depended on the artifacts it omitted.

| Input | SHA-256 |
|---|---|
| `editorial_lock` | `7d3871804c82e7da09a59c01cd5ef4342ad0ad9141158869acc71d6d291a1319` |
| `operator_canvas` | `3376437f8eda00a4aec5b1ef6e0ff5379abb2f051e3512fc5d683ed2720b158f` |
| `episode_investment_thesis` | `868dc798eeb0513b083debb08ea376b333ae486e9a535be7facf5183e94726f4` |
| `narrative_spine` | `c053f4d95542ce9fc42e9a665d10576cc69e99577fc8849208970f9163efbe4f` |
| `episode_beat_sheet` | `eb953ffa1a0fc5bf4540842f8cd86db19838a1692c00e439c9fdfd538225f4fb` |
| `claims_map` | `0c4f715d71f816fb8190c5fc3777e61cfdabd3c2cc5f26a2aee7a89d0f5fe4e1` |
| `script` | `e56bbb80c1b3a21679a17459402130d820be285ee389fc2978ef8216d6487db0` |
| `canonical_w` | `333a45d7449f5cb4c3e394a9e262c3a3a60c3825e76563bc0149498f0b41860c` |
| `spoken_identity` | `d753a2ca34cc01e0282d10e83158d877c67614b50dbdb9f3ae17de4fc2e004fe` |
| `narration_lock` | `61cfd940b9f8bfcb0e502e07f073a7a1457a671b9a4a35667e6ca08c2fafbbd5` |
| `narration_master` | `d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9` |
| `word_transcript` | `f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7` |
| `intentional_pause_map` | `0176614eb0902d945165956af8fa7ef890906d5f2e15692d14c9e0d9d8b8bdaa` |

Narration duration: **1137.927s** — what V4 binds unit timing to.

## Verified

- Editorial lock records `Gate E6: PASSED`; its 13 recorded artifact hashes match, 0 drifted.
- Narration lock records `Gate N7: PASSED`, `technical_pass` and `creative_approved` on one master.
- Transcript and pause map bound to that master hash and duration.
- Canonical `W` reproduces 3,186 tokens.
- Boundary Ledger core `2.0.0`; motion binding resolves the same version, status **provisional**.
- No open change request against Step 1 or Step 2.

Controls `a36`, `a37` and `a38` prove a missing entry, a drifted hash, or an unacknowledged
provisional motion-binding status each fail this gate.
