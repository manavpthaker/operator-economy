# EP006 engine honesty critique

## Packet identity

- Work order: `engine-honesty-critique`
- Required gate observed: `inputs_locked`
- Input lock SHA-256: `e99b847c5b5a767d74ad4208738374ac191da3d9d4c3e3654098a6c08e725691`
- Episode engine SHA-256: `e07ed63476684bc3e3a2757e1e30c651322859a9f27b4f25bc7a08d15ddc4b36`
- External sources, writes, paid services, and synthetic generation: none

## Verdict

The proposed engine is mechanically honest and suitable to continue through the orchestrator's approval decision. It preserves the OTA's useful first-booking job, does not treat a completed stay as permission or return intent, begins the counter-system with direct-path audit and repair, and separates an operator-side economic proof object from the guest-facing outcome object.

This packet does not approve the engine or advance production state. Two implementation-boundary risks below should become explicit world-validator and plan-review conditions. They do not negate the engine's current honesty because its authored descriptions and guardrails already state the correct ordering.

## Mechanical trace

1. **Useful acquisition remains intact.** The constraint says the OTA can provide useful discovery and a trustworthy first checkout. The visual mechanic keeps OTA discovery and the first stay in both the before and after systems. Nothing requires displacement of the first booking.
2. **A completed stay is not eligibility.** `input_customer` is a guest who completed an OTA-acquired stay, and its description explicitly rejects inferred permission, outreach qualification, and return intent. `eligible_return_customer` is a later, narrower, permissioned and qualified subset with a relevant reason to return.
3. **Audit and repair precede outreach.** The counter-system begins with audit and repair of the direct destination. The visual mechanic and guardrails preserve that dependency before permissioned follow-up or return activation.
4. **Consent precedes memory.** The physical key tag represents the stay only. The counter-system creates guest memory only after consent, and the motif repeats that the tag resolves into a permissioned memory record at the consent handoff. The engine does not use `capture` as a substitute for permission.
5. **Qualification, suppression, and judgment are visible.** The eligible-customer definition requires a human-reviewed qualification decision. The counter-system and motion verbs include qualification, suppression, review, approval, escalation, follow-up, retry, and measurement. Sensitive cases are expressly excluded or escalated.
6. **The outcome is bounded.** Success is one visible direct booking confirmation for a known, permissioned returning guest. The engine says the hotel can measure it without claiming every return was caused by the service, so the confirmation is not presented as guaranteed attribution or an income promise.
7. **Economic proof is separate.** The motif and guardrails reserve an operator-side settlement statement or commission ledger for the commission consequence. The direct booking confirmation remains a different object with a different job: showing the return outcome.
8. **Evidence is not decorative.** A guardrail requires sourced parameters to remain attached to what they support and prohibits decorative or synthetic proof. Generated platform interfaces, text, logos, and evidence are also forbidden.

## Acceptance-check matrix

| Check | Result | Evidence in the engine |
|---|---|---|
| First OTA booking remains useful | Pass | `constraint`, `visual_mechanic.behavior`, `visual_mechanic.after`, guardrail 1 |
| Completed stay does not imply eligibility | Pass | `input_customer`, `eligible_return_customer`, guardrail 2 |
| Audit and repair occur before outreach | Pass | `counter_system`, `visual_mechanic.behavior`, guardrail 3 |
| Permission is explicit and not shorthand capture | Pass | `counter_system`, `motion_verbs`, motif, guardrails 4 and 6 |
| Qualification and suppression are visible | Pass | `eligible_return_customer`, `counter_system`, `motion_verbs`, guardrail 5 |
| Human judgment and exceptions are visible | Pass, with boundary condition | `eligible_return_customer`, `counter_system`, `motion_verbs`; every outbound path still needs a mandatory human gate in `world.json` |
| Settlement proof is separate from confirmation | Pass | `outcome_object`, motif, forbidden list, guardrails 7 and 8 |
| Evidence integrity is protected | Pass at engine level | guardrails 9 and 10 plus generated-interface/evidence prohibitions; actual source pins remain a world/evidence review job |
| Visual cliché is actively constrained | Pass, with residual risk | specific recurring people, physical handoffs, lens/camera rules, tactile motif, and forbidden list |

## Risks and required downstream conditions

### 1. Consent-result states are more precise than the motion vocabulary

`request_permission` is present, and the prose correctly says memory is created only after consent. The motion vocabulary does not separately name granted, declined, expired, or revoked consent. A visual plan could therefore accidentally depict a request as if it were permission.

Required condition: the persistent world must model a distinct affirmative-consent state plus declined, revoked or expired exits. A permission request must never activate guest memory, qualification, outreach, or retries by itself. `retry` must not reopen a suppressed, declined, revoked, or sensitive case.

### 2. Human review must not become selectively bypassable

The eligible-customer definition requires a human-reviewed qualification decision, but the counter-system phrase "sends judgment-dependent work through human review" could be read as allowing other outbound cases to bypass review.

Required condition: every outbound follow-up path in the world must traverse the human judgment and exception gate after consent, qualification, and suppression checks. Automation may prepare or route work; it must not silently make the final sensitive-case or outreach decision.

### 3. Evidence integrity cannot be proven from an engine alone

The engine has the correct proof rules, but it does not and should not invent evidence IDs. The later world and visual plan must attach settlement or commission parameters to hash-pinned claim/source records, label illustrative values as illustrative, and keep a missing evidence item as a conspicuous ticket rather than a plausible stand-in.

### 4. The inn world still has boutique-ad drift risk

Morning light, courtyard or breakfast details, wood, linen, and green are specific enough to orient the world but can still become generic boutique-hotel lifestyle imagery. The key-tag transformation can also become a familiar magical data-morph if treated decoratively.

Required condition: use the recurring operator and guest only for concrete handoffs and decisions; keep placeholders conspicuous; preserve the physical key tag until affirmative consent; and render the consent transition as a legible state handoff, not a decorative transformation. Do not let beauty footage replace the direct-path audit, suppression, failure, settlement, or human-review mechanics.

## Approval recommendation

The engine's authored logic passes this honesty review. The orchestrator may consider it for approval without treating this packet as approval. Before world approval, validation must prove the two non-bypass rules: affirmative consent before memory or outreach, and human judgment on every outbound path. Evidence pins and asset tickets must then prove that economic claims and reality/proof material remain sourced rather than simulated.

## Worker boundary

No canonical episode JSON, production state, approval record, runtime, schema, renderer entry point, or documentation file was changed. This report is an isolated critique packet only.
