# Synthetic-guide to Saved-C transfer microtest

Status: both exact G1 and recovery G1R1 authorizations are consumed. Each stopped after its one
candidate-A request returned HTTP `403`; no audio, retry, redirect, fallback, or candidate-B call
occurred. G1R1 independently read back the temporary `roles/aiplatform.user` entry before the
request and verified its exact removal afterward. `AUTH-V1` remains blocked because no guide exists.

## Question

Can a model with a separate natural-language acting field create the emotion, inflection,
thought-space, and argument turns missing from both direct Eleven v3 Saved-C candidates, and can
ElevenLabs Voice Changer then preserve that selected performance while restoring the existing
Original C Manav identity?

This fixture isolates those questions in sequence. It does not compare new voice identities,
reopen Step 1, rewrite the script, retry v0.4, run a full cold open, select a production method,
pass N4A, authorize full capture, lock Step 2, start Step 3, share audio, or publish anything.

## Exact locked scope

- Canonical source: AI Visibility v1.1 under `oe-spoken-text-v1`.
- Full W identity: 3,019 tokens; SHA-256
  `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`.
- Microtest: exact absolute half-open `W[30,110)`.
- Token count: 80.
- Token-slice SHA-256:
  `790a8176c5085968bd24c8572dacc5539b4e686f6b9b269cba2fd330c08d4a4a`.
- Single-space 465-character transport SHA-256:
  `db3ccbb400f6bde4099f08b79b4402c374577cae4e622b0087649482e4f7d1cb`.
- Human-readable mirror: [`passages/P01-W0030-W0110.locked.txt`](passages/P01-W0030-W0110.locked.txt).

The five paragraph hashes are:

| Range | Function | Token-slice SHA-256 |
| --- | --- | --- |
| `W[30,37)` | Immediate missing-company consequence | `ed9fca4fe6b739dec4e383e8e3d39d0ee2abd41e9680e857ce2b9d8583e0f5e9` |
| `W[37,57)` | Stale-2022 absurdity and dry irritation | `4b6d93aee26659cb693486ba3c7585fb7f6cd7d1c828737f2d487a60c76f9d14` |
| `W[57,65)` | Apparently green dashboard | `39109a971904a8361aaefcd63ee7d36ca5b496c3268f0a1dab188e5a2930fa2c` |
| `W[65,78)` | Different-doorway diagnostic reset | `60993213b04479fe5e8965c3d5089124285e67ba842bb60eae9f903c56fc0e41` |
| `W[78,110)` | Practical business possibility lift | `38844419a0bf1b8014636678a01f8d83570aa68e88f5e9746ed1c85663280439` |

## Stage G1: synthetic guide

The proposed guide request is Google Cloud Text-to-Speech:

- `POST https://us-texttospeech.googleapis.com/v1/text:synthesize`;
- model `gemini-2.5-pro-tts`;
- voice `Achird`, language `en-US`;
- exact locked transport in `input.text`;
- separate frozen acting direction in `input.prompt`;
- `advancedVoiceOptions.enableTextnorm: false`;
- `LINEAR16`, 24 kHz, mono provider WAV;
- two identical, unseeded, stochastic calls;
- no retry, redirect, fallback, alternate model, or alternate voice; and
- maximum two original provider WAV outputs.

The exact prompt is one line with no terminal LF:

```text
An experienced operator sits across a table from one smart peer. He is camera-ready, personally engaged, and working through a real puzzle, not reading copy. Speak the text exactly as written: add, omit, repeat, or paraphrase nothing. Start with the consequence. Let "Or worse" carry dry, knowing irritation; make "Everything is green" briefly deadpan; then turn at "That missing view" into genuine curiosity and practical excitement. Keep forward momentum, with thought-space at each turn. Energy eight of ten. Natural American conversation; emphasis follows meaning. Never sound like an announcer, trailer, podcast host, stage pitch, or motivational speaker. Pronounce "2022" as "twenty twenty-two." Do not vocalize these directions.
```

It is 735 UTF-8 bytes with SHA-256
`8cfe0391324bce56cb6bf6d83ef0e781479de14c08a7861716e9716f9017b416`.
The canonical compact request body is 1,440 bytes with SHA-256
`4acd99a738125e942fc1a6c2e4ef8df9c819397c9a2627fb494e73d63d004c53`.
The two-call request-set identity and committed artifact hashes are listed in `RESULTS.md` after
runtime compilation.

