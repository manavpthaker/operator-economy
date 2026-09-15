import {readFile,writeFile,access} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {createRequire} from 'node:module';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
const root=dirname(fileURLToPath(import.meta.url)),repo=resolve(root,'../../../../../..');
const require=createRequire(resolve(root,'../r11-presenter-first/package.json'));
const {fal}=await import(require.resolve('@fal-ai/client'));
const mode=process.argv[2],id=process.argv[3];
assert(['upload','submit','status','result','download'].includes(mode));assert(['a','b'].includes(id));
const hash=b=>createHash('sha256').update(b).digest('hex');
const read=p=>readFile(resolve(root,p));
const json=async p=>JSON.parse(await read(p));
const save=(name,j,exclusive=false)=>writeFile(resolve(root,`provider/${id}-${name}.json`),JSON.stringify(j,null,2)+'\n',exclusive?{flag:'wx'}:{});
const exists=async p=>{try{await access(resolve(root,p));return true;}catch(e){if(e.code==='ENOENT')return false;throw e;}};
const auth=await json('GENERATION-AUTHORIZATION.json'),manifest=await json('provider/INPUTS.json');
assert.equal(auth.status,'authorized');assert.equal(auth.owner_statement,'lets do it');assert.equal(auth.maximum_submissions,2);assert.equal(auth.automatic_retries,0);assert.equal(auth.model,'fal-ai/sync-lipsync/v3');
assert(auth.conservative_total_usd_max<=auth.agent_imposed_estimated_usd_ceiling);
const input=manifest.inputs.find(x=>x.id===id);assert(input);
assert.equal(hash(await read(input.audio_path)),input.audio_sha256);assert.equal(hash(await read(input.video_path)),input.video_sha256);
const env=await readFile(resolve(repo,'.env'),'utf8');
const key=process.env.FAL_KEY||env.split(/\r?\n/).find(l=>l.startsWith('FAL_KEY='))?.slice(8).trim().replace(/^['"]|['"]$/g,'');
if(!key)throw new Error('FAL_KEY unavailable');
fal.config({credentials:key});
async function api(url,body){
 assert.equal(new URL(url).hostname,'queue.fal.run');
 const response=await fetch(url,{method:body?'POST':'GET',headers:{Authorization:`Key ${key}`,'Content-Type':'application/json','X-Fal-No-Retry':'1','x-app-fal-disable-fallback':'1'},...(body?{body:JSON.stringify(body)}:{}),signal:AbortSignal.timeout(60000)});
 const payload=await response.json();
 if(!response.ok){await save('ERROR',{http_status:response.status,payload,actual_billed_usd:null});throw new Error(`Fal HTTP${response.status}; sanitized summary only; inspect local error receipt; no automatic retry`);}
 return payload;
}
if(mode==='upload'){
 assert(!await exists(`provider/${id}-UPLOAD.json`),'Upload receipt exists; reuse it');
 const audio=await read(input.audio_path),video=await read(input.video_path);
 const audio_url=await fal.storage.upload(new File([audio],`ep007-r15-pickup-${id}.wav`,{type:'audio/wav'}));
 const video_url=await fal.storage.upload(new File([video],`ep007-r15-performance-${id}.mp4`,{type:'video/mp4'}));
 await save('UPLOAD',{audio_url,video_url,audio_sha256:input.audio_sha256,video_sha256:input.video_sha256},true);
 console.log(JSON.stringify({id,uploaded:true,duration:input.duration}));
}else if(mode==='submit'){
 const upload=await json(`provider/${id}-UPLOAD.json`);
 assert.equal(upload.audio_sha256,input.audio_sha256);assert.equal(upload.video_sha256,input.video_sha256);
 const body={video_url:upload.video_url,audio_url:upload.audio_url,sync_mode:'cut_off'};
 await save('ATTEMPT',{at:new Date().toISOString(),model:auth.model,input:body,input_sha256:hash(JSON.stringify(body)),authorization_sha256:hash(await read('GENERATION-AUTHORIZATION.json')),duration:input.duration,estimated_usd:input.duration*8/60,status:'pending_or_uncertain',retry_permitted:false},true);
 const job=await api('https://queue.fal.run/'+auth.model,body);
 await save('JOB',job,true);console.log(JSON.stringify({id,request_id:job.request_id,status:job.status}));
}else if(mode==='status'||mode==='result'){
 const job=await json(`provider/${id}-JOB.json`),result=await api(mode==='status'?job.status_url:job.response_url);
 await save(mode.toUpperCase(),result);
 console.log(JSON.stringify(mode==='status'?{id,request_id:job.request_id,status:result.status,queue_position:result.queue_position}:{id,result_received:true,video:!!result.video?.url}));
}else{
 const result=await json(`provider/${id}-RESULT.json`),url=result.video?.url;
 assert(url&&new URL(url).protocol==='https:');assert(!await exists(`provider/presenter-${id}-generated.mp4`));
 const response=await fetch(url,{signal:AbortSignal.timeout(60000)});assert(response.ok,'Download failed');
 const bytes=Buffer.from(await response.arrayBuffer());
 await writeFile(resolve(root,`provider/presenter-${id}-generated.mp4`),bytes,{flag:'wx'});
 await save('DOWNLOAD',{url,path:`provider/presenter-${id}-generated.mp4`,bytes:bytes.length,sha256:hash(bytes)},true);
 console.log(JSON.stringify({id,downloaded:true,bytes:bytes.length,sha256:hash(bytes)}));
}
