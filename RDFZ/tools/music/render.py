"""CPU-only FluidSynth library renderer and offline stem mixer.
No audio driver/CLI required. No network imports. CC mappings explicitly selected.
"""
import ctypes as C, ctypes.util, json, math, hashlib, subprocess, os, inspect
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy import signal
from notation import ROOT, midi
WORK=Path(os.environ.get('RDFZ_MUSIC_WORK',str(ROOT.parent.parent/'music-work')))
SR=44100

def bind(lib,name,result,args):
 f=getattr(lib,name);f.restype=result;f.argtypes=args;return f
class Synth:
 def __init__(self,font,program,bank=0):
  l=C.CDLL(ctypes.util.find_library('fluidsynth'));self.lib=l;ptr=C.c_void_p;i=C.c_int;char=C.c_char_p
  self.settings=bind(l,'new_fluid_settings',ptr,[])()
  num=bind(l,'fluid_settings_setnum',i,[ptr,char,C.c_double]);integer=bind(l,'fluid_settings_setint',i,[ptr,char,i])
  for key,value in [('synth.sample-rate',SR),('synth.gain',.5)]:num(self.settings,key.encode(),value)
  for key,value in [('synth.reverb.active',0),('synth.chorus.active',0),('synth.polyphony',128),('synth.cpu-cores',1),('synth.threadsafe-api',0)]:integer(self.settings,key.encode(),value)
  self.synth=bind(l,'new_fluid_synth',ptr,[ptr])(self.settings)
  assert self.synth,'FluidSynth initialization failed'
  sid=bind(l,'fluid_synth_sfload',i,[ptr,char,i])(self.synth,str(font).encode(),0);assert sid>=0,font
  self.channel=9 if bank==128 else 0
  self.preset=bind(l,'fluid_synth_program_select',i,[ptr,i,i,i,i])(self.synth,self.channel,sid,bank,program)
  assert self.preset==0,(font,bank,program)
  self.on=bind(l,'fluid_synth_noteon',i,[ptr,i,i,i]);self.off=bind(l,'fluid_synth_noteoff',i,[ptr,i,i]);self.ccf=bind(l,'fluid_synth_cc',i,[ptr,i,i,i])
  self.write=bind(l,'fluid_synth_write_float',i,[ptr,i,ptr,i,i,ptr,i,i])
  self.cc(7,100);self.cc(11,100);self.cc(10,64);self.cc(91,0);self.cc(93,0)
 def cc(self,n,v):self.ccf(self.synth,self.channel,n,v)
 def event(self,e):
  kind=e[1]
  if kind=='on':self.on(self.synth,self.channel,e[2],e[3])
  elif kind=='off':self.off(self.synth,self.channel,e[2])
  else:self.cc(e[2],e[3])
 def audio(self,n):
  x=np.empty((n,2),dtype=np.float32)
  self.write(self.synth,n,x.ctypes.data,0,2,x.ctypes.data,1,2)
  return x
 def close(self):
  bind(self.lib,'delete_fluid_synth',None,[C.c_void_p])(self.synth)
  bind(self.lib,'delete_fluid_settings',None,[C.c_void_p])(self.settings)

def fonts():
 cfg=json.loads((ROOT/'music/production.json').read_text())
 return {name:WORK/entry['path'] for name,entry in cfg['soundfonts'].items()}

def render_stem(s,tr,cycles=3):
 bpm=s['tempo_map'][0]['bpm'];fpb=SR*60/bpm
 n=round(s['length_beats']*fpb);loop=s['loop']['enabled']
 cycles=cycles if loop else 1
 total=n*cycles+(0 if loop else SR*6)
 events=[]
 for c in range(cycles):
  for ev in tr['controls']:events.append((c*n+round(ev['beat']*fpb),'cc',ev['cc'],ev['value']))
  for note in tr['notes']:
   events.append((c*n+round(note['beat']*fpb),'on',note['pitch'],note['velocity']))
   events.append((c*n+round((note['beat']+note['duration'])*fpb),'off',note['pitch'],0))
 if not loop:events.append((n,'cc',64,0))
 order={'cc':0,'off':1,'on':2};events.sort(key=lambda e:(e[0],order[e[1]]))
 engine=Synth(fonts()[tr['font']],tr['program'],tr['bank'])
 audio=np.zeros((total,2),dtype=np.float32);pos=0
 try:
  for event in events+[(total,'cc',64,0)]:
   end=min(total,event[0])
   while pos<end:
    step=min(8192,end-pos);audio[pos:pos+step]=engine.audio(step);pos+=step
   engine.event(event)
 finally:engine.close()
 if loop:
  # Keep the entire second cycle; one full warm-up, plus a third for seam context.
  period=audio[n:2*n].copy()
  context={'natural_step':float(np.max(np.abs(audio[2*n]-audio[2*n-1]))),'extracted_step':float(np.max(np.abs(period[0]-period[-1]))),'state_drift_rms':float(np.sqrt(np.mean((audio[2*n:3*n]-period)**2)))}
  return period,context
 return audio,{}

