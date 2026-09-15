# Week 2 full-07: v8 video standard pass

Owner request 2026-09-15: bring the Wednesday selfie up to the week-4 context video standard before it posts. Full-06 picture and audio stay underneath; nothing was regenerated and no provider credits were used.

Added:
- Hook (0 to 2.417s): Counterproof proof ground (#F3F6F5), presenter inset with the top cropped below the hairline, "Worth automating?" on the ground with the matted head in front (CoreML matte from `hyperframes remove-background`). Cuts to full frame on "do the task". Owner asked for this over the earlier blurred fill, which hid part of the title.
- Burned word-highlight captions from SCRIPT.txt words timed by whisper medium.en (`asr/transcript.json`; wanna/gotta merged).
- "Fix it" shot, frames 230 to 304: the same Warp + Claude Code window, `mv *.png Assets/` fails, then the request to update the rule.
- "Leave it manual" shot, frames 610 to 746: Finder icon view, two files dragged into folders by hand.

Both new shots are illustrative, not real screen captures, on the same MacBook reference photo as the earlier Finder and Warp inserts.

Build: `cd build && python3 generate.py && npm run render`, then
`ffmpeg -i build/renders/full07-picture.mp4 -i build/assets/base.mp4 -map 0:v -map 1:a -c copy -movflags +faststart renders/week2-full07-standard.mp4`
(`base.mp4` is full-06 `week2-full06-terminal-broll.mp4`, so audio packets are copied unchanged.)

Output: 720x1280, 24 fps, 1101 frames / 45.875s, SHA-256 `0bb1639346bfbc46933e27c5c94dc3f0ef186075a9752039a4ff9bda890cf0b1`. Copy in `media/revision-7/`. Owner review pending; the scheduled LinkedIn post and owner exception still reference full-06.
