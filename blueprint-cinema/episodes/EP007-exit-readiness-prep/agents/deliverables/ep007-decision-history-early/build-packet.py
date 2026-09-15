import json,pathlib,hashlib,re,datetime
ROOT=pathlib.Path.cwd()
OUT=ROOT/'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/deliverables/ep007-decision-history-early'
WO=ROOT/'blueprint-cinema/episodes/EP007-exit-readiness-prep/agents/work-orders/ep007-decision-history-early.json'
w=json.loads(WO.read_text())
B='blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes'
F='blueprint-cinema/episodes/EP007-exit-readiness-prep/review/decision-history/owner-feedback.json'
fb=json.loads((ROOT/F).read_text())['messages']
byid={m['id']:m for m in fb}
sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def ref(path,a,b):return {'path':path,'lines':[a,b],'sha256':sha(path)}
def r(v,file,a,b):
 ds={3:'r3-relevant-edit',4:'r4-question-first',5:'r5-rough-question',6:'r6-character-first',7:'r7-rapport-pause',8:'r8-context-coverage',9:'r9-realization-model',10:'r10-film-to-presenter',11:'r11-presenter-first',12:'r12-logo-led',13:'r13-unanswered-job',14:'r14-opening-bridge'}
 return ref(f'{B}/reviews/{ds[v]}/{file}',a,b)
def feedback(*ids):
 result=[]
 lines=(ROOT/F).read_text().splitlines()
 for i in ids:
  m=byid[i];n=next(j for j,l in enumerate(lines,1) if f'"id": "{i}"' in l)
  result.append({'message_id':i,'quote':m['text'],'timestamp':m['timestamp'],'source_session':m['source_session'],'source_session_line':m['source_line'],'extract_reference':ref(F,n,n+6)})
 return result
STYLE='msg_01a079f2-7558-72c1-bc43-0b0bdd0c82c4';MEANING='msg_01a07a1c-8948-7280-bb82-42398f918ebe';EQ='msg_01a07abd-c7d2-70c3-a654-3bb58ff81f59';HANDS='msg_01a07add-323b-7b41-944d-fe3e498fb791';CHAR='msg_01a07ae0-a7e6-72d1-8166-f9e30e818e77';RAP='msg_01a07e78-c469-74b0-99b7-9aac4e670526';COV='msg_01a08149-ea63-7f01-92cc-264f64306a5e';DYNAMIC='msg_01a0814e-6903-7cc3-8667-05ea044ec717';R8GOOD='msg_01a081e2-50a9-7a92-8e25-c20c392ecd7d';GRID='msg_01a0820e-4e44-78d2-9ff7-2bb4a8bfc5d7';OPEN='msg_01a0873a-fcad-7672-a54e-419ddb1356e0';LOGO='msg_01a08795-a169-7a53-a9f8-8723d1068124';REDUND='msg_01a087a0-550a-7f32-9322-056814c7842e';OVER='msg_01a087b9-d63e-7ed3-8094-44114465bbfc';REJECT='msg_01a087c9-a113-7772-8bd3-80afd3dae35f'
versions=[]
def version(id,scope,change,reason,outcome,refs,msgs=(),binding='Direct artifact description; feedback-to-version mapping follows explicit brief/review where available, otherwise temporal sequence and described content.'):
 versions.append({'version':id,'scope_and_clock':scope,'change':change,'rationale_attribution':reason,'historical_disposition':outcome,'evidence':refs,'owner_feedback':feedback(*msgs),'feedback_version_binding':binding,'approval_boundary':'Historical creative disposition only. No new approval or canonical production gate is claimed.'})
version('base-revision-C','Master 0–59.86; root declares 30fps. Brief describes generated still-plate animatic, not live moving footage.',
 'Bright functioning workshop; shared blank operating sheet/work ticket; page approach 26.80–27.92 and proposed match cut into explicit BUSINESS AS IT RUNS TODAY − OWNER FOR 30 DAYS = ?; three condition labels; incomplete oxide practice path; identity/title.',
 {'assistant_intent':'Turn one observable owner-dependent task into mental arithmetic without asking generated footage to create legible page text. Trust → curiosity → quiet recognition → constructive possibility.','owner_directive':'No version-specific acceptance established in assigned base sources.'},
 'Historical starting hypothesis; later trials remove page-transform premise and challenge premature diagnosis.',[ref(B+'/BRIEF.md',10,15),ref(B+'/BRIEF.md',41,67),ref(B+'/STORYBOARD.md',18,31),ref(B+'/index.html',39,48)],binding='Base metadata explicit; no attempt to rename older experiments as R1/R2.')
version('R3','Isolated master 17.96–35.08, local 0–17.12 at 30fps authored cadence; native source 24fps.',
 'Retain Kling; question 0–3.32, c03 gesture 3.32–9.96 (source .625–7.265), arithmetic at local9.96/master27.92 by hard editorial cut. Later same-folder rough-line correction replaces thick smooth contours with114 fixed short partial paths.',
 {'owner_directive':'Keep Kling with a relevant edit; restore overlapping thin rough lines.','assistant_intent':'Gesture arrest chosen near narrated stops; fixed1.093×crop excludes invented right-edge paper.','agent_finding':'Rough style improved, but three-problem/owner-departure/stopped-token explanation diagnosed a failure too early.'},
 'Conditional candidate; agent recommends revising meaning, not accepting merely because sketch/runtime checks pass.',[r(3,'REVIEW.md',7,27),r(3,'REVIEW.md',39,49),r(3,'edit-decisions.json',18,60)],('msg_01a079cc-5ba1-72a2-83ba-09b5d8d33f8f',STYLE,MEANING))
