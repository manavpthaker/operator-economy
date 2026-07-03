# Claude Code prompt — hero-right becomes "The latest blueprint" + upcoming episodes & pages (2026-07-03)

Paste below the rule into Claude Code from the repo root.

---

**Mission.** Two connected changes on theoperatoreconomy.com: (1) replace the hero-right stack schematic with a data-driven "latest blueprint" document card; (2) under it, an **upcoming episodes list** with pipeline stages, where each upcoming episode links to its **own page** describing the thesis with a notify-me signup. The current hero panel (№001 stack with prices, `site/app/page.tsx`, the `<aside className={s.heroPanel}>` block) duplicates the "How every episode works" band directly below it. The new panel shows the *deliverable* — the newest Operator Blueprint on a growing stack — and updates itself every time an episode ships. Design decision record: hero-right answers "what do I get, how often, and what's coming," not "what is №001."

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
      "status": "upcoming",
      "stage": "research",
      "thesis": "One-paragraph thesis: the buildable business, stated plainly — who pays, what it replaces, why one person can run it. No figures until sourced.",
      "expected": "2026-07"
    }
  ]
}
```

Rules: `status` ∈ `live | upcoming | queued`. `stage` (upcoming only) ∈ `research | scripting | production` — mirrors the actual pipeline (research brief → script/Gate 1 → VO/render). Figures appear ONLY on `live` entries (the site already promises "figures publish with the episode"); `thesis` is prose, no numbers unless already sourced. `expected` is a month, never a date — no countdown-timer energy (disclosures ban scarcity). Seed from the live site today (№001 live; №002 voice-agent agency + №003 boring-automation agency upcoming/research; 18 queued) and pull theses from `topics/queue.md`.

## 2. Hero component — `site/app/components/LatestBlueprint.tsx`

Replaces the `<aside className={s.heroPanel}>` contents. Anatomy (navy panel, drafting grid, Rev C tokens):

- **Header row:** mono label `THE LATEST BLUEPRINT` (gold) · right: sage pulse dot + `ships every Monday`.
- **The document:** paper (#F5F0E6) card, 2px radius, engineering title block: top rule row `OPERATOR BLUEPRINT №00X` / `REV X · LIVE` (gold `LIVE`), title in Zodiak 700, then a mono spec table (1px `ruleStrong` row dividers): `SOURCES → {sources_verified} verified` · `STACK → {stack_cost}` · `HONEST MATH → {honest_math}` + ` · est.` when flagged · `PLAYBOOK → {playbook_span}`. Footer row: `PDF · every citation` + navy button `Get №00X →` (links `pdf_href`).
- **The stack behind it:** N−1 ghosted paperSunken sheets offset 5px/10px diagonally behind the top document (cap visible ghosts at 4), where N = count of `live` episodes. At N=1 render one subtle ghost so the stack metaphor reads from day one.
- **Upcoming list (replaces the one-line ticker):** under the document, a compact mono list of `upcoming` entries (max 3), each row a LINK to `/episodes/{slug}`: `№002 The voice-agent agency` · stage chip on the right (`● research` sage-dim / `● scripting` / `● production` gold-dim). Rows separated by faint hairlines, whole row clickable with a subtle `→` on hover. Below the rows, faint: `{queue_depth} more in the research queue`.
- Component reads `site/data/episodes.json`; latest = highest `number` with `status: "live"`. No props hard-coding. Keep the panel's existing responsive/mobile behavior (stacks below copy at 390px).

Also: the hero's `liveChip` ("Episode №001 live · …") should read from the same data. Keep the "Watch the latest breakdown ↗" CTA pointing at `episode_href` of the latest live entry.

**Do not** delete the stack-schematic markup wholesale — move it into the "How every episode works" band region only if it's not already represented there; otherwise delete. (The band already shows the format schematic; the №001 stack with prices lives in the episode/library layer, where it belongs.)

## 3. Episode pages — `site/app/episodes/[slug]/page.tsx`

One dynamic route serving every episode from `episodes.json` (generateStaticParams over all non-`queued` entries). Two states:

**Upcoming state** (`status: "upcoming"`) — the notify page:
- Masthead consistent with home (nav back to `/`).
- Header: `№00X · {category}` label + stage chip, Boska/Zodiak title, `expected {month}` in mono.
- **The thesis** — the `thesis` paragraph as an editorial block (this is the page's substance; sentence case, no hype, ≤1 italic).
- **What ships with it** — a static three-item mono list: the episode, the Operator Blueprint (PDF, free), the Monday note. This is expectation-setting boilerplate, same on every upcoming page.
- **Pipeline position** — a small horizontal schematic: research → script → production → live, current stage marked with the sage pulse. This is the working-schematic motif doing honest status duty; no dates, no countdowns.
- **Notify form** — one email field + button `Notify me when №00X is live`. Reuse the existing capture form styles (`CaptureForms.tsx`); all forms converge on the shared capture contract from §5 with tag = `notify:{slug}` (blueprint form `blueprint:{slug}`, ledger `newsletter`).
- Fine print: "One email when it ships. You're also on the Monday note unless you opt out." — honest about what signup means.

**Live state** (`status: "live"`) — same route, richer page: title block header (rev, date, sources), embedded/linked episode (YouTube), blueprint capture (reuse `BlueprintForm` fed by data), honest-math row. Keep this minimal for now — the library section anchors already point at `#capture`; retarget the №001 library card to `/episodes/ai-implementation-consulting` once this page exists.

