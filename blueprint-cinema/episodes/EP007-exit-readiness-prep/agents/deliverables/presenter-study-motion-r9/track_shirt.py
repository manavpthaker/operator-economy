"""Direct-to-reference shirt patch matching. Outputs stay beside this script."""
from pathlib import Path
import hashlib, itertools, json, math, subprocess, time
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
EXP=Path('/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-PRESENTER-001')
SOURCE=EXP/'media/repair-r7/test-g-full-scope-avatar-iii-1080p.mp4'
REF=EXP/'media/repair-r8/study-shoulder-extension-reference.png'
INDEX=EXP/'study-composite-r8/index.html'
EXPECTED='6bfc0bd9190448e4a41d7ea694797ee48135d6ece85467a90bfb3e11926c749f'
PATCHES=[('left_upper',36,800,100,112),('left_lower',40,906,120,84),('right_upper',474,812,96,116),('right_lower',452,920,116,72)]
PIVOT=np.array([304.,950.])
REFERENCE_FRAME=10
RADIUS=18 # 36 full-resolution pixels
DOWN_RADIUS=36 # One correction: allow 72px downward motion; lower patches moved up.

def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def window_sum(a,h,w):
    ii=np.pad(a.cumsum(0).cumsum(1),((1,0),(1,0)))
    return ii[h:,w:]-ii[:-h,w:]-ii[h:,:-w]+ii[:-h,:-w]

def match(search,template):
    h,w=template.shape
    t=template-template.mean()
    shape=(search.shape[0]+h-1,search.shape[1]+w-1)
    corr=np.fft.irfft2(np.fft.rfft2(search,s=shape)*np.fft.rfft2(t[::-1,::-1],s=shape),s=shape)
    corr=corr[h-1:search.shape[0],w-1:search.shape[1]]
    variance=np.maximum(window_sum(search*search,h,w)-window_sum(search,h,w)**2/(h*w),1e-9)
    score=corr/np.sqrt(variance*np.sum(t*t))
    y,x=np.unravel_index(np.argmax(score),score.shape)
    peak=float(score[y,x]);other=score.copy()
    other[max(0,y-4):y+5,max(0,x-4):x+5]=-1
    gap=peak-float(other.max())
    def parabola(v0,v1,v2):
        den=v0-2*v1+v2
        return float(np.clip(0.5*(v0-v2)/den,-.5,.5)) if den < -1e-9 else 0.
    dx=parabola(score[y,x-1],peak,score[y,x+1]) if 0<x<score.shape[1]-1 else 0.
    dy=parabola(score[y-1,x],peak,score[y+1,x]) if 0<y<score.shape[0]-1 else 0.
    return x+dx-RADIUS,y+dy-RADIUS,peak,gap,x in (0,2*RADIUS) or y in (0,RADIUS+DOWN_RADIUS)

def similarity(p,q,weights):
    weights=np.asarray(weights,float);weights=weights/weights.sum()
    pc=(p*weights[:,None]).sum(0);qc=(q*weights[:,None]).sum(0)
    pp=p-pc;qq=q-qc
    den=(weights*np.sum(pp*pp,axis=1)).sum()
    a=(weights*np.sum(pp*qq,axis=1)).sum()/den
    b=(weights*(pp[:,0]*qq[:,1]-pp[:,1]*qq[:,0])).sum()/den
    matrix=np.array([[a,-b],[b,a]])
    translate=qc-matrix@pc
    residual=np.sqrt(np.sum((p@matrix.T+translate-q)**2,axis=1))
    move=matrix@PIVOT+translate-PIVOT
    return matrix,translate,residual,np.array([move[0],move[1],math.degrees(math.atan2(b,a)),math.hypot(a,b)])

def fit(points,observations,weights):
    best=None
    for pair in itertools.combinations(range(4),2):
        if np.linalg.norm(points[pair[0]]-points[pair[1]])<250: continue
        m,t,_,_=similarity(points[list(pair)],observations[list(pair)],weights[list(pair)])
        residual=np.linalg.norm(points@m.T+t-observations,axis=1)
        loss=float(np.sum(weights*np.minimum(residual,8)**2))
        if best is None or loss<best[0]: best=(loss,residual)
    inliers=best[1]<5
    if sum(inliers)>=2:
        m,t,r,values=similarity(points[inliers],observations[inliers],weights[inliers])
        residual=np.linalg.norm(points@m.T+t-observations,axis=1)
    else:
        m,t,residual,values=similarity(points,observations,weights)
    return values,residual,inliers

