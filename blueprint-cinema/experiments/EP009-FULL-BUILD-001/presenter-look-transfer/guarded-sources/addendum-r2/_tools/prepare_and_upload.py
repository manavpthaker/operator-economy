#!/usr/bin/env python3
"""Original seg059 with eight guards for terminal-performance defect repair."""
import argparse,importlib.util,sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parents[1];BASE=D.parent/'_tools/prepare_and_upload.py'
s=importlib.util.spec_from_file_location('guarded_full_source',BASE);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.D=D;m.ALLOWED={'seg059':153};original_save=m.save
def save(p,d):
 if d.get('record_type')=='ep009_full_source_guarded_repair':
  d['record_type']='ep009_full_source_guarded_repair_addendum'
  d['authorization']='Root requested original seg059 guard repair after graphics review found terminal drift in the last six frames of its 153-frame wardrobe result. Original source is 152 frames, guarded input 160. Storage only, no generation or estimates.'
  d['preparation_helper']=m.bound(Path(__file__));d['base_preparation_helper']=m.bound(BASE)
  d['original_batch']=m.bound(D.parent/'DELIVERY.json')
 original_save(p,d)
m.save=save
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','upload']);a=p.parse_args();(m.prepare if a.mode=='prepare' else m.upload)()
