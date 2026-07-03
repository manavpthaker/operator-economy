# Claude Code prompt — encode the edit grammar into the pipeline (2026-07-03)

Paste everything below the rule into Claude Code from the repo root.

---

**Mission.** Encode the faceless-video edit grammar into the OE video workflow — the storyboard stage, the evals/rubric, AND the Remotion composition. You may rebuild `BlueprintComposition` from scratch. Read these first, in order:

1. `CLAUDE.md` (pipeline architecture, gates, constraints)
2. `docs/faceless-video-editing-research.md` — **the authoritative edit-grammar spec.** Everything below implements it.
3. `docs/faceless-video-craft.md` — supporting research (sound-design numbers, motion parameters, Remotion API patterns)
4. `docs/storyboard-stage.md` — the storyboard-stage design (you will upgrade it to v2)
5. `docs/content-rubric.md` — the 100-pt craft rubric (you will add the edit rubric)
6. `studio/remotion/src/BlueprintComposition.tsx` + `src/oe/` — current render layer

**Non-negotiables:** Rev C design system (`design-system/README.md` §4 + hard bans — one accent per frame, Boska ≥40px only, Fragment Mono for numbers, no gradients/glass, sourced numbers only). Never CSS transitions — every animated value derives from `useCurrentFrame`. Don't touch Gate 1 POV enforcement, `script.json` content, or VO files. The evals are the tests. Hard cuts between screens are allowed (smash cuts are an edit tool); "fades/slides only" governs element motion within screens.

## Phase 1 — rubric + spec (docs)