version('R4','Same master17.96–35.08; last local9.96–17.12 redesigned.',
 'Remove three conditions, routes, owner checkpoint/departure, work token and evidence header. Keep typeset unanswered equation with only six rough subtraction-rule passes.',
 {'assistant_intent':'Establish the question without asserting business failure or prematurely revealing later mechanisms.','owner_response':'Questions whether the sketch was discarded for a simple equation.'},
 'Trial technically checked; later R5 brief calls this an overcorrection. Approval to try did not approve the process or full opening.',[r(4,'BRIEF.md',18,40),r(4,'REVIEW.md',8,19),r(4,'STORYBOARD.md',6,20),r(5,'BRIEF.md',6,9)],(EQ,))
version('R5','Same master17.96–35.08; only last7.16s changes.',
 'Replace equation with rough worktable and empty owner chair, conditional IF THE OWNER IS AWAY / FOR A MONTH? and open question. Draw completes local13.68 then holds.',
 {'owner_directive':'Restore meaningful rough illustration.','assistant_intent':'Clearly hypothetical absence without owner departing, task failing or later mechanism.','owner_response':'Illustration still does not convey intended idea; film only shows hands; drawing-to-screen relationship is not legible.'},
 'Style and hypothetical semantics passed bounded agent QA, but owner questioned meaning and opening context. Leads to character-first film.',[r(5,'BRIEF.md',6,14),r(5,'REVIEW.md',6,14),r(5,'REVIEW.md',21,35)],(HANDS,CHAR))
version('R6','Full cold-open master0–44.50; 24fps.',
 'Film only: wide0–15, owner medium15–30, closer owner30–44.5; establish both faces before small stalled gesture and unresolved concentration. Remove opening sketch.',
 {'owner_directive':'Opening should show characters.','assistant_intent':'Three setups, task-focused narrated observation without literal acted speech.','owner_response':'Look and feel better, but little interaction or eyeline rapport; no stakes/ebb and flow matching narration.'},
 'Photographic direction retained, relationship/performance direction revised into R7. No supplied R6 REVIEW.md exists in assigned inputs.',[r(6,'BRIEF.md',6,13),r(6,'STORYBOARD.md',1,23),r(6,'index.html',16,22)],(CHAR,RAP))
version('R7','Master10.92–27.92, local0–17.00.',
 'Two takes: warm shared rapport A source.32–10.68 at0–10.36, closer attempted response B source0–6.64 at10.36–17. Source in moved from.50 after performance inspection.',
 {'owner_directive':'Need actual interaction, attention and stakes; retain look/Kling.','assistant_intent':'Warmth → focused question → open-hand explanation arrests; gaze break carries spoken stop.','agent_finding':'Gesture stops earlier than exact words; B mouths words and introduces small yellow prop. Technical checks do not clear literal no-speech brief.'},
 'Owner liked conversation and answer cut, requested buyer/question and closer answer coverage; defects retained as bounded review findings.',[r(7,'BRIEF.md',8,16),r(7,'REVIEW.md',3,18),r(7,'STORYBOARD.md',5,23)],(RAP,COV))
version('R8','Master10.92–27.92; local0–17,408frames/24fps.',
 'Rapport0–3.833333; buyer question3.833333–10.083333; owner readiness/answer/stop10.083333–17. New source ins revised .75→0 after audition without shifting record boundaries. Explicit narrated dramatization replaces rigid no-mouthed-words approach.',
 {'owner_directive':'Keep conversation; cut to buyer asking, close before owner tries to answer; make skill choose tools from scene context.','assistant_intent':'Anticipatory close-up and protected reaction hold, not compulsory cut frequency.','agent_finding':'Mouth action approximate; buyer foreground departure may imply withdrawal; no exact four-words claim.'},
 'Owner said much better and otherwise great, noted mouths do not match narration, requested further stress/realization close-up. Historical creative response does not certify phoneme sync.',[r(8,'BRIEF.md',8,16),r(8,'REVIEW.md',11,27),r(8,'STORYBOARD.md',3,12),r(8,'index.html',19,22)],(COV,DYNAMIC,R8GOOD))
version('R9','Master10.92–44.503333; local0–33.583333,806frames/24fps.',
 'Preserve R8 first408frames; realization D17–24.166667 source.416667–7.583333; rough owner-dependent model24.166667–33.583333. Three functions converge; owner moves aside, terminal connection opens; ticket travels then waits; one oxide question.',
 {'owner_directive':'Add closer realization through arithmetic, then illustration; recover earlier strong illustration.','assistant_intent':'Move from behavior to explanation by hard cut; fixed thin overlapping fragments and large business-owner arrangement.','owner_response':'Grid relationship to narration not understood.','later_agent_correction':'The final line means a new sale-readiness practice opportunity, not her existing business hidden inside her.'},
 'Film D retained later; grid/model rejected as clarity solution. Earlier remembered approved illustration was never identified with certainty.',[r(9,'BRIEF.md',8,15),r(9,'REVIEW.md',7,11),r(9,'STORYBOARD.md',5,26),r(10,'BRIEF.md',6,10)],('msg_01a081e5-80af-7812-846c-36f4e328c7cb',GRID))
