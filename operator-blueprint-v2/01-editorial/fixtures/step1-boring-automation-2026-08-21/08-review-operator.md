# Operator review: workflow-reliability script v0.1

Status: completed against immutable `07-script-v0.1.md`

Verdict: revise

## Findings

### WFR-OP-01 — Diagnostic must decide whether implementation is sold

Severity: high

The draft says “the sprint includes” implementation before establishing that discovery may reject the workflow. Separate the paid diagnostic from the implementation decision. The operator should earn the right to propose the build only after rules, access, consequence, exceptions, and baseline pass.

### WFR-OP-02 — Buyer acceptance criteria need one concrete measure

Severity: medium

The draft lists several possible outcomes. For the modeled onboarding thread, choose one primary acceptance measure—such as time from signed proposal to acknowledged kickoff ownership—while retaining failure counts as guardrails.

### WFR-OP-03 — Client ownership boundary is strong

Severity: positive

Client-controlled accounts, least privilege, access inventory, and clean handoff make the service more credible. Preserve these details.

### WFR-OP-04 — Maintenance separation passes

Severity: positive

The script does not smuggle a retainer back into the base model. Preserve the incident-and-response test.
