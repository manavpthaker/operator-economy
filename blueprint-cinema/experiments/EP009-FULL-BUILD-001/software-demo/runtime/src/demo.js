'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const local = path.join(root, '.local');
const stateFile = path.join(local, 'state.json');
const hash = value => crypto.createHash('sha256').update(typeof value === 'string' ? value : JSON.stringify(value)).digest('hex');
const fixture = Object.freeze({
  id:'alder-maya-20260918', guest:'Maya Chen', property:'Alder House Inn', fictional:true,
  checkout:'2026-09-18T10:00:00-04:00', timezone:'America/New_York',
  communicationPreference:'One-off thank-you only. No future promotions.',
  oneOffThankYou:true, seasonalCampaign:false,
  innNotes:'A small, independent inn. Voice: warm, direct and unhurried. Thank Maya for staying. No invented activities, staff interactions, gifts or personal history. No discount, booking link or future promotion.',
  nextDayRule:'Next calendar day at 10:00 America/New_York'
});
function atomic(file, value) { fs.mkdirSync(path.dirname(file),{recursive:true}); const tmp=file+'.tmp'; fs.writeFileSync(tmp,JSON.stringify(value,null,2)+'\n',{mode:0o600}); fs.renameSync(tmp,file); }
function initial(){ return {schema:'ep009-node-red-demo/v1',fixture,providerAttempts:0,maxProviderAttempts:2,draft:null,queue:null,review:null,seasonal:{eligible:false,humanConfirmed:false,reason:null},lastEvent:null,createdAt:new Date().toISOString()}; }
function state(){ if(!fs.existsSync(stateFile))atomic(stateFile,initial()); const s=JSON.parse(fs.readFileSync(stateFile,'utf8')); if(s.fixture.id!==fixture.id)throw new Error('Unexpected fixture. Preserve state and inspect.'); return s; }
function event(s,type,data){
  const at=new Date().toISOString();
  const e={schema:'ep009-demo-event/v1',at,type,fixtureId:fixture.id,data,previousEvent:s.lastEvent};
  e.sha256=hash(e); s.lastEvent=e.sha256;s.updatedAt=at;
  fs.appendFileSync(path.join(local,'events.jsonl'),JSON.stringify(e)+'\n',{mode:0o600});atomic(stateFile,s);return s;
}
function readPublic(){ const s=state();return {...s,capability:{providerEnabled:process.env.EP009_ALLOW_OPENAI==='1',providerKeyPresent:Boolean(process.env.OPENAI_API_KEY),model:process.env.EP009_OPENAI_MODEL||'gpt-4.1-mini',maxOutputTokens:180},service:'Node-RED · OpenAI / test workflow',emailSendingAvailable:false}; }
function problem(code,message){const e=new Error(message);e.statusCode=code;throw e;}
function prepareDraft(){
  const s=state();
  if(s.draft)problem(409,'A real draft already exists. Reuse it; this demo does not regenerate automatically.');
  if(process.env.EP009_ALLOW_OPENAI!=='1')problem(403,'Provider test is not enabled yet. No request was sent.');
  if(!process.env.OPENAI_API_KEY)problem(503,'Server API key is unavailable. No request was sent.');
  if(s.providerAttempts>=s.maxProviderAttempts)problem(409,'The two-request cap has been reached. No request was sent.');
  if(s.pendingRun)problem(409,'One provider request is already in progress.');
  const model=process.env.EP009_OPENAI_MODEL||'gpt-4.1-mini';
  const prompt='Draft ONE short thank-you note of 45–70 words, from the inn to the guest. Output only the note. It is a one-off post-stay thank-you, not a marketing campaign. Do not offer promotions, ask for another booking, or invent guest history.\n\n'+JSON.stringify(fixture);
  const body={model,input:prompt,max_output_tokens:180,store:false};
  const runId='draft-'+new Date().toISOString().replace(/[:.]/g,'-')+'-'+crypto.randomBytes(3).toString('hex');
  const dir=path.join(local,'runs',runId);fs.mkdirSync(dir,{recursive:true});
  atomic(path.join(dir,'REQUEST.json'),{runId,at:new Date().toISOString(),fixtureId:fixture.id,body,bodySha256:hash(body),maximumRequests:2,operation:'real_openai_response',noEmailSend:true});
  s.providerAttempts++;s.pendingRun=runId;event(s,'provider_request_intent',{runId,model,requestSha256:hash(body),maxOutputTokens:180,attempt:s.providerAttempts});
  return {runId,body,url:'https://api.openai.com/v1/responses'};
}
function finishDraft(runId,response,statusCode){
  const s=state();if(s.pendingRun!==runId)problem(409,'Provider result does not match the pending run.');
  const dir=path.join(local,'runs',runId);
  atomic(path.join(dir,'RESPONSE.json'),{statusCode,response,receivedAt:new Date().toISOString()});
  delete s.pendingRun;
  if(statusCode<200||statusCode>=300||response.error){
    const code=String(response?.error?.code||'provider_http_'+statusCode).slice(0,100);
    event(s,'provider_request_failed',{runId,statusCode,code});problem(502,'OpenAI request failed ('+code+'). The attempt is retained; no automatic retry.');
  }
  const text=(response.output||[]).flatMap(x=>x.content||[]).filter(x=>x.type==='output_text').map(x=>x.text).join('\n').trim();
  if(!text){event(s,'provider_request_failed',{runId,statusCode,code:'empty_output'});problem(502,'Provider returned no usable text. No automatic retry.');}
  s.draft={id:runId,providerResponseId:response.id||null,model:response.model||null,rawText:text,text,createdAt:new Date().toISOString(),requestSha256:hash(JSON.parse(fs.readFileSync(path.join(dir,'REQUEST.json'),'utf8')).body),responseSha256:hash(response),usage:response.usage||null,source:'real_openai_response',mock:false};
  event(s,'draft_created',{runId,responseId:s.draft.providerResponseId,responseSha256:s.draft.responseSha256,textSha256:hash(text),usage:s.draft.usage});return readPublic();
}
function failDraft(runId){const s=state();if(s.pendingRun===runId){delete s.pendingRun;event(s,'provider_transport_failed',{runId,reason:'Transport failure; see local Node-RED runtime log. No automatic retry.'});}}
function queue(){const s=state();if(!s.draft)problem(409,'Create a real draft before queueing.');if(s.queue)return readPublic();
  // This isolated fixture is deliberately fixed: next calendar day, local 10am, same UTC−04 offset.
  if(s.fixture.checkout!=='2026-09-18T10:00:00-04:00')problem(409,'Fixture timestamp differs from the bound example.');
  const next=new Date(Date.parse(s.fixture.checkout)+24*60*60*1000);
  const localDate=new Intl.DateTimeFormat('en-CA',{timeZone:s.fixture.timezone,year:'numeric',month:'2-digit',day:'2-digit'}).format(next);
  s.queue={id:'queue-'+s.draft.id,draftId:s.draft.id,checkout:s.fixture.checkout,scheduledFor:localDate+'T10:00:00-04:00',scheduledUtc:next.toISOString(),timezone:s.fixture.timezone,status:'awaiting_human_review',sendEnabled:false,queuedAt:new Date().toISOString()};
  event(s,'draft_queued',{...s.queue,rule:s.fixture.nextDayRule});return readPublic();}
