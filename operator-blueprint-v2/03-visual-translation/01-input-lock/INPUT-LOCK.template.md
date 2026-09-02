# Visual translation input lock: [episode]

Gate: **V1 — input lock**

Template version: proposed Step 3 v0.2

Episode: EP###

Verified: YYYY-MM-DD

Verified by: [name]

## Step 1 editorial lock

| Artifact | Path | SHA-256 | Matches disk |
|---|---|---|---|
| Editorial lock | | | yes / no |
| Operator Canvas | | | yes / no |
| Episode Investment Thesis | | | yes / no |
| Narrative spine | | | yes / no |
| Episode beat sheet | | | yes / no |
| Claims map | | | yes / no |
| Script | | | yes / no |

- `Gate E6: PASSED` present in the editorial lock: yes / no
- Locked `W` identity reproduces its recorded token count and SHA-256: yes / no
- `W` token count: [count]

## Step 2 narration lock

| Artifact | Path | SHA-256 | Matches disk |
|---|---|---|---|
| Narration lock (N7) | | | yes / no |
| Narration master | | | yes / no |
| Word-level transcript | | | yes / no |
| Intentional-pause map | | | yes / no |

- `technical_pass` recorded, naming this master hash: yes / no
- `creative_approved` recorded, naming the same master hash: yes / no
- Transcript and pause map bound to that exact master hash and duration: yes / no
- Narration duration: [seconds]

**Step 3 does not proceed on a partial narration lock.** Both decisions must exist against the same hash.

## Boundary Ledger semantic lock

Step 3 selects from these files; it does not copy their roles or operations into a local vocabulary.

| Authority | Path | Version/status | SHA-256 | Matches disk |
|---|---|---|---|---|
| Semantic core | `design-system/boundary-ledger/semantic-core.json` | | | yes / no |
| Motion binding | `design-system/boundary-ledger/bindings/motion.json` | | | yes / no |

- Semantic core identifies `Boundary Ledger`: yes / no
- Core and binding declare the same system version: yes / no
- Every operation referenced by the motion binding exists in the core: yes / no
- Motion binding status recorded without upgrading its implementation evidence: yes / no

Any hash change invalidates this lock until compatibility is reviewed and the full Step 3 acceptance
set passes. An unchanged operation ID is not assumed semantically unchanged.

## Open change requests

- Against Step 1: none / [list]
- Against Step 2: none / [list]
- Boundary Ledger compatibility blocker: none / [describe]

## Gate V1 decision

Result: pass / fail

Editorial or narration failure returns the package upstream. Boundary Ledger drift blocks Step 3
until compatibility is reviewed. Step 3 repairs neither.

Approved by: [name]
