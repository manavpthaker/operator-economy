# Gate 1 punch list — EP004 `small-cohort-business`

Generated 2026-07-31 (Cowork week-driver). Draft script produced via `_cowork_script_batch.py`
(Batches API shim replicating `generate_script.py`), then `eval_script --mode draft`,
`eval_package`, `confidence --stage script`.

**Working title:** The Six-Person Business Model Nobody Markets
**Confidence: 0.700 → ESCALATE** (rigor hard-fail + below 0.85 threshold)
**Rigor: 15/22 · Craft auto-score: 57/63 → PROJECTED PASS** (+37 human-judged; gate needs ≥80/100 and zero kills)

> **Updated 2026-07-31.** Both eval bugs flagged in §B below are now **fixed** (`docs/evals.md`).
> The kill-list hit is gone and the hook now scores 10/10 + 5/5 — **with no change to the script**;
> it was always a false positive. Score moved 0.604 → 0.700 and the publish verdict went
> BLOCKED → PROJECTED PASS. §B is kept as the record of what was wrong.
> Everything in §A is still real work and still yours.

Escalation at draft stage is normal — Gate 1 is where it gets fixed. Below is everything the
evals flagged, sorted by whether it's a real defect or an eval artifact.

---

## A. Real fixes — content (yours, this is the POV pass)

**1. POV tokens: 1, need ≥2.** Only one insertion point survived:
- `evidence#2` — *"[POV: Manav could add what it was like building her intake flow and watching the consults not convert despite a clean funnel]"*

That one is well-placed. You need at least one more, and the obvious hole is **`stack`** — you
built the Reframe & Ready platform and the script currently describes the stack without you in
it. The queue's POV note for this episode is "builder-behind-the-infrastructure," and right now
the infrastructure has no builder on screen.

**2. Unsourced money claims (rigor hard-fail):**
- `hook#1` — cites "twenty million dollars" and the Miro acquisition with `source: null`. Both are
  in the brief (TechCrunch/a16z; Miro newsroom Mar 24 2026). Just needs the source field.
- `evidence#3` — no source, but it makes no money claim; it's the "Joanie is not proof of demand"
  beat. Likely a false trip from "fifteen people will pay two thousand dollars." Mark as
  reference-to-prior-claim or restate without the figures.
- `evidence#7` and `economics#1`/`#4` also carry `source: null` — no numbers in them, low priority.

**3. Evidence section fails the low-end/high-end span check.** The eval scans the evidence
section for `billion|enterprise` (high) and `solo|freelancer|one person|small` (low). It finds
**neither**, because every high-end figure is in millions and the low end is named as "Joanie"
rather than described as solo. Both fixes are legitimate copy improvements, not eval-gaming:
- High end: Miro is a multi-**billion**-dollar company. "A company worth billions bought the
  category's flagship" is truer and hits harder than the current phrasing.
- Low end: say "**solo**" or "**one person**" out loud in the Joanie beats.

**4. Caption highlight words:**
- `thesis#3` — highlights `'one cohort a year'`, but the VO says "a **single** cohort a year." Match them.
- `economics#1` — only 1 highlight word; needs 2–4.

**5. Hook is 57 words (152% of the 38-word budget) ≈ 23 seconds.** Retention-log Rule 1 says the
hook number lands **≤0:15**. This hook is good — three operators, same model, wildly different
outcomes — but it's long. Cut ~20 words.

**6. Section word budgets are light.** Total 1,388 vs 1,624 target (85%, ≈9:15 at 150wpm).
`stack` 72%, `playbook` 69%, `cta` 66%. Add beats rather than lengthening sentences.

**7. Sections don't end on open loops:** `thesis`, `playbook`, `economics`. `evidence#7` does it
well ("what's actually left for the person running it alone?") — copy that move.

**8. `economics#1` opens the section with the blueprint CTA.** It passes the mid-video-mention
rule, but leading a section with the ask is weak placement. Move it to the section's back half.

---

## B. Eval artifacts — BOTH FIXED 2026-07-31 (record kept)

