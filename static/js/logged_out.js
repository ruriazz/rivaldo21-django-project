window.addEventListener("load", async () => {
    initializeFirebaseMessaging({
        onTokenReceived: async (token, messaging) => {
            try {
                await messaging.deleteToken();
                await fetch("/api/notifications/token/delete", {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ token }),
                });
                localStorage.removeItem(CONFIG.tokenStorageKey);
            } catch (err) {
                console.warn("Error deleting token:", err);
            }
        },
    })
});