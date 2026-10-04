"""Notation compiler: expands explicitly authored phrases, never invents melodies.
Durations are quarter-note beats. Each | is a 4/4 bar. r is a rest.
"""
import json, re, struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SCORES=ROOT/'music/scores'
INSTRUMENTS={
 'piano':(0,'salamander','keyboard',0,0.16),
 'nylon':(24,'general','plucked',-0.25,0.13),
 'harp':(46,'general','plucked',0.22,0.19),
 'flute':(73,'general','wind',-0.12,0.22),
 'clarinet':(71,'general','wind',0.16,0.18),
 'oboe':(68,'general','wind',-0.18,0.18),
 'cello':(42,'general','sustain',0.08,0.18),
 'strings':(48,'general','sustain',-0.12,0.24),
 'pizz':(45,'general','plucked',0.2,0.13),
 'vibes':(11,'general','plucked',0.15,0.18),
 'celesta':(8,'general','plucked',-0.18,0.17),
 'marimba':(12,'general','plucked',0.2,0.12),
 'electric':(4,'general','keyboard',-0.12,0.12),
 'bass':(32,'general','bass',0,0.05),
 'ebass':(33,'general','bass',0,0.05),
 'pad':(89,'general','sustain',0.12,0.25),
 'drums':(0,'general','drums',0,0.08),
}
PITCH={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def pitch(s):
 if isinstance(s,int):return s
 m=re.fullmatch(r'([A-G])([#b]?)(-?\d+)',s)
 if not m:raise ValueError(s)
 return 12*(int(m[3])+1)+PITCH[m[1]]+({'#':1,'b':-1,'':0}[m[2]])
def bars(text):return [x.strip() for x in text.strip().split('|')]
def transform(text, *, octave=0, replacement=None):
 """Only an explicitly requested octave handoff or specified bar rewrite."""
 result=bars(text)
 for i,b in (replacement or {}).items():result[i]=b
 if octave:
  def change(m):return m[1]+str(int(m[2])+octave)
  result=[re.sub(r'([A-G][#b]?)(\d)',change,b) for b in result]
 return ' | '.join(result)

def notes(text,start=0,velocity=68,gate=.9,curve=None):
 out=[]; curve=curve or [0,2,4,0,1,3,-1,-5]
 for bi,bar in enumerate(bars(text)):
  t=0
  for token in bar.split():
   head,duration=token.rsplit(':',1);dur=float(duration)
   assert dur>0,(token,dur)
   if head!='r':
    head,_,explicit=head.partition('@');v=int(explicit) if explicit else velocity+curve[bi%len(curve)]
    # Intentional phrase accent, never random jitter.
    if not explicit and t in (0,2):v+=2
    for p in head.split('+'):
     out.append({'beat':start+4*bi+t,'duration':round(dur*gate,5),'pitch':pitch(p),'velocity':max(1,min(120,v)),'articulation':'detached' if gate<.8 else 'tenuto'})
   t+=dur
  assert t<=4.00001,(bi,bar,t)
 return out

def chord_part(chords,style='held'):
 """Local accompaniment cells chosen by the composer for each section.
Explicit voicings, not inferred/root-position chords. Rests leave room for lead.
"""
 result=[]
 for i,c in enumerate(chords):
  ns=c.split();joined='+'.join(ns)
  if c=='r':result.append('r:4');continue
  if style=='held':b=joined+':3.5 r:.5'
  elif style=='breath':b='r:1 '+joined+':2 r:1'
  elif style=='offbeat':b=f'r:.5 {joined}:.75 r:.75 {joined}:.5 r:1.5'
  elif style=='broken':b=f'{ns[0]}:1 {ns[1]}:.5 {ns[-1]}:1 r:.5 {ns[2]}:.5 r:.5'
  elif style=='dialogue':b=(f'{ns[0]}+{ns[1]}:1.5 r:.5 {ns[2]}+{ns[-1]}:1 r:1' if i%2==0 else f'r:1 {joined}:2 r:1')
  elif style=='pulse':b=f'{ns[0]}+{ns[1]}:.5 r:.5 {ns[2]}:.5 {ns[1]}:.5 r:.5 {ns[-1]}:.5 r:1'
  else:raise ValueError(style)
  result.append(b)
 return ' | '.join(result)

def percussion(style,length):
 # Paired bars and phrase-end fills are authored arrangements, not randomization.
 patterns={
 'brush':('C2@43:.2 r:1.8 D2@34:.2 r:1.8','r:1 C2@40:.2 r:1.8 D2@38:.2 r:.8'),
 'backbeat':('C2@65:.2 r:1.3 D2@56:.2 r:.3 C2@52:.2 r:.8 D2@61:.2 r:.8','C2@61:.2 r:.8 D2@57:.2 r:1.3 C2@54:.2 r:.3 D2@60:.2 r:.8'),
 'drive':('C2@70:.2 r:.8 D2@63:.2 r:.3 C2@52:.2 r:.8 D2@66:.2 r:1.3','C2@63:.2 r:1.3 D2@60:.2 r:.3 C2@56:.2 r:.8 D2@63:.2 r:.8'),
 'ticks':('F#2@33:.1 r:1.4 F#2@26:.1 r:1.9 F#2@31:.1 r:.4','r:.5 F#2@28:.1 r:1.4 F#2@34:.1 r:1.9'),
 'light':('C2@49:.2 r:1.8 G#2@39:.2 r:1.8','r:1 G#2@34:.2 r:.8 C2@42:.2 r:1.8'),
 }
 seq=[patterns[style][i%2] for i in range(length)]
 if length>=8 and style in ('drive','backbeat'):
  seq[-1]='C2@60:.2 r:.8 D2@53:.25 D2@46:.25 r:.5 F2@49:.25 G2@53:.25 D2@58:.25 r:1.25'
 return ' | '.join(seq)

def part(instrument,text,velocity=65,gate=None,role='melody',gain=1):
 return {'instrument':instrument,'text':text,'velocity':velocity,'gate':gate if gate is not None else (.83 if INSTRUMENTS[instrument][2]=='wind' else .92),'role':role,'gain':gain}

def section(name,description,**voices):return {'name':name,'description':description,'voices':voices}

def score(cue,sections,revision=1,loop=True):
 tracks={};arr=[];offset=0
 for sec in sections:
  count=max(len(bars(v['text'])) for v in sec['voices'].values())
  for key,v in sec['voices'].items():
   assert len(bars(v['text']))==count,(cue['id'],sec['name'],key)
   instrument=v['instrument'];program,font,family,pan,send=INSTRUMENTS[instrument]
   track=tracks.setdefault(key,{'id':key,'instrument':instrument,'program':program,'bank':128 if instrument=='drums' else 0,'font':font,'family':family,'pan':pan,'send':send,'gain':v['gain'],'role':v['role'],'notes':[],'controls':[]})
   assert track['instrument']==instrument,(key,instrument)
   track['notes']+=notes(v['text'],offset,v['velocity'],v['gate'])
   for bi in range(count):
    beat=offset+bi*4
    if family=='keyboard':track['controls'] += [{'beat':beat,'cc':64,'value':0},{'beat':beat+.08,'cc':64,'value':66},{'beat':beat+3.65,'cc':64,'value':0}]
    if family=='sustain':track['controls'] += [{'beat':beat,'cc':11,'value':75},{'beat':beat+1,'cc':11,'value':86},{'beat':beat+2.5,'cc':11,'value':92},{'beat':beat+3.5,'cc':11,'value':74}]
   for n in track['notes']:
    if n['beat']>=offset:n['section']=sec['name']
  for bi in range(count):
   active={key:{'role':v['role'],'instrument':v['instrument'],'notation':bars(v['text'])[bi]} for key,v in sec['voices'].items() if bars(v['text'])[bi]!='r:4'}
   arr.append({'bar':offset//4+bi+1,'section':sec['name'],'intent':sec['description'],'voices':active})
  offset+=count*4
 assert not cue.get('bars') or offset//4==cue['bars'],(cue['id'],offset//4,cue.get('bars'))
 s={'schema':1,'id':cue['id'],'title':cue['title'],'scene':cue.get('scene',cue.get('trigger')),'themes':cue.get('themes',[cue.get('theme')]),'revision':revision,'meter':[4,4],'tempo_map':[{'beat':0,'bpm':cue.get('bpm',100)}],'length_beats':offset,'loop':{'enabled':loop,'start_beat':0,'end_beat':offset,'cadence':'末句保留属/共同音导向开头；连续周期渲染，不用淡入淡出遮盖'},'target_lufs':cue.get('lufs',-20),'sections':[{'name':x['name'],'description':x['description']} for x in sections],'tracks':list(tracks.values()),'arrangement':arr,'audition':'未进行主观听觉验证'}
 (SCORES/(cue['id']+'.json')).write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
 return s

def vlq(n):
 n=int(n);out=[n&127];n>>=7
 while n:out.insert(0,(n&127)|128);n>>=7
 return bytes(out)
def midi(s,path):
 division=480;channels={};chunks=[]
 def chunk(events):
  events.sort(key=lambda e:(e[0],e[1]));last=0;body=b''
  for tick,priority,data in events:body+=vlq(tick-last)+data;last=tick
  body+=b'\0\xff\x2f\0';return b'MTrk'+struct.pack('>I',len(body))+body
 tempo=[]
 for t in s['tempo_map']:tempo.append((round(t['beat']*division),0,b'\xff\x51\x03'+int(60000000/t['bpm']).to_bytes(3,'big')))
 tempo += [(0,0,b'\xff\x58\x04\x04\x02\x18\x08')]
 chunks.append(chunk(tempo));channel=0
 for tr in s['tracks']:
  ch=9 if tr['family']=='drums' else channel
  if tr['family']!='drums':channel+=1;channel+=channel==9
  assert ch<16
  name=tr['id'].encode();ev=[(0,0,b'\xff\x03'+vlq(len(name))+name),(0,0,bytes([0xc0|ch,tr['program']])),(0,0,bytes([0xb0|ch,10,round(64+tr['pan']*40)]))]
  for c in tr['controls']:ev.append((round(c['beat']*division),1,bytes([0xb0|ch,c['cc'],c['value']])))
  for n in tr['notes']:
   ev.append((round(n['beat']*division),3,bytes([0x90|ch,n['pitch'],n['velocity']])))
   ev.append((round((n['beat']+n['duration'])*division),2,bytes([0x80|ch,n['pitch'],0])))
  ev.append((round(s['length_beats']*division),4,bytes([0xb0|ch,64,0])))
  chunks.append(chunk(ev))
 Path(path).write_bytes(b'MThd'+struct.pack('>IHHH',6,1,len(chunks),division)+b''.join(chunks))