Library cards for upcoming episodes (№002/№003) also become links to their pages, replacing the dead "Figures publish with the episode" text-only cards.

## 4. Pipeline emit — keep it current automatically

In `studio/scripts/originate/derive_content.py` (the derive step that already writes `content/{blueprint,newsletter,linkedin_posts}.md`), add an `update_episodes_json()` step: upsert this episode's entry in `site/data/episodes.json` (number, slug, title, thesis from the script's thesis section, figures from economics, sources count from the claim registry). `stage` advances automatically with the pipeline: `originate.py new` → `research`, Gate 1 approval → `scripting`, `continue` → `production`, and `python scripts/originate/publish.py <slug>` flips `status: live` + sets `date`. Never invent figures: pull from `script.json`/`render_data`, omit any field not present (components must tolerate missing optional fields).

## 5. Interactivity pass — nothing on the page may be dead

Decision (locked): capture backend is a **custom API + Resend**; watch links point at the **channel URL until №001 publishes** (then `youtube_url` in episodes.json takes over — no code change).

**5a. Capture backend.**
- `site/app/api/subscribe/route.ts` (POST `{email, tag}`): validate email, honeypot field + basic rate limit, store subscriber, fire Resend transactional. Storage: Vercel Postgres (`subscribers`: id, email, tag, slug, created_at, unsubscribed_at, unsubscribe_token) — the site deploys on Vercel. Env: `DATABASE_URL`, `RESEND_API_KEY`, `RESEND_FROM`. The Resend key + from-address are already in `site/.env.local` (gitignored — NEVER commit or echo the key; read it only via `process.env`). Remaining operator setup: verify the sending domain in Resend, add the same env vars to the Vercel project, and provision Vercel Postgres for `DATABASE_URL`.
- Transactional sends by tag: `blueprint:{slug}` → welcome email with the Blueprint PDF link (PDF hosted at `site/public/blueprints/{slug}.pdf`; if absent, email says it ships with the episode — never a broken link); `newsletter` → Monday-note welcome; `notify:{slug}` → confirmation ("one email when №00X ships"). All emails: plain, sourced-research-note tone, one-click unsubscribe link (`/api/unsubscribe?token=`) — the disclosures promise no drip, so there is NO sequence, only the welcome + the weekly note.
- `site/app/lib/capture.ts`: shared client helper all three forms call. States: idle → submitting (button shows `…`) → success (inline mono confirmation, e.g. `Filed. Check your inbox.`) → error (honest message, retry). No toasts, no modals — inline, in character.
- Publish hook: `publish.py <slug>` gains `--notify` which sends the "№00X is live" email to `notify:{slug}` subscribers via Resend (CLI confirmation with count before sending).

**5b. Kill every dead control.**
- Nav `Subscribe` is currently a `<span>` — make it a real link to `#capture` (smooth scroll, `scroll-margin-top` on targets).
- Library filters (All / Services / Software / Media) are static text — make them functional client-side filters over episodes.json categories, with counts; tabs with zero entries render disabled-muted, not clickable-dead.
- `Watch the episode ↗` / `Watch the latest breakdown ↗` → `youtube_url ?? channel URL` (https://www.youtube.com/@TheOperatorEconomy), target _blank. Never `#capture`.
- `Blueprint №001 (PDF)` → scrolls to capture AND pre-tags the blueprint form for that slug (the form's hidden tag updates); label stays honest: the PDF arrives by email.
- Citation/source chips (`SOURCE Accenture FY2025 · CIO Dive`, `REPORTED Medium · Mar 2026`) become links to the actual sources where URLs exist in the research brief (`research/` / claim registry), target _blank, dotted underline on hover. This is the single most on-brand interaction available: every number on the site becomes checkable.
- Footer/annotation "fig. 01 recomputed ↻ 2d ago" and "V1 · date" derive from `episodes.json.updated` — computed relative time, never hard-coded.
- Sage `● Running` pulses stay (they're design-system status idiom) but must sit only on things that ARE running: the pipeline (hero panel, ships-every-Monday) and stage chips — remove from anything static.

**5c. Alive-by-default touches (cheap, in-character):**
- Hero document stack: reveals with a settle animation on load (respect `prefers-reduced-motion`); hover lifts the top sheet 2px.
- Upcoming rows + library cards: hover reveals the `→`, border-strong on hover, whole row/card clickable.
- Schematic nodes in the format band: node figures tick in on scroll-into-view (IntersectionObserver, once).
- Inputs: visible focus ring per the design tokens; forms submittable by Enter.

## 6. Verify

- `cd site && npm run build` passes; hero renders from JSON (temporarily add a fake №002 live entry, confirm the card swaps, ghost count increments, ticker advances — then remove it).
- Mobile 390px: document card full-width below copy, ghosts still visible but reduced offset.
- Rev C compliance: one accent (gold) in the panel; sage only on the pulse dot; radii ≤3px on the document (12px panel container may keep the site's existing card radius); Fragment Mono for every number; no gradients.
- Lighthouse/a11y: the document is a `<figure>` with an aria-label describing the latest blueprint; button has accessible name.

Commit in two parts: (1) data contract + component swap, (2) pipeline emit + publish CLI.
