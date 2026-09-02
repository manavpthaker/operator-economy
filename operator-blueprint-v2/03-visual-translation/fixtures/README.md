# Step 3 fixtures

Test-only. These cannot create an episode workspace, approve visuals, or authorize Step 4.

- `ACCEPTANCE-SET.md` — the behavioural controls and what they prove
- `validate.py` — mechanical gate checks; clears hygiene only
- `positive/` — preserved v0.1 baseline plus the v0.2 Boundary Ledger derivation baseline
- `adversarial/` — twenty-two controls, each of which must fail exactly one target gate

The v0.2 baseline resolves the live, hash-pinned Boundary Ledger semantic core and motion binding.
Its thirteen adversarial cases use `case.json` patches over `positive/boundary-ledger-derived`. This
leaves the original v0.1 controls unchanged and makes actual Boundary Ledger drift fail the
integration set. Current validation fails closed on any contract other than v0.2; preserved v0.1
evidence is available only through the explicit `--legacy` flag.

Run:

```bash
python3 validate.py --legacy positive/clean-baseline
for d in adversarial/a[1-9]-*; do python3 validate.py --legacy "$d"; done

python3 validate.py positive/boundary-ledger-derived
for d in adversarial/a1[0-9]-* adversarial/a2[0-2]-*; do python3 validate.py "$d"; done
```
