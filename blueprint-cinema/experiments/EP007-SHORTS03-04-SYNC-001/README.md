# EP007 Shorts 03–04: conditional Fal Sync v3

This is a one-shot private-production runner, not an instruction to sync every generated clip. Use it only if sound-on review of a completed, exact Higgsfield video shows a specific mouth-timing error. Place `VIDEO-SOURCE.json` and `SYNC-NEED.json` in the target segment directory; the templates here are not evidence. Do not submit based on a provisional silent-frame visual check.

Targets: `short03-a`, `short03-b`, `short04-a`, `short04-b`. The latter uses Short04 return **v2**. The pinned partial Higgsfield batch has jobs only for `short03-a` and `short04-b`; the other two targets remain held until a separately authorized and bound generation result exists. This runner does not accept new job IDs by command-line override.

After checking the local source and necessity records, run from this directory:

```bash
python3 sync_one_shot.py check short04-b --video-url 'https://d8j0ntlcm91z4.cloudfront.net/user_3J3m5xtqP8Xv0MOsPutf0uV3maX/hf_..._EXACT-JOB-ID.mp4'
```

`check` is local, read-only, and does not need `FAL_KEY`. It validates the exact source, upload, audio, job and authorization evidence; computes a per-target and aggregate forecast. It fails if any dependency is missing. Inspect its output, particularly `forecast_cents`, `aggregate_forecast_cents`, `provider_enforced_spend_cap: false`, and the exact input URLs. Fal Sync v3's published rate is $8/minute; this script conservatively rounds each job's forecast up to the next cent based on the longer of decoded video or exact audio duration. The $15 limit is a local operational gate, not a provider-level spending lock.

To make one paid call, substitute `submit` for `check` with the **same** exact URL. The script obtains `FAL_KEY` from the process environment or repo `.env`, writes an immutable request and intent before a single POST, and has no retry path. If a POST fails or its outcome is uncertain, stop and reconcile manually; do not rerun. It serializes concurrent submissions with a local file lock. `status <target>` reads the queued job and writes immutable status snapshots; `result <target>` is permitted only after a recorded `COMPLETED` status and preserves the returned result. Both are read-only provider calls, not new jobs. The Fal output is a candidate **picture** only; neither Higgsfield nor Fal audio replaces the continuous exact Original C program master. No owner acceptance, final sound-on QC, publication, or upload is implied by a completed sync result.

Evidence binding: `SYNC-PLAN-V1.json` is SHA-pinned by the runner; it binds the owner authorization, the partial Higgsfield batch receipt, exact generation intents, uploaded audio IDs and local MP3 hashes. The runner validates the approved CDN host and exact Higgsfield job UUID in each video URL. It caps this slate at four Fal submission intents and $15 total forecast, and stops if Short02 Fal submission evidence appears so the shared owner cap can be reconciled.
