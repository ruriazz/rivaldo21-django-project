if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => initializeFirebaseMessaging({
        onTokenReceived: async (token, _) => {
            if (localStorage.getItem(CONFIG.tokenStorageKey) !== token) {
                await fetch('/api/notifications/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ token }),
                });
                localStorage.setItem(CONFIG.tokenStorageKey, token);
            }
        },
        onMessageReceived: async (payload, messaging) => {
            console.log('foreground message received:', payload);
        }
    }));
}