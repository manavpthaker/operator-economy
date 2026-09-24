import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

// Compile a fixed pencil drawing. No random/wobble/filter runs in the player.
// Existing timeline code is copied byte-for-byte; its paths only reveal masks.
const here = path.dirname(fileURLToPath(import.meta.url));
const source = path.join(here, 'hyperframes');
const output = path.join(here, 'pencil-study');
const figureFile = path.resolve(here, '../../episodes/EP007-exit-readiness-prep/agents/deliverables/pencil-figures-001/pencil-figure-geometry.json');
const expected = '0282f63fd9a14c0095c444af53adc2aaf2121464a7fb4e26dff92c27b2bcbe9d';
const sha = x => crypto.createHash('sha256').update(x).digest('hex');
const baseline = fs.readFileSync(path.join(source, 'index.html'), 'utf8');
if (sha(baseline) !== expected) throw new Error('Baseline changed; review and repin before rebuilding.');
const figures = JSON.parse(fs.readFileSync(figureFile, 'utf8'));
const replacements = {
  ...figures.replacements,
  // Deliberately unequal corners and sides; outline gaps are actual missing marks.
  'hf-f6hf': 'M -2 13 L 87 9 L 178 8 L 280 1 M 284 7 L 282 39 L 288 70 M 280 83 L 186 81 L 84 89 L 9 85 M 4 79 L 0 52 L 3 24',
  'hf-io9r': 'M -3 13 L 96 5 L 183 8 L 278 0 M 281 10 L 288 44 L 284 70 M 280 87 L 186 91 L 93 86 L 8 92 M 2 78 L 5 51 L 1 23',
  'hf-inse': 'M 1 9 L 88 3 L 183 6 L 284 2 M 291 15 L 286 44 L 291 74 M 281 80 L 194 84 L 105 91 L 14 85 M 3 77 L -1 47 L 3 23',
  'hf-favb': 'M -2 15 L 74 8 L 181 10 L 279 1 M 285 10 L 282 37 L 293 68 M 286 81 L 191 87 L 97 84 L 9 93 M 2 79 L 4 49 L -1 26',
  'hf-jcw1': 'M -2 13 L 107 7 L 216 10 L 327 1 M 331 14 L 328 153 L 334 301 L 330 447 M 323 463 L 222 458 L 107 470 L 10 465 M 3 450 L 6 319 L -2 178 L 2 30',
  'hf-oaxp': 'M 1 14 L 123 5 L 260 9 L 389 0 M 395 17 L 390 152 L 399 298 L 396 448 M 387 462 L 261 467 L 128 460 L 12 471 M 3 450 L 6 313 L -2 170 L 2 30',
  'hf-jodq': 'M -1 14 L 111 6 L 245 9 L 373 0 M 379 13 L 378 82 L 387 177 M 372 190 L 238 185 L 129 198 L 12 192 M 4 177 L -2 100 L 2 31',
  'hf-14uq': 'M -2 65 L 79 60 L 168 64 M 174 57 L 204 17 L 308 23 L 404 17 L 507 22 M 510 34 L 504 163 L 509 306 L 503 445 L 510 563 M 497 570 L 372 564 L 250 571 L 124 562 L 1 568 M -4 550 L 3 426 L -3 289 L 2 160 L -2 76'
};
const fills = {
  'hf-yzb9': 'M 2 12 L 327 4 L 332 448 L 323 465 L 10 467 L 0 28 Z',
  'hf-k82r': 'M 1 12 L 390 3 L 397 448 L 387 463 L 11 468 L 0 27 Z',
  'hf-7zcg': 'M 1 13 L 374 3 L 384 178 L 371 192 L 12 195 L 0 28 Z'
};
const hatches = [...figures.hatches,
  {parentSelector:'#pricing-part',d:'M 6 18 L 21 5 M 7 25 L 31 5 M 8 33 L 31 13 M 15 7 L 27 23 M 7 15 L 20 30',tone:'mineral',width:1.3,opacity:.6},
  {parentSelector:'#process-part',d:'M 263 11 L 282 29 M 264 20 L 285 40 M 269 34 L 287 51 M 272 12 L 263 26 M 282 28 L 269 43',tone:'mineral',width:1.35,opacity:.59},
  {parentSelector:'#customer-part',d:'M 7 62 L 25 80 M 7 70 L 21 86 M 14 58 L 31 76 M 9 82 L 25 66 M 17 87 L 31 74',tone:'mineral',width:1.4,opacity:.61},
  {parentSelector:'#key-part',d:'M 263 57 L 282 75 M 259 64 L 275 80 M 263 80 L 281 63 M 274 82 L 288 69',tone:'steel-dark',width:1.5,opacity:.61},
  {parentSelector:'#checklist-card',d:'M 8 26 L 30 6 M 9 34 L 38 9 M 9 43 L 30 23 M 15 11 L 32 28 M 10 23 L 23 37 M 306 450 L 327 426 M 310 458 L 329 438 M 312 433 L 329 450',tone:'mineral',width:1.4,opacity:.58},
  {parentSelector:'#records-card',d:'M 367 12 L 392 36 M 360 14 L 391 45 M 375 9 L 393 26 M 367 32 L 385 15 M 377 42 L 394 25 M 7 442 L 26 462 M 7 451 L 19 465 M 9 461 L 28 443',tone:'mineral',width:1.4,opacity:.58},
  {parentSelector:'#written-process',d:'M 8 28 L 27 8 M 9 38 L 34 13 M 15 14 L 29 29 M 9 25 L 21 37 M 360 177 L 379 158 M 367 181 L 382 167 M 364 164 L 378 178',tone:'mineral',width:1.4,opacity:.58},
  {parentSelector:'#package',d:'M 180 55 L 209 28 M 190 56 L 219 27 M 201 54 L 230 29 M 213 51 L 239 28 M 223 50 L 246 29 M 194 30 L 213 51 M 205 25 L 231 50 M 219 27 L 241 46 M 232 27 L 248 43',tone:'mineral',width:1.7,opacity:.69}
];
let html = baseline;
for (const h of hatches) {
  const attr = h.parentSelector.startsWith('#') ? `id="${h.parentSelector.slice(1)}"` : h.parentSelector.slice(1,-1);
  const i = html.indexOf(attr);
  if (i < 0) throw new Error(`Missing hatch parent: ${h.parentSelector}`);
  let end = html.indexOf('>',i)+1;
  // Paper fills must be below the graphite. Figure hatches remain below contours.
  if (/^\s*<path[^>]*class="record-fill"/.test(html.slice(end))) end=html.indexOf('/>',end)+2;
  const mark = `<path class="rough rough-${h.tone}" data-pencil-hatch="" stroke-width="${h.width}" opacity="${h.opacity}" d="${h.d}" />`;
  html = html.slice(0,end)+mark+html.slice(end);
}

