# Revision 05 global voice synchronization

Completed one authorized Sync v3 request, `01a09842-e419-7821-8d4b-158fc159a783`, with `sync_mode:silence`. This pass reuses the exact full R4 voice recording and script with the newly assembled facial performance. No new TTS, speech editing or retry was performed.

The returned raw video is [the R5 Sync result](https://v3b.fal.media/files/b/0aaa3224/fyA4CN5ZziTCnU8AFYA_w_BJJmaXoO.mp4), preserved at `media/revision-05/home-olive-gtm-r5-sync.mp4`: 54,370,568 bytes, SHA-256 `1b210aa34c6d696dce47604918d875ec3676beb54851750896fb5d0786177bfb`. It retains 720 × 1280, 24 fps, 1293 frames / 53.875 seconds. Strict full decoding passed.

Fresh comparison measured the source soundtrack insertion at **+0.342125 seconds**. All four independently aligned windows returned that same offset, with maximum sampled local drift of 0 seconds at 16 kHz analysis resolution. Minimum window correlation was 0.99975418; full-source correlation was 0.99980944 across all 52.848625 seconds. The source endpoint lands at 53.190750 seconds, and the final decoded half-second is silent. These are waveform and placement checks, not a subjective audiovisual sync verdict.

`FINAL-QA.json` binds the exact native, voice, script, raw result and supporting records. Its SHA-256 is `ddd654f446485e93e81eebaf0791da92232f6231385e50744be5f97b69a4b280`. Caption timestamps based on the unchanged R4 WAV must add the fresh R5 offset above. Root owns captions and final packaging; this worker did not modify either.

The retained source is the 52.848625-second 48 kHz mono PCM WAV, SHA-256 `b2c10c8e5b3267a43f8aaa4b3aba2132f4b20d6df6cd22fbfdcf0dc831e7e3b3`. The script SHA-256 is `3eb28bd243f2c169b5906852f3b055553d1bc0e0520a029082fa5bf41a36fbe3`. `INPUT.json` pins both. The new assembled picture must preserve 720 × 1280, 24 fps, 1293 frames / 53.875 seconds, with retained sections of 484 / 378 / 431 frames and no embedded native audio.

Root supplies an assembled-native manifest with `video_url`, repo-relative `local_path`, `sha256`, `width:720`, `height:1280`, `frame_rate:"24/1"`, `frame_count:1293`, `video_duration_seconds:53.875`, `segment_frame_counts:[484,378,431]`, and `audio_stream_count:0`. The local video must be under ignored `media/revision-05/`. Preparation verifies both local and hosted media hashes before binding the new native input. No R4 request or submission intent is reused.

```sh
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-05/lip-sync/restore.py preflight
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-05/lip-sync/restore.py prepare /absolute/path/to/assembly-manifest.json
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-05/lip-sync/restore.py submit
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-05/lip-sync/restore.py status
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-05/lip-sync/restore.py result
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-05/lip-sync/restore.py download
```

The preparation and submission commands above document the completed lifecycle; do not run them again for this revision. Root supplied the verified native input and dispatched execution. One exclusive intent preceded the one permitted `fal-ai/sync-lipsync/v3` POST. Authentication stayed on `queue.fal.run`, redirects were denied, and automatic retry/fallback was disabled. A typed error or uncertain submission requires inspection; it does not authorize another request.

Returned raw media belongs at `media/revision-05/home-olive-gtm-r5-sync.mp4`. Technical QA compares the complete output soundtrack with the fixed source, measures this result's new uniform insertion offset and four local offsets, and checks frame count/dimensions/duration plus full decoding. R4's measured offset is not reused. Native assembly has no soundtrack to compare. Preserve the returned placement during downstream remuxing; it is not itself a measured audiovisual sync error.

Stop after source-integrity and full-decode reporting. Root owns phone packaging, visual review and any publishing decisions; subjective performance acceptance belongs to the owner. No canonical state, captions, commits or other generation belongs to this worker scope.
