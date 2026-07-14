const API_URL = "https://monitoraggioparametri.onrender.com";

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    if (token && token !== "undefined" && token !== "null") {
        window.location.href = "dashboard.html";
    }
});

document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("usernameInput").value;
    const password = document.getElementById("passwordInput").value;

    try {
        // 1. Invio della richiesta di registrazione (JSON)
        const registerResponse = await fetch(`${API_URL}/registrati`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: username, password: password })
        });

        if (!registerResponse.ok) {
            const errData = await registerResponse.json();
            alert(`Errore registrazione: ${errData.detail || "Impossibile completare"}`);
            return;
        }

        // 2. Registrazione riuscita! Eseguiamo il login silenzioso automatico (Form URL Encoded)
        const loginData = new URLSearchParams();
        loginData.append("username", username);
        loginData.append("password", password);

        const loginResponse = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: loginData
        });

        if (loginResponse.ok) {
            const tokenData = await loginResponse.json();
            localStorage.setItem("token", tokenData.access_token);
            window.location.href = "dashboard.html"; // Spedito in dashboard!
        } else {
            alert("Account creato, ma si è verificato un errore durante l'accesso automatico. Prova a fare il login manualmente.");
            window.location.href = "index.html";
        }

    } catch (error) {
        console.error("Errore durante la registrazione:", error);
        alert("Impossibile connettersi al server per completare l'operazione.");
    }
});