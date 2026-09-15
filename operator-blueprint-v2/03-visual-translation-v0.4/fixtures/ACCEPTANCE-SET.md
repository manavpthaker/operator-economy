# Step 3 v0.4 acceptance set

Status: **candidate controls; no process or episode approval implied**.

The full set has 73 controls:

- 54 preserved v0.3 controls, executed against their unchanged bytes and expectations; and
- 19 additive v0.4 controls: two positive baselines, one production-directory guard, and sixteen
  adversarial cases.

Run:

```bash
python3 operator-blueprint-v2/03-visual-translation-v0.4/fixtures/run_acceptance.py
```

## New controls

| Control | What it proves | Expected |
|---|---|---|
| `positive/film-layer` | both mode axes, an honest `EST-*` unit, a `BO-*` Working Model unit, and all exact application pins pass together | clean |
| `positive/full-input-lock` | the standalone V1 record resolves its governing process and all thirteen Step 1/Step 2 inputs | clean |
| `p03-production-case-guard` | production directories cannot redefine canonical paths or expected failures through fixture metadata | clean |
| `a51-skills-lock-missing` | an absent OE skill lock blocks the application freeze | V1 |
| `a52-illustration-hash-drift` | a changed Working Model language cannot pass under an old hash | V1 |
| `a53-reference-manifest-drift` | the owner-accepted visual-language reference cannot drift silently | V1 |
| `a54-picture-mode-missing` | a timed unit cannot omit who carries language | V4 |
| `a55-carrier-mismatch` | narrated observation cannot assign language to a silent scene participant | V4 |
| `a56-visible-speech-mismatch` | narrated observation cannot require visible speech | V4 |
| `a57-mute-expectation-mismatch` | narrated observation cannot make a muted viewer expect a missing line | V4 |
| `a58-event-binding-missing` | a unit must bind to a real semantic event | V4 |
| `a59-event-binding-ambiguous` | a unit cannot be both a business change and viewer establishment | V4 |
| `a60-v7-skill-pin-dropped` | V7 cannot discard the filmmaking authority frozen at V1 | V7 |
| `a61-unit-job-missing` | picture must contribute a stated job beyond filling time | V4 |
| `a62-process-lock-hash-drift` | the episode cannot claim a governing process whose bytes changed | V1 |
| `a63-upstream-input-hash-drift` | a changed Step 1/Step 2 artifact invalidates the standalone freeze | V1 |
| `a64-upstream-input-missing` | every required Step 1/Step 2 input needs a resolvable path and hash | V1 |
| `a65-process-path-fork` | a self-consistent alternate process path cannot replace the governing process | V1 |
| `a66-upstream-path-fork` | changing an upstream path and its hash together still invalidates the freeze | V1 |

## What the machine proves

- exact governing-process, Step 1/Step 2, and local application-authority paths and hashes;
- OE skill-lock membership and local member hashes;
- source-ledger reference-only status and expected source IDs;
- illustration reference-manifest status and asset integrity;
- allowed picture/audio tuples;
- exactly one `BO-*` or `EST-*` binding per timed unit;
- correct state domain for that event; and
- preservation of application hashes at V7.

## What remains human

The validator cannot prove that a unit job is worth seeing, that a picture/audio mode is the best
choice, that establishment is lucid, that the Working Model is genuinely rough rather than merely
noisy, that a direction-bible treatment is directable, or that the resulting film feels cinematic.
Those remain the named human decisions at V2 through V7 and the motion/performance tests in Step 4.

The v0.3 acceptance document's stale prose references to contract `0.2`, twenty-two adversarial
cases, and an earlier run-evidence tree are historical documentation defects. They are not used as
v0.4 evidence. This set executes the preserved validators and current fixture bytes directly and
freezes a new result below.
