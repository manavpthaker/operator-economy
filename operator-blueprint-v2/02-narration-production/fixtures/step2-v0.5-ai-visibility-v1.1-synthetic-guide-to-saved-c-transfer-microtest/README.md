# Synthetic-guide to Saved-C transfer microtest

Status: credential-free, zero-authority fixture with an installed but inactive G1 executor.
`AUTH-G1` is a draft with zero caps and a pending quota-project hash. `AUTH-V1` is a blocked draft
that cannot become executable until one generated guide passes QA, the owner selects its exact
original-provider WAV hash, ElevenLabs data-use protection is verified, rights are rebound, and a
separate authorization is issued.

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

## Installed but inactive G1 executor

The runtime can execute only a separately materialized, active, unexpired `AUTH-G1` whose exact
caps, request hashes, consumption path, and SHA-256 of the private quota-project value all validate.
The raw quota project comes only from `GOOGLE_CLOUD_QUOTA_PROJECT`; this draft deliberately stores
`pending`. Local ADC metadata is preflighted from the configured `gcloud` location without storing
its path or content. Only after immutable authorization consumption may the runtime run exact argv
`gcloud auth application-default print-access-token --scopes=https://www.googleapis.com/auth/cloud-platform --quiet`.
That subprocess receives only `PATH`, `HOME`, `CLOUDSDK_CONFIG`, `LANG`, `LC_ALL`, and `LC_CTYPE`,
plus fixed `CLOUDSDK_CORE_DISABLE_PROMPTS=1`.
Tokens, raw project identity, credential material, response bodies, and `gcloud` stderr never enter
committed artifacts.

The later active authorization ID deterministically names its local evidence:

- `authorizations/consumed/<authorization_id>.consumed.json` before token refresh or provider
  network;
- `receipts/google/<authorization_id>.run.json` after both outputs pass; or
- `receipts/google/<authorization_id>.failure.json` after any post-consumption failure.

The two WAV destinations remain the exact candidate-A and candidate-B paths compiled in this
fixture. All writes are new, owner-only, symlink-resistant, and immutable. There is no redirect,
retry, fallback, alternate request, or resume. If call two fails after call one succeeds, the first
WAV remains as a receipt-bound partial output and the consumed authorization cannot be reused.
Attempted calls accrue `$0.33` each only as modeled authorization spend, never observed billing.

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
- `authorizations/02-elevenlabs-saved-c-transfer.DRAFT.json` is blocked pending the exact selected
  guide, all prerequisite evidence, and a later separate owner decision.
- `reviews/` contains separate guide QA, performance, selection, transfer QA, and owner-disposition
  templates.
- A later active G1 derives one credential-free consumption record and exactly one run-or-failure
  receipt at the paths above; none exists in the current fixture.
- `.gitignore` excludes provider audio, local media, and private receipts. Credential-free active
  and consumed authorization evidence must remain reviewable and committed when it exists.

## Hard boundary

Dry-run validity is not authorization. This fixture has made zero provider calls, accessed zero
credentials, generated zero audio, uploaded zero cross-provider bytes, mutated zero voices, and
spent `$0`. Neither draft may be activated by inference from “go,” a prior authorization, provider
login, guide quality, a successful dry run, or the existence of Original C.

The G1 transport is implemented, but this committed draft cannot authorize it: all caps are zero,
the quota-project hash is pending, and `execution_ready` is false. Voice Changer remains
validation/compilation-only and rejects `--execute`. No credential read, authorization consumption,
provider call, receipt, or audio write has occurred for this fixture.
