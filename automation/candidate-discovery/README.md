# Operator Economy candidate discovery pool

Status: noncanonical upstream discovery surface.

This folder records live questions, market changes, buyer problems, emerging capabilities, and
possible operator-business ideas before formal Operator Blueprint V2 Step 0 intake.

Nothing here is a Step 0 candidate, score, eligibility decision, promotion, episode, script, or
narration authorization. Canonical intake begins only when the Monday research bench deliberately
admits one shortlisted lead into `operator-blueprint-v2/00-intake/01-candidates/` using the current
candidate template.

## Files

- `POOL.md` is the current discovery pool and shortlist.
- `runs/YYYY-MM-DD.md` records the complete evidence and disposition from each scout run.
- A same-date rerun appends a numbered section; it never replaces an earlier observation.

## Lead states

| State | Meaning |
|---|---|
| `new` | A sourced signal worth screening, but not yet qualified for the Monday bench. |
| `shortlisted` | Passed every scout filter, including the delivery-boundary and willingness-to-pay tests, and may be considered for formal Step 0 admission. |
| `held` | Plausible, but blocked on a named missing signal, source, access, or timing condition. |
| `rejected` | Generic, duplicate, evidence-free, guest-dependent, non-showable, outside the thesis, or otherwise not worth reopening without a stated material change. |
| `admitted` | The Monday bench created a formal Step 0 candidate and recorded its ID. The scout may not set this state. |

The pool carries no numeric score. Ordering is editorial priority, with a short reason, not a
substitute Step 0 rubric.

## Lead contract

Every lead must preserve:

- stable discovery ID;
- first-seen and last-checked dates in America/New_York;
- exact question, tension, or observed change;
- source URLs and observation dates;
- signal type: conversation, search direction, buyer behavior, spend, adoption, operating change,
  regulation, capability, workflow, or other named type;
- who appears to care and what they are trying to decide or accomplish;
- buyer, costly problem, possible offer, observable outcome, and delivery-mechanism hypothesis;
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
- **automated or productised substitute** and its published price, when one exists;
- **willingness-to-pay signal** for the residual named in the delivery boundary, recorded with its
  type and source, or an explicit statement that none was found;
- expiry or recheck date;
- status, disposition reason, and exact reopening condition when held or rejected; and
- Step 0 candidate ID only after a later Monday-bench admission.

Google Trends supplies relative direction and related-query evidence, not exact monthly volume.
Reddit and other community activity supplies qualitative language and recurrence evidence, not
proof of demand, willingness to pay, or market size. A source-access failure is an evidence limit,
not a negative market finding.

## The two tests added 2026-09-21

Owner decision, 2026-09-21, after four consecutive leads and two Step 0 candidates failed on the same
axis: a regulation-triggered service whose delivery boundary requires a licensed professional, whose
pricing evidence is seller copy, and for which no buyer-paid evidence exists.

**Delivery boundary.** A rule that creates work usually also names who is allowed to do it. Name that
person. If a licence or credential is required for any part of the core deliverable, state in one
specific sentence what remains for an unlicensed operator once every regulated task is removed. That
residual is the offer. If it cannot be stated, the lead is `held` with "delivery boundary unresolved",
not `shortlisted`. If the residual is substantially what an automated substitute already outputs,
hold or reject.

**Willingness to pay.** At least one signal that the target buyer pays an independent provider for
the residual. Accepted: a buyer describing a payment with identifiable scope; a service request,
brief, or job posting carrying a budget; a disclosed engagement, invoice, contract, or first-party
result; an observed marketplace transaction; or an incumbent visibly charging a named buyer for that
specific residual. Not accepted in any combination: vendor or agency pricing pages, directory rate
cards, cost-explainer content marketing, seller guidance published to win adjacent work, loss or
fraud statistics, category size, funding, a deadline, or the volume of coverage a change attracts.

Holding is the expected outcome for a fresh regulatory trigger. A held lead costs nothing; a
shortlisted one consumes a Monday bench run.

The full test wording, including the transition rule for leads shortlisted before 2026-09-21, is in
`../prompts/oe-candidate-scout.md` under "Qualification and disposition".

## Capacity and handoff

- Keep no more than five `shortlisted` leads at once. Five is a ceiling, not a target: under the two
  tests above, an empty or one-lead shortlist is a normal result, and neither test may be relaxed to
  fill the pool.
- Add no more than three materially new leads per scout run.
- Continue or refresh existing leads before expanding the pool.
- Do not keep a lead live merely because it is fashionable. Expire, hold, or reject stale signals.
- Only the Monday research bench may admit one shortlisted lead into formal Step 0.

## Prohibited actions

The scout never:

- creates or edits Step 0 candidate, research, validation, scorecard, disposition, promotion, or
  canonical queue artifacts;
- assigns a readiness score or claims eligibility;
- promotes, numbers, scripts, narrates, produces, publishes, or distributes anything;
- infers owner experience or approval;
- treats public conversation as proof of commercial demand; or
- fills an inaccessible source with a weaker claim presented as equivalent evidence.
