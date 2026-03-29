# Transport API (`transport_api`)

API REST Django pour une plateforme de réservation de transport : utilisateurs (passagers / transporteurs), véhicules, trajets, réservations, paiements et notifications. Authentification **JWT** via `djangorestframework-simplejwt`.

## Structure du projet

```
transport_api/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── transport_api/          # configuration Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/
├── vehicules/
├── trajets/
├── reservations/
├── paiements/
└── notifications/
```

## Installation

```bash
cd transport_api
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optionnel (admin Django + validation paiements)
python manage.py runserver
```

Base **SQLite** par défaut (`db.sqlite3`). Pour **PostgreSQL**, définir les variables d’environnement (voir `.env.example`) :

- `USE_POSTGRESQL=True`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

## Authentification JWT

Toutes les routes sous `/api/...` (sauf inscription, login et refresh) attendent un en-tête :

```http
Authorization: Bearer <access_token>
```

### `POST /api/auth/register/`

Inscription. Le mot de passe est envoyé sous le nom **`mot_de_passe`** ; il est stocké comme champ sécurisé standard Django (`password`).

| Champ | Type | Description |
|--------|------|-------------|
| `email` | string | Obligatoire, unique |
| `username` | string | Obligatoire (peut être identique à l’email) |
| `nom`, `prenom` | string | Obligatoire |
| `role` | string | `PASSAGER` ou `TRANSPORTEUR` |
| `telephone` | string | Obligatoire si `role=PASSAGER` |
| `nom_compagnie`, `licence` | string | Obligatoires si `role=TRANSPORTEUR` |

**Exemple de requête (Postman) — passager**

```json
{
  "email": "passager@example.com",
  "username": "passager1",
  "nom": "Diallo",
  "prenom": "Amadou",
  "role": "PASSAGER",
  "telephone": "+221771234567",
  "mot_de_passe": "secretpass123"
}
```

**Réponse (201)**

```json
{
  "id": 1,
  "username": "passager1",
  "email": "passager@example.com",
  "nom": "Diallo",
  "prenom": "Amadou",
  "role": "PASSAGER",
  "passager": { "telephone": "+221771234567" },
  "transporteur": null
}
```

### `POST /api/auth/login/`

Obtain pair JWT. Django utilise `USER_MODEL.USERNAME_FIELD` = **email** : le corps envoie **`email`** et **`password`** (clé `password`, pas `mot_de_passe`).

**Requête**

```json
{
  "email": "passager@example.com",
  "password": "secretpass123"
}
```

**Réponse (200)**

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### `POST /api/auth/refresh/`

**Requête**

```json
{
  "refresh": "<refresh_token>"
}
```

**Réponse (200)**

```json
{
  "access": "<new_access_token>",
  "refresh": "<new_refresh_if_rotation>"
}
```

---

## Utilisateurs

### `GET /api/me/`

Profil de l’utilisateur connecté.

**Réponse (200)**

```json
{
  "id": 1,
  "username": "passager1",
  "email": "passager@example.com",
  "nom": "Diallo",
  "prenom": "Amadou",
  "role": "PASSAGER",
  "passager": { "telephone": "+221771234567" },
  "transporteur": null
}
```

### `GET /api/users/`

Liste des utilisateurs — **réservé au staff** (`is_staff` / superuser).

### `GET /api/users/{id}/`

Détail d’un utilisateur — authentifié.

---

## Véhicules

