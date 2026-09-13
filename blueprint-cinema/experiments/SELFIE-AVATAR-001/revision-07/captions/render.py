"""R7 first-section review with the latest requested Counterproof heading captions.

Map the first 68 R4 script words through the actual R7 voice sample map, then
apply the fresh measured offset from that edited voice to the clean sample.
Use the installed burner and preserve the proven heading design and soundtrack.
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


R4_SRT_SHA256 = 'eb157d8a967facdd2c8eebd1449adecd1dcebd86d0d57104c1dae42110673124'
SCRIPT_SHA256 = '3eb28bd243f2c169b5906852f3b055553d1bc0e0520a029082fa5bf41a36fbe3'
VOICE_SHA256 = 'b2c10c8e5b3267a43f8aaa4b3aba2132f4b20d6df6cd22fbfdcf0dc831e7e3b3'
FONT_SHA256 = '0e094a7d3c7c4c25cf1310c4b30014f1dae9332220b1c2c88f4fa996f0b05053'
WORD_CLOCK_SHA256 = 'b46d878fd1b0cfebd3d7e42a02ea5a5f66a9d1d9b13a5dacfd4188612cb1a3be'
R7_VOICE_REPORT_SHA256 = '4e5b95a90e5ed8a3c6249db63e45c8edafebda58eebaa01432a087c7a654274e'
R4_OFFSET_SECONDS = 0.342125
SOURCE_WORD_TIMES = [[0,0.48],[0.48,0.64],[0.64,0.84],[0.84,1],[1,1.16],[1.16,1.32],[1.32,1.7],[1.7,2],[2,2.14],[2.14,2.28],[2.28,2.46],[2.46,2.7],[2.7,2.9],[2.9,3.02],[3.02,3.38],[3.96,4.14],[4.14,4.36],[4.36,4.48],[4.48,4.66],[4.66,4.86],[4.86,5.12],[5.64,5.82],[5.82,6.18],[6.48,6.54],[6.54,6.68],[6.68,6.82],[6.82,7.08],[7.08,7.38],[7.38,7.68],[7.68,7.96],[7.96,8.28],[8.28,8.52],[8.52,8.68],[8.68,8.92],[8.92,9.18],[9.18,9.5],[9.5,9.74],[9.74,10.06],[10.06,10.38],[10.38,10.58],[11.28,11.48],[11.48,11.66],[11.66,11.86],[11.86,12.22],[12.22,13.04],[13.04,13.26],[13.26,13.66],[13.66,13.82],[13.82,14],[14,14.2],[14.2,14.48],[14.48,14.82],[15.26,15.44],[15.44,15.6],[15.6,15.76],[15.76,15.9],[15.9,16.18],[16.5,16.72],[16.72,17.38],[17.38,17.78],[17.78,18.02],[18.02,18.3],[18.3,18.5],[18.5,18.78],[18.78,18.96],[18.96,19.1],[19.1,19.3],[19.3,19.72]]


def text_sha(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def parse_input_srt(value):
    result = []
    previous_end = 0.0
    for ordinal, block in enumerate(re.split(r'\n\s*\n', value.strip()), 1):
        lines = block.splitlines()
        assert len(lines) >= 3 and lines[0] == str(ordinal), ordinal
        match = re.fullmatch(
            r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> '
            r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', lines[1])
        assert match, lines[1]
        values = [int(v) for v in match.groups()]
        times = []
        for i in (0, 4):
            hour, minute, second, milli = values[i:i+4]
            assert minute < 60 and second < 60
            times.append(hour*3600 + minute*60 + second + milli/1000)
        start, end = times
        assert previous_end <= start < end, (ordinal, previous_end, start, end)
        text = ' '.join(' '.join(lines[2:]).split())
        assert text, ordinal
        result.append({'text': text, 'start': start, 'end': end})
        previous_end = end
    assert len(result) == 49, len(result)
    return result



def stamp(seconds):
    millis = round(seconds * 1000)
    assert millis >= 0
    return f'{millis//3600000:02}:{millis//60000%60:02}:{millis//1000%60:02},{millis%1000:03}'


cfg = json.loads(Path('inputs.json').read_text())
assert cfg['font_sha256'] == FONT_SHA256
assert text_sha(cfg['script']) == SCRIPT_SHA256
assert text_sha(cfg['prior_srt']) == R4_SRT_SHA256
full_cues = parse_input_srt(cfg['prior_srt'])
prior_cues = full_cues[:18]
script_words = cfg['script'].split()[:68]
assert len(script_words) == len(SOURCE_WORD_TIMES) == 68
assert ' '.join(c['text'] for c in prior_cues).split() == script_words
voice_report_sha256 = text_sha(cfg['voice_report_json'])
assert voice_report_sha256 == cfg['voice_report_sha256'] == R7_VOICE_REPORT_SHA256
voice = json.loads(cfg['voice_report_json'])
assert voice['source_sha256'] == VOICE_SHA256
assert voice['sample_rate_hz'] == 48000
assert re.fullmatch(r'[0-9a-f]{64}', voice['output_sha256'])
rate = voice['sample_rate_hz']
sample_map = voice['sample_map']
expected_ranges = [(0,534480), (534480,782640), (782640,782640),
                   (782640,955200), (955200,968000), (968000,968000)]
assert len(sample_map) in (5,6)
assert [tuple(part['source_samples']) for part in sample_map] == expected_ranges[:len(sample_map)]
output_cursor = 0
for part in sample_map:
    ss, se = part['source_samples']
    os_, oe = part['output_samples']
    assert all(isinstance(n, int) for n in (ss,se,os_,oe))
    assert 0 <= ss <= se and output_cursor == os_ <= oe
    assert part['source_sample_count'] == se-ss
    assert part['output_sample_count'] == oe-os_
    if ss == se:
        expected_op = 'insert_silence' if ss == 782640 else 'pad_to_video_frame'
        assert part['operation'] == expected_op
        if expected_op == 'insert_silence':
            assert oe-os_ == 5760
    elif (ss,se) in [(0,534480),(955200,968000)]:
        assert oe-os_ == se-ss
    else:
        assert oe-os_ > se-ss
    output_cursor = oe
assert output_cursor == voice['output_sample_count']
assert voice['frame_count']*2000 == output_cursor


def map_source(seconds, boundary):
    sample = seconds * rate
    # The first R4 SRT cue rounded 0.342125 to 0.342; remove that six-sample
    # quantization residue without moving any speech or assuming a new offset.
    if sample < 0:
        assert sample >= -rate*0.0011
        sample = 0.0
    positive = [part for part in sample_map if part['source_sample_count'] > 0]
    for part in positive:
        ss, se = part['source_samples']
        inside = ss <= sample < se if boundary == 'start' else ss < sample <= se
        if inside or sample == 0 == ss:
            os_, oe = part['output_samples']
            return (os_ + (sample-ss)*(oe-os_)/(se-ss)) / rate
    raise AssertionError(('source time outside first section', seconds, boundary))


offset = float(cfg['audio_offset_seconds'])
assert math.isfinite(offset)
alignment = cfg['audio_alignment']
assert alignment['video_sha256'] == cfg['video_sha256']
assert alignment['source_voice_sha256'] == voice['output_sha256']
assert alignment['full_source_voice_preserved'] is True
assert alignment['uniform_offset'] is True
assert abs(float(alignment['offset_seconds']) - offset) < 0.000001
drift, correlation = float(alignment['max_drift_seconds']), float(alignment['min_window_correlation'])
assert math.isfinite(drift) and 0 <= drift <= 0.02
assert math.isfinite(correlation) and 0.99 <= correlation <= 1.0
assert re.fullmatch(r'[0-9a-f]{64}', alignment['evidence_sha256'])
alignment_receipt = {key: alignment[key] for key in (
    'video_sha256','source_voice_sha256','full_source_voice_preserved',
    'uniform_offset','offset_seconds','max_drift_seconds',
    'min_window_correlation','evidence_sha256')}

mapped_words = [
    {'word_index':i+1, 'text':text, 'source_start':times[0], 'source_end':times[1],
     'start':map_source(times[0],'start')+offset,
     'end':map_source(times[1],'end')+offset}
    for i,(text,times) in enumerate(zip(script_words,SOURCE_WORD_TIMES))]
mapped_cues = []
cursor, previous_end = 0, 0.0
for index, cue in enumerate(prior_cues, 1):
    count = len(cue['text'].split())
    source_start, source_end = cue['start']-R4_OFFSET_SECONDS, cue['end']-R4_OFFSET_SECONDS
    # Check the SRT-derived source clock against the frozen full-precision word
    # clock before applying the actual piecewise sample ratios.
    assert abs(source_start-SOURCE_WORD_TIMES[cursor][0]) <= 0.0011
    assert abs(source_end-SOURCE_WORD_TIMES[cursor+count-1][1]) <= 0.0011
    start = map_source(source_start,'start')+offset
    end = map_source(source_end,'end')+offset
    assert previous_end <= start < end <= output_cursor/rate+offset
    mapped_cues.append({'cue':index,'text':cue['text'],'start':start,'end':end,
                       'source_start':source_start,'source_end':source_end,
                       'source_first_word':cursor+1,'source_last_word':cursor+count})
    cursor += count
    previous_end = end
assert cursor == 68 and len(mapped_cues) == 18
srt = '\n\n'.join(f"{c['cue']}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}"
                  for c in mapped_cues) + '\n'
Path('caps.srt').write_text(srt, encoding='utf-8')
mapped_srt_sha256 = sha('caps.srt')
timing_report = {
    'status':'mapped_for_review_not_phoneme_alignment_proof',
    'prior_srt_sha256':R4_SRT_SHA256,'srt_sha256':mapped_srt_sha256,
    'source_script_sha256':SCRIPT_SHA256,'source_word_clock_sha256':WORD_CLOCK_SHA256,
    'original_voice_sha256':VOICE_SHA256,'edited_voice_sha256':voice['output_sha256'],
    'voice_report_sha256':voice_report_sha256,'sample_rate_hz':rate,
    'sample_map':sample_map,'removed_r4_offset_seconds':R4_OFFSET_SECONDS,
    'new_measured_audio_offset_seconds':offset,'word_count':68,'cue_count':18,
    'caption_text_matches_first_68_source_words':True,'words':mapped_words,
    'cues':mapped_cues,'audio_alignment':alignment_receipt,
    'timing_limit':'Actual interval sample counts define linear mappings within transformed ranges. Tempo processing may have local phase variation; speech/caption review remains required.'}
Path('TIMING-MAP.json').write_text(json.dumps(timing_report,indent=2,ensure_ascii=False))

for url, path, digest in [
    (cfg['video_url'], 'clean.mp4', cfg['video_sha256']),
    (cfg['font_url'], 'Archivo.ttf', cfg['font_sha256']),
]:
    urllib.request.urlretrieve(url, path)
    assert sha(path) == digest, path
assert sha('caps.srt') == mapped_srt_sha256

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
assert len(layout) == 18
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
contact = Image.new('RGB',(1440,1790),'#202426')
for j,index in enumerate([0,4,12,17]):
    start,end,text = cues[index]
    image_path = f'frame-{index}.jpg'
    run(['ffmpeg','-v','error','-ss',str((start+end)/2),'-i','heading.mp4',
         '-frames:v','1','-q:v','2',image_path])
    contact.paste(Image.open(image_path).resize((360,640)),(j*360,0))
    contact.paste(Image.open(image_path).crop((32,880,640,1090)).resize((360,124)),(j*360,675))
# Additional review-only face crops show the smile returning to speaking.
# They do not alter the delivered video or require a second upload slot.
expression_times = [3.5,3.875,4.25,4.5,4.875,5.25,5.667,6.125]
expression_samples = []
contact_draw = ImageDraw.Draw(contact)
contact_font = ImageFont.truetype('Archivo.ttf',22)
for j, requested_time in enumerate(expression_times):
    frame_index = round(requested_time*24)
    actual_time = frame_index/24
    image_path = f'expression-frame-{frame_index}.jpg'
    run(['ffmpeg','-v','error','-ss',str(actual_time),'-i','heading.mp4',
         '-frames:v','1','-q:v','2',image_path])
    left, top = (j%4)*360, 820+(j//4)*480
    contact_draw.text((left+10,top+5),f'{actual_time:.3f}s | frame {frame_index}',
                      font=contact_font,fill='#F3F6F5')
    face = Image.open(image_path).crop((90,175,630,835)).resize((360,440))
    contact.paste(face,(left,top+35))
    expression_samples.append({'requested_seconds':requested_time,
                               'sample_seconds':actual_time,'frame':frame_index,
                               'source_crop':[90,175,630,835]})
contact.save('contact.jpg',quality=94)
report = {'status':'mechanically_verified_pending_visual_review',
          'source_sha256':cfg['video_sha256'],'output_sha256':sha('heading.mp4'),
          'output_bytes':Path('heading.mp4').stat().st_size,
          'srt_sha256':sha('caps.srt'),'prior_srt_sha256':R4_SRT_SHA256,
          'caption_text_matches_first_68_source_words':True,'word_count':68,'cue_count':18,
          'source_script_sha256':SCRIPT_SHA256,'source_word_clock_sha256':WORD_CLOCK_SHA256,
          'original_voice_sha256':VOICE_SHA256,'edited_voice_sha256':voice['output_sha256'],
          'voice_report_sha256':voice_report_sha256,
          'new_measured_audio_offset_seconds':offset,
          'timing_method':'actual piecewise voice sample map plus measured Sync offset',
          'timing_map_report_sha256':sha('TIMING-MAP.json'),'audio_alignment':alignment_receipt,
          'expression_contact_samples':expression_samples,
          'font_sha256':sha('Archivo.ttf'),'font_size_px':56,'weight':630,'width_axis':100,
          'tracking_em':-0.06,'text':'#F3F6F5','highlight':'#202426',
          'audio_unchanged_by_caption_burn':True,'audio_decoded_hash':audio_hashes[0].strip(),
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
    for name in ['REPORT.json','LAYOUT.json','TIMING-MAP.json','caps.srt']:
        archive.write(name)
print('RECORDS_ZIP_BASE64='+base64.b64encode(buf.getvalue()).decode(),flush=True)
print('RENDER_COMPLETE',report['output_sha256'],report['output_bytes'],flush=True)
