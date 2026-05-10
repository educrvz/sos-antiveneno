var CACHE_NAME = 'sos-antiveneno-v21';

// Same-origin assets — fetched with default CORS, cache.addAll handles them.
var LOCAL_ASSETS = [
    './',
    './index.html',
    './hospitals.json',
    './manifest.json'
];

// Cross-origin assets pre-cached on install. The Google Fonts woff2 files
// are intentionally NOT pre-listed: their URLs are not stable across browsers
// (fonts.googleapis.com returns different @font-face src by UA), so we let
// the runtime cache pick them up on first online use.
var EXTERNAL_ASSETS = [
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
    'https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800;900&display=swap'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(LOCAL_ASSETS).then(function() {
                // Cross-origin: use no-cors so opaque responses can be cached
                // without addAll's status-check rejecting them.
                return Promise.all(EXTERNAL_ASSETS.map(function(url) {
                    return fetch(url, { mode: 'no-cors', credentials: 'omit' })
                        .then(function(resp) { return cache.put(url, resp); })
                        .catch(function() { /* best-effort */ });
                }));
            });
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(keys) {
            return Promise.all(
                keys.filter(function(k) { return k !== CACHE_NAME; })
                    .map(function(k) { return caches.delete(k); })
            );
        })
    );
    self.clients.claim();
});

// OSM tiles are intentionally never cached — too many, no value to a user
// who's already offline (they won't pan a map they can't reload).
function isOsmTile(url) {
    return /\.tile\.openstreetmap\.org$/.test(url.hostname);
}

function isCacheable(request, response, url) {
    if (request.method !== 'GET') return false;
    if (url.protocol !== 'http:' && url.protocol !== 'https:') return false;
    if (isOsmTile(url)) return false;
    // 'opaque' responses (no-cors cross-origin) have status 0; we can still
    // cache and replay them. 'basic'/'cors' require a 2xx status.
    if (response.type === 'opaque') return true;
    return response.ok;
}

self.addEventListener('fetch', function(event) {
    var url = new URL(event.request.url);

    if (url.pathname.endsWith('hospitals.json')) {
        // Network-first for data (allows updates)
        event.respondWith(
            fetch(event.request).then(function(resp) {
                var clone = resp.clone();
                caches.open(CACHE_NAME).then(function(cache) {
                    cache.put(event.request, clone);
                });
                return resp;
            }).catch(function() {
                return caches.match(event.request);
            })
        );
        return;
    }

    // Cache-first, populate on success — accumulates Leaflet/font/etc. in
    // the cache during normal online use so offline reloads keep working.
    event.respondWith(
        caches.match(event.request).then(function(cached) {
            if (cached) return cached;
            return fetch(event.request).then(function(resp) {
                if (isCacheable(event.request, resp, url)) {
                    var clone = resp.clone();
                    caches.open(CACHE_NAME).then(function(cache) {
                        cache.put(event.request, clone);
                    });
                }
                return resp;
            });
        })
    );
});
