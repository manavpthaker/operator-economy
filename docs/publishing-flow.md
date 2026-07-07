# The Publishing Flow

**Codified from EP001's launch (July 6, 2026).** This is the operating manual for shipping an episode. The engine model, per `research/synthesis.md` finding #8: **YouTube is the engine, LinkedIn is the ignition, email is the destination.** LinkedIn matters most for the first 1,000 subs; the compounding loop is LI seeds early watch time → YouTube suggested takes over → views mint email subs → newsletter drives hour-one watch time on the next video.

---

## Phase 0 — Production (Claude runs it; the chain from script to renders)

All from `studio/`, in order. Each stage is idempotent; caches make re-runs cheap.

```
python scripts/originate/generate_vo.py originate/<slug>/script.json     # performance pass → TTS (v2 stitched) → master
python scripts/originate/layout_vo.py originate/<slug>/script.json      # bridge splice (verifies before caching)
python scripts/originate/generate_vo.py originate/<slug>/script.json    # reassemble words/timeline
python originate/<slug>/hand_tune_storyboard.py                         # phrase-anchored screens
python scripts/originate/pace_storyboard.py originate/<slug>/script.json
python scripts/originate/prepare_longform.py originate/<slug>/script.json
python scripts/originate/arrange_bed.py originate/<slug>/script.json --stage cut
python scripts/originate/arrange_bed.py originate/<slug>/script.json --stage mix
python scripts/originate/derive_content.py originate/<slug>/script.json # LI posts, newsletter, blueprint, shorts briefs
python scripts/originate/prepare_shorts.py originate/<slug>/script.json # vertical shorts audio + props
python scripts/originate/render_blueprint.py originate/<slug>/script.json --hero '$X → $Y' --hero-caption '...'  # THE lead magnet
```

**The designed blueprint PDF is what email signups receive** — `render_blueprint.py` turns `content/blueprint.md` into the Working-Schematic PDF (Rev C tokens, matches the №001 Claude-Design reference): cover with stack rail + meta block, evidence table with confidence chips, playbook, honest math, numbered sources. Outputs `originate/<slug>/Operator-Blueprint-<NNN>.pdf` + `site/public/blueprints/<slug>.pdf`. Renders via local Chrome headless (or WeasyPrint). `launch.py` refuses `--go` if it's missing.

