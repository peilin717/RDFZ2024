#!/usr/bin/env python3
"""Offline incremental rebuild from saved original scores. No model/API calls.
Initialization is the only stage permitted to download dependencies/soundfonts.
"""
import argparse,json,hashlib,subprocess,sys,shutil,ctypes.util,os
from pathlib import Path
from notation import ROOT
from render import WORK,render
from export_scores import export
from validate import score_checks,audio_checks
from publish import publish

def initialize(offline):
 for name in ['stems','masters','previews','reports','cache','soundfonts']:(WORK/name).mkdir(parents=True,exist_ok=True)
 missing=[]
 for cmd in ['ffmpeg','node']:
  if not shutil.which(cmd):missing.append(cmd)
 if not ctypes.util.find_library('fluidsynth'):missing.append('libfluidsynth shared library')
 if missing:raise RuntimeError('Install local free dependencies first: '+', '.join(missing))
 cfg=json.loads((ROOT/'music/production.json').read_text())
 for name,entry in cfg['soundfonts'].items():
  path=WORK/entry['path']
  if not path.exists():
   if offline:raise RuntimeError(f'Offline mode: missing {path}; run init with network first.')
   import urllib.request,tarfile
   path.parent.mkdir(parents=True,exist_ok=True)
   if name=='general':urllib.request.urlretrieve(entry['source'],path)
   else:
    archive=WORK/'cache/salamander.tar.xz';urllib.request.urlretrieve(entry['source'],archive)
    with tarfile.open(archive) as tar:
     # Extract only the expected SF2; no archive paths or executable contents trusted.
     members=[m for m in tar.getmembers() if Path(m.name).name==path.name];assert len(members)==1
     with tar.extractfile(members[0]) as inp,path.open('wb') as out:shutil.copyfileobj(inp,out)
  h=hashlib.sha256()
  with path.open('rb') as f:
   for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
  if h.hexdigest()!=entry['sha256']:raise RuntimeError(f'Soundfont hash mismatch: {name}; expected pinned version.')
 print('Local tools and pinned soundfonts verified.',flush=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['init','compile','render','mix','verify','publish','build','all'],nargs='?',default='all');ap.add_argument('--offline',action='store_true');ap.add_argument('--cues',nargs='*');ap.add_argument('--force',action='store_true');ap.add_argument('--resume',action='store_true',help='Incremental resume is the default; explicit for reproducible commands.');args=ap.parse_args()
 for name in ['stems','masters','previews','reports','cache']:(WORK/name).mkdir(parents=True,exist_ok=True)
 if args.stage in ('init','all'):initialize(args.offline)
 if args.stage=='init':return
 # Prevent accidental remote calls in the production stages, including with --offline omitted.
 import socket
 def deny(*a,**k):raise RuntimeError('Networking disabled during music production')
 socket.socket=deny;socket.create_connection=deny
 catalog=json.loads((ROOT/'music/cues.json').read_text());ids=[c['id'] for c in catalog['bgm']+catalog['stingers']]
 names=args.cues or ids
 assert set(names)<=set(ids),'Unknown cue IDs'
 reports=[];checkpoint=WORK/'reports/checkpoint.json'
 for id in names:
  s=json.loads((ROOT/f'music/scores/{id}.json').read_text())
  check=score_checks(s)
  if check['errors']:raise RuntimeError(check)
  if args.stage in ('compile','all'):
   digest=hashlib.sha256(json.dumps(s,sort_keys=True).encode()+Path(__file__).with_name('export_scores.py').read_bytes()+Path(__file__).with_name('notation.py').read_bytes()).hexdigest();cache=WORK/f'cache/{id}-compile.hash'
   if args.force or not cache.exists() or cache.read_text()!=digest or any(not (ROOT/f'music/scores/{id}{suffix}').exists() for suffix in ['.mid','.musicxml','.arrangement.md']):export(s);cache.write_text(digest)
  if args.stage in ('render','mix','all'):render(s,args.force)
  if args.stage in ('verify','all'):
   production=WORK/f'reports/{id}-production.json';p=json.loads(production.read_text());verify=WORK/f'reports/{id}-validation.json'
   digest=hashlib.sha256(production.read_bytes()+Path(__file__).with_name('validate.py').read_bytes()).hexdigest()
   # Includes actual output bytes so a corrupted export cannot hide behind a manifest cache.
   h=hashlib.sha256(digest.encode())
   for path in [Path(p['master']),ROOT/p['web'],ROOT/p['fallback'],Path(p['preview'])]:
    with path.open('rb') as f:
     for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
   digest=h.hexdigest();old=json.loads(verify.read_text()) if verify.exists() else {}
   if not args.force and old.get('fingerprint')==digest:r=old
   else:
    r={'fingerprint':digest,'score':check,'audio':audio_checks(s)};verify.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
   reports.append(r);print(id,'verified',r['audio']['failures'],flush=True)
   if r['audio']['failures']:raise RuntimeError(f'{id}: {r["audio"]["failures"]}')
  checkpoint.write_text(json.dumps({'stage':args.stage,'last_completed':id,'offline':True,'source':'persisted scores; no composition model calls'},indent=2))
 if args.stage in ('verify','all'):
  from review_structure import review
  from validate_exports import validate
  review();validate()
  from validate_loops import validate as validate_loops
  validate_loops()
 if reports:
  dest=ROOT/'music/reports';dest.mkdir(exist_ok=True);(dest/'technical-validation.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
 if args.stage in ('publish','build','all'):publish()
 if args.stage in ('build','all'):subprocess.run(['node','tools/build_web.mjs'],cwd=ROOT,check=True)
if __name__=='__main__':main()
