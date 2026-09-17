"""Build TAKE-PLAN.json and per-part AVATAR-PROMPT.txt for the EP009 presenter regeneration."""
import json, math
from pathlib import Path
G = Path(__file__).resolve().parents[1]; B = G.parent
R = next(x for x in G.parents if (x / '.agents').is_dir())
SHOT = json.loads((B / 'direction/SHOT-PLAN.json').read_text())
TAKES = {t['take_id']: t for t in SHOT['presenter_takes']}
WT = json.loads((R / 'operator-blueprint-v2/episodes/EP009-direct-booking-recovery/02-narration-production/word-transcript.json').read_text())['words']
SR = 48000
HI = {'P02', 'P03', 'P04', 'P06', 'P08', 'P10', 'P11', 'P12'}
# cut frames (k/24) chosen inside measured master silence, see TAKE-PLAN.json split_method
CUTS = {'P02': [1912], 'P03': [4674], 'P07': [12569], 'P08': [16225, 16345], 'P11': [28468], 'P12': [28906], 'P13': [29372]}
GAP = {1912: [79.40, 79.965], 4674: [194.57, 194.95], 12569: [523.57, 523.825], 16225: [675.91, 676.22], 16345: [680.84, 681.23], 28468: [1185.955, 1186.375], 28906: [1204.065, 1204.74], 29372: [1223.655, 1224.035]}
NUM = {5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen'}
# one gesture at most per part; kind + the phrase it sits on + sentence for the prompt
PERF = {
 'P01':  ('look-away', "I couldn't find anyone", 'On "I couldn\'t find anyone" his eyes drop briefly down to his left as he recalls the search, then return to the lens by "selling it" and stay there. Hands rest on the table throughout. The question "So what did that second stay actually cost her, and who gets paid to stop it?" is delivered still, with a light gathering of the inner brows.'),
 'P02a': ('none', None, 'Hands rest on the table throughout with no gesture. Eyes stay near the lens.'),
 'P02b': ('small-lift', 'four numbers', 'Hands rest on the table through "By the end you\'ll be able to take". On "four numbers" his right hand lifts a few centimetres off the table, then settles back to rest by "small property" and stays there. Eyes stay near the lens: this is a promise.'),
 'P03a': ('open-palm', "keeps the guest's email", 'Hands rest on the table through "The site introduces the guest". On "keeps the guest\'s email" his left hand opens slightly, palm up, then settles back to rest.'),
 'P03b': ('none', None, 'Hands rest on the table throughout with no gesture. On "can somebody from outside get paid to do it?" the inner brows gather lightly, pensive rather than challenging, and he stays near the lens.'),
 'P04':  ('flat-hand-lower', 'is a number', 'Hands rest on the table through "But only for what it recovers, and what it recovers". On "is a number" his right hand, held flat, lowers a few centimetres and comes to rest on the table, and stays there. Eyes near the lens for "By the end you\'ll be able to compute it for any inn."'),
 'P05':  ('both-palms-up', 'just do it', 'Hands rest on the table through "If the parts to fix this are cheap, why doesn\'t the inn". On "just do it" both palms turn up a few centimetres together, then return to rest immediately.'),
 'P06':  ('hand-to-chest', 'I could not find anyone', 'On "I could not find anyone" his right hand touches lightly to his chest and returns to the table by "twenty room inn", then both hands rest with no further gesture.'),
 'P07a': ('none', None, 'Hands rest on the table throughout with no gesture.'),
 'P07b': ('set-aside', "It's the wrong number", 'On "It\'s the wrong number" one hand makes a small sideways motion just above the table, as if setting something aside, then settles back to rest by "because" and stays there.'),
 'P08a': ('small-lift', 'four properties', 'Hands rest on the table through "Director of Customer Experience at Coqui Coqui". On "four properties" his right hand lifts slightly off the table, then settles back to rest and stays there.'),
 'P08b': ('look-away', "I've never owned a hotel", 'A quiet, candid admission. On "I\'ve never owned a hotel" his eyes drop briefly down and away, then return to the lens by "revenue manager" and stay there. Hands rest on the table throughout.'),
 'P08c': ('open-palm', "That's the test", 'Hands rest on the table through "I don\'t know what a thirty room inn will pay to fix it." On "That\'s the test" one hand opens slightly, palm up, then settles back to rest before "the pitch".'),
 'P09':  ('none', None, 'Hands rest on the table throughout with no gesture. Level, plain delivery near the lens.'),
 'P10':  ('small-lift', 'Up the band', 'Hands rest on the table and the head stays still through "That\'s a side income. It\'s a foothold. It is not a living." On "Up the band" his right hand, palm down, rises one small step of about ten centimetres, then returns to rest.'),
 'P11a': ('none', None, 'Hands rest on the table throughout with no gesture. Settled, direct, near the lens on "My verdict is build. Bounded."'),
 'P11b': ('flat-hand-lower', 'the audit is the test', 'Hands rest on the table through "And the arithmetic at the bottom of the band is thin". On "the audit is the test" his right hand, held flat, lowers a few centimetres onto the table and stays there.'),
 'P12a': ('hand-to-chest', 'including me', 'Hands rest on the table through "Nobody knows that yet". On "including me" his right hand touches lightly to his chest and returns to rest. Near the lens and still for "You\'ll know by day thirty."'),
 'P12b': ('small-lift', 'Ask for four numbers', 'Hands rest on the table through "Find one innkeeper you already know." On "Ask for four numbers" his right hand lifts a few centimetres off the table, then settles back to rest for "Run the ceiling."'),
 'P13a': ('open-palm', "ask if they'd pay you", 'On "ask if they\'d pay you to fix it" one hand opens slightly toward the lens, palm up, then settles back to rest by "Not to close them." and stays there.'),
 'P13b': ('none', None, 'Hands rest on the table throughout with no gesture. Still and near the lens on "Right now nobody knows.", then settled and relaxed for the ask, with no announcer lift and no pointing.'),
}
TEMPLATE = """One continuous {dur_word}-second eye-level fixed-camera seated wide shot of the man in the IMAGE reference. Preserve his identity, clear-framed glasses, light blue chambray button-down with the sleeves rolled to the forearm, the small country inn breakfast room with its wooden tables and chairs, soft daylight from the side window, lighting and framing with both forearms and complete hands visible on the wooden table. He sits naturally and relaxed, shoulders easy, neither stiff and upright nor slouched.

The first VIDEO supplies relaxed conversational facial settling, ordinary blinks and comfortable stillness. The second VIDEO supplies connected public-facing articulation. They are behavior references only. Do not copy their clothing, room, microphone, headphones, screen-call gaze, unrelated speech or mouth timing. The IMAGE controls identity and setting. The AUDIO controls words, voice, cadence and pauses.

Speak only the exact {audio_s:.2f}-second AUDIO reference: "{words}"

Lip sync is the priority: mouth shapes match every syllable of the AUDIO precisely and close fully on the pauses. Keep the head steady and facing the lens, with only the small movement that speech stress causes; no sway, tilt, turn or repeated nod. {perf} Hold still until the picture ends with no extra words.

No finger point, head shake, smirk, raised-brow performance or theatrical surprise. Keep the camera fixed and wide. No camera move, cut, zoom, caption, title, logo, music, additional person or extra objects.
"""
def words_in(t0, t1):
    return ' '.join(w['token'] for w in WT if t0 <= (w['start'] + w['end']) / 2 < t1)
parts = []
for tid, t in TAKES.items():
    f0, f1 = round(t['master_in'] * 24), round(t['master_out'] * 24)
    bounds = [t['master_in']] + [c / 24 for c in CUTS.get(tid, [])] + [t['master_out']]
    n = len(bounds) - 1
    for i in range(n):
        pid = tid if n == 1 else tid + 'abc'[i]
        a, b = round(bounds[i], 6), round(bounds[i + 1], 6)
        samples = int(round(b * SR)) - int(round(a * SR)); aud = samples / SR
        gen = math.ceil(aud) + 1; res = '1080p' if tid in HI else '720p'; rate = 9 if res == '1080p' else 6.5
        segs = [s for s in t['segment_ids'] if next(x for x in SHOT['segments'] if x['id'] == s)['master_in'] < b - 1e-6 and next(x for x in SHOT['segments'] if x['id'] == s)['master_out'] > a + 1e-6]
        kind, phrase, perf = PERF[pid]
        w = words_in(a, b)
        prompt = TEMPLATE.format(dur_word=NUM[gen], audio_s=aud, words=w, perf=perf)
        d = G / pid; d.mkdir(exist_ok=True); (d / 'AVATAR-PROMPT.txt').write_text(prompt)
        cut_in = CUTS.get(tid, []) and i > 0 and CUTS[tid][i - 1]
        parts.append({'part_id': pid, 'take_id': tid, 'segment_ids': segs, 'master_in': a, 'master_out': b, 'samples': samples, 'audio_seconds': round(aud, 6),
                      'generation_seconds': gen, 'resolution': res, 'credits_per_second': rate, 'est_credits': gen * rate, 'words': w,
                      'gesture': {'kind': kind, 'phrase': phrase}, 'prompt': str((d / 'AVATAR-PROMPT.txt').relative_to(R)),
                      'cut_in': ({'frame': cut_in, 'master_seconds': round(cut_in / 24, 6), 'silent_run_below_minus40_dbfs': GAP[cut_in]} if cut_in else None)})
tot = sum(p['est_credits'] for p in parts)
plan = {'record_type': 'presenter_regen_take_plan', 'episode': 'EP009-direct-booking-recovery', 'source_contract': 'direction/SHOT-PLAN.json presenter_takes (ranges and words unchanged)',
        'look': {'id': 'L3-chambray', 'image_reference': '173ee5c5-012c-4313-8b8f-13f93db6255c', 'path': 'blueprint-cinema/experiments/EP009-FULL-BUILD-001/presenter-regen/look/L3-chambray.png', 'sha256': '0b529748f457774986e661dcfe31e916ad9507c8f7cf4803171cb602a012d7c5'},
        'behavior_references': ['7dc478bc-0449-4867-a760-50670f4caccf', '5ec537ee-b01c-4bb5-a343-636882e4b747'],
        'provider': {'model': 'seedance_2_5', 'mode': 'omni_reference', 'aspect_ratio': '16:9', 'generate_audio': True, 'restoration': 'fal-ai/sync-lipsync/v3 sync_mode silence on the median-offset-trimmed native'},
        'split_rule': 'Passages over 11.5 s of audio split into parts of at most about 11.5 s at a silent gap of at least 0.25 s; generation_seconds = ceil(part audio) + 1.',
        'split_method': 'Candidate gaps from word-transcript.json word boundaries, confirmed on the master waveform as runs of 5 ms RMS blocks below -40 dBFS (breath and room tone sit between -40 and -55 dBFS in this master, so the -55 dBFS cut rule finds no gap in P02 or P08). Each cut is the 1/24 s frame nearest the run centre, preferring sentence ends over balance.',
        'split_notes': {
            'P02': 'Only sentence gap: "meet them again." / "By the end" (79.40 to 79.965, a breath at -41 to -47 dBFS). 6.125 + 8.167 s.',
            'P03': 'Cut after "email." (0.38 s) rather than the more balanced "back," (0.26 s, mid sentence). 6.083 + 10.333 s.',
            'P07': 'Both sentence gaps measure about 0.25 s ("stops." 523.57 to 523.825; "sites." 528.69 to 529.0 with a click at 528.92). Chose "stops." for the clean run. 3.292 + 8.542 s. Gap is at the 0.25 s floor.',
            'P08': 'Three parts, not two: the only gap near the middle ("manager," 678.685 to 678.98) leaves a 12.25 s first part, over the 11.5 s limit. Sentence ends "ago." and "anybody." give 9.458 + 5.0 + 8.417 s for 9 more credits than the two-part split. The middle part is the admission, which the r1 crop plan also isolated.',
            'P11': 'Cut after "The parts are cheap." (1185.955 to 1186.375) gives 11.125 + 10.292 s; the SHOT-PLAN fallback after "direct." would leave an 11.83 s second part.',
            'P12': 'Cut on the seg072/seg073 boundary (after "day thirty.", 0.67 s gap). 7.958 + 9.458 s.',
            'P13': 'Cut after "their size." (1223.655 to 1224.035) gives 9.958 + 9.769 s; the seg074/seg075 boundary would leave a 12.0 s first part. seg075 continues part b.'},
        'expected_vs_actual_parts': {'expected': 20, 'actual': len(parts), 'difference': 'P08 in three parts (see split_notes.P08)'},
        'parts': parts,
        'totals': {'parts': len(parts), 'generation_seconds': sum(p['generation_seconds'] for p in parts), 'est_credits': tot,
                   'est_fal_usd_upper': round(sum(p['generation_seconds'] for p in parts) * 8 / 60, 2)}}
(G / 'TAKE-PLAN.json').write_text(json.dumps(plan, indent=2) + '\n')
for p in parts: print(p['part_id'], p['segment_ids'], p['master_in'], p['master_out'], round(p['audio_seconds'], 3), p['generation_seconds'], p['resolution'], p['est_credits'], p['gesture']['kind'], '|', p['words'][:60])
print(plan['totals'])
