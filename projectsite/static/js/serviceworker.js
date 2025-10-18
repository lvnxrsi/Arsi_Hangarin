const CACHE_NAME = 'projectsite-cache-v3';

const urlsToCache = [
    '/',  
    '/task-list/',
    '/note-list/',
    '/subtask-list/',
    '/category-list/',
    '/priority-list/',
    
    '/static/css/bootstrap.min.css',
    '/static/css/ready.css',
    '/static/css/demo.css',
    '/static/css/custom.css',
    
    '/static/js/main.js',
    '/static/js/ready.min.js',
    '/static/js/core/jquery.3.2.1.min.js',
    '/static/js/core/popper.min.js',
    '/static/js/core/bootstrap.min.js',
    
    '/static/img/icon-192.png',
    '/static/img/icon-512.png',
    '/static/img/mainprofile.jpg',
    
    '/static/fonts/Roboto-Regular.woff2',
    '/static/fonts/Roboto-Bold.woff2',
    '/static/fonts/Roboto-Italic.woff2'
];


self.addEventListener('install', (event) => {
    console.log('[Service Worker] Install');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[Service Worker] Caching all files');
                return cache.addAll(urlsToCache);
            })
            .then(() => self.skipWaiting())
    );
});


self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Activate');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[Service Worker] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});


self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;
            }

            return fetch(event.request)
                .then((networkResponse) => {
                    
                    if (event.request.url.startsWith(self.location.origin)) {
                        return caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, networkResponse.clone());
                            return networkResponse;
                        });
                    } else {
                        return networkResponse;
                    }
                })
                .catch(() => {
                    
                    if (event.request.mode === 'navigate') {
                        return caches.match('/');
                    }
                });
        })
    );
});
