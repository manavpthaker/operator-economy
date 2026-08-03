"""
Master VO through Auphonic (adaptive leveler + noise reduction + loudness
normalization + global filtering), then optionally apply a warm-curve
post-pass in ffmpeg to fit Manav's LANDR "Warm/Low" A/B preference.

Reads `originate/<slug>/vo/<section>.dry.mp3` (the raw ElevenLabs output
kept beside every mastered file by generate_vo.py) and writes
`originate/<slug>/vo/<section>.auphonic.mp3`. The primary `<section>.mp3`
is left alone so you can A/B; run with --commit to promote auphonic
output to primary (existing primary backed up to `<section>.legacy.mp3`).

Requires AUPHONIC_API_KEY in env. Free tier gives 2 audio-hours/month —
enough to master ~1 episode of VO end-to-end.

Usage:
    python scripts/originate/master_vo_auphonic.py originate/<slug>/vo/
    python scripts/originate/master_vo_auphonic.py originate/<slug>/vo/ --sections hook
    python scripts/originate/master_vo_auphonic.py originate/<slug>/vo/ --commit
    python scripts/originate/master_vo_auphonic.py originate/<slug>/vo/ --no-warm
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

API = "https://auphonic.com/api"
POLL_INTERVAL_S = 5
POLL_TIMEOUT_S = 600

# Warm-curve post-pass. Runs on the Auphonic output ONLY when --warm is on
# (default). Low-shelf boost adds body, high-shelf tame cuts glare — the
# curve Manav preferred in LANDR "Warm/Low" A/B. Loudness stays flat
# because we do +1.5 / -1 on shelves that mostly balance out; loudnorm
# safety pass at the end keeps -14 LUFS locked either way.
WARM_CHAIN = (
    "equalizer=f=200:t=q:w=1.2:g=1.5,"  # low body
    "equalizer=f=10000:t=q:w=1.4:g=-1.0,"  # tame air glare
    "loudnorm=I=-14:TP=-1.5:LRA=9"
)


def load_env_file() -> None:
    """Mirror generate_avatar.py: studio/.env autoload so this works when
    the shell hasn't sourced it (Cowork runs each call in a fresh shell)."""
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def auth_headers() -> dict:
    key = os.environ.get("AUPHONIC_API_KEY")
    if not key:
        sys.exit("AUPHONIC_API_KEY not set (add to studio/.env)")
    return {"Authorization": f"Bearer {key}"}


def create_and_start(mp3_path: Path, title: str) -> str:
    """Create an Auphonic production with the mp3 uploaded inline and
    algorithms applied, then start it. Returns the production UUID."""
    algorithms = {
        "leveler": True,
        "denoise": True,
        "denoiseamount": 0,      # -1..100, 0 = auto-detected level
        "hipfilter": True,       # global 80Hz highpass
        "loudnesstarget": -14,
        "normloudness": True,
    }
    with mp3_path.open("rb") as fh:
        r = requests.post(
            f"{API}/simple/productions.json",
            headers=auth_headers(),
            data={
                "action": "start",
                "title": title,
                "algorithms": json.dumps(algorithms),
                "output_files": json.dumps([
                    {"format": "mp3", "bitrate": "192", "ending": "mp3"}
                ]),
            },
            files={"input_file": (mp3_path.name, fh, "audio/mpeg")},
            timeout=120,
        )
    if r.status_code >= 300:
        sys.exit(f"Auphonic create failed [{r.status_code}]: {r.text[:400]}")
    return r.json()["data"]["uuid"]


def wait_done(uuid: str, label: str) -> dict:
    """Poll until the production finishes. Auphonic status_string is
    'Done' on success; anything else at timeout is a failure."""
    started = time.time()
    last_status = ""
    while time.time() - started < POLL_TIMEOUT_S:
        r = requests.get(f"{API}/production/{uuid}.json",
                         headers=auth_headers(), timeout=30)
        r.raise_for_status()
        data = r.json()["data"]
        status = data.get("status_string", "?")
        if status != last_status:
            print(f"  [{label}] {status}")
            last_status = status
        if status == "Done":
            return data
        if status in {"Error", "Incomplete Form", "File Transfer Error"}:
            sys.exit(f"Auphonic failed [{label}]: {status} — {data.get('error_message')}")
        time.sleep(POLL_INTERVAL_S)
    sys.exit(f"Auphonic timeout after {POLL_TIMEOUT_S}s [{label}]")


