/* Small static effects share the BGM AudioContext, master gain and mute control. */
window.createRDFZSfx = ({context, output, enabled}) => {
  const cues = window.RDFZSfxManifest?.cues || {};
  const cache = new Map(), pending = new Map(), live = new Set(), last = new Map();
  const stats = {played: [], failures: [], skipped: 0, maxVoices: 0};
  let epoch = 0;
  function canPlay() { return enabled() && !document.hidden && context()?.state === 'running'; }
  async function load(id) {
    if (cache.has(id)) return cache.get(id);
    if (pending.has(id)) return pending.get(id);
    const task = (async () => {
      const cue = cues[id]; let error;
      for (const url of [cue.ogg, cue.mp3]) {
        try {
          const response = await fetch(url, {signal: AbortSignal.timeout(5000)});
          if (!response.ok) throw new Error(`HTTP ${response.status}`);
          const buffer = await context().decodeAudioData(await response.arrayBuffer());
          if (Math.abs(buffer.duration - cue.duration) > .03) throw new Error('Invalid effect duration');
          cache.set(id, buffer); return buffer;
        } catch (e) { error = e; }
      }
      throw error;
    })();
    pending.set(id, task);
    try { return await task; } finally { pending.delete(id); }
  }
  function dispose(node) {
    try { node.source.stop(); } catch {}
    node.source.disconnect(); node.gain.disconnect(); live.delete(node);
  }
  function stop() { epoch++; for (const node of [...live]) dispose(node); }
  async function play(id) {
    const cue = cues[id];
    if (!cue || !canPlay()) return;
    const now = performance.now(), interval = cue.group === 'impact' ? 105 : 180;
    if (now - (last.get(cue.group) ?? -Infinity) < interval) { stats.skipped++; return; }
    last.set(cue.group, now);
    const token = epoch;
    try {
      const buffer = await load(id);
      // A cold/failed request must never replay an old hit after navigation or mute.
      if (!canPlay() || token !== epoch || performance.now() - now > 220) { stats.skipped++; return; }
      if (live.size >= 4) dispose(live.values().next().value);
      const ctx = context(), source = ctx.createBufferSource(), gain = ctx.createGain();
      source.buffer = buffer; gain.gain.value = .7;
      source.connect(gain); gain.connect(output());
      const node = {source, gain}; live.add(node);
      source.onended = () => { source.disconnect(); gain.disconnect(); live.delete(node); };
      source.start(); stats.played.push(id);
      if (stats.played.length > 80) stats.played.shift();
      stats.maxVoices = Math.max(stats.maxVoices, live.size);
    } catch (e) {
      stats.failures.push(`${id}: ${e.message}`);
      if (stats.failures.length > 20) stats.failures.shift();
    }
  }
  function warm() {
    if (!canPlay()) return;
    // Eight sub-second assets; no download until the first permitted gesture.
    for (const id of Object.keys(cues)) load(id).catch(() => {});
  }
  RDFZ.on('combatImpact', ({detail}) => {
    if (!state.started || state.paused || !detail.amount) return;
    void play(detail.absorbed > 0 ? 'block' : detail.kind === 'element' ? 'element' : 'impact');
  });
  RDFZ.on('combatFeedback', ({detail}) => {
    if (!state.started || state.paused) return;
    const {text, type} = detail;
    if (type === 'shield' && /闪避|免疫|无敌|无效|锁血|无法消灭|屏障破解/.test(text)) void play('evade');
    else if ((type === 'shield' || type === 'heal') && /护盾|◈/.test(text) && /\+\s*[1-9]|护盾[1-9]|◈[1-9]/.test(text)) void play('shield');
  });
  RDFZ.on('combatSkill', () => { if (state.started && !state.paused) void play('skill'); });
  RDFZ.on('battleEntered', () => { stop(); void play('confirm'); });
  RDFZ.on('battlePause', () => { stop(); void play('pause'); });
  RDFZ.on('stageComplete', stop);
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
  return {play, warm, stop, diagnostics: () => ({...stats, played: [...stats.played], failures: [...stats.failures], cached: [...cache.keys()], live: live.size})};
};