started=time.time()
assert sha(SOURCE)==EXPECTED
assert sha(REF)=='2514fbe72d35436cca84468efe8bd5a97080aab41fc081ba39c79bf794713149'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(SOURCE)]))['streams'][0]
assert probe['nb_frames']=='765' and probe['r_frame_rate']=='25/1'
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(SOURCE),'-vf','crop=608:1080:656:0,scale=304:540:flags=area','-an','-pix_fmt','gray','-f','rawvideo','-'])
frames=np.frombuffer(raw,np.uint8).reshape(765,540,304)
reference=frames[REFERENCE_FRAME].astype(float)
points=np.array([[x+w/2,y+h/2] for _,x,y,w,h in PATCHES])
templates=[]
for name,x,y,w,h in PATCHES:
    x,y,w,h=x//2,y//2,w//2,h//2
    templates.append(reference[y:y+h,x:x+w])

records=[]
for n,frame in enumerate(frames):
    observed=[];weights=[];patch_records=[]
    for (name,x,y,w,h),template in zip(PATCHES,templates):
        xx,yy,ww,hh=x//2,y//2,w//2,h//2
        search=frame[yy-RADIUS:yy+hh+DOWN_RADIUS,xx-RADIUS:xx+ww+RADIUS].astype(float)
        dx,dy,ncc,gap,boundary=match(search,template)
        if n==REFERENCE_FRAME: dx=dy=0.
        observed.append([x+w/2+dx*2,y+h/2+dy*2])
        weights.append(max(.01,ncc)**4)
        patch_records.append({'id':name,'dx':dx*2,'dy':dy*2,'ncc':ncc,'peak_gap':gap,'search_boundary':bool(boundary)})
    values,residual,inliers=fit(points,np.array(observed),np.array(weights))
    for p,r,good in zip(patch_records,residual,inliers): p.update(residual_px=float(r),fit_inlier=bool(good))
    reliable=sum(p['fit_inlier'] and p['ncc']>=.72 and p['peak_gap']>=.015 and not p['search_boundary'] for p in patch_records)>=3
    records.append({'frame':n,'time_seconds':n/25,'raw':values.tolist(),'reliable':reliable,'patches':patch_records,'fit_rms_px':float(np.sqrt(np.mean(residual[inliers]**2))) if sum(inliers) else None})
    if n%100==0: print('tracked',n,'elapsed',round(time.time()-started,1),flush=True)

values=np.array([r['raw'] for r in records]);good=np.array([r['reliable'] for r in records]);good[10]=True
# Reject isolated implausible registration jumps; do not clip motion into plausible values.
local_median=np.array([np.median(values[max(0,i-2):i+3],axis=0) for i in range(765)])
outliers=(np.max(np.abs(values[:,:2]-local_median[:,:2]),axis=1)>5)|(np.abs(values[:,2]-local_median[:,2])>.8)|(np.abs(values[:,3]-local_median[:,3])>.015)
good &= ~outliers;good[10]=True
raw_valid=values[good]
gaps=[];run=0
for flag in good:
    if flag:
        if run:gaps.append(run)
        run=0
    else:run+=1
if run:gaps.append(run)
reliable_fraction=float(good.mean())
longest_gap=max(gaps,default=0)
within_bounds=bool(np.max(np.abs(raw_valid[:,0]))<=36 and np.max(np.abs(raw_valid[:,1]))<=64 and np.max(np.abs(raw_valid[:,2]))<=4 and raw_valid[:,3].min()>=.94 and raw_valid[:,3].max()<=1.06)
accepted=reliable_fraction>=.85 and longest_gap<=12 and within_bounds

# Candidate smoothing is only released when the observations satisfy the acceptance thresholds.
smoothed=None
if accepted:
    ix=np.arange(765);known=ix[good]
    filled=np.column_stack([np.interp(ix,known,values[good,j]) for j in range(4)])
    kernel=np.exp(-.5*(np.arange(-4,5)/2.)**2);kernel/=kernel.sum()
    smoothed=np.column_stack([np.convolve(np.pad(filled[:,j],(4,4),mode='edge'),kernel,mode='valid') for j in range(4)])
    # Compose T(t) with inverse T(reference), including translation under rotation/scale.
    base=smoothed[10].copy()
    for row in smoothed:
        angle=math.radians(row[2]-base[2]);scale=row[3]/base[3]
        rotated_base=scale*np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])@base[:2]
        row[:2]-=rotated_base;row[2]=math.degrees(angle);row[3]=scale
    smoothed[10]=[0.,0.,0.,1.]

