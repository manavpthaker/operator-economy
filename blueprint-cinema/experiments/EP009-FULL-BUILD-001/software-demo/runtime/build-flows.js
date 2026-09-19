'use strict';
const fs=require('node:fs');
const tab='ep009workflow';const nodes=[{id:tab,type:'tab',label:'EP009 · One guest, one thank-you',disabled:false,info:'A real, isolated test workflow using fictional Maya Chen at Alder House Inn. OpenAI drafts; Node-RED persists a date-based queue. Human edits and approves one draft, and confirms exclusion from seasonal marketing. No email/send node exists.'}];
function node(id,type,name,x,y,extra={}){nodes.push({id,type,z:tab,name,x,y,...extra});}
function fn(id,name,x,y,func,wires,outputs=1){node(id,'function',name,x,y,{func,outputs,timeout:0,noerr:0,initialize:'',finalize:'',libs:[],wires});}
function input(id,url,method,y,next){node(id,'http in',method.toUpperCase()+' '+url,170,y,{url,method,upload:false,swaggerDoc:'',wires:[[next]]});}
const respond="msg.headers={'Content-Type':'application/json','Cache-Control':'no-store'}; return msg;";
const attempt=expression=>`const demo=global.get('ep009');try{msg.payload=${expression};msg.statusCode=200;}catch(e){msg.statusCode=e.statusCode||500;msg.payload={error:e.message};} ${respond}`;
node('response','http response','Real result → operator form',1190,440,{statusCode:'',headers:{},wires:[]});
input('page','/review','get',80,'pagehtml');fn('pagehtml','Working operator interface',460,80,"msg.payload=global.get('ep009').html(); msg.headers={'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store'};return msg;",[['response']]);
input('state','/api/state','get',140,'getstate');fn('getstate','Read persisted fixture + state',480,140,attempt('demo.readPublic()'),[['response']]);
input('draft','/api/draft','post',240,'prepdraft');
fn('prepdraft','Fictional fixture → capped real request',480,240,"const demo=global.get('ep009');try{const r=demo.prepareDraft();msg.ep009Run=r.runId;msg.url=r.url;msg.method='POST';msg.headers={'Authorization':'Bearer '+env.get('OPENAI_API_KEY'),'Content-Type':'application/json'};msg.payload=r.body;return [msg,null];}catch(e){msg.statusCode=e.statusCode||500;msg.payload={error:e.message};msg.headers={'Content-Type':'application/json'};return [null,msg];}",[['openai'],['response']],2);
node('openai','http request','OpenAI · genuine thank-you draft',790,240,{method:'use',ret:'obj',paytoqs:'ignore',url:'',tls:'',persist:false,proxy:'',insecureHTTPParser:false,authType:'',senderr:false,headers:[],wires:[['draftresult']]});
fn('draftresult','Bind output + retain usage',1050,240,"const demo=global.get('ep009');try{msg.payload=demo.finishDraft(msg.ep009Run,msg.payload,msg.statusCode||0);msg.statusCode=200;}catch(e){msg.statusCode=e.statusCode||500;msg.payload={error:e.message};}delete msg.ep009Run;"+respond,[['response']]);
input('queue','/api/queue','post',360,'queuedate');fn('queuedate','Checkout + one day → queued draft',530,360,attempt('demo.queue()'),[['response']]);
input('review','/api/review','post',440,'humanedit');fn('humanedit','Human voice edit → save',510,440,attempt('demo.saveReview(msg.payload||{})'),[['response']]);
input('approve','/api/approve','post',520,'humanapprove');fn('humanapprove','Human approval · one draft only',520,520,attempt('demo.approve()'),[['response']]);
input('exclude','/api/exclude','post',600,'humanexclude');fn('humanexclude','Human confirms NO future promotion',550,600,attempt('demo.exclude()'),[['response']]);
node('catch','catch','Transport failure',800,680,{scope:['openai'],uncaught:false,wires:[['failure']]});
fn('failure','Retain failure · never auto-retry',1050,680,"global.get('ep009').failDraft(msg.ep009Run);msg.statusCode=502;msg.payload={error:'Provider transport failed. Attempt retained; no automatic retry.'};delete msg.error;delete msg.ep009Run;"+respond,[['response']]);
node('note','comment','TEST WORKFLOW · FICTIONAL GUEST · NO SEND NODE',570,20,{info:'The displayed form is purpose-built and genuinely executes this flow. Results persist under ignored .local state. External request cap2; disabled until root enables EP009_ALLOW_OPENAI=1. No simulated model output.'});
fs.writeFileSync(require('node:path').join(__dirname,'flows.json'),JSON.stringify(nodes,null,2)+'\n');
