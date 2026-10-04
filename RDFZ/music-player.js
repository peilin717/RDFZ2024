/* Static, gesture-unlocked game music. No sample libraries or composition at runtime. */
(() => {
  'use strict';
  const manifest = window.RDFZMusicManifest;
  if (!manifest) return;
  const visible = id => {const el=document.getElementById(id);return !!el && !el.classList.contains('hidden');};
  const chapters=['basement','yifu','basketball','garden','library','canteen','playground','junior','senior','laboratory','admin'];
  const bossStages=new Set(['c1-6','c2-6','c2-ex','c4-4','c5-4','c6-4','c8-6','c9-7','c10-3']);
  function resolveScene() {
    if (visible('startScreen')) return 'title';
    if (visible('stageNarrative')) {
      if (narrativeScenario==='seniorCafe' || (narrativeMode==='post' && ['adminFinal','final','rooftop'].includes(narrativeScenario))) return 'ending';
      if (narrativeScenario==='adminFinal') return 'admin';
      if (narrativeMode==='pre' && ['garden','libraryDog','juniorMutiny','juniorPossession','ancientTree','reportHall'].includes(narrativeScenario)) return 'suspense';
      return chapters[state.chapter-1] || 'home';
    }
    if (visible('soulHuntScreen')) return 'boss';
    if (visible('basketballGame')) return 'basketball';
    if (visible('libraryPuzzle')) return 'library';
    if (visible('parkourGame')) return document.getElementById('parkourGame').classList.contains('driving-mode') ? 'laboratory' : 'playground';
    if (visible('summonScreen') || visible('summonResult')) return 'summon';
    // Result/pause overlays inherit the battle, rather than retriggering it.
    if (visible('app')) return state.currentStageId==='c11-4' ? 'final' : bossStages.has(state.currentStageId) ? 'boss' : 'battle';
    if (visible('chapterMapScreen')) return chapters[state.chapter-1] || 'home';
    if (visible('homeScreen') || visible('campaignMapScreen') || visible('storyScreen')) return 'home';
    return desired || 'home'; // formation, roster, bag, help inherit their actual underlying cue
  }
  let ctx, master, bgmBus, fxBus, unlocked=false, muted=false, desired='', current=null;
  let generation=0, controller=null, fxController=null, fxGeneration=0, fx=null, queued=false;
  const bgmCache=new Map(), fxCache=new Map(), live=new Set();
  const sfx=window.createRDFZSfx?.({context:()=>ctx,output:()=>master,enabled:()=>unlocked&&!muted});
  const stats={starts:0,requests:0,aborted:0,failures:[],decoded:[],stingers:[],maxLiveBgm:0};
  try {muted=localStorage.getItem('rdfz-music-muted')==='1';} catch {}
  function ramp(param,value,seconds=.35) {
    const now=ctx.currentTime;
    if (param.cancelAndHoldAtTime) param.cancelAndHoldAtTime(now);
    else {const prior=param.value;param.cancelScheduledValues(now);param.setValueAtTime(prior,now);}
    param.linearRampToValueAtTime(value,now+seconds);
  }
  function buttons() {
    for (const id of ['soundBtn','hubSound','musicToggle']) {
      const b=document.getElementById(id);if (!b) continue;
      const text=id==='musicToggle'?(muted?'♫ 关':'♫ 开'):(muted?'×':'♪');if (b.textContent!==text) b.textContent=text;
      b.setAttribute('aria-label',muted?'开启声音（音乐与音效）':'关闭声音（音乐与音效）');b.setAttribute('aria-pressed',String(!muted));
      b.title=muted?'开启声音（音乐与音效）':'关闭声音（音乐与音效）';
    }
  }
  function createContext() {
    if (ctx) return;
    const Audio=window.AudioContext||window.webkitAudioContext;
    if (!Audio) throw new Error('Web Audio is unavailable');
    ctx=new Audio({sampleRate:44100});master=ctx.createGain();bgmBus=ctx.createGain();fxBus=ctx.createGain();
    master.gain.value=muted?0:.72;bgmBus.gain.value=1;fxBus.gain.value=.85;
    bgmBus.connect(master);fxBus.connect(master);master.connect(ctx.destination);
  }
  async function unlock(event) {
    if (event && !event.isTrusted) return;
    if(unlocked && ctx?.state==='running')return;
    try {createContext();await ctx.resume();unlocked=ctx.state==='running';sfx?.warm();if(unlocked && !(event?.target?.closest?.('#startBtn,#continueBtn') && resolveScene()==='title')) sync(true);}
    catch (e) {stats.failures.push('unlock: '+e.message);}
  }
  async function load(id,signal,cache) {
    if(cache.has(id)) {const b=cache.get(id);cache.delete(id);cache.set(id,b);return b;}
    const cue=manifest.cues[id];if(!cue) throw new Error('Unknown music cue: '+id);
    let last;
    for (const url of [cue.ogg,cue.mp3]) {
      if (signal.aborted) throw new DOMException('Aborted','AbortError');
      try {
        stats.requests++;const response=await fetch(url,{signal});if(!response.ok)throw new Error(`${response.status} ${url}`);
        const data=await response.arrayBuffer();if(signal.aborted)throw new DOMException('Aborted','AbortError');
        const buffer=await ctx.decodeAudioData(data);if(signal.aborted)throw new DOMException('Aborted','AbortError');
        const expected=Math.round(cue.frames*ctx.sampleRate/cue.sampleRate);
        if(Math.abs(buffer.length-expected)>1)throw new Error(`Decoded duration mismatch ${id}: ${buffer.length}/${expected}`);
        stats.decoded.push({id,frames:buffer.length,sampleRate:buffer.sampleRate,url});if(stats.decoded.length>80)stats.decoded.shift();
        cache.set(id,buffer);while(cache.size>2)cache.delete(cache.keys().next().value);
        return buffer;
      } catch(e) {if(e.name==='AbortError')throw e;last=e;}
    }
    throw last;
  }
  function dispose(node) {try{node.source.stop();}catch{}node.source.disconnect();node.gain.disconnect();live.delete(node);}
  function cancelFx() {
    fxGeneration++;fxController?.abort();fxController=null;
    if(fx){try{fx.stop();}catch{}fx.disconnect();fx=null;}
    if(ctx)ramp(bgmBus.gain,1,.2);
  }
  async function play(id) {
    const token=++generation;controller?.abort();controller=new AbortController();const signal=controller.signal;
    if(current?.id===id)return;
    try {
      const buffer=await load(id,signal,bgmCache);
      if(token!==generation || muted || desired!==id)return;
      const source=ctx.createBufferSource(),gain=ctx.createGain();source.buffer=buffer;source.loop=true;
      source.loopStart=0;source.loopEnd=manifest.cues[id].frames/manifest.cues[id].sampleRate;
      source.connect(gain);gain.connect(bgmBus);gain.gain.value=0;
      // At most the new cue and one fading predecessor, even during rapid navigation.
      for(const node of [...live])if(node!==current)dispose(node);
      const old=current;current={id,source,gain,started:ctx.currentTime};live.add(current);
      source.start();ramp(gain.gain,1,.7);stats.starts++;stats.maxLiveBgm=Math.max(stats.maxLiveBgm,live.size);
      if(old){ramp(old.gain.gain,0,.7);setTimeout(()=>dispose(old),800);}
      controller=null;
    } catch(e) {
      if(e.name==='AbortError')stats.aborted++;
      else {stats.failures.push(id+': '+e.message);console.warn('Music remains optional:',id,e.message);}
    }
  }
  function sync(retry=false) {
    toggleButton.hidden=visible('homeScreen') || visible('app');
    const id=resolveScene(),changed=id!==desired;
    if(changed){if(!['battle','boss','final'].includes(id))sfx?.stop();desired=id;generation++;controller?.abort();cancelFx();}
    if(unlocked && !muted && (changed||retry) && current?.id!==id)void play(id);
  }
  async function stinger(id) {
    if(!unlocked||muted)return;
    cancelFx();const token=fxGeneration,scene=desired;fxController=new AbortController();
    try {
      const buffer=await load(id,fxController.signal,fxCache);
      if(token!==fxGeneration||scene!==desired||muted)return;
      const source=ctx.createBufferSource();source.buffer=buffer;source.connect(fxBus);fx=source;
      ramp(bgmBus.gain,.3,.1);source.start();stats.stingers.push(id);
      source.onended=()=>{source.disconnect();if(fx===source){fx=null;ramp(bgmBus.gain,1,.7);}};
    } catch(e){if(e.name!=='AbortError')stats.failures.push('stinger '+id+': '+e.message);}
  }
  function toggle() {
    muted=!muted;try{localStorage.setItem('rdfz-music-muted',muted?'1':'0');}catch{}
    if(ctx)ramp(master.gain,muted?0:.72,.18);
    if(muted){sfx?.stop();generation++;controller?.abort();controller=null;cancelFx();}else {void unlock().then(()=>sfx?.warm());sync(true);}
    buttons();
  }
  const toggleButton=document.createElement('button');toggleButton.id='musicToggle';toggleButton.type='button';
  document.body.append(toggleButton);
  for(const id of ['soundBtn','hubSound','musicToggle']) {const b=document.getElementById(id);if(b)b.onclick=toggle;}
  buttons();sync();
  addEventListener('pointerdown',unlock,{passive:true});addEventListener('keydown',unlock);
  document.addEventListener('visibilitychange',()=>{if(!ctx)return;if(document.hidden)void ctx.suspend();else if(unlocked)void ctx.resume().catch(()=>{});});
  new MutationObserver(()=>{if(!queued){queued=true;requestAnimationFrame(()=>{queued=false;sync();});}})
    .observe(document.body,{attributes:true,attributeFilter:['class'],childList:true,subtree:true});
  const completedChapters=new Set(campaignChapters.filter(c=>chapterComplete(c)).map(c=>c.index));
  RDFZ.on('stageComplete',({detail})=>{
    const chapter=campaignChapters[detail.chapter-1];
    const newlyComplete=detail.win&&detail.firstClear!==false&&!RDFZ.getStage(detail.stageId)?.optional&&chapter&&chapterComplete(chapter)&&!completedChapters.has(chapter.index);
    if(newlyComplete)completedChapters.add(chapter.index);
    void stinger(detail.win?(newlyComplete?'chapter-clear':'victory'):'defeat');
  });
  RDFZ.on('summon',({detail})=>void stinger(detail.pulls.some(id=>RDFZ.getHero(id)?.rank==='S')?'rare':'recruit'));
  // Explicit lifecycle wrappers preserve all original game/save behavior.
  const narrativeBase=openStageNarrative;
  openStageNarrative=function(...args){const result=narrativeBase.apply(this,args);sync();if(args[0]==='pre'&&['adminFinal','juniorPossession','libraryDog'].includes(narrativeScenario))void stinger('revelation');return result;};
  const basketBase=finishBasketballGame;
  finishBasketballGame=function(...args){const result=basketBase.apply(this,args);void stinger('victory');return result;};
  const puzzleBase=completePuzzleStage;
  completePuzzleStage=function(...args){const result=puzzleBase.apply(this,args);void stinger('victory');return result;};
  const parkourBase=finishParkour;
  finishParkour=function(success,...args){const result=parkourBase.call(this,success,...args);void stinger(success?'victory':'defeat');return result;};
  window.RDFZMusic=Object.freeze({
    resolveScene, refresh:()=>sync(true),
    diagnostics:()=>({sfx:sfx?.diagnostics(),desired,current:current?.id||null,started:current?.started||null,muted,unlocked,context:ctx?.state||'locked',live:live.size,bgmCache:[...bgmCache.keys()],fxCache:[...fxCache.keys()],...JSON.parse(JSON.stringify(stats))})
  });
})();
