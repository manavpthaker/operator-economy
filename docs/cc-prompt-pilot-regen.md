# Claude Code prompt — pilot regen in final voice (paste everything below into CC)

Repo: ~/Documents/GitHub/operator-economy. Pull latest first (git pull).

Goal: regenerate the pilot episode VO in the FINAL channel voice (NY-A1) and produce a
fresh render that verifies three fixes already committed: caption hold+fade, Boska 900
impact lines, and the new voice with automatic mastering.

Context:
- Channel voice is FINAL: ElevenLabs "OE Narrator NY-A1" (jd5NxG8GP6b1WEHcoUtt),
  already set in studio/config/blueprint.json with "mastering": true and stability 0.4.
- generate_vo.py masters every section automatically (exciter/presence EQ/de-ess/
  -14 LUFS, duration-preserving). Do NOT add a separate mastering step; do not modify
  MASTER_CHAIN.
- ELEVENLABS_API_KEY is in studio/.env — export it before running.
- Captions.tsx (studio/remotion/src/oe/): HOLD_MAX_S=0.45 + group fade is the correct
  architecture. prepare_longform.py deliberately does NOT tile caption groups (see the
  NOTE in group_words) — beats ARE tiled, captions are not. Do not "fix" either.

Steps:
1. cd studio && set -a && source .env && set +a
2. Delete the stale old-voice VO cache entirely:
   rm -rf originate/ai-implementation-consulting/vo
3. python3 scripts/originate/generate_vo.py originate/ai-implementation-consulting/script.json
   Expect 7 sections; each .mp3 gets a .raw.mp3 sibling (pre-master). Verify mastering
   ran: mastered files should measure ≈ -14 LUFS
   (ffmpeg -i <file> -af loudnorm=print_format=summary -f null - 2>&1 | grep Input).
   Stability is 0.4 — if any single section sounds too theatrical, delete just that
   section's mp3 + words-<id>.json from vo/ and re-run (resumable cache makes it
   surgical). If two regens still overshoot, bump stability to 0.45 in blueprint.json
   for that run and say so in the commit message.
4. python3 scripts/originate/prepare_longform.py originate/ai-implementation-consulting/script.json
5. ONE code task — wire impact-line ground rotation by narrative role, per the
   documented Rev C rule (one accent per frame; rotate GROUNDS, not accents):
   - Ink #1A1A1A ground: thesis / cold-open impact lines
   - Schematic Navy #14263E with the drafting grid: evidence turning-points
   - Paper #F5F0E6 inverted (Ink text): honest-math lines
   QuoteCard.tsx already takes a bg; drive it from the storyboard/scene role
   (thesis|evidence|economics section id is a reasonable proxy if the storyboard has
   no explicit role tag). ChapterReset stays Ink. Boska stays weight 900.
6. cd remotion && npm install (if needed) && npx remotion render src/index.ts
   Blueprint ../../output/ai-implementation-consulting.mp4
   --props=../originate/ai-implementation-consulting/render_data/blueprint.json
   (check remotion.config.ts / package.json for the exact render invocation if that
   doesn't match)
7. Verify before handing back: captions fade out ≤0.45s after a phrase ends (no
   lingering through pauses, no first-word holdover), impact lines are heavy-weight
   Boska on the correct grounds, VO is the NY-A1 voice — NY/NJ accent, pitch moves,
   crisp not muffled.
8. Commit everything including the vo/ artifacts and render_data with message:
   "Pilot VO regenerated in final NY-A1 voice; impact-line ground rotation wired"

Do not touch: eval scripts, confidence.py, blueprint.json voice config, MASTER_CHAIN.
