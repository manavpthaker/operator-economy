# Week 3 selfie cost reconstruction

Audit date: 2026-09-13. Scope: SELFIE-AVATAR-001 original setting tests through R13 closing-screen revision. This is an internal cost reconstruction, not a provider invoice or publication approval. No generation, account mutation, or purchase occurred during this audit. Receipts are deduplicated by provider job/request ID.

**Identifiable subtotal: 1,646.12 Higgsfield credits plus approximately $37.31 of fal lip-sync usage.** All 16 successful native job debits are now corroborated by the live Higgsfield usage ledger inspected by the parent account auditor. The historical balance chain independently corroborates the last 1,366.62 credits. Actual fal billed dollar amounts are not in the receipts. Voice, still-image, sandbox/ASR, and general assistant usage are not dollar-itemized here, so there is no verified all-in cash total.

## Native video ledger

| Stage | Successful jobs | Credits | Evidence and status |
| --- | ---: | ---: | --- |
| Original home/outdoors/cafe tests | 3 | 156 | `../run.json`: 52-credit quote per video; all three completed. Live usage ledger confirms 52 + 52 + 52 at September 12, 11:31am. |
| R2 olive wardrobe and voice B | 1 | 65 | `../revision-02/video/REQUEST.json`, `SUBMISSION.json`; live ledger confirms 65 at September 12, 1:32pm. |
| R3 faster, more expressive take | 1 | 58.5 | `../revision-03/RUN.json`, `video/REQUEST.json`, `SUBMISSION.json`; live ledger confirms 58.5 at September 12, 4:18pm. |
| R4 first full script | 3 | 357.5 | `../revision-04/video/REQUESTS.json`, `SUBMISSION.json`; balance 1,597 → 1,239.5. |
| R5 full expressive revision | 3 | 357.5 | `../revision-05/video/PREFLIGHT.json`, `SUBMISSION.json`; balance 1,239.5 → 882. |
| R6 section sync correction | 0 | 0 new native cost | Three fal requests below. |
| R7 opening and pacing | 1 | 143 | `../revision-07/video/REQUEST.json`, `SUBMISSION.json`; balance 882 → 739. |
| R8 smile reduction edit | 1 | 138.12 | `../revision-08/video/REQUEST.json`, `SUBMISSION.json`; balance 739 → 600.88. |
| R9 attempted mouth/head edit | 0 | 0 net debit | One rejected job; live ledger shows 136.77 spent then 136.77 refunded, matching `video/REQUEST.json` estimate. Balance 600.88 before and after. `../revision-09/BLOCKED-EDIT.json`, `DELIVERY.json`, `video/SUBMISSION.json`. |
| R10 replacement script | 3 | 370.5 | `../revision-10/DELIVERY.json`: balance 600.88 → 230.38, explicit credits used. |
| R11 tail sync correction | 0 | 0 new native cost | One fal request below. |
| R12/R13 closing screens | 0 | 0 new native cost | Both `DELIVERY.json` records explicitly state `provider_generation_submissions: 0`; rendering costs are separate and unknown. |
| **Total** | **16** | **1,646.12** | **All 16 successful debits corroborated by live usage ledger; 1,366.62 also corroborated by historical balance changes.** |

The live usage ledger corroborates all quoted stage charges, but credit debits do not themselves establish a cash invoice allocation. No unexplained additional debit appears in the retained R4–R10 balance chain.

Native job IDs (each counted once):

