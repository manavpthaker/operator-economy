"""P08r3b only: hash-bound lexical alias resolution, unchanged gate; original records preserved."""
import importlib.util,sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('p08_r1',D/'_tools/p08_retime_r1.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
assert sys.argv[2]=='P08r3b';d=m.G/'P08r3b';path=d/'NATIVE-OFFSET-SELECTION.json'
assert m.sha(path)=='6e18c3335a5d29f1c0702deb069039bb6851a69082b86da270373a889aad6b57'
sel=m.read(path);assert sel['status']=='selected_for_processing' and sel['max_spread_s']==.3
for key in ['original_offsets','selected_offsets','independent_lexical_audit','native','narration']:
 b=sel[key];assert m.sha(m.R/b['path'])==b['sha256']
audit=m.read(m.R/sel['independent_lexical_audit']['path']);assert audit['wrong_word_alias_excluded'] and audit['matched_sequence_verified']
for b in audit['source_bindings'].values():assert m.sha(m.R/b['path'])==b['sha256']
chosen=m.R/sel['selected_offsets']['path'];orig=m.R/sel['original_offsets']['path'];rec=m.read(chosen)
assert rec['original_offsets']==sel['original_offsets'] and rec['independent_lexical_audit']==sel['independent_lexical_audit']
assert rec['method']=='lexically-anchored-envelope-windows'
lo,hi=audit['lag_domain_seconds'];assert all(lo<=w['native_minus_narration_s']<=hi for w in rec['windows'])
oldread,oldsha,oldwrite=m.r.rj,m.r.sha,m.r.wj
mapped=lambda p:chosen if Path(p).resolve()==orig.resolve() else p
m.r.rj=lambda p:oldread(mapped(p));m.r.sha=lambda p:oldsha(mapped(p))
base_read=m.read
m.read=lambda p:base_read(d/'MOTION-REVIEW-lexically-resolved.json' if Path(p)==d/'MOTION-REVIEW.json' else p)
def write(p,value):
 if Path(p).name=='TRIM.json':value={**value,'native_offset_selection':{'path':m.r.rel(path),'sha256':m.sha(path)}}
 oldwrite(p,value)
m.r.wj=write
m.r.native_gate('P08r3b')
m.main()
