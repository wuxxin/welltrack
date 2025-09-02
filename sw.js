// This is a basic service worker for caching the app shell for offline use.

const CACHE_NAME = 'welltrack-cache-v1';
// We only need to cache the main HTML file.
// Other assets are loaded from CDNs and will be handled by the browser's cache.
const urlsToCache = [
  './welltrack.html'
];

// Install event: open cache and add the main app file.
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache and caching app shell');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event: serve from cache first, then fall back to network.
// This makes the app load instantly on subsequent visits and work offline.
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return the cached response
        if (response) {
          return response;
        }
        // Not in cache - fetch from the network
        return fetch(event.request);
      }
    )
  );
});

// Activate event: clean up old, unused caches.
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
