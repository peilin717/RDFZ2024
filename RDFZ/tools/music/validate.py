"""Technical failures and advisory score observations are separate outputs.
No aesthetic score, no model calls, no "listened" claims.
"""
import json,hashlib,subprocess
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from notation import ROOT
from render import WORK,SR,measure

def score_checks(s):
 errors=[];advice=[];length=s['length_beats'];all_notes=[]
 for t in s['tracks']:
  ns=t['notes'];all_notes.extend(ns)
  for n in ns:
   if not(0<=n['pitch']<=127 and 1<=n['velocity']<=127 and n['duration']>0 and 0<=n['beat']<length and n['beat']+n['duration']<=length+1e-5):errors.append({'track':t['id'],'note':n,'error':'event bounds'})
  if ns and len(set(n['velocity'] for n in ns))==1:advice.append({'track':t['id'],'issue':'constant note velocity; check intentional percussion/ostinato'})
  if t['family']=='wind':
   long=[n for n in ns if n['duration']*60/s['tempo_map'][0]['bpm']>8]
   if long:advice.append({'track':t['id'],'issue':'wind breath over 8 seconds','count':len(long)})
  perbar={}
  for b in range(int(length/4)):
   events=tuple((round(n['beat']%4,4),n['pitch'],n['duration']) for n in ns if b*4<=n['beat']<(b+1)*4)
   if events:perbar.setdefault(events,[]).append(b+1)
  for pattern,barlist in perbar.items():
   if len(barlist)>=8:advice.append({'track':t['id'],'issue':'repeated authored bar; assess theme/ostinato context, not automatic failure','bars':barlist})
 groups={}
 for a in s['arrangement']:groups.setdefault(a['section'],[]).append(a)
 melodic_fingerprints=[]
 for name,entries in groups.items():
  fingerprint=[]
  for a in entries:
   fingerprint.append(tuple((k,v['notation']) for k,v in a['voices'].items() if v['role']=='melody'))
  melodic_fingerprints.append((name,str(fingerprint)))
 for i,(name,fp) in enumerate(melodic_fingerprints):
  for other,fp2 in melodic_fingerprints[:i]:
   if fp==fp2:advice.append({'issue':'entire melodic section identical','sections':[other,name]})
 return {'id':s['id'],'errors':errors,'advisories':advice,'duration':length*60/s['tempo_map'][0]['bpm'],'bars':length/4,'subjective_audition':'未进行主观听觉验证'}

def decode(path):
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ac','2','-ar',str(SR),'-'])
 return np.frombuffer(raw,dtype='<f4').reshape(-1,2)

def audio_checks(s):
 report=json.loads((WORK/'reports'/f"{s['id']}-production.json").read_text())
 failures=[];checks={}
 for label,path in [('master',Path(report['master'])),('ogg',ROOT/report['web']),('mp3',ROOT/report['fallback'])]:
  x=decode(path);assert len(x)>0
  peak=float(np.max(abs(x)));l=measure(path)
  if not np.isfinite(x).all():failures.append(label+': non-finite samples')
  if peak>=1:failures.append(label+': clipped samples')
  if float(l['input_tp'])>-1:failures.append(label+': true peak above -1 dBTP')
  if abs(len(x)-report['frames'])>1:failures.append(label+': decoded length mismatch')
  # Activity at one-second scale; intentional sparse spaces are reported, not flattened.
  rms=np.array([np.sqrt(np.mean(chunk*chunk)) for chunk in np.array_split(x,max(1,len(x)//SR))])
  silent=int(np.sum(rms<1e-5))
  if np.max(rms)<1e-5:failures.append(label+': entirely silent')
  step=float(np.max(abs(x[0]-x[-1])))
  differences=np.max(abs(np.diff(x,axis=0)),axis=1)
  normal=float(np.quantile(differences,.999))
  seam_ratio=step/max(normal,1e-8)
  if report['loop'] and step>max(.015,normal*4):failures.append(label+': discontinuity exceeds natural waveform envelope')
  edge=np.sqrt(np.mean(np.concatenate([x[-SR//4:],x[:SR//4]])**2))
  if report['loop'] and edge<1e-5:failures.append(label+': silent loop boundary')
  if not report['loop'] and np.sqrt(np.mean(x[-SR//4:]**2))>0.001:failures.append(label+': short-cue tail not settled')
  checks[label]={'frames':len(x),'peak':peak,'true_peak_db':float(l['input_tp']),'lufs':float(l['input_i']),'loop_step':step,'natural_step_p999':normal,'seam_ratio':seam_ratio,'one_second_silent_windows':silent,'boundary_250ms_rms':float(edge)}
 # A decoded three-loop file must preserve all three complete periods.
 if report['loop']:
  trip=decode(Path(report['preview']))
  if abs(len(trip)-3*report['frames'])>1:failures.append('three-loop preview length mismatch')
  checks['three_loop_frames']=len(trip)
 return {'id':s['id'],'failures':failures,'measurements':checks,'threshold_policy':'fixed before representative rendering; discontinuity compared with natural waveform slope, not aesthetic judgement','subjective_audition':'未进行主观听觉验证'}

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('cues',nargs='*');parser.add_argument('--scores-only',action='store_true');args=parser.parse_args()
 selected=args.cues or [p.stem for p in (ROOT/'music/scores').glob('*.json')]
 results=[]
 for name in selected:
  s=json.loads((ROOT/f'music/scores/{name}.json').read_text());r={'score':score_checks(s)}
  if not args.scores_only:r['audio']=audio_checks(s)
  results.append(r);print(name,'score errors',len(r['score']['errors']),'audio failures',r.get('audio',{}).get('failures',[]),flush=True)
 path=WORK/'reports'/('validation-'+('-'.join(selected) if len(selected)<4 else 'all')+'.json');path.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 assert all(not r['score']['errors'] and not r.get('audio',{}).get('failures') for r in results),str(path)
