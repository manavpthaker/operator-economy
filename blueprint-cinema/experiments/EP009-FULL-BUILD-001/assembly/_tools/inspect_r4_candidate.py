#!/usr/bin/env python3
"""Inspect encoded candidate joins and preserve source comparison evidence."""
import json
import sys
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from PIL import Image, ImageDraw
from build_r3 import A, bound, read, verify_bound, write
from inspect_r3_frames import extract, W, H


def main():
    manifest=A/'r4/ep009-full-r4-opening-candidate-BUILD.json';d=read(manifest)
    if d['status']!='encoded_candidate_lipsync_unresolved' or d['scope']!='full':raise ValueError('Completed full candidate required')
    out=verify_bound({'path':d['output'],'sha256':d['output_sha256']})
    directory=A/'qa/r4/candidate-integration-frames'
    if directory.exists():raise FileExistsError('Preserve existing inspection')
    directory.mkdir()
    groups=[{'id':'opening-presenter','label':'Flagged opening candidate: sampled frames, no sync clearance','frames':[0,1,14,24,43,60,79,84,85]},
            {'id':'opening-film-joins','label':'Exact opening return and retained film joins','frames':[85,86,87,96,110,134,135,136,251,252]},
            {'id':'locked-brand','label':'Locked brand cut retained','frames':[1426,1427,1431,1436,1437,1438,1439,1442]},
            {'id':'locked-hospitality','label':'Locked narration and labeled P08 still retained','frames':[15919,15920,15926,16091,16262,16263]}]
    for selection in read(verify_bound(d['film_selections']))['selections']:
        spans=[s for s in d['source_spans'] if s.get('film_selection_id')==selection['id']]
        lo,hi=spans[0]['output_frames'][0],spans[-1]['output_frames'][1]
        groups.append({'id':selection['id'],'label':selection['label'],'frames':[lo-1,lo,(lo+hi)//2,hi-1,hi]})
    requested=sorted({f for g in groups for f in g['frames']});encoded=extract(out,requested)
    mappings={};by_source={}
    for f in requested:
        s=next(s for s in d['source_spans'] if s['output_frames'][0]<=f<s['output_frames'][1])
        sf=s['source_start_frame']+f-s['output_frames'][0]
        mappings[f]={'segment':s['segment_id'],'kind':s['kind'],'source':s['source'],'source_frame':sf,'candidate':s.get('candidate_id'),'film_selection':s.get('film_selection_id')}
        if s['kind']=='video':by_source.setdefault(s['source']['path'],{'bound':s['source'],'frames':set()})['frames'].add(sf)
    images={p:extract(verify_bound(v['bound']),v['frames']) for p,v in by_source.items()}
    lock=read(verify_bound(d['owner_scoped_lock']));stillframes=[f for f in requested if mappings[f]['kind']=='still']
    stillimages=extract(verify_bound(lock['hospitality_preview']),[f-15920+120 for f in stillframes])
    comparisons=[]
    for f,m in mappings.items():
        expected=images[m['source']['path']][m['source_frame']] if m['kind']=='video' else stillimages[f-15920+120]
        if m['kind']=='still':m['comparison_reference']={'accepted_context':lock['hospitality_preview'],'frame':f-15920+120}
        diff=np.abs(encoded[f].astype(float)-expected.astype(float))
        comparisons.append({'output_frame':f,'seconds':f/24,**m,'mean_abs_rgb_difference':float(diff.mean()),'fraction_pixels_mean_rgb_difference_above20':float((diff.mean(2)>20).mean())})
        Image.fromarray(encoded[f]).save(directory/f'frame-{f:05d}.png')
    sheets=[]
    for g in groups:
        cols=3 if len(g['frames'])<=9 else 4;rows=(len(g['frames'])+cols-1)//cols
        sheet=Image.new('RGB',(cols*W,rows*(H+35)+40),'#eeeeee');draw=ImageDraw.Draw(sheet);draw.text((12,10),g['label'],fill='black')
        for i,f in enumerate(g['frames']):
            x,y=(i%cols)*W,40+(i//cols)*(H+35);sheet.paste(Image.fromarray(encoded[f]),(x,y))
            draw.text((x+10,y+H+7),f'r4 frame {f} | {f/24:.6f}s | {mappings[f]["segment"]}',fill='black')
        p=directory/(g['id']+'.jpg');sheet.save(p,quality=94);sheets.append(bound(p))
    report={'record_type':'ep009_exact_P00_candidate_encoded_integration','build':bound(manifest),'output':bound(out),
        'method':'Exact decoded frame indices at opening and both retained film joins, six later film inserts, locked brand and corrected experience. Source frames follow bound BUILD. Static P08 compared with locked context. RGB at 640x360.',
        'frame_count':len(requested),'groups':groups,'sheets':sheets,'comparisons':comparisons,
        'maximum_mean_abs_rgb_difference':max(c['mean_abs_rgb_difference'] for c in comparisons),
        'maximum_fraction_pixels_mean_rgb_difference_above20':max(c['fraction_pixels_mean_rgb_difference_above20'] for c in comparisons),
        'sync_cleared':False,'owner_accepted':False,'limits':['Frame inspection verifies picture placement and sampled visual continuity, not normal-speed audiovisual perception or lip sync.','P00 diagnostic flags remain unresolved; index and bulk state are unchanged.']}
    write(directory/'FRAME-COMPARISON.json',report);print(json.dumps({'frames':len(requested),'sheets':len(sheets),'report':str(directory/'FRAME-COMPARISON.json')},indent=2))


if __name__=='__main__':main()
