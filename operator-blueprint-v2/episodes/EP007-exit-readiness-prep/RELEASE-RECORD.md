# EP007 release record (public №001)

Internal ID EP007 · slug `exit-readiness-prep` · public №001 · title **The One-Person Business That
Gets Companies Ready for a Sale** · premiere Mon 2026-10-05 11:00 ET · Shorts Tue–Fri 08:30 ET.

This is the index for everything done from locked cut to launch. Runbooks derived from it:
- Finish: `operator-blueprint-v2/06-resolve-finish/FINISH-RUNBOOK-v0.1-from-EP007.md`
- Packaging, channel, site, YouTube: `operator-blueprint-v2/07-publishing/PACKAGING-AND-LAUNCH-RUNBOOK-v0.1-from-EP007.md`
- Shorts: `operator-blueprint-v2/08-distribution/SHORTS-RUNBOOK-v0.1-from-EP007.md`
- LinkedIn: `operator-blueprint-v2/08-distribution/LINKEDIN-RUNBOOK-v0.1-from-EP007.md`

Decision log: `blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/events.jsonl`
(hash-chained; owner quotes in the `ep007-owner-*.json` source files beside it).

## Pipeline as run

| Stage | What happened | Key records |
|---|---|---|
| 1–5 Editorial → production | Locked Canvas, script, narration; scene-by-scene build S00–S26; whole-episode lock R79 | `01-editorial/`, `02-narration-production/`, `blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/PRODUCTION-CHECKPOINT.md`, `r79-owner-whole-episode-lock-v1` |
| Shorts | Four net-new 9:16 companion Shorts; Short 01 accepted 09-22, 02–04 accepted 09-23 | `studio/originate/exit-readiness-prep/shorts-net-new/PRODUCTION-MANIFEST-V8.json`, `ep007-short01-clean-frame-owner-accepted-v25`, `ep007-shorts02-04-owner-accepted-v4` |
| Finish (R80) | 54 leaves re-rendered at 4K → 1080p plates; R50 kept locked frames | `blueprint-cinema/episodes/EP007-exit-readiness-prep/edit/handoff/r80-4k-plates/`, `ep007-finishing-4k-rerender-v1`, `ep007-r80-plates-owner-review-v1` |
| Conform | Resolve 21 free, console Lua, OTIO-verified | `ep007-r80-resolve-conform-verified-v1` |
| Cut (R81) | Removed "I have never sold a business." + 4-frame dissolve | `…/edit/handoff/r81-cut-never-sold/`, `ep007-r81-cut-never-sold-v1`, `ep007-r81-owner-accept-mix-direction-v1` |
| Mix, captions, masters | Dialogue only, -14.0 LUFS / -1.6 dBTP; SRT ASR-verified; H.264 + ProRes masters | `…/r81-cut-never-sold/finishing/DELIVERY-REPORT.json`, `ep007-r81-masters-verified-v1` |
| Packaging | Title + HELP HER SELL thumbnail after 5 rounds; copy approved; facts.md section approved | `studio/originate/exit-readiness-prep/content/`, `launch/thumbnail-note.md`, `ep007-packaging-title-thumbnail-v1` |
| Release plan | Oct 5; Content OS gate skipped for EP007 by owner exception | `ep007-release-plan-v1` |
| Channel reset | 32 old videos private; new banner/About/keywords; avatar manual | `channel/youtube-reset-2026-09-23/`, `ep007-channel-reset-v1` |
| Site + LinkedIn + Canvas | Site rebuilt (positioning-first); LinkedIn page refreshed; deliverable = Operator Canvas | `site/REBUILD-NOTES.md`, `ep007-site-linkedin-canvas-v1` |
| Numbering | Internal EP007 = public №001 | `ep007-public-renumber-v1` |

## Owner rulings that set standards (reuse)

- Shorts: standalone payoff for a cold viewer; net-new vertical, not crops; presenter → working
  screens → presenter; clean frame; visual-only episode route at the end.
- Finishing: sharpness over speed (4K re-render); locked timing beats sharpness where they conflict (R50).
- Honesty over polish: cut a false line rather than keep a locked take.
- Mix: dialogue only, -14 LUFS, no music.
- Thumbnail/title: episode's own cast, presenter as small serious guide, episode-specific aspiration
  verb; title promises the how-to.
- Channel: fresh start; brand = Boundary Ledger wordmark; About "…business of one using AI".
- Site: lead with positioning, CTA to newest episode; keep the Operator Canvas.
- The deliverable is always the Operator Canvas, rendered from the locked Canvas.

## Later owner rulings (2026-09-23, evening)

- Operator Canvas PDF: figures that facts.md forbids are dropped cleanly, not shown as withheld markers.
- Site Canvas page keeps a low / base / high economics assumptions table (from Canvas §10).
- Shorts publish in order 01–04, Tue–Fri 08:30 ET.

## Costs recorded (session of 2026-09-23 onward)

| Item | Amount |
|---|---|
| Shorts 02–04 voice (ElevenLabs, Original C) | 1,540 credits |
| Shorts 02–04 avatar (Higgsfield) | 612 credits quoted; balance fell 682 (70 unattributed) |
| Shorts 03–04 lip-sync (Fal) | ~$4.44 forecast |
| Thumbnail exploration + upscale (Higgsfield) | ~9 credits |
| YouTube API | free (quota-limited) |

## Incidents and fixes

- A concurrent session committed EP007's staged files under its own message → reworded (unpushed).
- `launch.py` would have uploaded EP006's Shorts from a shared folder → now prefers the episode's `shorts/`.
- Resolve `endFrame` is exclusive → 54 one-frame gaps caught by OTIO check, rebuilt.
- PDF was rendered from a derived worksheet, not the locked Canvas → being re-rendered as Operator Canvas №001.
- OE YouTube channel belongs to a different Google account than the operator's Chrome → avatar is a manual step.

## Still to do (update this file as each lands)

- [x] YouTube uploads + schedule, thumbnail, captions, playlists (2026-09-24) → `launch/links.json`, `launch/UPLOAD-VERIFICATION-2026-09-24.md`, event `ep007-youtube-upload-verified-v1`
  - Episode https://youtu.be/7juZ1KXdd04 · private, publishAt Mon 2026-10-05 11:00 ET (15:00Z)
  - Short 01 https://youtu.be/Hc9j4B9nnk8 · Tue 2026-10-06 08:30 ET (12:30Z)
  - Short 02 https://youtu.be/mpGtH0WC1OA · Wed 2026-10-07 08:30 ET
  - Short 03 https://youtu.be/EtkyEqmKzUY · Thu 2026-10-08 08:30 ET
  - Short 04 https://youtu.be/UWI-v4M78do · Fri 2026-10-09 08:30 ET
  - Playlists (public): Episodes `PLCmSnXQWzHxo`, Shorts `PLdu7PeWE3s2M`
- [ ] Studio: avatar, pinned comments, end screen, altered-content check
- [ ] Site: rebuild with the live link, owner preview, deploy
- [ ] LinkedIn: episode post (Mon 11:00), Shorts posts (Tue–Fri 08:30), newsletter edition
- [ ] Legal review of the licensing claim (open since research)
- [x] Owner approval of the four v0.1 runbooks (2026-09-24)
