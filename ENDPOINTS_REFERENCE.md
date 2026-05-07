# 📡 API ENDPOINTS - POSTMAN COLLECTION

## Base URL

```
http://localhost:8000
```

## API Root

```
http://localhost:8000/api/v1/
```

---

## 🔐 AUTHENTICATION

### Get Token

```
POST http://localhost:8000/api-token-auth/

Headers:
Content-Type: application/json

Body (JSON):
{
  "username": "admin",
  "password": "your-password"
}

Response:
{
  "token": "abc123def456..."
}
```

### Use Token in Requests

```
Authorization: Token abc123def456
```

---

## 👥 USERS ENDPOINTS

### List All Users

```
GET http://localhost:8000/api/v1/users/users/

Headers:
Authorization: Token YOUR_TOKEN
```

### Create New User

```
POST http://localhost:8000/api/v1/users/users/

Headers:
Content-Type: application/json
Authorization: Token YOUR_TOKEN

Body:
{
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "Jean",
  "last_name": "Dupont",
  "phone_number": "+33612345678",
  "role": "client",
  "password": "securepass123",
  "password_confirm": "securepass123"
}
```

### Get My Profile

```
GET http://localhost:8000/api/v1/users/users/me/

Headers:
Authorization: Token YOUR_TOKEN
```

### Get User Detail

```
GET http://localhost:8000/api/v1/users/users/{id}/

Headers:
Authorization: Token YOUR_TOKEN
```

### Update User

```
PUT http://localhost:8000/api/v1/users/users/{id}/

Headers:
Content-Type: application/json
Authorization: Token YOUR_TOKEN

Body:
{
  "first_name": "Jean",
  "last_name": "Dupont",
  "bio": "Je suis un utilisateur",
  "phone_number": "+33612345678"
}
```

### Change Password

```
POST http://localhost:8000/api/v1/users/users/change_password/

Headers:
Content-Type: application/json
Authorization: Token YOUR_TOKEN

Body:
{
  "old_password": "current-password",
  "new_password": "new-secure-password"
}
```

---

## 🚗 VEHICULES ENDPOINTS

### List All Vehicles

```
GET http://localhost:8000/api/v1/vehicules/vehicules/

Headers:
Authorization: Token YOUR_TOKEN

Query Parameters:
?type_vehicule=bus
?status=disponible
?search=Toyota
?ordering=-date_creation
```

### Create Vehicle

```
POST http://localhost:8000/api/v1/vehicules/vehicules/

Headers:
Content-Type: application/json
Authorization: Token YOUR_TOKEN

Body:
{
  "marque": "Toyota",
  "modele": "Hiace",
  "plaque_immatriculation": "ABC123",
  "numero_chassis": "VIN123456",
  "type_vehicule": "minibus",
  "capacite": 14,
  "annee_fabrication": 2020,
  "couleur": "Blanc",
  "assurance_date_expiration": "2025-12-31",
  "controle_technique_date": "2025-06-30"
}
```

### Get Vehicle Detail

```
GET http://localhost:8000/api/v1/vehicules/vehicules/{id}/

Headers:
Authorization: Token YOUR_TOKEN
```

### Update Vehicle

```
PUT http://localhost:8000/api/v1/vehicules/vehicules/{id}/

Headers:
Content-Type: application/json
Authorization: Token YOUR_TOKEN

Body:
{
  "status": "maintenance",
  "kilometrage": 45000
}
```

### Delete Vehicle

```
DELETE http://localhost:8000/api/v1/vehicules/vehicules/{id}/

Headers:
Authorization: Token YOUR_TOKEN
```

---

## 🛣️ TRAJETS ENDPOINTS

### List All Routes

```
GET http://localhost:8000/api/v1/trajets/trajets/

Headers:
Authorization: Token YOUR_TOKEN

Query Parameters:
?status=planifie
?depart=Paris
?arrivee=Lyon
?search=Paris
```

### Get Available Routes Only

```
GET http://localhost:8000/api/v1/trajets/trajets/disponibles/

Headers:
Authorization: Token YOUR_TOKEN
```

### Create Route

```
POST http://localhost:8000/api/v1/trajets/trajets/

Headers:
Content-Type: application/json
Authorization: Token YOUR_TOKEN

Body:
{
  "vehicule": 1,
  "chauffeur": 2,
  "depart": "Paris",
  "arrivee": "Lyon",
  "distance_km": 463,
  "duree_estimee": "07:30:00",
  "date_depart": "2026-03-20T08:00:00Z",
  "prix_base": 45.00,
  "places_disponibles": 10,
  "places_totales": 14,
  "points_arret": ["Dijon", "Roanne"]
}
```

### Get Route Detail

```
GET http://localhost:8000/api/v1/trajets/trajets/{id}/

Headers:
Authorization: Token YOUR_TOKEN
```

### Update Route Status

```
PATCH http://localhost:8000/api/v1/trajets/trajets/{id}/

Headers:
Content-Type: application/json
Authorization: Token YOUR_TOKEN

Body:
{
  "status": "en_cours"
}
```

---

## 📋 RESERVATIONS ENDPOINTS

### List My Reservations

```
GET http://localhost:8000/api/v1/reservations/reservations/

Headers:
Authorization: Token YOUR_TOKEN

Query Parameters:
?status=confirmee
```

### Create Reservation

```
POST http://localhost:8000/api/v1/reservations/reservations/

Headers:
Content-Type: application/json
Authorization: Token YOUR_TOKEN

Body:
{
  "trajet": 1,
  "nombre_places": 2,
  "prix_total": 90.00,
  "notes": "Besoin d'une fenêtre"
}
```

