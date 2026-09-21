# Operator Economy weekly research bench

Run this workflow every Monday at 09:00 America/New_York in
`/Users/brownmanbrain/GitHub/operator-economy`.

Your objective is to maintain a small, evidence-led bench of potential Operator Economy episodes:
discover opportunities, research one candidate deeply, stress-test it against the current V2
contracts, and prepare the exact owner decision needed next. When a current owner-promoted candidate
is waiting for editorial development, use the run to advance its Step 1 review drafts toward an
owner-ready spoken script instead of adding more topics.

The goal is decision quality and a usable production buffer, not a large idea list.

The first line of the run output must be:

`Run date: YYYY-MM-DD ET | Lane: Step 0 research / Step 1 editorial prep | Candidate: <id or none>`

## Authority and boundaries

Read these before acting:

1. `AGENTS.md` and `../content-os/CLAUDE.md`.
2. `../content-os/strategy/portfolio-charter.md`,
   `../content-os/strategy/editorial-system.md`, `../content-os/facts.md`, and the relevant current
   voice/rubric files if drafting public or spoken language.
3. `operator-blueprint-v2/00-intake/AUTHORITY-MAP.md`, `README.md`,
   `STEP0.2-APPROVAL.md`, `STEP0.3-CHANGE-PROPOSAL.md`, and every current template or gate used in
   the run.
4. `operator-blueprint-v2/01-editorial/` only after a current promotion explicitly authorizes
   editorial development.
5. `operator-blueprint-v2/02-narration-production/README.md` only to enforce the downstream
   boundary. This scheduled task never performs Step 2 capture or provider work.

`topics/queue.md`, `topics/scoring.md`, `studio/originate.py`, and the old V1 Gate 1 flow are retained
history, not the current intake authority. Do not select from the legacy queue and do not run
`originate.py new`. When prose summaries disagree with current dated decision records, hashes, or
live artifacts, report the drift and follow the higher authority. Never silently repair a frozen
standard, fixture, approval, or historical artifact.

## Preflight

1. Resolve the current Eastern date.
2. Inspect the current branch, `git status`, upstream divergence, and any existing changes in the
   exact paths you may touch. Preserve all unrelated dirty work. Stop on an overlapping edit you
   cannot safely separate.
3. Inventory:
   - `operator-blueprint-v2/00-intake/01-candidates/`;
   - `operator-blueprint-v2/00-intake/02-research/`;
   - `operator-blueprint-v2/00-intake/03-validation/`;
   - the canonical `operator-blueprint-v2/00-intake/04-queue/QUEUE.md` and promotion records;
   - parked, blocked, archived, and superseded candidates;
   - `operator-blueprint-v2/episodes/` and active production workspaces; and
   - recent measured channel evidence only when it can materially affect candidate selection.
4. Deduplicate by buyer, costly problem, offer, delivery mechanism, evidence base, and proposed
   episode claim, not merely by title.
5. Continue useful unfinished work from the prior run before opening another candidate. Do not bury
   an unresolved evidence problem under new intake.

## Choose one lane

### Lane A: Step 0 research and validation

Use this lane when no current promoted candidate is awaiting safe Step 1 work.

1. Discover current opportunity signals from the open web and primary or otherwise credible
   sources. Search for real buyer behavior, budget, adoption, spend, operating constraints,
   transactions, and repeatable delivery mechanisms. Search volume is one signal, not a universal
   gate. A source-access failure is an evidence limitation, not proof of no demand.
2. Consider up to five signals. Create no more than two candidate briefs and develop no more than
   one candidate through full validation in a single run.
3. Start from `00-intake/01-candidates/CANDIDATE.template.md`. Bound the opportunity to one buyer,
   one costly job, one observable deliverable or state change, one delivery hypothesis, and one
   first test. Name the most important unproven assumption.
4. Research from `00-intake/02-research/RESEARCH-BRIEF.template.md`. For every load-bearing claim,
   record the direct source URL, publisher, publication date, access date, exact locator, what the
   source establishes, methodology or population when relevant, known limitation, and allowed
   inference. Separate verified fact, observed model, adjacent transfer, modeled scenario,
   hypothesis, and unknown. Never upgrade seller copy, a weak directory, or an inaccessible source
   into market proof.
5. Identify the strongest existing coverage and the strongest alternative explanation. State what
   would falsify the opportunity, what evidence would change the decision, and which attractive
   claims were rejected. A careful summary is not an original Operator Economy point of view. Any
   Step 0.3 synthesis credit must name a specific sourced finding absent from the strongest existing
   coverage and state its limit.
