async function initializeFirebaseMessaging({ onTokenReceived, onMessageReceived }) {
    try {
        const permission = await Notification.requestPermission();
        if (permission !== "granted") {
            throw new Error("Notification permission denied");
        }

        firebase.initializeApp(firebaseConfig);
        const messaging = firebase.messaging();

        const registration = await navigator.serviceWorker.register(
            "/static/firebase-messaging-sw.js",
            { scope: '/static/' }
        );

        if (registration.installing) {
            console.log('Service worker installing');
            const serviceWorker = registration.installing || registration.waiting;
            await new Promise((resolve) => {
                serviceWorker.addEventListener('statechange', function (e) {
                    console.log('Service worker state:', e.target.state);
                    if (e.target.state === 'activated') {
                        resolve();
                    }
                });
            });
        }

        console.log('Service worker activated successfully');

        const currentToken = await messaging.getToken({
            vapidKey: vapidKey,
            serviceWorkerRegistration: registration,
        });

        if (onTokenReceived && typeof onTokenReceived === 'function') {
            onTokenReceived(currentToken, messaging);
        }

        if (currentToken) {
            listenMessage(messaging);
            if (onMessageReceived && typeof onMessageReceived === 'function') {
                messaging.onMessage(payload => onMessageReceived(payload, messaging));
            }
        } else {
            console.log(
                "No registration token available. Request permission to generate one."
            );
        }
    } catch (err) {
        console.error("An error occurred while initializing: ", err);
    }
}

const listenMessage = (messaging) => {
    messaging.onMessage(function (payload) {
        console.log(
            "[DEBUG] Attempting to handle foreground message"
        );
        console.log("[DEBUG] Payload received:", payload);

        if (payload.notification) {
            const notificationData = {
                title: payload.notification.title || "New Message",
                body: payload.notification.body,
                icon: payload.notification.icon,
                image: payload.notification.image,
            };
            console.log(
                "[DEBUG] Creating notification with:",
                notificationData
            );
            new Notification(
                notificationData.title,
                notificationData
            );
        }
    });
}