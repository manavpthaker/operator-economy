# N3 configuration freeze: EP008

Status: **frozen** by reuse of the approved method, 2026-09-03

Episode: EP008

Locked script: `../01-editorial/editorial-lock.md` / `76e41bfd02883e7f199d976440fe5e262e8b74d13f4a8e8b5f7b4750eac01874`

Canonical `W`: `../01-editorial/canonical-w.txt` / `ea3743bfcc6e881a96902556959d141f5a75a2288ecad713ccc6fa7ba787ca63` (3400 tokens)

## Method

`n3-two-stage-acted-guide-v2`, the method frozen at N3 and carried through EP007's N4A calibration and N4B full capture without change. Nothing in the chain below differs from EP007, so per the Step 2 invalidation rules N4A remains current and no renewed calibration is required.

| Stage | Provider and model | Identity | Settings | Native format |
|---|---|---|---|---|
| Guide performance | Google Cloud Text-to-Speech `gemini-2.5-pro-tts` | voice `Algieba`, `en-US` | candidate-C4 method-level register as the prompt; `enableTextnorm: false`; aliases attached only where a display form occurs | LINEAR16, 24 kHz, mono, 16-bit |
| Identity transfer | ElevenLabs Voice Changer `eleven_multilingual_sts_v2` | Original C `scMbPZwQjr40V1MzL3Nj` | stability 0.4, similarity 0.8, style 0.0, speaker boost on, speed 1.0, seed 2026082501, background-noise removal off | `pcm_48000` written to 48 kHz, mono, 16-bit WAV |

No lossy intermediate exists: the guide WAV is uploaded as-is and the transfer is requested as raw PCM. Delivery-master format is 48 kHz / 16-bit / mono PCM WAV, the same as EP007.

## Frozen inputs

| Input | Path | SHA-256 |
|---|---|---|
| Register prompt (candidate-C4) | `02-narration-production/prompts/NARRATOR-REGISTER.candidate-C4.google-gemini-tts.style-instructions.json` | `b747d7b0afa4469b2be05c20eb16306a25bb5185b9fa8b12e2d4aa4ddd8d3efc` |
| Provider adapters (request shapes, credentials, probes) | `02-narration-production/tools/calibrate.py` | `d59303278dbb79bef6fe0080f1d2b6c1e701e9228e95c7b3cdea4f3eec78cc00` |
| N4B executor (chunking, W verification, completeness gating, register) | `02-narration-production/tools/capture_n4b.py` | `92cb89dfb0f2ae971755fce63e8d7b1c3b095d9c3b031920149edc91c3694495` |

## Chunking and session rule

Chunks group whole Step 1 narration blocks (scenes) up to 1,250 characters, never splitting a block unless it alone exceeds the ceiling, in which case it is split on sentence ends into balanced `.1/.2` parts, with the F2 short-tail merge. The silent identity sting (S01) is not captured; its room is inserted at N5. Planned for EP008: **21 chunks, 42 provider calls minimum**.

## Completeness contract at capture

Every chunk must decay into silence at both stages: tail energy (RMS of the final 60 ms over peak) below 0.02. A chunk still sounding at its final sample is regenerated, up to four attempts per stage, before the run stops for review. Accepted raw files are immutable, hashed, and registered in `take-register.json`.

## Pronunciation aliases

None added at N3. The narration handoff's pronunciation register maps display forms to realizations without changing token identity; the C4 alias policy attaches an alias to the prompt only where the display form occurs in the chunk.

## Approval

Owner and voice custodian: Manav Thaker. The owner authorized Step 2 capture for EP008 on 2026-09-03 on the frozen EP007 method ("Yes, both episodes"), which is the configuration recorded here. Original C is the owner's own saved voice identity; rights basis unchanged from EP007.
