# Operator Economy — Evidence Base No. 01

**Canonical thesis source.** `report-source.md` is the editable original; `build_pdf.py` renders it.

Content OS evidence records cite this directory. Four records in the signed-desk issue
(`E-OE-EVIDENCE-EXEC-001`, `-FORMATION-001`, `-CONTROL-001`, `-FALSIFIERS-001`) resolve here by
commit reference, so **this directory must stay committed** — before 2026-08-28 it existed only in
a working tree, on no remote, and a `git clean -fd` would have destroyed the issue's evidence base.

## The rendered PDF

`output/pdf/operator-economy-emergence-evidence-signals-2026.pdf`
sha256 `dc0048bcf6d8f1464cecfab42862715b6465c116dbabc04da03b3ee42fe72e23`

That file is committed alongside the source because **the build is not reproducible**. `build_pdf.py`
has no determinism controls: the PDF embeds `/CreationDate`, `/ModDate`, and a timestamp-derived
`/ID`, so re-running produces different bytes and a different hash. Rendering also requires
`reportlab`, which is not installed on every portfolio host.

Cite `report-source.md` at a commit for evidence purposes. The PDF hash is a corroborating record
of the artifact that was read, not a value any host can re-derive on demand.

## Page anchors used by evidence records

| Pages | Section |
|---|---|
| 2 | Executive verdict |
| 8–10 | Claim ladder |
| 12 | Mechanisms F (formation) and G (value and control) |
| 25–26 | §10 promotion rules and falsifiers |

## Related

`../operator-economy-thesis/` is Working Paper No. 02 — the earlier source-state audit that
established which Working Paper No. 01 claims had to be killed or repaired. It is retained
provenance and is **not** the cited evidence base. See its own README.
