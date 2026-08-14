#!/usr/bin/env python3
"""Originate: one way to reach a model, for every script that needs one.

Why this exists (2026-08-13). The key in .env went stale and returned 401, and
that took the whole pipeline down -- on a machine already signed in to Claude
Code, where the shell alias is literally `env -u ANTHROPIC_API_KEY claude`
because the account is the intended auth path. Nothing but these scripts
insisted on a key.

They also disagreed about where a key comes from. thumbnail_spec.py and
derive_thumbnail_prompt.py read .env; generate_script.py, derive_content.py,
plan_assets.py and storyboard.py read only os.environ, so with nothing exported
they were broken before the key ever expired. That is now one function.

Order is: a working API key, else the signed-in CLI. A REJECTED key falls
through rather than being fatal -- a stale string in .env should not outrank a
signed-in machine.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

# parents[2] is studio/, not the repo root — .env sits one level above it.
REPO = Path(__file__).resolve().parents[3]


class ModelError(RuntimeError):
    pass


def env_key(name: str) -> str | None:
    """A credential from the environment, falling back to the repo .env.

    Generalised from anthropic_key() on 2026-08-14, when EP006 could not generate
    voiceover: generate_vo.py read ELEVENLABS_API_KEY from os.environ only, and
    nothing exports it. The key was sitting in .env the whole time. That is the
    same defect four Anthropic scripts had — worth one function rather than five
    copies of the same lookup.
    """
    key = os.environ.get(name)
    if not key and (REPO / ".env").exists():
        for line in (REPO / ".env").read_text().splitlines():
            if line.startswith(f"{name}="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    return key or None


def anthropic_key() -> str | None:
    """The API key from the environment or .env, or None. None is not fatal."""
    return env_key("ANTHROPIC_API_KEY")


def cli_available() -> bool:
    """Whether the `claude` binary is on PATH at all."""
    return subprocess.run(["which", "claude"], capture_output=True).returncode == 0


def complete_via_cli(system: str, user: str, model: str, timeout: int = 900) -> str:
    """Run the prompt through the `claude` CLI on the ACCOUNT's auth.

    Stripping ANTHROPIC_API_KEY from the child environment is load-bearing, not
    decoration. A subprocess inherits our environment, so a present-but-invalid
    key would be picked straight back up by the CLI and 401 a second time. The
    user's shell alias does this for interactive use; a subprocess never sees a
    shell alias, so it is done explicitly here.
    """
    if not cli_available():
        raise ModelError(
            "no usable ANTHROPIC_API_KEY and no `claude` on PATH. Either put a "
            "working key in .env or sign in with `claude`.")
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    p = subprocess.run(
        # --tools "" is not tidiness. Without it the nested CLI will sometimes
        # decide it wants a tool, hit a permission prompt it cannot answer
        # headlessly, and return "The command needs your approval before I..."
        # as though that were the model's reply. These calls are pure text in,
        # text out; no tool should ever be reachable.
        ["claude", "-p", user, "--append-system-prompt", system,
         "--model", model, "--tools", "", "--output-format", "text"],
        capture_output=True, text=True, env=env, timeout=timeout)
    if p.returncode != 0:
        raise ModelError(
            f"claude CLI failed (rc={p.returncode}). Either sign in with "
            f"`claude` or put a working key in .env.\n  {p.stderr.strip()[-400:]}")
    out = p.stdout.strip()
    if not out:
        raise ModelError("claude CLI returned nothing")
    return out


def complete_json(system: str, user: str, model: str, max_tokens: int = 8000) -> dict:
    """complete(), for callers that need JSON back.

    The CLI path narrates. Asked for strict JSON it will still sometimes open
    with a sentence about what it did — on EP006 it prefaced a clean object with
    a note about file reads timing out, referencing a path that does not exist.
    A caller that only strips code fences gets a JSONDecodeError and blames the
    prompt. So the object is extracted rather than assumed to start at index 0.
    """
    import json as _json
    import re as _re
    text = complete(system, user, model, max_tokens=max_tokens)
    text = _re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=_re.M).strip()
    try:
        return _json.loads(text)
    except _json.JSONDecodeError:
        m = _re.search(r"\{[\s\S]*\}", text)
        if not m:
            raise ModelError(f"no JSON object in model output; got: {text[:400]!r}")
        return _json.loads(m.group(0))


def complete(system: str, user: str, model: str, max_tokens: int = 8000,
             quiet: bool = False) -> str:
    """Return the model's text for one system+user turn, by whichever route works."""
    key = anthropic_key()
    if key:
        try:
            import anthropic
        except ImportError:
            raise ModelError("pip install anthropic")
        try:
            msg = anthropic.Anthropic(api_key=key).messages.create(
                model=model, max_tokens=max_tokens, system=system,
                messages=[{"role": "user", "content": user}])
            text = "".join(b.text for b in msg.content
                           if getattr(b, "type", "") == "text").strip()
            if not text:
                raise ModelError(
                    f"no text block (stop_reason={msg.stop_reason}, "
                    f"blocks={[getattr(b,'type','?') for b in msg.content]})")
            return text
        except anthropic.AuthenticationError:
            if not quiet:
                print("  ANTHROPIC_API_KEY rejected; falling back to the claude CLI")
    return complete_via_cli(system, user, model)