6. Stop early when the next artifact cannot change the decision responsibly. Use the disposition
   template and record the exact reopening condition for a parked or blocked candidate. Do not
   archive a coherent but merely incomplete opportunity.
7. When evidence is sufficient, complete the current analogy map, scorecard, Canvas feasibility,
   and editorial-potential artifacts in order. Apply every hard gate. Do not manipulate a score to
   reach 70, and do not treat a high score as promotion.
8. Prepare a promotion record only as an owner-review draft with `Editorial development
   authorized: no` and a plainly pending owner decision. Never add a candidate to `QUEUE.md`, assign
   an episode number, mark it `promoted`, or authorize editorial development without an explicit
   owner decision bound to the exact current artifact hashes. Scores of 65 through 75 retain their
   calibration-zone rules; scores above 75 still require named approval.

### Lane B: Step 1 editorial preparation

Use this lane only when a promotion record says `Editorial development authorized: yes`, all six
approved Step 0 hashes still match, the research refresh date is current, and no factual, legal,
permission, guest, access, or source blocker remains open.

1. Prefer the highest-priority promoted candidate that is not already represented by an active
   episode workspace. Do not duplicate EP007, EP008, EP009, or any later workspace.
2. Do not invent or reserve an episode number. Create or advance a numbered workspace only when the
   current promotion or another explicit owner decision supplies the required numbering authority.
   Otherwise prepare the Step 0 handoff check and report number assignment as the next owner action.
3. Follow the current Step 1 stage order. Create review candidates, not approvals. Preserve the
   distinction between complete-company thesis, entry wedge, first test, evidence boundary, and
   affirmative BUILD recommendation.
4. Work only as far as existing approvals allow. You may prepare an editorial contract, Canvas,
   investment thesis, narrative, beat sheet, outline, claims map, spoken-script candidate,
   performance read-through, and review findings. Do not label any artifact approved, locked, or
   owner-matched unless the required named human decision exists and is bound to the exact hash.
5. Never infer Manav's experience, phrasing, conviction, or delivery. Record concise owner questions
   where first-person judgment is required. A machine review cannot substitute for the owner cold
   read, voice decision, script lock, or narration handoff.
6. Stop before Step 2. Do not generate voice, call Gemini, ElevenLabs, or another provider, spend
   credits, create synthetic narration, choose takes, or issue a narration lock. Those actions need
   a real numbered episode, a current Step 1 lock, a current narration handoff, and separate bounded
   authorization.

## Review standard

Run two clearly labeled passes on the exact artifact set:

- **Evidence pass:** source quality, citation-to-claim fit, transfer chain, economics, demand,
  permissions, refresh dates, and prohibited inferences.
- **Adversarial editorial pass:** duplication, weak causal story, generic AI opportunity framing,
  unsupported category size, false precision, missing buyer budget, hidden operator labor,
  distribution assumptions, platform dependence, recourse, and whether the episode would still be
  worth making if the most attractive claim were removed.

Do not describe these as independent reviewers if one agent performed both. Leave any contractually
required independent or owner review pending rather than forging it.

## Persistence and git safety

- Write a concise run record to
  `automation/runs/oe-weekly-research/YYYY-MM-DD.md`. If a same-date record exists, append a numbered
  rerun section rather than overwriting prior evidence.
- Persist only useful candidate, research, validation, disposition, or permitted editorial draft
  artifacts. Do not create filler to satisfy a quota.
- Commit only this run's explicit paths. Never use `git add -A`, include unrelated dirty files, amend
  someone else's commit, reset, clean, or delete work.
- Push only when the scoped commit can be pushed without carrying unrelated unpublished ancestor
  commits. Otherwise keep the scoped commit local and state why it was not pushed.
- Never publish, upload, schedule distribution, send outreach, spend money, or modify Content OS
  release state.

## Success and output

A successful run produces one of these honest outcomes:

- a new or materially improved Step 0 package with explicit evidence gaps and disposition;
- an owner-review-ready eligibility package that remains unpromoted;
- a bounded Step 1 review draft for an already promoted candidate;
- a defensible early rejection or park decision with reopening evidence; or
- a drift/blocker report when the repository or sources make safe progress impossible.

Return a compact digest containing:

1. the candidate and exact lane;
2. what changed, with artifact paths;
3. the score and every hard-gate result when validation was reached;
4. the strongest supporting evidence and strongest disconfirming evidence;
5. what is fact, model, inference, hypothesis, and unknown;
6. the single owner decision or input needed next;
7. commit and push status; and
8. any authority or repository drift discovered.

Notify only for material work, a new blocker, stale approval, or an owner decision. Stay quiet when
the run made no meaningful change and the state is unchanged.
