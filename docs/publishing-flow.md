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
```

Render locally (Manav's machine — Remotion only):

```
cd studio/remotion
npx remotion render src/index.ts Blueprint out/ep00N.mp4 --props=../originate/<slug>/render_data/blueprint.json
npx remotion render src/index.ts Short out/short-0K.mp4 --props=../originate/<slug>/render_data/short-0K.json   # ×4
```

Review in **VLC, never QuickTime** (QuickTime drifts + pitches down long AAC files — verified EP001).

## Phase 1 — Schedule (Sunday night / Monday early)

Everything targets **Monday 11:00 AM ET** for the episode ("ships every Monday" is on the site), **8:30 AM ET** for daily posts.

| What | Where | When | How |
|---|---|---|---|
| Episode | YouTube | Mon 11:00 AM | `upload_youtube.py <file> --title ... --description-file ... --privacy private --publish-at <UTC>` — AI-disclosure flag auto-set |
| SRT captions | YouTube Studio | with upload | Generated from alignment (`ep00N.srt`); drag into Subtitles (API lacks force-ssl scope) |
| Thumbnail | YouTube Studio | with upload | Extract the title-card frame (`ffmpeg -ss ~21.5s`) — it IS the thumbnail. Requires phone-verified channel |
| End screen | YouTube Studio | with upload | Last 6s (outro card) designed for overlays: Subscribe + "Best for viewer" video |
| Shorts ×4 | YouTube | Tue–Fri 8:30 AM | Same script, `--publish-at` staggered; description carries episode + blueprint links |
| Episode post | LinkedIn **OE page** | Mon 11:00 AM | Hour-one package, see Phase 2 |
| Shorts posts ×4 | LinkedIn **OE page** | Tue–Fri 8:30 AM | Native vertical video + standalone insight text |
| Newsletter | Resend | Mon ~11:15 AM | From `content/newsletter.md`; drives hour-one watch time |
| Site | theoperatoreconomy.com | Mon | `episodes.json` gets `youtube_url`, status live; git push deploys |

**Identity rule: all OE content posts from The Operator Economy page.** Personal profile's role is defined in Phase 3.

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

> **EP001 gap:** we shipped a text post, no carousel, and the newsletter didn't go. The carousel is the single highest-leverage missing piece. → automation backlog below.

## Phase 3 — The personal-profile play (1K followers + DM relationships)

The register rule from `research/comp-synthesis.md`: the audience (35–55 ops/product leaders) detects and punishes undisclosed self-promotion. **Never repeatedly "share" OE as something stumbled upon** — that middle path is the FakeGuru exposure pattern. Two sanctioned framings:

- **Analyst framing (the default, 2–3×/week):** share the *finding*, not the channel. "Accenture's only growing line is installation work — here's the unit economics." Own commentary, OE credited low-key as the source. The insight earns the engagement; the curious follow the trail. These are the Tue–Fri derivation posts — they can live on the personal profile in Manav's voice because they're his analysis *of* the material.
- **Publisher framing (rare, at milestones):** "I've been building a research property on this thesis." Once at launch (after 2–3 episodes exist, so a click-through finds a library), then at real milestones. Building in public is on-thesis — the channel is its own proof of concept.

**The DM pipeline** (the warm-relationship asset — this is what 1K followers + real relationships buy):
- **Tier 1 — direct relevance (5–10 people/episode):** people actively facing the episode's problem (career transition, exploring AI income). Personal note, analyst register: "saw this breakdown of the AI implementation business — the honest-math section made me think of your situation." Link the episode. No ask.
- **Tier 2 — operators/amplifiers (3–5/episode):** people who run the kind of business covered or have adjacent audiences. Ask for a *reaction to the thesis*, not a share. Their comment is worth 50 impressions.
- **Tier 3 — the standing list:** anyone who's ever DM'd about "what should I do next" — they're the ICP. One message per episode max; stop if no response twice.
- Rule: DMs carry the analyst framing. The relationship is the moat; never spend it on a blast.

### The Product of One group (owned community — highest-trust surface)

The group solves a real OE problem (warm ICP audience) and OE solves a real group problem (it's been one-way broadcast). Rules of engagement:

- **Disclose once, lightly**: first OE share includes one clause — "a research property I publish." In a hosted community, the 'outside source I found' framing is the highest-risk move, not the safest: when members connect it (they will — same design language, reposts on the personal profile), host-promoting-his-own-thing-covertly is the exact trust hit the comp synthesis warns about. After the one disclosure, OE is just a cited source.
- **Format: carousel + a genuine question**, never an announcement. The question must be one the host is actually unsure about (e.g. "which entry is realistic for a product-of-one — the $2K first project or a day-one retainer?"). Discussion is the goal; the episode is the reference material.
- **Cadence**: 1 per episode max, a day or two AFTER the main launch (the group is depth, not hour-one ignition). Member answers feed back into future episode research — the group is also a research instrument.

## Phase 4 — The week (Tue–Fri)

- **Shorts publish daily** (YT 8:30, LI page 8:30) — discovery only; every short's description + pinned comment routes to the long-form (+20% documented watch-hour lift from pinned comments).
- **2–3 analyst-framing text posts** on personal, derived from script acts + surplus research data points (`content/linkedin_posts.md` is the seed; each stands alone, OE credited).
- **Every surface funnels the same way:** blueprint download → email → newsletter → hour-one watch time on the next episode → Grapevines overlap where relevant.

## Automation backlog (in priority order)

1. **Carousel generator** — `derive_content.py` gains a `carousel` output: 8–12 slide JSON → branded PDF via the OE design system (navy/paper/gold, Boska/Fragment Mono — same tokens as `remotion/src/oe/theme.ts`). Blocks Phase 2 being automatic.
2. **Re-auth YouTube token with `youtube.force-ssl` scope** (`tools/youtube_auth.py`) — unlocks captions upload AND posting/pinning the shorts' episode-link comments via API.
3. **Newsletter send** wired into launch (Resend; blocked on DNS setup from launch checklist).
4. **`launch.py`** — one command that runs Phase 1 end-to-end from a manifest (upload episode + shorts with computed publish-at times, set thumbnail, write the hour-one checklist). LinkedIn stays manual/browser until an API path exists.
5. **DM shortlist generator** — per episode, Claude drafts the Tier 1/2 candidate list + message drafts from Manav's relationship notes; he approves and sends.

## Kill criteria & cadence guards

- Episode ships Monday or it ships next Monday — never mid-week (the site promise is the contract).
- If hour-one assets aren't ready by Sunday night, the episode still ships; carousel follows same-day. Never delay the video for the marketing.
- Personal profile: max 3 OE-derived posts/week; zero "look what I found" shares.
