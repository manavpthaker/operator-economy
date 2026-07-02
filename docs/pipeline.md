# Producing one video (end to end)

Engine lives in `../studio` (vendored from viddy 2026-07-02 — this copy is canonical for OE). Channel config: `studio/config/blueprint.json`.

```bash
cd studio   # from repo root

# 0. Research brief (Claude/Cowork deep research → save as md)
# 1. Script — stops at Gate 1
python originate.py new "AI receptionists for independent hotels" --research brief.md

# GATE 1 (~30-45 min): edit originate/<slug>/script.json
#   - replace every [POV: ...] token with your experience  ← monetization moat
#   - verify every number against sources

# 2. VO + asset plan — stops at Gate 2
python originate.py continue <slug>

# GATE 2 (~15-30 min): review assets_review.md, record screen_rec shot list

# 3. Render data + derived content (blueprint.md, newsletter.md, LI posts, shorts briefs)
python originate.py render <slug>

# GATE 3: preview in Remotion Studio, then:
cp -r originate/<slug>/vo remotion/public/vo   # audio must be reachable by staticFile
cd remotion && npx remotion render src/index.ts Blueprint ../output/<slug>.mp4 \
    --props=../originate/<slug>/render_data/blueprint.json

# 4. Shorts — existing viddy pipeline on the rendered long-form
python pipeline.py output/<slug>.mp4

# 5. Publish (seeding motion — order matters, per research synthesis)
#   - upload long-form, CHECK THE AI-DISCLOSURE BOX, schedule
#   - blueprint.md → email-gated lead magnet page (single-field opt-in; video-SPECIFIC magnet)
#   - within FIRST HOUR of publish: newsletter send with the video (early watch-time signal)
#   - LinkedIn: NATIVE document/carousel of the core framework — YT link in COMMENTS only
#     (external links in post body cost 50-70% reach); text posts Tue-Fri
#   - shorts → YT Shorts (pinned comment → long-form) + LI native video; shorts ≤40% of uploads
# 6. Log the video in videos/<slug>/ (links, publish date, then 7/30-day stats)
```

Target: ~60–90 min human time per video across the three gates.

## Not yet automated (Phase C)

YouTube API upload + A/B titles · analytics readback into topic scoring · b-roll auto-fetch for originate · vo→remotion/public copy step.
