# Proposed final-sentence performance repair

Status: prepared, not authorized or submitted. This is a new isolated audition. R21 remains the current local framing preview.

## Intended result

Keep this sentence exactly:

> By the end you will know exactly what this practice can honestly charge for, and the one number that decides whether it works at all.

Direct one natural stress on “one number,” with a little more weight and room on that phrase, then settle into “that decides whether it works at all.” Keep the surrounding words conversational and connected. Match the existing speaker identity and grounded delivery. No shouting, theatrical pause, clipped syllables, permanent smile, repeated emphasis or extra words. Target about 9 seconds; natural delivery takes precedence over an exact target.

R21's closer framing supplies the visual emphasis. The proposed video pass changes lips only; it does not attempt a finger gesture or a new body performance.

## One bounded sequence

1. Generate one guide with `gemini-2.5-pro-tts`, explicitly selecting **Algieba** and the existing candidate-C4 register, with the additional performance direction above. Do not invoke the full episode capture or its retry loop.
2. If the guide has the exact words, usable delivery and fits the available performance footage, transfer it once to **Original C**, using the existing `eleven_multilingual_sts_v2` settings: similarity 0.8, speed 1.0, stability 0.4, style 0.0, speaker boost true, seed 2026082501, PCM 48 kHz. Review this audio before the video call; reject a take that loses the requested stress or mismatches the surrounding voice.
3. Only if the audio passes, submit one `fal-ai/sync-lipsync/react-1` call with `model_mode: lips`, `emotion: neutral`, `lipsync_mode: cut_off`, and temperature 0.5. Use the original selected404 performance, not video with Sync 3 lips already applied. React-1 is an unproven comparison on this presenter, not a guaranteed repair.

Each stage has a maximum of one submission and zero retries. A failure, ambiguous submission result, incorrect words, unusable delivery or exceeded budget stops the sequence. No fallback model or additional generation is implied.

## Picture and timing

The raw selected404 source has 289 frames at 24 fps, duration 12.041667 seconds. Use a contiguous tail window ending at frame 289, sized to the selected audio: `N = ceil(audio_duration_seconds * 24)`, source frames `[289-N, 289)`. The new audio, including necessary silence handles, must be at most 12 seconds. This may start earlier than R15's B window at frame 83; that is an explicit new performance selection requiring review. Never truncate spoken words, repeat, bounce, freeze or retime the source to force a fit.

Source: `blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/404.mp4`, SHA-256 `a0de31c36bde22219a1e067178b86cf750e7da1f11a69a775c370c82df6f29dd`. Use the locked v4 narration and R15 `pickup-b.wav` as voice continuity references; their current pins are recorded in `PERFORMANCE-INPUT-PINS.json`.

Frame-quantize only the trailing audio silence by less than one frame if necessary. Match equal input durations before the lip-sync call. Preserve all spoken samples and document the final timing. The new private preview may extend its final sentence to accommodate the natural take. Earlier R21 cuts stay intact; the “one number” reframe moves to the new word onset. No new master replaces the locked narration or uses its old transcript as if still valid.

## Spend boundary

Proposed maximum: **$3 estimated external cash spend plus 250 existing ElevenLabs credits**, with no top-up, credit purchase, paid overage or billing-plan change. At roughly 9 seconds, the lip pass is approximately $1.50, the Google guide normally under $0.01, and the voice transfer approximately 150 credits. Exact ElevenLabs cash conversion depends on this account's plan and is not asserted here.

Before a paid submission, verify the selected route's current estimate and sufficient existing credits. Stop if the estimate exceeds the cap or cannot be bounded. Unused allowance does not authorize another attempt. Public pricing is an estimate, not an invoice guarantee.

- [Fal React-1 price and schema](https://fal.ai/models/fal-ai/sync-lipsync/react-1/api): lips mode, explicit cut_off, $10 per minute.
- [Google Gemini TTS pricing](https://cloud.google.com/text-to-speech/pricing): Pro text/audio token billing; 25 audio tokens per second.
- [ElevenLabs voice changer](https://elevenlabs.io/docs/overview/capabilities/voice-changer): voice transfer; current account credit availability/rate must be verified before use.

## Acceptance and authority

Review the entire new final sentence at normal speed with its intended audio, plus the preceding cut. Verify exact wording, voice continuity, one audible emphasis, natural jaw/lip articulation, the closed-lip sounds in “number,” and the final clause. Check for altered identity, hallucinated text, flicker, face artifacts and extra gestures. Integrate only a usable candidate into a new private review version; otherwise preserve R21 and report the failed attempt.

The previous Kling Avatar authorization covered one submission and is exhausted. `blueprint-cinema/AGENTS.md` requires separate authorization before paid generation. This proposal does not authorize a call, revise canonical narration, advance an episode gate or publish anything.
