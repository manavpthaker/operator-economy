import {readFile,readdir,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';

const root=dirname(fileURLToPath(import.meta.url)),baseline=resolve(root,'../r13-unanswered-job');
const read=(base,path)=>readFile(resolve(base,path));
const hash=b=>createHash('sha256').update(b).digest('hex');
const sha=async(base,path)=>hash(await read(base,path));
const original=await read(baseline,'index.html'),current=await read(root,'index.html');
assert.equal(hash(original),'8e814b137d6ff1696050834e216bfdf880a0c22f75674040325f3a6876944da5','R13 baseline changed');
function clips(html){return [...html.toString().matchAll(/<(video|audio|div)\b([^>]+)>/g)].map(m=>({tag:m[1],...Object.fromEntries([...m[2].matchAll(/([\w-]+)="([^"]*)"/g)].filter(x=>x[1]!=='data-hf-id').map(x=>[x[1],x[2]]))})).filter(x=>x['data-track-index']);}
const before=clips(original),after=clips(current);
const retained=x=>x.filter(c=>['1','100'].includes(c['data-track-index']));
assert.deepEqual(retained(after),retained(before),'Picture or audio placements drifted');
assert.equal(after.filter(c=>c['data-track-index']==='1').length,13);
assert.equal(after.filter(c=>c.tag==='audio').length,2);
const overlay=after.filter(c=>c['data-track-index']==='10');
assert.equal(overlay.length,1);assert.equal(after.length,before.length+1);
assert.equal(+overlay[0]['data-start'],2.5);
assert.equal(+overlay[0]['data-duration'],124/24);
assert.equal(overlay[0]['data-composition-id'],'r14-opening-bridge');
assert.equal(overlay[0]['data-composition-src'],'compositions/opening-bridge.html');
assert(+overlay[0]['data-start']<97/24);
assert.equal(+overlay[0]['data-start'] + +overlay[0]['data-duration'],184/24);
assert(current.toString().includes('data-duration="56.5"'));
const tagClean=html=>html.toString().replace(/ data-hf-id="[^"]*"/g,'');
assert.deepEqual([...tagClean(current).matchAll(/<video\b[^>]*>/g)].map(x=>x[0]),[...tagClean(original).matchAll(/<video\b[^>]*>/g)].map(x=>x[0]));
const equal=[];
for(const folder of ['public/media','public/audio','public/fonts','public/vendor','compositions']){
  const names=(await readdir(resolve(baseline,folder),{withFileTypes:true})).filter(x=>x.isFile()).map(x=>x.name);
  for(const name of names){const path=folder+'/'+name,a=await read(baseline,path),b=await read(root,path);assert(a.equals(b),'Asset drift: '+path);equal.push({path,sha256:hash(b),bytes:b.length});}
  assert.deepEqual((await readdir(resolve(root,folder),{withFileTypes:true})).filter(x=>x.isFile()).map(x=>x.name).sort(),[...names,...(folder==='compositions'?['opening-bridge.html']:[])].sort());
}
assert.equal(await sha(root,'public/audio/review-narration.wav'),'edc0d688907fff230d203978b5cf875ac2cbe554b65376fa2e02f93579b99fe8');
assert.equal(await sha(root,'public/media/presenter-pickups-browser.mp4'),'502ba0dbeb2ba159c60a9df72c6a7a755947aac70bac10aa340f905ac4956d65');
const bridge=(await read(root,'compositions/opening-bridge.html')).toString();
assert(bridge.includes('<template>'));assert(bridge.includes('data-composition-id="r14-opening-bridge"'));assert(bridge.includes("window.__timelines['r14-opening-bridge']"));
assert(bridge.includes('>25 years.</div>'));assert(bridge.includes('>Profitable.</div>'));
const authored=[];
for(const path of ['index.html','compositions/opening-bridge.html','BRIEF.md','frame.md','STORYBOARD.md','verify-r14.mjs'])authored.push({path,sha256:await sha(root,path)});
const result={checked_at:new Date().toISOString(),ok:true,scope:'isolated preview; static regression and source hashes, not phoneme or encoded-export QA',baseline:{path:'../r13-unanswered-job',index_sha256:hash(original)},duration:56.5,frames:1356,fps:24,dimensions:[1280,720],checks:{r13_preserved:true,all_picture_and_audio_declarations_unchanged:true,all_24_retained_files_byte_identical:true,narration_and_avatar_source_pins:true,one_new_overlay_only:true,overlay_spans_first_cut:true,overlay_clears_one_frame_before_closeup:true,subcomposition_contract:true},overlay:{start:2.5,tenure_reveal_end:65/24,film_cut:97/24,profit_reveal_start:153/24,profit_reveal_end:157/24,exit_start:181/24,end:184/24,owner_closeup:185/24,track:10},retained:equal,authored,paid_generation:false,original_narration_changes:false,lip_sync_changes:false,final_render:false};
await writeFile(resolve(root,'ASSET-AND-EDIT-MANIFEST.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({ok:true,retainedFiles:equal.length,pictureClips:13,audioClips:2,newOverlay:1,duration:56.5,index_sha256:hash(current)}));
