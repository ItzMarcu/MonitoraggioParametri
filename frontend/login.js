const API_URL = "https://monitoraggioparametri.onrender.com";

        document.getElementById("loginForm").addEventListener("submit", async (e) => {
            e.preventDefault();

            const username = document.getElementById("usernameInput").value;
            const password = document.getElementById("passwordInput").value;

            // FastAPI si aspetta i dati del login come form urlencoded, non come JSON puro
            const formData = new URLSearchParams();
            formData.append("username", username);
            formData.append("password", password);

            try {
                const response = await fetch(`${API_URL}/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    
                    // Salviamo il codice di sblocco (Token JWT) nel browser
                    localStorage.setItem("token", data.access_token);
                    
                    // Reindirizziamo alla dashboard principale
                    window.location.href = "dashboard.html";
                } else {
                    alert("Credenziali errate. Accesso negato.");
                }
            } catch (error) {
                console.error("Errore di connessione:", error);
                alert("Impossibile connettersi al server di autenticazione.");
            }
        });