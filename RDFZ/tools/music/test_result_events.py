"""Actual game result emitter, including repeat and optional-stage semantics."""
import json
from playwright.sync_api import sync_playwright
from render import WORK
report=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page();page.goto('http://127.0.0.1:4180',wait_until='networkidle');page.click('#startBtn');page.wait_for_function("RDFZMusic.diagnostics().current==='home'")
 page.evaluate("finishTutorial();window.capturedResults=[];RDFZ.on('stageComplete',e=>capturedResults.push(e.detail));state.team=heroes.slice(0,5).map((h,i)=>({...cloneHero(h),pos:i+1}));state.chapter=1;state.currentStageId='c1-1';state.cleared=['c1-1'];showResult(true)")
 page.wait_for_function("RDFZMusic.diagnostics().stingers.at(-1)==='victory'");d=page.evaluate('capturedResults.at(-1)');assert d['firstClear']==False;report.append({'case':'real showResult repeated clear','passed':True,'event':d})
 page.evaluate("state.cleared=campaignChapters[0].stages.filter(s=>s.id!=='c1-6').map(s=>s.id);state.currentStageId='c1-6';showResult(true)")
 page.wait_for_function("RDFZMusic.diagnostics().stingers.at(-1)==='chapter-clear'");d=page.evaluate('capturedResults.at(-1)');assert d['firstClear']==True;report.append({'case':'real final main stage first clear','passed':True,'event':d})
 page.evaluate("state.chapter=2;state.cleared=campaignChapters[1].stages.filter(s=>!s.optional).map(s=>s.id);state.currentStageId='c2-ex';showResult(true)")
 page.wait_for_function("RDFZMusic.diagnostics().stingers.at(-1)==='victory'");d=page.evaluate('capturedResults.at(-1)');assert d['firstClear']==True;report.append({'case':'optional clear does not replay chapter completion','passed':True,'event':d})
 page.evaluate('showResult(false)');page.wait_for_function("RDFZMusic.diagnostics().stingers.at(-1)==='defeat'");report.append({'case':'real loss result','passed':True})
 assert not page.evaluate('RDFZMusic.diagnostics().failures');b.close()
(WORK/'reports/result-event-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('Actual result event checks:',len(report))
