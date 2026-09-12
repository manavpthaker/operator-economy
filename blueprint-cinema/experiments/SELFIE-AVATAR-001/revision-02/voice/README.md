# Revision 02 voice auditions

Two new performances use the exact same 23 spoken words from the earlier sample. Only acting direction changed. Both use the current `capture_n4b.py` request family: Google Gemini 2.5 Pro TTS, Algieba, followed by ElevenLabs `eleven_multilingual_sts_v2` onto Original C `scMbPZwQjr40V1MzL3Nj`. Transfer settings remain stability 0.4, similarity 0.8, style 0, speaker boost enabled, speed 1, seed 2026082501, noise removal disabled. Canonical narration, clones and default configuration were not changed.

## A: relaxed conversation

- Direction requests relaxed, connected, softly spoken conversation, with small organic variation and ordinary pauses.
- Final audio: `../../media/revision-02/voice-a.original-c.wav`, 11.424208 seconds, 48 kHz mono 16-bit PCM.
- Higgsfield media ID: `db288cf0-d2b8-4fff-add6-ea3d1fa70cb8`.
- Independent ASR recognized all spoken words in both guide and transferred audio. It placed the final word at 10.56–11.04 seconds.
- The guide and transferred recording retain material endpoint energy. This may be an ending artifact or breath, but has not been heard and must not be described as clean. The audition preserves the original provider bytes. It is not the first video-test recommendation.

## B: greater conversational inflection

- Direction requests more varied pitch and pace within thoughts, lighter connective words, and a candid final aside, without theatrical stress, fake fillers or imposed hesitation.
- Final audio: `../../media/revision-02/voice-b.original-c.wav`, 9.984583 seconds, 48 kHz mono 16-bit PCM.
- Higgsfield media ID: `2077e52f-e430-4e22-8cae-319446c05796`.
- Independent ASR recognized all spoken words in guide and transferred audio. It placed `It makes money` at 8.78–9.62 seconds, followed by a quiet ending.
- Suitable as the input for the separately owned 10-second home video test. This is a technical readiness decision, not an owner preference or an expressivity verdict.

## What was verified

Exactly two guide requests and two identity-transfer requests were made; all four returned HTTP 200. No additional generation attempts or retries occurred. Guide-to-transfer duration differences are about 0.014 seconds for B and 0.013 seconds for A. No time stretch, imposed duration, EQ, noise, normalization or new clone was used.

Both final audio files were uploaded through the existing Fal storage route and then through Higgsfield's sandbox upload route. Their confirmed Higgsfield CDN downloads hash-match the original local WAV files. The `.mp3` URL suffix is assigned by Higgsfield; actual returned bytes remain PCM WAV. `FINAL-ASR-AND-HOSTED.json` and `HOSTED-READBACK.json` contain exact URLs, IDs, hashes, durations and word timestamps.

The numbered directions express creative intent. No perceptual listening comparison has been completed, so these measurements do not establish that either audition sounds natural, recognizably like Manav, or sufficiently spontaneous. The approved identity route is preserved; subjective voice match, inflection and ease still require listening.

Input hashes, complete acting prompts, raw provider response paths and receipts are retained. Binary provider responses, raw PCM and WAV files live under `media/revision-02/voice*`; keep them as media artifacts, not text commits. No video or lipsync jobs were submitted by this voice task. Provider charges were not returned in these receipts.
