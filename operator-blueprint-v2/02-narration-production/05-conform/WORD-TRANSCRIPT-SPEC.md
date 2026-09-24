# Final Word-Level Transcript Specification

Status: proposed v0.2.

The transcript describes the exact final narration master that Step 3 will use as its timeline. It
is generated after narration editing from the frozen master candidate and finalized only after
lexical conformity.

## Required companion identity

The transcript package records:

- episode number and slug;
- locked script revision and SHA-256;
- narration master relative path and SHA-256;
- narration master duration in integer milliseconds;
- `oe-spoken-text-v1` ordered `W`-token count and SHA-256;
- transcript creation tool and version;
- alignment date; and
- human reviewer and review state.

## Required word fields

Each spoken word record contains:

| Field | Contract |
| --- | --- |
| `index` | Zero-based integer in `W` order. |
| `canonical_token` | Exact whitespace-delimited token corresponding to the locked script. |
| `start_ms` | Integer, inclusive start. |
| `end_ms` | Integer, exclusive end. |
| `confidence` | Numeric or named confidence when the aligner supplies it; otherwise `null`. |
| `review_state` | Must be `approved` in an authoritative transcript. |
| `alignment_parts` | Optional ordered acoustic sub-intervals; subordinate to this `W` record. |

Optional fields such as `w_id`, `display_token`, `sentence_id`, or `section_id` may be added when
the schema permits them, without replacing `canonical_token`. A `w_id` is derived deterministically
from `index`: index zero is `W000001`. `alignment_parts` do not create new canonical words or alter
the `W` count/hash.

## Timing invariants

For every record:

```text
0 <= start_ms < end_ms <= master_duration_ms
```

Across records:

```text
previous.end_ms <= current.start_ms
```

Intervals are half-open: `[start_ms, end_ms)`. Gaps are allowed for breaths and pauses. Overlaps are not allowed in the authoritative narration track.

## Lexical invariants

- Word records reproduce every locked `W` token exactly once and in order.
- The transcript contains no visual captions, music lyrics, sound effects, or editor notes.
- Acoustic-comparison rules match the approved lexical-conformity report.
- A display-friendly or ASR token cannot replace or obscure the canonical `W` token.
- Low-confidence names, numbers, acronyms, negations, and qualifications receive human verification.

## Example shape

```json
{
  "schema_version": "oe-word-transcript-v1",
  "base_dir": ".",
  "spoken_identity": {
    "schema_version": "oe-spoken-text-v1",
    "token_count": 3019,
    "sha256": "..."
  },
  "master": {
    "path": "narration-master.wav",
    "sha256": "...",
    "duration_ms": 123456
  },
  "words": [
    {
      "index": 0,
      "canonical_token": "This",
      "start_ms": 240,
      "end_ms": 510,
      "confidence": 0.99,
      "review_state": "approved"
    }
  ],
  "unresolved_mismatches": 0
}
```

The example is structural only and does not create an episode artifact.

## Validation and invalidation

Validation must confirm:

- required identity fields exist;
- the master path resolves;
- the observed master hash and duration match;
- indices are contiguous and unique;
- exact canonical tokens, count, order, and ordered-token SHA-256 match Step 1;
- timing invariants pass;
- the transcript word sequence conforms to the locked script; and
- every flagged uncertainty has a disposition.

Any sample-level master change invalidates the final alignment, transcript, intentional-pause map,
`technical_pass`, `creative_approved`, narration lock, and Step 3 handoff. Regenerate and re-review
them before Step 3 resumes.
