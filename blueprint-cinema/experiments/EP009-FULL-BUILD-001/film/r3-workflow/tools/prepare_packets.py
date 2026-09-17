import json, pathlib, hashlib, datetime

ROOT=pathlib.Path.cwd()
BASE=ROOT/'blueprint-cinema/experiments/EP009-FULL-BUILD-001/film/r3-workflow'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def binding(p):return {'path':str(p.relative_to(ROOT)),'sha256':sha(p)}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
uploads={x['id']:x for x in json.loads((BASE/'UPLOADS.json').read_text())}
master=ROOT/'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/master/narration-master.wav'
transcript=master.parent.parent/'word-transcript.json'
words=json.loads(transcript.read_text())['words']
shared='''Continue the exact supplied first frame as a single uninterrupted live-action documentary shot. Preserve the same innkeeper, dark pinned-up hair, olive cardigan over cream shirt, wooden inn reception counter, laptop, guestbook, key cubbies, brass bell, daffodils, telephone, paper stacks, daylight, camera position and existing object geography. Maintain natural human anatomy and object permanence. Fixed tripod camera, normal real-time movement, no zoom, no pan, no cuts, no slow motion. Narrated observation: external narration will carry all words. The innkeeper keeps her mouth closed throughout; nobody speaks, mouths words, nods approval, smiles for the camera, or looks at the viewer. Keep existing printed marks and screens soft and unreadable; no invented legible numbers, text, logos, booking confirmations, signatures, charts, or outcome indicators. No new objects or people appear. No effects, music or audio. '''
specs=[
('WF00-F06','seg031','S08',[9511,9685],8,'listening',1108,1128,
'The innkeeper is already listening on the telephone in exactly the pose of the first frame, with her other hand resting on the existing paper stack. She remains listening with closed lips. Her gaze makes one small natural settling movement toward the paper and then stays there. Keep the receiver against her ear and the free hand still. Only quiet breathing and an occasional natural blink. Do not lift, transfer or hang up the receiver. Do not type, reach for keys, write, gesture, or perform a second activity. End in the same listening posture.',
'The owner must find time for reservation follow-up while handling ordinary inn work. The image shows competing work already in progress; it does not reenact every narrated task.',
'Restore the missing human work beat using an already-listening start and one small eye adjustment.',
'Does quiet listening remain anatomically stable with lips closed and no failed telephone/key handoff?'),
('WF01-monthly','seg041','S11',[14843,14980],8,'world',1739,1753,
'One primary action: the innkeeper uses her left hand, on the window/telephone side, to draw the top sheet of the existing paper stack beside the telephone a short distance toward herself and reads it. She stays seated behind the laptop. Make this a modest single reach and paper draw within the first four seconds, then hold her attention on the paper. The other hand stays near the laptop. No turning the sheet toward camera, no writing, no phone pickup and no reaction implying good results. Keep the laptop and vase stationary. End with the top sheet separated slightly from its stack, still resting on the counter beside the laptop.',
'A monthly owner report is the deliverable under discussion. The world remains the same small inn; no real report contents or performance are asserted.',
'Make the monthly report a physical object reaching the owner rather than another diagram.',
'Does the owner handle one existing sheet naturally without hand/flower/laptop collision or implied result?'),
('WF02-reports','seg048','S14',[18105,18200],8,'reports',2130,2138,
'The foreground practitioner is represented only by the two existing hands and charcoal knitted sleeves. One primary action: the right hand slides the existing right-hand printed report a few centimeters left and slightly forward until it sits neatly beside the left report. The left hand steadies the left sheet in place. Complete the small alignment in the first three seconds, then let both hands rest. The innkeeper remains quietly occupied behind the laptop, mouth closed. Do not lift the pages, point, write, touch the phone, or add sheets. End with two separate papers side by side; their print remains unreadable.',
'The practitioner is gathering the two source reports before computing the commission line. Computation returns to the designed plate after this insert.',
'Show the concrete act of bringing two source documents together with one simple page alignment.',
'Are two separate sheets retained and aligned with stable fingers, unreadable print and no implied calculation result?'),
('WF03-phone','seg048','S14',[18294,18399],8,'phone',2150,2160,
'The foreground practitioner holds the existing black smartphone in the left hand. The existing RIGHT INDEX FINGER is already poised at the screen. One primary action: that same right index finger makes one deliberate light tap on the screen within the first two seconds and withdraws a small distance. Then both hands hold steady while the practitioner inspects the phone. Preserve the grip and finger anatomy from the reference; do not substitute a thumb or switch hands. The screen remains soft, oblique and unreadable, with no visible confirmation or purchase. No scrolling, typing, swipe, second tap or extra choreography. The innkeeper stays occupied behind the laptop with closed lips. End holding the phone in the same orientation.',
'The practitioner tests the guest-facing direct path on a phone. This illustrates testing, not an actual booking, product UI or successful conversion.',
'Make the guest-path check visibly physical with one index-finger tap and inspection pause.',
'Does one index tap read at speed with stable hands and no fabricated legible UI or booking result?'),
('WF04-exception','seg053','S15',[20491,20682],10,'reports',2377,2397,
'The two existing reports stay flat on the counter. The foreground practitioner uses the RIGHT INDEX FINGER for one slow tracing action down a short section of the right-hand report, then stops at one row and holds. Begin the trace around the second second, finish by the fifth second, and preserve a quiet inspection pause through the end. The left hand keeps the left report still. Do not shift sheets or write. The innkeeper remains neutral and task-focused behind the laptop, with her lips closed. No pleased reaction, nod, head shake, pointing toward the viewer, or comparison graphics. Keep all paper marks unreadable and unchanged. This is patient inspection of an unresolved report, without a demonstrated positive or negative result.',
'The narration says the report must show an unchanged metric honestly and trigger investigation. No numeric outcome is established by this illustrative image.',
'Let inspection and an unresolved pause carry the exception-report beat without decorating it with invented results.',
'Does the tracing gesture resolve into inspection without suggesting fabricated proof or a celebratory result?'),
('WF05-answer','seg063','S19',[25999,26120],8,'reports',2997,3014,
'The foreground practitioner records a brief note. The right hand picks up the existing black pen immediately to the right of the right-hand report, then makes one short handwritten note near the lower right part of that same sheet. Keep this one purposeful writing activity compact: secure the pen within the first two seconds, write a few small strokes during seconds two through four, then rest with the pen tip just above the paper. The left hand keeps the left report still. Do not sign, draw a checkmark, present a document, shake hands, exchange money, or show a legible yes/no answer. The innkeeper stays neutral behind the laptop, mouth closed, no approving nod. No fabricated acceptance or sale. End on the brief unreadable note with stable pen and fingers.',
'The practitioner must put the proposed retainer under the economic ceiling and record each owner answer. No specific answer or successful sale has been established.',
'Finish the fieldwork instruction with the physical act of recording an answer, without staging acceptance.',
'Does writing read as a short neutral note with a persistent pen and stable fingers, without legible answer or implied sale?')]
shots=[]; requests=[]
for index,(sid,segment,scene,frames,duration,ref,wa,wb,action,context,intent,review) in enumerate(specs,1):
 d=BASE/sid;d.mkdir(exist_ok=True)
 prompt=shared+action+' Output 16:9.'
 (d/'PROMPT.txt').write_text(prompt+'\n')
 params={'model':'kling3_0','mode':'pro','sound':'off','aspect_ratio':'16:9','duration':duration,'count':1,'prompt':prompt,'medias':[{'role':'start_image','value':uploads[ref]['media_id']}]}
 selected=[w for w in words if wa<=int(w['w_id'][1:])<=wb]
 shot={'id':sid,'index':index,'segment':segment,'scene':scene,'original_frames':frames,'original_master_in':frames[0]/24,'original_master_out':frames[1]/24,'target_frames':frames[1]-frames[0],'generation_duration':duration,'expected_cost_credits':duration*1.75,'reference':uploads[ref],'prompt':binding(d/'PROMPT.txt'),'scene_context':context,'editorial_intent':intent,'picture_audio_mode':'narrated_observation','language_carrier':'locked external narrator','visible_speech':'prohibited','face_function':'task_focus','direction_facts':{'camera':'fixed tripod at first-frame position','primary_action':action,'world':'recurring innkeeper and inn retained','media_truth':'illustrative generated plate, not evidence','effects':'none','factual_claims_from_image':'none'},'cue_words':selected,'exact_passage':' '.join(w['token'] for w in selected),'review_question':review,'review_status':'pending_encoded_footage_review'}
 if sid=='WF00-F06':shot['reference_extraction']={'raw_source':binding(BASE.parent/'F06/raw.mp4'),'frame_index':150,'fps':24,'selection_note':'Start image only; prior failed take remains rejected.'}
 if sid=='WF04-exception':shot['cue_note']='Last narrated word ends at861.9 after picture cut861.75; locked master audio remains uninterrupted.'
 write(d/'DIRECTION.json',shot);shots.append(shot);requests.append({'index':index,'params':params})
