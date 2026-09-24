from pathlib import Path
import hashlib
import json
import wave
import re

ROOT = Path('/Users/brownmanbrain/GitHub/operator-economy')
OUT = Path(__file__).resolve().parent
BASE = 'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/'
MASTER = BASE + 'master/narration-master.v4.wav'
TRANSCRIPT = BASE + 'word-transcript.json'
ACCEPTANCE = 'blueprint-cinema/experiments/EP007-PRESENTER-001/avatar-v5-gestures/ACCEPTANCE.json'
STYLE = 'operator-blueprint-v2/02-narration-production/prompts/NARRATOR-REGISTER.candidate-C4.google-gemini-tts.style-instructions.json'
CAL = 'operator-blueprint-v2/02-narration-production/tools/calibrate.py'
CAPTURE = 'operator-blueprint-v2/02-narration-production/tools/capture_n4b.py'
R35 = 'blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/hyperframes/reviews/r35-default-outcome-avatar/provider/'

def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

assert sha(MASTER) == 'd8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9'
assert sha(TRANSCRIPT) == 'f5decf2102d6cd565b89823e6fae38b2f4838c0984f7fce67f36c03cfa0f0ef7'
accepted = json.loads((ROOT / ACCEPTANCE).read_text())
refs = {k: accepted['recipe']['inputs'][k] for k in ['framing', 'rebecca_behavior', 'henry_articulation']}
for v in refs.values():
    assert sha(v['path']) == v['sha256']
assert sha(accepted['artifact']['path']) == accepted['artifact']['sha256']
words = json.loads((ROOT / TRANSCRIPT).read_text())['words']
his = [w for w in words if re.sub(r'[^a-z]', '', w['token'].lower()) == 'his']
assert len(his) == 0

# Both cuts are exactly on 24fps frame boundaries and integral 48kHz samples.
start_sample, end_sample = 12116000, 12368000
with wave.open(str(ROOT / MASTER), 'rb') as w:
    params = w.getparams()
    assert params.nchannels == 1 and params.sampwidth == 2 and params.framerate == 48000
    w.setpos(start_sample)
    pcm = w.readframes(end_sample - start_sample)
