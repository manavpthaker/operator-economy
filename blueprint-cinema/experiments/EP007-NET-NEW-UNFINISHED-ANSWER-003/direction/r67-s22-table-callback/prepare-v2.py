#!/usr/bin/env python3
"""Write the binder correction as new unsubmitted requests; preserve v1 evidence."""
from pathlib import Path
import hashlib,json,copy
D=Path(__file__).resolve().parent
ROOT=D.parents[4]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v): p.write_text(json.dumps(v,indent=2)+'\n')
a="""One continuous eight-second locked-off tripod shot at the exact workshop table in the supplied image. Preserve these same two adults, faces, hair, glasses, tan work shirt, steel-blue overshirt, daylight, table, green binder, blank sheet, pencil, keys and workshop background. Owner stays seated screen-left; buyer stays seated screen-right. Keep the camera fixed: no pan, zoom, orbit, drift, reframing or cut. Natural real-time motion.

One primary action: the owner promptly makes the existing green binder available to the buyer. Without a thinking pause, she places her hand on the closed green binder and slides it smoothly a short distance across the table toward his reach, along a clear route that does not cross the blank sheet, pencil or keys. It stays flat on the tabletop and closed. No hand-to-hand exchange. She releases it and returns her hand to rest. The buyer's eyes follow the arriving binder and settle on it; he remains seated, waiting to inspect it. Begin promptly, complete this single presentation gesture naturally in roughly two to three seconds, then maintain calm, purposeful attention to the delivered binder for the remaining handle.

The existing central blank sheet stays unchanged. No marks appear on it. No writing, pencil pickup, binder opening, second document, loose new page, repeat slide, reversal, handshake, nod of approval, satisfied smile, celebration, signature or closing gesture. No speech, lip movement or conversational pantomime. No new person or prop, object teleportation, changing binder size or color, hand morphing, collisions with other props or role reversal. This is making a preparation package available, not reaching an agreement."""
b="""One continuous eleven-second locked-off shot continuing the exact supplied frame and its settled binder position. Keep the same workshop, owner seated left in tan, buyer seated right in blue with glasses, daylight, table, green binder, original blank loose sheet, pencil and keys. Preserve the exact starting object positions and action line. Camera remains fixed: no movement, pan, zoom, orbit, reframing or cuts. Natural real-time motion.

One primary action: the buyer independently inspects the supplied green binder. Promptly lift its front cover once and open it toward his reading position. Inside is an already-prepared page with soft, indistinct rows of writing, visible as soon as the cover exposes it. Keep these existing rows stable, too small and oblique to read; no legible names, values, facts, prices or logos. Nothing is written or materialized in view. The original loose blank sheet stays untouched.

After opening, he reads down the exposed record with small natural eye and head movements, breathing and occasional blinks. He continues studying different parts of the same page through the end. His hand can rest lightly on its edge to keep it open. The owner keeps both hands at rest and allows him to inspect without explaining. End while he is still inspecting, with no decision or verdict.

No speech, lip movement, conversational gestures, writing, separate pointing or tracing, page turn, repeated opening or closing, new loose page, duplicated paper, empty binder page, changing page contents, binder or hand morphing, nod, smile, handshake, signature, offer, celebration, head shake or glance back to the owner. No frozen body, repeated gesture, optical slow motion or closing beat."""
b=b.replace('Promptly lift its front cover once and open it toward his reading position.', 'Promptly lift its front cover once and open it toward his reading position in about the first second, then begin reading immediately.')
for name,prompt in [('A',a),('B',b)]:
 original=json.loads((D/f'TAKE-{name}.request.json').read_text())
 original['revision']='v2_binder'
 original['input']['prompt']=prompt
 if name=='B':
  original['seed_dependency']['condition']='A passes identity, binder mechanics, prompt response and 170 usable frames.'
  original['seed_dependency']['selection_rule']='Extract a settled frame after the closed green binder is within buyer reach and the owner has released it. Bind frame number, source and PNG hashes before upload/submission. Do not submit B if A fails.'
 (D/f'TAKE-{name}-PROMPT-v2.txt').write_text(prompt+'\n')
 save(D/f'TAKE-{name}-v2.request.json',original)
event=json.loads((D/'DECISION.json').read_text())
event['event_id']='r67-s22-table-callback-plan-v2'
event['supersedes']='r67-s22-table-callback-plan-v1'
event['data']['choice']='Same table/question, then present the existing closed green binder; buyer opens and independently reads the prepared record.'
event['data']['reason']='Binder avoids implying the answer was simply overlooked on the reverse of the original blank sheet. Two primary actions retain the preparation-to-inspection change.'
event['data']['alternatives'].append({'choice':'Reverse the original blank sheet','reason_not_selected':'Could recast the original failure as an overlooked reverse side and needs risky paper-flip geometry.'})
event['data']['nuance']['replaces_event']='r67-s22-table-callback-plan-v1'
event['data']['nuance']['source_basis']='R67 independent footage-audit critique accepted; owner has not authorized paid generation.'
event['evidence']=[{'path':str((D/'DIRECTION-v2.md').relative_to(ROOT)),'sha256':sha(D/'DIRECTION-v2.md'),'locator':'Current binder direction'},
 {'path':str((D/'TAKE-A-v2.request.json').relative_to(ROOT)),'sha256':sha(D/'TAKE-A-v2.request.json'),'locator':'Current unsubmitted take A'},
 {'path':str((D/'TAKE-B-v2.request.json').relative_to(ROOT)),'sha256':sha(D/'TAKE-B-v2.request.json'),'locator':'Current unsubmitted take B; seed depends on A'},
 {'path':str((D/'COST-PROPOSAL.json').relative_to(ROOT)),'sha256':sha(D/'COST-PROPOSAL.json'),'locator':'Unchanged cost scope'}]
save(D/'DECISION-v2.json',event)
save(D/'CURRENT.json',{'status':'prepared_awaiting_separate_paid_authorization','direction':'DIRECTION-v2.md','requests':['TAKE-A-v2.request.json','TAKE-B-v2.request.json'],'cost':'COST-PROPOSAL.json','superseded_direction':'DIRECTION.md','paid_calls':0})
print(json.dumps({'revision':'v2_binder','paid_calls':0}))
