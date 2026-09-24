# Presenter Reference Kit

A set of short clips of Manav, shot on purpose, that teach the presenter model how he moves. They replace the two behavior clips the EP009 recipe borrowed from call recordings (`presenter/PRESENTER-PLAN.json` `reference_media.video_references`). The prompt had to tell the model to ignore those clips' headphones, microphone, screen-call gaze and unrelated speech. Clips shot for the job need no such exclusions.

What the kit is for:

- **Behavior references:** passed as `video_references` to Seedance 2.5 `omni_reference`. The IMAGE (the locked look) still controls identity, outfit and room, and the AUDIO (locked VO) controls words and timing. The kit only supplies how his face settles, how his mouth moves and how his hands move.
- **Hold and gap footage:** K08 is real listening behavior, which is the case where generated takes freeze (EP009 P08's 208 ms held pose).
- **Motion-transfer test material,** if we try driving the presenter from a read-along later.

Shoot it once. Reshoot only if the accepted likeness changes: new glasses, beard, haircut. The look (room and outfit) changes every episode; the kit doesn't.

## Setup

| | |
|---|---|
| Camera | Phone rear camera, main 1x lens (not ultrawide), 4K. Lock exposure and focus on the face. |
| Frame rate | 24 fps, matching the episode timeline. Turn off Action Mode and Cinematic mode. |
| Position | Seated, eye level, lens roughly 1.5–2 m away. Frame from the top of the head to mid-thigh so both forearms and complete hands stay in frame. This matches the presenter framing the recipe asks for. |
| Eyes | Into the lens, not at a screen. Tape a small mark next to the lens if that helps. |
| Light | Soft window or softbox light about 45° to one side, a little above eye level. No light behind him. No overhead fluorescents. |
| Background | Plain and uncluttered. It gets discarded; it only has to stay out of the way. |
| Wardrobe | Solid mid-tone shirt, no logo or pattern. Glasses on if the likeness wears them. No headphones, no visible mic. |
| Sound | Record it: a lav, or the phone within about 1 m. It lets us check mouth shapes against sound; the voice itself is not used. |
| Takes | Two takes of each clip. Leave 2 s of stillness before and after each line. |

## The clips

Aim for 8–15 s per clip. Say the lines at presenting pace, slightly slower than conversation. These lines are reference only and never publish.

**K01 — Neutral delivery.** Calm, level, direct to lens.
> Most small businesses don't lose money in one big mistake. They lose it in the handoffs nobody owns. That's where we're looking today.

**K02 — Explaining with hands.** Place each step in the air, left to right from the viewer's side. Palms open.
> Here's the system. A request comes in over here. Someone checks it here. The answer goes back out here. Each step has one owner.

**K03 — Serious caution.** Slight lean in, slower, no smile.
> This is the part people skip. If nobody checks the output, the automation just makes the same mistake faster.

**K04 — First-person admission.** A small, genuine half-smile on "broke on me", then back to level.
> I'll be honest, the first version of this broke on me. Twice. Here's what I changed.

**K05 — Question to the viewer.** Eyebrows lift on the question, then settle for the answer.
> So why would anyone pay for this? Because the alternative is doing it by hand, every week, for as long as you run the business.

**K06 — Emphasis on a turn.** Short pause before "the follow-up". One hand lands on the table with it.
> The tool isn't the business. The follow-up is the business.

**K07 — Think, then speak.** Hold 2 s looking slightly off-lens, as if checking something. Come back to the lens, then:
> Let's check whether that actually holds up.

**K08 — Listening, silent, 15 s.** No words. Neutral attention toward the lens, natural blinks, one or two small nods, a small breath. Don't freeze and don't perform.

**K09 — Angles, silent, 12 s.** Slow head turn about 30° to his left, back to center, 30° to his right, back to center, chin slightly up, slightly down, center. Eyes lead each turn.

**K10 — Lean and settle.** Start sitting back. Lean in on the first line, sit back on the second.
> Here's the move. Then give it a week and see what changed.

**K11 — Mouth-shape drill.** Slow and deliberate, full closures on p/b/m. A pause between groups.
> Pay. Buy. Map. — Five. Very. — Think. Then. — Who. You. Move. — See. Me. Need. — Ah. How. Now.

**K12 — Relaxed aside.** Looser, conversational, a little faster. Slight shrug on "honestly".
> Honestly, most of this is boring. That's the point. Boring is what keeps running when you're not watching.

## After the shoot

1. Copy the raw files to `blueprint-cinema/references/presenter-kit/<YYYY-MM-DD>/K01-a.mov`, `K01-b.mov`, and so on. Video files under `blueprint-cinema/` are gitignored, so raw face footage never reaches the public repo.
2. Pick the better take of each and write `presenter-kit/<YYYY-MM-DD>/SELECTS.json`: clip ID, file, sha256, in/out seconds, and one line on what it teaches.
3. Trim each select to its in/out points. Keep them under 15 s, because the model takes short references, not long footage.
4. Run a bounded test before any episode uses the kit. Take one existing EP009 line, the locked look still and the locked VO. Render it twice through `oe-cinema generate --lane presenter`, once with the old call-recording references and once with K01 + K08. Compare lip closure, blink rhythm, hand motion and held-pose gaps. Adopt the kit only if it wins.
5. Once adopted, the kit selects become the standing `video_references` in the presenter recipe. Upload them once and reuse the hosted URLs. They are behavior references, not look references, so the look lock doesn't govern them.

## Notes

- Seedance has accepted real-face video references: EP009's behavior clips were real recordings. Photo references of real faces are what its filter rejects, so the kit goes in as video, never as stills.
- Uploading this footage gives the provider real face video of Manav. Higgsfield's terms let it train on uploaded content. Decide whether that's acceptable before step 5.
- The YouTube altered/synthetic media disclosure still applies to every episode with a generated presenter.
