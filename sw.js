// This is a basic service worker for caching the app shell for offline use.

const CACHE_NAME = 'welltrack-cache-v2';
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

// Fetch event: Network-first strategy for navigation, cache-first for others.
// This ensures the user gets the latest version of the app when online,
// but still allows the app to work offline by serving from the cache.
self.addEventListener('fetch', event => {
  // For navigation requests (the HTML file), use a network-first strategy.
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // If the fetch is successful, clone the response, cache it, and return it.
          const responseToCache = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache);
            });
          return response;
        })
        .catch(() => {
          // If the network request fails, try to serve the response from the cache.
          return caches.match(event.request);
        })
    );
  } else {
    // For non-navigation requests (like CDN scripts), use a cache-first strategy.
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          return response || fetch(event.request);
        })
    );
  }
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
