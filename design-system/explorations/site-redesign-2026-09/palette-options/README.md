# OE palette options

Status: **locked visual direction** inside an isolated design exploration. No production authority
and no token changes. See [LOCK.md](./LOCK.md) for the frozen invariants and change boundary.

Locked direction: **Boundary Ledger**. Signal Ledger remains as a historical alternate reference.

Current homepage iteration: the original [B4 homepage](../artboards/B4-homepage.html), recolored
at runtime, with its existing latest-sheet card attached to a full-width episode working model.
The illustration is a deliberately rough hotel–OTA–guest sketch: the first stay passes through
the intermediary and the oxide second-stay path returns directly to the hotel. The card and
illustration are added only to Boundary Ledger; the source artboard remains unchanged.

Prior clean layout study: [boundary-ledger-clean.html](./boundary-ledger-clean.html). This keeps
the Boundary Ledger palette, removes blueprint notation from the page typography, and presents
the Episode and Operator Canvas as separate editorial surfaces. The Canvas pairing is
design-specimen copy, not publication approval.

The prior clean study includes an isolated photographic **Working Plate** built from an approved
key-handoff still. It remains a historical comparison, not the current illustration direction or
a production brand lock.

This lab applies two palette directions to the existing September site-redesign
artboards at runtime:

- **Boundary Ledger** — Rev C paper with deep mineral, core oxide, and perimeter steel.
- **Signal Ledger** — Rev C paper and navy with Datum-derived teal and orange-red signals.

The underlying homepage, Canvas, and PDF artboards remain untouched. The lab injects
temporary CSS custom-property overrides into same-origin iframes.

## Review

From the repository root:

```bash
python3 -m http.server 8899
```

Then open:

```text
http://localhost:8899/design-system/explorations/site-redesign-2026-09/palette-options/
```

Use **Compare** for a simultaneous responsive view and **Focus** for a larger,
interactive rendering of one direction. Surface, palette, view, and device selections
are preserved in the URL.
