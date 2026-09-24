# Deterministic Spoken-Text Identity Specification

Status: proposed Step 2 v0.2.

Specification ID: `oe-spoken-text-v1`

This contract turns one locked Step 1 script into one reproducible ordered `W`-token sequence.
That sequence—not a word count alone, ASR guess, provider prompt, pronunciation alias, or
performance-marked copy—is the lexical identity used by direction, capture, editing, conformity,
transcript alignment, narration lock, and Step 3 handoff.

## Required inputs

- The exact locked-script bytes named by the current Step 1 v1.5 editorial lock.
- The script SHA-256 recorded by that lock.
- The current Step 1 narration handoff and pronunciation register.

The extractor fails closed if the observed script hash differs, a narration block contains a
placeholder, or the Markdown structure is ambiguous.

## Canonical extraction

1. Decode the locked script as UTF-8 without changing the source file.
2. Recognize each ordered `## SNN: ...` scene and its exact `### Narration` heading.
3. Select only the narration body until the next level-two or level-three heading.
4. Exclude the silent sting and every scene without narration, plus headings, metadata, editorial
   checks, claim IDs, performance notes, and post-script receipts.
5. Fail when a narration heading occurs outside a recognized scene, a scene ID repeats, no narration
   exists, or selected text contains unresolved markup or placeholders.
6. Trim only the selected block's outer whitespace. Split and serialize tokens as defined below.

Each extracted block keeps its Step 1 scene ID, such as `S00` or `S12`, plus half-open
`start_token`/`end_token`, token count, block hash, and `authority: subordinate_part`. Block and later
acoustic identities may help direction and alignment; none can replace the single full `W` authority.

## Canonical Step 1 `W` tokens

Tokenization deliberately reproduces the approved Step 1 convention:

1. Split the selected narration text on one or more Unicode whitespace characters.
2. Preserve every non-whitespace character in each token, including attached punctuation,
   apostrophes, dashes, currency symbols, and numerals.
3. Preserve case. Do not expand, normalize, case-fold, or silently repair any token.
4. Write the tokens in spoken order, one exact token per line, with one terminal LF.
5. SHA-256 that one-token-per-line byte stream. This is the ordered narration-token SHA-256.

`canonical-w.txt` is the byte authority: exact tokens, one per LF, with one terminal LF. A
companion `spoken-identity.json` records the script hash, tokenization and serialization IDs, full
token count/hash, and subordinate scene-block ranges. `W000001`, `W000002`, and so on are
deterministically derived from zero-based token position when a human-readable ID is needed.

## Pronunciation and acoustic alignment

Pronunciation direction may map a `W` token to an intended spoken realization without replacing its
identity. When one `W` token is realized as several acoustic words, the final transcript keeps the
canonical `W` ID on the full interval and may add ordered `alignment_parts`. Those parts are
subordinate acoustic evidence; they do not increase the `W` count or alter the ordered-token hash.

A change in intended word or meaning is not a pronunciation alias. It returns to Step 1.

Every alias record includes:

- canonical `W` ID and exact token;
- intended spoken form;
- plain-language pronunciation note;
- approval owner and date; and
- source or subject-matter confirmation where necessary.

## Reproduction test

N1 passes identity only when two clean extractor runs against the same locked-script bytes produce:

- the same scene-block IDs, ranges, counts, and subordinate hashes;
- byte-identical `canonical-w.txt` output;
- identical `spoken-identity.json` after holding the recorded source path constant; and
- the same full token count and ordered-token SHA-256.

For the approved AI Visibility v1.1 Step 2 fixture, the expected result is:

- locked script SHA-256:
  `74048b55ed15ed6ed679abb5a6c892def8a8a40e75e7cebeafdfde319dd67efa`;
- `W` count: `3019`; and
- ordered narration-token SHA-256:
  `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`.

Any difference is a blocker. Step 2 may not invent a normalization judgment to make a mismatch pass.
