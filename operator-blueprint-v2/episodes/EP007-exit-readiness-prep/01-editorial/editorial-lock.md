# Editorial lock: EP007 — a sale-readiness practice

Status: **LOCKED**

Gate: **E6 — script lock**

Episode: EP007

Locked: 2026-09-01

Locked by: Manav Thaker

These are the exact words Step 2 is authorized to perform.

## Frozen artifact hashes

| Artifact | Path | SHA-256 |
|---|---|---|
| Editorial contract | `editorial-contract.md` | `163fc364c3d89aa5e80d1fc789a605a261c855e99729182292e944ea0b32f0e5` |
| Operator Canvas | `operator-canvas.md` | `3376437f8eda00a4aec5b1ef6e0ff5379abb2f051e3512fc5d683ed2720b158f` |
| Episode Investment Thesis | `episode-investment-thesis.md` | `868dc798eeb0513b083debb08ea376b333ae486e9a535be7facf5183e94726f4` |
| Narrative spine | `narrative-spine.md` | `c053f4d95542ce9fc42e9a665d10576cc69e99577fc8849208970f9163efbe4f` |
| Episode beat sheet | `episode-beat-sheet.md` | `eb953ffa1a0fc5bf4540842f8cd86db19838a1692c00e439c9fdfd538225f4fb` |
| Episode outline | `episode-outline.md` | `c8a2a52a41d30826fdc9dc3711492b3325bb7def654cf5fb00598cca20013e3b` |
| Voice and comedy map | `voice-and-comedy-map.md` | `c8f874cac4951f4d00ccf86d1a0b0f1d789e75dabc0231da1600f117351ed880` |
| Claims map | `claims-map.md` | `0c4f715d71f816fb8190c5fc3777e61cfdabd3c2cc5f26a2aee7a89d0f5fe4e1` |
| Script | `script.md` | `e56bbb80c1b3a21679a17459402130d820be285ee389fc2978ef8216d6487db0` |
| Clean read-through | `performance-readthrough.txt` | `e7b017837add63830d689f47e723b98da242a5d3d3cbad522d5a79260add59de` |
| E5V conformity report | `editorial-voice-conformity.md` | `587d4670de84fb4b06ff2515c362fbfde7aa4cae124978617c062ecd5fb047de` |
| Review disposition log | `review-disposition.md` | `680ca02ed43388ede0078d896fc92dbf652290311ad98e27be07229aab59db89` |
| Step 0 handoff record | `handoff.md` | `1a90d6f0768f6781db1c228986d4bdf38661cbe1e140983341f6358f715df72d` |

## Reviewed external authorities

| Authority | SHA-256 |
|---|---|
| `content-os/voice.md` | `3b9b9400f9f2ac6aeaff09d62cca2092c322a969447bbc85d161b56a42d0d20e` |
| `01-editorial/VOICE-ARCHITECTURE.md` | `ce9b0af23221ff5d9266460a279c0a6fd6f53874e39c2f5831ceeb22a3569474` |
| `studio/config/speech-profile.md` | `75913da0bc5d5b360c88f18c70b60d8d4af14128184e8164872edd56f71ceddc` |

Content OS routing confirmed: `voice.md` §1 routes **YouTube VO and audio-first episode narration hosted by Manav** to the **Operator Economy hosted long-form** register. The script was written to that register.

## Spoken identity

- Exact spoken-word count: **3186**
- Expected duration range: **19.3 to 22.8 minutes** (140 to 165 words per minute)
- The clean read-through contains the same words as the script's spoken layer and no production metadata.

## Required exact strings, present in the locked words

**Fixed brand string:**

> This is The Operator Economy, where we show you how to use AI to build, own, and operate a sustainable business of one.

**Pre-sting payoff tease:**

> That pause costs her more than anything else in the room. And there is a business hiding inside it that almost nobody is running.

**Final like-and-subscribe sentence:**

> If you want more blueprints taken apart like this one, including the parts that do not survive the arithmetic, subscribe.

## Gate E6 conditions

| Condition | Result |
|---|---|
| Final script and claims-map hashes recorded | **pass** |
| Contract, Canvas, thesis, spine, beat sheet, outline, voice map hashes recorded | **pass** |
| Named owner, decision, timestamp | **pass** |
| Exact word count, clean read-through, expected duration range | **pass** |
| Passed E5V tied to the final script and reviewed authority hashes | **pass** |
| Passed owner cold read tied to the exact final script and read-through hashes | **pass** |
| Positive hosted-voice evidence complete across all five functions | **pass** |
| Owner answered the direct voice-match question `yes` | **pass** |
| Content OS routes YouTube VO to the Manav-hosted long-form register | **pass** |
| Exact pre-sting tease and final audience ask present in locked words | **pass** |
| No unresolved change request | **pass** |

**Gate E6: PASSED. Script locked.**

## Spoken-text identity (`oe-spoken-text-v1`)

Step 2 consumes this identity, not the prose.

| Field | Value |
|---|---|
| Specification | `oe-spoken-text-v1` |
| Tokenization | unicode-whitespace split, case and punctuation preserved |
| Serialization | one token per line, UTF-8, single terminal LF |
| Ordered `W` token count | **3186** |
| Canonical `W` SHA-256 | `333a45d7449f5cb4c3e394a9e262c3a3a60c3825e76563bc0149498f0b41860c` |
| Byte authority | `canonical-w.txt` |
| Companion record | `spoken-identity.json` (26 subordinate scene blocks) |

**Structure correction recorded.** The script was first drafted with `## B00` beat headings and
blockquoted narration, which does not match the Step 1 v1.5 script template and would have failed
the `oe-spoken-text-v1` extractor closed on ambiguous structure. It was converted programmatically
to the template's `## SNN:` / `### Narration` form. The spoken words are byte-identical to the
version the owner cold-read: **3186** tokens before and after. The owner voice
decision therefore stands against the same words.

## Boundary for Step 2

Step 2 may add non-lexical performance direction. Step 2 may **not** change words, invent a payoff tease, or improvise an audience ask.

Any added, removed, reordered, or rewritten spoken word creates a new script revision and hash, and invalidates this lock. A pronunciation spelling or performance tag may live in the narration layer only if the spoken lexical sequence remains identical.

If Step 2 finds an unperformable or misleading sentence, it issues a change request. Step 1 revises and relocks before narration resumes.
