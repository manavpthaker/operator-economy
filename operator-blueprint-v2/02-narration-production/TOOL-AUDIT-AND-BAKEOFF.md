# Step 2 Provider Audit and Narration Bakeoff

Status: proposed Step 2 v0.3 with credential-free validation and request compilation. No provider,
account, UI, media, or scoring action is authorized by this file.

V0.2 remains the frozen record of the first AI Visibility narration calibration. V0.3 adds a
provider-selection test because that batch proved the acquisition path technically but did not
meet the owner's creative standard.

## Current decision

The retained AI Visibility v1.1 N4A batch has:

- technical acquisition result: **PASS**;
- owner creative result: **REVISE**;
- N4A gate: **not passed**;
- Step 1 status: **still locked; do not reopen**;
- N4B full-capture authority: **none**; and
- Step 3 authority: **none**.

The problem to solve is the performed voice, not the approved words. The v0.3 test therefore uses
the same Step 1 v1.5 script identity and the same nonlexical performance intent. A candidate may not
gain an advantage by rewriting, paraphrasing, adding fillers, or removing qualifications.

## Audit verdict: repair the Eleven transport before comparing providers

The first Eleven calibration was technically valid but was not a fair test of the approved
performance direction. Its transport space-joined each canonical `W` slice and sent only the words,
model, voice, and voice settings. The documented turns, energy movement, restraint, pauses, and
acting intent did not reach Eleven v3 as provider-supported direction. The owner **REVISE** result
therefore proves that the plain transport is creatively insufficient; it does not prove that the
locked script is wrong or that Eleven v3 cannot perform the episode.

The corrected Eleven comparison path must:

- reconstruct the exact canonical words while inserting only frozen, allowlisted, non-spoken v3
  tags at approved `W` boundaries;
- preserve a separate hash for canonical spoken text and provider transport text;
- keep E1/E2 text, tags, model, voice, and settings identical, varying only seed/generation;
- treat seed as best-effort rather than deterministic reproduction;
- respect the current 5,000-character v3 request limit; and
- avoid claiming v3 request stitching. The current 18,434-character full-control transport needs
  at least four independent parts, so full-length identity and prosody continuity remain unproven
  until the separately authorized long-form test.

Hume Octave 1 is the selected challenger, not a presumed winner. It is suitable for this test
because the utterance text stays separate from a natural-language acting description, continuation
is documented, and WAV/48 kHz PCM output is available. Octave 1 does not provide the Octave 2 word
timestamps, so every Octave 1 result requires local forced alignment against canonical `W`; raw
provider timing cannot be assumed.

This audit verdict makes the short round deliberately asymmetric in transport but symmetric in
intent: Eleven receives the corrected v3-native expression of the envelope; Hume receives the same
envelope through its separate description field. Neither provider receives different words or
different creative goals.

## Provider capability boundary

The bakeoff compares the current ElevenLabs path with one Hume clone made from an owner-controlled
original human recording. Product capabilities are live references, not permanent V2 canon.

| Area | ElevenLabs boundary | Hume boundary | V2 consequence |
| --- | --- | --- | --- |
| Direction | Eleven v3 supports model-specific audio tags inside its text input. Tags must be allowlisted and must not become spoken words. | Hume separates utterance text from a natural-language description. | The canonical performance envelope stays provider-agnostic. Each adapter records its translation and unsupported controls. |
| Exact input | Eleven v3 currently documents a 5,000-character request limit. | Hume currently documents 5,000 text characters and 1,000 description characters per utterance. | Every candidate uses the same exact `W` ranges. Provider limits may change chunking, never words. |
| Reproducibility | A supplied seed is best-effort, not a deterministic waveform guarantee. | Candidate identity must record the exact model, voice, description, settings, and generation receipt. | Reproducibility means a frozen request envelope and immutable result, not byte-identical regeneration. |
| Output | The TTS endpoint exposes PCM and MP3 output formats. | The synthesis endpoint documents WAV, 48 kHz PCM, and MP3 output. | Request provider-native PCM or PCM WAV first. A lossy exception is narrow and explicit. |
| Clone/source | The existing OE comparison voice is present in the owner's account. Read-only metadata and original-sample retrieval still require separate authority. | Public audio-sample cloning guidance currently describes the Hume Platform upload flow. The public Create Voice API saves from a TTS `generation_id`; it is not a public human-audio upload-clone API. | Hume sample upload and one clone creation are treated as a UI-mediated external action with a receipt. Logged-in browser state is not authority. |
| Commercial use | Rights and the active paid account terms must be verified for the selected voice and production use. | Commercial use requires an eligible paid tier; Free and Starter are not accepted for OE production. | Unresolved consent, ownership, tier, or commercial-use terms are hard failures before scoring. |
| Timing/continuity | Eleven v3 does not use the documented request-stitching path; the 18,434-character control therefore needs at least four independent parts. | Hume continuation is documented. Word timestamps are Octave 2-only; this Octave 1 test requires forced alignment. | Final Step 2 timing still comes from the edited narration master, never raw provider timing. |