version('R10','Master10.92–74.086667; local0–63.166667/1516frames.',
 'Replace R9 model with shared aftermath E24.166667–33.583333; wordmark33.583333–37.583333; exact-introduction TestQ avatar37.583333–63.166667. R8A–C/R9D source windows preserved.',
 {'owner_directive':'Try corrected film-to-presenter path; explicitly use TestQ.','assistant_intent':'Keep unresolved meeting through opportunity tease; presenter names show/practice. Detailed owner-dependency mechanism deferred to S08 with exact words.','agent_finding':'E lips remain partly open longer than requested; Q recurring hand/chin beats; in-app runtime showed stale presenter image although Chrome and snapshots matched sequence.'},
 'Isolated comparison, later R11 replaces structure/selected presenter. No whole-opening or performance acceptance inferred from generation.',[r(10,'BRIEF.md',6,14),r(10,'STORYBOARD.md',11,35),r(10,'REVIEW.md',22,28)],('msg_01a08216-859d-7f60-808a-b934104af22b',OPEN))
version('R11','Full master0–59.5,1428frames/24fps; no silence edit yet.',
 'Presenter begins0–4.041667 then film wide/owner/buyer reframes. Question screen17.75–21; protected answer21–27.916667; stare27.916667–30.208333; rough arithmetic30.208333–35.083333; room35.083333–40.083333; presenter opportunity40.083333–44.5; sting44.5–48.541667; identity avatar48.541667–56.041667; titleto59.5.',
 {'owner_directive':'Film alone too long for attention: start avatar, cut mid first sentence, preserve film closeups, restore question, arithmetic after stare, avatar return, sting/title.','assistant_intent':'Each medium owns a different narrative job; preserve original narration using selected404 performance retargeted bySync3.','agent_finding':'Comparison did not prove a platform-wide winner; digital closeups are crops and reaction is subdued rather than acute stress.'},
 'Assembly becomes baseline; owner next removes identity-avatar interruption, then challenges arithmetic redundancy. Exact narration remains authority.',[r(11,'BRIEF.md',7,15),r(11,'REVIEW.md',8,14),r(11,'REVIEW.md',33,41),r(11,'STORYBOARD.md',5,22),r(11,'index.html',19,33)],(OPEN,LOGO,REDUND))
version('R12','Master0–59.5; local same, before silence trim.',
 'Logo now44.5–56.041667 through all show promise; remove48.541667 identity-avatar cut; retain title56.041667–59.5. Post-title presenter59.5–74.5 planned but not yet mounted.',
 {'owner_directive':'Keep logo through BUILD OWN OPERATE into title; avatar explains episode afterward.','assistant_intent':'Institutional identity owns show promise, title names subject, presenter owns explanation. Finite entrance then stillness.','source_constraint':'No matching selected404 take for next15s; cannot reuse wrong speech/loop short12.04s source.'},
 'Identity architecture retained in accepted R13. Post-title pickup remains separate from creative edit authorization.',[r(12,'BRIEF.md',7,15),r(12,'REVIEW.md',5,7),r(12,'REVIEW.md',17,23),r(12,'STORYBOARD.md',5,13)],(LOGO,REDUND))
version('R13','Review0–56.5; master0–45 then48–59.5. Master45–48 pure silence removed.',
 'Only arithmetic slot30.208333–35.083333 becomes one worker/customer-job-sheet/owner handoff. Offer local.375–1.125; hypothetical owner removal scene2.125/master32.333 on not. Persist sheet/worker/furniture. Logo44.5–53.041667; title53.041667–56.5; This starts45.52,1.02s after logo.',
 {'owner_directive':'Arithmetic feels decorative; make problem illustrative and reduce excess pre-intro pause.','assistant_intent':'Specific interrupted decision rather than equation; preserve uncertainty and original words.','later_owner_response_in_range':'Much better; later removes R14 overlays and calls intro good to go.'},
 'Exact R13 intro creatively accepted after R14 rejection, per INTRO-DECISION; future mechanism revisions not adjudicated in this early packet.',[r(13,'BRIEF.md',7,13),r(13,'REVIEW.md',9,22),r(13,'STORYBOARD.md',9,35),ref(B+'/reviews/INTRO-DECISION-20260909.md',3,21)],(REDUND,'msg_01a087a5-c0f2-7d43-8a5f-23176e27a24f','msg_01a087b5-6d9a-7992-b049-c37670e30ea1',REJECT))
version('R14','Review0–56.5; unchanged R13 audio/picture except overlay2.5–7.666667.',
 'Test25 years at2.5 over avatar, persists across4.041667 filmcut; Profitable at6.375, both clearby7.666667 beforeownerclose7.708333. Brief opacity changes; no sketches/count-up/captions.',
 {'owner_directive':'Try text/motion that bridges avatar to film to engage viewers.','assistant_intent':'Fixed overlay ties two carriers without masking face or changing timing.','owner_response':'Does not add; remove; maybe reserve attention graphics/text for shorts/clips.'},
 'Explicitly rejected for inclusion; revert active intro toR13. Not a ban on purposeful diagrams/evidence/question/title screens or an approved shorts treatment.',[r(14,'BRIEF.md',7,13),r(14,'STORYBOARD.md',5,13),ref(B+'/reviews/INTRO-DECISION-20260909.md',3,21)],(OVER,REJECT))

cases=[]
def case(id,title,context,job,form,alternatives,selected,rejected,cues,continuity,reuse,avoid,refs,msgs,classification='Conditional craft inference grounded in this episode; requires fresh narrative fit in every new scene.'):
 cases.append({'case_id':id,'title':title,'context':context,'narrative_job':job,'form_and_style':form,'candidate_alternatives':alternatives,'selected_rationale':selected,'rejected_rationale':rejected,'cue_constraints':cues,'continuity_constraints':continuity,'reuse_when':reuse,'do_not_apply_when':avoid,'evidence':refs,'owner_feedback':feedback(*msgs),'portability_status':classification})
