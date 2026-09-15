// Read-only checks of source media and trial assembly. Writes only a generated local QA receipt.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const sum = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const probe = p => JSON.parse(execFileSync('ffprobe', ['-v','error','-show_streams','-show_format','-of','json',p], {encoding:'utf8'}));
const pins = {
  'SHOT-01-PROMPT.md': 'adcf675ad61b205a5bf6ca7711d9aa0c943a5b20988958f2c3493f717b9a3924',
  'SHOT-02-PROMPT.md': '81ecc234e2e2098f0914b81a70527e443a816e48411ad209211954d78b940bf5',
  'SHOT-03-PROMPT.md': '91aadfb17e615164b716ad228e363b320b5b1706049abb4cfe06a63c871a2f8a',
  'public/media/shot-01-start.png': '1d50aab4871153888039cadcbbd14602434b89d2ed190899483108da61879b96',
  'public/media/shot-02-start.png': '9338ba62ae205b63aa6a7613d1fa8b8bd1c7451a3c5849f82c63fc77d69e1875',
  'public/media/shot-03-start.png': '37780230b232285763334022a57c82b5aa1eaf711827f283ab17bd6abfa0357f',
  'public/media/shot-03-start-v2.png': '0ed81e07b12747f5b5ed39152e995030496e095556b61841b51455daab06d57a',
  'public/audio/opening-narration.wav': '120c7a64ae8582f55f9bb4338c9ec276d763d79d88718aac482fc81c48ddbfb1',
};
for (const [p,h] of Object.entries(pins)) assert.equal(sum(path.join(here,p)),h,p+' changed');
assert.equal(sum(path.resolve(here,'../r5-rough-question/index.html')), 'c7492a6874291acd934f5848d0749f9c88562c9728d5090d070a85a711d64c08', 'R5 changed');
const html = fs.readFileSync(path.join(here,'index.html'),'utf8');
const tags = [...html.matchAll(/<video\s([^>]+)>/g)].map(m => Object.fromEntries([...m[1].matchAll(/([\w-]+)="([^"]*)"/g)].map(x=>[x[1],x[2]])));
assert.equal(tags.length,3);
let cursor=0;
const shots=[];
for (const [i,t] of tags.entries()) {
  const n=String(i+1).padStart(2,'0');
  assert.equal(Number(t['data-start']),cursor);
  assert.equal(Number(t['data-media-start']),0);
  assert.equal(t['data-track-index'],'1');
  assert.equal(t['data-playback-rate'],undefined);
  const file=path.join(here,t.src), p=probe(file), video=p.streams.find(s=>s.codec_type==='video');
  assert.ok(video && p.streams.every(s=>s.codec_type!=='audio'));
  assert.ok(Number(video.duration)>=Number(t['data-duration']));
  assert.equal(video.r_frame_rate,'24/1');
  const original=path.join(here,`renders/candidates/shot-${n}.mp4`);
  const receipt=JSON.parse(fs.readFileSync(original+'.response.json','utf8'));
  assert.equal(sum(file),sum(original));
  assert.equal(sum(file),receipt.output.sha256);
  assert.equal(receipt.request.referenceSha256,pins[`public/media/shot-${n}-start${n==='03'?'-v2':''}.png`]);
  assert.equal(receipt.model,'fal-ai/kling-video/v3/pro/image-to-video');
  assert.equal(receipt.request.generateAudio,false);
  const text=fs.readFileSync(path.join(here,`SHOT-${n}-PROMPT.md`),'utf8');
  assert.ok(text.match(/## Prompt\s+([\s\S]*?)(?=\n## |$)/)[1].trim().length<=2500);
  shots.push({id:n,src:t.src,sha256:sum(file),requestId:receipt.requestId,record:[cursor,cursor+Number(t['data-duration'])],source:[0,Number(t['data-duration'])],probe:video});
  cursor+=Number(t['data-duration']);
}
assert.equal(cursor,44.5);
assert.ok(html.includes('data-duration="44.5"'));
assert.ok(!/<svg|<canvas|<img|data-composition-src|data-playback-rate/.test(html));
const ids=[...html.matchAll(/\sid="([^"]+)"/g)].map(m=>m[1]);
assert.equal(new Set(ids).size,ids.length);
const receipt={status:'mechanical-trial-check-passed',durationSeconds:cursor,frames:1068,fps:24,creativeApproval:false,productionGateAdvance:false,finalRender:false,pins,shots,indexSha256:sum(path.join(here,'index.html')),estimatedVideoListCostUsd:5.04,billingInvoiceVerified:false,limitations:['Frame sampling and media probes do not prove the intended performance or human comprehension.','Still-reference generation is separate from the video list-price estimate.','User approval and final render remain pending.']};
fs.writeFileSync(path.join(here,'renders/verification.json'),JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify({status:receipt.status,duration:cursor,shots:shots.map(s=>({id:s.id,hash:s.sha256,requestId:s.requestId})),creativeApproval:false,gateAdvance:false}));