Règles : création / modification / suppression réservées au **transporteur** connecté (véhicule rattaché à son profil).

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/vehicules/` | Liste |
| `POST` | `/api/vehicules/` | Création |
| `GET` | `/api/vehicules/{id}/` | Détail |
| `PUT` | `/api/vehicules/{id}/` | Mise à jour complète |
| `PATCH` | `/api/vehicules/{id}/` | Mise à jour partielle |
| `DELETE` | `/api/vehicules/{id}/` | Suppression |

**POST /api/vehicules/** — corps exemple :

```json
{
  "immatriculation": "DK-1234-AB",
  "capacite": 18,
  "type": "BUS",
  "latitude": "14.7167",
  "longitude": "-17.4677"
}
```

Note : `transporteur` est **rempli côté serveur** à partir du compte transporteur.

**Réponse (201)**

```json
{
  "id": 1,
  "immatriculation": "DK-1234-AB",
  "capacite": 18,
  "type": "BUS",
  "latitude": "14.716700",
  "longitude": "-17.467700",
  "transporteur": 2
}
```

---

## Trajets

Filtres en query string : `ville_depart`, `ville_arrivee`, `date_depart` (YYYY-MM-DD), `statut`, `ordering` (`date_depart`, `-prix`, etc.).

Création / mise à jour / suppression : **transporteur** ; le véhicule doit lui appartenir.

| Méthode | Endpoint |
|---------|----------|
| `GET` | `/api/trajets/` |
| `POST` | `/api/trajets/` |
| `GET` | `/api/trajets/{id}/` |
| `PUT` / `PATCH` | `/api/trajets/{id}/` |
| `DELETE` | `/api/trajets/{id}/` |

**POST /api/trajets/** — exemple :

```json
{
  "ville_depart": "Dakar",
  "ville_arrivee": "Saint-Louis",
  "date_depart": "2026-04-15",
  "heure_depart": "08:00:00",
  "prix": "3500.00",
  "nombre_places_disponibles": 18,
  "statut": "ouvert",
  "vehicule": 1
}
```

**Réponse (201)** : objet trajet avec `transporteur` renseigné automatiquement.

---

## Réservations

- **Passager** : voit et crée **ses** réservations ; `passager` est fixé côté API.
- **Transporteur** : voit les réservations sur **ses** trajets.

| Méthode | Endpoint |
|---------|----------|
| `GET` | `/api/reservations/` |
| `POST` | `/api/reservations/` |
| `GET` | `/api/reservations/{id}/` |
| `PUT` / `PATCH` | `/api/reservations/{id}/` |
| `DELETE` | `/api/reservations/{id}/` |
| `POST` | `/api/reservations/{id}/annuler/` | Passe le statut à `annule` et libère les places si la réservation était `confirme` |

**POST /api/reservations/** — exemple :

```json
{
  "trajet": 1,
  "nombre_places": 2,
  "statut": "en_attente"
}
```

- Si `statut` = `confirme` à la création, les **places disponibles** du trajet sont décrémentées immédiatement (si suffisantes).
- Passage `en_attente` → `confirme` (PATCH) : décrémente les places.
- Annulation : voir route `annuler`.

**Réponse (201)**

```json
{
  "id": 1,
  "passager": 1,
  "trajet": 1,
  "nombre_places": 2,
  "date_reservation": "2026-03-28T12:00:00Z",
  "statut": "en_attente"
}
```

Une **notification** de type `reservation` est créée après création (signal Django).

---

## Paiements

- **Passager** : paie pour **ses** réservations ; le **montant** doit égaler `trajet.prix × nombre_places`.
- Après validation, la **réservation** passe en `confirme` si elle était `en_attente`, et une **notification** `paiement` est envoyée.

| Méthode | Endpoint |
|---------|----------|
| `GET` | `/api/paiements/` |
| `POST` | `/api/paiements/` |
| `GET` | `/api/paiements/{id}/` |
| `PUT` / `PATCH` | `/api/paiements/{id}/` |
| `DELETE` | `/api/paiements/{id}/` |
| `POST` | `/api/paiements/{id}/valider/` | Staff / superuser — validation « métier » |
| `POST` | `/api/paiements/{id}/marquer_valide/` | Démo pour tests (titulaire de la réservation) — **à remplacer par un webhook PSP en production** |

**POST /api/paiements/**

```json
{
  "reservation": 1,
  "montant": "7000.00",
  "methode": "carte"
}
```

**Réponse après validation (ex.)**

```json
{
  "id": 1,
  "reservation": 1,
  "montant": "7000.00",
  "methode": "carte",
  "statut": "valide",
  "date_paiement": "2026-03-28T12:05:00Z"
}
```

---

## Notifications

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/notifications/` | Notifications de l’utilisateur connecté |
| `GET` | `/api/notifications/{id}/` | Détail |

**Réponse liste (200)**

```json
[
  {
    "id": 1,
    "user": 1,
    "message": "Votre réservation #1 pour le trajet Dakar → Saint-Louis a été enregistrée (2 place(s)).",
    "type": "reservation",
    "date_envoi": "2026-03-28T12:00:00Z"
  }
]
```

---

## Récapitulatif des endpoints

| Domaine | Méthodes principales |
|---------|----------------------|
| Auth | `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/refresh/` |
| Profil | `GET /api/me/` |
| Users (admin) | `GET /api/users/` |
| Users | `GET /api/users/{id}/` |
| Véhicules | `GET/POST /api/vehicules/`, `GET/PUT/PATCH/DELETE /api/vehicules/{id}/` |
| Trajets | `GET/POST /api/trajets/`, `GET/PUT/PATCH/DELETE /api/trajets/{id}/` |
| Réservations | CRUD `/api/reservations/`, `POST .../annuler/` |
| Paiements | CRUD `/api/paiements/`, `POST .../valider/`, `POST .../marquer_valide/` |
| Notifications | `GET /api/notifications/` |

---

## Variables d’environnement (rappel)

Voir `.env.example`. **`SECRET_KEY`** doit être changée en production.

## Licence

Projet pédagogique / modèle — adaptez selon vos besoins.
