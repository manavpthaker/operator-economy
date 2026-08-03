# Gate 1 — `solo-design-agency`

Updated 2026-07-31 after the editorial pass. Brief: `research/briefs/ep-solo-design-agency.md`.
Pre-edit draft preserved at `script.json.pre-gate1`.

**Working title:** One Person, $5,000 a Month, No Employees

| | draft | now |
|---|---|---|
| Confidence | 0.829 ESCALATE | **0.979 AUTO-PASS** |
| Rigor | 14/22 | **22/22** |
| Craft (auto) | 54/63 | **63/63** |
| Kill-list | none | none |
| Length | 1,098 words (~7:20) | **1,633 words (~10:00)** |

Everything the evals can check is clear. **The only work left is yours: two POV tokens.**

---

## The one thing left

`eval_script --mode approved` hard-fails while any `[POV:` token remains, so `continue` will not
run until both are replaced. These are deliberately the two places the script is thinnest on
lived experience:

**`evidence#5`**
> *[POV: add one specific detail from building a BusyLobby demo — what the demo-first approach actually looked like for one real prospect]*

Sits right after the beat where you say BusyLobby isn't a revenue case yet. One concrete detail
here is what turns that admission from a weakness into the most credible moment in the episode.

**`stack#4`**
> *[POV: the moment the tools produced something good and you still had to overrule them — one specific call the software couldn't have made]*

This is the load-bearing one. The whole stack section argues that production collapsed but
judgment didn't, and right now that argument is asserted rather than demonstrated. A specific
overrule is the proof.

Then:

```bash
cd studio && python originate.py continue solo-design-agency
```

---

## What changed in the editorial pass

**Added Figma's actual money (`evidence#8-9`).** The draft had Figma three times as a *tool* and
never once as a company. Now: IPO day-one close ~$68B, $1.056B FY2025 revenue, ~$1.4B FY2026
guidance, set against the ~$15.1B US design services industry it sells into. This landed the
brief's sharpest structural point — the tool vendor captured the category — and fixed the failing
low-end/high-end span check. `evidence#9` names the market-cap-vs-annual-revenue comparison as
unfair in the VO rather than letting it slide, and calls back to EP003's Zapier finding as a
pattern the channel keeps hitting rather than a fresh discovery.

**Brought the thin sections to budget.** `stack` 50%→96%, `playbook` 52%→98%, by adding beats
rather than lengthening sentences. New material, all from the brief:
- `stack#4` — the tools produce, they don't pick (carries the second POV token)
- `stack#5` — more than half of Figma's largest customers now generate inside the tool weekly; your clients have the same buttons
- `playbook#6` — the $549/mo floor and why narrow scope is what lets you charge $5,000
- `playbook#7` — build the renewal in month one; this is a retention business dressed as a creative one
- `playbook#8` — the first client comes from the warm list; the cold pipeline is how you learn what to say

**Trimmed the hook** 52→40 words to land inside the 0:15 rule (retention-log Rule 1), keeping the
money in the first two sentences so all three hook checks still pass.

**Hedged every weak-sourced claim aloud.** 13 beats carried `[reported]`/`[estimate]` sources with
no hedge in the spoken text. All now flag it in the VO, not just the footnote — house rule, and
the reason the rigor check went to 22/22. Phrasing is varied ("reportedly," "an estimate,"
"reported by him," "one person's reported number, not a law") so it reads as rigor rather than
disclaimer.

**Open loops on all five body sections** (was 0/5). Each now ends on the question the next section
answers — `evidence#9` closes on *"what's actually left for one person?"*, `stack#5` on *"knowing
the stack isn't the same as knowing how to get the first person to pay for it."*

**Fixed** three caption beats under the 2-word minimum, one more that referenced text not in the
VO, and sourced the `playbook#5` capacity chart.

---

## Fact-check — every number traced to the brief

| Claim | Verdict |
|---|---|
| Designjoy reported at $1M / $1.5M / $1.7M / $2M+ / $3.1M, all self-reported, no audit | ✅ said aloud |
| Zero contractors, ~35 clients, $4,995/mo flat, ~5 hrs/day, $95/mo tools, $29 template start | ✅ hedged |
| Superside $44.9M ARR 2024 (from $30.8M), $35M raised, ~850 employees, 450+ clients, $15K/mo min | ✅ |
| Figma IPO ~$68B day one; $1.056B FY2025; ~$1.4B FY2026 guidance; >50% of largest customers in Make weekly; 70% AI adoption | ✅ |
| US design services ~$15.1B/yr | ✅ comparison flagged as unfair in VO |
| Relume $38/mo, v0/Lovable ~$25/mo, ManyPixels $549/mo floor, solo band $2,500–$7,500 | ✅ |
| BusyLobby: 6 outreach, 1 callback, first close in progress, **not a revenue case** | ✅ stated plainly |

Nothing in the script that isn't in the brief.

**BusyLobby state confirmed 2026-07-31:** 6 outreach, 1 callback, **no signed client.** `evidence#4`
was overstating with "first close in progress" and now reads "Six outreach emails so far. One
callback. No signed client."

**On the 1-of-6 number — decided, don't revisit.** It is never stated as a percentage. 16.7% from
six emails implies a rate the sample can't support, and it's the exact move the evidence section
spends four beats criticizing in Designjoy's self-reported figures. Instead, `evidence#5` (new)
gives the raw count, the sourced 2026 benchmark (3–5% average reply; ~5.8% for lists under 50),
and then names the sample problem out loud:

> *"But six emails is not a sample. It's an anecdote with a good ratio, and calling it a seventeen
> percent response rate would be exactly the move I just called out."*

This is stronger than either the bare count or the percentage — it demonstrates the rigor the
episode demands of everyone else, and the benchmark data independently supports the playbook's
core claim that small hyper-targeted lists beat volume.

---

## Packaging (the constraint this quarter)

Thumbnail options: **`850 vs 1`** / `One Person Studio` / `No Employees`.

`850 vs 1` is the pick. Two numerals, maximum contrast, readable at 120px, and it encodes the
episode's whole argument. EP003 drew 0.0% CTR on 142 recommended impressions with an unreadable
title-card frame — this is the test of retention-log Rule 6.

Also carried forward: pinned comments carry live URLs, no "link in bio" (Rule 7); fix the `№ 001`
title-card number in the shorts renderer before shorts are cut.

---

## Still worth a decision

Second consecutive episode where the first-party example has no revenue — EP004 is Joanie's cohort
of one, this is BusyLobby pre-close. Both handle it honestly and `evidence#4` says it plainly. But
twice reads as a pattern. Either land the close before this ships, or make "I publish the ones I'm
still in the middle of" an explicit channel stance rather than a drift.
