# EP004 `solo-design-agency` — local runbook

Generated 2026-07-31. Adapted from `docs/pipeline.md` for this episode.
Everything runs from `studio/`. Renumbered to **№004** (was 5; swapped with
`small-cohort-business`, which is now №005).

**Current state:** Gate 1 evals pass **21/22** in `--mode approved`. The only
failure is the two `[POV:]` tokens. Confidence 0.979 AUTO-PASS.

```bash
cd studio
set -a && . ./.env && set +a     # ANTHROPIC / ELEVENLABS / HEYGEN / OPENAI keys
```

---

## 0. Gate 1 — the POV pass (only you can do this)

Two tokens. `originate.py continue` hard-fails until both are gone.

```bash
grep -n "\[POV:" originate/solo-design-agency/script.json
```

- **`evidence` beat 6** (~40–60 words) — sits between *"six emails is not a sample"*
  and the Superside pivot. One concrete detail from building a BusyLobby demo for a
  real prospect: what made you pick them, how long it took, what PostHog showed when
  they opened it, what the callback said.
- **`stack` beat 4** (~30–50 words) — the setup is already written (*"What the stack
  doesn't do is pick…"*). One time a tool handed you something genuinely good and you
  overruled it, and why. This is the load-bearing one: the section argues production
  collapsed but judgment didn't, and right now that's asserted, not shown.

Verify before moving on:

```bash
python scripts/originate/eval_script.py originate/solo-design-agency/script.json --mode approved
# want: 22/22, "POV: zero tokens remain (Gate 1 complete)"
```

---

## 1. Phase 2 — VO, avatar, assets, storyboard

```bash
python originate.py continue solo-design-agency
```

Runs: approved evals (hard gate) → ElevenLabs VO ×7 sections → HeyGen avatar corner
clips → VO timeline reassembly → `plan_assets` → `storyboard` → storyboard pacing
evals → edit rubric §VII.

**Resumable.** VO is cached per section and avatar jobs persist in
`originate/solo-design-agency/avatars/jobs.json` — if a poll times out, just re-run
the same command.

Then eyeball `avatars/*.mp4`. If the twin reads uncanny, set `avatar.enabled=false`
in `config/blueprint.json` and re-run.

---

## 2. Hand-tune the storyboard (every episode has needed this)

The auto storyboard scores ~8/23 on the edit rubric — static one-reveal screens.
Hand-tuned lands ~20/23. All three shipped episodes have their own script; copy the
most recent as the starting point:

```bash
cp originate/boring-automation-agency/hand_tune_storyboard.py \
   originate/solo-design-agency/hand_tune_storyboard.py
# edit: slug, № 004, and anchor screens to THIS episode's performed-VO phrases
#       (it reads vo/words.json + vo/timeline.json, so it's voice-agnostic)

python originate/solo-design-agency/hand_tune_storyboard.py
python scripts/originate/eval_storyboard.py originate/solo-design-agency/script.json
python scripts/originate/eval_edit.py originate/solo-design-agency/script.json
```

Edit rubric escalates below 16/20 or on any kill (unresolved placeholder, abstract
b-roll, unsourced money claim, >2 stacked sheets, static hold >45s).

---

## 3. Phase 3 — render data + derived content

```bash
python originate.py render solo-design-agency
```

Runs: `prepare_longform` → edit rubric → `derive_content` (blueprint.md,
newsletter.md, linkedin_posts.md, shorts_briefs.json, trailer_brief.json,
youtube_metadata.md) → craft rubric incl. shorts checks → prepublish confidence →
**thumbnail candidates** (new step).

The thumbnail step will **exit 2** — that's expected and not a failure. It means no
scene image exists yet. See §4.

---

## 4. Thumbnail (this is what EP003 skipped, and it cost 0.0% CTR)

Generate the café scene from the prompt in `launch/thumbnail-note.md` (Gemini, Pro
model, click "Create image" first), then:

```bash
cp ~/Downloads/<generated>.png remotion/public/thumbs/solo-design-agency-a.png
python scripts/originate/prepare_thumbnail.py originate/solo-design-agency/script.json

cd remotion
npx remotion still src/index.ts Thumbnail ../output/thumb-004-a.png \
    --props=../originate/solo-design-agency/render_data/thumbnail-a.json
npx remotion still src/index.ts Thumbnail ../output/thumb-004-b.png \
    --props=../originate/solo-design-agency/render_data/thumbnail-b.json
cd ..
```

**Ship gate: judge both at 320px AND 168px.** Candidate B's text still needs writing
by hand — only `850 vs 1` came out rubric-clean (see the note).

---

## 5. Render the long-form

```bash
cp -r originate/solo-design-agency/vo remotion/public/vo   # staticFile needs this; not automated yet

cd remotion
npm run studio          # optional: preview first
npx remotion render src/index.ts Blueprint ../output/solo-design-agency.mp4 \
    --props=../originate/solo-design-agency/render_data/blueprint.json
cd ..

# Loudness — required for publish (YouTube normalizes to -14 LUFS)
ffmpeg -i output/solo-design-agency.mp4 -af 'loudnorm=I=-14:TP=-1:LRA=11' \
    -c:v copy output/solo-design-agency.norm.mp4

python scripts/originate/eval_edit.py originate/solo-design-agency/script.json \
    --rendered output/solo-design-agency.norm.mp4
```

---

## 6. Shorts + trailer

```bash
python scripts/originate/prepare_shorts.py originate/solo-design-agency/script.json \
    --video output/solo-design-agency.norm.mp4
python scripts/originate/write_shorts_scenes.py solo-design-agency   # v2 scenes — words-only shorts underperform

cd remotion
for n in 01 02 03 04; do
  npx remotion render src/index.ts Short ../output/short-$n.mp4 \
      --props=../originate/solo-design-agency/render_data/short-$n.json
done
cd ..

# Trailer (optional — a missing trailer never delays the episode)
python scripts/originate/prepare_shorts.py originate/solo-design-agency/script.json --trailer
cd remotion && npx remotion render src/index.ts Short ../output/trailer.mp4 \
    --props=../originate/solo-design-agency/render_data/trailer.json && cd ..
```

**Kicker now reads № 004 automatically** — that was hardcoded to № 001 until
2026-07-31 and every prior short shipped with the wrong number.

---

## 7. Blueprint PDF

```bash
python scripts/originate/render_blueprint.py originate/solo-design-agency/script.json \
    --number 004 --rev A --hero "850 vs 1" \
    --hero-caption "Same business model. Three orders of magnitude apart in headcount."
```

---

## 8. Launch package

```bash
# Dry run first — prints the plan, writes the package with placeholders
python launch.py solo-design-agency --monday 2026-08-03 --title "One Person, $5,000 a Month, No Employees"

# Then for real (uploads + schedules via YouTube API)
python launch.py solo-design-agency --monday 2026-08-03 --title "..." --go
```

Writes `launch/checklist.md`, `links.json`, `dm_shortlist.md`. Rubric-lints every
LinkedIn copy file; hard fails abort.

---

## 9. Publish

```bash
python scripts/originate/publish.py solo-design-agency --rev A --date 2026-08
```

Manual, in YT Studio — the parts no script does:

- **Check the AI-disclosure box** (synthetic VO — mandatory, Jan 2026 policy)
- Audience = NOT made for kids
- Upload SRT captions, set the custom thumbnail, add the end screen
- Add to the episodes playlist
- **Schedule ≥24h out**, don't publish-now
- Post the pinned comment once live — **with real URLs, no "link in bio."**
  EP002's shorts pulled 403 views into a pinned comment with no clickable link.
- Newsletter send within the first hour (early watch-time signal)

---

## Blocking gate you can't skip

`autonomy.training_mode` is `true` in `config/blueprint.json`, so the pre-publish
episode-library review is **mandatory regardless of confidence score**. Review the
whole set — video, shorts, posts, newsletter, blueprint — before scheduling.

## Open item

Confirm BusyLobby's numbers against `busylobby/tracking/autopilot-pipeline.csv`
before VO. `evidence#4` says "six outreach emails, one callback, no signed client"
and it's first-party and load-bearing. That repo isn't mounted in Cowork, so it was
never verified against source.
