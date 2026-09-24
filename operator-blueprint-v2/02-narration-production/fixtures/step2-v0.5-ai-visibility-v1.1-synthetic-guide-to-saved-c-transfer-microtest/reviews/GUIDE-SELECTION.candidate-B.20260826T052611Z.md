# Synthetic guide owner selection — candidate B

Status: `selected_for_guide_transfer_evaluation_only`

Owner decision verbatim: `B is definitely better`

Selected by: `Manav Thaker`

Selected at: `2026-08-26T05:26:11Z`

## Bound execution and QA evidence

| Artifact | Path | SHA-256 |
| --- | --- | --- |
| G1R2 consumption record | `authorizations/consumed/AUTH-G1R2-ai-visibility-v1.1-p01-synthetic-guide-20260826T042506Z.consumed.json` | `3c4f9354dec64af0637911e89242784ca4e9a8d63053d315db100abd27ffa35b` |
| G1R2 run receipt | `receipts/google/AUTH-G1R2-ai-visibility-v1.1-p01-synthetic-guide-20260826T042506Z.run.json` | `2898d5f26f6523de6691782e668ab45951f4710751b78414ca8caedeb9fe0a1f` |
| Candidate A QA | `reviews/GUIDE-LEXICAL-AND-TECHNICAL-QA.candidate-A.20260826T045942Z.md` | `7529b156ab17ac23f48666a343d6678f8ca211c9cf6a88fc2d5caa24b65718ab` |
| Candidate B QA | `reviews/GUIDE-LEXICAL-AND-TECHNICAL-QA.candidate-B.20260826T045942Z.md` | `e9e65eab04cda98e648973f6ca20825d4c7a7d3fc9784c7557601086e7b18de2` |
| G1R2 success/private-audition disposition | `evidence/G1R2-GUIDE-SUCCESS-AND-PRIVATE-AUDITION-DISPOSITION.20260826T045943Z.json` | `485ce6db50852055abbd2f620d8cc5979982415042ff2afcc0a4ac2be97227df` |

## Candidate dispositions

| Candidate | Disposition | Basis |
| --- | --- | --- |
| A | `not_selected_and_remains_ineligible_for_this_method` | Candidate B is the owner's definite preference. Candidate A independently remains ineligible because its exact words were not established. |
| B | `selected_for_advancement_to_guide_transfer_evaluation_only` | The owner explicitly chose B over A. Candidate B passed strict media QA and the two-mode offline lexical diagnostic, subject to the remaining human and transfer gates below. |

## Selected original provider guide

Selected candidate ID: `candidate-B`

Selected request ID: `gemini-guide-02`

Selected original provider guide path:
`outputs/raw/google/P01-W0030-W0110/candidate-B.wav`

Selected guide SHA-256: `04448e9fdd50c8de67912b454e8d396f5822eaa881daf18128b825260623c915`

Selected guide byte count: `1646010`

Selected guide duration seconds: `34.290958333333336`

Selected guide media geometry:
`{"container":"wav","codec":"pcm_s16le","sample_rate_hz":24000,"channels":1,"bit_depth":16,"frame_count":822983}`

Original provider bytes unchanged: `true`

Listening derivative selected: `false`

Owner performance preference recorded: `true`

Owner human exact-word confirmation completed: `false`

Owner “twenty twenty-two” pronunciation confirmation completed: `false`

V1-compatible owner-selection approval created: `false`

Approved for Voice Changer transfer: `false`

Selection state: `selected_for_guide_transfer_evaluation_only`

## Authority boundary

| Authority | State |
| --- | --- |
| Guide selected for local transfer evaluation | `true` |
| Candidate A not selected and remains ineligible for this method | `true` |
| Creative preference beyond this exact A/B comparison | `false` |
| Cross-provider disclosure authorized | `false` |
| ElevenLabs upload authorized | `false` |
| Voice Changer request compiled or authorized | `false` |
| V1 execution authorized | `false` |
| Full capture authorized | `false` |
| Step 2 lock authorized | `false` |
| Step 3 authorized | `false` |
| External sharing authorized | `false` |
| Publication authorized | `false` |

## Remaining gates

Before any cross-provider disclosure or Voice Changer action, the workflow still requires:

1. owner human exact-word and “twenty twenty-two” pronunciation confirmation for the unchanged
   selected WAV;
2. current ElevenLabs account data-use protection evidence;
3. separate rights and consent for disclosing this exact guide to ElevenLabs and using Original C;
4. an exact selected-guide-bound multipart request and hash set; and
5. a fresh, separate, active V1 authorization.

This record selects candidate B and leaves candidate A not selected and independently ineligible
for this guide-transfer evaluation. It is not an `oe-synthetic-guide-owner-selection-v1` record, does
not set `approved_for_voice_transfer=true`, and does not authorize upload, transfer, regeneration,
full capture, Step 2 lock, Step 3, sharing, or publication.
