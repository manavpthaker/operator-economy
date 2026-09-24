# EP009 Shorts R4 — the standalone-payoff revision

Four 9:16 private review candidates, re-cut and re-copied so each one orients a cold viewer in
its own speech and resolves one narrow answer before it ends. Built only from already locked
material: the r3 narration master, its word transcript, the r8 tool-clarity carrier and the
accepted look-transfer natives. **No provider call, no generation, no retime, no spend.**

Governing ruling: owner, 2026-09-21 — decision event `ep009-owner-shorts-standard-ruling-v1`,
source record
`blueprint-cinema/episodes/EP009-direct-booking-recovery/review/source-records/2026-09-21-owner-shorts-rulings.json`.
Governing standard: `docs/content-rubric.md`, Shorts addendum, kill list and Shorts derivative
checks. `cliffhanger_line` is retired.

Review page: `blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/qa/ep009-shorts-r4/index.html`
(private host path `https://mini.tail1c89f5.ts.net:3071/ep009-shorts-r4/`).

| # | Title | Duration | Frames | Re-cut | Validator |
|---|---|---|---|---|---|
| 01 | When the guest returns, the commission does too | 16.71 s | 401 | yes, proof beat +78 frames | exit 0 |
| 02 | Cheap parts, and a job still left to sell | 24.25 s | 582 | yes, orientation beat +155 frames | exit 0 |
| 03 | The booking site keeps the guest's email | 17.17 s | 412 | yes, answer beat +46 frames | exit 0 |
| 04 | The commission total is the wrong number | 16.54 s | 397 | no | exit 0 |

Publish order carried forward from the copy package: **01, 04, 02, 03**.

## What to read

- `STANDARD-JUDGMENT.md` — the per-Short judgment against the standard, before and after, with
  the frames and words that decide it. Start here.
- `COPY-DELTA.md` — what of the approved copy was applied where, and the six places the re-cut
  forced a minimal change.
- `<slug>/manifest.json` — the `shorts_contract.py` manifest: cold-viewer context, hook,
  payoff, closing line, standalone payoff, pinned comment, description.
- `<slug>/CONTRACT-VALIDATION.json` — the validator command, its exit code and its actual JSON.
- `<slug>/source-contract.json` — exact master frame ranges, native frame ranges, ffmpeg
  transform chains, what changed against r3 and what it cost.
- `VERIFICATION.json` — frame counts, per-beat audio correlation against the locked master,
  per-frame luma spread, locked-source digests, and what could not be judged.
- `PHONE-PLAYBACK-QA.json` — browser playback at 390×844, unmuted, normal speed.
- `LOCK-PRESERVATION.json` — every source read, with `all_unchanged: true`.
- `superseded/README.md` — the r3 renders that must not be picked up.

## Per Short

Each project directory holds `build.py` (self-contained and re-runnable), `index.html`,
`index.motion.json`, `compositions/`, `assets/`, `captions.json`, `captions.srt`,
`captions.vtt`, `manifest.json`, `CONTRACT-VALIDATION.json`, `source-contract.json`, and
`review/<slug>-r4.mp4`.

Captions are burned-in phrase groups generated from the locked word timings and composited as
an overlay on the picture — no reserved keep-out band, per `.agents/skills/captions-overlay`.
The `.srt` and `.vtt` sidecars carry the same verbatim text; in Short 03 the sidecars
additionally carry the final spoken line, which is deliberately not railed because the answer
card carries those exact words on screen at that moment.

## Rebuild

```bash
cd blueprint-cinema/experiments/EP009-SHORTS-004
for d in 01-second-commission 02-cheap-tools 03-guest-relationship 04-wrong-number; do
  (cd "$d" && python3 build.py && npx --yes hyperframes@0.8.53 check --strict \
     && npx --yes hyperframes@0.8.53 render -o "review/$d-r4.mp4" --quality delivery --strict-all)
done
python3 write_manifests.py
python3 verify.py
python3 build_review.py
```

`build.py` refuses to run if any locked source fingerprint has changed.

## Boundaries

- **Nothing here is owner acceptance.** All four carry `owner_approved: false`.
- No upload, no publication, no scheduling. Related Video is unbound on all four.
- EP009's slug is `direct-booking-practice`. The episode URL is the literal placeholder
  `[EPISODE_URL]` everywhere and stays that way until `launch/links.json` originates one. The
  live August episode URL, which belongs to EP006 `direct-booking-recovery`, is not restated in
  this revision.
- Short 03's answer beat carries a designed card rather than presenter picture, because no
  lip-synced frames exist for that narration. See `STANDARD-JUDGMENT.md`.
- Perceptual lip sync was not machine-verified on any beat.
