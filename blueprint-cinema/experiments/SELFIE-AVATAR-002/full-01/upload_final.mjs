import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const base=path.dirname(fileURLToPath(import.meta.url));
const repo=path.resolve(base,'../../../..');
const source=path.join(base,'assembly/renders/week2-full01-uncaptioned.mp4');
const folder=path.join(base,'upload');fs.mkdirSync(folder,{recursive:true});
const bytes=fs.readFileSync(source),sha256=crypto.createHash('sha256').update(bytes).digest('hex');
const qa=JSON.parse(fs.readFileSync(path.join(base,'FINAL-AUDIO-QA.json'),'utf8'));
if(qa.video_sha256!==sha256 || Math.abs(qa.global_audio.lag_seconds)>.025 || qa.global_audio.correlation<.98)throw Error('Final voice QA does not bind this output.');
const save=(name,data)=>fs.writeFileSync(path.join(folder,name),JSON.stringify(data,null,2)+'\n',{flag:'wx'});
save('INTENT.json',{at:new Date().toISOString(),source:path.relative(repo,source),sha256,scope:'Upload finished authorized Week2 review video. No generation or public posting.'});
const req=createRequire(path.join(repo,'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r11-presenter-first/package.json'));
const {fal}=req('@fal-ai/client');
const line=fs.readFileSync(path.join(repo,'.env'),'utf8').split(/\r?\n/).find(x=>x.startsWith('FAL_KEY='));
if(!line)throw Error('FAL_KEY unavailable');
fal.config({credentials:line.slice(8).trim().replace(/^['"]|['"]$/g,'')});
try{
 const file_url=await fal.storage.upload(new File([bytes],'selfie-week2-full01-'+sha256.slice(0,16)+'.mp4',{type:'video/mp4'}));
 save('RESPONSE.json',{at:new Date().toISOString(),file_url,sha256});
 const response=await fetch(file_url);if(!response.ok)throw Error('Readback failed');
 const check=Buffer.from(await response.arrayBuffer());
 if(crypto.createHash('sha256').update(check).digest('hex')!==sha256)throw Error('Readback hash mismatch');
 const record={status:'verified',file_url,sha256,size_bytes:bytes.length,content_type:response.headers.get('content-type'),at:new Date().toISOString()};
 save('UPLOAD.json',record);console.log(JSON.stringify(record));
}catch(error){save('ERROR.json',{name:error?.name||'Error',instruction:'Do not resubmit; reconcile saved response first.'});console.error('Upload or readback failed; inspect scoped receipts without repeating the upload.');process.exitCode=1;}