metrics={
    'runtime_seconds':time.time()-started,'reliable_fraction':reliable_fraction,'longest_unreliable_gap_frames':longest_gap,
    'isolated_outlier_frames':np.flatnonzero(outliers).tolist(),'within_bounds':within_bounds,'accepted_for_review':accepted,
    'patch_ncc_median':{name:float(np.median([r['patches'][i]['ncc'] for r in records])) for i,(name,*_) in enumerate(PATCHES)},
    'patch_reliable_fraction':{name:float(np.mean([p['ncc']>=.72 and p['peak_gap']>=.015 and not p['search_boundary'] for p in [r['patches'][i] for r in records]])) for i,(name,*_) in enumerate(PATCHES)},
    'raw_ranges':dict(zip(['dx_px','dy_px','rotation_deg','scale'],[[float(v.min()),float(v.max())] for v in values.T])),
    'valid_ranges':dict(zip(['dx_px','dy_px','rotation_deg','scale'],[[float(v.min()),float(v.max())] for v in raw_valid.T])),
    'fit_rms_px_median':float(np.median([r['fit_rms_px'] for r in records if r['fit_rms_px'] is not None])),
    'thresholds':{'ncc':.72,'peak_gap':.015,'fit_inliers_required':3,'residual_px':5,'valid_fraction':.85,'max_unreliable_gap_frames':12,'translation_x_abs_max_px':36,'translation_y_abs_max_px':64,'rotation_abs_max_deg':4,'scale_min':.94,'scale_max':1.06}
}
output={'status':'candidate_motion_for_review' if accepted else 'tracking_unreliable_do_not_apply',
 'inputs':[{'path':str(p),'sha256':sha(p)} for p in [SOURCE,REF,INDEX]],
 'method':'Four shirt-only patches; half-resolution zero-mean normalized cross correlation by FFT directly to frame 10; subpixel parabola; robust similarity fit from cross-body patch pairs; no accumulation drift',
 'crop':{'x':656,'y':0,'width':608,'height':1080},'reference_frame':10,'reference_seconds':.4,'fps':25,'frame_count':765,
 'pivot_source_px':PIVOT.tolist(),'transform_formula':'q = pivot + translation + scale * rotation_clockwise_in_screen_coordinates * (p - pivot)',
 'patches':[{'id':name,'rect_source_px':[x,y,w,h]} for name,x,y,w,h in PATCHES],
 'metrics':metrics,'smoothing':'Nine-frame symmetric Gaussian sigma=2 frames; only short rejected gaps interpolated; reference rebased to identity; no output when acceptance fails',
 'frames':[{'frame':r['frame'],'time_seconds':r['time_seconds'],'reliable_observation':bool(good[i]),'transform':dict(zip(['x_px','y_px','rotation_deg','scale'],map(float,smoothed[i]))) if smoothed is not None else None,'raw':r['raw'],'patches':r['patches']} for i,r in enumerate(records)],
 'limits':['Shirt is nonrigid; local texture motion may not support a single global torso transform.','Does not track or alter the head, face, neck, source video, or narration.','No new gesture is inferred from missing shoulders.','Candidate transform needs an independent moving composite review.']}
