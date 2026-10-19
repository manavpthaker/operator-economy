# EP009 final r8 lock audit

**Verdict: pass.** The exact r8 carrier is soundly locked as the final long-form picture and narration assembly. The 9:16 authorization is correctly limited to local derivative production from existing, hash-bound material. No field overreaches into release clearance, upload, publication, paid generation, new claims, or automatic acceptance of a Short.

## Evidence

- All six issued work-order inputs match their recorded SHA-256 values.
- The carrier SHA-256 is `cc5805a990d10812b5349568e50a74dc0e21b09ed402b49250f9796640ed710e`.
- Independent `ffprobe -count_frames` returned 1,280 x 720, 24 fps, 29,323 decoded video frames, 1,221.791667 seconds, 48 kHz stereo audio.
- Independent loudness measurement returned -19.49 LUFS, 3.70 LU LRA and -5.69 dBTP, matching the rounded lock values.
- The lock binds the unchanged r3 narration master and word transcript; both current hashes match.
- The r3 brand/experience lock, r4 avatar-opening lock, S13 native-tool lock, P08 picture source and P08 editorial review all match their bound hashes.
- All 26 path/hash occurrences across the final decision payload, lock and owner-feedback payload resolve and match; they represent 13 unique bound files.
- The 211-event decision log has a valid hash chain. The final decision is line 210, event hash `2889c78c2e5edd83d10076b980dffc32985f088e8e04c4170aa391e83da683e9`. The owner acceptance is line 211, event hash `edafe419c01b8fdfa1f43b791b06e7ea588a8ae2e897d9a87c72b0ae782b66be`.
- The standalone decision and owner-feedback JSON files exactly equal their corresponding decision-log payloads after excluding the helper-added hash envelope.

## Scope assessment

The owner message supports both recorded actions: locking the exact current r8 episode and beginning 9:16 Shorts with the pieces already made. The lock freezes every output frame `[0,29323)` and the r3 narration. It does not convert the review carrier into a release-cleared publication master.

The derivative permission is appropriately bounded. It allows word-accurate excerpt selection, cutting, portrait reframing, captions, evidence crops and faithful reuse of existing high-resolution components. It requires separate review for each Short and prohibits long-form mutation, new claims, invented evidence or UI, paid/external generation, upload and publication.

The older build and component records retain their original `owner_accepted: false` diagnostic fields. That is intentional history, not a conflict: owner acceptance is separately attached to the exact full r8 carrier by the final lock and line-211 feedback event.

## Findings

- Blocking defects: none.
- Missing lock bindings: none.
- Overreaching authorization: none.
- False release or publication claim: none.

The packet passes direct Draft 2020-12 schema validation. The full `oe-cinema validate-deliverable` route cannot run because this legacy EP009 folder has no `episode.json` or `production-state.json`; that tooling limitation does not affect the hash or scope findings above.
