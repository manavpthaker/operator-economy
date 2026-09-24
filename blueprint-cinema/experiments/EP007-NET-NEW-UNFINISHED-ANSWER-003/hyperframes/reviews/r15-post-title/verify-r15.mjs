import {readFile,readdir,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
const root=dirname(fileURLToPath(import.meta.url)),baseline=resolve(root,'../r13-unanswered-job'),repo=resolve(root,'../../../../../..');
const read=(base,path)=>readFile(resolve(base,path));
const digest=b=>createHash('sha256').update(b).digest('hex');
const sha=async(base,path)=>digest(await read(base,path));
const original=await read(baseline,'index.html'),current=await read(root,'index.html');
assert.equal(digest(original),'8e814b137d6ff1696050834e216bfdf880a0c22f75674040325f3a6876944da5');
function clips(html){return [...html.toString().matchAll(/<(video|audio|div)\b([^>]+)>/g)].map(m=>({tag:m[1],...Object.fromEntries([...m[2].matchAll(/([\w-]+)="([^"]*)"/g)].filter(x=>x[1]!=='data-hf-id').map(x=>[x[1],x[2]]))})).filter(x=>x['data-track-index']);}
const before=clips(original),after=clips(current);
assert.deepEqual(after.filter(x=>+x['data-start']<56.5),before,'Accepted intro drift');
assert.equal(after.length,18);assert(!current.includes('opening-bridge'));assert(!current.includes('25 years.'));
const assets=[];
for(const folder of ['public/media','public/audio','public/fonts','public/vendor','compositions']){
 for(const d of await readdir(resolve(baseline,folder),{withFileTypes:true})){if(!d.isFile())continue;const path=folder+'/'+d.name,a=await read(baseline,path),b=await read(root,path);assert(a.equals(b),'Retained asset changed '+path);assets.push({path,sha256:digest(b),bytes:b.length,retained_r13:true});}
}
function pcm(b){let p=12,data,fmt;assert.equal(b.toString('ascii',0,4),'RIFF');while(p+8<=b.length){const n=b.readUInt32LE(p+4),id=b.toString('ascii',p,p+4);if(id==='fmt ')fmt=b.subarray(p+8,p+8+n);if(id==='data')data=b.subarray(p+8,p+8+n);p+=8+n+(n%2);}assert.equal(fmt.readUInt16LE(0),1);assert.equal(fmt.readUInt16LE(2),1);assert.equal(fmt.readUInt32LE(4),48000);assert.equal(fmt.readUInt16LE(14),16);return data;}
const masterPath='operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav';
const masterBytes=await read(repo,masterPath);assert.equal(digest(masterBytes),'d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9');
const master=pcm(masterBytes),extended=pcm(await read(root,'public/audio/review-narration-extended.wav'));
assert(extended.equals(master.subarray(0,3576000*2)));
const audio=after.filter(x=>x.tag==='audio').sort((a,b)=>+a['data-start']-+b['data-start']);
assert.deepEqual(audio.map(x=>[+x['data-start'],+x['data-duration'],+x['data-media-start']]),[[0,45,0],[45,11.5,48],[56.5,15,59.5]]);
const pieces=[];for(const c of audio){assert.equal(c['data-volume'],'1');const samples=pcm(await read(root,c.src));pieces.push(samples.subarray(Math.round(+c['data-media-start']*48000)*2,Math.round((+c['data-media-start'] + +c['data-duration'])*48000)*2));}
const assembled=Buffer.concat(pieces);assert.equal(assembled.length,3432000*2);assert(assembled.equals(Buffer.concat([master.subarray(0,45*48000*2),master.subarray(48*48000*2,74.5*48000*2)])));
assert(master.subarray(45*48000*2,48*48000*2).every(x=>x===0));
const picture=after.filter(x=>x['data-track-index']==='1').sort((a,b)=>+a['data-start']-+b['data-start']);let cursor=0;
const probes={};for(const c of picture){const start=+c['data-start'],duration=+c['data-duration'];assert(Math.abs(start-cursor)<1e-7);assert(Math.abs(start*24-Math.round(start*24))<1e-7);assert(Math.abs(duration*24-Math.round(duration*24))<1e-7);cursor=start+duration;if(c.tag==='video'){probes[c.src]||=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-of','json',resolve(root,c.src)],{encoding:'utf8'}));const v=probes[c.src].streams.find(x=>x.codec_type==='video');assert.equal(v.r_frame_rate,'24/1');assert(+c['data-media-start']+duration<=+v.duration+1e-6);assert(current.toString().match(new RegExp('<video[^>]*id="'+c.id+'"[^>]*>'))[0].includes('muted'));}else{const sub=(await read(root,c['data-composition-src'])).toString();assert(sub.includes('<template>'));assert(sub.includes('data-composition-id="'+c['data-composition-id']+'"'));}}
assert.equal(cursor,71.5);assert.equal(picture.length,15);
for(const [id,frames] of [['a',154],['b',206]]){const path=`public/media/post-title-${id}.mp4`,v=probes[path].streams[0];assert.equal(v.pix_fmt,'yuv420p');assert.equal(+v.nb_frames,frames);assert.equal(probes[path].streams.length,1);assets.push({path,sha256:await sha(root,path),frames,retained_r13:false});}
assets.push({path:'public/audio/review-narration-extended.wav',sha256:await sha(root,'public/audio/review-narration-extended.wav'),retained_r13:false});
const authored=[];for(const path of ['index.html','BRIEF.md','frame.md','STORYBOARD.md','GENERATION-AUTHORIZATION.json','provider/INPUTS.json','verify-r15.mjs'])authored.push({path,sha256:await sha(root,path)});
const result={checked_at:new Date().toISOString(),ok:true,scope:'isolated extended preview; not final delivery or mouth-accuracy certification',dimensions:[1280,720],duration:71.5,fps:24,frames:1716,checks:{r13_root_and_all_24_retained_files_preserved:true,all_15_prior_clip_declarations_preserved:true,picture_15_clips_frame_aligned_gapless:true,original_audio_exact_retained_samples:true,only_prior_three_seconds_silence_omitted:true,all_picture_muted:true,no_rejected_r14_overlay:true,source_bounds:true,new_video_frames_and_8bit_proxy:true},authored,assets,timeline:picture,audio,assembled_pcm_sha256:digest(assembled),provider:'fal-ai/sync-lipsync/v3',paid_submissions:2,actual_billed_usd:null,final_render:false};
await writeFile(resolve(root,'ASSET-AND-EDIT-MANIFEST.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({ok:true,duration:71.5,frames:1716,pictureClips:15,audioClips:3,index_sha256:digest(current)}));
