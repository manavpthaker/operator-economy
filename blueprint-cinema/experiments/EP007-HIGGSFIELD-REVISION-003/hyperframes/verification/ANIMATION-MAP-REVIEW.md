# Animation-map review

The local helper completed for the assembled 59.8666667-second revision at 1280 × 720, 30 fps, with four samples per tween. It mapped 42 of 50 entries and skipped eight micro-tweens. Raw output: `../.hyperframes/anim-map/animation-map.json`.

The report contains 13 `degenerate`, 13 `offscreen`, 28 `collision` and one `paced-fast` flags. These require interpretation; this is not a clean automated motion pass.

- The helper reports child-local and rebased entries together. For example, `#question-business` appears at local 0–0.30 and twice at record 35.08–35.38; `#presenter-title` appears at local 7.52–7.82 and twice at record 56.04–56.34. The duplicated record entries generate collision flags for the same element.
- Local-time samples address children while their enclosing record window is hidden. The lone `paced-fast` flag is the hidden local `#question-title` exit at 9.42–9.62. The map's element census also reports video elements by their own opacity without resolving all ancestor visibility; the actual scene wrappers determine which footage is visible.
- GSAP dead zones include long filmed shots and intentional holds. They do not establish frozen video playback. Media decode, actual snapshots, Studio playback and the encoded pixels are the relevant additional checks.

The unchanged question HTML and its complete model assets were verified byte-identical to experiment 002. The 15-point final HyperFrames check with selected avatar 205 passed with no lint, runtime, layout or contrast findings; its motion sidecar was disabled. Scene snapshots provide separate mount/layout evidence. No animation was altered to suppress these diagnostic flags. Independent Studio and exported-pixel review remain separate from this map interpretation and from owner acceptance of the performance.
