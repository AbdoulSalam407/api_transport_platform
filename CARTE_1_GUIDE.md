# Transport Platform API - Configuration DRF

## ✅ Configuration complétée

### 1. Installation Django REST Framework

- Django REST Framework ajouté à `INSTALLED_APPS` dans `settings.py`

### 2. Configuration Settings.py

- ✅ `rest_framework` ajouté aux apps installées
- ✅ `transports` app créée et ajoutée
- ✅ Configuration REST_FRAMEWORK ajoutée:
  - Pagination par défaut (10 éléments par page)
  - Support du tri et de la recherche

### 3. Création de l'API Transports

- ✅ Modèle `Transport` avec champs:
  - nom, type, plaque_immatriculation, capacité
  - statuts: disponible, en_cours, maintenance
  - timestamps: date_creation, date_modification

- ✅ Serializer DRF pour le modèle Transport

- ✅ ViewSet complet avec:
  - Actions CRUD standard
  - Endpoint personnalisé `/transports/disponibles/` pour lister les transports disponibles
  - Endpoint personnalisé `POST /transports/{id}/changer_status/` pour changer le statut

- ✅ Admin interface configurée
- ✅ Tests unitaires inclus

## 📝 Commandes d'utilisation

### 1. Faire les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Lancer le serveur de développement

```bash
python manage.py runserver
```

### 3. Accéder aux endpoints de l'API

#### Liste des transports (avec pagination)

```
GET http://localhost:8000/api/transports/
```

#### Créer un transport

```
POST http://localhost:8000/api/transports/
Content-Type: application/json

{
  "nom": "Bus 101",
  "type": "Bus",
  "plaque_immatriculation": "ABC123",
  "capacite": 50,
  "status": "disponible"
}
```

#### Récupérer un transport spécifique

```
GET http://localhost:8000/api/transports/{id}/
```

#### Mettre à jour un transport

```
PUT http://localhost:8000/api/transports/{id}/
PATCH http://localhost:8000/api/transports/{id}/
```

#### Supprimer un transport

```
DELETE http://localhost:8000/api/transports/{id}/
```

#### Lister les transports disponibles

```
GET http://localhost:8000/api/transports/disponibles/
```

#### Changer le statut d'un transport

```
POST http://localhost:8000/api/transports/{id}/changer_status/
Content-Type: application/json

{
  "status": "en_cours"
}
```

### 4. Interface d'administration

```
http://localhost:8000/admin/
```

### 5. Documentation API (si coreapi est installé)

```
http://localhost:8000/api/docs/
```

## 🧪 Tester avec curl ou Postman

### Exemple avec curl - Créer un transport

```bash
curl -X POST http://localhost:8000/api/transports/ \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Taxi 001",
    "type": "Taxi",
    "plaque_immatriculation": "XYZ789",
    "capacite": 4,
    "status": "disponible"
  }'
```

### Exemple avec curl - Récupérer les transports

```bash
curl http://localhost:8000/api/transports/
```

### Exemple avec curl - Changer le statut

```bash
curl -X POST http://localhost:8000/api/transports/1/changer_status/ \
  -H "Content-Type: application/json" \
  -d '{"status": "en_cours"}'
```

## 📦 Structure du projet

```
api_transport_platform/
├── api_transport_platform/
│   ├── settings.py         # Configuration avec DRF
│   ├── urls.py            # URLs configurées
│   └── ...
├── transports/            # App créée
│   ├── models.py          # Modèle Transport
│   ├── serializers.py     # Serializer DRF
│   ├── views.py           # ViewSet DRF
│   ├── urls.py            # Routes de l'app
│   ├── admin.py           # Admin interface
│   ├── tests.py           # Tests
│   └── ...
└── manage.py
```

## 🚀 Prochaines étapes

1. Exécuter les migrations pour créer la base de données
2. Créer un utilisateur admin pour accéder à l'interface admin
3. Tester les endpoints avec curl, Postman ou l'interface web
4. Enrichir les modèles et serializers selon vos besoins
5. Ajouter l'authentification et les permissions

---

Carte 1 : Installation et configuration de Django REST Framework ✅ COMPLÉTÉE
