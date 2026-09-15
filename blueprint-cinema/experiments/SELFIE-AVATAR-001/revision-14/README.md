# R14: v8 video standard pass

Owner request 2026-09-15: bring the Monday GTM Engine selfie up to the week-4 context video standard. No avatar, voice or lip-sync generation.

Changes from R13:
- Cut "Maybe I've gotta build a bit more to find that out. That's fine." (R13 frames 899 to 987, cut inside silences; 15 ms audio fades). The jump is covered by the decide shot. Body 51.417s plus the unchanged R13 closing card = 57.417s (was 61.08s).
- Clean picture rebuilt from `media/revision-10/home-olive-gtm-r10-sync.mp4` frames 0 to 901 plus `media/revision-11/home-olive-gtm-r11-tail-sync.mp4` (the accepted R11 assembly without captions). Audio from R13.
- Hook (0 to 6.2s): "Could I sell this?" behind the head over a blurred fill.
- Burned word-highlight captions replace the old caption style (script words, whisper medium.en timings in `asr/`).
- Illustrative GTM Engine screens on the MacBook reference photo: ~/GitHub projects in Finder ("other things I wanna build"), `uv run gtm run littlefables` Focus output ("GTM Engine... looks at the code"), `.gtm/research/report.md` in Cursor ("who might need it... what to test"), `gtm report` proposed test and next-decision options with explore picked ("choose it over their usual way" / "keep working on it"). Wording follows the real engine's statuses and phases; findings text is illustrative and mostly blurred.

Build: `cd build && python3 generate.py && npm run render`, then mux `build/renders/r14-picture.mp4` video with `build/assets/base.mp4` audio by stream copy.

Output: 720x1280, 24 fps, 1378 frames / 57.417s, SHA-256 `0dccc6591f70db1bca8e46bc0cf28e6cb5ad6dbf099f5159e00a2c616443fcae`, in `media/revision-14/`. Owner review pending. The content-os package, script.txt, captions and owner exception still reference R13; the post copy is unaffected by the cut.
