"""Prepare the one owner-authorized S17 C take; no paid operations."""
from pathlib import Path
import datetime, hashlib, json, subprocess, wave

D = Path(__file__).resolve().parent
R = next(p for p in D.parents if (p / '.agents').is_dir())
E = D.parents[1]
H = E / 'hyperframes/reviews/r76-s17-presenter'
P = H / 'provider'
P.mkdir(parents=True, exist_ok=True)
(P / 'audio').mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, obj):
    with p.open('x') as f: json.dump(obj, f, indent=2); f.write('\n')
def pin(p): return {'path': str(p.relative_to(R)), 'sha256': sha(p)}

plan = E / 'direction/r62-s17-fixed-fee/presenter/PRESENTER-PLAN.json'
assert sha(plan) == '2134689bb68e5d44c47de3d0c4590bb6b638b60a516c40369068ba5a81457ccd'
master = R / 'operator-blueprint-v2/episodes/EP007-exit-readiness-prep/02-narration-production/master/narration-master.v4.wav'
assert sha(master) == 'd8f7cb9630ae12ad427dca2c7bd1f29611f56c7985ce900ea312df3b9fec8da9'
avatar = R / 'blueprint-cinema/experiments/EP007-PRESENTER-001'
accepted = json.loads((avatar / 'avatar-v5-gestures/ACCEPTANCE.json').read_text())
refs = {k: accepted['recipe']['inputs'][k] for k in ('framing', 'rebecca_behavior', 'henry_articulation')}
for rec in refs.values(): assert sha(R / rec['path']) == rec['sha256']
audio = P / 'audio/c.wav'
with wave.open(str(master), 'rb') as src:
    assert src.getframerate() == 48000 and src.getnchannels() == 1 and src.getsampwidth() == 2
    src.setpos(37176000)
    pcm = src.readframes(384000)
with wave.open(str(audio), 'wb') as out:
    out.setnchannels(1); out.setsampwidth(2); out.setframerate(48000); out.writeframes(pcm)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(audio),'-c:a','libmp3lame','-b:a','192k',str(P/'audio/c.mp3')], check=True)
auth = {'record_type':'generation_authorization', 'at':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'owner_statement':'yea that works', 'interpretation':'Owner accepts the immediately preceding explanation and priced proposal for S17 C. One new nine-second presenter generation and one original-narration restoration; resulting eight-second edit remains subject to review.', 'scope':'S17 C only, master 774.5–782.5, existing EP007 V5 look and behavior references.', 'caps':{'higgsfield_credits':90,'fal_usd':1.6,'retries':0}, 'proposal':pin(plan), 'master':pin(master), 'audio_wav':pin(audio), 'audio_mp3':pin(P/'audio/c.mp3'), 'reference_inputs':refs, 'balance_before_credits':527, 'accepted_surroundings_unchanged':True}
save(D/'AUTHORIZATION.json',auth)
prompt = '''One continuous nine-second eye-level fixed-camera seated wide shot of the man in the IMAGE reference. Preserve his identity, glasses, navy shirt, softly daylit study, lighting and framing with both forearms and complete hands visible.

The first VIDEO supplies relaxed conversational facial settling, ordinary blinks and comfortable stillness. The second VIDEO supplies connected public-facing articulation. They are behavior references only. Do not copy their clothing, room, microphone, headphones, screen-call gaze, unrelated speech or mouth timing. The IMAGE controls identity and setting. The AUDIO controls words, voice, cadence and pauses.

Speak only the exact eight-second AUDIO reference: "I am not going to name states, because the line moves and I am not your lawyer. That is a real piece of homework for wherever you are."

Lip sync is the priority: mouth shapes match every syllable of the AUDIO precisely and close fully on pauses. Plain, candid, direct address to one viewer near the lens. Head steady, expression level and open, no smile on the disclaimer, no head shake, wagging finger, shrug, theatrical brow raise or apologetic look. Hands rest comfortably until the final thought. On "homework for wherever you are", one hand opens in a small relaxed palm-up gesture near the tabletop, then returns to rest after the final word. Keep the other hand relaxed. Follow the supplied voice timing without stretching the speech. No repeated beats or compulsory glances.

Hold quietly after the final word through nine seconds. Natural breathing and blinking; hands and fingers remain anatomically consistent. Camera, background and light remain still. No cut, zoom, caption, title, logo, music, extra words, additional person or extra objects.'''
(D/'PROMPT.txt').write_text(prompt+'\n')
params={'model':'seedance_2_5','mode':'omni_reference','duration':9,'resolution':'1080p','bitrate_mode':'high','generate_audio':True,'use_unlim':False,'aspect_ratio':'16:9','count':1,'medias':[{'role':'image','value':'875a3997-b5c7-4410-9487-309a8c7740df'},{'role':'video','value':'7dc478bc-0449-4867-a760-50670f4caccf'},{'role':'video','value':'5ec537ee-b01c-4bb5-a343-636882e4b747'}], 'prompt':prompt, 'declined_preset_id':'24bae836-2c4a-48e0-89b6-49fcc0b21612'}
save(P/'PARAMS-WITHOUT-AUDIO.json',params)
event={'event_id':'r76-s17-c-generation-authorized-v1','decision_id':'s17-fixed-fee','event_type':'feedback','tags':['presenter-return','paid-authorization'],'data':{'decision_event_id':'r62-s17-plan-v1','actor':'owner','verbatim':'yea that works','interpretation':auth['interpretation'],'verdict':'accept','scope':auth['scope']+' Approval of proposal and bounded spend, not acceptance of an ungenerated take.', 'artifact_hashes':[pin(plan),pin(D/'AUTHORIZATION.json')]},'evidence':[dict(pin(D/'AUTHORIZATION.json'),locator='Current owner authorization and exact bounded inputs')]}
save(D/'AUTHORIZATION-EVENT.json',event)
print(json.dumps({'audio':pin(audio),'authorization':pin(D/'AUTHORIZATION.json'),'provider':str(P)}))
