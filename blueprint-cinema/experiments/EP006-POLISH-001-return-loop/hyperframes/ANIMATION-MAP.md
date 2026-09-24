# Animation map

Runtime: HyperFrames `0.8.5`, local GSAP `3.14.2`, 1920×1080 at 30 fps. All timelines are paused, explicit, deterministic, and seek-safe. Root duration is `30.405s`.

Registry searches were run before authoring for object match cuts, gate-dependent route drawing, and stop/human-approval decisions. `match-cut` and `svg-stroke-trace` were installed for source inspection. Their useful mechanics—single-frame matched geometry and measured SVG dash drawing—were adapted to the OE direction. Their generic gradients, glow, drift, bounce, UI styling, and remote GSAP dependency were not used.

## Root

| Clip | Start | Duration | Track | Role |
|---|---:|---:|---:|---|
| `scene-01-return` | `0.000` | `4.375` | 0 | reality handoff |
| `scene-02-permission` | `4.375` | `7.865` | 0 | permission and memory |
| `scene-03-judgment` | `12.240` | `8.100` | 0 | qualification, suppression, judgment |
| `scene-04-direct-return` | `20.340` | `4.763` | 0 | useful OTA plus direct return |
| `scene-05-outcome` | `25.103` | `5.302` | 0 | separate proof composition |
| locked VO | `0.000` | `30.405` | 10 | exact narration slice |

## Scene 1 — Return

- Plate reframe: `x 0→-14`, `scale 1.008→1.016`, `0.000–4.375`, linear.
- `FIRST STAY / OTA` enters at word 1784 (`2.700s` relative root).
- Gold rule draws at word 1785 (`3.080s`).
- Key-tag contour uses a measured `710` dash length, drawing at word 1786 (`3.592–4.092s`).
- At word 1787 (`4.104s`) the contour completes a restrained 10px catch into the exact exit geometry.

## Scene 2 — Permission

- The vector key tag begins at the same `x976 y515 w270 h126` geometry as Scene 1’s contour.
- At word 1788 (`0.015s` local) it advances only 30px and physically stops at the closed gate.
- The historical OTA underline draws at word 1790 (`0.505s` local); OTA context then dims but remains.
- The request status appears at word 1791 (`1.758s` local); downstream stays absent.
- At word 1796 (`3.949s` local) the bolt slides/rotates once over `0.360s` and a sage resolved mark appears only after completion.
- At word 1800 (`4.958s` local) the tag crosses the open gate, compressing to `32%` and moving upward.
- At word 1801 (`6.209s` local) the `STAY CONTEXT` object appears and the same tag rests as its brass pin.

## Scene 3 — Judgment

- Phase A: relevance route and token move only at word 1812 (`2.337s` local).
- Phase B hard cut at word 1815 (`3.096s` local): sensitive token accelerates into a brick-red stop and holds.
- Phase C hard cut at word 1816 (`4.100s` local): operator plate. At word 1818 (`4.910s` local) the tag overlay follows the physical placement. At word 1819 (`5.453s` local), the review rule resolves over `0.280s`; `HUMAN REVIEW` changes to resolved at `5.733s`.
- Phase D hard cut at word 1821 (`5.869s` local): only now does the direct route dash draw and the eligible key tag travel. The outgoing label follows the completed route.

## Scene 4 — Direct return

- OTA route is present from entry as historical acquisition.
- At word 1825 (`0.500s` local), OTA route and label dim to 62%; they are never red, crossed out, or removed.
- At word 1834 (`2.808s` local), the direct route draws over `0.920s` and the persistent key tag moves along it.
- `NEXT APPROPRIATE STAY / DIRECT` lands after the route exists.

## Scene 5 — Outcome

- Hard cut to Paper proof bench.
- At word 1839 (`0.950s` local), the hotel-owned return line draws and the tag travels onto it.
- At word 1843 (`2.357s` local), the faint repeat-acquisition loop retracts; the original OTA introduction remains recorded.
- At word 1846 (`3.319s` local), the explicitly warned outcome fixture appears.
- Final causal frame holds `3.319–5.302s` local (`1.983s`) without new motion.

## Motion prohibitions enforced

No CSS keyframes, runtime randomness, ambient looping, particle system, bounce, elastic spring, opacity-only object replacement, camera flyover, Prezi pan, whole-network reveal, gradient, glow, or render-time network fetch exists in the authored six render files.
