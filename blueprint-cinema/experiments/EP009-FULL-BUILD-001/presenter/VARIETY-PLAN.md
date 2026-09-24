# EP009 presenter variety plan

Status: presenter lane plan, written before any submission. Source: `direction/SHOT-PLAN.json` `presenter_takes` performance briefs and the DIRECTION-PLAN presenter take set. Triggers: EP007 `next-recording-head-variety-v1` (owner deferred head variety to the next avatar recording) and `r40-next-avatar-visible-hands-v1` (visible natural hands).

Rule applied: no two adjacent takes share a head pattern (nod, tilt, turn, lean, side-to-side, look-away, stillness-led) as their main head action, or a hand pattern (single palm up, both palms up, open hand to lens, flat hand, chest touch, placement, air line, shape between hands) as their main hand action. Eyes near lens on every promise; look-aways only on recall lines (P06, P08). Nods: at most one per take, never in adjacent takes.

| Take | Head (main action, word) | Hands (main actions) | Eyes |
|---|---|---|---|
| P01 | small tilt toward his left shoulder on "find", level by "arithmetic"; brows gather on "actually ... her"; still on the question | right palm turns up on "anyone", rests by "arithmetic"; both hands still from "and" to the end | near lens |
| P02 | one gentle settle on "direct"; upright and still for the promise (no lean) | both hands hold a small sheet-sized space on "four numbers", release on "property"; one flat hand lowers a few centimetres on "honestly pay" | near lens throughout (promise) |
| P03 | small turn to camera-right on "site", back by "keeps"; slow lean-in "who ... inn?"; small tilt toward his right shoulder on "nobody"; still with lightly gathered inner brows on the last question | right hand sets a place on the table to his right on "site", left hand sets a second place to his left on "guest's email"; hands draw together on "When"; one palm opens outward toward lens on "outside" | near lens on the final question |
| P04 | upright; one small firm nod on "number" | right hand lightly to chest on "I think"; flat horizontal line drawn in the air on "recovers", held to "number" (ceiling line, first of two); hand lowers to rest on "any inn" (no open hand, to differ from P03) | near lens on the promise |
| P05 | slight tilt with a relaxed brow on "Fair question here", back to centre on "doesn't" | both palms turn up together on "do it?" and return | near lens |
| P06 | brief look-away down to his left on "I could not find anyone", back on "selling"; small side-to-side weighing on "nobody selling this has published" | fingertips lightly together at the start; on "published what" the fingers part and the hands separate a little, palms facing each other, then rest (not palms up, to differ from P05) | recall glance only at the start |
| P07 | slight lean back on the first sentence, forward to centre on "It's"; one short downward nod on "wrong number"; still on "It needs the sites" | right hand sweeps a small set-aside motion across the table on "stops"; both hands flat and quiet on "needs the sites"; right hand slides a short distance across the table on "can shift" | near lens |
| P08 | quietest take: near-still to lens; one brief look-away up-left on "a decade ago", back on "I've"; still through the limits sentence; on "That's the test, not the pitch" the head stays still and the jaw sets calmly (no nod, to differ from P07) | at rest; on "I don't know what a thirty room inn will pay to fix it" one hand lifts a little and turns outward, back to rest by "That's" | near lens except the one recall glance |
| P09 | small tilt toward his right shoulder on "hypotheses", firmly upright on "I won't" | one hand, fingers spread, lowers flat onto the table on "not a funnel", stays through "conversion rate", lifts back on "one" | near lens |
| P10 | stillness-led: still through "That's a side income. It's a foothold. It is not a living." and the pause (no nod, to differ from P11); slight chin lift on "the band" | at rest through the three sentences; right flat palm rises one small step on "Up the band it becomes a business" and returns | near lens |
| P11 | centred; one small nod on "build"; no movement on "Bounded"; slight turn to camera-left on "from four directions", back; small settles on "direct" and "cheap"; slight forward lean on "So build the audit" | two flat hands set a small box on the table on "Bounded", hold, release on "The"; open right palm on "real"; left palm on "direct"; rest on "cheap"; thumb and forefinger close to a thin gap on "thin"; forward open hand on "build the audit", then rest | near lens |
| P12 | slight candid lean back on the first sentence; level on "including me"; near-lens and still for "You'll know by day thirty"; lighter small tilt on "The first move costs you an afternoon" | rest through the first sentence; right hand lightly to chest on "me"; one raised index finger, pointing up, on "one innkeeper"; flat horizontal line in the air on "Run the ceiling" (callback to P04) | near lens on "day thirty" |
| P13 | warm, slightly forward on the first sentence; upright on "Not to close them"; small side-to-side consideration on "whether this business exists"; complete stillness on "Right now nobody knows"; settled for the ask | open hand toward lens on "pay"; palm-down small wave-off low over the table on "Not to close them"; both hands shape a small size on "at their size"; rest on "Right now nobody knows"; one small open hand on "leave a like", then rest | near lens on "nobody knows" and the ask |

## Adjacency check

- Head main actions in order: tilt, settle-and-still, turn and lean-in, nod, tilt, look-away and side-to-side, lean back and nod, stillness and look-away, tilt, stillness and chin lift, nod and turn, lean back and tilt, forward and side-to-side. Nods: P04, P07, P11 only (never adjacent). Tilts: P01, P03 (secondary), P05, P09, P12 (secondary): P03 to P05 are separated by P04.
- Hand main actions in order: single palm up, held sheet, placements, chest and air line, both palms up, fingertips then separate, sweep and slide, lift and turn out, spread flat hand, palm step up, box and pinch, chest and raised finger and air line, open hand and wave-off and size shape.
- The air-drawn ceiling line appears exactly twice (P04, P12) by design; chest touch appears twice (P04, P12), not adjacent.

## Deviations from the SHOT-PLAN briefs (all small, recorded for review)

1. P02: forward lean on "By the end" removed; P03's lean-in is the adjacent take's main head action.
2. P04: closing "hand opens toward lens on any" changed to a plain lowering to rest; P03 ends on an outward palm to lens.
3. P06: closing "small open empty-hands gesture" changed to hands separating, palms facing; P05 is both palms up.
4. P08: small nod on "That's the test" replaced by stillness with a calm set of the jaw; P07 nods.
5. P10: slow nod on "foothold" replaced by stillness; P11 nods on "build".
6. P03: the brief's left hand placing to his right (and right hand to his left) would cross the arms; each hand places on its own side instead. The two places, site and inn, are kept.

Provider limit: Seedance 2.5 maximum is 30 s (models_explore, 2026-09-16), so P08 (24 s) and P11 (23 s) run as single takes; no length fallback split is used.
Known limit: Seedance does not reliably honour word-timed gestures (EP007 `lesson-i2v-ignores-timing-prompts-v1` for Kling; R59 body drift). Gesture timing is a request, reviewed per take, not a guarantee.
