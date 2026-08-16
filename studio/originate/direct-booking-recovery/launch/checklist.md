# EP006 launch pre-flight — 2026-08-16 16:00 ET

**Episode:** EP006 `direct-booking-recovery` — "Hotels Pay 30% to Book Their Own Rooms"
**Target Monday:** 2026-08-17 (inferred; not set in script.json or blueprint.json)
**Run by:** brownbot oe-sunday-launch-prep 2026-08-16

---

## Step 0 — Destructive-overwrite guard

- PASS `launch/links.json` does not exist — clear to proceed, no backup needed

---

## Step 2 — Asset pre-flight

- FAIL `ep*-final.mp4` — MISSING. Remotion render has not been run.
- FAIL `render_out/short-*.mp4` (or `shorts/short-*.mp4`) — MISSING. 4 expected, 0 found.
- FAIL `Operator-Blueprint-*.pdf` — MISSING.
- FAIL `ep*.srt` — MISSING.
- FAIL `thumbnail-*.png` — **HARD STOP.** No thumbnail file exists. EP003 got 0.0% CTR on 142 impressions because no thumbnail was generated and nothing noticed. This check exists because of that incident.
- FAIL `content/launch_linkedin.md` — MISSING. `launch.py` rubric-lints this file and hard-fails if absent.
- PASS `content/linkedin_posts.md` — present.
- PASS `content/trailer_linkedin.md` — present.
- NOTE `trailer.mp4` — missing. `content/trailer_brief.json` exists. Per rules, a missing trailer is skipped and never delays the episode.

---

## Step 3 — Evals

- PASS `eval_script.py --mode approved` — exit 0, 22/22 checks pass. Zero [POV:] tokens. No hype lexicon. All money claims sourced or marked estimate.
- PASS `eval_package.py` — exit 0. Craft auto-score 69/75. Structure micro-open-loops check failed (1/5 sections flagged). Projected gate pass (needs ≥80/100 total; human-judged portion not yet scored).
- ESCALATE `confidence.py --stage prepublish` — exit 2 (normal verdict, not a crash). Score 0.921, above 0.85 threshold, but ESCALATE because `training_mode: true` makes pre-publish review mandatory. Two weak claims flagged: `$135,000/year commission-loss figure` (illustrative model) and `5-15% RevPAR uplift` (vendor self-report, unverified). Human review required before scheduling.

---

## Step 4 — Dry-run launch

- FAIL `launch.py direct-booking-recovery --monday 2026-08-17 --title "Hotels Pay 30% to Book Their Own Rooms"` exited 1: "episode video not found — pass --video". Dry run cannot complete without a rendered video. No `links.json` written.
- NOTE Monday date (2026-08-17) and title ("Hotels Pay 30% to Book Their Own Rooms") are inferred — not set in `script.json` or `render_data/blueprint.json`. Confirm both before running launch.py.

---

## Step 5 — URL discipline

- FLAG `studio/originate/too-small-to-bother/launch/thumbnail-note.md:30` contains `https://youtu.be/pF_Tf8qd8xs` (EP005 YouTube Studio draft ID) outside a `launch/links.json`. Per URL discipline rules, any `youtu.be` hit outside `links.json` is a hard stop. Context: this is an internal ops note for a manual thumbnail upload step, not publishable copy. EP005 is not shipping this week. Manav to review and either remove the URL or acknowledge it is safe.
- PASS Research files (`research/thumbnails/compset.json`, `research/reports/`) — YouTube URLs are external competitor citation links, not episode video IDs. Not a concern.
- PASS EP006 content files (`content/*.md`) — no YouTube URLs found. Copy is clean.
- PASS Already-launched episodes (`solo-design-agency`, `voice-agent-agency`, `boring-automation-agency`) — URLs in their content files are for live published episodes. Expected.

---

## Step 6 — AI disclosure

- HUMAN STEP at upload: "Altered content / AI disclosure: YES (synthetic VO)" — cannot be checked here.

---

## content-os doctor.sh --gate verdict (verbatim)

```
content-os doctor — week of 2026-08-10

repos
  ok    brown-man-content found
  ok    operator-economy found

uncommitted work
  ok    brown-man-content clean (last commit 2026-08-16)
  warn  operator-economy has 12 uncommitted paths (last commit 2026-08-16)

date-hardcoded prompts
  ok    no prompt pins a specific week

episode URL integrity
  warn  pass --slug <episode> to check episode URL integrity

image readiness — week of 2026-08-10
  ok    every image-day has a rendered PNG
  ok    0 post(s) flipped to ready

measurement loop
  ok    last review 2026-08-15-weekly-review.md (1d ago)

landmine guards
  ok    publish_mon.sh requires an explicit slug

single source of truth
  ok    every rule doc redirects to content-os
  ok    no instruction surface asserts a retired pillar-mix / voice-blend value

release gate
content-os gate — week of 2026-08-10
  specs: 65 banned terms, 332 sourced numbers, 31 do-not-state claims, no known video ids

  BLOCK monday/article.md: banned term: 'best'  (override with <!-- gate:allow best -->)
  BLOCK monday/article.md: unsourced claim: $674,000  (override with <!-- gate:allow $674,000 -->)
  BLOCK monday/article.md: unsourced claim: 2006  (override with <!-- gate:allow 2006 -->)

1 piece(s) checked.
HELD — 3 block(s). Nothing releases until these clear.
Fix them, or re-run with --warn-only if you are deliberately overriding.
  FAIL  copy is HELD by the gate (see above)
  warn  pass --slug <episode> to gate on-screen graphics

one or more checks failed — fix before publishing.
```

---

## Blocking items for 19:00 review

1. **No rendered video** — `ep*-final.mp4` missing. The Remotion render must be run before anything else can proceed. All downstream artifacts (shorts, captions, finalize) depend on this.
2. **No thumbnail — HARD STOP** — `thumbnail-*.png` missing. Refer to EP003 (0.0% CTR on 142 impressions). Generate and confirm before scheduling.
3. **No shorts** — `render_out/short-*.mp4` missing (4 expected). Must be cut from the rendered video via `pipeline.py`.
4. **No blueprint PDF** — `Operator-Blueprint-*.pdf` missing.
5. **No captions** — `ep*.srt` missing.
6. **`launch_linkedin.md` missing** — `launch.py` will hard-fail. Must be created before the launch run.
7. **content-os gate HELD** — `monday/article.md` has 3 blocks (banned term 'best'; unsourced '$674,000'; unsourced '2006'). Nothing releases until cleared.
8. **confidence.py ESCALATE** — normal verdict, not a crash. `training_mode: true` makes manual review mandatory before scheduling. Two weak claims require acknowledgement: the $135K commission-loss estimate and the 5-15% RevPAR vendor claim.
9. **EP005 YouTube URL outside links.json** — `too-small-to-bother/launch/thumbnail-note.md:30` contains `youtu.be/pF_Tf8qd8xs`. Review and resolve.
10. **Monday date and title not confirmed in config** — `script.json` and `blueprint.json` return `None` for both. Confirm 2026-08-17 is the target before running `launch.py`.

## Non-blocking notes

- Trailer: `trailer.mp4` missing, `trailer_brief.json` present. Per rules, skipped — never delays the episode.
- eval_package.py: structure micro-open-loops check flagged 4 of 5 sections as lacking markers. Does not fail the gate (score is projected-pass); human rubric judgement covers it.
- operator-economy has 12 uncommitted working-tree paths (Manav's in-progress changes). These were not committed by this pre-flight — they belong to the active editing session.
