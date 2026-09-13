# Week 2 opening performance test

Owner selected the v11 stone-polo forward-leaning reference: “Much better let’s try that”. The bounded test uses the existing Higgsfield Seedance 2.5 connection, one seven-second 720p high-bitrate clip, with the first 21 exact words and Original C source voice. Live balance was 122.38 credits; exact preflight was 45.5 credits, announced before submission. A full take still exceeds the remaining balance and the alternative-provider choice is unresolved.

Use the first two complete sentences to test the new posture and facial/mouth performance before the full script. Preserve source PCM samples [0, 291590), followed by 44,410 silent samples to allow a natural ending in the seven-second model output. The cut is at 6.074791667 seconds, just before next-sentence speech energy. Do not align it to frame 146: that would catch the next syllable. No speech speed change, pitch change, normalization or new voice generation.

REQUEST.json binds the approved reference, prepared audio, direction and cost. SUBMISSION.json preserves the single accepted native job. The MP3 is a reference for native generation; test01-original-c.wav preserves the source audio and is the authority for any needed restoration and final delivery. Inspect native timing before deciding whether the existing Sync v3 repair route is needed. No additional native generation is automatically authorized by a successful but imperfect result.

The native clip preserved all 21 words but altered the speech clock. One Sync v3 silence-mode pass restored Original C. The delivered 7.042-second MP4 has zero measured audio lag in six speech windows and minimum waveform correlation 0.999667 after AAC encoding. Its hosted bytes match the local hash and HTTP range playback is available. Sampled final frames retain the forward lean, polo and office, with slightly looser framing than the source still. Frame inspection does not prove moving lip sync or naturalness. See DELIVERY.json and FINAL-QA.json.

The full script and Week 3 video remain unchanged. This test has no captions, music, B-roll, end card or publication approval. Owner playback review remains required for the moving result.
