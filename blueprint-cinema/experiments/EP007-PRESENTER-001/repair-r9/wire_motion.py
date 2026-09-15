"""Wire measured shirt motion into the isolated, seek-safe HyperFrames wrapper."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / 'study-composite-r9'
TRACKING = ROOT.parents[1] / 'episodes/EP007-exit-readiness-prep/agents/deliverables/presenter-study-motion-r9/tracking.json'
data = json.loads(TRACKING.read_text())
assert data['metrics']['accepted_for_review']
assert data['fps'] == 25 and data['frame_count'] == 765
factor = .9821018813
pivot = (536.8108057 + factor * 304, -166.4062213 + factor * 950)
poses = [dict(time=f['time_seconds'], x=f['transform']['x_px'] * factor,
              y=f['transform']['y_px'] * factor,
              rotation=f['transform']['rotation_deg'], scale=f['transform']['scale'])
         for f in data['frames']]
ref = poses[10]
assert abs(ref['x']) < 1e-8 and abs(ref['y']) < 1e-8
assert abs(ref['rotation']) < 1e-8 and abs(ref['scale'] - 1) < 1e-8
(PROJECT / 'assets/shirt-motion.js').write_text(
    '// Derived from shirt-only measurements in G; no face animation.\n'
    'window.shirtMotion = ' + json.dumps(poses, separators=(',', ':')) + ';\n')
path = PROJECT / 'index.html'
html = path.read_text()
html = html.replace('<script src="assets/vendor/gsap.min.js"></script>',
                    '<script src="assets/vendor/gsap.min.js"></script>\n'
                    '  <script src="assets/shirt-motion.js"></script>')
start = poses[0]
css = (f'    #shirt-motion{{position:absolute;inset:0;width:1672px;height:941px;'
       f'transform-origin:{pivot[0]}px {pivot[1]}px;'
       f'transform:translate({start["x"]}px,{start["y"]}px) '
       f'rotate({start["rotation"]}deg) scale({start["scale"]})}}\n')
html = html.replace('    #shirt-clip{', css + '    #shirt-clip{')
html = html.replace('      <div data-hf-id="hf-gkee" id="shirt-clip">',
                    '      <div id="shirt-motion" data-layout-allow-overflow="">\n'
                    '      <div data-hf-id="hf-gkee" id="shirt-clip">')
html = html.replace('      <div data-hf-id="hf-dfqs" id="moving-person"',
                    '      </div>\n      <div data-hf-id="hf-dfqs" id="moving-person"')
html = html.replace('Static synthetic outer-shoulder coverage only',
                    'Synthetic outer shoulders following measured shirt motion only')
html = html.replace("    window.__timelines['study-composite']=gsap.timeline({paused:true});",
    """    const timeline = gsap.timeline({paused:true});
    const poses = window.shirtMotion;
    // Finite linear segments preserve measured timing during direct seek and render.
    for (let i=1; i<poses.length; i++) {
      const p=poses[i], previous=poses[i-1];
      timeline.to('#shirt-motion', {
        x:p.x, y:p.y, rotation:p.rotation, scale:p.scale,
        duration:p.time-previous.time, ease:'none'
      }, previous.time);
    }
    window.__timelines['study-composite']=timeline;""")
path.write_text(html)
print(json.dumps({'poses': len(poses), 'pivot_design_px': pivot, 'reference': ref}))
