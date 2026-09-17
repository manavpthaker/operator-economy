#!/usr/bin/env python3
"""Write the separate local candidate review page after both encoded checks pass."""
import json
from pathlib import Path
from build_r3 import A, bound, read, verify_bound, write

def main():
    full=A/'r4/ep009-full-r4-opening-candidate-BUILD.json'
    context=A/'r4/ep009-r4-opening-context-candidate-BUILD.json'
    evidence=[]
    for p in (full,context):
        v=p.with_name(p.name.replace('-BUILD.json','-VERIFICATION.json'));d=read(v)
        if d['build']!=bound(p) or d['status']!='technical_checks_passed_lipsync_unresolved_review_candidate':raise ValueError('Current candidate verification required')
        verify_bound(d['output']);evidence.append(bound(v))
    source=A/'qa/ep009-r3-review.html';target=A/'qa/ep009-r4-review.html'
    if target.exists():raise FileExistsError('Preserve existing r4 page')
    html=source.read_text().replace('EP009 · revision 3 review','EP009 · avatar-first opening review')
    html=html.replace('Revision 3 · 20:22 runtime','Revision 4 review candidate · 20:22 runtime')
    html=html.replace('Full revision 3 review draft. The shortened brand pause, corrected experience and new film selections are integrated.',
        'The avatar delivers the first sentence, then the opening returns to the inn footage. The locked brand pause and corrected experience are retained.')
    old='<div class="notice"><strong>Presenter production is unfinished.</strong> Fourteen presenter segments retain the r1 footage. The corrected hospitality paragraph uses the locked L3 still with a visible “corrected narration · presenter pending” label. These are review placeholders, not finished presenter delivery. Lip-sync restoration remains pending.</div>'
    new='<section><h2>Avatar-first opening · lip sync still under review</h2><video aria-label="10.5-second opening transition candidate" id="opening" controls preload="metadata" src="r4/ep009-r4-opening-context-candidate.mp4"></video><p class="muted">10.5 seconds · opening review candidate</p></section>\n<div class="notice"><strong>Presenter delivery remains under review.</strong> The opening avatar’s lip sync is unresolved. Fourteen other presenter sections retain r1 footage; the corrected experience uses a still labeled “corrected narration · presenter pending.”</div>\n<h2>Full episode · opening review candidate</h2>'
    if old not in html:raise ValueError('Source notice changed; review copy before publishing')
    html=html.replace(old,new).replace('aria-label="Full episode revision 3"','aria-label="Full episode revision 4 opening candidate"').replace('src="r3/ep009-full-r3-review-draft.mp4"','src="r4/ep009-full-r4-opening-candidate.mp4"')
    details='<details><summary>Opening review notes</summary><p>This candidate keeps the current lip-sync flag. The original take is mechanically intact and sampled mouth shapes are plausible, but those checks do not establish perceptual sync. The onset test had no qualifying samples; mouth-opening correlation was 0.343 against narration and 0.382 against the guide voice. This review artifact does not clear the presenter batch or final release.</p><p><a href="r4/CANDIDATE-QA.md">Candidate evidence and limits</a> · <a href="ep009-r3-review.html">Retained revision 3</a></p></details>\n'
    html=html.replace('<details><summary>All 75 mapped segment starts</summary>',details+'<details><summary>All 75 mapped segment starts</summary>')
    with target.open('x') as f:f.write(html)
    write(A/'r4/REVIEW-PAGE.json',{'record_type':'ep009_exact_P00_candidate_review_page','page':bound(target),'source_page':bound(source),
        'verification':evidence,'url':'http://localhost:3070/ep009-r4-review.html','sync_cleared':False,'owner_accepted':False,
        'method':'Generated from retained r3 page with unchanged locked preview sources and exact existing 75 cue/six film jumps; separately linked verified candidate context/full media.'})
    print(target)

if __name__=='__main__':main()
