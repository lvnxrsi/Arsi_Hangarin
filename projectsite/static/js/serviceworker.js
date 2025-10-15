
const CACHE_NAME = 'projectsite-cache-v1';


const urlsToCache = [
    '/',  // Home page
    '/static/css/bootstrap.min.css',
    '/static/css/ready.css',
    '/static/css/demo.css',
    '/static/js/main.js',
    '/static/js/ready.min.js',
    '/static/img/icon-192.png',
    '/static/img/icon-512.png',
    '/static/img/profile.jpg'
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
        caches.match(event.request)
            .then((response) => {
                
                return response || fetch(event.request).catch(() => {
                    
                    if (event.request.mode === 'navigate') {
                        return caches.match('/');
                    }
                });
            })
    );
});
