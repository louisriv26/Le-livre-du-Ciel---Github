const VERSION = 'ldc-v1.3.1';
const SHELL = [
  './', './index.html', './corpus/manifest.json',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(VERSION).then(c => c.addAll(SHELL))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // Corpus files: cache-first, then network
  if (url.pathname.includes('/corpus/')) {
    e.respondWith(
      caches.match(e.request).then(cached => {
        if (cached) return cached;
        return fetch(e.request).then(res => {
          const clone = res.clone();
          caches.open(VERSION).then(c => c.put(e.request, clone));
          return res;
        });
      })
    );
    return;
  }
  // Shell: network-first with cache fallback
  e.respondWith(
    fetch(e.request).then(res => {
      const clone = res.clone();
      caches.open(VERSION).then(c => c.put(e.request, clone));
      return res;
    }).catch(() => caches.match(e.request))
  );
});
