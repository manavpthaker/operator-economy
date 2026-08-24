# Step 2 CLI Validation Contract

Status: proposed v0.3 contract with an implemented credential-free validation and request-compilation
surface. Frozen v0.2 capture evidence remains history. No external action is authorized by this
document.

## Purpose and boundary

`oe-narration` is the repository-local, Python 3.11-or-newer validator and bounded capture client for V2 Narration Production. It has no import from `studio/`, no legacy script-rewrite prompt, and no command that can approve performance or set `creative_approved`.

The runtime implements v0.3 offline validation for the provider-agnostic performance envelope,
provider adapters, provider-bakeoff plan, compiled dry run, and the four initial action-
authorization shapes. It also contains one deliberately narrow external-action client for
`AUTH-01`: read the exact bound ElevenLabs voice metadata and, only when that metadata resolves to
exactly one sample, retrieve that sample's original bytes. The client cannot generate speech,
modify a voice, upload a sample, create a clone, call Hume, or authorize later work. The bounded
v0.2 ElevenLabs capture client remains a separate, retained surface; it cannot execute a v0.3
bakeoff plan or reuse a consumed authorization.

Run it from the Step 2 folder as:

```text
python3 runtime/oe-narration <command> ...
```

Successful commands emit one JSON object to standard output and return `0`. Contract failures emit `{ "valid": false, "errors": [...] }` to standard error and return `2`. The CLI fails closed on missing files, hashes, provenance, authorization, codecs, or timing.

## The one spoken-word authority

The authoritative spoken sequence is `W` under `oe-spoken-text-v1`:

1. Read the locked Step 1 Markdown as Unicode UTF-8 and require NFC.
2. Visit the ordered `## Snn:` scenes.
3. Extract only non-empty `### Narration` bodies. A `Narration: none` scene contributes nothing.
4. Reject merge markers, placeholders, HTML, Markdown links/images, footnotes, URLs, and inline performance-direction tags inside narration.
5. Tokenize with Python `str.split()`. Punctuation remains attached; no case-folding, rewriting, or normalization is permitted.
6. Serialize one token per LF and include the terminal LF.
7. SHA-256 that byte sequence.

For the locked AI Visibility v1.1 fixture, the only valid identity is:

```text
blocks: S00, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12
block count: 12
token count: 3019
W SHA-256: 096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a
```

Block, acoustic, capture, and alignment ranges are subordinate parts of W. They may carry hashes for their bounded W slices, but they cannot declare another authoritative word count or identity. In particular, the historical 3,043-word acoustic count is not a competing authority.

## V0.3 provider-bakeoff implementation boundary

The current CLI can validate the locked package, derive canonical `W`, validate the v0.2
ElevenLabs capture contract, and validate and compile the proposed v0.3 cross-provider bakeoff
without credentials, network, UI automation, or audio creation. Its sole v0.3 network exception is
the separately authorized `retrieve-elevenlabs-sample` client described below. It has no command
that may:

- upload a human sample through the Hume Platform or create a Hume clone;
- synthesize Hume narration;
- generate or unseal blind candidate codes;
- score creative performance;
- select a provider method;
- authorize the later long-form continuity/pickup test; or
- grant N4B full capture or Step 3 authority.

Those are deliberate authority boundaries, not claims that Hume can never be executed by a later
reviewed adapter. V0.3 records external actions with separate human authorization, immutable hashes,
provider/UI receipts, and fail-closed review. Offline validation proves only that a record matches
the machine contract. A completed Markdown template or valid JSON is not authority or execution.

The four initial authorization scopes are exactly:

1. `elevenlabs_sample_retrieval` — read-only metadata and exactly one original-sample retrieval;
2. `hume_clone_creation` — one provenance-bound UI upload and exactly one clone creation;
3. `elevenlabs_calibration` — P1/P2 by E1/E2; and
4. `hume_calibration` — P1/P2 by H1/H2.