case('early-01','Rough pencil is a construction language, not a filter',
 'Owner recognized a regression from overlapping thin sketches to hard polished linework in R3. Meaning review separately found the model premature.',
 'Keep human/model character while allowing viewers to inspect an unfinished dependency.',
 {'drawing':'Short partial contours, unequal retraces, open corners, overshoot, sparse hatch, pressure variation; no heavy clean master beneath noise.','animation':'Fixed authored geometry, deterministic reveal respecting opacity tiers, stable after settle.','text':'Exact orientation text typeset, not fake handlettered UI.','historical_parameters':'R3:114paths;1/1.45/2/2.55px;settledopacity.34/.64/.92. R9:2045 fixed fragments. Counts and widths are implementation-specific.'},
 ['Continuous5–6.4px vector contours','Roughness filter over clean shape','Independently authored partial/retraced thin strokes'],
 {'owner':'Asked thin overlapping rough lines.','agent':'114-path repair visibly read rough; preserves intentional lighter construction marks.'},
 {'agent':'Revealing every mark atopacity1 erased pressure variation; polished master contours read marker/vector. Passing style does not prove meaning.'},
 ['Normalize fragment staggering inside existing semantic reveal windows; adding strokes must not extend the beat.','Do not animate completed marks to demonstrate roughness.'],
 ['Retain objectidentity,layout,text,cuewindows when doing style-only repair.','Reference supplies mark language only, not hotel objects/layout.'],
 ['A WorkingModel surface is selected and rough drawn reasoning suits its status.','Explicit owner/design reference identifies markmaking as part of accepted language.'],
 ['An evidence document needs exact reproduction.','The mechanism is confusing: solve causal meaning before polishing lines.','Phone scale cannot retain faint strokes without losing primary form.'],[r(3,'REVIEW.md',39,51),r(3,'REVIEW.md',7,17),r(9,'REVIEW.md',7,18)],(STYLE,MEANING))
case('early-02','Do not replace a confusing explanation with literal narration arithmetic',
 'R3 exposed too many diagnoses; R4 withheld them using an equation, R5 restored an empty-chair sketch, and R11 arithmetic was again called decorative.',
 'Let the viewer formulate the month-away question while gaining a visible operational implication.',
 {'allowed':'Explicit conditional example with a concrete decision/object; rough illustration if it adds understanding.','withheld':'Detailed relationships/concentration/records explanation before relevant script stage; confirmed failure or zero valuation.'},
 ['Three categories plus owner departure/stoppedtoken','BUSINESS − OWNER = ?','Conditional emptychair/table','One concrete worker-to-owner job handoff'],
 {'historical':'R13 selected the handoff after earlier equation/emptychair trials; it gave a concrete business interaction.','critical_limit':'This early packet records acceptance at that time; later audit must still verify that present/absent conditions visibly differ.'},
 {'owner':'R4 removed the desired sketch; R5 illustration did notmake sense; R11 arithmetic felt like animation for its own sake.','agent':'R3 diagnosed failure too early; equation merely paraphrased rather than showing what becomes uncertain.'},
 ['Use actual arithmetic line only as interpretation context, not a command to draw math.','Keep graphic within earned narrative scope; do not import later three-case diagnosis.'],
 ['Business remains functioning; no customer loss,collapse,zero-price inference.','Hypothetical condition must be distinct from observed fact.'],
 ['Audience lacks a visible model of who decides/how work proceeds when owner absent.','A concrete intervention can reveal a causal difference.'],
 ['Removing the diagram loses no understanding.','Both compared states show identical outcome without a baseline completed action.','The only added value is labels repeating narration.'],[r(4,'BRIEF.md',18,40),r(5,'REVIEW.md',6,14),r(13,'STORYBOARD.md',13,17)],(EQ,HANDS,REDUND))
case('early-03','Establish people before using a hand or page as the transition carrier',
 'The early film framed hands/pencil and the illustrated scene did not look causally connected to the page. Owner wanted characters in the opening.',
 'Establish who is affected, their relationship and capable business context before attention narrows to a task.',
 {'coverage':'Character two-shot/master first, then purposeful closer coverage.','transition':'Hard editorial cut from behavior into authored explanation when no true visual continuity is supplied; page-plane match requires a visible shared carrier.'},
 ['Hands-only opening + claimed page-to-screen match','Characters first + hand detail later','Hard cut into independent explanation'],
 {'owner':'Opening should show characters.','agent':'R6 removed unrelated opening sketch and showed readable owner/buyer faces; R9 later states no physical-page transformation.'},
 {'owner':'Drawing becoming onscreen animation did not come across.','agent':'Blank generated paper plus unrelated diagram cannot establish continuity by assertion.'},
 ['Base proposed26.80–27.92 approach was abandoned, not a continuing default.','R3 uses hardcutatmaster27.92/Because; R9 behavior→explanationatmaster35.086667.'],
 ['Ownercapable,buyercollaborative,workshopfunctioning.','No tracked false writing or invented legible generated documents.','A future matched transition needs geometry/object/action continuity demonstrable on both sides.'],
 ['A scene introduces unfamiliar characters or relationship stakes.','Object detail is only meaningful once participant roles are known.'],
 ['Roles already established and insert reveals new information economically.','A diagram legitimately stands alone and no filmed-pageorigin is implied.','An episode needs presenter/evidence first; characters-first is not universal opener.'],[ref(B+'/BRIEF.md',43,55),r(3,'REVIEW.md',21,27),r(6,'BRIEF.md',6,11),r(9,'STORYBOARD.md',26,26)],(HANDS,CHAR))
