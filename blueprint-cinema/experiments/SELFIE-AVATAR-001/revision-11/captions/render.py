"""R11 caption adapter preserving the accepted R10 Counterproof treatment.

The verified R10 SRT is valid only with its unchanged full audio timeline.
The finisher proves copied packet payloads, decoded audio, and timeline identity,
then binds the same caption bytes to the new clean picture before this burn.
"""
import base64
import hashlib
import io
import json
import os
import math
import re
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


SCRIPT_SHA256 = '242ab0bedea72a8fc5d303191f9dc61569614dc70cfdbef759891a7fa94affd6'
FONT_SHA256 = '0e094a7d3c7c4c25cf1310c4b30014f1dae9332220b1c2c88f4fa996f0b05053'


def text_sha(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def parse_input_srt(value):
    result, previous_end = [], 0.0
    for ordinal, block in enumerate(re.split(r'\n\s*\n', value.strip()), 1):
        lines = block.splitlines()
        assert len(lines) >= 3 and lines[0] == str(ordinal), ordinal
        match = re.fullmatch(
            r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> '
            r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', lines[1])
        assert match, lines[1]
        values = [int(v) for v in match.groups()]
        times = []
        for i in (0,4):
            hour, minute, second, milli = values[i:i+4]
            assert minute < 60 and second < 60
            times.append(hour*3600 + minute*60 + second + milli/1000)
        start, end = times
        assert previous_end <= start < end, (ordinal,previous_end,start,end)
        text = ' '.join(' '.join(lines[2:]).split())
        assert text, ordinal
        result.append({'text':text,'start':start,'end':end})
        previous_end = end
    assert len(result) >= 4
    return result


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format',
                           '-of','json',path],capture_output=True,text=True).stdout)


cfg = json.loads(Path('inputs.json').read_text())
assert text_sha(cfg['script']) == SCRIPT_SHA256
assert cfg['font_sha256'] == FONT_SHA256
assert text_sha(cfg['srt']) == cfg['srt_sha256']
input_cues = parse_input_srt(cfg['srt'])
script_words = cfg['script'].split()
caption_words = ' '.join(c['text'] for c in input_cues).split()
assert caption_words == script_words
word_count, cue_count = len(script_words), len(input_cues)
assert word_count > 0

transcription = cfg['transcription']
assert transcription['video_sha256'] == cfg['video_sha256']
assert transcription['script_sha256'] == SCRIPT_SHA256
assert transcription['srt_sha256'] == cfg['srt_sha256']
assert transcription['word_count'] == word_count
similarity = float(transcription['similarity'])
assert math.isfinite(similarity) and 0.90 <= similarity <= 1.0
assert re.fullmatch(r'[0-9a-f]{64}',transcription['evidence_sha256'])
transcription_receipt = {key:transcription[key] for key in (
    'video_sha256','script_sha256','srt_sha256','word_count','similarity','evidence_sha256')}

# Root supplies this only after checking the complete narration in this final
# clean video. The renderer separately verifies the decoded audio hash below.
audio_binding = cfg['audio_binding']
assert audio_binding['video_sha256'] == cfg['video_sha256']
assert audio_binding['full_source_audio_preserved'] is True
for key in ('source_audio_sha256','video_audio_decoded_sha256','evidence_sha256'):
    assert re.fullmatch(r'[0-9a-f]{64}',audio_binding[key]), key
audio_receipt = {key:audio_binding[key] for key in (
    'video_sha256','source_audio_sha256','video_audio_decoded_sha256',
    'full_source_audio_preserved','evidence_sha256')}

if cfg.get('video_local_path'):
    assert cfg['video_local_path'] == 'clean.mp4'
    assert Path('clean.mp4').is_file()
    assert sha('clean.mp4') == cfg['video_sha256']
else:
    urllib.request.urlretrieve(cfg['video_url'], 'clean.mp4')
    assert sha('clean.mp4') == cfg['video_sha256']
if not Path('Archivo.ttf').is_file():
    urllib.request.urlretrieve(cfg['font_url'], 'Archivo.ttf')
assert sha('Archivo.ttf') == cfg['font_sha256']
Path('caps.srt').write_text(cfg['srt'],encoding='utf-8')
assert sha('caps.srt') == cfg['srt_sha256']
before = probe('clean.mp4')
for kind in ('video','audio'):
    stream = next(item for item in before['streams'] if item['codec_type'] == kind)
    stream_end = float(stream.get('start_time',0)) + float(stream['duration'])
    assert input_cues[-1]['end'] <= stream_end+0.05, (kind,input_cues[-1],stream_end)

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
assert len(layout) == cue_count
Path('LAYOUT.json').write_text(json.dumps(layout, indent=2, ensure_ascii=False))


after = probe('heading.mp4')
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
assert audio_hashes[0].strip().split('=')[-1] == audio_receipt['video_audio_decoded_sha256']
run(['ffmpeg','-v','error','-xerror','-i','heading.mp4','-f','null','-'])

cues = module['parse_srt']('caps.srt')
assert len(cues) == cue_count
contact_times = cfg.get('contact_times_seconds', [38.2, 44.0, 49.0, 54.5])
assert len(contact_times) == 4
contact_samples = []
contact = Image.new('RGB',(1440,1280),'#202426')
for j, sample_time in enumerate(contact_times):
    assert 0 <= sample_time < float(after['format']['duration'])
    index = min(range(len(cues)), key=lambda k: abs((cues[k][0]+cues[k][1])/2-sample_time))
    start,end,text = cues[index]
    contact_samples.append({'cue_index':index+1,'sample_seconds':sample_time,'nearest_cue_text':text})
    image_path = f'frame-contact-{j}.jpg'
    run(['ffmpeg','-v','error','-ss',str(sample_time),'-i','heading.mp4',
         '-frames:v','1','-q:v','2',image_path])
    contact.paste(Image.open(image_path).resize((360,640)),(j*360,0))
    contact.paste(Image.open(image_path).crop((32,880,640,1090)).resize((360,124)),(j*360,675))
contact = contact.crop((0,0,1440,820))
contact.save('contact.jpg',quality=94)
report = {'status':'mechanically_verified_pending_visual_review',
          'source_sha256':cfg['video_sha256'],'output_sha256':sha('heading.mp4'),
          'output_bytes':Path('heading.mp4').stat().st_size,
          'srt_sha256':sha('caps.srt'),'matches_supplied_srt_bytes':True,
          'script_sha256':SCRIPT_SHA256,'word_count':word_count,'cue_count':cue_count,
          'transcription':transcription_receipt,'audio_binding':audio_receipt,
          'contact_samples':contact_samples,
          'font_sha256':sha('Archivo.ttf'),'font_size_px':56,'weight':630,'width_axis':100,
          'tracking_em':-0.06,'text':'#F3F6F5','highlight':'#202426',
          'audio_unchanged_by_caption_burn':True,'audio_decoded_hash':audio_hashes[0].strip(),
          'before':before,'after':after,'bundled_burner_sha256':sha(bundled_path)}
Path('REPORT.json').write_text(json.dumps(report,indent=2))
if not cfg.get('finish_manages_delivery'):
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
