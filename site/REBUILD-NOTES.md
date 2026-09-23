# Site rebuild for the EP007 relaunch (2026-09-23)

Local only. Nothing was committed, pushed or deployed. `npm run build` passes (Next 16.3.4).

## What changed

| Area | Change |
|---|---|
| Registry | `app/lib/operations.ts` now holds one operation: `exit-readiness-prep` (Sale-Readiness Practice). №001-006 are unregistered; their source is in git history. No episode URL lives in the registry. |
| Homepage `/` | Leads with EP007: episode title, one-line business, premiere state or watch link, "Open the Operator Canvas", docket and thumbnail. Then the positioning line, tagline and AI disclosure, then email signup, then the three-decision Canvas explainer and the standard. Old hero ("You can build it now...") removed. |
| EP007 page `/businesses/exit-readiness-prep` | New `app/businesses/[slug]/SaleReadinessPage.tsx`: titleblock + docket + thumbnail, three-decision summary, five sheets (00 Opportunity, 01 System, 02 Evidence, 03 Economics, 04 Guardrails) with the guided-walkthrough toggle, episode section, gated Blueprint download, newsletter. Same anatomy as the retired №006 page and the Step 7 v0.1 proposal. |
| Blueprint PDF | `studio/originate/exit-readiness-prep/Operator-Blueprint-007.pdf` copied to `public/blueprints/exit-readiness-prep.pdf`. Requested through the existing capture flow: `BlueprintRequestForm` posts `blueprint:exit-readiness-prep` to `/api/subscribe`, which emails the PDF link. `data/episodes.json` now lists only EP007 with `pdf_ready: true`, and `api/subscribe/route.ts` sends the link when `status === 'live' \|\| pdf_ready`. The PDF file itself is still world-readable at its path (same as the precedent). |
| Thumbnail | `launch/thumbnail.jpg` resized to 1920x1080 at `public/episodes/exit-readiness-prep/thumbnail.jpg`, captioned "Everyone pictured is AI-generated." Also used as the page's OG image. |
| `/businesses` | One entry; filters and "Legacy" labels removed. |
| `/about` | Was a redirect; now a page with the positioning, tagline, AI disclosure and the no-income-promise standard. |
| `/newsletter` | Was a redirect; now a page with the form. |
| `/method` | "Why this exists" opens with the positioning; AI disclosure added under "How it is made"; "Current library" row now names the one Canvas. |
| `/privacy` | Updated for the email-gated Blueprint ("Updated September 23, 2026"). |
| Chrome | Wordmark is small spaced "THE" + Boska "Operator Economy" (brand-2026-09). Nav: Businesses, Method, About, Subscribe. Footer carries the tagline and AI disclosure. |
| Metadata | Site description and OG text use the positioning and tagline. |
| Sitemap | Home, the EP007 page, businesses, method, about, newsletter, privacy. No old slugs. |
| CSS | New `app/styles/boundary-ledger/relaunch.css` (Boundary Ledger tokens only, no new colors), imported from `globals.css`. |
| Moved, not deleted | `app/businesses/[slug]/DirectBookingPage.tsx` → `operator-economy/_to_delete/site-relaunch-2026-09-23/`. Old PDFs in `public/blueprints/` stay on disk but are redirected. |

Owner copy used verbatim from `app/lib/brand.ts`: the positioning, the tagline and the AI disclosure.

## Redirects (`next.config.mjs`, all 308 to `/`)

For each retired slug (`ai-implementation-consulting`, `voice-agent-agency`, `boring-automation-agency`,
`solo-design-agency`, `too-small-to-bother`, `direct-booking-recovery`, `small-cohort-business`):
`/episodes/<slug>`, `/businesses/<slug>`, `/blueprints/<slug>.pdf`, `/carousels/<slug>.pdf`.

`/episodes/exit-readiness-prep` (the `blueprint_url` in links.json) 308s to `/businesses/exit-readiness-prep`
via `app/episodes/[slug]/page.tsx`. Verified locally with curl.

## The one place the YouTube URL is injected

`app/lib/episode-links.ts` → `getEpisodeLinks(slug)`. At build time it reads
`../studio/originate/<slug>/launch/links.json` and returns the URL only when `episode_url` is an https
YouTube URL, `slug` matches, and `dry_run` is not `true`. Otherwise every surface shows
"Premieres Mon Oct 5, 11:00 ET" (formatted from `episode_publish_et`). `WatchAction`,
`EpisodeThumbnail` and `episodeStatus` in `app/components/WatchAction.tsx` are the only consumers.
No URL is typed anywhere in `site/`. Tested against a scratch copy: a real URL shows, a dry run or
`[PENDING_UPLOAD]` shows the premiere state.

Pages are static, so **the site must be rebuilt and redeployed after the upload writes links.json.**

## Every claim on the EP007 page, with its facts.md pointer

All in `content-os/facts.md` "EP007 research — sale readiness practice (approved 2026-09-23)".