function randomFor(s) {
  let n = parseInt(sha(s).slice(0,8),16) || 1;
  return () => {n ^= n<<13; n ^= n>>>17; n ^= n<<5; return (n>>>0)/4294967296;};
}
const num = n => (+n.toFixed(2)).toString();
const distance = (a,b) => Math.hypot(b[0]-a[0],b[1]-a[1]);
function flatten(d) {
  const t = d.match(/[a-zA-Z]|[-+]?(?:\d*\.)?\d+(?:e[-+]?\d+)?/g) || [];
  let i=0, c, p=[0,0], start, lastControl=null, paths=[], current;
  const point = () => [Number(t[i++]), Number(t[i++])];
  const add = q => {current.push(q); p=q;};
  while(i<t.length) {
    if(/[a-zA-Z]/.test(t[i])) c=t[i++];
    if(c==='M') {p=point(); start=p; current=[p]; paths.push(current); c='L'; lastControl=null;}
    else if(c==='L') {add(point()); lastControl=null;}
    else if(c==='H') {add([Number(t[i++]),p[1]]);lastControl=null;}
    else if(c==='V') {add([p[0],Number(t[i++])]);lastControl=null;}
    else if(c==='C'||c==='S') {
      const a=p, b=c==='C'?point():(lastControl?[2*p[0]-lastControl[0],2*p[1]-lastControl[1]]:p), e=point(), f=point();
      const steps=Math.max(5,Math.ceil((distance(a,b)+distance(b,e)+distance(e,f))/5));
      for(let j=1;j<=steps;j++){const u=j/steps,v=1-u;add([v*v*v*a[0]+3*v*v*u*b[0]+3*v*u*u*e[0]+u*u*u*f[0],v*v*v*a[1]+3*v*v*u*b[1]+3*v*u*u*e[1]+u*u*u*f[1]]);}
      lastControl=e;
    } else if(c==='Z') {add(start);c=null;lastControl=null;}
    else throw new Error(`Unsupported SVG command ${c}`);
  }
  return paths;
}
function pointAt(points,lengths,s) {
  const total=lengths.at(-1);s=Math.max(0,Math.min(total,s));
  let i=1;while(i<lengths.length-1&&lengths[i]<s)i++;
  const f=(s-lengths[i-1])/(lengths[i]-lengths[i-1]||1),a=points[i-1],b=points[i];
  return [a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f];
}
let sourcePaths=0, visibleStrokes=0, revealMasks=0;
html=html.replace(/<path\b[^>]*\/>/g, tag=>{
  const attr = name => tag.match(new RegExp(`(?:^|\\s)${name}="([^"]*)"`))?.[1];
  const hf=attr('data-hf-id'),id=attr('id'),d=replacements[hf]||attr('d');
  if(fills[hf]) return tag.replace(/ d="[^"]*"/,` d="${fills[hf]}"`);
  const cls=attr('class')||'';
  if(!cls.split(' ').includes('rough')&&!cls.includes('construction')) return tag;
  sourcePaths++;
  const construction=cls==='construction',hatch=tag.includes('data-pencil-hatch');
  const rnd=randomFor(`${hf||sourcePaths}:${d}`), tone=cls.match(/rough-([a-z-]+)/)?.[1]||'construction';
  const oldWidth=Number(attr('stroke-width')||3), originalOpacity=Number(attr('opacity')||1);
  const weight=(hatch?oldWidth:(construction?.78:Math.min(2.65,.93+oldWidth*.2)))*(tone==='oxide'?1.35:1);
  const chunks=[];
  for(const points of flatten(d)) {
    if(points.length<2)continue;
    const lengths=[0];for(let i=1;i<points.length;i++)lengths.push(lengths.at(-1)+distance(points[i-1],points[i]));
    const total=lengths.at(-1);let s=rnd()*1.8;
    while(s<total-.5) {
      const len=hatch?total:(construction?24+rnd()*28:13+rnd()*26);
      const e=Math.min(total,s+len),passes=hatch?1:(construction?1:(rnd()<.48?3:2));
      for(let pass=0;pass<passes;pass++) {
        if(pass===2&&rnd()<.25)continue;
        let a=Math.max(0,s+(pass?rnd()*6-3:0)),b=Math.min(total,e+(pass?rnd()*8-4:0));
        if(b-a<.7)continue;
        const jitter=hatch?.45:construction?.7:(pass?2.9:1.45);
        const count=Math.max(1,Math.ceil((b-a)/9)),offsetX=(rnd()-.5)*jitter*2,offsetY=(rnd()-.5)*jitter*2;
        const ps=[];
        for(let j=0;j<=count;j++){const p=pointAt(points,lengths,a+(b-a)*j/count);ps.push([p[0]+offsetX+(rnd()-.5)*jitter,p[1]+offsetY+(rnd()-.5)*jitter]);}
        const strokeD=ps.map((p,j)=>`${j?'L':'M'} ${num(p[0])} ${num(p[1])}`).join(' ');
        const width=weight*(pass?.38+rnd()*.46:.64+rnd()*.65),opacity=hatch?originalOpacity:(pass?.36+rnd()*.30:.72+rnd()*.26);
        const color=construction?'var(--rule-strong)':`var(--${tone})`;
        chunks.push(`<path d="${strokeD}" fill="none" stroke="${color}" stroke-width="${num(width)}" opacity="${num(opacity)}" stroke-linecap="round" stroke-linejoin="miter"/>`);visibleStrokes++;
      }
      // Real gaps and uneven retracing, not a dashed stroke or a contour filter.
      s=e+(rnd()<.31?2.2+rnd()*5:-1.5+rnd()*2);
    }
  }
  const unitOpacity=construction?.30:(hatch?1:originalOpacity);
  if(tag.includes('data-draw')) {
    revealMasks++;
    const mask=`pencil-reveal-${sourcePaths}`;
    const points=flatten(d).flat(),xs=points.map(p=>p[0]),ys=points.map(p=>p[1]);
    const minX=Math.min(...xs)-24,minY=Math.min(...ys)-24;
    const maskWidth=Math.max(...xs)-minX+24,maskHeight=Math.max(...ys)-minY+24;
    // Keep one original timed path per semantic mark. Its exact ID/duration/stagger
    // is unchanged. The white path is never drawn as visible artwork.
    const maskPath=tag.replace(/ class="[^"]*"/,'').replace(/ stroke-width="[^"]*"/,'').replace(/ opacity="[^"]*"/,'').replace(' />','/>').replace('/>', ' fill="none" stroke="white" stroke-width="28" stroke-linecap="butt"/>');
    return `<g data-pencil-unit="${id||hf}" opacity="${unitOpacity}"><defs><mask id="${mask}" maskUnits="userSpaceOnUse" x="${num(minX)}" y="${num(minY)}" width="${num(maskWidth)}" height="${num(maskHeight)}" style="mask-type:alpha">${maskPath}</mask></defs><g mask="url(#${mask})">${chunks.join('')}</g></g>`;
  }
  return `<g ${id?`id="${id}" `:''}${hf?`data-hf-id="${hf}" `:''}data-pencil-unit="${hf||sourcePaths}" opacity="${unitOpacity}">${chunks.join('')}</g>`;
});
const script = s => s.slice(s.indexOf('<script>'),s.indexOf('</script>',s.indexOf('<script>'))+9);
if(script(html)!==script(baseline))throw new Error('Timeline must remain byte-identical.');
fs.mkdirSync(output,{recursive:true});
for(const name of ['assets','.media']) {
  const target=path.join(output,name);
  if(!fs.existsSync(target))fs.cpSync(path.join(source,name),target,{recursive:true});
}
for(const name of ['package.json','hyperframes.json','hyperframes.lock.json','meta.json','index.motion.json','frame.md','BRIEF.md','STORYBOARD.md','ledger.json','scene-manifest.json','AGENTS.md']) {
  fs.copyFileSync(path.join(source,name),path.join(output,name));
}
fs.writeFileSync(path.join(output,'index.html'),html);
fs.writeFileSync(path.join(output,'pencil-build.json'),JSON.stringify({
  status:'render_pending', purpose:'Internal A/B linework study; not production approval',
  source_sha256:expected, output_sha256:sha(html),figure_proposal_sha256:sha(fs.readFileSync(figureFile)),
  timeline_byte_identical:script(html)===script(baseline),source_paths:sourcePaths,visible_pencil_strokes:visibleStrokes,reveal_masks:revealMasks,
  changes:['Fixed short overlapping pencil strokes','Unequal broken silhouettes','Sparse cross-hatching','Skewed document edges'],
  unchanged:['Palette','Typography','Words','Object identity','Outer transforms','28-second timing','Audio','Semantic labels']
},null,2)+'\n');
console.log(JSON.stringify({output,sourcePaths,visibleStrokes,revealMasks,htmlBytes:html.length,timelineUnchanged:true},null,2));
