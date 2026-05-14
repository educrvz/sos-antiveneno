var CACHE_NAME = 'sos-antiveneno-v23';

// Same-origin assets only. Cross-origin (Leaflet, Google Fonts, OSM) is
// handled at runtime — never pre-cached with no-cors, because returning
// opaque responses to <script crossorigin> / <link crossorigin> tags makes
// the browser block them (this broke the previous attempt).
var ASSETS = [
    './',
    './index.html',
    './hospitals.json',
    './manifest.json'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(ASSETS);
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

// OSM tiles are intentionally never intercepted — too many, no value to a
// user already offline (they won't pan a map they can't reload). Letting the
// browser handle them directly also avoids any chance of the SW corrupting
// the image stream.
function isOsmTile(url) {
    return /\.tile\.openstreetmap\.org$/.test(url.hostname);
}

function safeCachePut(request, response) {
    // Cache only:
    //  - successful basic/cors responses (2xx, headers valid), OR
    //  - opaque responses from no-cors fetches (status 0, but cacheable).
    // Anything else (3xx redirects, 4xx/5xx, network errors) would pollute
    // the cache and hide future failures.
    if (response.type === 'opaque' || response.ok) {
        var clone = response.clone();
        caches.open(CACHE_NAME).then(function(cache) {
            cache.put(request, clone);
        }).catch(function() { /* quota / disabled — ignore */ });
    }
}

self.addEventListener('fetch', function(event) {
    var request = event.request;
    if (request.method !== 'GET') return;

    var url = new URL(request.url);
    if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

    // OSM tiles: don't intercept. Browser handles directly.
    if (isOsmTile(url)) return;

    var sameOrigin = url.origin === self.location.origin;

    if (sameOrigin && url.pathname.endsWith('hospitals.json')) {
        // Network-first for data (allows fresh hospital updates to ship).
        event.respondWith(
            fetch(request).then(function(resp) {
                safeCachePut(request, resp);
                return resp;
            }).catch(function() {
                return caches.match(request);
            })
        );
        return;
    }

    if (sameOrigin) {
        // Cache-first for the app shell (index.html, manifest, icons).
        // Populate on miss so any newly added same-origin asset gets cached
        // on first use without requiring a CACHE_NAME bump.
        event.respondWith(
            caches.match(request).then(function(cached) {
                if (cached) return cached;
                return fetch(request).then(function(resp) {
                    safeCachePut(request, resp);
                    return resp;
                });
            })
        );
        return;
    }

    // Cross-origin (Leaflet CSS/JS from unpkg, Google Fonts CSS + woff2):
    // network-first, fall back to cache when offline. We deliberately do
    // NOT pre-cache these — letting the browser do its real CORS request
    // online means the response cached is one the browser is happy to
    // replay later (no opaque-vs-CORS mismatch).
    event.respondWith(
        fetch(request).then(function(resp) {
            safeCachePut(request, resp);
            return resp;
        }).catch(function() {
            return caches.match(request);
        })
    );
});
