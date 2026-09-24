# R14 review — opening graphic bridge

Preview: http://localhost:3002/#project/r14-opening-bridge?v=1&t=0&tab=design&rc=0

Only the opening annotation is new: “25 years.” appears over the avatar at2.5s and holds fixed across the4.041667 workshop cut. “Profitable.” joins at6.375s. Both clear at7.666667, one frame before the first owner close-up. The original narration, current avatar/lip-sync, all film source selections, crops, later illustration, question, logo and title remain unchanged. Runtime56.5s at24fps.

Verification:

- `node verify-r14.mjs` passes. All13 picture declarations and both audio declarations match R13. All19 public assets and five existing subcompositions are byte-identical. R13 index remains pinned and untouched.
- Independent QA packet: `blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/ep007-r14-overlay-qa-20260909/deliverable.json`. Passes the same static regression checks; makes no listening/phoneme-perfect claim.
- `npx hyperframes@0.8.33 check --strict --at 0,2.4,2.8,4,4.083333,6.2,6.8,7.5,7.666667,7.75,9,12,16,19,24,29,31.75,34.8,38,42,48,54.8 --json` passes with zero lint, runtime, layout or contrast findings. Three sampled contrast checks passed. Motion-sidecar assertions are not enabled.
- Ten snapshot frames inspected across the opening and all existing mounted compositions: text reads clearly on both avatar and workshop, leaves faces clear, and disappears before the close-up; question/sketch/logo/title still mount. The7.708333 screenshot rounds just below the cut, so7.75 is used for post-cut runtime validation.
- Initial lint caught missing subcomposition font declarations; explicit local font declarations added before the passing check. Existing local type rendered correctly in the first snapshot pass via the parent declarations.
- Local server responds HTTP200. HyperFrames0.8.33 retained; skill update reports current. Local catalog word search surfaced caption/flash/drift templates, not the scoped fixed editorial label; no template or external feedback used.

Boundary Ledger determined the paper/mineral type treatment and brief reveal/settle behavior. No decorative sketch, count-up, ambient movement or sound was added. No paid generation, new audio, timing shift, lip-sync repair, full encoded export, publication or production-gate change. Pending post-title avatar is outside this review.
