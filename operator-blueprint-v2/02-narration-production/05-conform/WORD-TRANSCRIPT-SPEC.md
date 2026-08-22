# Final Word-Level Transcript Specification

Status: proposed v0.1.

The transcript describes the exact final narration master that Step 3 will use as its timeline. It is generated after narration editing and lexical conformity.

## Required companion identity

The transcript package records:

- episode number and slug;
- locked script revision and SHA-256;
- narration master relative path and SHA-256;
- narration master duration in integer milliseconds;
- transcript creation tool and version;
- alignment date; and
- human reviewer and review state.

## Required word fields

Each spoken word record contains:

| Field | Contract |
| --- | --- |
| `index` | Zero-based integer in spoken order. |
| `word` | Canonical spoken token corresponding to the locked script. |
| `start_ms` | Integer, inclusive start. |
| `end_ms` | Integer, exclusive end. |
| `confidence` | Numeric or named confidence when the aligner supplies it; otherwise `null`. |
| `review_state` | `unreviewed`, `machine_pass`, or `human_verified`. |

Optional fields such as `display_word`, `sentence_id`, or `section_id` may be added without replacing the canonical `word`.

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

- Word records follow the locked spoken words in order.
- The transcript contains no visual captions, music lyrics, sound effects, or editor notes.
- Normalized comparison rules match the approved lexical-conformity report.
- A display-friendly token cannot replace or obscure the canonical spoken token.
- Low-confidence names, numbers, acronyms, negations, and qualifications receive human verification.

## Example shape

```json
{
  "episode": "EP###-slug",
  "script_sha256": "...",
  "master": {
    "path": "narration-master.wav",
    "sha256": "...",
    "duration_ms": 123456
  },
  "words": [
    {
      "index": 0,
      "word": "This",
      "start_ms": 240,
      "end_ms": 510,
      "confidence": 0.99,
      "review_state": "human_verified"
    }
  ]
}
```

The example is structural only and does not create an episode artifact.

## Validation and invalidation

Validation must confirm:

- required identity fields exist;
- the master path resolves;
- the observed master hash and duration match;
- indices are contiguous and unique;
- timing invariants pass;
- the transcript word sequence conforms to the locked script; and
- every flagged uncertainty has a disposition.

Any sample-level master change invalidates the transcript. Regenerate and re-review it before Step 3 resumes.
