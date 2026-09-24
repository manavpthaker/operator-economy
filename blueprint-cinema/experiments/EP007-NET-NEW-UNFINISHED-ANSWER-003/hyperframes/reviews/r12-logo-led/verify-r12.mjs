import {readFile,writeFile,readdir} from 'node:fs/promises';
// R12 preserves R11 source assets and PCM; only the logo/identity picture window changes.
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
const root=dirname(fileURLToPath(import.meta.url)),repo=resolve(root,'../../../../../..');
const digest=b=>createHash('sha256').update(b).digest('hex');
const read=p=>readFile(resolve(root,p));
const sha=async p=>digest(await read(p));
const master='operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav';
const pins=[
 [resolve(repo,master),'d8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9'],
 [resolve(repo,'blueprint-cinema/experiments/EP007-PREMIUM-CONTROLLED-004/review-media/404.mp4'),'a0de31c36bde22219a1e067178b86cf750e7da1f11a69a775c370c82df6f29dd'],
 ['public/media/presenter-identity.mp4','1752e0356a3c0b86cbee70849e2b40df6de4ba483db103e9f2ef9904d606b965'],
 ['public/media/presenter-pickups.mp4','6fb42c381d17d8dd2130e71a6986845f995f90d7e4f3c4a1a957b8973fbaf81f'],
 ['public/media/establishing.mp4','e0b4067004d83f4ba00be589d72ffc43d8305319a63be2217f19d594d6d2521c'],
 ['public/media/shot-b.mp4','7326ee4b326ff4397ea5b7158174004c0c66a62a3c90f6e0edd1e2e44a893f7f'],
 ['public/media/shot-c.mp4','8293c4bcc201259cb4624c94673690c1ec1d34a0bcdfa63464eae0a91feda60e'],
 ['public/media/shot-d.mp4','c09986f249dcdfe365a9bbd56fef13b89760f71d0503b8a31e3745ff7715fa4c'],
 ['public/media/shot-e.mp4','36ddf54067fb28c2223a81ce8dcac31298112cdd5c6b862eeb6e772ae10598a2']
];
for(const [p,s] of pins) assert.equal(await sha(p),s,'stale input '+p);
function wav(b){assert.equal(b.toString('ascii',0,4),'RIFF');let i=12,format,data;while(i+8<=b.length){const n=b.readUInt32LE(i+4),tag=b.toString('ascii',i,i+4);if(tag==='fmt ') format=b.subarray(i+8,i+8+n);if(tag==='data')data=b.subarray(i+8,i+8+n);i+=8+n+(n%2);}assert(data&&format);assert.equal(format.readUInt16LE(0),1);assert.equal(format.readUInt16LE(2),1);assert.equal(format.readUInt32LE(4),48000);assert.equal(format.readUInt16LE(14),16);return data;}
const masterPCM=wav(await read(resolve(repo,master))),finalPCM=wav(await read('public/audio/review-narration.wav')),pickupPCM=wav(await read('public/audio/presenter-pickups.wav'));
assert.equal(finalPCM.length,2856000*2);assert(finalPCM.equals(masterPCM.subarray(0,2856000*2)),'final audio is not exact master excerpt');
assert(pickupPCM.equals(Buffer.concat([masterPCM.subarray(0,304000*2),masterPCM.subarray(1908000*2,2154000*2)])),'provider pickups differ from locked samples');
const html=await readFile(resolve(root,'index.html'),'utf8');
const clips=[...html.matchAll(/<(video|audio|div)\b([^>]+)>/g)].map(m=>({tag:m[1],...Object.fromEntries([...m[2].matchAll(/([\w-]+)="([^"]*)"/g)].map(x=>[x[1],x[2]]))})).filter(o=>o['data-track-index']);
const picture=clips.filter(o=>o['data-track-index']==='1').sort((a,b)=>+a['data-start']-+b['data-start']);
let cursor=0;const mediaCache={},timeline=[];
for(const c of picture){const start=+c['data-start'],duration=+c['data-duration'];assert(Math.abs(start-cursor)<1e-7,'picture gap or overlap at '+c.id);assert(Math.abs(start*24-Math.round(start*24))<1e-7);assert(Math.abs(duration*24-Math.round(duration*24))<1e-7);cursor=start+duration;
 if(c.tag==='video'){
 const src=c.src;mediaCache[src] ||=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',resolve(root,src)],{encoding:'utf8'}));const v=mediaCache[src].streams.find(s=>s.codec_type==='video');assert.equal(v.r_frame_rate,'24/1');assert(+c['data-media-start']+duration<=+v.duration+1e-6,'source beyond video '+c.id);
 if(src.endsWith('-browser.mp4')){assert.equal(v.pix_fmt,'yuv420p');assert.equal(mediaCache[src].streams.length,1);assert.equal(+v.nb_frames,src.includes('pickups')?275:273);}
 const tag=html.match(new RegExp('<video[^>]*id="'+c.id+'"[^>]*>'))[0];assert(/\bmuted\b/.test(tag),'unmuted film');
 }else{const sub=await readFile(resolve(root,c['data-composition-src']),'utf8');assert(sub.includes('<template>'));assert(sub.includes('data-composition-id="'+c['data-composition-id']+'"'));assert(sub.includes("window.__timelines['"+c['data-composition-id']+"']"));}
 timeline.push({id:c.id,frame_in:Math.round(start*24),frame_out:Math.round(cursor*24),source:c.src||c['data-composition-src'],source_in_seconds:c['data-media-start']?+c['data-media-start']:null});
}
assert.equal(cursor,59.5);assert.equal(clips.filter(c=>c.tag==='audio').length,1);
const assets=[];for(const dir of ['public/media','public/audio','public/fonts','public/vendor'])for(const name of await readdir(resolve(root,dir))){const path=dir+'/'+name,b=await read(path);assets.push({path,sha256:digest(b),bytes:b.length,...(mediaCache[path]?{streams:mediaCache[path].streams.map(({codec_type,codec_name,profile,pix_fmt,duration,nb_frames,r_frame_rate})=>({codec_type,codec_name,profile,pix_fmt,duration,nb_frames,r_frame_rate}))}:{})});}
const sources={'establishing.mp4':'../r6-character-first/public/media/shot-01.mp4','shot-b.mp4':'../r8-context-coverage/public/media/shot-b.mp4','shot-c.mp4':'../r8-context-coverage/public/media/shot-c.mp4','shot-d.mp4':'../r10-film-to-presenter/public/media/shot-d.mp4','shot-e.mp4':'../r10-film-to-presenter/public/media/shot-e.mp4'};
for(const [name,src]of Object.entries(sources))assert.equal(await sha('public/media/'+name),await sha(src));
const sourceFiles=['index.html','compositions/question.html','compositions/arithmetic.html','compositions/sting.html','compositions/title.html','BRIEF.md','frame.md','STORYBOARD.md'];
const authored=[];for(const path of sourceFiles)authored.push({path,sha256:await sha(path)});
const result={checked_at:new Date().toISOString(),ok:true,scope:'isolated assembled preview; not final rendered delivery',dimensions:[1280,720],fps:24,frames:1428,duration:59.5,checks:{source_pins:true,film_copies_identical:true,original_pcm_exact:true,pickup_pcm_exact:true,one_soundtrack_all_picture_muted:true,frame_aligned_gapless_picture:true,source_ranges_in_bounds:true,browser_derivatives_8bit_preserve_frame_counts:true,subcomposition_contract:true},authored,timeline,assets,provenance:{narration:master,narration_sha256:pins[0][1],retained_film_sources:sources,new_avatar:'Sync3 hosted-WAV recovery002; original result preserved',browser_derivatives:'ffmpeg -i input.mp4 -map 0:v:0 -an -c:v libx264 -preset fast -crf17 -pix_fmt yuv420p -movflags +faststart output-browser.mp4; no trim, fps change or retime',avatar_crop:'1280x724 top-anchored, clipped at1280x720; bottom-edge artifact removal',illustration:'new short independently authored SVG strokes; measured draw law adapted from installed Whiteboard Ink registry component'}};
await writeFile(resolve(root,'ASSET-AND-EDIT-MANIFEST.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({ok:result.ok,frames:1428,pictureClips:picture.length,assets:assets.length,pcm:'exact original',index_sha256:authored[0].sha256}));
