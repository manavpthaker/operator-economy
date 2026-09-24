# N4A calibration technical review: AI Visibility v1.1 fixture

Status: **TECHNICAL PREFLIGHT PASS; OWNER CREATIVE LISTEN PENDING; N4A NOT PASSED**

Review date: 2026-08-23

Batch ID: `20260823T200928Z`

## Authority and frozen inputs

- N2 owner approval SHA-256: `cf83d9fe7176918bd01db011d9a4c5bc5d42309b54fca37feb9f3132917af384`
- Human N4A authorization SHA-256: `a2c25ef96a8c6506ea0262314c528a5ab379bf7770e6890f8d9aad7200ff9d44`
- Machine N4A authorization SHA-256: `b580a468dd7d97468e2dda5124b677294ed209af8e987837a729109a0099ad4b`
- Authorization-consumption SHA-256: `9884b6a1e10627bb6c7562f5f7fa9f9650ca93fa23a297f6759d7e4b15fd4cd6`
- Capture-plan SHA-256: `abccb4a507734b72ae0693ce44c4497ffc7eff6168730932a15544177375dad4`
- Step 1 script SHA-256: `74048b55ed15ed6ed679abb5a6c892def8a8a40e75e7cebeafdfde319dd67efa`
- Canonical spoken sequence: 3,019 tokens, SHA-256
  `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`
- Provider capture-run receipt SHA-256:
  `784140a2f68b287df1b01ce7ff9dadf5588788b5f0d1701d41e77ed9b19ad4a5`

The authorization was consumed before the first request and cannot be reused. The five request
envelopes were generated from the frozen token intervals. No prose review document became an
alternate source of spoken words.

An independent read-only audit rehashed the complete chain, decoded every working WAV, and verified
that converting each working S24LE file back to S16LE reproduces its immutable provider-raw SHA-256.
It found no corruption, full-scale sample, clipping, fallback artifact, or extra request.

## Bounded execution result

| Check | Result |
| --- | --- |
| Provider/model/voice | ElevenLabs / `eleven_v3` / existing OE voice `yUXeTfC1IFOCSjGc96sQ` |
| Authorized maximum | 10 calls and 16,310 attempted characters |
| Actual use | 5 calls and 8,155 attempted characters |
| Preferred format requested first | yes, for every payload |
| Actual source format | native raw PCM S16LE, 48 kHz, mono |
| MP3 fallback used | no |
| Lossy source in batch | no |
| Failed or extra request | none |
| Full capture or pickup | none |
| Credential stored in artifacts | no |
| Creative approval written by automation | no |

## Passage and conversion review

Every raw take is immutable. Each working file was created once from its matching raw PCM source as
48 kHz, 24-bit, mono PCM WAV. No resampling was required; the only representation change was the
single approved S16LE-to-S24LE WAV conversion.

| Payload | `W` interval | Tokens | Raw SHA-256 | Working SHA-256 | Duration | Pace |
| --- | ---: | ---: | --- | --- | ---: | ---: |
| C01A cold open | `[0,139)` | 139 | `34e07e0090278d5dacfae28f317f069b9da97a17ab869614b49338b63fa0d6b5` | `29008d8083a6c4cda3dc7503bff4b34bd40f39e6b6964726c836f8cf065cac4d` | 56.16 s | 148.5 wpm |
| C01B post-sting promise | `[139,236)` | 97 | `6a716c6aad54c85e42d1fa095ce0f74f4e9a69d69c24aba7905080d43dae8a8b` | `f8ae4b2315b468a30a1255b1ca94bb51d6ba953a97f627693ee55941ef5f5b29` | 40.24 s | 144.6 wpm |
| C02 dense evidence | `[236,544)` | 308 | `e4a244f51ea448511f3a8347fdac192c6213ade2c4168d63990906867709a7f4` | `984e228be7403df448ac50fd26e39ab127c4161707d818f76bd96a8eea9e66cc` | 131.68 s | 140.3 wpm |
| C03 economics | `[2111,2462)` | 351 | `2b53842f3b93a95cf719e50f7e9ee0ea46c3a9220275d068dd0022eac704b4ae` | `8e06efa9eda5538876fb65b026e353b41b65e770aa08fa0d92d8f07889fc7dba` | 193.44 s | 108.9 wpm |
| C04 pronunciation | `[890,1326)` | 436 | `de57bc92b3e4e7215f8b5d40ff899b50211d38379b48bdcce3c0483e03a6954f` | `1370f4c30a2b1b7685850e447a6726a6c1f4f980cf5a18fb862c2aefcc0f0597` | 199.68 s | 131.0 wpm |

## Signal checks

| Payload | Integrated loudness | Loudness range | True peak | Silence at least 0.75 s | Decode/format |
| --- | ---: | ---: | ---: | ---: | --- |
| C01A | -15.9 LUFS | 3.4 LU | -0.5 dBFS | 0 | pass |
| C01B | -16.3 LUFS | 2.3 LU | -0.7 dBFS | 0 | pass |
| C02 | -16.4 LUFS | 3.9 LU | -0.4 dBFS | 0 | pass |
| C03 | -17.0 LUFS | 4.9 LU | -0.4 dBFS | 0 | pass |
| C04 | -15.7 LUFS | 2.7 LU | -0.3 dBFS | 0 | pass |

All five WAVs decode without error and match the required 48 kHz, 24-bit, mono PCM working format.
No sample or true peak reaches 0 dBFS. The files have limited peak headroom but are unmastered
calibration sources; final gain and mix decisions are outside N4A.

No local ASR engine was available, so no diagnostic transcript was produced. This is not treated as
proof of a word mismatch or as proof of lexical performance. The exact request envelopes pass; the
owner must still listen for omissions, substitutions, repeats, pronunciation errors, and unnatural
delivery.

## Owner-listen watches

- Does C01A earn attention immediately and tease the business payoff before the silent sting?
- Does C01B resume as the same narrator, and does the brand string sound natural rather than read?
- Does C02 keep the source qualifications audible while remaining conversational?
- Does C03 make each model case and uncertainty boundary understandable without sounding lethargic?
- Does C04 pronounce every named company, technical phrase, and number naturally and accurately?
- Across all five, does this sound like the intended Operator Economy narrator rather than generic
  synthetic documentary VO?

Machine silence detection found no pause of 0.75 seconds or longer inside any take. That is not a
technical failure, but it makes pacing and breathing an explicit creative-listen item. The S01 sting
gap is editorial silence and was correctly not synthesized.

The audio files total approximately 142 MB. They remain in the local fixture worktree and are
excluded from Git under `calibration/.gitignore`, consistent with the repository's existing policy
against committing large generated media. The small authorization, capture, conversion, and review
receipts remain versionable. No audio file should be deleted or regenerated while the owner decision
is pending.

## Decision

- Immutable raw acquisition and provenance: pass
- PCM-first source policy: pass
- One-conversion working format: pass
- Decode, channel, sample-rate, bit-depth, and no-clipping checks: pass
- Exact provider request envelopes: pass
- Audible lexical and pronunciation conformity: pending owner listen
- Intended voice, pacing, mode contrast, and continuity: pending owner listen
- Technical recommendation: **PASS TO OWNER LISTEN**
- Owner creative decision: **PENDING**
- N4A gate: **PENDING**
- Full-capture authorization: **NOT GRANTED**
- Step 2 lock: **NOT GRANTED**
- Step 3 authority: **NOT GRANTED**
