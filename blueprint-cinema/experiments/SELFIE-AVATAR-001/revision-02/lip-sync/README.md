# New voice-B restoration

This is a fresh restoration for the olive-overshirt home revision. `INPUT.json` pins new audition B (9.984583 seconds), its original 48 kHz PCM WAV and its exact hash. No seven-second voice, navy test intent or previous failed restoration request is reused.

The one permitted submission uses `fal-ai/sync-lipsync/v3`, `sync_mode: silence`, the completed native Higgsfield clip from job `4ca5df2c-61f8-42b5-8c2c-f3be896622ab`, and the hosted new B WAV. `restore.py` verifies source bytes, writes the intent exclusively before POST, forbids credential redirects and refuses a second intent. An uncertain error must be inspected, never automatically retried.

When complete, the untouched Fal output is retained as `media/revision-02/home-olive-voice-b-sync.mp4`. Root or the visual agent preserves the input as `media/revision-02/home-olive-native.mp4`. Result, download receipt, media probe and audio comparison belong here. `compare_audio.py` measures the new B source against the resulting soundtrack over early, middle and final-sentence windows. Similarity and waveform placement are not a perceptual lip-sync verdict; actual playback review remains required.

## Completed result

One request completed: `01a096b4-1653-79b3-a5ef-9ed62c1fb3d7`. Fal inference time was 166.662 seconds. No retries or additional submissions occurred. The prior experiment's HTTP 403 remains preserved in its original folder.

- [Returned video](https://v3b.fal.media/files/b/0aaa27e6/gsdnvCvgHlsnO_ZvPg3Jm_MIOsFgKl.mp4)
- Local file: `media/revision-02/home-olive-voice-b-sync.mp4`.
- SHA-256: `d5e4e908ad7e6a134f3d2f5fd3afb178853a71fa6ee9cb345cb5de28c9197b8e`; 10,785,661 bytes.
- Native and returned picture both measure 720 × 1280, 24 fps, 241 frames and 10.041667 seconds. Full strict decoding passed.
- Source-B waveform correlation is 0.998316 over the whole aligned source; early, middle and final-sentence correlations are 0.997913, 0.998238 and 0.998742. Source placement is approximately +0.019 seconds. This offset measures soundtrack placement only.
- The native generation's B-source correlation was 0.0500; preservation was not established in its generated soundtrack. The returned restoration supports preservation of the intended new B performance through delivery encoding.

`RESTORED-AUDIO-QA.json`, `NATIVE-AUDIO-QA.json` and `MEDIA-QA.json` contain the measurements. No perceptual lip-sync, face-naturalness or voice-expressivity pass is claimed by this technical task. Actual Fal charge was not returned.
