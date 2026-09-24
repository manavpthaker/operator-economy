# EP009 full build: shared conventions for every lane

Status: binding for EP009-FULL-BUILD-001. Written by the orchestrator 2026-09-16.

## Authorities (read, never edit)

- Owner scope: `blueprint-cinema/episodes/EP009-direct-booking-recovery/review/source-records/2026-09-16-owner-build-scope.json`
- Plan: `direction/DIRECTION-PLAN.md` and `direction/SHOT-PLAN.json` (the segment contract). Do not change segment boundaries. If a boundary is wrong, stop that segment and report; do not silently move it.
- Decision log: `blueprint-cinema/episodes/EP009-direct-booking-recovery/review/decisions/events.jsonl`, appended only through `.agents/skills/oe-video-direction/scripts/decision_log.py` exactly as `references/decision-record.md` says.
- Locked words and timing: `operator-blueprint-v2/episodes/EP009-direct-booking-recovery/01-editorial/` and `02-narration-production/word-transcript.json`. Master audio: `02-narration-production/master/narration-master.wav` (48 kHz mono, sha256 `e433c0fd6d7dd522efb9f6593986f930f9ccc54b2be5132dec50c20ff3c1f944`). On-screen numbers, sources and caveats come only from `01-editorial/claims-map.md`.
- Skills: `.agents/skills/oe-video-direction`, `oe-boundary-ledger`, `oe-film-direction`, `hyperframes` and its domain skills.

## Format

1280x720, 24 fps, 48 kHz stereo in every rendered deliverable. Every segment's frame count is `round(master_out*24) - round(master_in*24)`; a deliverable with any other frame count is wrong.

## Folder ownership (write only in your own)

| Lane | Writes to |
|---|---|
| world kit | `world-kit/` |
| presenter | `presenter/` and `ledger/presenter.jsonl` |
| film | `film/` and `ledger/film.jsonl` |
| act N models | `scenes/<segment id>/` for segments whose `builder_group` is `actN-models` |
| assembly | `assembly/` |
| review | `review/` |

Every lane may append to the decision log. Nobody commits to git; the orchestrator commits.

## Scene project layout (model, evidence, screen, sting segments)

Copy the skeleton from EP007's accepted scene `blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r60-s15-p1/` (package.json pinned to `hyperframes@0.8.36`, hyperframes.json, `public/fonts`, `public/vendor/gsap.min.js`). One project per segment at `scenes/<segment id>/`, or one project covering several contiguous segments of the same act when a single continuous composition is the right build; name it `scenes/<first id>__<last id>/`.

- Import drawn objects from `world-kit/` (copy the SVG symbols into `public/art/`). Do not redraw a kit object differently. If you need an object the kit lacks, draw it in the kit's construction and record it in your BUILD.json `new_objects`.
- Audio: `public/audio/narration.wav` is the sample-exact master excerpt `[master_in, master_out)`: `ffmpeg -i <master> -af "atrim=start_sample=<round(in*48000)>:end_sample=<round(out*48000)>,asetpts=N/SR/TB" -ac 1 narration.wav`.
- Cues are word IDs from `word-transcript.json` converted to seconds relative to `master_in`; keep a `C` cue map in the script like r60.
- Checks before delivery: `npx --yes hyperframes@0.8.36 check --strict` with 0 errors; render to `qa/<name>.mp4`; confirm frame count; extract stills at each cue into `qa/stills/` and look at them; render audio vs master excerpt correlation at zero lag ≥ 0.999; no uniform (blank) frames except a planned hold.
- Deliver `BUILD.json`: `{segments:[ids], master_in, master_out, frames, mp4:{path,sha256}, stills:[paths], checks:{strict_errors, frames_ok, audio_corr, uniform_frames}, new_objects:[], deviations:[], decision_event_ids:[]}`.

## Provider lanes

- Spend rules are in `ledger/SPEND-LEDGER.json`. Your lane's allocation there is a hard ceiling. Write an intent line before every paid call and a done/failed line after.
- Credentials: `ELEVENLABS_API_KEY` and `FAL_KEY` in the repo `.env` (never print them). Higgsfield through the Higgsfield MCP tools available in this session (load them with ToolSearch; check `balance` before and after).
- Reuse EP007 transports rather than writing new HTTP code: Fal upload/queue in `blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r32-performance-refinement/provider/fal_ops.py`; S14 presenter flow in `hyperframes/reviews/r59-s14-presenter/provider/`; Kling flow in `hyperframes/reviews/r53-s10/provider/` and `r52-walkout`.
- Deliver per take: the raw provider file, the final conformed clip at the segment's exact frame count with the master excerpt as its audio (stereo, unity upmix `pan=stereo|c0=c0|c1=c0`), and `TAKE.json` with job ids, costs, offsets measured in three windows, trims, and checks.

## Review honesty

A passing check is not a creative verdict. Record what you looked at and what you could not judge. Agent verdicts in this build are recommendations; nothing here is owner acceptance, and no canonical gate is passed.

No em dashes in anything written for this build.