case('early-04','Performance mode follows scene context: observation and dramatization differ',
 'R6 no-speech task focus produced weak rapport. R7 generated mouths despite nonverbal prompts. Owner liked the conversation and R8 adopted explicit narrated dramatization.',
 'Professional ease becomes a real interpersonal question, attempted answer and interruption, with narration carrying essential language.',
 {'mode':'Narrated dramatization allows illustrative interaction/mouthmovement; neither exact dialogue norcaseevidence. Presenteraddress later requires synchronized visible speech.','performance':'Mutualeyelines,smallwarmacknowledgment,focusedattention,unfinishedgesture,patientbuyer; restraint should not eliminate interaction.'},
 ['Rigidclosed-mouth task-only observation','Illustrative narrated conversation with mode/disclosure','Synchronized literal dialogue','Adversarialreaction or shock'],
 {'owner':'Wanted interaction, rapport and ebb/flow; liked conversation despite words/mouth mismatch.','agent':'R8 mode makes narrator the language carrier and allows scene-specific conversational behavior.'},
 {'agent':'No-speech claim could not clear R7 actual B mouthshapes. Owner collapse or buyer withdrawal implies an unsupported outcome.','owner':'R6 look alone lacked stakes.'},
 ['Protectownerattempt/stop across narrated21.28–26.80 and subsequent pause.','Use source audition to choose strongest causedgesture/gazecue; do not falsely call exactfourwords.'],
 ['Ownerleft,buyerright;reciprocalgaze;consistentwardrobe,light,tableprops.','Review buyer foreground movement: exiting mayreadrejection.','No new audible dialogue/narration.'],
 ['Narration explicitly supplies meaning of fictionalillustrativeinteraction.','The mode and disclosure make relation to audible words clear.'],
 ['Documentaryobservational footage appears tomissanaudibleline.','Literalquoted/testimonial words demand actualsync.','Presenteraddress is expected: approximate dramatization mouthmovement isinsufficient.'],[r(6,'STORYBOARD.md',7,22),r(7,'REVIEW.md',7,18),r(8,'BRIEF.md',8,16),r(8,'REVIEW.md',17,25)],(RAP,COV,DYNAMIC,R8GOOD))
case('early-05','Cuts transfer dramatic responsibility; holds protect the action',
 'Owner asked for buyer close-up atquestion and ownercloseup before attemptedanswer, then closerrealization afterstop. Morecuts meant moreusefulcoverage, not a fixedfrequency.',
 'Letviewer see whointroduces challenge, anticipate answer, witness interruption, then read consequence.',
 {'grammar':'Sharedmaster → buyerquestion → anticipatoryownerclose → uninterruptedattempt/stop → tighterrealization → sharedaftermath. Hardcuts default; actualperformance suppliesmotion.','framing':'Digitalowner/buyercrops of samecontinuouswide retained in R11; distinguish crop from anewcameraangle.'},
 ['One long sharedshot','Uniform15secondchunks','Randomtightening on every sentence','Question/answer/consequence-driven coverage'],
 {'owner':'Liked smallanswercut; wanted buyeraskingandclose beforeheranswer.','agent':'R8 moves toownerbeforefirstanswerword and preservesstop; R9 adds causedrealization; R11 tightens fullopening usingexistingcontinuoussource.'},
 {'agent':'Narration alone is not a cutquota; gratuitoustransition would interrupt recognition.','performance_limit':'R8 B asks earlierthanrequested; C mouth settlesearly. Trims adapt pictureswithout changingVO.'},
 ['R8localcuts3.833333,10.083333; master14.753333,21.003333.','R8A source.32–4.153333; B0–6.25; C0–6.916667.','R9D local17–24.166667; master27.92–35.086667; source.416667–7.583333.','R11roomreturn35.083333,avataropportunity40.083333.','Recordbothexactcueintentandactualdeliveredperformanceoffset.'],
 ['Samecast,screenaxis,propsandlight.','Do not cutaway duringinterruptedanswer justtocreateactivity.','Inspect actualgeneratedtake before locking sourcein/out; availablehandles constrainchoice.'],
 ['Dramaticresponsibility changes orviewer needsreactionbefore/afteraquestion.','Alternateframing providesmeaning that widecannot.'],
 ['Continuousactionwould losecausalityacrosscut.','Aninsertmerely repeatsalreadyvisibleaction.','Performance sourcecannotfillselectedwindowwithoutloop/freezeretime.'],[r(8,'REVIEW.md',11,25),r(8,'STORYBOARD.md',10,12),r(9,'STORYBOARD.md',5,9),r(11,'STORYBOARD.md',7,22)],(COV,R8GOOD))