| Claim as shown | Hedge shown with it | facts.md row |
|---|---|---|
| Roughly three in ten listed small businesses actually sell | EPI trains and certifies exit planners, has an interest; directional | Market problem, row 1 (C001) |
| Roughly half of exits are not planned (five Ds) | Not any given owner; same EPI caveat | Market problem, row 2 (C002) |
| Over half intend to exit within five years; about a quarter have had a valuation; fewer than one in ten has an estate plan | Self-reported survey; unpreparedness, not willingness to pay | Market problem, rows 3-5 (C003) |
| Almost nine in ten deals above $5M drew at least three offers; a third drew ten or more; Q2 2026 | Advisers reporting own closings, not audited | Market problem, rows 7-8 (C005) |
| Readiness work is paid at three separate scales | Adjacent, not proof of small-business demand | Job and legal line, row 1 (C006) |
| Sale-tied fee regulated in a meaningful number of states; can cost every fee earned | No state named; not legal advice | Job and legal line, row 3 (CLM-004) |
| Preparing and selling are different jobs; fixed fee | Editorial framing | Job and legal line, row 4 (C008) |
| Everyone around the sale is paid when it closes | Editorial characterisation, no firm named | Job and legal line, row 5 (C014) |
| AI drafting is "now the cheapest part of the job instead of the most expensive"; judgment stays human | Capability, not outcome | Job and legal line, row 6 (C013) |
| $12,000 × 8 = $96,000; $10,000 costs; $86,000; $120,000 target does not clear, "It is not close" | "Modeled scenario, not observed performance or an earnings forecast" in the section intro and boundary | Model table |
| $130,000 required; about 11 engagements; 85 hours; 935 hours, "essentially your entire working year"; about $16,250 at 8 | Same disclosure; 85 hours "an assumption, not a finding" | Model table |
| Nobody has measured the hours, including the host | Stated as unknown | Model, "deciding unknown" |
| Thirty-day dependency map | "a test setting, not a proven threshold" | Shorts-only parameters |
| The host has no transaction experience | Owner-approved wording | Host authority |
| Kill conditions (owners agree and defer; brokers do it free) | Unknowns, not findings | Shorts-only parameters; Canvas §11 |

Deliberately not used (facts.md "DO NOT STATE — EP007" and non-ledger Canvas figures): the
prepared-seller multiple gap (only an unnumbered "excluded on purpose" note, as in the approved
blueprint), any state or state count (the Canvas's "34 states plus DC" is omitted), the 80% net-worth
figure, the transition population, consolidator multiples, any typical fee, "never sold a business",
the Canvas's 680/900/220-hour capacity check, the $500/$6,000 cost split, the "55+" buyer age, the
"one to five years" qualifier, the "three brokers" stop line, source counts and the episode number.
Voice checks: no em dashes, no `voice.md` §2a/§2b words, no income promises.

## Screenshots

`/private/tmp/claude-501/-Users-brownmanbrain-GitHub-operator-economy/a41aa8bb-cc59-4eab-9ffd-21e9735a6ca3/scratchpad/site-review/`
(`site/_review/` is not gitignored, so they were kept out of the repo). Desktop 1440 and mobile 390
for home, the EP007 page (full page plus one shot per Canvas section) and the other pages. The site
has no dark mode, so there are light-only shots.

## Deploy steps (not executed)

1. Review, then commit on a branch (`site/`, `_to_delete/` move, this file).
2. After the YouTube upload writes a real `episode_url` into
   `studio/originate/exit-readiness-prep/launch/links.json` (with `dry_run` false), commit that file.
3. Confirm the Vercel project's Root Directory is `site/` and the build clones the whole repo
   (needed for the links.json read; if links.json is missing the build still passes and shows the premiere state).
4. Confirm env vars: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `RESEND_API_KEY`, optional
   `RESEND_FROM`, `NEXT_PUBLIC_SITE_URL`. Without them the Blueprint and newsletter forms return 503.
5. `vercel` (preview), check `/`, `/businesses/exit-readiness-prep`, the redirects and one test
   Blueprint request, then `vercel --prod`.
6. Redeploy again after any links.json change.

## Open questions

1. Episode number: no number is printed on the site (PACKAGE-NOTES Q5 is open), but the PDF and the
   Blueprint email subject still say №007.
2. Thumbnail vs Boundary Ledger: the owner asked for the thumbnail, while the design system says photography does not
   replace the Working Model on episode identity. It is shown as an episode thumbnail with an
   AI-generated caption. There is no EP007 Working Model illustration.
3. The PDF is world-readable at `/blueprints/exit-readiness-prep.pdf` (soft gate, same as before).
   A tokenized download is on the Step 7 backlog.
4. Legal review of CLM-004 (PACKAGE-NOTES Q9) is still open. The page says "not legal advice" and names no state.
5. The unused Rev C components (`LatestBlueprint`, `LibraryClient`, `CaptureForms`, `episodes/[slug]/EpisodeForms`,
   `YouTubeEmbed`) and old PDFs in `public/` remain on disk. They are unreachable, and can be removed later.
