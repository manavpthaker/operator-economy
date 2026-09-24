"""Owner-requested highlighted, offset Counterproof heading captions.

Keep the previous verified SRT and clean R4 master. Adapt the installed subtitle
burner's label renderer; preserve its hold, overlay and audio-copy pipeline.
"""
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.request
import zipfile
from PIL import Image, ImageDraw, ImageFont


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


cfg = json.loads(Path('inputs.json').read_text())
for url, path, digest in [
    (cfg['video_url'], 'clean.mp4', cfg['video_sha256']),
    (cfg['font_url'], 'Archivo.ttf', cfg['font_sha256']),
]:
    urllib.request.urlretrieve(url, path)
    assert sha(path) == digest, path
Path('caps.srt').write_text(cfg['srt'], encoding='utf-8')
assert sha('caps.srt') == cfg['srt_sha256']
script_words = cfg['script'].split()
caption_words = ' '.join(line for line in cfg['srt'].splitlines()
                         if line.strip() and not line.isdigit() and '-->' not in line).split()
assert caption_words == script_words and len(caption_words) == 184
assert cfg['prior_transcription_similarity'] >= 0.90

bundled_path = Path(os.environ['HF_WORKFLOWS'])/'subtitles/scripts/subtitle_paper_burn.py'
source = bundled_path.read_text()
old = '"-filter_complex",fc'
assert source.count(old) == 1
source = source.replace(old, '"-filter_complex_threads","1","-filter_complex",fc')
module = {'__name__': 'heading_caption_burner', '__file__': str(bundled_path)}
exec(compile(source, str(bundled_path), 'exec'), module)
font_loader = ImageFont.truetype


def heading_font(*args, **kwargs):
    font = font_loader(*args, **kwargs)
    if str(args[0]).endswith('Archivo.ttf'):
        font.set_variation_by_axes([630, 100])
    return font


ImageFont.truetype = heading_font
font = heading_font('Archivo.ttf', 56)
tracking = -0.06 * font.size
max_text_width = 528


def width(text):
    return font.getlength(text) + max(len(text)-1, 0)*tracking


def lines_for(text):
    if width(text) <= max_text_width:
        return [text]
    words = text.split()
    options = [(' '.join(words[:i]), ' '.join(words[i:])) for i in range(1, len(words))]
    choices = [lines for lines in options if max(map(width, lines)) <= max_text_width]
    assert choices, text
    return list(min(choices, key=lambda lines: max(map(width, lines))))


def fixed_size(draw, texts, path, size, max_w, **kwargs):
    for text in texts:
        assert len(lines_for(text)) <= 2
    return 56


layout = []


def heading_label(text, supplied_font, W, H, bottom_frac, maxw_frac, **kwargs):
    assert (W, H) == (720, 1280)
    lines = lines_for(text)
    # Same stable left axis for every cue, so short captions remain off center.
    left, top, pad_x, pad_y = 48, 900, 16, 12
    ink_box = font.getbbox('Ágjy')
    ink_height = ink_box[3]-ink_box[1]
    pitch = max(53, ink_height+2)
    longest = max(width(line) for line in lines)
    right = left + int(longest+0.999) + 2*pad_x
    bottom = top + 2*pad_y + ink_height + (len(lines)-1)*pitch
    assert right <= 608 and bottom <= 1064
    canvas = Image.new('RGBA', (W,H), (0,0,0,0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((left,top,right,bottom), fill=(32,36,38,255))
    for index, line in enumerate(lines):
        y = top+pad_y-ink_box[1]+index*pitch
        for i, char in enumerate(line):
            x = left+pad_x+font.getlength(line[:i])+i*tracking
            draw.text((x,y), char, font=font, fill=(243,246,245,255))
    bbox = canvas.getbbox()
    assert bbox[0] == left and bbox[1] == top and bbox[2] <= 609 and bbox[3] <= 1065
    layout.append({'text': text, 'lines': lines, 'box': list(bbox),
                   'font_size': 56, 'weight': 630, 'width_axis': 100,
                   'tracking_px': tracking, 'line_pitch': pitch})
    return canvas


module['bold_fit_size'] = fixed_size
module['bold_label'] = heading_label
sys.argv = ['heading_burner', '--in', 'clean.mp4', '--srt', 'caps.srt',
            '--out', 'heading.mp4', '--style', 'bold', '--font', 'Archivo.ttf',
            '--no-caps', '--no-outline', '--fontsize-frac', str(56/1280),
            '--gap', '0.042', '--tail', '0.18', '--bridge', '0.35', '--min-dur', '0.30']
module['main']()
assert len(layout) == 49
Path('LAYOUT.json').write_text(json.dumps(layout, indent=2, ensure_ascii=False))


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format',
                           '-of','json',path],capture_output=True,text=True).stdout)


