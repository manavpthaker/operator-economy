# N3 Narrator Identity and Acquisition Configuration Freeze

Template: `../../02-direction/VOICE-AND-CAPTURE-LOCK.template.md` (proposed Step 2 v0.3)

This is the N3 configuration freeze for the **two-stage acted-guide method**. It makes calibration
reproducible. It does not approve a performance and does not authorize an external provider call.

## Method selected

The owner rejected direct ElevenLabs v3 generation on Saved-C at N4A on 2026-08-25 with the exact
decision `reject both. they are both flat theres no inflection or emotion`. The replacement method
separates **performance** from **identity**, because Google's TTS exposes a natural-language acting
field and ElevenLabs Voice Changer does not:

```text
locked W range
  -> Google Cloud TTS gemini-2.5-pro-tts (voice Achird) + frozen candidate-C acting direction
  -> original 24 kHz mono PCM WAV guide           [performance]
  -> ElevenLabs Voice Changer eleven_multilingual_sts_v2 onto Original C
  -> 48 kHz mono PCM output                        [identity]
```

Owner method selection recorded 2026-08-28: `C is right`.

### Measured basis for the selection

Executed end-to-end on 2026-08-28 over exact `W[30,110)`:

| Measure | Value | Meaning |
| --- | --- | --- |
| Transfer vs its own guide, envelope correlation | `+0.899` | Voice Changer preserves the performance |
| Dynamic range (CV), guide -> transfer | `0.838 -> 0.838` | The transfer does not flatten |
| Duration, guide -> transfer | `27.731s -> 27.771s` (+0.14%) | Timing is preserved |

This establishes that the 2026-08-25 flatness originated in ElevenLabs v3 *generating* the read, not
in the transfer step. It is technical evidence only; it is not an N4A creative approval.

## Identity and authorization

- Fixture: `step2-v0.5-ai-visibility-v1.1-synthetic-guide-to-saved-c-transfer-microtest`
- Canonical source: AI Visibility v1.1 under `oe-spoken-text-v1`
- Configuration revision: `n3-two-stage-acted-guide-v2` (supersedes v1, 2026-08-30)
- Full `W` identity: 3,019 tokens, SHA-256 `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`
- Calibration range in this freeze: exact absolute half-open `W[30,110)`, 80 tokens
- Locked transport (465 chars) SHA-256: `db3ccbb400f6bde4099f08b79b4402c374577cae4e622b0087649482e4f7d1cb`
- Provider-agnostic performance envelope: `performance-envelope.json` SHA-256 `3621352c6772404938f0701eb7db242c9113153f3755da520e0a6d3a6e668b88`
- Narrator-profile path: `../../02-direction/OE-NARRATOR-PROFILE.md` SHA-256 `473d4152f373d51e88ca8a427414aa320a84537a9fe0a76607e7b2adcd85a2ac`
  - **Superseded for method.** That profile freezes the direct `eleven_v3` path on `yUXeTfC1IFOCSjGc96sQ`
    which received an owner creative REVISE. Its pronunciation baseline and acquisition-format order
    are retained below; its provider/model/settings are not.
- Primary narration path: **synthetic**
- Narrator represented: Manav Thaker
- Authorized voice identity: `scMbPZwQjr40V1MzL3Nj` — `OE Narrator Manav C Base v1` ("Original C")
- Original C provenance: ElevenLabs Voice Remix of source voice `yUXeTfC1IFOCSjGc96sQ`,
  owner-selected 2026-08-25T10:20:40Z, selected audio SHA-256
  `d46f8335e71bac3cf6c2b6396d3da7bdab4d82bd11db64f696fda8b5ede18392`
- Identity owner / voice custodian: Manav Thaker
- Third-party imitation or cloning: **no** — the identity is the owner's own

## Synthetic capture profile — Stage 1 (guide, performance)

- Provider: Google Cloud Text-to-Speech
- Endpoint: `POST https://us-texttospeech.googleapis.com/v1/text:synthesize`
- Model: `gemini-2.5-pro-tts`
- Voice: **`Algieba`**, language `en-US` (owner-selected 2026-08-30, supersedes `Achird`)
  - The guide voice carries performance only. Narrator identity comes from the Stage 2 transfer onto
    Original C, so changing it does not change who the audience hears.
- Acting direction: **candidate C4**, `../../prompts/NARRATOR-REGISTER.candidate-C4.google-gemini-tts.style-instructions.json`
  - record SHA-256 `b747d7b0afa4469b2be05c20eb16306a25bb5185b9fa8b12e2d4aa4ddd8d3efc`
  - `style_instructions` 961 UTF-8 bytes, SHA-256 `f20d010c0e8ec5129ea7a7bf088e25f34a92a9ef05fca108618ae060b245e8d5`
  - **Method-level register, passage-independent.** Supersedes candidate C, which named phrases
    occurring only in P01 (see `N4A-RESULTS.md` F5). Pronunciation aliases attach per passage only
    where the display form occurs; the composed prompt hash is recorded per chunk.
  - carried in `input.prompt`; the locked words are carried in `input.text` and are never modified