case('early-06','Resolve the referent before designing the visual metaphor',
 'R9 model on “business hiding inside it” showed her existing business/ownerrelationship. R10 explicitly corrected that phrase to a sale-readiness practice opportunity.',
 'Shiftfrom unresolvedsalequestion to a newpractice somebodycouldbuild; do not silentlychange scriptmeaning.',
 {'appropriate_carrier':'Sharedaftermath orpresenteropportunitytease; latermechanismwhenwordsactuallyexplain independence.','metaphor_boundary':'A businessbox is not validmerelybecausevoice says business.'},
 ['Widenownerdependencygridinsidetheexistingbusiness','Remainwithhumansandunresolvedpause','Presenterintroducesnewpractice','Deferredownerdependencymechanismatlaterbusiness/jobcontrast'],
 {'agent':'R10 removesgridand keepsaftermath, thenpresenternamespractice; mechanismproposedforS08specificwords.','owner':'Grid didnotrelatetonarration.'},
 {'agent':'R9 wrongparaphrase substituted “whole business” meaning and made hiddenbusiness seem aphysicalinterior. Moving samegridlaterwouldnotfixclarity.'},
 ['R10master35.086667–44.503333 holdsaftermath.','R10proposedS08 master250.980–296.940; business/jobcontrast260.959–263.230; independentmachine272.880–296.940. Thisisahistoricalproposal, not a universalcurrentplacement.'],
 ['Keep pronoun/referent meanings attachedtolockedscript.','Do not replace later relationships/concentration/records categories with pricing/work/customers.','No omittedepisodepassages silentlybridgedbyconcatenation.'],
 ['Abstractreferentcouldmean multipleobjects/businesses/actors.','A phrasebridgesfromexampletoopportunity ormechanismtoeconomics.'],
 ['Literalreferentisalreadyclear and extra analysiswould addnothing.','Anoldhistoricalplacementproposalcontradicts laterapprovedscenecontext.'],[r(10,'BRIEF.md',6,10),r(10,'STORYBOARD.md',25,35),r(9,'REVIEW.md',9,11)],(GRID,))
case('early-07','Assign presenter, film, question, identity and title different jobs',
 'Owner found filmintrolong; requested presenterforfirstsentence,filmcoverage,questioncard,stare/model,presenterreturn,andsting/title. Then askedlogoholdthroughverbs.',
 'Presenter establishesvoice/opportunity; filmgroundspeople; questionmakestestunmissable; modeladdsoperation; identityholdsbrandpromise; titlenamessubject.',
 {'structure':'Use medium-specificjobs, not a fixed X-second alternation. R11→R12 removesidentity-avatarinterruption soidentitycanown the fullspoken showpromise.','performance':'Selected404lookwithoriginalnarration; Sync3corrects originalperformanceaudio mismatch.'},
 ['Film-onlylead','Presenterfirstthenmotivatedfilmcut','Questionasspokenfilmonly','Exactfullframequestioninterruption','Avatarreadingbrandpromise','Logoholdthroughpromiseandtitlethenselectedavatar'],
 {'owner':'ExplicitR11structureandR12logodurationrequest.','agent':'Avoidcarriercompetition; followinstitutionalidentitywithspecificsubjectthenpracticalexplanation.'},
 {'owner':'Filmgen too longtokeepattention; logo shouldpersistthroughBUILDOWNOPERATE.','agent':'A selectedavatarlookisnotavailableexactwordfootage; neverreusestalevisiblespeechfornewVO.'},
 ['R11avatar0–4.041667thenfilm; sourcecontinuousowner7.708333andbuyer11.25reframes.','Question17.75–21; stare27.916667–30.208333; model30.208333–35.083333; room35.083333–40.083333; avatar40.083333–44.5.','R12logo44.5–56.041667,title56.041667–59.5; R13silencetrimshiftstitleby3seconds.','Source/recordoffsetmustbeexplicitafteredit.'],
 ['Preserveoriginalnarrationlanguageandselectedappearance.','Do not infergeneralauthorizationtogeneratefromidentityeditapproval.','Modechangesneedviewer-readablepurpose.'],
 ['Longmixed-media episodebenefitsfromdifferentcarriersforhumanstakes,logic,proofandpromise.','Presenterpresenceaddsauthorshiporexplanation.'],
 ['Formatdoesnotneedpresenterorcharacters.','Cutwouldcompete withcriticalsingleperformance.','No exact-word synchronizedpresentersourceisavailable; do nothideassetgapwithwrongmouths.'],[r(11,'BRIEF.md',7,15),r(11,'STORYBOARD.md',7,22),r(12,'BRIEF.md',7,15),r(12,'REVIEW.md',17,23)],(OPEN,LOGO))
case('early-08','A hypothetical interruption needs persistent objects and a readable intervention',
 'R13 replaces equationwith workerhandoff; owner absentstate removesonlyowner,leavingjob/chair/workerunchanged.',
 'Make unresolved owner-dependentjudgment inspectable throughsamejobandcounterfactualcondition.',
 {'motion':'One finiteforearm/sheetofferthenhardstatechange,thenheldconsequence; no animatedlinetracing,grid,wobbleorambientmotion.','drawnform':'Roughworkshopfigures/bench/job sheet; nofakecustomerfacts.'},
 ['Animateequationterms','Fadeentirebusiness','Destroyjob/customerleaves','Keepjobpersistentandremoveonlydecisionmaker'],
 {'historical':'R13ownerfeedbackmuchbetterandintroacceptancefavoredconcretehandoff.','agent':'Preservingobjectsletsviewerattributechangetoabsence,notaredrawnscene.','critical_check':'Acceptance at thismomentdoes notestablish thescene’s causalcontrastisstrongenough forfinalepisode; root shouldintegratelaterfailed-baselinefinding.'},
 {'agent':'Collapsedbusiness orlostcustomer would invent outcomes. Morelineanimationwouldnotaddcausalinformation.'},
 ['Graphicslot30.208333–35.083333.','Offerlocal.375–1.125 (0.75seconds,12°→0°rotationaroundelbow).','Ownerabsenceswitchlocal2.125/master32.333on “not”; heldthroughremainingline/silence.'],
 ['Sameworker,hand,job,chair,bench; onlyownerpresencechanges.','Labelasinference/illustration,notverifiedstoryfact.','Entryandexitneedunambiguousstateandrelationship.'],
 ['A singlecounterfactualintervention testsonecausaldependency.','Unchangedobjectshelpviewercomparebefore/after.'],
 ['No workingbaseline is visible; bothstates merelyshowunansweredjob.','Multipleconditionschangeatonceandcausalitycannotbeisolated.','Narrationsupportsonlyunknownoutcome butanimationassertsfailure.'],[r(13,'REVIEW.md',9,12),r(13,'REVIEW.md',19,21),r(13,'STORYBOARD.md',13,17),ref(B+'/reviews/INTRO-DECISION-20260909.md',7,15)],(REDUND,'msg_01a087b5-6d9a-7992-b049-c37670e30ea1',REJECT))
