# 🫀 MonitoraggioParametri

<p align="center">
  <img src="frontend/assets/DatiCuore.png" alt="Project Logo" width="120" height="120">
</p>

<p align="center">
  <strong>A private, minimalist, and exclusive biometric log for tracking vital parameters.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Frontend-Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/Hosting-Render_%26_GitHub_Pages-black?style=for-the-badge" alt="Hosting">
</p>

---

## 🖤 Overview

**MonitoraggioParametri** is a responsive and encrypted web app born from the need to have a personal, secure clinical diary accessible only to its owner. The system is protected by an **OAuth2 with JWT** authentication wall, securing data saved on a remote relational database to prevent any unauthorized read or write operations.

The interface features a sleek, refined dark design, optimized with a *mobile-first* approach for quick and immediate viewing on both desktops and smartphones.

---

## 🚀 Technical Architecture

The project is structured following a decoupled services model (Decoupled Architecture) at zero management cost:

* **Frontend**: Static interface hosted on **GitHub Pages**, built with HTML5 and **Tailwind CSS**, featuring asynchronous state management via native JavaScript (`Fetch API`).
* **Backend**: High-performance RESTful API developed in Python using **FastAPI**, deployed on **Render**.
* **Database**: Serverless cloud **PostgreSQL** instance hosted on the **Neon** platform.

---

## 🔒 Key Features & Security

* **Authentication Gate**: Secure login via url-encoded form. No public registration form; credentials are immutable and managed directly by the server owner.
* **Bcrypt Encryption**: Passwords are verified at a low level using native hashing steps, without plaintext storage.
* **Timed Sessions**: Generation of cryptographic **JWT (HS256)** tokens with an automatic expiration set to 120 minutes to prevent session hijacking.
* **Mobile-First Layout**: Advanced adaptive grids (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`) that transform the history log from side-by-side cards on PC to a clean, ergonomic vertical feed on smaller screens.

---

## 🛠️ Tech Stack

### Backend
* **Python 3.12**
* **FastAPI** (Routing, dependencies, and validation)
* **Psycopg 3** (Native and high-performance PostgreSQL driver)
* **Python-Jose** & **Bcrypt** (Token management and cryptographic hashing)

### Frontend
* **HTML5** & **JavaScript ES6+**
* **Tailwind CSS** (Interface via CDN)
* **LocalStorage API** (Secure storage of the Bearer Token on the client)

---

## 📦 Repository Structure

```text
├── backend/
│   ├── main.py               # Core logic, API routes, and security middleware
│   ├── requirements.txt      # Required Python dependencies for the server
│   └── .env                  # Local environment variables (Database and JWT)
└── frontend/
    ├── index.html            # Login screen (GitHub Pages entry point)
    ├── dashboard.html        # Private dashboard with form and card history
    ├── login.js              # Form submission handling and JWT token storage
    ├── app.js                # Token interception, protected fetches, and dynamic rendering
    └── assets/
        └── DatiCuore.png     # Official application icon