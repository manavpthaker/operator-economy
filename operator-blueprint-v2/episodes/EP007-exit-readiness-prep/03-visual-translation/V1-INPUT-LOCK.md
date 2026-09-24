# Gate V1 candidate: fresh input lock — EP007

Status: **MECHANICALLY VERIFIED CANDIDATE under proposed Step 3 v0.4.** This is not a gate pass,
because v0.4 has not been approved as the governing Step 3 process. No owner decision is inferred.

Machine record: `input-lock.json`

SHA-256: `9adde76470b05da2d635521e8711e4d55ed76353a1479db50ba430449899a384`

## Restart boundary

This run starts from the exact Step 1 and Step 2 locks. It does not import the returned v0.3
engine, world, characters, locations, props, generated footage, shot order, angles, camera moves,
edit timing, or creative preferences.

The old candidate remains unchanged at
`../03-visual-translation-pilot-v0.3-returned-2026-09-06/`.

## Process candidate

| Artifact | SHA-256 | Standing |
|---|---|---|
| Proposed v0.3 base process manifest | `4f830d71d677efa8915429dfe35628012289c28ac988cb74f77261331519690c` | exact preserved base; not authority |
| Proposed v0.4 process manifest | `f1ea099a82b5f72f0032d27cbb570a2af1a5abbeb0aeb9a3731569d97f935c5f` | 73/73 mechanical controls; not approved |

## Complete Step 1 and Step 2 freeze

All hashes were recomputed against disk.

| Input | SHA-256 |
|---|---|
| Editorial lock | `7d3871804c82e7da09a59c01cd5ef4342ad0ad9141158869acc71d6d291a1319` |
| Operator Canvas | `3376437f8eda00a4aec5b1ef6e0ff5379abb2f051e3512fc5d683ed2720b158f` |
| Episode Investment Thesis | `868dc798eeb0513b083debb08ea376b333ae486e9a535be7facf5183e94726f4` |
| Narrative spine | `c053f4d95542ce9fc42e9a665d10576cc69e99577fc8849208970f9163efbe4f` |
| Episode beat sheet | `eb953ffa1a0fc5bf4540842f8cd86db19838a1692c00e439c9fdfd538225f4fb` |
| Claims map | `0c4f715d71f816fb8190c5fc3777e61cfdabd3c2cc5f26a2aee7a89d0f5fe4e1` |
| Script | `e56bbb80c1b3a21679a17459402130d820be285ee389fc2978ef8216d6487db0` |
| Canonical spoken words | `333a45d7449f5cb4c3e394a9e262c3a3a60c3825e76563bc0149498f0b41860c` |
| Spoken identity | `d753a2ca34cc01e0282d10e83158d877c67614b50dbdb9f3ae17de4fc2e004fe` |
| Narration lock | `61cfd940b9f8bfcb0e502e07f073a7a1457a671b9a4a35667e6ca08c2fafbbd5` |
| Narration master v4 | `d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9` |
| Word transcript | `f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7` |
| Intentional-pause map | `0176614eb0902d945165956af8fa7ef890906d5f2e15692d14c9e0d9d8b8bdaa` |

The governing narration lock records N7 `PASSED`, `technical_pass`, and Manav Thaker's
`creative_approved` against the same v4 master on 2026-09-02.

Timing contract: **1137.927 seconds**, **3,186 words**, and **276** pauses of at least 0.30 seconds
totalling **182.34 seconds**. V4 must bind to the transcript's word indices; it may not estimate.

## Boundary Ledger and filmmaking freeze

| Authority | SHA-256 | Status |
|---|---|---|
| Boundary Ledger manifest | `3881bab69ab3531b02b50a9077d5ee078e5cdca000204a70bd24d369b7b592a0` | canonical semantic authority |
| Semantic core | `30a316f79bc94e017705de0823a0af5b85747a20938eb0a2723d39a1a298978e` | canonical 2.0.0 |
| Motion binding | `b2ca3e3295ef2f1dd676732b6b9c7bdefbcfbf55ff642cdf1ab90dc9c84fb450` | provisional implementation |
| Working Model illustration language | `f5945a71249beaa64f15e9562f2a1233c516bed23a4dfb0cd57eacb74d28a3b6` | canonical mark language |
| EP006 illustration reference manifest | `69d845f5030361dab03dea5a34765eeb3bb1a01815ff843579c3f7e2ee8443e1` | locked visual-language reference only |
| EP006 reference image | `083533f79798ef04d66b112fa1a2275e1e181074c6e80c22591fc67ea54c6712` | mark-making reference; content excluded |
| Boundary Ledger scene contract | `407d0dc58dd1c3de09279cc892676a967c9596c0cae21fc8c40937b49a78f3fe` | runtime-neutral |
| Boundary Ledger production-skill authority | `8ee324973fe71bca11883603559a58ee206c121e4cd4350886960414fa496090` | locked |
| OE production-skill lock | `485594a623c58f431992882838097a38b6f129a1e464e863ac3170680f36bbb2` | locked; six local files match |
| Film-reference source ledger | `1b0853355f83503bcdecd5eafd8f60e664be7a4c5ce62ba330905fba38553fb1` | reference-only; four expected sources |

The Boundary Ledger validator reports 0 errors across 55 paths. The OE skill validator reports 0
local findings. External source bytes were independently checked against the four pinned commits in
this working session; production relies on the locked OE synthesis, not on a live external checkout.

## Carried Step 2 limits

These remain visible rather than being converted into Step 3 claims:

1. The narration is a working master, not a delivery master: 48 kHz, 16-bit, mono, about -22 dBFS
   RMS with 1.31 dB peak headroom. Final program loudness and headroom remain delivery work.
2. One of 24 chunks is marginally above the tail-energy threshold; owner review heard no defect.
3. No independent second-person listen occurred. The Step 2 lock records that as disclosed, not
   closed, despite the general N7 contract naming such a listen.
4. The v4 WAV is gitignored and local-only. It exists and decodes in this checkout but will not
   appear automatically in another worktree.
5. Any sample-level master change invalidates the transcript, pause map, technical pass, creative
   approval, narration lock, and this timing handoff.

## Mechanical result

- 13 Step 1/Step 2 inputs, 10 Boundary Ledger/OE application files, and the v0.4 process manifest
  match disk: yes — 24 unique files total.
- v0.4 application validator through V1: no findings.
- Full proposed v0.4 acceptance set: 73/73 controls passed.
- Motion and sound implementation status was not upgraded: confirmed.
- Runtime selected: none.

Result: **mechanically verified V1 candidate; process approval still required before this can be
recorded as a gate pass.**
