# Step 3 v0.3 process approval

Decision: **approve**

Artifact and SHA-256: `PROCESS-MANIFEST.json`
`4f830d71d677efa8915429dfe35628012289c28ac988cb74f77261331519690c`

The manifest pins every covered file. Verified against the working tree on 2026-09-24:

| Covered | Hash |
|---|---|
| `SCOPE-BOUNDARY.md` | `255ac7810bb8f5736309a1c851b319db3bc0f6f25af5c77c1b2fa36eff7d4ee5` |
| `VISUAL-TRANSLATION-STANDARD.md` | `4a44366a223940f98ea8d02d40581597770c9f9eaf402ff19c3072f5ad09078d` |
| `STAGE-GATES.md` | `3c2d564a271acfe130f87ef8769c8a3adf99ab11f9a62404ccc0f7d73449d1ce` |
| `AUTHORITY-MAP.md` | `0cb648224f7cb93a39cc091e7702b5b04d1fc4f4b28fd051b66ce8873ce95333` |
| `PORTING-MANIFEST.md` | `247ac31fd1e07a631a9801b9e2b5b587b719c8fad124a021fa522db386afdfbc` |
| 8 templates (`01-input-lock/` to `07-approval/`) | as listed in `PROCESS-MANIFEST.json`; all match |
| `fixtures/validate.py` | `fc1721583c49975991a4c69f09a572ffbee83d0107a16c1d794a3d6d02396470` |
| Fixture tree (299 files, `FIXTURE-TREE.json`) | `ea50a923f1ac9afff790aaafb862eec05f92911852daa511af0fcac15d0c83cb`; all 299 per-file hashes match the index |
| Boundary Ledger `semantic-core.json` | `30a316f79bc94e017705de0823a0af5b85747a20938eb0a2723d39a1a298978e` |
| Boundary Ledger `bindings/motion.json` | `b2ca3e3295ef2f1dd676732b6b9c7bdefbcfbf55ff642cdf1ab90dc9c84fb450` (status `provisional`) |

Acceptance run on 2026-09-24: 54 of 54 controls pass (10 legacy v0.1, 44 v0.3), matching
`fixtures/ACCEPTANCE-EVIDENCE.md`.

Process or gate version: Step 3 v0.3, gates V1 to V7.

Scope of this decision: I approve Step 3 v0.3 as the governing visual-translation process, against
the hashes recorded in this approval. This approves the process only. It does not by itself approve
an episode, authorize Step 4, or approve publication. This re-grants the authority returned on
2026-09-02.

Pre-authority episode reviews: **none activated by this record.** The V1 to V3 records under
`episodes/EP007-*/03-visual-translation*/`, `episodes/EP008-*/03-visual-translation/` and
`episodes/EP009-*/03-visual-translation/` were written while the process was proposed. Each becomes
a gate pass only through its own later decision naming its exact artifact hash.

Known limitations accepted:

- V4 to V7 have never run on a real episode.
- Direction-bible and rhythm-map prose stay human-audited.
- Look development is provisional by rule.
- No runtime is chosen. The Boundary Ledger motion binding is `provisional` in its own record.
- The fixture tree hash could not be recomputed from `FIXTURE-TREE.json` because the combining
  method is not written down. The 299 per-file hashes it indexes all match. The tree hash in the
  header of `ACCEPTANCE-EVIDENCE.md` (`3b1face3…`) differs from the manifest's; that file is run
  output and is excluded from the manifest.
- Proposed v0.4 (`../03-visual-translation-v0.4/`) builds on this exact base and needs its own
  approval.

What this does not authorize: Step 4, a runtime, any episode's visuals, v0.4, or Steps 4 to 8.

Approved by: Manav Thaker

Approved on: 2026-09-24
