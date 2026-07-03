
const API_URL = "https://monitoraggioparametri.onrender.com";

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    if (!token || token === "undefined" || token === "null") {
        localStorage.removeItem("token"); // Pulisci eventuali sporcizie
        window.location.href = "index.html";
        return;
    }

    const oraLocale = new Date();
    oraLocale.setMinutes(oraLocale.getMinutes() - oraLocale.getTimezoneOffset());
    document.getElementById("dataInput").value = oraLocale.toISOString().slice(0, 16);
    caricaDati();
});


document.getElementById("dataForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = document.getElementById("dataInput").value;
    const bpm = document.getElementById("bpmInput").value;
    const pressione = document.getElementById("pressioneInput").value;
    const saturazione = document.getElementById("saturazioneInput").value;

    const params = new URLSearchParams();
    if (data) params.append("data", data);
    if (bpm) params.append("frequenza_cardiaca", bpm);
    if (pressione) params.append("pressione", pressione);
    if (saturazione) params.append("saturazione", saturazione);

    try {
        const response = await fetch(`${API_URL}/registra-dati?${params.toString()}`, {
            method: "POST"
        });

        if (response.ok) {
            alert("Dati salvati con successo!");
            document.getElementById("bpmInput").value = "";
            document.getElementById("pressioneInput").value = "";
            document.getElementById("saturazioneInput").value = "";
            caricaDati();
        } else {
            const err = await response.json();
            alert(`Errore: ${err.detail}`);
        }
    } catch (error) {
        console.error("Errore di connessione:", error);
        alert("Impossibile connettersi al server backend.");
    }
});

async function caricaDati() {
    const container = document.getElementById("cardsContainer");
    container.innerHTML = "<p class='text-gray-400 col-span-2 text-center py-4'>Caricamento in corso...</p>";

    try {
        const response = await fetch(`${API_URL}/ottieni-dati`);
        if (response.status === 401) {
            localStorage.removeItem("token");
            window.location.href = "index.html";
            return;
        }
        
        if (!response.ok) throw new Error("Errore nel recupero dei dati");
        let listaDati = await response.json();
        listaDati.sort((a, b) => new Date(b.data) - new Date(a.data));
        container.innerHTML = "";

        if (listaDati.length === 0) {
            container.innerHTML = "<p class='text-gray-500 col-span-2 text-center py-4'>Nessun dato registrato.</p>";
            return;
        }

        listaDati.forEach(item => {
            const opzioni = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
            const dataFormattata = new Date(item.data).toLocaleDateString('it-IT', opzioni);

            const card = document.createElement("div");
            card.className = "bg-gray-800 border border-gray-700/60 rounded-xl p-5 shadow-md flex flex-col justify-between hover:border-gray-600 transition";

            card.innerHTML = `
                        <div>
                            <div class="text-xs text-indigo-400 font-semibold uppercase tracking-wider mb-2">${dataFormattata}</div>
                            <div class="space-y-2 mt-3">
                                <div class="flex justify-between items-center bg-gray-900/40 px-3 py-1.5 rounded-lg text-sm">
                                    <span class="text-gray-400">Frequenza:</span>
                                    <span class="font-bold text-red-400">${item.frequenza_cardiaca ? item.frequenza_cardiaca + ' BPM' : '--'}</span>
                                </div>
                                <div class="flex justify-between items-center bg-gray-900/40 px-3 py-1.5 rounded-lg text-sm">
                                    <span class="text-gray-400">Pressione:</span>
                                    <span class="font-bold text-blue-400">${item.pressione ? item.pressione + ' mmHg' : '--'}</span>
                                </div>
                                <div class="flex justify-between items-center bg-gray-900/40 px-3 py-1.5 rounded-lg text-sm">
                                    <span class="text-gray-400">Saturazione:</span>
                                    <span class="font-bold text-green-400">${item.saturazione ? item.saturazione + ' %' : '--'}</span>
                                </div>
                            </div>
                        </div>
                    `;
            container.appendChild(card);
        });

    } catch (error) {
        console.error(error);
        container.innerHTML = "<p class='text-red-400 col-span-2 text-center py-4'>Errore durante il caricamento dello storico.</p>";
    }
}