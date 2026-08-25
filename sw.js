/* prosty cache-first - wystarcza, zeby appka byla "instalowalna" i dzialala offline */
const CACHE = 'krol-kufla-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './assets/logo-mark.png',
  './assets/app-icon.png',
  './assets/crown.jpg',
  './assets/background.jpg',
  './assets/card-back-texture.jpg',
  './assets/icons/deck-klasyk.png',
  './assets/icons/deck-nowa.png',
  './assets/icons/deck-chaos.png',
  './assets/icons/deck-mix.png',
  './assets/icons/deck-trzezwo.png'
];

self.addEventListener('install', e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e=>{
  e.waitUntil(
    caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k))))
  );
  self.clients.claim();
});

self.addEventListener('fetch', e=>{
  if(e.request.method!=='GET') return;
  e.respondWith(
    caches.match(e.request).then(hit=>hit || fetch(e.request).then(res=>{
      const copy=res.clone();
      caches.open(CACHE).then(c=>c.put(e.request, copy));
      return res;
    }).catch(()=>hit))
  );
});