with wave.open(str(OUT / 'question-original.wav'), 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(48000)
    w.writeframes(pcm)
with wave.open(str(OUT / 'question-original.wav'), 'rb') as w:
    assert w.readframes(w.getnframes()) == pcm

spoken = 'What happens here if you are not around for a month. That is not small talk.'
prompt = '''One continuous six-second eye-level fixed-camera seated wide shot of the man in the IMAGE reference. Preserve his exact identity, glasses, navy shirt, softly daylit study, lighting and framing with both forearms and complete hands visible. This is an owner-authorized avatar of the person in both VIDEO references.

The first VIDEO supplies relaxed conversational facial settling, ordinary blinks, small asymmetric head-angle adjustments and comfortable stillness. The second VIDEO supplies clear public-facing articulation and brief emphasis that settles. Use them as complementary behavior references only. Do not copy their clothing, room, microphone, headphones, interview gaze, unrelated speech or mouth timing. The IMAGE controls identity and setting. The AUDIO controls the actual words and delivery.

Speak only this exact 5.25-second AUDIO reference, preserving the original voice, words, cadence and pauses: "What happens here if you are not around for a month. That is not small talk."

This is a thoughtful question to one attentive viewer. Begin naturally engaged near the lens with easy jaw and quiet hands. Through "if you are not around for a month," let a little consideration gather around the inner brows. Keep it restrained and conversational; do not become stern, worried or accusatory. The question is what matters, so no glance away, finger point or large hand gesture at its center. Ordinary blinks and small asymmetry are welcome. Do not freeze into a stare.

Through "That is not small talk," let the face become quietly certain as the explanation begins. Form the connected mouth shapes clearly without fixed teeth display, exaggerated open jaw or a held smile. Finish "talk" completely and settle the lips naturally. Do not repeat rhythmic nods, side tilts, head bobs or a gesture loop. A small one-time hand settling motion is sufficient if it arises naturally. Preserve the original audio pauses rather than slowing the voice to manufacture thoughtfulness.

The AUDIO is exactly 5.25 seconds including its source lead and tail. Finish it at its original pace and stay comfortably at rest until the six-second picture ends. Keep the camera fixed and wide so the editor can choose the crop. No generated camera move, cut, zoom, caption, title, logo, music, additional person or extra words.
'''
(OUT / 'AVATAR-PROMPT.txt').write_text(prompt)
save('AUDIO-EXTRACT.json', {
    'source': {'path': MASTER, 'sha256': sha(MASTER)},
    'master_in': start_sample / 48000, 'master_out': end_sample / 48000,
    'master_samples_half_open': [start_sample, end_sample],
    'review_in_before_pickup_shift': start_sample / 48000 - 3,
    'review_out_before_pickup_shift': end_sample / 48000 - 3,
    's08_local_in_before_pickup_shift': start_sample / 48000 - 250.625,
    's08_local_out_before_pickup_shift': end_sample / 48000 - 250.625,
    'duration_seconds': 5.25, 'frames_at_24fps': 126,
    'audio_format': '48000Hz mono signed16bitPCM WAV',
    'pcm_unchanged': True, 'gain_fade_retime_or_processing': 'none',
    'word_range': ['W000726', 'W000741'], 'spoken_text': spoken,
    'boundary_basis': {
        'start': 'Low-energy interval before audible-energy onset around252.50; transcript starts What at252.60 and is late relative to PCM onset. Start252.416667 preserves onset and preceding breath.',
        'end': 'Talk release continues beyond transcript257.48 through approximately257.60. End257.666667 lies in low-energy interval before next phrase onset around257.975.',
        'start_25ms_rms_window252_4': 51.7,
        'end_25ms_rms_window257_65': 8.3,
        'limitations': 'No exact-zero run exists at these seams. Energy inspection and exactPCM preservation are verified; native-speed listening and lip-sync remain review requirements.'
    },
    'output': {'path': str((OUT / 'question-original.wav').relative_to(ROOT)), 'sha256': sha(str((OUT / 'question-original.wav').relative_to(ROOT)))}
})
save('AVATAR-TAKE-PLAN.json', {
    'status': 'prepared_not_submitted', 'take_id': 'r38-s08-question-v5',
    'picture_audio_mode': 'presenter_address', 'face_function': 'presenter_delivery',
    'language_carrier': 'presenter', 'visible_speech': 'presenter_synced',
    'spoken_text': spoken, 'audio': 'question-original.wav',
    'references': refs, 'baseline_acceptance': {'path': ACCEPTANCE, 'sha256': sha(ACCEPTANCE)},
    'generation_parameters': {'model':'seedance_2_5','mode':'omni_reference','duration':6,'resolution':'1080p','aspect_ratio':'16:9','bitrate_mode':'high','generate_audio':True,'count':1,'use_unlim':False},
    'prompt_path': 'AVATAR-PROMPT.txt',
    'provisional_cost_basis': {'higgsfield_credits':54,'fresh_quote_required':True,'prior_source':R35+'HIGGSFIELD-COST-PREFLIGHT.json','restoration_model':'fal-ai/sync-lipsync/v3','prior_usd_per_minute':8,'six_second_estimate_usd':0.8,'suggested_restoration_cap_usd':1,'prior_price_source':R35+'FAL-PRICE-PREFLIGHT.json'},
    'paid_calls': 0, 'paid_retries_proposed': 0,
    'integration': ['Measure source audio offset from at least three speech windows after any restoration.', 'Requested picture: master252.583333 through257.875, 127 continuous frames at24fps. Source selection begins0.166667 seconds into the matched audio and ends0.208333 seconds after its end. Preserve natural post-speech rest; do not repeat a frame.', 'A6-second native source covers that picture only if its measured audio insertion offset is at most0.541667 seconds. Verify actual duration and coverage after generation.', 'Review quiet eyebrow progression in chosen crop at normal speed; waveform alignment does not certify lip movement.', 'Keep reference-audio local0 tied to source master252.416667 even if callback pickup shifts absolute review time.'],
    'camera': 'Fixed generated wide. Editorial crop is a root directing choice; no unmotivated mid-sentence cut is required.',
    'authorization': 'New generation and optional one restoration require current explicit scoped authority; R35 receipt is cost precedent only.'
})

style = json.loads((ROOT / STYLE).read_text())['style_instructions']
callback = 'Back to his question, then.'
context_read = callback + ' ' + spoken
settings = {'similarity_boost':0.8,'speed':1.0,'stability':0.4,'style':0.0,'use_speaker_boost':True}
guide = lambda text: {'advancedVoiceOptions':{'enableTextnorm':False},'audioConfig':{'audioEncoding':'LINEAR16','sampleRateHertz':24000},'input':{'prompt':style,'text':text},'voice':{'languageCode':'en-US','modelName':'gemini-2.5-pro-tts','name':'Algieba'}}
save('CALLBACK-PICKUP-REQUEST.json', {
    'status': 'proposal_not_authorization_not_submitted',
    'owner_requested_replacement': callback,
    'original': {'master_word_id':'W000723','spoken_token':'her','master_range':[251.26,251.44]},
    'existing_word_transplant_audit': {'word_count':len(words),'standalone_his_count':len(his),'conclusion':'No whole-word his donor exists in the locked master transcript. Do not synthesize a phoneme splice.'},
    'actual_original_recipe': {'config':'n3-two-stage-acted-guide-v2','register':'candidate-C4','guide_voice':'Algieba','transfer_identity':'Original C'},
    'short_pickup_risk': 'Local calibration notes flag isolated short takes as liable to drift in pace and level; a prior3.65-second tail was2.1dBhot. No new pickup can be called matched before listening.',
    'selected_context_bearing_request': {'purpose':'Produce callback in connected delivery using following unchanged text as context; integrate only callback, keep locked question recording.', 'guide_endpoint':'https://us-texttospeech.googleapis.com/v1/text:synthesize','body':guide(context_read),'spoken_character_count':len(context_read),'calls':1,'no_short_take_first':True,'not_additional_authority':'One chosen contextual take, not an exact-short-take followed by a retry.'},
    'transfer': {'method':'POST multipart/form-data','url':'https://api.elevenlabs.io/v1/speech-to-speech/scMbPZwQjr40V1MzL3Nj?output_format=pcm_48000&enable_logging=true','fields':{'model_id':'eleven_multilingual_sts_v2','remove_background_noise':'false','seed':'2026082501','voice_settings':json.dumps(settings,sort_keys=True),'file_format':'other'},'file':'Exact guide WAV produced by selected option; hash before transfer.'},
    'spend': {'guide_calls_proposed':1,'voice_transfer_calls_proposed':1,'automatic_retries':0,'current_price_verified':False,'cost_basis':'Original recipe and text count are local facts. No current Google or ElevenLabs pricing is stored with the EP007 capture. Root must obtain a current read-only rate/estimate before quoting a dollar bound.'},
    'existing_helper': {'path':CAL,'important_override':'guide/chain --voice Algieba; calibrate.py default Achird is not this episode recipe','execute_boundary':'Helper has no authorization latch. Do not add --execute before root current scoped authorization and preserve receipts.'},
    'integration_contract': {
        'preserve_master': True, 'preserve_original_callback': True,
        'candidate_only': True,
        'available_callback_interval_master':[250.625,252.41666666666666],
        'available_callback_seconds':1.7916666666666667,
        'preferred_first_word_master_anchor':250.98,
        'after_pickup': 'Keep original audio from master252.416667 onward untouched and preserve its internal timing.',
        'fit': 'If naturally spoken callback plus a clean trailing pause fits1.791667s, keep all existing later review cues.',
        'overflow': 'If it does not fit naturally, extend only S08 callback by an integral24fps frame count delta. Shift the avatar and every laterS08 audio/visual cue by the same delta. Preserve R36prefix0–247.625 and master source coordinates.',
        'prohibited': ['No time-stretch to squeeze into the old slot.','No phoneme fabrication.','No silent master replacement.','No new questionaudio substitution when only callback is being corrected.'],
        'review': ['Listen against neighboring originalvoice for timbre/pace/level.', 'Check exact words and finalthen release.', 'Trim context at a real low-energy sentenceboundary.', 'Use crossfades only in non-speech roomtone if needed; retain originalsourceclips and derivation.', 'Save a versioned candidate audiooverride and offsetmap; canonical narrationrevision is a separate controlled action.']
    }
})
save('GOOGLE-CALLBACK-GUIDE-BODY.json', guide(context_read))
(OUT / 'CALLBACK-CONTEXT-TEXT.txt').write_text(context_read + '\n')

inputs = [MASTER, TRANSCRIPT, ACCEPTANCE, BASE+'take-register.json', STYLE, CAL, CAPTURE, R35+'HIGGSFIELD-REQUEST.json', R35+'HIGGSFIELD-COST-PREFLIGHT.json',R35+'FAL-PRICE-PREFLIGHT.json'] + [v['path'] for v in refs.values()]
pins = [{'path':p,'sha256':sha(p)} for p in inputs]
save('WORK-ORDER-INPUTS.json', {'work_order_id':'r38-audio-plan','episode_folder':'EP007-exit-readiness-prep','role':'source_audio_and_presenter_take_planner','input_hashes':pins,'owned_output_path':str(OUT.relative_to(ROOT)),'permission_boundary':'Local reads and owned packet files only; no uploads, provider calls, media generation, runtime edits, canonical edits, skill edits or shared decision log writes.','acceptance_checks':['Source and V5 input hashes match','Exact sourcePCM extract reproduced','Standalonehis donor audit complete','Requestparameters trace to actualEP007 recipe','No externalpaid actions'],'stopping_conditions':['Any input hash differs','Packet requires provider execution']})
files = [p for p in OUT.iterdir() if p.is_file() and p.name != 'deliverable.json']
save('deliverable.json', {
    '$schema':'../../../../../schemas/agent-deliverable.schema.json','schema_version':'1.0.0','workflow_version':'blueprint-cinema-1.0','work_order_id':'r38-audio-plan','episode_folder':'EP007-exit-readiness-prep',
    'input_hashes_used':pins,'files_produced':[str(p.relative_to(ROOT)) for p in files],
    'checks':[{'command':'Recompute issued master and transcript hashes plus V5 reference and accepted media hashes','outcome':'pass'},{'command':'Compare extracted WAV PCM bytes with original half-open sample interval12116000:12368000','outcome':'pass'},{'command':'Search all3186 transcript tokens for standalonehis','outcome':'pass'},{'command':'Read actual EP007 capture recipe and original provider request parameters','outcome':'pass'},{'command':'Native-speed listening or perceptual lip-sync review','outcome':'not_run'},{'command':'Current Google ElevenLabs Higgsfield and fal pricing verification','outcome':'not_run'}],
    'sources_and_provenance':['Only local locked narration, acceptedV5 references, source recipes and previous request receipts were read.','Local original-audio excerpt preserves exactPCM; no synthetic generation performed.'],
    'assumptions':['Review clock before any pickup extension is master minus3seconds after the accepted silence removal.','Current owner correction authorizes planning a new callback; original pinned master remains preserved.'],
    'unresolved_questions':['Fresh provider quotes and current scoped spend authorization remain root responsibilities.','Pickup length/timbre and actual avatar lip-sync remain unknown before generation and playback.','BlueprintCinema EP007 README,episode.json,input-lock.json do not exist; source pins and private review context supplied by root were used.'],
    'external_writes':False,'paid_services':False,'synthetic_generation':False,'approval_claimed':False,'production_state_changed':False,'status':'complete'
})
print('Packet prepared; no provider calls.')
