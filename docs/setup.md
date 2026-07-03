# Setup & operations map (who runs what, keys, triggers)

Companion to `automation-architecture.md`. This is the do-this-now checklist.

## Division of labor

| Layer | Runs | Needs |
|---|---|---|
| **Cowork (agent)** | Research briefs (web research + nuance hunting), script drafts, all evals + confidence scoring, queue management, repo hygiene, analytics synthesis, scheduled tasks | Nothing — no API keys. The agent writes scripts directly; evals are pure Python |
| **Claude Code / terminal (Manav's machine)** | Keyed studio steps: `originate.py continue` (ElevenLabs VO), render, `upload_youtube.py`, anything touching accounts | Local env vars (below) |
| **Manav (human)** | Escalated reviews, episode-library review (training mode), POV input, Studio finishing checklist (~10 min), screen recordings if an episode truly needs one | Judgment |

Handoff medium = the git repo. The scheduled task commits; you pull and run keyed steps; artifacts commit back.

## Status — July 2, 2026 session

DONE: Anthropic key → `studio/.env` (gitignored) · domain bought (Vercel) · YouTube channel branded via browser (name "The Operator Economy", @operatoreconomy, full description published) · GCC project `operator-economy` under brownmanbeard@gmail.com: YouTube Data API v3 + Analytics API enabled, OAuth consent screen (External/testing), Desktop OAuth client created, client-secret JSON in Downloads (→ move to `studio/.secrets/`, gitignored), brownmanbeard added as test user.
DONE (later same day): ElevenLabs key → `studio/.env` — account is **Pro tier** (607K chars/mo, commercial rights) and a **Professional Voice Clone already exists**: 'brown man pro' (`q9RtP62PWHxX4IPG7uSM`), now set in `studio/config/blueprint.json`. Smoke-tested the exact pipeline path (PVC + eleven_v3 + with-timestamps endpoint): 5s audio + character alignment returned clean.
## Voice clone quality — diagnosis & retrain protocol (July 2026)

The PVC was trained on 4 mismatched sources: 2 noisy quick memos (noise floor −55/−60dB, peaks near clipping — DROP these), one clean 24-min read (−78dB floor, good), and a 65-min file that was noise-gated + heavily compressed (LRA 2.5, digital-zero gaps — the main quality culprit). Mixed acoustic signatures = muddy clone.

**Retrain protocol:** (1) Use the two cleaned files (highpass + matched to −19.4 LUFS both, produced 2026-07-02, in Cowork outputs) — ~88 min total, comfortably above PVC minimums. (2) In ElevenLabs → the "Operator Economy" voice → Edit → REMOVE all four old samples → upload the two cleaned files → retrain. (3) Best upgrade beyond cleanup: record 15–20 min of NARRATION-style reading (the pilot script, natural pace, expressive) on a decent mic in a quiet room — the gated 65-min file also taught the clone a flat delivery; new narration-style source fixes tone, not just noise. Add it as a third sample. (4) Re-run the smoke test line and A/B against the old render. Tool for future sample prep: `studio/tools/clean_voice_samples.sh` (two-pass loudnorm version — run locally).

**VOICE FINAL v2 (2026-07-03): 'OE Narrator NY-A1' — `jd5NxG8GP6b1WEHcoUtt`** — N3 lasted one render: in full-episode context it read as slightly southern and flat (culprit phrases in its design: "relaxed rhythm", "soft gentle sentence endings"). Round 7: two NY/NJ designs (accent-forward A, dynamics-forward B), 6 previews + 3 A1-remixes at matched mastering → NY-A1 won. Design keys that worked: explicit "New York New Jersey metro accent, natural and lived-in, never a caricature" + concrete pitch-movement clauses ("rises on questions, punches the key word, drops low and slows before a big number"). Stability lowered 0.5→0.4 to keep the dynamics alive in long sections. Backup sibling 'OE Narrator NY-A3' (`YR5XeZ2m8xkiHvN7OYSZ`) saved permanently. Mastering chain (exciter/presence EQ/de-ess/-14 LUFS, 192k) runs automatically in generate_vo.py. Locked for the first 10 episodes; retention data arbitrates after.

Superseded: 'OE Narrator N3' `lwlQZ256x0pEeDBOaBMm` (natural batch, 6-round search — kept in library) and 'Operator Economy Narrator' `JhQpKkIWYoZ6C57GRz08`, a DESIGNED voice (Voice Design v3; East Coast + natural-conversational blend, 3 iteration rounds), saved permanently and smoke-tested through the pipeline path (v3 + with-timestamps). Decision: designed publication voice over the muddy PVC; PVC retained for a possible Phase 2 retrain (protocol above stays valid). Disclosure unchanged: containsSyntheticMedia=true on every upload.

**E2E TEST PASSED (2026-07-03):** full path validated — narrator VO (v3+timestamps) → ffmpeg assembly (-14 LUFS) → OAuth (token.json, 3 scopes, refresh working) → `videos.insert` upload → **private AND unlisted both work** (audit lock did NOT bite at this quota tier) → `containsSyntheticMedia: True` confirmed set via API. First test (https://youtu.be/trVrdmT3Hyo) landed on the PERSONAL channel — token was bound to the wrong identity at the consent chooser; youtube_auth.py now verifies + prints channel binding. Re-auth bound to The Operator Economy; second test https://youtu.be/grqF6IXf2hI uploaded to the CORRECT channel (private, disclosure flag set). Manav deletes both test videos. Post-test hygiene: rotate Anthropic/ElevenLabs keys + the two GOCSPX secrets that passed through chat; disable the wrong-project gen-lang OAuth client.

PENDING: YouTube API compliance audit form · phone verification for thumbnails · pronunciation dictionary (build during pilot VO) · Resend domain DNS · site build on Vercel.

## Accounts & keys checklist

| # | Tool | Plan / cost | Setup action | Key |
|---|---|---|---|---|
| 1 | Anthropic API | usage (~$20–40/mo) | console.anthropic.com → key | `ANTHROPIC_API_KEY` (local env) |
| 2 | **ElevenLabs** | **Creator $22/mo** (required: commercial rights + Professional Voice Clone) | ✅ have account → upgrade to Creator → record PVC clone (30+ min clean audio) → paste voice_id into `studio/config/blueprint.json` → build pronunciation dictionary (finance terms: ARR, EBITDA, SaaS, tickers) — **model must stay `eleven_v3`** (dictionaries silently ignored on multilingual_v2) | `ELEVENLABS_API_KEY` |
| 3 | Google Cloud | free | Create project → enable **YouTube Data API v3 + YouTube Analytics API** → OAuth desktop credentials → **submit API compliance audit NOW** (unaudited projects upload private-only; no review timeline) → phone-verify the channel (custom thumbnails) | OAuth `client_secret.json` + token (local) |
| 4 | Domain | $11.25/yr | Buy theoperatoreconomy.com ([Vercel](https://vercel.com/domains/search?q=theoperatoreconomy.com)) | — |
| 5 | **Resend** (decided) | $0 (3K emails/mo free) | Manav has account. Add theoperatoreconomy.com domain in Resend → set DKIM/SPF DNS records in Vercel → Audiences for the list + Broadcasts for the newsletter; capture form on the Vercel site posts to Resend API | `RESEND_API_KEY` |
| 6 | ~~Buffer~~ **LinkedIn via existing computer-use workflow** (decided) | $0 | OE posts ride the same Claude-driven LinkedIn workflow as brownbot/Grapevines — weekly volume adds no new risk surface. Human reviews before post | — |
| 7 | *Later:* Templated | $29/mo | Thumbnail templates from design system — only when manual thumbnails become the bottleneck | `TEMPLATED_API_KEY` |
| 8 | *Later:* AWS + Cloudflare R2 | pennies | Remotion Lambda — only when local render time actually hurts | AWS creds |
| 9 | *Later:* Exa / Perplexity | $0–20/mo | Only if agent-native research outgrows sessions (volume, not quality) | keys |

**MCPs worth connecting in Cowork:** none required to start. Optional later: a YouTube Analytics connector (or we script the weekly pull locally via OAuth), and email platform MCP if one exists for beehiiv/Kit.

## Triggers & crons

| Trigger | What fires | Mechanism |
|---|---|---|
| **Monday morning** | Weekly kickoff: pick top queue topic → agent research (nuance requirement) → brief + claim registry → script draft → rigor + craft evals → confidence verdict → commit → notify (Gate 1 summary + AUTO-PASS/ESCALATE) | **Cowork scheduled task** |
| Post-Gate-1 | `originate.py continue <slug>` (VO + assets + checks) then `render` | You (or Claude Code) on your machine — takes minutes |
| Pre-publish | Episode library assembled → confidence `--stage prepublish` → training-mode review → `upload_youtube.py` + Studio checklist | Session with the agent |
| Publish day | Newsletter send (first hour), Buffer LinkedIn queue, Shorts schedule | beehiiv/Kit automation + Buffer queue (set up once) |
| **Friday** | Analytics readback: pull 7d/28d metrics → compare to rubric predictions → topic-score suggestions | **Cowork scheduled task** (once OAuth wired; manual export until then) |
| Monthly | 10-video sameness test + rubric reweight review | Calendar reminder / scheduled task |

## Voice / video / avatar verdicts (July 2026)

**Voice — keep ElevenLabs.** It remains the naturalness leader, which matters more here than anywhere: perceived-synthetic VO carries a measured retention penalty, and our whole brand is trust. Alternatives fail on fit: Cartesia's edge is latency (irrelevant for offline renders), OpenAI TTS has no cloning and lower naturalness, PlayHT is winding down post-Meta acquisition. Non-negotiables: Creator plan (commercial rights), PVC clone of YOUR voice (keeps it human-authored in spirit + Phase 2 face-transition continuity), v3 model, pronunciation dictionary, two-pass loudnorm to −14 LUFS.

**Video creation/editing — Remotion IS the editor for this format.** Our videos are data-driven motion graphics + VO; Remotion renders them from code, which is the entire automation thesis. A timeline editor (Premiere/Descript/CapCut) would reintroduce the manual step we engineered out. Descript becomes relevant only for Phase 2 interview episodes (transcript-based editing of real footage).

**Avatar — not for the flagship, optional for Shorts experiments.** The format is deliberately faceless-documentary; an AI avatar fronting it lands in the uncanny "AI-slop" zone our audience punishes, and a *realistic avatar of a real person* triggers mandatory synthetic-media disclosure in its strongest form. When the face-forward phase comes (Phase 2+), it should be your real face. If you want avatar experiments before that: HeyGen is the current quality leader (Avatar IV, ~$24/mo Creator) vs Synthesia (enterprise-priced, $29/mo for only 120 min/yr) — use it for low-stakes Shorts tests, never the flagship. Your existing avatar test script (the "$40K receptionist") is the right test vehicle.
