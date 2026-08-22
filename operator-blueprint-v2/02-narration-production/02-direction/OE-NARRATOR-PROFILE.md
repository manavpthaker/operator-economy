# Operator Economy Narrator Profile

Status: proposed Step 2 calibration baseline; not yet owner-approved or canonical

## Boundary

This profile governs who speaks the locked words and how the audio system preserves that narrator's identity. It does not govern the script's tone, vocabulary, sentence construction, humor, or message delivery. Those word-level choices must already pass Step 1 editorial-voice conformity.

Step 2 may add non-spoken direction supported by the selected model. It may not rewrite the script to recreate Manav's language.

## Source identity

- V1 source: `studio/config/blueprint.json`
- Reviewed source SHA-256: `1a1d691561a2aac703fa3532aed48cae3c36b4f68abcda227292762c98e326f8`
- Source configuration section: `voiceover`
- Selection evidence date recorded in V1: 2026-08-19
- Source authority status: V1 production evidence; proposed V2 calibration baseline

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

That history supports testing this profile first. It does not replace a fresh V2 calibration and owner listen.

## Proposed non-lexical performance rules

- Use reviewed, provider-supported vocal tags only when they clarify a real beat.
- Use selective capitalization, ellipses, punctuation, whitespace, and paragraph resets only as non-lexical direction.
- Do not add routine synthetic breaths.
- Do not add, remove, replace, or reorder spoken words.
- Generate a complete episode as one controlled batch while the selected model lacks reliable request stitching.
- Do not regenerate one section in isolation and silently splice it into the episode.
- Never mix narrator IDs inside an episode.
- Preserve raw provider outputs, request identifiers, settings, and alignment metadata.

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

## Acquisition-format issue to test

The V1 configuration requests `mp3_44100_192`. That is the current source format, not an approved V2 production-master standard. The V2 proposal calls for a 48 kHz, 24-bit mono WAV narration master, but transcoding a lossy 44.1 kHz MP3 does not restore source fidelity.

Before Step 2 is approved, calibration must decide whether the provider can supply an acceptable PCM source under the current account and model. If not, the V2 master must disclose the actual acquisition format rather than implying native 48 kHz, 24-bit quality.

## Missing approval evidence

- Owner-selected reference clip and SHA-256: pending
- Rights/consent record path: pending V2 record
- Fresh cold-open calibration: pending
- Dense-evidence calibration: pending
- Economics/uncertainty calibration: pending
- Pronunciation calibration: pending
- Source-format decision: pending

## Approval

- Profile decision: proposed / approved / revise / retired
- Approved by:
- Approval date:
- Approved profile SHA-256:

No provider call is authorized by this document.