After AUTH-01 stopped on multiple attached samples, the owner separately authorized the corrective
scope `elevenlabs_sample_metadata_inventory`. It is not a fifth bakeoff-generation action. It can
make one read-only metadata request, preserve a safe inventory for owner selection, and do nothing
else. It cannot select or download a sample and cannot be substituted for any of the four initial
scopes.

The 3.5-to-4.5-minute long-form continuity and several-hours-later same-word pickup test is a fifth,
later human authorization scope. It is not one of the initial machine enum values. None of these
scopes is `full`; never encode one as full capture merely to fit a schema.

The provider-agnostic performance envelope and each provider adapter are separately hashed v0.3
review inputs governed by their own schemas. The bakeoff plan binds them directly; the v0.2
`capture-plan.schema.json` remains unchanged and may not be overloaded. Provider direction never
enters canonical `W`.

## Commands

### `extract`

```text
oe-narration extract --script LOCKED_SCRIPT [--out EMPTY_DIRECTORY]
```

Without `--out`, print the script hash, W identity, and subordinate scene ranges. With `--out`, create exactly:

- `canonical-w.txt`: canonical terminal-LF serialization;
- `spoken-identity.json`: the one authority plus scene-range hashes.

The command refuses a non-empty output directory.

### `verify-package`

```text
oe-narration verify-package --manifest package-manifest.json
```

The manifest uses `oe-narration-package-v1`. It declares portable roots relative to the manifest and gives every source a `root_id`, traversal-free relative path, and SHA-256. Absolute source paths, source `..` segments, undeclared roots, and symlink escapes fail. This permits the OE repository and sibling `content-os` repository to be named explicitly without checkout-specific absolute paths.

Verification hashes every source, re-extracts W from the locked script, verifies the clean read-through is token-identical, verifies the block identity, and rejects alternate word authorities. An owner approval in prose does not bypass a mismatch.

### `validate-performance-envelope`

```text
oe-narration validate-performance-envelope --envelope ENVELOPE.json --canonical-w W
```

Validate `oe-performance-envelope-v1` against canonical `W`. The envelope must stay provider-
neutral, bind exact P1/P2 ranges and thought boundaries, carry no credential-shaped fields, and
grant no external action, public-fact clearance, Step 3 authority, or creative approval.

### `validate-provider-adapter`

```text
oe-narration validate-provider-adapter --adapter ADAPTER.json \
  --envelope ENVELOPE.json --canonical-w W
```

Validate one `oe-provider-adapter-v1` translation against the exact envelope and `W`. The Eleven
adapter may insert only the allowlisted, non-spoken v3 tags at declared boundaries; stripping those
tags must reproduce the exact passage words. The Hume Octave 1 adapter keeps text separate from
bounded natural-language descriptions and may not add dialogue.

### `validate-provider-bakeoff-plan`

```text
oe-narration validate-provider-bakeoff-plan --plan PLAN.json \
  --envelope ENVELOPE.json --canonical-w W
```

Validate `oe-provider-bakeoff-plan-v1`, its envelope and adapter hashes, exact P1/P2 partitions,
provider identities, candidate equality, destinations, PCM/WAV-first policies, permitted fallback,
and call/character accounting. Eleven defines two identical-body calls per passage that differ only
in candidate generation metadata. Hume defines one `POST /v0/tts` JSON call per passage with
`num_generations: 2`.

### `dry-run-provider-bakeoff`

```text
oe-narration dry-run-provider-bakeoff --plan PLAN.json \
  --envelope ENVELOPE.json --canonical-w W [--record DRY_RUN.json]
```

Compile `oe-provider-bakeoff-dry-run-v1` without credentials, network, account reads, UI control, or
audio. Eleven transport uses double-LF paragraph joining, separate canonical/provider-text hashes,
and the 5,000-character v3 ceiling. Hume compiles `POST /v0/tts` bodies with separate utterance text
and acting descriptions, `format.type: wav`, and `num_generations: 2`. The result records primary
and fallback accounting and explicit execution blockers. `--record` writes exclusively and refuses
to overwrite an existing receipt.

### `validate-provider-action-authorization`

