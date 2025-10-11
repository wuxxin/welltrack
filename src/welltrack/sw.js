/**
 * @file This service worker handles caching for the WellTrack application,
 * enabling offline functionality and ensuring users have the latest version.
 */

const CACHE_NAME = 'welltrack-cache-v2';
const urlsToCache = [
  './welltrack.html'
];

/**
 * Handles the 'install' event of the service worker.
 * This is where the core application shell is cached for offline use.
 * @param {ExtendableEvent} event The install event.
 */
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache and caching app shell');
        return cache.addAll(urlsToCache);
      })
  );
});

/**
 * Handles the 'fetch' event.
 * It implements a network-first strategy for the main application page to ensure
 * users get updates, and a cache-first strategy for other assets.
 * @param {FetchEvent} event The fetch event.
 */
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
    // For non-navigation requests (like CDN scripts), let the browser handle it.
    // This relies on the browser's standard HTTP caching.
    // No specific caching strategy is implemented here for third-party resources.
  }
});

/**
 * Handles the 'activate' event.
 * This is where old, unused caches are cleaned up to free up storage space.
 * @param {ExtendableEvent} event The activate event.
 */
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
