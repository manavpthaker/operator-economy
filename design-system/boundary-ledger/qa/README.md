# Boundary Ledger QA

The package is reviewed as a reference system, not as evidence that the production site migrated.

Required viewport checks: `1280`, `933`, `390`, `373`, and `320` CSS pixels.

At every width verify:

- `document.documentElement.scrollWidth === document.documentElement.clientWidth` without overflow masking;
- the working-model image reports `1536 × 1024`, remains 3:2, and uses `object-fit: contain`;
- the complete hotel–OTA–guest relationship and oxide return path remain visible;
- the feature docket attaches by 16px and covers only the drawing's quiet top edge;
- mobile keeps 24px content gutters, an inset docket, and full-bleed working paper;
- keyboard targets are at least 44 CSS pixels in their relevant logical dimension;
- oxide focus is visible on paper and bright oxide focus is visible on mineral;
- source order remains coherent without layout CSS;
- reduced-motion mode removes smooth scrolling and animated transitions.

[`contrast.json`](./contrast.json) records the tested text and focus color pairs. Recalculate it when
any foreground or background token changes.

[`responsive-harness.html`](./responsive-harness.html) loads the real field manual in fixed-width,
same-origin frames. It exists for inspection only and is not a public page pattern.

[`verification-2026-09-02.json`](./verification-2026-09-02.json) records the browser measurements
for the locked 1.0.0 reference. Re-run the checks after any token, component, or asset change.
