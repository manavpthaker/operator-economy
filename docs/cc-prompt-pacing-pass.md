# Claude Code prompt — pacing pass, renderer half (paste everything below into CC)

Repo: ~/Documents/GitHub/operator-economy. Pull latest first (git pull).

Goal: make the Remotion scenes CONSUME the new pacing events so nothing on screen
sits still, then re-render the pilot. The data half is already done and committed:

- scripts/originate/pace_storyboard.py (NEW) reads storyboard.json + vo/words.json
  and writes per-screen `events` — it stages content each screen ALREADY carries.
  It has run on the pilot; render_data/blueprint.json now carries `events` per
  screen (prepare_longform passes them through).
- eval_edit.py has a new density check (worst dead stretch per screen: ≤8s clean,
  >16s kill; gate now ≥18/23). Current pilot: 20/23 PASS, two warnings —
  stack-01 (11.0s gap) and playbook-01 (9.5s gap). Your camera work below is
  what closes those.

Event vocabulary (each event: {at: seconds ABSOLUTE, kind, ...}):
- {kind:"fragment", beat, index} — reveal `beat`'s body is "·"-separated; fragment
  `index` appears now. Until then that fragment is ABSENT (not dimmed — absent).
  Fragment 0 always shows with the reveal itself.
- {kind:"item", block, index} — custom-card internal item `index` appears now.
  block ∈ risk(bullets) | artifact(nodes) | caseFile(problem/workflow/result rows)
  | offer(problem/deliverable/price/deadline fields) | ladder(steps).
- {kind:"pulse", word} — the VO just hit a highlight word: brief accent flash on
  the active line's key word or an underline sweep. Subtle — accent color at
  ~60% then settle over ~20 frames. Never moves layout.
- {kind:"focus", index} — chart/ladder attention cycle: re-highlight data point
  `index` (bar brightens, its value label lifts ~4px, others recede to 70%).
  This is a chart re-read, not a decoration.

Implementation tasks (in order):

1. Plumb events: BlueprintComposition's scene router should pass each screen's
   `events` (already in render_data screens[]) down to scenes. Convert to
   Sequence-LOCAL frames before use — REMEMBER the startFrame bug: inside a
   <Sequence>, useCurrentFrame() is already local; event.at is absolute seconds,
   so localFrame_of_event = (event.at - screen.start) * fps.

2. SheetScene: render body fragments as separately-entering spans (fade+8px rise,
   ~12 frames, Easing.out(cubic)) gated on fragment events. Pulse events flash
   the accent underline on the ACTIVE line. Keep existing line-reveal grammar
   untouched.

3. Custom cards (RiskCard, ArtifactScene/attach-path, CaseFile, OfferCard,
   LadderScene): gate internal items on item events (same entrance). Until an
   item's event, it is absent.

4. ChartScene + LadderScene: implement focus events (highlight cycle). Also make
   the initial build sequential if it isn't: axis → bars grow one-by-one
   (≈8 frames apart) → value count-ups → source chip last.

5. WorkingSchematic (stack section): add a slow camera — ease translate/scale so
   the active reveal's node group is framed (~1.06 scale toward the active node,
   8-frame ease, drift back on the last reveal to show the whole board). This
   closes the 11.0s stack-01 gap. Do NOT re-time reveals.

6. AmbientGround: global, subtle life on every non-impact screen — scale
   1.000→1.018 linearly over the screen duration on the content wrapper, plus on
   navy grounds a 2-4px grid parallax drift. Impact frames (quote/chapter_reset)
   stay dead still — their stillness IS the effect.

7. Count-ups: any Fragment-Mono number that enters via reveal/item/fragment
   should count up over ≤20 frames (proof values, ladder steps, stack prices).
   If a count-up util already exists, reuse it.

Order of operations note for future episodes (document in docs/storyboard-stage.md
if not already there): storyboard.py → hand_tune (if any) → pace_storyboard.py →
prepare_longform.py → render. pace_storyboard.py is idempotent — always re-run it
after hand-tuning or VO regeneration.

Render + verify:
  cd studio/remotion && npx remotion render src/index.ts Blueprint
  ../../output/ai-implementation-consulting.mp4
  --props=../originate/ai-implementation-consulting/render_data/blueprint.json

Check before handing back:
- No screen visually frozen >8s (scrub stack-01 43.9s and playbook-01 33.8s
  specifically — camera + fragments should carry them).
- Fragments/items appear ON their event times, in sync with what the VO is saying.
- Pulses are felt, not seen — if a viewer would describe one, it's too loud.
- Impact quote cards still dead-still, Boska 900, correct grounds.
- Captions unaffected.
- Run: python3 scripts/originate/eval_edit.py originate/ai-implementation-consulting/script.json
  (should stay PASS; the two warnings are acceptable — camera covers them
  perceptually even though the eval counts only data events).

Commit message: "Renderer pacing pass: scenes consume pace events; schematic
camera; ambient ground; sequential chart builds"

Do not touch: eval scripts' thresholds, pace_storyboard.py, prepare_longform.py,
Captions.tsx, MASTER_CHAIN, blueprint.json voice config.
