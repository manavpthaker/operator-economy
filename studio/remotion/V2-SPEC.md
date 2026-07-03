# BlueprintComposition v2 — "The Working Schematic Edition"

Spec for the rebuild (v1 was a mechanical scaffold; verdict from the pilot render: "not even an okay slide deck" — correct). Design authority: `/design-system/` (Rev C). Same `render_data/blueprint.json` props contract — no pipeline changes.

## The core motion idea (the thing v1 completely lacked)

**The episode IS a schematic being drawn.** The Rev C "Working Schematic" — navy drafting panel, wired nodes with real prices, sage RUNNING pulses — becomes the video's persistent world. As the narration progresses, the business gets *assembled on screen*: the thesis section drops the first node, the stack section wires in each tool (with its real monthly price), the playbook connects client nodes, the economics section draws the measurement bracket over the whole system. **By the sign-off, the completed, running schematic of the business is on screen — the thesis visualized.** End-card = the engineering title block with the blueprint CTA.

This is narratively motivated motion (semantic density, per the craft rubric) — not decoration.

## Scene grammar (replaces v1's undifferentiated slides)

| Beat type | Treatment |
|---|---|
| Hook | Ink world. Mono numeral count-up ($5.9B), then the **GapFigure** gold arrow `$5.9B → $2K` — the signature move, once per episode |
| Section transitions | **Sheet cards**: `SHEET 02 OF 07 — THE EVIDENCE` (SheetHeader style, drafting frame draws itself in ~320ms) |
| Stats/claims | **Stat** blocks: Fragment Mono numerals with count-up easing + **CitationChip** lower-third (`SOURCE: CIO DIVE · FY2025`) on EVERY figure; gold `ESTIMATE`/`REPORTED — UNVERIFIED` variant chips |
| Charts | Rev C BarChart language: hairline axes, mono labels, one gold highlight bar, bars grow with spring ease, citation chip bottom-left |
| Slides (lists) | Killed as a format. Replaced by: annotation rail reveals — thin callout lines + small-caps labels annotating the schematic or a figure, staggered 120ms |
| Schematic beats | Nodes drop in with wire-draw animation; each node carries its real figure (placeholder nodes banned per DS) |
| B-roll | Monochrome-treated (Ink duotone), subtle scale drift, citation-style location label — phase 2: AI-generated b-roll (Runway/Veo API) replaces stock |
| Captions | Keep word-timing; restyle: Supreme 500, Paper color, gold active-word (replaces sage), lower placement, tighter measure |

## Tokens & type in Remotion

Palette from `tokens/colors.css`: Ink #1A1A1A · Paper #F5F0E6 · Schematic Navy #14263E · Ledger Gold #C4A45F (dark surfaces) · Sage = status pulses only. One accent per frame. Fonts: Fragment Mono (via @remotion/google-fonts), Boska/Zodiak/Supreme (Fontshare CSS — load with delayRender/continueRender, or vendor the woffs into `remotion/public/fonts/`). Boska ≥40px hard floor. Motion: fades/slides only, 120/200/320ms curves scaled to frames; no whip-pans/zoom-punches (DS + craft-rubric ban).

## Audio (part of "dynamic," cheap win)

Music bed under VO (−26dB, duck −6dB more under speech via sidechain-style volume automation on the Audio component); sparse tick/whoosh SFX on node-drops and sheet transitions. Source: YouTube Audio Library (free, safe) to start.

## What we do NOT do

- No deck-in-Figma/Canva → animate-elsewhere flow: manual step, breaks automation, lower ceiling than Remotion (which renders anything a browser can).
- No template-video APIs (Creatomate/JSON2Video): template ceiling, generic look.
- No Motion Canvas migration (research verdict stands).
- AI video generators (Runway Gen-4, Veo) are an ASSET layer (b-roll clips composited inside Remotion), never the compositor. Phase 2.

## Build order

1. Port tokens + fonts into `remotion/src/oe/` (theme.ts + font loader).
2. Frame-driven primitives: `MonoCounter`, `CitationChip`, `SheetCard`, `StatBlock`, `AnnotationRail`, `GapArrow`, `OEBarChart` (adapt DS `.jsx` components — they're CSS-transition based; re-drive with `useCurrentFrame` + `spring`).
3. `WorkingSchematic` composition layer: node registry per episode (nodes/wires declared in assets.json via new optional `schematic` spec), progressive assembly keyed to sections.
4. Scene router: replace v1's slide/chart/fallback switch with the grammar above.
5. Audio bed + SFX.
6. Re-render pilot, A/B against v1, iterate with Manav's design pass.

Asset-plan implication: `plan_assets.py` prompt gains the new spec types (`stat`, `sheet`, `annotation`, `schematic_node`) once v2 lands.
