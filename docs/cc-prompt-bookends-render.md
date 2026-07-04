# Claude Code prompt — bookends + pronunciation render (paste everything below into CC)

Repo: ~/Documents/GitHub/operator-economy. Pull latest first (git pull).

Goal: render the pilot and verify two committed changes. NO data work is needed —
VO, storyboard, pacing, and render_data are already regenerated and committed.
This is a render + verify session.

What changed (context, don't redo):
- Pronunciation: eleven_v3 IGNORES pronunciation dictionaries — generate_vo.py now
  uses speech_aliases (blueprint.json): the voice speaks "en eight en" / "zappier" /
  "air table", and restore_alias_words() puts the display words ("n8n", "Zapier",
  "Airtable") back into words.json so captions read correctly. Stack section was
  regenerated with this; other sections untouched.
- Bookends: BrandSting (navy+grid, 1.8s) → TitleCard (paper, episode title +
  thesis, 3.2s) → episode → OutroCard (navy+grid, domain + CTAs, 6.0s). New file
  studio/remotion/src/oe/scenes/Bookends.tsx; BlueprintComposition wraps the
  episode in a Sequence offset by the intro; render_data.total_frames already
  includes the bookends (Root.tsx calculateMetadata reads it — no change needed).
- Quote grounds: ink fully retired; navy+grid default (QuoteCard, ChapterReset,
  section fallback).

Render:
  cd studio/remotion && npx remotion render src/index.ts Blueprint \
    ../../output/ai-implementation-consulting.mp4 \
    --props=../originate/ai-implementation-consulting/render_data/blueprint.json

Verify (scrub these moments before handing back):
1. 0:00–0:05 — brand sting on navy+grid ("The Operator Economy" / gold rule /
   "Build. Own. Operate."), then paper title card with the episode title and
   thesis. Text should not clip; if the Boska title wraps to 3+ lines, reduce
   its fontSize in Bookends.tsx TitleCard (currently 104/124 by length).
2. First VO word lands AFTER the title card, at ~5.0s, in sync with the hook
   screen and captions (everything shifted by exactly the intro duration —
   if captions are offset from VO, something double-shifted; check that
   Captions sits INSIDE the episode Sequence, audio too).
3. Stack section (~3:30–4:15): listen for "en eight en", "zappier", "air table";
   captions must DISPLAY "n8n", "Zapier", "Airtable".
4. Section transitions still carry the 0.85s breath.
5. Sheet ordinals advance across screens (01 → 02 → 03 within a section).
6. All quote cards + chapter resets on navy with the drafting grid — zero
   near-black grounds anywhere.
7. Last ~6s: outro card — tagline in Boska 900, theoperatoreconomy.com in gold
   mono, two CTA rows, brand line. Confirm total duration ≈ 332s + 11s bookends.

If anything fails, fix the RENDERER side only (Bookends.tsx / BlueprintComposition
wiring). Do not touch: generate_vo.py, pace_storyboard.py, prepare_longform.py,
eval scripts, blueprint.json, vo/ caches, storyboard.json.

Commit after verification:
  "Pilot render with bookends + corrected pronunciation (verified)"