```text
oe-narration validate-provider-action-authorization --authorization AUTHORIZATION.json
```

Validate one `oe-provider-action-authorization-v1` against its bound envelope, plan, compiled dry
run, target, provider identity, scope-specific operations, and caps. A safe draft may validate while
reporting `execution_ready: false` and `network_authorized: false`; validity is not approval. An
active record must additionally be human-approved, unexpired, unconsumed, and fully bounded before
it can report ready. The only initial machine scopes are `elevenlabs_sample_retrieval`,
`hume_clone_creation`, `elevenlabs_calibration`, and `hume_calibration`. This command never consumes
or executes an authorization. AUTH-05 remains a separate human record, not an initial machine
scope.

### `retrieve-elevenlabs-sample`

```text
oe-narration retrieve-elevenlabs-sample --authorization AUTH-01.json
oe-narration retrieve-elevenlabs-sample --authorization AUTH-01.json \
  --record DRY_RUN.json
oe-narration retrieve-elevenlabs-sample --authorization AUTH-01.json --execute
```

The first two forms are credential-free dry runs. They validate the authorization and executor
preflight while making zero provider calls. `--record` writes an immutable dry-run record and may
not be combined with `--execute`.

Execution is restricted to scope `elevenlabs_sample_retrieval` and requires the API key in the
process environment plus an active, approved, unexpired, unconsumed authorization with a zero-dollar
spend ceiling. The runner writes the owner-only consumption record before constructing or opening
the first request. Once that record exists, the authorization is permanently consumed even if
metadata, selection, transport, storage, or provenance later fails. There is no automatic retry.

The runner can make only two `GET` requests: the exact plan-bound voice metadata endpoint, then the
official sample-audio endpoint derived from the single returned sample ID. Zero samples or multiple
samples stop after the metadata call. Redirects, symlinked custody paths, ambiguous response sizes
or MIME types, existing destinations, cap overruns, response mismatches, and unparseable or
zero-duration audio fail closed. The original bytes and all receipts are created owner-only; the
sample remains under the ignored `local-media/` tree. Credentials are never written to a request
body, receipt, path, or command result.

A successful download remains `pending_human_review`. Provider metadata, an audio MIME label, and
parseable bytes do not prove that the recording is Manav, entirely human, or single-speaker, and do
not authorize Hume disclosure or upload. A human provenance listen and a new `AUTH-02` are required
before the sample can leave local custody.

### `inventory-elevenlabs-samples`

```text
oe-narration inventory-elevenlabs-samples --authorization AUTH-01B.json
oe-narration inventory-elevenlabs-samples --authorization AUTH-01B.json \
  --record DRY_RUN.json
oe-narration inventory-elevenlabs-samples --authorization AUTH-01B.json --execute
```

This separate corrective client accepts only scope `elevenlabs_sample_metadata_inventory` and
action kind `read_only_voice_metadata_inventory`. Dry-run is credential-free and uses the same
executor preflight. Execution consumes the authorization before one exact voice-metadata `GET`.
The caps are one call, zero downloads, zero spend, and at most 2,000,000 response bytes.

The action must state `selection_permitted: false`, `download_permitted: false`, and
`raw_payload_storage_permitted: false`. It
has no sample endpoint, sample ID selector, download destination, Hume field, local-media path, or
generation path. Its local receipt is created mode `0600` and contains only a credential-filtered,
normalized inventory:
sample IDs, base filenames, provider category/source fields, MIME/size/hash fields, and explicit
original/generated flags when the provider exposes them, plus the raw response hash and byte count.
Unknown fields and raw metadata payloads are discarded. Recording an inventory is not sample
selection, provenance approval, download permission, or downstream authority.

### `validate-capture-plan`

```text
oe-narration validate-capture-plan --plan capture-plan.json --canonical-w canonical-w.txt
```

The `oe-capture-plan-v1` plan binds:

- a fixture or episode target;
- locked script and W identities;
- traversal-safe paths and current hashes for the N1 package manifest, N2 performance direction,
  and N3 voice/capture lock;
