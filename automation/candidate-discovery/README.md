# Operator Economy candidate discovery pool

Status: noncanonical upstream discovery surface.

This folder records buyer problems that one person may now solve with AI (including always-on
agents) well enough to build a sustainable business, before formal Operator Blueprint V2 Step 0
intake. Leads start from what buyers say and do, never from sellers, tools, or trends. Industry size
does not matter; whether one operator can serve many buyers for a share of the value does (owner
decision 2026-10-13).

Nothing here is a Step 0 candidate, score, eligibility decision, promotion, episode, script, or
narration authorization. Canonical intake begins only when the Monday research bench deliberately
admits one shortlisted lead into `operator-blueprint-v2/00-intake/01-candidates/` using the current
candidate template.

## Files

- `POOL.md` is the current discovery pool and shortlist.
- `runs/YYYY-MM-DD.md` records the buyer observation ledger, evidence, and disposition from each
  scout run (Wednesday and Sunday).
- A same-date rerun appends a numbered section; it never replaces an earlier observation.

## Lead states

| State | Meaning |
|---|---|
| `new` | A sourced signal worth screening, but not yet qualified for the Monday bench. |
| `shortlisted` | Passed the five scout tests (real buyer and problem, one person with AI, delivery boundary, substitutes, showable fit) and may be considered for formal Step 0 admission. |
| `held` | Plausible, but blocked on a named missing signal, source, access, or timing condition. |
| `rejected` | Generic, duplicate, evidence-free, guest-dependent, non-showable, outside the thesis, or otherwise not worth reopening without a stated material change. |
| `admitted` | The Monday bench created a formal Step 0 candidate and recorded its ID. The scout may not set this state. |

The pool carries no numeric score. Ordering is editorial priority, with a short reason, not a
substitute Step 0 rubric.

## Lead contract

Every lead must preserve:

- stable discovery ID;
- first-seen and last-checked dates in America/New_York;
- **origin observation**: the buyer-side observation (posting, brief, question, complaint, review,
  comment, or rising search) that generated the lead, with source and date;
- exact question, tension, or observed change;
- source URLs and observation dates;
- signal type: conversation, search direction, buyer behavior, spend, adoption, operating change,
  regulation, capability, workflow, or other named type;
- who appears to care and what they are trying to decide or accomplish;
- buyer, costly problem, possible offer, observable outcome, and delivery-mechanism hypothesis;
- what AI and agents do, what the one operator does, and what the job looked like before AI;
- **unit economics sketch** (modeled scenario): value at stake per buyer, a plausible fee as a share
  of value or a fixed fee, roughly how many buyers one person could serve, and whether that sustains
  one person;
- why now;
- strongest existing answer or coverage and what it appears to miss;
- possible Operator Economy point of view;
- strongest invalidating question;
- evidence still needed;
- semantic deduplication result against candidates, episodes, parked work, archives, research, and
  production workspaces;
- **delivery boundary** — who is legally or professionally permitted to deliver the core deliverable,
  and, if any part requires a licence or credential, what concretely remains for an unlicensed
  operator once every regulated task is removed;
- **substitutes** (self-serve tools, done-for-you services, firms, the buyer's own staff) with
  published prices, and what the operator provides that the buyer does not get from them;
- **problem-value signals**, each typed (`residual`, `old-way spend`, `problem cost`,
  `adjacent spend`, or `demand signal`) and sourced;
- **payment evidence:** `found` (type and source) or `unknown — viewer's first test`;
- for an `old-way spend` signal, the **switching question**: why this buyer would move that spend to
  an outside operator rather than to software or its own staff using software;
- expiry or recheck date;
- status, disposition reason, and exact reopening condition when held or rejected; and
- Step 0 candidate ID only after a later research-bench admission.

Google Trends supplies relative direction and related-query evidence, not exact monthly volume.
Reddit and other community activity supplies qualitative language and recurrence evidence, not
proof of demand, willingness to pay, or market size. A source-access failure is an evidence limit,
not a negative market finding.

## The five tests (rewritten 2026-10-13)

Owner decision 2026-10-13 (`../../operator-blueprint-v2/00-intake/OWNER-DECISION-2026-10-13-DISCOVERY-RESET.md`)
replaced the nine-test stack after 21 runs produced no episode. Full wording is in
`../prompts/oe-candidate-scout.md` under "Qualification: five tests".

1. **Real buyer, real problem.** Two independent buyer-side observations, or one plus a dated
   operating change; at least one typed problem-value signal. Payment evidence is recorded as
   `found` or `unknown — viewer's first test` and is not required (owner decision 2026-09-28).
2. **One person with AI.** AI and agents are what let one operator deliver to many buyers, with a
   unit economics sketch that could sustain one person.
3. **Delivery boundary.** Who may legally deliver the core work, and the unlicensed residual.
4. **Substitutes.** A tool sold to buyers is evidence the problem is real, not a reason to reject.
   Reject only when a done-for-you service already delivers the outcome at a price one operator
   cannot beat and buyers readily use it, or buyer-side evidence shows buyers run the tool themselves.
5. **Showable and fit.** Thesis fit, showable without a guest, not hype or duplicate.

Seller pages, vendor pricing, cost explainers, category size, funding, and deadlines are context
only, never buyer evidence.

## Capacity and handoff

- Keep no more than ten `shortlisted` leads at once (raised from five 2026-10-13). Ten is a ceiling,
  not a target, and no test
  may be relaxed to fill the pool.
- Add no more than three materially new leads per scout run.
- Continue or refresh existing leads before expanding the pool.
- Do not keep a lead live merely because it is fashionable. Expire, hold, or reject stale signals.
- Only the research bench (Monday and Thursday) may admit one shortlisted lead into formal Step 0,
  or the owner may admit a held lead directly (owner decision 2026-09-28).

## Prohibited actions

The scout never:

- creates or edits Step 0 candidate, research, validation, scorecard, disposition, promotion, or
  canonical queue artifacts;
- assigns a readiness score or claims eligibility;
- promotes, numbers, scripts, narrates, produces, publishes, or distributes anything;
- infers owner experience or approval;
- treats public conversation as proof of commercial demand; or
- fills an inaccessible source with a weaker claim presented as equivalent evidence.