before, after = probe('clean.mp4'), probe('heading.mp4')
for kind in ['video','audio']:
    a = next(s for s in before['streams'] if s['codec_type'] == kind)
    b = next(s for s in after['streams'] if s['codec_type'] == kind)
    assert abs(float(a['duration'])-float(b['duration'])) < 0.05
    assert a.get('start_time') == b.get('start_time')
    if kind == 'video':
        for key in ['width','height','r_frame_rate','nb_frames']:
            assert a[key] == b[key], key
audio_hashes = [run(['ffmpeg','-v','error','-i',p,'-map','0:a:0',
                    '-f','streamhash','-hash','sha256','-'],capture_output=True,text=True).stdout
                for p in ['clean.mp4','heading.mp4']]
assert audio_hashes[0] == audio_hashes[1]
run(['ffmpeg','-v','error','-xerror','-i','heading.mp4','-f','null','-'])

cues = module['parse_srt']('caps.srt')
contact = Image.new('RGB',(1440,1280),'#202426')
for j,index in enumerate([0,7,17,48]):
    start,end,text = cues[index]
    image_path = f'frame-{index}.jpg'
    run(['ffmpeg','-v','error','-ss',str((start+end)/2),'-i','heading.mp4',
         '-frames:v','1','-q:v','2',image_path])
    contact.paste(Image.open(image_path).resize((360,640)),(j*360,0))
    contact.paste(Image.open(image_path).crop((32,880,640,1090)).resize((360,124)),(j*360,675))
contact = contact.crop((0,0,1440,820))
contact.save('contact.jpg',quality=94)
report = {'status':'mechanically_verified_pending_visual_review',
          'source_sha256':cfg['video_sha256'],'output_sha256':sha('heading.mp4'),
          'output_bytes':Path('heading.mp4').stat().st_size,
          'srt_sha256':sha('caps.srt'),'srt_unchanged':True,'word_count':184,'cue_count':49,
          'font_sha256':sha('Archivo.ttf'),'font_size_px':56,'weight':630,'width_axis':100,
          'tracking_em':-0.06,'text':'#F3F6F5','highlight':'#202426',
          'audio_unchanged':True,'audio_decoded_hash':audio_hashes[0].strip(),
          'before':before,'after':after,'bundled_burner_sha256':sha(bundled_path)}
Path('REPORT.json').write_text(json.dumps(report,indent=2))
for path,key,mime in [('heading.mp4','video_upload_url','video/mp4'),
                      ('contact.jpg','contact_upload_url','image/jpeg')]:
    status=run(['curl','-f','-sS','-X','PUT','-H','Content-Type: '+mime,'--upload-file',path,
                '-o','/dev/null','-w','%{http_code}',cfg[key]],capture_output=True,text=True).stdout
    assert status == '200', path
    print('UPLOAD_OK',path,200,flush=True)
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED) as archive:
    for name in ['REPORT.json','LAYOUT.json','caps.srt']:
        archive.write(name)
print('RECORDS_ZIP_BASE64='+base64.b64encode(buf.getvalue()).decode(),flush=True)
print('RENDER_COMPLETE',report['output_sha256'],report['output_bytes'],flush=True)