- provider, model, voice, and non-lexical settings;
- PCM-first and MP3-fallback policy; and
- exact subordinate W ranges.

Calibration requires cold-open, evidence, economics, and pronunciation modes. A full plan must cover W exactly once and contiguously. Provider authorization is forbidden inside the plan; it is a separate hashed artifact.

### `capture-elevenlabs`

```text
oe-narration capture-elevenlabs --plan PLAN --canonical-w W
oe-narration capture-elevenlabs --plan PLAN --canonical-w W --record DRY_RUN.json
oe-narration capture-elevenlabs --plan PLAN --canonical-w W --execute \
  --authorization AUTHORIZATION --output-dir EMPTY_DIRECTORY
```

The first two forms are always dry runs. They make zero network calls, do not require an API key,
and print credential-free request envelopes. `--record` writes the same result exclusively and
refuses to overwrite an existing receipt. Each envelope exposes URL/query, bounded W range, text
hash, body hash, and character count. `output_format` is a URL query parameter, never a JSON body
field. Execution writes its own run or failure receipt and therefore rejects `--record`.

`--execute` requires all of the following before network access:

- `ELEVENLABS_API_KEY` in the process environment;
- an active, approved, unexpired `oe-provider-authorization-v1` artifact;
- exact target, capture-plan, script, W, provider, model, voice, and format bindings;
- `max_calls` between the part count and twice the part count, because a proven PCM capability failure may require one MP3 retry per part;
- an enforceable payload-character ceiling or a positive USD spending ceiling;
- an unconsumed authorization with a safe relative consumption-record path; and
- an empty capture output directory.

Execution consumes the authorization with an exclusive record before the first request. A retry requires a new authorization. Every PCM attempt and every fallback attempt consumes one call and repeats the part's payload-character count; the runtime stops before exceeding either ceiling. A USD value is recorded only as an authorization ceiling, never as observed provider billing. Provider outputs are written exclusively and never overwritten. Run and failure receipts exclude credentials and include the attempted call/character totals, request envelopes, provider request/job identifiers exposed in known response headers, raw hashes, plan/auth hashes, and `creative_approved: false`.

The first request always uses `?output_format=pcm_48000`. The runtime may retry a part as `mp3_44100_192` only after preserving an explicit, non-retryable HTTP 400, 404, or 422 response that specifically says PCM/output-format capability is unavailable. Authentication errors, timeouts, TLS/DNS/network failures, HTTP 408, 429, or any 5xx response cannot trigger fallback.

This remains the separate executable ElevenLabs v0.2 capture rule. It cannot accept a v0.3 bakeoff
plan or action authorization. The cross-provider v0.3 doctrine requests
provider-native PCM or PCM WAV first and permits only the separately authorized
`mp3_44100_192` capability-unavailable exception. A future Hume executor must enforce equivalent
raw preservation, actual-codec inspection, bounded retry, character/call accounting, and consumed
authorization before it can be used. A Hume UI download or a file with a `.wav` extension is not,
by itself, proof of a lossless acquisition.

### `inspect-audio`

```text
oe-narration inspect-audio --input AUDIO
oe-narration inspect-audio --input RAW_PCM --receipt CAPTURE_RUN [--part-id ID]
```

Normal inspection uses `ffprobe` and reports the actual codec, container, rate, channel count, bit depth, bitrate, duration, and hash. Extensions are not trusted; an MP3 renamed `.wav` remains MP3.

ElevenLabs `pcm_48000` is headerless signed 16-bit little-endian PCM. It has no self-identifying container. The second form therefore requires the hashed runtime capture receipt, matches exactly one raw hash/part, verifies the declared PCM contract, and checks non-empty even-byte geometry.

### `convert-working`

```text
oe-narration convert-working --input RAW --output WORKING.wav \
  [--receipt PROVENANCE] [--part-id ID] [--record CONVERSION.json]
```

