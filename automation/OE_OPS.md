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

## Verified pipeline reference

Checked against the actual CLIs on 2026-08-09, because the first draft of these
prompts was written from the docs and got several of these wrong. Re-verify with
`--help` before changing a prompt; do not trust prose (including this file).

**Entry points.** `originate.py {new,continue,render,finalize}`:

| Subcommand | Signature |
|---|---|
| `new` | `originate.py new "<topic>" [--research FILE]` — stops at Gate 1 |
| `continue` | `originate.py continue <slug>` — VO + asset plan, stops at Gate 2 |
| `render` | `originate.py render <slug> [--skip-derive]` — render data + derived content |
| `finalize` | `originate.py finalize <slug> [--input MP4] [--no-grade] [--no-master]` — post-Remotion colour grade + loudness master |

**`launch.py` — the two traps.**

```
launch.py <slug> --monday YYYY-MM-DD --title "..." [--video MP4] [--go] [--rubric-waiver REASON]
```

1. **There is no `--dry-run`.** Dry run is the default; `--go` is what uploads.
   Passing `--dry-run` is an argparse error, not a safe no-op.
2. **A dry run still writes `originate/<slug>/launch/links.json`**, with
   `episode_url: "[PENDING_UPLOAD]"` and `dry_run: true`. Since `links.json` is
   the only sanctioned home for an episode URL, running it against a launched
   episode destroys that URL. Check the existing file's `dry_run` field first.

`launch.py` rubric-lints `content/launch_linkedin.md`,
`content/linkedin_posts.md` and `content/trailer_linkedin.md` internally and
hard-fails on a violation. It shells out with `sys.executable`, so it stays
inside the venv.

**`rubric_check.py` is not an episode gate.** It is a LinkedIn copy linter:
`rubric_check.py [--surface {feed,carousel,dm,group}] <file>`. Do not invoke it
standalone in a pre-flight.

**Exit codes are verdicts.**

| Script | 0 | 1 | 2 |
|---|---|---|---|
| `eval_script.py` | pass (a `[WARN]` does not fail) | hard fail (e.g. surviving `[POV: ...]`) | — |
| `eval_package.py` | pass | fail | — |
| `confidence.py` | AUTO-PASS | — | **ESCALATE** |

A `2` from `confidence.py` is a normal outcome to report, not a crash to fix.

**Per-episode artifact paths** (what `launch.py` actually globs):

```
originate/<slug>/ep*-final.mp4              episode
originate/<slug>/ep*.srt                    captions
originate/<slug>/render_out/short-*.mp4     shorts (fallback: <slug>/shorts/)
originate/<slug>/Operator-Blueprint-*.pdf   blueprint
originate/<slug>/carousel-*.pdf             carousel
originate/<slug>/thumbnail-*.png            thumbnail
originate/<slug>/content/*.md               derived copy
originate/<slug>/launch/{checklist.md,links.json,dm_shortlist.md}
```

Note the blueprint PDF lives in the episode directory, **not** in
`site/public/blueprints/` — that is the published copy, a later step.

**Committed `links.json` files carry absolute paths under
`/Users/manavthaker/…`**, the MacBook's home. They do not resolve on the mini
(`/Users/brownmanbrain/…`). Regenerating on the mini writes mini paths, so
anything consuming `blueprint_pdf` / `carousel_pdf` across machines should treat
them as advisory.

## Required environment

Read from this repo's own `.env` (gitignored, copied to the mini by hand):
`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, and optionally
`PEXELS_API_KEY` / `AUPHONIC_API_KEY`. YouTube uses `.secrets/token.json` from
`python tools/youtube_auth.py`, not an env var.
