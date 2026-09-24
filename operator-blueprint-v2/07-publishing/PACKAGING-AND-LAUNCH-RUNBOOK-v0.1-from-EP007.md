# Step 7 runbook v0.1: packaging, channel, site and YouTube launch

Status: **proposed, derived from EP007 / public №001 (2026-09-23).** Not authoritative until owner
approval. `content-os/flow.md` still owns release gating; this runbook covers the creative and
operational work that feeds it. Decision records: `blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decisions/`.

## 1. Copy package (owner reviews every file)

Draft in `studio/originate/<slug>/content/`: `youtube-longform.md` (titles, thumbnail concepts,
description, chapters, tags, pinned comment, disclosure), `youtube-shorts.md`, `newsletter.md`,
`linkedin_posts.md`, `PACKAGE-NOTES.md` (claim map + open questions). Sources: locked narration,
editorial lock, claims map, the locked Operator Canvas, `content-os/facts.md`.
- Add the episode section to `content-os/facts.md` (claims, hedges, do-not-state list). The gate
  scrapes every number in facts.md regardless of any banner, so review it before anything is
  marked ready. EP007 section approved 2026-09-23.
- Resolve host-authority facts with the owner before packaging (EP007: the "never sold a business"
  line conflicted with the Subziwalla exit → cut from the episode).
- Disclosure: say exactly what is synthetic (EP007: voice clone of the host; host avatar and every
  other person AI-generated). `containsSyntheticMedia: true` on every upload.
- The deliverable is the **Operator Canvas**, rendered from the locked Canvas — never a derived
  "blueprint" worksheet. "Legacy Blueprint" is only for V1 artifacts.

## 2. Title and thumbnail (owner rules, EP007)

Rules the owner set (memory: `thumbnail-and-title-approach`):
1. The thumbnail shows the episode's **own cold-open cast and set**, so the first seconds pay off
   the click. Generate from real episode frames as references (Higgsfield `gpt_image_2_5`,
   ~0.25–0.5 credits per image at medium).
2. The presenter (the episode's locked look, `presenter/LOOK-LOCK.json`) is in frame for authenticity, as a **smaller guide
   (~⅓ frame), serious, not smiley**, pointing at the story behind.
3. Text = the **episode-specific action the viewer learns** (EP007: `HELP HER SELL`), never a line
   that would fit any episode. Keep claims boundaries (help her sell ≠ sell her business).
4. Title promises the how-to, not the problem (EP007: "The One-Person Business That Gets
   Companies Ready for a Sale"). Thumbnail carries the verb, title names the business.

Process: study the EP006 reference (`studio/output/direct-booking-recovery-thumbnail-rev-d.png`) and
live comps (YouTube search via page `ytInitialData`, download `i.ytimg.com/vi/<id>/hqdefault.jpg`);
generate 3 options per round; show them **inside a mock YouTube feed** (desktop, phone, sidebar)
next to the comps before asking for a pick; upscale the chosen image (don't regenerate); crop to
3840×2160; save `launch/thumbnail.png` + a < 2 MB `thumbnail.jpg`; shrink-test at 168/320 px on
white and #0f0f0f; write `launch/thumbnail-note.md`. EP007 took 5 rounds, ~9 credits.

## 3. Channel and brand (one-time for a relaunch; re-check each launch)

- Boundary Ledger identity: small spaced "THE" + Boska "Operator Economy", paper on deep mineral,
  oxide rule. Assets: `channel/brand-2026-09/` (YouTube banner 2560×1440 with text in the
  1546×423 safe area, avatar 800², LinkedIn cover 4512×764, logo 400²). Render HTML → PNG with
  headless Chrome; preview desktop + phone before applying.
- YouTube via Data API (`studio/.secrets/token.json`, scopes incl. youtube.force-ssl):
  `channelBanners.insert` then `channels.update` with the full `brandingSettings.channel` object
  (description, keywords) + banner URL. **Avatar cannot be set by API**; set it in Studio from the
  Google account that owns the channel (it is not the account signed in to the operator's Chrome).
- Relaunch reset (EP007): all old videos set **private** (never deleted); before-state and per-video
  log in `channel/youtube-reset-2026-09-23/`.
- Public numbering restarted: internal EP007 = public №001 (memory: `public-episode-numbering`).

## 4. Site (theoperatoreconomy.com, `site/`, Next.js on Vercel)

- Homepage: **positioning leads** ("Build, own and operate a business of one using AI.") with a
  newest-episode CTA card, then the episode section, signup, Canvas explainer, the standard.
- Episode page: the Operator Canvas (three decisions + sheets) built only from the locked Canvas
  and facts.md; economics labelled modeled; scope boundary visible.
- The Canvas PDF is delivered by email via `/api/subscribe` (Resend); number from `site/data/episodes.json`.
- The YouTube URL enters the site from **one place**: `site/app/lib/episode-links.ts` reads
  `studio/originate/<slug>/launch/links.json` at build time → rebuild and deploy **after** upload.
- Old episodes removed from registry; old URLs redirect home (`site/next.config.mjs`).
- Verify: `npm run build`, dev server (`.claude/launch.json` → `oe-site`, port 3217), desktop and
  375 px in the browser pane (headless Chrome can't render below ~500 px). Notes: `site/REBUILD-NOTES.md`.

## 5. YouTube launch (API)

- Pre-flight: `python launch.py <slug> --monday <YYYY-MM-DD> --title "…" --video <master>` (dry run).
  It rubric-gates LinkedIn copy, needs `content/youtube_description.txt`, `content/shorts_briefs.json`,
  `shorts/short-0N.mp4` (symlinks to accepted renders, hashes checked vs the Shorts manifest) and
  the Canvas PDF. Plan: `studio/originate/<slug>/launch/UPLOAD-PLAN.md`.
- **Quota: 10,000 units/day; each upload 1,600.** Episode + 4 Shorts ≈ 8,000 + thumbnails (50 each)
  + captions (400) → do uploads on a fresh quota day, nothing else.
- `--go` uploads private + `publishAt` (episode Mon 11:00 ET, Shorts Tue–Fri 08:30 ET), bakes the
  episode link into Short descriptions, writes `launch/links.json`. Then: `thumbnails.set`,
  `captions.insert` (SRT), playlists. Manual in Studio: pin comments, end screen, confirm the
  altered-content setting.
- Then rebuild + deploy the site (watch link now live), then schedule LinkedIn (Step 8).

## 6. Records to keep per release

Owner source JSON for every direction (verbatim), a decision/feedback/verification event in the
episode log (`agents/deliverables/ep007-decision-log-helper/decision_log.py append`), manifests with
hashes, and a `RELEASE-RECORD.md` in the episode folder (EP007:
`operator-blueprint-v2/episodes/EP007-exit-readiness-prep/RELEASE-RECORD.md`).
