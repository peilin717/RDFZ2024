"""Browser integration, actual codec decode and Web Audio loop scheduling.
Uses a fresh disposable browser profile, never the player's saved profile.
"""
import json,os,time
from pathlib import Path
from playwright.sync_api import sync_playwright
from render import WORK
BASE=os.environ.get('RDFZ_TEST_URL','http://127.0.0.1:4173')
report={'url':BASE,'checks':[],'codec_checks':[],'errors':[],'subjective_audition':'未进行主观听觉验证'}
def check(name,value,details=None):
 report['checks'].append({'name':name,'passed':bool(value),'details':details});(WORK/'reports/browser-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');assert value,(name,details)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 context=browser.new_context(viewport={'width':1360,'height':900});page=context.new_page();audio_requests=[]
 page.on('pageerror',lambda e:report['errors'].append(str(e)))
 page.on('request',lambda r:audio_requests.append(r.url) if '/assets/music/' in r.url else None)
 page.goto(BASE,wait_until='networkidle');page.wait_for_timeout(600)
 check('No audio transfer before user gesture',not audio_requests,audio_requests[:])
 page.click('#startBtn');page.wait_for_function("window.RDFZMusic?.diagnostics().current==='home'",timeout=30000)
 page.evaluate("finishTutorial()")
 d=page.evaluate('RDFZMusic.diagnostics()');check('Gesture unlock and home audio',d['unlocked'] and d['current']=='home',d)
 page.screenshot(path=str(WORK/'visuals/home-with-music.png'))
 before=page.evaluate('RDFZMusic.diagnostics().starts');page.evaluate('openRoster()');page.wait_for_timeout(500)
 check('Roster inherits home without restarting',page.evaluate('RDFZMusic.diagnostics().starts')==before)
 page.evaluate("document.getElementById('rosterScreen').classList.add('hidden');openCampaignMap();state.cleared=campaignChapters.flatMap(c=>c.stages.map(s=>s.id))")
 mappings=[]
 for chapter,cue in enumerate(['basement','yifu','basketball','garden','library','canteen','playground','junior','senior','laboratory','admin'],1):
  page.evaluate('(n)=>openChapterMap(n)',chapter)
  page.wait_for_function('(id)=>RDFZMusic.diagnostics().desired===id',arg=cue)
  mappings.append([chapter,page.evaluate('RDFZMusic.resolveScene()')])
 check('All eleven chapter mappings',all(x[1]==y for x,y in zip(mappings,['basement','yifu','basketball','garden','library','canteen','playground','junior','senior','laboratory','admin'])),mappings)
 page.wait_for_function("RDFZMusic.diagnostics().current==='admin'",timeout=30000)
 page.evaluate("openStageNarrative('pre','adminFinal')");page.wait_for_function("RDFZMusic.diagnostics().stingers.includes('revelation')",timeout=20000)
 check('Revelation trigger',True)
 page.evaluate("openStageNarrative('post','adminFinal')");page.wait_for_function("RDFZMusic.diagnostics().current==='ending'",timeout=30000)
 page.screenshot(path=str(WORK/'visuals/ending-with-music.png'))
 check('Final epilogue maps to ending',True)
 page.evaluate("document.getElementById('stageNarrative').classList.add('hidden');state.currentStageId='c1-1';state.team=heroes.slice(0,5).map((h,i)=>({...cloneHero(h),pos:i+1}));document.getElementById('app').classList.remove('hidden');enterBattle()")
 page.wait_for_function("RDFZMusic.diagnostics().current==='battle'",timeout=30000)
 check('Ordinary battle music',True)
 start=page.evaluate('RDFZMusic.diagnostics().starts');page.evaluate('render();render();render()');page.wait_for_timeout(400)
 check('Battle rerenders do not restart music',page.evaluate('RDFZMusic.diagnostics().starts')==start)
 page.evaluate("state.currentStageId='c2-6';RDFZMusic.refresh()")
 page.wait_for_function("RDFZMusic.diagnostics().current==='boss'",timeout=30000);check('Boss music',True)
 page.evaluate("state.currentStageId='c11-4';RDFZMusic.refresh()")
 page.wait_for_function("RDFZMusic.diagnostics().current==='final'",timeout=30000);check('Final battle music',True)
 page.evaluate("RDFZ.emit('stageComplete',{chapter:11,stageId:'c11-4',win:false})")
 page.wait_for_function("RDFZMusic.diagnostics().stingers.includes('defeat')",timeout=20000);check('Defeat trigger',True)
 page.evaluate("RDFZ.emit('stageComplete',{chapter:1,stageId:'c1-1',win:true})")
 page.wait_for_function("RDFZMusic.diagnostics().stingers.includes('chapter-clear')",timeout=20000);check('Chapter clear trigger',True)
 page.evaluate("RDFZ.emit('stageComplete',{chapter:1,stageId:'c1-1',win:true})")
 page.wait_for_function("RDFZMusic.diagnostics().stingers.includes('victory')",timeout=20000);check('Victory trigger',True)
 page.evaluate("document.getElementById('app').classList.add('hidden');openSummon()")
 page.wait_for_function("RDFZMusic.diagnostics().current==='summon'",timeout=30000)
 page.evaluate("RDFZ.emit('summon',{pulls:[heroes.find(h=>h.rank==='S').id]})")
 page.wait_for_function("RDFZMusic.diagnostics().stingers.includes('rare')",timeout=20000)
 page.evaluate("RDFZ.emit('summon',{pulls:[heroes.find(h=>h.rank!=='S').id]})")
 page.wait_for_function("RDFZMusic.diagnostics().stingers.includes('recruit')",timeout=20000);check('Recruit and rare triggers',True)
 # Save fields remain byte-identical across audio-only operations.
 saved=page.evaluate('JSON.stringify({gems:state.gems,owned:state.owned,cleared:state.cleared,team:state.savedTeamIds})')
 page.click('#musicToggle');page.wait_for_timeout(300)
 check('Mute independent of player progression',saved==page.evaluate('JSON.stringify({gems:state.gems,owned:state.owned,cleared:state.cleared,team:state.savedTeamIds})'))
 requests=len(audio_requests)
 page.evaluate("document.getElementById('summonScreen').classList.add('hidden');openChapterMap(4)");page.wait_for_timeout(500)
 check('Muted navigation starts no downloads',len(audio_requests)==requests)
 page.reload(wait_until='networkidle');page.wait_for_timeout(300)
 check('Mute survives reload',page.evaluate('RDFZMusic.diagnostics().muted'))
 # Codec decode, and an actual offline-rendered loop transition for EVERY cue.
 # This is signal validation; no claim of hearing the result.
 result=page.evaluate('''async()=>{
 const ac=new AudioContext({sampleRate:44100}),out=[];
 for(const [id,c] of Object.entries(RDFZMusicManifest.cues)){
  for(const codec of ['ogg','mp3']){
   const r=await fetch(c[codec]);if(!r.ok)throw new Error(c[codec]);
   const b=await ac.decodeAudioData(await r.arrayBuffer());
   const item={id,codec,frames:b.length,expected:c.frames,rate:b.sampleRate,error:0};
   if(c.loop){
    const n=22050,off=new OfflineAudioContext(2,n*2,44100),s=off.createBufferSource();s.buffer=b;s.loop=true;s.loopEnd=c.frames/44100;s.connect(off.destination);s.start(0,(c.frames-n)/44100);
    const rendered=await off.startRendering();
    for(let ch=0;ch<2;ch++){const x=rendered.getChannelData(ch),y=b.getChannelData(ch);for(let i=0;i<n*2;i++){const expected=y[(c.frames-n+i)%c.frames];item.error=Math.max(item.error,Math.abs(x[i]-expected));}}
   }
   out.push(item);
  }
 }
 await ac.close();return out;
}''')
 report['codec_checks']=result
 check('All 50 browser decodes preserve frame counts',all(abs(r['frames']-r['expected'])<=1 and r['rate']==44100 for r in result),result)
 check('All 38 BGM Web Audio boundary schedules preserve samples',all(r['error']<1e-5 for r in result),max(r['error'] for r in result))
 # Unmute then race slow requests; stale responses must not start an old cue.
 page.click('#musicToggle');page.click('#startBtn');page.evaluate("finishTutorial();state.cleared=campaignChapters.flatMap(c=>c.stages.map(s=>s.id))")
 page.wait_for_function("RDFZMusic.diagnostics().current==='home'",timeout=30000)
 page.evaluate("openChapterMap(1);RDFZMusic.refresh();openChapterMap(5);RDFZMusic.refresh();openChapterMap(9);RDFZMusic.refresh();openChapterMap(4);RDFZMusic.refresh()")
 page.wait_for_function("RDFZMusic.diagnostics().current==='garden'",timeout=30000);page.wait_for_timeout(1100)
 d=page.evaluate('RDFZMusic.diagnostics()')
 check('Rapid navigation resolves only final requested cue',d['current']=='garden' and d['live']==1 and d['maxLiveBgm']<=2,d)
 check('Decoded cache stays bounded',len(d['bgmCache'])<=2 and len(d['fxCache'])<=2,d)
 check('No uncaught browser errors',not report['errors'],report['errors'])
 check('No codec/load errors in final player session',not d['failures'],d['failures'])
 context.close();browser.close()
(WORK/'reports/browser-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Browser checks:',len(report['checks']),'codec decodes:',len(report['codec_checks']))