def download_output(prod: dict, dest: Path) -> None:
    outputs = prod.get("output_files") or []
    if not outputs:
        sys.exit(f"No output files on production {prod['uuid']}")
    url = outputs[0]["download_url"]
    r = requests.get(url, headers=auth_headers(), timeout=180, stream=True)
    r.raise_for_status()
    with dest.open("wb") as fh:
        for chunk in r.iter_content(chunk_size=64 * 1024):
            fh.write(chunk)


def apply_warm(src: Path, dst: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
         "-i", str(src), "-af", WARM_CHAIN,
         "-ar", "44100", "-b:a", "192k", str(dst)],
        check=True,
    )


def process_section(dry: Path, warm: bool) -> Path:
    section = dry.name.removesuffix(".dry.mp3")
    out = dry.parent / f"{section}.auphonic.mp3"
    if out.exists():
        print(f"  {section}: cached ({out.name})")
        return out

    print(f"→ {section}: uploading to Auphonic...")
    uuid = create_and_start(dry, title=f"OE / {dry.parent.parent.name} / {section}")
    prod = wait_done(uuid, section)

    if warm:
        raw_out = out.with_suffix(".auphonic.raw.mp3")
        download_output(prod, raw_out)
        apply_warm(raw_out, out)
        raw_out.unlink()
    else:
        download_output(prod, out)

    print(f"  ✓ {section} → {out.name}")
    return out


def commit(vo_dir: Path) -> int:
    """Promote every .auphonic.mp3 to primary .mp3, backing up existing
    primaries to .legacy.mp3 (only once — won't overwrite a legacy)."""
    promoted = 0
    for auph in sorted(vo_dir.glob("*.auphonic.mp3")):
        section = auph.name.removesuffix(".auphonic.mp3")
        primary = vo_dir / f"{section}.mp3"
        legacy = vo_dir / f"{section}.legacy.mp3"
        if primary.exists() and not legacy.exists():
            primary.rename(legacy)
        auph.replace(primary)
        print(f"  ✓ {section}: promoted (legacy kept at {legacy.name})")
        promoted += 1
    return promoted


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("vo_dir", type=Path, help="originate/<slug>/vo/")
    ap.add_argument("--sections", nargs="+",
                    help="section ids to process (default: all *.dry.mp3)")
    ap.add_argument("--no-warm", dest="warm", action="store_false",
                    help="skip warm-curve post-pass (use raw Auphonic output)")
    ap.add_argument("--commit", action="store_true",
                    help="replace primary .mp3 with .auphonic.mp3 after mastering")
    args = ap.parse_args()

    load_env_file()

    if not args.vo_dir.is_dir():
        sys.exit(f"Not a directory: {args.vo_dir}")

    if args.sections:
        drys = [args.vo_dir / f"{s}.dry.mp3" for s in args.sections]
        missing = [d for d in drys if not d.exists()]
        if missing:
            sys.exit(f"Missing dry files: {[str(m) for m in missing]}")
    else:
        drys = sorted(args.vo_dir.glob("*.dry.mp3"))
        if not drys:
            sys.exit(f"No *.dry.mp3 files in {args.vo_dir}")

    print(f"Mastering {len(drys)} section(s) via Auphonic "
          f"(warm-curve post-pass: {'on' if args.warm else 'off'})")
    for dry in drys:
        process_section(dry, warm=args.warm)

    if args.commit:
        print("\nCommitting to primary...")
        n = commit(args.vo_dir)
        print(f"Promoted {n} section(s). Legacy masters kept as *.legacy.mp3.")
    else:
        print("\nA/B ready. Compare:")
        print(f"  existing:  {args.vo_dir}/<section>.mp3")
        print(f"  auphonic:  {args.vo_dir}/<section>.auphonic.mp3")
        print("Promote with:  --commit")


if __name__ == "__main__":
    main()