### Get Reservation Detail

```
GET http://localhost:8000/api/v1/reservations/reservations/{id}/

Headers:
Authorization: Token YOUR_TOKEN
```

### Cancel Reservation

```
POST http://localhost:8000/api/v1/reservations/reservations/{id}/annuler/

Headers:
Authorization: Token YOUR_TOKEN
Content-Type: application/json

Body: {}
```

---

## 💳 PAIEMENTS ENDPOINTS

### List My Payments

```
GET http://localhost:8000/api/v1/paiements/paiements/

Headers:
Authorization: Token YOUR_TOKEN

Query Parameters:
?status=reussi
?methode_paiement=carte_bancaire
```

### Get Payment Detail

```
GET http://localhost:8000/api/v1/paiements/paiements/{id}/

Headers:
Authorization: Token YOUR_TOKEN
```

---

## 🔔 NOTIFICATIONS ENDPOINTS

### List My Notifications

```
GET http://localhost:8000/api/v1/notifications/notifications/

Headers:
Authorization: Token YOUR_TOKEN

Query Parameters:
?type_notification=reservation
?is_read=false
```

### Get Unread Notifications Only

```
GET http://localhost:8000/api/v1/notifications/notifications/non_lues/

Headers:
Authorization: Token YOUR_TOKEN
```

### Mark Notification as Read

```
POST http://localhost:8000/api/v1/notifications/notifications/{id}/marquer_comme_lue/

Headers:
Authorization: Token YOUR_TOKEN
Content-Type: application/json

Body: {}
```

### Mark All As Read

```
POST http://localhost:8000/api/v1/notifications/notifications/marquer_tous_comme_lus/

Headers:
Authorization: Token YOUR_TOKEN
Content-Type: application/json

Body: {}
```

---

## 🎭 TRANSPORTS (Existing App)

### List Transports

```
GET http://localhost:8000/api/v1/transports/transports/

Headers:
Authorization: Token YOUR_TOKEN
```

### Create Transport

```
POST http://localhost:8000/api/v1/transports/transports/

Headers:
Content-Type: application/json
Authorization: Token YOUR_TOKEN

Body:
{
  "nom": "Bus 101",
  "type": "Bus",
  "plaque_immatriculation": "ABC123",
  "capacite": 50,
  "status": "disponible"
}
```

### Get Available Transports

```
GET http://localhost:8000/api/v1/transports/transports/disponibles/

Headers:
Authorization: Token YOUR_TOKEN
```

### Change Transport Status

```
POST http://localhost:8000/api/v1/transports/transports/{id}/changer_status/

Headers:
Content-Type: application/json
Authorization: Token YOUR_TOKEN

Body:
{
  "status": "en_cours"
}
```

---

## 🔍 FILTERING & SEARCH EXAMPLES

### Search in Any App

```
GET http://localhost:8000/api/v1/trajets/trajets/?search=Paris

GET http://localhost:8000/api/v1/vehicules/vehicules/?search=Toyota
```

### Filter Results

```
GET http://localhost:8000/api/v1/trajets/trajets/?status=planifie

GET http://localhost:8000/api/v1/reservations/reservations/?status=payee

GET http://localhost:8000/api/v1/notifications/notifications/?type_notification=reservation&is_read=false
```

### Sort Results

```
GET http://localhost:8000/api/v1/trajets/trajets/?ordering=-date_depart

GET http://localhost:8000/api/v1/paiements/paiements/?ordering=montant
```

### Pagination

```
GET http://localhost:8000/api/v1/users/users/?page=1&page_size=20

GET http://localhost:8000/api/v1/trajets/trajets/?page=2
```

---

## 📊 COMMON RESPONSE CODES

| Code | Meaning                                   |
| ---- | ----------------------------------------- |
| 200  | ✅ OK - Success                           |
| 201  | ✅ Created - Resource created             |
| 204  | ✅ No Content - Success, no response body |
| 400  | ❌ Bad Request - Invalid data             |
| 401  | ❌ Unauthorized - Token missing/invalid   |
| 403  | ❌ Forbidden - Permission denied          |
| 404  | ❌ Not Found - Resource doesn't exist     |
| 429  | ❌ Too Many Requests - Rate limited       |
| 500  | ❌ Server Error - Django error            |

---

## 🛠️ POSTMAN SETUP GUIDE

### 1. Create Environment

- Variable Name: `base_url`
- Variable Value: `http://localhost:8000`
- Variable Name: `token`
- Variable Value: (leave empty, will be filled afterauthentication)

### 2. Get Token

1. Use Authenticate endpoint
2. Extract token from response
3. Set `token` environment variable

### 3. Use Token in Headers

```
Authorization: Token {{token}}
```

### 4. Authorization Tab Setup

- Type: Bearer Token
- Token: `{{token}}`

---

## 💡 USEFUL TIPS

### Test Complete Flow

1. Create user via signup
2. Get token via auth
3. Create vehicle
4. Create trajet
5. Create reservation
6. Create payment
7. Update status to completed
8. Check notifications

### Common Parameters

```
?page=1                           # Pagination
?page_size=50                     # Items per page
?search=keyword                   # Search
?ordering=-field                  # Sort (- for desc)
?status=value                     # Filter
?is_read=true&type_notification=reservation  # Multiple filters
```

---

**Note:** Replace `{id}` with actual resource IDs and `YOUR_TOKEN` with your authentication token.  
**Important:** Always include `Authorization` header with token for authenticated endpoints.

Happy Testing! 🚀
