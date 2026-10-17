# Owner decision 2026-10-17: the scout and the research bench may use Exa

Status: approved owner decision. Recorded 2026-10-17 from the owner's instruction in chat.

Decided by: Manav Thaker (owner)

Owner's words: "we should also run the OE candidate scout and research bench through exa" and
"Yes: write the owner decision and add Exa to both OE prompts with $0.40 (scout) and $0.20 (bench)
per-run caps."

Scope: `automation/prompts/oe-candidate-scout.md` and `automation/prompts/oe-weekly-research.md`.
This decision does **not** edit any locked Step 0.2 file or the Step 0.3 amendment, and does not
change hard gates, scoring, evidence standards, the calibration zone, or owner promotion.

## Why

The 2026-10-13 discovery reset found that searches surfaced sellers and rarely buyers, because
vendor pages are easy to find and buyer conversation is blocked (Reddit refused everywhere since
2026-09-21; Quora and Upwork return 403). Exa, through brownbot's scout (Content OS decision D-262,
`../content-os/outreach/research-sources.md`), searches by meaning, can exclude vendor domains, can
be scoped to forums and Reddit, and returns full page text for pages the browser and WebFetch
refuse. Content OS routines have used it since 2026-10-16, and both workflows were already
routed through the scout first (commit b34cbb2d); this decision sets the budget and makes Exa the
one allowed spend.

## Decision

1. **The scout may use Exa** to gather buyer-side observations: `exa` (with `--text`, and
   `--domains` or `--exclude` to steer toward forums, review sites, Reddit and job boards and away
   from vendors) and `contents` to read pages in full. At most **$0.40 a run**.
2. **The research bench may use Exa only to check and read**: `contents` for claim sources and
   recency, and `exa --category news --since <date>` or `company` for recent changes to a
   shortlisted lead. No broad topic discovery, as before. At most **$0.20 a run**.
3. Both jobs pass `--routine oe-candidate-scout` or `--routine oe-research-bench` on every Exa
   command, so spend is logged by job against the shared monthly cap ($20, shared with Content OS
   routines). Run `$BB scout -- status` first. If the month's total is **$15 or more**, use no Exa
   that run. Stop Exa when the run's cap is reached or a call is refused, and continue with the
   free tools.
4. This is the only spending either job may do. Every other "never spend money" and "never spend
   credits" rule stands.
5. **Evidence rules do not change.** Exa finds and reads pages; it is not a source. Cite the page
   it returned (URL, publisher, date), never "Exa" itself. An Exa search result with a snippet only
   counts as a search summary; text returned in full counts as a page read. Seller pages found
   through Exa are still not buyer-side observations.
6. Each run record lists the Exa commands run, how many usable observations or checks each gave,
   and the run's Exa spend, so later runs rotate queries and the owner can judge the value.

## Revisit

2026-10-30, with Content OS D-262's review of Exa spend by routine: whether Exa observations
reached the shortlist, and whether the caps should move.