- `advancedVoiceOptions.enableTextnorm`: `false`
- Requested native acquisition: `LINEAR16`, 24 kHz, mono — provider-native PCM WAV
- Compact request body for this range: 1,687 bytes, SHA-256 `41f4fc82edbacd333e066a4e0e9e535744cd049285f9953fc1b198592c6acaee`
- Generation is unseeded and stochastic; each call is a distinct performance
- Auth: ADC. **`x-goog-user-project` is mandatory.** Without it `texttospeech.googleapis.com`
  returns `403 PERMISSION_DENIED / SERVICE_DISABLED`, which is the previously unexplained cause of
  the 2026-08-25 G1 and 2026-08-26 G1R1 failures. The authoritative value is `quota_project_id` in
  the ADC file (`operator-economy`), not `gcloud config get-value project`, which is unset here.

## Synthetic capture profile — Stage 2 (transfer, identity)

- Provider: ElevenLabs Voice Changer (speech-to-speech)
- Endpoint: `POST https://api.elevenlabs.io/v1/speech-to-speech/scMbPZwQjr40V1MzL3Nj`
- Model: `eleven_multilingual_sts_v2`
- Seed: `2026082501` (best-effort; the provider does not guarantee determinism)
- Voice settings: `{"similarity_boost": 0.8, "speed": 1.0, "stability": 0.4, "style": 0.0, "use_speaker_boost": true}`
- `remove_background_noise`: `false`; `file_format`: `other`
- Requested native acquisition: `pcm_48000` (raw PCM, wrapped locally into 48 kHz mono WAV)
- Input must be the **exact original Google provider WAV bytes**. A listening derivative is ineligible.
- Voice Changer has no acting field: the performance must already exist in the guide.

## Acquisition-format and raw-evidence contract

- Actual returned codec inspected rather than inferred: **yes**
- Native output preserved byte-for-byte before processing: **yes** (raw provider bytes written first, mode 0600)
- Permitted fallback: `mp3_44100_192` only, reason `pcm_capability_unavailable` only
- Fallback requires an audible codec-artifact review and exactly one decode/resample: **acknowledged**
- Lossy intermediates after native acquisition are prohibited: **acknowledged**
- A PCM WAV derived from MP3 stays labeled lossy-origin and is never native PCM: **acknowledged**
- Audio origin vocabulary for this method: `native_pcm` at both stages
- Delivery working/master format: PCM WAV / 48 kHz / 24-bit / mono
  - Note: Stage 2 returns 48 kHz **16-bit**. Promotion to the 24-bit delivery master is a single
    lossless width conversion, recorded as such. It is not a second acquisition.

## Context and chunking method

The full `W` identity (3,019 tokens) exceeds one comfortable guide request, so a capture batch
contains several requests. This method has **two stochastic stages per chunk**, so continuity is the
main risk and the rules are stricter than under the single-stage profile:

- Chunk only on Step 1 narration-block boundaries. Never split a sentence or a numbered claim.
- Size chunks by **expected spoken duration, not character count**. The provider ceiling is roughly
  75-78 seconds of generated audio (finding F1); measured rate is ~15.5 characters of locked text per
  second across both guide voices, number-dense copy included. Target <=65s per chunk.
- Merge any trailing chunk shorter than ~15 seconds into the previous chunk (finding F2). An isolated
  short tail is a near-contextless generation and lands at its own level: M4's 3.65s tail sat 2.1 dB
  hot against its own mode.
- Every chunk in a batch uses byte-identical style instructions, model, voice, settings, seed,
  sample rate, and adapter. Only the `input.text` range differs.
- Every chunk records: batch ID, request ID, chunk ID, exact ordered `W` range, and both provider
  response identifiers.
- A chunk is regenerated only as a whole chunk, under the same frozen envelope.
- A synthetic pickup is not an isolated convenience edit; it follows the approved continuity
  protocol and requires a full-run continuity listen before the batch is accepted.
- Guide and transfer stages are paired per chunk. A guide is never transferred with settings that
  differ from the batch freeze.

## Pronunciation-alias method

Retained from the narrator profile; carried in the acting direction, not by dictionary, because
provider dictionaries are not reliably honored on this path:

| Display form | Spoken alias |
| --- | --- |
| Airtable | air table |
| n8n | en eight en |
| Zapier | zappier |
| SaaS | sass |
| EBITDA | ee bit dah |
| Manav | Mah-nuhv |
| MP | Em Pee |
| GenAI | Gen A.I. |

Range-specific alias in this freeze: `2022` -> `twenty twenty-two` (present in the candidate-C
direction). Aliases never change canonical on-screen spelling or the locked words.

**Open:** exact-word and `twenty twenty-two` confirmation for `candidate-C.01.wav` requires human
review. Offline ASR is diagnostic and cannot clear exact words.

