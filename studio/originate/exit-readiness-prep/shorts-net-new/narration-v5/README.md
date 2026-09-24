# EP007 Short 02 — one-guide continuation (not authorized yet)

This directory contains a guide-only, no-retry runner. It does not continue the stopped
`narration-v3` batch and cannot make an Original C transfer, avatar, lip-sync, render,
release, upload or publication call. The accepted Short 01 voice process is precedent,
not permission to reuse its audio or spend cap.

`capture_short02_guide.py check` performs a local, read-only hash and request check.
`preflight` and `submit` require two *existing* files under the EP007 decisions
directory: a fresh owner source record and the matching owner/accept feedback event
that has been appended to `events.jsonl`. Neither file is supplied by this directory.
Run either with `--owner-source <path> --owner-event <path>` only after the owner
answers the already-presented one-guide question affirmatively.

The source record must preserve that question verbatim, the owner's verbatim affirmative
answer, a capture time after the accepted avatar-route event, and exact `authorized`
fields required by the runner: Short 02 ID, locked script/request/body hashes, one
Google `gemini-2.5-pro-tts` Algieba guide, a $0.05 *operational forecast* ceiling,
zero automatic/manual retries and guide-only scope. Its `not_authorized` list must
retain Original C transfer, avatar generation, lip-sync, render, release, upload and
publication. The event must match that answer and authorization, carry the source
and exact input hashes, and pass the episode decision-log chain check. A route choice,
old four-Short narration cap, or generic “keep going” cannot satisfy this gate.

The runner checks credentials before writing its exclusive intent, then writes that
intent **before** the one provider POST. It preserves the full raw response in a
private local file and emits only a small status, never credentials or provider
payloads, to stdout. Once an intent exists, no invocation can submit again. Failed,
uncertain, malformed, over-cap or high-tail outcomes create a hold without retry.
High tail energy preserves the original guide for listening; it is not auto-padded,
discarded or transferred. Even a technically clean guide remains pending exact-copy
ASR and owner listening. No provider-side monetary limiter is claimed: actual output
duration and final Google billing remain separately measurable.
