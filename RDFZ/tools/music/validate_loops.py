"""Encoded three-cycle boundary checks; observations are not listening claims."""
import json,hashlib
from pathlib import Path
import numpy as np
from notation import ROOT
from render import WORK,SR
from validate import decode

def validate():
 results=[]
 for cue in json.loads((ROOT/'music/cues.json').read_text())['bgm']:
  id=cue['id'];r=json.loads((WORK/f'reports/{id}-production.json').read_text());path=Path(r['preview'])
  digest=hashlib.sha256(path.read_bytes()+Path(__file__).read_bytes()).hexdigest();cache=WORK/f'reports/{id}-three-loop-check.json'
  old=json.loads(cache.read_text()) if cache.exists() else {}
  if old.get('fingerprint')==digest:results.append(old);continue
  x=decode(path);n=r['frames'];assert len(x)==3*n,(id,len(x),n)
  boundaries=[]
  for index in [n,2*n]:
   window=x[index-SR//4:index+SR//4];step=float(np.max(np.abs(x[index]-x[index-1])))
   natural=float(np.quantile(np.max(np.abs(np.diff(window,axis=0)),axis=1),.999))
   before=float(np.sqrt(np.mean(x[index-SR//4:index]**2)));after=float(np.sqrt(np.mean(x[index:index+SR//4]**2)))
   assert step<=max(.015,natural*4),(id,'encoded seam',step,natural)
   assert max(before,after)>1e-5,(id,'silent encoded boundary')
   # Compare identical beat-grid windows between successive encoded periods.
   first=x[:SR];next_cycle=x[index:index+SR]
   relative_error=float(np.sqrt(np.mean((first-next_cycle)**2))/max(1e-8,np.sqrt(np.mean(first**2))))
   boundaries.append({'frame':index,'step':step,'local_natural_step_p999':natural,'before_250ms_rms':before,'after_250ms_rms':after,'cycle_start_one_second_relative_waveform_difference':relative_error,'inserted_or_dropped_frames':0})
  peak=float(np.max(np.abs(x)));assert peak<1,(id,'preview clipping')
  s=json.loads((ROOT/f'music/scores/{id}.json').read_text());ideal=s['length_beats']*60/s['tempo_map'][0]['bpm']*SR
  result={'id':id,'fingerprint':digest,'period_frames':n,'score_period_rounding_error_frames':n-ideal,'three_cycle_frames':len(x),'sample_peak':peak,'boundaries':boundaries,'subjective_audition':'未进行主观听觉验证'}
  cache.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');results.append(result)
 (ROOT/'music/reports/three-loop-validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 print('Encoded three-cycle boundaries checked:',len(results)*2)
 return results
if __name__=='__main__':validate()
