# The Operator Economy — Design System (Rev C)

> **Build. Own. Operate.** — Documentary-grade evidence for the businesses experienced professionals could actually build now that AI collapsed the cost of building.

This design system encodes the visual and verbal language of **The Operator Economy**, a YouTube channel + newsletter + blueprint library aimed at skeptical senior professionals (35–55). The north-star test for every decision: *would a 45-year-old VP of Product share this under their real name on LinkedIn?*

**The idea (locked, Rev C): design like a blueprint, not like a publication — and make the blueprint feel ALIVE.** Premium-editorial trust (cream, serif, restraint) fused with **The Working Schematic**: a navy drafting panel where the business being described is drawn as a live, running system — labeled nodes, wires, real prices, verified sources. It looks like the business the viewer is going to build, because it is.

---

## 1. Product context

The Operator Economy is a **pure media property** — channel, Monday newsletter, and a library of "Operator Blueprint" lead-magnet PDFs. Each episode is a **thesis** ("this is the kind of business you can build, and here's how hard it really is") proven with real companies as evidence.

### Surfaces this system serves
- **YouTube** — thumbnails (evidence object focal, 3–4 words, never a face), video graphics (citation lower-thirds, sheet chapter cards, blueprint end-cards).
- **Website** (`theoperatoreconomy.com`) — split hero: cream editorial + live navy schematic.
- **Newsletter** — the Monday email styled as a sourced research note, gap figure in the mast.
- **Operator Blueprints** — document-grade PDFs with engineering title blocks.
- **LinkedIn carousels** — blueprint sheets exported natively.

---

## 2. Sources (provenance)

