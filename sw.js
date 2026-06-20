const VERSION = 'ldc-v2.5.24';
const SHELL = [
  './', './index.html', './manifest.json', './sw.js',

  // Icons
  './icons/icon-192.png', './icons/icon-512.png',
  './icons/apple-touch-icon.png', './icons/favicon-32.png',

  // Local fonts (no CDN dependency)
  './assets/fonts/fonts.css',
  './assets/fonts/im-fell-english-latin-400-normal.woff2',
  './assets/fonts/im-fell-english-latin-400-italic.woff2',
  './assets/fonts/crimson-text-latin-400-normal.woff2',
  './assets/fonts/crimson-text-latin-400-italic.woff2',
  './assets/fonts/crimson-text-latin-600-normal.woff2',

  // Tabler Icons (local)
  './assets/icons/tabler-icons.min.css',
  './assets/icons/tabler-icons.woff2',

  // SortableJS (local)
  './assets/js/sortable.min.js',

  // Corpus manifest
  './corpus/manifest.json',

  // T1–T8 pre-cached for immediate offline reading
  // (remaining tomes load on demand and are cached on first access)
  './corpus/volume_01.json', './corpus/paragraphs_01.json', './corpus/search_01.json', './corpus/speakers_01.json',
  './corpus/volume_02.json', './corpus/paragraphs_02.json', './corpus/search_02.json', './corpus/speakers_02.json',
  './corpus/volume_03.json', './corpus/paragraphs_03.json', './corpus/search_03.json', './corpus/speakers_03.json',
  './corpus/volume_04.json', './corpus/paragraphs_04.json', './corpus/search_04.json', './corpus/speakers_04.json',
  './corpus/volume_05.json', './corpus/paragraphs_05.json', './corpus/search_05.json', './corpus/speakers_05.json',
  './corpus/volume_06.json', './corpus/paragraphs_06.json', './corpus/search_06.json', './corpus/speakers_06.json',
  './corpus/volume_07.json', './corpus/paragraphs_07.json', './corpus/search_07.json', './corpus/speakers_07.json',
  './corpus/volume_08.json', './corpus/paragraphs_08.json', './corpus/search_08.json', './corpus/speakers_08.json',
];

self.addEventListener('message', e => {
  if (e.data && e.data.type === 'SKIP_WAITING') self.skipWaiting();
});

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
          if (res && res.ok) {
            const clone = res.clone();
            caches.open(VERSION).then(c => c.put(e.request, clone));
          }
          return res;
        });
      })
    );
    return;
  }
  // Shell: network-first with cache fallback
  e.respondWith(
    fetch(e.request).then(res => {
      if (res && res.ok) {
        const clone = res.clone();
        caches.open(VERSION).then(c => c.put(e.request, clone));
      }
      return res;
    }).catch(() => caches.match(e.request))
  );
});
