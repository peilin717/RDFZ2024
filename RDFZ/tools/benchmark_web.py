"""Compare cold-start downloads using two static servers and identical networking."""
import argparse
import json
import statistics
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser()
parser.add_argument('--before',default='http://127.0.0.1:4174')
parser.add_argument('--after',default='http://127.0.0.1:4173')
parser.add_argument('--browser',default='/usr/bin/chromium')
parser.add_argument('--runs',type=int,default=3)
args=parser.parse_args()
result={'network':{'download_mbps':10,'latency_ms':80},'runs':args.runs}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=args.browser,args=['--no-sandbox'])
    for label,url in [('before',args.before),('after',args.after)]:
        samples=[]
        for index in range(args.runs):
            context=browser.new_context(viewport={'width':1440,'height':900})
            page=context.new_page()
            cdp=context.new_cdp_session(page)
            cdp.send('Network.enable')
            cdp.send('Network.emulateNetworkConditions',{
                'offline':False, 'latency':80,
                'downloadThroughput':10_000_000/8,
                'uploadThroughput':1_000_000/8,
                'connectionType':'cellular4g'
            })
            page.goto(url,wait_until='networkidle')
            samples.append(page.evaluate('''() => {
                const nav=performance.getEntriesByType('navigation')[0];
                const resources=performance.getEntriesByType('resource');
                return {bytes:resources.reduce((n,r)=>n+r.encodedBodySize,nav.encodedBodySize),
                    imageRequests:resources.filter(r=>r.name.includes('/assets/')).length,
                    settledMs:Math.max(nav.responseEnd,...resources.map(r=>r.responseEnd)),
                    domReadyMs:nav.domContentLoadedEventEnd};
            }'''))
            context.close()
        result[label]={'samples':samples,'median':{key:statistics.median(s[key] for s in samples) for key in samples[0]}}
    browser.close()
print(json.dumps(result,ensure_ascii=False,indent=2))
