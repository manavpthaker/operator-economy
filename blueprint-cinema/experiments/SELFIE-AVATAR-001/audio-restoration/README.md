# Original-voice previews: synchronization unfinished

The three `media/voice-preview-*.mp4` files contain the exact 7.5-second source performance, encoded to AAC with trailing silence added to the native video duration. No speech retiming, filter, new synthesis or picture changes were applied. Each compressed video stream hash matches its native source, with all 193 frames preserved at 720 × 1280, 24 fps (8.041667 seconds of picture).

All three preview soundtracks have aligned source correlation 0.999987 at zero offset. Their early, middle and final-sentence correlations exceed 0.99998. These measurements establish preservation through audio encoding, not audiovisual synchronization or perceptual naturalness.

The untouched native videos remain at `media/native-{home,outdoors,cafe}.mp4`. Their source-waveform correlations were respectively 0.0633, 0.0543 and 0.0660; they do not establish preservation of the requested voice or timing.

One original-audio lipsync restoration request for home was attempted through the previously accepted `fal-ai/sync-lipsync/v3` route. Fal rejected it with HTTP 403: the account is locked because its balance is exhausted. No restoration job ID was created. The intent and error are preserved under `home/`; no retry or other location request was submitted. No `restored-*.mp4` files were produced.

The previews are soundtrack remuxes for comparing appearance and original voice. Lip synchronization remains unfinished and requires a funded, separately resumed correction pass followed by playback review. No perceptual listening or lip-sync approval is claimed here.

`INPUT.json` pins the exact source, method and checked price source. Per-location `VOICE-PREVIEW.json`, `native-audio-check.json` and `preview-audio-check.json` preserve output hashes, media properties and measurements. `compare_audio.py` reproduces waveform checks with ffmpeg and numpy. `restore.py` preserves the existing host-restricted credential method and refuses duplicate intent submission.