case('early-09','Preserve thinking pauses but shorten empty identity waiting by exact silent samples',
 'Owner questionedpre-“This isTheOperatorEconomy”pause whileapprovingoverallshape. R13removesonlymaster45–48.',
 'Givequestion/stop recognitionroom withoutmakingbrandintroductionfeelstalled.',
 {'timingform':'Protected dramaticpausesinsidefilm; finiteidentityentranceplusabout1secondbeforewordonset.','audioedit':'Two rootclipsagainstuntouchedmaster; retained0–45,48–59.5 at1×gain1. Removalprovenpurezero/no timedwords.'},
 ['Removeallpauses globally','Retimespeechtofit','Leave4secondidentitywait','Removeauthorized3secondsinsideverifiedsilence'],
 {'owner':'Asked ifpre-intropausetoolong,approvedproposedshorterhold.','agent':'144000zero-valuedsamplesremovedwithoutchangingword,voice,gainorspeed; downstreampicturesearliershift3seconds.'},
 {'agent':'Earlierthinkingpausescarryaction/consequence and shouldnotbecutbyblanketpaceoptimization.'},
 ['Master45–48omitted; reviewtime equalsmastertime−3for tail.','Logoentry44.5; “This”45.52review;1.02secbreatingroom.','Titlemaster56.04roundsto review53.041667framegrid.'],
 ['Lockexactmasterhash andwordtimings; storepiecewise mapping.','Updatealltailcues/captions,notjustaudioclip.','Verifyzero-valuedsplice neighborhoodsandnotimedwordoverlap.'],
 ['Narrativejobofasilenceisunderstoodandownerpermitsedit; unusedgapcanbesafelyisolated.'],
 ['Silenceisprotectingreaction,readtimeorsuspense.','Silenceboundaryincludesbreathconsonanttailorword.','TimingchangeswoulddetachapprovedgraphicsfromVOwithoutremap.'],[r(13,'BRIEF.md',9,13),r(13,'REVIEW.md',11,21),r(13,'index.html',30,34),ref(B+'/reviews/INTRO-DECISION-20260909.md',19,21)],(REDUND,'msg_01a087a5-c0f2-7d43-8a5f-23176e27a24f'))
case('early-10','Bridging labels still need an information gain',
 'R14tried25years/Profitableacrossavatar→film. Itwasmechanicallycleanandownerrejectedbecauseitaddednothing.',
 'Engagevieweronlyiftextprovidesusefulorientation,proof,contrastorrememberablethesis.',
 {'tested':'Smallfixedlowerlefttypelabels;shortopacityreveal;carriedacrosshardcut;clearbeforecloseup.','selected':'CleanR13longformintro; purposefulquestion/model/identity/title retained.'},
 ['Fixededitoriallabelsacrossmediumcut','Kineticwordcaptions','Cleanfilmandpresenter','Purposefuldiagrams/evidencelabelsonlywhenneeded'],
 {'owner':'RemoveR14becauseitdoesnotadd;maybeusethatstyleinshorts/clips.','agent':'ReturnexactR13ratherthanrebuildingandaccidentallydisturbingacceptedcut.'},
 {'owner':'25years/Profitablemerelyrestatesaudiblemessage.','agent':'Mechanicallegibility/contrast/transitioncontinuitydidnotproveaudiencebenefit.'},
 ['25years appears2.5;heldover4.041667picturecut.','Profitable joins6.375;bothclear7.666667,oneframebeforeownercloseup7.708333.','Rejectionmeansopening-bridgehostmustnotmount,notallgraphicsshoulddisappear.'],
 ['R13pictureselections,crops,audio,illustration,question,logo/title unchanged.','Maybe-shortformlanguageisnotapprovaltoapplyoverlaysglobally.'],
 ['Textaddscomparison,source,scope,orientationthatpicture/voicecannotcarryeconomically.','Short-formexperimentseparatelyrequiresitsownaudiencejob.'],
 ['Onlyrationale ismoreengaging/produced.','Labelrepeatsfactviewerjustheardwithoutnewrelationship.','Itcompeteswithfaceoranticipatoryreaction.'],[r(14,'BRIEF.md',7,13),r(14,'STORYBOARD.md',5,13),ref(B+'/reviews/INTRO-DECISION-20260909.md',3,21)],(OVER,REJECT))
