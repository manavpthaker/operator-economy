"""Author the bounded EP008 act-one proposal; never alters production state or audio."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path('/Users/brownmanbrain/GitHub/operator-economy')
OUT = Path(__file__).parent
PLANNING = ROOT / 'blueprint-cinema/experiments/EP008-FULL-BUILD-001/inputs/PLANNING-INPUTS.json'
WORDS = ROOT / 'operator-blueprint-v2/episodes/EP008-ai-implementation-service/02-narration-production/word-transcript.json'
WORK_ORDER = ROOT / 'blueprint-cinema/episodes/EP008-ai-implementation-service/agents/work-orders/EP008-ACT1-DIRECTION.json'
word_list = json.loads(WORDS.read_text())['words']
planning = json.loads(PLANNING.read_text())
shots = []

def add(scene, first, last, medium, title, action, change, continuity, false_inference,
        claims, simpler, asset, hold, cue_words=None):
    count = 1 + sum(s['scene_id'] == scene for s in shots)
    shot = dict(shot_id=f'{scene}-A{count:02}', scene_id=scene, medium=medium, title=title,
                visible_action=action, viewer_change=change, continuity=continuity,
                false_inference=false_inference, claim_ids=claims,
                strongest_simpler_alternative=simpler, asset_need=asset, final_hold=hold,
                picture_audio_mode={'presenter':'presenter_address','film':'narrated_observation',
                                    'model':'silent_graphic','evidence':'silent_graphic',
                                    'identity':'silent_graphic'}[medium])
    if first is None:
        shot.update(first_word_id=None,last_word_id=None,speech_in=None,speech_out=None,
                    text='', boundary_proposal='Preserve the complete existing S00/S02 silence. The planning S01 entry overlaps W000159 by 0.020 seconds; root must resolve on the encoded frame/audio clock without cutting speech.')
    else:
        selected = word_list[first:last+1]
        shot.update(first_word_id=selected[0]['w_id'],last_word_id=selected[-1]['w_id'],
                    speech_in=selected[0]['start'],speech_out=selected[-1]['end'],
                    speech_duration_seconds=round(selected[-1]['end']-selected[0]['start'],6),
                    first_token=selected[0]['token'],last_token=selected[-1]['token'],
                    text=' '.join(w['token'] for w in selected),
                    boundary_proposal='Hard cut in the natural gap preceding the first word; root derives contiguous frames and verifies waveform. Original master audio is continuous.')
    if medium in ('presenter','film'):
        duration=shot['speech_duration_seconds']
        shot['generation_planning']={
            'status':'unsubmitted proposed ticket; look/footage selection and spend unresolved',
            'proposed_native_seconds':min(12,round(duration+0.65,3)),
            'maximum_native_seconds':12,
            'performance':'One primary action, fixed camera, simple performance; no body retiming. Pilot and audiovisual review before bulk.',
            'reference_scope':'Episode-specific appearance and geography only; no EP007 or EP009 footage reuse.',
            'audio':'Presenter uses exact listed EP008 audio; film has no visible speech and no fabricated dialogue.'}
    if cue_words:
        shot['action_cues']=[{'word_id':word_list[i]['w_id'],'token':word_list[i]['token'],
                               'master_seconds':word_list[i]['start'],'action':a} for i,a in cue_words]
    shots.append(shot)

add('S00',0,20,'presenter','Direct invitation into eleven oclock',
    'A still, near-lens opening. One small open-hand invitation on the customer question; hands settle before the cut.',
    'The viewer enters a specific support situation through the narrator, without mistaking it for a documented client.',
    'Proposed EP008 look: pale ecru shirt, modest ecommerce operations workspace; owner must select likeness/look. Preserve complete hands in the wide source. Picture holds to approximately 6.4s before film.',
    'The presenter has personally served this store; this is an actual customer case.',[],
    'An illustrative customer close-up would locate the question, but loses the requested direct presenter opening.',
    'PRES-A01: one exact opening take; EP008 look-selection stills required first.',
    'Let the last word and face settle through the existing gap; protect the whole first sentence.')
add('S00',21,51,'film','The bought tool at the working desk',
    'In one oblique desk view, the founder wakes the laptop and settles to it; no readable interface. The unchanged parcel and empty adjacent support chair establish a modest operating business.',
    'Buying and switching on the tool is an ordinary reasonable act, not evidence that useful setup is complete.',
    'Establish SHOP-01, FOUNDER-01, DESK-01, laptop left, unused support chair right, parcel behind; warm practical night light. Preserve this geography for the late callback.',
    'A fabricated product screen is a real Gorgias capture; the founder is careless or defeated.',[],
    'A bought/switched-on label could explain the event, but would miss the ordinary human reason for the purchase.',
    'FILM-A01: one 8.45s proposed night-desk take, no visible speech, no legible screen.',
    'Keep the founder engaged with the actual work; no frown or reaction inserted after the narration.')
add('S00',52,71,'model','A handoff with no receiving person',
    'The same order ticket arrives at the rented helpdesk boundary. The agent routes it once to a human handoff slot; the slot has no person at eleven. The ticket stops there, unresolved.',
    'The failure is an unstaffed destination after a handoff, not slow AI or a missing software purchase.',
    'Introduce TICKET-ORDER-01, HELPDESK-01, HANDOFF-01. Keep the store and agent intact; use a time note only when eleven/nine matters.',
    'The vendor is down; all tickets fail; the AI has answered the question.',[],
    'Holding the empty chair is simpler but cannot expose how the ticket reached that absence.',
    'MODEL-A01: authored ticket route, store outline, unstaffed handoff; no platform UI.',
    'Hold the unanswered ticket at the empty receiving position through there will be one at nine.',
    [(52,'Ticket becomes active'),(58,'Single handoff begins'),(63,'Reveal that receiving position is unstaffed')])
add('S00',72,114,'model','Two costs and one small meter',
    'Keep the unresolved ticket at the handoff. Add two occupied human work positions as the narration names them. At the vendor edge, a separate resolved-event tally is visibly short but unnumbered; payment follows only that event branch.',
    'Human work remains while a second payment condition exists; the illustration does not pretend to quantify this imagined store.',
    'Reuse HELPDESK-01 and HANDOFF-01. Introduce METER-01 as a billing event counter, not a green correctness indicator; no fake invoice.',
    'Specific invented invoice amount, actual resolution rate, or two staff as a researched denominator. The two people belong only to this illustrative store.', ['C006','C007'],
    'A bill close-up cannot be genuine for the fictional store and would introduce fake evidence; the bounded model makes the two obligations explicit.',
    'MODEL-A02: two human task positions, separate vendor meter, no quantities beyond narrated illustrative headcount.',
    'Settle with the human queue still present and the vendor meter separate; never clear the queue as a cosmetic exit.')
add('S00',115,159,'model','The job has no owner yet',
    'Within the same store-to-vendor arrangement, separate the switch-on point from the functioning answer route. Leave one human work position between them unassigned. Do not insert the proposed implementer until later.',
    'The proposed opportunity is responsibility between purchase and operation; who leaves it there remains the open question.',
    'Carry TICKET-ORDER-01 and HANDOFF-01. Introduce JOB-GAP-01 as the unassigned task, not a monetary opportunity badge.',
    'The gap is observed demand, the wizard is proven deficient, or the job already sells at a known fee.', ['C023','C022'],
    'Presenter could state the entire proposition; retain the model because the empty responsibility will return when the company is proposed in S11.',
    'MODEL-A03: two operational states and one unfilled work position; no engine/car metaphor.',
    'Leave the job unassigned through who left the job undone; hard cut to identity only after all speech.')
add('S01',None,None,'identity','Institutional identity in the existing pause',
    'Present the approved institutional wordmark with a single finite reveal and stable reading hold; retain Build. Own. Operate. only if the current identity binding requires it.',
    'The viewer recognizes the editorial desk before the show promise.',
    'Boundary Ledger institutional field and typography; use current semantic binding, not EP007 R74 legacy navy/gold/grid.',
    'The sting is an opportunity verdict, verification stamp, or approval of the practice.',[],
    'A static wordmark may be enough; choose it if motion adds no orientation.',
    'IDENTITY-A01: current wordmark/vector/fonts; local dependencies. No new theme music assumed.',
    'Preserve the full existing silent interval. A shorter sting is only an optional separately measured proposal; no audio shortening in this packet.')
add('S02',160,182,'presenter','The show promise',
    'Return to the same ecru-shirt presenter, near-lens delivery, one inclusive hand movement across the whole build/own/operate phrase rather than three gestures.',
    'The program promises a careful business examination, not a guaranteed livelihood.',
    'Same EP008 look as opening; a slightly different editorial crop may follow thought but no generated camera motion.',
    'Successful operation or a particular income is promised.',[],
    'The wordmark alone could carry the line, but direct address gives the editorial promise an accountable speaker.',
    'PRES-A02: exact 52.580–58.760s speech; new source, not the EP007 audition.',
    'Stay engaged through one; cut only after the phrase settles.')
add('S02',183,241,'model','The practice and the questions it must answer',
    'The unassigned job gains a provisional one-person position. Show two different routes: answer with a rule, or hand off with a boundary. The job then sits between an unfilled buyer-value measure, operator-cost measure, and a vendor-owned tool edge that can move.',
    'The service is setup plus limits, and value/cost/platform risk are questions this episode will test.',
    'Reuse JOB-GAP-01, TICKET-ORDER-01, HELPDESK-01. PROPOSED remains visible on the practice; no results or price yet.',
    'The solo category, customer willingness to pay, or vendor replacement event is already established.', ['C004','C023','C022'],
    'A title plus three nouns would be shorter but would not connect the proposed operator to the two permission routes.',
    'MODEL-A04: provisional practice figure and two rule-controlled routes; unfilled measures are questions, not zero values.',
    'Finish on the dependency at the vendor-owned edge, without animating actual deletion.')

add('S03',242,274,'film','A small shop does ordinary work',
    'Daytime in SHOP-01: a support worker checks one parcel against the oblique laptop and returns to the same task. One action, no montage of frantic staff.',
    'The underlying business and support work function before the critique begins.',
    'Same desk and parcel position; daytime is an explanatory ordinary-work passage, not a claimed morning following the opening.',
    'An actual researched brand, a measured support workload, or a poorly run shop.',[],
    'An abstract storefront could orient the viewer but omits the ordinary work the service must fit.',
    'FILM-A02: one 11.12s proposed task-focus take; screen and labels unreadable.',
    'Hold at task completion long enough to see attention return to support.')
add('S03',275,307,'model','Several channels, one queue',
    'An order-status ticket and a return ticket arrive from differently marked channels into one shared queue at the same store. A human removes one ticket for work while others remain.',
    'The helpdesk is the common working queue across email/chat/social; it is not a new separate business.',
    'TICKET-ORDER-01 persists. Introduce TICKET-RETURN-01; channel labels are authored conceptual labels, not product logos or fake screenshots.',
    'An exact channel mix, throughput, queue size or agent productivity.',[],
    'Holding the support worker would preserve humanity but conceal the multi-channel consolidation described here.',
    'MODEL-A05: one small queue with bounded channel inputs and one active human action.',
    'Settle the single queue and keep its working human; do not empty it on narration cadence.')
add('S03',308,341,'evidence','The helpdesk price ladder has a source',
    'Show source-attributed vendor identities, then the specific Gorgias Shopify listing price endpoints in one stable receipt; keep the access date and plan population visible.',
    'These are published tool plan prices at a research cutoff, separate from a service fee or Gorgias AI resolution price.',
    'Use evidence surface distinct from Working Model; source attribution must not let the shared Gorgias/Zendesk spoken introduction attach Gorgias plan figures to both vendors.',
    'Both vendors have identical plan prices; the price includes per-resolution AI usage.', ['C005'],
    'A clean pricing ladder without its receipt is easier to read but removes the attribution needed to limit the shared-vendor wording.',
    'EVID-A01: frozen Gorgias Shopify listing or authored receipt with exact source, date, locator and C005; source capture still required.',
    'Hold source attribution through as of when I checked; no scrolling at the final caveat.')
add('S03',342,439,'model','The agent route gains a billing condition',
    'Inside the established queue, insert an agent between ticket and human. With a known answer it completes one bounded route; without one it hands off. On the first change, retain that complete route and connect its completion event to METER-01. A handoff produces no billing event.',
    'The agent is embedded in the existing queue, and the vendor payment depends on an outcome event rather than the mere presence of the agent.',
    'Same ticket/store/helpdesk. Founder choice is reasonable; meter separate from correctness. Use one staged change at a time with still holds, no conveyor loop.',
    'Every ticket is answerable, the vendor gains no other subscription revenue, or a closed ticket proves a correct answer.', ['C006','C007','C021'],
    'A presenter explanation would be sufficient for purchase empathy but cannot as clearly distinguish the billed branch from handoff.',
    'MODEL-A06: embedded agent, two routes and one event-linked meter; no actual product interface.',
    'Leave the completion-to-payment connection readable through resolutions.',
    [(342,'Add agent to the existing queue'),(399,'Hold the first arrangement before the two changes'),(402,'Activate the event-to-billing connection')])
add('S03',440,489,'evidence','Two adoption measures are not one measure',
    'Present the Census survey receipt first and the Chase transaction study second, each with its own population and measurement label. Keep the conceptual early-adopter conclusion separate from the numerical receipts.',
    'The audience sees sparse adoption supported by two different measures, neither of which measures demand for setup services.',
    'Stable source typography; no merged sample or averaged bar. Retain fewer-than-one-in-five wording instead of inventing a single blended statistic.',
    'Measured setup spending, retail support adoption specifically, or a single pooled survey.', ['C001','C002'],
    'One giant adoption number hides the measurement difference; two compact receipts preserve it.',
    'EVID-A02: Census BTOS and Chase Institute frozen sources or exact receipts; each date/population/claim ID retained.',
    'Leave both measurement labels legible while the narration returns to early users.')
add('S03',490,517,'film','The same ticket remains work for somebody',
    'The founder passes the unresolved physical task to the seated support worker; the worker takes it and begins inspecting the parcel. Laptop content stays out of focus. No acted complaint or phone exchange.',
    'The abstract handoff returns to work borne by people; the human queue has not disappeared.',
    'SHOP-01 daylight, same parcel, founder left and worker right. One unbroken transfer across the same screen direction.',
    'The worker or founder is incompetent, or the shot is an actual customer failure.',[],
    'A three-face montage would repeat the stakeholder list; one task transfer shows the common burden.',
    'FILM-A03: one 10.80s proposed handoff take, no speech.',
    'Protect the worker receiving and beginning the task; no reaction insert.')
add('S04',518,563,'model','Who owns the enabling work',
    'Hold the vendor meter, store and unassigned setup position in one frame. The completed-event payment path remains clear; the setup input stops at the empty responsibility position. Reveal the short question Who does the setup? only after the spoken question begins.',
    'The incentive and the allocation of work can diverge; the missing party becomes the episode question.',
    'Reuse JOB-GAP-01 and METER-01; no explanatory handbook solution yet, no blame coloring.',
    'The vendor refuses small stores, all stores fail, or lack of support is established causation.', ['C006','C007','C023'],
    'A plain question card is viable; retain the model only because it makes the payment/work mismatch inspectable without answering prematurely.',
    'MODEL-A07: restrained question in persistent world; no new icons.',
    'Keep the unassigned position unresolved through the question and its following silence.')

add('S05',564,575,'presenter','Mark this as the narrators read',
    'Direct, quiet near-lens delivery; slight open palm on my read, then rest.',
    'What follows is an editorial interpretation that still has to earn support.',
    'Same selected EP008 look and continuous original audio; no verdict badge.',
    'The interpretation is proven market evidence.',[],
    'An on-screen caveat could mark status, but direct address makes the narrator own the interpretation.',
    'PRES-A03: exact 183.740–186.660s speech, simple single thought.',
    'Preserve the natural gap before the metaphor.')
add('S05',576,646,'model','The same enabling job at two customer sizes',
    'Keep the vendor tool as the same tool, not a literal engine/car. A larger customer receives a person at the setup position; the smaller store receives a wizard outline, with the task of converting policy to an operating route still assigned to its side. Show the work position rather than claiming the wizard cannot perform it.',
    'The metaphor describes who does setup and how value is billed; observed sold work and proposed solo work remain distinct.',
    'Same vendor boundary and JOB-GAP-01. The larger-customer person and smaller-store wizard are evidence-linked, not scaled revenue graphics.',
    'The wizard has been tested and found deficient; all stores below a threshold receive no help; the solo buyer has paid.', ['C009','C010','C012','C023'],
    'A literal engine and odometer would follow the words but abandon the persistent helpdesk world and conceal the actual job.',
    'MODEL-A08: two supported setup paths, proposed small-store work position; evidence receipt reference retained for later S10 proof.',
    'Hold the small-store responsibility as a proposed business position, not a completed paid sale.')
add('S05',647,674,'presenter','The vendor can close it',
    'Return to direct address; a small closing movement of one hand on close, then stillness through the warning.',
    'Platform dependence is part of the proposal, not a footnote withheld until the end.',
    'EP008 presenter look; no falling graphs or imaginary release announcement.',
    'A replacement release is announced or inevitable.', ['C022'],
    'Animating the vendor swallowing the practice would imply an observed event; a conditional spoken judgment is more precise.',
    'PRES-A04: exact 218.560–226.920s speech.',
    'Hold engagement through we will get there; avoid a reassuring smile that neutralizes the risk.')

add('S06',675,765,'evidence','What the vendor actually bills',
    'Show the Zendesk receipt first: announcement date and $1.50 tied to its named automated-resolution definition. Then display the 72-hour no-return condition as an evidence-backed timing annotation. Transition within the evidence surface to Gorgias mechanism-only receipt; leave its per-ticket figure explicitly unstated.',
    'A billed resolution is a vendor-defined event; one vendors known price must not transfer to the other.',
    'Evidence surface with source/date/locator/C007 and C006. The timing annotation explains source language, not an invented measured customer journey.',
    'Gorgias also charges $1.50; Zendesk closure validates answer correctness; this is the fictional stores actual bill.', ['C007','C006','C021'],
    'A fictional invoice would be visually familiar but falsely evidentiary; an attributed receipt answers the billing question directly.',
    'EVID-A03: Zendesk pricing/definition/announcement and Gorgias mechanism sources, frozen at approved cutoff; no fabricated dashboard.',
    'Hold the Gorgias attribution and unquoted figure through the complete omission statement.')
add('S06',766,782,'presenter','The fair case for outcome pricing',
    'Deliver the good-deal concession without irony; one slight nod on no AI charge, then settle.',
    'The viewer can accept the vendors rational value proposition before inspecting its limits.',
    'Same presenter; preserve conditional if nothing resolves and for the AI in the complete line.',
    'The store has no helpdesk subscription bill at all.', ['C006','C007'],
    'A zero-dollar graphic could erase the AI-only qualifier; presenter preserves the exact condition.',
    'PRES-A05: exact 262.140–268.180s speech.',
    'Do not cut before for the AI; the qualifier is the point.')
add('S06',783,821,'model','Answer and permission are separate inputs',
    'Return to the ticket route and meter. The answer path has two distinct prerequisite slots, store knowledge and permitted action. Leave both unresolved, and show the completion gate waiting for them rather than depicting an arbitrary stalled token.',
    'Useful resolution needs both information and authority; the missing work is specific.',
    'METER-01 remains downstream. Introduce HANDBOOK-01 and AUTHORIZATION-01 as empty model inputs; no correctness checkmark.',
    'Buying the tool grants money-moving permission or the agent necessarily lacks all knowledge.', ['C004','C006','C007','C021'],
    'Two labels beside a presenter would name prerequisites but fail to show why either one changes the permitted route.',
    'MODEL-A09: two prerequisite gates, same ticket and completion event.',
    'Hold both unresolved inputs while the narrator asks who makes sure; answer only in S07.')

add('S07',822,904,'evidence','The setup job in the vendors own guide',
    'Read the actual guide in a stable evidence crop. Focus its prerequisite, then skills, handover, playground and first-week review in narration order. Only the current cited passage receives emphasis; prior material stays visible enough to preserve source context.',
    'The job is documented by the vendor, with an enabling knowledge source and explicit testing/review responsibility.',
    'Use the real source or an exact attributed receipt; no synthetic settings UI, no implication the wizard skips the list.',
    'These are measured shortcomings of the wizard, or ten reviewed tickets prove quality for every ticket.', ['C004'],
    'A five-item slide repeats nouns; an accountable source passage establishes that the vendor itself names the work.',
    'EVID-A04: Gorgias Set up and go live with AI Agent, exact locators and date; capture required before final build.',
    'Leave the ten-ticket first-week requirement and source attribution still through the sentence end.')
add('S07',905,936,'film','A person decides what the policy means',
    'At DESK-01, an implementer compares a plain policy page with a task note, then writes one decision while the founder watches the line. The writing itself remains unreadable; no mime of every noun.',
    'Policy clarification and review take human attention; this is labor someone must own.',
    'Establish IMPLEMENTER-01 facing FOUNDER-01 across the same desk; handbook remains the same plain physical folder, exact readable rules belong in authored graphics.',
    'An actual paid client engagement, a completed week of review in eleven seconds, or a signed authorization.', ['C004'],
    'A diagram could summarize the work but miss the situated judgment of turning a founders habit into a rule.',
    'FILM-A04: one 11.73s proposed compare-and-record take, no visible speech, no readable generated writing.',
    'Hold the written decision and mutual attention without a celebratory handshake.')
add('S07',937,1004,'model','The temp has neither handbook nor escalation rule',
    'Transform the existing agent position into an explicitly analogical temp role, leaving shop geometry intact. An order arrives at a blank handbook position; the refund path has no human-authority rule. Demonstrate one clearly hypothetical wrong-routing attempt, then show that the separate vendor meter could still count the closed event.',
    'Speed and closure do not supply policy knowledge, authority or correctness.',
    'Keep HANDBOOK-01, AUTHORIZATION-01 and METER-01 distinct. Label the analogy as a Working Model; return to the ordinary agent representation before leaving.',
    'An actual agent error, a measured error rate, or all vendor-metered resolutions being wrong.', ['C004','C021'],
    'A photographed temp would create a second human world and imply an actual staffing relationship; the model keeps this an analogy.',
    'MODEL-A10: temp-role substitution, missing handbook and escalation input, one hypothetical unresolved/wrong route; no money amount.',
    'Keep the meter and correctness question visibly separate through the billing line; no success badge.')
add('S07',1005,1021,'presenter','Name the job without overselling it',
    'Quiet direct address; hands rest while the narrator lands the handbook as owned responsibility.',
    'The product opportunity is the policy work, not another AI tool.',
    'Same EP008 look; hold original pacing and avoid adding a grand reveal.',
    'Every small team neglects policy or someone has already agreed to pay.', ['C004','C023'],
    'A big handbook title would restate the metaphor; presenter can own the judgment simply.',
    'PRES-A06: exact 356.570–362.700s speech.',
    'Keep full final word and short rest before scale changes in S08.')

add('S08',1022,1118,'evidence','Enterprise findings stay in their population',
    'Establish a plainly labeled large-company evidence field. Present MIT NANDA via the retained Fortune report; show the no-measurable-P-and-L result separately from the purchased-versus-built success comparison. Keep metric, cohort and source limitations attached to each.',
    'Integration work matters in the cited enterprise research; the two numbers answer different questions and are not a small-store result.',
    'Do not overlay the 95 percent on SHOP-01 or draw an arrow from enterprise results into its queue. Primary PDF was unavailable in the approved research; secondary status stays visible.',
    '95 percent of small-store agents fail, a common denominator between the two metrics, or the research proves demand for this service.', ['C003'],
    'One dramatic giant percentage would land quickly but erase population and metric distinctions; source-led staged evidence is required.',
    'EVID-A05: retained Fortune/Yahoo source receipt with MIT NANDA attribution, enterprise label, date and C003. No fabricated primary PDF.',
    'Keep enterprise scope visible through the purchased/internal-build comparison, with no triumphant color coding.')
add('S08',1119,1146,'presenter','Say the transfer is a hypothesis',
    'Direct near-lens delivery, restrained hands; the explicit limitation is given uninterrupted time.',
    'The viewer knows the episode is making a limited inference across company sizes.',
    'Return from evidence to accountable narrator; no supporting small-shop footage suggesting a real result.',
    'The enterprise figure is empirically validated at a two-person brand.', ['C003'],
    'A small disclaimer under the enterprise chart is easier to ignore; full direct address gives the boundary its intended weight.',
    'PRES-A07: exact 397.390–407.220s speech.',
    'Protect hypothesis, not a fact as one complete delivered thought.')
add('S08',1147,1165,'model','Buying does not fill the handbook',
    'Return to the same small-store tool; retain its bought status, then expose the still-unfilled handbook input beside it. Nothing is taken away from the purchase.',
    'Buying can be preferable to building and still leave operating knowledge to supply.',
    'SHOP-01 and HANDBOOK-01 return without enterprise numbers. This is the small-brand hypothesis, not a replay of research results.',
    'The purchase is worthless or the wizard cannot supply the handbook.', ['C003','C004'],
    'Presenter alone is sufficient verbally, but this callback prepares the exact decision cases that will fill the handbook.',
    'MODEL-A11: preserve purchased tool and reveal the missing operating input.',
    'End on the empty policy space that S09 will fill, not on an error symbol.')

add('S09',1166,1248,'model','A written condition changes the permitted route',
    'Open HANDBOOK-01 beside the same queue. First insert an order-status lookup rule: the ticket can access tracking and produce an answer. Replace only the ticket intent with returns; show an inside-window route permitted by policy and an outside-window or angry-customer route to the human. The written condition visibly sets the gate before the ticket moves.',
    'The setup task is choosing distinct action classes; one written rule enables or redirects a specific ticket.',
    'TICKET-ORDER-01 and TICKET-RETURN-01 share the same queue. Keep policy-window values unspecified; no universal days or return entitlement. Do not quantify most of the queue.',
    'Every order-status ticket is safe, every store uses the same return policy, or this is a measured intent distribution.', ['C004','X001','X002'],
    'Three safe/conditional/never columns would name classes but conceal the enabling condition; gates show why the route differs.',
    'MODEL-A12: two sequential case tests in the same world; authored labels and finite route changes.',
    'Hold the outside-policy human route with the condition still visible; no scrolling list of completed tickets.',
    [(1186,'Order-status case becomes active'),(1213,'Return case replaces only ticket intent')])
add('S09',1249,1312,'model','The never list is a permission boundary',
    'Introduce damaged-item refund at the same gate. Leave the money-moving path physically present but inactive. Insert the never-list rule; route the ticket to the founder. Show a distinct unsigned per-action authorization space beyond the boundary and do not sign it.',
    'The agent may be technically capable, while authority deliberately forbids the action until the founder signs for that action.',
    'Introduce TICKET-REFUND-01 and NEVER-LIST-01; preserve HANDBOOK-01 and AUTHORIZATION-01. No green/red moral labels on the person or platform.',
    'The agent cannot move money, one blanket consent permits all actions, or an actual founder has authorized a refund.', ['X003','C020','C021'],
    'A crossed-out refund icon could imply inability; the visible-but-inactive path separates capability from permission.',
    'MODEL-A13: refund route, unfilled authorization and never-list rule; no cash animation or invented amount.',
    'Keep the action stopped and ownership at the founder through the product/configuration distinction.')
add('S09',1313,1385,'evidence','Klarna establishes a trade-off at another scale',
    'Show a dated Klarna source receipt for initial handled share, then the later quality statement and human-recruiting change in sequence. Maintain the explicit scale boundary throughout; do not map the companys metrics onto the small shop.',
    'The source illustrates an automation-quality trade-off, not the demand or expected automation rate of this buyer.',
    'Use the recorded trade-press source and accurate paraphrase; one date/claim at a time. No invented CEO video or unsupported direct quote.',
    'Klarna is a small-store comparable, two thirds is a target, or quality declined solely because a literal never list was absent.', ['C013'],
    'A presenter anecdote would leave the factual claims invisible; the source receipt permits inspection without importing its economics.',
    'EVID-A06: CX Dive May 2025 retained source with C013 and scale limitation.',
    'Keep not evidence about our buyer visible and spoken before returning to the modeled store.')
add('S09',1386,1408,'model','The objective is bounded work, not maximal automation',
    'Return to the same three ticket intents. With no permitted routes, all remain human work; with the money path unrestricted, a refund crosses the boundary. Restore the authored rule-controlled middle condition with the refund still human-owned, not a numerical optimum.',
    'Both under-use and unbounded permission have costs; the product is the deliberate boundary.',
    'Use prior routes only; label this a conceptual comparison. No invented error count, lost customer, optimum rate or financial result.',
    'The episode has measured an ideal automation rate, or a wrong refund always loses a customer.', ['X001','X002','X003','C021'],
    'A seesaw or slider would imply an arbitrary balanced midpoint; replaying permission conditions makes the actual choice concrete.',
    'MODEL-A14: bounded comparison of existing routes; no new explanatory metaphor.',
    'Settle on the never-list boundary, not on more tickets flowing for visual energy.')

add('S10',1409,1486,'evidence','The vendor sells the work',
    'Use the vendors actual onboarding/service source. Focus implementation sessions and named setup service; identify the fifty-days/half-support offer as vendor marketing, then show its separate sixty-day average-launch statement with source context.',
    'The vendor itself sells human setup work; its pitch and its reported average are different statements, neither a measured outcome for this buyer.',
    'Evidence surface only; no vendor presenter dramatization, invented invoice or growth chart.',
    'Fifty-percent automation is achieved, the service has a public price, or sixty days is every customers result.', ['C009'],
    'A generic implementer scene could humanize the work but cannot establish that the vendor actually sells it.',
    'EVID-A07: Gorgias onboarding/professional-services source, pitch label, average-launch locator and C009.',
    'Keep sixty days with its average/vendor context through the dedicated-person conclusion.')
add('S10',1487,1559,'model','Customer-size allocation and two different milestones',
    'Attach the vendors cited three-million annual-revenue boundary to two setup paths: self-serve and dedicated person. Within a separate time strip, show go-live and useful sustained operation as different labeled milestones; keep the forty-eight-hour and sixty-day source statements in their respective quoted contexts, not as comparable stopwatch measurements.',
    'Customer size changes the service offered, and launch statements can coexist because they describe different support routes and milestones.',
    'Same store, wizard and work position from S05. Attribute threshold to the vendors plan guide; no barred door or denied-support sign.',
    'Stores under three million are contractually forbidden all help, the wizard is inadequate, or sixty days and forty-eight hours are one controlled comparison.', ['C012','C009','C010'],
    'One gap timeline would suggest a measured delay; two source-labeled paths preserve the distinction.',
    'MODEL-A15 with EVID-A08 receipt: vendor plan guide/AMD-01; attributed threshold and separate stated launch measures.',
    'Keep the self-serve route intact; do not portray it as broken when the dedicated path is highlighted.')
add('S10',1560,1582,'film','A small account is still real work',
    'At the same desk, the founder completes packing one parcel before returning attention to the support workspace. Calm task focus, no victim or villain performance.',
    'The service-allocation problem is ordinary unit economics; a small business is doing real work with limited resources.',
    'SHOP-01, same founder, parcel and desk; no actual vendor employee represented. Human action is illustration, not proof of the subscription economics.',
    'The vendor is negligent, or the founder is pleading for rescue.', ['C005','C012'],
    'A dismissive vendor character would manufacture motives; ordinary founder work keeps the concession fair.',
    'FILM-A05: one 8.10s proposed parcel-completion take; fixed camera and unreadable labels.',
    'Let the completed parcel stay in frame while the founder redirects attention, without an exaggerated sigh.')
add('S10',1583,1600,'film','The handbook remains on the stores desk',
    'A closer desk view: the founder draws the plain handbook folder toward their side and opens it to inspect, then holds. The folder has no readable invented contents.',
    'Self-service leaves ownership of operating policy with the store, without proving the wizard cannot help.',
    'Same physical HANDBOOK-01, founder hand/wardrobe and desk direction; derive close setup from FILM-A05 geography.',
    'The document is blank because the wizard failed, or the founder has completed implementation.', ['C004','C012'],
    'A model handoff repeats an already understood route; this brief physical callback returns the responsibility to a person.',
    'FILM-A06: one 5.95s proposed folder draw/open action; no screen, no writing or signature.',
    'Hold on active inspection, not a closed folder that could imply shelving the work.')
add('S10',1601,1669,'evidence','Observed sellers, not observed solo economics',
    'Show the certified partner directory/program receipt, then the named Barcelona shops service-tier/retainer receipt. Keep price-on-call where no number is published; return both vendor and agency evidence to a single observed-service conclusion.',
    'The category is sold at vendor and agency layers, while price, solo demand and attainable economics remain unknown.',
    'These are two operating layers, not three: the specialist shop belongs to the agencies. No agency output or automation claim becomes an outcome.',
    'A price band, a successful solo seller, referral volume, partner admission or a guaranteed client stream.', ['C008','C011','C023'],
    'A three-rung market ladder would count the specialist twice and overstate scale evidence; paired receipts are more accurate.',
    'EVID-A09: vendor directory/partner program and custo.tech source receipts with dates, locators and claim IDs.',
    'Keep the observed-service evidence stable through sold by vendor and agencies; do not fill the missing price.')
add('S10',1670,1700,'presenter','Own the missing price and solo evidence',
    'Direct admission with simple steady delivery; no apologetic shrug. Hands rest through the complete absence-of-observation statement.',
    'The viewer does not confuse publicly offered services with verified fees or a demonstrated solo business.',
    'Same EP008 selected look. Exact speech is 11.0 seconds; proposed native take 11.65 seconds including handles remains under twelve.',
    'Nobody anywhere pays for the service; absence in this research proves nonexistence.', ['C023'],
    'A missing-data card can look like zero demand; direct first-person wording preserves the research limit.',
    'PRES-A08: exact 605.740–616.740s speech; preflight duration and pilot recipe before batch.',
    'Protect at a price they would say out loud as part of the limited claim.')
add('S10',1701,1724,'evidence','What the application actually lists',
    'Show the authentic partner-application categories in one cropped source view. Indicate their scope without adding a crossed-out person or rejection stamp.',
    'The program is visibly organized around organizations; solo exclusion or admission remains unverified.',
    'Retain source context and C008. Do not fabricate an application screenshot if a capture is unavailable; use an attributed receipt instead.',
    'A solo operator was refused, or the vendor does not accept individuals.', ['C008'],
    'A giant no-solos symbol would be simpler but unsupported; source categories carry only the evidence actually held.',
    'EVID-A10: authentic application/category source capture or exact attributed receipt.',
    'Leave the listed categories still through it does not list a person; no additional exclusion icon.')
add('S10',1725,1743,'model','Return to the unresolved store',
    'Bring the same small store, self-serve wizard, two support positions and unassigned policy/setup work into one restrained frame. The narrated two-thousand ticket label identifies only this proposed buyer example; do not draw two thousand moving tickets.',
    'The category evidence has not removed the small stores specific setup responsibility; the frame prepares S11 to place the proposed practice.',
    'Reuse SHOP-01, HELPDESK-01, JOB-GAP-01 and HANDBOOK-01; keep the place for the implementer empty until S11.',
    'Two thousand tickets is an observed client, sixty days is its measured delivery time, or the proposed solo service already has a customer.', ['C009','C012','C023'],
    'A summary noun slide loses the spatial relationship established since the opening; the persistent world lets S11 answer the missing-role question.',
    'MODEL-A16: one stateful callback, no new figure or product claim.',
    'Hold the still-unfilled implementer position through the boundary into S11; no independent fade-to-black.')

assert len(shots)==40, len(shots)
assert {s['scene_id'] for s in shots}=={f'S{i:02}' for i in range(11)}
speech=[s for s in shots if s['first_word_id']]
expected=0
for s in speech:
    a=int(s['first_word_id'][1:]); b=int(s['last_word_id'][1:])
    assert a==expected, (s['shot_id'],a,expected)
    assert b>=a
    expected=b+1
    if s['medium'] in ('presenter','film'):
        assert s['speech_duration_seconds']+0.65<=12, s['shot_id']
assert expected==1744
work_order=json.loads(WORK_ORDER.read_text())
assert hashlib.sha256(PLANNING.read_bytes()).hexdigest()==work_order['inputs'][0]['sha256']
inputs=[]
for p in [PLANNING,WORDS,WORK_ORDER,
          ROOT/'blueprint-cinema/experiments/EP008-FULL-BUILD-001/inputs/NARRATION-MAP.md',
          ROOT/'operator-blueprint-v2/episodes/EP008-ai-implementation-service/01-editorial/claims-map.md',
          ROOT/'.agents/skills/oe-video-direction/SKILL.md',
          ROOT/'.agents/skills/oe-video-direction/references/presenter-references.md',
          ROOT/'.agents/skills/oe-film-direction/SKILL.md',
          ROOT/'blueprint-cinema/TOOLCHAIN.md']:
    inputs.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
proposal={
    'record_type':'bounded_episode_direction_proposal','episode':'EP008-ai-implementation-service',
    'work_order_id':'EP008-ACT1-DIRECTION','status':'agent proposal; not owner accepted or canonical',
    'scope':{'scenes':['S00','S01','S02','S03','S04','S05','S06','S07','S08','S09','S10'],
             'first_word_id':'W000000','last_word_id':'W001743','shot_count':40,'original_audio_unchanged':True},
    'input_hashes':inputs,
    'global_direction':{
        'viewer_arc':'A reasonable purchase leaves an operating responsibility; source-backed evidence identifies who owns it today; the proposed solo practice has not yet entered the empty position.',
        'world':['SHOP-01','FOUNDER-01','IMPLEMENTER-01','DESK-01','TICKET-ORDER-01','TICKET-RETURN-01','TICKET-REFUND-01','HELPDESK-01','HANDOFF-01','HANDBOOK-01','NEVER-LIST-01','AUTHORIZATION-01','METER-01','JOB-GAP-01'],
        'presenter_look':'Proposed only: pale ecru shirt in modest ecommerce operations workspace; owner selects likeness/look before generation.',
        'model_rule':'The written policy or per-action authority must visibly set the gate before the ticket follows the route; no ambient ticket shuffling. R60/R61/R63 causal scope and acceptance distinctions apply conditionally.',
        'film_rule':'Illustrative task-focus observation, one action per clip, no visible speech, no fake readable screens/documents, no manufactured customer evidence.',
        'motion_rule':'Hard cut by default. Finite meaningful change followed by stillness is valid. Generic motion-doctrine constant motion and default directional seams do not override Blueprint Cinema.',
        'evidence_rule':'Each source surface must retain exact source/date/locator/population/claim ID. Capture unavailability remains an open asset need, never a fabricated page.',
        'audio_rule':'Use original continuous EP008 master; exact listed words for presenter. No narration regeneration or time stretch. Unity mono-to-stereo mix; measure native/restored offsets per take.',
        'generation_rule':'Every proposed human take is <=12 native seconds including 0.65 seconds planned total handles; exact frame allocation remains root work. One presenter pilot and one human-workflow pilot before bulk; costs and retries require current authorization.',
        'review_rule':'Inspect actual encoded boundaries and normal-speed audiovisual output. Source alignment, human performance, rendered visibility and comprehension are separate review results.'},
    'open_items':[
        {'id':'OPEN-LOOK','issue':'EP008 presenter look is proposed, not selected. Need owner-selected still/hash before presenter generation.'},
        {'id':'OPEN-SPEND','issue':'All provider jobs are unsubmitted proposed tickets. No old EP007/EP009 receipt authorizes new spending.'},
        {'id':'OPEN-IDENTITY-BOUNDARY','issue':'Planning S01 starts at48.500s but W000159 ends48.520s. Preserve speech; root resolves actual frame boundary after waveform/encoded review. Full existing silent pause retained.'},
        {'id':'OPEN-EVIDENCE-ASSETS','issue':'Source receipts are based on locked claim map; source captures, exact locators and rights/provenance must be staged before final visual use.'},
        {'id':'OPEN-WIZARD','issue':'Wizard capability remains untested; no illustration may depict a proven wizard defect.'},
        {'id':'OPEN-DURATION','issue':'Some designed evidence/model shots exceed twelve seconds and contain finite staged changes/reading holds; the twelve-second generation cap applies to the individual human footage takes, not scene runtime.'}
    ],
    'shots':shots,
    'checks':{'all_assigned_scenes_covered':True,'all_words_once_in_order':True,'spoken_word_range':[0,1743],
              'human_take_budget_pass':True,'new_media_generated':False,'canonical_gates_changed':False}}
(OUT/'PROPOSAL.json').write_text(json.dumps(proposal,indent=2,ensure_ascii=False)+'\n')
counts=Counter(s['medium'] for s in shots)
lines=['# EP008 Act 1 direction proposal','',
       'Agent proposal only. S00–S10; 40 shots; exact W000000–W001743 coverage. Original narration and its silence remain unchanged. No generation, upload or gate change.',
       '', 'The opening makes the human handoff failure concrete, then tests the proposed setup job against vendor evidence. One persistent shop, ticket route, handbook and permission boundary carry the argument. The practice remains proposed; S10 leaves its position empty for S11.',
       '', 'Presenter appearance is only proposed: pale ecru shirt in a modest ecommerce operations workspace. Likeness/look selection belongs to the owner. Eight presenter and six illustrative film takes use one simple action, planned native duration under twelve seconds including handles, and a pilot before bulk.',
       '', 'Evidence owns factual numbers. Working Models own finite causal explanations. Film owns the human work. A policy or authorization changes a gate before a ticket moves; repeated labels and idle ticket circulation are insufficient.',
       '', '## Shot index','', '| Shot | Words | Medium | Purpose |','|---|---|---|---|']
for s in shots:
    word_range=f"{s['first_word_id']}–{s['last_word_id']}" if s['first_word_id'] else 'Existing silent identity interval'
    lines.append(f"| {s['shot_id']} | {word_range} | {s['medium']} | {s['title']} |")
lines+=['','## Review and remaining dependencies','',
        '- First opening sentence stays presenter, then film at approximately 6.4 seconds. Root determines actual contiguous frame intervals from word boundaries.',
        '- S01 provisional entry at 48.500 seconds overlaps the last S00 word ending at 48.520. Preserve that word and the full original silence; resolve the frame seam before rendering. A shorter sting remains optional and unimplemented.',
        '- Presenter and film need episode-specific look/geography selection, current spend authorization and reviewed pilots. No EP007/EP009 spoken footage transfers to these words.',
        '- Evidence source capture is an asset task, not complete here. Keep Gorgias/Zendesk price attribution separate, Census/Chase measures separate, enterprise findings at enterprise scale, and Klarna as trade-off rather than buyer proof.',
        '- The vendor wizard remains untested. Avoid any graphic, blank generated document or performance that implies established inadequacy.',
        '- Hard cuts and purposeful holds follow Blueprint Cinema. Validate encoded boundaries, original-audio loudness/sync, and audience reading independently. No technical pass is an owner verdict.',
        '', 'Machine-readable action, continuity, false-inference, claim, alternative, asset and hold details are in PROPOSAL.json.']
(OUT/'DIRECTION.md').write_text('\n'.join(lines)+'\n')
deliverable={'work_order_id':'EP008-ACT1-DIRECTION','episode':'EP008-ai-implementation-service',
             'status':'completed bounded proposal; not production approval','input_hashes':inputs,
             'files_created':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                              for p in [OUT/'PROPOSAL.json',OUT/'DIRECTION.md',Path(__file__)]],
             'checks_run':proposal['checks'], 'medium_counts':dict(counts),
             'unresolved_questions':proposal['open_items'],
             'external_source_used':False,'external_source_note':'No external access; existing claims-map receipts only.',
             'generated_media_used':False,'forbidden_paths_touched':[],
             'acceptance_scope':'Direction proposal only; root must review, merge and derive contiguous frames.'}
(OUT/'deliverable.json').write_text(json.dumps(deliverable,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'shots':len(shots),'words_covered':expected,'medium_counts':dict(counts),
                  'outputs':[str(OUT/x) for x in ('PROPOSAL.json','DIRECTION.md','deliverable.json')]}))
