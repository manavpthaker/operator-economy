# N4A Calibration Results — two-stage acted-guide method

Executed: 2026-08-28
Configuration: `N3-VOICE-AND-CAPTURE-LOCK.md`, revision `n3-two-stage-acted-guide-v1` (N3 passed)
Executor: `../../tools/calibrate.py`
Canonical `W` SHA-256: `096329c04c9ce0ce9964e67279657be9fbd488772ae7df8893a28f76083d283a`

All four calibration modes were acquired under the frozen N3 configuration. Style instructions,
model, voice, settings, and seed were byte-identical across every request; only the text range
differed.

## Modes acquired

| Mode | Purpose | Block(s) | Range | Tokens | Chunks | Duration | Passage SHA-256 |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| M1 | cold open and episode promise | S00+S02 | `W[0,236)` | 236 | 1 | 73.747s | `345c52ea1151cf83f1a412fe71b481c1c3fa6acdb768e55a1c40303049195d68` |
| M2 | dense evidence | S05 | `W[890,1326)` | 436 | 3 | 172.803s | `1ec4e1d25f7362b40b2ae29fa444b0b04ae7187174b9381bc0c586b38e357e0c` |
| M3 | economics and uncertainty | S08 | `W[1875,2111)` | 236 | 2 | 107.462s | `1f5a8b6ebb21c87efb762092163e999e582e29f49d801a1756a2f40826db66e2` |
| M4 | names, numbers, acronyms, pronunciation | S09 | `W[2111,2462)` | 351 | 4 | 140.295s | `43ff3e600b2dcb1b1b4c68b9add2f354d71799584e91c35b3db421b39296533a` |

Total 1,259 tokens, 494.3 seconds. Every passage was verified as an exact token slice of canonical
`W`, and every chunk set rejoins to its passage string exactly — no sentence, number, or token was
split or lost.

Masters: `outputs/raw/n4a/<mode>/N4A-<mode>.saved-c.master.wav`, one per-chunk manifest each.

## Technical results

| Mode | Format | Guide→transfer envelope r | Dynamic range CV | Peak | Chunk RMS spread |
| --- | --- | ---: | ---: | ---: | ---: |
| M1 | 48 kHz / 16-bit / mono | `+0.893` | 0.828 | −0.72 dBFS | n/a (1 chunk) |
| M2 | 48 kHz / 16-bit / mono | `+0.886` | 0.868 | −0.61 dBFS | 0.4 dB |
| M3 | 48 kHz / 16-bit / mono | `+0.870` | 0.917 | −0.12 dBFS | 0.9 dB |
| M4 | 48 kHz / 16-bit / mono | `+0.896` | 0.903 | −0.46 dBFS | 2.1 dB |

**Performance preservation is consistent.** Envelope correlation between each guide and its transfer
holds at `+0.87` to `+0.90` across all four modes and both short and long passages, matching the
`+0.899` measured on the `W[30,110)` microtest. Dynamic range is preserved, not flattened. The
method reproduces reliably.

## Findings

### F1 — Provider ceiling is audio duration, not characters (accepted, mitigated)

`gemini-2.5-pro-tts` returns HTTP 502 above roughly 75–78 seconds of generated audio.
Measured: 1,360 chars → 73.7s passed; 1,479 chars → 502, deterministic on retry; M3 chunk 1 at
1,213 chars → 76.7s passed; M4 chunk 1 at 1,233 chars → 502.

Character count is a poor proxy because number-dense text expands when spoken — `2,601` is five
characters and several spoken words. M4 required `--max-chars 700` where M1–M3 ran at 1,250–1,400.

Consequence for N4B: the full 3,019-token episode needs roughly 13–16 chunks, and number-heavy
sections need smaller ones. Chunk size must be set from expected spoken duration, not length.

### F2 — Short trailing chunks drift in level (open, chunking-rule change proposed)

M4's chunk RMS spread is 2.1 dB, versus 0.4 dB (M2) and 0.9 dB (M3). The outlier is M4 chunk 4: a
3.65-second, single-sentence trailing chunk at −17.0 dBFS against −19.1 dBFS for chunk 2.

Each chunk is an independent stochastic generation, so a very short chunk carries little context and
lands at its own level and pace. Proposed rule for N4B: **merge any trailing chunk under ~15 seconds
into the previous chunk** rather than emitting it alone, accepting a slightly over-target chunk
instead of an isolated fragment. M1–M3 need no change.

### F3 — Every master runs hot (open, needs a delivery decision)

