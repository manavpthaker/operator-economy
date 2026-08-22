# Claims review: unsupported mutation package

Status: completed against deterministic derived script

Base claims-map SHA-256: `141cd559c10624d44b2f457df9c733e1b1ca15d8d8a2c111294c5b1f1a079c1c`

Derived script SHA-256: `f28dd3afcd291eadb5cd435d27c8ce7957edd2642981fad4414be20ae32a9a66`

Verdict: fail

## Findings

### E5-CL-01 — Unsupported annual-cost magnitude

Severity: blocker

Exact claim: “Across small agencies, broken onboarding quietly costs more than one hundred thousand dollars a year.”

Problem: The approved package contains no small-agency loss study, annual-cost model, affected population, baseline, or equation. The German administrative-burden source is broader, geographically different, and explicitly prohibited from proving recoverable workflow cost.

Disposition required: Remove, or request a bounded Step 0 amendment for the exact population, cost definition, and evidence.

### E5-CL-02 — Unsupported prevalence, willingness to pay, and minimum price

Severity: blocker

Exact claim: “Most small agencies will pay at least three thousand dollars for a reliable handoff.”

Problem: Partner programs and vendor cases establish that a service category and procurement paths exist. They do not establish representative agency demand, majority prevalence, willingness to pay, or a $3,000 minimum price.

Disposition required: Remove, or request a bounded Step 0 amendment for representative buyer evidence and the exact price proposition.

### E5-CL-03 — Modeled scenario upgraded to market truth

Severity: blocker

Exact claim: “A three-thousand-dollar sprint is a conservative market price, and two new sprints per month is a realistic starting pace.”

Problem: C009 classifies $3,000, two sprints, delivery hours, and contribution as modeled test assumptions. “Conservative market price” and “realistic starting pace” convert them into typical market and acquisition claims. No approved evidence supports that upgrade.

Disposition required: Restore the modeled-scenario wording, or return to Step 0 for price and acquisition evidence.

## Why softer tone would not fix the claims

The following revisions would still require evidence:

- “Broken onboarding can cost agencies up to $100,000.”
- “Many agencies may pay around $3,000.”
- “A relatively conservative price is $3,000.”
- “Two monthly clients should be achievable.”

Words such as `can`, `may`, `many`, `around`, `conservative`, `reasonable`, and `achievable` alter certainty. They do not create provenance.

## Isolation result

Existing base-script claims outside M01-M03: unchanged and within the frozen dry-run claims map

New approved claim IDs: zero

Step 0 amendment required if mutations are retained: yes

E5 pass possible while any mutation remains: no
