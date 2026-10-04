/* Online, demand-driven artwork loading. No service worker or offline cache. */
(function (global) {
  'use strict';
  const manifest = global.RDFZ_ASSET_MANIFEST || {};
  const loaded = new Map();
  const pending = [];
  const versions = new WeakMap();
  let active = 0;

  function url(source, variant = 'full') {
    return manifest[source]?.[variant] || manifest[source]?.full || source;
  }
  const art = (source, variant) => `url('${url(source, variant)}')`;

  // Keep image decoding and downloads bounded when opening a long collection.
  function pump() {
    while (active < 4 && pending.length) {
      const task = pending.shift();
      active++;
      const image = new Image();
      image.decoding = 'async';
      image.fetchPriority = task.priority;
      let done = false;
      const finish = (ok) => {
        if (done) return;
        done = true;
        clearTimeout(timer);
        image.onload = image.onerror = null;
        if (!ok) {
          image.src = '';
          loaded.delete(task.src); // A later visit/retry must be able to recover.
        }
        active--;
        task.resolve(ok);
        pump();
      };
      const timer = setTimeout(() => finish(false), 12000);
      image.onload = () => image.decode().catch(() => {}).then(() => finish(true));
      image.onerror = () => finish(false);
      image.src = task.src;
    }
  }

  function load(source, variant = 'full', priority = 'auto') {
    const src = url(source, variant);
    if (!loaded.has(src)) {
      const promise = new Promise(resolve => {
        const task = {src, priority, resolve};
        if (priority === 'low') pending.push(task);
        else {
          const firstLow = pending.findIndex(item => item.priority === 'low');
          pending.splice(firstLow < 0 ? pending.length : firstLow, 0, task);
        }
      });
      loaded.set(src, promise);
      pump();
    }
    return loaded.get(src);
  }

  async function background(element, source, {variant = 'full', property = 'background-image'} = {}) {
    const version = {};
    versions.set(element, version);
    element.querySelector(':scope > .art-retry')?.remove();
    element.classList.remove('art-error');
    element.style.removeProperty(property);
    if (!source) {
      element.classList.remove('art-loading');
      return false;
    }
    element.classList.add('art-loading');
    const ok = await load(source, variant);
    if (versions.get(element) !== version || !element.isConnected) return false;
    element.classList.remove('art-loading');
    if (ok) element.style.setProperty(property, art(source, variant));
    else {
      element.classList.add('art-error');
      // Collection cards still open details; only standalone art gets a retry button.
      if (!element.matches('button')) {
        const retry = document.createElement('button');
        retry.className = 'art-retry';
        retry.textContent = '图片加载失败，点击重试';
        retry.onclick = event => {
          event.stopPropagation();
          background(element, source, {variant, property});
        };
        element.append(retry);
      }
    }
    return ok;
  }

  // Each collection owns its observer, so rerendering never retains old cards.
  const observers = new WeakMap();
  function observe(root) {
    observers.get(root)?.disconnect();
    const cards = root.querySelectorAll('[data-art-src]');
    const reveal = element => background(element, element.dataset.artSrc, {variant: 'thumb', property: '--art'});
    if (!('IntersectionObserver' in global)) {
      cards.forEach(reveal);
      return;
    }
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        observer.unobserve(entry.target);
        reveal(entry.target);
      }
    }, {rootMargin: '120px 0px'});
    observers.set(root, observer);
    cards.forEach(element => observer.observe(element));
  }

  function prefetch(source) {
    const connection = navigator.connection;
    if (!source || connection?.saveData || /(^|-)2g$/.test(connection?.effectiveType || '')) return;
    // At most the next relevant image; never fetch a chapter or the whole library.
    return load(source, 'full', 'low');
  }

  global.RDFZAssets = {url, art, load, background, observe, prefetch};
})(window);
