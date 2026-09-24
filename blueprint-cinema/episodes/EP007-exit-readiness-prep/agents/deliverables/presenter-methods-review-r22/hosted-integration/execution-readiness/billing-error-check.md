# fal failed-media billing check

Checked official public documentation on 2026-09-08. Read-only research; no credentials or authenticated requests used.

**A terminal HTTP 422 does not guarantee a free request.** fal's FAQ says invalid-input errors may incur a charge when the runner used GPU time before detecting the error. HTTP 500+ server errors are never charged. Accounts lock when their balance drops below the account's lock threshold; adding credits is the documented unlock action. [Official FAQ](https://fal.ai/docs/documentation/model-apis/faq)

The error reference classifies `file_download_error` as HTTP 422 and non-retryable: the server could not retrieve the supplied input URL. It recommends a URL accessible without a login or authentication wall. Replacing a failed data URI with a verified accessible CDN URL corrects the input; repeating the identical failed input is not the documented remedy. [Official error reference](https://fal.ai/docs/documentation/model-apis/errors#file_download_error)

The broader pricing page says failed outputs are not charged and singles out 500+ errors. The FAQ supplies the more specific 422 caveat, so the broad statement should not be used to promise a refund for this request. [Official pricing](https://fal.ai/docs/documentation/model-apis/pricing)

No official reservation-release schedule, automatic 422 refund guarantee, or unlock propagation time was established in this bounded review. The parent's reported accepted request, terminal 422, and subsequent exhausted-balance 403 do not by themselves establish the actual charge or why the remaining balance is below threshold. Reconcile the exact request against usage and billing for the account that owns the API key; if unresolved, retain the request ID, error body, and top-up receipt for fal support. Account keys and billing belong to the selected account, so personal and team balances are separate. [Accounts and identity](https://fal.ai/docs/documentation/setting-up/accounts-and-identity), [support](https://fal.ai/docs/documentation/model-apis/support)

This finding does not diagnose a reservation, a missing payment, or a provider billing error. Parent owns account inspection and all further generation decisions.
