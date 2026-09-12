# Revision 04 full GTM Engine voice

Input is the owner's exact `../SCRIPT.txt`, 184 words, SHA-256 `3eb28bd243f2c169b5906852f3b055553d1bc0e0520a029082fa5bf41a36fbe3`. The full input, adapted acting direction, provider settings and helper hashes are pinned in `R4/INPUT.json`. No script text was edited.

## Completed voice

One full guide, one explicitly authorized ending pickup, and one whole Original C transfer completed. The final source is `media/revision-04/voice-r4.original-c.wav`: **52.848625 seconds**, 48 kHz mono 16-bit PCM, 2,536,734 samples, 5,073,512 bytes. SHA-256: `b2c10c8e5b3267a43f8aaa4b3aba2132f4b20d6df6cd22fbfdcf0dc831e7e3b3`. [Verified full WAV](https://v3b.fal.media/files/b/0aaa2fe9/0g2B6ygqc2BCtUFM0scTp_selfie-r4-final-b2c10c8e5b3267a4.wav).

The actual final pace is approximately 209 script words per minute, faster than the approximately 169 wpm selected R3 sample and shorter than the 65–70-second direction. No speed processing or forced duration was applied. This is the performed take for listening, not an asserted pace or naturalness approval.

Independent final ASR with VAD and previous-text conditioning disabled recognizes the complete supplied script, including `you’d built`. The workflow explicitly accepts `gotta`/`got to` and `wanna`/`want to` as colloquial transcription equivalents; raw ASR is retained, and the supplied text is unchanged. `R4/FINAL-WORD-TIMINGS.json` maps the 188 ASR tokens to all 184 exact script words. `R4/FINAL-ASR-INITIAL.json` preserves the earlier decoder's low-confidence, largely zero-duration tail repetition; the verification decoder did not repeat it. No audio was removed to affect that result.

The final word `business?` is recognized at 52.30–52.50 seconds. Final sample and last 10ms RMS are zero; last 60ms RMS is 0.00576, last 300ms RMS 0.02749, and the existing relative tail-energy check is 0.0111 (quiet). Technical checks do not establish full perceptual quality.

Root selected contiguous picture boundaries at frame **484 / 24 = 20.1666667 seconds** (sample 968000) and frame **862 / 24 = 35.9166667 seconds** (sample 1724000). Their 50ms RMS levels are 0.00247 / −52.15 dBFS and 0.00356 / −48.98 dBFS. The latter deliberately retains modest breath in the later speech gap. No audio is removed at these boundaries. These are suggested picture splits; final audiovisual synchronization remains a later task. Root owns segmentation, native video, global synchronization and delivery.

## Ending correction provenance

The one 37-word pickup used the unchanged hobby paragraph as context and the exact final question. It passed independent ASR including `you’d built`, but its raw endpoint retained residual energy. Root explicitly directed preserving that endpoint for the transfer and later listening.

The corrected guide retains original PCM samples `[0,1139998)` unchanged, then pickup PCM samples `[139200,267143)` unchanged, all at 24 kHz. The join occurs at original 47.4999167 seconds and pickup 5.8 seconds; both adjacent join samples are zero. No fades, gain, EQ, retiming or synthetic silence were used. Corrected-guide duration is 52.830875 seconds, SHA `88e9aeb69622670c11da44d5d327a33a9d81c916f628430a9cde9f80a15805bd`. Both retained PCM ranges were verified byte-identical. `R4/GUIDE-CORRECTION.json` records exact mapping and provenance. Its full ASR passed before the sole whole-voice transfer, which added approximately 0.01775 seconds.

## Initial guide

One whole Algieba guide was requested from `gemini-2.5-pro-tts`. It returned HTTP 200 and 53.610958333 seconds of 24 kHz mono 16-bit PCM WAV, with a quiet endpoint (last-window relative energy 0.0009). This is shorter than the requested 65–70 seconds: approximately 206 script words per minute, compared with approximately 169 in the selected R3 excerpt. No duration processing or second guide was used.

Guide SHA-256: `56c013dbff2dd0e11b59408b5d0e4006cd31ae5ca3d05b847b21e8b17661271f`. [Verified existing guide](https://v3b.fal.media/files/b/0aaa2fb4/vxKcTdYdF6jGcYVvUwB_i_selfie-r4-guide-56c013dbff2dd0e1.wav).

Independent base.en and small.en ASR both recognized the entire passage and complete final question, but both rendered two `gotta` occurrences as `got to`, two `wanna` occurrences as `want to`, and the final `you’d built` as `you built`. The first two may reflect normal transcription conventions. The contracted final d was initially unverified; ASR cannot establish whether an unreleased consonant was actually absent. `R4/GUIDE-ASR.json` retains `normalized_exact_match: false` with complete small.en word timings. Transfer paused at that point; the authorized pickup above resolved the contraction before transfer.

## Reusable execution

From the repository root, the isolated runner accepts `prepare`, `guide`, and `transfer`. All stages have already run and must not be repeated. Transfer checked the corrected guide, source hashes and accepted ASR before creating its exclusive submission intent. Both provider transports refuse credential redirects, preserve raw responses and have no retries. These commands document the completed route; they are not further work to execute.

```sh
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-04/voice/capture_r4.py transfer
node blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-04/voice/upload_audio.mjs final
```

The transfer is the unchanged `eleven_multilingual_sts_v2` onto Original C, `scMbPZwQjr40V1MzL3Nj`, with similarity 0.8, stability 0.4, style 0, speed 1, speaker boost on, seed 2026082501, noise removal off and `pcm_48000` output. No stored clone or global defaults are modified.

## Preflight evidence and limits

The script is 958 UTF-8 bytes including its newline, below the current [Google Cloud TTS limit](https://docs.cloud.google.com/text-to-speech/docs/gemini-tts) of 4,000 bytes per text or prompt field. The documented output cap is approximately 655 seconds. The local helper's 1,250-character margin follows an older observed 75-second failure; it is not the current published limit. [Voice Changer](https://elevenlabs.io/docs/overview/capabilities/voice-changer) permits five minutes and bills 1,000 characters per processed audio minute.

A read-only subscription query before generation returned an active ElevenLabs Pro plan, 35,957 used of 888,122 credits (852,165 remaining). The actual guide would imply roughly 894 transfer credits if submitted. [Google pricing](https://cloud.google.com/text-to-speech/pricing) is $20 per million output audio tokens at 25 tokens per second, so this guide's audio component is approximately $0.0268 plus input-token charges. Neither provider returned a final billed-cost receipt in this task.

No canonical narration, existing media, video jobs, lip-sync jobs, commits or publishing states were changed. Root owns any later segmentation, picture and delivery.