| Stage | Unique provider job IDs |
| --- | --- |
| Original | `1e9e8873-8299-4db0-a465-76fecd138479`, `6e38c9f9-6f87-46a3-b2f6-c7fb28690b32`, `be26d6d5-4a35-4658-8120-05dd0f51ae57` |
| R2 | `4ca5df2c-61f8-42b5-8c2c-f3be896622ab` |
| R3 | `904f7c14-ab23-4605-b586-6c8b8ad76a84` |
| R4 | `501d9f3d-0073-40dd-b4f6-e367370c2aad`, `1e1598ba-6e25-4443-988f-6736a61b30ff`, `20958e3e-69b0-4ad1-86ca-4dd616757e2a` |
| R5 | `5cf37eaa-a04a-4431-ab80-71435ee5f2e1`, `0f1dfbcf-19d8-46ac-9d06-13cdf660f0fa`, `19cfdc7c-0fa0-4742-ae56-337fb874f6f4` |
| R7 | `047cb79c-0747-4ef6-bed2-44e9054dd34b` |
| R8 | `d40c526d-a4af-4d48-a988-d95247163d63` |
| R9 rejected, excluded | `bbdd8299-7ff1-481c-9ce6-692837baa35c` |
| R10 | `c07ba44f-bd53-429a-a490-9efdf63bdf58`, `8330caf5-3447-4f54-b588-ca328f78190b`, `f87bdc83-e65f-47ce-b64f-0fff26c29fbd` |

## Fal lip-sync ledger