## Continuity contract

- Approved narrator reference: Original C selected audio SHA-256 `d46f8335e71bac3cf6c2b6396d3da7bdab4d82bd11db64f696fda8b5ede18392`
- Tone and pace reference: **M3, economics and uncertainty** —
  `outputs/raw/n4a/M3/N4A-M3.saved-c.master.wav` SHA-256
  `2f9e21d28b90` (owner-selected 2026-08-30; 107.5s, 132 wpm, dynamic range CV 0.917, 0.9 dB chunk
  spread). Supersedes the 27-second `candidate-C-to-saved-c.wav` microtest as the continuity anchor.
- Full-run continuity listen before batch acceptance: **required**
- Prohibited substitutions: any other voice ID, any fallback voice, any direct-TTS generation on
  Original C, and any invocation or import of `studio/scripts/originate/generate_vo.py`
- Changes that return the work to N3: narrator or voice ID, either provider or model, the style
  instructions, any exposed generation setting, seed policy, sample rate, bit depth, channel count,
  requested output format, or the chunking rule

## External-action boundary

- Separate calibration (N4A) authorization required: **yes**
- Separate full-capture (N4B) authorization required: **yes**
- This document grants provider-call authority: **no**
- This document grants upload, clone, long-form, N4B, Step 2 lock, or Step 3 authority: **no**
- Legacy `studio/scripts/originate/generate_vo.py` invocation/import prohibited: **acknowledged**

## Execution tooling

Calibration runs on `../../tools/calibrate.py` (SHA-256
`bb5f09764cc68a4553a274d400b870429b87d0676d6e1377cefae92f2c2f4a52`), plain casting-loop tooling with
no authorization latch or evidence chain. It reproduces the frozen request identities above and
fully drains each response body before writing.

The governed runtime `oe_narration/voice_transfer.py` is **not usable for calibration**: it is
hardcoded to `SELECTED_GUIDE_PATH = .../candidate-B.wav` and enforces
`TRANSFER_MAX_OUTPUT_DURATION_SECONDS = 50.0` with `_TRANSFER_WORKER_RESULT_BODY_MAX_BYTES = 4_800_000`
(exactly 50.0s at 48 kHz/16-bit). No calibration mode fits. Generalizing it is deferred to N4B.

## Rights and consent

The prior record `AUTH-R2-20260825T102051Z-source-voice-rights-and-consent.json` covered only a
one-time voice save and explicitly recorded `directed_tts_permitted: false`,
`full_episode_capture_permitted: false`, and `any_other_provider_disclosure_or_upload: false`. It
does not cover this method and is superseded for this configuration revision.

Renewed owner rights and consent were granted on 2026-08-28 by Manav Thaker, owner of the
represented identity, covering:

1. disclosure of the locked script text to Google Cloud Text-to-Speech for guide generation;
2. upload of Google-generated guide audio to ElevenLabs Voice Changer; and
3. generation on Original C `scMbPZwQjr40V1MzL3Nj` by speech-to-speech transfer.

Owner statement of record: `rights are approved, run the four calibration modes`.

Scope limits carried forward unchanged: the voice represents the owner's own identity, no
third-party imitation, no public sharing of the voice asset, and the incumbent source voice
`yUXeTfC1IFOCSjGc96sQ` remains unmodified. This grant covers N4A calibration under this exact
configuration revision. N4B full capture still requires its own separate authorization.

## Gate N3 configuration decision

- Configuration frozen: **yes**
- Method selected by owner: **yes** — `C is right`, 2026-08-28
- Rights basis verified for calibration: **yes** — granted 2026-08-28, this section
- This document grants provider-call authority: **no** — N4A is separately bounded below
- N3 gate result: **passed** for revision `n3-two-stage-acted-guide-v2` (v1 superseded 2026-08-30)
- Workflow outcome: `in_progress` — **N4A passed 2026-09-01** under this revision. Both technical
  and creative decisions are recorded against the same four-mode set; see `N4A-RESULTS.md`.
- Owner: Manav Thaker
- Voice custodian: Manav Thaker
- Approval date: 2026-08-28
- Exceptions: none claimed

## N4A calibration scope authorized under this freeze

Four modes, cut on Step 1 narration-block boundaries per the chunking rule above, against canonical
`W` SHA-256 `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`:

| Mode | Purpose | Block(s) | Range | Tokens |
| --- | --- | --- | --- | ---: |
| M1 | cold open and episode promise | S00 + S02 | `W[0,236)` | 236 |
| M2 | dense evidence | S05 | `W[890,1326)` | 436 |
| M3 | economics and uncertainty | S08 | `W[1875,2111)` | 236 |
| M4 | names, numbers, acronyms, pronunciation | S09 | `W[2111,2462)` | 351 |

One guide generation and one transfer per mode. No retry, redirect, fallback, alternate model, or
alternate voice. Passage hashes are recorded in `N4A-RESULTS.md`.