if smoothed is not None:
    align_scale=.98210188129886555
    align_translation=np.array([536.81080567706067,-166.4062213300034])
    pivot_reference=PIVOT*align_scale+align_translation
    for i,record in enumerate(output['frames']):
        tx,ty,rotation,scale=smoothed[i]
        angle=math.radians(rotation);a=scale*math.cos(angle);b=scale*math.sin(angle)
        delta=smoothed[i,:2]*align_scale
        e,f=pivot_reference+delta-np.array([[a,-b],[b,a]])@pivot_reference
        record['reference_space_transform']={'x_px':float(delta[0]),'y_px':float(delta[1]),'rotation_deg':float(rotation),'scale':float(scale),'css_matrix':[float(a),float(b),float(-b),float(a),float(e),float(f)]}
    output['reference_space_mapping']={'dimensions':[1672,941],'source_alignment_scale':align_scale,'source_alignment_translation':align_translation.tolist(),'pivot_reference_px':pivot_reference.tolist(),'application':'A new wrapper outside existing #shirt-clip; preserve nested scaleY(1.14). Translate relative to this pivot, then rotate/scale about it. Do not also add css_matrix when using decomposed properties.','transform_order':'translate(x,y) rotate(rotation) scale(scale) with transform-origin at pivot_reference_px'}
    step=np.diff(smoothed,axis=0)
    qa={'frame_count':len(smoothed),'fps':25,'frame_zero_seconds':0,'last_frame_seconds':764/25,'reference_frame':10,'reference_transform':output['frames'][10]['transform'],
        'reference_exact_identity':bool(np.array_equal(smoothed[10],[0,0,0,1])),
        'all_values_finite':bool(np.isfinite(smoothed).all()),
        'all_times_and_frames_contiguous':all(r['frame']==i and r['time_seconds']==i/25 for i,r in enumerate(output['frames'])),
        'smoothed_ranges':dict(zip(['dx_px','dy_px','rotation_deg','scale'],[[float(v.min()),float(v.max())] for v in smoothed.T])),
        'max_adjacent_step':dict(zip(['dx_px','dy_px','rotation_deg','scale'],[float(np.max(np.abs(v))) for v in step.T])),
        'max_adjacent_translation_vector_px':float(np.max(np.linalg.norm(step[:,:2],axis=1))),
        'median_translation_step_px':float(np.median(np.linalg.norm(step[:,:2],axis=1))),
        'continuity_bounds':{'translation_vector_px_per_frame':4.,'rotation_deg_per_frame':.5,'scale_per_frame':.01},
        'continuity_pass':bool(np.max(np.linalg.norm(step[:,:2],axis=1))<4 and np.max(np.abs(step[:,2]))<.5 and np.max(np.abs(step[:,3]))<.01),
        'note':'Continuity and numeric fit are technical checks, not independent composite-motion approval.'}
    assert qa['reference_exact_identity'] and qa['all_values_finite'] and qa['all_times_and_frames_contiguous'] and qa['continuity_pass']
    (ROOT/'motion-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
(ROOT/'tracking.json').write_text(json.dumps(output,indent=2)+'\n')
(ROOT/'tracking-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
(ROOT/'media').mkdir(exist_ok=True)
colors=[(77,172,225),(231,138,70),(168,118,218),(70,187,139)]
plot=Image.new('RGB',(1200,900),(248,248,245));d=ImageDraw.Draw(plot)
for j,label in enumerate(['Horizontal shift at pivot (source px)','Vertical shift at pivot (source px)','Rotation (degrees)','Scale']):
    y0=35+j*215;lo=float(values[:,j].min());hi=float(values[:,j].max());span=max(hi-lo,1e-4)
    d.text((25,y0),label,fill=(20,20,20));d.text((25,y0+20),f'raw range {lo:.4f} to {hi:.4f}',fill=(50,50,50))
    d.rectangle((90,y0+40,1170,y0+185),outline=(140,140,140))
    pts=[(90+i/764*1080,y0+180-(v-lo)/span*135) for i,v in enumerate(values[:,j])]
    d.line(pts,fill=colors[j],width=1)
    for i in np.flatnonzero(~good)[::5]:
        x=90+i/764*1080;d.line((x,y0+183,x,y0+187),fill=(210,50,50),width=1)
    if smoothed is not None:
        d.line([(90+i/764*1080,y0+180-(v-lo)/span*135) for i,v in enumerate(smoothed[:,j])],fill=(20,20,20),width=2)
    d.text((90,y0+190),'0 s',fill=(30,30,30));d.text((1120,y0+190),'30.56 s',fill=(30,30,30))
plot.save(ROOT/'media/motion-diagnostic.png')
sheet=Image.new('RGB',(912,1110),(22,22,22));draw=ImageDraw.Draw(sheet)
for j,n in enumerate([10,100,198,400,580,764]):
    im=Image.fromarray(frames[n]).convert('RGB');idraw=ImageDraw.Draw(im)
    for k,((name,x,y,w,h),p) in enumerate(zip(PATCHES,records[n]['patches'])):
        xx=x/2+p['dx']/2;yy=y/2+p['dy']/2
        idraw.rectangle((xx,yy,xx+w/2,yy+h/2),outline=colors[k],width=2)
    x=(j%3)*304;y=(j//3)*555
    sheet.paste(im,(x,y+15));draw.text((x+6,y),f'{n/25:.2f}s  reliable={bool(good[n])}',fill='white')
sheet.save(ROOT/'media/patch-contact-sheet.jpg',quality=90)
print(json.dumps(metrics,indent=2))
