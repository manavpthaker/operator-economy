#!/usr/bin/env python3
"""Two newly confirmed truncations only; preserve the original six-item batch."""
import argparse,hashlib,importlib.util,sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parents[1]
BASE=D.parent/'_tools/prepare_and_upload.py'
spec=importlib.util.spec_from_file_location('guarded_full_source',BASE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.D=D;m.ALLOWED={'seg012':337,'seg037':281}
original_save=m.save
def save(p,d):
 if d.get('record_type')=='ep009_full_source_guarded_repair':
  d['record_type']='ep009_full_source_guarded_repair_addendum'
  d['authorization']='Root requested two additional confirmed terminal truncations: seg012 337/343 and seg037 281/284. Storage only; no generation, estimates or current-plan changes.'
  d['preparation_helper']=m.bound(Path(__file__))
  d['base_preparation_helper']=m.bound(BASE)
  d['original_batch']=m.bound(D.parent/'DELIVERY.json')
 original_save(p,d)
m.save=save
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','upload']);a=p.parse_args()
 (m.prepare if a.mode=='prepare' else m.upload)()