Render locally (Manav's machine — Remotion only):

```
cd studio/remotion
npx remotion render src/index.ts Blueprint out/ep00N.mp4 --props=../originate/<slug>/render_data/blueprint.json
npx remotion render src/index.ts Short out/short-0K.mp4 --props=../originate/<slug>/render_data/short-0K.json   # ×4
```

Review in **VLC, never QuickTime** (QuickTime drifts + pitches down long AAC files — verified EP001).

## Phase 1 — Schedule (Sunday night / Monday early)

Everything targets **Monday 11:00 AM ET** for the episode ("ships every Monday" is on the site), **8:30 AM ET** for daily posts.

**The chain is dependency-ordered — YouTube always schedules first because every downstream surface needs the links:**

1. **Schedule YT episode** (Mon 11:00) → capture episode URL.
2. **Schedule YT Shorts ×4** (Tue–Fri 8:30, staggered) → capture 4 short URLs.
3. **Links in hand → build + rubric-gate the carousel**, then **schedule OE page episode post** (Mon 11:00, carousel as the media, YT link held for the sources comment).
4. **Schedule OE page shorts posts ×4** (Tue–Fri 8:30, native vertical video + standalone insight text).
5. Everything after this point (personal repost, group, DMs) triggers off the OE page post going LIVE — see Phases 2–3.

| What | Where | When | How |
|---|---|---|---|
| Episode | YouTube | Mon 11:00 AM | `upload_youtube.py <file> --title ... --description-file ... --privacy private --publish-at <UTC>` — AI-disclosure flag auto-set |
| SRT captions | YouTube Studio | with upload | Generated from alignment (`ep00N.srt`); drag into Subtitles (API lacks force-ssl scope) |
| Thumbnail | API (`thumbnails/set`) | with upload | `Thumbnail` Remotion composition (1280×720) gated by **`docs/thumbnail-rubric.md`** — the install-moment concept (this week's business, viewer as hero, expressive faces), ≤3 elements, ≤4 words in Supreme 800, no channel branding, text bottom-left, shrink test at 168px is the ship gate. Concept locks at script gate. Two candidates/episode; Test & Compare when eligible; day-7 CTR by traffic source |
| End screen | YouTube Studio | with upload | Last 6s (outro card) designed for overlays: Subscribe + "Best for viewer" video |
| Shorts ×4 | YouTube | Tue–Fri 8:30 AM | Same script, `--publish-at` staggered; description carries episode + blueprint links |
| Episode post | LinkedIn **OE page** | Mon 11:00 AM | Hour-one package, see Phase 2 |
| Shorts posts ×4 | LinkedIn **OE page** | Tue–Fri 8:30 AM | Native vertical video + standalone insight text |
| Newsletter | Resend | Mon ~11:15 AM | From `content/newsletter.md`; drives hour-one watch time |
| Site | theoperatoreconomy.com | Mon | `episodes.json` gets `youtube_url`, status live; git push deploys |

**Identity rule: all OE content posts from The Operator Economy page.** Personal profile's role is defined in Phase 3.

**Rubric gate: every post, carousel copy, group prompt, and DM passes `docs/post-rubric.md` (hooks, watermark ban, register-by-surface, 7-point sniff test) BEFORE it's scheduled.** No exceptions — the register is the moat.

**LinkedIn scheduler gotchas (learned the hard way):**
- Media dropped straight onto the composer gets **discarded by any schedule-dialog round trip**. Order that works: set text → set schedule → attach video LAST → Schedule immediately. (Or commit media through the editor's preview + Next.)
- The time field only commits via dropdown-select or blur; typed values silently don't count.
- Can't schedule <10 min out; can't open a new composer while a video upload is processing.
- Comments can't be scheduled — the sources comment is posted manually right after the post goes live.

## Phase 2 — Hour One (the ignition; ⚠ EP001 SKIPPED THE CAROUSEL)

Per synthesis finding #8, the first hour concentrates the early watch-time signal that triggers suggested-feed distribution. Three simultaneous surfaces:

1. **Native document/carousel on the OE page** — the episode's core framework as a 8–12 page PDF carousel (top LinkedIn format, ~7% engagement). Content: the thesis → the gap chart → the stack → the honest math → last page = blueprint CTA. **YT link in the comments only** (external links in the post body = 50–70% reach penalty).
2. **Sources comment** under the post: episode link, blueprint link, key sources with confidence flags.
3. **Newsletter send** — subscribers are the highest-intent hour-one watchers.
4. **Personal repost of the OE carousel post** — repost WITH a one-line analyst comment (a real observation about the finding, rubric-gated), never a bare repost (bare reposts get near-zero reach) and never commentary about the channel. The repost is transparent by design: the OE page shows as author, so there's no origin story to perform. Counts toward the 3/week personal cap.

> **EP001 gap:** we shipped a text post, no carousel, and the newsletter didn't go. The carousel is the single highest-leverage missing piece. → automation backlog below.

## Phase 3 — The personal-profile play (1K followers + DM relationships)

The register rule from `research/comp-synthesis.md`: the audience (35–55 ops/product leaders) detects and punishes undisclosed self-promotion. **Never repeatedly "share" OE as something stumbled upon** — that middle path is the FakeGuru exposure pattern. Two sanctioned framings:

- **Surface model (Manav's call, July 6, 2026 — supersedes analyst posts):** the personal profile carries OE ONLY as **reposts of OE page posts** — no original OE-derived text posts on personal, ever. Reposts are bare or one-line, never commentary about the channel, and are transparent by design (the OE page shows as author, no origin story to perform). Cadence: 1–2 reposts/week, the episode carousel post being the default. Reposts don't collide with Grapevines personal slots (different distribution class), but still max one repost/day.
- **Original OE analyst posts on personal: retired** along with publisher framing. Grapevines owns the personal feed's original slots. If someone asks about OE directly, don't lie — deflect or answer privately.

**The DM pipeline** (the warm-relationship asset — this is what 1K followers + real relationships buy):
- **Tier 1 — direct relevance (5–10 people/episode):** people actively facing the episode's problem (career transition, exploring AI income). Personal note, analyst register: "saw this breakdown of the AI implementation business — the honest-math section made me think of your situation." Link the episode. No ask.
- **Tier 2 — operators/amplifiers (3–5/episode):** people who run the kind of business covered or have adjacent audiences. Ask for a *reaction to the thesis*, not a share. Their comment is worth 50 impressions.
- **Tier 3 — the standing list:** anyone who's ever DM'd about "what should I do next" — they're the ICP. Seed names (Manav, July 6 2026): Henry, Joni — expand per episode from relationship notes. One message per episode max; stop if no response twice.
- **Active pitches / people Manav is talking to:** allowed, but the episode must be *relevant to their situation*, and it never rides inside a pitch thread — separate message, analyst register, no ask. Mixing OE distribution into a live pitch reads as funnel behavior and burns both.
- Rule: DMs carry the analyst framing. The relationship is the moat; never spend it on a blast.
- Per-episode DM shortlist is drafted at schedule time (backlog item #5) so sends happen Mon–Tue while the episode is fresh.

### The Product of One group (owned community — highest-trust surface)

The group solves a real OE problem (warm ICP audience) and OE solves a real group problem (it's been one-way broadcast). Rules of engagement:

- **Neutral citation (Manav's call, July 6, 2026)**: OE is never claimed as his — and never performed as a discovery either. It's cited the way any research source would be: "New breakdown on X. Source: The Operator Economy." The data leads; the source is a footnote. The one banned move inside this framing is active discovery theater ("stumbled onto this," "found this random channel") — passive non-attribution is fine, performed independence is the FakeGuru pattern.
- **Format: carousel + a genuine question**, never an announcement. The question must be one the host is actually unsure about (e.g. "which entry is realistic for a product-of-one — the $2K first project or a day-one retainer?"). Discussion is the goal; the episode is the reference material.
- **Cadence**: 1 per episode max, a day or two AFTER the main launch (the group is depth, not hour-one ignition). Member answers feed back into future episode research — the group is also a research instrument.

### The weekly sequence at a glance

| Day | Surface | Action |
|---|---|---|
| Sun night | YouTube | Schedule episode + Shorts ×4 (links captured) |
| Sun night | LinkedIn OE page | Schedule episode post w/ carousel + shorts posts ×4 (all rubric-gated) |
| Mon 11:00 | — | Episode + OE post live; sources comment; newsletter |
| Mon hour one | Personal | Repost OE carousel post + one-line analyst comment |
| Mon–Tue | DMs | Tier 1/2/3 sends from the shortlist |
| Tue–Wed | Product of One group | Carousel + genuine question (neutral citation) |
| Tue–Fri | YT + OE page | Shorts daily; 2–3 personal analyst posts |

## Phase 4 — The week (Tue–Fri)

- **Shorts publish daily** (YT 8:30, LI page 8:30) — discovery only; every short's description + pinned comment routes to the long-form (+20% documented watch-hour lift from pinned comments).
- **Personal = reposts only** (1–2/week of OE page posts, bare or one-line). `content/linkedin_posts.md` derivations now feed the OE PAGE's midweek posts and the group, not the personal feed.
- **Every surface funnels the same way:** blueprint download → email → newsletter → hour-one watch time on the next episode → Grapevines overlap where relevant.

## The automated week (built July 6, 2026)

Three pieces run the week; humans approve every outbound post.

**1. `studio/launch.py`** — one command, Phase 1 end-to-end:

```
python launch.py <slug> --monday YYYY-MM-DD --title "..."        # dry run
python launch.py <slug> --monday YYYY-MM-DD --title "..." --go   # upload + schedule
```

Rubric-lints all LI copy (`scripts/originate/rubric_check.py` — automated subset of `post-rubric.md`: em-dash/lexicon/opener/income-promise checks; hard fails abort, `--rubric-waiver "reason"` is stamped into the checklist). Schedules YT episode (Mon 11:00 ET) + shorts ×4 (Tue–Fri 8:30 ET), bakes the episode link into shorts descriptions, writes `originate/<slug>/launch/`: `checklist.md`, `links.json` (the manifest the scheduled tasks read), `dm_shortlist.md`.

**2. Cowork scheduled tasks** (approval-gated; LinkedIn via Chrome with the composer gotchas encoded):

| Task | When | Does |
|---|---|---|
| `oe-sunday-launch-prep` | Sun 7pm | Asset check → rubric fix-ups → launch.py dry run → hand Manav the `--go` command → draft + schedule OE page posts (approval per click) → DM shortlist candidates |
| `oe-monday-hour-one` | Mon 10:40 | Verify live → sources comment → newsletter reminder/send → personal repost draft (one-line analyst comment) → site flip → DM reminders |
| `oe-week-driver` | Tue–Fri 8:15 | Verify short + OE post live → daily personal analyst post draft (3/wk cap enforced) → Tue/Wed group package → Tue DM follow-through + amplifier-ladder logging → Fri week wrap |

**3. Rubric linter** — `scripts/originate/rubric_check.py <file> --surface feed|carousel|dm|group`. Run on anything before it ships; it catches the watermarks, humans still do the read-aloud/byline/tap/guru tests.

## Remaining backlog

1. **Re-auth YouTube token with `youtube.force-ssl` scope** (`tools/youtube_auth.py`) — unlocks captions upload AND posting/pinning the shorts' episode-link comments via API (the week-driver currently just flags unpinned comments).
2. **Newsletter send** wired into launch (Resend; blocked on DNS setup from launch checklist).
3. **Thumbnail set via API** — still manual in YT Studio (needs phone-verified channel + force-ssl).

## Packaging loop (thumbnail + title, per episode)

- Title: accurate first, number/hook front-loaded (mobile truncation), branding at the end, curiosity the video resolves. Never over-promise: fast abandonment reads as clickbait and suppresses recommendations.
- Thumbnail: two candidates rendered per episode (`render_data/thumbnail-a/b.json`), reviewed AT SMALL SIZE (320px is the judgment view), winner pushed via API.
- Day 7: check CTR by traffic source in Studio. Only compare like to like (search vs search). Revisit stale thumbnails on older episodes quarterly.
- When the channel unlocks Test & Compare: A/B the two candidates against real impressions instead of picking by eye.

## Kill criteria & cadence guards

- Episode ships Monday or it ships next Monday — never mid-week (the site promise is the contract).
- If hour-one assets aren't ready by Sunday night, the episode still ships; carousel follows same-day. Never delay the video for the marketing.
- Personal profile: reposts of OE page posts only (max 1-2/week, max 1/day); zero original OE posts, zero "look what I found" shares.
