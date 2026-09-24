# P00 candidate scope audit

Independent review, 2026-09-17. **No concrete mechanical or lexical defect found that prevents showing this exact opening as an explicitly flagged review candidate. Lip sync remains unresolved.** This conclusion does not approve normal conform, bulk generation, release or owner acceptance.

The inspected `presenter-regen/P00/NOTES.json` and `qa/RESTORATION-REVIEW.json` retain both diagnostic flags: zero qualifying onsets is insufficient measurement; narration-mouth correlation is 0.343 versus 0.382 for the guide. P01a/P01b also remain flagged in `diagnostics/pilot-restored-r1/PILOT-REVIEW.json`. Neither pilot is substituted by this candidate.

I inspected all 86 intended mouth frames in the four existing sheets and the six seam frames. The face and shot remain intact and the ending settles before the film cut. These still images do not establish normal-speed audiovisual sync; possible anticipation remains unresolved. The lexical audit corroborates the complete ten-word native sentence and documents the rejected wrong-word correlation peak. Its measurement correction establishes the lag domain, not perceptual sync. The candidate uses the unchanged r3 narration, not generator speech. Existing preview verification measures audio correlation 0.999966 against its exact master slice.

## Independent mapping and mechanism check

- Expanded and compared all 29,323 source-frame assignments against frozen r3: only `[0,86)` changes, using candidate source frames `[0,86)` in order. The remaining 29,237 assignments are identical. F01 returns at its source frame86 and F02 starts at output135. All six later film inserts remain unchanged.
- All 75 row boundaries, cues and other row fields are identical. The r3 master, transcript, time map, owner lock, corrected hospitality paragraph and pending P08 still are retained. The master is padded only to the same 58,646,000 program samples.
- Independently reconstructed the 84 spans and 58 render groups, checked every emitted graph branch, concat order and audio input, and verified 74 bound file hashes. There is no picture retiming, inserted frame hold or generator-audio substitution in this path.
- `build_r4_candidate.py` binds the exact candidate, instruction, decision and frozen r3; it exposes no alternate presenter selection or general flag override. Existing outputs are protected from overwrite. Nine protected helper/plan/index/review artifacts match their recorded hashes.
- `sync_cleared`, `conform_readiness_cleared`, `owner_accepted`, `bulk_cleared`, `release_cleared` and `delivery_master` are all false. The normal r4 eligibility path is unchanged. `final-r5/INDEX.json` remains pending/technical-incomplete; its earlier missing-TAKE explanation is a stale snapshot, not a current missing file or readiness claim. The candidate separately binds the current flagged notes and gate.

## Audit bindings

Paths below are relative to `EP009-FULL-BUILD-001`.

| Artifact | SHA-256 |
| --- | --- |
| `assembly/r3/ep009-full-r3-review-draft-BUILD.json` | `806ec203069d994fb5928c61aaa1350c788b2faf5fa3e9d2663e593ab962aa12` |
| `presenter-regen/P00/qa/opening-P00-private-review-r1.mp4` | `f1618fcf58cb9924656e226ce1a0d494fc545ca944890366e5de910fadb24307` |
| `assembly/_tools/build_r4_candidate.py` | `47d563433acc4ebe2db2ed44666ae91dcec8b2dd3835a4ba602450fc8998a370` |
| `assembly/r4/ep009-full-r4-opening-candidate-graph.txt` | `f1fa88e0b69497d41dbab00f20cfa82091624b78df21d6fc501c877c93357202` |
| Initial candidate BUILD, status `rendering_candidate_lipsync_unresolved` | `e666f83f3e3ce7be1b9c2b1b8d0495d229c324b5872c854bd6a235751fad62c2` |
| Final candidate BUILD, status `encoded_candidate_lipsync_unresolved` | `fad999994483aa029f045a4b1ac6286ca42e7aef91b43fcb454822e5363bec02` |
| `assembly/qa/r4/ep009-full-r4-opening-candidate.mp4` | `c60d5d111cbea3346203a15b842d521f09070c975627c0dd7f500c9f412fcbee` |
| Stable mapping payload | `b1c1f158366ddd61a6ac9b84a0893537bc5c004c5906e5fe4d834d8ea66682fa` |

Stable payload is the candidate BUILD subset `all_75_rows, source_spans, render_groups, sources, master, timemap, transcript, owner_scoped_lock, film_selections, candidate, protected_artifacts, graph, command, candidate_instruction, candidate_decision, candidate_builder, review_label`, serialized with Python `json.dumps(sort_keys=True,separators=(',',':'))` and SHA-256. Final carrier refresh requires this digest to remain identical.

Final carrier refresh: stable payload is identical; reconstructing the earlier BUILD proves only encode status, exit code and output hash changed. Output SHA and all nine protected artifacts were checked again. Assembly's completed full verification (`ep009-full-r4-opening-candidate-VERIFICATION.json`, SHA `199a8b38ba528e9aa52acd86d588c5e508e21d2f405b335d9929057cbf4691ae`) binds this final BUILD/output and records zero errors, all 29,323 decoded frames, all 58,646,000 program samples, minimum voiced correlation 0.9999701467 and silent codec padding. The context verification also passes. These are inspected assembly results, not a duplicate decode by this reviewer.

Inspected `assembly/qa/ep009-r4-review.html` (SHA `0bba6dcadc12e0b66393924d15b2c73740c09fffe2b253221445d08e915cdadc`): opening heading and prominent notice explicitly say lip sync remains under review/unresolved; full video is labeled a review candidate; detailed notes retain both numeric diagnostic flags and no bulk/release clearance. Media links target the intended candidate files and the evidence link resolves through the existing QA symlink. Source inspection found no false pass or acceptance claim. Root owns live browser/playback verification. This audit does not establish perceptual sync.

## Spend cross-check

Latest terminal rows per item, with no open intents: original presenter 1,872 credits / $24.4825; film 121.5 / $9.856; separate regeneration 223.5 / $1.9223. Thus the original shared scope totals **1,993.5 of 2,000 credits** and **$34.3385 of $40**. Regeneration retains **1,576.5 actual credits** and **$28.0777** under its separate 1,800/$30 caps. Its 1,526-credit remaining offline plan projects 1,749.5 total, leaving 50.5 credits. These reconcile with the current checkpoint. Historical pilot totals predate P00's $0.5111 restoration; no current contradiction found. Fal dollar amounts are rate-times-duration ledger estimates, not independently fetched invoices. Narration provider costs are separately recorded and are not included in these three ledgers.

Ledger SHA-256: `presenter.jsonl` `0c99d2ce5a7811a51ddf7a89e2fe4bf2de702929c8ff338bdff7af1aba8f79c6`; `film.jsonl` `4912bf078d019bcb42874f58cf22cdd441c1a08a589baa7aaba19650a6834cb0`; `presenter-regen.jsonl` `1301e78ce907fa0aa4b7ea6d34d995e713855c6c6723a8550d6ff77f802412e5`.
