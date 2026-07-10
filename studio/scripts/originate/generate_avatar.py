"""
Originate Step 2b: Generate lip-synced avatar clips (HeyGen) from section VO.

Reads the approved script.json + the per-section VO already produced by
generate_vo.py and, for each configured section, submits the section's
mastered MP3 to HeyGen's audio-driven avatar endpoint. The result is one
MP4 per configured section — Manav's digital twin speaking that section's
VO — which prepare_longform.py threads into render_data and the Remotion
Blueprint composition renders as a corner block.

Decision context: docs/avatar-decision.md. The face block covers the
hook + direct-address sections only, not the whole runtime. Disclosure:
compliance.ai_disclosure already covers synthetic VO; avatar clips fall
under the same checked box at upload (Gate 3).

Resumable per section (Cowork 45s shell cap safe):
  - avatars/<section>.mp4 exists          -> skipped entirely
  - avatars/jobs.json holds submitted ids -> re-run only polls/downloads
  Run repeatedly until all sections report done; every run is idempotent.

Usage:
    python scripts/originate/generate_avatar.py originate/<slug>/script.json
    ... [--sections hook,cta] [--poll-timeout 600] [--submit-only]

Config (config/blueprint.json -> "avatar"):
    enabled     false = exit 0 no-op (originate.py always calls this step)
    avatar_id   HeyGen avatar id ("SET_ME" sentinel = hard fail if enabled)
    segments    section ids to generate (subset of format.sections)
    dimension   requested clip size (rendered small; 720p is plenty)
    background  solid color behind the twin (brand charcoal)

Output:
    originate/<slug>/avatars/<section_id>.mp4
    originate/<slug>/avatars/jobs.json      # submitted HeyGen job state
    originate/<slug>/avatars/avatars.json   # manifest for prepare_longform
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "blueprint.json"

API_BASE = "https://api.heygen.com"
UPLOAD_BASE = "https://upload.heygen.com"

TERMINAL_OK = {"completed"}
TERMINAL_BAD = {"failed"}

# "Rounder, person in a room" master (Manav's call, 2026-07-08): the
# HeyGen voice clone carries his room's acoustics (trained on the avatar
# footage's camera mic) and that in-a-room quality is WHY it won over the
# studio-processed ElevenLabs VO — so this chain must never scrub the
# room out. Gentle glue compression, a touch of low-mid warmth, tame the
# top, loudness-match the rest of the episode. No de-esser, no room tone
# (the room is real), looser LRA than the EL chain to keep the dynamics.
VOICE_MASTER_CHAIN = (
    "highpass=f=70,"
    "acompressor=threshold=-20dB:ratio=2.5:attack=12:release=220:makeup=3,"
    "equalizer=f=180:t=q:w=1.2:g=1.2,"
    "highshelf=f=7800:g=-1.5,"
    "loudnorm=I=-14:TP=-1.5:LRA=11"
)


def load_env_file() -> None:
    """generate_vo.py expects keys in the environment; mirror that, but
    also read studio/.env directly so the step works when the shell
    didn't source it (Cowork runs each call in a fresh shell)."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def api_key() -> str:
    key = os.environ.get("HEYGEN_API_KEY")
    if not key:
        print("Error: HEYGEN_API_KEY not set (env or studio/.env).", file=sys.stderr)
        sys.exit(1)
    return key


def headers() -> dict:
    return {"x-api-key": api_key()}


def upload_audio(mp3: Path) -> str:
    """Upload a section MP3 as a HeyGen asset; returns asset id."""
    r = requests.post(
        f"{UPLOAD_BASE}/v1/asset",
        headers={**headers(), "Content-Type": "audio/mpeg"},
        data=mp3.read_bytes(),
        timeout=120,
    )
    r.raise_for_status()
    data = r.json().get("data") or {}
    asset_id = data.get("id") or data.get("asset_id")
    if not asset_id:
        raise RuntimeError(f"asset upload returned no id: {r.text[:300]}")
    return asset_id


