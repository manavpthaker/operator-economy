# Week 2 full-06: terminal automation B-roll

Adds a 61-frame (2.542s) insert over "I can use AI to build something that does it for me", frames [87,148) / 3.625–6.167s, cutting back to the presenter on "But".

`broll-terminal/` is a HyperFrames composition: a Warp-style window running Claude Code, composited with a perspective transform onto `full-04/media/macbook-reference.png` (the same photo the generated Finder B-roll came from), plus handheld drift, glare, vignette and grain. The request types, then the camera pushes in on `mv notes.txt Sources/` and `mv *.png Assets/`. Illustrative, not a real screen capture. No generation credits.

Base: `full-05/assembly/renders/week2-full05-closing.mp4`. Output: `assembly/renders/week2-full06-terminal-broll.mp4`, 720×1280, 24 fps, 1101 frames / 45.875s.

Assembly re-encodes picture (libx264 slow, CRF 12) because the base has no keyframe at frame 87; audio is packet-copied. Verified: AAC packet bytes identical to full-05 (1824 packets); frames outside the insert min PSNR 48.2 dB vs full-05; strict decode passed. Output SHA-256 `cea7b8e1a6f1fbcb1d8113cbb136ea8d93f616f5cab97b034359509196325426`.

Render: `cd broll-terminal && npm run render`, then
`ffmpeg -i ../full-05/assembly/renders/week2-full05-closing.mp4 -i broll-terminal/renders/broll-terminal.mp4 -filter_complex "[1:v]setpts=PTS-STARTPTS+87/(24*TB)[b];[0:v][b]overlay=eof_action=pass:format=auto,format=yuv420p[v]" -map "[v]" -map 0:a -c:v libx264 -preset slow -crf 12 -profile:v high -r 24 -video_track_timescale 12288 -c:a copy -movflags +faststart assembly/renders/week2-full06-terminal-broll.mp4`

HyperFrames check: lint, runtime, motion and contrast pass; layout flags overlap/out-of-canvas from the 3D-tilted window and intentional push-in (inspected in snapshots). Owner review pending.
