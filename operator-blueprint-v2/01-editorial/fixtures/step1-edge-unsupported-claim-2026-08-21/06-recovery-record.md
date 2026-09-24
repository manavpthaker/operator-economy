# E5 recovery record: remove unsupported claims

Status: completed fixture recovery

Failed derived script SHA-256: `f28dd3afcd291eadb5cd435d27c8ce7957edd2642981fad4414be20ae32a9a66`

## Dispositions

| Finding | Decision | Exact recovery | Reason |
|---|---|---|---|
| E5-CL-01 | remove | Delete M01 with no replacement. | The annual-cost claim is unnecessary and unsupported. |
| E5-CL-02 | remove | Delete M02 with no replacement. | Category evidence does not prove prevalence, willingness to pay, or price. |
| E5-CL-03 | restore | Restore: “It assumes a three-thousand-dollar fixed sprint, two new sprints per month, and twenty-four delivery hours for each one.” | C009 authorizes these only as modeled assumptions. |

## Recovered identity

Recovered script: Exact frozen base script v0.2

Recovered script SHA-256: `42b03e49d212edbb35fdb0c2a1197ea9654c06e14ad7a2638275071144a3a5c1`

Claims-map SHA-256: `141cd559c10624d44b2f457df9c733e1b1ca15d8d8a2c111294c5b1f1a079c1c`

Performance read-through SHA-256: `b8cbef13e5860b5baf1ddbc3f7ff9d159a561c18d44cf767b3822f7ea365fb53`

Spoken words: 1,018

Normalized script-to-read-through lexical sequence: match

Step 0 amendment approved: not required because no unsupported claim remains

## Invalidation result

The failed 1,052-word derived script is rejected and may not be performed. The recovery returns to an already recorded script identity rather than creating a hidden rewrite. Production approval remains absent.
