# EP006 engine review

Status: validated and hash-approved only when `production-state.json` records the matching hash.

- Engine: `73b22204a8a19a9a71d420d6aef69218f717cdab804486175f2929922d4af543`
- Mechanic: relationship leak and recovery loop
- Operator: The owner or general manager of a ten-to-forty-room independent hotel who is accountable for demand, guest experience, consent, exceptions, and repeat revenue without a dedicated revenue-management team.
- Input customer: A guest who completed an OTA-acquired stay at the property; completion of that stay alone does not imply permission to contact them, qualification for outreach, or a reason to return.
- Qualified subset: The appropriate, permissioned subset of prior guests who later has a relevant reason to return, is not suppressed or sensitive, and passes a human-reviewed qualification decision.
- Outcome: A visible direct booking confirmation for a known, permissioned returning guest, connected to the prior stay and separately measurable by the hotel without presenting it as guaranteed attribution.

## Honesty test

The machine never treats all prior guests as return prospects and never frames the OTA as a villain. It preserves the useful first booking, exposes the operator-side settlement consequence, makes disqualification and exceptions visible, and represents success only as an appropriate direct return confirmed by the property.

## Guardrails and risks

- The first OTA booking remains useful acquisition; only a later appropriate booking is a recovery opportunity.
- A completed OTA-acquired stay is the input, not an assumption that the guest already wants to return.
- The direct booking destination is audited and repaired before any guest outreach activates.
- Permission is requested explicitly and never replaced by the shorthand capture.
- Qualification, suppression, human review, and sensitive-case exceptions remain visible stages.
- The physical key tag becomes guest memory only after the consent handoff.
- An operator settlement statement or commission ledger shows economic consequence; the guest confirmation does not.
- A direct booking confirmation is the visible outcome, not a guaranteed attribution or income promise.
- Evidence enters as a sourced parameter attached to what it supports, never as decorative or synthetic proof.
- No stock guest, generated person, platform reconstruction, or prior visual assignment is represented as a factual case.
