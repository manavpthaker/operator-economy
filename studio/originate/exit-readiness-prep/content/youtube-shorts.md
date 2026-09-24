# EP007 Shorts: YouTube publication copy

Status: **owner-approved 2026-09-23.** Nothing uploaded, scheduled, or published. No URL is stated.
`{{EPISODE_URL}}` resolves only from `studio/originate/exit-readiness-prep/launch/links.json`,
which does not exist yet. If the launch gate has not filled it, the pinned comment does not post.

Scope: the four owner-locked Shorts in `shorts-net-new/STANDALONE-SCRIPTS-V3.json` (script sha256
`6be1ee7c...cf6c`), with editorial titles from `shorts-net-new/private-phone-preview/manifest.json`.
Claims are limited to `shorts-net-new/CLAIM-CLEARANCE-V1.md`. The editorial titles are script
labels, not platform titles (V3 approval boundary), so platform titles are proposed below.

Standard: `docs/content-rubric.md` (owner ruling 2026-09-21: cold-viewer context plus one narrow
payoff resolved inside each Short; the episode link adds distinct depth only). Register:
Operator Economy documentary. No hashtags, by decision (same as the EP009 package: no OE
packaging document supports them, and the kill list blocks hashtag walls). No questions as
titles. No figures in titles.

## Related Video (all four)

Set **Related Video = the EP007 long-form**, resolved from `links.json` at schedule time, never
typed by hand. It is additive routing only: every Short resolves its own answer before any link.
If the long-form is not live when a Short is scheduled, leave Related Video empty and backfill it
the day the episode goes live (flow.md failure mode 3: EP002's Shorts pointed nowhere).

Suggested order: 02, 01, 04, 03. 02 orients a cold viewer to what the service is. 01 hands them the
first tool. 04 tests the channel. 03 carries the legal boundary and benefits most from the other
three having set up what "preparation" means.

## AI disclosure (all four)

- **Altered or synthetic content: YES** on every Short (same rule as the long-form).
- What is synthetic: the narration is an **AI voice clone of the host's own voice** (owner
  confirmed "clone", 2026-09-23; the proposed chain in `shorts-net-new/NARRATION-CAPTURE-PROPOSAL-V1.md`
  transfers a Google TTS performance onto Manav's accepted voice through ElevenLabs Voice Changer),
  and the presenter footage is AI-generated. All four Shorts were narrated through this chain; the owner confirmed on 2026-09-23 that the
  Original C voice is the same clone of his voice ("yes same clone").
- Add this as the last line of each Short's description, below the episode line:

```
The narration is an AI voice clone of the host's own voice, and the presenter footage is AI-generated.
```

- When the API upload path is used, set `containsSyntheticMedia: true`.

---

## Short 01: The Thirty-Day Map

**Title:** Map what a business can't do without its owner (47 chars)

**Description:**

```
A service can help an owner get a business ready to sell years before any buyer shows up. The first tool is a dependency map.

Ask whether the business could run for thirty days without the owner, and have the owner explain how. Circle every answer that turns into "I call," "I approve," or "I know." Beside each one, write who else could act, what they would need, and what stops if nobody can.

That map is a working diagnostic, not a prediction about a sale or a valuation. Thirty days is a test setting, not a proven threshold.

Full episode, with the rest of the practice and the arithmetic: {{EPISODE_URL}}
```

**Pinned comment:**

```
{{EPISODE_URL}}

The full episode takes the map further: the three shapes an owner dependency usually takes (customer relationships, revenue concentration, records a stranger can't verify), what the engagement delivers after the map, and a modeled look at whether one person can make this pay. The model's base case does not clear its own target, and the episode says so.
```

---

## Short 02: An Operations Business Wearing a Suit

**Title:** Getting a business ready to sell is operations work (51 chars)

**Description:**

```
Helping an owner get a business ready to sell sounds like M&A. The work before a deal is closer to operations.

A buyer needs to know whether customers get served, decisions get made, and records can be found when the owner steps away. An experienced operator can trace those dependencies and write down how the business actually runs. AI can organize interview material and draft procedures. It can't decide which gap a buyer will question.

Valuation, finding a buyer, and negotiation stay outside this kind of engagement.

Full episode: {{EPISODE_URL}}
```

**Pinned comment:**

```
{{EPISODE_URL}}

In the full episode: why this job exists at all (everyone around a small-business sale is paid when it closes), three places where similar readiness work is already paid for, and why none of them reaches the small owner-run business, and why the time with the owner is the part no tool shortens.
```

---

## Short 03: How You Charge Changes the Job

**Title:** How you charge for sale prep changes the job (44 chars)

**Description:**

```
If you help owners prepare a business for sale, how you charge changes what job you're doing.

A fee tied to the sale can trigger brokerage rules, depending on where you operate. One bounded model is a fixed fee for defined preparation work: map owner dependencies, organize records, document operations, deliver a readiness plan. That fee does not depend on whether a sale closes.

Fixed-fee wording does not settle every legal question. It gives you a clear scope to take to local counsel.

This is not legal advice. Verify the rules in your jurisdiction.

Full episode: {{EPISODE_URL}}
```

**Pinned comment:**

```
{{EPISODE_URL}}

The full episode covers what that pricing constraint does to the rest of the business: why the thing you deliver is a signed checklist rather than a sale, and what the numbers look like when the fee can't scale with the deal. The episode names no state and gives no legal ruling. Check yours with counsel.
```

Legal copy boundary (claim clearance, Short 03): never add a state name, a licence count, a map,
"compliant," "licence-free," or "fixed fee = safe" to the title, description, comment, or cover.

---

## Short 04: Test the Front Door

**Title:** Why a broker may be your first sale-prep conversation (53 chars)

**Description:**

```
If you want to build a service that gets businesses ready to sell, your first useful conversation may be with a broker, not an owner.

Ask one question: what happens to a business you can't list because it isn't ready? If they already do that work for free, the referral channel may be closed. If they turn it away or send it elsewhere, ask what was missing and who handles it now.

A referral shows access, not demand. Only an owner agreeing to pay starts to prove the business.

Full episode: {{EPISODE_URL}}
```

**Pinned comment:**

```
{{EPISODE_URL}}

The full episode names the two things that would end this business before it starts: owners who agree with every word and still defer, and brokers who already do the work for free. It also runs the modeled arithmetic on what one person would need to charge.
```

---

## Checks run on this file

- `shorts_contract.validate_payload(..., mode="derived", require_pinned_comment=True)` on a
  scratch `shorts_briefs` payload built from these four records plus the locked V3 hook, closing
  line, and standalone payoff: see `PACKAGE-NOTES.md` for the result.
- Every pinned comment opens on `{{EPISODE_URL}}` on its own line and adds depth the Short does
  not need. None supplies the Short's answer.
- No em dash, emoji, exclamation mark, hashtag, hype term, income promise, or question title.
- Short 01 treats "thirty days" as a test setting (claim clearance production boundary).
- Short 04 keeps every broker outcome conditional ("may be," "if").
