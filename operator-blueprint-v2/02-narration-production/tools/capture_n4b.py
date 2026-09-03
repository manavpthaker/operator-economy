#!/usr/bin/env python3
"""N4B full-capture executor for a locked V2 episode.

Two-stage acted-guide chain frozen at N3 as `n3-two-stage-acted-guide-v2`:
  stage 1  Google Cloud TTS `gemini-2.5-pro-tts`, voice Algieba, candidate-C4 register
  stage 2  ElevenLabs Voice Changer `eleven_multilingual_sts_v2` onto Original C

Provider request shapes, credentials, probing and tail-energy detection are
imported from `calibrate.py` so the capture is byte-for-byte the same request
family that passed N4A. What this file adds is the N4B contract:

  * chunks are grouped on Step 1 narration-block (scene) boundaries, never
    splitting a block unless it alone exceeds the provider ceiling, with the
    F2 short-tail merge;
  * the exact locked words are verified against `canonical-w.txt` before any
    call is made (whitespace tokens of all narration blocks == W);
  * every chunk must decay into silence (tail energy < 0.02) at BOTH stages;
    a chunk that does not is regenerated, up to --max-attempts times, because
    provider truncation is stochastic;
  * every raw file is immutable once accepted, hashed, and registered in
    `take-register.json` in the EP007 shape;
  * the run is resumable: a chunk with both accepted files on disk is reused,
    never re-billed.

Nothing here calls a provider without --execute.

Usage:
  capture_n4b.py --episode-dir operator-blueprint-v2/episodes/EP008-... [--execute]
                 [--only-chunk N] [--max-chars 1250] [--max-attempts 4]
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import calibrate as cal  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[3]
STYLE = REPO / "operator-blueprint-v2/02-narration-production/prompts/NARRATOR-REGISTER.candidate-C4.google-gemini-tts.style-instructions.json"
CONFIG_ID = "n3-two-stage-acted-guide-v2"
GUIDE_VOICE = "Algieba"
MIN_TAIL_CHARS = int(cal.MIN_TAIL_SECONDS * cal.CHARS_PER_SECOND)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# --- locked words -----------------------------------------------------------

_SCENE = re.compile(r"^## (S\d+[^:\n]*):", re.M)


def narration_blocks(script_path: pathlib.Path) -> list[tuple[str, str]]:
    """Return [(scene_id, exact narration text)] in script order.

    A scene's narration is the text under its `### Narration` heading up to the
    next `###` or `##` heading. Scenes with no narration (the silent sting) are
    skipped. Paragraph breaks are preserved as single blank lines.
    """
    text = script_path.read_text(encoding="utf-8")
    blocks: list[tuple[str, str]] = []
    positions = [(m.start(), m.group(1)) for m in _SCENE.finditer(text)]
    for i, (start, sid) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        body = text[start:end]
        m = re.search(r"^### Narration\s*\n(.*?)(?=^###? |\Z)", body, re.S | re.M)
        if not m:
            continue
        narration = m.group(1).strip()
        if narration and narration.lower() != "none":
            blocks.append((sid, narration))
    return blocks


def verify_against_w(blocks: list[tuple[str, str]], w_path: pathlib.Path) -> tuple[int, str]:
    tokens = [t for _, n in blocks for t in n.split()]
    w = w_path.read_text(encoding="utf-8").split("\n")
    if w and w[-1] == "":
        w.pop()
    if tokens != w:
        n = next((i for i, (a, b) in enumerate(zip(tokens, w)) if a != b), min(len(tokens), len(w)))
        sys.exit(f"error: narration blocks do not reproduce canonical W at token {n}: "
                 f"{tokens[n:n+3]!r} vs {w[n:n+3]!r} (counts {len(tokens)} vs {len(w)})")
    return len(w), sha(w_path.read_bytes())


# --- chunking ----------------------------------------------------------------

def split_block(sid: str, narration: str, max_chars: int) -> list[tuple[str, str]]:
    """Split one over-ceiling block into .1/.2/... parts on sentence ends.

    Parts are balanced (target = len / ceil(len / max_chars)) so that no part
    lands near the provider ceiling and no isolated short tail is produced.
    """
    import math
    sentences = cal.split_sentences(narration)
    n_parts = max(2, math.ceil(len(narration) / max_chars))
    target = len(narration) / n_parts
    parts: list[str] = []
    current = ""
    for sentence in sentences:
        candidate = f"{current} {sentence}".strip()
        remaining = n_parts - len(parts)
        if current and remaining > 1 and len(candidate) > target:
            parts.append(current)
            current = sentence
        else:
            current = candidate
    if current:
        parts.append(current)
    if len(parts) > 1 and len(parts[-1]) < MIN_TAIL_CHARS:
        parts[-2] = f"{parts[-2]} {parts[-1]}"
        parts.pop()
    if any(len(x) > max_chars for x in parts):
        return split_block(sid, narration, max_chars - 100) if max_chars > 600 else [(f"{sid}.{i}", x) for i, x in enumerate(parts, 1)]
    return [(f"{sid}.{i}", p) for i, p in enumerate(parts, 1)]


RESPLIT: dict[str, int] = {}  # scene id -> forced part count, set from --resplit


def plan_chunks(blocks: list[tuple[str, str]], max_chars: int) -> list[dict]:
    """Group whole blocks into chunks <= max_chars; a scene boundary is always
    a legal chunk boundary; a block over the ceiling is split by sentence.
    A scene named in RESPLIT is split into that many balanced parts regardless
    of length, so a passage that truncates reliably can end on a different
    sentence without touching any word."""
    units: list[tuple[str, str]] = []
    for sid, narration in blocks:
        if sid in RESPLIT:
            n = RESPLIT[sid]
            import math
            units.extend(split_block(sid, narration, max(300, math.ceil(len(narration) / n))))
        elif len(narration) > max_chars:
            units.extend(split_block(sid, narration, max_chars))
        else:
            units.append((sid, narration))
    chunks: list[dict] = []
    cur_ids: list[str] = []
    cur_text = ""
    for sid, text in units:
        joined = f"{cur_text}\n\n{text}".strip() if cur_text else text
        if cur_text and len(joined) > max_chars:
            chunks.append({"scenes": "+".join(cur_ids), "text": cur_text})
            cur_ids, cur_text = [sid], text
        else:
            cur_ids.append(sid)
            cur_text = joined
    if cur_text:
        chunks.append({"scenes": "+".join(cur_ids), "text": cur_text})
    if len(chunks) > 1 and len(chunks[-1]["text"]) < MIN_TAIL_CHARS:
        last = chunks.pop()
        chunks[-1]["scenes"] += "+" + last["scenes"]
        chunks[-1]["text"] = f"{chunks[-1]['text']}\n\n{last['text']}"
    for i, c in enumerate(chunks, 1):
        c["chunk"] = i
        c["chars"] = len(c["text"])
        c["text_sha256"] = sha(c["text"].encode("utf-8"))
    return chunks


# --- provider stages -----------------------------------------------------------

def guide_once(text: str, style: str, headers: dict[str, str], retries: int = 2) -> tuple[int, bytes]:
    body = cal.compact_json(cal.guide_body(text, style, GUIDE_VOICE))
    status, payload = cal.post(cal.GUIDE_ENDPOINT, body, headers)
    attempt = 0
    while status in (502, 503, 429) and attempt < retries:
        attempt += 1
        time.sleep(3 * attempt)
        status, payload = cal.post(cal.GUIDE_ENDPOINT, body, headers)
    return status, payload


def transfer_once(guide_path: pathlib.Path, api_key: str) -> tuple[int, bytes]:
    fields = {
        "model_id": cal.TRANSFER_MODEL,
        "remove_background_noise": "false",
        "seed": str(cal.TRANSFER_SEED),
        "voice_settings": json.dumps(cal.TRANSFER_VOICE_SETTINGS, sort_keys=True),
        "file_format": "other",
    }
    body, content_type = cal.multipart(fields, guide_path.name, guide_path.read_bytes())
    url = f"{cal.TRANSFER_ENDPOINT}?output_format={cal.TRANSFER_OUTPUT_FORMAT}&enable_logging=true"
    return cal.post(url, body, {"xi-api-key": api_key, "Content-Type": content_type, "Accept": "*/*"})


def accepted(path: pathlib.Path) -> bool:
    return path.is_file() and path.stat().st_size > 1000 and cal.tail_energy(path) < cal.TAIL_ENERGY_THRESHOLD


# --- main ---------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--episode-dir", required=True)
    ap.add_argument("--execute", action="store_true", help="actually call the providers (spends credits)")
    ap.add_argument("--only-chunk", type=int, default=None)
    ap.add_argument("--max-chars", type=int, default=cal.MAX_GUIDE_CHARS)
    ap.add_argument("--max-attempts", type=int, default=4, help="regenerations per stage when a chunk does not decay into silence")
    ap.add_argument("--resplit", action="append", default=[], metavar="SCENE:N",
                    help="force scene SCENE into N balanced parts (e.g. S17:3); recorded in the take register")
    ap.add_argument("--stage", choices=("both", "guides", "transfers"), default="both",
                    help="guides: Google stage only; transfers: ElevenLabs stage only, reusing accepted guides")
    args = ap.parse_args()

    ep_dir = pathlib.Path(args.episode_dir).resolve()
    episode = ep_dir.name.split("-")[0]
    # a re-split recorded in the take register is part of the plan; reuse it so a
    # later stage never re-plans the chunks differently from the accepted guides
    prior = ep_dir / "02-narration-production" / "take-register.json"
    if prior.is_file():
        RESPLIT.update({k: int(v) for k, v in (json.loads(prior.read_text()).get("resplit") or {}).items()})
    for item in args.resplit:
        s, n = item.split(":")
        RESPLIT[s] = int(n)
    ed = ep_dir / "01-editorial"
    nd = ep_dir / "02-narration-production"
    raw = nd / "raw"
    script = ed / "script.md"
    w_path = ed / "canonical-w.txt"
    lock = ed / "editorial-lock.md"
    for p in (script, w_path, lock):
        if not p.is_file():
            sys.exit(f"error: missing {p}")
    if "Status: **LOCKED**" not in lock.read_text(encoding="utf-8"):
        sys.exit("error: editorial lock is not LOCKED; N4B may not run")

    blocks = narration_blocks(script)
    w_count, w_sha = verify_against_w(blocks, w_path)
    base_style, label, aliases = cal.load_style(STYLE)
    chunks = plan_chunks(blocks, args.max_chars)

    print(f"[{episode}] {len(blocks)} narration blocks, W={w_count} sha {w_sha[:12]}, "
          f"{len(chunks)} chunks at <={args.max_chars} chars, register {label}")
    for c in chunks:
        style = cal.compose_style(base_style, aliases, c["text"])
        c["style_sha256"] = sha(style.encode("utf-8"))
        print(f"  c{c['chunk']:02d} {c['scenes']:<22} {c['chars']:>5} chars  ~{c['chars']/cal.CHARS_PER_SECOND:5.1f}s")
    est = sum(c["chars"] for c in chunks) / cal.CHARS_PER_SECOND
    print(f"  estimated speech {est/60:.1f} min; provider calls {2*len(chunks)} minimum")
    if not args.execute:
        print("  DRY RUN - no calls made. Re-run with --execute.")
        return 0

    raw.mkdir(parents=True, exist_ok=True)
    reg_path = nd / "take-register.json"
    register = json.loads(reg_path.read_text()) if reg_path.is_file() else {
        "episode": episode, "config": CONFIG_ID, "guide_voice": GUIDE_VOICE, "register": label,
        "canonical_w_sha256": w_sha, "w_token_count": w_count,
        "style_file_sha256": sha(STYLE.read_bytes()), "chunks": [],
    }
    if RESPLIT:
        register["resplit"] = dict(RESPLIT)
    elif register.get("resplit"):
        RESPLIT.update({k: int(v) for k, v in register["resplit"].items()})
    by_chunk = {c["chunk"]: c for c in register["chunks"]}

    token = cal.google_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"}
    project = cal.google_quota_project()
    if project:
        headers["x-goog-user-project"] = project
    api_key = cal.read_dotenv_key("ELEVENLABS_API_KEY")

    calls = {"google": 0, "elevenlabs": 0}
    for c in chunks:
        i = c["chunk"]
        if args.only_chunk and i != args.only_chunk:
            continue
        gp = raw / f"c{i:02d}.guide.wav"
        tp = raw / f"c{i:02d}.saved-c.wav"
        rec = by_chunk.get(i)
        same_text = bool(rec) and rec.get("text_sha256") == c["text_sha256"]
        if same_text and accepted(gp) and accepted(tp):
            print(f"  c{i:02d} reused (both stages accepted on disk)")
            continue
        if args.stage == "guides" and same_text and accepted(gp):
            print(f"  c{i:02d} guide reused")
            continue
        style = cal.compose_style(base_style, aliases, c["text"])
        # stage 1: guide, regenerate until it decays into silence
        g_attempts = list(rec.get("guide_attempt_tail_energy", [])) if same_text else []
        guide_ok = same_text and accepted(gp)
        if args.stage == "transfers" and not guide_ok:
            print(f"  c{i:02d} no accepted guide on disk; run --stage guides first")
            continue
        for attempt in range(1, (0 if guide_ok else args.max_attempts) + 1):
            status, payload = guide_once(c["text"], style, headers)
            calls["google"] += 1
            if status != 200:
                print(f"  c{i:02d} guide HTTP {status}: {payload[:300].decode('utf-8','replace')}")
                print("  aborting; completed chunks are kept, re-run to resume")
                _save(reg_path, register, calls)
                return 1
            gp.write_bytes(base64.b64decode(json.loads(payload)["audioContent"]))
            os.chmod(gp, 0o600)
            te = cal.tail_energy(gp)
            g_attempts.append(round(te, 4))
            if te < cal.TAIL_ENERGY_THRESHOLD:
                break
            print(f"  c{i:02d} guide attempt {attempt}: tail energy {te:.3f} (still sounding), regenerating")
        else:
            if not guide_ok:
                print(f"  c{i:02d} guide never decayed into silence after {args.max_attempts} attempts; stopping for review")
                _save(reg_path, register, calls)
                return 1
        if args.stage == "guides":
            gi = cal.probe(gp)
            by_chunk[i] = {
                "chunk": i, "scenes": c["scenes"], "chars": c["chars"],
                "text_sha256": c["text_sha256"], "style_sha256": c["style_sha256"],
                "guide_attempt_tail_energy": g_attempts,
                "guide": gi | {"path": str(gp.relative_to(REPO))},
            }
            register["chunks"] = [by_chunk[k] for k in sorted(by_chunk)]
            _save(reg_path, register, calls)
            print(f"  c{i:02d} {c['scenes']:<22} guide {gi['duration_seconds']:6.1f}s  tail {gi.get('tail_energy')}  sha {gi['sha256'][:12]}")
            continue
        # stage 2: transfer, same rule
        t_attempts = []
        for attempt in range(1, args.max_attempts + 1):
            status, audio = transfer_once(gp, api_key)
            calls["elevenlabs"] += 1
            if status != 200:
                print(f"  c{i:02d} transfer HTTP {status}: {audio[:300].decode('utf-8','replace')}")
                _save(reg_path, register, calls)
                return 1
            cal.wav_from_pcm(audio, cal.TRANSFER_OUTPUT_RATE_HZ, tp)
            os.chmod(tp, 0o600)
            te = cal.tail_energy(tp)
            t_attempts.append(round(te, 4))
            if te < cal.TAIL_ENERGY_THRESHOLD:
                break
            print(f"  c{i:02d} transfer attempt {attempt}: tail energy {te:.3f}, regenerating transfer")
        else:
            print(f"  c{i:02d} transfer never decayed into silence; stopping for review")
            _save(reg_path, register, calls)
            return 1
        gi, ti = cal.probe(gp), cal.probe(tp)
        rec = {
            "chunk": i, "scenes": c["scenes"], "chars": c["chars"],
            "text_sha256": c["text_sha256"], "style_sha256": c["style_sha256"],
            "guide_attempt_tail_energy": g_attempts, "transfer_attempt_tail_energy": t_attempts,
            "guide": gi | {"path": str(gp.relative_to(REPO))},
            "transfer": ti | {"path": str(tp.relative_to(REPO))},
        }
        by_chunk[i] = rec
        register["chunks"] = [by_chunk[k] for k in sorted(by_chunk)]
        _save(reg_path, register, calls)
        print(f"  c{i:02d} {c['scenes']:<22} guide {gi['duration_seconds']:6.1f}s -> transfer {ti['duration_seconds']:6.1f}s  "
              f"tail {ti.get('tail_energy')}  sha {ti['sha256'][:12]}")
    print(f"  done: google calls {calls['google']}, elevenlabs calls {calls['elevenlabs']}")
    return 0


def _save(reg_path: pathlib.Path, register: dict, calls: dict) -> None:
    register.setdefault("provider_calls", {"google": 0, "elevenlabs": 0})
    register["provider_calls"]["google"] += calls["google"]
    register["provider_calls"]["elevenlabs"] += calls["elevenlabs"]
    calls["google"] = calls["elevenlabs"] = 0
    reg_path.write_text(json.dumps(register, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
