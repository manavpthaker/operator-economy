# BC-REHEARSAL-001 preflight

## Identity and scope

- Experiment: `BC-REHEARSAL-001-missed-call-recovery`
- Canonical repository: `/Users/brownmanbrain/GitHub/operator-economy`
- Lightweight shell explicitly rejected: `/Users/brownmanbrain/Documents/GitHub/operator-economy`
- Output boundary: this experiment folder only
- Format: 1920×1080, 30 fps, 60–75 seconds
- Synthetic-only: yes; never publishable as an episode or claim

## Starting repository state

- Branch: `ep006-rev-e-redesign`
- Upstream relation: `origin/ep006-rev-e-redesign`, ahead 16
- Pre-existing modified or staged paths: 52
- Pre-existing untracked path entries: 20
- The populated checkout was already dirty, including valuable EP006, documentation, renderer, and Blueprint Cinema scaffold work.
- This rehearsal does not modify, move, reset, delete, or reinterpret any of that work.

## Authority read

The repository, content-os, Blueprint Cinema canon, direction/shot/asset/finish/review references, and every episode template required by the rehearsal were read completely before authoring. Blueprint Cinema direction overrides generic HyperFrames creative defaults where they conflict.

## Toolchain found

| Tool | Version or identity | Result |
| --- | --- | --- |
| Node.js | `v25.6.1` | pass; exceeds HyperFrames 22+ requirement |
| HyperFrames CLI | `0.8.4` | pass; project will pin this exact version |
| FFmpeg / ffprobe | `8.1.1` | pass |
| macOS voice | `/usr/bin/say`, Samantha, 150 words/minute | pass; local/offline |
| whisper.cpp | `1.8.5`, `small.en`, DTW enabled, flash attention disabled | pass; local cached model |
| OS | macOS 26.2, build 25C56 | recorded |

`npx hyperframes skills update general-video` completed as a no-op: installed skills were already current. HyperFrames preference and recipe probes returned no remembered defaults and no recipes. No external media provider is required.

## Implemented boundary

Blueprint Cinema v2 defines this production team and handoff, but the shared v1 CLI/state/schema runtime does not enforce the v2 direction, HyperFrames, or Resolve contracts. This rehearsal therefore implements only experiment-local contracts and checks. It will report those as manually assembled or experiment-local machine-enforced; it will not claim shared production implementation.

## Clean-room exclusions

The rehearsal does not read, copy, import, or reference any real episode visual decision, including EP006 storyboard/visual-plan/render-data files, Remotion components, legacy frames, pilots, or existing renders. It uses only the user-provided synthetic narration, locally generated synthetic VO/timings, the approved Blueprint Cinema canon/templates, and OE brand tokens/font binaries.

## Go / no-go

`GO`: a 61.411-second local VO and a defensible 158-word alignment were produced. Direction may proceed from the locked timing authority.
