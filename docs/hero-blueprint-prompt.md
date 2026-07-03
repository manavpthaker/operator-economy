# Claude Code prompt — hero-right becomes "The latest blueprint" (2026-07-03)

Paste below the rule into Claude Code from the repo root.

---

**Mission.** Replace the hero-right stack schematic on theoperatoreconomy.com with a data-driven "latest blueprint" document card. The current panel (№001 stack with prices, `site/app/page.tsx`, the `<aside className={s.heroPanel}>` block) duplicates the "How every episode works" band directly below it. The new panel shows the *deliverable* — the newest Operator Blueprint as a document on top of a growing stack — and updates itself every time an episode ships. Design decision record: this hero-right slot answers "what do I get and how often," not "what is №001."

Read first: `CLAUDE.md`, `design-system/README.md` (Rev C rules — the panel stays navy with the drafting grid; title block anatomy in §4), `site/app/page.tsx` + `page.module.css`, and `studio/scripts/originate/derive_content.py` (you'll add the emit step).

## 1. Data contract — `site/data/episodes.json`

Single source of truth the site reads at build time:

```json
{
  "updated": "2026-07-03",
  "queue_depth": 18,
  "episodes": [
    {
      "number": 1,
      "slug": "ai-implementation-consulting",
      "title": "AI implementation as a service",
      "category": "Services",
      "status": "live",
      "rev": "A",
      "date": "2026-07",
      "sources_verified": 8,
      "stack_cost": "< $100/mo",
      "honest_math": "$2–8K/mo yr 1",
      "honest_math_estimate": true,
      "playbook_span": "weeks 1–4",
      "read_minutes": 9,
      "pdf_href": "#capture",
      "episode_href": "#library"
    },
    {
      "number": 2,
      "slug": "voice-agent-agency",
      "title": "The voice-agent agency",
      "category": "Services",
      "status": "in_research"
    }
  ]
}
```

Rules: `status` ∈ `live | in_research | queued`. Figures appear ONLY on `live` entries (the site already promises "figures publish with the episode"). Seed the file from what's on the live site today (№001 live, №002 voice-agent agency + №003 boring-automation agency in research, 18 queued).

## 2. Hero component — `site/app/components/LatestBlueprint.tsx`

Replaces the `<aside className={s.heroPanel}>` contents. Anatomy (navy panel, drafting grid, Rev C tokens):

- **Header row:** mono label `THE LATEST BLUEPRINT` (gold) · right: sage pulse dot + `ships every Monday`.
- **The document:** paper (#F5F0E6) card, 2px radius, engineering title block: top rule row `OPERATOR BLUEPRINT №00X` / `REV X · LIVE` (gold `LIVE`), title in Zodiak 700, then a mono spec table (1px `ruleStrong` row dividers): `SOURCES → {sources_verified} verified` · `STACK → {stack_cost}` · `HONEST MATH → {honest_math}` + ` · est.` when flagged · `PLAYBOOK → {playbook_span}`. Footer row: `PDF · every citation` + navy button `Get №00X →` (links `pdf_href`).
- **The stack behind it:** N−1 ghosted paperSunken sheets offset 5px/10px diagonally behind the top document (cap visible ghosts at 4), where N = count of `live` episodes. At N=1 render one subtle ghost so the stack metaphor reads from day one.
- **Footer ticker:** left `№00{next.number} {next.title} · in research` (first `in_research` entry) · right `{queue_depth} queued` (faint).
- Component reads `site/data/episodes.json`; latest = highest `number` with `status: "live"`. No props hard-coding. Keep the panel's existing responsive/mobile behavior (stacks below copy at 390px).

Also: the hero's `liveChip` ("Episode №001 live · …") should read from the same data. Keep the "Watch the latest breakdown ↗" CTA pointing at `episode_href` of the latest live entry.

**Do not** delete the stack-schematic markup wholesale — move it into the "How every episode works" band region only if it's not already represented there; otherwise delete. (The band already shows the format schematic; the №001 stack with prices lives in the episode/library layer, where it belongs.)

## 3. Pipeline emit — keep it current automatically

In `studio/scripts/originate/derive_content.py` (the derive step that already writes `content/{blueprint,newsletter,linkedin_posts}.md`), add an `update_episodes_json()` step: upsert this episode's entry in `site/data/episodes.json` (number, slug, title, figures from the script's economics section, sources count from the claim registry, status stays `in_research` until the operator flips it to `live` at publish — add a tiny CLI for that: `python scripts/originate/publish.py <slug>` sets `status: live` + `date`). Never invent figures: pull from `script.json`/`render_data`, and omit any field not present (the component must tolerate missing optional fields).

## 4. Verify

- `cd site && npm run build` passes; hero renders from JSON (temporarily add a fake №002 live entry, confirm the card swaps, ghost count increments, ticker advances — then remove it).
- Mobile 390px: document card full-width below copy, ghosts still visible but reduced offset.
- Rev C compliance: one accent (gold) in the panel; sage only on the pulse dot; radii ≤3px on the document (12px panel container may keep the site's existing card radius); Fragment Mono for every number; no gradients.
- Lighthouse/a11y: the document is a `<figure>` with an aria-label describing the latest blueprint; button has accessible name.

Commit in two parts: (1) data contract + component swap, (2) pipeline emit + publish CLI.
