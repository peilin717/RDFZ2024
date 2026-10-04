"""End-to-end web smoke test against a running static server.

pip install playwright
python tools/test_web.py --url http://127.0.0.1:4173 --browser /usr/bin/chromium
All save fixtures live in a disposable browser context.
"""
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import build_opener, ProxyHandler, Request
from playwright.sync_api import sync_playwright, expect

parser = argparse.ArgumentParser()
parser.add_argument('--url', default='http://127.0.0.1:4173')
parser.add_argument('--browser', default='/usr/bin/chromium')
parser.add_argument('--artifacts', default='/tmp/rdfz-web-test')
args = parser.parse_args()
artifacts = Path(args.artifacts)
artifacts.mkdir(parents=True, exist_ok=True)
base = args.url.rstrip('/')

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=args.browser, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    errors, failed_http, requests = [], [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('response', lambda response: failed_http.append(response.url) if response.status >= 400 else None)
    page.on('request', lambda request: requests.append(request.url))
    page.goto(base, wait_until='networkidle')
    assert not any('/assets/' in url for url in requests), 'Start screen downloaded artwork'
    expect(page.locator('#app')).to_be_hidden()
    expect(page.locator('#startBtn')).to_be_visible()
    page.screenshot(path=str(artifacts / 'start.png'))

    def settle():
        page.wait_for_function("document.querySelectorAll('.art-loading').length === 0")
        page.wait_for_load_state('networkidle')

    page.click('#startBtn')
    page.click('#skipTutorial')
    expect(page.locator('#homeScreen')).to_be_visible()
    page.click('#rosterBtn')
    # IntersectionObserver runs after layout; an empty loading set is not readiness.
    page.wait_for_function("[...document.querySelectorAll('#rosterGrid [data-art-src]')].some(e=>e.style.getPropertyValue('--art'))")
    settle()
    cards = page.locator('#rosterGrid [data-art-src]')
    total_cards = cards.count()
    assert total_cards > 20
    loaded = page.evaluate("[...document.querySelectorAll('#rosterGrid [data-art-src]')].filter(e=>e.style.getPropertyValue('--art')).length")
    assert 0 < loaded < cards.count(), (loaded, cards.count())
    assert not any('/story/' in url or '/web/story-' in url for url in requests)
    page.screenshot(path=str(artifacts / 'roster.png'))
    last = cards.last
    last.scroll_into_view_if_needed()
    page.wait_for_function("[...document.querySelectorAll('#rosterGrid [data-art-src]')].at(-1).style.getPropertyValue('--art').includes('.webp')")
    last.click()
    settle()
    assert page.locator('#heroDetailArt').evaluate("e=>e.style.getPropertyValue('--art')").find('-full.') >= 0
    page.screenshot(path=str(artifacts / 'detail.png'))
    page.click('#heroDetail [data-close]')
    page.click('#rosterScreen [data-hide]')

    page.click('#summonBtn')
    page.click('#tenPull')
    expect(page.locator('#pullCards .pull-card')).to_have_count(10)
    page.wait_for_load_state('networkidle')
    # Verify generated inline CSS remains valid inside HTML attributes.
    assert '.webp' in page.locator('.pull-art').first.evaluate("e=>getComputedStyle(e).backgroundImage")
    page.click('#closePull')
    page.click('#summonScreen [data-hide]')
    page.click('#battleBtn')
    page.click('.chapter-node[data-chapter="1"]')
    page.click('.stage-node[data-stage="c1-1"]')
    page.click('#recommendTeam')
    expect(page.locator('#confirmFormation')).to_be_enabled()
    page.click('#confirmFormation')
    expect(page.locator('#app')).to_be_visible()
    expect(page.locator('#playerTeam .unit')).to_have_count(5)
    page.wait_for_load_state('networkidle')
    assert '.webp' in page.locator('#playerTeam .avatar').first.evaluate("e=>getComputedStyle(e).backgroundImage")
    page.screenshot(path=str(artifacts / 'battle.png'))
    page.click('#basicAttack')
    page.wait_for_function('state.round >= 2 && !state.busy', timeout=30000)
    page.click('#pauseBtn')
    expect(page.locator('#pauseScreen')).to_be_visible()
    page.click('#resumeBattle')
    page.click('#pauseBtn')
    saved = page.evaluate('({owned: [...state.owned].sort(), team: state.savedTeamIds, gems: state.gems})')
    page.click('#returnHome')
    expect(page.locator('#homeScreen')).to_be_visible()
    page.wait_for_function('state.owned.length > 4')
    restored = page.evaluate('({owned: [...state.owned].sort(), team: state.savedTeamIds, gems: state.gems})')
    assert saved == restored, (saved, restored)
    expect(page.locator('#app')).to_be_hidden()

    # Test later chapter screens with explicit fixtures instead of altering real saves.
    page.evaluate("state.cleared = allCampaignStages().map(s=>s.id); state.owned = heroes.map(h=>h.id); state.tutorialDone = true")
    page.evaluate("selectCampaignStage('c1-2'); recommendFormation(); confirmFormation()")
    page.wait_for_load_state('networkidle')
    assert page.evaluate('state.enemies[0].heroId') == 'lzy'
    assert '.webp' in page.locator('#enemyTeam .avatar').first.evaluate("e=>getComputedStyle(e).backgroundImage")
    # Defeated variants are also routed through the manifest.
    page.evaluate('state.team[0].alive=false; state.team[0].hp=0; render()')
    page.wait_for_load_state('networkidle')
    assert 'defeated-' in page.locator('#playerTeam .avatar').first.evaluate("e=>getComputedStyle(e).backgroundImage")
    page.evaluate('returnToChapterAfterBattle()')
    page.evaluate("openStageNarrative('pre','adminFinal')")
    settle()
    first_art = page.locator('#narrativePoster').evaluate('e=>e.style.backgroundImage')
    assert 'admin-pre-1-full' in first_art
    page.click('#nextNarrative')
    settle()
    assert 'admin-pre-2-full' in page.locator('#narrativePoster').evaluate('e=>e.style.backgroundImage')
    page.screenshot(path=str(artifacts / 'narrative.png'))
    page.evaluate("$('#stageNarrative').classList.add('hidden'); openBasketballGame('c3-2')")
    expect(page.locator('#basketballGame')).to_be_visible()
    page.click('#shootBall')
    page.click('#leaveBasketball')
    page.evaluate('openBookSortingPuzzle()')
    for number in [2, 3, 5, 8, 13, 21]:
        page.click(f'.puzzle-book[data-n="{number}"]')
    expect(page.locator('#chapterMapScreen')).to_be_visible()
    page.evaluate('openSoulHunt()')
    page.wait_for_load_state('networkidle')
    assert 'rooftop-haunting-full' in page.locator('#soulHuntScreen').evaluate('e=>getComputedStyle(e).backgroundImage')
    page.evaluate("$('#soulHuntScreen').classList.add('hidden'); openParkourGame()")
    expect(page.locator('#parkourGame')).to_be_visible()
    page.keyboard.press('ArrowLeft')
    page.click('#leaveParkour')
    assert not errors, errors
    assert not failed_http, failed_http

    # Every generated server resource must exist and have the right MIME type.
    urls = page.evaluate('Object.values(RDFZ_ASSET_MANIFEST).flatMap(Object.values)')
    def check_asset(path):
        opener = build_opener(ProxyHandler({}))
        with opener.open(Request(f'{base}/{path}', method='HEAD'), timeout=15) as response:
            assert response.status == 200
            assert response.headers.get_content_type() == 'image/webp', path
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(check_asset, urls))
    context.close()

    # Fresh session: injected image failure must have a usable retry action.
    recovery = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = recovery.new_page()
    page.goto(base, wait_until='networkidle')
    page.click('#startBtn'); page.click('#skipTutorial')
    page.route('**/assets/web/heroes-haq-full.*.webp', lambda route: route.abort())
    page.evaluate("openHeroDetail('haq')")
    expect(page.locator('#heroDetailArt .art-retry')).to_be_visible()
    page.unroute('**/assets/web/heroes-haq-full.*.webp')
    page.click('#heroDetailArt .art-retry')
    page.wait_for_function("document.querySelector('#heroDetailArt').style.getPropertyValue('--art').includes('.webp')")
    expect(page.locator('#heroDetailArt .art-retry')).to_have_count(0)
    # A failed/stale image must never replace a more recently requested one.
    page.evaluate("openHeroDetail('fjy'); openHeroDetail('zbh')")
    settle()
    assert 'heroes-zbh-full' in page.locator('#heroDetailArt').evaluate("e=>e.style.getPropertyValue('--art')")
    recovery.close()

    # Narrow touch viewport: offscreen cards remain deferred and tap opens details.
    mobile = browser.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True)
    page = mobile.new_page()
    page.goto(base, wait_until='networkidle')
    page.click('#startBtn'); page.click('#skipTutorial'); page.click('#rosterBtn')
    settle()
    page.locator('#rosterGrid [data-art-src]').first.tap()
    expect(page.locator('#heroDetail')).to_be_visible()
    settle()
    page.screenshot(path=str(artifacts / 'mobile-detail.png'))
    mobile.close()
    browser.close()
    print(json.dumps({'result':'passed','assets_checked':len(urls),'roster_initial_cards':loaded,'roster_total_cards':total_cards,'artifacts':str(artifacts)},ensure_ascii=False))
