"""Explainable structural observations, deliberately no musical quality score."""
import json,hashlib,itertools,collections
from notation import ROOT,notes
from render import WORK
from validate import score_checks

def melody(s):
 out=[]
 for a in s['arrangement']:
  for v in a['voices'].values():
   if v['role']=='melody':out.extend(notes(v['notation'],start=(a['bar']-1)*4,gate=1))
 return sorted(out,key=lambda n:(n['beat'],n['pitch']))
def signature(ns,relative=True):
 if not ns:return ()
 tonic=ns[0]['pitch'] if relative else 0;start=ns[0]['beat']
 return tuple((round(n['beat']-start,5),n['pitch']-tonic,n['duration']) for n in ns)
def review():
 scores=[json.loads(p.read_text()) for p in (ROOT/'music/scores').glob('*.json')]
 bgm=[s for s in scores if s['loop']['enabled']];duplicates=[];shared=[];reports=[]
 for a,b in itertools.combinations(bgm,2):
  if signature(melody(a))==signature(melody(b)):duplicates.append([a['id'],b['id']])
  # Report full shared phrases even when transferred to another octave/instrument.
  ag={};bg={}
  for s,d in [(a,ag),(b,bg)]:
   ns=melody(s)
   for start in range(0,s['length_beats'],32):
    phrase=[n for n in ns if start<=n['beat']<start+32]
    if phrase:d.setdefault(signature(phrase),[]).append(start//4+1)
  for sig in ag.keys()&bg.keys():shared.append({'cues':[a['id'],b['id']],'phrase_start_bars':[ag[sig],bg[sig]],'interpretation':'Review deliberate thematic quotation; not a failed check.'})
 for s in scores:
  r=score_checks(s);ns=melody(s);gaps=[]
  for prev,n in zip(ns,ns[1:]):
   gap=n['beat']-(prev['beat']+prev['duration'])
   if gap>=.25:gaps.append({'after_beat':prev['beat'],'rest_beats':gap})
  # Constant rhythmic cells over multiple full bars, regardless of pitches.
  rhythm=[]
  for b in range(s['length_beats']//4):
   rhythm.append(tuple((n['beat']%4,n['duration']) for n in ns if b*4<=n['beat']<(b+1)*4))
  longest=run=1
  for prev,n in zip(rhythm,rhythm[1:]):run=run+1 if n and n==prev else 1;longest=max(longest,run)
  bass_runs=[]
  for t in s['tracks']:
   if t['family']!='bass':continue
   cells=[signature([n for n in t['notes'] if b*4<=n['beat']<(b+1)*4]) for b in range(s['length_beats']//4)]
   streak=maximum=1
   for x,y in zip(cells,cells[1:]):streak=streak+1 if y and x==y else 1;maximum=max(maximum,streak)
   if maximum>=8:bass_runs.append({'track':t['id'],'consecutive_transposition_equivalent_bars':maximum})
  r.update({'melodic_breaths':gaps,'longest_unchanged_rhythm_bars':longest,'bass_advisories':bass_runs,'form':[sec['name'] for sec in s['sections']]})
  if longest>=8:r['advisories'].append({'issue':'Eight or more bars share exact melodic rhythm; review intentional pacing.'})
  reports.append(r)
 result={'not_aesthetic_scoring':True,'whole_cue_transposition_equivalent_melodies':duplicates,'shared_eight_bar_theme_phrases':shared,'scores':reports,'subjective_audition':'未进行主观听觉验证'}
 (ROOT/'music/reports/structure-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print('Whole-cue equivalents:',duplicates,'shared thematic phrases:',len(shared))
 print('Rhythm/bass advisories:',[(r['id'],r['longest_unchanged_rhythm_bars'],r['bass_advisories']) for r in reports if r['longest_unchanged_rhythm_bars']>=8 or r['bass_advisories']])
 return result
if __name__=='__main__':review()
