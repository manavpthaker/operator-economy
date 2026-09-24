# R9 - quieter-mouth comparison; head unchanged

User requested smaller mouth movements and a slight head tip instead of the head shake around "I've gotta get better at that."

The new Seedance2.5 edit was blocked by Higgsfield moderation (`nsfw`) without a detailed reason. No new performance was produced; no retry or provider switch was made. Balance was 600.88 before and after. See `BLOCKED-EDIT.json` and `video/`.

The delivered 21.25-second comparison uses already existing R8 native picture before the additional Sync pass, with the exact approved R8 audio stream-copied. This is a diagnostic comparison only: head motion and smile remain unchanged, and the requested head tip was not produced. It contains the first 68 script words through "what they're doing already," with the same 18 Counterproof heading captions.

Review video: https://d2ol7oe51mr4n9.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/48e46aaf-54e3-4d36-964c-60d463100fb9.mp4

## Evidence and limits

- `REMUX-QA.json`: decoded picture equals existing prepared R8 native picture; decoded audio equals approved R8 final audio.
- `AUDIO-QA.json`: final audio insertion has zero measured offset/drift relative to the approved paced WAV. This does not test visual lip sync.
- `captions/REPORT.json`: 720x1280, 24 fps, 510 frames; 18 cues, 68 words; strict decode and unchanged decoded audio through caption burn.
- Caption SRT and decoded audio are identical to R8. Original voice, slower GTM explanation and pause remain intact.
- `diagnosis/`: native-versus-Sync mouth frame observations and native-audio clock comparison. Native timing differs around 11-13.7 seconds; most later native speech is about 25 ms early. Exact word-level lip sync is not established.
- Root inspected the final contact sheet. Caption layout and identity remain intact in inspected frames. A sequence of stills does not establish natural delivery.
- Hosted file hash and HTTP 206 range support verified. Browser loaded the expected 21.25-second portrait video without media error.

`DELIVERY.json` binds the result and checks. Media are retained locally under the ignored `media/revision-09/` directory. This is not integrated into the full video, selected as a canonical avatar, or approved for publication.
