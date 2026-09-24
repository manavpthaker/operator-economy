# Revision 04 global voice synchronization

Completed with exactly one request, `01a097fd-0bb8-7571-aeea-53f07512c185`, after root dispatched the finished assembly. Inference took 261.205 seconds. The runner pinned the complete 52.848625-second R4 Original C WAV, its script and hashes, and the assembled video-only picture at 720 × 1280, 24 fps, 1293 frames / 53.875 seconds. The three retained native sections are 484 / 378 / 431 frames, with picture joins at frames 484 and 862.

The raw [returned video](https://v3b.fal.media/files/b/0aaa305b/GCs5DS7yF-AvWL8yetW3y_4qj7cU2E.mp4) is retained locally at `media/revision-04/home-olive-gtm-r4-sync.mp4`, 53,525,383 bytes, SHA-256 `abc6c79ccb64e430ca9ac58b00c941b8ee096a497a017cc93683205c586ad584`. Local and independently downloaded sandbox bytes match. Actual billed cost was not returned.

`MEDIA-QA.json` confirms both native and returned picture preserve 720 × 1280, yuv420p, 24 fps, 1293 decoded video frames and 53.875 seconds. Strict full decoding passed. Native input has no audio track; returned audio is 48 kHz mono AAC.

`RESTORED-AUDIO-QA.json` records 0.999810 aligned correlation over all 52.848625 seconds of source audio. Each of four independently measured windows gives the same **+0.342125-second** source insertion offset, with zero measured spread at the 16 kHz analysis resolution. Window correlations range from 0.999756 to 0.999821. The source ends at output 53.19075 seconds; the source's ASR-timed final word maps to approximately 52.642–52.842 seconds, and the final half-second is silent. Preserve this returned soundtrack placement during remuxing. It is not a measured audiovisual sync error, and the technical checks do not approve facial continuity or lip-sync perception at either picture join.

Root supplies an assembled-native manifest with `video_url`, repo-relative `local_path`, `sha256`, `width:720`, `height:1280`, `frame_rate:"24/1"`, `frame_count:1293`, `video_duration_seconds:53.875`, `segment_frame_counts:[484,378,431]`, and `audio_stream_count:0`. The local video must live under ignored `media/revision-04/`. Preparation independently downloads the authorized hosted video and audio and verifies their hashes before freezing the native manifest and exact request.

```sh
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-04/lip-sync/restore.py preflight
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-04/lip-sync/restore.py prepare /absolute/path/to/assembly-manifest.json
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-04/lip-sync/restore.py submit
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-04/lip-sync/restore.py status
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-04/lip-sync/restore.py result
python3 blueprint-cinema/experiments/SELFIE-AVATAR-001/revision-04/lip-sync/restore.py download
```

The listed preparation and submission commands document completed work and must not be repeated. One exclusive intent preceded the sole permitted POST. Credentials are confined to `queue.fal.run`; redirects and automatic retry/fallback are disabled. Typed provider errors and uncertain transport outcomes are retained and stop the run. The existing intent prevents another submission.

The [current Fal v3 API contract](https://fal.ai/models/fal-ai/sync-lipsync/v3/api) accepts separate `video_url` and `audio_url` and does not declare a required embedded soundtrack. This workflow uses `sync_mode:silence` with no override options. Native input therefore has no audio to compare. The returned soundtrack will be checked against the full pinned R4 WAV over opening, middle, final section and final question, alongside frame count/dimensions/duration and strict full decoding. Measured source insertion offset must be preserved and reported; it is not itself a measured lip-sync error.

Returned raw media belongs at `media/revision-04/home-olive-gtm-r4-sync.mp4`. Root owns final assembly, video-first remux, mobile hosting, viewing and publishing decisions. No subjective voice, face or lip-sync approval follows from technical checks.
