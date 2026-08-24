# Provider Bakeoff Results

Status: `auth01b_inventory_complete_owner_selection_pending`

## Current result

No listening result exists. The fixture proves the locked passages and planned provider payloads
can be inspected offline. AUTH-01 stopped after finding multiple samples. The corrective AUTH-01B
then recorded a complete three-sample metadata inventory without selecting or downloading audio.

| State | Result |
| --- | --- |
| Exact locked passage identities | runtime-validated against the 3,019-token canonical W |
| Provider-neutral performance envelope | runtime-validated: 2 passages, 35 paragraph boundaries, 14 thought boundaries |
| Provider adapters | runtime-validated: ElevenLabs and Hume each bind both passages |
| Bakeoff plan | runtime-validated: 6 primary calls, 8 expected outputs, no external authority |
| ElevenLabs dry-run compilation | CLI-generated and non-executable: 4 primary calls, 4 outputs |
| Hume dry-run compilation | provisionally complete; pending clone binding and mandatory recompile; non-executable |
| ElevenLabs read-only identity audit | AUTH-01 consumed; multiple-sample stop; AUTH-01B consumed; complete three-sample inventory |
| Hume UI upload/clone | not authorized; not run |
| ElevenLabs calibration | not authorized; not run |
| Hume calibration | not authorized; not run |
| Provider calls made | `2` cumulative read-only ElevenLabs metadata calls: AUTH-01 and AUTH-01B |
| Credentials accessed | environment-only for AUTH-01 and AUTH-01B; not persisted |
| Samples retrieved or uploaded | `0` |
| Voices cloned | `0` |
| Audio files produced | `0` |
| Blind scores | not available |
| Long-form confirmation | not available |
| Selected provider | none |
| Owner creative decision | pending |

## AUTH-01 execution result

The single authorized metadata call returned multiple attached samples. The runner did not choose
among them and did not make the permitted download call. The authorization was consumed before
network access and cannot be retried. No local voice media exists, and Hume remains untouched.

The failed-closed AUTH-01 receipt preserved the multiple-sample reason but not its inventory. That
receipt defect was repaired before AUTH-01B. AUTH-01B then made one independently authorized
metadata call and stored only the safe normalized inventory below. It made no selection and had no
download path.

## AUTH-01B inventory

| Filename | Sample ID | MIME | Provider bytes | Provider provenance fields |
| --- | --- | --- | ---: | --- |
| `ivc_1.mp3` | `rHrnt10vbIpD444OcGVZ` | `audio/mpeg` | 5,760,813 | category/source/original/generated not exposed |
| `ivc_3.mp3` | `snRkGS2XRR1nJW0hIGJP` | `audio/mpeg` | 5,592,621 | category/source/original/generated not exposed |
| `ivc_2.mp3` | `W8D70GbyW9cfeYGLRWQF` | `audio/mpeg` | 5,760,813 | category/source/original/generated not exposed |

The inventory is structurally complete: three well-formed entries, three unique IDs, and three
filenames. It is not provenance proof. The generic filenames and absent provider provenance fields
do not support choosing one sample. A later local-only download requires a new exact authorization;
Hume remains untouched.

## Planned comparison inventory

| Passage | Eleven candidate A | Eleven candidate B | Hume candidate A | Hume candidate B |
| --- | --- | --- | --- | --- |
| `P01-S00` | planned | planned | blocked on clone receipt | blocked on clone receipt |
| `P02-S11-S12` | planned | planned | blocked on clone receipt | blocked on clone receipt |

## Runtime-derived request and character counts

These numbers are dry-run planning values only. The compiled record is authoritative once present.

| Provider | Primary calls | Expected outputs | Primary billable characters | Primary modeled cost | Maximum calls with one fallback per primary | Maximum repeated characters | Maximum modeled cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ElevenLabs v3 | 4 | 4 | 6,540 | `$0.6540` | 8 | 13,080 | `$1.3080` |
| Hume Octave 1 | 2 | 4 | 6,278 | `$0.9417` | 4 | 12,556 | `$1.8834` |
| Combined | 6 | 8 | 12,818 | `$1.5957` | 12 | 25,636 | `$3.1914` |

The maximum assumes exactly one separately bound fallback attempt for every failed primary request.
A fallback is conditional, not a planned generation, and does not increase the expected eight
candidate outputs. The two Eleven generations for a passage have identical text, paragraph
separators, tags, bodies, and character counts. No estimate is an account quote, invoice
prediction, authorization, or evidence of commercial-use eligibility.

## Reproducible provider score

Score all eight blinded clips. After the signed score sheets are frozen and the provider map is
unblinded:

1. The owner and one independent listener each score all eight clips. A clip's score is the
   arithmetic mean of those two frozen totals.
2. For each provider and passage, select its highest-scoring candidate that passed every hard
   gate.
3. A disqualified candidate cannot represent the provider, even if its preference score is high.
   If neither generation passes one passage, that provider is ineligible.
4. The provider short-form score is the arithmetic mean of its selected `P01-S00` score and its
   selected `P02-S11-S12` score.
5. Record the alternate candidate's failures and variance as operational evidence; do not average
   it into or subtract it from the provider score.
6. A provider must score at least 80 to remain eligible. The leader advances; a runner-up within
   5.0 points also advances. A provider more than 5.0 points behind does not advance.
7. Long-form continuity and the several-hours-later same-word pickup are pass/fail confirmation;
   they never rescore or change the frozen short scores.
8. Retain ElevenLabs when it remains eligible, passes confirmation, and its frozen short score
   leads Hume or is within 5.0 points of Hume. Adopt Hume only when it scores at least 80, leads
   ElevenLabs by more than 5.0 points, and passes confirmation. If neither reaches 80, the favored
   path fails confirmation, or the comparison is unavailable, select neither.

| Provider | Best passing P01 candidate /100 | Best passing P02 candidate /100 | Provider short-form score /100 | Within five points |
| --- | ---: | ---: | ---: | --- |
| ElevenLabs |  |  |  | yes / no |
| Hume |  |  |  | yes / no |

## Decision record

- Blind review date:
- Blind-map custodian:
- Independent listener(s):
- Owner listener:
- Passage-level winner(s):
- Long-form confirmation winner:
- Selected acquisition path:
- Rejected path and reason:
- Caveats:
- Owner signature/date:

Do not mark a winner until every candidate passes lexical conformity and provenance, the scorer
remains blind to provider identity, and the winning path passes the long-form confirmation.
