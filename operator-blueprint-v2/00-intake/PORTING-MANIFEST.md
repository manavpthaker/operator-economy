# Step 0 porting manifest

Created: 2026-08-21

Port type: frozen V1 references copied into the parallel Operator Blueprint V2 scaffold.

The files below were copied verbatim. Their matching source and destination hashes prove provenance; they do not make historical claims current or canonical.

## Copied references

| Source | V2 destination | SHA-256 | Classification |
|---|---|---|---|
| `topics/scoring.md` | `00-intake/03-validation/references/topic-scoring-v4.md` | `d47f8e2ecc850cfcf0254b6373f1ee4f40e51e4de47effda7317324b6a074f8f` | V1 validation reference |
| `topics/queue.md` | `00-intake/05-archive/topic-operations/topic-queue-v4-snapshot.md` | `5bccce359b2c9cb48ebe09d029e024aa90af9d566f97a445987ab220e4428658` | V1 queue snapshot |
| `topics/intake-2026-08-14.md` | `00-intake/05-archive/topic-operations/intake-2026-08-14.md` | `10f82335032b86c1a8a1c81db4efcca7be98245837823c63a034bc2c5941f28e` | V1 intake record |
| `topics/parked.md` | `00-intake/05-archive/topic-operations/parked-v1.md` | `879209d7eff4dd02621ed68b61849824b75e642679f69b46984356db81b18816` | V1 parked snapshot |
| `topics/archive/2026-08-queue-v3.md` | `00-intake/05-archive/topic-operations/topic-queue-v3-retired.md` | `92a2d275855a8ee191dfada942d075cd1f609d101a3aa2187f92090d892b22d2` | Retired V1 queue |
| `research/deep-research-prompt.md` | `00-intake/02-research/references/opportunity/channel-opportunity-deep-research-v1.md` | `6f1efc3d0816a3e30888091b01859a71ceca4958fbbdea8e93ae11c4d3aa37de` | Historical opportunity prompt |
| `research/strategy/01-opportunity-report.md` | `00-intake/02-research/references/opportunity/opportunity-report-v1.md` | `b9e01b2e58299ed73967bdae2596fa898273f33724a76227a01df3c08e07f897` | Historical opportunity report |
| `research/strategy/02-lanes-and-pipeline-memo.md` | `00-intake/02-research/references/opportunity/lanes-and-pipeline-memo-v1.md` | `1ced4c147a54c022d300b383041bae1d0b3a93fd2378f667ffce0d0f747f36d9` | Historical strategy memo |
| `research/synthesis.md` | `00-intake/02-research/references/opportunity/opportunity-synthesis-v1.md` | `7be6f0fd629a326415580ae44987fba445f0af7549fe227931ba6adf29ea6425` | Historical opportunity synthesis |
| `research/reports/report-1-strategic-evaluation.md` | `00-intake/02-research/references/opportunity/foundational-report-1-strategic-evaluation.md` | `d21acffd020a1084f85a1b58e431b692621c72282444ef2930eaff144e796cc0` | Foundational opportunity research |
| `research/reports/report-2-portfolio-research.md` | `00-intake/02-research/references/opportunity/foundational-report-2-portfolio-research.md` | `76b820ef14b0b27b105907586165fca9fc607cce2384fa8c3910299da87012b4` | Foundational opportunity research |
| `research/reports/report-3-strategy-analysis.md` | `00-intake/02-research/references/opportunity/foundational-report-3-strategy-analysis.md` | `3e94c304d14d359d08ffc238867c50313210925042adda49df83fdf7a14b82d8` | Foundational opportunity research |
| `research/competitor-research-prompt.md` | `00-intake/02-research/references/competition/competitor-research-prompt-v1.md` | `06ffc0356d1f88d46ddd23a913fb682e7657f3cbf084c92cb3746db156c34bd2` | Historical competition prompt |
| `research/comp-synthesis.md` | `00-intake/02-research/references/competition/competitive-synthesis-v1.md` | `39d18c3afca4df6b06df8ffa81871f8582bee0b0aa3cc34f980c414f18138a62` | Historical competition synthesis |
| `research/reports/comp-report-1-claude.md` | `00-intake/02-research/references/competition/competitive-report-1-claude.md` | `35e51f35faa5e9604a596ec8ce4d745324b07efcd761590a380ad5568dac16f7` | Competitive reference report |
| `research/reports/comp-report-2-chatgpt.md` | `00-intake/02-research/references/competition/competitive-report-2-chatgpt.md` | `4b6cce9893460a4e5e97bddda258a45ab7f97f3718c6646e1613b25c61334fc7` | Competitive reference report |
| `research/reports/comp-report-3-gemini.md` | `00-intake/02-research/references/competition/competitive-report-3-gemini.md` | `89acff8805448ce3f4a34d3a2e4d1482a8800f6de9f59f129a981f6d1acd051e` | Competitive reference report |
| `docs/growth-strategy.md` | `00-intake/02-research/references/constraints/growth-strategy-v1.md` | `f67a7084941d70b5bd3de59f9dd181e6702f711efa61f1c82b13e0c605de9cce` | Historical discovery constraint |
| `docs/kill-criteria.md` | `00-intake/02-research/references/constraints/kill-criteria-v1.md` | `55f76a4c43f710ed28c82589488616db0911f990436e5a91bf659974b517b7ff` | Historical channel constraint |

## Referenced, not copied

| Source | SHA-256 | Treatment |
|---|---|---|
| `research/reports/comp-report-4.pdf` | `b6cf0b55322afcec551ae414bc926074bd4a4946c45a9d6152b2e74bbc314c73` | Retained in V1 and indexed by `02-research/references/competition/BINARY-REFERENCES.md`. |
| `../content-os/facts.md`, `voice.md`, `rubric.md`, `flow.md`, and `bin/doctor.sh` | Not duplicated | Remain external authorities listed in `AUTHORITY-MAP.md`. |

## Deliberately excluded from Step 0

- Episode-specific research briefs and interview notes.
- Script generation, script evaluation, narration, and voice processing.
- Craft, thumbnail, storyboard, visual-plan, media, and render research.
- Automation and production-toolchain research.
- Blueprint Cinema, HyperFrames, Remotion, and Resolve production artifacts.
- Generated media, screenshots, and other binaries.

These exclusions are routing decisions, not deletion decisions. The original files remain available in V1 for later stage-specific review.
