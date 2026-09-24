# Commands and reproduction

All commands run in this deliverable directory. The installed cached 0.8.36 and 0.8.46 CLI entry points were called directly to avoid writes to external npm caches. `HYPERFRAMES_NO_TELEMETRY=1`, `HYPERFRAMES_RUN_ID=ep007-r64b-title-swap`, and `TMPDIR=<this directory>/tmp` were set for HyperFrames commands. No provider/auth/describe generation was used.

```text
# Read-only upgrade preflight, using currently installed latest 0.8.46:
node /Users/brownmanbrain/.npm/_npx/110f701c48e68d66/node_modules/hyperframes/bin/hyperframes.mjs upgrade --project . --check --json

# Initial checks on both versions (the original final-card color failed contrast):
node /Users/brownmanbrain/.npm/_npx/ea0faf17744cb98d/node_modules/hyperframes/bin/hyperframes.mjs check --strict --at 9,18.8,29.208333,29.291667,45.1 --json
node /Users/brownmanbrain/.npm/_npx/110f701c48e68d66/node_modules/hyperframes/bin/hyperframes.mjs check --strict --at 9,18.8,29.208333,29.291667,45.1 --json

# Corrected final gate:
node /Users/brownmanbrain/.npm/_npx/110f701c48e68d66/node_modules/hyperframes/bin/hyperframes.mjs check --strict --at 0,9,18.8,29.208333,29.25,29.291667,29.5,29.75,45.1 --json

# Apply upgrade only to this isolated candidate after passing check:
node /Users/brownmanbrain/.npm/_npx/110f701c48e68d66/node_modules/hyperframes/bin/hyperframes.mjs upgrade --project . --json

# Representative comparison, one invocation per runtime:
node /Users/brownmanbrain/.npm/_npx/ea0faf17744cb98d/node_modules/hyperframes/bin/hyperframes.mjs snapshot --at 9,18.8,29.25,29.291667,45.1 --no-end --describe false --output qa/stills/runtime-0.8.36
node /Users/brownmanbrain/.npm/_npx/110f701c48e68d66/node_modules/hyperframes/bin/hyperframes.mjs snapshot --at 9,18.8,29.25,29.291667,45.1 --no-end --describe false --output qa/stills/runtime-0.8.46

# Single-worker final render:
node /Users/brownmanbrain/.npm/_npx/110f701c48e68d66/node_modules/hyperframes/bin/hyperframes.mjs render --fps 24 --quality standard --workers 1 --output qa/r64b-s19.mp4

# Original S18 tail + corrected S19 + locked master PCM; verify and extract review stills:
python3 build_and_verify.py
```

Exact FFmpeg/ffprobe arguments from the last command are stored in `qa/ffmpeg-commands.json`. Full CLI evidence is under `qa/logs/`. Re-running the Python script rewrites only this candidate's context and QA outputs; it does not change the original projects.
