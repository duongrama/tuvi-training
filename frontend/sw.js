// Service Worker for Tử Vi Push Notifications
// Served at /sw.js — proper root scope

const CACHE_NAME = 'tuvi-push-v1';

self.addEventListener('push', function(event) {
    if (!event.data) return;

    try {
        const data = event.data.json();
        const options = {
            body: data.body || 'Bạn có vận hạn mới hôm nay',
            icon: data.icon || '/icon-192.png',
            badge: data.badge || '/icon-72.png',
            vibrate: [100, 50, 100],
            data: { url: data.url || '/', dateOfArrival: Date.now() },
            actions: [
                { action: 'open', title: 'Xem ngay' },
                { action: 'close', title: 'Để sau' }
            ]
        };
        event.waitUntil(
            self.registration.showNotification(data.title || 'Tử Vi · Vận Hạn Hôm Nay', options)
        );
    } catch (e) {
        event.waitUntil(
            self.registration.showNotification('Tử Vi', {
                body: 'Vận hạn hôm nay của bạn đã sẵn sàng',
                icon: '/icon-192.png'
            })
        );
    }
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    if (event.action === 'close') return;
    const urlToOpen = event.notification.data?.url || '/';
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then(function(clientList) {
                for (const client of clientList) {
                    if (client.url === urlToOpen && 'focus' in client) return client.focus();
                }
                if (clients.openWindow) return clients.openWindow(urlToOpen);
            })
    );
});

self.addEventListener('install', function() { self.skipWaiting(); });
self.addEventListener('activate', function(event) { event.waitUntil(clients.claim()); });
