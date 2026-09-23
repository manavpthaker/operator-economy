# S22 binder timing-plan review

Reviewed DIRECTION-v2.md and the HTML plan source against the locked transcript. No film-source, rendered-layout or continuous audio review performed. This report does not claim that the proposed binder actions exist.

## Finding: constrain the opening phase in take B

Take B starts at local12.000 / master1059.083333. The word “read” starts1059.420, only0.336667seconds later; “check” starts1060.360,1.276667seconds later. The full “He can read it. He can check it.” passage ends1060.760.

DIRECTION-v2 correctly avoids requiring word-by-word mime, but it gives no upper bound for opening the closed binder. A slow opening that consumes the full passage would delay the independent-inspection payoff beyond the words that establish it. Carry this concrete acceptance condition into playback review: **the record is exposed and his attention is reading it by approximately master1060.36, local13.276667**. He can continue checking naturally afterward. If the generated opening is slower, choose a better source phase or revise the picture cut after inspection; do not compensate with speed changes, a frozen hold or a claim that the planned action already exists.

This is an execution constraint, not a finding that an ungenerated take has failed. The plan's fixed9.833-second B window still needs sustained actual inspection.

## Timing and claim checks

No other concrete timing or claim defect was found in the inspected plan source:

- The55/24 cut is master1049.375,5ms before “He asks” at1049.38. The118/24 cut is master1052.000,20ms before “And this time” at1052.02. The local12 cut is master1059.083333,36.667ms before “He can read it” at1059.12. Total duration remains524frames and retains the selected1068.916667 low-energy endpoint.
- A's prompt slide at the start of “And this time” addresses the earlier hesitation risk. The direction keeps the old blank sheet untouched and makes the green binder the prepared-record carrier.
- TAKE A/B are explicitly “TO GENERATE”; both footers say reference image only and identify the missing action. The image alt text also states the binder actions are not generated. Future-tense plan semantics are clear despite present-tense action descriptions inside those labeled cards.
- Existing coverage names the owner and buyer; B makes him the independent reader. No adviser role, payment, sale, signature or approval verdict is introduced. The direction expressly ends on inspection and prohibits the misleading outcomes.

## Binding and limits

HTML SHA-256: `0e861e96f561c1cb42932177590f9f1327239a96ade49f9a1cd7dab2cd7d0543`

DIRECTION-v2 SHA-256: `81b0b434afd2b5d36708383ad11ddc36020ac71d1aac2c1ec984e497960e3b95`

These checks establish source-level cue logic and plan labeling only. Root owns rendered visibility, footage suitability, actual binder mechanics, normal-speed comprehension and final selection. No shared source/runtime/log/provider/gate was changed.
