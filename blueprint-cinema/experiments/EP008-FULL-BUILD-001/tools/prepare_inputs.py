"""Read-only upstream audit and derived planning inputs for EP008. No gate mutation."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parents[1]
UP = ROOT / 'operator-blueprint-v2/episodes/EP008-ai-implementation-service'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

def main():
    state = json.loads((UP / '02-narration-production/narration-state.json').read_text())
    transcript = json.loads((UP / '02-narration-production/word-transcript.json').read_text())
    expected = {
        UP/'02-narration-production/master/narration-master.wav': state['master']['sha256'],
        UP/'02-narration-production/word-transcript.json': state['transcript']['sha256'],
        UP/'02-narration-production/intentional-pause-map.json': state['intentional_pause_map']['sha256'],
        UP/'01-editorial/script.md': state['identities']['script_sha256'],
        UP/'01-editorial/canonical-w.txt': state['identities']['spoken_text_sha256'],
        UP/'01-editorial/editorial-lock.md': state['identities']['editorial_lock_sha256'],
        UP/'02-narration-production/narration-lock.md': state['narration_lock_sha256'],
    }
    names = ['01-editorial/claims-map.md','01-editorial/operator-canvas.md',
        '01-editorial/episode-investment-thesis.md','01-editorial/episode-beat-sheet.md',
        '01-editorial/narrative-spine.md','01-editorial/episode-outline.md',
        '02-narration-production/visual-translation-handoff.md',
        '02-narration-production/narration-state.json',
        '03-visual-translation/CANDIDATE-STATUS.md']
    files = []
    for path in list(expected) + [UP/name for name in names]:
        actual = sha(path)
        files.append({'path':str(path.relative_to(ROOT)), 'sha256':actual,
            'expected_sha256':expected.get(path),
            'matches_lock':actual == expected[path] if path in expected else None})
    assert all(x['matches_lock'] is not False for x in files), 'Locked input drift'
    words = transcript['words']
    assert len(words) == 3400
    script = (UP/'01-editorial/script.md').read_text()
    scenes = []
    cursor = 0
    for match in re.finditer(r'^## (S\d+): ([^\n]*)\n(.*?)(?=^## S\d|\Z)', script, re.M|re.S):
        sid,title,body = match.groups()
        narration = re.search(r'^### Narration\n(.*?)(?=^### |\Z)',body,re.M|re.S)
        if not narration:
            assert sid == 'S01'
            scenes.append({'scene_id':sid,'title':title,'paragraphs':[],'narration':''})
            continue
        speech = narration.group(1).strip()
        paragraphs=[]
        first=cursor
        for para in re.split(r'\n\s*\n',speech):
            tokens=para.split()
            selected=words[cursor:cursor+len(tokens)]
            assert [w['token'] for w in selected] == tokens, (sid,cursor,'spoken token mismatch')
            paragraphs.append({'paragraph_id':f'{sid}-P{len(paragraphs)+1:02}',
                'first_word_id':selected[0]['w_id'],'last_word_id':selected[-1]['w_id'],
                'speech_in':selected[0]['start'],'speech_out':selected[-1]['end'],'text':para})
            cursor+=len(tokens)
        scenes.append({'scene_id':sid,'title':title,'narration':speech,'paragraphs':paragraphs,
            'first_word_id':words[first]['w_id'],'last_word_id':words[cursor-1]['w_id'],
            'speech_in':words[first]['start'],'speech_out':words[cursor-1]['end']})
    assert cursor == len(words), (cursor,len(words))
    fps=24
    duration=transcript['master_duration_seconds']
    for index, scene in enumerate(scenes):
        if index==0: start=0
        elif scene['scene_id']=='S01': start=scenes[index-1]['speech_out']
        elif scenes[index-1]['scene_id']=='S01': start=scene['speech_in']
        else: start=(scenes[index-1]['speech_out']+scene['speech_in'])/2
        scene['proposed_frame_in']=round(start*fps)
    for index, scene in enumerate(scenes):
        scene['proposed_frame_out']=scenes[index+1]['proposed_frame_in'] if index+1<len(scenes) else round(duration*fps)
        scene['proposed_in']=scene['proposed_frame_in']/fps
        scene['proposed_out']=scene['proposed_frame_out']/fps
    result={'record_type':'ep008_planning_inputs','status':'verified source bytes; proposed scene boundaries only',
        'episode':'EP008-ai-implementation-service','duration_seconds':duration,'fps':fps,
        'frame_count':round(duration*fps),'word_count':len(words),
        'boundary_method':'nearest 24fps frame at inter-scene speech-gap midpoint; identity occupies existing S00/S02 gap; waveform and audiovisual review required before cuts',
        'canonical_gate_changes':False,'source_files':files,'scenes':scenes}
    save(RUN/'inputs/PLANNING-INPUTS.json',result)
    md=['# EP008 narration and provisional scene times','',
        'All 3,400 spoken tokens and seven locked hashes match. This is planning evidence, not a visual approval.','']
    for scene in scenes:
        md += [f"## {scene['scene_id']} {scene['title']} | {scene['proposed_in']:.3f}–{scene['proposed_out']:.3f}s",'']
        for para in scene['paragraphs']:
            md += [f"{para['paragraph_id']} | {para['first_word_id']}–{para['last_word_id']} | {para['speech_in']:.3f}–{para['speech_out']:.3f}",'',para['text'],'']
    (RUN/'inputs/NARRATION-MAP.md').write_text('\n'.join(md))
    print(json.dumps({'hashes_verified':len(expected),'spoken_tokens_verified':cursor,
        'scenes':len(scenes),'duration_seconds':duration,'frames':round(duration*fps),
        'planning_inputs_sha256':sha(RUN/'inputs/PLANNING-INPUTS.json')}))

if __name__=='__main__': main()