Current official rates checked for reconstruction: [Sync v3, $8/minute](https://fal.ai/models/fal-ai/sync-lipsync/v3) and [Sync v2 Pro, $5/minute](https://fal.ai/models/fal-ai/sync-lipsync/v2/pro). Each estimate is input media seconds / 60 × published rate. Provider billing rounding or exact actual charges remain unknown; completed-job receipts do not contain a billed dollar amount.

| Stage | Model | Input video seconds | Unique fal request ID |
| --- | --- | ---: | --- |
| R2 | v3 | 10.041667 | `01a096b4-1653-79b3-a5ef-9ed62c1fb3d7` |
| R3 | v3 | 9.041667 | `01a09748-dff7-7381-84c3-6f63b8895cc9` |
| R4 | v3 | 53.875 | `01a097fd-0bb8-7571-aeea-53f07512c185` |
| R5 | v3 | 53.875 | `01a09842-e419-7821-8d4b-158fc159a783` |
| R6 section 1 | v3 | 20.166666667 | `01a09865-c8c4-7141-9b2a-ef0b151a7f09` |
| R6 section 2 | v3 | 15.75 | `01a09865-c8c6-7af3-a7e6-39c9fd425b2f` |
| R6 section 3 | v3 | 17.958333333 | `01a09865-c8c5-74c1-a602-8018c3817336` |
| R7 | v2 Pro | 21.25 | `01a09882-2de8-7631-88cb-95123257a6d4` |
| R8 | v2 Pro | 21.25 | `01a09897-248f-7980-b4f8-1b403464e297` |
| R10 | v3 | 55.083333333 | `01a098ec-6fca-7783-ab5f-d345989cd8ef` |
| R11 | v3 | 17.5 | `01a09aec-7100-7213-a253-d9e53db10e27` |

- Nine v3 jobs: 253.291667333 input seconds; estimated $33.77222231.
- Two v2 Pro jobs: 42.5 input seconds; estimated $3.54166667.
- **Eleven successful jobs; estimated total $37.31388898, rounded $37.31.**
- The original home restoration attempt was rejected with HTTP 403 before a job ID because fal balance was exhausted. No charge is evidenced for it. The outdoors and cafe restorations were not submitted.

Evidence: R2–R5 each retain `lip-sync/JOB.json` and media QA; R6 has `lip-sync/section-01`, `section-02`, `section-03` JOB/INPUT records; R7/R8 retain `lip-sync/MANIFEST.json` and requests; R10 has `lip-sync/NATIVE-INPUT.json` and `DELIVERY.json`; R11 has `INPUT-REPORT.json` and `DELIVERY.json`. The original rejection is `../audio-restoration/home/SYNC-ERROR.json`.

## Other work counted but not dollar-itemized

- **Six Google voice-guide syntheses:** R2 A/B, R3, R4 full guide, R4 pickup, and R10. Six HTTP-200 guide receipts total 149.305958333 seconds. R4 `CORRECTED-GUIDE-RECEIPT.json` records an edit to existing synthesis, so it is not counted as another synth.
- **Five ElevenLabs identity transfers:** R2 A/B, R3, R4, R10. Each has `voice/<take>/TRANSFER-RECEIPT.json`. No actual cost or account debit per request is recorded.
- **Four built-in still-image generations:** the three initial setting previews plus the R2 wardrobe image, documented in the experiment README/run manifest and R2 README. No Higgsfield image credit debit or standalone cash cost is asserted.
- **Caption/ASR/edit/render work:** caption variants, repairs, inspections, transcoding, assembly, and both animated closing screens used existing media. R12 and R13 READMEs explicitly describe HyperFrames execution in the Higgsfield sandbox. Neither closing has a new avatar/voice generation. No sandbox/ASR billed amount is itemized in these records, so this audit does not call that work free.
- Previously accepted OE identity, source voice excerpt, and behavior references were reused. Their historical creation costs belong to earlier experiments, outside this Week 3 scope.

## Optional dollar allocation, not a video invoice

The parent account audit reports the contemporaneous Ultra pool as 3,000 monthly credits with a discounted $99 recurring plan component ($129 less $30 promotion). Allocating that full plan component evenly across the 3,000 included credits is an **assumption**, not a per-credit purchase price or proof of this video's cash charge.

Under that assumption: 1,646.12 × ($99 / 3,000) = **$54.32196** of plan allocation. Add the unrounded fal estimate $37.31388898 = **$91.63584898**, or approximately **$91.64 / roughly $92 identifiable subtotal**. This is an allocation estimate and the unitemized components above still apply. Do not add entire account upgrade invoices to this video; those bought shared account access/credits and cover other work. Parent audit owns the invoice evidence and current account state.

## Live usage ledger cross-check

Parent account auditor inspected `https://higgsfield.ai/me/settings/usage`, last seven days, on September 13. The following September 12 rows use the UI's displayed times. Their amounts and sequence match the retained job receipts and historical quotes. The source UI does not expose a job ID for every row, so matching is by time, sequence, amount, and the preserved provider receipts.

| Displayed time | Credit debit(s) | Matched stage |
| --- | --- | --- |
| 11:31am | 52 + 52 + 52 | Original three tests |
| 1:32pm | 65 | R2 |
| 4:18pm | 58.5 | R3 |
| 7:27pm | 104 + 117 + 136.5 | R4 |
| 8:43pm | 104 + 117 + 136.5 | R5 |
| 9:57pm | 143 | R7 |
| 10:14pm | 138.12 | R8 |
| 10:38pm | 136.77 debit and 136.77 refund | R9 rejected, net zero |
| 11:43pm | 117 + 117 + 136.5 | R10 |

The separate 54-credit row at September 12, 5:37am and 108-credit row at September 13, 10:38am are excluded: they are outside the known Week 3 job sequence. The UI's seven-day account total (4,175.87 credits / $167.035 displayed) is also excluded from this project's total. Parent audit retains the live-account observation; this report did not independently operate the account UI.

## Balance evidence from the exact source session

Source: `/Users/brownmanbrain/.codex/sessions/2026/09/12/rollout-2026-09-12T10-54-24-01a0961c-cb6c-71f0-9741-99cb92838d68.jsonl`. The following are actual `higgsfield_balance` output observations; all timestamps UTC. No unrelated sessions were searched.

| JSONL line | Timestamp | Credits |
| ---: | --- | ---: |
| 1733 | 2026-09-12T23:11:02.115Z | 1597 |
| 2965 | 2026-09-13T00:42:55.823Z | 1239.5 |
| 4011 | 2026-09-13T01:53:56.131Z | 882 |
| 4458 | 2026-09-13T02:13:03.647Z | 739 |
| 4791 | 2026-09-13T02:37:09.010Z | 600.88 |
| 4873 | 2026-09-13T02:41:43.275Z | 600.88 |
| 5099 | 2026-09-13T03:34:26.702Z | 600.88 |
| 5753 | 2026-09-13T04:06:35.031Z | 230.38 |

The 2,407.5-credit balance mentioned near the start of this source session is a read of an older EP007 avatar-v5 receipt, not a fresh Week 3 balance. It is excluded from this audit.

To establish an actual all-in bill, missing evidence is: fal per-request billing amounts, Google voice billing, ElevenLabs per-request debits and plan allocation, image-generation cost attribution, and Higgsfield sandbox/ASR usage charges if any.
