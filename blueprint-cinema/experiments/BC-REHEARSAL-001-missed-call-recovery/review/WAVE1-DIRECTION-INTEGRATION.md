# Wave 1 direction integration · BC-REHEARSAL-001

Status: review integrated for bounded animatic build; no creative approval claimed.

## Packets received

| Work order | Packet status | Authority | Root disposition |
|---|---|---|---|
| `wave1-art-motion-critic` | Complete; 5 blocking, 5 major, 2 minor findings | Critique only | Accepted as review evidence. No worker gate/state claim. |
| `wave1-evidence-continuity-critic` | Complete; 4 blocking, 5 major, 3 minor findings | Critique only | Accepted as review evidence. No worker gate/state claim. |

Both packets verified the exact issued input hashes and wrote only their isolated deliverable files. Their `approval_claimed` and `production_state_changed` fields are `false`.

## Integrated blocking corrections

1. **Persistent identity:** the integrated references show one brick `CALL-R01 / 20:47` tag. `UNCERTAIN` and `REVIEWED` are subordinate state tabs. The work-order card shows stable ID `WO-R01` and uses one state chain: `EMPTY → OFFERED → SCHEDULED → MEASURED`.
2. **Human gate:** the integrated Shot 04 board represents the unresolved HOLD phase only. The card is `EMPTY`; there is no pre-release offer on the far side of the barrier. Scene direction still requires release before offer.
3. **Fixture warning and pin:** the exact `SYNTHETIC TEST FIXTURE — NOT EVIDENCE` line remains on one right-edge source pin from Shot 03 onward.
4. **Outcome disclosure:** the work-order card itself carries `AST-OUTCOME-004 · SYNTHETIC WORK ORDER — NOT EVIDENCE`. A detached ticket slate cannot qualify the synthetic scheduled state.
5. **Branch causality:** Shot 05 uses one connected fork. The decline branch terminates at STOP; the one real tag occupies only the demonstrated accepted branch and docks to the existing card.
6. **Shot 05 state conflict:** `visual-plan.json` now says the card remains `OFFERED` during the decline demonstration, matching its business state before the accepted path changes it to `SCHEDULED`.
7. **Shot 07 permanence and hold:** the tag stays docked to the card; CALL is a measurement label/tick, not a duplicate tag. The card stamps `MEASURED` at 58.680, allowing a final 1.14-second settled hold after the bracket closes at 60.270.
8. **Composition grammar:** the integrated boards remove headline-plus-box sequences, equal workflow cards, detached outcome explanations, and a framed overview map. Captions and timing notes sit outside the image. Each frame shows one physical cause/consequence relationship.

## Superseded review references

The original `style-frames/*.png` and `shot-board/static-shot-board.png` remain untouched because they are the hash-pinned evidence the independent critics reviewed. They are rejected review inputs, not implementation authority.

The integrated build references are:

- `style-frames/01-reality-v2.png`
- `style-frames/02-system-proof-v2.png`
- `style-frames/03-gate-outcome-v2.png`
- `shot-board/approved-direction-board.png`
- `shot-board/approved-direction-board.html`

## Residual risks carried into implementation QA

- The proof frame must keep the full warning readable at phone size without letting the source sheet become a second focal point.
- The human placeholder must behave as physical contact, not a floating UI panel.
- The Shot 06 pullback must reveal causal context once and settle; it must not become a map tour.
- The card/tag dock must not cover the `SCHEDULED` or `MEASURED` state text.
- Static references cannot prove DOM identity, event timing, or screen-space continuity; those remain machine/render review obligations.

Root integration result: **accepted for bounded implementation with residual checks; creative approval remains human and unclaimed.**
