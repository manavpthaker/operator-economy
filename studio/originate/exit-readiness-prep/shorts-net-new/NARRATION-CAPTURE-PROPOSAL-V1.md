# EP007 standalone Shorts — narration capture proposal V1

Status: **proposal only · not authorized · not submitted**

## Recommendation

Keep the established EP007 voice chain: Google `gemini-2.5-pro-tts` with Algieba performing the
candidate-C4 conversational register, then ElevenLabs Voice Changer transferring that performance
onto Manav's accepted Original C identity.

Do not use a generic HeyGen or local Kokoro voice for the final cuts. Either could make a temporary
timing track, but both would break the channel's accepted voice continuity and would have to be
replaced before matching avatar production.

## Exact proposed batch

- Authority: `STANDALONE-SCRIPTS-V3.json`, SHA-256
  `6be1ee7c13ba6fc607d215e9a61c74fda31cc3f60026632eff6fc029f903cf6c`.
- Four scripts, 423 words, 2,499 spoken-copy characters.
- One Google guide call and one ElevenLabs transfer call per Short.
- Eight calls maximum; no automatic retries.
- If any call fails or a take is unusable, stop and return for a new decision.
- New avatar generation, lip sync, music, final render and publication are outside this batch.

## Current cap

The four silent animatics currently total 170.3 seconds. At the official rates checked on
2026-09-21, Google Gemini 2.5 Pro TTS output is $20 per million audio tokens and audio uses 25 tokens
per second. That makes the current visual-duration estimate about **$0.09** in Google output, plus
negligible text input; the proposed Google cap is **$0.15**.

ElevenLabs currently lists Voice Changer at **1,000 credits per minute**. The current timing estimate
is about **2,839 credits**; the proposed cap is **3,200 credits**. The cash equivalent depends on the
account plan and rollover balance, so credits—not a guessed dollar conversion—are the binding cap.

Sources:

- <https://cloud.google.com/text-to-speech/pricing>
- <https://elevenlabs.io/pricing>

## Output if approved

Four immutable guide WAVs, four immutable Original C WAVs, hashes and receipts, exact-word QC,
local word-timed transcripts, and revised scene boundaries derived from the real audio clock.

Explicit owner approval of this exact four-Short, eight-call, no-retry cap is required before the
first provider call.