def highpass(x,hz):
 return signal.sosfilt(signal.butter(2,hz,fs=SR,btype='highpass',output='sos'),x,axis=0).astype(np.float32)

def periodic_filter(x,hz):
 # Start filter from previous cycle tail; avoids an artificial seam at frame zero.
 tail=min(len(x),SR*2)
 y=highpass(np.concatenate([x[-tail:],x]),hz)
 return y[tail:]

def room(x,loop):
 """Shared modest Schroeder room: no per-stem reverb/chorus stacking."""
 tail=min(len(x),SR*5)
 inp=np.concatenate([x[-tail:],x]) if loop else x
 inp=signal.sosfilt(signal.butter(2,[180,5800],fs=SR,btype='bandpass',output='sos'),inp,axis=0)
 wet=np.zeros_like(inp)
 # Fixed 25–45 ms diffusing delays. No random aesthetic decisions.
 for delay,feedback,cross in [(1117,.69,False),(1361,.65,True),(1559,.62,False),(1789,.59,True)]:
  # sparse recursive comb, evaluated by repeated shifted contributions
  source=inp[:,::-1] if cross else inp
  power=1.;offset=delay
  while power>.001 and offset<len(inp):
   wet[offset:]+=source[:-offset]*(power*.075)
   offset+=delay;power*=feedback
 wet=signal.sosfilt(signal.butter(1,4200,fs=SR,output='sos'),wet,axis=0).astype(np.float32)
 return wet[tail:] if loop else wet

def measure(path):
 cmd=['ffmpeg','-hide_banner','-nostats','-i',str(path),'-af','loudnorm=I=-18:TP=-1:LRA=12:print_format=json','-f','null','-']
 r=subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True,check=True)
 return json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0]

