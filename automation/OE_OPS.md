# OE_OPS — how the Operator Economy motions run

Governance for the four scheduled motions that brownbot fires inside this repo.
Same architecture as `mp-career-agent/automation/FUNNEL_OPS.md` and
`brown-man-content/automation/GROWTH_OPS.md`.

## The mechanism

`brownbot/src/operator-economy.ts` holds the cron. Each motion is a **headless
Claude Code session** (`claude -p`, Sonnet, `--dangerously-skip-permissions`)
started with `cwd` set to this repo. The prompt body is the matching file in
`automation/prompts/`, **read at fire time** — so editing a prompt here deploys
on the next 5-minute sync, with no brownbot rebuild.

Output is DM'd to Manav over iMessage. A motion whose output ends with
`DIGEST_CLEAR` sends nothing.

| Motion | Cron (ET) | Prompt | Timeout |
|---|---|---|---|
| `oe-weekly-research` | Mon 09:00 | `oe-weekly-research.md` | 55 min |
| `oe-sunday-launch-prep` | Sun 16:00 | `oe-sunday-launch-prep.md` | 55 min |
| `oe-friday-readback` | Fri 16:00 | `oe-friday-readback.md` | 55 min |
| `oe-commit-sweep` | daily 22:00 | `oe-commit-sweep.md` | 10 min |

On demand from the phone: "run oe-friday-readback" — brownbot's `run_motion`
tool starts it and the digest arrives when it finishes.

Kill switch: `OE_ENABLED=false` in brownbot's `.env`. Note that
`brownbot/AUTOMATIONS_OFF` also suppresses all four (it skips the scheduler
entirely); `run_motion` still works while that sentinel is present.

## The rules every prompt inherits

1. **State the resolved date/week in the first line of output.** A stale run
   must be obvious. A prompt hardcoded to a dead week ran wrong for five weeks
   before anyone noticed.
2. **Commit and push before finishing.** This repo is in brownbot's
   `CONTENT_REPOS`, which pulls `--ff-only` every 5 minutes. A motion that
   leaves the tree dirty **deadlocks the deploy loop for every repo behind
   it**, and stamps `sync_last_error` into the doctor. Work that isn't
   committed doesn't exist.
3. **`content-os` is the authority on facts, voice, rubric, and flow.** Read
   `../content-os/facts.md` before writing anything public. If that repo is not
   present on this machine yet, say so in the digest and do not invent numbers.
4. **No em dashes. No hype lexicon.** `brand/brand.md` and
   `../content-os/voice.md` govern.
5. **Never publish, never spend, never message anyone but Manav.** Publishing
   is owned by YouTube's and LinkedIn's native schedulers. These motions
   originate, pre-flight, read back, and commit.
6. **Escalate rather than guess.** A confidence score below threshold or a hard
   trigger is a reportable outcome, not something to work around.
7. **End with `DIGEST_CLEAR` when there is genuinely nothing to report.** A
   quiet success is the normal case for the commit sweep.
8. **Never invoke bare `python` or `python3`.** See below — it will be the wrong
   interpreter and nothing will be installed in it.

## Python on the mini

The pipeline runs in a **uv-managed CPython 3.12 virtualenv at `.venv/`**
(gitignored). Recreate it with:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r studio/requirements.txt
```

**Always call it explicitly.** Your cwd is the repo root, so that is
`.venv/bin/python`; if you `cd studio`, it is `../.venv/bin/python`.

This is not a style preference. brownbot is started by launchd with
`PATH=/usr/bin:/bin:/usr/sbin:/sbin`, which excludes Homebrew, so a bare
`python3` in a motion resolves to Apple's `/usr/bin/python3` (3.9.6) where none
of the dependencies exist. It is the same reason `CLAUDE_CODE_BIN` and
`CLICLICK_BIN` are pinned by absolute path on the brownbot side.

Homebrew's `python@3.14` on this machine is **broken** — its `pyexpat` links
against a `/usr/lib/libexpat.1.dylib` newer than the one macOS actually ships, so
`ensurepip`/`pip` cannot run at all. Do not try to fix a motion by falling back
to it.

## Required environment

Read from this repo's own `.env` (gitignored, copied to the mini by hand):
`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, and optionally
`PEXELS_API_KEY` / `AUPHONIC_API_KEY`. YouTube uses `.secrets/token.json` from
`python tools/youtube_auth.py`, not an env var.
