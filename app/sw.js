var CACHE_NAME = 'sos-antiveneno-v23';

// Same-origin assets only. Cross-origin (Leaflet, Google Fonts, OSM) is
// handled at runtime so the browser stores responses with the right CORS mode.
var ASSETS = [
    './',
    './index.html',
    './hospitals.json',
    './manifest.json',
    './privacy.html',
    './terms.html',
    './icons/icon-192.svg',
    './icons/icon-512.svg',
    './og-image.png'
];

function isOsmTile(url) {
    return /\.tile\.openstreetmap\.org$/.test(url.hostname);
}

function safeCachePut(request, response) {
    // Cache only successful responses, plus opaque responses from no-cors
    // fetches. Redirects, errors and failed requests should not mask deploys.
    if (response.type === 'opaque' || response.ok) {
        var clone = response.clone();
        caches.open(CACHE_NAME).then(function(cache) {
            cache.put(request, clone);
        }).catch(function() {});
    }
}

function fallbackFor(request) {
    var url = new URL(request.url);
    if (url.pathname.endsWith('/privacy') || url.pathname.endsWith('/privacy.html')) {
        return caches.match('./privacy.html');
    }
    if (url.pathname.endsWith('/terms') || url.pathname.endsWith('/terms.html')) {
        return caches.match('./terms.html');
    }
    if (request.mode === 'navigate' || url.pathname.endsWith('/index.html')) {
        return caches.match('./index.html');
    }
    return caches.match(request);
}

function networkFirst(request) {
    return fetch(request).then(function(resp) {
        safeCachePut(request, resp);
        return resp;
    }).catch(function() {
        return fallbackFor(request);
    });
}

function cacheFirst(request) {
    return caches.match(request).then(function(cached) {
        if (cached) return cached;
        return fetch(request).then(function(resp) {
            safeCachePut(request, resp);
            return resp;
        });
    });
}

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

self.addEventListener('fetch', function(event) {
    var request = event.request;
    if (request.method !== 'GET') return;

    var url = new URL(request.url);
    if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

    // OSM tiles are intentionally never intercepted: too many, little value
    // offline, and direct browser handling avoids corrupting image streams.
    if (isOsmTile(url)) return;

    var sameOrigin = url.origin === self.location.origin;

    if (sameOrigin && (
            url.pathname.endsWith('hospitals.json') ||
            request.mode === 'navigate' ||
            url.pathname.endsWith('/index.html') ||
            url.pathname.endsWith('/privacy') ||
            url.pathname.endsWith('/privacy.html') ||
            url.pathname.endsWith('/terms') ||
            url.pathname.endsWith('/terms.html'))) {
        // Network-first for data and HTML avoids stale app shells after deploys.
        event.respondWith(networkFirst(request));
        return;
    }

    if (sameOrigin) {
        // Cache-first for local static assets, populated on first use.
        event.respondWith(cacheFirst(request));
        return;
    }

    // Cross-origin assets (Leaflet CSS/JS, Google Fonts CSS + woff2):
    // network-first, then cached copy when offline.
    event.respondWith(networkFirst(request));
});
