// Pusty service worker dla /komfortoweogrody/.
// Nie obsługuje "fetch", więc wszystkie żądania idą prosto do sieci,
// a cache-first worker strony głównej (Król Kufla) nie przechwytuje tej podstrony.
self.addEventListener('install', function(){ self.skipWaiting(); });
self.addEventListener('activate', function(e){ e.waitUntil(self.clients.claim()); });
