# EP007 S16 native Google Sheets capture

Native workbook: https://docs.google.com/spreadsheets/d/1C7nhlBdABRz2tfPqOS6fkoLZOcNOQKv7v4DGSWoCYvw/edit#gid=30220403

Created by importing the locally verified `seed.xlsx` using the Google Drive connector with `upload_mode: native_google_sheets`. Native MIME and all three tab values/formats were read back. The file is in the new My Drive root ChatGPT folder (`1cscaJ1M9SRNo5sHCCJx-0Mn5z8ErQfOU`). Drive metadata reports `shared: false` and owner-only permission. No share or publication action occurred.

## Capture targets

| Tab | Native sheet ID | Relevant range |
| --- | --- | --- |
| Readiness checklist | 30220403 | A1:D7 |
| Package index | 1753393686 | A1:D7 |
| Interview notes | 927469059 | A1:D7 |

Meaningful action: read the fictional owner's Q3 in `Interview notes!C7`, then classify `Readiness checklist!B7` as `Unresolved` and enter the reason in `D7`: `Only the owner can approve exceptions; no backup is authorised.`

The sheet currently contains the completed classification. To film the action, the root recorder can stage only B7 as `To review` and D7 as `Review owner interview Q3`, then make the final changes through the real interface. Preserve A7/C7 and the surrounding rows. This staging is an illustrative recording action, not a real assessment or evidence of results. Conditional formatting highlights B7 only when its value is `Unresolved`.

The first row is documented handoff; its reason still reads `Exception prices still need owner approval.` Standard-price orders may proceed through Sam. Do not imply documentation resolved the exception dependency.

## Verification and limits

- Local Artifact Tool render visually inspected for all three sheets: readable 15 pt Arial, four columns, 94 px body rows, no clipping.
- Native Google cells verified: all values, disclosure, font sizes, text wrap, title/header formatting and unresolved conditional rule survived conversion.
- Root must visually check native Google rendering at normal zoom before recording. This worker did not control the browser.
- The source labels are filenames from the content agent's illustrative package. They are plain text references, not live hyperlinks or published downloads.
- All tabs explicitly disclose `ILLUSTRATIVE EXAMPLE / NOT A CLIENT CASE`.
- No financial scores, valuation claims, readiness conclusion or real client data.

## Provenance

Content supplied by `/root/s20_direction` in the current authorized EP007 tool-demo task. The source excerpts are shortened verbatim extracts from the supplied fictional interview. The operative rows reflect its Q1-Q3 and preserve the unresolved owner dependency. Local `seed.xlsx` SHA-256: `d120d895280a27de27826dd795d7cc290c3b28fd5d16b02e78c58abf210db050`.

Legacy `agent-deliverable.schema.json` requires `external_writes: false` unconditionally. This packet necessarily records `external_writes: true` because the parent explicitly authorized creation of this private native Google Sheet. That one schema mismatch is reported, not concealed; no schema or approval gate was changed.
