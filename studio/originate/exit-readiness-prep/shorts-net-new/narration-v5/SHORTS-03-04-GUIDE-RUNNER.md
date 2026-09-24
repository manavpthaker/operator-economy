# EP007 Short 03/04 Algieba guides

`capture_short03_04_guides.py` is a separate continuation from the stopped
`narration-v3` batch. It is pinned to the locked Short 03/04 scripts and Google
requests, the fresh full-private-production owner source/event, and the one
Short 02 guide receipt already consumed.

From the repository root:

```sh
python3 studio/originate/exit-readiness-prep/shorts-net-new/narration-v5/capture_short03_04_guides.py check
python3 studio/originate/exit-readiness-prep/shorts-net-new/narration-v5/capture_short03_04_guides.py preflight --short short-03-how-you-charge
python3 studio/originate/exit-readiness-prep/shorts-net-new/narration-v5/capture_short03_04_guides.py preflight --short short-04-test-the-front-door
```

Those commands do not call a provider. Only `submit --short <id>` can submit
one Google POST for that short. It writes an exclusive immutable intent before
the POST, saves the raw response and receipt, and refuses an existing or
uncertain attempt. No automatic retry, Original C transfer, avatar job, render,
upload, or publication is performed by this runner. A guide remains pending
exact-copy ASR and listening after its format/tail check.

Execution guardrail: Short 02 observed estimate plus Short 03/04 forecast
must stay at or below $0.15, and a later Short 04 preflight uses Short 03's
observed estimate if its receipt exists. The estimate is not an invoice or a
provider-enforced billing cap. An unresolved earlier guide intent blocks the
next submission because its cost is unknown. Submit Short 03 and Short 04
sequentially so each preflight sees the prior result.
