# Launch week — The Phone Call Businesses Never Answer (2026-07-13)

Pre-staged by the e2e run (2026-07-06). Flow: docs/publishing-flow.md. All copy below rubric-gated (linkedin_posts.md, newsletter.md, hour_one.md, dm_shortlist.md).

## Blocked on local render (Manav's machine, from studio/)
- [ ] `cp -r originate/voice-agent-agency/vo remotion/public/vo` (prepare_longform already synced)
- [ ] `cd remotion && npx remotion render src/index.ts Blueprint out/ep002-final.mp4 --props=../originate/voice-agent-agency/render_data/blueprint.json`
- [ ] Shorts ×4: `npx remotion render src/index.ts Short out/short-0K.mp4 --props=../originate/voice-agent-agency/render_data/short-0K.json`
- [ ] Carousel ×10: CarouselSlide comp with render_data/carousel-01..10.json → assemble PDF
- [ ] Review in VLC (never QuickTime)
- [ ] Move final: `mv remotion/out/ep002-final.mp4 originate/voice-agent-agency/`

## Then schedule (Sunday 7/12 night)
- [ ] `python launch.py voice-agent-agency --monday 2026-07-13 --title "The Phone Call Businesses Never Answer"` (dry run → review → `--go`)
- [ ] YT episode Mon 11:00 ET + shorts ×4 Tue–Fri 8:30 ET (launch.py; links land in launch/links.json)
- [ ] SRT captions (drag into YT Studio Subtitles), thumbnail = title-card frame (~21.5s), end screen last 6s
- [ ] AI-disclosure box CHECKED (the episode discloses itself in the thesis — the box still gets checked)
- [ ] OE page episode post Mon 11:00 (copy: launch/hour_one.md; carousel PDF attached LAST, then Schedule)
- [ ] OE page shorts posts ×4 Tue–Fri 8:30 (native vertical + standalone insight text from content/linkedin_posts.md)

## Hour one — Monday 11:00–12:00
- [ ] Sources comment under OE post (launch/hour_one.md §2)
- [ ] Newsletter send (content/newsletter.md — insert YT + blueprint links)
- [ ] Personal repost of OE carousel post + one-liner (launch/hour_one.md §3)
- [ ] Site flip: `python scripts/originate/publish.py voice-agent-agency`

## The week
- [ ] Mon–Tue: DM sends from launch/dm_shortlist.md (no ask, analyst register)
- [ ] Tue–Wed: Product of One group — carousel + genuine question (launch/hour_one.md §4, neutral citation)
- [ ] Tue–Fri: verify shorts live; pin episode-link comments; midweek OE page posts from content/linkedin_posts.md

## Pipeline state (for the record)
- Script: 22/22 evals · craft 70/70 auto · confidence 0.886 AUTO-PASS (script stage)
- Storyboard: hand-tuned (44 screens, 6 quotes) · edit rubric 20/23 PASS, 0 kills
- Prepublish confidence: 0.859 — ESCALATE only on training_mode (mandatory episode review) + 5 tracked weak claims (all hedged aloud)
- VO: 745s (12.4 min) · bridge @ 15.63s · bed v7 mixed
- Meta reveal: the episode's own AI voice is disclosed in the thesis section (Manav's call, 7/6)
