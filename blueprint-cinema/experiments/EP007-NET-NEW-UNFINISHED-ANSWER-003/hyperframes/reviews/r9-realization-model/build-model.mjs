// Build fixed native pencil assets. The historical geometry and compiler remain untouched.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const repo=path.resolve(here,'../../../../../..');
const source=path.join(repo,'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-001/hyperframes/compositions/sequences/03-model-exposure.html');
const pencil=path.join(repo,'blueprint-cinema/experiments/EP007-BL-MOTION-001/build-pencil-study.mjs');
const sum=x=>crypto.createHash('sha256').update(x).digest('hex');
const original=fs.readFileSync(source,'utf8');
assert.equal(sum(original),'0d1297cddaf0eb8b8fd87d9dec89198bbb6c0677a5c15b83efb7d3032ce54c39');
assert.equal(sum(fs.readFileSync(pencil)),'c592416ea034da1bff45594089483f8eb103d2a73bdea8099d96badfedc3c6b5');
const dir=path.join(here,'public/model');fs.mkdirSync(dir,{recursive:true});
const group=name=>original.match(new RegExp('<g[^>]*class="'+name+'"[^>]*>([\\s\\S]*?)</g>'))[1];
const tags=s=>[...s.matchAll(/<path\b[^>]*\/>/g)].map(m=>m[0]);
const attr=(s,n)=>s.match(new RegExp('(?:^|\\s)'+n+'="([^"]*)"'))?.[1];
const color={mineral:'#204440','mineral-deep':'#173530',steel:'#586d74',oxide:'#b5482f'};
const n=x=>(+x.toFixed(2)).toString();
const distance=(a,b)=>Math.hypot(b[0]-a[0],b[1]-a[1]);
function randomFor(s){let v=parseInt(sum(s).slice(0,8),16)||1;return()=>{v^=v<<13;v^=v>>>17;v^=v<<5;return(v>>>0)/4294967296;};}
function flatten(d){
 const t=d.match(/[a-zA-Z]|[-+]?(?:\d*\.)?\d+(?:e[-+]?\d+)?/g)||[];
 let i=0,c,p=[0,0],start,lastControl=null,paths=[],current;
 const point=()=>[Number(t[i++]),Number(t[i++])];const add=q=>{current.push(q);p=q;};
 while(i<t.length){
  if(/[a-zA-Z]/.test(t[i]))c=t[i++];
  if(c==='M'){p=point();start=p;current=[p];paths.push(current);c='L';lastControl=null;}
  else if(c==='L'){add(point());lastControl=null;}
  else if(c==='H'){add([Number(t[i++]),p[1]]);lastControl=null;}
  else if(c==='V'){add([p[0],Number(t[i++])]);lastControl=null;}
  else if(c==='C'||c==='S'){
   const a=p,b=c==='C'?point():(lastControl?[2*p[0]-lastControl[0],2*p[1]-lastControl[1]]:p),e=point(),f=point();
   const steps=Math.max(5,Math.ceil((distance(a,b)+distance(b,e)+distance(e,f))/5));
   for(let j=1;j<=steps;j++){const u=j/steps,v=1-u;add([v*v*v*a[0]+3*v*v*u*b[0]+3*v*u*u*e[0]+u*u*u*f[0],v*v*v*a[1]+3*v*v*u*b[1]+3*v*u*u*e[1]+u*u*u*f[1]]);}lastControl=e;
  }else if(c==='Z'){add(start);c=null;lastControl=null;}else throw Error('Unsupported SVG command '+c);
 }return paths;
}
function pointAt(points,lengths,s){
 s=Math.max(0,Math.min(lengths.at(-1),s));let i=1;while(i<lengths.length-1&&lengths[i]<s)i++;
 const f=(s-lengths[i-1])/(lengths[i]-lengths[i-1]||1),a=points[i-1],b=points[i];return[a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f];
}
let strokes=0,units=0;
function rough(tag,hatch=false){
 const d=attr(tag,'d'),cls=attr(tag,'class')||'',id=attr(tag,'data-hf-id')||String(++units);
 const tone=cls.includes('mineral-deep')?'mineral-deep':cls.includes('oxide')?'oxide':cls.includes('steel')?'steel':'mineral';
 const oldW=Number(attr(tag,'stroke-width')||({w1:2.1,w2:3.1,w3:4.4,w4:5.8}[cls.match(/w[1-4]/)?.[0]]||2.1));
 const opacity=Number(attr(tag,'opacity')||(cls.includes('faint')?.34:cls.includes('soft')?.58:.88));
 const rnd=randomFor(id+':'+d),weight=(hatch?1.2:Math.min(2.2,.7+oldW*.19))*(tone==='oxide'?1.3:1);
 const chunks=[];
 for(const points of flatten(d)){
  if(points.length<2)continue;const lengths=[0];for(let i=1;i<points.length;i++)lengths.push(lengths.at(-1)+distance(points[i-1],points[i]));
  const total=lengths.at(-1);let s=rnd()*1.8;
  while(s<total-.5){
   const e=Math.min(total,s+(hatch?total:13+rnd()*26)),passes=hatch?1:(rnd()<.48?3:2);
   for(let pass=0;pass<passes;pass++){
    if(pass===2&&rnd()<.25)continue;
    const a=Math.max(0,s+(pass?rnd()*6-3:0)),b=Math.min(total,e+(pass?rnd()*8-4:0));if(b-a<.7)continue;
    const jitter=hatch?.45:(pass?2.9:1.45),count=Math.max(1,Math.ceil((b-a)/9)),ox=(rnd()-.5)*jitter*2,oy=(rnd()-.5)*jitter*2,ps=[];
    for(let j=0;j<=count;j++){const p=pointAt(points,lengths,a+(b-a)*j/count);ps.push([p[0]+ox+(rnd()-.5)*jitter,p[1]+oy+(rnd()-.5)*jitter]);}
    const strokeD=ps.map((p,j)=>`${j?'L':'M'} ${n(p[0])} ${n(p[1])}`).join(' ');
    chunks.push(`<path d="${strokeD}" fill="none" stroke="${color[tone]}" stroke-width="${n(weight*(pass?.38+rnd()*.46:.64+rnd()*.65))}" opacity="${n(pass?.36+rnd()*.30:.72+rnd()*.26)}" stroke-linecap="round" stroke-linejoin="miter"/>`);strokes++;
   }
   s=e+(rnd()<.31?2.2+rnd()*5:-1.5+rnd()*2);
  }
 }return `<g data-pencil-unit="${id}" opacity="${opacity}">${chunks.join('')}</g>`;
}
const compiled=ts=>ts.map(t=>rough(t)).join('');
const ownerTags=tags(group('owner-figure'));
const benchIds=new Set(['hf-p0gh','hf-pxlm','hf-oide','hf-83ph','hf-mn0b']);
const hatch=tags(group('hatch-mark'));
const business=compiled(tags(group('seed-mark')+group('construction-mark')+group('business-contour')+group('business-structure')))+hatch.slice(0,8).map(t=>rough(t,true)).join('');
const owner=compiled(ownerTags.filter(t=>!benchIds.has(attr(t,'data-hf-id'))))+hatch.slice(8).map(t=>rough(t,true)).join('');
const bench=compiled(ownerTags.filter(t=>benchIds.has(attr(t,'data-hf-id'))));
const routes=compiled(tags(group('dependency-route')));
const ticket='<path d="M -36 -29 L 36 -32 L 39 27 L -38 30 Z" fill="#f5f0e6"/>'+rough('<path class="rough mineral w3 firm" d="M -37 -27 L 36 -32 M 39 -26 L 37 26 M 32 30 L -37 27 M -40 22 L -38 -23 M -24 -9 L 24 -11 M -23 4 L 18 2 M -21 15 L 10 13"/>');
const qPath='M1292 610 C1286 582 1306 563 1332 568 C1357 572 1366 593 1355 609 C1346 623 1328 627 1325 646 M1324 672 L1326 675';
const question=rough(`<path class="rough oxide w4 firm" d="${qPath}"/>`);
const labels='<g fill="#204440" font-family="Caveat" font-size="48" font-weight="700"><text x="397" y="305" text-anchor="middle" transform="rotate(-2 397 305)">pricing</text><text x="684" y="308" text-anchor="middle" transform="rotate(1 684 308)">work</text><text x="978" y="303" text-anchor="middle" transform="rotate(-1 978 303)">customers</text></g>';
const ownerLabel='<text x="1484" y="364" text-anchor="middle" fill="#204440" font-family="Caveat" font-size="48" font-weight="700" transform="rotate(-2 1484 364)">owner</text>';
const font=fs.readFileSync(path.join(here,'public/fonts/Caveat-700-latin.woff2')).toString('base64');
const svg=(body,defs='')=>`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><defs><style>@font-face{font-family:Caveat;src:url(data:font/woff2;base64,${font}) format('woff2');font-weight:700;}</style>${defs}</defs>${body}</svg>`;
const routeDefs='<clipPath id="r9-before-gap"><rect x="0" y="0" width="1220" height="1080"/></clipPath><clipPath id="r9-terminal"><rect x="1220" y="0" width="160" height="1080"/></clipPath>';
const layers={business:business+labels,owner:owner+ownerLabel,bench,'dependency-route':`<g clip-path="url(#r9-before-gap)">${routes}</g>`,'terminal-connection':`<g clip-path="url(#r9-terminal)">${routes}</g>`,'work-ticket':ticket,'decision-question':question};
for(const[id,body]of Object.entries(layers))fs.writeFileSync(path.join(dir,id+'.svg'),svg(body,routeDefs));
const finalBody=`<rect width="1920" height="1080" fill="#f5f0e6"/>${business}${labels}${bench}<g transform="translate(100 0)" opacity=".18">${owner}${ownerLabel}</g><g clip-path="url(#r9-before-gap)">${routes}</g><g transform="translate(1187 683)">${ticket}</g>${question}`;
const still=path.join(dir,'owner-dependency-reference.svg');fs.writeFileSync(still,svg(finalBody,routeDefs));
const composition=`<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"></head><body><template>
<style>
@font-face{font-family:Caveat;src:url(public/fonts/Caveat-700-latin.woff2) format('woff2');font-weight:700;}
#root{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;background:#f5f0e6;}
.working-model{position:absolute;inset:0;width:1920px;height:1080px;}
</style>
<div id="root" data-composition-id="ep007-r9-owner-dependency" data-start="0" data-duration="9.416666666666668" data-width="1920" data-height="1080">
<svg class="working-model" viewBox="0 0 1920 1080" role="img" aria-label="Pricing, daily work and customer relationships connect back to the owner. In the month-away thought experiment, a work request reaches an unanswered handoff while the business remains intact.">
<defs>${routeDefs}<clipPath id="r9-route-reveal"><rect id="r9-route-window" x="210" y="0" width="1180" height="1080"/></clipPath><mask id="r9-question-reveal" maskUnits="userSpaceOnUse" x="1250" y="540" width="145" height="155" style="mask-type:alpha"><path id="r9-question-pen" d="${qPath}" fill="none" stroke="white" stroke-width="20" stroke-linecap="round"/></mask></defs>
<g id="r9-business">${business}${labels}</g>
<g id="r9-bench">${bench}</g>
<g id="r9-owner">${owner}${ownerLabel}</g>
<g clip-path="url(#r9-route-reveal)"><g id="r9-existing-route" clip-path="url(#r9-before-gap)">${routes}</g><g id="r9-terminal-connection" clip-path="url(#r9-terminal)">${routes}</g></g>
<g transform="translate(687 615)"><g id="r9-work-ticket">${ticket}</g></g>
<g id="r9-question" mask="url(#r9-question-reveal)">${question}</g>
</svg></div>
<script>
window.__timelines=window.__timelines||{};
const root=document.querySelector('[data-composition-id="ep007-r9-owner-dependency"]');
const find=s=>root.querySelector(s),tl=gsap.timeline({paused:true});
const pen=find('#r9-question-pen'),length=pen.getTotalLength();
gsap.set('#r9-route-window',{attr:{width:0}});
gsap.set('#r9-work-ticket',{opacity:0,x:0,y:0});
gsap.set('#r9-question-pen',{strokeDasharray:length,strokeDashoffset:length});
tl.fromTo('#r9-route-window',{attr:{width:0}},{attr:{width:1180},duration:1.4,ease:'none'},.35);
tl.fromTo('#r9-owner',{x:0,opacity:1},{x:100,opacity:.18,duration:.75,ease:'power2.inOut'},3.05);
tl.fromTo('#r9-terminal-connection',{opacity:1},{opacity:0,duration:.35,ease:'none'},3.4);
tl.fromTo('#r9-work-ticket',{opacity:0},{opacity:1,duration:.15,ease:'none'},3.75);
tl.fromTo('#r9-work-ticket',{x:0,y:0},{x:243,y:21,duration:.55,ease:'none'},3.9);
tl.to('#r9-work-ticket',{x:500,y:68,duration:.8,ease:'power2.out'},4.45);
tl.fromTo('#r9-question-pen',{strokeDashoffset:length},{strokeDashoffset:0,duration:.7,ease:'none'},5.15);
window.__timelines['ep007-r9-owner-dependency']=tl;
</script></template></body></html>`;
fs.writeFileSync(path.join(here,'compositions/owner-dependency.html'),composition);
const core=path.join(repo,'design-system/boundary-ledger/semantic-core.json');
const asset=file=>({path:'public/model/'+file,mediaType:'image/svg+xml',width:1920,height:1080,sha256:sum(fs.readFileSync(path.join(dir,file)))});
const manifest={
 $schema:path.relative(here,path.join(repo,'design-system/boundary-ledger/motion-ready-asset.schema.json')),
 schemaVersion:'1.0',id:'ep007-r9-owner-dependency',semanticCore:{path:path.relative(here,core),version:'2.0.0',sha256:sum(fs.readFileSync(core))},
 sourceStill:{path:'public/model/owner-dependency-reference.svg',sha256:sum(fs.readFileSync(still)),preservedUnchanged:true},
 format:{aspectRatio:'16:9',width:1920,height:1080,adaptation:'authored-recomposition'},
 persistentObjects:[{id:'business',role:'Three ordinary business functions remain present, not verified case evidence',layerIds:['business']},{id:'owner',role:'Same illustrative actor moves aside in the hypothetical month away',layerIds:['owner']},{id:'bench',role:'Stable operating surface stays when owner is absent',layerIds:['bench']},{id:'work-ticket',role:'One request travels and remains waiting before the unanswered endpoint',layerIds:['work-ticket']},{id:'decision',role:'One active question, not a verified failure or solution',layerIds:['decision-question']}],
 layers:Object.keys(layers).map(id=>({id,semanticRole:id,asset:asset(id+'.svg'),authoredRoughness:true})),
 routes:[{id:'current-owner-dependency',semanticRole:'existing dependency; unanswered handoff when owner unavailable',from:'business',to:'owner',strokeLayerIds:['dependency-route','terminal-connection']},{id:'active-decision',semanticRole:'one oxide unanswered ownership decision at the same endpoint',from:'work-ticket',to:'decision',strokeLayerIds:['decision-question']}],
 evidenceAnchors:[],review:{objectPermanence:true,roughnessAuthored:true,cropBased:false,reviewerRole:'director-implementer; owner preview pending'}
};
fs.writeFileSync(path.join(here,'motion-ready-asset.json'),JSON.stringify(manifest,null,2)+'\n');
fs.writeFileSync(path.join(here,'pencil-build.json'),JSON.stringify({status:'compiled-preview-pending',source:path.relative(repo,source),sourceSha256:sum(original),compilerReference:path.relative(repo,pencil),compilerReferenceSha256:sum(fs.readFileSync(pencil)),sourceStill:manifest.sourceStill,visibleFragments:strokes,authoredRoughness:true,runtimeRandomness:false,sourceHistoricalFilesUnchanged:true,creativeApproval:false,claim:'Illustrative dependency question only; no factual business failure asserted'},null,2)+'\n');
console.log(JSON.stringify({strokes,compositionBytes:composition.length,sourceSha256:sum(original),output:here}));