function saveReview(input){const s=state();if(!s.draft||!s.queue)problem(409,'Create and queue the draft first.');const text=String(input.text||'').trim();if(!text||text.length>3000)problem(400,'Provide a non-empty draft of at most3000 characters.');const before=s.draft.text;s.draft.text=text;s.review={editedAt:new Date().toISOString(),edited:before!==text||Boolean(s.review?.edited),approved:false,approvalScope:'one_off_thank_you_only'};s.queue.status='awaiting_human_review';event(s,'human_saved_edit',{draftId:s.draft.id,beforeText:before,afterText:text,beforeSha256:hash(before),afterSha256:hash(text)});return readPublic();}
function approve(){const s=state();if(!s.review||!s.queue)problem(409,'Save and review the draft before approval.');if(!s.fixture.oneOffThankYou)problem(409,'The fixture does not permit a thank-you.');s.review.approved=true;s.review.approvedAt=new Date().toISOString();s.queue.status='approved_draft_only';event(s,'human_approved_one_draft',{draftId:s.draft.id,scope:'one_off_thank_you_only',sendEnabled:false,broaderCampaignApproved:false});return readPublic();}
function exclude(){const s=state();s.seasonal={eligible:false,humanConfirmed:true,reason:'One-off thank-you only. No future promotions.',confirmedAt:new Date().toISOString()};event(s,'human_confirmed_seasonal_exclusion',{eligible:false,previousEligible:false,reason:s.seasonal.reason,fixturePreference:fixture.communicationPreference});return readPublic();}
module.exports={readPublic,prepareDraft,finishDraft,failDraft,queue,saveReview,approve,exclude,html:()=>fs.readFileSync(path.join(__dirname,'review.html'),'utf8')};
