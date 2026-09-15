# R37 S08 cue and meaning audit

Both issued input hashes match. S07/S08/S09 context was read. This packet proposes timing anchors and meaning limits; it does not verify audio cuts, rendered motion, or owner acceptance.

## Exact interval and cut limitation

S08 speech is W000721–W000837, master **250.98–296.94**, review **247.98–293.94**. The new section starts at master250.625 / review247.625. Local time is master minus250.625.

S09 starts W000838, “That,” at master **296.95**, review **293.95**. Its first phrase, “That failure shows up in three shapes,” spans W000838–W000844, master296.95–299.03; the complete opening sentence ends W000851 at master301.28.

**No 24fps boundary fits the transcript's 10ms gap between S08 and S09.** Frame7126 is master296.916666667, before the declared S08 word end; frame7127 is296.958333333, after S09's declared onset. Neither can be called clean from this transcript. The cue JSON therefore leaves the recommended outpoint unset. Root should inspect original PCM and listen around the end of “selling it” and the following breath, then choose a measured frame. Do not cut the word to satisfy a neat duration. If continuing directly into S09, picture may cut at a motivated point while original narration remains uninterrupted.

## Meaning and reveal order

1. **Question before consequence.** W000726–W000736 asks the one-month absence question. Treat it as a test of dependence, not a declaration that this business fails when she leaves. S07 has established scrutiny, not a buyer rejection.
2. **Business or job.** W000742–W000756 establishes what the buyer is checking. The persistent business should remain recognizably the same object. Replacing it with a literal industrial machine risks losing the point that customer relationships, operations, and memory are part of the business.
3. **Revenue as evidence.** W000770–W000779 separates the revenue record from what is transferable. Do not make the record disappear as though revenue is false, or invent amounts or supporting financial documents. The picture can distinguish evidence of output from the operating arrangement that produces it.
4. **Operating without her.** W000780–W000795 states what the buyer wants. The ownership/operating dependency is the useful visual relation. Make more than order flow depend on the owner if the model represents the whole business; avoid a decorative machine or a sequence of repeated narration labels.
5. **Conditional failure.** The explicit branch starts with “And if” at W000796–W000797, master279.2–279.43 / review276.2–276.43. The owner-as-machine realization ends W000804 at master281.58. Only after this condition is established should the model expose an untransferable dependency. Keep the business intact: interrupt or expose the necessary connection rather than demolishing the company or asserting measured revenue loss.
6. **Handover versus sale.** W000815–W000825 describes failed transfer under that condition; W000826–W000837 states the requirement. It does not establish a completed transaction, a buyer's personal decision, or that a readiness service fixes the operations. A final green “sold” state, celebratory buyer, or automatic repaired route would add an unsupported outcome.

S09 will distinguish relationships, concentration, and records. S08 needs only to establish the common inspection/transfer question; it should not pre-empt all three examples or give this seller a definitive failed-sale verdict. A cue can trigger a state test without claiming that it happened to a real company.

## Handoff

`cues.json` contains the full S08 word sequence, phrase ranges, exact master/review/local clocks, and nearest-frame visual anchors. Those rounded anchors are optional directing positions, not source-audio cut approvals. The final outpoint needs the root's PCM finding. No files outside the assigned packet were changed and no source media, provider, paid service, or rendered runtime was used.