The requested authorization ceiling is exactly two calls, 2,880 submitted request-body bytes, two
outputs, 50 seconds and 2,500,000 WAV bytes per output, 5,000,000 total audio bytes, 4,000,000
provider-response bytes per call, and a modeled maximum of `$0.66`. Provider billing cannot be
capped in the request itself; the installed executor enforces every bound locally. Credentials and
raw billing-project identity remain outside Git.
`authorizations/01-google-synthetic-guide.DRAFT.json` grants zero calls, bytes, outputs, and spend.

## Installed G1 executor and consumed one-shot authority

The runtime can execute only a separately materialized, active, unexpired `AUTH-G1` whose exact
caps, request hashes, consumption path, and SHA-256 of the private quota-project value all validate.
The raw quota project comes only from `GOOGLE_CLOUD_QUOTA_PROJECT`; the preserved draft stores
`pending`, while the active record stores only the approved SHA-256 binding. Local ADC metadata is
preflighted from the configured `gcloud` location without storing its path or content. Only after
immutable authorization consumption may the runtime run exact argv
`gcloud auth application-default print-access-token --quiet` without passing a `--scopes` override.
That subprocess receives only `PATH`, `HOME`, `CLOUDSDK_CONFIG`, `LANG`, `LC_ALL`, and `LC_CTYPE`,
plus fixed `CLOUDSDK_CORE_DISABLE_PROMPTS=1`.
Tokens, raw project identity, credential material, response bodies, and `gcloud` stderr never enter
committed artifacts.

The consumed authorization ID deterministically names its local evidence:

- `authorizations/consumed/<authorization_id>.consumed.json` before token refresh or provider
  network;
- `receipts/google/<authorization_id>.run.json` after both outputs pass; or
- `receipts/google/<authorization_id>.failure.json` after any post-consumption failure.

The two WAV destinations remain the exact candidate-A and candidate-B paths compiled in this
fixture. All writes are new, owner-only, symlink-resistant, and immutable. There is no redirect,
retry, fallback, alternate request, or resume. If call two fails after call one succeeds, the first
WAV remains as a receipt-bound partial output and the consumed authorization cannot be reused.
Attempted calls accrue `$0.33` each only as modeled authorization spend, never observed billing.

The separately committed G1R1 recovery wrapper added no grant path. It verified the already-present
hash-bound role, invoked the same G1 executor once, and removed the role in a mandatory `finally`
path. Its final readback recorded zero target-role entries. G1R1 nevertheless returned the same HTTP
`403`, so absence of that direct role is not a sufficient explanation for the second failure. The
actual Google cause remains unknown.

## Guide gate and selection

Each original provider WAV must pass exact-word human review, nonempty full decode, exact declared
PCM-frame payload with no trailing audio, 24 kHz mono media inspection, 20-to-50-second duration,
artifact review, and owner performance review. ASR may flag possible regions but cannot clear exact
words. The owner must hear the consequence, dry irritation, dashboard contradiction, possibility
lift, thought-space, and across-the-table relationship.

If neither guide passes, stop before ElevenLabs. If one or both pass, only the owner can select one
exact original provider WAV. That same unchanged 24 kHz WAV is the only permissible Voice Changer
input. An optional local listening derivative is ineligible.

Later transfer eligibility also requires the successful two-output guide-run receipt, active G1
authorization, consumption record, spend, timestamps, response sizes, and output identities to
cross-hash and prove both requests completed inside the consumed authorization window.

## Stage V1: blocked Saved-C transfer

The future adapter is frozen only so its boundary can be reviewed. It targets Original C
`scMbPZwQjr40V1MzL3Nj` through ElevenLabs Voice Changer using
`eleven_multilingual_sts_v2`, one exact selected WAV, a fixed best-effort seed, conservative voice
settings, and `pcm_48000` first. Voice Changer has no dialogue or acting-direction field; the
selected audio must already contain the performance.

`AUTH-V1` stays blocked until all five prerequisites are exact and verified:

