# Week 2 voice: what is worth leaving manual

The complete Original C voice is produced and independently transcribed with all 130 supplied script words and a complete word timing map. Owner listening remains the test for delivery and naturalness.

[Final 38.870208-second WAV](https://v3b.fal.media/files/b/0aaa497f/OkYsRfHU_qQUz8Ck7DoGj_selfie-w2b-final-0ad39c68a67b6c0f.wav). Local source: `media/voice/voice-w2b.original-c.wav` relative to this experiment. SHA-256: `0ad39c68a67b6c0f11edcbbe952380fc616716a59788dc049e2613313e4091e0`. Hosted bytes match the local source.

The exact script SHA-256 is `0434553ff578eb611f7764a93ad8bc1df1e3942ee29fd400917fb23a8fbf91bf`. Google Cloud `gemini-2.5-pro-tts` Algieba performs the guide; ElevenLabs `eleven_multilingual_sts_v2` transfers it to approved Original C, `scMbPZwQjr40V1MzL3Nj`. Similarity 0.8, stability 0.4, style 0, speed 1, speaker boost on, seed 2026082501, noise removal off and 48 kHz PCM output are unchanged. Direction requests normal casual conversation with meaning-led variation and no duration target. No retiming, normalization, EQ, added ambience or other post-transfer processing occurred.

The initial W2 guide is fully preserved. Both small.en and medium.en transcribed one “I’m” as “I am,” so no transfer was run on that guide. The orchestrator then authorized exactly one corrected W2B guide, explicitly retaining contraction articulation. W2B guide and final transfer independently match all supplied words. There were two Google guide calls total, one ElevenLabs transfer and no transport retries.

The final audio contains 1,865,770 samples at 48 kHz, mono 16-bit PCM. Its final “after?” is recognized at 38.32–38.58 seconds. The last sample and last 10 ms RMS are zero; last 60 ms RMS is 0.0000333432. Peak amplitude is 0.9216919 and no samples reach full scale.

For a provider requiring sections under 30 seconds, a quiet candidate boundary after “as well.” is frame 524 at 24 fps: 21.833333 seconds / sample 1,048,000. The contiguous sections would be 21.833333 and 17.036875 seconds. The 50 ms energy at that boundary is -90.68 dBFS. No audio was sliced; preserve the exact continuous source for assembly and synchronization.

`FINAL-VOICE.json` binds the source, provider receipts, script, style and verification. `W2B/FINAL-WORD-TIMINGS.json` supplies the actual-source word map for later captions. `W2/VOICE-STATUS.json` preserves the first attempt's held status. ASR ran in the Higgsfield sandbox with no previous-text conditioning or initial prompt. Exact-match normalization accepts punctuation and apostrophe style, spelled AI, and gotta/got to or wanna/want to; it does not accept contraction expansion or changed wording.

No video, captions or end card were produced by this voice task. The sandbox is released. Provider billed amounts were not returned. No canonical voice, episode state or commit was changed.

