"""EP009 act 4 fix round 1 helpers (copied into each act 4 project's tools/).

Scenes chain: each scene module exposes scene() -> dict(body, lines, ids, css, dur). A later scene includes the
earlier scene's body and replays its timeline to progress(1) at load, so its frame 0 is the earlier scene's exact
last frame (no hand-copied end state)."""
import importlib.util
import json
from pathlib import Path

from act4lib import HEAD, TL, kit_defs  # noqa

SCENES = Path(__file__).resolve().parents[2]


def load_scene(project):
    p = SCENES / project / 'tools/build.py'
    spec = importlib.util.spec_from_file_location('scene_' + project.replace('_', ''), p)
    m = importlib.util.module_from_spec(spec)
    import sys
    sys.path.insert(0, str(p.parent))
    spec.loader.exec_module(m)
    return m.scene()


class TL2(TL):
    def mv(self, sel, at, a, b, d=.8, ease='power2.inOut'):
        """Move a wrapper <g transform="matrix(1,0,0,1,0,0)"> so its child, placed at a=(x,y,s), ends at b=(x,y,s).
        Attribute tween (seek-safe, no svgOrigin compensation)."""
        k = b[2] / a[2]
        x, y = b[0] - k * a[0], b[1] - k * a[1]
        self.lines.append(f"t.to('{sel}',{{attr:{{transform:'matrix({k:.4f},0,0,{k:.4f},{x:.2f},{y:.2f})'}},duration:{d},ease:'{ease}'}},{at});")

    def dim(self, sel, at, o=.3, d=.5):
        self.lines.append(f"t.to('{sel}',{{opacity:{o},duration:{d},ease:'power1.inOut'}},{at});")


DRAW = ("const draw=(sel,at,d)=>{document.querySelectorAll(sel).forEach(p=>{const L=Math.ceil(p.getTotalLength())+2;"
        "t.set(p,{autoAlpha:1,strokeDasharray:L+' '+L,strokeDashoffset:L},at);t.to(p,{strokeDashoffset:0,duration:d,ease:'power1.inOut'},at);"
        "t.set(p,{strokeDasharray:'none'},at+d+.01);});};\n")


def prelude(prev_lines):
    """Replay earlier scenes' timelines to their last frame, in order."""
    out = []
    for lines in prev_lines:
        out.append('(function(){const t=gsap.timeline({paused:true});\n' + DRAW + '\n'.join(lines) + '\nt.progress(1,false);})();\n')
    return ''.join(out)


def page2(title, root, comp_id, duration, body, defs, tl, cues, prev_lines=(), css=''):
    return (HEAD.format(title=title, root=root).replace('</style>', css + '</style>', 1)
            + f'<div id="{root}" data-composition-id="{comp_id}" data-start="0" data-duration="{duration}" data-width="1280" data-height="720" data-fps="24">\n'
            + '<svg class="stage" viewBox="0 0 1280 720" role="img" aria-label="' + title + '">\n<defs>\n' + defs + '\n</defs>\n'
            + body + '\n</svg>\n'
            + f'<audio id="{root}-narration" src="public/audio/narration.wav" data-start="0" data-duration="{duration}" data-media-start="0" data-track-index="100" data-volume="1"></audio>\n'
            + '</div>\n<script>\nwindow.__timelines=window.__timelines||{};\n'
            + prelude(prev_lines)
            + 'const t=gsap.timeline({paused:true});\n'
            + 'const C=' + json.dumps(cues) + ';\n' + DRAW
            + '\n'.join(tl.lines) + f"\nt.set({{}},{{}},{duration});\nwindow.__timelines['{comp_id}']=t;\n</script></body></html>\n")
