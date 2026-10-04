"""Actual scene inventory and static deployment/preview smoke checks."""
import json,os,hashlib,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
from notation import ROOT
from render import WORK
BASE=os.environ.get('RDFZ_TEST_URL','http://127.0.0.1:4180')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);page=b.new_page()
 page.goto(BASE,wait_until='networkidle')
 mapping=page.evaluate('''()=>{
 const title=RDFZMusic.resolveScene();document.getElementById('startScreen').classList.add('hidden');
 const stages=[];
 for(const c of campaignChapters)for(const s of c.stages){state.chapter=c.index;state.currentStageId=s.id;document.getElementById('app').classList.remove('hidden');
 const combat=RDFZMusic.resolveScene();document.getElementById('app').classList.add('hidden');document.getElementById('chapterMapScreen').classList.remove('hidden');const map=RDFZMusic.resolveScene();document.getElementById('chapterMapScreen').classList.add('hidden');
 const special={'c3-2':'basketball','c3-3':'basketball','c3-4':'basketball','c5-1':'library','c5-2':'library','c7-1':'playground','c9-8':'ending','c10-1':'laboratory'};
 stages.push({stage:s.id,name:s.name,chapter:c.index,map,play:special[s.id]||combat,optional:!!s.optional});}
 const narrativeChapters={final:1,garden:2,rooftop:2,basketball:3,centralLawn:4,ancientTree:4,libraryDog:5,reportHall:6,roastRack:7,juniorMutiny:8,juniorPossession:8,windowHall:9,physicsOffice:9,seniorCafe:9,adminFinal:11};
 const narratives=[];
 for(const [scenario,story] of Object.entries(stageNarratives))for(const mode of ['pre','post'])if(story[mode]?.length){state.chapter=narrativeChapters[scenario];openStageNarrative(mode,scenario);narratives.push({scenario,mode,cue:RDFZMusic.resolveScene()});}
 document.getElementById('stageNarrative').classList.add('hidden');
 return {title,stages,narratives,inherit:['rosterScreen','heroDetail','bagScreen','formationScreen','ratesScreen','tutorialScreen','helpScreen','pauseScreen','battleStatsScreen'],music_ids:Object.keys(RDFZMusicManifest.cues)};
}''')
 assert all(x['map'] in mapping['music_ids'] and x['play'] in mapping['music_ids'] for x in mapping['stages'])
 (ROOT/'music/scene-mapping.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
 resources=page.evaluate('Object.values(RDFZMusicManifest.cues).flatMap(c=>[c.ogg,c.mp3])')
 statuses=[]
 for url in resources+['music-credits.html','music/licenses/GeneralUser-GS.txt','music/licenses/Salamander-FreePats.txt']:
  response=page.request.get(BASE+'/'+url);assert response.status==200,(url,response.status)
  statuses.append({'url':url,'status':response.status,'bytes':len(response.body())})
 assert len(resources)==50
 requests=[];page.on('request',lambda r:requests.append(r.url) if r.url.endswith(('.ogg','.mp3','.wav')) else None)
 page.goto('http://127.0.0.1:4176/preview.html',wait_until='networkidle')
 assert page.locator('article').count()==25 and page.locator('audio').count()==50
 assert not requests,requests
 page.click('h1');page.locator('audio').first.evaluate('(a)=>a.play()');page.wait_for_function("document.querySelector('audio').currentTime>.2")
 page.wait_for_function("(d)=>Math.abs(document.querySelector('audio').duration-d)<.01",arg=json.loads((ROOT/'music/reports/production-summary.json').read_text())[0]['duration'])
 page.locator('audio').first.evaluate('(a)=>a.currentTime=100');page.wait_for_function("document.querySelector('audio').currentTime>=100")
 page.locator('audio').first.evaluate('(a)=>{a.pause();a.currentTime=0}')
 preview_durations=page.evaluate('''async()=>{const out=[];for(const a of document.querySelectorAll('audio')){a.preload='metadata';a.load();if(a.readyState<1)await new Promise((resolve,reject)=>{a.onloadedmetadata=resolve;a.onerror=()=>reject(new Error(a.src))});out.push({url:a.src,duration:a.duration})}return out}''')
 expected=json.loads((ROOT/'music/reports/production-summary.json').read_text())
 for cue,pair in zip(expected,[preview_durations[i:i+2] for i in range(0,len(preview_durations),2)]):
  assert abs(pair[0]['duration']-cue['duration'])<.01,(cue['id'],pair)
  assert abs(pair[1]['duration']-cue['duration']*(3 if cue['id'] in [c['id'] for c in json.loads((ROOT/'music/cues.json').read_text())['bgm']] else 1))<.01,(cue['id'],pair)
 page.screenshot(path=str(WORK/'visuals/preview.png'))
 forbidden=[str(p.relative_to(ROOT/'dist')) for p in (ROOT/'dist').rglob('*') if p.suffix.lower() in ('.wav','.sf2','.sfz','.mid','.musicxml','.py')]
 assert not forbidden,forbidden
 result={'url':BASE,'actual_stages':len(mapping['stages']),'narrative_variants':len(mapping['narratives']),'resource_checks':statuses,'preview_tracks':25,'preview_players':50,'preview_preloads_audio':False,'preview_playback':True,'preview_seek_to_100_seconds':True,'preview_metadata':preview_durations,'large_production_artifacts_in_deployment':forbidden,'public_vercel_deployment':'not performed; static local build tested'}
 (WORK/'reports/delivery-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');b.close()
print('Delivery:',result['actual_stages'],'stages,',result['narrative_variants'],'narrative variants,',len(statuses),'HTTP assets')