plan={'schema':'ep009-workflow-film-plan/v1','created_at_utc':now,'status':'ready_for_exact_price_preflight','owner_authority':'Root relayed approved owner revision direction and six take authorization; canonical decision ep009-owner-r2-revision-direction retained by root.','master':binding(master),'word_transcript':binding(transcript),'target_format':{'width':1280,'height':720,'fps':24,'speed':1},'shots':shots,'total_base_generation_seconds':50,'total_base_credits':87.5,'total_target_frames':sum(x['target_frames'] for x in shots),'review_only':True}
write(BASE/'PLAN.json',plan)
write(BASE/'REQUESTS.json',{'plan':binding(BASE/'PLAN.json'),'requests':requests})
budget={'created_at_utc':now,'status':'authorized_not_yet_submitted','original_shared_higgsfield_cap':2000,'original_presenter_consumed':1872,'original_film_prior_consumed':20,'original_total_prior_consumed':1892,'original_film_reallocated_cap':128,'original_film_new_headroom':108,'base_six_takes':87.5,'one_optional_8_second_retry_max':14,'maximum_planned_new_spend':101.5,'remaining_original_after_base':20.5,'remaining_original_after_retry':6.5,'setup_stills':{'provider':'built-in image_gen','higgsfield_credits':0,'price':'not exposed; no Higgsfield debit claimed'},'pending_additional_presenter_reservation':1607,'latest_preworkflow_live_balance':1719,'minimum_live_balance_after_base':1631.5,'minimum_live_balance_after_retry':1617.5,'original_fal_cap_usd':40,'original_fal_reallocation':{'presenter':24.50,'film':15.50},'new_fal_calls':0,'constraints':['Never exceed original shared2000','Never spend1607 pending presenter reservation','One retry only for explicit rejected take with bounded fix','No Fal paid attempts','No extra generation or still-model charges inferred']}
write(BASE/'BUDGET.json',budget)
print(json.dumps({'shots':len(shots),'base_credits':87.5,'target_frames':plan['total_target_frames'],'requests_sha256':sha(BASE/'REQUESTS.json')}))
