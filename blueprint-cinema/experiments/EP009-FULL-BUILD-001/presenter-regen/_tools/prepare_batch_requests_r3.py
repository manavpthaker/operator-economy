#!/usr/bin/env python3
"""Prepare the remaining Henry-only requests offline; never calls a provider."""

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-regen"
IMAGE = "eb9cdb1e-a6c2-44cb-bb06-a097b8432a30"
VIDEO = "d11ea443-81ae-4208-a651-b3807fd43ff3"
TIMING = (
    "Follow the AUDIO reference at its original speed and cadence. Finish speaking "
    "when the AUDIO reference ends, then hold the existing resting pose for the "
    "remaining picture duration with no extra words. Do not stretch the speech "
    "to fill the generated clip."
)
NUMBER = {5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def binding(path):
    return {"path": str(path.relative_to(ROOT)), "sha256": sha(path.read_bytes())}


def read(path):
    return json.loads(path.read_text())


def preserve_write(path, content):
    if path.exists():
        assert path.read_bytes() == content, f"Refusing to replace differing artifact: {path}"
    else:
        with path.open("xb") as stream:
            stream.write(content)


def main():
    active_path = BASE / "ACTIVE-PLAN.json"
    active = read(active_path)
    plan_path = ROOT / active["path"]
    assert plan_path == BASE / "EXECUTION-PLAN-r4.json"
    assert binding(plan_path)["sha256"] == active["sha256"]
    plan = read(plan_path)
    base_plan_path = BASE / "TAKE-PLAN.json"
    assert binding(base_plan_path)["sha256"] == active["base_plan_sha256"]
    upload_path = BASE / "AUDIO-UPLOADS-r2.json"
    inventory = read(upload_path)
    assert inventory["plan_sha256"] == active["base_plan_sha256"]
    uploads = {part["part_id"]: part for part in inventory["parts"]}
    assert len(uploads) == len(inventory["parts"]) == 20
    selected = [part for part in plan["parts"] if part["part_id"] in uploads]
    assert len(selected) == 20
    assert {part["part_id"] for part in plan["parts"]} - uploads.keys() == {"P01a", "P01b"}
    assert plan["behavior_references"] == [VIDEO]
    assert plan["provider"]["model"] == "seedance_2_5"
    assert plan["provider"]["mode"] == "omni_reference"

    role_path = BASE / "P01/AVATAR-PROMPT-henry-only.txt"
    accepted_role = role_path.read_text().strip().split("\n\n")[1]
    assert accepted_role.startswith("The VIDEO supplies connected public-facing articulation only.")
    old_role = (BASE / "P02a/AVATAR-PROMPT.txt").read_text().strip().split("\n\n")[1]
    assert old_role.startswith("The first VIDEO supplies")

    image_upload_path = BASE / "look/HIGGSFIELD-IMAGE-UPLOAD.json"
    image_upload = read(image_upload_path)
    assert image_upload["media_id"] == IMAGE
    assert binding(ROOT / image_upload["source"])["sha256"] == image_upload["sha256"]
    master_path = ROOT / "operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav"
    assert binding(master_path)["sha256"] == inventory["master_sha256"]

    requests, records, staged = [], [], []
    for index, part in enumerate(selected, 1):
        part_id = part["part_id"]
        original_path = ROOT / part["prompt"]
        original = original_path.read_text()
        paragraphs = original.strip().split("\n\n")
        assert len(paragraphs) == 5 and paragraphs[1] == old_role
        assert original.count(old_role) == 1
        duration = part["generation_seconds"]
        assert isinstance(duration, int) and 1 <= duration <= 12
        assert original.startswith(f"One continuous {NUMBER[duration]}-second ")
        if part_id == "P11a":
            assert original_path == BASE / "P11a/AVATAR-PROMPT-r2.txt" and duration == 12
        spoken = re.fullmatch(r'Speak only the exact ([0-9.]+)-second AUDIO reference: "(.*)"', paragraphs[2])
        assert spoken and spoken[2] == part["words"]
        assert abs(float(spoken[1]) - part["audio_seconds"]) <= 0.00501
        assert part["audio_seconds"] <= duration

        # Only the reference-role paragraph changes; timing is a separate addition.
        revised = original.replace(old_role, accepted_role).rstrip() + "\n\n" + TIMING + "\n"
        revised_paragraphs = revised.strip().split("\n\n")
        assert all(revised_paragraphs[n] == paragraphs[n] for n in (0, 2, 3, 4))
        assert revised_paragraphs[1] == accepted_role and revised_paragraphs[5] == TIMING
        prompt_path = BASE / part_id / "AVATAR-PROMPT-henry-only.txt"
        staged.append((prompt_path, revised.encode()))

        upload = uploads[part_id]
        upload_record_path = BASE / part_id / "audio/HIGGSFIELD-UPLOAD-r2.json"
        assert read(upload_record_path) == upload
        assert upload["status"] == "uploaded" and upload["put_http"] == 200
        assert upload["uploaded_mp3_hash_verified_after_confirmation"] is True
        assert upload["source_pcm_identity"]["identical_to_local_master_excerpt_pcm"] is True
        assert upload["source_pcm_identity"]["verified_directly_against_locked_master"] is True
        assert upload["sha256"] == upload["generated_mp3"]["sha256"]
        assert upload["samples"] == part["samples"]
        assert upload["sample_rate"] == 48000
        assert all(abs(a-b) < 0.000002 for a, b in zip(upload["master_range"], [part["master_in"], part["master_out"]]))
        wav_path = BASE / part_id / "audio/narration.wav"
        assert binding(wav_path)["sha256"] == upload["source_pcm_identity"]["local_wav_sha256"]
        params = {
            "model": "seedance_2_5", "mode": "omni_reference",
            "resolution": part["resolution"], "duration": duration,
            "aspect_ratio": "16:9", "generate_audio": True, "count": 1,
            "prompt": revised,
            "medias": [
                {"role": "image", "value": IMAGE},
                {"role": "video", "value": VIDEO},
                {"role": "audio", "value": upload["media_id"]},
            ],
        }
        requests.append({"index": index, "params": params})
        records.append({
            "index": index, "part_id": part_id, "take_id": part["take_id"],
            "planned_part_sha256": sha(canonical(part)),
            "original_prompt": binding(original_path),
            "prompt": {"path": str(prompt_path.relative_to(ROOT)), "sha256": sha(revised.encode())},
            "request_params_sha256": sha(canonical(params)),
            "words": part["words"], "gesture": part["gesture"],
            "master_range": [part["master_in"], part["master_out"]],
            "samples": part["samples"], "audio_seconds": part["audio_seconds"],
            "generation_seconds": duration, "resolution": part["resolution"],
            "est_credits": part["est_credits"],
            "audio_upload_record": binding(upload_record_path),
            "audio_upload_record_canonical_sha256": sha(canonical(upload)),
            "uploaded_audio": {"media_id": upload["media_id"], "sha256": upload["sha256"], "bytes": upload["bytes"]},
            "local_narration_wav": binding(wav_path),
            "source_pcm_sha256": upload["source_pcm_identity"]["sha256"],
        })
    total_credits = sum(part["est_credits"] for part in selected)
    assert total_credits == 1607
    assert len({record["uploaded_audio"]["media_id"] for record in records}) == 20
    batch = {
        "record_type": "presenter_generation_requests_prepared",
        "episode": "EP009-direct-booking-recovery", "revision": "r3",
        "status": "prepared_not_submitted", "pilot_gate": "pending",
        "cost_preflight": "pending_root", "provider_calls_made_by_preparation": 0,
        "scope": "The 20 remaining parts P02a through P13b. P01a/P01b are excluded and handled separately. This file is preparation evidence, not submission authorization or a provider cost receipt.",
        "bindings": {
            "active_plan": binding(active_path), "selected_plan": binding(plan_path),
            "base_plan": binding(base_plan_path), "audio_upload_inventory": binding(upload_path),
            "accepted_henry_role_source": binding(role_path),
            "image_upload": binding(image_upload_path),
            "locked_image": binding(ROOT / image_upload["source"]),
            "locked_narration_master": binding(master_path),
            "preparation_script": binding(Path(__file__).resolve()),
        },
        "prompt_change": {
            "role_paragraph": accepted_role, "added_audio_timing": TIMING,
            "preserved": ["planned words", "source shot length", "locked look", "performance and gesture", "prohibitions"],
            "p11a_source": "P11a/AVATAR-PROMPT-r2.txt (12-second override)",
        },
        "requests": requests, "parts": records,
        "totals": {"parts": 20, "generation_seconds": sum(p["generation_seconds"] for p in selected), "est_credits": total_credits},
        "verification": {
            "active_plan_hash_matches": True, "all_prompts_match_planned_words": True,
            "all_durations_at_most_12_seconds": True, "source_performance_and_look_preserved": True,
            "all_audio_ids_are_confirmed_uploads": True, "all_local_wav_hashes_match_upload_provenance": True,
            "all_source_ranges_and_sample_counts_match_active_plan": True,
            "uploaded_audio_hashes_bound_from_confirmed_inventory": True,
            "locked_master_hash_verified_locally": True, "image_hash_verified_locally": True,
            "remote_audio_not_fetched_during_preparation": True,
            "totals_recomputed_from_selected_parts": True,
            "note": "The batch binds active EXECUTION-PLAN-r4.json and recomputes totals from its selected 20 parts. The active plan is not modified.",
        },
        "future_submission_groups": [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], [13, 14, 15, 16, 17, 18], [19, 20]],
    }
    for path, content in staged:
        if path.exists():
            assert path.read_bytes() == content, f"Differing existing prompt: {path}"
    output = BASE / "BATCH-REQUESTS-r3.json"
    batch_bytes = (json.dumps(batch, indent=2, ensure_ascii=False) + "\n").encode()
    if output.exists():
        assert output.read_bytes() == batch_bytes, "Differing existing batch; preserve it"
    for path, content in staged:
        preserve_write(path, content)
    preserve_write(output, batch_bytes)
    print(json.dumps({"batch": binding(output), "totals": batch["totals"], "status": batch["status"]}, indent=2))


if __name__ == "__main__":
    main()
