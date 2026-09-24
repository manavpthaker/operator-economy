# Operator Economy Narrator Profile

Status: retained Step 2 v0.2 ElevenLabs baseline under proposed v0.3 provider review; technical
calibration passed, owner creative decision is revise; not canonical

## Boundary

This profile governs who speaks the locked words and how the audio system preserves that narrator's identity. It does not govern the script's tone, vocabulary, sentence construction, humor, or message delivery. Those word-level choices must already pass Step 1 editorial-voice conformity.

Step 2 may add non-spoken direction supported by the selected model. It may not rewrite the script to recreate Manav's language.

## Source identity

- V1 source: `studio/config/blueprint.json`
- Reviewed source SHA-256: `1a1d691561a2aac703fa3532aed48cae3c36b4f68abcda227292762c98e326f8`
- Source configuration section: `voiceover`
- Selection evidence date recorded in V1: 2026-08-19
- Source authority status: V1 production evidence; owner-selected V2 calibration baseline only

## Proposed primary narrator

- Internal name: `OE Narrator Manav IVC v1`
- Narrator represented: Manav Thaker
- Path: synthetic voice based on the owner's authorized identity
- Provider: ElevenLabs
- Voice ID: `yUXeTfC1IFOCSjGc96sQ`
- Model: `eleven_v3`
- Provider preset described by V1: Natural
- Stability: `0.5`
- Similarity boost: `0.6`
- Style: `0.1`
- Speaker-boost setting: not explicitly present in the reviewed V1 configuration
- Credentials: external secret storage only; never record them here

## V1 selection rationale retained for calibration

The current V1 note says this voice was restored after a firmer remix over-enunciated and flattened long-form delivery. The selected identity plus Eleven v3 Natural, supported emotion tags, and explicit thought-boundary pauses produced the closest tested match to Manav's conversational cadence.

That history supported testing this profile first. The retained v0.2 batch passed technical
acquisition but received an owner creative **REVISE**, so this profile is now one controlled
ElevenLabs baseline in the v0.3 bakeoff. It is not the selected production method.

## Proposed non-lexical performance rules

- Use reviewed, provider-supported vocal tags only when they clarify a real beat.
- Use selective capitalization, ellipses, punctuation, whitespace, and paragraph resets only as non-lexical direction.
- Do not add routine synthetic breaths.
- Do not add, remove, replace, or reorder spoken words.
- Generate the complete episode as one controlled batch; use several recorded requests only when
  provider limits require them and the V2 chunk/continuity protocol is followed.
- Do not regenerate one section in isolation and silently splice it into the episode.
- Never mix narrator IDs inside an episode.
- Preserve raw provider outputs, request identifiers, settings, and alignment metadata.
- Do not invoke or import V1 `studio/scripts/originate/generate_vo.py`.

## Pronunciation baseline

V1 currently records:

| Display form | Proposed spoken alias |
| --- | --- |
| Airtable | air table |
| n8n | en eight en |
| Zapier | zappier |
| SaaS | sass |
| EBITDA | ee bit dah |
| Manav | Mah-nuhv |
| MP | Em Pee |
| GenAI | Gen A.I. |

The V1 pronunciation-dictionary locator is retained as provenance, but V1 reports that Eleven v3 ignores it. Episode-specific aliases must therefore be reviewed and logged in the Step 2 capture lock without changing canonical on-screen spelling.

## Locked acquisition-format order

Request native PCM first and inspect the actual returned codec. If the current ElevenLabs account
and `eleven_v3` path cannot return native PCM, accept only the existing `mp3_44100_192` output with
fallback reason `pcm_capability_unavailable`.

The raw provider file remains immutable. A fallback MP3 must be labeled audio origin `lossy_mp3`,
pass an audible codec-artifact review, and be decoded/resampled exactly once to 48 kHz, 24-bit, mono
PCM. No later lossy intermediate is allowed. The resulting WAV is a lossless working/delivery file
with lossy origin, never native PCM acquisition.

The default delivery master remains 48 kHz, 24-bit, mono PCM WAV regardless of source origin.

## Missing approval evidence

- Original owner sample metadata and exactly-one-sample retrieval: pending separate AUTH-01
- Original owner sample path/SHA-256: pending provenance gate; audio remains outside Git
- Hume UI upload and one clone creation: pending separate AUTH-02
- Rights/consent record path: pending V2 record
- Retained v0.2 native-PCM technical calibration: pass
- Retained v0.2 owner creative calibration: revise
- Blind two-passage/two-generation Eleven/Hume bakeoff: pending AUTH-03 and AUTH-04
- Later eligible-method long-form/pickup test: pending separate AUTH-05

## Approval

- Profile decision: proposed / approved / revise / retired
- Approved by:
- Approval date:
- Approved profile SHA-256:

No provider read, sample retrieval, upload, clone, generation, or full capture is authorized by
this document. The exact v0.3 separation is defined in
[`../TOOL-AUDIT-AND-BAKEOFF.md`](../TOOL-AUDIT-AND-BAKEOFF.md). A selected method must still pass
N4A, and N4B full capture then requires a new authorization.
