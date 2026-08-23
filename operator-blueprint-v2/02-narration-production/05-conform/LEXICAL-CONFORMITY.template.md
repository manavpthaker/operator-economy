# Lexical Conformity Report

Template version: proposed Step 2 v0.2.

## Authority pair

- Episode:
- Locked script path/revision:
- Locked script SHA-256:
- Locked spoken-word count:
- Ordered `W`-token SHA-256:
- Narration master path:
- Narration master SHA-256:
- Narration master duration:
- Comparison method/tool/version:
- Final-master alignment/transcript path/SHA-256:
- Reviewer/date:

## Acoustic-comparison rules

- Case:
- Punctuation:
- Numerals:
- Abbreviations/acronyms:
- Contractions:
- Hyphens:
- Approved pronunciation aliases:
- Non-spoken annotations excluded:

Acoustic comparison may recognize an approved pronunciation realization. It may not change,
retokenize, or excuse a mismatch in the canonical whitespace-delimited `W` sequence. Any
`alignment_parts` remain subordinate to one `W` token.

## Automated result

- Canonical script `W` tokens:
- Aligned master `W` records:
- Ordered `W` identity match:
- Additions detected:
- Omissions detected:
- Substitutions detected:
- Repeats detected:
- Truncations detected:
- Low-confidence regions:

## Mismatch disposition

| ID | Script anchor | Master timecode | Detected mismatch | Human finding | Confirmed lexical mismatch | Required action | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | Tool error / equivalent form / real mismatch | yes / no | Pickup / Step 1 change / none | |

## Decision

- Zero unresolved spoken-word mismatches: yes / no
- Every qualification and negation preserved: yes / no
- Final canonical `W` count confirmed:
- Gate N6 lexical result: passed / failed / return_to_editorial / blocked
- Conformity editor/signature/date:

A human may resolve an alignment or normalization error. A human may not waive a confirmed spoken-word mismatch inside Step 2.