def spoken_text(vo_dir: Path, section_id: str, script: dict) -> str:
    """The text the avatar speaks in heygen-voice mode: the performed
    section (same performance pass the EL VO used), with breath tags
    stripped — HeyGen reads bracketed tags as literal text."""
    perf = vo_dir / f"performed-{section_id}.txt"
    if perf.exists():
        text = perf.read_text()
    else:
        sec = next(s for s in script["sections"] if s["id"] == section_id)
        text = " ".join(b["vo_text"] for b in sec.get("beats", []))
    text = re.sub(r"\[[^\]\n]{1,40}\]", "", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def whisper_words(mp3: Path) -> list[dict]:
    """Word-level timestamps via OpenAI Whisper — same alignment source
    the shorts pipeline uses. Returns [{word, start, end}]."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set (needed to align "
                           "heygen-voice audio for captions/timeline).")
    with open(mp3, "rb") as f:
        r = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {key}"},
            files={"file": (mp3.name, f, "audio/mpeg")},
            data={"model": "whisper-1", "response_format": "verbose_json",
                  "timestamp_granularities[]": "word"},
            timeout=300,
        )
    r.raise_for_status()
    return [{"word": w["word"].strip(), "start": round(w["start"], 3),
             "end": round(w["end"], 3)} for w in r.json().get("words", [])]


def adopt_clip_audio(clip: Path, vo_dir: Path, section_id: str,
                     cfg: dict) -> None:
    """Make the avatar clip's audio the section's master VO: extract,
    master (rounder, keep the room), tail-pad (the breath between
    sections), overwrite vo/<id>.mp3 + words-<id>.json. generate_vo.py's
    resumable path then reassembles words.json/timeline.json from the
    caches — run it again after this step (originate.py does)."""
    voice_cfg = cfg.get("voice") or {}
    chain = voice_cfg.get("master_chain", VOICE_MASTER_CHAIN)
    pad_s = voice_cfg.get("tail_pad_s", 0.85)
    dest = vo_dir / f"{section_id}.mp3"
    raw = vo_dir / f"{section_id}.heygen.raw.mp3"
    subprocess.run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                    "-i", str(clip), "-vn", "-ar", "44100", "-b:a", "192k",
                    str(raw)], check=True)
    af = chain + (f",apad=pad_dur={pad_s}" if pad_s > 0 else "")
    subprocess.run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                    "-i", str(raw), "-af", af,
                    "-ar", "44100", "-b:a", "192k", str(dest)], check=True)
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(dest)],
        capture_output=True, text=True, check=True).stdout.strip())
    words = whisper_words(dest)
    (vo_dir / f"words-{section_id}.json").write_text(
        json.dumps({"duration": dur, "words": words}, indent=2))
    print(f"         VO master replaced: vo/{section_id}.mp3 "
          f"({dur:.1f}s, {len(words)} words aligned)")


# Room-match for elevenlabs_room mode: the EL studio VO gains the room
# the on-screen face lives in. Subtle early reflections (no long tail —
# duration must not change, EL word timestamps stay valid), softened top,
# slight low-mid body, loudness re-anchored. Tunable via
# avatar.voice.room_chain in config.
ROOM_MATCH_CHAIN = (
    "aecho=0.72:0.68:11|19|29:0.16|0.11|0.07,"
    "highshelf=f=9500:g=-1.2,"
    "equalizer=f=250:t=q:w=1.4:g=0.8,"
    "loudnorm=I=-14:TP=-1.5:LRA=9"
)


def roomize_vo(vo_dir: Path, section_id: str, cfg: dict) -> Path:
    """Process the section's EL VO through the room-match chain, in
    place. The dry original is preserved at vo/<id>.dry.mp3 — its
    existence is also the idempotency marker (re-runs never double-
    process). Duration is unchanged, so words-<id>.json stays valid."""
    mp3 = vo_dir / f"{section_id}.mp3"
    dry = vo_dir / f"{section_id}.dry.mp3"
    if dry.exists():
        return mp3  # already room-matched
    chain = (cfg.get("voice") or {}).get("room_chain", ROOM_MATCH_CHAIN)
    dry.write_bytes(mp3.read_bytes())
    tmp = mp3.with_suffix(".room.mp3")
    subprocess.run(["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                    "-i", str(dry), "-af", chain,
                    "-ar", "44100", "-b:a", "192k", str(tmp)], check=True)
    tmp.replace(mp3)
    print(f"         room-matched vo/{section_id}.mp3 (dry kept at "
          f"vo/{section_id}.dry.mp3)")
    return mp3


def submit_video(cfg: dict, section: str, asset_id: str | None = None,
                 script_text: str | None = None) -> str:
    """Create the avatar generation job via POST /v2/videos (Avatar IV
    engine — supports digital twins, photo input, and photo-avatar looks).
    Returns video id.

    Modes (cfg["mode"]):
      photo (default) — animates cfg["photo_asset_id"] (a real photo of
        Manav) with AI motion. Real likeness + motion_prompt/expressiveness
        control. Chosen 2026-07-08: the trained twin's motion is stitched
        from (still) training footage — exaggerated mouth, static head/
        eyes — while the photo engine synthesizes natural head/eye motion
        from the audio. Wardrobe/backdrop = whatever the source photo
        shows, so the brand set is one good photo away.
      twin — the trained video avatar (cfg["avatar_id"]). Real footage
        motion; no motion_prompt support.
      look — a prompt-generated look image id in cfg["look_id"], animated
        like photo mode (weaker likeness; eyeball before adopting).
    """
    mode = cfg.get("mode", "photo")
    payload = {
        "title": f"OE avatar — {section}",
        "resolution": cfg.get("resolution", "720p"),
        "aspect_ratio": cfg.get("aspect_ratio", "9:16"),
        "background": {"type": "color",
                       "value": cfg.get("background", "#1A1A1A")},
    }
    # Voice: HeyGen's own clone speaking the performed script (won the
    # 2026-07-08 A/B — sounds like a person in the room, matching the
    # face) vs. lip-syncing the ElevenLabs audio asset.
    if script_text is not None:
        payload["script"] = script_text
        payload["voice_id"] = (cfg.get("voice") or {})["voice_id"]
    else:
        payload["audio_asset_id"] = asset_id
    if mode == "twin":
        payload["avatar_id"] = cfg["avatar_id"]
    else:
        if mode == "look":
            payload["avatar_id"] = cfg["look_id"]
        else:
            payload["image_asset_id"] = cfg["photo_asset_id"]
        # Motion controls apply to photo-engine modes only.
        if cfg.get("motion_prompt"):
            payload["motion_prompt"] = cfg["motion_prompt"]
        payload["expressiveness"] = cfg.get("expressiveness", "medium")
    r = requests.post(f"{API_BASE}/v2/videos",
                      headers={**headers(), "Content-Type": "application/json"},
                      json=payload, timeout=60)
    r.raise_for_status()
    body = r.json()
    video_id = (body.get("data") or {}).get("video_id")
    if not video_id:
        raise RuntimeError(f"/v2/videos returned no video_id: {r.text[:300]}")
    return video_id


def video_status(video_id: str) -> dict:
    r = requests.get(f"{API_BASE}/v1/video_status.get",
                     headers=headers(), params={"video_id": video_id},
                     timeout=30)
    r.raise_for_status()
    return r.json().get("data") or {}


def download(url: str, dest: Path) -> None:
    tmp = dest.with_suffix(".part")
    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 16):
                f.write(chunk)
    tmp.replace(dest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", help="originate/<slug>/script.json")
    ap.add_argument("--sections", help="comma list; overrides config segments")
    ap.add_argument("--look", help="talking_photo look id; overrides config look_id "
                                   "(per-episode wardrobe/backdrop)")
    ap.add_argument("--poll-timeout", type=int, default=900,
                    help="seconds to poll before exiting (jobs persist; re-run resumes)")
    ap.add_argument("--submit-only", action="store_true",
                    help="submit jobs and exit without polling (Cowork slice mode)")
    args = ap.parse_args()

    load_env_file()

    config = json.loads(CONFIG.read_text())
    cfg = config.get("avatar") or {}
    if args.look:
        cfg["look_id"] = args.look
    if not cfg.get("enabled"):
        print("avatar.enabled is false — skipping avatar generation.")
        return
    mode = cfg.get("mode", "photo")
    required = {"photo": "photo_asset_id", "twin": "avatar_id",
                "look": "look_id"}.get(mode)
    if not required:
        print(f"Error: avatar.mode '{mode}' unknown (photo|twin|look).",
              file=sys.stderr)
        sys.exit(1)
    if cfg.get(required, "SET_ME") in (None, "", "SET_ME"):
        print(f"Error: avatar.{required} unset (required for mode '{mode}'). "
              "See config note + scripts/originate/avatar_looks.py list.",
              file=sys.stderr)
        sys.exit(1)

    script_path = Path(args.script)
    ep_dir = script_path.parent
    vo_dir = ep_dir / "vo"
    out_dir = ep_dir / "avatars"
    out_dir.mkdir(exist_ok=True)
    jobs_path = out_dir / "jobs.json"
    jobs = json.loads(jobs_path.read_text()) if jobs_path.exists() else {}

    sections = (args.sections.split(",") if args.sections
                else cfg.get("segments", ["hook", "cta"]))
    sections = [s.strip() for s in sections if s.strip()]

    script_data = json.loads(script_path.read_text())
    voice_cfg = cfg.get("voice") or {}
    heygen_voice = voice_cfg.get("source") == "heygen"

    # 1. Submit anything not yet submitted (skip finished mp4s)
    for sec in sections:
        dest = out_dir / f"{sec}.mp4"
        if dest.exists():
            print(f"  [skip] {sec}: avatars/{sec}.mp4 exists")
            continue
        if sec in jobs and jobs[sec].get("video_id"):
            print(f"  [pend] {sec}: job {jobs[sec]['video_id']} already submitted")
            continue
        if heygen_voice:
            print(f"  [send] {sec}: submitting (HeyGen voice, performed script)…")
            text = spoken_text(vo_dir, sec, script_data)
            video_id = submit_video(cfg, sec, script_text=text)
            jobs[sec] = {"video_id": video_id, "status": "submitted",
                         "voice": "heygen"}
        else:
            mp3 = vo_dir / f"{sec}.mp3"
            if not mp3.exists():
                print(f"Error: {mp3} missing — run generate_vo.py first.",
                      file=sys.stderr)
                sys.exit(1)
            if voice_cfg.get("source") == "elevenlabs_room":
                mp3 = roomize_vo(vo_dir, sec, cfg)
            print(f"  [send] {sec}: uploading VO + submitting job…")
            asset_id = upload_audio(mp3)
            video_id = submit_video(cfg, sec, asset_id=asset_id)
            jobs[sec] = {"asset_id": asset_id, "video_id": video_id,
                         "status": "submitted"}
        jobs_path.write_text(json.dumps(jobs, indent=2))
        print(f"         video_id={video_id}")

    if args.submit_only:
        print("Submitted. Re-run without --submit-only to poll + download.")
        return

    # 2. Poll + download
    deadline = time.time() + args.poll_timeout
    pending = [s for s in sections if not (out_dir / f"{s}.mp4").exists()]
    while pending and time.time() < deadline:
        for sec in list(pending):
            info = video_status(jobs[sec]["video_id"])
            status = info.get("status")
            jobs[sec]["status"] = status
            jobs_path.write_text(json.dumps(jobs, indent=2))
            if status in TERMINAL_OK:
                url = info.get("video_url")
                print(f"  [done] {sec}: downloading…")
                clip = out_dir / f"{sec}.mp4"
                download(url, clip)
                # HeyGen-voice clips ARE the section's new voice — adopt
                # their audio as the VO master so lips, captions, and
                # timeline all reference one source.
                if jobs.get(sec, {}).get("voice") == "heygen":
                    adopt_clip_audio(clip, vo_dir, sec, cfg)
                pending.remove(sec)
            elif status in TERMINAL_BAD:
                err = info.get("error") or {}
                print(f"Error: {sec} job failed: {err}", file=sys.stderr)
                jobs.pop(sec, None)  # allow clean resubmit next run
                jobs_path.write_text(json.dumps(jobs, indent=2))
                sys.exit(1)
            else:
                print(f"  [wait] {sec}: {status}")
        if pending:
            time.sleep(min(15, max(1, deadline - time.time())))

    if pending:
        print(f"Timed out with pending sections: {pending}. "
              "Jobs persist in avatars/jobs.json — re-run to resume.")
        sys.exit(3)

    # 3. Manifest for prepare_longform.py
    manifest = [{"section": s, "src": f"avatars/{s}.mp4"} for s in sections]
    (out_dir / "avatars.json").write_text(json.dumps(manifest, indent=2))
    print(f"\nAvatar clips complete: {', '.join(sections)} -> {out_dir}/")


if __name__ == "__main__":
    main()
