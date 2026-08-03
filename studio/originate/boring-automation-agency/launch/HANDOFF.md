# EP003 launch handoff — The Boring-Automation Agency (Mon 2026-07-27)

Everything that can be prepped in Cowork is done. What's left is Mac-side (Remotion renders + YouTube upload) and Chrome (LinkedIn scheduling), because neither can run in the Cowork sandbox. This doc is the exact order.

---

## Status

| Piece | State |
|---|---|
| Long-form storyboard | Re-tuned 18 → **21/23** (PASS, 0 kills). 39 → 56 screens, no static hold > ~18s. |
| Long-form render-data | Regenerated (`render_data/blueprint.json`, 56 screens, 674s). Music bed rebuilt. |
| Long-form MP4 | **STALE** (`output/boring-automation-agency.mp4` is the old 39-screen cut). Needs re-render. |
| 4 shorts | Render-data + audio ready (v1: captions over audio). ⚠ short-02 (62s) / short-03 (56s) run long. |
| Pre-launch trailer | Built: 24.7s, v2 montage scenes, Monday end card. `render_data/trailer.json`. Preview HTML delivered. |
| Post-launch teaser | Built: same montage, "watch now" end card + live-episode link. `render_data/teaser.json`. |
| Blueprint PDF | Draft rendered (WeasyPrint) → `Operator-Blueprint-003.pdf` (5pp) + sampler (4pp) + on site. Re-render via Chrome for final fonts. |
| Carousel | `carousel-003.pdf` (8 slides, on-brand). |
| All LinkedIn + newsletter copy | Written + rubric-gated. `launch/linkedin_package.md`, `launch/group_package.md`, `content/newsletter.md`. |
| Launch package | `links.json` + `checklist.md` written (dry-run). |

---

## Gate 3 — pre-publish review (mandatory in training_mode)

Automated evals: **rigor 0.98 · craft 75/75 · edit 21/23 · 0 kill-list hits.** Confidence **0.729 → ESCALATE**.

The ESCALATE is driven entirely by the claim registry reading `verified_ratio: 0.0` (25% weight). It flags 6 load-bearing money claims as "unverified." But every one of them is already sourced and hedged in the script and blueprint:

1. Zapier ~$310M revenue / ~$5B valuation on ~$1.4M raised — getLatka/Sacra, flagged **reported**
2. n8n $2.5B valuation, 3,000+ enterprise customers — Ventureburn/TechCrunch, **verified**
3. Make/Integromat acquisition, 500K+ users, $9/mo — Zapier blog/G2, **reported**
4. iPaaS market $14–23B, 20%+ CAGR — analyst estimates, flagged **wide range / estimate**
5. Solo agency fees $1,500–5,000 / retainers $500–5,000/mo — vendor guides, flagged **reported, unaudited**
6. Stack < $100/mo; year-one $2–6K/mo — public tool pricing (exempt) + **estimate**, flagged aloud

**My read: editorially publish-ready.** The confidence gate is catching an unpopulated registry, not a sourcing problem. Your call at Gate 3: confirm the six are handled (they are), and if you want confidence above 0.85, mark them verified/reported/estimate in the claim registry and re-run `confidence.py --stage prepublish`. Nothing here should block the Monday drop.

---

## Do this on your Mac (in order)

**1. Re-render the long-form** (the long pole — start it first):
```
cd studio/remotion
npx remotion render src/index.ts Blueprint ../output/boring-automation-agency.mp4 \
    --props=../originate/boring-automation-agency/render_data/blueprint.json
```
VO is already in `remotion/public/vo/` (unchanged) and the bed is in `remotion/public/music/`. Review in VLC, not QuickTime.

**2. (Optional but recommended) tighten shorts 02 & 03**, then re-cut all shorts + trailer + teaser from the fresh render:
```
cd studio
python scripts/originate/prepare_shorts.py originate/boring-automation-agency/script.json \
    --video output/boring-automation-agency.mp4 --trailer
python scripts/originate/write_shorts_scenes.py boring-automation-agency   # re-pins trailer + teaser scenes
```
(To tighten 02/03, move their `cliffhanger_line` earlier in `content/shorts_briefs.json` so the window lands ~30–40s, then re-run the two commands.)

**3. Render shorts + trailer + teaser** (from `studio/remotion`):
```
npx remotion render src/index.ts Short out/trailer.mp4 --props=../originate/boring-automation-agency/render_data/trailer.json
npx remotion render src/index.ts Short out/teaser.mp4  --props=../originate/boring-automation-agency/render_data/teaser.json
for n in 01 02 03 04; do npx remotion render src/index.ts Short out/short-$n.mp4 --props=../originate/boring-automation-agency/render_data/short-$n.json; done
```

**4. Re-render the blueprint PDF via Chrome** (final font fidelity — Chrome auto-detected on your Mac):
```
cd studio
python scripts/originate/render_blueprint.py originate/boring-automation-agency/script.json \
    --number 003 --rev A --difficulty Med --hero "\$5B → \$2K" \
    --hero-caption "The same boring job at two scales: Zapier's valuation, and a solo operator's first build." --rail-out "\$2K"
```

**5. Schedule the YouTube week** (episode Mon 11:00, trailer Sun 18:00, shorts Tue–Fri 8:30):
```
cd studio
python launch.py boring-automation-agency --monday 2026-07-27 \
    --title "The 5 Billion Dollar Business That Sounds Boring" \
    --video output/boring-automation-agency.mp4 --go
```
This uploads via the YouTube API (needs your token), captures the real URLs, and rewrites `links.json` + `checklist.md`. Then in YT Studio: SRT captions, custom thumbnail, end screen, AI-disclosure box (required — synthetic VO).

---

## LinkedIn (Chrome, approval-gated — I can drive this once links.json has real URLs)

All from `launch/linkedin_package.md`, all from the OE page, no links in post bodies:
- Sun ~6pm: trailer post (native `trailer.mp4`) + first comment.
- Mon 11:00: episode post (attach `carousel-003.pdf` LAST) + sources comment at 11:05.
- Tue–Fri 8:30: 4 shorts posts (native verticals).
- Tue or Wed: Product of One group post (`group_package.md`, attach carousel) — deconflict with any enabled Grapevines `li-*-group*` task (max one group post/day across engines).
- Mon hour one: personal repost of the episode post + the one-liner.
- Mon ~11:15: newsletter send (`content/newsletter.md`).

Say the word once you've run `--go` and I'll schedule these in Chrome, pausing for your approval on each.

---

## Before you close the laptop: commit

The entire `studio/originate/boring-automation-agency/` directory is **untracked in git**, and this session also edited shared files: `hand_tune_storyboard.py` (the re-tune), `write_shorts_scenes.py` (EP003 + teaser scenes), and `content/blueprint.md` (conformed to the renderer's canonical section names — a real fix; `derive_content.py`'s blueprint template emits non-canonical headings that crash `render_blueprint.py`, worth fixing at the source later). Last commit was Jul 14. Commit + push so a day of EP003 work isn't sitting loose.
