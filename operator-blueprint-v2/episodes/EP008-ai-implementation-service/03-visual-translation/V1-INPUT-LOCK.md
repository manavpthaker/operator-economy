# Gate V1 returned candidate: input lock — EP008

Status: **RETURNED.** This is a complete candidate input inventory, not a Gate V1 lock.

The current proposed Step 3 v0.3 gate requires the literal phrase `Gate E6: PASSED` in the editorial
lock. EP008's editorial lock records `Status: LOCKED`, `Gate: E6 — script lock`, and
`Decision: LOCKED`, but it does not contain that literal phrase. Mechanical hash integrity cannot
substitute for the missing gate condition.

Step 3 v0.3 is also not an authorized process: `PROCESS-MANIFEST.json` records
`proposed; authority returned by owner 2026-09-02 and not re-granted`.

## Step 1 internal-chain defect

The files exist at the hashes inventoried below, but their own headers do not form a closed current
chain:

| Dependency | Current SHA-256 | Downstream header still cites |
|---|---|---|
| Operator Canvas | `d5caa22c0114759247ca8084f3e2cf677f81f66fad5844d7fbc86c8fb963b209` | `b2a7f15e0da25835657cf9645c8257563ed31d70494589513d02ec293520451f` in thesis, spine, beat sheet, and script |
| Episode Investment Thesis | `19ac4015597220d9567cb182b5852125bebc20642cdbbc27d668aef868b662a3` | `c2a7ea3efd9cc3ef376a54bc4b65d76a9ae6ac406aa1007fc26f26f0828b2375` in spine, beat sheet, and script |
| Narrative Spine | `e57bb6cbd6ef2f93c19375be6c66fdc6eceb517d923e34164eef13e67a6478ee` | `2deed0e5ba791b704f28d36b821c0603e5b07e43e63862ae3d8eebc83485f415` in beat sheet and script |
| Episode Beat Sheet | `18a1fc026fc551bbaa986affa4096d212dcd319fe003d8941547eb198250f542` | `452e940ba6f69ce1c3488547dec52f5cf5025c4f462e3cd5905d38224e50993e` in script |

The current script header also still says `Status: review ... owner cold read pending`, while the
external editorial lock records `Status: LOCKED` and `Decision: LOCKED`. Step 1 authority must rule
on and rebind this internal chain; Step 3 may not silently treat the external lock as repairing it.

## Complete governing input candidate

All 13 inputs required by the current validator are present on this host and bound in `engine.json`.

| Input | Path from this directory | SHA-256 |
|---|---|---|
| `editorial_lock` | `../01-editorial/editorial-lock.md` | `76e41bfd02883e7f199d976440fe5e262e8b74d13f4a8e8b5f7b4750eac01874` |
| `operator_canvas` | `../01-editorial/operator-canvas.md` | `d5caa22c0114759247ca8084f3e2cf677f81f66fad5844d7fbc86c8fb963b209` |
| `episode_investment_thesis` | `../01-editorial/episode-investment-thesis.md` | `19ac4015597220d9567cb182b5852125bebc20642cdbbc27d668aef868b662a3` |
| `narrative_spine` | `../01-editorial/narrative-spine.md` | `e57bb6cbd6ef2f93c19375be6c66fdc6eceb517d923e34164eef13e67a6478ee` |
| `episode_beat_sheet` | `../01-editorial/episode-beat-sheet.md` | `18a1fc026fc551bbaa986affa4096d212dcd319fe003d8941547eb198250f542` |
| `claims_map` | `../01-editorial/claims-map.md` | `a5d0693ed70115d2a5973c15ee1fb6d751c0d1ab9ed74c680631cfcf9a564e24` |
| `script` | `../01-editorial/script.md` | `ca1dd86903b700c6fe41f9a22ae9e5862294808d9538f9a5a01f3a7d53a88373` |
| `canonical_w` | `../01-editorial/canonical-w.txt` | `ea3743bfcc6e881a96902556959d141f5a75a2288ecad713ccc6fa7ba787ca63` |
| `spoken_identity` | `../01-editorial/spoken-identity.json` | `8be1e30286b0018e8fd3d8b6359c6c478f79e9c700ace7c2c8299438ac17ba25` |
| `narration_lock` | `../02-narration-production/narration-lock.md` | `cb192c05231cf67196737835b5bcc858e7e4f1732cb09ac0afb508324071285f` |
| `narration_master` | `../02-narration-production/master/narration-master.wav` | `f3d749314141dc2ff158fa2860203cb3431aa6d052230dad9e89112d86ad571e` |
| `word_transcript` | `../02-narration-production/word-transcript.json` | `ad6d372e41d1a24ea0f8a93d64a66051c67426accfcb5a56774eec2b422c04ee` |
| `intentional_pause_map` | `../02-narration-production/intentional-pause-map.json` | `9e6bc05de75956f7c437aa7cb4ff02bb21b109a75e9d22c288dd785cbdd6120c` |