1. selected original-provider guide path, SHA-256, byte count, duration, and media geometry;
2. passing lexical, technical, and performance QA tied to that hash;
3. explicit owner guide selection;
4. verified current account opt-out that is processed and effective for new submissions with
   `enable_logging=true`, or confirmed enterprise ZRM protection with `enable_logging=false`; and
5. renewed owner rights and consent for the selected guide disclosure and Original C transfer,
   bound to the historical Original C owner-selection and saved-voice receipts.

Only then may an exact multipart request be recompiled, rehashed, shown to the owner, and separately
authorized. The active record must bind the chosen `enable_logging` value plus exact primary and
disabled-fallback compiled-request SHA-256 values and exact multipart-body byte counts and SHA-256
values. The current blocked adapter is not executable and contains no guide path, guide hash,
logging decision, compiled request, or multipart identity. A later active transfer is capped at two
calls, one output, a 50,000,000-byte and 50-second source, 100 submitted seconds, and `$0.24`.

## Files

- `performance-envelope.json` freezes the provider-neutral acting map for exact `W[30,110)`.
- `performance-transfer-plan.json` binds the guide request, both adapter paths/hashes, and the
  blocked future transfer contract.
- `adapters/google-cloud-gemini-tts.json` records the exact guide transport.
- `adapters/elevenlabs-voice-changer-saved-c.BLOCKED.json` records the future transfer controls with
  no source guide.
- `compiled/synthetic-guide-dry-run.json` records two identical, zero-network guide requests.
- `compiled/elevenlabs-voice-transfer.BLOCKED.json` proves why no exact multipart request can yet
  exist.
- `authorizations/01-google-synthetic-guide.DRAFT.json` is zero-authority pending owner review.
- `authorizations/01-google-synthetic-guide.ACTIVE.20260825T233757Z.json` is the exact G1 authority
  that was consumed before the failed request.
- `evidence/G1-OWNER-AUTHORIZATION-AND-READINESS.20260825T233757Z.md` records the bounded owner
  decision, operator-reported cloud readiness, immutable hashes, and evidence limits.
- `evidence/G1-FAILURE-DISPOSITION.20260825T235236Z.md` binds the consumed authorization and HTTP
  `403` failure without claiming an unproven provider cause.
- `authorizations/03-google-synthetic-guide-recovery.ACTIVE.20260826T003835Z.json` is the fresh,
  now-consumed same-scope G1R1 authority.
- `evidence/G1R1-TEMPORARY-IAM-AUTHORITY-AND-STATE.20260826T003835Z.md` and
  `evidence/G1R1-OWNER-RECOVERY-AUTHORIZATION.20260826T003835Z.md` disclose the pre-record grant
  ordering deviation and bind the mandatory cleanup transaction.
- `evidence/G1R1-IAM-AND-GUIDE-TRANSACTION.20260826T003835Z.json` proves the exact role readback,
  one failed-closed G1 child invocation, and final role absence.
- `evidence/G1R1-FAILURE-AND-IAM-CLEANUP-DISPOSITION.20260826T011214Z.md` records the second HTTP
  `403`, verified cleanup, and zero downstream authority.
- `authorizations/02-elevenlabs-saved-c-transfer.DRAFT.json` is blocked pending the exact selected
  guide, all prerequisite evidence, and a later separate owner decision.
- `reviews/` contains separate guide QA, performance, selection, transfer QA, and owner-disposition
  templates.
- G1 produced the bound consumption record and failure receipt. The run receipt and both candidate
  WAVs are absent.
- `.gitignore` excludes provider audio and local media. Credential-free authorization, consumption,
  and redacted provider receipts remain reviewable and committed when they exist.

## Hard boundary

Dry-run validity is not authorization; the two separate active records were. Across G1 and G1R1,
this fixture made two authorized candidate-A Google requests, generated zero audio, uploaded zero
cross-provider bytes, mutated zero voices, and recorded `$0.66` total modeled attempted spend. The
exact provider cause of HTTP `403` is unknown. G1R1 does establish that the second request failed
while the exact direct `roles/aiplatform.user` entry was present and that the entry was removed
afterward.

The consumed G1 and G1R1 authorize nothing further. The preserved G1 draft remains zero-authority.
Voice Changer remains validation/compilation-only and rejects `--execute`. No retry, replacement
request, IAM mutation, transfer, or downstream production action is authorized.
