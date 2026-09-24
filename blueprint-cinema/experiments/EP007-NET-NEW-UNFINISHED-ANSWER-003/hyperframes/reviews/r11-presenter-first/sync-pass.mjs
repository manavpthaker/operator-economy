import { readFile, writeFile, mkdir, access } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const root = dirname(fileURLToPath(import.meta.url));
const repo = resolve(root, '../../../../../..');
const receipts = resolve(root, 'renders');
const mode = process.argv[2];
const hash = b => createHash('sha256').update(b).digest('hex');
const save = async (name, data, flags) => writeFile(resolve(receipts, name), JSON.stringify(data, null, 2)+'\n', flags);
await mkdir(receipts, {recursive:true});
const env = await readFile(resolve(repo, '.env'), 'utf8');
const key = process.env.FAL_KEY || env.split(/\r?\n/).find(l=>l.startsWith('FAL_KEY='))?.slice(8).trim().replace(/^['"]|['"]$/g,'');
if (!key) throw new Error('FAL_KEY unavailable');
async function api(url, body) {
  if (new URL(url).hostname !== 'queue.fal.run') throw new Error('Unexpected API host');
  const response = await fetch(url, {method: body ? 'POST':'GET', headers:{Authorization:`Key ${key}`,'Content-Type':'application/json'}, ...(body ? {body:JSON.stringify(body)}:{}), signal:AbortSignal.timeout(60000)});
  const payload = await response.json();
  if (!response.ok) {
    const sanitized = JSON.parse(JSON.stringify(payload, (k,v)=>k==='input'?'[media input omitted]':typeof v==='string'&&v.startsWith('data:')?'[data URI omitted]':v));
    await save('SYNC-ERROR.json',{http_status:response.status,payload:sanitized,job_record_preserved:true,retry_permitted:false,actual_billed_usd:null});
    throw new Error(`Fal ${response.status}: ${JSON.stringify(sanitized).replaceAll(key,'[REDACTED]').slice(0,1200)}`);
  }
  return payload;
}
if (mode === 'submit') {
  const auth = JSON.parse(await readFile(resolve(root,'GENERATION-AUTHORIZATION.json'),'utf8'));
  if(auth.status!=='authorized'||auth.maximum_submissions!==1||auth.maximum_estimated_usd<12.05*8/60) throw new Error('Authorization mismatch');
  const original = resolve(repo,'blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/404.mp4');
  if(hash(await readFile(original))!=='a0de31c36bde22219a1e067178b86cf750e7da1f11a69a775c370c82df6f29dd') throw new Error('Performance source hash mismatch');
  const previous = JSON.parse(await readFile(resolve(repo,'blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/FAL-SYNC-REQUEST.json'),'utf8'));
  const audio = await readFile(resolve(root,'public/audio/presenter-pickups.wav'));
  const body = {video_url:previous.input.video_url,audio_url:`data:audio/wav;base64,${audio.toString('base64')}`,sync_mode:'cut_off'};
  // Exclusive pre-submit checkpoint survives a timeout before a job ID is returned.
  await save('SYNC-SUBMISSION-ATTEMPT.json',{at:new Date().toISOString(),model:auth.model,audio_sha256:hash(audio),input_sha256:hash(JSON.stringify(body)),estimated_usd_max:12.05*8/60,status:'submission_pending_or_uncertain',retry_permitted:false},{flag:'wx'});
  await save('SYNC-REQUEST.json',{model:auth.model,input:{...body,audio_url:'local:public/audio/presenter-pickups.wav'},audio_sha256:hash(audio),full_request_sha256:hash(JSON.stringify(body))});
  const job = await api(`https://queue.fal.run/${auth.model}`,body);
  await save('SYNC-JOB.json',job,{flag:'wx'});
  console.log(JSON.stringify({request_id:job.request_id,status:job.status}));
} else if(mode==='status'||mode==='result') {
  const job = JSON.parse(await readFile(resolve(receipts,'SYNC-JOB.json'),'utf8'));
  const data = await api(mode==='status'?job.status_url:job.response_url);
  await save(mode==='status'?'SYNC-STATUS.json':'SYNC-RESULT.json',data);
  console.log(JSON.stringify(mode==='status'?{request_id:job.request_id,status:data.status,queue_position:data.queue_position}:data));
} else if(mode==='download') {
  const result = JSON.parse(await readFile(resolve(receipts,'SYNC-RESULT.json'),'utf8'));
  const url = result.video?.url;
  if(!url||new URL(url).protocol!=='https:') throw new Error('No HTTPS result');
  const output=resolve(root,'public/media/presenter-pickups.mp4');
  try { await access(output); throw new Error('Output exists; not replacing'); } catch(e) { if(e.code!=='ENOENT') throw e; }
  const response = await fetch(url,{signal:AbortSignal.timeout(60000)});
  if(!response.ok) throw new Error(`Download ${response.status}`);
  const bytes=Buffer.from(await response.arrayBuffer());
  await writeFile(output,bytes,{flag:'wx'});
  await save('SYNC-DOWNLOAD.json',{output,sha256:hash(bytes),bytes:bytes.length,url});
  console.log(JSON.stringify({output,sha256:hash(bytes),bytes:bytes.length}));
} else throw new Error('Choose submit, status, result or download');
