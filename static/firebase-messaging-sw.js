importScripts('https://www.gstatic.com/firebasejs/11.2.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/11.2.0/firebase-messaging-compat.js');
importScripts('/static/config.js');

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

self.addEventListener('install', function (event) {
    console.log('Service Worker installed');
});

self.addEventListener('activate', function (event) {
    console.log('Service Worker activated');
    event.waitUntil(self.clients.claim());
});

self.addEventListener("push", function (event) {
    let data;
    const payload = event.data?.json() || {};

    console.log('payload:', payload);

    const title = payload.notification?.title || "New Message";
    const options = {
        body: data?.body || payload.notification?.body || "",
        icon: data?.icon || payload.notification?.icon,
        image: data?.image || payload.notification?.image,
        data: {
            ...payload.data,
            click_action: payload.data?.click_action || '/'
        }
    };

    event.waitUntil(self.registration.showNotification(title, options));
});

// Handle notification click
self.addEventListener("notificationclick", async function (event) {
    event.notification.close();

    console.log('[SW] Notification clicked');

    try {
        let urlToOpen = event.notification.data?.click_action || '/';

        // Ensure URL is absolute
        if (!urlToOpen.startsWith('http') && !urlToOpen.startsWith('https')) {
            urlToOpen = self.location.origin + (urlToOpen.startsWith('/') ? '' : '/') + urlToOpen;
        }

        console.log('[SW] Opening URL:', urlToOpen);

        // Always open new window
        event.waitUntil(
            clients.openWindow(urlToOpen)
                .then(() => console.log('[SW] Window opened successfully'))
                .catch(error => {
                    console.error('[SW] Error opening window:', error);
                    return clients.openWindow('/');
                })
        );
    } catch (error) {
        console.error('[SW] Critical error:', error);
        event.waitUntil(clients.openWindow('/'));
    }
});
