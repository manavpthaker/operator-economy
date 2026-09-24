# Week 2 full-04: generated B-roll

Status: finished and technically verified. Root inspected all encoded B-roll
boundaries and the final frame, and its voice review found zero lag in all 39
windows. Owner review remains pending. All prior versions remain untouched.

Final: `renders/week2-full04-uncaptioned.mp4` — 29,762,978 bytes.
SHA256: `7019cafe97ebe69d4904bc18c2059565e7ecaa71d58e9a829590439f926a5377`.

| Input | Global frame range | Source |
|---|---|---|
| `public/media/selfie-base.mp4` | [0,933) | Exact full-03 final selfie |
| `public/media/broll-main.mp4` | [304,534) | Confirmed `../media/broll-main-prepared.mp4`, 230 frames |
| `public/media/broll-manual.mp4` | [684,746) | Confirmed `../media/broll-manual-prepared.mp4`, 62 frames |
| `public/audio/original-c.wav` | Entire spoken take | Unchanged Original C master |

The two B-roll clips must be native 720 × 1280, 24 fps and begin at source time
zero. They are generated illustrations of a phone filming a MacBook screen;
root owns their source quality and provenance. The assembly adds no zoom,
crop, dissolve, text, captions or music. Both insert videos are muted. The base
video continues behind them so every return preserves the existing source clock.

`INPUTS.json` records local links and source hashes.
`reports/PROTECTED-BASELINE.json` pins eleven prior critical media files.
Every write by this worker stays inside full-04/assembly.

HyperFrames is pinned at 0.8.38. Output remains 720 × 1280, 24 fps,
933 frames / 38.875 seconds. Reproduce the confirmed assembly with:

```sh
HYPERFRAMES_RUN_ID=selfie-week2-full04 npm run check -- --at 0,6,12.625,12.666666666666666,17,18.625,18.666666666666668,22.208333333333332,22.25,28.458333333333332,28.5,30,31.041666666666668,31.083333333333332,38.83 --json
HYPERFRAMES_RUN_ID=selfie-week2-full04 npx --yes hyperframes@0.8.38 snapshot --at 12.625,12.666666666666666,17,18.625,18.666666666666668,22.208333333333332,22.25,28.458333333333332,28.5,30,31.041666666666668,31.083333333333332
HYPERFRAMES_RUN_ID=selfie-week2-full04 npm run render
npm run finish
ffprobe -v error -show_streams -show_format -of json renders/week2-full04-uncaptioned.mp4
```

`render` uses one worker, high quality and CRF 16, writing
`renders/week2-full04-hyperframes-audio.mp4`. The required `finish` step copies
that picture bitstream and directly encodes the Original C WAV as mono 48 kHz
AAC at 192 kb/s. It applies no gain, filters, normalization, stretching or audio
splices and refuses to overwrite an existing final.

The final passed strict decode, 933-frame format checks and all eleven protected
prior-media hashes. All 933 video packets remain identical through direct-audio
finishing; all 1,824 audio packets are identical to the verified full-03 voice.
Root checked the encoded transitions 303→304, 447→448, 533→534, 683→684 and
745→746, plus the final frame. See `reports/DELIVERY.json` and the root voice
record `../FINAL-AUDIO-QA.json`. Root owns delivery and publication decisions;
technical success is not owner acceptance.

`../SELECTIONS.json` binds the generated source windows and limits. The main
insert changes from the folder scene to the settings scene at frame 448 /
18.666666666666668 seconds. The manual clip uses its selected source frames
[18,80). All prepared picture runs at 1× with no spatial transform. Root accepts
these as illustrative activity, with imperfect peripheral dropdown labels and
brief drag/highlight artifacts; they are not a precise macOS tutorial.

The runtime retains a clip at its exact authored end. Both B-roll durations
therefore end 1 ms before their exclusive frame boundary. This changes no
selected source frame or speed: all 230 and 62 intended output frames remain.
The first export is preserved under the `-inclusive-end-v1` suffix; see
`reports/EXCLUSIVE-END-FIX.json`.
