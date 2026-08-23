# Step 1 porting manifest

Status: approved V2 Step 1 v1.5 port record. No V1 files copied. V1.4 and earlier versions remain frozen history.

## Decision

Step 1 uses a routing map rather than duplicating V1 editorial files.

Reasons:

- Content OS facts and editorial-voice rules are live authority and should not drift through copies.
- `studio/config/speech-profile.md` is the live observed Manav spoken-language authority and should not drift through a copy.
- The V1 video rubric combines script, packaging, visuals, editing, and publishing concerns.
- The V1 blueprint configuration hard-codes a structure that Step 1 is explicitly reconsidering.
- The V1 VO-first document mixes the durable lock order with a superseded coverage workflow.
- Executable scripts are implementation references, not documentation authority.

The committed V1 identities, hashes, useful concepts, and exclusions are recorded in [`REFERENCE-MAP.md`](REFERENCE-MAP.md).

## Copied sources

None.

## Not ported

- Episode-specific scripts, research, reviews, or voice files.
- Generated JSON, media, transcripts, or renders.
- Title, thumbnail, Shorts, visual, edit, or publishing material.
- Voice-provider and audio-toolchain configuration.
- V1 executable code.
- Blueprint Cinema, HyperFrames, Remotion, or Resolve production instructions.

## Future additions

Any future copy must record source path, source commit when applicable, destination, SHA-256, reason, authority status, and known stale assumptions. A copied reference remains reference-only unless separately approved as V2 authority.

## Approved v1.5 live-authority routing

| Linked source | SHA-256 reviewed for regression | Step 1 use | Explicit exclusion |
| --- | --- | --- | --- |
| `studio/config/speech-profile.md` | `75913da0bc5d5b360c88f18c70b60d8d4af14128184e8164872edd56f71ceddc` | Observed sentence mechanics, vocabulary, conversational moves, and phrasing applied before script lock. | Voice ID, vocal timbre, provider model, generation settings, audio processing, and permission to introduce new facts. |

`content-os/voice.md` remains linked live authority; approved hosted-long-form SHA-256 reviewed for the v1.5 lock: `ec65d503a9973ec77919ca8edf37d37f18e6762c696d931690a86b179017574a`.

`content-os/rubric.md` remains linked live written-surface routing authority. It explicitly excludes Operator Blueprint V2 video scripts and routes them to the approved Step 1 controls. SHA-256 reviewed for the v1.5 lock: `41f4468128061205285313e9cff6815d682e0e4bbe278a82697b3c700ba697fa`.

`SCRIPT-BEAT-RESEARCH.md`, `VOICE-ARCHITECTURE.md`, and `04-narrative/EPISODE-INVESTMENT-THESIS.template.md` are newly authored V2 authority, not ports. The first two apply the reported-explainer craft review to the V2 long-form register while preserving Content OS truth rules and the studio speech profile's observed Manav mechanics. The Episode Investment Thesis contract adds the approved Gate E3I route between the locked Canvas and narrative development. It separates the complete company from its first offer, records the short spoken name and precise operating definition, and requires an evidence-safe BUILD verdict without creating a public claim or downstream production authority.
