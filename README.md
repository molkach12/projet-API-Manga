# 📌 Projet FastAPI — API de Gestion de Personnages (Projet Fil Rouge)

Ce projet est une application développée avec **FastAPI**, simulant une API REST complète pour gérer des personnages fictifs issus de différents univers. Elle comprend des fonctionnalités avancées (authentification, dashboard HTML, base de données, logs) et respecte les principes d’un mini pipeline ETL.

---

## 📁 Structure du projet (par étapes)

```
projet_fil_rouge/
│
├── etape1_etl/                         # Extraction et transformation de données
│   ├── exercice3.py                    # Script ETL : extraction API, transformation, sauvegarde
│   ├── donnees_filtrees_chat.json      # Données filtrées (JSON)
│   └── partie1.pdf                     # Enoncé de l’étape ou support
│
├── etape2_webhook_envoi/              # Simulation d’envoi d’événements vers l'API
│   ├── ex4.py                          # Script d'envoi des personnages (POST)
│   └── webhook_log.json               # Log JSON des événements reçus
│
├── etape3_bdd_fastapi/                # API sans JWT, simple enregistrement
│   └── main.py                         # Version initiale de FastAPI
│
├── etape4_dashboard_html/             # API complète avec base, dashboard, JWT
│   ├── mainp3.py                       # Version principale avec sécurité + dashboard
│   ├── index.p2.html                   # Page HTML d’affichage (fetch API)
│   └── tp.p1.html                      # Test HTML avec CORS/token
│
├── etape5_auth_jwt/                   # Réenvoi des données avec sécurité
│   └── retraitement.py                 # Re-traitement du JSON → API
│
├── donnees/                           # Données communes
│   └── webhook_log.json                # Copie centrale (optionnel)
│
├── Projet fil rouge.pdf               # Sujet officiel fourni
└── README.md                          # Fichier d'explication (ce fichier)
```

---

## 🧩 Fonctionnalités réalisées

### ✅ Étape 1 — Mini ETL (extraction + transformation)
- Récupération des données depuis une API paginée (ProPublica)
- Filtrage des données : uniquement celles avec une `city`
- Calcul de la moyenne d’un champ `income_amount`
- Sauvegarde dans un fichier JSON filtré (`donnees_filtrees_chat.json`)

### ✅ Étape 2 — Envoi automatique de données
- Simulation d’un appel `POST /webhook/personnage` avec Python (module `requests`)
- Ajout automatique du champ `niveau` basé sur le score
- Sauvegarde dans un fichier `webhook_log.json`

### ✅ Étape 3 — FastAPI sans sécurité
- Création d’une API `POST /webhook/personnage`
- Enregistrement des données dans un fichier JSON

### ✅ Étape 4 — FastAPI avec Base de Données et Dashboard
- Connexion à une base SQLite via SQLAlchemy
- Ajout de `uuid` pour chaque personnage
- Route `/dashboard` → HTML dynamique affichant les personnages
- Route `/personnage/{id}` → récupération directe depuis la base

### ✅ Étape 5 — Authentification sécurisée (JWT)
- Route `/login` qui retourne un `access_token`
- Utilisation de `Depends(get_current_user)` pour protéger les routes (`/dashboard`, `/webhook/personnage`, etc.)

### ✅ Bonus réalisés :
- 🔐 Authentification sécurisée avec JWT
- 🛢️ Enregistrement en base SQLite
- 🧠 Enrichissement automatique (niveau)
- 📊 Dashboard HTML dynamique avec CSS
- 🔁 Simulation de push automatique (`ex4.py`)
- 🧾 Logs JSON des données reçues
- 🆔 Identifiants UUID uniques
- 🧪 Gestion des erreurs API (timeout, retry, status)

---

## 👤 Utilisateur pour les tests
```
username : mikou
password : mikou
```

Token JWT requis pour `/webhook/personnage`, `/dashboard`, `/personnage/{id}`.

---

## 🚀 Pour lancer le projet

```bash
uvicorn etape4_dashboard_html.mainp3:app --reload
```

Puis tester sur Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📎 Auteur : Molka Chakchouk – EPSI M1 Ingénierie des Données
Projet pédagogique "Fil Rouge" – Année 2024/2025
