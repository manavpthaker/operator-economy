# V2 Step 2 v0.5 change proposal: Synthetic Guide to Saved-C Transfer

Status: proposed; G1 one-shot transport implemented, independently replayed, and inactive pending
an exact owner authorization

Proposal date: 2026-08-25

Prior state: the Saved-C direct Eleven v3 P01 calibration is frozen as a technical pass and an
owner creative `FAIL / REVISE`. Both candidates were rejected as flat, with no inflection or
emotion. The locked AI Visibility words, Step 1 structure, Original C voice identity, and earlier
evidence remain unchanged.

External-action authority: none. `AUTH-G1` and `AUTH-V1` are zero-authority drafts. No credential,
network, account, browser, provider, audio-generation, or cross-provider upload action is granted by
this proposal.

Runtime boundary: v0.5 implements only the Google G1 guide transport. The committed `AUTH-G1` has
zero caps, a pending quota-project hash, and no authority, so that transport cannot run from this
fixture. ElevenLabs Voice Changer remains validation/compilation-only and rejects `--execute`.

## Decision under test

The rejected v0.4 pair does not establish that Original C is the wrong identity. It establishes
that direct Eleven v3 TTS did not turn the documented performance map into the required acting.
V0.5 therefore separates two jobs:

1. Google Cloud Gemini TTS performs the exact locked words from a separate natural-language acting
   prompt, producing a synthetic guide whose performance is judged before any transfer; then
2. only one exact owner-selected, technically and lexically passing guide may become the input to
   ElevenLabs Voice Changer, which attempts to transfer that performance into the existing
   owner-selected Original C voice identity.

The microtest asks whether this two-stage instrument preserves enough of the selected guide's
emotion, inflection, timing, and thought movement while sounding recognizably like Manav. A short
pass would justify only a separately authorized long-form continuity and pickup test. It would not
select the production tool, pass N4A, authorize full capture, lock Step 2, start Step 3, or publish
anything.

## Frozen microtest

The isolated fixture is
[`fixtures/step2-v0.5-ai-visibility-v1.1-synthetic-guide-to-saved-c-transfer-microtest/`](fixtures/step2-v0.5-ai-visibility-v1.1-synthetic-guide-to-saved-c-transfer-microtest/).
It uses exact canonical `W[30,110)`:

- 80 `oe-spoken-text-v1` tokens;
- token SHA-256
  `790a8176c5085968bd24c8572dacc5539b4e686f6b9b269cba2fd330c08d4a4a`;
- 465-character single-space transport SHA-256
  `db3ccbb400f6bde4099f08b79b4402c374577cae4e622b0087649482e4f7d1cb`;
- consequence and dry-irritation turn at `W[30,57)`;
- dashboard contradiction at `W[57,78)`; and
- practical possibility lift at `W[78,110)`.

Neither provider may rewrite, normalize, improve, or add to the locked dialogue. Direction is
nonlexical. Any vocalized direction, addition, omission, substitution, repetition, changed name,
changed number, changed negation, or changed qualification fails the candidate.

## Hard sequential chain

```text
locked script and canonical W
-> provider-neutral performance-transfer plan
-> exact Google adapter and compiled request
-> separate active AUTH-G1
-> two immutable Gemini guide candidates
-> technical and exact-word QA
-> owner performance review and one exact guide selection
-> exact selected-guide hash, format, geometry, and duration binding
-> Eleven Voice Changer multipart manifest
-> verified Eleven no-training opt-out or ZRM state
-> separate active AUTH-V1 for that exact guide only
-> one immutable transferred candidate
-> technical, exact-word, identity, and performance-transfer QA
-> owner creative disposition
```

The chain is intentionally sequential. `AUTH-V1` cannot be executable before a guide exists,
passes its gates, and is selected by the owner. The system must not auto-select the less broken
guide, infer selection from a filename, or authorize both stages in one gesture.

## Guide-generation contract

The guide leg uses current Google Cloud Text-to-Speech, not the Gemini Developer API preview:

- endpoint: `POST https://us-texttospeech.googleapis.com/v1/text:synthesize`;
- model: `gemini-2.5-pro-tts`;
- voice: `Achird`, language `en-US`;
- exact dialogue in `input.text` and the frozen acting prompt in `input.prompt`;
- `advancedVoiceOptions.enableTextnorm: false`;
- `LINEAR16`, 24 kHz, mono lossless WAV response audio;
- two identical, unseeded, stochastic requests;
- no retry, redirect, alternate voice, alternate model, lossy fallback, or second provider; and
- two local raw outputs at most.

