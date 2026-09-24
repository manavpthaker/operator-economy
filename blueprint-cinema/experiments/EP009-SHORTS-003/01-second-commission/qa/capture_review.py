from pathlib import Path
import subprocess,json
P=Path(__file__).resolve().parents[1];times=[.3,1.6,3.8,4.13,5.5,7.8,7.88,9.7,11.25,12.9]
for i,t in enumerate(times):
 out=P/'qa'/f'frame-{i:02}.jpg'
 subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(P/'review-r3.mp4'),'-frames:v','1','-q:v','2','-y',str(out)],check=True)
subprocess.run(['ffmpeg','-v','error','-framerate','1','-i',str(P/'qa/frame-%02d.jpg'),'-vf','scale=270:480,tile=5x2','-frames:v','1','-q:v','2','-y',str(P/'qa/contact-sheet.jpg')],check=True)
(P/'qa/frame-times.json').write_text(json.dumps(times)+'\n')
