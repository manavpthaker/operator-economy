# R38 S08 audio and presenter packet

The original recording says **her**. No standalone **his** occurs anywhere in the 3,186-word master transcript, so there is no direct whole-word donor. A fresh, versioned callback pickup is the clean option. The original master and previous review audio remain untouched.

The actual narration recipe is Google `gemini-2.5-pro-tts`, **Algieba**, with the candidate-C4 acting register, followed by ElevenLabs Voice Changer `eleven_multilingual_sts_v2` onto **Original C** (`scMbPZwQjr40V1MzL3Nj`). It is not direct ElevenLabs text-to-speech. The local `calibrate.py` helper defaults to **Achird**, so a future authorized invocation must explicitly select **Algieba**.

## Prepared original audio

`question-original.wav` is exact PCM from master **252.4166667–257.6666667**, half-open samples **12,116,000–12,368,000** at 48 kHz. It is **5.25 seconds**, mono, signed 16-bit WAV. No gain, fade, retiming or sample changes were applied.

The source words are “What happens here if you are not around for a month. That is not small talk.” The late transcript boundary for “then” should not determine this cut: voiced energy collapses at approximately 252.075; the tail falls to RMS 52 by 252.40; a small breath occurs around 252.425–252.47; the next strong onset begins around 252.50. The start preserves that breath and onset. “Talk” releases after the transcript end at 257.48 and decays by approximately 257.60. The chosen outpoint sits in the low-energy interval before the next phrase. There is no exact-zero gap at either cut, so these are energy-based selections. Native-speed listening was not performed and remains necessary.

Root's proposed picture cut **252.583333–257.875** is **127 frames at 24 fps**. It starts 0.166667 seconds into this audio reference and needs 0.208333 seconds of natural rest after its end. A six-second generated source can cover it if its measured audio insertion offset is at most 0.541667 seconds. Measure that offset and the actual source duration; do not extend coverage with repeated frames. After any callback timing change, shift review time while retaining these master coordinates.

## One contextual callback pickup

`GOOGLE-CALLBACK-GUIDE-BODY.json` is the exact proposed Google request body. It generates:

> Back to his question, then. What happens here if you are not around for a month. That is not small talk.

Only the first sentence is intended for integration. The following unchanged text supplies connected delivery context; the existing original question recording remains the source for the avatar. This is one chosen contextual take, not a short attempt followed by a retry. Local calibration notes explain the choice: a prior isolated 3.65-second tail landed 2.1 dB hot, and very short independently generated passages can drift in pace and level.

`CALLBACK-PICKUP-REQUEST.json` contains the exact transfer endpoint, form fields, voice settings, seed and integration constraints. The current callback slot, ending at the preserved question-audio start, is **1.791667 seconds**. If the pickup and a natural sentence pause fit, preserve the current timing. If they do not, extend only this unaccepted S08 slot by a whole number of 24 fps frames and shift all later S08 cues equally. Never time-stretch the pickup to force it into the old slot. Preserve the accepted R36 prefix through review 247.625.

## V5 presenter request

`AVATAR-PROMPT.txt` and `AVATAR-TAKE-PLAN.json` prepare one **six-second, 1080p, 16:9 Seedance 2.5** take using the accepted V5 wide identity, Rebecca settling and Henry articulation references. All three reference hashes and the V5 accepted artifact hash were verified.

The performance begins engaged, becomes slightly more considered during “if you are not around for a month,” then settles into quiet certainty for “That is not small talk.” Hands remain restrained; no scheduled glance, rhythmic head movement or exaggerated teeth/jaw display. The camera remains fixed and wide for editorial framing. Source audio governs cadence and wording.

R35 used the same six-second video parameters for **54 credits**, and its stored Fal Sync v3 price was **$8/minute**, about **$0.80** for six seconds. These are historical cost bases, not fresh quotes. No current Google or ElevenLabs price is stored with the EP007 capture. Root must verify current rates before quoting the combined cap. The proposed scope is one contextual guide call, one Original C transfer, one six-second avatar generation, and at most one lip-sync restoration, with no paid retries.

No upload, external request, paid call, synthetic generation, shared runtime edit, skill update, decision-log write or canonical state change occurred in this packet.
