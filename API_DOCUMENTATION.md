# Transport Platform API Documentation

Base URL: `http://127.0.0.1:8000`

All authenticated endpoints require the following header:
```
Authorization: Token <your_token>
Content-Type: application/json
```

---

## Table of Contents

- [Authentication](#authentication)
- [Users](#users)
- [Trajets](#trajets)
- [Reservations](#reservations)
- [Paiements](#paiements)
- [Notifications](#notifications)
- [Vehicules](#vehicules)
- [Transports](#transports)

---

## Authentication

### Register
**POST** `/users/register/`

Register a new user (passager, transporteur, or admin).

**Request Body (passager)**
```json
{
  "username": "jean_dupont",
  "email": "jean@example.com",
  "password": "Test1234!",
  "password_confirm": "Test1234!",
  "nom": "Dupont",
  "prenom": "Jean",
  "role": "passager",
  "telephone": "+33600000001"
}
```

**Request Body (transporteur)** — requires additional fields:
```json
{
  "username": "transport_sarl",
  "email": "transport@example.com",
  "password": "Test1234!",
  "password_confirm": "Test1234!",
  "nom": "Martin",
  "prenom": "Paul",
  "role": "transporteur",
  "telephone": "+33600000002",
  "nom_entreprise": "Transport SARL",
  "numero_licence": "LIC-2024-001"
}
```

**Response** `201 Created`
```json
{
  "user": {
    "id": 1,
    "username": "jean_dupont",
    "email": "jean@example.com",
    "nom": "Dupont",
    "prenom": "Jean",
    "role": "passager",
    "telephone": "+33600000001",
    "is_verified": false,
    "is_actif": true
  },
  "token": "dddcb8db9a3d76f95c61e56ec120bf5ecaf7402d"
}
```

---

### Login
**POST** `/users/login/`

Authenticate and retrieve a token.

**Request Body**
```json
{
  "email": "jean@example.com",
  "password": "Test1234!"
}
```

**Response** `200 OK`
```json
{
  "token": "dddcb8db9a3d76f95c61e56ec120bf5ecaf7402d",
  "user_id": 1,
  "email": "jean@example.com",
  "nom": "Dupont",
  "prenom": "Jean",
  "role": "passager"
}
```

---

### Logout
**POST** `/users/logout/`

Invalidate the current token.

**Response** `200 OK`
```json
{
  "message": "Déconnexion réussie"
}
```

---

### Get Profile
**GET** `/users/me/`

Returns the authenticated user's profile.

**Response** `200 OK`
```json
{
  "id": 1,
  "username": "jean_dupont",
  "email": "jean@example.com",
  "nom": "Dupont",
  "prenom": "Jean",
  "role": "passager",
  "telephone": "+33600000001",
  "is_verified": false,
  "is_actif": true
}
```

---

### Change Password
**POST** `/users/change-password/`

**Request Body**
```json
{
  "old_password": "Test1234!",
  "new_password": "NewPass5678!",
  "new_password_confirm": "NewPass5678!"
}
```

**Response** `200 OK`
```json
{
  "message": "Mot de passe modifié avec succès"
}
```

---

## Users

### List Users *(admin only)*
**GET** `/users/`

**Response** `200 OK`
```json
{
  "count": 4,
  "results": [
    {
      "id": 1,
      "username": "jean_dupont",
      "email": "jean@example.com",
      "role": "passager"
    }
  ]
}
```

---

### Get User
**GET** `/users/{id}/`

**Response** `200 OK`
```json
{
  "id": 1,
  "username": "jean_dupont",
  "email": "jean@example.com",
  "nom": "Dupont",
  "prenom": "Jean",
  "role": "passager"
}
```

---

### Activate User *(admin only)*
**POST** `/users/{id}/activate/`

**Response** `200 OK`
```json
{
  "message": "Utilisateur activé avec succès"
}
```

---

### Deactivate User *(admin only)*
**POST** `/users/{id}/deactivate/`

**Response** `200 OK`
```json
{
  "message": "Utilisateur désactivé avec succès"
}
```

---

### Verify User *(admin only)*
**POST** `/users/verify/{id}/`

**Response** `200 OK`
```json
{
  "message": "Utilisateur vérifié avec succès"
}
```

---

## Trajets

### List Trajets
**GET** `/trajets/trajets/`

Returns active upcoming trips. Supports query params: `?depart=Paris&destination=Lyon&date=2026-04-15`

**Response** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "depart": "Paris",
      "destination": "Lyon",
      "date_depart": "2026-04-15T08:00:00Z",
      "places_disponibles": 18,
      "places_totales": 20,
      "prix_base": "35.00",
      "statut": "actif"
    }
  ]
}
```

---

### Create Trajet *(transporteur)*
**POST** `/trajets/trajets/`

**Request Body**
```json
{
  "depart": "Paris",
  "destination": "Lyon",
  "date_depart": "2026-04-15T08:00:00Z",
  "date_arrivee_estimee": "2026-04-15T12:00:00Z",
  "places_totales": 20,
  "places_disponibles": 20,
  "prix_base": "35.00",
  "distance_km": 465,
  "description": "Trajet direct Paris-Lyon"
}
```

**Response** `201 Created`
```json
{
  "id": 1,
  "transporteur": 3,
  "depart": "Paris",
  "destination": "Lyon",
  "date_depart": "2026-04-15T08:00:00Z",
  "places_totales": 20,
  "places_disponibles": 20,
  "prix_base": "35.00",
  "statut": "actif"
}
```

---

### Get Trajet
**GET** `/trajets/trajets/{id}/`

**Response** `200 OK` — full trajet object with etapes and transporteur details.

---

### Update Trajet *(transporteur)*
**PATCH** `/trajets/trajets/{id}/`

**Request Body**
```json
{
  "prix_base": "40.00",
  "description": "Trajet mis à jour"
}
```

**Response** `200 OK`

---

### Delete Trajet *(transporteur)*
**DELETE** `/trajets/trajets/{id}/`

**Response** `204 No Content`

---

### Search Trajets
**GET** `/trajets/rechercher/?depart=Paris&destination=Lyon`

**Response** `200 OK` — list of matching active trips with available seats.

---

### Check Available Seats
**GET** `/trajets/trajets/{id}/places/`

**Response** `200 OK`
```json
{
  "places_disponibles": 18,
  "places_totales": 20,
  "taux_remplissage": 10.0
}
```

---

### Trajets by Transporteur
**GET** `/trajets/transporteur/{transporteur_id}/trajets/`

**Response** `200 OK` — list of trips for the given transporteur.

---

### Add Etape
**POST** `/trajets/etapes/`

**Request Body**
```json
{
  "trajet": 1,
  "lieu": "Mâcon",
  "heure_prevue": "2026-04-15T10:00:00Z",
  "ordre": 1
}
```

**Response** `201 Created`

---

## Reservations

### Create Reservation *(passager)*
**POST** `/reservations/creer/`

**Request Body**
```json
{
  "trajet": 1,
  "nombre_places": 2,
  "numero_siege": "A1"
}
```

**Response** `201 Created`
```json
{
  "id": 1,
  "passager": 4,
  "trajet": 1,
  "nombre_places": 2,
  "prix_total": "70.00",
  "statut": "confirmee",
  "date_reservation": "2026-03-28T20:00:00Z"
}
```

---

### My Reservations *(passager)*
**GET** `/reservations/mes-reservations/`

**Response** `200 OK` — list of the authenticated passager's reservations.

---

### List All Reservations
**GET** `/reservations/reservations/`

**Response** `200 OK` — filtered by role (admin sees all, passager sees own, transporteur sees their trips).

---

### Get Reservation
**GET** `/reservations/reservations/{id}/`

**Response** `200 OK` — full reservation object.

---

### Update Reservation
**PATCH** `/reservations/reservations/{id}/`

**Request Body**
```json
{
  "numero_siege": "B3"
}
```

**Response** `200 OK`

---

### Confirm Reservation
**POST** `/reservations/reservations/{id}/confirmer/`

**Response** `200 OK`
```json
{
  "message": "Réservation confirmée"
}
```

---

### Cancel Reservation
**POST** `/reservations/reservations/{id}/annuler/`

**Response** `200 OK`
```json
{
  "message": "Réservation annulée"
}
```

---

### Mark Passenger Picked Up *(transporteur)*
**POST** `/reservations/reservations/{id}/recupere/`

**Response** `200 OK`
```json
{
  "message": "Passager marqué comme récupéré"
}
```

---

### Generate Ticket
**POST** `/reservations/reservations/{id}/generer-billet/`

**Response** `201 Created`
```json
{
  "id": 1,
  "code_qr": "2ec04bacb0b1468b806e",
  "date_emission": "2026-03-28T21:00:00Z"
}
```

---

### Get Ticket by QR Code
**GET** `/reservations/billets/qr/{code_qr}/`

**Response** `200 OK` — returns PNG image of the QR code.

---

### Set Pickup Point
**POST** `/reservations/reservations/{id}/point-ramassage/`

**Request Body**
```json
{
  "adresse": "12 rue de la Paix, Paris",
  "latitude": "48.869000",
  "longitude": "2.330000",
  "instructions": "Devant la pharmacie"
}
```

**Response** `201 Created`

---

### Delete Reservation *(admin)*
**DELETE** `/reservations/reservations/{id}/`

**Response** `204 No Content`

---

## Paiements

### Initiate Payment *(passager)*
**POST** `/paiements/initier/`

**Request Body**
```json
{
  "reservation": 1,
  "methode": "mobile_money",
  "montant": "70.00"
}
```

Available methods: `carte`, `mobile_money`, `paypal`, `especes`

**Response** `201 Created`
```json
{
  "paiement": {
    "id": 1,
    "montant": "70.00",
    "methode": "mobile_money",
    "statut": "en_cours"
  },
  "transaction_id": "1c9fea11c3f94aa798d5"
}
```

---

### Confirm Payment
**POST** `/paiements/confirmer/{transaction_id}/`

**Request Body**
```json
{
  "statut": "success"
}
```

**Response** `200 OK`
```json
{
  "message": "Paiement réussi",
  "statut": "reussi"
}
```

---

### Check Payment Status
**GET** `/paiements/verifier/{id}/`

**Response** `200 OK`
```json
{
  "id": 1,
  "montant": "70.00",
  "methode": "mobile_money",
  "statut": "reussi",
  "date_validation": "2026-03-28T21:00:00Z"
}
```

---

### Refund Payment *(admin)*
**POST** `/paiements/rembourser/{id}/`

**Response** `200 OK`
```json
{
  "message": "Paiement remboursé"
}
```

---

### List Payments
**GET** `/paiements/paiements/`

**Response** `200 OK` — filtered by role.

---

### List Transaction Logs *(admin)*
**GET** `/paiements/logs/`

Optional filter: `?paiement=1`

**Response** `200 OK`
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "action": "initier",
      "statut": "en_cours",
      "message": "Paiement initié",
      "date_creation": "2026-03-28T21:00:00Z"
    }
  ]
}
```

---

## Notifications

### My Notifications
**GET** `/notifications/mes-notifications/`

**Response** `200 OK`
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "type": "confirmation",
      "titre": "Réservation confirmée",
      "message": "Votre réservation #1 a été confirmée.",
      "est_lu": false,
      "date_creation": "2026-03-28T21:00:00Z"
    }
  ]
}
```

---

### Unread Notifications
**GET** `/notifications/non-lues/`

**Response** `200 OK` — list of unread notifications.

---

### Count Unread
**GET** `/notifications/compter/`

**Response** `200 OK`
```json
{
  "count": 2
}
```

---

### Mark as Read
**PATCH** `/notifications/marquer/{id}/`

**Response** `200 OK`
```json
{
  "message": "Notification marquée comme lue"
}
```

---

### Mark All as Read
**POST** `/notifications/marquer-lues/`

**Response** `200 OK`
```json
{
  "message": "Toutes les notifications ont été marquées comme lues"
}
```

---

### Delete Notification
**DELETE** `/notifications/supprimer/{id}/`

**Response** `200 OK`
```json
{
  "message": "Notification supprimée"
}
```

---

### Delete All Notifications
**DELETE** `/notifications/supprimer-toutes/`

**Response** `200 OK`

---

### Create Notification *(admin)*
**POST** `/notifications/creer/`

**Request Body**
```json
{
  "utilisateur": 4,
  "type": "info",
  "titre": "Bienvenue",
  "message": "Votre compte a été créé avec succès."
}
```

Available types: `info`, `confirmation`, `annulation`, `rappel`, `depart_imminent`, `paiement`

**Response** `201 Created`

---

### Notify Trip Passengers *(transporteur)*
**POST** `/notifications/trajet/{trajet_id}/notifier/`

**Request Body**
```json
{
  "message": "Votre trajet démarre dans 30 minutes."
}
```

**Response** `200 OK`
```json
{
  "message": "Passagers notifiés",
  "count": 5
}
```

---

## Vehicules

### List Marques
**GET** `/vehicules/marques/`

**Response** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "nom": "Toyota",
      "nombre_modeles": 2
    }
  ]
}
```

---

### Create Marque *(admin)*
**POST** `/vehicules/marques/`

**Request Body**
```json
{
  "nom": "Toyota"
}
```

**Response** `201 Created`

---

### List Modeles
**GET** `/vehicules/modeles/`

Optional filter: `?marque=1`

**Response** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "marque": 1,
      "marque_nom": "Toyota",
      "nom": "Hiace",
      "nombre_places": 15
    }
  ]
}
```

---

### Create Modele *(admin)*
**POST** `/vehicules/modeles/`

**Request Body**
```json
{
  "marque": 1,
  "nom": "Hiace",
  "nombre_places": 15
}
```

**Response** `201 Created`

---

### List Vehicules *(transporteur)*
**GET** `/vehicules/vehicules/`

**Response** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "modele": 1,
      "immatriculation": "DK-1234-AB",
      "couleur": "Blanc",
      "annee": 2022,
      "disponible": true,
      "en_maintenance": false,
      "climatisation": true,
      "wifi": false
    }
  ]
}
```

