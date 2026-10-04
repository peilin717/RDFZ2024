"""Export authored JSON to MIDI, MusicXML and bar-by-bar arrangement maps."""
import json
from pathlib import Path
from xml.etree.ElementTree import Element,SubElement,ElementTree,indent
from notation import ROOT,midi

def sub(e,tag,text=None,**attrs):
 x=SubElement(e,tag,attrs)
 if text is not None:x.text=str(text)
 return x

def export(s):
 out=ROOT/'music/scores';midi(s,out/(s['id']+'.mid'))
 xml=Element('score-partwise',version='4.0');work=sub(xml,'work');sub(work,'work-title',s['title'])
 ident=sub(xml,'identification');sub(ident,'creator','Original RDFZ score authored in the Codex session',type='composer')
 parts=sub(xml,'part-list')
 names=[('C',0),('C',1),('D',0),('E',-1),('E',0),('F',0),('F',1),('G',0),('A',-1),('A',0),('B',-1),('B',0)]
 for pi,t in enumerate(s['tracks'],1):
  pid=f'P{pi}';listing=sub(parts,'score-part',id=pid);sub(listing,'part-name',t['id']+' / '+t['role'])
  inst=sub(listing,'score-instrument',id=pid+'-I');sub(inst,'instrument-name',t['instrument'])
  mi=sub(listing,'midi-instrument',id=pid+'-I');sub(mi,'midi-channel',10 if t['family']=='drums' else pi if pi<10 else pi+1);sub(mi,'midi-program',t['program']+1)
  part=sub(xml,'part',id=pid)
  for bar in range(int(s['length_beats']/4)):
   measure=sub(part,'measure',number=str(bar+1))
   if bar==0:
    attrs=sub(measure,'attributes');sub(attrs,'divisions',480);time=sub(attrs,'time');sub(time,'beats',4);sub(time,'beat-type',4);clef=sub(attrs,'clef');sub(clef,'sign','F' if t['family']=='bass' else 'G');sub(clef,'line',4 if t['family']=='bass' else 2)
    direction=sub(measure,'direction');sub(direction,'sound',tempo=str(s['tempo_map'][0]['bpm']))
   if pi==1 and (bar==0 or s['arrangement'][bar]['section']!=s['arrangement'][bar-1]['section']):
    direction=sub(measure,'direction');dtype=sub(direction,'direction-type');sub(dtype,'rehearsal',s['arrangement'][bar]['section'])
   ns=sorted((n for n in t['notes'] if bar*4<=n['beat']<(bar+1)*4),key=lambda n:(n['beat'],n['pitch']))
   cursor=0;laststart=None
   for n in ns:
    start=round((n['beat']-bar*4)*480);dur=round(n['duration']*480)
    chord=start==laststart
    if not chord:
     if start>cursor:forward=sub(measure,'forward');sub(forward,'duration',start-cursor)
     elif start<cursor:backup=sub(measure,'backup');sub(backup,'duration',cursor-start)
    node=sub(measure,'note')
    if chord:sub(node,'chord')
    pitch=sub(node,'pitch');step,alter=names[n['pitch']%12];sub(pitch,'step',step)
    if alter:sub(pitch,'alter',alter)
    sub(pitch,'octave',n['pitch']//12-1);sub(node,'duration',dur)
    if not chord:cursor=start+dur
    laststart=start
   if cursor<1920:forward=sub(measure,'forward');sub(forward,'duration',1920-cursor)
 indent(xml,space='  ');ElementTree(xml).write(out/(s['id']+'.musicxml'),encoding='utf-8',xml_declaration=True)
 lines=[f"# {s['title']} — arrangement map",'',f"{s['tempo_map'][0]['bpm']} BPM · {s['length_beats']//4} bars · revision {s['revision']}",'','| 小节 | 段落 | 活动声部与作用 |','|---:|---|---|']
 for a in s['arrangement']:
  desc='；'.join(f"{k}（{v['role']}）" for k,v in a['voices'].items()) or '写定留白'
  lines.append(f"| {a['bar']} | {a['section']} | {desc} |")
 lines+=['','## 段落意图','']+[f"- {sec['name']}：{sec['description']}" for sec in s['sections']]
 (out/(s['id']+'.arrangement.md')).write_text('\n'.join(lines)+'\n')
if __name__=='__main__':
 for p in (ROOT/'music/scores').glob('*.json'):export(json.loads(p.read_text()))
