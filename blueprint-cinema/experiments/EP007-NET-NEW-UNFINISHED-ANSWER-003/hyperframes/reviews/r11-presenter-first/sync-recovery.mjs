import { fal } from '@fal-ai/client';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const root=dirname(fileURLToPath(import.meta.url)), repo=resolve(root,'../../../../../..');
const mode=process.argv[2], attempt=process.argv[3]||'002';
if(!/^00[2-9]$/.test(attempt)) throw new Error('Explicit recovery attempt002–009 required');
const dir=resolve(root,`renders/recovery-${attempt}`);
await mkdir(dir,{recursive:true});
const hash=b=>createHash('sha256').update(b).digest('hex');
const save=(name,j,exclusive=false)=>writeFile(resolve(dir,name),JSON.stringify(j,null,2)+'\n',exclusive?{flag:'wx'}:{});
const env=await readFile(resolve(repo,'.env'),'utf8');
const key=process.env.FAL_KEY||env.split(/\r?\n/).find(l=>l.startsWith('FAL_KEY='))?.slice(8).trim().replace(/^['"]|['"]$/g,'');
if(!key) throw new Error('FAL_KEY unavailable');
fal.config({credentials:key});
async function api(url,body) {
  if(new URL(url).hostname!=='queue.fal.run') throw new Error('Unexpected API host');
  const r=await fetch(url,{method:body?'POST':'GET',headers:{Authorization:`Key ${key}`,'Content-Type':'application/json','X-Fal-No-Retry':'1','x-app-fal-disable-fallback':'1'},...(body?{body:JSON.stringify(body)}:{}),signal:AbortSignal.timeout(60000)});
  const j=await r.json();
  if(!r.ok) {await save('ERROR.json',{http_status:r.status,payload:j,actual_billed_usd:null});throw new Error(`Fal${r.status}: ${JSON.stringify(j).replaceAll(key,'[REDACTED]').slice(0,1500)}`);}
  return j;
}
if(mode==='upload') {
  const b=await readFile(resolve(root,'public/audio/presenter-pickups.wav'));
  const url=await fal.storage.upload(new File([b],'ep007-r11-presenter-pickups.wav',{type:'audio/wav'}));
  await save('UPLOAD.json',{url,sha256:hash(b),bytes:b.length,sdk:'@fal-ai/client@1.10.1'},true);
  console.log(JSON.stringify({uploaded:true,bytes:b.length,sha256:hash(b)}));
} else if(mode==='submit') {
  const auth=JSON.parse(await readFile(resolve(root,'RECOVERY-AUTHORIZATION.json'),'utf8'));
  if(auth.owner_statement!=='do it and retry as much as necessary') throw new Error('Authorization mismatch');
  const upload=JSON.parse(await readFile(resolve(dir,'UPLOAD.json'),'utf8'));
  if(hash(await readFile(resolve(root,'public/audio/presenter-pickups.wav')))!==upload.sha256) throw new Error('Audio changed after upload');
  const parent=JSON.parse(await readFile(resolve(repo,'blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/FAL-SYNC-REQUEST.json'),'utf8'));
  const input={video_url:parent.input.video_url,audio_url:upload.url,sync_mode:'cut_off'};
  await save('ATTEMPT.json',{at:new Date().toISOString(),model:'fal-ai/sync-lipsync/v3',input,request_sha256:hash(JSON.stringify(input)),estimated_usd_max:12.05*8/60,status:'pending_or_uncertain'},true);
  const job=await api('https://queue.fal.run/fal-ai/sync-lipsync/v3',input);
  await save('JOB.json',job,true);console.log(JSON.stringify({request_id:job.request_id,status:job.status}));
} else if(mode==='status'||mode==='result') {
  const job=JSON.parse(await readFile(resolve(dir,'JOB.json'),'utf8'));
  const j=await api(mode==='status'?job.status_url:job.response_url);
  await save(mode==='status'?'STATUS.json':'RESULT.json',j);
  console.log(JSON.stringify(mode==='status'?{request_id:job.request_id,status:j.status,queue_position:j.queue_position}:j));
} else if(mode==='download') {
  const result=JSON.parse(await readFile(resolve(dir,'RESULT.json'),'utf8'));
  if(!result.video?.url?.startsWith('https://')) throw new Error('No generated result');
  const r=await fetch(result.video.url,{signal:AbortSignal.timeout(60000)});if(!r.ok) throw new Error(`Download${r.status}`);
  const bytes=Buffer.from(await r.arrayBuffer());
  await writeFile(resolve(root,'public/media/presenter-pickups.mp4'),bytes,{flag:'wx'});
  await save('DOWNLOAD.json',{url:result.video.url,bytes:bytes.length,sha256:hash(bytes)});
  console.log(JSON.stringify({downloaded:true,bytes:bytes.length,sha256:hash(bytes)}));
} else throw new Error('Choose upload, submit, status, result, download');