**1. `[FAIL] hook: concrete tension in first two sentences` is a false negative.**
The check (`eval_script.py:110-131`) wants a digit, `?`, a quoted phrase, or one of
`but / yet / however / instead / not because / isn't / is not` in the first two sentences. The
hook has genuine contrast — *"one paying student"* vs *"filled six seats"* — but the numbers are
**spelled out**, which is correct for voiceover, and the contrast is implied rather than signposted.

Cheapest honest fix is in the copy: signpost the pivot with an explicit contrast word. But note
the structural tension — this check will keep punishing VO-correct number spelling on every
episode. Worth widening the regex to catch spelled-out numerals.

**2. `KILL-LIST: early CTA` is a false positive, and it is currently blocking the publish gate.**
`eval_package.py:202` does a bare substring test:

```python
early_cta = any(w in early_text for w in ["subscribe", "blueprint", "link below", "download"])
```

The only match in the whole early script is `evidence#4`: *"he had a multi-million-**subscriber**
audience before he sold a single seat."* "subscriber" contains "subscribe." There is no CTA
anywhere before the payoff.

This is a one-line fix (word-boundary match, `\bsubscribe\b`) and it will otherwise mis-kill any
episode that says the word "subscriber" — which, for a channel about audience businesses, is
going to be often. **I did not apply it** — it changes gate logic, so it's your call.

---

## C. Fact-check — every load-bearing number traced to the brief

| Claim in script | Brief | Verdict |
|---|---|---|
| Joanie: one enrollee, peer filled six, $60 webinar underfilled | §1, first-party call notes | ✅ |
| "$800 is a lot," consults not converting, testing pay-on-placement | §1 | ✅ |
| Abdaal ~$5K/seat, first cohort ~$294K, later ~$1.9M, discounted on screen | §1 ⚠️ reported | ✅ — and the discount is stated, which is the point |
| Maven $20M Series A (a16z), 300+ cohorts, ~$9M in 18 months | §2 | ✅ |
| Reforge $81M raised, 100K alumni, Netflix/SAP | §2 | ✅ |
| Reforge acquired by Miro, March 2026, into a workplace software company | §2, Miro newsroom | ✅ |
| 6 × $2,000 = $12,000; Maven fee ≈ $1,500 ≈ one enrollee | §4 | ✅ — this is the episode's best beat |
| First-timer realistic: 6–8 seats, $4K–$15K gross | §1 derived, marked `estimate` | ✅ marked |

No invented numbers. No claim in the script that isn't in the brief.

---

## D. What's genuinely good (don't edit it out)

- **The three-way hook** — one student / six students / $20M-and-acquired, same business model.
- **The Reforge-to-Miro read** (`evidence#6-7`): "The best-funded version of selling expertise to
  professionals didn't become an education empire. It became a feature inside someone else's
  product." That's the episode's non-consensus angle and it's landed.
- **The Abdaal discount** — naming the ceiling anecdote as "close to worthless for planning your
  first cohort" is exactly the register competitors won't use.
- **The platform-tax beat** — "one enrollee's worth of revenue, gone before you've taught a single
  session." Concrete, sourced, and it's the shorts moment.
- **`economics#4`**: "The build risk is close to zero now. The enrollment risk never went away."
  That's the thesis in two sentences.

---

## E. Carried forward from this week's launch review

Applies at publish, not now, but these are the open EP004 obligations:

- **Thumbnail gate (retention-log Rule 6).** EP003 shipped the raw title-card frame and drew
  0.0% CTR on 142 recommended impressions. EP004 needs a 3-word thumbnail readable at 120px.
  The generated options are usable: `Six Is Enough` / `One Student. Real.` / `The Fee Nobody Mentions`.
- **Pinned comments carry live URLs (Rule 7).** No "link in bio."
- **Joanie gets the EP004 blueprint PDF before ship**, and her stuck-points calibrate blueprint
  depth. Both were promised on the July 14 call and both survive the interview being dropped.
- Fix the `№ 001` title-card number in the shorts renderer before EP004's shorts are cut.

---

## Next command (after the POV pass)

```bash
cd studio && python originate.py continue small-cohort-business
```

`eval_script --mode approved` hard-fails on any remaining `[POV:` token, so the pass has to be
complete before VO generation will run.
