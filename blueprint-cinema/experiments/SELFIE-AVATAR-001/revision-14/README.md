# R14: v8 video standard pass

Owner request 2026-09-15: bring the Monday GTM Engine selfie up to the week-4 context video standard. No avatar, voice or lip-sync generation.

Changes from R13:
- Cut "Maybe I've gotta build a bit more to find that out. That's fine." (R13 frames 899 to 987, cut inside silences; 15 ms audio fades). The jump is covered by the decide shot. Body 51.417s plus the unchanged R13 closing card = 57.417s (was 61.08s).
- Clean picture rebuilt from `media/revision-10/home-olive-gtm-r10-sync.mp4` frames 0 to 901 plus `media/revision-11/home-olive-gtm-r11-tail-sync.mp4` (the accepted R11 assembly without captions). Audio from R13.
- Hook (0 to 4.79s): Counterproof proof ground, presenter inset with the top cropped below the hairline, "Could I sell this?" on the ground with the matted head in front; cuts to full frame on "I could sell this".
- Burned word-highlight captions replace the old caption style (script words, whisper medium.en timings in `asr/`).
- Screens on the MacBook reference photo. The ~/GitHub projects folder is a mockup of real folder names. Every code shot shows real lines from `~/GitHub/gtm-engine` at commit 92cf5dc, read at build time with file line numbers, in a Cursor-style window (owner request: code on screen must be real, not decoration):
  - "It looks at the code": `src/gtm_engine/focus_extract.py` 830 to 856, `_capabilities` ranking evidence, code weighted above tests and docs (line 847 highlighted).
  - "researches who might need it and what they're using already... what to test": `.claude/workflows/phase2-research.js` 174 to 185, the default research lenses; buyers-and-triggers then alternatives-and-gaps highlighted on those words.
  - "choose it over their usual way" / "I don't have to decide it's a business": `src/gtm_engine/guided.py` 2376 to 2393, the outcome rules; ADVANCE's "Design a larger bounded test; do not scale without a new approval." highlighted.

Build: `cd build && python3 generate.py && npm run render`, then mux `build/renders/r14-picture.mp4` video with `build/assets/base.mp4` audio by stream copy.

Output: 720x1280, 24 fps, 1378 frames / 57.417s, SHA-256 `ed14a56fd064f6a25e6a8cd78e85017c7362bee5de428de075429ebcc8740569`, in `media/revision-14/`. Owner review pending. The content-os package, script.txt, captions and owner exception still reference R13; the post copy is unaffected by the cut.
