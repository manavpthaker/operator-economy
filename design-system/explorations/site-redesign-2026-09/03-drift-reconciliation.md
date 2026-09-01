# Drift reconciliation — LP mockup → Rev C tokens

The committed LP mockup (`design-system/explorations/rev-d/operator-canvas-lp-mockup.html`,
`24c4a024`) is harvested for structure and copy. Its self-declared `:root` is discarded
wholesale; every artboard in this effort consumes the real token layer
(`design-system/styles.css` or verbatim-inlined `design-system/tokens/*.css`) and may use
only `var(--*)` references, `.oe-*` base helpers, and the `--type-*` role shorthands.

## Value mappings (mockup → token)

| Mockup value | Token replacement | Note |
|---|---|---|
| `--blue: #315f92` | `--drafting-blue: #1F3A5F` (text/accents on paper) or `--blue-500: #35608C` (hover/lighter accent) | Pick by role, not by nearest hex |
| `--gold-deep: #765921` | `--gold-700: #7A5E24` | The AA-tuned gold text on paper (5.3:1) |
| `--gold: #c4a45f` | `--gold-bright: #C4A45F` on navy/ink; `--gold-500: #B08D3E` for fills | Same hex, correct alias + surface rule |
| `--navy: #14263e` / `--navy-deep: #0d1a2c` | `--surface-schematic: #14263E` (aliases `--blue-900`) for both | No darker navy token exists; the mockup's #0d1a2c surfaces flatten onto `--blue-900` rather than adding a token |
| SF Mono | Fragment Mono 400 | Mono means published; single weight, no synthetic bold |
| `--shadow: 0 24px 60px rgba(13,26,44,.12)` | `--shadow-md` / `--shadow-lg` | Token shadows whisper; the 60px shadow is banned |
| `--content: min(1380px, 100vw - 56px)` | `--container-wide: 1320px` + `--margin-page` | |
| Hand-written on-ink opacities `rgba(245,240,230,…)` | `--text-on-ink-muted` (0.62) / `--text-on-ink-faint` (0.40) / `--border-ink` (0.16) | Also fixes the same drift in `site/app/page.module.css` when implemented |
| `vendor-published + modeled` chip labels | The four canonical classes: `OBSERVED / PARALLEL / MODELED / UNKNOWN` | Per-claim; distinct from Model status |
| Footer line "Human consequence. Operating clarity." | removed | Rev D internal working-direction line, not a tagline |

## Typography (owner decision 2026-09-01)

Site artboards use **Zodiak 700** (display + headings), **Supreme 400/500** (body/UI),
**Fragment Mono 400** (numbers, evidence, metadata). **No Boska on site artboards** —
Boska remains for PDF covers (B9) and brand surfaces. No Zodiak 900 or Supreme 700 on
site surfaces (an owner style rule: the DS token layer does load those weights, but the
site's self-hosted font set omits them and this decision keeps it that way).

Where the mockup used its display face at hero scale, artboards use a **site-scoped
display role** rather than reusing the Boska-bound shorthands: define
`--type-site-display: var(--w-bold) 44px/var(--leading-tight) var(--font-heading)` with
`--tracking-heading` (Zodiak's documented ceiling is 44px; the token `--type-display` /
`--type-h1` roles remain Boska-bound and unused on site artboards). This range override
is recorded here deliberately.

## Composition rules re-imposed during the port

- One accent + one gold arrow + max one italic **per sheet** (one section = one
  composition; defined this way so a long Canvas scroll can comply mechanically).
- Sentence case everywhere; UPPERCASE reserved for mono labels (`SOURCE:`, `SHEET 02 OF 05`,
  `REV A · 2026-09-01`, evidence-class chips).
- Radii ≤ 3px; `--radius-pill` for status dots only.
- Motion: `--dur-fast/normal/slow` fades and slides only, gated by
  `prefers-reduced-motion`. Decorative arrow drawing and pulsing are deferred until
  comprehension testing passes (product contract §3).
- Language on rendered surfaces: no em dashes (voice.md §3; comma, colon, mid-dot, or
  rewrite), contractions always, and at most one two-beat antithetical construction per
  viewport (§2e mirror-shell guard).

## Non-regression behaviors (the mockup already does these; the new prototype must too)

1. Keyboard-operable tabs and toggles (roving focus, arrow keys where tabs).
2. URL history: guided steps and sheet anchors update the hash; back/forward restore state;
   deep links land on the right sheet/step.
3. `prefers-reduced-motion` disables all transitions.
4. Mobile overflow: wide tables and equation blocks scroll inside their own containers;
   the page body never scrolls horizontally at 320/375px.
5. Escape closes the mobile nav panel; `aria-expanded` reflects state; touch targets ≥ 44px.
6. Source disclosures operable by click/tap/focus — never hover-only.
