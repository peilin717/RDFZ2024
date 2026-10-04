"""Economy regression in disposable browser profiles; conda env rdfz2024."""
import os,json
from playwright.sync_api import sync_playwright
BASE=os.environ.get('RDFZ_TEST_URL','http://127.0.0.1:4173')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox'])
 def run(config=None,old=None):
  c=b.new_context();page=c.new_page()
  if config:
   page.route('**/game-config.js',lambda r:r.fulfill(content_type='text/javascript',body='window.RDFZGameConfig='+json.dumps(config)))
  page.goto(BASE)
  if old:page.evaluate('(s)=>localStorage.setItem("rdfz-profile",JSON.stringify(s))',old)
  page.click('#startBtn');page.wait_for_function("!document.querySelector('#homeScreen').classList.contains('hidden')")
  page.evaluate('finishTutorial()')
  return c,page
 c,page=run();assert page.evaluate('state.gems===3000&&!state.unlimitedGems&&state.owned.length===1')
 page.evaluate('summon(10)');assert page.evaluate('state.gems')==300
 page.evaluate('summon(1)');assert page.evaluate('state.gems')==0
 n=page.evaluate('state.owned.length');page.evaluate('summon(1)');assert page.evaluate('state.gems')==0 and page.evaluate('state.owned.length')==n
 page.wait_for_timeout(300);page.reload();page.click('#startBtn');page.wait_for_function("!document.querySelector('#homeScreen').classList.contains('hidden')")
 assert page.evaluate('state.gems===0&&!state.unlimitedGems');c.close()
 c,page=run({'initialGems':9000,'unlimitedGems':True});page.evaluate('summon(10)');assert page.evaluate('state.gems===9000&&state.unlimitedGems');c.close()
 old={'gems':999999999,'unlimitedGems':True,'owned':['haq','bella'],'cleared':['c1-1'],'tutorialDone':True,'inventory':{'fragments':{},'upgrades':{}}}
 c,page=run(old=old);assert page.evaluate("state.gems===3000&&!state.unlimitedGems&&state.owned.includes('bella')&&state.cleared.includes('c1-1')")
 page.evaluate('summon(1)');page.wait_for_timeout(300);page.reload();page.click('#startBtn');page.wait_for_function("!document.querySelector('#homeScreen').classList.contains('hidden')")
 assert page.evaluate('state.gems===2700&&!state.unlimitedGems');c.close()
 old['gems']=4567;old['unlimitedGems']=False
 c,page=run({'initialGems':8000,'unlimitedGems':False},old);assert page.evaluate('state.gems')==4567;c.close()
 c,page=run({'initialGems':8000,'unlimitedGems':False});assert page.evaluate('state.gems')==8000;c.close()
 b.close();print('PASS: defaults, costs, insufficient funds, reload, overrides, legacy migration, normal save preservation')