- **Codebase (ground truth):** `operator-economy/` (mounted, read-only): `brand/brand.md`, `brand/design-system.md` (the original v1 spec), `channel/positioning.md`, `docs/content-rubric.md`, real episode copy in `studio/originate/ai-implementation-consulting/script.json`. Legacy viddy tokens in `studio/config/brand.json` are superseded.
- **GitHub:** [`github.com/manavpthaker/operator-economy`](https://github.com/manavpthaker/operator-economy) — same repo; explore it to design against real product copy.
- **Rev history:** Rev A built the v1 editorial spec (Source Serif/IBM Plex). Rev B explored AI-native directions on canvas (`explorations/`). **Rev C (this)** locks the approved merge: Working Schematic structure × Boska/Zodiak type. The full decision trail lives in `explorations/AI-Native Directions.html` and `explorations/Refined Direction.html`.

> **No visual assets existed in the sources** — no logo, no images, no font binaries. The wordmark is set in type; see §7.

---

## 3. Content fundamentals (voice & copy)

**Register:** documentary rigor + operator credibility. Practical, specific, calm — never hustle.

**Person:** the reader is **"you"**; the host is **"I"**, used sparingly and accountably ("I want to be careful here — that number comes from a blog, not audited books").

**Casing:** sentence case everywhere. UPPERCASE is reserved for labels: `SOURCE:`, `SHEET 02 OF 05`, `REV C · 2026-07-02`.

**Numbers:** always specific, always sourced or explicitly marked as estimates, always with units, always set in Fragment Mono with a citation chip. **If a number is in mono, it is published and defensible.**

**Italic ration (Rev C rule):** at most **one italic phrase per composition** — the single emphasis beat ("*actually*", "*Solo scale.*").

**Emoji:** never, on any surface.

**Never (voice kill-list):** hype words ("insane", "secret", "SHOCKING") · income promises ("$0 → $10K/mo") · "hey guys" openers · fake scarcity · wrap-up signals.

**Signature phrases:** intro "Welcome to The Operator Economy." · sign-off "Build it. Own it. Operate it." · lead magnets are "Operator Blueprint №00X".

---

## 4. Visual foundations

**Color.** One palette; any composition = Ink + Paper (or Navy) + **one** accent:
- `Ink #1A1A1A` — text, thumbnail/video ground.
- `Paper #F5F0E6` — page, print, sheets (warm cream).
- `Schematic Navy #14263E` (`--surface-schematic`) — the working panel; `Drafting Blue #1F3A5F` is the accent/linework color on paper.
- `Ledger Gold` — THE accent of the dark world: `#C4A45F` text/arrow on navy & ink (6.4:1 AA), `#B08D3E` fills, `#7A5E24` text on paper (darkened in Rev C to pass AA 5.3:1).
- `Sage #7B9E87` — **status only** (live/verified dots, RUNNING tags). Not an accent.
- `#9B3E2E` muted brick for negative deltas/violations.

**Type (two serifs, one job each).**
- **Boska 700/900** — display ≥40px ONLY (hero, covers, tagline). Below 40px its hairlines sparkle — hard floor.
- **Zodiak 700** — the 18–44px workhorse (newsletter headlines, section heads), tracked −0.02em, narrow measure. Zodiak 900 for thumbnail support lines.
- **Supreme** — body/UI (400/500; it ships no 600 — `--w-semibold` maps to 500).
- **Fragment Mono** — every number & citation; single 400 weight, tabular, slashed zero. Scale carries emphasis, never synthetic bold.

**The signature elements (the five unfakeables):**
1. **Citation chip** — `SOURCE: Sacra · Apr 2026` mono chip (≥10px) beside every figure; 2px accent left rule; gold `ESTIMATE` variant.
2. **Gold gap arrow** — `$5.9B → $2K`; origin neutral, arrow + destination gold; one per composition.
3. **Engineering title block** — №, Rev, date, sources grid on every document (1.5px frame, 1px dividers).
4. **Margin annotation rail** — revision tag + mono research notes; recomputed figures get dotted gold underline + `↻`.
5. **Working schematic** — navy panel, drafting grid (36px, `rgba(245,240,230,.055)`), wired nodes with step labels + real prices, sheet tag, sage RUNNING pulse, measurement bracket, sourced footer. **Rule: every node carries a real figure; placeholder nodes are banned.**

**Backgrounds:** flat Paper, Ink, or Navy-with-grid. No gradients, no glassmorphism, no textures. Corners 2–3px max; pills = status dots only. Shadows whisper-quiet; depth = hairlines + paper tone. Motion = fades/slides only (120/200/320ms), sage pulse for live status, all gated by `prefers-reduced-motion`.

---

## 5. Tokens

Consumers link one file: **`styles.css`** → `tokens/fonts.css` (Fontshare: Boska/Zodiak/Supreme + Google: Fragment Mono), `tokens/colors.css` (ramps + semantic aliases + schematic anatomy tokens), `tokens/typography.css` (families, roles, the 40px floor), `tokens/spacing.css`, `tokens/base.css` (resets + `.oe-mono`, `.oe-label`, `.oe-caps`, `.oe-pulse` helpers).

---

## 6. Components

React primitives on `window.TheOperatorEconomyDesignSystem_bf951d`:

**Core** (`components/core/`): **Button** (primary/secondary/ghost), **Badge**, **Card** (`sheet` top rule), **Input**.

**Brand** (`components/brand/`) — the signatures: **CitationChip**, **TitleBlock**, **Stat**, **SheetHeader**, **Annotation**, and new in Rev C: **GapFigure** (the gold arrow), **Schematic** + **SchematicNode** (the navy working panel; wires auto-inserted, node figures required).

**Data** (`components/data/`): **DataTable**, **BarChart**.

> **Intentional additions:** none exist as code in the source repo; all express the locked spec. No Toast/Tabs/Modal — the surfaces don't use them.

---

## 7. Iconography

Deliberately icon-light. The marks are typographic: `№`, the gold `→`, `×`, `↻` (recomputed), `●` status dots, measurement brackets. No icon font or SVG set exists or is bundled; emoji banned. If UI icons ever become necessary, Lucide (1.5px stroke) is the flagged substitution — confirm before adopting.

---

## 8. Index / manifest

- `styles.css` + `tokens/` — the token layer.
- `guidelines/Design System.html` — **the published system document** (foundation, tokens, contrast audit, signature anatomy, hard bans, the four reference surfaces, do/don't).
- `surfaces/` — final reference comps: `hero.html` (1280×880), `thumbnail.html` (1280×720), `masthead.html` (1280×640), `cover.html` (1280×880). All are starting points.
- `foundations/` — specimen cards (Colors / Type / Spacing / Brand groups).
- `components/` — `core/`, `brand/`, `data/` (each: `.jsx` + `.d.ts` + `.prompt.md` + card).
- `ui_kits/` — `website/`, `newsletter/`, `blueprint/` — interactive Rev-A-era screens; they consume tokens so they inherit Rev C type/color, but their layouts predate the Working Schematic. Use `surfaces/` as the canonical look.
- `explorations/` — the decision trail (turns 1–3 on canvas).
- `SKILL.md` — Claude-Code-portable skill entry.

## Hard bans (any one breaks the brand)

Instrument Serif / default-AI-startup look · neon · gradients · glassmorphism · shocked faces · income overlays · emoji · countdown/scarcity · placeholder schematic nodes · unsourced numbers · Boska <40px · synthetic-bold mono · >1 italic per frame · radii >3px · >1 accent per composition.

## Caveats & known substitutions

1. **Fonts are CDN, not vendored** (Fontshare + Google). No binaries existed in the sources; ask if offline use is needed.
2. **No logo mark** — wordmark set in Zodiak 700 (Boska at display sizes); nothing invented.
3. **UI kits are Rev-A layouts** — token-migrated but not yet rebuilt around the Working Schematic. `surfaces/` is canonical; say the word to rebuild the kits.
4. **Gold on paper** was darkened to `#7A5E24` for AA (the audit table in the system document shows the math).
