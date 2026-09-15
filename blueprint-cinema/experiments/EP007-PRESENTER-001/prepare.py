#!/usr/bin/env python3
"""Prepare exact locked-VO presenter excerpts; no provider calls or state writes."""
import hashlib
import json
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EP = ROOT / "operator-blueprint-v2/episodes/EP007-exit-readiness-prep"
NARRATION = EP / "02-narration-production"
PINS = {
    NARRATION / "master/narration-master.v4.wav": "d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9",
    NARRATION / "word-transcript.json": "f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7",
    EP / "01-editorial/canonical-w.txt": "333a45d7449f5cb4c3e394a9e262c3a3a60c3825e76563bc0149498f0b41860c",
    NARRATION / "narration-lock.md": "61cfd940b9f8bfcb0e502e07f073a7a1457a671b9a4a35667e6ca08c2fafbbd5",
}
SELECTIONS = [
    ("presenter-01-introduction", 118, 190, "Introduce the presenter and episode promise"),
    ("presenter-02-scope", 1663, 1754, "Own personal experience and its limits; first test"),
    ("presenter-03-model-caveat", 2522, 2561, "State the model's assumptions before arithmetic"),
    ("presenter-04-verdict", 3045, 3109, "Deliver the qualified verdict"),
]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    for path, expected in PINS.items():
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"Locked input changed: {path.relative_to(ROOT)}")
    transcript = json.loads((NARRATION / "word-transcript.json").read_text())
    words = transcript["words"]
    canonical = (EP / "01-editorial/canonical-w.txt").read_text().split()
    if [word["token"] for word in words] != canonical:
        raise RuntimeError("Transcript tokens differ from canonical W")
    out = HERE / "media"
    out.mkdir(exist_ok=True)
    clips = []
    source_path = NARRATION / "master/narration-master.v4.wav"
    with wave.open(str(source_path), "rb") as source:
        params = source.getparams()
        rate = params.framerate
        if (params.nchannels, params.sampwidth, rate, params.comptype) != (1, 2, 48000, "NONE"):
            raise RuntimeError("Unexpected narration format")
        for clip_id, first, last, purpose in SELECTIONS:
            selected = words[first:last + 1]
            if [w["w_id"] for w in selected] != [f"W{i:06d}" for i in range(first, last + 1)]:
                raise RuntimeError("Noncontiguous word IDs")
            start, end = selected[0]["start"], selected[-1]["end"]
            # Bounds respect neighboring words; alignment is not proof of clean audible edges.
            source_in = max(0, start - .25, words[first - 1]["end"] + .02 if first else 0)
            source_out = min(params.nframes / rate, end + .25,
                             words[last + 1]["start"] - .02 if last + 1 < len(words) else params.nframes / rate)
            first_frame, end_frame = round(source_in * rate), round(source_out * rate)
            if first_frame > round(start * rate) or end_frame < round(end * rate):
                raise RuntimeError("Handle would exclude selected speech")
            source.setpos(first_frame)
            pcm = source.readframes(end_frame - first_frame)
            target = out / f"{clip_id}.wav"
            with wave.open(str(target), "wb") as dest:
                dest.setparams(params)
                dest.writeframes(pcm)
            with wave.open(str(target), "rb") as check:
                if check.readframes(check.getnframes()) != pcm:
                    raise RuntimeError("Extract PCM differs from locked source")
                if check.getnframes() != end_frame - first_frame:
                    raise RuntimeError("Unexpected extracted duration")
            clips.append({
                "id": clip_id, "status": "candidate_audio_prepared", "purpose": purpose,
                "word_first": selected[0]["w_id"], "word_last": selected[-1]["w_id"],
                "text": " ".join(w["token"] for w in selected),
                "episode_speech_in": start, "episode_speech_out": end,
                "spoken_range_duration": round(end - start, 6),
                "source_in_sample": first_frame, "source_out_sample_exclusive": end_frame,
                "source_in_seconds": first_frame / rate, "source_out_seconds": end_frame / rate,
                "speech_offset_in_clip_seconds": round(start - first_frame / rate, 6),
                "clip_duration_seconds": (end_frame - first_frame) / rate,
                "path": str(target.relative_to(HERE)), "sha256": sha256(target),
                "pcm_matches_master_slice": True, "audible_edge_review": "pending",
                "picture_audio_mode": "presenter_address", "face_function": "presenter_delivery",
                "heygen_video_id": None, "generated_video_review": "not_generated",
            })
    manifest = {
        "episode": "EP007-exit-readiness-prep", "packet": "EP007-PRESENTER-001",
        "status": "candidate_edit_not_approved_placements", "created_date": "2026-09-07",
        "avatar_group_id": "cc6abe9744e74df7a103b7a37262d2f7",
        "generation_avatar_or_look_id": None,
        "look_direction": "Owner selected landscape chest-up restrained study",
        "inputs": [{"path": str(p.relative_to(ROOT)), "sha256": h} for p, h in PINS.items()],
        "audio_format": {"sample_rate": rate, "channels": 1, "sample_width_bytes": 2},
        "total_spoken_range_seconds": round(sum(c["spoken_range_duration"] for c in clips), 6),
        "clips": clips,
        "final_conform": "Use continuous locked master. Provider audio is sync reference. Remove recorded handles without changing playback speed.",
        "gate_changes": [], "upstream_modifications": [],
    }
    (HERE / "presenter-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"clips": len(clips), "total_spoken_range_seconds": manifest["total_spoken_range_seconds"],
                      "input_hashes_verified": len(PINS), "pcm_slice_checks": "passed", "manifest": str(HERE / "presenter-manifest.json")}))


if __name__ == "__main__":
    main()
