"""Diagnostic source/candidate frame pairs, without altering production media."""
import argparse,cv2,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--candidate',required=True);p.add_argument('--end',type=int,required=True);p.add_argument('--out',required=True);a=p.parse_args();out=Path(a.out);assert not out.exists()
indices=list(range(a.end-12,a.end));sources=[Path(a.source),Path(a.candidate)];rows=[]
caps=[cv2.VideoCapture(str(x)) for x in sources]
for frame in indices:
 row=Image.new('RGB',(960,296),'black');dr=ImageDraw.Draw(row)
 for i,cap in enumerate(caps):
  cap.set(cv2.CAP_PROP_POS_FRAMES,frame);ok,bgr=cap.read();assert ok
  im=Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)).resize((480,270));row.paste(im,(i*480,0));dr.text((i*480+5,276),('ORIGINAL'if i==0 else'EDIT')+f' frame {frame}',fill='white')
 rows.append(row)
for c in caps:c.release()
sheet=Image.new('RGB',(960,296*len(rows)))
for i,row in enumerate(rows):sheet.paste(row,(0,296*i))
sheet.save(out,quality=93)
out.with_suffix('.json').write_text(json.dumps({'diagnostic_only':True,'frames':indices,'source':{'path':str(sources[0]),'sha256':hashlib.sha256(sources[0].read_bytes()).hexdigest()},'candidate':{'path':str(sources[1]),'sha256':hashlib.sha256(sources[1].read_bytes()).hexdigest()},'sheet_sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2)+'\n')
