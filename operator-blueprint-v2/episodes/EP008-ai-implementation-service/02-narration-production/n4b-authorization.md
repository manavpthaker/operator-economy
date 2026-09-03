# N4B full-capture authorization: EP008

Authorization ID: `EP008-N4B-2026-09-03`

Status: **active** from 2026-09-03; consumed when `take-register.json` records every planned chunk accepted, or revoked by the owner

Human scope: `full_capture_provider_calls`

Authorized human: Manav Thaker

Authorized at: 2026-09-03

Owner statement of record, 2026-09-03, to the direct question "After lock, re-recording means paid provider calls on your ElevenLabs account and Google TTS, roughly 48 calls per episode as with EP007. Authorize narration capture now?": **"Yes, both episodes"** (run N1 to N4B for EP008 and EP009 on the frozen EP007 method).

## Exact scope

- Episode: EP008
- Locked words: canonical `W` `ea3743bfcc6e881a96902556959d141f5a75a2288ecad713ccc6fa7ba787ca63` (3400 tokens), editorial lock `76e41bfd02883e7f199d976440fe5e262e8b74d13f4a8e8b5f7b4750eac01874`
- Configuration: `n3-configuration-freeze.md` (method `n3-two-stage-acted-guide-v2`, unchanged from EP007)
- Executor: `tools/capture_n4b.py` at `92cb89dfb0f2ae971755fce63e8d7b1c3b095d9c3b031920149edc91c3694495`, invoked with `--execute`
- Providers and accounts: Google Cloud Text-to-Speech on the owner's ADC quota project; ElevenLabs on the owner's account (`ELEVENLABS_API_KEY` in the repo `.env`, never logged)
- Bound: 21 planned chunks, 42 calls minimum, at most 4 attempts per stage per chunk under the completeness contract, so at most 168 calls in total. Resume never re-bills an accepted chunk.
- Outputs: `raw/cNN.guide.wav`, `raw/cNN.saved-c.wav`, `take-register.json`

## Observed before the first call

ElevenLabs subscription read on 2026-09-03: tier `pro`, 408,689 of 696,811 characters used in the period, **status `past_due`**. The owner authorized capture knowing the account is live; if the provider refuses a call on account status, the run stops and the owner is told. No account or billing setting is changed by this process.

## Provider events

- 2026-09-03, EP008 chunk 1 probe: Google guide call returned HTTP 200 and the guide decayed into silence. ElevenLabs Voice Changer returned HTTP 401 `payment_required` ("Your subscription has a failed or incomplete payment. Complete the latest invoice to continue usage."). **Transfers are held.** Guide generation continues under this authorization; the transfer stage resumes only after the owner settles the ElevenLabs invoice, with no further authorization needed because the scope above is unchanged.

## Not authorized

Any change to the locked words, any other voice identity, any other provider or model, any pickup outside the planned chunks, any outbound action other than the calls above.