Peaks land between −0.72 and −0.12 dBFS. M3 at −0.12 dBFS is effectively at full scale. The
provider returns audio at this level; nothing in this chain applies gain.

This is acceptable as raw acquisition evidence but is not a safe delivery level — inter-sample peaks
can clip on conversion or encode. The delivery-master step must apply headroom (normalize to a
target such as −3 dBFS peak or a loudness target) as a single recorded conversion. Raw provider
bytes remain immutable per the N3 format contract.

### F4 — Transient provider 502s (accepted, mitigated)

Several 502s were not reproducible. M4 chunk 4 (66 characters, an ordinary sentence) failed once and
succeeded on retry. The executor now retries transient 502s and resumes a mode from completed
chunks, so a mid-mode failure never re-bills successful work.

## Decision states

### `technical_pass` — **PASS** for configuration v2 (recorded 2026-09-01)

Passing:

- exact configuration reproducibility: every request used byte-identical frozen settings
- provenance: per-chunk manifests bind text SHA-256, request-body SHA-256, and both output hashes
- valid audio: all masters decode as 48 kHz / 16-bit / mono PCM, correct durations, no truncation
- passage integrity: all four passages verified as exact canonical-`W` slices; chunks rejoin exactly
- format contract: native PCM at both stages, no lossy intermediate, raw outputs preserved at 0600

Exact-word review: **complete by human listen**, 2026-09-01. Offline ASR was not usable — the only
local model is a 575 KB `for-tests-ggml-tiny` stub that returns empty output — and per the N4A gate
ASR is diagnostic and cannot clear exact words in any case.

The highest-risk conformity hypothesis was tested directly: M1 carries the only true contractions in
the set (`Let's` at chunk 1 ~49s, `We're` at chunk 2 ~7s). Had `gemini-2.5-pro-tts` expanded them to
"Let us" / "We are" despite `advancedVoiceOptions.enableTextnorm: false`, every take would have been
lexically nonconforming regardless of delivery quality. Owner confirmed on isolated excerpts:
`it says Let's and We're`. Text normalization is off and effective on this path.

Carried open, not blocking this gate:

- **F3** headroom must be dispositioned before any delivery master is produced.
- **F8** contractions are a Step 1 editorial item; the owner declined to reopen Step 1 for it.

### `creative_approved` — **PASS** for configuration v2 (recorded 2026-09-01)

Owner decision on the `n3-two-stage-acted-guide-v2` set (Algieba + candidate C4, all four modes):
`they all pass`.

Superseded: the 2026-08-30 REVISE below applied to configuration v1 (Achird + candidate C) and is
retained as history.

### F8 — no contractions: routed to Step 1, not Step 2

Owner note on the passing set: the read has no contractions, `"cannot" instead of "can't" et al`.

This is an editorial property of the locked words, not a narration defect. Step 2 speaks the exact
`W` sequence; substituting `can't` for `cannot` is a word change and is exactly what the lexical
conformity chain exists to prevent.

Measured across canonical `W` (3,019 tokens):

| Form | Count |
| --- | ---: |
| `cannot` | 3 |
| `do not` / `does not` / `is not` / `are not` / `will not` / `would not` (and similar) | 0 |
| tokens with an internal apostrophe | 12 (`Let's`, `We're`, `You're` + 8 possessives) |

Per mode: M1 carries `Let's` and `We're`; M2, M3 and M4 carry only possessives plus one `cannot`
each. The script is therefore not uniformly formal — the formality sits in three `cannot`
occurrences and in the general absence of negative contractions, which is a Step 1 voice decision.

**Remedy is a Step 1 editorial revision.** Consequence under the invalidation rules: a new Step 1
lock invalidates the Step 2 narration lock, and a script-hash change invalidates affected direction,
takes, conformity, transcript and handoff. The N3 configuration freeze is **not** invalidated — the
provider chain, guide voice, register, settings and format contract all survive — so re-acquisition
is a rerun of the proven configuration, roughly 11 chunk pairs, not another calibration search.

**Exact-word review item:** M1 contains `Let's` and `We're`. Confirm the model did not expand them
to `Let us` and `We are`. `advancedVoiceOptions.enableTextnorm` is `false` specifically to prevent
that, but it is unverified on this path and would be a lexical conformity failure, not a style note.

Two of four modes fail creative review, so the set does not pass. This is a performance-only
revision: the exact approved words are unchanged, so per the invalidation rules it returns to
N2/N3 and does **not** reopen Step 1.

