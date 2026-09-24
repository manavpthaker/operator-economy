# Voice and capture lock: AI Visibility v1.1 fixture

Status: N3 calibration configuration frozen; no external call authorized.

Lock revision: `ai-visibility-step2-n3-v0.2-preflight`

Episode: none; unassigned fixture

## Identity and authorization boundary

- Primary narration path: synthetic
- Narrator identity: `OE Narrator Manav IVC v1`
- Identity represented and owned by: Manav Thaker
- Voice ID: `yUXeTfC1IFOCSjGc96sQ`
- Third-party imitation or cloning: no
- Selection basis: the owner chose the existing OE voice for this Step 2 test
- Technical source: `studio/config/blueprint.json`, SHA-256 `1a1d691561a2aac703fa3532aed48cae3c36b4f68abcda227292762c98e326f8`
- Lexical speech-profile source: `studio/config/speech-profile.md`, SHA-256 `75913da0bc5d5b360c88f18c70b60d8d4af14128184e8164872edd56f71ceddc`
- External call authority: none; only an executed provider-call authorization can grant it

This lock records configuration. It contains no credential and does not authorize spending, generation, full capture, publication, or Step 3.

## Synthetic capture profile

| Field | Frozen value |
| --- | --- |
| Provider | ElevenLabs |
| Model | `eleven_v3` |
| Voice ID | `yUXeTfC1IFOCSjGc96sQ` |
| Stability | `0.5` |
| Similarity boost | `0.6` |
| Style | `0.1` |
| Speaker boost | unspecified; do not infer or silently enable |
| Seed | not exposed/frozen; receipt must disclose if the provider adds one |
| Preferred request format | `pcm_48000` |
| Only permitted fallback | `mp3_44100_192` |
| Fallback reason | exactly `pcm_capability_unavailable` |
| Working and delivery container | PCM WAV, 48 kHz, 24-bit, mono |
| Full-capture strategy | one controlled episode batch after calibration approval |
| Script authority | exact `oe-spoken-text-v1` sequence only |

The actual returned codec, sample rate, channel count, bit depth, and bitrate must be inspected from the bytes. A filename or requested format is not evidence of what the provider returned.

## Strict fallback receipt

If `pcm_48000` is unavailable, `mp3_44100_192` may be accepted only when every item below is true:

1. The provider capability failure or rejection is recorded with the request time and non-secret account/model context.
2. The raw MP3 is stored unchanged before any processing and receives a SHA-256.
3. The receipt records provider job/request ID, exact payload hash, voice, model, all material settings, requested format, observed codec, observed sample rate, observed channels, and observed bitrate.
4. The origin is recorded as `lossy_mp3`, with reason `pcm_capability_unavailable`.
5. The MP3 is decoded and resampled exactly once to 48 kHz, 24-bit, mono PCM WAV.
6. Every later edit and intermediate remains PCM/lossless. No intermediate MP3 or AAC may re-enter the edit chain.
7. The working WAV remains labeled `lossy_origin: true`. It is never described as native PCM or restored fidelity.
8. Calibration includes an audible check for watery consonants, brittle sibilance, pre-echo, pumping, smeared room tone, and pickup mismatch. Any material artifact blocks the take.

No other lossy format, bitrate, or silent provider fallback is permitted.

## Exact-word and direction contract

- The legacy `studio/scripts/originate/generate_vo.py` path is prohibited for this fixture because Step 2 cannot permit a post-lock rewrite.
- Only the locked spoken sequence may reach the provider.
- Nonlexical direction may control pace, pauses, energy, restraint, emphasis, and supported vocal treatment.
- Performance tags, punctuation, capitalization, whitespace, pronunciation aliases, and context must be proven nonlexical before use.
- Context may help continuity but may not be rendered as additional speech.
- A word addition, removal, replacement, reorder, repeat, or truncation fails lexical conformity.

## Pronunciation lock for calibration

| Canonical form | Calibration direction | State |
| --- | --- | --- |
| McKinsey | `mih-KIN-zee` | supplied by Step 1 handoff |
| Accenture | `AK-sen-chur` | supplied by Step 1 handoff |
| Semrush | verify the company's common spoken form without changing the word | pending calibration |
| ChatGPT | verify natural letter-name treatment | pending calibration |
| Gemini | verify natural product-name treatment | pending calibration |
| Perplexity | verify stress and intelligibility | pending calibration |
| AirOps | verify natural company-name treatment | pending calibration |
| iPullRank | verify natural company-name treatment | pending calibration |
| generative-engine optimization | preserve all words; test mouth comfort | pending calibration |
| `443.6 million`, `10 million`, `18.45`, `19` | group deliberately; preserve every qualifier and boundary | pending calibration |

Any alias is stored separately from canonical display text and must preserve the same intended word identity.

## Continuity and recalibration

The following changes return the fixture to N3 and require a fresh four-mode calibration: narrator/voice ID, provider, model/version, stability, similarity, style, speaker boost, seed behavior, source-format policy, pronunciation strategy, or material context/chunking method.

A same-word pickup must use the frozen configuration. If it does not match, regenerate a larger bounded passage; do not conceal a voice change with processing.

## N3 disposition

- Existing OE narrator selected by owner: yes
- Configuration frozen for the proposed calibration: yes
- PCM-first and strict MP3 fallback frozen: yes
- Provider credential stored here: no
- Provider call authorized: no
- Calibration audio approved: no; not generated
- Full capture authorized: no

Decision: **N3 CONFIGURATION PREFLIGHT PASS; EXTERNAL CALL REMAINS BLOCKED.**
