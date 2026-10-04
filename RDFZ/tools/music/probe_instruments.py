"""Actual local soundfont probes: dynamics, onset, release, register/repetition.
These are diagnostic phrases, not finished cues and not a listening evaluation.
"""
import json
import numpy as np
from scipy.io import wavfile
from render import Synth,fonts,WORK,SR
from notation import INSTRUMENTS,ROOT
used={}
for path in (ROOT/'music/scores').glob('*.json'):
 for t in json.loads(path.read_text())['tracks']:
  used.setdefault(t['instrument'],[]).extend(n['pitch'] for n in t['notes'])
result={}
for instrument in sorted(used):
 program,font,family,pan,send=INSTRUMENTS[instrument];engine=Synth(fonts()[font],program,128 if family=='drums' else 0)
 phrase=[];stats=[];pitches=[48,60,72] if instrument=='piano' else [60,67,74] if family=='wind' else [43,50,55] if family=='bass' else [60,64,67]
 if family=='drums':pitches=[36,38,42]
 register=[min(used[instrument]),sorted(used[instrument])[len(used[instrument])//2],max(used[instrument])]
 pitches=register
 for vel,note in list(zip([65,65,65],register))+[(v,register[1]) for v in [40,65,90]]:
  engine.on(engine.synth,engine.channel,note,vel);x=engine.audio(SR)
  engine.off(engine.synth,engine.channel,note);tail=engine.audio(SR*2)
  env=np.max(abs(x),axis=1);peak=float(env.max());idx=np.flatnonzero(env>max(1e-5,peak*.05))
  stats.append({'pitch':note,'velocity':vel,'peak':peak,'rms':float(np.sqrt(np.mean(x*x))),'onset_5percent_ms':float(idx[0]/SR*1000) if len(idx) else None,'tail_last_250ms_rms':float(np.sqrt(np.mean(tail[-SR//4:]**2)))})
  phrase.extend([x,tail])
 # A real repeated-note figure at a restrained 4 Hz, not assumed "true staccato".
 for n in [pitches[1],pitches[1],pitches[2],pitches[1]]:
  engine.on(engine.synth,engine.channel,n,62);phrase.append(engine.audio(SR//8));engine.off(engine.synth,engine.channel,n);phrase.append(engine.audio(SR//8))
 expression=None
 if family=='sustain':
  n=register[1];engine.on(engine.synth,engine.channel,n,65);engine.audio(SR)
  engine.cc(11,55);quiet=engine.audio(SR)
  engine.cc(11,105);loud=engine.audio(SR)
  expression={'cc11_55_rms':float(np.sqrt(np.mean(quiet[SR//2:]**2))),'cc11_105_rms':float(np.sqrt(np.mean(loud[SR//2:]**2)))}
  engine.off(engine.synth,engine.channel,n);phrase.extend([quiet,loud])
 engine.cc(64,0);phrase.append(engine.audio(SR*3));engine.close()
 wave=np.concatenate(phrase);wavfile.write(WORK/'previews'/f'probe-{instrument}.wav',SR,wave)
 assert all(x['peak']>1e-5 and x['peak']<1 for x in stats),(instrument,stats)
 result[instrument]={'bank':128 if family=='drums' else 0,'program_zero_based':program,'tests':stats,'actual_score_register':register,'expression':expression,'subjective_audition':False,'decision':'No unsupported legato/articulation claims; wind phrases include breaths; piano uses dedicated SF2. Sustain uses CC11, not CC1.'}
(WORK/'reports/instrument-probes.json').write_text(json.dumps(result,indent=2)+'\n')
print('Instrument probes completed:',', '.join(result))