Current official references reviewed for this proposal:

- ElevenLabs: [TTS API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert),
  [Eleven v3](https://elevenlabs.io/docs/models#eleven-v3),
  [prompting principles](https://elevenlabs.io/docs/best-practices/prompting),
  [v3 creative playground](https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech),
  [request stitching guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/request-stitching),
  [voice metadata](https://elevenlabs.io/docs/api-reference/voices/get), and
  [original sample audio](https://elevenlabs.io/docs/api-reference/voices/samples/get).
- Hume: [TTS overview](https://dev.hume.ai/docs/text-to-speech-tts/overview),
  [acting instructions](https://dev.hume.ai/docs/text-to-speech-tts/acting-instructions),
  [continuation](https://dev.hume.ai/docs/text-to-speech-tts/continuation),
  [JSON synthesis endpoint](https://dev.hume.ai/reference/text-to-speech-tts/synthesize-json),
  [file synthesis endpoint](https://dev.hume.ai/reference/text-to-speech-tts/synthesize-file),
  [voice-cloning guide](https://dev.hume.ai/docs/voice/voice-cloning),
  [Create Voice API](https://dev.hume.ai/reference/voices/create), and
  [pricing and commercial-use boundary](https://www.hume.ai/pricing).

The compiled Hume calibration request uses `POST /v0/tts` JSON with `num_generations: 2`; the file
endpoint is retained only as an additional output-format reference. Recheck these live documents
and the active account terms before any authorization. A documentation
URL does not prove that the owner's account has a capability or that an output is commercially
licensed.

## Provider-agnostic performance envelope

The performance envelope is the creative control shared by every candidate. It contains only
nonlexical intent:

- listener and narrator relationship;
- central promise and final landing;
- baseline identity, trust, warmth, restraint, pace, and energy range;
- argument-mode turns: diagnose, prove, teach, warn, and invite;
- required contrast between the cold open, proof, economics, risk, and final case;
- emphasis, de-emphasis, pause function, and comprehension space;
- pronunciation intent for names, acronyms, numbers, and technical terms;
- anti-targets such as trailer voice, announcer cadence, flat synthetic reading, false intimacy,
  and motivational uplift; and
- continuity and pickup expectations.

The envelope must not contain Eleven tags, Hume descriptions, provider IDs, model settings, or
replacement prose. Each provider receives a separately hashed adapter that translates the same
envelope into supported controls. The adapter records every unsupported instruction rather than
simulating it with additional spoken text.

Materially changing the envelope or tuning only one provider after listening invalidates the round.
Both providers must be rerun under a new, equally bounded round authorization.

## Original-sample provenance and retrieval gate

Hume clone creation is blocked until one original human recording is proven to be:

- Manav's own voice or otherwise explicitly owned and consented for this use;
- an original recording, not TTS output, a generated remix, a YouTube rip, a mastered episode mix,
  or an unknown derivative;
- retrieved through an authorized read-only path or matched to an independently held original;
- preserved byte-for-byte outside Git under the approved local-media policy;
- inspected for actual container, codec, sample rate, bit depth when meaningful, channels, duration,
  clipping, processing, and background content;
- registered with source account, voice ID, provider sample ID when exposed, original filename when
  exposed, retrieval time, SHA-256, and custody path; and
- accompanied by an owner consent and commercial-use record.

If ElevenLabs exposes metadata but not the original sample bytes, or if the retrieved bytes cannot
be tied to the owner and existing voice, stop. Do not substitute a generated sample or scrape audio
from another surface. Unknown provenance is a rights failure, not an invitation to approximate.

The read-only selector must resolve exactly one original sample before retrieval. Zero samples
blocks the gate. More than one candidate sample also blocks the gate until the owner issues a new
authorization naming the exact sample ID; an agent may not choose among several recordings. A
sample with multiple speakers, synthetic speech, or ambiguous human provenance may be retained only
as blocked evidence. It cannot advance to Hume upload or clone creation.

## Four separately authorized external actions

The initial bakeoff requires four distinct, human-approved authorization records. They may not be
combined, inferred from login state, or reused.

### AUTH-01 — ElevenLabs read-only voice metadata and original-sample retrieval

Machine scope: `elevenlabs_sample_retrieval`.

Allowed only:

- read metadata for the exact existing OE voice ID;
- enumerate its provider sample identifiers when exposed; and
- retrieve the exact authorized original sample bytes when the account and documented interface
  support retrieval.

Not allowed: TTS generation, voice edit, deletion, retraining, remixing, cloning, sample upload,
or changing account state. The authorization names exact read-call and download ceilings, expires,
and is consumed when the retrieval attempt begins. An unavailable download is recorded as blocked;
it is not retried through an undocumented route. The bounded runner stores raw bytes only in
ignored local media and leaves identity, originality, and single-speaker approval pending until a
human listens to the retrieved sample.

If AUTH-01 stops because the bound voice exposes multiple samples, do not weaken its selector and
do not reuse it. A separately approved corrective action may use machine scope
`elevenlabs_sample_metadata_inventory` to make one metadata request and preserve a safe sample
inventory for the owner. That action allows zero selection, zero downloads, zero generation, zero
spend, and no Hume access. A later download still requires a new authorization naming one exact
sample ID.

### AUTH-02 — Hume UI sample upload and one clone creation

Machine scope: `hume_clone_creation`.

Allowed only after the provenance gate passes:

- upload the one hash-bound original sample through the documented Hume Platform flow; and
- create exactly one named clone tied to that sample.

Not allowed: narration synthesis, a second clone, replacing the upload, account-tier purchase,
training another person's voice, or using the public Create Voice API as if it were an audio-upload
clone endpoint. The action records the operator, start/end time, source hash, visible clone name and
ID, Hume receipt or UI evidence, terms/tier check, and any uncertain external state. The user's
existing logged-in Hume browser session is access context only, not upload or clone authority.

### AUTH-03 — ElevenLabs short calibration, two passages by two generations

Machine scope: `elevenlabs_calibration`.

Allowed only:

- one frozen Eleven request envelope producing candidates E1 and E2 from separate generations;
- the same two exact `W`-bound passages for each candidate;
- four planned outputs total, plus only the explicitly capped PCM-capability fallbacks; and
- immutable raw responses and credential-free receipts.

No creative retry, pickup, third passage, long-form generation, voice change, or full capture is
included. The authorization binds the performance envelope, provider adapter, candidate settings,
script and `W` hashes, output policy, calls, repeated character ceiling, and expiration.

### AUTH-04 — Hume short calibration, two passages by two generations

Machine scope: `hume_calibration`.

Allowed only:

- the single provenance-bound Hume clone;
- one frozen `POST /v0/tts` JSON request per passage, each with `num_generations: 2`, producing
  H1 and H2 from the same request and acting description;
- the same two exact `W`-bound passages used for Eleven, once per candidate;
- four planned outputs total, plus only the explicitly capped PCM/WAV-capability fallbacks; and
- immutable raw responses and credential-free receipts.

No second clone, creative retry, pickup, third passage, long-form generation, or full capture is
included. The v0.3 runtime can validate and compile this Hume request without credentials, including
its separate acting descriptions, `POST /v0/tts` body, `num_generations: 2`, and bounded accounting.
It has no Hume network executor, sample uploader, clone creator, or authorization consumer. Offline
compilation is not execution authority; an independently reviewed executor is required before any
provider call can occur.

## Short calibration design

The short round contains eight scored clips across two providers, two passages, and two generations:

```text
Eleven candidate E1 × passages P1 and P2
Eleven candidate E2 × passages P1 and P2
Hume candidate H1 × passages P1 and P2
Hume candidate H2 × passages P1 and P2
```

P1 tests the cold open, identity, attention, and episode promise. P2 tests the build, validation
test, final verdict, and CTA. Both passages are exact contiguous `W` ranges and include the same
punctuation and pronunciation intent for every candidate.

E1 and E2 must use identical Eleven text, tags, model, voice, and settings. They differ only by the
candidate seed/generation; the seed is best-effort and does not promise a deterministic waveform.
Within each passage, H1 and H2 must be the two generations from the same Hume `POST /v0/tts`
request, text, description, model, voice, and settings. They are not separately tuned
configurations. No candidate may receive different words, source identity, cleanup, or review
mastering.

Before listening, a curator who does not score the round:

1. verifies the hard gates;
2. creates lossless review copies using one disclosed, identical gain-only policy when needed;
3. assigns random candidate and passage codes that reveal no provider, model, settings, filenames,
   or generation order;
4. seals the mapping and raw hashes; and
5. gives scorers only the review files, scorecard, locked passage text, and provider-agnostic
   envelope.

The owner and at least one independent listener score all eight clips separately before discussion.
For each clip, its creative score is the arithmetic mean of the scorers' signed 100-point totals.
The signed scorecards stay blind and immutable. They contain no consolidation or provider identity.
Only after all scorecards are hashed does the curator bind both scorecard hashes and the sealed-map
hash in a separate consolidation record, unseal the map, and compute the candidate and provider
scores.

For each provider, select its highest-scoring hard-gate-passing generation for P1 and its
highest-scoring hard-gate-passing generation for P2. The provider short-form score is the arithmetic
mean of those two selected passage scores. A hard-gate-disqualified generation cannot be selected;
if neither generation passes for one passage, that provider is ineligible. Record the unselected
generation's failures, score spread, and output variance as operational metrics. Do not subtract
those metrics from the selected clips' creative scores.

## Hard gates before scoring

A candidate is ineligible, regardless of creative score, when any of these fail:

- narrator consent, original-sample provenance, provider tier, or commercial-use basis;
- exact target, script hash, `W` ranges, performance envelope, and authorization binding;
- zero confirmed additions, omissions, substitutions, repeats, or truncations;
- no spoken direction tags and no damaged names, numbers, negations, or qualifications;
- immutable raw, actual-format inspection, request/generation receipt, and complete custody chain;
- native PCM or PCM WAV first, or the one authorized and truthfully labeled fallback;
- no material clipping, truncation, corruption, watery consonants, brittle sibilance, synthetic
  artifacts, codec damage, or hidden postprocessing;
- the passage remains understandable without music, captions, or visuals;
- the same source identity and fair two-candidate/two-passage treatment; and
- blind-code integrity.

Diagnostic ASR may flag a mismatch but cannot clear one. A human must disposition every likely
lexical or pronunciation issue against the exact audio.

## Blind short-form score: 100 points

| Dimension | Points | What is judged |
| --- | ---: | --- |
| OE identity and trust | 25 | Experienced operator, grounded authority, no generic AI-demo or announcer character. |
| Camera-ready energy | 25 | Holds attention without trailer voice, forced excitement, or flattening the argument. |
| Documented turns | 20 | Performs the exact opening, promise, build, validation, verdict, and CTA turns in the envelope. |
| Natural, credible, and sustainable | 15 | Believable phrasing and cadence that can carry a full OE episode without synthetic fatigue. |
| Evidence, caveats, action, and verdict distinction | 10 | These modes remain audibly different and understandable without visuals. |
| Editability and pickup fit | 5 | Clean sentence landings, usable silence, stable identity, and credible same-word pickup potential. |
| **Total** | **100** | |

Every provider must have passing P1 and P2 selects and a provider short-form score of at least 80 to
be eligible. Advance the highest-scoring eligible provider to the later long-form test. Advance the
runner-up only when its provider score is within 5.0 points of the leader. If no provider reaches
80, stop: no N4A pass, long-form test, N4B full capture, or Step 3 handoff is allowed. Gemini stock
voice may then be considered as a
diagnostic only under a new, separately approved authorization; it is not a silent substitute.

## Later AUTH-05 — Long-form continuity and pickup test

Human scope: `long_form_continuity_and_later_pickup`. It is not one of the four initial machine
scope enums.

The long-form test is a fifth, later authorization created only after the blind short scores are
unsealed and the advancement rule is applied. It is not one of the initial four authorizations and
does not authorize N4B full capture.

For each advanced method, the test freezes:

- one 3.5-to-4.5-minute exact `W` range containing a conceptual transition, a dense-evidence
  passage, and a number-heavy section;
- the exact chunk/context method and one uninterrupted review assembly;
- one bounded same-word pickup recorded or generated several hours later and inserted behind a
  blind seam to test identity and join matching;
- provider-native PCM or PCM WAV first and the same strict fallback policy;
- exact call, character, spend, retry, and expiration ceilings; and
- blind review copies and a sealed identity map.

The long-form round is pass/fail confirmation, not a second score. The owner and independent
listener each complete an eyes-closed fatigue review and confirm:

- exact words, names, numbers, negations, and qualifications;
- sustained OE identity and camera-ready energy;
- conceptual, evidence, and number-heavy turns;
- naturalness and comprehension across the full range;
- no unacceptable synthetic artifact, chunk reset, or fatigue;
- a clean blind seam; and
- a matching several-hours-later same-word pickup.

The long-form hard gates still apply. A short-form score cannot waive a word error, rights problem,
format failure, authorization overrun, fatigue failure, or unusable pickup.

## Asymmetric final provider rule

The final method-selection decision deliberately favors continuity with the existing Eleven path
unless Hume proves a material improvement:

- compare only the frozen short provider scores; long-form/pickup supplies pass/fail confirmation;
- retain ElevenLabs when it is eligible, passes long-form/pickup, and its frozen short provider
  score is within 5.0 points of Hume or leads Hume;
- adopt Hume only when its frozen short provider score is at least 80 and more than 5.0 points above
  ElevenLabs, and Hume passes long-form continuity and same-word pickup; no Eleven long-form test is
  required when Eleven was more than 5.0 points behind and therefore did not advance; and
- if neither reaches 80, select neither and stop before full capture.

If the required score comparison cannot be made, or the provider favored by the rule fails its
long-form/pickup confirmation, select neither rather than inventing a new exception.

The owner signs the provider-method selection after unblinding. That selection freezes an N3
candidate configuration only. It does not set `creative_approved`, pass N4A, authorize long-form
retries, grant N4B full-capture authority, create a narration lock, or permit Step 3.

After method selection, N4A still requires the owner to approve the chosen calibration performance
against the frozen configuration. N4B then requires a new, separate full-capture authorization.

## Required v0.3 records

- provider-agnostic performance envelope and hash;
- original-sample provenance and retrieval record;
- four initial authorization records and four independent consumption/outcome receipts;
- Eleven and Hume provider-adapter records;
- candidate plan with exact `W` ranges and equal-treatment declaration;
- immutable raw take register and source-format inspection;
- sealed blind-code map held outside scorer packets;
- two immutable signed blind short-form scorecards;
- separate curator consolidation binding both scorecard hashes and the sealed-map hash;
- later AUTH-05 and blind long-form/pickup pass-fail reviews when authorized;
- provider-method selection record; and
- explicit N4A status that keeps technical and owner creative decisions separate.

No credential, original sample, cloned-voice media, provider output, or other large/sensitive audio
belongs in Git under the current repository policy. Version only safe metadata, hashes, receipts,
decisions, and local or approved-store locators.
