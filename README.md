# 🫀 DatiCuoreAPI & MonitoraggioParametri

<p align="center">
  <img src="frontend/assets/DatiCuore.png" alt="Logo Progetto" width="120" height="120">
</p>

<p align="center">
  <strong>Un registro biometrico privato, minimale ed esclusivo per il tracciamento dei parametri vitali.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Frontend-Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/Hosting-Render_%26_GitHub_Pages-black?style=for-the-badge" alt="Hosting">
</p>

---

## 🖤 Overview

**MonitoraggioParametri** è una web app responsive e cifrata nata dall'esigenza di avere un diario clinico personale, sicuro e accessibile solo al proprietario. Il sistema è protetto da un muro di autenticazione **OAuth2 con JWT**, che blinda i dati salvati su un database relazionale remoto impedendo qualsiasi tipo di lettura o scrittura non autorizzata.

L'interfaccia adotta un design scuro e raffinato, ottimizzato con un approccio *mobile-first* per una consultazione rapida e immediata sia da desktop che da smartphone.

---

## 🚀 Architettura Tecnica

Il progetto è strutturato seguendo un modello a servizi disaccoppiati (Decoupled Architecture) a costo zero di gestione:

* **Frontend**: Interfaccia statica ospitata su **GitHub Pages**, costruita in HTML5 e **Tailwind CSS**, con gestione asincrona degli stati tramite JavaScript nativo (`Fetch API`).
* **Backend**: API RESTful ad altissime prestazioni sviluppata in Python con **FastAPI**, deployata su **Render**.
* **Database**: Istanza cloud serverless **PostgreSQL** ospitata sulla piattaforma **Neon**.

---

## 🔒 Funzionalità Chiave & Sicurezza

* **Gate di Autenticazione**: Accesso protetto tramite form url-encoded. Nessun form di registrazione pubblico; le credenziali sono immutabili e gestite dal proprietario del server.
* **Criptazione Bcrypt**: Le password vengono verificate a basso livello tramite passaggi hash nativi, senza memorizzazione in chiaro.
* **Sessioni Temporizzate**: Generazione di token crittografici **JWT (HS256)** con scadenza automatica impostata a 120 minuti per impedire il dirottamento della sessione.
* **Layout Mobile-First**: Griglie adattive avanzate (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`) che trasformano lo storico da card affiancate su PC a un feed verticale pulito ed ergonomico su display ridotti.

---

## 🛠️ Stack Tecnologico

### Backend
* **Python 3.12**
* **FastAPI** (Routing, dipendenze e validazione)
* **Psycopg 3** (Driver PostgreSQL nativo e performante)
* **Python-Jose** & **Bcrypt** (Gestione dei token e hashing crittografico)

### Frontend
* **HTML5** & **JavaScript ES6+**
* **Tailwind CSS** (Interfaccia via CDN)
* **LocalStorage API** (Persistenza sicura del Bearer Token sul client)

---

## 📦 Struttura della Repository

```text
├── backend/
│   ├── main.py               # Logica core, rotte API e middleware di sicurezza
│   ├── requirements.txt      # Dipendenze Python necessarie per il server
│   └── .env                  # Variabili d'ambiente locali (Database e JWT)
└── frontend/
    ├── index.html            # Schermata di Login (Punto d'accesso di GitHub Pages)
    ├── dashboard.html        # Pannello privato con form e storico card
    ├── login.js              # Gestione sottomissione form e archiviazione token JWT
    ├── app.js                # Intercettazione token, fetch protette e rendering dinamico
    └── assets/
        └── DatiCuore.png     # Icona ufficiale dell'applicazione