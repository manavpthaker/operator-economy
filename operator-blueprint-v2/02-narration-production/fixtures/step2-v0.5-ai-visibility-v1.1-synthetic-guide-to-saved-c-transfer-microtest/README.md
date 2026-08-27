# Synthetic-guide to Saved-C transfer microtest

Status: fresh recovery-bound G1R2 is consumed and succeeded with both exact provider WAVs. Candidate
A passes technical QA but is lexically unresolved and ineligible; both offline decodes heard `this`
where locked `W` requires `the`. Candidate B passes technical and offline lexical QA (`80/80`) and
the owner selected it for guide-transfer evaluation with the exact decision `B is definitely
better`. Candidate A is not selected and independently remains ineligible for this method.
`AUTH-V1` remains blocked and zero-authority.

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

### Candidate C and D manual style refinements

The prompt above remains frozen history for candidates A and B. The proposed next manual Google
pass uses
[`prompts/P01-W0030-W0110.candidate-C.google-gemini-tts.style-instructions.json`](prompts/P01-W0030-W0110.candidate-C.google-gemini-tts.style-instructions.json).
It keeps the locked words unchanged, removes the instruction that made the opening sound like a
headline, keeps both uses of `missing` light inside their phrases, and replaces designed
thought-space with brief, irregular, idea-led pauses. Any output must be a new `candidate-C.wav`;
candidates A and B remain unchanged. The prompt record grants zero provider authority.

The owner-supplied candidate C audition still over-stressed the target word. Naming that word and
several exact beats in the prompt likely made them more salient, while instructions for deliberate
irregularity still produced designed timing. The replacement
[`prompts/P01-W0030-W0110.candidate-D.google-gemini-tts.style-instructions.json`](prompts/P01-W0030-W0110.candidate-D.google-gemini-tts.style-instructions.json)
removes every word-specific direction, named line anchor, energy score, and constructed pause
pattern. Rather than describing delivery, it establishes the preceding question, concrete buyer
risk, dashboard knowledge gap, peer relationship, and reason for speaking; prosody is left as a
side effect of that situation. Candidate C remains unchanged; any new output must be
`candidate-D.wav`. This prompt record also grants zero provider authority.

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
actual Google cause remains unknown. A later bounded service transaction enabled the one confirmed
configuration anomaly, `aiplatform.googleapis.com`, and a fresh recovery-bound G1R2 authorization
then completed both original requests. It produced two unchanged 24 kHz mono provider WAVs with no
retry, redirect, or fallback and consumed the full modeled `$0.66` ceiling.

## Guide gate and selection

Candidate A is excluded from owner performance review because its exact words are not established:
both offline decoding modes returned the same possible `the`/`this` substitution. Candidate B is the
only current audition candidate; both offline modes matched all 80 locked tokens after normalization.
The owner then selected exact candidate B for guide-transfer evaluation. Candidate A is not selected
and independently remains ineligible for this method. That local comparison selection does not
clear human exact-word or pronunciation review and does not authorize disclosure, upload, or
transfer.

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

The candidate-B selection now supplies the exact local guide identity and the owner's binary
comparison preference. It is not the validator's `oe-synthetic-guide-owner-selection-v1`
prerequisite and does not approve Voice Changer transfer. Human exact-word and “twenty twenty-two”
pronunciation confirmation, current data-use evidence, renewed rights and consent, exact multipart
compilation, a V1-compatible owner-selection approval, and a separate active V1 remain open.

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
- `authorizations/10-google-synthetic-guide-g1r2.ACTIVE.20260826T042506Z.json` is the exact,
  now-consumed recovery-bound authority that produced both original provider WAVs.
- `authorizations/consumed/AUTH-G1R2-ai-visibility-v1.1-p01-synthetic-guide-20260826T042506Z.consumed.json`
  and `receipts/google/AUTH-G1R2-ai-visibility-v1.1-p01-synthetic-guide-20260826T042506Z.run.json`
  are the immutable one-shot consumption and successful run evidence.
- `reviews/GUIDE-LEXICAL-AND-TECHNICAL-QA.candidate-A.20260826T045942Z.md` fails candidate A closed
  on lexical certainty; `reviews/GUIDE-LEXICAL-AND-TECHNICAL-QA.candidate-B.20260826T045942Z.md`
  clears candidate B only for private owner audition.
- `evidence/G1R2-OFFLINE-ASR-DIAGNOSTIC.20260826T045358Z.json` binds the local Whisper binary and
  model hashes, network-denied beam and greedy settings, normalization rule, transcripts, and exact
  token comparisons. It is diagnostic evidence, not human review or authority.
- `evidence/G1R2-GUIDE-SUCCESS-AND-PRIVATE-AUDITION-DISPOSITION.20260826T045943Z.json` cross-binds
  the successful run, both raw WAVs, both QA records, and the still-closed downstream authority.
- `reviews/GUIDE-SELECTION.candidate-B.20260826T052611Z.md` records the owner's exact decision
  `B is definitely better`, selects unchanged candidate B for local guide-transfer evaluation, and
  leaves candidate A not selected and independently ineligible without authorizing upload or
  transfer.
- `authorizations/02-elevenlabs-saved-c-transfer.DRAFT.json` is the preserved historical,
  pre-selection zero-authority draft. Its embedded all-pending blocker list is not a statement of
  current readiness; the candidate-B selection record and the current remaining gates above govern
  the present state.
- `reviews/` contains separate guide QA, performance, selection, transfer QA, and owner-disposition
  templates.
- G1R2 produced the bound consumption record, successful run receipt, and both original provider
  WAVs. The WAVs remain local excluded media and must not be rewritten or replaced by derivatives.
- `.gitignore` excludes provider audio and local media. Credential-free authorization, consumption,
  and redacted provider receipts remain reviewable and committed when they exist.

## Hard boundary

Across G1, G1R1, and G1R2, this fixture made four authorized Google calls, generated two provider
WAVs, uploaded zero cross-provider bytes, mutated zero voices, and recorded `$1.32` total modeled
attempted spend. G1 and G1R1 failed with HTTP `403`; G1R2 later completed both exact original-plan
requests after the separate service-enablement transaction. That sequence does not retroactively
prove the earlier provider cause.

All three guide authorizations are consumed and authorize nothing further. Candidate A is
ineligible and not selected for this method. Candidate B is selected only for local guide-transfer
evaluation of its exact raw bytes. That preference is not cross-provider disclosure or transfer
approval. The preserved G1 draft and `AUTH-V1` remain zero-authority; Voice Changer remains
validation/compilation-only and rejects `--execute`. No regeneration, upload, transfer, full
capture, Step 2 lock, Step 3, external sharing, or publication is authorized.