---

### Create Vehicule *(transporteur)*
**POST** `/vehicules/vehicules/`

**Request Body**
```json
{
  "modele": 1,
  "immatriculation": "DK-1234-AB",
  "couleur": "Blanc",
  "annee": 2022,
  "climatisation": true,
  "wifi": false,
  "prise_usb": true,
  "espace_bagages": "Grand coffre"
}
```

**Response** `201 Created`

---

### Update Vehicule *(transporteur)*
**PATCH** `/vehicules/vehicules/{id}/`

**Request Body**
```json
{
  "couleur": "Gris",
  "wifi": true
}
```

**Response** `200 OK`

---

### Delete Vehicule *(transporteur)*
**DELETE** `/vehicules/vehicules/{id}/`

**Response** `204 No Content`

---

### Set Vehicule Available
**POST** `/vehicules/vehicules/{id}/disponible/`

**Response** `200 OK`
```json
{
  "message": "Véhicule disponible"
}
```

---

### Set Vehicule in Maintenance
**POST** `/vehicules/vehicules/{id}/maintenance/`

**Response** `200 OK`
```json
{
  "message": "Véhicule en maintenance"
}
```

---

### Vehicules by Transporteur
**GET** `/vehicules/transporteur/{transporteur_id}/vehicules/`

**Response** `200 OK` — list of vehicles for the given transporteur.

