# Week 2 full-07: v8 video standard pass

Owner request 2026-09-15: bring the Wednesday selfie up to the week-4 context video standard before it posts. Full-06 picture and audio stay underneath; nothing was regenerated and no provider credits were used.

Added:
- Hook (0 to 3.625s): presenter steps back over a blurred fill so "Worth automating?" sits behind the head (CoreML matte from `hyperframes remove-background`).
- Burned word-highlight captions from SCRIPT.txt words timed by whisper medium.en (`asr/transcript.json`; wanna/gotta merged).
- "Fix it" shot, frames 230 to 304: the same Warp + Claude Code window, `mv *.png Assets/` fails, then the request to update the rule.
- "Leave it manual" shot, frames 610 to 746: Finder icon view, two files dragged into folders by hand.

Both new shots are illustrative, not real screen captures, on the same MacBook reference photo as the earlier Finder and Warp inserts.

Build: `cd build && python3 generate.py && npm run render`, then
`ffmpeg -i build/renders/full07-picture.mp4 -i build/assets/base.mp4 -map 0:v -map 1:a -c copy -movflags +faststart renders/week2-full07-standard.mp4`
(`base.mp4` is full-06 `week2-full06-terminal-broll.mp4`, so audio packets are copied unchanged.)

Output: 720x1280, 24 fps, 1101 frames / 45.875s, SHA-256 `8c9bb79a9010020e0fde3f78032bfebc40e2f3ce25e47ba6660c5be3b86cb128`. Copy in `media/revision-7/`. Owner review pending; the scheduled LinkedIn post and owner exception still reference full-06.