The exact 735-byte acting prompt has SHA-256
`8cfe0391324bce56cb6bf6d83ef0e781479de14c08a7861716e9716f9017b416`.
The canonical compact 1,440-byte JSON request body has SHA-256
`4acd99a738125e942fc1a6c2e4ef8df9c819397c9a2627fb494e73d63d004c53`.
Both calls use that identical body. Stochastic variance is expected; it is not a basis for request
drift.

The plan binds both provider adapters by relative path and SHA-256. Validation also checks their
full semantics against the frozen request and blocked-transfer contracts; a rehashed adapter with
changed meaning fails.

The planned `AUTH-G1` ceiling is two calls, 2,880 total request bytes, two outputs, 50 seconds and
2,500,000 WAV bytes per output, 5,000,000 total audio bytes, 4,000,000 provider-response bytes per
call, and a modeled maximum of `$0.66`. Google does not provide in-request caps for all of those
dimensions, so the installed executor enforces them locally and stops after the second call.
Receipts record `$0.33` of modeled authorization spend per attempted call, not observed provider
billing or an invoice.

Cloud credentials, raw quota-project identity, account identity, tokens, and headers stay outside
Git. A later active authorization must bind the SHA-256 of the private
`GOOGLE_CLOUD_QUOTA_PROJECT` value. The executor preflights symlink-free local ADC metadata, then,
only after writing the immutable consumption record, runs exactly
`gcloud auth application-default print-access-token --scopes=https://www.googleapis.com/auth/cloud-platform --quiet`
under an environment containing only `PATH`, `HOME`, `CLOUDSDK_CONFIG`, `LANG`, `LC_ALL`, and
`LC_CTYPE`, plus fixed `CLOUDSDK_CORE_DISABLE_PROMPTS=1`. It never serializes the token, raw project,
credential path or content, provider body, or `gcloud` stderr. A valid dry run remains zero
authority until the owner sees the exact request and separately materializes a bounded, expiring
`AUTH-G1`.

An authorized execution has four fixed artifact classes:

- two original provider WAV outputs at the compiled candidate-A and candidate-B destinations;
- `authorizations/consumed/<authorization_id>.consumed.json`, written before token refresh or
  provider network;
- `receipts/google/<authorization_id>.run.json` on complete success; or
- `receipts/google/<authorization_id>.failure.json` on any post-consumption failure.

All use directory descriptors, `O_EXCL`, `O_NOFOLLOW`, `fsync`, and mode `0600`. There is no
redirect, retry, fallback, or resume. A failure after the first successful call preserves that
immutable first WAV, records it as a partial output, writes only the failure receipt, and leaves the
authorization consumed. Receipt spend is modeled from attempted calls; no receipt may claim
observed provider billing.

## Selected-guide gate

Each immutable original provider guide candidate must first pass:

- actual WAV/PCM inspection, nonempty full decode, exact declared PCM-frame payload, no undeclared
  trailing audio, 24 kHz mono geometry, 20-to-50-second duration, and no clipping, truncation, or
  obvious synthetic artifact;
- exact-word human review against `W[30,110)`, with ASR used only as a diagnostic;
- no vocalized prompt text or direction;
- intelligibility without music or visuals; and
- owner judgment that the required performance turns, emotion, inflection, thought-space, and
  across-the-table relationship are present.

If neither guide passes, stop before ElevenLabs. Do not transfer a flat or lexically uncertain
guide merely to test voice identity. If both pass, the owner must select one exact original
provider WAV hash; the runtime cannot choose. An optional local listening derivative is clearly
ineligible as Voice Changer input.

The later transfer chain must also bind a successful guide-run receipt to the exact two compiled
destinations, a consumed active `AUTH-G1`, its consumption record, request hashes, timestamps,
response-byte counts, output durations and hashes, and spend within the authorization window and
caps. Files or review forms without that acquisition chain are insufficient.

## Voice-transfer contract

The blocked future transfer leg targets the existing Original C private voice
`scMbPZwQjr40V1MzL3Nj` through:

- endpoint `POST /v1/speech-to-speech/scMbPZwQjr40V1MzL3Nj`;
- model `eleven_multilingual_sts_v2`;
- one multipart `audio` file containing the exact selected original 24 kHz provider WAV bytes,
  unchanged;