Narration duration recorded for downstream timing: **1223.556 seconds**. The local file probes at
1223.555729 seconds; the lock and handoff use the rounded value above. Transcript: 3,400 of 3,400
ordered `W` tokens, zero unresolved mismatches. Pause map: 318 pauses at or above 0.30 seconds,
208.41 seconds total.

- N6 `technical_pass` names master `f3d749314141dc2ff158fa2860203cb3431aa6d052230dad9e89112d86ad571e`.
- N7 owner `creative_approved` names that same master.
- The transcript and pause map bind that exact master and the same recorded duration.

## Boundary Ledger candidate lock

| Authority | Path from this directory | Status | SHA-256 |
|---|---|---|---|
| Semantic core 2.0.0 | `../../../../design-system/boundary-ledger/semantic-core.json` | current | `30a316f79bc94e017705de0823a0af5b85747a20938eb0a2723d39a1a298978e` |
| Motion binding 2.0.0 | `../../../../design-system/boundary-ledger/bindings/motion.json` | **provisional** | `b2ca3e3295ef2f1dd676732b6b9c7bdefbcfbf55ff642cdf1ab90dc9c84fb450` |

## Step 2 limitations carried forward

- The WAV is a working master, not a delivery master: integrated RMS -22.04 dBFS, peak -5.94 dBFS.
- Scene-room targets were inherited from EP007's measured pause distribution rather than recomputed
  from this master. Changing a join creates a new master and returns to N6.
- The independent second-person listen was not performed and is disclosed as such.
- The narration master is host-local. It exists here at 117,461,428 bytes, but `master/` is ignored
  by `02-narration-production/.gitignore` and the WAV is not tracked. The SHA is verifiable on this
  host; a repository checkout alone cannot reproduce or supply the audio bytes.
- The wizard sandbox residue remains open and non-blocking for the locked narration. No visual may
  imply that the wizard is inadequate or that it leaves any specific work undone.

## Narration tooling compatibility check

The repository package verifier accepts the exact frozen Step 2 package: `valid: true`, 16 sources,
22 blocks, 3,400 tokens, and spoken identity
`ea3743bfcc6e881a96902556959d141f5a75a2288ecad713ccc6fa7ba787ca63`.

The proposed generic narration validators do not accept the same locked artifacts:

- `validate-transcript` reports `valid: false` with 17,006 findings. The first findings identify a
  schema/shape mismatch, missing generic spoken-identity and master objects, a 24-bit requirement,
  and generic integer-millisecond/index/token/review-state/`w_id` fields not present in the bespoke
  transcript.
- `validate-state` reports `valid: false` with 11 findings against the bespoke N2/N6 result shape,
  creative-approval representation, master/transcript/pause bindings, N1-N7 status contract, and
  audio-origin vocabulary.

This is a contract/tooling compatibility finding, not evidence that Step 2 content, approval, or
hashes drifted. The proposed V1 gate does not name these generic commands, their schemas, or the
24-bit contract, so this finding is not independently a V1 failure and creates no Step 2 change
request. It must be ruled before approving the shared process: either keep the generic checks as
separate diagnostics or provide an approved adapter. Step 3 does not rewrite the locked Step 2
artifacts to manufacture a pass.

## Returned conditions

- Against Step 1: issue the literal E6 pass/status ruling and close or explicitly supersede the
  stale internal hash/status chain above. The wizard sandbox test remains an open evidence
  condition and must stay unknown until performed.
- Against Step 2: none recorded; no content or master change is requested.
- Boundary Ledger compatibility: nine open semantic-operation gaps are recorded in `engine.json`;
  none has a local substitute.
- Step 3 process authority: pending. Its tooling decision must classify the generic narration checks
  as separate diagnostics or supply an approved adapter; the current V1 text does not require them.

## Decision

Result: **RETURNED — NOT PASSED**

Reason: the literal Gate E6 condition is absent; the Step 1 internal chain is stale; and the
governing Step 3 process remains proposed. No owner V1 decision is recorded for this candidate.
