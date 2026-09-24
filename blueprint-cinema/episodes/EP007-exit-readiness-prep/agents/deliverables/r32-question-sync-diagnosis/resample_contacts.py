"""Regenerate only diagnostic images at explicit frame numbers; preserve all media."""
from pathlib import Path
import hashlib,io,json,math,subprocess
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent
REPO=Path('/Users/brownmanbrain/GitHub/operator-economy')
j=json.loads((OUT/'evidence.json').read_text())
selected=REPO/j['issued_inputs'][4]['path']
def frame(path,n):
    # Seek just before exact presentation time to avoid decimal rounding selecting n+1.
    t=max(0,n/24-0.00001)
    raw=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{t:.9f}','-i',str(path),'-frames:v','1','-f','image2pipe','-c:v','png','-'])
    return Image.open(io.BytesIO(raw)).convert('RGB')
for item in j['contacts']:
    indices=[round(t*24)+8 for t in item['selected_timeline_sample_seconds']]
    width,height,caption=390,280,34
    sheet=Image.new('RGB',(5*width,math.ceil(len(indices)/5)*(height+caption)),'#eeeae2')
    for i,n in enumerate(indices):
        im=frame(selected,n)
        if item['crop_pixels']:im=im.crop(item['crop_pixels'])
        im.thumbnail((width,height));x=i%5*width;y=i//5*(height+caption)
        sheet.paste(im,(x+(width-im.width)//2,y+(height-im.height)//2))
        local=(n-8)/24
        ImageDraw.Draw(sheet).text((x+5,y+height+4),f'frame {n} | local {local:.3f} | master {local+134:.3f}',fill='black')
    p=REPO/item['path'];sheet.save(p,quality=95)
    item['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    item['source_frame_indices']=indices
    item['selected_timeline_sample_seconds']=[(n-8)/24 for n in indices]
video=OUT/'question-local-r31-original-audio.mp4'
sheet=Image.new('RGB',(1280,768),'#eeeae2')
for i,n in enumerate([214,215,216,306]):
    im=frame(video,n);im.thumbnail((640,360));x=i%2*640;y=i//2*384
    sheet.paste(im,(x,y));ImageDraw.Draw(sheet).text((x+6,y+363),f'export frame {n}, local {n/24:.6f}',fill='black')
p=OUT/'standalone-crop-and-end.jpg';sheet.save(p,quality=95)
j['contacts'].append({'path':str(p.relative_to(REPO)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'standalone_frame_indices':[214,215,216,306]})
(OUT/'evidence.json').write_text(json.dumps(j,indent=2)+'\n')
print('Contacts regenerated at exact nearest frame indices; export crop and endpoint included.')
