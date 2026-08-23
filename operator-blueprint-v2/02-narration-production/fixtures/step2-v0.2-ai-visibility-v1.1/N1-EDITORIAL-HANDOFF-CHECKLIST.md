# N1 editorial handoff checklist: AI Visibility v1.1 fixture

Status: **N1 PASS** for the AI Visibility v1.1 fixture.

Review date: 2026-08-23

Episode: none; unassigned fixture

Step 1 authority commit: `27c90fd628fe3972fea556c1d9ed189f1b657867`

Manifest: `package-manifest.json`

## Required artifact verification

| Artifact | Source ID | Expected SHA-256 | Observed SHA-256 | Result |
| --- | --- | --- | --- | --- |
| Editorial lock 133 | `editorial-lock` | `d968d4dae9c2621f2d86a2ec4d860212d1ac5046cd016a6034ca0d2419f22501` | `d968d4dae9c2621f2d86a2ec4d860212d1ac5046cd016a6034ca0d2419f22501` | pass |
| Narration handoff 134 | `narration-handoff` | `e4091d5f7604018367bf865b133c9012a0ce107c53f01052b3a72e7b7ee74da0` | `e4091d5f7604018367bf865b133c9012a0ce107c53f01052b3a72e7b7ee74da0` | pass |
| Locked script 122 | `locked-script` | `74048b55ed15ed6ed679abb5a6c892def8a8a40e75e7cebeafdfde319dd67efa` | `74048b55ed15ed6ed679abb5a6c892def8a8a40e75e7cebeafdfde319dd67efa` | pass |
| Investment Thesis 117 | `investment-thesis` | `ca3fb01512563d41c22361f7ad4f422da61ccbf8732be551f98118a791a870fb` | `ca3fb01512563d41c22361f7ad4f422da61ccbf8732be551f98118a791a870fb` | pass |
| Beat sheet 119 | `episode-beat-sheet` | `2a03556fac55c83bc2ae25f5352c5b3f298c6b3d66e2ecdcf9d70f542141f0c7` | `2a03556fac55c83bc2ae25f5352c5b3f298c6b3d66e2ecdcf9d70f542141f0c7` | pass |
| Positive hosted-voice conformity 126 | `editorial-voice-conformity` | `656dc965cfc52dd70e710b4a1c133a950fedb38d17dae160d45cb28413399509` | `656dc965cfc52dd70e710b4a1c133a950fedb38d17dae160d45cb28413399509` | pass |
| Operator Canvas 129 | `operator-canvas` | `84f23af68a9eb42d7356b58630d0756a249ac590ca6db192ef366ba0f28b5639` | `84f23af68a9eb42d7356b58630d0756a249ac590ca6db192ef366ba0f28b5639` | pass |
| Claims map 116 | `claims-map` | `a35db8c138d8955a52657e8a8b65a1df63cb52ca69b11d4b0461ad127cb596df` | `a35db8c138d8955a52657e8a8b65a1df63cb52ca69b11d4b0461ad127cb596df` | pass |
| Narrative spine 118 | `narrative-spine` | `9cccd7f54371ad236f66bf8d0e3f4e9e65861e326ca234e6d422b100831d88cc` | `9cccd7f54371ad236f66bf8d0e3f4e9e65861e326ca234e6d422b100831d88cc` | pass |
| Outline 120 | `episode-outline` | `b0223f58e23008478694a3e5e15caf2d2be7a7ce3ecd30b5e89c8b1b6db8f1a2` | `b0223f58e23008478694a3e5e15caf2d2be7a7ce3ecd30b5e89c8b1b6db8f1a2` | pass |
| Voice map 121 | `voice-and-comedy-map` | `a8036227a56512e2ad60870a3a53be099cefea33a7073a9bf285f0f72ecd4393` | `a8036227a56512e2ad60870a3a53be099cefea33a7073a9bf285f0f72ecd4393` | pass |
| Performance read-through 123 | `performance-readthrough` | `544deaeb4324c116fcb5bb7b89e636908d460d63de2bbfd9121155e324979aa6` | `544deaeb4324c116fcb5bb7b89e636908d460d63de2bbfd9121155e324979aa6` | pass |
| Live Content OS voice | `content-os-voice` | `ec65d503a9973ec77919ca8edf37d37f18e6762c696d931690a86b179017574a` | `ec65d503a9973ec77919ca8edf37d37f18e6762c696d931690a86b179017574a` | pass |
| Script Beat Research | `script-beat-research` | `e67c480e6aae4f3638ab388bd17b67b2aa768d3ae4e9f59f985f2eea17f4f9fe` | `e67c480e6aae4f3638ab388bd17b67b2aa768d3ae4e9f59f985f2eea17f4f9fe` | pass |
| Voice Architecture | `voice-architecture` | `ce9b0af23221ff5d9266460a279c0a6fd6f53874e39c2f5831ceeb22a3569474` | `ce9b0af23221ff5d9266460a279c0a6fd6f53874e39c2f5831ceeb22a3569474` | pass |
| Studio speech profile | `studio-speech-profile` | `75913da0bc5d5b360c88f18c70b60d8d4af14128184e8164872edd56f71ceddc` | `75913da0bc5d5b360c88f18c70b60d8d4af14128184e8164872edd56f71ceddc` | pass |

The script's older header says it was a candidate. The later, hash-specific fixture lock 133 controls its current fixture status; the source file was not rewritten after approval.

## Spoken-text identity

- Required comparison contract: `oe-spoken-text-v1`
- Expected narration blocks: 12; `S01` is excluded because it contains no narration.
- Expected spoken-token count: 3,019
- Expected ordered-token SHA-256: `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`
- Read-through must resolve to the same identity: yes
- Canonical CLI-generated `identity/canonical-w.txt`: pass; SHA-256 `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`
- Canonical CLI-generated `identity/spoken-identity.json`: pass; SHA-256 `d6e40df20bb70365790179cb48434a8b89993d85de72dc7eb497f5ee36848beb`
- Independent extraction runs: two; byte-identical canonical W and identity receipts
- Package manifest: 16 sources verified; SHA-256 `8d628064647c829094146ad1c7f653436ad5e7ec29ca7adb03e1a4014c451fa0`
- Manual word-count substitution allowed: no

## Rights and boundaries

- Narrator path: existing authorized OE synthetic self-voice
- Third-party imitation: no
- Provider call authorized by this handoff: no
- Unresolved public-facts blocker: yes, intentionally; fixture cannot be public production
- Unresolved fixture editorial blocker: no
- Episode number: none
- Step 3 authority: none

## Decision

Source and boundary preflight: **PASS**.

Formal Gate N1: **PASS FOR FIXTURE TESTING**.

Next gate: N2 owner review of `PERFORMANCE-DIRECTION.md`. N1 does not authorize a provider call,
audio generation, production use, or Step 3.

If the manifest verifier or extractor reports any mismatch, N1 fails closed. Step 2 does not repair the script or reinterpret the locked word identity.