### F5 — candidate C is passage-specific direction, not a method-level register (root cause)

The frozen candidate-C style instructions name `"missing"`, `"Or worse"`, `"Everything is green"`,
and `"2022"`. Those phrases exist only in P01 `W[30,110)`.

| | P01 | M1 | M2 | M3 | M4 |
| --- | --- | --- | --- | --- | --- |
| named phrases present | yes | yes | no | no | no |

M1 is `W[0,236)`, which contains P01, so M1 received the full specific direction. M2/M3/M4 received
dangling references to absent text and were effectively driven by the general clauses alone.

This inverts the result: **M3 and M4 scored best because the passage-specific direction did not
apply to them.** M1 received the complete direction and was fastest at 192 wpm, because that
direction is uniformly compressive — "Keep phrases connected", "brief pauses only when the thought
changes", "Energy seven of ten". On short cold-open sentences those compound.

M2 and M4 sit at 151 and 150 wpm, so pace alone does not explain the split. M4 carries 0.61s mean
pauses at 71% speech density; M2 carries 0.58s at 75%. Dense abstract argument needs more room than
concrete numbers and received less.

**Consequence: candidate C cannot serve as the production direction for a multi-section episode.**
The method needs a stable, passage-independent narrator register, with any passage-specific notes
carried separately and only where they apply. A replacement register prompt must be frozen at N3
before N4A is re-acquired.

## Register search log (2026-08-30)

M2/M3/M4 are body-register content and are solved. M1 (cold open) is the only unsolved mode.

| Candidate | Register change | M1 wpm | M1 artic | M1 pause | M1 p.var | Owner verdict |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| C | passage-specific (P01) | 192 | 244 | 0.44s | 0.24 | M1, M2 fast |
| C1 | uniform slowdown | 148 | 205 | 0.57s | 0.35 | M1 ok; M2 drags |
| C2 | contrastive room, energy 7 | 176 | 235 | 0.45s | 0.22 | faster than rejected C |
| C3 | room between ideas, not inside | 172 | 249 | 0.66s | 0.43 | **M2 great**; M1 robotic |
| C4 | + elision, short sentences flow | 180 | 238 | 0.53s | 0.31 | M2 good; M1 still robotic |

Alternative guide voices, M1 under C4 (identity unchanged — the guide only carries performance):

| Guide voice | wpm | artic | pause | p.var | CV |
| --- | ---: | ---: | ---: | ---: | ---: |
| Achird (frozen) | 180 | 238 | 0.53s | 0.31 | 0.841 |
| Umbriel | 189 | 238 | 0.47s | 0.31 | 0.826 |
| Algieba | 164 | **226** | 0.52s | 0.32 | **0.911** |
| Enceladus | 174 | 236 | 0.41s | 0.29 | 0.899 |

### F6 — M1 articulation is content-bound, not direction-bound

Across five registers and four guide voices, M1 articulation never fell below 226, against M2's 190
under the identical configuration — a persistent ~25% gap. Short declarative cold-open sentences
produce crisp, fully-articulated delivery regardless of prompt or voice.

Two consequences. First, the accepted body register (C3/C4) is validated and should be frozen for
M2/M3/M4-type content. Second, the cold open needs either its own register and guide voice, recorded
as a second frozen configuration bound to the sections it covers, or a non-prompt remedy at the edit
stage. A sixth register candidate is not indicated.

### F7 — wpm is the wrong control variable

Articulation rate (words per minute of speech only) and inter-idea pause move independently, and
every candidate before C3 moved them together. C1 = slow words + varied pauses → drags.
C2 = fast words + tight pauses → rushed. C3/C4 = brisk words + varied pauses → accepted on M2.
Direction and QA for N4B should target the pair, not overall wpm.

## Gate N4A result

- All four modes acquired under frozen N3 configuration: **yes**
- Technical measurements complete: **yes**
- Exact-word human review complete: **no**
- Owner creative decision recorded: **yes** — PASS on configuration v2, 2026-09-01 (`they all pass`)
- Owner note carried to Step 1: no contractions (F8) — editorial, not narration
- Exact-word review complete: **yes** — 2026-09-01, contraction conformity confirmed
- **N4A gate result: PASSED** for configuration `n3-two-stage-acted-guide-v2`
- N4B full capture: **not authorized** — requires N4A closed plus its own separate authorization
- N4B full capture: **not authorized**; requires N4A pass plus its own separate authorization