- JSON-encoded `voice_settings` with stability `0.40`, similarity `0.80`, style `0.0`, speaker
  boost enabled, and speed `1.0`;
- `remove_background_noise: false` and input `file_format: other` for WAV;
- fixed best-effort seed `2026082501`;
- primary output query `output_format=pcm_48000`;
- `enable_logging=true` only when the account-wide training opt-out is verified processed and
  effective for new submissions; use `enable_logging=false` only with confirmed enterprise Zero
  Retention Mode eligibility and protection; and
- at most one accepted transferred output.

Voice Changer receives no text or acting prompt. It must preserve performance from the audio, but
that behavior is generative and best effort, not a lexical guarantee. The transferred candidate
therefore repeats full lexical, identity, technical, and human creative gates.

A separately authorized capability-only `mp3_44100_192` request may exist as the sole fallback only
after an explicit, unambiguous PCM-format capability rejection. Timeout, disconnect, DNS/TLS,
authentication, `408`, `429`, `5xx`, malformed response, ambiguous provider outcome, or unknown
billing state stops without fallback. The transfer ceiling is one primary call and one output;
the absolute separately authorized capability-fallback ceiling is two calls, one output, a
50,000,000-byte and 50-second source, 100 submitted seconds, and `$0.24`. A lossy result is
ineligible for method advancement.

## Cross-provider rights and data boundary

Generating and privately reviewing a Gemini guide does not authorize disclosure of that audio to
ElevenLabs. The selected guide is Google-derived Customer Data entering a second provider. Before
upload, all of these must be independently present and hash-bound:

1. one exact guide selection and passing guide QA;
2. owner confirmation of the right to use that exact guide as Voice Changer input;
3. current evidence that the account training opt-out is processed and effective for new
   submissions with `enable_logging=true`, or confirmed enterprise ZRM protection with
   `enable_logging=false`;
4. renewed Original C voice ownership and consent binding for the exact primary compiled request,
   multipart body, guide, plan, transfer action, and hashed historical owner-selection and
   saved-voice provenance;
5. exact multipart request, guide bytes, duration, format, destination, call, unit, and spend caps;
   the chosen `enable_logging` value; exact primary and disabled-fallback compiled-request
   SHA-256 values; and exact primary and disabled-fallback multipart-body byte counts and SHA-256
   values; and
6. a separate active, expiring, unconsumed `AUTH-V1`.

If the no-training state cannot be verified, stop. Do not upload the guide. The Google leg and the
Eleven leg may never share one authorization.

## Technical media policy

Preserve provider responses byte-for-byte outside Git. Inspect actual media rather than trusting
extensions or generic MIME labels. Google `LINEAR16` guide audio stays in its original,
self-describing 24 kHz mono WAV for strict decode, QA, owner selection, and transfer input. Do not
resample or wrap it before upload. Header-only, zero-frame, truncated-payload, or undeclared-trailing
audio fails. An optional local listening derivative is review-only and ineligible as transfer
input. Native Eleven `pcm_48000` is raw signed 16-bit little-endian mono PCM
and becomes the 48 kHz, 24-bit, mono working WAV through one documented conversion. An approved MP3
exception must verify actual MP3 codec, 44.1 kHz geometry, and at least 192 kbps before one decode
to the working format. No later lossy intermediate is allowed.

Raw and working destinations must be new, traversal-free, symlink-free, fixture-contained paths.
No output may be overwritten. Receipts must exclude credentials and include request, authorization,
raw-media, conversion, and provider identifier hashes sufficient for independent replay of the
decision, not replay of the provider call.

## Stop and advancement rules

- Bad, flat, direction-vocalizing, or lexically uncertain guide: reject and stop before transfer.
- Missing selection, rights, no-training evidence, or exact `AUTH-V1`: stop before upload.
- Bad transfer: reject and stop. Do not iterate settings under the same authority.
- Passing microtest: eligible only for a later separately authorized 3.5-to-4.5-minute continuity,
  conceptual-transition, dense-evidence, number-heavy, and several-hours-later pickup test.
- No outcome authorizes a full episode, N4A, N4B, narration lock, Step 3, sharing, or publication.

V0.4 remains immutable history. V0.5 does not alter `STAGE-GATES.md`; it is an isolated method
proposal and fixture until the owner separately approves any semantic promotion.
