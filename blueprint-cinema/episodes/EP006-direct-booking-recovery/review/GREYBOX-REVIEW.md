# EP006 greybox review

- Render-data hash: `7d4fec2ed85e9e8d621a210551696e97cd3900f2959a66a4abfd4cc41bfeaa15`
- Representative frame rendered: yes
- 90-second deck prototype review MP4 rendered: yes
- 90-second deck prototype media: h264 960x540 at 30/1, aac 2 channels at 48000 Hz, 90.048000s container duration, 4598932 bytes
- 90-second deck prototype SHA-256: `0665fc2261723b5587a6e3babc765b62c61e84fdc7297109c4e5660d1b751048`
- Superseded map-camera review MP4 rendered: yes
- Superseded map-camera media: h264 960x540 at 30/1, aac 2 channels at 48000 Hz, 915.605333s container duration, 61507359 bytes
- Superseded map-camera SHA-256: `adb0777cc9693f1ed3830c9da45d2cbb0aa26815122fa721e9ce91b0f23b66de`
- Current production state: `greybox_ready`

The full map-camera render is retained as a rejected diagnostic: it preserved the system correctly but asked the viewer to decode a network diagram. The 90-second deck prototype is also retained as a rejected diagnostic: it improved object continuity but still treated the episode as arranged boxes rather than precisely directed causal scenes. Neither is the current creative direction.

The next candidate must be compiled from validated shot-level scene direction. Director packets expose the exact VO, word timings, approved world slice, evidence, and tickets. Authored directions must then specify the audience inference, visual sentence, pixel geometry, exact text and emphasis, word-cued motion, evidence choreography, and transition handoff before another renderer pass.

Container duration can include frame or muxing padding beyond the locked narration. Neither prototype nor the superseded whole-episode render records `greybox_approved`.