---

## Transports

### List Transports
**GET** `/transports/transports/`

**Response** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "nom": "Bus Express Dakar",
      "type": "Bus",
      "plaque_immatriculation": "DK-5678-CD",
      "capacite": 50,
      "status": "disponible",
      "date_creation": "2026-03-28T21:00:00Z"
    }
  ]
}
```

---

### Create Transport
**POST** `/transports/transports/`

**Request Body**
```json
{
  "nom": "Bus Express Dakar",
  "type": "Bus",
  "plaque_immatriculation": "DK-5678-CD",
  "capacite": 50,
  "status": "disponible"
}
```

**Response** `201 Created`

---

### Get Transport
**GET** `/transports/transports/{id}/`

**Response** `200 OK`

---

### Update Transport
**PATCH** `/transports/transports/{id}/`

**Request Body**
```json
{
  "capacite": 45,
  "nom": "Bus Express Dakar-Thiès"
}
```

**Response** `200 OK`

---

### Delete Transport
**DELETE** `/transports/transports/{id}/`

**Response** `204 No Content`

---

### List Available Transports
**GET** `/transports/transports/disponibles/`

**Response** `200 OK` — list of transports with `status: disponible`.

---

### Change Transport Status
**POST** `/transports/transports/{id}/changer_status/`

**Request Body**
```json
{
  "status": "en_cours"
}
```

Available statuses: `disponible`, `en_cours`, `maintenance`

**Response** `200 OK`
```json
{
  "id": 1,
  "nom": "Bus Express Dakar",
  "status": "en_cours"
}
```

---

## Error Responses

| Code | Description |
|------|-------------|
| `400` | Bad Request — validation error |
| `401` | Unauthorized — missing or invalid token |
| `403` | Forbidden — insufficient permissions |
| `404` | Not Found — resource does not exist |
| `500` | Internal Server Error |

**Example error response:**
```json
{
  "error": "Email ou mot de passe incorrect",
  "status_code": 401
}
```

---

## Interactive Documentation

Swagger UI is available at:
```
http://127.0.0.1:8000/api/docs/
```

OpenAPI schema:
```
http://127.0.0.1:8000/api/schema/
```
