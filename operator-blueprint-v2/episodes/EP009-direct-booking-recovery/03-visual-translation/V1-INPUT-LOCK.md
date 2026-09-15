# Gate V1 input lock candidate: EP009

Status: **NOT PASSED.** This is a hash-verified candidate record, not a gate pass or owner approval.

Template version: proposed Step 3 v0.3

Verified: 2026-09-04

Verified by: Codex, mechanical audit only

## Process snapshot

- Proposed Step 3 process manifest: `operator-blueprint-v2/03-visual-translation/PROCESS-MANIFEST.json`
- SHA-256: `4f830d71d677efa8915429dfe35628012289c28ac988cb74f77261331519690c`
- Recorded status: `proposed; authority returned by owner 2026-09-02 and not re-granted`

This record does not approve that process.

## Complete governing input set

All thirteen artifacts named by the proposed V1 freeze exist on this host and match these recomputed hashes.

| Input | Path | SHA-256 | Matches disk |
|---|---|---|---|
| `editorial_lock` | `../01-editorial/editorial-lock.md` | `246330740a5c7447e455f967b7a8597a3a8352fa417ff1f241e730c448da2d20` | yes |
| `operator_canvas` | `../01-editorial/operator-canvas.md` | `c3b00ed94fa4587b82a0dc8fb6d30044cd7768be984217f3bef4d1aaff27ec35` | yes |
| `episode_investment_thesis` | `../01-editorial/episode-investment-thesis.md` | `f5210eec2bd8edfcaec25f612a82cf6420ff43f4859731d844a91c53f76c6c93` | yes |
| `narrative_spine` | `../01-editorial/narrative-spine.md` | `b1383559042fbabef276e52a1af1e24d389501de5280ca9d6332d23924819548` | yes |
| `episode_beat_sheet` | `../01-editorial/episode-beat-sheet.md` | `ae3e89c3b4c366000a574504b71f629ca0e7a4fa3de3773a746a37cc8b7f2578` | yes |
| `claims_map` | `../01-editorial/claims-map.md` | `37f9f4727cde1b7e52fd75745117685336a28ec5f6756cf5f1be3dea1bb68798` | yes |
| `script` | `../01-editorial/script.md` | `cbe74c03e021998cafc1d11a8b0dff50e6dfaa4d0109fc223c958a6ecc37993c` | yes |
| `canonical_w` | `../01-editorial/canonical-w.txt` | `7b9d18bfb2820a124f96308568cbb5509eef792a38150a5e78c3643ced9e191e` | yes |
| `spoken_identity` | `../01-editorial/spoken-identity.json` | `85475673b31cd8335aa56ba79eb2e36e59f605ee5fdd23f814e4f2b73b790f67` | yes |
| `narration_lock` | `../02-narration-production/narration-lock.md` | `fe522d418e2f5bd37b195c55fdf7db7b2e784db0a4ae65154b98c508c2178ae5` | yes |
| `narration_master` | `../02-narration-production/master/narration-master.wav` | `e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944` | yes, host-local |
| `word_transcript` | `../02-narration-production/word-transcript.json` | `3c28411effaea94c4dffaac51e114f333f386170fe4716fa96b30d24e41384aa` | yes |
| `intentional_pause_map` | `../02-narration-production/intentional-pause-map.json` | `62811b5f0ae93359d520f7adfec06ebf46404e8e146cedf274b1f327f9a5cd84` | yes |

Narration duration recorded by the transcript and pause map: **1233.602 seconds**. Host probe: **1233.602500 seconds**, PCM signed 16-bit little-endian, 48 kHz, mono.

## Step 1 finding

- Editorial lock status is `LOCKED`, owner decision is `LOCKED`, Step 2 is authorized, and unresolved blockers are recorded as none.
- The literal string `Gate E6: PASSED` is **not present** in `editorial-lock.md`.
- Canonical `W` reproduces **3,399 tokens** and SHA-256 `7b9d18bfb2820a124f96308568cbb5509eef792a38150a5e78c3643ced9e191e`.
- `spoken-identity.json` binds the same script and `W` identity.
- R001 remains a Step 0 evidence request about messaging-window durations. The editorial lock explicitly rules it non-blocking and records no unresolved Step 1 blocker.

The external lock names the current files, but the Step 1 package does not close its internal dependency chain:

