# Step 3 fixtures

Test-only. These cannot create an episode workspace, approve visuals, or authorize Step 4.

- `ACCEPTANCE-SET.md` — the behavioural controls and what they prove
- `validate.py` — mechanical gate checks; clears hygiene only
- `positive/` — clean baseline that must pass with no findings
- `adversarial/` — nine controls, each of which must fail exactly one target gate

Run:

```bash
for d in positive/* adversarial/*; do python3 validate.py "$d"; done
```
