"""Integrate only the three verified new sources into the existing R31 draft."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

BASE = Path(__file__).resolve().parent
PROJECT = BASE.parent
TAKES = ['v5-opportunity', 'v5-post-title-continuous', 'v5-question']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == '__main__':
    if (BASE / 'INTEGRATION.json').exists():
        raise SystemExit('Integration already recorded; inspect before changing it.')
    rows = {}
    for name in TAKES:
        folder = BASE / name
        source = folder / 'restored.mp4'
        qa = json.loads((folder / 'restored-qa.json').read_text())
        assert qa['sha256'] == digest(source), name
        assert qa['full_decode'] == 'pass' and qa['fps'] == '24/1', name
        assert qa['audio']['aligned_audio_correlation'] > .98, name
        assert not qa['audio']['offset_at_search_boundary'], name
        offset = qa['audio']['audio_insertion_offset_seconds']
        frame = round(offset * 24)
        assert frame >= 0, 'Negative placement needs an explicit source decision'
        selected_in = frame / 24
        needed = {'v5-opportunity': 4.75, 'v5-post-title-continuous': 15,
            'v5-question': 289 / 24}[name]
        assert qa['duration_seconds'] + .001 >= selected_in + needed, name
        rows[name] = {'restored_source_sha256': qa['sha256'], 'waveform_offset_seconds': offset,
            'picture_offset_frames': frame, 'picture_offset_seconds': selected_in,
            'quantization_residual_seconds': offset - selected_in}
    for name in TAKES:
        src = BASE / name / 'restored.mp4'
        dst = PROJECT / 'public/media' / f'{name}.mp4'
        assert not dst.exists(), 'Do not overwrite an existing review proxy'
        subprocess.run(['ffmpeg', '-v', 'error', '-n', '-i', str(src), '-c:v', 'libx264',
            '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
            '-movflags', '+faststart', str(dst)], check=True)
        rows[name]['review_proxy_sha256'] = digest(dst)
    qoffset = rows['v5-question']['picture_offset_seconds']
    hold = PROJECT / 'public/media/v5-question-hold.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-ss', str(qoffset + 12), '-i',
        str(PROJECT / 'public/media/v5-question.mp4'), '-frames:v', '1', '-q:v', '2', str(hold)], check=True)
    source = (PROJECT / 'index.html').read_text()
    source = source.replace('EP007 R31 — V5 wide opening · remaining avatar replacements prepared',
        'EP007 R31 — All presenter scenes use V5 · wide to close')
    source = source.replace('height:724px', 'height:720px').replace('object-fit:fill', 'object-fit:cover')
    source = source.replace('.promise-framing', '.post-title-framing')
    opportunity = re.search(r'<video[^>]*id="avatar-opportunity"[^>]*>', source).group()
    updated = opportunity.replace('public/media/presenter-pickups-browser.mp4', 'public/media/v5-opportunity.mp4')
    updated = re.sub(r'data-media-start="[^"]+"',
        f'data-media-start="{rows["v5-opportunity"]["picture_offset_seconds"] + 8/24}"', updated)
    source = source.replace(opportunity, updated)
    definition_line = next(line for line in source.splitlines() if 'id="post-title-definition"' in line)
    promise_line = next(line for line in source.splitlines() if 'id="post-title-promise"' in line)
    replacement = ('<div class="viewport" data-layout-allow-overflow=""><div id="post-title-framing" '
        'class="post-title-framing" data-layout-allow-overflow=""><video data-hf-id="hf-fb3k" '
        'id="avatar-post-title" class="clip avatar" src="public/media/v5-post-title-continuous.mp4" '
        f'data-start="56.5" data-duration="15" data-media-start="{rows["v5-post-title-continuous"]["picture_offset_seconds"]}" '
        'data-track-index="1" muted playsinline aria-label="One continuous V5 wide presenter take; '
        'editorial crops change at the viewing promise and just after and before one number."></video></div></div>')
    source = source.replace(definition_line, replacement).replace(promise_line + '\n', '')
    source = source.replace("tl.set('#promise-framing', {x:-160, y:-24, scale:1.25, transformOrigin:'0 0'}, 0);",
        "tl.set('#post-title-framing', {x:0, y:0, scale:1, transformOrigin:'0 0'}, 0);\n"
        "tl.set('#post-title-framing', {x:-140.8, y:-12, scale:1.22, transformOrigin:'0 0'}, 62.916666666666664);")
    source = source.replace("tl.set('#promise-framing', {x:-256, y:-42, scale:1.4, transformOrigin:'0 0'}, 'one-number');",
        "tl.set('#post-title-framing', {x:-320, y:-22, scale:1.5, transformOrigin:'0 0'}, 'one-number');")
    question = (PROJECT / 'compositions/presenter-question.html').read_text()
    question = question.replace('public/media/presenter-question.mp4', 'public/media/v5-question.mp4')
    question = question.replace('public/media/presenter-question-hold.jpg', 'public/media/v5-question-hold.jpg')
    question = question.replace('data-media-start="0"', f'data-media-start="{qoffset}"')
    question = question.replace('scale:1.08,x:-51.2,y:-12', 'scale:1,x:0,y:0')
    assert 'scale:1.2,x:-128,y:-22' in question
    question = question.replace('scale:1.2,x:-128,y:-22', 'scale:1.42,x:-268.8,y:-22')
    (PROJECT / 'index.html').write_text(source)
    (PROJECT / 'compositions/presenter-question.html').write_text(question)
    rows['editorial'] = {'post_title_crops': [[56.5, 1], [62.916666666666664, 1.22], [67.58, 1.5]],
        'question_crops': [[131, 1], [139.9583333333, 1.42]],
        'post_title_single_video_element': True, 'source_voice_in_edit': 'Unchanged original master WAV files',
        'question_hold_source_time_seconds': qoffset + 12, 'question_hold_duration_seconds': .75,
        'question_hold_sha256': digest(hold), 'review_status': 'Integrated candidate; check actual crops and seams before handoff'}
    (BASE / 'INTEGRATION.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(json.dumps(rows))
