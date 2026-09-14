Execution update: the owner signed in using GitHub. Root submitted the exact request once through the existing browser account at $0.42. Job 74a9da4ce7af4856a5c5583b2c48d26e completed and the direct MP4 loads and plays to its endpoint. See DELIVERY.json. A shared submission intent blocks additional API submission. No API key was created.

# InfiniteTalk comparison preparation

One authorized seven-second, 720p test using the supplied near-frontal V12 PNG and unchanged Original C test WAV. The helper and input record are prepared; preparation itself made no authenticated requests or generation calls.

Run `python3 infinitetalk.py preflight`, then `submit` once, and use `status`, `result`, and `download` individually. The helper reads `WAVESPEED_API_KEY` from runtime first or the scoped Operator Economy `.env`; it never prints credentials or follows redirects. A submission intent is exclusively created and fsynced before generation. Any existing intent blocks another generation POST, including an uncertain outcome. No automatic polling, retry, fallback, batch, repair, account creation or purchase exists.

Preflight hashes both hosted assets, checks the exact local seven-second WAV, requests a current dynamic quote and account balance, and retains receipts. Submit repeats those checks. It requires a USD quote for the exact payload, a discounted estimate no greater than $0.42, and sufficient existing balance. The ceiling is a client preflight guard, not a provider-enforced final billing cap. If the pricing API rejects these inputs or returns a different schema, the helper stops before generation; it does not substitute a base-price guess.

The output download is `infinitetalk-test03.mp4` in this directory, ignored by Git. Completion and hash checks do not establish perceptual lip-sync or identity quality.

Official documentation checked for this implementation:

- [InfiniteTalk schema and rates](https://wavespeed.ai/docs/docs-api/wavespeed-ai/infinitetalk): image and audio required; prompt, resolution, seed and mask optional. This test uses 720p and no mask. Published 720p rate is $0.06 per second, with whole-second duration rounding and a three-second minimum; seven seconds estimates $0.42.
- [Pricing API](https://wavespeed.ai/docs/pricing-api): `POST /api/v3/model/price`, body `{model_id, inputs}`. `discounted_price` is the quoted account payable amount; a request without inputs returns a base price instead.
- [Balance API](https://wavespeed.ai/docs/docs-common-api/balance): `GET /api/v3/balance`, USD amount at `data.balance`.
- [Result endpoint](https://wavespeed.ai/docs/get-result): `GET /api/v3/predictions/{id}/result`; completed is success, while failed, cancelled, timeout and deleted are terminal failures.