# Normalize incidental word concatenations in hand-authored data where they materially impair readability.
# Preserve paths, identifiers, and exact historical quotes unchanged.
history={'schema':'ep007-decision-history-review-v1','scope':'Base revision C plus R3–R14 only','review_method':'Read all52 issued input files, recomputed hashes, inspected source HTML timing declarations. No fresh live/render/perceptualQA, paidcalls, sourceeditsorcanonicalgates. Historical reviews quoted as historical findings.','mapping_policy':'Prefer explicit version-bound brief/review. Feedback lacking version/URL is linked by adjacent chronology and matching described change and is not independent proof of an exact visual version.','versions':versions,'cases':cases,'known_gaps':['No separately named R1/R2 folder is reconstructed by this work order; base Revision C is the only root included.','Exact earlier illustration remembered by owner beforeR9 remains unidentified perR9review.','R6 has no REVIEW.md amongassignedinputs; source/brief/storyboard and ownerfeedback supply bounded account.','Detailed provider comparisons outside these issued files are summarized only where versionreviews explicitlyrecord them.','LaterR15–R29 decisions supersede parts of earlycreativeacceptance; merge chronology before marking anyrulecurrentlylocked.']}
(OUT/'history.json').write_text(json.dumps(history,indent=2,ensure_ascii=False)+'\n')
# Human report uses concise portable reading and exact locators into machine packet.
lines=['# EP007 early decision history: base C and R3–R14','',
'Read-only historical packet. All 52 work-order input hashes match. Every listed brief/review/storyboard was read; root HTML cue declarations were inspected. This report records past owner feedback and past agent findings, not new creative approval. No media generation, source edit, runtime rebuild, or canonical state change occurred.','',
'## What the sequence teaches','',
'The revisions did not move simply from rough to polished. They repeatedly changed the narrative job: a decorative or premature mechanism was simplified into an equation, which then lost the useful illustration; an empty chair still failed to explain the situation; character context and rapport made the film legible; purposeful coverage and a distinct explanatory insert helped; generic opening labels were removed even after technical checks passed. A reusable decision agent must preserve that chain and its exceptions, rather than extracting “use rough sketches,” “cut more,” or “always open with people.”','',
'## Version inventory','', '| Version | Change and cue boundary | Reason and historical disposition |','|---|---|---|']
for v in versions:
 lines.append('| '+v['version']+' | '+v['change'].replace('|','/')+' | '+v['historical_disposition'].replace('|','/')+' |')
lines+=['','## Conditional cases','']
for c in cases:
 lines+=['### '+c['case_id']+' — '+c['title'],'',c['context'],'','**Narrative job:** '+c['narrative_job'],'','**Reuse when:** '+'; '.join(c['reuse_when']),'','**Do not apply when:** '+'; '.join(c['do_not_apply_when']),'','**Cue / continuity:** '+'; '.join(c['cue_constraints']+c['continuity_constraints']),'','**Source references:** '+ '; '.join(f"`{e['path']}:{e['lines'][0]}–{e['lines'][1]}` (SHA-256 `{e['sha256']}`)" for e in c['evidence']),'','**Owner message IDs:** '+', '.join(x['message_id'] for x in c['owner_feedback']), '']
lines+=['## Attribution and remaining limits','',
'- `history.json` preserves owner quotes, message IDs, source session line numbers, extraction line ranges and full current SHA-256 hashes. Rationale fields distinguish owner requests, assistant intent, and historical agent findings.',
'- Exact R13 intro acceptance is bound by INTRO-DECISION-20260909.md to root hash `8e814b137d6ff1696050834e216bfdf880a0c22f75674040325f3a6876944da5`; R14 overlays were explicitly rejected. This early disposition must be reconciled with later revisions before declaring today’s selected cut.',
'- Some owner messages have no version label. Matching sequence and described change support the mapping; the quoted message alone does not independently identify the preview artifact.',
'- R10 corrected an assistant semantic error: “business hiding inside it” names the sale-readiness opportunity, not her existing business inside her. The S08 placement was a historical proposal, not an eternally fixed rule.',
'- Film was narrated synthetic dramatization after R8. Mouth mismatch is a different review problem from synchronized presenter delivery. Numerical audio correlation cannot establish naturalness or every phoneme.',
'- No fresh full-speed audiovisual review was performed for this history task. Earlier QA statements remain attributed to their dated source reports.',
'- The source work order covers base C and R3–R14; it does not identify separate R1/R2 artifacts. R6 lacks a REVIEW.md in assigned inputs. The earlier illustration remembered before R9 remains unknown.',
'- Memory quick pass was used only to orient the source audit; current source files support the packet. If parent cites that memory use in its user response, relevant lines are MEMORY.md:265–266; useful rollout 01a078b6-acf7-76a2-ab00-4c2cff805684.',
'']
(OUT/'report.md').write_text('\n'.join(lines))
manifest={'$schema':'../../../../../schemas/agent-deliverable.schema.json','schema_version':'1.0.0','workflow_version':'blueprint-cinema-1.0','work_order_id':w['work_order_id'],'episode_folder':w['episode_folder'],'input_hashes_used':[{'path':i['path'],'sha256':sha(i['path'])} for i in w['inputs']], 'files_produced':[str((OUT/p).relative_to(ROOT)) for p in ['history.json','report.md','build-packet.py','deliverable.json']], 'checks':[{'command':'Recompute SHA-256 for all 52 issued source inputs and compare with work order','outcome':'pass'},{'command':'Read every issued brief/review/storyboard and inspect HTML timing declarations; verify source-reference line ranges and feedback IDs','outcome':'pass'},{'command':'python3 build-packet.py && local JSON/schema/source reference validation','outcome':'pass'},{'command':'Fresh full-speed audiovisual or final render review','outcome':'not_run'}], 'sources_and_provenance':[F,B+'/reviews/INTRO-DECISION-20260909.md','Issued52files are historical source artifacts; no generatedmedia wasaccessedoraltered.'],'assumptions':['Version mapping for unlabeled feedback uses adjacent chronology and uniquely matching described changes; confidence is bounded.','Historical acceptance is not present-day approval after later revisions.'],'unresolved_questions':history['known_gaps'], 'external_writes':False,'paid_services':False,'synthetic_generation':False,'approval_claimed':False,'production_state_changed':False,'status':'complete'}
(OUT/'deliverable.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Wrote',len(versions),'versions and',len(cases),'cases')