**1a. `docs/content-rubric.md`:** add a new addendum section "VII. Edit rubric (Gate 3, applied to the rendered video / storyboard)" — separate 20-pt block, gate ≥16, with its own kill list. Criteria (from the research doc's edit-density eval):

- Scene grammar in use: ≥5 quote/punchline moments AND ≥3 artifact/screen-rec/proof screens per 6 min (5 pts, AUTO from storyboard.json)
- Cadence: no static composition >20s unless actively building; composition reset every 25–45s; never >2 consecutive `sheet` screens (5 pts, AUTO)
- Every `broll` query names a concrete noun/action (no abstract queries); every money-claim screen carries a source label (4 pts, AUTO)
- Hook: visual event every 4–8s in first 30s; premise proven (shown) not just stated (3 pts, AUTO+HUMAN)
- Sound: music bed present with per-section change + ducking; SFX on reveals/transitions/impacts; master −14 LUFS ±1, true peak ≤ −1 dBTP (3 pts, AUTO via ffmpeg loudnorm print)

Edit kill list (any = no publish): unresolved placeholder screen · generic/abstract b-roll · >45s without composition reset · unsourced money figure on screen · caption text duplicating a quote card verbatim while the card is up.

**1b. `docs/storyboard-stage.md` → v2:** merge the research doc's layout types and tag system. Layouts: `sheet`, `schematic`, `chart`, `gap`, `quote`, `proof_card`, `artifact`, `offer_card`, `case_file`, `risk_card`, `ladder`, `source_card`, `screen_rec`, `broll`, `chapter_reset`, `cta`. Script tags per beat: `claim` `number` `tool` `operator_pov` `punchline` `risk` `question` `process` `cta`. Tag→layout mapping per the research doc (§"Add script tags before rendering"). Cadence heuristics from §"Visual cadence". Shot hierarchy: artifact/screen-rec > constructed artifact > data viz > quote card > specific b-roll > generic stock (last resort, effectively banned by the kill list).

## Phase 2 — storyboard stage (Python)

**2a. `studio/scripts/originate/storyboard.py`:** runs after `generate_vo.py` (real word timings exist). Input: `script.json` + VO durations + existing `assets.json` if present. Steps: (1) tag each beat (LLM call using the models config in `studio/config/blueprint.json`, same client pattern as the other originate scripts); (2) map tags→layouts; (3) group into screens obeying cadence rules; (4) emit `originate/<slug>/storyboard.json` — schema per `docs/storyboard-stage.md` v2, each screen with layout, heading, reveals (with word-level timing anchors), figure/source, sfx cues (`tick`/`whoosh`/`hit`), and music intensity (`calm`/`build`/`silence`).

**2b. `studio/scripts/originate/eval_edit.py`:** the edit-density eval implementing every AUTO check in Phase 1a against `storyboard.json`. Exit codes + `edit_review.md` escalation report, matching the existing eval conventions (`eval_script.py` / `eval_package.py`). Wire into `confidence.py` (craft-weighted) and `originate.py render`.

**2c. `prepare_longform.py`:** emit `screens[]` (the storyboard) in `render_data/blueprint.json` alongside the legacy `sections[]`.

## Phase 3 — composition v3 (rebuild allowed)

Architecture: `screens[]`-driven, using `@remotion/transitions` `<TransitionSeries>` where it helps (transitions overlap scenes — recompute total duration accordingly), or the existing extended-Sequence cross-dissolve pattern if simpler. Fall back to legacy run-grouping when `screens[]` is absent.

**Scene components** (new, in `src/oe/scenes/`): `QuoteCard` (full-screen single statement, Boska on ink/navy, HARD cut in — no fade — spring scale-settle `spring({config:{damping:200}})` remapped from 0.96→1, hold 1.2–2.5s short / 3–4s long lines, captions HIDDEN while up, L-cut: VO continues over it), `ProofCard` (one number + CitationChip, count-up in Fragment Mono), `ArtifactScene` (framed screenshot/doc with annotation callout + source label), `OfferCard` (problem/deliverable/price/deadline as a card), `RiskCard` (blunt warning, brick accent `#9B3E2E`), `LadderScene` (3-step scale comparison, one sourced figure per step), `SourceCard`, `CaseFile`. Keep/upgrade: `SheetScene` (add the right-hand **figure well** — active line's key number large in mono, swapping per reveal), `WorkingSchematic`, `ChartScene`, `HookGap`.

**Motion:** asymmetric easing tokens in `theme.ts` (entrance `Easing.bezier(0,0,0.2,1)`, standard `(0.4,0,0.2,1)`, exit `(0.4,0,1,1)`); stagger siblings 1–3 frames; land visuals 2–3 frames before their VO word; slow camera drift on every screen (2–4% Ken Burns scale/pan via interpolate on the screen container, alternate direction per screen; the navy drafting grid parallaxes slightly against content); hairlines draw in; citation chips tick in after their figure.

**Sound layer:** (1) music bed — read `music` config from `studio/config/blueprint.json` (add the config block: track paths per intensity, master gain); volume-as-callback ducked −15 to −18 dB under VO, J-cut pre-lap ~15 frames before section changes, HARD SILENCE from ~0.5s before each quote card and the gap reveal; if no licensed track file exists at the configured path, log a warning and render without music (never block, never placeholder-tone). (2) SFX — `remotion/public/sfx/` (tick/whoosh/hit); tick on sheet-line + schematic-node reveals (quiet, −18 dB), whoosh on section transitions, ONE hit per quote card; same missing-file tolerance. (3) Document a post-render loudness step in `docs/pipeline.md`: `ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1 ...` and add it to the render wrapper if one exists.

**Captions:** keep the gold karaoke grammar; hide during `quote`/`chapter_reset` screens (the card IS the caption — duplication is a kill-list item).

## Phase 4 — apply to №001 and re-render

Build `originate/ai-implementation-consulting/storyboard.json` (hand-tune the auto output). Quote-card moments from the research doc (VO timestamps):

| Time | Line | Layout |
|---|---|---|
| 23.55–25.20 | "It's called implementation." | quote (ink) |
| 45.61–47.76 | "The gap was never the software." | quote |
| 48.77–50.72 | "Until it actually ran." | quote follow-up (typewriter hit) |
| 63.65–67.28 | "Why is Accenture charging billions for it?" | quote (question) → evidence |
| 84.66–87.76 | "The AI implementation work is the only thing growing." | proof_card (w/ "flat overall" contrast) |
| 135.85–137.84 | "Services attach to services." | quote → schematic |
| 153.84–157.00 | "That's not scope creep. That's the business model." | quote (high impact) |
| 157.12–170.40 | "Same business, three scales" | **ladder** — the bare-sheet fix: freelancer → boutique → Accenture, one sourced figure per step; payoff feel |
| 258.00–263.64 | "Businesses don't buy automation…" | offer_card ("Missed calls get answered and booked" + price/deliverable) |
| 270.67–274.56 | "Your credibility from the industry you left is the actual asset." | artifact (operator-credibility network map: credibility → warm intro → first install) — REPLACES the broll placeholder at 263.69s |
| 323.33–325.04 | "Revenue stops when you stop." | risk_card |
| 283.80–286.64 | "The first project is designed to surface the second." | schematic (project → retainer) |
| 359.99–362.40 | "Build it. Own it. Operate it." | final brand card |

Then: `python scripts/originate/eval_edit.py originate/ai-implementation-consulting/storyboard.json` must pass; re-render; verify the checklist (no placeholder screens, ≥5 quote moments, ≤2 consecutive sheets, sound layer active or cleanly absent, captions hidden on quote cards); run the loudness step.

**Order of work:** Phase 1 (docs) → 2 (storyboard+eval) → 3 (composition) → 4 (apply + render). Commit per phase with clear messages. If a phase forces a design decision not covered here or by the research doc, choose the option that maximizes trust/authenticity (the brand moat) and note it in the commit message.
