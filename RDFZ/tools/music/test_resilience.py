"""Mobile UI, fallback codec, failed requests and cancelled decodes."""
import json,os
from playwright.sync_api import sync_playwright
from render import WORK
BASE=os.environ.get('RDFZ_TEST_URL','http://127.0.0.1:4173')
checks=[]
def check(name,ok,detail=None):
 checks.append({'name':name,'passed':bool(ok),'detail':detail});(WORK/'reports/browser-resilience.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n');assert ok,(name,detail)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 context=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);page=context.new_page()
 requests=[];page.on('request',lambda r:requests.append(r.url) if '/assets/music/' in r.url else None)
 page.route('**/assets/music/*.ogg',lambda route:route.abort('failed'))
 page.goto(BASE,wait_until='networkidle');page.tap('#startBtn')
 page.wait_for_function("RDFZMusic.diagnostics().current==='home'",timeout=30000)
 d=page.evaluate('RDFZMusic.diagnostics()')
 check('MP3 fallback after failed Vorbis request',d['decoded'][-1]['url'].endswith('.mp3') and not d['failures'],d)
 check('Entering home does not download title music',not any('/title.' in x for x in requests),requests)
 page.evaluate("finishTutorial();state.cleared=campaignChapters.flatMap(c=>c.stages.map(s=>s.id))")
 page.screenshot(path=str(WORK/'visuals/mobile-home-with-music.png'))
 check('Mobile mute control is visible and reachable',page.locator('#hubSound').is_visible())
 page.route('**/assets/music/basement*.mp3',lambda route:route.abort('failed'))
 page.evaluate('openChapterMap(1)');page.wait_for_function("RDFZMusic.diagnostics().failures.length>0",timeout=30000)
 d=page.evaluate('RDFZMusic.diagnostics()');check('Both codecs failing keeps prior cue and game usable',d['current']=='home' and page.locator('#stagePath').is_visible(),d)
 page.unroute('**/assets/music/basement*.mp3');page.evaluate('RDFZMusic.refresh()')
 page.wait_for_function("RDFZMusic.diagnostics().current==='basement'",timeout=30000);check('Explicit retry recovers after network failure',True)
 page.tap('#musicToggle');n=len(requests);page.evaluate('openChapterMap(5)');page.wait_for_timeout(400)
 check('Muted mobile navigation makes no request',len(requests)==n)
 page.tap('#musicToggle');page.wait_for_function("RDFZMusic.diagnostics().current==='library'",timeout=30000);check('Unmute loads current scene, not previous scene',True)
 page.unroute('**/assets/music/*.ogg')
 # Delay response in the browser, allowing later scene changes to overtake fetch.
 page.evaluate('''()=>{const native=window.fetch;window.fetch=async(...args)=>{if(String(args[0]).includes('/garden.'))await new Promise(r=>setTimeout(r,900));return native(...args)};
 openChapterMap(4);RDFZMusic.refresh();setTimeout(()=>{openChapterMap(9);RDFZMusic.refresh()},30)}''')
 page.wait_for_function("RDFZMusic.diagnostics().current==='senior'",timeout=30000);page.wait_for_timeout(1800)
 d=page.evaluate('RDFZMusic.diagnostics()');check('Late request cannot replace newer scene',d['current']=='senior' and d['live']==1,d)
 # Visibility mapping of real mini-game routines, then stop their timers.
 page.evaluate('openDrivingGame();RDFZMusic.refresh()');check('Driving maps to laboratory',page.evaluate('RDFZMusic.resolveScene()')=='laboratory')
 page.evaluate('leaveParkour();openParkourGame();RDFZMusic.refresh()');check('Parkour maps to playground',page.evaluate('RDFZMusic.resolveScene()')=='playground')
 page.evaluate("leaveParkour();openBasketballGame('c3-2');RDFZMusic.refresh()");check('Basketball minigame maps to basketball',page.evaluate('RDFZMusic.resolveScene()')=='basketball')
 context.close();b.close()
print('Resilience checks:',len(checks))
