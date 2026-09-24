# HeyGen Avatar IV seven-second comparison

Execution update: root submitted one job through the existing CLI OAuth Creator subscription. It completed as e90419bc8bc1a7dc2ee798178edbce38, with an observed four-credit balance decrease and no new cash purchase. See DELIVERY.json for media, QA and review status. The request and submission intent are bound; do not rerun submit.

## Existing subscription route

Read-only `heygen auth status` and `heygen user me get` verified the owner's existing Creator
subscription with **557 premium credits** on September 13. The stored OAuth credential uses
subscription credits, separately from the API cash balance. No login changes were made.
Published Avatar IV Photo Look pricing is **16 credits per minute**, giving approximately
**1.87 credits for seven seconds before provider rounding**, with no new cash purchase.

Use the existing credential with `python3 run_oauth.py preflight`, followed by `submit`,
`status`, `result`, and `download` as separate commands. This route checks the exact known
owner account, subscription billing, and at least three remaining credits before dispatch.
It sends the unchanged JSON over stdin to `heygen video create --data -` without `--wait`.
Both helpers share the same durable submission intent, so switching helpers cannot duplicate
the test. Only the root operator may submit. No helper automatically retries a create command.

The prepared API-key route below remains an alternative, not a second comparison render.

`REQUEST.json` is the exact body for `POST https://api.heygen.com/v3/videos`.
The approved V12 image and exact Original C WAV remain the inputs. Supplied audio replaces
script/voice synthesis. Duration follows that seven-second WAV; there is no duration parameter.
The direct-image request uses default Avatar IV, at 720p portrait, with no captions or audio adjustment.
The installed official CLI's `CreateVideoFromImage` schema has no `engine` field, so it is omitted;
the explicit engine selector belongs to the avatar-ID request variant.

Run from this directory:

```sh
python3 run_test.py preflight
python3 run_test.py submit
python3 run_test.py status
python3 run_test.py result
python3 run_test.py download
```

`preflight` GETs the two already-hosted inputs, verifies their hashes and local authorities,
checks WAV sample count, and checks credential presence. It makes no authenticated HeyGen call.
The root operator must first verify account identity, API eligibility, and available API funds.
The helper reads only runtime `HEYGEN_API_KEY` or that key in this OE checkout's `.env`.
It never prints, writes, or forwards credentials outside the exact API origin; redirects are disabled.

`submit` writes and fsyncs an exclusive `SUBMISSION-INTENT.json` before its only POST.
Any intent blocks another submission, including after a timeout or uncertain result.
Use provider history and the fixed `callback_id` to reconcile uncertainty; do not remove an
intent to retry. `status` and `result` issue one read-only GET each and preserve receipts.
`download` saves the untouched MP4 into this directory's ignored `media/` folder.
No command polls automatically, changes audio, repairs lips, captions, or starts a full take.

The published Avatar IV photo rate gives an estimate of **$0.35 for seven seconds**.
Direct-image billing classification, account availability, exact billing, and any watermark
remain unverified until provider/account readback. API funds are separate from web subscriptions.

Sources checked September 13, 2026:

- [Audio to Video](https://developers.heygen.com/audio-to-video): direct `image` + `audio_url`, audio-led duration and portrait output.
- [Avatar IV](https://developers.heygen.com/avatar-iv): default engine, arbitrary-image support and explicit engine selection.
- [Create Video](https://developers.heygen.com/reference/create-video) and [Get Video](https://developers.heygen.com/reference/get-video): authenticated v3 endpoints and result fields.
- [API pricing](https://help.heygen.com/en/articles/10060327-heygen-api-pricing-explained): photo Avatar IV is $3 per minute at 720p/1080p, billed by seconds.

Additional local schema verification: `heygen video create --request-schema`, selecting the
`CreateVideoFromImage` variant, on September 13. Only documented fields are present in this request.

Documentation inconsistency: the Audio to Video and Avatar IV pages say arbitrary-image requests
accept `motion_prompt` and `expressiveness`; the Image to Video page's comparison table says those
controls require a registered photo avatar. This request omits both optional fields. Do not create
an avatar or add a paid setup call to resolve that inconsistency within this one-render comparison.

Acceptance remains the owner's normal-speed judgment of moving likeness, restrained mouth movement,
and natural delivery, plus decoded-audio comparison with the original WAV and complete opening/end.
The helper does not claim that supplying the original WAV proves the returned audio is preserved.

Credential lookup: the prior EP007 R10 helper invokes the installed `heygen` CLI. Its local
`~/.heygen/credentials` currently stores OAuth, not an API key (only key names/presence inspected).
CLI auth help says OAuth uses subscription credits, while an API key uses separate API funds.
`run_test.py` intentionally does not extract or reuse OAuth; `run_oauth.py` delegates authentication
to the existing CLI. An existing API-key credential remains required only for the API-cash route.
Do not replace the stored CLI login or create a new key automatically.
