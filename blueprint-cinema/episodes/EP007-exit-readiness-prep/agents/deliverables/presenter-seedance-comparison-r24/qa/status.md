# Seedance comparison QA: no media returned

**Status: blocked before media QA.** The first Seedance request returned HTTP 422 with `content_policy_violation` and reason `partner_validation_failed`.

The saved provider error states: “The images or videos provided may contain likenesses of real people or other private information that cannot be processed.” This was an upstream provider rejection, not a quality finding about a rendered presenter.

Evidence: [first request result](/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001/repair-r24/seedance-01.json), SHA256 `516085a6e93a534ee94ab93f517fe812a5892cf6fa1b14460d81b3a4f91780a5`. This reviewer read the terminal error fields and verified that neither expected local Seedance MP4 exists. The parent confirmed that sample 02 was not submitted.

No Seedance duration, audio correspondence, mouth sync, head/hand motion, or comparative quality can be assessed without an output. All such judgments remain unverified. The existing InfiniteTalk preference is unchanged; this rejection does not establish whether Seedance would look better or worse.

Work stopped immediately on the parent's instruction. The agent only read the existing QA helper before the rejection notification; no new Seedance QA script or media diagnostic was created. No credentials, provider calls, second request, media edits, remuxes, reference changes, or production approvals were made by this agent.

The original WAV remains hash-matched: `c565f1dfe8c218f156e9d0b76d0515a264be26cc1d0cea7d1ea8977a3c565566`.