def render(s,force=False):
 cfg=(ROOT/'music/production.json').read_bytes();engine=Path(__file__).read_bytes()
 fingerprint=hashlib.sha256(json.dumps(s,sort_keys=True).encode()+cfg+engine).hexdigest()
 out=WORK/'reports'/f"{s['id']}-production.json"
 if out.exists() and not force:
  old=json.loads(out.read_text())
  if old.get('fingerprint')==fingerprint and all(p.exists() for p in [WORK/'masters'/f"{s['id']}.wav",ROOT/old['web'],ROOT/old['fallback'],Path(old['preview']),*[WORK/'stems'/s['id']/(t['id']+'.wav') for t in s['tracks']]]):print('cached',s['id'],flush=True);return old
 midi(s,ROOT/f"music/scores/{s['id']}.mid")
 stemdir=WORK/'stems'/s['id'];stemdir.mkdir(parents=True,exist_ok=True)
 mix=None;send=None;contexts={};stemstats={}
 loop=s['loop']['enabled']
 for tr in s['tracks']:
  print(s['id'],tr['id'],flush=True)
  stemengine=''.join(inspect.getsource(fn) for fn in [Synth,render_stem,highpass,periodic_filter]).encode()
  stemhash=hashlib.sha256(json.dumps({'track':tr,'tempo':s['tempo_map'],'length':s['length_beats'],'loop':s['loop']},sort_keys=True).encode()+cfg+stemengine).hexdigest()
  meta=stemdir/(tr['id']+'.json');wav=stemdir/(tr['id']+'.wav')
  cached=json.loads(meta.read_text()) if meta.exists() else {}
  if not force and wav.exists() and cached.get('hash')==stemhash:
   rate,x=wavfile.read(wav);assert rate==SR;ctx=cached['context']
  else:
   x,ctx=render_stem(s,tr)
   pan=tr['pan'];x[:,0]*=min(1,1-pan);x[:,1]*=min(1,1+pan)
   x*=tr['gain']
   cutoff=35 if tr['family']=='bass' else 100 if tr['family'] in ('wind','sustain') else 45
   x=periodic_filter(x,cutoff) if loop else highpass(x,cutoff)
   wavfile.write(wav,SR,x)
   meta.write_text(json.dumps({'hash':stemhash,'context':ctx}))
  contexts[tr['id']]=ctx
  # Gain belongs to the authored instrument balance, never a per-track normalizer.
  stemstats[tr['id']]={'peak':float(abs(x).max()),'rms':float(np.sqrt(np.mean(x*x))),'frames':len(x),'role':tr['role'],'font':tr['font'],'program':tr['program'],'gain':tr['gain']}
  if mix is None:mix=np.zeros_like(x);send=np.zeros_like(x)
  mix+=x;send+=x*tr['send']
 mix+=room(send,loop)
 temp=WORK/'cache'/f"{s['id']}-premaster.wav";wavfile.write(temp,SR,mix)
 m=measure(temp);loud=float(m['input_i']);tp=float(m['input_tp'])
 assert math.isfinite(loud) and math.isfinite(tp),(s['id'],m)
 desired=s['target_lufs']-loud
 gain=min(desired,-1.6-tp) # reserve headroom for lossy encoding; no flattening to hit LUFS
 mix*=10**(gain/20)
 tail_trim=0
 if not loop:
  # Keep measured release, not an arbitrary six-second silent export pad.
  active=np.flatnonzero(np.max(np.abs(mix),axis=1)>10**(-90/20))
  end=min(len(mix),int(active[-1])+SR//4+1) if len(active) else len(mix)
  tail_trim=len(mix)-end;mix=mix[:end]
 master=WORK/'masters'/f"{s['id']}.wav"
 # 24-bit PCM lossless master, no fade at looping boundaries.
 floats=WORK/'cache'/f"{s['id']}-master-float.wav";wavfile.write(floats,SR,mix)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(floats),'-c:a','pcm_s24le',str(master)],check=True)
 final=measure(master)
 web=ROOT/'assets/music';web.mkdir(exist_ok=True)
 # Ogg Vorbis carries exact decoded frame count at 44.1k; MP3 fallback checked separately.
 tmp=web/f"{s['id']}.ogg"
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(master),'-c:a','libvorbis','-q:a','5',str(tmp)],check=True)
 digest=hashlib.sha256(tmp.read_bytes()).hexdigest()[:12];dest=web/f"{s['id']}.{digest}.ogg";tmp.replace(dest)
 tmpmp=web/f"{s['id']}.mp3"
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(master),'-c:a','libmp3lame','-b:a','160k',str(tmpmp)],check=True)
 digestmp=hashlib.sha256(tmpmp.read_bytes()).hexdigest()[:12];mp=web/f"{s['id']}.{digestmp}.mp3";tmpmp.replace(mp)
 preview=WORK/'previews'/f"{s['id']}-three-loops.ogg"
 if loop:
  subprocess.run(['ffmpeg','-v','error','-y','-stream_loop','2','-i',str(master),'-c:a','libvorbis','-q:a','5',str(preview)],check=True)
 else:
  import shutil;shutil.copyfile(dest,preview)
 result={'id':s['id'],'fingerprint':fingerprint,'revision':s['revision'],'sample_rate':SR,'frames':len(mix),'duration':len(mix)/SR,'loop':loop,'master':str(master),'stems':stemstats,'continuous_render':contexts,'premaster':m,'gain_db':gain,'tail_trim_frames':tail_trim,'measured':final,'web':dest.relative_to(ROOT).as_posix(),'fallback':mp.relative_to(ROOT).as_posix(),'preview':str(preview),'audition':'未进行主观听觉验证'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 temp.unlink();floats.unlink()
 print('done',s['id'],round(result['duration'],2),final['input_i'],flush=True)
 return result
