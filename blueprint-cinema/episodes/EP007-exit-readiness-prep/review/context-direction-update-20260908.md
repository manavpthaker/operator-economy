# Context-sensitive film direction — implementation verification

2026-09-08. User authorized proceeding with the context-sensitive skill update. This records system
maintenance, not an episode creative approval, media review, or production-state advance.

## Implemented

- OE film direction now reads the scene and adjacent beats before selecting form, coverage,
  performance, camera and cut/hold behavior. No fixed setup count or cut interval is imposed.
- Scene-direction schema 1.2.0 requires authored sequence `scene_context` and shot
  `editorial_intent`. The compiler preserves both; it supplies adjacent narration to directors.
- Explicit `narrated_dramatization` permits motivated interaction under narration. Its disclosure
  plan and actual-audio comprehension check are required; no character dialogue or exact sync is
  inferred. Observation, source, dialogue and presenter safeguards remain distinct.
- A one-layer film plate is valid; decoration is not required to satisfy a layer count.
- Direction templates, Blueprint Cinema rules, and Boundary Ledger's film-language references agree.
  The OE skill-file lock and its Boundary Ledger manifest hash were recomputed from actual bytes.
- Prior 1.1.0 direction requires deliberate reauthoring; no old packet was silently upgraded.

## Verification

| Check | Result |
|---|---|
| Skill-creator quick validation, using offline cached PyYAML environment | Passed |
| OE production-skill lock | Passed: 7 local files, 4 declared sources; upstream source bytes not reverified |
| Boundary Ledger validator | Passed: 6 roles, 8 operations; semantic core unchanged |
| Targeted scene/compiler tests after final fix | 55 passed |
| Full Blueprint Cinema test suite after final fix | 93 passed, 1 unrelated source-pin failure |
| Four independent behavioral cases | Different justified plans for conversation, neutral process, evidence, and avatar/arrival opening |
| Three closed work orders and deliverable contracts | Validated; historical review pins retained |

Boundary Ledger retains its existing warnings: audio-first encoded output is unverified and the
flattened illustration does not prove a motion-ready Working Model. Its motion/sound bindings and
consumer migration status were not promoted.

The full-suite failure is `test_current_world_structural_and_semantic_validity`: EP006's
`evidence-operator-history` pins Content OS facts at
`fd337d4013d5d2d8ed83f1ba02e9e211c1263c5e3e8d5f119ff1bc5c7e5a4309`, while the current file hashes to
`d1b67dd431b36dcf201b8c42053c663ef47c6c34e5bde272daedb9eabcc9a201`.
Neither that evidence lock nor Content OS facts was changed in this task.

## Independent review and resolved finding

- [Behavioral test](../agents/deliverables/ep007-film-skill-forward-test-20260908/report.md)
  used frozen skill inputs. Its production-doc conflict describes the read-time state before root
  alignment, not the final integrated state.
- [Integration review](../agents/deliverables/ep007-context-direction-integration-review-20260908/report.md)
  verified 52 pre-fix cases and identified an unguarded malformed `dramatization_context` value.
  Root subsequently added a type guard and null/list/string regression cases. All 55 targeted
  cases pass. The independent report remains a truthful pre-fix record; it is not rewritten as
  post-fix approval.

## Preserved boundaries

R7, Kling footage, narration, avatar takes, and the rough Working Model were not edited or generated.
No paid calls, renders, publication, commits, or episode approval changes occurred. The proposed
Step 3 v0.4 package remains unapproved and unmigrated; this task does not promote it. The broader
HyperFrames/Resolve production-state migration is still outside the implemented bounded contract.

## Final source fingerprints

```json
[
  {
    "path": ".agents/skills/oe-film-direction/SKILL.md",
    "sha256": "0877dfb4945906048907d904214b8aadbd01f2c4b31ceced31f3155e190d0f43"
  },
  {
    "path": ".agents/skills/oe-film-direction/references/context-and-coverage.md",
    "sha256": "bae45db93a7fa4eaf784c81066b1a6cd106fd1bf3a2caf761bbbc2f9320be0fd"
  },
  {
    "path": ".agents/oe-skills-lock.json",
    "sha256": "4008ad19f24442841e6aafd2e2bf9469d0bdf4810798cd4b902b8eff910ddf7e"
  },
  {
    "path": "blueprint-cinema/schemas/scene-directions.schema.json",
    "sha256": "d64648087ba95d346301165a27ff2a0f5ae3516716ae6e624ec0aa839192961d"
  },
  {
    "path": "blueprint-cinema/src/blueprint_cinema/validation.py",
    "sha256": "f962080f8e6567235b521d699c85a3b9043276d0aa6a636f446f4d86626e0c28"
  },
  {
    "path": "blueprint-cinema/src/blueprint_cinema/scene_prompts.py",
    "sha256": "f1bb89de919fcc274d1e49e955b63dac9cd9fab906aeac4664d805e8e64002e2"
  },
  {
    "path": "blueprint-cinema/tests/test_context_direction.py",
    "sha256": "69287c4540c3a19fa975947c0a4043e0ee0d1c5e8c06d94b12641d84df99a8b2"
  },
  {
    "path": "design-system/boundary-ledger/semantic-core.json",
    "sha256": "30a316f79bc94e017705de0823a0af5b85747a20938eb0a2723d39a1a298978e"
  }
]
```