| Dependency | Current SHA-256 | Hash embedded by dependent artifacts |
|---|---|---|
| Operator Canvas | `c3b00ed94fa4587b82a0dc8fb6d30044cd7768be984217f3bef4d1aaff27ec35` | thesis, spine, beat sheet, claims map, and script cite `ac26ef455272ef63046e181305311bf2754bf18cb19448d2d90d1b0fc4538847` |
| Episode Investment Thesis | `f5210eec2bd8edfcaec25f612a82cf6420ff43f4859731d844a91c53f76c6c93` | spine, beat sheet, and script cite `293cee76cb0bea309e5d37d629177a21d3cb51082095256005872d2ba95c189c` |
| Narrative spine | `b1383559042fbabef276e52a1af1e24d389501de5280ca9d6332d23924819548` | beat sheet and script cite `b129310309a4ee1a25d82cb668209955a5b687d7fed92943026b9ed6d6771ad6` |
| Episode beat sheet | `ae3e89c3b4c366000a574504b71f629ca0e7a4fa3de3773a746a37cc8b7f2578` | script cites `455bb222fa3484741da7477e7568aa44c53aadc79ba889b12642d229722fa86e` |
| Claims map | `37f9f4727cde1b7e52fd75745117685336a28ec5f6756cf5f1be3dea1bb68798` | thesis, spine, beat sheet, and script cite earlier claims-map identity `2863880e2874184ae23b4b707faacfbd0ebcd116f46539b5cda0433b1846dc50` |

The script itself still says `Status: review (integrated revision v0.3, owner cold read pending)` and ends `Decision: drafted, owner approval pending`, despite the external editorial lock recording the cold read and exact script hash as passed. The embedded hashes may be historical draft identities rather than content drift, but the current Step 1 contract instructs dependent artifacts to store their approved upstream hashes. V1 therefore cannot infer internal closure from the external lock alone. This is a bounded Step 1 ruling/change request; Step 3 does not edit those files.

The proposed V1 gate also requires the literal E6 pass string. Substantive lock equivalence is not inferred here, and the immutable editorial lock is not edited to manufacture it.

## Step 2 finding

- Narration lock records `Gate N7: PASSED`.
- `technical_pass` and `creative_approved` name master `e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944`.
- The transcript contains 3,399 aligned words and the pause map contains 318 pauses. Both bind that master and the same recorded duration.
- c05 remains an accepted marginal technical caveat: tail energy `0.024` against the `0.02` flag threshold, with a full-length final word and transfer length matching the guide. It is not treated here as a new N6 or N7 failure.
- Independent second-person listening was not performed, as disclosed in the narration lock.

The repository package verifier reports the Step 2 package valid. The generic narration transcript and state validators do not accept this episode's bespoke transcript/state shape or its frozen 16-bit format. That is a validator-contract mismatch, not hash drift. The proposed V1 gate does not name those generic commands, schemas, or the 24-bit contract, so the mismatch is not independently a V1 failure and creates no Step 2 change request. Before the shared process is approved, it must classify the checks as separate diagnostics or supply an approved adapter.

## Boundary Ledger lock

| Authority | Path | Version/status | SHA-256 | Matches disk |
|---|---|---|---|---|
| Semantic core | `../../../../design-system/boundary-ledger/semantic-core.json` | `2.0.0` | `30a316f79bc94e017705de0823a0af5b85747a20938eb0a2723d39a1a298978e` | yes |
| Motion binding | `../../../../design-system/boundary-ledger/bindings/motion.json` | `2.0.0` / `provisional` | `b2ca3e3295ef2f1dd676732b6b9c7bdefbcfbf55ff642cdf1ab90dc9c84fb450` | yes |

The two files resolve the same system version. The motion binding's implementation status remains provisional; this record does not upgrade it.

## Host-local reproducibility boundary

The master and its raw/select audio are intentionally ignored by the episode's `.gitignore` and are absent from `HEAD`. The exact master is present and hash-verifiable on this host, but a clean clone cannot reproduce or verify the audio without a separately transferred media package. The text package manifest verifies sixteen text sources and the 3,399-token spoken identity; it is not an audio-media archive.

## Open change requests

- Against Step 1: bounded closure ruling required for the stale embedded dependency hashes and the script's review/pending metadata versus the external editorial lock. R001 remains a separate Step 0 request and is explicitly non-blocking.
- Against Step 2: none recorded; no content or master change requested.
- Boundary Ledger drift: none detected.
- Process/template authority: pending; Step 3 v0.3 remains proposed. Its tooling decision must classify the generic narration checks as separate diagnostics or supply an approved adapter; current V1 text does not require them.

## V1 decision

Result: **NOT PASSED**.

Reasons:

1. The proposed gate's required literal `Gate E6: PASSED` is absent from the otherwise locked editorial record.
2. The current Step 1 package does not internally close its dependency hashes, and the script still records review/pending status despite the external lock. Their intended historical-vs-current meaning requires an upstream ruling.
3. Step 3 v0.3 and its templates remain proposed and have not regained owner authority.

No later gate is activated by this candidate record. V2 and V3 material may exist only as explicitly ungated drafts for review; it is not a V2 or V3 gate attempt and does not authorize Step 4.

Approved by: **nobody**
