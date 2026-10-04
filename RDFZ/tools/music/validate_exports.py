"""Independent MIDI byte parser: check exported events against saved score.
Also checks CC endpoints, peak polyphony and MusicXML part/measure integrity.
"""
import json,struct,xml.etree.ElementTree as ET
from notation import ROOT

def vlq(data,pos):
 n=0
 while True:
  b=data[pos];pos+=1;n=n*128+(b&127)
  if not b&128:return n,pos

def read_track(data):
 pos=0;tick=0;events=[]
 while pos<len(data):
  delta,pos=vlq(data,pos);tick+=delta;status=data[pos];pos+=1
  if status==255:
   meta=data[pos];pos+=1;size,pos=vlq(data,pos);payload=data[pos:pos+size];pos+=size
   events.append((tick,'meta',meta,payload));continue
  assert 128<=status<240,status
  length=1 if status&240 in (192,208) else 2;payload=data[pos:pos+length];pos+=length;events.append((tick,status,*payload))
 return events

def validate():
 results=[]
 for path in (ROOT/'music/scores').glob('*.json'):
  s=json.loads(path.read_text());raw=path.with_suffix('.mid').read_bytes();assert raw[:4]==b'MThd'
  size,fmt,tracks,ppq=struct.unpack('>IHHH',raw[4:14]);assert fmt==1 and ppq==480 and tracks==len(s['tracks'])+1
  pos=14;parsed=[]
  while pos<len(raw):
   assert raw[pos:pos+4]==b'MTrk';n=int.from_bytes(raw[pos+4:pos+8],'big');parsed.append(read_track(raw[pos+8:pos+8+n]));pos+=8+n
  poly={}
  for t,events in zip(s['tracks'],parsed[1:]):
   actual=[];pending={};maximum=0;live=0;lastpedal=0
   for e in events:
    if e[1]=='meta':continue
    typ=e[1]&240
    if typ==144:
     assert e[2] not in pending,(s['id'],t['id'],'same pitch overlap')
     pending[e[2]]=(e[0],e[3]);live+=1;maximum=max(maximum,live)
    elif typ==128:
     start,vel=pending.pop(e[2]);actual.append((start,e[0]-start,e[2],vel));live-=1
    elif typ==176 and e[2]==64:lastpedal=e[3]
   assert not pending and lastpedal==0,(s['id'],t['id'],'hanging note/pedal')
   expected=sorted((round(n['beat']*480),round((n['beat']+n['duration'])*480)-round(n['beat']*480),n['pitch'],n['velocity']) for n in t['notes'])
   assert sorted(actual)==expected,(s['id'],t['id'],'MIDI differs from score')
   assert maximum<=128,(s['id'],t['id'],'polyphony limit')
   for c in t['controls']:assert 0<=c['beat']<=s['length_beats'] and 0<=c['cc']<=127 and 0<=c['value']<=127
   poly[t['id']]=maximum
  xml=ET.parse(path.with_suffix('.musicxml')).getroot();parts=xml.findall('part');assert len(parts)==len(s['tracks'])
  for part in parts:assert len(part.findall('measure'))==s['length_beats']//4
  results.append({'id':s['id'],'midi_exact_event_match':True,'pedal_released':True,'peak_active_notes_per_stem':poly,'musicxml_parts':len(parts),'musicxml_measures_per_part':s['length_beats']//4})
 (ROOT/'music/reports/export-validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 print('MIDI, control and XML export validation:',len(results),'scores')
 return results
if __name__=='__main__':validate()
