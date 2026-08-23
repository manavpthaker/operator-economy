# Step 2 CLI Validation Contract

Status: proposed v0.2 runtime contract; no provider call is authorized by this document.

## Purpose and boundary

`oe-narration` is the repository-local, Python 3.11-or-newer validator and bounded capture client for V2 Narration Production. It has no import from `studio/`, no legacy script-rewrite prompt, and no command that can approve performance or set `creative_approved`.

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

### `validate-capture-plan`

```text
oe-narration validate-capture-plan --plan capture-plan.json --canonical-w canonical-w.txt
```

The `oe-capture-plan-v1` plan binds:

- a fixture or episode target;
- locked script and W identities;
- the N1 package manifest, N2 performance direction, and N3 voice/capture lock hashes;
- provider, model, voice, and non-lexical settings;
- PCM-first and MP3-fallback policy; and
- exact subordinate W ranges.

Calibration requires cold-open, evidence, economics, and pronunciation modes. A full plan must cover W exactly once and contiguously. Provider authorization is forbidden inside the plan; it is a separate hashed artifact.

### `capture-elevenlabs`

```text
oe-narration capture-elevenlabs --plan PLAN --canonical-w W
oe-narration capture-elevenlabs --plan PLAN --canonical-w W --execute \
  --authorization AUTHORIZATION --output-dir EMPTY_DIRECTORY
```

The first form is always a dry run. It makes zero network calls, does not require an API key, and prints credential-free request envelopes. Each envelope exposes URL/query, bounded W range, text hash, body hash, and character count. `output_format` is a URL query parameter, never a JSON body field.

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
- `word-transcript.schema.json`; and
- `narration-state.schema.json`.

The standard-library `unittest` suite is run with:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=runtime python3 -m unittest discover -s runtime/tests -v
```

The acceptance suite covers the locked 12-block/3,019-token identity, deterministic extraction, forbidden narration artifacts, hash tampering, a missing negation, path traversal and symlink escape, dry-run isolation, query/body separation, authorization tampering/expiry/consumption, renamed MP3, 128 kbps rejection, forbidden fallback failures, native raw PCM conversion, lossy-origin persistence, transcript timing, master mutation, pause-map binding, and the prohibition on automated creative approval. Tests never make a real provider call.
