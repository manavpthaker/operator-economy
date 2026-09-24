# EP006 90-second HyperFrames candidate

This is the native HyperFrames side of an isolated runtime comparison. It is not a port of the Remotion composition and it does not alter Blueprint Cinema production state.

Both treatments use the same locked EP006 narration and the same 0–90 second content window. The Remotion deck is the control. This candidate follows HyperFrames' `faceless-explainer` workflow and uses nine editorial motion frames: a physical guest/key hook, a restrained proof placeholder, a three-stop guest journey, audit-first recovery, a show-identity card, an episode-title card, a fair OTA acquisition sequence, the guarded after-stay thesis, and the disconnected-work accumulation.

No generated voice, BGM, SFX, captions, stock, AI imagery, platform UI, or vendor logo is used. `audio_meta.json` routes the hash-verified full EP006 narration through the assembler's only full-duration audio lane; despite that lane's field name, the file is narration, not background music.

Generated and ignored paths include `assets/ep006-locked-vo.mp3`, `.hyperframes/`, `snapshots/`, `renders/`, and `node_modules/`.

Commands:

```bash
python3 stage_locked_vo.py
node ../../../../.agents/skills/faceless-explainer/scripts/frame-packets.mjs --project "$PWD" --storyboard "$PWD/STORYBOARD.md"
node ../../../../.agents/skills/faceless-explainer/scripts/assemble-index.mjs --storyboard "$PWD/STORYBOARD.md" --hyperframes "$PWD"
node ../../../../.agents/skills/faceless-explainer/scripts/transitions.mjs inject --storyboard "$PWD/STORYBOARD.md" --hyperframes "$PWD"
node ../../../../.agents/skills/faceless-explainer/scripts/transitions.mjs verify --storyboard "$PWD/STORYBOARD.md" --index "$PWD/index.html"
npm run lint
npm run check
npm run snapshot
npm run render:high
```

The operator-facing comparison output and exact results are recorded in the EP006 review folder after both renders are probed.