The command preserves and re-hashes the raw source, refuses to overwrite the output, and performs one decode/resample into mono 48 kHz, 24-bit `pcm_s24le` WAV. Headerless native PCM requires its capture-run receipt. MP3 requires an `oe-pcm-capability-failure-v1` receipt bound to the raw hash and must inspect as mono 44.1 kHz at 192 kbps. A 128 kbps file fails.

The conversion record permanently carries `lossy_origin`. Converting MP3 into WAV never relabels the acquisition as native or lossless. All subsequent editing stays PCM; the CLI provides no lossy intermediate-export command.

### `validate-transcript`

```text
oe-narration validate-transcript --transcript WORDS.json --canonical-w W [--master MASTER.wav]
```

`oe-word-transcript-v1` must point to the exact 48 kHz, 24-bit, mono PCM WAV master and its hash/duration. It must contain exactly one ordered record per W token with integer, non-overlapping half-open `[start_ms,end_ms)` timing inside the master. `canonical_token` must exactly equal W; optional deterministic `w_id` is `w000000`, `w000001`, and so on. Optional acoustic `alignment_parts` remain ordered subordinate intervals inside their parent word and do not affect W identity.

Every word must have `review_state: approved`, and unresolved mismatches must be zero. Changing one word, dropping `not`, changing the master bytes, using draft/provider timestamps, escaping `base_dir`, or leaving an uncertain disposition fails. A pass sets only `technical_pass: true`; it always reports `creative_approved: false`.

### `validate-state`

```text
oe-narration validate-state --state narration-state.json
```

Gate results are `pending`, `passed`, `failed`, or `invalidated`. Workflow status is `draft`, `blocked`, `returned_to_editorial`, `abandoned`, `in_progress`, or `locked`. Draft state may carry null master, transcript, pause map, and source-format fields.

A locked state requires:

- N1 through N7 all passed;
- `technical_pass: true`;
- explicit creative approval with `set_by_type: human`, approver, and date;
- no active invalidation;
- current master, transcript, and intentional-pause-map hashes;
- transcript and pause map bound to that exact master;
- transcript bound to current W; and
- truthful `audio_origin` and fallback disclosure.

`native_pcm` requires a null fallback reason. `lossy_mp3` requires `pcm_capability_unavailable`. Any sample-level master change invalidates the transcript, intentional-pause map, N6/N7 authority, and Step 3 handoff. The validator never writes creative approval.

## Schemas and test authority

Machine-readable shapes live in `schemas/`:

- `package-manifest.schema.json`;
- `capture-plan.schema.json`;
- `provider-authorization.schema.json`;
- `performance-envelope.schema.json`;
- `provider-adapter.schema.json`;
- `provider-bakeoff-plan.schema.json`;
- `provider-action-authorization.schema.json`;
- `word-transcript.schema.json`; and
- `narration-state.schema.json`.

The standard-library `unittest` suite is run with:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=runtime python3 -m unittest discover -s runtime/tests -v
```

The acceptance suite covers the locked 12-block/3,019-token identity, deterministic extraction,
forbidden narration artifacts, hash tampering, a missing negation, path traversal and symlink
escape, v0.2 dry-run isolation, query/body separation, authorization tampering/expiry/consumption,
renamed MP3, 128 kbps rejection, forbidden fallback failures, native raw PCM conversion, lossy-
origin persistence, transcript timing, master mutation, pause-map binding, and the prohibition on
automated creative approval. V0.3 tests additionally cover provider-neutral envelope enforcement,
adapter word preservation, equal P1/P2 request compilation, Eleven double-LF/tag behavior, Hume
description expansion and `num_generations: 2`, primary/fallback accounting, authorization scope
and bound-hash tampering, credential rejection, and zero-network dry runs. Tests never make a real
provider call.

## Current state interpretation

The retained AI Visibility v1.1 N4A batch is a v0.2 technical **PASS** and owner creative
**REVISE**. That combination does not set N4A to passed, does not set `creative_approved`, and does
not satisfy `workflow_status: locked`. The CLI must not reopen Step 1 because of a performance
revision, and it must not infer provider-bakeoff, long-form, full-capture, or Step 3 authority from
the earlier consumed authorization.
