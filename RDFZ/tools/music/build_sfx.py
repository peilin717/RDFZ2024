"""Authored MIDI gestures -> pinned GeneralUser SF2 -> offline mix -> Ogg/MP3.
Run in conda env rdfz2024. No runtime synthesis, downloads or music API.
"""
import hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from notation import ROOT, midi
from render import Synth, SR, highpass, room

WORK = ROOT.parent / 'music-work'

def build():
    cfg = json.loads((ROOT / 'music/production.json').read_text())['soundfonts']['general']
    font = WORK / cfg['path']
    if hashlib.sha256(font.read_bytes()).hexdigest() != cfg['sha256']:
        raise RuntimeError('GeneralUser soundfont differs from pinned BGM source')
    catalog = json.loads((ROOT / 'music/sfx/gestures.json').read_text())
    out = ROOT / 'assets/sfx'
    out.mkdir(exist_ok=True)
    masters = WORK / 'sfx'; masters.mkdir(parents=True, exist_ok=True)
    manifest = {'schema': 1, 'cues': {}}
    reports = []
    for cue in catalog:
        frames = round(cue['duration'] * SR)
        mix = np.zeros((frames, 2), np.float32)
        tracks = []
        for i, layer in enumerate(cue['layers']):
            engine = Synth(font, layer['program'], layer.get('bank', 0))
            events = []
            notes = []
            for start, duration, pitch, velocity in layer['notes']:
                events += [(round(start * SR), 'on', pitch, velocity),
                           (round((start + duration) * SR), 'off', pitch, 0)]
                notes.append({'beat':start * 2, 'duration':duration * 2, 'pitch':pitch, 'velocity':velocity})
            events.sort(key=lambda e:(e[0], e[1] == 'on'))
            audio = np.zeros_like(mix); pos = 0
            try:
                for event in events + [(frames, 'cc', 123, 0)]:
                    end = min(frames, event[0])
                    if end > pos: audio[pos:end] = engine.audio(end-pos); pos=end
                    engine.event(event)
            finally: engine.close()
            mix += highpass(audio, 65) * layer['gain']
            tracks.append({'id':f'layer-{i}', 'family':'drums' if layer.get('bank') == 128 else 'plucked',
                           'program':layer['program'], 'pan':0, 'controls':[], 'notes':notes})
        # Short shared room, gentle end taper; preserve authored relative layer gains.
        mix += room(mix * .055, False)
        fade = min(round(.065*SR), frames//3)
        mix[-fade:] *= np.linspace(1, 0, fade)[:,None]
        mix[:88] *= np.linspace(0, 1, 88)[:,None]
        peak = float(np.max(np.abs(mix)))
        if peak < 1e-5: raise RuntimeError('Silent cue: ' + cue['id'])
        mix *= 10**(cue['peak_db']/20) / peak
        master = masters / (cue['id'] + '.wav')
        wavfile.write(master, SR, mix)
        score = {'tempo_map':[{'beat':0,'bpm':120}], 'length_beats':cue['duration']*2, 'tracks':tracks}
        midi(score, ROOT / 'music/sfx' / (cue['id']+'.mid'))
        record = {'title':cue['title'], 'frames':frames, 'sampleRate':SR, 'duration':cue['duration'], 'group':cue['group']}
        measurements = {}
        for ext, codec in [('ogg',['-c:a','libvorbis','-q:a','5']), ('mp3',['-c:a','libmp3lame','-b:a','160k'])]:
            temp = masters / (cue['id']+'.'+ext)
            subprocess.run(['ffmpeg','-v','error','-y','-i',str(master),*codec,str(temp)],check=True)
            data = temp.read_bytes(); digest=hashlib.sha256(data).hexdigest()[:12]
            dest=out/(cue['id']+'.'+digest+'.'+ext);dest.write_bytes(data)
            record[ext]=dest.relative_to(ROOT).as_posix()
            raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(dest),'-f','f32le','-ac','2','-ar',str(SR),'-'])
            decoded=np.frombuffer(raw,dtype=np.float32).reshape(-1,2)
            assert abs(len(decoded)-frames)<=round(.03*SR), (cue['id'],ext,len(decoded),frames)
            assert np.isfinite(decoded).all() and 0 < np.max(np.abs(decoded)) < .9
            measurements[ext]={'bytes':len(data),'frames':len(decoded),'peak_db':float(20*np.log10(np.max(np.abs(decoded))))}
        manifest['cues'][cue['id']]=record
        reports.append({'id':cue['id'],'duration':cue['duration'],'codecs':measurements})
    (ROOT/'sfx-manifest.js').write_text('window.RDFZSfxManifest = '+json.dumps(manifest,ensure_ascii=False,separators=(',',':'))+';\n')
    (ROOT/'music/reports/sfx-production.json').write_text(json.dumps({'source_sha256':cfg['sha256'],'python':sys.version.split()[0],'checks':reports,'subjective_audition':False},ensure_ascii=False,indent=2)+'\n')
    keep={Path(c[k]).name for c in manifest['cues'].values() for k in ('ogg','mp3')}
    for file in out.iterdir():
        if file.name.split('.')[0] in manifest['cues'] and file.suffix in ('.ogg','.mp3') and file.name not in keep:
            file.unlink()
    print('Built and decoded',len(reports),'sample-rendered effects')

if __name__ == '__main__': build()
